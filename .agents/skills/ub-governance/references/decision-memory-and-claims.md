# Decision-Memory and Claim Policy

This file defines the decision-memory boundary for workflow-backed work,
repository ADR escalation, and claim governance.

## 1) Decision-Memory Model

Use the lightest durable record that still matches the decision's scope.

Level model:

1. Level 0 or quick edits: keep governance lightweight and use local change
   context plus explicit validation notes when needed.
2. Level 1 workflow-backed initiatives: treat `prd.md`, `roadmap.md`,
   per-sprint `sprint.md`, `closeout.md`, sprint `evidence/`, and bounded
   initiative `research/` or `exceptions/` as the default operational record.
3. Level 2 or repository-level governance: escalate into `docs/adr/`,
   ADR registry alignment, waivers, and claim checks when the decision is
   durable beyond one initiative or changes repository-wide contracts.

## 2) Gate Decision Inputs

1. required artifact inventory for scope
2. selected governance level and whether workflow-backed initiative artifacts
   are in play
3. high-risk path matches
4. ADR registry alignment state when ADR escalation applies
5. claim-register status for blocking rationale
6. active exception validity from governance contract

## 3) Workflow-Native Decision-Memory Rules

For Level 1 workflow-backed work:

1. the primary operational record lives in workflow artifacts rather than
   repository ADRs by default
2. important sprint- or initiative-level reasoning must be durable enough that
   another operator can understand what changed, why it changed, which
   alternative was rejected, and what was explicitly deferred
3. sprint `evidence/` is the default evidence location for sprint-scoped proof
   and should stay closer to the work than initiative-root summaries
4. initiative-root `research/` and `exceptions/` are supporting surfaces, not
   generic dumping grounds

## 4) ADR Escalation Rules

Escalate from workflow-native decision memory into repository ADRs when any of
these are true:

1. the decision is durable beyond one initiative
2. the decision changes repository-wide contracts, defaults, or shared
   architecture expectations
3. a Level 2 or explicit repository-governance run requires ADR alignment
4. high-risk path changes are being evaluated under the ADR gate or equivalent
   escalated governance flow

When ADR escalation applies:

1. high-risk path changes require ADR alignment or active ADR waiver
2. confidence/release completion cannot rely on expired waivers
3. structural/high-risk runs require non-empty `decision.adrRefs` in the
   validation record

## 5) Claim-Verification Rules

1. `verified`: allowed for blocking rationale
2. `partial`: allowed for blocking rationale only with active bounded exception
3. `unverified`: not allowed for blocking rationale

## 6) Gate Decision Process

1. inventory required artifacts for the selected governance level
2. verify deterministic presence and freshness
3. decide whether workflow-native decision memory is sufficient or ADR
   escalation is required
4. evaluate ADR alignment state when escalation applies
5. evaluate claim-confidence constraints
6. evaluate exception validity
7. declare `pass`, `fail`, or `blocked` with explicit reasons and artifact
   paths
