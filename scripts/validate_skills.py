#!/usr/bin/env python3
"""Validate Syntavell Codex skill structure without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SECRET_PATTERNS = [
    r"gho_[A-Za-z0-9_]+",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"BEGIN [A-Z ]*PRIVATE KEY",
    "OPENAI" + r"_API_KEY",
    "ANTHROPIC" + r"_API_KEY",
    "GEMINI" + r"_API_KEY",
    "AWS" + r"_SECRET_ACCESS_KEY",
    r"password\s*=",
    r"token\s*=",
]
SECRET_RE = re.compile("(" + "|".join(SECRET_PATTERNS) + ")", re.IGNORECASE)
ALLOWED_SKILL_ENTRIES = {"SKILL.md", "agents", "references", "scripts", "assets"}


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(errors, path, "file is not UTF-8 text")
    except OSError as exc:
        fail(errors, path, f"cannot read file: {exc}")
    return ""


def parse_frontmatter(path: Path, text: str, errors: list[str]) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(errors, path, "missing YAML frontmatter")
        return {}, text

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail(errors, path, "frontmatter is not closed")
        return {}, text

    raw = lines[1:end]
    body = "\n".join(lines[end + 1 :])
    data: dict[str, str] = {}
    for line in raw:
        if not line.strip():
            continue
        if ":" not in line:
            fail(errors, path, f"invalid frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value

    extra = set(data) - {"name", "description"}
    if extra:
        fail(errors, path, f"frontmatter has unsupported keys: {', '.join(sorted(extra))}")
    return data, body


def validate_openai_yaml(skill_dir: Path, skill_name: str, errors: list[str]) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        fail(errors, path, "missing agents/openai.yaml")
        return
    text = read_text(path, errors)
    required = ["display_name:", "short_description:", "default_prompt:"]
    for item in required:
        if item not in text:
            fail(errors, path, f"missing {item}")
    if f"${skill_name}" not in text:
        fail(errors, path, f"default_prompt must mention ${skill_name}")
    if "TODO" in text:
        fail(errors, path, "contains TODO")


def validate_references(skill_dir: Path, skill_text: str, errors: list[str]) -> None:
    refs = skill_dir / "references"
    if not refs.exists():
        return
    for ref in sorted(refs.glob("*.md")):
        rel = f"references/{ref.name}"
        if rel not in skill_text:
            fail(errors, ref, f"reference is not linked from SKILL.md as {rel}")
        text = read_text(ref, errors)
        if "TODO" in text:
            fail(errors, ref, "contains TODO")


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    for child in skill_dir.iterdir():
        if child.name not in ALLOWED_SKILL_ENTRIES:
            fail(errors, child, "unexpected skill entry")

    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        fail(errors, skill_path, "missing SKILL.md")
        return

    text = read_text(skill_path, errors)
    data, body = parse_frontmatter(skill_path, text, errors)
    name = data.get("name", "")
    description = data.get("description", "")

    if name != skill_dir.name:
        fail(errors, skill_path, f"frontmatter name {name!r} does not match folder")
    if not NAME_RE.match(name):
        fail(errors, skill_path, f"invalid skill name {name!r}")
    if len(description) < 40:
        fail(errors, skill_path, "description is too short")
    if "Use " not in description:
        fail(errors, skill_path, "description must include trigger language with 'Use'")
    if "TODO" in text:
        fail(errors, skill_path, "contains TODO")
    if len(text.splitlines()) > 500:
        fail(errors, skill_path, "SKILL.md exceeds 500 lines")
    if not body.strip():
        fail(errors, skill_path, "missing body")

    validate_openai_yaml(skill_dir, name, errors)
    validate_references(skill_dir, text, errors)


def scan_for_secrets(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".txt"}:
            continue
        text = read_text(path, errors)
        match = SECRET_RE.search(text)
        if match:
            fail(errors, path, f"possible secret or forbidden token pattern: {match.group(0)}")


def main() -> int:
    errors: list[str] = []
    if not SKILLS.exists():
        fail(errors, SKILLS, "missing skills directory")
    else:
        skill_dirs = [path for path in sorted(SKILLS.iterdir()) if path.is_dir()]
        if not skill_dirs:
            fail(errors, SKILLS, "no skills found")
        for skill_dir in skill_dirs:
            validate_skill(skill_dir, errors)

    scan_for_secrets(errors)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All skills are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
