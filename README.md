# Uncle Bob

<table>
<tr>
<td width="300">
<img src="docs/assets/uncle-bob.png" alt="Uncle Bob" width="280" />
</td>
<td>

Uncle Bob is a practical collection of skills and a focused teaching agent for GitHub Copilot in VS Code, Copilot CLI, Claude Code, and Codex users. It gives agentic coding tools stronger defaults for planning, quality, governance, authoring, and implementation work without forcing a heavy framework around day-to-day development.

I use these skills in an actual corporate production environment for supply-chain management in the aerospace industry.

</td>
</tr>
</table>

## What This Is

This repository is a practical operating system for guided agentic coding work.

Its center of gravity is not the framework-specific skills.
The real backbone is:

1. `ub-workflow` for planning, specs, initiatives, sprints, audit, and archive
2. `ub-quality` for the always-on baseline of structure, clarity, and code or doc hygiene
3. `ub-governance` for evidence, decision memory, testing, and repository-control discipline

The language and framework skills matter, but they are supporting specialists.
They plug into the workflow once the work has been shaped and routed correctly.

## Why Use It

Use it when you want your coding agent to work through a clearer system instead of acting like a collection of disconnected prompts.

The repository is designed so bigger work starts with the right planning surface,
moves through explicit review points, and stays resumable across sessions.
That is why `ub-workflow` is the main driver: it decides whether the work should
stay direct, become a lightweight spec, or grow into a full initiative with a
PRD, roadmap, sprint preparation, execution, and final audit.

## Tooling Footnote

For repository Python commands, prefer `uv run python ...`.

Use `python3 ...` only for short ad hoc local inspection when `uv` is not
needed, and do not assume bare `python` exists on `PATH`.

When the repo already exposes a Taskfile entrypoint, prefer that wrapper over a
custom shell command.

## Workflow At A Glance

The planning model in this repo is intentionally tiered:

1. direct bounded work for truly small tasks that do not need a durable
   planning artifact
2. lightweight specs for bounded work that has become planning-heavy enough to
   need assumptions, scope, options, validation, or an execution shape written
   down
3. initiatives for broader, higher-impact work where PRD, roadmap, sprint
   preparation, sprint execution, and final audit improve delivery quality

In practice, specs are the preferred small planning surface, while initiatives
plus sprints are the main driver for bigger impact areas.

If you want guided help choosing the right lane, ask the main coding agent to
explain `ub-workflow` from its skill contract and choose the smallest correct
planning surface.

## Interaction Modes

`ub-workflow` supports four modes that change how visible and hands-on the
execution flow feels. They do not weaken readiness rules. They change how much
analysis is surfaced, when follow-up questions appear, and whether the
workflow pauses between sprints or execution chunks.

1. `reviewed`
   The most interactive and hands-on mode. Before execution, it surfaces the
   analysis, exposes meaningful options when there is a real choice, and asks
   follow-up questions when confirmation or direction is needed. After
   execution, it reports what changed, why it mattered, what to watch out for
   next, and then pauses for manual advancement before the next sprint or
   execution chunk.
2. `flow`
   A little faster and lighter. It still gives a short explanatory note before
   execution and a fuller update after execution, but it does not normally stop
   to ask pre-execution questions unless something important is unclear or
   risky. It still waits for manual advancement after each sprint or chunk.
3. `auto`
   More autonomous. Most pre-execution analysis stays internal, and the updates
   back to the user are shorter and more focused. It keeps moving forward
   automatically unless it hits an interruption condition such as a blocker, a
   conflict, a material ambiguity, or a decision that could significantly
   reshape the work.
4. `continuous` (`yolo`)
   The least interruptive mode. It still does internal analysis, planning, and
   artifact updates, but it does not stop to provide routine before-and-after
   user-facing notes, and it does not pause between sprints unless a major
   blocker, contradiction, or conflict forces the work to stop and be resolved
   before continuing.

## How The Workflow Feels

The main value of this repo is not that it gives an agent more prompts.
It gives the work a better shape.

The intended rhythm looks like this:

1. start with rough R&D, discovery, or problem framing
   Capture what is unclear, what needs to be true, and what level of planning
   the work actually deserves.
2. choose the smallest planning surface that will hold
   Use direct work for very small tasks, a spec for bounded one-offs, and an
   initiative when the work needs a PRD, roadmap, and staged delivery.
3. turn bigger work into explicit sprints
   Instead of one long fuzzy thread, the work gets broken into prepared sprint
   slices with validation focus, dependencies, and likely touched surfaces.
