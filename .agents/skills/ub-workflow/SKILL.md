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

When this skill is adopted in a repository or project, the default operating
surface is `./.ub-workflows/` unless the host intentionally chooses a
different operations root.

Use that operations root for three lanes:

1. direct bounded work when no durable planning artifact is needed
2. lightweight specs under `./.ub-workflows/specs/` when the work needs a
   written contract but not a roadmap and sprint pack
3. initiatives under `./.ub-workflows/initiatives/` when the work needs a
   full PRD, roadmap, and resumable sprint execution

Use the deterministic helper to bootstrap that operations root when it is
missing, scaffold dated initiative roots under `./.ub-workflows/initiatives/`,
scaffold dated lightweight specs under `./.ub-workflows/specs/`, materialize
sprint directories from an approved roadmap, and archive completed initiatives
on explicit request. Prepare sprint content before execution, whether that
preparation is done directly in the artifacts or through a helper-supported
flow.

## Core Principle

Drive work through this ordered flow:

1. intake classification
2. direct bounded task, lightweight spec, or full initiative chosen explicitly
3. research and discovery when the work needs durable planning
4. execution-ready PRD for full initiatives
5. initiative scaffold and durable planning baseline
6. durable roadmap generated and approved in one pass
7. sprint-content preparation
8. sprint materialization and start readiness
9. standalone resumable sprint execution
10. running sprint decision memory and initiative rollup updates
11. sprint closeout with explicit handoff and review pause
12. final audit and review pause
13. retained note and archive decision

## Initiative-Level Gates

Use these lifecycle gates for initiative work:

1. `prd_ready`
2. `roadmap_ready`
3. `research_ready`
4. `sprint_content_ready`
5. `sprint_start_ready`
6. `sprint_closeout`
7. `archive_ready`
8. `initiative_complete`

Allowed states:

1. `pass`
2. `fail`
3. `blocked`

These are initiative workflow gates, not repository governance gates.

## Interaction Modes

Interaction mode controls how visible and autonomous `ub-workflow` feels once
the current workflow lane is actually ready.

Interaction mode does not change lane readiness requirements.

Lane decides required artifacts and readiness checks.
Mode decides user-facing visibility, pause behavior, and interruption
behavior.

Modes:

1. `reviewed`
   - default mode
   - user-facing pre-execution analysis
   - user-facing post-execution reporting with considerations and watchouts
   - mandatory pause between sprints or bounded execution chunks
2. `flow`
   - short user-facing pre-execution note, but no mandatory pre-execution stop
   - richer user-facing post-execution reporting with considerations and
     watchouts
   - manual advancement after each sprint or bounded execution chunk
3. `auto`
   - internal pre-execution analysis by default
   - concise user-facing post-execution reporting
   - automatic advancement unless interruption conditions are met
4. `continuous`
   - user-facing alias: `yolo`
   - internal analysis and artifact updates still required
   - no routine user-facing pre/post-execution reporting
   - no routine pause between sprints or bounded execution chunks
   - interrupt only when a major blocker or conflict requires aborting or
     pausing the work

Persistence and precedence:

1. explicit user turn override
2. persisted artifact mode
3. default fallback = `reviewed`

Persistence by lane:

1. initiative lane: persist in initiative artifacts
2. lightweight-spec lane: persist in `spec.md`
3. direct bounded lane: runtime only unless promoted into a durable artifact

Question handling:

1. prefer `AskUserQuestion` / `vscode/askQuestions` when the host exposes it
2. always allow a custom reply path
3. when the question tool is unavailable, fall back to the same text pattern:
   `(*)` on the best qualitative fit, a short explanation under every option in
   `(...)`, and a final `Custom` option

## Load References On Demand

- Read `../references/authoring-conventions.md` when adjusting routing
  guidance, shared output structure, or cross-skill authoring conventions.
- Read `docs/quick-start.md` when the user needs first-use workflow help,
  lane selection guidance, or a compact explanation of how specs and
  initiatives differ in practice.
- Read `references/workflow-contract.md` for the canonical lifecycle and
  stop-resume rules.
- Read `references/artifact-contracts.md` for the required files and section
  contracts.
