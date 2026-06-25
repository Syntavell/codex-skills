# Security Checklist

## Data and Privacy

- Are research contents encrypted at rest where required?
- Are SQLite WAL files, caches, thumbnails, OCR images, compiler outputs, logs, and crash dumps covered?
- Are local absolute paths redacted from logs and exported diagnostics?
- Does the UI preview remote provider data boundaries?
- Are provider keys stored through the intended secret store?

## Key Management

- Are key encryption keys, workspace master keys, object keys, database keys, ledger payload keys, and derived search keys separated?
- Is recovery explicit and tested?
- Is key rotation possible without corrupting existing data?
- Are forgotten recovery keys handled honestly in UX and docs?

## AI and Prompt Injection

- Is external content marked as untrusted data?
- Can model output trigger tools or writes without user confirmation?
- Are tool parameters schema-validated?
- Can a document or webpage cause cross-workspace access?
- Are prompts free of real secrets?

## Parsers and Compilers

- Are untrusted PDFs, webpages, templates, Typst, LaTeX, and archives isolated?
- Are time, memory, process, network, and filesystem limits present?
- Is shell escape disabled by default?
- Are plaintext intermediates cleaned?
- Are parser versions recorded for provenance?

## Sync and Cloud

- Is server state prevented from becoming the only source of truth?
- Are only encrypted objects and signed operations synchronized when in encrypted mode?
- Are metadata leaks considered?
- Are device registration and revocation explicit?

## Supply Chain

- Are dependency updates reviewed for licenses and security?
- Are GitHub Actions pinned sensibly?
- Are release artifacts signed or planned for signing?
- Is SBOM generation considered for desktop releases?
- Are templates traced to their source and license?

## Reporting Format

Use:

```text
Severity: critical | high | medium | low
Asset:
Boundary:
Issue:
Impact:
Evidence:
Fix:
Residual risk:
```
