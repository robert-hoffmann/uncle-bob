---
name: ub-governance
description: Unified governance skill for repository governance, testing and TDD governance, evidence and ADR/claim governance, and shared governance contracts. Use when defining, auditing, or executing deterministic governance gates and bounded exception-aware controls.
metadata:
  desktop-portfolio-help-topics: "overview,evidence,testing,repository,core,glossary,combos,invoke"
  desktop-portfolio-help-aliases: "repo=repository"
  desktop-portfolio-help-default-topic: "overview"
---

# UB Governance

## Overview

Use this skill as the single owner for governance in the current repository or
project where it is adopted.
This skill is self-contained and merges repository, testing, evidence, and
shared contract governance.

## Operating Modes

1. `repository mode`: repository hygiene, CI/release governance, branch/ruleset policy, deterministic tooling
2. `testing mode`: testing policy, TG001-TG005 signal controls, regression-first bug-fix flow, and behavior-first TDD execution
3. `evidence mode`: evidence lifecycle, ADR alignment, claim verification, gate readiness
4. `core-contract mode`: shared profile, gate semantics, exception metadata, report sections
5. `full governance audit mode`: run repository + testing + evidence checks in one deterministic sequence

## Mode Selection

- Select exactly one mode for focused tasks.
- Use `full governance audit mode` only for end-to-end governance assessment or release/merge readiness.
- Default to `lean` profile unless the user explicitly requests `advanced`.

## Load References On Demand

### Core Contracts

- Read `../references/authoring-conventions.md` when adjusting routing
  guidance, output structure, or cross-skill authoring conventions.
- Read `references/profile-model.md` for profile selection.
- Read `references/gate-and-report-contract.md` for canonical gate/report semantics.
- Read `references/exception-contract.md` for canonical exception metadata.
- Read `references/vocabulary.md` for normalized governance vocabulary.
- Read `references/governance-commands.md` for stable command entrypoints.

### Repository Governance

- Read `references/repository-baseline.md` for repository defaults.
- Read `references/github-implementation-playbook.md` for GitHub implementation patterns.
- Read `references/release-please-playbook.md` for release automation policy.

### Testing Governance

- Read `references/testing-policy-and-signals.md` for TG001-TG005 and TDD policy.
- Read `references/execution-playbook.md` for Red-Green-Refactor execution.
- Read `references/ci-artifact-contract.md` for required test artifacts.
- Read `references/stack-baseline.md` for lean testing stack defaults.

### Evidence Governance

- Read `references/evidence-baseline.md` for default evidence controls.
- Read `references/evidence-lifecycle.md` for evidence freshness and retention.
- Read `references/evidence-artifact-taxonomy.md` for risk-tiered artifact requirements.
- Read `references/decision-memory-and-claims.md` for ADR/claim decision rules.
- Read `references/high-risk-paths.yaml` for high-risk scope detection.
- Read `references/agent-validation-record.schema.json` for validation-record schema.
- Read `references/adr-registry.schema.json` for ADR registry schema.
- Read `references/claim-register.schema.json` for claim-register schema.
- Read `references/adr-template-madr.md` for ADR authoring structure.

## Core Workflow

1. Detect requested mode and evaluated scope from repository truth.
2. Select profile (`lean` default, `advanced` only with explicit rationale).
3. Propose at least two implementation paths for non-trivial governance decisions with concise pros/cons.
4. Run mode-specific controls and keep outputs deterministic.
5. Apply bounded exceptions only through `references/exception-contract.md`.
6. Emit gate outcome (`pass`, `fail`, `blocked`) with traceable artifact paths.

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
2. treat reported defects as regression-first work before code fixes are accepted
3. enforce TG001-TG004 as blocking and TG005 as warning
4. require behavior-first TDD flow for behavior-changing work and keep increments outcome-oriented
5. use the testing references to keep test design readable, boundary-aware, and deterministic without turning advisory guidance into new gates

### Evidence Mode

1. classify `changeType`, `evidenceLevel`, and `profile`
2. detect high-risk path impact
3. choose the lightest durable record that matches the decision scope before
   asking for heavier governance artifacts
4. treat workflow-backed initiative artifacts as the default operational record
   for ordinary Level 1 work, including sprint-local evidence and closeout
   notes
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

- Keep this skill self-contained and do not require other governance skills.
- Keep defaults lean and activate advanced controls explicitly.
- Blocking governance decisions must rely on deterministic artifacts.
- Exception metadata must include owner, expiry, and follow-up.
- Do not duplicate canonical contract definitions across files.
- Do not imply that repository ADR machinery is the default record for ordinary
  Level 1 workflow-backed work.

## Output Requirements

Treat this section as the stable output expectation for non-trivial governance
work in this catalog.

When producing governance output, include:

1. `environment_note`
2. `scope_note`
3. `decision_note` (chosen path plus one alternative with pros/cons)
4. `gate_note`
5. `exception_note`
6. `validation_note`

Add mode-specific sections when applicable:

1. `quality_gate_note` for testing mode
2. `evidence_inventory`, decision-note extensions, and `claim_note` for evidence mode

## Completion Checklist

- Selected mode is explicit.
- Profile choice is explicit (`lean` or `advanced`).
- Required deterministic artifacts are present or explicitly missing.
- Gate result is traceable and reproducible.
- Exceptions use canonical contract and remain bounded.
- Governance guidance stays self-contained and internally consistent.