- Read `references/scaffold-adaptation.md` for placeholder policy and
  repository adaptation rules.
- Read `references/scaffold-helper.md` when using the deterministic helper or
  validating scaffold, sync, and archive behavior.
- Read `references/placeholder-contract.md` when validating generated
  initiative output for unresolved placeholders or deciding whether strict
  placeholder enforcement should block progress.
- Read `references/governance-bridge.md` when explicit governance alignment,
  evidence depth, or audit mapping is needed.
- Read `references/validation-and-completion.md` for per-phase exit criteria,
  validation gates, and completion checks.
- Read `docs/user-guide.md` for the deeper human-facing guide, richer usage
  examples, handoff guidance, and smoke prompts.

## Bundled Assets

Use the assets under `assets/operations-root/`,
`assets/initiative-template/`, and `assets/lightweight-spec-template/` as the
canonical internal templates for this skill.

Use `scripts/scaffold_initiative.py` when deterministic scaffold creation is
preferred over manual copying.

Rules:

1. Bootstrap `./.ub-workflows/` when it is missing instead of asking the user to create it by hand.
2. Do not require a copied local `initiative-template/` inside the generated operations root.
3. Do not edit the canonical asset templates for one specific initiative.
4. Replace placeholders explicitly; do not leave repository-specific facts
   implied.
5. Do not set approval gates on behalf of the human unless the workflow explicitly says the gate is agent-owned.

## When Not To Use

- Do not use this skill for governance-only questions or deterministic gate
  execution; defer those to `ub-governance`.
- Do not use this skill when the work is already a small direct code change
  that does not need durable planning artifacts.
- Do not use this skill as a substitute for language/framework implementation
  guidance once the workflow lane and execution surface are already clear.

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

1. Detect whether the user needs direct bounded work, lightweight-spec shaping,
   initiative PRD shaping, roadmap generation, sprint preparation, sprint
   initialization, sprint execution support, or final audit.
2. Inspect repository truth before writing repository-specific validation or
   adaptation details.
3. Start rough ideas with explicit assumption surfacing and a scale decision:
   direct bounded task, lightweight spec, or full initiative.
4. If `./.ub-workflows/` does not exist, bootstrap it first through
   `scripts/scaffold_initiative.py`.
5. When the work is below initiative scale but still needs a durable contract,
   create or refine a lightweight spec under
   `./.ub-workflows/specs/YYYY-MM-DD-slug/spec.md`.
6. Scaffold new initiatives under `./.ub-workflows/initiatives/YYYY-MM-DD-slug/`
   only when the work truly needs a PRD, roadmap, and sprint execution model.
7. When the user provides a source PRD, copy that file into the initiative root
   as `./prd.md` without rewriting or summarizing it.
8. Make `prd.md` self-contained before generating a roadmap.
9. Generate the full roadmap in one pass before sprint execution starts.
10. Treat the completed `roadmap.md` as the durable post-plan artifact.
11. Surface a review checklist for sprint breakdown completeness, ordering and
  dependencies, scope boundaries and non-goals, and validation/docs
  expectations before `roadmap_ready: pass` can be set.
12. Do not prepare sprint content, initialize sprint folders, or begin sprint
   execution until `roadmap_ready: pass`.
13. Make the roadmap explicit about every planned sprint from `Sprint 01`
   through `Sprint NN`, then keep the final audit as the last roadmap item.
14. Prepare each planned sprint as a standalone execution-ready `sprint.md`
   before Sprint 01 or any later sprint begins.
15. Initialize or repair all planned sprint folders from the canonical
   `ub-workflow` sprint template only after roadmap approval and in a way that
   preserves the prepared sprint content.
16. When a sprint needs additional context refresh before execution, record the
   checkpoint explicitly before the sprint begins.
17. Keep each `sprint.md` standalone so execution does not depend on reopening
   the master PRD.
18. Resolve the active interaction mode before execution and keep it consistent
   with the current lane.
19. For initiatives, require the same readiness prerequisites in every mode:
   approved roadmap, prepared sprint pack, execution-ready current sprint, and
   no unresolved blockers that prevent safe execution.
