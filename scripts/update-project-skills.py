#!/usr/bin/env python3
"""Update a consuming repository's .codex submodule and exposed skills."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(args: list[str], cwd: Path, dry_run: bool) -> None:
    print("+ " + " ".join(args))
    if dry_run:
        return
    proc = subprocess.run(args, cwd=cwd, check=False, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed with exit code {proc.returncode}: {' '.join(args)}")


def default_roots(script_path: Path) -> tuple[Path, Path]:
    codex_root = script_path.resolve().parents[1]
    project_root = codex_root.parent if codex_root.name == ".codex" else Path.cwd().resolve()
    return project_root, codex_root


def main() -> int:
    parser = argparse.ArgumentParser()
    project_default, codex_default = default_roots(Path(__file__))
    parser.add_argument("--project-root", type=Path, default=project_default)
    parser.add_argument("--codex-root", type=Path, default=codex_default)
    parser.add_argument("--ref", default="origin/main", help="submodule ref to check out after fetch")
    parser.add_argument("--apply", action="store_true", help="perform the update; default is dry-run")
    parser.add_argument("--force-install", action="store_true", help="replace existing exposed skill directories")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    codex_root = args.codex_root.resolve()
    dry_run = not args.apply

    if not (codex_root / ".git").exists():
        print(f"error: {codex_root} is not a standalone Git checkout", file=sys.stderr)
        return 2

    try:
        run(["git", "fetch", "origin"], codex_root, dry_run)
        run(["git", "checkout", args.ref], codex_root, dry_run)
        install_cmd = [
            sys.executable,
            str(codex_root / "scripts" / "install-project-skills.py"),
            "--project-root",
            str(project_root),
            "--codex-root",
            str(codex_root),
        ]
        if args.force_install:
            install_cmd.append("--force")
        run(install_cmd, project_root, dry_run)
        run(
            [
                sys.executable,
                str(codex_root / "scripts" / "check-installation.py"),
                "--project-root",
                str(project_root),
                "--codex-root",
                str(codex_root),
            ],
            project_root,
            dry_run,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if dry_run:
        print("Dry run complete. Rerun with --apply to update the submodule checkout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
