---
name: syntavell-docs-and-adr
description: Create, revise, or review Syntavell documentation, Typst design docs, ADRs, RFCs, specs, roadmap documents, and contributor-facing docs. Use when documenting product decisions, architecture, workspace formats, security models, AI workflows, templates, releases, or repository policies.
---

# Syntavell Docs and ADR

## Overview

Use this skill to keep Syntavell documentation decision-oriented, source-controlled, and useful to future implementers. Documentation should explain boundaries, invariants, consequences, and verification, not just restate implementation.

Read `references/documentation-standards.md` before editing docs. For ADR or RFC work, also read `references/adr-rfc-templates.md`.

## Workflow

1. Identify the document type.
   - Product docs, architecture docs, ADR, RFC, workspace spec, template spec, security policy, maintenance doc, or user-facing guide.

2. Place it in the right repository.
   - Product and app architecture in `Syntavell/syntavell`.
   - Workspace, vault, provenance, and sync specifications in `Syntavell/workspace-spec`.
   - Templates and Venue Profiles in `Syntavell/templates`.
   - Reusable agent workflows in `Syntavell/codex-skills`.

3. Write for implementers.
   - State decisions, non-goals, invariants, tradeoffs, and verification.
   - Keep speculative ideas separate from accepted decisions.
   - Link to source documents rather than duplicating long sections.

4. Preserve Syntavell principles.
   - Local-first, evidence-first, human verification, open formats, privacy by construction, and no premature cloud infrastructure.

5. Verify docs.
   - Compile Typst documents when changed.
   - Update generated PDFs and checksums when tracked.
   - Check links and repository paths.
   - Keep ADR numbering stable.

## Documentation Defaults

- Prefer concise Markdown for contributor-facing docs.
- Prefer Typst for formal design, ADR, RFC, and review documents when the repository already uses Typst.
- Keep generated artifacts clearly tied to their sources.
- Do not invent final policy where the project has not decided license, governance, support, or security contacts.
