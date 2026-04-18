# MADR-Based ADR Template (Governance v2)

Use this template for new ADR files in `docs/adr/`.

Use ADRs for repository-level or cross-initiative decisions that remain durable
beyond one workflow-backed initiative. Do not turn routine sprint decisions
into repository ADRs when workflow artifacts already provide the right
operational record.

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

Lifecycle guidance:

1. use `proposed` while the decision is still being reviewed
2. use `accepted` once the repository-level decision is the active rule
3. use `superseded` when a newer ADR explicitly replaces this one; update the
   newer ADR's `supersedes` field and keep the older ADR for historical context
4. use `deprecated` when the decision is no longer recommended but is not
   cleanly replaced by one direct successor ADR

Supersession workflow:

1. create the new ADR with its own identifier and active decision text
2. set the new ADR's `supersedes` field to the older ADR id or ids
3. update the older ADR status to `superseded` when the replacement is active
4. do not delete old ADRs; they remain part of repository decision memory
