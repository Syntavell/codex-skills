# Syntavell Commit Policy

## When to read

Read this before staging, writing, amending, or reviewing a Syntavell commit message.

## Operation Modes

- `inspect-only` must not change Git state.
- `stage-and-commit` may stage only inspected paths that belong to the requested logical change.
- `amend` requires explicit user authorization and must report the previous and new commit hash.
- `publish` requires explicit user authorization and must report the remote branch and pushed commit.
- `submodule-pointer` must keep the submodule content commit separate from the parent pointer commit.

## Commit Message Format

Use Conventional Commits with English subjects:

```text
type(scope): imperative summary

Optional body explaining why, risk, migration notes, and verification.
```

Subject rules:

- Keep the subject under 72 characters when practical.
- Use imperative mood: `add`, `fix`, `document`, `prepare`, `remove`.
- Do not end the subject with a period.
- Use one scope, usually the package, crate, app, domain, or repository area.

Common types:

| Type | Use for |
| --- | --- |
| `feat` | New user-facing or developer-facing capability |
| `fix` | Bug fixes and broken behavior |
| `docs` | Documentation-only changes |
| `spec` | Workspace, protocol, schema, or template specification changes |
| `security` | Security-sensitive design, fixes, hardening, or policy |
| `test` | Test-only changes and fixtures |
| `refactor` | Behavior-preserving code restructuring |
| `perf` | Performance improvements |
| `build` | Build system, dependency, packaging, or release plumbing |
| `ci` | GitHub Actions or automation changes |
| `chore` | Maintenance that does not fit another type |

Recommended Syntavell scopes:

- `codex`: reusable Codex skills and agent workflow rules
- `docs`: project documentation and generated PDFs
- `workspace-spec`: open workspace, vault, provenance, or sync specs
- `templates`: Typst/LaTeX templates and venue profiles
- `reader`, `writer`, `vault`, `provider`, `sync`, `metadata`, `ui`
- `repo`: repository setup, community files, or project configuration

Examples:

```text
chore(codex): add reusable git commit skill
docs(product): organize Syntavell repository boundaries
spec(workspace-spec): define encrypted vault manifest fields
security(vault): document recovery key handling
ci(repo): add Rust and Typst verification workflow
```

## Commit Body

Add a body when the commit:

- affects security, encryption, schemas, sync, templates, release flow, or generated artifacts;
- changes behavior across repositories;
- includes a migration or compatibility decision;
- required non-obvious validation.

Use this structure when useful:

```text
Why:
- ...

Verification:
- ...
```

Do not add AI attribution, co-authors, or sign-offs unless the repository policy or user explicitly requires them. If a `DCO` policy exists, include `Signed-off-by` exactly as the policy requires.

## Staging Rules

- Stage one logical change per commit.
- Prefer explicit paths over broad staging.
- Keep generated artifacts with their source changes only when the repository intentionally tracks them.
- Keep vendored third-party material separate from product changes.
- Commit large binary fixtures only when they are documented test fixtures or release assets.

## Safety Checks

Before committing, inspect for:

- `.env`, `.pem`, `.key`, `.p12`, `.mobileprovision`, private certificates, and keychain exports;
- API keys, provider tokens, GitHub tokens, OpenAI keys, Anthropic keys, Gemini keys, and cloud credentials;
- local absolute paths under `/Users/`, `/home/`, or machine-specific temp directories;
- private research PDFs, unpublished datasets, local databases, logs, crash dumps, and telemetry;
- generated model transcripts that may contain private document content.

If any unsafe content appears, stop and remove it from the commit plan.

Run deterministic staged checks when available:

```bash
python skills/syntavell-git-commit/scripts/check_staged_paths.py
python skills/syntavell-git-commit/scripts/scan_staged_secrets.py
```

## Push Rules

- Commit locally first.
- Push only when the user explicitly asked for remote update or the task is incomplete without the remote commit and the user authorized it.
- If pushing to `main`, verify that direct pushes are acceptable for the repository stage. Mature protected repositories should use a branch and PR.
- After pushing, report the remote branch and commit hash.