4. execute with durable handoffs
   Each sprint is designed to be resumable. Decisions, evidence, closeout, and
   rollup artifacts make it easier to stop, resume, review, or hand the work
   to another human or agent later.
5. validate and close intentionally
   The workflow is built around proving what changed, surfacing risks, and
   finishing with a final audit instead of letting bigger work fade out in chat
   history.

That is why the workflow layer matters so much here.
It turns agent use into a delivery system:

- research and planning before blind execution
- explicit scope before broad refactors
- sprints for bigger impact areas instead of one sprawling session
- handoffs and validation so progress survives across time, tools, and people

If the work is small, this stays lightweight.
If the work is important, it becomes structured without becoming bureaucratic.

## Prompt-Driven Initiative Flow

If you already have a PRD, the workflow can be driven almost entirely through
prompts while still keeping the work structured and resumable.

The usual progression is:

1. scaffold the initiative from the PRD
   Start by invoking `ub-workflow` once and giving it the PRD. The first prompt
   is simply to scaffold a new initiative from that PRD. That creates the
   working structure and establishes `prd.md` as the source of truth.
2. generate and review the roadmap
   Next, ask it to generate the roadmap from the PRD. Review the roadmap before
   moving forward so the sprint sequence, dependencies, and planned slices are
   correct before execution starts.
3. prepare and initialize the sprint set
   Once the roadmap looks right, ask it to prepare the sprints from that
   roadmap and then initialize them so the sprint structure is ready for
   execution. `reviewed` or `flow` mode is usually the cleanest fit here.
4. execute Sprint 01 with the generated artifacts as context
   Start Sprint 01, work through the sprint using the prepared artifacts as the
   context system, then close out the sprint and prepare the handoff into the
   next one.
5. repeat sprint by sprint until final audit
   From there, the flow becomes intentionally simple: start the next sprint,
   complete the work, close it out, and move forward. When the delivery work is
   done, run the final audit, write the retained note, and archive
   intentionally.

In other words, the prompts drive the workflow, but the artifacts hold the
state. That is the key difference.

You are not relying on one long chat thread to remember what the plan was.
The PRD, roadmap, sprint pack, decision logs, closeouts, and rollups carry the
context forward.

Practical note:

- after a cold restart, it is usually worth resuming in a more context-heavy
  mode first, or simply reusing the existing session when possible, so the
  agent reloads the initiative state before continuing execution

## Core Drivers

These are the three surfaces that explain how the repo actually works:

1. `ub-workflow`
   The orchestration layer. It shapes work into direct tasks, specs, or
   initiatives and then carries larger work through roadmap, sprint,
   final-audit, and archive flow.
2. `ub-quality`
   The mandatory baseline. It keeps code and documents readable, reviewable,
   and consistent across everything else in the repo.
3. `ub-governance`
   The control layer. It defines how evidence, testing posture, ADR usage,
   repository constraints, and exception handling should work.
   The extracted repo-maintenance checks in this development repository are a
   separate surface, not part of the distributable governance command path.

The other skills are implementation specialists that become useful after the
workflow and quality baselines have already done their job.

## What's Included

| Skill             | Description                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------- |
| ub-workflow       | Main planning driver: direct work, specs, initiatives, roadmaps, resumable sprints, audit, archive.                 |
| ub-quality        | Mandatory baseline for code quality, formatting, documentation, and refactoring.                                    |
| ub-authoring      | Shared authoring conventions for routing, non-use boundaries, naming, and progressive disclosure.                   |
| ub-governance     | Governance routing for testing posture, evidence, ADR or claim decisions, repository controls, and exceptions.      |
| ub-customizations | Builder skill for Copilot skills, agents, prompts, instructions, hooks, MCP, and plugin bundles.                    |
| ub-python         | Typed Python patterns, boundary validation, structured error handling, and Ruff-aware repo truth.                   |
| ub-ts             | TypeScript typing, module resolution, compiler flags, tsconfig baselines, and optional ESLint starters.             |
| ub-css            | CSS and Vue/Nuxt styling with design tokens, cascade layers, and progressive enhancement.                           |
| ub-vuejs          | Vue SFCs, composables, reactivity, SSR and hydration, and strict TypeScript contracts.                              |
| ub-nuxt           | Nuxt patterns for typed composables, rendering modes, runtime config, and server routes.                            |
| ub-tailwind       | Tailwind setup, migration, and debugging across HTML, Vue, and Nuxt.                                                |

| Agent             | Description                                                                          |
| ----------------- | ------------------------------------------------------------------------------------ |
| ub-teacher        | Beginner-friendly explanations and code walkthroughs.                                |

## Install Options

There are three practical ways to consume this repo. The best choice depends on
your host tool and how much control you want over updates.

