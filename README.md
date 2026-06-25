# Syntavell Codex Skills

Reusable Codex skills for Syntavell engineering workflows.

This repository is intended to be consumed by Syntavell repositories as a `.codex` submodule:

```bash
git submodule add https://github.com/Syntavell/codex-skills.git .codex
```

## Skills

- `syntavell-git-commit`: safe, consistent Git review, staging, commit, push, and submodule pointer workflow for Syntavell repositories.
- `syntavell-rust-engineering`: Rust implementation guidance for native Syntavell crates and Tauri boundaries.
- `syntavell-typescript-engineering`: TypeScript implementation guidance for the shared product layer.
- `syntavell-maintenance`: repository health, release, versioning, CI, and submodule maintenance.
- `syntavell-security-review`: security and privacy review for Syntavell changes.
- `syntavell-docs-and-adr`: documentation, Typst, ADR, and RFC workflow guidance.

## Layout

```text
skills/
├── syntavell-git-commit/
├── syntavell-rust-engineering/
├── syntavell-typescript-engineering/
├── syntavell-maintenance/
├── syntavell-security-review/
└── syntavell-docs-and-adr/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
```

Keep each skill focused and compact. Put detailed policy in `references/` and only load it when the workflow needs it.

## Validation

Run the same check used by CI:

```bash
python scripts/validate_skills.py
```
