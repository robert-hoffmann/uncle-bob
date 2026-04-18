<!-- #region Purpose -->
# UB Workflow User Guide

## Purpose

This guide explains how to use `ub-workflow` in day-to-day repository
work.

Use it for two jobs:

1. operating the skill and companion agent as a human user
2. iterating on the skill and agent later with a stable usage baseline

For first-use onboarding, start with [quick-start.md](./quick-start.md).
This guide is the deeper operational reference.
<!-- #endregion Purpose -->

<!-- #region Mental Model -->
## Mental Model

`ub-workflow` is the planning and orchestration layer for larger work.

It exists to choose and shape the right planning surface:

1. direct bounded work when no durable planning artifact is needed
2. a lightweight spec when the work needs assumptions, scope, and validation
   written down but does not justify a roadmap and sprint pack
3. a full initiative when the work is too large, risky, or multi-session to
   run reliably from chat history alone

Rule of thumb:

1. prefer a lightweight spec for bounded one-off work that still needs a
   durable contract
2. prefer an initiative for broader, higher-impact work where PRD, roadmap,
   sprints, and final audit improve delivery and review quality

The core lifecycle is:

1. scale decision
2. lightweight spec or initiative planning chosen explicitly
3. discovery and research when the work needs durable planning
4. self-contained PRD for full initiatives
5. roadmap generated and approved in one pass
6. sprint pack prepared so each planned `sprint.md` is execution-ready
7. sprint folders materialized when needed from the approved roadmap
8. standalone resumable sprint execution, one sprint per explicit user request
9. final audit
10. retained note
<!-- #endregion Mental Model -->

<!-- #region Modes -->
## Interaction Modes

`ub-workflow` supports four interaction modes.

The mode does not change workflow readiness requirements.
It changes how much the user sees, when the workflow pauses, and when the
agent interrupts.

Short mode reference:

1. `reviewed`: counterfactual pre-sprint preview, questions that change the
   sprint path,
   explicit approval before execution, fuller post-execution summary, manual
   advancement
2. `flow`: short pre-execution note, fuller post-execution report, manual
   advancement
3. `auto`: internal pre-execution analysis, concise post-execution report,
   automatic advancement unless interruption is warranted
4. `continuous` (`yolo`): internal analysis and artifact updates, no routine
   user-facing sprint notes, continue until a major blocker or conflict
   requires abort or pause

Mode precedence:

1. explicit user turn override
2. persisted artifact mode
3. default fallback = `reviewed`

Persistence:

1. initiatives persist mode in initiative artifacts
2. lightweight specs persist mode in `spec.md`
3. direct bounded work uses mode as runtime behavior only unless promoted

When follow-up questions are needed, the preferred host path is
`AskUserQuestion` / `vscode/askQuestions`.
When that tool is unavailable, the workflow should use text questions with:

1. `(*)` on the best qualitative fit
2. a short explanation under every option in `(...)`
3. a final `Custom` option
4. the same decision structure as the reviewed-mode preview pattern in the
   workflow contract, not just the same typography

In `reviewed` mode, start approval is itself a checkpoint.
That means the workflow should not silently move from “sprint is ready” to
“sprint is executing”.
It should first surface the pre-sprint preview of what would happen if the
sprint started now, then ask any questions that change the sprint path, and only
then ask for explicit approval to start the sprint.
In `reviewed` mode, that approval must come in a later reply after the preview
is shown.

For non-trivial reviewed-mode sprints, that preview should read like a short
decision note, not a bookkeeping note.
Lead with:

1. `What Repo Truth Says`
2. `Inference`
3. `Implementation Paths`
4. `Recommendation`
5. `Questions That Change The Sprint Path`
6. explicit approval boundary

Artifact or validation notes can still appear, but they should not be the
opening content unless they are themselves the repo truth that materially
changes the sprint.
<!-- #endregion Modes -->

<!-- #region Entry Points -->
## Primary Entry Point

The primary entrypoint is the custom agent:

- `.github/agents/ub-workflow.agent.md`

Use the agent when:

1. you are not sure which initiative step comes next
2. you want to scaffold a new initiative
3. you want to resume paused initiative work
4. you want help with PRD, roadmap, sprint, or final-audit flow

