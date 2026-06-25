---
name: syntavell-git-commit
description: Commit Syntavell repository changes safely and consistently. Use when Codex is asked to review, stage, commit, push, or prepare commits in any Syntavell repository, including submodule pointer updates, generated documentation artifacts, release preparation, and agent-produced code changes.
---

# Syntavell Git Commit

## Overview

Use this skill to turn finished Syntavell work into intentional Git history. Treat every commit as a durable project record: scoped, reviewed, reproducible, and free of unrelated or unsafe changes.

Before staging or writing the commit message, read `references/commit-policy.md`. When repository-specific verification or submodule behavior matters, also read `references/repository-rules.md`.

## Required Workflow

1. Resolve the target repository.
   - Run `git rev-parse --show-toplevel`, `git remote -v`, `git branch --show-current`, and `git status --short --branch`.
   - If multiple Syntavell repositories are involved, handle one repository at a time.
   - If the current repository is inside `.codex`, remember it is a submodule from `Syntavell/codex-skills`.

2. Inspect before staging.
   - Review `git diff --stat`, `git diff --name-only`, and relevant full diffs.
   - Run `git diff --check` before committing.
   - Identify untracked files, generated files, binary files, deleted files, and submodule pointer changes explicitly.
   - Do not stage changes you did not inspect.

3. Protect user work.
   - Never revert, reset, checkout, clean, or overwrite user changes unless explicitly instructed.
   - If unrelated changes are present, stage only the paths that belong to the requested commit.
   - If unrelated changes are in the same file as requested changes, inspect carefully and either make a narrow patch or ask before committing mixed ownership.

4. Screen for unsafe content.
   - Search staged and unstaged text for secrets, private keys, API keys, local absolute paths, personal tokens, unpublished vulnerability details, and accidental research data.
   - Do not commit logs, caches, build outputs, model outputs, private PDFs, local database files, `.env` files, or credential material unless the repository policy explicitly says the artifact is intended.

5. Validate at the right level.
   - Run the smallest meaningful verification for the change.
   - Prefer repository-native commands and documented scripts over ad hoc checks.
   - For docs, compile or lint the changed docs when practical.
   - For code, run formatter, linter, type check, and tests appropriate to the touched language and blast radius.

6. Stage intentionally.
   - Prefer explicit path staging: `git add path/to/file`.
   - Use `git add -p` when only part of a file belongs in the commit.
   - Avoid `git add .` unless the worktree is small, fully inspected, and entirely part of one logical change.

7. Write the commit.
   - Use the message format in `references/commit-policy.md`.
   - Include verification in the body when the change is non-trivial, security-relevant, generated, or cross-repository.
   - Keep each commit focused on one reason to change.

8. Push only when appropriate.
   - Push when the user asks to publish, push, update the remote, or when the current task clearly requires the remote repository to contain the commit.
   - After pushing a submodule repository, update parent repository submodule pointers only when the parent repository should consume that new commit.

## Submodule Rule

When committing inside `Syntavell/codex-skills`, there are usually two separate commits:

1. Commit and push the skill changes in `codex-skills`.
2. Update each consuming repository's `.codex` submodule pointer and commit that pointer update in the parent repository.

Do not mix skill content changes and parent application changes in the same repository commit. Report any parent repositories that still point at an older `.codex` commit.

## Final Report

After committing, report:

- repository and branch;
- commit hash and subject;
- whether it was pushed;
- verification commands and results;
- any remaining uncommitted changes;
- any submodule pointers that need follow-up.
