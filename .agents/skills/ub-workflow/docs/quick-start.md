# UB Workflow Quick Start

Use `ub-workflow` when the work is big enough that chat history alone is not a
safe system of record.

## Start Here

`ub-workflow` has three lanes:

1. direct bounded work
   Use this when the task is small and does not need a durable planning
   artifact.
2. lightweight spec
   Use this for smaller one-offs that still need assumptions, scope, and
   validation written down.
3. initiative
   Use this for broader, higher-impact, multi-session work.
   This is the main planning driver for bigger areas because it gives you a
   PRD, roadmap, sprint preparation, sprint execution, final audit, and
   archive flow.

## Rule Of Thumb

If the work is a bounded one-off, start with a spec.

If the work will likely span multiple sessions, affect multiple areas, or
benefit from stepwise delivery and review, start an initiative.

## What An Initiative Actually Means

An initiative is not “extra paperwork.”
It is the durable planning surface for bigger work:

1. shape the PRD
2. generate and approve the roadmap
3. prepare the sprint pack
4. initialize the sprint set
5. execute one sprint at a time or continue by mode
6. run the final audit
7. write the retained note and archive intentionally

Fresh scaffold note:

1. a newly scaffolded initiative or lightweight spec can be valid for its
   current phase even when placeholder findings are still present
2. treat those findings as next-phase readiness markers unless strict
   readiness for the next phase is being checked
3. do not confuse “still incomplete for later work” with “broken now”
4. do not confuse “sprint pack ready” with “execution started”; opening or
   initializing sprint artifacts is still pre-execution until the active
   sprint is explicitly started

## Modes At A Glance

1. `reviewed`
   Counterfactual pre-sprint preview, path-shaping questions when needed,
   explicit approval before execution, full post-sprint summary, and manual
   advancement.
2. `flow`
   Short pre-step note, fuller post-step reporting, manual advancement.
3. `auto`
   Internal pre-step analysis, concise post-step reporting, automatic
   advancement unless interruption is needed.
4. `continuous` (`yolo`)
   Internal planning and artifact updates, no routine user-facing sprint notes,
   continue until a major blocker or conflict requires a stop.

Modes do not weaken readiness rules.
They only change visibility, pause behavior, and interruption behavior.

In `reviewed` mode, “ready to start” is not the same thing as “already
started”.
The sprint should stop for a pre-sprint preview of what it would do if started
now, then resolve any questions that change the sprint path, and only then ask for explicit
approval before execution begins.
A prompt like `Start the next sprint.` opens that preview, but execution starts
only after a later approval message.

For non-trivial reviewed-mode sprints, that preview should read like a short
decision note:
`What Repo Truth Says`, `Inference`, `Implementation Paths`,
`Recommendation`, then the questions that change the sprint path.

## Good First Prompts

```text
Help me decide whether this should be direct work, a spec, or a full initiative.
```

```text
This is a bounded one-off. Make a lightweight spec for it.
```

```text
This is a bigger impact area. Start an initiative and help me shape the PRD.
```

```text
I already have an initiative. Resume it and tell me what comes next.
```

## If You Are Unsure

Use the workflow agent and ask in plain language.

The agent should classify the work, explain the smallest correct next step, and
surface help without requiring you to memorize the full lifecycle first.
