# Documentation Standards

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
