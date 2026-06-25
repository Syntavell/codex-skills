# Maintenance Playbook

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

## CI Upkeep

- Keep CI fast enough for pull requests.
- Make required checks deterministic.
- Avoid CI that depends on local absolute paths.
- Use pinned major versions for GitHub Actions.
- Keep secrets out of pull_request workflows from forks.

## Submodules

- Update `.codex` only after `Syntavell/codex-skills` has the desired commit pushed.
- Review `git diff --submodule`.
- Commit the submodule pointer separately unless paired with a deliberate consumer change.

## Roadmap Hygiene

- Keep MVP scope separate from later-stage work.
- Move speculative ideas into RFCs rather than expanding the current implementation surface.
- Keep "not in scope" lists visible when they prevent scope creep.
