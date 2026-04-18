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

## 2) Ordinary Operator Fast Path

Use this quick triage before reaching for heavier governance machinery:

1. ordinary initiative work that stays inside one workflow-backed initiative:
   keep the durable record in `prd.md`, `roadmap.md`, `sprint.md`,
   `decision-log.md`, `closeout.md`, and sprint `evidence/`
2. repository-wide durable decisions, defaults, or shared architecture
   changes: escalate to Level 2 and align the repository ADR surfaces
3. explicit high-risk or repository-governance runs: treat the work as
   escalated governance and apply ADR and claim controls only as that run
   requires

Practical intent:

1. workflow artifacts are the default answer for ordinary initiative work
2. ADR machinery is the escalation path, not the starting point
3. claim-register checks matter only when blocking rationale depends on claims

## 3) Gate Decision Inputs

1. required artifact inventory for scope
2. selected governance level and whether workflow-backed initiative artifacts
   are in play
3. high-risk path matches
4. ADR registry alignment state when ADR escalation applies
5. claim-register status for blocking rationale
6. active exception validity from governance contract

## 4) Workflow-Native Decision-Memory Rules

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

Ordinary initiative example:

1. a sprint updates local workflow or documentation guidance for one approved
   initiative
2. durable memory stays in the initiative workflow artifacts and sprint-local
   evidence
3. ADR alignment and claim-register checks are not required by default

## 5) ADR Escalation Rules

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

Repository-wide durable-decision example:

1. a shared repository default or cross-initiative governance contract changes
2. workflow artifacts can still record execution context, but repository ADR
   alignment becomes the durable decision-memory owner
3. claim-register checks apply only if blocking rationale for the gate depends
   on claims

## 6) Claim-Register Trigger Rules

Use the claim register when a governance decision needs claim confidence to
support a blocking outcome.

Typical triggers:

1. a Level 2 or high-risk gate relies on claims about compatibility, security,
   evidence coverage, or policy conformance
2. a pass, fail, or blocked result cites a claim as part of the blocking
   rationale
3. an exception or waiver remains acceptable only because supporting claims
   stay verified or explicitly bounded

Do not require claim-register work by default for:

1. ordinary Level 1 workflow-backed initiative records
2. descriptive examples or non-blocking explanatory prose
3. decisions that can be justified directly from deterministic artifacts
   without claim confidence

High-risk-governance example:

1. an explicit high-risk run touches governed paths and the gate rationale
   depends on claims about alignment or residual risk
2. ADR alignment or active waiver is required
3. claim-register validation output becomes part of the blocking evidence set

## 7) Claim-Verification Rules

1. `verified`: allowed for blocking rationale
2. `partial`: allowed for blocking rationale only with active bounded exception
3. `unverified`: not allowed for blocking rationale

## 8) Gate Decision Process

1. inventory required artifacts for the selected governance level
2. verify deterministic presence and freshness
3. decide whether workflow-native decision memory is sufficient or ADR
   escalation is required
4. evaluate ADR alignment state when escalation applies
5. evaluate claim-confidence constraints
6. evaluate exception validity
7. declare `pass`, `fail`, or `blocked` with explicit reasons and artifact
   paths