The agent is designed to classify intent for you.
You should not need to memorize many commands.

## Suggested Arguments

The skill and the companion agent currently hint these entry words:

1. `overview`
2. `scaffold`
3. `spec`
4. `resume`
5. `prd`
6. `roadmap`
7. `sprint`
8. `audit`
9. `archive`
10. `what-next`

Treat these as guidance, not a rigid command language.

If you forget them, plain language should still work.
<!-- #endregion Entry Points -->

<!-- #region Usage -->
## Common Real-World Uses

### Start A New Initiative

Examples:

```text
Use initiative flow to scaffold a new initiative for parser performance work.
```

```text
Create a new initiative from ./tmp/todo/parser-performance-prd.md.
```

Expected behavior:

1. the agent classifies this as scaffold or new-initiative setup
2. it uses the scaffold helper when appropriate
3. it copies the source PRD into `./prd.md` without rewriting it
4. it explains the roadmap-planning step after scaffolding
5. it makes the default interaction mode explicit unless the user chose a
   different one
6. in `reviewed` mode, it stops for an explicit start checkpoint before any
   sprint execution begins

### Shape A PRD

Examples:

```text
I have a rough idea. Help me turn it into a PRD another engineer could execute later.
```

```text
Use initiative flow to refine this into an execution-ready PRD.
```

Expected behavior:

1. the agent starts by surfacing assumptions, unknowns, and constraints
2. it makes an explicit scale decision between direct bounded work,
   lightweight spec work, and full initiative PRD work
3. when full-initiative scope is justified, it stays in PRD-shaping mode
4. it clarifies goals, non-goals, scope, risks, and options
5. it does not jump straight to sprinting

### Shape A Lightweight Spec

Examples:

```text
This is bigger than a quick fix but still smaller than a whole initiative. Make a lightweight spec for it.
```

```text
Use initiative flow, but keep this in the lightweight-spec lane unless you find it truly needs roadmap and sprints.
```

Expected behavior:

1. the agent surfaces assumptions, unknowns, and constraints first
2. it records why this is not just a direct bounded task
3. it records why this does not yet need a full initiative
4. it creates or refines a self-contained `spec.md`
5. it leaves promotion to a full initiative explicit instead of implied
6. it records the active interaction mode in the spec snapshot

### Generate The Roadmap

Examples:

```text
The PRD is ready. Generate the roadmap but do not initialize sprint folders yet.
```

```text
Split this finished PRD into a full roadmap with standalone sprints.
```

Expected behavior:

1. the roadmap is generated in one pass
2. sprint order and dependencies are explicit
3. the final audit remains the last roadmap item
4. sprint folders are not initialized in this step
5. the agent surfaces a review checklist and waits for explicit human approval before `roadmap_ready: pass`

### Prepare The Sprint Pack

Examples:

```text
The roadmap is approved. Prepare the sprint pack before we start Sprint 01.
```

```text
Make each sprint PRD execution-ready, but do not start implementation yet.
```

Expected behavior:

1. the agent prepares each planned sprint so `sprint.md` is no longer a
 placeholder shell
2. roadmap subtasks are expanded into richer execution slices instead of
   staying flat checklist items only
3. each slice prompts for acceptance, verification, dependencies, and likely
   touched areas where those details matter
4. concrete scope, validation, and handoff expectations are written into each
 sprint PRD
5. the agent respects the current interaction mode for how much of this
   preparation is surfaced to the user
6. the agent stops after sprint preparation so a human can review before sprint
 execution or helper redesign work continues
7. in `reviewed` mode, the next sprint still requires its own explicit
   pre-sprint preview after sprint-pack preparation is done

### Initialize The Sprint Set

Examples:

```text
The roadmap is approved. Initialize the sprint set now.
```

```text
Use the approved roadmap to create the sprint folders.
```

Expected behavior:

1. the agent confirms the roadmap is ready first
2. it initializes the numbered sprint folders from the roadmap when directory
 creation is still needed
3. it preserves any prepared sprint content rather than reverting to placeholder
 shells
4. it stops after initialization
5. sprint execution remains a separate explicit user request

### Resume An Initiative

Examples:

