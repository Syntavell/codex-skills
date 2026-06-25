# Maintenance Playbook

## When to read

Read this for repository bootstrap, dependency maintenance, CI upkeep, submodule updates, and roadmap hygiene. For release work, also read `release-and-versioning.md`.

## Operating Rule

Maintenance work starts with classification and an impact summary. Prefer dry-run output before changing dependencies, CI permissions, release metadata, or submodule pointers.

## Repository Health

Each mature Syntavell repository should eventually have:

- `README.md`;
- `LICENSE` or explicit license status;
- `CONTRIBUTING.md`;
- `SECURITY.md`;
- `CODE_OF_CONDUCT.md`;
- issue forms and PR template;
- CI for its main artifacts;
- branch protection;
- dependency update automation;
- release and changelog policy when it publishes artifacts.

Do not add policy files with fake contacts, undecided licenses, or unsupported promises.

## Routine Maintenance

Use separate commits for:

- dependency updates;
- CI changes;
- formatting-only changes;
- generated artifacts;
- submodule pointer updates;
- documentation reorganizations;
- release metadata.

Avoid combining unrelated maintenance with feature implementation.

## Dependency Updates

- Inspect changelogs for security, license, and breaking changes.
- Keep lockfiles committed.
- Run the narrowest meaningful test suite.
- For parser, crypto, storage, sync, compiler, and desktop dependencies, treat the update as high-risk until reviewed.
- Summarize direct and transitive version changes.
- Separate pre-existing test failures from failures introduced by the update.
- Do not broaden a dependency update beyond the requested package or version range without approval.

## CI Upkeep

- Keep CI fast enough for pull requests.
- Make required checks deterministic.
- Avoid CI that depends on local absolute paths.
- Use pinned major versions for GitHub Actions.
- Keep secrets out of pull_request workflows from forks.
- Review workflow `permissions:` before adding jobs.
- Treat reusable workflow version changes as behavior changes.

## Submodules

- Update `.codex` only after `Syntavell/codex-skills` has the desired commit pushed.
- Review `git diff --submodule`.
- Commit the submodule pointer separately unless paired with a deliberate consumer change.
- Do not update a parent pointer to an unpushed local submodule commit.

## Roadmap Hygiene

- Keep MVP scope separate from later-stage work.
- Move speculative ideas into RFCs rather than expanding the current implementation surface.
- Keep "not in scope" lists visible when they prevent scope creep.
- Preserve decision status: current, accepted, proposed, preferred, fallback, and illustrative are not interchangeable.
