---
name: syntavell-docs-and-adr
description: >
  Use this skill to create, reorganize, revise, or review Syntavell
  documentation, Typst design docs, ADRs, RFCs, specs, roadmap documents, and
  contributor-facing docs. Do not use it for ordinary code implementation,
  security review, Git commits, or to turn speculative ideas into accepted
  decisions without evidence and user approval.
metadata:
  syntavell.version: "0.2.0"
  syntavell.owner: "documentation"
  syntavell.status: "experimental"
  syntavell.compatibility.requires:
    - git
---

# Syntavell Docs and ADR

## Goal

Keep Syntavell documentation decision-oriented, source-controlled, and useful to future implementers without confusing current state, accepted decisions, preferred direction, and illustrative examples.

## Activation Boundaries

Use when:

- The task creates, rewrites, reviews, reorganizes, or reconciles Syntavell docs, Typst design docs, ADRs, RFCs, specs, roadmap documents, repository policies, or contributor docs.
- The task records product decisions, architecture, workspace formats, security models, AI workflows, templates, releases, or repository policies.
- Code and docs contradict each other and the user asks to resolve documentation.

Do not use when:

- The task is ordinary code implementation or testing.
- The user asks for security review; use `syntavell-security-review`.
- The user asks to commit finished changes; use `syntavell-git-commit`.
- The request would mark a decision accepted without source evidence or user approval.

Companion skills:

- Use engineering skills when docs require code truth from Rust or TypeScript.
- Use security review for security policy, threat model, disclosure, or privacy-sensitive docs.
- Use maintenance for release docs, health files, and repository policy operations.

## Source-of-truth precedence

1. The user's explicit documentation goal and accepted wording.
2. Current repository files, manifests, code, and docs.
3. Accepted ADRs and accepted specifications.
4. Proposed RFCs and draft documents.
5. This skill's placement defaults and templates.

Treat `current`, `accepted`, `preferred`, `proposed`, `fallback`, and `illustrative` as distinct document states.

## Inputs and Preconditions

- Target document type and repository.
- Source documents or code evidence.
- Decision status: draft, proposed, accepted, superseded, deprecated, or informative.
- Any generated artifact rules for Typst/PDF/checksums.

## Select a mode

- `doc-review`: review structure, accuracy, placement, and stale claims.
- `existing-doc-rework`: reorganize or rewrite docs without changing decisions.
- `new-adr`: record a decision ready for acceptance or proposed review.
- `adr-transition`: accept, supersede, deprecate, or link decisions.
- `rfc`: write or revise a proposal that still has open questions.
- `conflict-resolution`: reconcile code, docs, ADRs, and specs when they disagree.

## Workflow

1. Collect sources.
   - Inspect current docs, code, manifests, accepted ADRs, and relevant specs.
   - Do not rely on memory when repository evidence exists.

2. Classify document type and state.
   - Separate current behavior, accepted decisions, preferred future direction, fallback behavior, and examples.

3. Place the document.
   - Read `references/documentation-standards.md` before moving or creating docs.
   - Keep repository placement consistent with source of truth.

4. Write for implementers.
   - State decisions, non-goals, invariants, tradeoffs, compatibility, security notes, and validation.
   - Link to sources rather than duplicating long sections.

5. Manage ADR lifecycle.
   - Read `references/adr-rfc-templates.md` for ADR/RFC work.
   - Preserve numbering and add supersedes/superseded-by links.

6. Verify.
   - Compile Typst when changed.
   - Update generated PDFs and checksums only when tracked by the repository.
   - Check links, paths, and status consistency.

## Authorization Gates

Explicit user approval is required before:

- Marking an ADR or policy as accepted.
- Inventing license, governance, support, security contact, or disclosure commitments.
- Deleting or superseding existing decisions.
- Regenerating and committing formal PDFs or checksums when the source is uncertain.

## Stop Conditions

Stop without editing when:

- Source-of-truth conflicts cannot be resolved from repository evidence.
- The requested doc would misrepresent a draft as accepted.
- The right repository or document owner cannot be identified.
- The edit would create public promises the project has not accepted.

## Validation Matrix

| Mode | Required validation |
|---|---|
| `doc-review` | source links, stale claim scan, placement check |
| `existing-doc-rework` | no decision-state change, links and paths checked |
| `new-adr` | context, decision, alternatives, consequences, validation |
| `adr-transition` | status, date, supersedes/superseded-by, index consistency |
| `rfc` | goals, non-goals, proposal, compatibility, open questions |
| `conflict-resolution` | source precedence applied and conflict documented |

## Failure Classification

- `caused-by-change`: introduced by the documentation edit.
- `pre-existing`: stale or conflicting docs found before the edit.
- `environment`: missing compiler, renderer, or source document.
- `unsupported`: requested wording would assert an undecided policy or false status.

## Final Output Contract

```text
Repository:
Mode:
Documents:
Source evidence:
Decision-state changes:
Actions:
Validation:
New failures:
Pre-existing conflicts:
Remaining risks:
Follow-up:
```

## Reference Routing

- Read `references/documentation-standards.md` before creating, moving, or reorganizing docs.
- Read `references/adr-rfc-templates.md` for ADR, RFC, decision-state, or supersession work.
- Maintain trigger scenarios in `evals/trigger-validation.json`.
- Maintain behavior scenarios in `evals/behavior-evals.json`.