```text
Resume the initiative in ./.ub-workflows/initiatives/2026-04-02-parser-performance.
```

```text
I lost track of where we are in this initiative. What comes next?
```

Expected behavior:

1. the agent reads the initiative in resume order
2. it reports current phase, gate state, blocker, and next action
3. it does not reopen the whole initiative from scratch unless needed
4. in `reviewed` mode, it surfaces a distinct pre-sprint preview and approval
   checkpoint before sprint execution resumes

### Guide The Active Sprint

Examples:

```text
Only help me with the current sprint.
```

```text
Guide the active sprint without changing the roadmap.
```

Expected behavior:

1. the agent keeps scope bounded to the active sprint
2. it identifies the next implementation or validation step
3. it preserves roadmap and closeout discipline
4. it does not treat placeholder-only sprint shells as executable state
5. it respects the active interaction mode for pre-execution visibility,
   post-execution reporting, and pause behavior
6. it still refuses to execute a sprint that is not actually ready
7. in `reviewed` mode, it records the pre-sprint preview, resolves any
   questions that change the sprint path, and waits for explicit approval
   before execution begins
8. in `reviewed` mode, a request like `Start the next sprint.` opens the
   preview only; it does not start execution in the same turn

### Run Final Audit

Examples:

```text
Run the final audit for this initiative.
```

```text
I think this initiative is done. Verify whether we can close it.
```

Expected behavior:

1. the agent checks for missing closeouts or retained note work
2. it asks about follow-up audits or refactors
3. it prepares the initiative for durable closure

### Switch Interaction Mode

Examples:

```text
Use workflow in reviewed mode for this initiative.
```

```text
Switch this initiative to auto mode.
```

```text
Use yolo mode for this lightweight spec once the plan is execution-ready.
```

Expected behavior:

1. the agent explains mode changes in terms of visibility, pause behavior, and
   interruption behavior
2. it does not treat a mode change as permission to bypass workflow readiness
3. it records the new mode in the durable artifact when the lane supports
   persistence
4. it still uses runtime-only mode behavior for direct bounded work

### Archive A Completed Initiative

Examples:

```text
Archive this completed initiative.
```

```text
Move ./.ub-workflows/initiatives/2026-04-02-parser-performance into the archive if it is actually complete.
```

Expected behavior:

1. the agent verifies completion readiness first
2. it uses the deterministic helper directly when tooling permits, otherwise it provides the exact command
3. it keeps archive actions explicit and never archives by assumption
<!-- #endregion Usage -->

<!-- #region Recovery -->
## Workflow Recovery

One of the main reasons to use the agent is recovery when people skip steps.

Typical recovery prompts:

```text
I skipped the roadmap and already created sprint folders by hand. Can we keep going?
```

```text
We finished implementation, but I never wrote the retained note.
```

```text
I only have research notes. Should I start sprinting?
```

Expected recovery behavior:

1. identify the missing prerequisite
2. explain why it matters
3. recommend the smallest correct next step

Typical missing prerequisites now include:

1. roadmap approval before sprint preparation
2. sprint-pack preparation before sprint execution
3. final audit review before archive
<!-- #endregion Recovery -->

<!-- #region Handoffs -->
## Handoffs

The agent currently provides these handoffs:

1. `Scaffold Initiative`
2. `Resume Initiative`
3. `Shape PRD`
4. `Generate Roadmap`
5. `Prepare Sprint Pack`
6. `Initialize Sprint Set`
7. `Operate Active Sprint`
8. `What Next?`
9. `Final Audit`
10. `Archive Initiative`
11. `Execute Active Sprint`

The intended sequence is:

1. `Scaffold Initiative`
2. `Shape PRD` when needed
3. `Generate Roadmap`
4. `Prepare Sprint Pack`
5. `Initialize Sprint Set`
6. `Operate Active Sprint`
7. `Final Audit`
8. `Archive Initiative`

Use handoffs when the next action is obvious and you want a fast transition.
<!-- #endregion Handoffs -->

<!-- #region Scaffolding -->
## Deterministic Scaffolding

For repeatable setup in this repository, use:

```text
uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>
uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py prepare-sprints <initiative-root>
uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints <initiative-root>
uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive <initiative-root>
```

