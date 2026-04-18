# Governance Bridge

Use this reference when the initiative workflow should coordinate with
ub-governance.

## Positioning

`ub-workflow` owns execution structure.
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
3. treat `prd.md`, `roadmap.md`, per-sprint `sprint.md`, `closeout.md`, sprint
   `evidence/`, and bounded initiative `research/` or `exceptions/` as the
   default operational record
4. keep repository ADR machinery optional unless a repository-level decision or
   explicit escalation trigger applies
5. ask whether follow-up audits or refactors are wanted at final audit time
6. record the selected bridge level in `README.md` or `prd.md`

### Level 2: Full Governance Bridge

Use initiative scaffolding plus explicit ub-governance coordination.

Appropriate when:

1. the repository uses evidence levels, profile selection, or ADR alignment
2. the final audit should map cleanly to governance review expectations
3. a decision is durable beyond one initiative or changes repository-wide
   contracts

Recommended coordination:

1. declare the governance profile explicitly
2. load ub-governance for evidence or audit work
3. map initiative validation to repository governance commands
4. record bounded exceptions using the canonical governance exception metadata
5. record governance bridge level and profile in `README.md`, `prd.md`, and
   the final retained note
6. escalate into `docs/adr/` only for repository-level or cross-initiative
   durable decisions, not for routine sprint execution choices

## Recording Locations

When governance coordination is active, record it durably in these places:

1. `README.md`: current governance bridge level and profile
2. `prd.md`: governance rationale, validation expectations, and documentation touch points
3. `closeout.md`: initiative workflow gate state plus governance gate type when applicable
4. `retained-note.md`: final governance bridge summary, validation baseline, and exception or ADR references

## Escalation Triggers

Escalate from Level 0 to Level 1 when:

1. explicit validation language or bounded exceptions are needed
2. the final audit should use governance-shaped closeout language

Escalate from Level 1 to Level 2 when any of these are true:

1. evidence levels, profile selection, or ADR alignment are required
2. high-risk path changes require durable governance reasoning
3. confidence or release-style audit mapping is needed
4. governance exceptions must be recorded with canonical metadata
5. the decision is durable beyond one initiative or changes repository-wide
   contracts

Use the `lean` profile by default.

Escalate to `advanced` only with explicit rationale.

## Exception Records

When Level 1 or Level 2 governance uses bounded exceptions:

1. store them under `./exceptions/`
2. use sortable dated filenames such as `YYYY-MM-DD-<slug>.yaml`
3. populate the canonical fields from ub-governance's exception contract
4. reference the exception record path from `closeout.md` and `retained-note.md`

## Mapping Guidance

Treat initiative gates and governance gates as adjacent but distinct:

- initiative gates answer whether the work package is ready to progress
- governance gates answer whether repository-level controls were satisfied

Use both when needed, but do not collapse one into the other.

Treat workflow-native decision memory and repository ADRs as adjacent but
distinct as well:

- workflow artifacts are the default operational record for Level 1 work
- repository ADRs are the escalated durable record for Level 2 or
  repository-wide decisions
