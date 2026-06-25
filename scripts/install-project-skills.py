#!/usr/bin/env python3
"""Expose .codex skills to a consuming repository's .agents/skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def default_roots(script_path: Path) -> tuple[Path, Path]:
    codex_root = script_path.resolve().parents[1]
    project_root = codex_root.parent if codex_root.name == ".codex" else Path.cwd().resolve()
    return project_root, codex_root


def relative_symlink(target: Path, link: Path) -> None:
    rel = os.path.relpath(target, start=link.parent)
    link.symlink_to(rel, target_is_directory=True)


def install_skill(source: Path, destination: Path, mode: str, force: bool) -> str:
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == source.resolve():
            return "already-linked"
        if not force:
            raise RuntimeError(f"{destination} already exists; rerun with --force to replace it")
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        else:
            shutil.rmtree(destination)

    if mode == "copy":
        shutil.copytree(source, destination)
        return "copied"

    try:
        relative_symlink(source, destination)
        return "linked"
    except OSError:
        if mode == "symlink":
            raise
        shutil.copytree(source, destination)
        return "copied"


def main() -> int:
    parser = argparse.ArgumentParser()
    project_default, codex_default = default_roots(Path(__file__))
    parser.add_argument("--project-root", type=Path, default=project_default)
    parser.add_argument("--codex-root", type=Path, default=codex_default)
    parser.add_argument("--mode", choices=["auto", "symlink", "copy"], default="auto")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    codex_root = args.codex_root.resolve()
    source_root = codex_root / "skills"
    destination_root = project_root / ".agents" / "skills"

    if not source_root.is_dir():
        print(f"missing skills directory: {source_root}", file=sys.stderr)
        return 2

    destination_root.mkdir(parents=True, exist_ok=True)
    results: dict[str, str] = {}
    for source in sorted(path for path in source_root.iterdir() if path.is_dir()):
        destination = destination_root / source.name
        results[source.name] = install_skill(source, destination, args.mode, args.force)

    for name, status in results.items():
        print(f"{name}: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
