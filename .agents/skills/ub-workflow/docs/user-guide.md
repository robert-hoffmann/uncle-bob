<!-- #region Purpose -->
# UB Workflow User Guide

## Purpose

This guide explains how to use `ub-workflow` in day-to-day repository
work.

Use it for two jobs:

1. operating the skill and companion agent as a human user
2. iterating on the skill and agent later with a stable usage baseline
<!-- #endregion Purpose -->

<!-- #region Mental Model -->
## Mental Model

`ub-workflow` is the planning and orchestration layer for larger work.

It exists for initiatives that are too large, risky, or multi-session to run
reliably from chat history alone.

The core lifecycle is:

1. discovery and research
2. self-contained PRD
3. roadmap generated and approved in one pass
4. sprint pack prepared so each planned `sprint.md` is execution-ready
5. sprint folders materialized when needed from the approved roadmap
6. standalone resumable sprint execution, one sprint per explicit user request
7. final audit
8. retained note
<!-- #endregion Mental Model -->

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
3. `resume`
4. `prd`
5. `roadmap`
6. `sprint`
7. `audit`
8. `archive`
9. `what-next`

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

### Shape A PRD

Examples:

```text
I have a rough idea. Help me turn it into a PRD another engineer could execute later.
```

```text
Use initiative flow to refine this into an execution-ready PRD.
```

Expected behavior:

1. the agent stays in PRD-shaping mode
2. it clarifies goals, non-goals, scope, risks, and options
3. it does not jump straight to sprinting

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
2. concrete scope, validation, and handoff expectations are written into each
 sprint PRD
3. the agent stops after sprint preparation so a human can review before sprint
 execution or helper redesign work continues

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
5. it stops after the active sprint work and waits for human review before any
 next sprint work

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

For repeatable setup, use:

```text
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py prepare-sprints <initiative-root>
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints <initiative-root>
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive <initiative-root>
```

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
