# Uncle Bob

<table>
<tr>
<td width="300">
<img src="docs/assets/uncle-bob.png" alt="Uncle Bob" width="280" />
</td>
<td>

Uncle Bob is a practical collection of skills and custom agents for GitHub Copilot in VS Code, Copilot CLI, Claude Code, and Codex users. It gives agentic coding tools stronger defaults for planning, quality, governance, and implementation work without forcing a heavy framework around day-to-day development.

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

## Workflow At A Glance

The planning model in this repo is intentionally tiered:

1. direct bounded work for small tasks that do not need a durable planning
   artifact
2. lightweight specs for bounded one-offs that still need assumptions, scope,
   and validation written down
3. initiatives for broader, higher-impact work where PRD, roadmap, sprint
   preparation, sprint execution, and final audit improve delivery quality

In practice, specs are the preferred small planning surface, while initiatives
plus sprints are the main driver for bigger impact areas.

If you want guided help choosing the right lane, start with the
`ub-workflow` agent or the workflow quick start in
[quick-start.md](./.agents/skills/ub-workflow/docs/quick-start.md).

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

The other skills are implementation specialists that become useful after the
workflow and quality baselines have already done their job.

## What's Included

| Skill             | Description                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| ub-workflow       | Main planning driver: direct work, specs, initiatives, roadmaps, resumable sprints, final audit, archive. |
| ub-quality        | Mandatory baseline for code quality, formatting, documentation, and refactoring.                          |
| ub-governance     | Repository, testing, evidence, and decision-memory governance with shared contracts.                      |
| ub-customizations | Builder skill for Copilot skills, agents, prompts, instructions, hooks, MCP, and plugin bundles.          |
| ub-markdown       | Markdown authoring with repo markdownlint alignment for README, skills, agents, docs, and workflow files. |
| ub-python         | Typed Python patterns, boundary validation, structured error handling, and Ruff-aware repo truth.         |
| ub-ts             | TypeScript typing, module resolution, compiler flags, tsconfig baselines, and optional ESLint starters.   |
| ub-css            | CSS and Vue/Nuxt styling with design tokens, cascade layers, and progressive enhancement.                 |
| ub-vuejs          | Vue SFCs, composables, reactivity, SSR and hydration, and strict TypeScript contracts.                    |
| ub-nuxt           | Nuxt patterns for typed composables, rendering modes, runtime config, and server routes.                  |
| ub-tailwind       | Tailwind setup, migration, and debugging across HTML, Vue, and Nuxt.                                      |

| Agent             | Description                                                                          |
| ----------------- | ------------------------------------------------------------------------------------ |
| ub-workflow       | Interactive workflow guide for specs, initiatives, sprints, and what-next decisions. |
| ub-governance     | Interactive guide for repository, testing, and evidence governance.                  |
| ub-customizations | Interactive builder for Copilot customization artifacts.                             |
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

For most real work, the best starting point is still the `ub-workflow` agent.
It helps decide whether the work should stay direct, become a lightweight
spec, or become a full initiative.

## Philosophy

Keep agentic coding practical. Start with strong quality defaults, add focused domain knowledge only where it helps, and prefer reusable instructions over one-off prompting. The goal is to make coding agents more dependable for day-to-day engineering work, not just better at generating snippets.

## License

MIT. See [LICENSE](LICENSE).
