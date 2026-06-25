#!/usr/bin/env python3
"""Check a consuming repository's .codex skill installation."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def default_roots(script_path: Path) -> tuple[Path, Path]:
    codex_root = script_path.resolve().parents[1]
    project_root = codex_root.parent if codex_root.name == ".codex" else Path.cwd().resolve()
    return project_root, codex_root


def main() -> int:
    parser = argparse.ArgumentParser()
    project_default, codex_default = default_roots(Path(__file__))
    parser.add_argument("--project-root", type=Path, default=project_default)
    parser.add_argument("--codex-root", type=Path, default=codex_default)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    codex_root = args.codex_root.resolve()
    failures: list[str] = []

    if not (codex_root / "skills").is_dir():
        failures.append(f"missing codex skills directory: {codex_root / 'skills'}")

    gitmodules = project_root / ".gitmodules"
    if codex_root.name == ".codex" and gitmodules.exists():
        text = gitmodules.read_text(encoding="utf-8")
        if "path = .codex" not in text:
            failures.append(".gitmodules exists but does not declare path = .codex")

    agents_root = project_root / ".agents" / "skills"
    if not agents_root.is_dir():
        failures.append(f"missing exposed skills directory: {agents_root}")
    else:
        for source in sorted(path for path in (codex_root / "skills").iterdir() if path.is_dir()):
            destination = agents_root / source.name
            if not destination.exists():
                failures.append(f"missing exposed skill: {destination}")
            elif destination.is_symlink() and destination.resolve() != source.resolve():
                failures.append(f"exposed skill points elsewhere: {destination}")

    validator = codex_root / "scripts" / "validate_skills.py"
    if validator.exists():
        code, out, err = run([sys.executable, str(validator)], codex_root)
        if code != 0:
            failures.append(err or out or "skill validation failed")
    else:
        failures.append(f"missing validator: {validator}")

    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    print("Syntavell project skill installation is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
