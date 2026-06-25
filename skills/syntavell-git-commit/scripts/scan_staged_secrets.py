#!/usr/bin/env python3
"""Scan staged text content for common secrets and local-private material."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


SECRET_PATTERNS = {
    "github-token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "openai-key": re.compile(r"\b" + "sk" + r"-[A-Za-z0-9_-]{20,}\b"),
    "private-key": re.compile("BEGIN " + r"[A-Z ]*PRIVATE KEY"),
    "openai-env": re.compile("OPENAI" + r"_API_KEY", re.IGNORECASE),
    "anthropic-env": re.compile("ANTHROPIC" + r"_API_KEY", re.IGNORECASE),
    "gemini-env": re.compile("GEMINI" + r"_API_KEY", re.IGNORECASE),
    "aws-secret": re.compile("AWS" + r"_SECRET_ACCESS_KEY", re.IGNORECASE),
    "assignment-secret": re.compile(r"\b(password|secret|api[_-]?key|access[_-]?token)\s*=", re.IGNORECASE),
    "local-user-path": re.compile(r"(/Users/|/home/)[A-Za-z0-9._-]+/"),
}
TEXT_SUFFIXES = {
    "",
    ".c",
    ".cpp",
    ".css",
    ".html",
    ".json",
    ".js",
    ".jsx",
    ".lock",
    ".md",
    ".py",
    ".rs",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def run_git(args: list[str], cwd: Path, text: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        stderr = proc.stderr if isinstance(proc.stderr, str) else proc.stderr.decode("utf-8", "replace")
        raise RuntimeError(stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def staged_paths(root: Path) -> list[str]:
    raw = run_git(["diff", "--cached", "--name-only", "-z"], root)
    assert isinstance(raw, str)
    return [part for part in raw.split("\0") if part]


def staged_file_bytes(root: Path, path: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", f":{path}"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def is_probably_text(path: str, data: bytes) -> bool:
    if b"\0" in data:
        return False
    suffix = Path(path).suffix.lower()
    return suffix in TEXT_SUFFIXES or data.startswith(b"#!")


def scan_text(path: str, text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append({"path": path, "line": line_no, "pattern": name})
    return findings


def main() -> int:
    root = Path(run_git(["rev-parse", "--show-toplevel"], Path.cwd()).strip())
    findings: list[dict[str, object]] = []
    skipped: list[str] = []

    for path in staged_paths(root):
        data = staged_file_bytes(root, path)
        if data is None:
            continue
        if not is_probably_text(path, data):
            skipped.append(path)
            continue
        text = data.decode("utf-8", "replace")
        findings.extend(scan_text(path, text))

    result = {"root": str(root), "findings": findings, "skipped_binary": skipped}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
