# Syntavell Codex Skills

Reusable Codex skills for Syntavell engineering workflows.

This repository is consumed by Syntavell repositories as a pinned `.codex` submodule and exposed into the repository-local `.agents/skills` directory.

## Recommended Installation

From a consuming Syntavell repository:

```bash
git submodule add https://github.com/Syntavell/codex-skills.git .codex
python .codex/scripts/install-project-skills.py
python .codex/scripts/check-installation.py
```

The installer creates `.agents/skills/<skill-name>` links to `.codex/skills/<skill-name>`. On platforms where directory symlinks are unavailable, rerun with `--mode copy`.

To initialize an existing checkout:

```bash
git submodule update --init --recursive
python .codex/scripts/install-project-skills.py
python .codex/scripts/check-installation.py
```

To inspect an upgrade without changing the submodule checkout:

```bash
python .codex/scripts/update-project-skills.py
```

To apply an upgrade:

```bash
python .codex/scripts/update-project-skills.py --apply
git diff --submodule
```

Commit the parent repository's `.codex` pointer separately unless the consuming repository intentionally combines that pointer update with related work.

## Skills

- `syntavell-git-commit`: Git inspection, staging, commit, amend, publish authorization, and submodule pointer workflows.
- `syntavell-rust-engineering`: Rust crate discovery, native boundary selection, implementation, validation, and security routing.
- `syntavell-typescript-engineering`: TypeScript package discovery, UI/domain/workflow/provider/runtime modes, validation, and security routing.
- `syntavell-maintenance`: maintenance task router for dependency, CI, release, submodule, bootstrap, and roadmap work.
- `syntavell-security-review`: evidence-driven security, privacy, integrity, and supply-chain review.
- `syntavell-docs-and-adr`: documentation placement, ADR/RFC lifecycle, source precedence, and conflict resolution.

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
    ├── references/
    ├── scripts/
    └── evals/
```

Keep each skill focused and compact. Put detailed policy in `references/`, deterministic checks in `scripts/`, and trigger or behavior scenarios in `evals/`.

## Validation

Run the same check used by CI:

```bash
python scripts/validate_skills.py
```

CI installs `requirements-validator.txt` and calls the organization reusable skill-validation workflow pinned to a specific `Syntavell/.github` commit.
