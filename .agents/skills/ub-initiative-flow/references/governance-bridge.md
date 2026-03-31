# Governance Bridge

Use this reference when the initiative workflow should coordinate with
ub-governance.

## Positioning

`ub-initiative-flow` owns execution structure.
`ub-governance` owns validation depth, evidence rigor, and governance semantics.

Do not merge the two domains into one skill.

## Integration Levels

### Level 0: No Governance Bridge

Use the initiative workflow alone.

Appropriate when:

1. the repository wants planning discipline but not formal governance
2. validation is lightweight or locally defined

### Level 1: Light Governance Bridge

Use initiative scaffolding plus governance-shaped sections.

Appropriate when:

1. the repo wants explicit validation, exceptions, and final audit language
2. ub-governance concepts help, but structured ADR or claim workflows are not
   required

Recommended coordination:

1. use governance-aligned closeout sections
2. reference repo validation commands explicitly
3. ask whether follow-up audits or refactors are wanted at final audit time

### Level 2: Full Governance Bridge

Use initiative scaffolding plus explicit ub-governance coordination.

Appropriate when:

1. the repository uses evidence levels, profile selection, or ADR alignment
2. the final audit should map cleanly to governance review expectations

Recommended coordination:

1. declare the governance profile explicitly
2. load ub-governance for evidence or audit work
3. map initiative validation to repository governance commands
4. record bounded exceptions using the canonical governance exception metadata

## Mapping Guidance

Treat initiative gates and governance gates as adjacent but distinct:

- initiative gates answer whether the work package is ready to progress
- governance gates answer whether repository-level controls were satisfied

Use both when needed, but do not collapse one into the other.