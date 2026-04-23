---
name: ub-workflow
description: >-
  Use this skill when the user wants to turn a rough idea, product problem,
  engineering thread, or research track into the right planning surface:
  direct bounded work, a lightweight spec, or a full initiative with PRD,
  roadmap, and standalone resumable sprints; when the task involves initiative
  scaffolding, lightweight-spec shaping, sprint planning, stop-resume
  handoffs, final audit flow, or retained notes for multi-session work; or
  when the user needs phased planning and context preservation for larger work.
  Do not use it for governance-only questions that belong to ub-governance.
argument-hint: "overview | scaffold | spec | resume | prd | roadmap | sprint | audit | archive | what-next"
user-invocable: true
disable-model-invocation: true
---

# UB Workflow

## Overview

Use this skill as the canonical workflow intake, initiative-planning, and
sprint-orchestration layer for work that is too large, risky, or stateful to
run safely from chat history alone.

The default operating surface is `./.ub-workflows/` unless the host
intentionally chooses a different operations root.

This skill owns three lanes only:

1. direct bounded work when the work is a truly small fix or bounded task that
   can be executed safely without a durable planning artifact
2. lightweight specs under `./.ub-workflows/specs/` when the work is still
   bounded but now needs a durable contract for assumptions, scope, options,
   validation, or a concrete execution plan
3. initiatives under `./.ub-workflows/initiatives/` when the work needs a
   PRD, roadmap, and resumable sprint execution because it is multi-session,
   staged, risky, or clearly cross-cutting

If the work is a bounded one-off, prefer a lightweight spec.
If the work is multi-session, cross-cutting, risky, or needs staged delivery,
use an initiative.

## Embedded Contract

These rules are the base contract of this skill and must not depend on a
secondary document to be applied correctly.

1. Make the lane choice explicit before opening durable artifacts: direct
   bounded work, lightweight spec, or initiative.
2. Keep direct bounded work narrow: do not stay direct once the conversation
   becomes planning-heavy, medium-sized, execution-shaped, or useful enough
   that another operator would benefit from a durable mini-contract.
3. Promote to a lightweight spec when brainstorming becomes real planning,
   even before implementation starts, if the work now needs durable
   assumptions, scope, options, validation, or an execution shape.
4. Promote to an initiative once the work clearly needs PRD-level
   decomposition, sequencing, stop-resume safety, or staged delivery rather
   than a bounded spec alone.
5. Surface a short promotion note when the lane changes so the user can see
   why direct bounded work or a lightweight spec is no longer the smallest safe
   surface.
6. For initiatives, make `prd.md` self-contained before generating
   `roadmap.md`.
7. Treat `roadmap.md` as the durable post-plan artifact.
8. Do not prepare sprint content, initialize sprint folders, or begin sprint
   execution until `roadmap_ready: pass`.
9. Prepare each sprint as a standalone `sprint.md` before the sprint begins.
10. Sprint execution never starts from placeholder-only sprint shells.
11. In `reviewed` mode, after sprint closeout, a request like `ok lets move on`
   or `Start the next sprint.` opens the next sprint preview only.
12. In `reviewed` mode, that preview analyzes the next sprint, surfaces any
   path-changing questions, and asks for one explicit start approval.
13. In `reviewed` mode, a later approval message starts execution and, when
   used, records `sprint_start_ready: pass`; it does not trigger a second start
   prompt.
14. End every initiative with a final audit and a retained note, then stop for
    human review before archive.

## Initiative Lifecycle

Drive initiative work through this ordered flow:

1. intake classification
2. lane choice
3. research and discovery when durable planning is needed
4. execution-ready PRD
5. initiative scaffold and planning baseline
6. roadmap generation and approval
7. sprint-content preparation
8. sprint materialization and start readiness
9. ordered sprint execution
10. sprint closeout with explicit handoff and review pause
11. final audit and review pause
12. retained note and archive decision

## Initiative-Level Gates

Use these lifecycle gates for initiatives:

1. `research_ready`
2. `prd_ready`
3. `roadmap_ready`
4. `sprint_content_ready`
5. `sprint_start_ready`
6. `sprint_closeout`
7. `archive_ready`
8. `initiative_complete`

Allowed states:

1. `pass`
2. `fail`
3. `blocked`

These are workflow gates, not repository governance gates.

## Interaction Modes

