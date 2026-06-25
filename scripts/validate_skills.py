#!/usr/bin/env python3
"""Validate Syntavell Codex skill structure and Syntavell conventions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover - CI installs PyYAML.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_.-]+):(?:\s*(.*))?$")
PATH_REFERENCE_RE = re.compile(r"`((?:references|scripts|assets|evals)/[^`]+)`")
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "metadata",
    "allowed-tools",
}
ALLOWED_SKILL_ENTRIES = {"SKILL.md", "agents", "references", "scripts", "assets", "evals"}
REQUIRED_SKILL_SECTIONS = [
    "## Activation Boundaries",
    "## Source-of-truth precedence",
    "## Select a mode",
    "## Authorization Gates",
    "## Stop Conditions",
    "## Validation Matrix",
    "## Failure Classification",
    "## Final Output Contract",
    "## Reference Routing",
]
REQUIRED_EVAL_FILES = ["trigger-validation.json", "behavior-evals.json"]
FORBIDDEN_DEFAULT_PROMPT_TERMS = [
    r"\bpush\b",
    r"\bpublish\b",
    r"\brelease\b",
    r"\btag\b",
    r"\bdelete\b",
    r"\bremove\b",
    r"\bbranch protection\b",
    r"\bmerge\b",
]
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


def duplicate_top_level_keys(raw: str) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for line in raw.splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#")):
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if not match:
            continue
        key = match.group(1)
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    return duplicates


def strip_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    """Small fallback parser for the repository's YAML subset.

    PyYAML is installed in CI. This fallback keeps local validation usable before
    dependencies are installed; it intentionally supports only the constructs used
    by this repository's frontmatter and agent metadata.
    """

    data: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith((" ", "\t")):
            index += 1
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if not match:
            index += 1
            continue
        key, rest = match.group(1), (match.group(2) or "").strip()

        if rest in {">", ">-", "|", "|-"}:
            index += 1
            block: list[str] = []
            while index < len(lines):
                next_line = lines[index]
                if next_line and not next_line.startswith((" ", "\t")):
                    break
                block.append(next_line.strip())
                index += 1
            data[key] = "\n".join(block) if rest.startswith("|") else " ".join(block)
            continue

        if rest:
            data[key] = strip_scalar(rest)
            index += 1
            continue

        index += 1
        nested: dict[str, Any] = {}
        items: list[str] = []
        while index < len(lines):
            next_line = lines[index]
            if next_line and not next_line.startswith((" ", "\t")):
                break
            stripped = next_line.strip()
            if stripped.startswith("- "):
                items.append(strip_scalar(stripped[2:]))
            else:
                nested_match = TOP_LEVEL_KEY_RE.match(stripped)
                if nested_match:
                    nested[nested_match.group(1)] = strip_scalar(nested_match.group(2) or "")
            index += 1
        data[key] = items if items and not nested else nested
    return data


def parse_yaml_text(path: Path, raw: str, errors: list[str]) -> dict[str, Any]:
    duplicates = duplicate_top_level_keys(raw)
    for key in duplicates:
        fail(errors, path, f"duplicate YAML key: {key}")

    if yaml is None:
        return parse_simple_yaml(raw)

    try:
        parsed = yaml.safe_load(raw) or {}
    except Exception as exc:  # noqa: BLE001 - report parser diagnostics.
        fail(errors, path, f"invalid YAML: {exc}")
        return {}
    if not isinstance(parsed, dict):
        fail(errors, path, "YAML root must be a mapping")
        return {}
    return parsed


def split_frontmatter(path: Path, text: str, errors: list[str]) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(errors, path, "missing YAML frontmatter")
        return "", text

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail(errors, path, "frontmatter is not closed")
        return "", text

    raw = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :])
    return raw, body


def parse_frontmatter(path: Path, text: str, errors: list[str]) -> tuple[dict[str, Any], str]:
    raw, body = split_frontmatter(path, text, errors)
    if not raw:
        return {}, body

    data = parse_yaml_text(path, raw, errors)
    extra = set(data) - ALLOWED_FRONTMATTER
    if extra:
        fail(errors, path, f"frontmatter has unsupported keys: {', '.join(sorted(extra))}")
    return data, body


def validate_required_sections(skill_path: Path, text: str, errors: list[str]) -> None:
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in text:
            fail(errors, skill_path, f"missing required section {section!r}")


def validate_path_references(skill_dir: Path, text: str, errors: list[str]) -> None:
    for match in PATH_REFERENCE_RE.finditer(text):
        rel = match.group(1).strip().rstrip(".,;:")
        target = skill_dir / rel
        if not target.exists():
            fail(errors, skill_dir / rel, "referenced path does not exist")


def validate_openai_yaml(skill_dir: Path, skill_name: str, errors: list[str]) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        fail(errors, path, "missing agents/openai.yaml")
        return
    text = read_text(path, errors)
    parsed = parse_yaml_text(path, text, errors)
    interface = parsed.get("interface")
    if not isinstance(interface, dict):
        fail(errors, path, "missing interface mapping")
        return

    for key in ["display_name", "short_description", "default_prompt"]:
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            fail(errors, path, f"interface.{key} must be a non-empty string")

    default_prompt = str(interface.get("default_prompt", ""))
    if f"${skill_name}" not in default_prompt:
        fail(errors, path, f"default_prompt must mention ${skill_name}")
    for pattern in FORBIDDEN_DEFAULT_PROMPT_TERMS:
        if re.search(pattern, default_prompt, re.IGNORECASE):
            fail(errors, path, f"default_prompt expands authority with high-risk term {pattern!r}")
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


def validate_evals(skill_dir: Path, errors: list[str]) -> None:
    evals = skill_dir / "evals"
    if not evals.exists():
        fail(errors, evals, "missing evals directory")
        return

    for filename in REQUIRED_EVAL_FILES:
        path = evals / filename
        if not path.exists():
            fail(errors, path, "missing required eval file")
            continue
        try:
            data = json.loads(read_text(path, errors))
        except json.JSONDecodeError as exc:
            fail(errors, path, f"invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            fail(errors, path, "eval file must contain a JSON object")
            continue

        if filename == "trigger-validation.json":
            positive = data.get("positive")
            negative = data.get("negative")
            if not isinstance(positive, list) or len(positive) < 4:
                fail(errors, path, "trigger eval must include at least four positive cases")
            if not isinstance(negative, list) or len(negative) < 4:
                fail(errors, path, "trigger eval must include at least four negative cases")
            for group_name, expected in [("positive", True), ("negative", False)]:
                for case in data.get(group_name, []):
                    if not isinstance(case, dict):
                        fail(errors, path, f"{group_name} case must be an object")
                        continue
                    if not isinstance(case.get("query"), str) or not case["query"].strip():
                        fail(errors, path, f"{group_name} case missing query")
                    if case.get("should_trigger") is not expected:
                        fail(errors, path, f"{group_name} case has wrong should_trigger value")

        if filename == "behavior-evals.json":
            cases = data.get("cases")
            if not isinstance(cases, list) or len(cases) < 3:
                fail(errors, path, "behavior eval must include at least three cases")
            for case in cases or []:
                if not isinstance(case, dict):
                    fail(errors, path, "behavior case must be an object")
                    continue
                for key in ["name", "prompt", "expected_behavior", "assertions", "forbidden_actions"]:
                    if key not in case:
                        fail(errors, path, f"behavior case missing {key}")


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

    if not isinstance(name, str):
        fail(errors, skill_path, "frontmatter name must be a string")
        name = ""
    if not isinstance(description, str):
        fail(errors, skill_path, "frontmatter description must be a string")
        description = ""
    if name != skill_dir.name:
        fail(errors, skill_path, f"frontmatter name {name!r} does not match folder")
    if not NAME_RE.match(name):
        fail(errors, skill_path, f"invalid skill name {name!r}")
    if "--" in name:
        fail(errors, skill_path, "skill name must not contain consecutive hyphens")
    if len(description) < 80:
        fail(errors, skill_path, "description is too short")
    if len(description) > 1200:
        fail(errors, skill_path, "description is too long")
    if "Use " not in description or "Do not use" not in description:
        fail(errors, skill_path, "description must include explicit Use and Do not use boundaries")
    if "TODO" in text:
        fail(errors, skill_path, "contains TODO")
    if len(text.splitlines()) > 500:
        fail(errors, skill_path, "SKILL.md exceeds 500 lines")
    if not body.strip():
        fail(errors, skill_path, "missing body")

    validate_required_sections(skill_path, text, errors)
    validate_path_references(skill_dir, text, errors)
    validate_openai_yaml(skill_dir, name, errors)
    validate_references(skill_dir, text, errors)
    validate_evals(skill_dir, errors)


def scan_for_secrets(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.suffix.lower() not in {".json", ".md", ".yaml", ".yml", ".py", ".txt"}:
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
