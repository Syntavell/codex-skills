# Rust Security Boundaries

## Secrets and Keys

- Never print, log, serialize, or include secrets in panic messages.
- Keep provider API keys, device keys, recovery material, and workspace master keys out of general-purpose structs.
- Prefer OS keychain or Stronghold-backed storage for local secrets.
- Treat key export, recovery, and rotation as explicit product flows with tests.

## Crypto

- Do not invent cryptographic primitives or custom modes.
- Use reviewed libraries for Argon2id, XChaCha20-Poly1305, signatures, and hashing.
- Separate key encryption keys, workspace master keys, object keys, database keys, ledger payload keys, and derived search keys.
- Store plaintext hashes inside encrypted manifests when hash disclosure could reveal file possession.
- Add test vectors for encryption wrappers and manifest serialization.

## Filesystem

- Canonicalize and validate paths before access.
- Enforce workspace boundaries.
- Prefer allowlists over blocklists.
- Use atomic writes for manifests, checkpoints, and backups.
- Exclude caches, temporary compiler output, and parser intermediates from durable storage unless intentionally encrypted.

## Parsers and Compilers

Treat PDFs, webpages, LaTeX, Typst, archives, metadata, and imported project files as untrusted.

Required controls:

- temporary work directories;
- timeouts;
- memory and output size limits where available;
- disabled network by default;
- no shell escape unless explicitly allowed by a high-trust profile;
- cleanup of plaintext intermediates;
- stable diagnostic capture without leaking full private content.

## Tauri Commands

- Keep commands narrow and permission-scoped.
- Validate all command inputs on the Rust side even when TypeScript validates them first.
- Do not expose arbitrary filesystem, network, subprocess, or secret access through generic commands.
- Use capability files to constrain which windows can call privileged commands.

## Operation Log and Recovery

- Append operations before updating rebuildable materialized views when that preserves recovery.
- Sign device-originated operations where the design requires provenance.
- Validate parent hashes and sequence constraints during replay.
- Add corruption tests for partial writes, missing objects, and bad signatures.
