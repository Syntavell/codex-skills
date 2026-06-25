---
name: syntavell-security-review
description: >
  Use this skill to review Syntavell changes, designs, dependencies, or releases
  for security, privacy, integrity, and supply-chain risk. Do not use it for
  ordinary implementation, documentation editing, Git commits, or public
  vulnerability disclosure text unless the user explicitly asks for security
  review or disclosure handling.
metadata:
  syntavell.version: "0.2.0"
  syntavell.owner: "security"
  syntavell.status: "experimental"
  syntavell.compatibility.requires:
    - git
---

# Syntavell Security Review

## Goal

Produce evidence-driven security review that names assets, trust boundaries, exploit preconditions, findings, confidence, coverage, and residual unknowns.

## Activation Boundaries

Use when:

- The task touches encryption, keys, local storage, backup/recovery, sync, AI provider calls, prompt injection defenses, parser/compiler isolation, Tauri commands, plugins, templates, CI, release, updater, or dependencies.
- The user asks for a security, privacy, supply-chain, or vulnerability review.
- A companion engineering skill identifies a high-risk trust boundary.

Do not use when:

- The user only asks for a normal code review without security-sensitive surface.
- The task is implementation and no review was requested.
- The task is public disclosure text without explicit vulnerability-handling context.

Companion skills:

- Use Rust or TypeScript engineering skills for implementation after findings are accepted.
- Use maintenance for dependency, CI, and release execution after review.
- Use docs/ADR when a durable security decision must be recorded.

## Source-of-truth precedence

1. User's requested review scope.
2. Current diff, design, manifests, workflows, and release artifacts.
3. Accepted security docs, ADRs, and repository policy.
4. Syntavell privacy and local-first principles.
5. This skill's defaults.

Do not invent missing implementation details. Mark unreviewed surfaces and unknowns explicitly.

## Inputs and Preconditions

- Review mode and target diff, design, dependency set, or release candidate.
- Files, manifests, workflows, or docs that define data movement and trust boundaries.
- Any unavailable evidence must be listed as not reviewed.

## Select a mode

- `diff-review`: review code or documentation changes currently in the worktree.
- `design-review`: review a proposal, ADR, RFC, architecture, or threat model.
- `dependency-review`: review dependency, lockfile, action, template, or toolchain changes.
- `release-review`: review version, artifact, signing, updater, changelog, and publication readiness.

## Workflow

1. Confirm scope and mode.
2. Build a coverage map: reviewed files, unreviewed files, assets, trust boundaries, and assumptions.
3. Identify assets and data movement.
4. Identify trust boundaries and exploit preconditions.
5. Apply `references/security-checklist.md` to the mode.
6. Read `references/disclosure-and-severity.md` for severity, vulnerability handling, or public wording.
7. Report findings first, ordered by severity and confidence.
8. Report not-reviewed surfaces and residual unknowns even when there are no findings.

## Authorization Gates

Explicit user approval is required before:

- Publishing vulnerability details, exploit steps, or security advisories.
- Changing code, dependencies, CI permissions, release artifacts, or secrets.
- Running commands that require private credentials, production keys, or private research data.

## Stop Conditions

Stop or narrow the review when:

- The requested scope is too broad to produce evidence-backed findings.
- Required files or diffs are unavailable and no useful design review can proceed.
- The task asks to disclose an unpatched vulnerability publicly.
- The review would require executing untrusted samples without a sandbox.

## Validation Matrix

| Mode | Required validation |
|---|---|
| `diff-review` | changed files, data flow, trust boundary, exploitability |
| `design-review` | assets, boundaries, abuse cases, controls, residual risk |
| `dependency-review` | changelog, license, native/network behavior, maintainer and lockfile impact |
| `release-review` | artifact inventory, signing/update path, secrets, rollback and publication gates |

## Failure Classification

- `confirmed`: evidence in reviewed files proves the issue.
- `probable`: evidence strongly suggests a risk but one dependency is assumed.
- `speculative`: plausible design risk with insufficient implementation evidence.
- `not-reviewed`: relevant surface outside the available scope.

## Final Output Contract

```text
Scope:
Mode:
Reviewed:
Not reviewed:
Findings:
Coverage:
Assumptions:
Residual unknowns:
Recommended next checks:
```

Finding format:

```text
Severity:
Confidence:
Asset:
Boundary:
Exploit preconditions:
Issue:
Impact:
Evidence:
Fix:
Residual risk:
```

## Reference Routing

- Read `references/security-checklist.md` for every security review.
- Read `references/disclosure-and-severity.md` for severity, vulnerability reports, public disclosure text, or security policy edits.
- Maintain trigger scenarios in `evals/trigger-validation.json`.
- Maintain behavior scenarios in `evals/behavior-evals.json`.
