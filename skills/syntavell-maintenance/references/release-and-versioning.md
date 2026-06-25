# Release and Versioning

## When to read

Read this for release preparation, version changes, changelog work, schema compatibility, template versioning, and submodule version decisions.

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
2. Identify the version source: manifest, tag, changelog, package metadata, or app bundle.
3. Run full repository validation.
4. Check migrations and compatibility notes.
5. Check security-sensitive dependency changes.
6. Update changelog or release notes if the repository uses them.
7. Confirm generated artifacts, checksums, signatures, and provenance.
8. Prepare a rollback plan.
9. Tag only after the commit intended for release is pushed and publication is authorized.

## Release Readiness Result

Report:

```text
Version:
Commit:
Artifacts:
Validation:
Security review:
Compatibility notes:
Rollback:
Publication gates:
Ready: yes | no
```

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
