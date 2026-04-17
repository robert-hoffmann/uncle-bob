# Sprint 03 Evidence

## Before And After Sprint Artifact Example

Before Sprint 03, the canonical sprint template was a generic placeholder shell
with sections such as:

```md
## Summary

Replace with the sprint summary.

## Scope

1. Replace with the first in-scope item.
2. Replace with the second in-scope item.
```

That shape was safe for scaffolding, but it did not turn roadmap data into an
execution-ready sprint PRD.

After Sprint 03, the template begins with machine-derived context and keeps the
human-authored reasoning sections separate:

```md
## Machine-Derived Context

- Sprint: `Sprint 01 - Define Contract`
- Goal: Define the contract so every later sprint inherits one stable workflow baseline
- Depends on: `none`
- Validation focus: Contract review with lifecycle and gate consistency checks
- Evidence folder: `./sprints/01-define-contract/evidence/`
- Planned subtasks:
- [ ] Draft the contract and capture the shared gate vocabulary
- [ ] Review the contract with stakeholders
```

The helper now renders that structure from roadmap metadata through the explicit
`prepare-sprints` command.

## Pending Handoff Marker Semantics

Allowed pending handoff markers now use the explicit prefix
`PENDING_HANDOFF:`.

They are reserved for fields that legitimately depend on prior closeout truth,
for example:

```md
3. PENDING_HANDOFF: Review `Sprint 01 - Define Contract` closeout and carry forward any blockers, validation changes, or repository-truth updates before execution begins.
```

Blocking placeholders and pending handoff markers are no longer treated as the
same thing:

1. `REPLACE_...` and `Replace with ...` remain blocking placeholders.
2. `PENDING_HANDOFF:` is allowed in prepared sprint PRDs when a previous sprint
   closeout still needs to flow forward.

## Deterministic Versus Authored Boundary

Deterministic helper-owned behavior in Sprint 03:

1. parse roadmap sprint title, path, goal, dependencies, validation focus,
   subtasks, and evidence folder
2. materialize sprint directories when needed
3. render machine-derived sprint context into `sprint.md`
4. preserve already-prepared sprint PRDs that no longer contain blocking
   placeholders

Human- or agent-authored behavior intentionally left outside the helper:

1. sprint-specific repository truth notes
2. chosen path and rejected alternative analysis
3. affected-area reasoning beyond roadmap metadata
4. sprint-specific validation commands beyond the roadmap baseline

That boundary preserves conservative deterministic scaffolding while still
producing resumable sprint PRDs before execution begins.
