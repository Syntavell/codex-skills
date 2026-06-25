---
name: syntavell-git-commit
description: >
  Use this skill only when the user asks Codex to inspect Git state, stage paths,
  create or amend a commit, prepare a commit message, update a Syntavell
  submodule pointer, or publish an already authorized branch. Do not use it for
  ordinary code review, implementation, documentation editing, or security
  review when no Git operation was requested.
metadata:
  syntavell.version: "0.2.0"
  syntavell.owner: "engineering"
  syntavell.status: "experimental"
  syntavell.compatibility.requires:
    - git
---

# Syntavell Git Commit

## Goal

Turn finished Syntavell work into intentional Git history: scoped, inspected, validated, reproducible, and free of unrelated or unsafe changes.

## Activation Boundaries

Use when:

- The user asks to commit, stage, amend, prepare a commit message, inspect Git state for commit readiness, or update a submodule pointer.
- The user asks to publish a commit or branch and explicitly authorizes that remote update.
- A prior task finished and the user asks to persist it in Git.

Do not use when:

- The user only asked for implementation, review, planning, or explanation.
- The task is a security review with no requested Git operation.
- The only action is remote repository administration, release publication, or issue/PR management.

Companion skills:

- Use the relevant engineering, docs, security, or maintenance skill before this one when the change itself is still unfinished.

## Source-of-truth precedence

1. The user's explicit Git request and authorization.
2. The current repository state from Git commands.
3. Repository-local `AGENTS.md`, contribution docs, and accepted ADRs.
4. Accepted Syntavell repository rules.
5. This skill's defaults.

Never stage, amend, publish, or rewrite history merely because this skill describes how to do it.

## Inputs and Preconditions

- A concrete target repository.
- A requested Git mode.
- A clean understanding of which paths belong to this commit.
- Explicit authorization for remote mutation, amend, force-with-lease, tags, or release publication.

## Select a mode

- `inspect-only`: report status, diffs, staged paths, and risks without modifying Git state.
- `stage-and-commit`: inspect, validate, stage selected paths, and create one local commit.
- `amend`: amend the latest commit only with explicit user authorization.
- `publish`: push an existing commit or branch only with explicit user authorization.
- `submodule-pointer`: update and commit a parent repository pointer to a pushed submodule commit.

## Workflow

1. Inspect Git state.
   - Prefer `scripts/inspect_git_state.py` when available.
   - Also inspect `git diff --stat`, `git diff --name-only`, and relevant full diffs.
   - Identify untracked files, generated files, binary files, deleted files, and submodule pointer changes.

2. Classify ownership.
   - Separate requested changes from unrelated user work.
   - Do not stage a file unless its relevant hunks were inspected.
   - If the same file contains unrelated ownership, use narrow staging or stop for clarification.

3. Screen for unsafe content.
   - Before committing, run `scripts/check_staged_paths.py` and `scripts/scan_staged_secrets.py` after staging.
   - Before staging, manually inspect suspicious unstaged paths so unsafe files never enter the index.

4. Validate.
   - Read `references/repository-rules.md` to select the smallest meaningful validation.
   - Run `git diff --check`.
   - Run repository-native checks for changed docs, code, workflows, or submodules.

5. Stage intentionally.
   - Prefer explicit path staging.
   - Use patch staging when only part of a file belongs in the commit.
   - Avoid broad staging unless the worktree is small, fully inspected, and one logical change.

6. Commit.
   - Read `references/commit-policy.md`.
   - Use Conventional Commits with an English subject.
   - Include verification in the body when the change is non-trivial, security-relevant, generated, or cross-repository.

7. Publish or update parent pointers only when authorized.
   - Keep content commits and parent submodule pointer commits separate.
   - Report consumers that still point at older submodule commits.

## Authorization Gates

Explicit user approval is required before:

- Running `git commit --amend`, force-with-lease, rebase, or any history rewrite.
- Pushing, publishing tags, creating releases, or changing a remote default branch.
- Deleting branches, cleaning files, reverting user work, or resetting the worktree.
- Committing generated artifacts, binary files, or large fixtures whose purpose is not documented.

## Stop Conditions

Stop without committing when:

- The requested commit includes uninspected or unrelated changes.
- A staged path fails the path or secret scan.
- Validation fails and the failure is caused by the staged change.
- The repository is detached, missing a remote required by the task, or has unresolved merge/rebase state.
- The user asks for a remote operation but has not explicitly authorized it.

## Validation Matrix

| Change type | Required validation |
|---|---|
| Markdown or docs | `git diff --check` plus link/path sanity where practical |
| Skill changes | `python scripts/validate_skills.py` from `Syntavell/codex-skills` |
| GitHub workflow | YAML review plus repository validation |
| Rust | formatter, clippy, tests, or documented narrower Cargo check |
| TypeScript | package-manager detection, lint/type/test when configured |
| Submodule pointer | `git submodule status` and `git diff --submodule` in the parent |

## Failure Classification

- `caused-by-change`: introduced by the staged paths or commit workflow.
- `pre-existing`: already present before this Git operation.
- `environment`: missing tools, credentials, network, or runner capability.
- `unsupported`: the requested Git operation would violate repository policy or user authorization.

## Final Output Contract

```text
Repository:
Mode:
Branch:
Commit:
Published:
Staged paths:
Validation:
New failures:
Pre-existing failures:
Remaining risks:
Follow-up:
```

## Reference Routing

- Read `references/commit-policy.md` before preparing or writing any commit message.
- Read `references/repository-rules.md` before selecting validation or handling submodules.
- Use `scripts/inspect_git_state.py` for deterministic state capture when available.
- Use `scripts/check_staged_paths.py` after staging and before committing.
- Use `scripts/scan_staged_secrets.py` after staging and before committing.
- Maintain trigger scenarios in `evals/trigger-validation.json`.
- Maintain behavior scenarios in `evals/behavior-evals.json`.
