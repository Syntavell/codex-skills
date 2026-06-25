# Release and Versioning

## Versioned Surfaces

Track versions for:

- workspace schema;
- encrypted vault format;
- operation schema;
- workflow definitions;
- template manifests;
- Venue Profiles;
- parser and chunker outputs;
- provider contracts;
- compiler locks;
- application releases.

## Release Preparation

Before a release:

1. Confirm scope and target repositories.
2. Run full repository validation.
3. Check migrations and compatibility notes.
4. Check security-sensitive dependency changes.
5. Update changelog or release notes if the repository uses them.
6. Confirm generated artifacts and checksums.
7. Tag only after the commit intended for release is pushed.

## Compatibility

- Never change persisted formats without migration notes.
- Keep examples and fixtures for old formats.
- For `workspace-spec`, distinguish draft, experimental, and stable fields.
- For templates, record source, license, compiler version, and checksum.
- For skills, treat `SKILL.md` frontmatter changes as trigger-surface changes.

## Changelog Tone

Prefer concrete entries:

- Added `syntavell-git-commit` skill for Git workflows.
- Changed Workspace export manifest version to `0.2`.
- Fixed evidence anchor migration for changed source snapshots.

Avoid vague entries like "misc improvements".
