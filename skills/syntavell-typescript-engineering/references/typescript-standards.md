# TypeScript Standards

## When to read

Read this for any TypeScript implementation or review. The current package manager files and workspace manifests are authoritative.

## Package Responsibilities

Illustrative package boundary candidates:

- `ui`: design system primitives and shared components;
- `domain`: core entities, invariants, schemas, and pure workflow logic;
- `reader`: PDF/web/code/dataset reading workflows and evidence anchors;
- `editor`: source editor integration and patch application;
- `workflows`: AI workflow definitions, structured outputs, and provenance;
- `providers`: LLM, embedding, local model, and relay adapters;
- `metadata`: DOI/arXiv/Crossref/Semantic Scholar/Unpaywall adapters;
- `retrieval`: parsing chunks, indexes, reranking, evidence retrieval;
- `sync`: encrypted object and operation synchronization protocol clients;
- `platform`: browser, desktop, worker, and API runtime interfaces.

These are target boundary examples, not required package names. Do not create a package or directory only because it is listed here.

## Types and Schemas

- Keep wire formats and persisted formats versioned.
- Use schema validators for untrusted JSON and provider responses.
- Model state machines as discriminated unions.
- Avoid `any`; use `unknown` at trust boundaries and validate before use.
- Keep IDs opaque and typed where possible.

## AI Workflows

- Store workflow IDs and versions.
- Record provider, requested model, reported model, parser version, chunker version, prompt hash, retrieved chunk IDs, token usage, cost estimate, and user decision.
- Require evidence for factual claims.
- Do not silently upgrade generated content into verified content.
- Present AI patches for user acceptance instead of rewriting whole files by default.

## Provider Adapters

Provider code must account for:

- streaming support;
- structured output support;
- tool calling support;
- embeddings support;
- vision and native PDF support;
- file upload support;
- context limits;
- CORS and browser-direct limitations.

Do not key product behavior only on model names.

## Testing

Prefer:

- unit tests for pure domain logic;
- contract tests for provider adapters;
- fixture tests for metadata and parser behavior;
- UI interaction tests for Reader/Writer workflows;
- regression tests for evidence anchors and AI citation precision.

When package scripts are absent, identify the expected script names instead of inventing local-only tooling.

Classify failures as caused by the change, pre-existing, environment, or unsupported. Do not hide pre-existing failures by claiming validation passed.
