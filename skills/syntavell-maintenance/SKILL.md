---
name: syntavell-maintenance
description: Maintain Syntavell repositories and project operations. Use for repository setup, dependency updates, CI upkeep, release preparation, versioning, submodule updates, issue labels, branch protection, health files, roadmap hygiene, and routine cross-repository maintenance.
---

# Syntavell Maintenance

## Overview

Use this skill for keeping Syntavell repositories healthy and coherent over time. Maintenance work should reduce operational ambiguity without changing product behavior unnecessarily.

Read `references/maintenance-playbook.md` before repository maintenance. Read `references/release-and-versioning.md` for release, version, changelog, schema, template, or submodule version work.

## Workflow

1. Identify the maintenance scope.
   - Separate repository hygiene, dependency updates, CI changes, release work, and submodule pointer updates.
   - Avoid mixing mechanical maintenance with product behavior changes.

2. Check repository state.
   - Inspect branch, remotes, status, CI configuration, lockfiles, and submodules.
   - Confirm whether the repository is public, private, empty, or protected.

3. Preserve governance.
   - Keep community health files consistent across repositories.
   - Do not invent licenses, CLA/DCO policy, security contacts, or support guarantees.
   - Make undecided governance explicit.

4. Update mechanically and review.
   - Prefer small, reviewable commits.
   - Keep generated lockfile changes with dependency changes.
   - Keep submodule pointer updates separate when they are the only parent change.

5. Verify.
   - Run repository-specific validation.
   - For this repository, run `python3 scripts/validate_skills.py`.
   - For changed GitHub Actions, review workflow syntax and run local checks where possible.

## Maintenance Defaults

- Favor predictable automation over manual convention.
- Track versioned contracts explicitly.
- Keep public promises conservative.
- Treat dependency and CI changes as supply-chain changes.
- Record what was verified in commit messages and final reports.
