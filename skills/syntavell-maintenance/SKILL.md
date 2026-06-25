---
name: syntavell-maintenance
description: >
  Use this skill to classify and plan Syntavell repository maintenance such as
  dependency updates, CI upkeep, release preparation, versioning, submodule
  pointer updates, repository bootstrap, and roadmap hygiene. Do not use it for
  ordinary feature implementation, documentation authoring, security review, Git
  commits, or remote GitHub administration unless the user explicitly requests
  that maintenance operation.
metadata:
  syntavell.version: "0.2.0"
  syntavell.owner: "engineering"
  syntavell.status: "experimental"
  syntavell.compatibility.requires:
    - git
---

# Syntavell Maintenance

## Goal

Classify maintenance work, expose risk, select the right workflow, and keep repository operations conservative and auditable.

## Activation Boundaries

Use when:

- The task is dependency maintenance, CI upkeep, release readiness, versioning, submodule update, repository bootstrap, health files, or roadmap hygiene.
- The user asks to assess or plan a repository maintenance operation.
- The task spans operational contracts rather than product behavior.

Do not use when:

- The task is ordinary Rust or TypeScript implementation.
- The user only asks to commit already finished work.
- The user asks for security analysis; use `syntavell-security-review` instead.
- The task requires remote GitHub governance mutation and the user has not explicitly authorized it.

Companion skills:

- Use `syntavell-security-review` for dependency, release, CI, updater, signing, and secret-sensitive work.
- Use `syntavell-git-commit` only after a concrete maintenance change is ready to commit.
- Use docs/ADR workflows when maintenance changes create durable policy.

## Source-of-truth precedence

1. The user's explicit requested maintenance operation and authorization.
2. Current repository files, manifests, lockfiles, workflows, and submodules.
3. Repository-local policy, accepted ADRs, and release docs.
4. Accepted organization defaults in `Syntavell/.github`.
5. This skill's defaults.

Never add community promises, licenses, support windows, release guarantees, or branch protection merely because this skill lists them as mature-project capabilities.

## Inputs and Preconditions

- Target repository and maintenance scope.
- Current Git status and relevant manifests.
- Dry-run result or impact summary for dependency, release, or remote operations.
- Explicit approval for remote mutation, release publication, tags, or branch protection.

## Select a mode

- `repository-bootstrap`: initial structure, README, health files, and CI planning.
- `dependency-maintenance`: dependency and lockfile updates with changelog, license, and test impact.
- `ci-maintenance`: workflow upkeep, permissions, runner behavior, and validation determinism.
- `release-preparation`: version source, artifact inventory, changelog, signing, tag readiness, and rollback plan.
- `submodule-update`: pointer update after the submodule commit is pushed.
- `roadmap-hygiene`: scope, milestone, and decision-state cleanup.
- `github-administration-plan`: plan branch protection, labels, or settings without mutating remotes by default.

## Workflow

1. Classify the task into one mode.
2. Inspect current state: branch, remotes, status, manifests, lockfiles, workflows, and submodules.
3. Produce a dry-run or impact summary before changing dependencies, release metadata, CI permissions, or submodule pointers.
4. Identify authorization gates and stop conditions.
5. Execute only the local, in-scope maintenance change requested by the user.
6. Validate with repository-native checks and the relevant maintenance checklist.
7. Hand off to `syntavell-git-commit` only when the user asks to commit.

## Authorization Gates

Explicit user approval is required before:

- Mutating remote GitHub settings, labels, branch protection, secrets, environments, or releases.
- Publishing tags, release artifacts, packages, installers, or checksums.
- Updating dependencies beyond the requested package or version range.
- Regenerating lockfiles in a way that changes unrelated dependency versions.
- Updating a submodule pointer to an unpushed or unreviewed commit.

## Stop Conditions

Stop without modifying anything when:

- The task mixes maintenance with feature behavior changes.
- The repository has uncommitted unrelated work that would be touched.
- A dependency update has unknown license, security, or breaking-change impact.
- A release lacks version source, artifact inventory, or rollback path.
- The requested remote operation is not explicitly authorized.

## Validation Matrix

| Mode | Required validation |
|---|---|
| `repository-bootstrap` | health-file consistency and no invented policy |
| `dependency-maintenance` | changelog/license review, lockfile diff, tests for affected surface |
| `ci-maintenance` | workflow syntax, permissions review, deterministic inputs |
| `release-preparation` | version source, artifact inventory, full repository validation |
| `submodule-update` | `git submodule status` and `git diff --submodule` |
| `roadmap-hygiene` | no scope expansion without ADR/RFC linkage |
| `github-administration-plan` | written plan; no remote mutation by default |

## Failure Classification

- `caused-by-change`: introduced by the maintenance edit.
- `pre-existing`: already failing before the maintenance edit.
- `environment`: missing tool, registry, credential, or network capability.
- `unsupported`: the requested operation exceeds authorization or project maturity.

## Final Output Contract

```text
Repository:
Mode:
Dry run or impact summary:
Actions:
Validation:
New failures:
Pre-existing failures:
Remote mutations:
Rollback:
Remaining risks:
Follow-up:
```

## Reference Routing

- Read `references/maintenance-playbook.md` for repository health, dependency, CI, submodule, and roadmap maintenance.
- Read `references/release-and-versioning.md` for release, changelog, version, schema, template, or compatibility work.
- Maintain trigger scenarios in `evals/trigger-validation.json`.
- Maintain behavior scenarios in `evals/behavior-evals.json`.