In an adopting repository, resolve the equivalent local Python runner first.

The helper:

1. bootstraps `./.ub-workflows/` when it is missing
2. creates dated initiative roots under `./.ub-workflows/initiatives/`
3. copies the source PRD into the initiative root as `./prd.md`
4. prepares roadmap-derived sprint PRDs when explicit sprint-pack preparation is requested
5. materializes every planned sprint directory from the roadmap only after roadmap approval
6. blocks unsafe reruns against populated initiative roots or incomplete sprint directories
7. archives completed initiatives on explicit request only

The helper currently handles deterministic directory and control-file
operations.

It does not, by itself, guarantee execution-ready sprint PRDs, so sprint-pack
preparation remains a separate workflow step before any sprint begins.

A fresh scaffold can still be phase-correct even when placeholder findings are
reported.
Treat that output as “valid for this phase, incomplete for the next phase”
unless strict readiness is being checked.
Treat `prepare-sprints` and `init-sprints` the same way:
they prepare execution, but they do not mean Sprint 01 or any later sprint has
already started.

The agent should use the helper directly when tooling permits it.

If the agent cannot execute the helper directly, it should provide the exact
command instead of paraphrasing it.
<!-- #endregion Scaffolding -->

<!-- #region Smoke Prompts -->
## Smoke Prompt Set

Use these prompts later when iterating on the agent.

### Core Prompts

1. `I want to start a new initiative for improving parser performance across the engine and docs.`
2. `Use workflow to set up a new initiative at ./.ub-workflows/initiatives/2026-04-02-parser-performance for the Platform Team.`
3. `I already have the idea, but I need help turning it into a self-contained PRD another engineer could execute later.`
4. `The PRD is done. Split it into a full roadmap, but do not initialize sprint folders yet.`
5. `The roadmap looks correct. I approve it. Mark roadmap_ready: pass and prepare the sprint pack.`
6. `The sprint pack is ready. Initialize the sprint set, but do not start implementation yet.`
7. `Execute only the current active sprint, then stop so I can review the result.`
8. `Resume the initiative in ./.ub-workflows/initiatives/2026-04-02-parser-performance and tell me what to do next.`
9. `I am in the middle of this initiative and I only want help with the current sprint.`
10. `I think this initiative is basically done. Can you verify whether we can close it?`
11. `Archive this initiative if it is actually complete and all required files are current.`
12. `What comes next here? I am not sure whether I should edit the PRD, generate the roadmap, prepare the sprint pack, or start implementing.`
13. `Switch this initiative to flow mode and keep giving me short pre-sprint notes without pausing before execution.`
14. `Use workflow in auto mode and continue through the prepared sprints unless a material conflict forces you to stop.`

### Governance Prompts

1. `Use initiative flow with a Level 1 governance bridge for this initiative.`
2. `This initiative needs Level 2 governance with the lean profile because the audit trail matters.`
3. `Record an exception for this governed sprint and tell me what metadata is required.`

### Recovery Prompts

1. `I skipped the roadmap and already created two sprint folders by hand. Can we just keep going?`
2. `I only have some research notes and half a PRD. Should I start sprinting?`
3. `We finished the implementation work, but I never wrote a retained note or asked about follow-up audits.`

### Out-Of-Scope Prompts

These should redirect instead of overreaching:

1. `Explain TG003 and how it affects our test suite.`
2. `Fix the failing parser tests in the current branch.`
3. `What is the best architecture for a new plugin system?`
<!-- #endregion Smoke Prompts -->

<!-- #region Iteration -->
## Iteration Notes

When improving the skill or agent later, review these areas first:

1. did the agent classify the user intent correctly?
2. did it ask too many or too few clarifying questions?
3. did it recover cleanly when the workflow was broken?
4. did it keep initiative orchestration separate from governance-only or coding-only work?
5. did the handoffs make the next step obvious?
6. did it make validation and documentation synchronization explicit enough to close a sprint safely?
<!-- #endregion Iteration -->

<!-- #region References -->
## References

- `SKILL.md`
- `references/workflow-contract.md`
- `references/artifact-contracts.md`
- `references/scaffold-helper.md`
- `.github/agents/ub-workflow.agent.md`
<!-- #endregion References -->
