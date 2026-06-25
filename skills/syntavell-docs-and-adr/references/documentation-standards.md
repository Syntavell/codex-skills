# Documentation Standards

## When to read

Read this before creating, moving, reorganizing, or reviewing Syntavell documentation.

## Source States

Use these labels consistently:

- `current`: what the repository currently does.
- `accepted`: a decision or policy that has been approved.
- `preferred`: a direction to favor when future implementation allows it.
- `proposed`: an RFC or draft that still needs review.
- `fallback`: a deliberate alternative when the preferred path is unavailable.
- `illustrative`: an example that must not be treated as a required structure.

## Repository Placement

- `Syntavell/syntavell`: product vision, PRDs, architecture, UI workflows, MVP plans, app implementation notes.
- `Syntavell/workspace-spec`: workspace schema, vault format, operation log, provenance, sync, migrations, validation fixtures.
- `Syntavell/templates`: template manifests, Venue Profiles, compile locks, publisher source notes, template validation fixtures.
- `Syntavell/codex-skills`: reusable agent workflows and engineering rules.
- `Syntavell/.github`: organization profile and community health defaults.

## Formal Docs

Formal docs should include:

- status;
- date;
- owner or repository;
- scope;
- non-goals;
- decisions;
- consequences;
- validation or acceptance criteria;
- references.

Do not mark decisions accepted unless the user or an accepted ADR/spec provides that status.

Use Typst when the document benefits from stable PDF output or formal review.

## Contributor Docs

Contributor docs should answer:

- what the repository is for;
- what is in and out of scope;
- how to set up locally;
- how to run validation;
- how to contribute safely;
- where security issues go;
- what is not yet stable.

## Generated Artifacts

When tracking generated PDFs:

- keep source and output in the same commit;
- compile from source during verification;
- update `SHA256SUMS` if present;
- do not hand-edit generated outputs.

## Language

- Use precise, direct wording.
- Prefer English for public engineering conventions and commit messages.
- Chinese docs are acceptable for internal product thinking, but keep repository entry points accessible to external contributors when the repository is public.
