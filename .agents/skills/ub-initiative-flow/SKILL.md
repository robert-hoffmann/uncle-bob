---
name: ub-initiative-flow
description: >-
  Use this skill when the user wants to turn a rough initiative, product idea,
  engineering problem, or research thread into an execution-ready PRD, a full
  roadmap, and standalone resumable sprints; when the task involves initiative
  scaffolding, sprint planning, stop-resume handoffs, final audit flow, or
  retained notes for multi-session work. Do not use it for simple single-session
  fixes, or for governance-only questions that belong to ub-governance.
argument-hint: "overview | scaffold | prd | roadmap | sprint | audit"
user-invocable: true
disable-model-invocation: true
---

# UB Initiative Flow

## Overview

Use this skill as the canonical initiative-planning and sprint-orchestration
workflow for large or risky work that cannot be executed reliably from chat
history alone.

This skill is portable by default. It ships neutral scaffolding and reusable
contracts, then adapts to the current repository through explicit placeholders
instead of hardcoded project facts.

## Core Principle

Drive work through this ordered flow:

1. brainstorming and research
2. execution-ready PRD
3. full roadmap generated in one pass
4. all sprint folders initialized up front
5. standalone resumable sprint execution
6. sprint closeout with explicit handoff
7. final audit
8. retained note

## Initiative-Level Gates

Use these lifecycle gates for initiative work:

1. `prd_ready`
2. `sprint_closeout`
3. `initiative_complete`

Allowed states:

1. `pass`
2. `fail`
3. `blocked`

These are initiative workflow gates, not repository governance gates.

## Load References On Demand

- Read `references/workflow-contract.md` for the canonical lifecycle and
  stop-resume rules.
- Read `references/artifact-contracts.md` for the required files and section
  contracts.
- Read `references/scaffold-adaptation.md` for placeholder replacement and
  repository adaptation rules.
- Read `references/scaffold-helper.md` for deterministic scaffold creation and
  safe rerun behavior.
- Read `references/governance-bridge.md` when the initiative should align with
  ub-governance.
- Read `references/validation-and-completion.md` for per-phase exit criteria
  and completion checks.
- Read `docs/user-guide.md` for human-facing usage examples, handoff guidance,
  and future iteration prompts.

## Bundled Assets

Use the neutral scaffold under `assets/initiative-template/` as the canonical
copy source for new initiatives.

Use `scripts/scaffold_initiative.py` when deterministic scaffold creation is
preferred over manual copying.

Rules:

1. Copy the scaffold before tailoring it to a repository or initiative.
2. Do not edit the canonical asset templates for one specific initiative.
3. Replace placeholders explicitly; do not leave repository-specific facts
   implied.

## Coordination With Sibling Skills

- Load `ub-quality` whenever creating or editing initiative documents.
- Load `ub-governance` when the repository wants explicit governance alignment,
  evidence depth, or audit mapping.
- Do not require ub-governance for basic scaffolding or PRD generation.

## Core Workflow

1. Detect whether the user needs discovery, PRD shaping, roadmap generation,
   sprint initialization, sprint execution support, or final audit.
2. Inspect repository truth before writing repository-specific validation or
   adaptation details.
3. Scaffold from `assets/initiative-template/` when starting a new initiative.
4. Make `prd.md` self-contained before generating a roadmap.
5. Generate the full roadmap in one pass before sprint execution starts.
6. Initialize all planned sprint folders from `sprint-template/` up front.
7. Keep each `sprint.md` standalone so execution does not depend on reopening
   the master PRD.
8. Run one sprint at a time, updating `roadmap.md`, `README.md`, and the active
   `closeout.md` as state changes.
9. End every initiative with a final audit and `retained-note.md`.

## Portability Rules

1. Keep the workflow opinionated, but keep the shipped scaffold repository
   neutral.
2. Treat validation commands, docs paths, governance settings, and ownership as
   adaptation inputs.
3. Prefer placeholders and adaptation notes over embedded local assumptions.
4. Keep this skill useful even in repositories that do not use ub-governance.

## Output Requirements

When using this skill to plan or scaffold an initiative, include:

1. `phase_note`      : current lifecycle phase
2. `scope_note`      : what the initiative or sprint covers
3. `decision_note`   : chosen path plus one rejected alternative
4. `artifact_note`   : which files were created, updated, or expected
5. `gate_note`       : initiative-level gate state and rationale
6. `validation_note` : checks run or still required
7. `next_action_note`: the next concrete step

## Completion Checklist

- The lifecycle phase is explicit.
- The current initiative-level gate is explicit.
- The PRD is self-contained before roadmap generation.
- The roadmap ends with a final audit step.
- All sprint folders are initialized before execution begins.
- Each sprint document is standalone and resumable.
- The retained note captures durable outcomes after completion.

## Deferred Work

For planned follow-on improvements beyond the initial implementation, use
`roadmap.md` in this skill folder as the durable pickup document.

For a human-oriented operating guide, use `docs/user-guide.md`.