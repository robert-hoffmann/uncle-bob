---
name: ub-workflow
description: >-
  Use this skill when the user wants to turn a rough initiative, product idea,
  engineering problem, or research thread into an execution-ready PRD, a full
  roadmap, and standalone resumable sprints; when the task involves initiative
  scaffolding, sprint planning, stop-resume handoffs, final audit flow, or
  retained notes for multi-session work; or when the user needs multi-sprint
  project planning, phased feature decomposition, or context preservation
  across sessions for large work. Do not use it for simple single-session
  fixes, or for governance-only questions that belong to ub-governance.
argument-hint: "overview | scaffold | resume | prd | roadmap | sprint | audit | archive | what-next"
user-invocable: true
disable-model-invocation: true
---

# UB Workflow

## Overview

Use this skill as the canonical initiative-planning and sprint-orchestration
workflow for large or risky work that cannot be executed reliably from chat
history alone.

In this repository, the default operating surface is `./.ub-workflows/`.

Use the deterministic helper to bootstrap that operations root when it is
missing, scaffold dated initiative roots under `./.ub-workflows/initiatives/`,
initialize sprint directories from the completed roadmap, and archive completed
initiatives on explicit request.

## Core Principle

Drive work through this ordered flow:

1. brainstorming and research
2. execution-ready PRD
3. durable roadmap generated and approved in one pass
4. all sprint folders initialized up front only after roadmap approval
5. standalone resumable sprint execution
6. sprint closeout with explicit handoff
7. final audit
8. retained note

## Initiative-Level Gates

Use these lifecycle gates for initiative work:

1. `prd_ready`
2. `roadmap_ready`
3. `sprint_closeout`
4. `initiative_complete`

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
- Read `references/scaffold-adaptation.md` for placeholder policy and
  repository adaptation rules.
- Read `references/scaffold-helper.md` when using the deterministic helper or
  validating scaffold, sync, and archive behavior.
- Read `references/governance-bridge.md` when explicit governance alignment,
  evidence depth, or audit mapping is needed.
- Read `references/validation-and-completion.md` for per-phase exit criteria,
  validation gates, and completion checks.
- Read `docs/user-guide.md` for human-facing usage examples, handoff guidance,
  and smoke prompts.

## Bundled Assets

Use the assets under `assets/operations-root/` and `assets/initiative-template/`
as the canonical internal templates for this skill.

Use `scripts/scaffold_initiative.py` when deterministic scaffold creation is
preferred over manual copying.

Rules:

1. Bootstrap `./.ub-workflows/` when it is missing instead of asking the user to create it by hand.
2. Do not require a copied local `initiative-template/` inside the generated operations root.
3. Do not edit the canonical asset templates for one specific initiative.
4. Replace placeholders explicitly; do not leave repository-specific facts
   implied.
5. Do not set approval gates on behalf of the human unless the workflow explicitly says the gate is agent-owned.

## Coordination With Sibling Skills

- Load and apply `ub-quality` whenever creating or editing initiative
  documents.
- Workflow artifacts explicitly required by this skill are allowed outputs
  under ub-quality's document-generation policy, but they still must satisfy
  ub-quality formatting and structure rules.
- Load `ub-governance` when the repository wants explicit governance alignment,
  evidence depth, or audit mapping.
- Do not require ub-governance for basic scaffolding or PRD generation.

## Core Workflow

1. Detect whether the user needs discovery, PRD shaping, roadmap generation,
   sprint initialization, sprint execution support, or final audit.
2. Inspect repository truth before writing repository-specific validation or
   adaptation details.
3. If `./.ub-workflows/` does not exist, bootstrap it first through `scripts/scaffold_initiative.py create ...`.
4. Scaffold new initiatives under `./.ub-workflows/initiatives/YYYY-MM-DD-slug/`.
5. When the user provides a source PRD, copy that file into the initiative root
  as `./prd.md` without rewriting or summarizing it.
6. Make `prd.md` self-contained before generating a roadmap.
7. Generate the full roadmap in one pass before sprint execution starts.
8. Treat the completed `roadmap.md` as the durable post-plan artifact.
9. Surface a review checklist for sprint breakdown completeness, ordering and
  dependencies, scope boundaries and non-goals, and validation/docs
  expectations before `roadmap_ready: pass` can be set.
10. Do not initialize sprint folders until `roadmap_ready: pass`.
11. Make the roadmap explicit about every planned sprint from `Sprint 01`
  through `Sprint NN`, then keep the final audit as the last roadmap item.
12. Initialize all planned sprint folders from the initiative's
  `sprint-template/` up front by running the deterministic helper, then stop
  and wait for an explicit user request before executing the active sprint.
13. Keep each `sprint.md` standalone so execution does not depend on reopening
  the master PRD.
14. Execute only one user-requested active sprint at a time, updating
  `roadmap.md`, `README.md`, and the active `closeout.md` as state changes.
15. Stop after each sprint so the human can review before any next sprint work.
16. Treat validation, documentation synchronization, and completion evidence
   as gating conditions for both sprint closeout and initiative completion.
17. End every initiative with a final audit and `retained-note.md`, then stop
  for human review before any archive action.
18. Archive only when the user explicitly asks for it and the completion
   controls pass.

## Repository Defaults

1. Treat `./.ub-workflows/initiatives/README.md`, `operation-guide.md`, and `user-guide.md` as the workflow entry surfaces for creating or resuming initiatives.
2. Treat `roadmap.md` as the smallest live progress document for an initiative.
3. Keep roadmap sprint entries rich enough to prevent omissions: path, goal, dependencies, validation focus, subtasks, and evidence folder.
4. Keep the skill useful outside this repository by keeping the canonical templates internal to the skill rather than requiring copied local scaffolding directories.
5. Treat roadmap approval as a human-owned checkpoint, not an automatic agent transition.

## Output Requirements

When using this skill to plan or scaffold an initiative, include:

1. `phase_note`      : current lifecycle phase
2. `scope_note`      : what the initiative or sprint covers
3. `decision_note`   : chosen path plus one rejected alternative
4. `artifact_note`   : which files were created, updated, or expected
5. `gate_note`       : initiative-level gate state and rationale
6. `validation_note` : checks run or still required
7. `next_action_note` : the next concrete step

## Completion Checklist

- The lifecycle phase is explicit.
- The current initiative-level gate is explicit.
- The PRD is self-contained before roadmap generation.
- The roadmap is the durable approved planning artifact before sprint initialization begins.
- `roadmap_ready: pass` is set only after explicit human approval.
- Validation expectations and documentation touch points are explicit.
- The roadmap ends with a final audit step.
- All sprint folders are initialized only after `roadmap_ready: pass`.
- Sprint execution never starts without an explicit user request.
- The workflow stops after every sprint and after final audit for human review.
- Each sprint document is standalone and resumable.
- Touched workflow documents satisfy ub-quality formatting and structure rules.
- The retained note captures durable outcomes after completion.

## Deferred Work

For planned follow-on improvements beyond the initial implementation, use
`roadmap.md` in this skill folder as the durable pickup document.

For a human-oriented operating guide, use `docs/user-guide.md`.