Interaction mode changes visibility, pause behavior, and interruption behavior.
It does not weaken readiness rules.

1. `reviewed`
   - default mode
   - user-facing pre-sprint preview as a distinct checkpoint
   - explicit human approval before execution
   - user-facing post-execution reporting with considerations and watchouts
   - the post-execution report is the pause boundary after a sprint
   - a later move-on request opens the next pre-sprint preview and start
     approval prompt
2. `flow`
   - short pre-execution note
   - richer post-execution reporting
   - manual advancement after each sprint or bounded execution chunk
3. `auto`
   - internal pre-execution analysis by default
   - concise post-execution reporting
   - automatic advancement unless interruption conditions are met
4. `continuous`
   - user-facing alias: `yolo`
   - internal analysis and artifact updates still required
   - no routine pause between sprints or bounded execution chunks
   - interrupt only when a major blocker or conflict requires user resolution

Mode precedence:

1. explicit user turn override
2. persisted artifact mode
3. default fallback = `reviewed`

Persistence by lane:

1. initiative lane: persist in initiative artifacts
2. lightweight-spec lane: persist in `spec.md`
3. direct bounded lane: runtime only unless promoted into a durable artifact

Question handling:

1. for multiple-choice user prompts, follow the shared choice-question
   contract in `../ub-authoring/references/authoring-conventions.md`
2. in `reviewed` mode, keep the same decision structure as the canonical
   reviewed-mode pre-sprint preview pattern
3. resolve the questions that change the sprint path before the single explicit
   start-approval question

For non-trivial `reviewed`-mode sprints, the preview should lead with:

1. `What Repo Truth Says`
2. `Inference`
3. `Implementation Paths`
4. `Recommendation`

Artifact or validation bookkeeping is secondary unless it is itself the repo
truth that materially shapes the sprint.

## Load References By Trigger

Use these load tiers literally.
If a trigger is not active, do not read the reference just because it exists.

- `[phase:lifecycle-detail]` Read `references/workflow-contract.md` for the
  detailed lifecycle, reviewed-mode preview pattern, and stop-resume rules.
- `[phase:artifact-create|artifact-validate]` Read
  `references/artifact-contracts.md` when creating or validating initiative or
  lightweight-spec artifacts.
- `[phase:gate-eval|closeout|readiness]` Read
  `references/validation-and-completion.md` when evaluating readiness, gate
  transitions, closeout, or completion.
- `[edge:helper-use]` Read `references/scaffold-helper.md` only when using or
  explaining the deterministic helper.
- `[edge:governance-escalation]` Read `references/governance-bridge.md` only
  when explicit governance alignment, evidence depth, or audit mapping is in
  play.
- `[edge:strict-placeholder-validation]` Read
  `references/placeholder-contract.md` only when strict placeholder validation
  or the placeholder checker is relevant.
- `[edge:authoring-conventions]` Read `../ub-authoring/references/authoring-conventions.md`
  only when adjusting shared routing or cross-skill authoring structure.

Do not treat human help docs as operational dependencies.

## Bundled Assets

Use the assets under `assets/operations-root/`,
`assets/initiative-template/`, and `assets/lightweight-spec-template/` as the
canonical internal templates for this skill.

Use `scripts/scaffold_initiative.py` when deterministic scaffold creation is
preferred over manual copying.

Rules:

1. Bootstrap `./.ub-workflows/` when it is missing instead of asking the user
   to create it by hand.
2. Do not require a copied local `initiative-template/` inside the generated
   operations root.
3. Do not edit the canonical asset templates for one specific initiative.
4. Replace placeholders explicitly; do not leave repository-specific facts
   implied.
5. Do not set human-owned approval gates on behalf of the user.

## When Not To Use

- Do not use this skill for governance-only questions or deterministic gate
  execution; defer those to `ub-governance`.
- Do not use this skill when the work is already a small direct code change
  that does not need durable planning artifacts.
- Do not use this skill as a substitute for language or framework
  implementation guidance once the execution surface is already clear.

## Coordination With Sibling Skills

- Load and apply `ub-quality` whenever creating or editing workflow documents.
- Workflow artifacts explicitly required by this skill are allowed outputs
  under ub-quality's document-generation policy, but they still must satisfy
  ub-quality formatting and structure rules.
