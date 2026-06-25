#!/usr/bin/env python3
"""Check staged paths for files that should not enter Syntavell commits."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


FORBIDDEN_PATH_PATTERNS = [
    re.compile(r"(^|/)\.env($|[./])"),
    re.compile(r"\.(pem|key|p12|mobileprovision)$", re.IGNORECASE),
    re.compile(r"(^|/)(id_rsa|id_dsa|id_ed25519|known_hosts)$"),
    re.compile(r"(^|/)(crash|debug|trace|telemetry).*\.log$", re.IGNORECASE),
    re.compile(r"(^|/)(local|private|secret|secrets)\.(db|sqlite|sqlite3|json|yaml|yml)$", re.IGNORECASE),
]
GENERATED_DIR_PARTS = {
    ".cache",
    ".next",
    ".nuxt",
    ".turbo",
    ".vite",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
}


def run_git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def staged_paths(root: Path) -> list[str]:
    raw = run_git(["diff", "--cached", "--name-only", "-z"], root)
    return [part for part in raw.split("\0") if part]


def binary_paths(root: Path) -> set[str]:
    raw = run_git(["diff", "--cached", "--numstat"], root)
    paths: set[str] = set()
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[0] == "-" and parts[1] == "-":
            paths.add(parts[2])
    return paths


def check_path(path: str) -> list[str]:
    failures: list[str] = []
    parts = set(Path(path).parts)
    matched_generated = sorted(parts & GENERATED_DIR_PARTS)
    if matched_generated:
        failures.append(f"generated or build directory: {', '.join(matched_generated)}")
    for pattern in FORBIDDEN_PATH_PATTERNS:
        if pattern.search(path):
            failures.append(f"forbidden path pattern: {pattern.pattern}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-empty", action="store_true", help="allow no staged paths")
    args = parser.parse_args()

    root = Path(run_git(["rev-parse", "--show-toplevel"], Path.cwd()).strip())
    paths = staged_paths(root)
    binaries = binary_paths(root)
    failures: list[dict[str, object]] = []

    if not paths and not args.allow_empty:
        failures.append({"path": None, "reasons": ["no staged paths"]})

    for path in paths:
        reasons = check_path(path)
        if path in binaries:
            reasons.append("binary file staged; confirm it is an intended fixture or artifact")
        if reasons:
            failures.append({"path": path, "reasons": reasons})

    result = {"root": str(root), "staged_paths": paths, "failures": failures}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
