---
name: syntavell-security-review
description: Review Syntavell changes for security, privacy, and supply-chain risk. Use for changes touching encryption, key management, local storage, backup/recovery, sync, AI provider calls, prompt injection defenses, parsers, compilers, Tauri commands, plugins, templates, CI, releases, or dependency updates.
---

# Syntavell Security Review

## Overview

Use this skill to review whether a Syntavell change preserves local-first privacy, evidence integrity, and safe native execution. Security review should be concrete: identify the asset, trust boundary, failure mode, and required control.

Read `references/security-checklist.md` before reviewing. For vulnerability reports, public disclosure text, security policy edits, or severity discussion, also read `references/disclosure-and-severity.md`.

## Workflow

1. Identify the assets.
   - Research files, notes, prompts, provider responses, API keys, recovery keys, workspace master keys, object keys, operation logs, compiled outputs, metadata, templates, and local paths.

2. Identify trust boundaries.
   - Browser to Tauri, TypeScript to Rust, user content to model, model output to app, workspace to filesystem, local device to cloud, parser/compiler subprocesses, plugin to host, public template to local compiler.

3. Check data movement.
   - Confirm what leaves the device.
   - Confirm what is logged.
   - Confirm what is encrypted at rest.
   - Confirm what is recoverable and what is intentionally unrecoverable without keys.

4. Check untrusted input handling.
   - PDFs, webpages, metadata, LaTeX, Typst, archives, model outputs, provider JSON, templates, and plugins must be validated or sandboxed.

5. Check supply chain.
   - Review dependencies, GitHub Actions, release scripts, update channels, code signing, generated artifacts, and template sources.

6. Report findings by severity.
   - Lead with exploitable issues and data-loss risks.
   - Include file references and exact remediation.
   - Distinguish confirmed issues from assumptions.

## Review Defaults

- Do not accept "local-only" as a complete security argument.
- Do not accept hashes as proof of scholarly correctness.
- Do not allow AI tools direct filesystem, network, or secret access without explicit permission design.
- Do not silently send research content to remote providers.
- Do not let generated content bypass human verification.
