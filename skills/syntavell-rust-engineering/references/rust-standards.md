# Rust Standards

## When to read

Read this for any Rust implementation or review. The current Cargo workspace and source tree are authoritative.

## Crate Boundaries

Use Rust for native execution that TypeScript cannot safely or efficiently own:

- filesystem scanning and atomic writes;
- encrypted object vault operations;
- SQLCipher and local indexes;
- parser, OCR, and compiler subprocess orchestration;
- background jobs and OS integration;
- Tauri command handlers and native bridges.

Avoid moving ordinary product workflows, UI state, prompt wording, and provider routing into Rust without a clear native requirement.

The examples above are boundary categories, not required crate names. Do not create a crate or directory only because an architecture document or skill mentions it.

## API Shape

- Use typed request and response structs for IPC and crate boundaries.
- Use enums for operation kinds, claim states, source types, and security modes.
- Use explicit versions for persisted payloads.
- Use `serde` carefully: deny unknown fields for security-sensitive config, but allow forward-compatible parsing for versioned export formats when documented.
- Keep domain validation near constructors or boundary functions.

## Error Handling

- Return structured errors that distinguish user action, invalid input, IO failure, corruption, permission failure, and internal bugs.
- Avoid stringly typed error matching.
- Do not expose secrets, plaintext snippets, provider keys, or local absolute paths in errors.
- Include enough context for debugging without leaking research content.

## Dependencies

- Prefer maintained crates with clear licenses and active security posture.
- Avoid adding large dependencies for trivial helpers.
- Pin critical crypto, database, and parser dependencies through lockfiles.
- Review transitive dependencies for native code, network behavior, and license compatibility.

## Persistence

- Use transactions for multi-step database updates.
- Keep materialized views rebuildable from object vault and operation log.
- Persist schema versions and migration state.
- Make migrations idempotent where practical.
- Add fixtures for old versions before changing persisted formats.

## Observability

- Use structured tracing.
- Redact research content, paths, prompts, model responses, and keys by default.
- Make debug logging opt-in and local.
- Do not add telemetry upload paths from Rust without explicit product and privacy design.

## Verification

Prefer this order:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features
cargo test
```

For early crates, `cargo check` is acceptable only when formatter, clippy, or tests are not yet configured. State that limitation in the final report.

Classify failures as caused by the change, pre-existing, environment, or unsupported. Do not hide pre-existing failures by claiming validation passed.
