# Syntavell Codex Skills

Reusable Codex skills for Syntavell engineering workflows.

This repository is intended to be consumed by Syntavell repositories as a `.codex` submodule:

```bash
git submodule add https://github.com/Syntavell/codex-skills.git .codex
```

## Skills

- `syntavell-git-commit`: safe, consistent Git review, staging, commit, push, and submodule pointer workflow for Syntavell repositories.

## Layout

```text
skills/
└── syntavell-git-commit/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
```

Keep each skill focused and compact. Put detailed policy in `references/` and only load it when the workflow needs it.
