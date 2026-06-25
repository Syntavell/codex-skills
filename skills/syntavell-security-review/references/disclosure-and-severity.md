# Disclosure and Severity

## When to read

Read this for severity calls, vulnerability reports, public disclosure wording, security policy edits, and release-blocking security decisions.

## Severity Guide

Critical:

- plaintext exposure of workspace keys or provider keys;
- remote code execution through parser, compiler, template, plugin, or updater path;
- silent upload of private research content at broad scope;
- corruption or unrecoverable deletion of encrypted workspaces without warning.

High:

- bypass of workspace boundaries;
- unsafe Tauri command exposing filesystem, subprocess, network, or secrets;
- broken encryption or recovery flow that exposes or loses protected data;
- prompt injection path that performs high-risk writes without confirmation.

Medium:

- sensitive metadata leaks;
- incomplete sandboxing with limited impact;
- missing audit record for AI or compiler operations;
- supply-chain weakening without immediate exploit path.

Low:

- unclear wording, missing warning, incomplete logging redaction in low-risk context, or hardening improvement.

## Public Handling

- Do not publish exploit details before a fix or mitigation is available.
- Prefer private GitHub vulnerability reporting for actionable vulnerabilities.
- Public issues may discuss general hardening only when they do not reveal exploit steps or sensitive data.
- Security policy text must avoid promising response times or support windows the project cannot meet.

## Review Language

Be concrete and bounded. Avoid vague statements like "make this secure." Name the asset, boundary, and failure mode.

Do not publish exploit steps or proof-of-concept details before a mitigation is available and the user explicitly authorizes disclosure handling.