- Load `ub-governance` only when the repository wants explicit governance
  alignment, evidence depth, or audit mapping.
- Do not require ub-governance for basic scaffolding, PRD generation, or
  ordinary lightweight-spec work.

## Core Workflow

1. Detect whether the user needs direct bounded work, lightweight-spec shaping,
   initiative PRD shaping, roadmap generation, sprint preparation, sprint
   initialization, sprint execution support, or final audit.
2. Inspect repository truth before writing repository-specific validation or
   adaptation details.
3. Make the scale decision explicit and promote out of direct bounded work as
   soon as the conversation needs a durable planning surface.
4. If `./.ub-workflows/` does not exist, bootstrap it through
   `scripts/scaffold_initiative.py`.
5. Create or refine a lightweight spec when the work is still bounded but now
   needs assumptions, scope, options, validation, or an execution plan written
   down.
6. Bias medium planning work toward a lightweight spec first, but scaffold a
   new initiative as soon as the work clearly needs a PRD, roadmap, or staged
   execution model.
7. Copy a source PRD into `./prd.md` without rewriting it.
8. Generate the full roadmap in one pass before sprint execution starts.
9. Surface a review checklist before `roadmap_ready: pass` can be set.
10. Prepare each planned sprint as a standalone execution-ready `sprint.md`.
11. Initialize sprint folders only after roadmap approval and in a way that
    preserves prepared sprint content.
12. Execute only the active sprint according to the active interaction mode,
    updating `roadmap.md`, `README.md`, `rollup.md`, `decision-log.md`, and
    `closeout.md` as state changes.
13. Treat validation, documentation synchronization, and completion evidence
    as gating conditions for both sprint closeout and initiative completion.
14. Archive only when the user explicitly asks for it and the completion
    controls pass.

## Repository Defaults

1. Treat `./.ub-workflows/specs/` as the default home for lightweight specs.
2. Treat `roadmap.md` as the smallest live progress document for an
   initiative.
3. Keep roadmap sprint entries rich enough to prevent omissions: path, goal,
   dependencies, validation focus, subtasks, and evidence folder.
4. Treat sprint preparation as a distinct lifecycle phase; do not treat
   initialized directories or placeholder sprint shells as execution-ready.
5. Treat sprint `decision-log.md` as the default sprint-memory surface and
   `rollup.md` as the initiative-level carry-forward surface.
6. Keep `research/` and `exceptions/` visibly secondary to the main workflow
   artifacts.
7. Treat roadmap approval and archive readiness as human-owned checkpoints.
8. Default new initiatives and lightweight specs to interaction mode
   `reviewed` until the user explicitly changes it.
9. In user-facing execution notes, include a concise mode reference so the
   user can see the available modes without opening extra docs.
10. Surface lane choice routinely only when promotion happens or when the user
    explicitly asks, so very small direct work stays lightweight.
11. Bias planning-heavy bounded work toward lightweight specs, and bias
    clearly multi-phase or cross-cutting work toward initiatives earlier than a
    purely minimal reading would.

## Output Requirements

When using this skill for non-trivial workflow work, include:

1. `phase_note`
2. `mode_note`
3. `scope_note`
4. `decision_note`
5. `promotion_note` when lane escalation happens
6. `artifact_note`
7. `gate_note`
8. `validation_note`
9. `next_action_note`

## Completion Checklist

- The lane choice is explicit.
- Lane promotion is explicit when work moves from direct bounded work to a
  lightweight spec or from a lightweight spec to an initiative.
- The lifecycle phase is explicit.
- The current initiative-level gate is explicit.
- Discovery and PRD readiness are explicit before roadmap generation.
- The PRD is self-contained before roadmap generation.
- The roadmap is the durable approved planning artifact before sprint
  initialization begins.
- `roadmap_ready: pass` is set only after explicit human approval.
- Sprint content is prepared before sprint execution begins.
- Sprint execution never starts without an explicit user request.
- Sprint execution never starts from a placeholder-only sprint shell.
- `reviewed` and `flow` pause after sprint execution; `auto` and
  `continuous` only continue when their interruption rules allow it.
- The workflow still stops after final audit for human review before archive.
- Each sprint document is standalone and resumable.
- Archive readiness is surfaced explicitly before any archive action.
- Touched workflow documents satisfy ub-quality formatting and structure rules.
- The retained note captures durable outcomes after completion.
