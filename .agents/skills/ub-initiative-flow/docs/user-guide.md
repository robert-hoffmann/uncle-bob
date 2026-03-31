# UB Initiative Flow User Guide

## Purpose

This guide explains how to use `ub-initiative-flow` in day-to-day repository
work.

Use it for two jobs:

1. operating the skill and companion agent as a human user
2. iterating on the skill and agent later with a stable usage baseline

## Mental Model

`ub-initiative-flow` is the planning and orchestration layer for larger work.

It exists for initiatives that are too large, risky, or multi-session to run
reliably from chat history alone.

The core lifecycle is:

1. discovery and research
2. self-contained PRD
3. roadmap generated in one pass
4. all sprint folders initialized up front
5. standalone resumable sprint execution
6. final audit
7. retained note

## Primary Entry Point

The primary entrypoint is the custom agent:

- `.github/agents/ub-initiative-flow.agent.md`

Use the agent when:

1. you are not sure which initiative step comes next
2. you want to scaffold a new initiative
3. you want to resume paused initiative work
4. you want help with PRD, roadmap, sprint, or final-audit flow

The agent is designed to classify intent for you.
You should not need to memorize many commands.

## Suggested Arguments

The agent currently hints these entry words:

1. `overview`
2. `scaffold`
3. `resume`
4. `prd`
5. `roadmap`
6. `sprint`
7. `audit`
8. `what-next`

Treat these as guidance, not a rigid command language.

If you forget them, plain language should still work.

## Common Real-World Uses

### Start A New Initiative

Examples:

```text
Use initiative flow to scaffold a new initiative for parser performance work.
```

```text
I want to start a new initiative at ./tmp/sprints/initiatives/2026-04-02-parser-performance.
```

Expected behavior:

1. the agent classifies this as scaffold or new-initiative setup
2. it uses the scaffold helper when appropriate
3. it explains the next planning step after scaffolding

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
The PRD is ready. Generate the roadmap and initialize the sprint folders.
```

```text
Split this finished PRD into a full roadmap with standalone sprints.
```

Expected behavior:

1. the roadmap is generated in one pass
2. sprint order and dependencies are explicit
3. the final audit remains the last roadmap item

### Resume An Initiative

Examples:

```text
Resume the initiative in ./tmp/sprints/initiatives/2026-04-02-parser-performance.
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

## Handoffs

The agent currently provides these handoffs:

1. `Scaffold Initiative`
2. `Resume Initiative`
3. `Shape PRD`
4. `Generate Roadmap`
5. `Initialize Sprint Set`
6. `Guide Active Sprint`
7. `What Next?`
8. `Final Audit`
9. `Execute Implementation`

Use handoffs when the next action is obvious and you want a fast transition.

## Deterministic Scaffolding

For repeatable setup, use:

```text
python .agents/skills/ub-initiative-flow/scripts/scaffold_initiative.py <target-root>
```

The helper:

1. copies the canonical scaffold
2. fills the most important placeholders
3. blocks reruns against populated initiative roots

## Smoke Prompt Set

Use these prompts later when iterating on the agent.

### Core Prompts

1. `I want to start a new initiative for improving parser performance across the engine and docs.`
2. `Use initiative flow to set up a new initiative at ./tmp/sprints/initiatives/2026-04-02-parser-performance for the Platform Team.`
3. `I already have the idea, but I need help turning it into a self-contained PRD another engineer could execute later.`
4. `The PRD is done. Split it into a full roadmap and initialize all sprint folders.`
5. `Resume the initiative in ./tmp/sprints/initiatives/2026-04-02-parser-performance and tell me what to do next.`
6. `I am in the middle of this initiative and I only want help with the current sprint.`
7. `I think this initiative is basically done. Can you verify whether we can close it?`
8. `What comes next here? I am not sure whether I should edit the PRD, generate the roadmap, or start implementing.`

### Recovery Prompts

1. `I skipped the roadmap and already created two sprint folders by hand. Can we just keep going?`
2. `I only have some research notes and half a PRD. Should I start sprinting?`
3. `We finished the implementation work, but I never wrote a retained note or asked about follow-up audits.`

### Out-Of-Scope Prompts

These should redirect instead of overreaching:

1. `Explain TG003 and how it affects our test suite.`
2. `Fix the failing parser tests in the current branch.`
3. `What is the best architecture for a new plugin system?`

## Iteration Notes

When improving the skill or agent later, review these areas first:

1. did the agent classify the user intent correctly?
2. did it ask too many or too few clarifying questions?
3. did it recover cleanly when the workflow was broken?
4. did it keep initiative orchestration separate from governance-only or coding-only work?
5. did the handoffs make the next step obvious?

## References

- `SKILL.md`
- `references/workflow-contract.md`
- `references/artifact-contracts.md`
- `references/scaffold-helper.md`
- `.github/agents/ub-initiative-flow.agent.md`