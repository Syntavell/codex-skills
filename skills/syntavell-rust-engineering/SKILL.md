---
name: syntavell-rust-engineering
description: >
  Use this skill when implementing or reviewing Rust code in Syntavell, including
  Tauri commands, native execution, vault crypto, local indexes, parsers,
  compiler hosts, filesystem tasks, background jobs, FFI, or WASM boundaries. Do
  not use it for TypeScript work, documentation-only edits, Git commits, or to
  create planned crates that are not present in the current repository.
metadata:
  syntavell.version: "0.2.0"
  syntavell.owner: "engineering"
  syntavell.status: "experimental"
  syntavell.compatibility.requires:
    - git
    - cargo
---

# Syntavell Rust Engineering

## Goal

Implement Rust changes at the right native boundary, with explicit crate discovery, security routing, validation, and failure attribution.

## Activation Boundaries

Use when:

- The task changes or reviews Rust source, Cargo manifests, native tests, Rust build scripts, Tauri command handlers, or Rust-facing FFI/WASM boundaries.
- The requested behavior requires privileged local execution, durable storage, parsing, crypto, indexing, compiler orchestration, or native OS integration.

Do not use when:

- The change belongs entirely in TypeScript, docs, CI, or Git history.
- A planned crate name appears only in architecture notes and not in current manifests.
- The user asks only for security review; use `syntavell-security-review`.

Companion skills:

- Route crypto, secrets, filesystem, parser, compiler, sync, or Tauri privilege changes through `syntavell-security-review`.
- Route durable architecture decisions through `syntavell-docs-and-adr`.
- Use `syntavell-git-commit` only when the user asks to commit.

## Source-of-truth precedence

1. The user's requested behavior.
2. Current `Cargo.toml`, workspace metadata, source tree, and tests.
3. Repository-local `AGENTS.md`, accepted ADRs, and specs.
4. Accepted cross-repository Syntavell specifications.
5. This skill's defaults and illustrative crate examples.

Current repository structure wins over target architecture examples. Never create a crate, directory, command, or storage boundary only because this skill mentions it.

## Inputs and Preconditions

- Cargo workspace or crate discovery result.
- Target crate, binary, test, or Tauri command boundary.
- Change type and risk level.
- Repository-native verification commands, or a clear note that they are absent.

## Select a mode

- `crate-discovery`: inspect current Cargo workspace, crates, features, and tests.
- `tauri-command`: typed IPC payloads, permissions, input validation, and error redaction.
- `persistence-migration`: durable state, schema versions, transactions, backups, and recovery tests.
- `parser-compiler`: hostile input, subprocess isolation, limits, diagnostics, and cleanup.
- `crypto-secrets`: key separation, reviewed primitives, test vectors, and redaction.
- `background-io`: filesystem, indexing, long-running jobs, cancellation, and crash recovery.
- `api-review`: boundary, error, serialization, and compatibility review.

## Workflow

1. Discover the current Rust surface.
   - Inspect `Cargo.toml`, workspace members, features, and existing tests.
   - Prefer repository-native scripts over assumed package names.

2. Classify the change mode and native boundary.
   - Keep product workflow, prompt wording, and UI state in TypeScript unless native capability is required.
   - Make crate-boundary choices explicit in the final output.

3. Read the relevant references.
   - Always read `references/rust-standards.md`.
   - Read `references/rust-security-boundaries.md` for privileged, hostile-input, crypto, filesystem, Tauri, backup, or sync work.

4. Implement narrowly.
   - Use typed structs, enums, explicit versions, structured errors, and bounded input handling.
   - Do not leak secrets, plaintext research content, provider responses, prompts, or absolute paths in logs or errors.

5. Test at the boundary.
   - Add unit, fixture, integration, property, migration, or corruption tests according to the mode.

6. Validate and attribute failures.
   - Run the narrowest meaningful Cargo validation.
   - Separate new failures from pre-existing and environment failures.

## Authorization Gates

Explicit user approval is required before:

- Adding or replacing crypto primitives, storage formats, or recovery semantics.
- Introducing network access, subprocess execution, broad filesystem access, or plugin host permissions.
- Changing persisted schema compatibility, migrations, or workspace-spec contracts.
- Adding large dependencies, vendored code, or native binaries.

## Stop Conditions

Stop before modifying code when:

- No current Cargo target or crate boundary can be identified.
- The requested change belongs in TypeScript or docs instead.
- The change requires a security or architecture decision that is not yet accepted.
- Validation would require unavailable credentials, private data, or unsafe sample inputs.

## Validation Matrix

| Mode | Required validation |
|---|---|
| `crate-discovery` | report manifests, crates, features, and available checks |
| `tauri-command` | Rust input validation, permission review, IPC tests where present |
| `persistence-migration` | migration fixtures, old-version compatibility, crash/corruption tests |
| `parser-compiler` | hostile fixture, timeout/limit path, diagnostic redaction |
| `crypto-secrets` | reviewed crate usage, test vectors, no plaintext logging |
| `background-io` | cancellation, atomicity, retry, and partial-write behavior |
| `api-review` | typed payloads, error taxonomy, serialization compatibility |

## Failure Classification

- `caused-by-change`: introduced by the Rust edit.
- `pre-existing`: present before the edit or outside touched crates.
- `environment`: missing toolchain, OS capability, fixture, database, or network.
- `unsupported`: requested behavior conflicts with accepted architecture or security policy.

## Final Output Contract

```text
Repository:
Mode:
Crate or target:
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

- Read `references/rust-standards.md` for any Rust implementation or review.
- Read `references/rust-security-boundaries.md` for crypto, secrets, filesystem, parser, compiler, Tauri, backup, sync, subprocess, or untrusted-input work.
- Maintain trigger scenarios in `evals/trigger-validation.json`.
- Maintain behavior scenarios in `evals/behavior-evals.json`.
