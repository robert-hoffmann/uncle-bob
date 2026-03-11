# MADR-Based ADR Template (Governance v2)

Use this template for new ADR files in `docs/adr/`.

Recommended filename: `NNNN-short-kebab-title.md`.

```markdown
---
id: ADR-0001
title: Short decision title
status: accepted
date: 2026-03-04
supersedes: []
tags:
  - governance
  - auth
paths:
  - .github/workflows/
  - src/auth/
constraints_refs:
  - docs/architecture/constraints.md#governance
source_claims:
  - CLM-20260001
review_by: 2026-06-30
---

# ADR-0001: Short decision title

## Status

Accepted

## Context

What changed, why now, and what constraints apply.

## Decision

Concrete architecture and governance rule chosen.

## Options Considered

### Option A

Pros:

- ...

Cons:

- ...

### Option B

Pros:

- ...

Cons:

- ...

## Consequences

### Positive

- ...

### Negative

- ...

## Invariants

- Non-negotiable rule 1
- Non-negotiable rule 2
- Non-negotiable rule 3

## Evidence and Links

- PR: ...
- Benchmarks/tests: ...
- Incident/risk note: ...
```

## Status Lifecycle

Allowed status values:

1. `proposed`
2. `accepted`
3. `deprecated`
4. `superseded`

Use `supersedes` to link transitions explicitly.
