---
name: syntavell-rust-engineering
description: Build, modify, or review Rust code for Syntavell. Use when working on Tauri commands, native-core crates, vault crypto, local indexes, document parsers, compiler hosts, filesystem tasks, background jobs, FFI/WASM boundaries, or any Rust implementation in Syntavell repositories.
---

# Syntavell Rust Engineering

## Overview

Use this skill for Rust work that touches Syntavell's local-first native boundary. Rust code in Syntavell is responsible for privileged local execution, encryption, storage, parsing, indexing, compiler hosting, process isolation, and Tauri IPC.

Before implementation, read `references/rust-standards.md`. If the change touches encryption, secrets, filesystem access, parsers, subprocesses, Tauri commands, backups, sync, or untrusted input, also read `references/rust-security-boundaries.md`.

## Workflow

1. Locate the crate and boundary.
   - Identify whether the change belongs in `native-core`, `vault-crypto`, `document-parser`, `local-index`, `compiler-host`, or `native-bridge`.
   - Keep product decisions and prompt/business logic in TypeScript unless the operation requires native capability.

2. Model data explicitly.
   - Prefer typed structs, enums, and error variants over ad hoc strings.
   - Treat workspace IDs, object IDs, operation hashes, device IDs, and key IDs as distinct domain types when practical.

3. Preserve local-first safety.
   - Never make server state the only source of truth.
   - Never log plaintext research content, secrets, keys, prompts, provider responses, or absolute local paths.
   - Keep encrypted object storage, materialized views, and operation logs conceptually separate.

4. Design for crash recovery.
   - Use atomic file writes or transactional database operations for durable state.
   - Keep migrations reversible or backed up.
   - Make recovery and verification paths testable.

5. Validate untrusted input.
   - Treat PDFs, webpages, templates, LaTeX, Typst, imported archives, provider responses, and plugin inputs as hostile.
   - Prefer bounded parsing, explicit limits, timeouts, and sandboxed subprocesses.

6. Test at the boundary.
   - Add unit tests for pure logic.
   - Add integration or fixture tests for filesystem, database, parser, compiler, and migration behavior.
   - Add property tests or test vectors for serialization, crypto wrappers, and log replay when feasible.

7. Verify before handoff.
   - Run `cargo fmt --check`.
   - Run `cargo clippy --all-targets --all-features` when the crate supports it.
   - Run `cargo test` or the narrowest meaningful test command.
   - If the project is still bootstrapping, run at least `cargo check` and explain any omitted checks.

## Design Defaults

- Keep `unsafe` out of product code unless there is no reasonable alternative and the invariants are documented.
- Prefer well-reviewed crates for crypto, serialization, SQL, and parsing.
- Keep public API contracts stable and versioned when they touch `workspace-spec`.
- Make Tauri command payloads small, typed, auditable, and permission-scoped.
- Prefer deterministic behavior over implicit global state.
