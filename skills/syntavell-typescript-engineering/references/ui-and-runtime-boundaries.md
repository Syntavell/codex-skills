# UI and Runtime Boundaries

## When to read

Read this for UI, Reader, Writer, platform runtime, browser/Tauri boundary, and privacy UI work.

## UI Principles

Syntavell is a research workspace, not a landing page.

- Build the usable work surface first.
- Prefer quiet, dense, scan-friendly UI for researchers.
- Keep common workflows fast: import, read, anchor evidence, review claims, synthesize, write, compile, export.
- Make keyboard navigation and screen-reader semantics part of the first implementation.
- Keep CJK, mixed-language titles, formulas, and long citations in mind.

## Reader

Reader work should preserve:

- page and region anchors;
- text quotes and hashes;
- outline and section paths;
- source snapshot identity;
- repair state when a source version changes.

PDF.js is display and selection infrastructure, not the sole scholarly parser.

## Writer

Writer work should preserve:

- one primary engine per manuscript: Typst or LaTeX;
- shared bibliography, evidence, figures, tables, and workflow history;
- patch-based AI edits;
- compile diagnostics and output hashes;
- Venue Profile validation.

## Runtime Interfaces

Business logic should depend on interfaces such as:

```ts
interface PlatformRuntime {
  files: FileService;
  secrets: SecretService;
  database: DatabaseService;
  tasks: BackgroundTaskService;
  llmTransport: LLMTransport;
  compiler: CompilerService;
  notifications: NotificationService;
}
```

Browser and Tauri implementations can differ, but product workflows should not call raw platform APIs directly.

If the current repository does not yet expose a runtime interface, report that boundary gap instead of inventing a new abstraction without user-visible need.

## Privacy UI

Before remote processing, show:

- exact pages, chunks, selected text, files, or metadata being sent;
- destination provider or relay;
- what is not sent;
- whether the request can be logged by the provider;
- local-only alternatives when available.
