# Syntavell Repository Rules

## Repository Map

| Repository | Commit focus |
| --- | --- |
| `Syntavell/syntavell` | Product application, architecture docs, MVP plans, app/runtime code |
| `Syntavell/workspace-spec` | Workspace format, vault format, provenance, sync protocol, validation CLI |
| `Syntavell/templates` | Typst/LaTeX templates, venue profiles, compile locks, template fixtures |
| `Syntavell/codex-skills` | Reusable Codex skills used by Syntavell repositories |
| `Syntavell/.github` | Organization profile and community health defaults |

## Verification Matrix

Use the smallest meaningful set for the touched files.

| Change type | Verification |
| --- | --- |
| Rust code | `cargo fmt --check`, `cargo clippy --all-targets --all-features`, `cargo test`, or at minimum `cargo check` when early-stage |
| TypeScript code | package-manager install check, formatter/linter, type check, unit tests |
| Typst docs | `typst compile <source> <output>` and checksum update when PDFs are tracked |
| Markdown docs | link/path sanity check and rendered structure review |
| Workspace spec | schema examples, round-trip tests, compatibility notes |
| Templates | compile representative fixtures and record engine/template versions |
| GitHub workflows | syntax review and, when possible, local action linting |
| Submodules | `git submodule status`, parent `git diff --submodule`, and updated pointer commit |

## Generated Artifacts

Syntavell may track generated PDFs and checksums for formal design documents. When doing so:

- compile from the `.typ` source;
- update the PDF in the same commit as the source change;
- update `SHA256SUMS` if present;
- mention the compile command in verification.

Do not commit build directories such as `target/`, `node_modules/`, `dist/`, `.turbo/`, `.vite/`, or editor caches.

## Submodule Handling

The `.codex` path in Syntavell repositories should point to `Syntavell/codex-skills`.

When updating skills:

1. Commit and push in `codex-skills`.
2. In the parent repository, run `git submodule update --remote .codex` or checkout the desired commit inside `.codex`.
3. Review `git diff --submodule`.
4. Commit only `.codex` and `.gitmodules` if the parent change is purely a skill pointer update.

Use a commit subject like:

```text
chore(codex): update reusable skills submodule
```

## Empty or New Repositories

For repositories with no prior commits:

- create a minimal, coherent initial commit;
- include `README.md`, `LICENSE` if decided, `.gitignore`, and core structure;
- avoid adding immature implementation stubs that imply production readiness.

If the license is undecided, call that out instead of inventing one.
