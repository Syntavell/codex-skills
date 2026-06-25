#!/usr/bin/env python3
"""Emit deterministic Git state for a commit workflow."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git_output(args: list[str], cwd: Path) -> str:
    code, out, err = run_git(args, cwd)
    if code != 0:
        raise RuntimeError(err or f"git {' '.join(args)} failed")
    return out


def optional_git_output(args: list[str], cwd: Path) -> str:
    code, out, _err = run_git(args, cwd)
    return out if code == 0 else ""


def main() -> int:
    cwd = Path.cwd()
    try:
        root = Path(git_output(["rev-parse", "--show-toplevel"], cwd))
    except RuntimeError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    data = {
        "ok": True,
        "root": str(root),
        "branch": optional_git_output(["branch", "--show-current"], root),
        "head": optional_git_output(["rev-parse", "--short", "HEAD"], root),
        "remote": optional_git_output(["remote", "-v"], root).splitlines(),
        "status": optional_git_output(["status", "--short", "--branch"], root).splitlines(),
        "staged": optional_git_output(["diff", "--cached", "--name-status"], root).splitlines(),
        "unstaged": optional_git_output(["diff", "--name-status"], root).splitlines(),
        "untracked": optional_git_output(["ls-files", "--others", "--exclude-standard"], root).splitlines(),
        "submodules": optional_git_output(["submodule", "status", "--recursive"], root).splitlines(),
    }
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
