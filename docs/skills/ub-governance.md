# UB Governance

Source: `.agents/skills/ub-governance/SKILL.md`

`ub-governance` is the control skill. It decides how much evidence, testing
scrutiny, exception handling, ADR alignment, release discipline, or gate
structure a change needs.

For the lean versus advanced model, read the
[UB Governance deep dive](/deep-dives/ub-governance).

## Core Principles

- Default to the lean profile unless advanced governance is explicitly
  justified.
- Keep gate states deterministic: `pass`, `fail`, or `blocked`.
- Treat ordinary Level 1 workflow-backed work as satisfied by workflow
  artifacts unless risk or scope requires more.
- Escalate ADR and claim machinery only for durable, repository-wide,
  high-risk, or explicitly governed decisions.
- Keep bounded exceptions owned, time-limited, and follow-up driven.
- For behavior-changing work, prefer behavior-first TDD: red, green, refactor,
  with regression-first proof for reported defects.
- Use testing-signal review to reject low-value tests without making every
  realism concern a hard blocker.

## Behavior In Practice

- Selects a governance mode first: repository controls, testing posture,
  evidence decisions, core contract semantics, or a full governance audit.
- Defaults to `lean`. Advanced governance is an explicit escalation, not a
  background tax on ordinary work.
- Uses workflow artifacts as the durable record for ordinary Level 1 work,
  then escalates to ADR or claim machinery only for repository-wide,
  high-risk, Level 2, or explicitly governed decisions.
- Applies deterministic gate language: `pass`, `fail`, or `blocked`, with
  traceable artifact paths rather than vague approval language.
- Reviews test quality with named signals. Type redundancy, interaction-only
  assertions, pass-through tests, and happy-path-only suites are blocking
  signals; internal-detail bias is warning-only; functional-realism concerns
  scale with risk.
- Pushes tests toward DAMP readability over over-DRY helper abstraction when
  duplication makes scenario setup, trigger, and observed outcome easier to
  understand.
- Uses the Prove-It defect pattern: reproduce the reported defect with a
  failing regression test, confirm the failure path, make the smallest fix,
  then rerun narrow and broader validation.
- Checks RED realism before implementation. A red test is not useful if it
  mocks the behavior under review, encodes the answer in a fake, or would pass
  if the real implementation disappeared.
- Keeps exceptions bounded with owner, rationale, creation date, expiration
  date, and follow-up. An exception is not an informal permission slip.
- Distinguishes repository governance from this repository's maintenance
  scripts. Skill catalog checks, README drift checks, and local path integrity
  are factory controls, not portable governance by default.

## Reference Highlights

- `.agents/skills/ub-governance/references/profile-model.md`: lean and
  advanced governance profiles, escalation triggers, and default expectations.
- `.agents/skills/ub-governance/references/testing-policy-and-signals.md`:
  behavior-first TDD posture, blocking test anti-patterns, warning signals,
  functional-realism guidance, suite-balance rules, and flake policy.
- `.agents/skills/ub-governance/references/decision-memory-and-claims.md`:
  when workflow artifacts are enough, when ADR escalation is justified, and
  when claim-register evidence becomes part of a blocking rationale.
- `.agents/skills/ub-governance/references/evidence-baseline.md`: evidence
  expectations for higher-risk paths, validation records, and freshness.
- `.agents/skills/ub-governance/references/gate-and-report-contract.md`:
  canonical gate types, gate states, report sections, and domain extensions.
- `.agents/skills/ub-governance/references/exception-contract.md`: bounded
  exception metadata, common exception templates, expiration requirements, and
  follow-up rules.

## Progressive Disclosure

The main skill handles ordinary governance routing. Deeper references load by
mode and risk: testing policy for test-signal review, evidence references for
Level 2 or high-risk work, repository references for repository controls, and
schema files only when concrete governance data is being authored or checked.

## Common Invocation Examples

- “Use `ub-governance` to decide whether this needs an ADR.”
- “Check whether this feature should follow red/green/refactor.”
- “Review this test plan for low-signal testing patterns.”
- “Tell me if this test is too DRY and hides the behavior.”
- “Check whether this exception is bounded enough.”
- “Explain the lean versus advanced governance choice.”
- “Does this change need claim evidence or are workflow artifacts enough?”

## Boundaries

Do not use it as a general workflow planner. Use `ub-workflow` to choose
delivery lanes, PRD shape, sprint flow, and stop-resume behavior.

## Tradeoffs

Strength: keeps ordinary work lightweight while preserving escalation paths for
risk, auditability, and durable decisions.

Cost: advanced governance adds overhead and should be activated deliberately.

## Deep Dive

See [UB Governance deep dive](/deep-dives/ub-governance) for profile selection,
governance modes, gate states, and bounded exceptions.