1. Copilot CLI plugin install
   Best fit for GitHub Copilot and Copilot CLI users because GitHub's official
   plugin docs support direct repository installs when `plugin.json` lives at
   the repository root or in `.github/plugin/`, which this repo provides.

   ```bash
   copilot plugin install robert-hoffmann/itech-agents
   ```

   If you prefer marketplace registration for team discovery, GitHub's docs
   also support registering a repository that contains
   `.github/plugin/marketplace.json`:

   ```bash
   copilot plugin marketplace add robert-hoffmann/itech-agents
   ```

   Pros:
   - most native path for Copilot CLI
   - uses the repo's plugin metadata directly
   - keeps agent and skill distribution tied to GitHub's documented plugin flow

   Cons:
   - primarily Copilot-oriented, not the most portable path for non-Copilot
     hosts

2. `skills.sh` install
   Best fit when you want one install/update flow across multiple agent hosts.
   The official `skills` CLI supports repository installs plus agent, skill,
   copy, and update flags, and Claude Code documents compatibility with the
   Agent Skills open standard.

   ```bash
   npx skills add https://github.com/robert-hoffmann/itech-agents
   ```

   Useful follow-ups:

   ```bash
   npx skills add https://github.com/robert-hoffmann/itech-agents --list
   npx skills add https://github.com/robert-hoffmann/itech-agents --skill ub-workflow --agent claude-code codex
   npx skills update
   ```

   Pros:
   - easiest cross-tool story for Claude Code, Codex-style setups, and other
     Agent Skills-compatible environments
   - supports targeted installs and updates
   - avoids hand-managed copy or symlink drift

   Cons:
   - installs whatever is currently pushed to GitHub, not uncommitted local
     changes
   - the public docs are still lighter than the Copilot plugin docs, so the CLI
     help output matters in practice

3. Manual vendoring
   Best fit when a team wants full control over what gets committed into a
   downstream repository. In that model, treat `AGENTS.md`, `.agents/skills/`,
   and `.github/agents/` as the main portable surfaces and manage updates on
   your own terms.

   Pros:
   - maximum control over review, pinning, and local adaptation
   - works even where plugin or skills managers are not allowed

   Cons:
   - highest maintenance overhead
   - easiest path to drift if you stop syncing upstream changes

### How Custom Agents Are Installed

Skills and custom agents do not currently have the same portability story.

1. VS Code Copilot
   Custom agents are workspace-discovered from `.github/agents/*.agent.md`.
   If you vendor this repo manually into another project, include
   `.github/agents/` alongside `.agents/skills/` and `AGENTS.md`.

2. Copilot CLI
   The plugin install path includes custom agents automatically because this
   repo's [plugin.json](./plugin.json) explicitly points its `agents` field to
   `.github/agents/`. After installing, you can verify that the agents loaded
   in a Copilot CLI session with `/agent`.

3. `skills.sh`
   `skills.sh` is excellent for distributing the skills, but it is not the
   install path for these repo-local Copilot custom agents. Its job is to place
   skills into host-specific skill directories, not to vend `.github/agents`
   style agent profiles from this repository.

4. Claude Code and Codex
   This repo is usable there today through skills and instruction surfaces, but
   these specific custom agents are not yet mirrored into host-native agent
   directories such as `.claude/agents/`. So there is not currently a
   first-class one-command custom-agent install story for those hosts from this
   repo alone.

### Support Notes

- VS Code Copilot and Copilot CLI are the strongest native targets today.
  Official docs explicitly support workspace-level agents in `.github/agents`,
  skill discovery under `.agents/skills`, and direct plugin installs from repos
  with `plugin.json`.
- Claude Code is compatible through the Agent Skills open standard and its
  native `.claude/skills` model. The smoothest path from this repo today is
  `skills.sh`, because this repository does not mirror every skill into a
  dedicated `.claude/skills/` tree.
- Codex users are supported through `AGENTS.md` and the broader Agent Skills
  ecosystem. This repo is usable there today, but its most polished packaging
  remains Copilot-first plus `skills.sh`.

For most real work, the best starting point is the main coding agent with
`ub-workflow` available in the repo.
It helps decide whether the work should stay direct, become a lightweight
spec, or become a full initiative.

Use `ub-teacher` when you want explanation-first help instead of execution.

## Philosophy

Keep agentic coding practical. Start with strong quality defaults, add focused domain knowledge only where it helps, and prefer reusable instructions over one-off prompting. The goal is to make coding agents more dependable for day-to-day engineering work, not just better at generating snippets.

## License

MIT. See [LICENSE](LICENSE).
