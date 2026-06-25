---
name: syntavell-typescript-engineering
description: Build, modify, or review TypeScript code for Syntavell. Use when working on React/Vite apps, shared domain packages, Reader, Writer, AI workflows, provider adapters, metadata, retrieval, sync, platform runtime interfaces, or any TypeScript implementation in Syntavell repositories.
---

# Syntavell TypeScript Engineering

## Overview

Use this skill for Syntavell's shared product layer: React UI, domain workflows, AI providers, Reader, Writer, metadata, retrieval, sync, and platform abstractions. TypeScript is the product brain; Rust is the native execution and safety boundary.

Before implementation, read `references/typescript-standards.md`. For UI, Reader, Writer, or platform runtime work, also read `references/ui-and-runtime-boundaries.md`.

## Workflow

1. Locate the package boundary.
   - Keep domain logic in shared packages, not inside app-only components.
   - Keep platform-specific behavior behind runtime interfaces.
   - Keep Tauri and browser APIs out of ordinary product workflows.

2. Preserve domain invariants.
   - Represent Source, FileSnapshot, EvidenceAnchor, Claim, WorkflowRun, Manuscript, TemplateLock, and VenueProfile with typed contracts.
   - Keep generated AI output in draft/review states until the user accepts it.
   - Never let unverified AI claims enter formal knowledge or manuscripts.

3. Make provider behavior capability-driven.
   - Route models through provider adapters and capability tables.
   - Do not assume every provider supports tools, JSON schema, native PDF, embeddings, or file upload.
   - Preview remote data boundaries before sending research content.

4. Build UI for repeated research work.
   - Prefer dense, predictable, keyboard-accessible interfaces.
   - Avoid marketing-style layouts inside the app.
   - Keep Reader, Writer, Synthesis, Provenance, and Security views task-focused.

5. Handle untrusted content.
   - Treat PDFs, webpages, metadata, model output, citations, templates, and imported files as untrusted.
   - Escape rendered content and validate structured model output.
   - Never put secrets in prompts or client-visible logs.

6. Verify with repository-native commands.
   - Run formatter, linter, type check, and tests when configured.
   - For UI changes, run visual or browser checks when a view changes.
   - State any missing project scripts clearly.

## Design Defaults

- Use TypeScript strictness as a design tool, not a nuisance.
- Prefer discriminated unions for state machines.
- Keep side effects at runtime/service boundaries.
- Make async workflow state explicit: pending, running, retrying, failed, cancelled, completed.
- Keep schema versions visible at persistence and sync boundaries.
