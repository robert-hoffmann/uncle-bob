---
name: ub-governance
description: >-
   Use this skill when the user wants to review governance rules, check testing
   posture, decide whether ADR or claim evidence is needed, evaluate
   repository or release controls, or understand exception and gate behavior;
   when the task involves governance modes, test-signal review, evidence
   levels, or decision-memory boundaries; or when they ask whether work needs
   governance escalation. Do not use it for workflow planning, framework
   implementation, or this repository's repo-maintenance catalog, path, and
   skill-integrity checks.
metadata:
  desktop-portfolio-help-topics: "overview,evidence,testing,repository,core,glossary,combos,invoke"
  desktop-portfolio-help-aliases: "repo=repository"
  desktop-portfolio-help-default-topic: "overview"
---

# UB Governance

## Overview

Use this skill as the owner for governance in the current repository or project
where it is adopted.

This skill should stay lean for ordinary workflow-backed work and should only
activate heavier controls when the selected mode or scope actually requires
them.

## Embedded Contract

These rules are the base contract of this skill and must not depend on a
secondary document to be applied correctly.

1. Default to the `lean` profile unless the user explicitly requests
   `advanced` with rationale.
2. Use only these governance gate states: `pass`, `fail`, `blocked`.
3. Every bounded exception must include `owner`, `rationale`, `created_at`,
   `expires_at`, and `follow_up`.
4. For ordinary Level 1 workflow-backed work, treat workflow artifacts as the
   default durable operational record.
5. Escalate to ADR and claim machinery only when the decision is durable
   beyond one initiative, repository-wide, high-risk, or explicitly governed
   at Level 2.
6. Keep blocking governance decisions tied to deterministic artifacts.

## Operating Modes

1. `repository mode`: repository hygiene, CI and release governance,
   branch or ruleset policy, deterministic tooling
2. `testing mode`: behavior-first TDD governance and low-signal testing
   anti-pattern review
3. `evidence mode`: evidence lifecycle, ADR alignment, claim verification,
   and gate readiness
4. `core-contract mode`: shared profile, gate, exception, and report
   semantics
5. `full governance audit mode`: run repository, testing, and evidence checks
   in one deterministic sequence

## Testing Signal Model

Use descriptive names in normal guidance.
Keep the numeric IDs as stable internal codes for tooling and compatibility.

Blocking signals:

1. `Type Redundancy` (`TG001`): runtime tests that restate type-system
   guarantees
2. `Interaction Without Outcome` (`TG002`): interaction assertions without
   observable outcome assertions
3. `Pass-Through Test` (`TG003`): trivial getter or setter pass-through tests
4. `Happy-Path-Only Suite` (`TG004`): repeated happy-path focus without
   boundary or error representation

Warning-only signal:

1. `Internal-Detail Bias` (`TG005`): probable verification of internal details
   over public behavior

## Load References By Trigger

Use these load tiers literally.
If a trigger is not active, do not read the reference just because it exists.

- `[phase:decision-boundary]` Read
  `references/decision-memory-and-claims.md` when deciding whether workflow
  artifacts are sufficient or ADR and claim escalation is required.
- `[phase:testing-mode]` Read
  `references/testing-policy-and-signals.md` when reviewing testing policy or
  applying the testing anti-pattern model.
- `[phase:testing-mode]` Read `references/execution-playbook.md` when the task
  is about TDD execution order, regression-first bug fixing, or testing
  workflow hygiene.
- `[phase:command-or-audit]` Read `references/governance-commands.md` when the
  user asks how to run checks or an audit path is being executed.
- `[edge:glossary-or-normalization]` Read `references/vocabulary.md` only when
  glossary help or wording normalization matters.
- `[edge:repository-mode]` Read `references/repository-baseline.md`,
  `references/github-implementation-playbook.md`, and
  `references/release-please-playbook.md` only when repository governance is
  actually in scope.
- `[edge:evidence-level-2]` Read `references/evidence-baseline.md`,
  `references/evidence-lifecycle.md`, `references/evidence-artifact-taxonomy.md`,
  `references/ci-artifact-contract.md`, and `references/stack-baseline.md`
  only when explicit Level 2 or evidence-heavy governance is active.
- `[edge:schema-or-data]` Read `references/high-risk-paths.yaml`,
  `references/agent-validation-record.schema.json`,
  `references/adr-registry.schema.json`,
  `references/claim-register.schema.json`, and
  `references/adr-template-madr.md` only when those concrete artifacts are
  being authored or validated.
