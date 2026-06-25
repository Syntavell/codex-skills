---
name: syntavell-typescript-engineering
description: >
  Use this skill when implementing or reviewing TypeScript in Syntavell,
  including React/Vite apps, shared domain packages, Reader, Writer, AI
  workflows, provider adapters, metadata, retrieval, sync, platform runtime
  interfaces, and browser/Tauri integration boundaries. Do not use it for Rust
  work, documentation-only edits, Git commits, or to create planned packages
  that are not present in the current repository.
metadata:
  syntavell.version: "0.2.0"
  syntavell.owner: "engineering"
  syntavell.status: "experimental"
  syntavell.compatibility.requires:
    - git
    - node
---

# Syntavell TypeScript Engineering

## Goal

Implement TypeScript changes in the correct product boundary, with package-manager discovery, mode-specific validation, runtime separation, and failure attribution.

## Activation Boundaries

Use when:

- The task changes or reviews TypeScript, React, Vite, package manifests, provider adapters, workflow definitions, schemas, runtime interfaces, or TypeScript tests.
- The requested behavior belongs in Syntavell's product layer rather than native Rust.

Do not use when:

- The change belongs entirely in Rust, docs, CI, or Git history.
- A planned package name appears only in architecture notes and not in current manifests.
- The user only asks for security review; use `syntavell-security-review`.

Companion skills:

- Route provider, remote processing, persisted schema, sync, and browser/Tauri boundary work through `syntavell-security-review`.
- Route durable architecture decisions through `syntavell-docs-and-adr`.
- Use `syntavell-git-commit` only when the user asks to commit.

## Source-of-truth precedence

1. The user's requested behavior.
2. Current package manager files, workspace manifests, source tree, and tests.
3. Repository-local `AGENTS.md`, accepted ADRs, and specs.
4. Accepted cross-repository Syntavell specifications.
5. This skill's defaults and illustrative package examples.

Current repository structure wins over target architecture examples. Never create a package, directory, provider, or runtime abstraction only because this skill mentions it.

## Inputs and Preconditions

- Package-manager and workspace discovery result.
- Target package, app, route, adapter, schema, or runtime boundary.
- Change mode and risk level.
- Repository-native validation commands, or a clear note that they are absent.

## Select a mode

- `ui`: React UI, Reader, Writer, navigation, accessibility, and visual behavior.
- `domain`: core entities, schemas, invariants, state machines, and pure workflow logic.
- `workflow`: AI workflow definitions, structured outputs, provenance, and review states.
- `provider`: LLM, embedding, local model, relay, capability table, and transport adapters.
- `metadata-retrieval`: DOI, arXiv, Crossref, Semantic Scholar, Unpaywall, chunking, retrieval, and ranking.
- `sync-runtime`: persisted schema, encrypted sync clients, runtime interfaces, browser/Tauri boundaries.
- `platform`: browser, desktop, worker, and API implementation behind product interfaces.

## Workflow

1. Discover the current TypeScript surface.
   - Inspect `package.json`, lockfiles, workspace files, framework config, scripts, and existing tests.
   - Prefer repository-native scripts over assumed package names.

2. Classify the mode and package boundary.
   - Keep domain logic out of app-only components when a shared package already exists.
   - Keep platform-specific behavior behind runtime interfaces.
   - Keep raw Tauri and browser APIs out of ordinary product workflows.

3. Read the relevant references.
   - Always read `references/typescript-standards.md`.
   - Read `references/ui-and-runtime-boundaries.md` for UI, Reader, Writer, platform, privacy UI, or runtime boundary work.

4. Implement narrowly.
   - Use strict types, schema validation at trust boundaries, explicit state machines, and capability-driven provider behavior.
   - Keep generated AI output in draft/review states until accepted by the user.

5. Validate according to the mode.
   - Run configured formatter, linter, typecheck, tests, and UI/browser checks where applicable.
   - State missing scripts instead of inventing local-only validation.

6. Attribute failures.
   - Separate failures introduced by this change from pre-existing or environment failures.

## Authorization Gates

Explicit user approval is required before:

- Sending private research content, prompts, source files, or metadata to remote providers.
- Changing persisted schema or sync compatibility.
- Adding provider transport, browser direct upload, Tauri bridge, or background network behavior.
- Adding large dependencies, generated code, or vendored SDKs.

## Stop Conditions

Stop before modifying code when:

- No current package or app boundary can be identified.
- The change requires a Rust-native capability instead.
- The change changes privacy, provider, persisted schema, or sync behavior without an accepted decision.
- Validation would require unavailable credentials, private data, or provider accounts.

## Validation Matrix

| Mode | Required validation |
|---|---|
| `ui` | typecheck, interaction or browser check, accessibility-sensitive review |
| `domain` | unit tests, schema tests, state-machine invariants |
| `workflow` | structured output validation, provenance, draft/review state tests |
| `provider` | capability table, contract tests, no model-name-only behavior |
| `metadata-retrieval` | fixture tests, untrusted input validation, rate/error behavior |
| `sync-runtime` | schema versioning, migration/compatibility tests, security review |
| `platform` | interface contract tests and browser/Tauri separation |

## Failure Classification

- `caused-by-change`: introduced by the TypeScript edit.
- `pre-existing`: present before the edit or outside touched packages.
- `environment`: missing package install, browser, credentials, provider account, or network.
- `unsupported`: requested behavior conflicts with accepted architecture or privacy policy.

## Final Output Contract

```text
Repository:
Mode:
Package or app:
Boundary decision:
Actions:
Validation:
New failures:
Pre-existing failures:
Security routing:
Remaining risks:
Follow-up:
```

## Reference Routing

- Read `references/typescript-standards.md` for any TypeScript implementation or review.
- Read `references/ui-and-runtime-boundaries.md` for UI, Reader, Writer, platform, privacy UI, or runtime boundary work.
- Maintain trigger scenarios in `evals/trigger-validation.json`.
- Maintain behavior scenarios in `evals/behavior-evals.json`.
