# ADR and RFC Templates

## ADR Template

```markdown
# ADR-0001: Short Decision Title

Status: proposed | accepted | superseded
Date: YYYY-MM-DD
Repository: Syntavell/<repo>

## Context

What forced a decision now?

## Decision

What is the chosen direction?

## Alternatives Considered

- Option A: tradeoff
- Option B: tradeoff

## Consequences

What becomes easier, harder, or impossible?

## Security and Privacy Notes

What assets, trust boundaries, or failure modes are affected?

## Validation

How will this decision be tested or reviewed?
```

## RFC Template

```markdown
# RFC: Short Proposal Title

Status: draft
Repository: Syntavell/<repo>
Authors:
Created: YYYY-MM-DD

## Summary

One concise paragraph.

## Motivation

Why this matters now.

## Goals

- ...

## Non-Goals

- ...

## Proposal

Detailed design.

## Compatibility

Schema, migration, API, template, provider, or workspace compatibility.

## Security and Privacy

Assets, trust boundaries, abuse cases, and mitigations.

## Rollout

Implementation phases and validation.

## Open Questions

- ...
```

## ADR vs RFC

- Use ADR for decisions already made or ready to accept.
- Use RFC for proposals that need design review.
- Do not use ADRs as changelogs.
- Do not leave accepted decisions only in chat or issue comments.