20. Execute the active sprint according to the active interaction mode,
   updating `roadmap.md`, `README.md`, `rollup.md`, the active
   `decision-log.md`, and the active `closeout.md` as state changes.
21. `reviewed` and `flow` stop after each sprint so the human can review before
   any next sprint work.
22. `auto` may continue between sprints when no interruption condition exists:
   hard blocker, material ambiguity, repo-truth conflict, or a decision that
   would materially reshape later sprints.
23. `continuous` / `yolo` may continue without routine user-facing reporting,
   but must abort or pause when a major blocker or conflict requires explicit
   user resolution, and that interruption must be documented clearly in the
   workflow artifacts.
24. Treat validation, documentation synchronization, and completion evidence
   as gating conditions for both sprint closeout and initiative completion.
25. End every initiative with a final audit and `retained-note.md`, then stop
   for human review before any archive action.
26. Archive only when the user explicitly asks for it and the completion
   controls pass.

## Repository Defaults

1. Treat `./.ub-workflows/initiatives/README.md`, `operation-guide.md`, and
   `user-guide.md` as the workflow entry surfaces for creating or resuming
   initiatives.
2. Treat `./.ub-workflows/specs/` as the default home for lightweight specs.
3. Treat `roadmap.md` as the smallest live progress document for an initiative.
4. Keep roadmap sprint entries rich enough to prevent omissions: path, goal,
   dependencies, validation focus, subtasks, and evidence folder.
5. Treat sprint preparation as a distinct lifecycle phase; do not treat
  initialized directories or placeholder sprint shells as execution-ready by
  default.
6. Treat sprint `decision-log.md` as the default running sprint-memory surface
   and `rollup.md` as the readable initiative-level carry-forward surface.
7. Keep `research/` and `exceptions/` visibly secondary to those main workflow
   artifacts.
8. Keep the skill useful across adopting repositories by keeping the canonical
   templates internal to the skill rather than requiring copied local
   scaffolding directories.
9. Treat roadmap approval and archive readiness as human-owned checkpoints,
   not automatic agent transitions.
10. Default new initiatives and lightweight specs to interaction mode
    `reviewed` until the user explicitly changes it.
11. In user-facing execution notes, include a concise mode reference so the
    user can see the available modes without opening the docs.

## Output Requirements

When using this skill to plan or scaffold an initiative, include:

1. `phase_note`      : current lifecycle phase
2. `mode_note`       : active interaction mode plus a concise mode reference
3. `scope_note`      : what the initiative or sprint covers
4. `decision_note`   : chosen path plus one rejected alternative
5. `artifact_note`   : which files were created, updated, or expected
6. `gate_note`       : initiative-level gate state and rationale
7. `validation_note` : checks run or still required
8. `next_action_note` : the next concrete step

## Completion Checklist

- The lifecycle phase is explicit.
- The current initiative-level gate is explicit.
- Discovery and PRD readiness are explicit before roadmap generation.
- The PRD is self-contained before roadmap generation.
- The roadmap is the durable approved planning artifact before sprint initialization begins.
- `roadmap_ready: pass` is set only after explicit human approval.
- Sprint content is prepared before sprint execution begins.
- Validation expectations and documentation touch points are explicit.
- The roadmap ends with a final audit step.
- When the lightweight-spec lane is used, `spec.md` is self-contained enough
  for another operator to continue without chat history.
- The active interaction mode is explicit when a durable workflow artifact
  exists.
- All sprint folders are initialized only after `roadmap_ready: pass` and in a
  way that preserves prepared sprint content.
- Sprint execution never starts without an explicit user request.
- Sprint execution never starts from a placeholder-only sprint shell.
- `reviewed` and `flow` pause after sprint execution; `auto` and `continuous`
  only continue when their interruption rules allow it.
- The workflow still stops after final audit for human review before archive.
- Each sprint document is standalone and resumable.
- Archive readiness is surfaced explicitly before any archive action.
- Touched workflow documents satisfy ub-quality formatting and structure rules.
- The retained note captures durable outcomes after completion.

## Deferred Work

For planned follow-on improvements beyond the initial implementation, use
`roadmap.md` in this skill folder as the durable pickup document.

For a human-oriented operating guide, use `docs/user-guide.md`.