- `[edge:authoring-conventions]` Read `../ub-authoring/references/authoring-conventions.md`
  only when adjusting routing or shared authoring structure.

## Core Workflow

1. Detect the requested governance mode and evaluated scope from repository
   truth.
2. Select profile: `lean` by default, `advanced` only with explicit rationale.
3. For ordinary workflow-backed work, prefer the Level 1 fast path and keep
   the durable record in workflow artifacts.
4. Escalate only when the decision scope, risk, or explicit governance run
   requires it.
5. Run the selected mode's controls and keep outputs deterministic.
6. Apply bounded exceptions only through the canonical exception contract.
7. Emit a traceable gate outcome with artifact paths.

## Quick Examples

1. `Does this auth change need an ADR or claim work?`
   Use `evidence mode` and the decision-boundary reference to decide whether
   ordinary workflow artifacts are sufficient or whether the change is truly
   repository-wide, high-risk, or Level 2.
2. `Are these tests mostly checking mock calls without user-visible outcome
   assertions?`
   Use `testing mode`, apply the test-signal model, and treat likely `TG002`
   findings as blocking only when the suite is asserting interaction without
   externally observable outcome.
3. `Show me the repo-maintenance checks for README, AGENTS, and skill schema.`
   Do not route that through governance. Those checks belong to the
   host repository's own maintenance/check surface.

## When Not To Use

- Do not use this skill for workflow intake, PRD shaping, roadmap generation,
  sprint preparation, or resumable initiative orchestration; defer those to
  `ub-workflow`.
- Do not use this skill as the primary surface for framework-specific
  implementation guidance when the task is about code changes rather than
  governance policy or gate semantics.
- Do not use this skill as a generic documentation-normalization layer when
  `ub-quality` is the actual owner of the task.

## Mode Workflows

### Repository Mode

1. verify repository baseline artifacts and deterministic tooling policy
2. verify CI, permissions, and merge-gate controls
3. verify release policy with Conventional Commits and `release-please`

### Testing Mode

1. detect stack and test runner
2. treat reported defects as regression-first work before code fixes are
   accepted
3. enforce `TG001` through `TG004` as blocking and `TG005` as warning-only
4. require behavior-first TDD flow for behavior-changing work
5. keep testing guidance readable, boundary-aware, and deterministic without
   turning advisory guidance into new gates

### Evidence Mode

1. classify `changeType`, `evidenceLevel`, and `profile`
2. detect high-risk path impact when the scope requires it
3. choose the lightest durable record that matches the decision scope
4. treat workflow-backed initiative artifacts as the default operational record
   for ordinary Level 1 work
5. escalate to ADR alignment only when Level 2, repository-wide durable
   decisions, or explicit high-risk governance applies
6. require claim-register validation only when blocking rationale depends on
   claims
7. validate required artifacts and freshness for the selected path

### Core-Contract Mode

1. apply canonical profile, gate, exception, and report semantics
2. normalize status language and report contract usage
3. reject duplicate or conflicting schema definitions

### Full Governance Audit Mode

1. execute `repository mode`
2. execute `testing mode`
3. execute `evidence mode`
4. consolidate output under canonical report sections

## Rules

- Keep defaults lean and activate advanced controls explicitly.
- Do not imply that repository ADR machinery is the default record for
  ordinary Level 1 workflow-backed work.
- Exception metadata must stay bounded, explicit, and time-limited.
- Do not duplicate canonical contract definitions across files when the main
  skill already embeds the short rule.
- Repository-maintenance tooling is not automatically the same thing as lean
  governance guidance.

## Output Requirements

When producing non-trivial governance output, include:

1. `environment_note`
2. `scope_note`
3. `decision_note`
4. `gate_note`
5. `exception_note`
6. `validation_note`

Add mode-specific sections when applicable:

1. `quality_gate_note` for testing mode
2. `evidence_inventory` and `claim_note` for evidence mode

## Completion Checklist

- Selected mode is explicit.
- Profile choice is explicit (`lean` or `advanced`).
- The ordinary Level 1 fast path versus Level 2 escalation path is explicit.
- Required deterministic artifacts are present or explicitly missing.
- Gate result is traceable and reproducible.
- Exceptions use the canonical fields and remain bounded.
- Governance guidance stays self-contained and internally consistent.
