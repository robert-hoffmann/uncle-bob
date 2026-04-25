# uncle-bob

> Repository-level agent instructions and skill registry.

## Version & Tooling Policy

Skills MUST NOT hardcode version numbers. Detect the project's actual versions from `package.json`, lockfiles, and `pyproject.toml`. Use web search to verify latest stable patterns. When the project's version differs from latest stable, note the gap and recommend an upgrade path.

## Shell Entry Points

Use these command-entry defaults when working in this repository:

1. use `uv run python ...` for repository Python scripts, tests, and helper
   tooling
2. for short ad hoc local inspection when `uv` is not needed, use the
   interpreter command that matches the local environment rather than assuming
   one universal fallback name
3. prefer interpreter-explicit commands and confirm the command exists in the
   current environment before relying on it
4. prefer `task` wrappers when the repository already exposes a check or helper
   through `Taskfile.yml`

## Policy Versus Defaults

This repository is intentionally opinionated, but not every opinion has the
same status.

Repository policy means the rule is explicitly part of the repository contract
and is often backed by validation, integrity checks, or mandatory skill
instructions.

Strong defaults mean the repository currently recommends the approach because it
fits best here, while downstream adopters may still need to adapt it
deliberately.

Freshness review for volatile framework and tool guidance is warning-only by
default. Do not turn freshness into a blocking gate unless the repository
explicitly promotes it beyond advisory status.

| Technology   | Version Policy      | Primary Tool     | Fallback |
| ------------ | ------------------- | ---------------- | -------- |
| Node.js      | Latest LTS          | bun              | npm/node |
| Python       | Latest stable       | uv               | pip      |
| TypeScript   | Latest stable       | (via bun or npm) | —        |
| Vue          | Latest stable       | —                | —        |
| Nuxt         | Latest stable       | —                | —        |
| Tailwind CSS | Latest stable       | —                | —        |
| Pydantic     | Latest stable (v2+) | —                | —        |

## Repository And Distribution Boundaries

This repository is the authoring and validation factory for the distributable
agent customizations. Do not assume every repository file ships to downstream
projects.

Distributable surfaces:

1. `.agents/skills/`
   The portable skill payload. Skills may depend on their own `SKILL.md`,
   `references/`, `assets/`, `scripts/`, and explicitly named sibling skills.
   Skills must not depend on repo-maintenance scripts, root `Taskfile.yml`, CI,
   plugin metadata, root documentation, `.ub-workflows/`, or optional agents.
2. `.github/agents/ub-teacher.agent.md`
   The optional teaching-agent payload. The agent may know about itself and the
   skills. Skills must not require this agent or mention it as a runtime
   dependency.
3. Repository-only surfaces
   `AGENTS.md`, `README.md`, `Taskfile.yml`, `pyproject.toml`, `plugin.json`,
   `.github/workflows/`, `scripts/repo-maintenance/`, `tests/`, `docs/`, and
   factory workflow artifacts are repository truth. These files may know about
   the skills, the optional agent, packaging, CI, and validation rules.

When editing:

1. Keep files under `.agents/skills/` host-agnostic, repo-agnostic, and
   portable unless the skill explicitly owns the referenced asset or helper.
2. Keep `ub-teacher` independent from factory-only paths except where it needs
   to locate the distributable skills in this repository.
3. Put factory-only planning, validation, release, and maintenance knowledge in
   repository-only surfaces, not inside distributable skill contracts.
4. If a downstream project needs repo behavior, bundle it through skill-owned
   `scripts/` or `assets/`, or describe how to detect and adapt the target
   project instead of pointing at this repository's root tooling.

## Documentation Synchronization Policy

This repository has three active truth surfaces:

1. `.agents/skills/` and `.github/agents/`
   These are runtime and distribution truth for the installed skills and custom
   agents.
2. `docs/` and `README.md`
   These are published explanation truth for humans evaluating and adopting
   the portable skills.
3. `AGENTS.md`, `Taskfile.yml`, `.github/workflows/`, `scripts/`, and
   repo-maintenance checks
   These are repository-control truth for local workflow, CI, validation, and
   synchronization rules.

Keep those surfaces synchronized. Documentation drift is a defect when any of
the following are true:

1. a real skill under `.agents/skills/` has no matching published docs page
2. docs mention a skill, custom agent, command, workflow, or path that no
   longer exists
3. skill or custom-agent behavior changes without matching documentation
   updates
4. public docs describe repository-maintenance internals instead of portable
   skill behavior
5. documentation introduces behavior, guarantees, or workflow steps that the
   skill contracts do not support
6. workflow, validation, deployment, or command docs no longer match
   `Taskfile.yml`, `package.json`, scripts, or GitHub Actions

Synchronization is bidirectional:

1. When editing any skill or custom agent, update the affected docs in the same
   change or explicitly state why no docs change is needed.
2. When editing docs, verify the described behavior against the real skill,
   agent, workflow, script, or config surface.
3. Keep public VitePress docs focused on portable skill behavior, skill usage,
   skill interaction, install flow, and diagrams that explain skill contracts.
4. Keep repository-maintenance details in `README.md`, `AGENTS.md`,
   `.github/workflows/README.md`, or repo-maintenance scripts instead of the
   public site.
5. Do not copy old reports into deep-dive docs. Use reports as research input,
   then verify claims against current `SKILL.md` and reference files.
6. When new docs conventions become deterministic, update
   `scripts/check-docs-sync.mjs` in the same change.
7. Do not make docs-sync warning-only unless this repository explicitly changes
   that policy.

Before finishing a change that touches skills, agents, docs, commands,
workflows, or repo-maintenance behavior, run the smallest relevant validation
set:

1. `task check` for the Python, YAML, catalog, governance, and workflow
   integrity baseline
2. `npm run check:docs-sync` when docs, skills, agents, commands, workflows, or
   repository paths are affected
3. `npm run docs:build` when docs content, docs configuration, package
   metadata, or Pages deployment changes
4. selected governance or workflow checks when ADR, claim, evidence, or
   workflow-control behavior is affected

If a check is intentionally skipped, state the reason and the remaining risk.

## Mandatory Skills

Always load these skills for every task — no exceptions.

| Skill          | Description                                                                                                            | Path                                 |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| **ub-quality** | Cross-language code quality standards for design patterns, formatting, documentation, code structure, and refactoring. | `.agents/skills/ub-quality/SKILL.md` |

`ub-quality` is mandatory and must not be skipped. Its `SKILL.md` body is the
always-loaded baseline; its deeper references are loaded by the explicit
trigger rules inside the skill before producing work that depends on them.

## Skills

| Skill             | Description                                                                                                                                      | Path                                        |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| ub-quality        | Cross-language code quality: design patterns, formatting, documentation, structure, refactoring.                                                 | `.agents/skills/ub-quality/SKILL.md`        |
| ub-authoring      | Shared authoring conventions for routing quality, non-use boundaries, naming, progressive disclosure, and reusable skill guidance.               | `.agents/skills/ub-authoring/SKILL.md`      |
| ub-css            | Plain CSS & Vue/Nuxt style blocks: design tokens, cascade layers, native nesting, container queries, progressive enhancement.                    | `.agents/skills/ub-css/SKILL.md`            |
| ub-nuxt           | Nuxt (latest stable): typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, app-directory semantics.                 | `.agents/skills/ub-nuxt/SKILL.md`           |
| ub-python         | Python (latest stable): typed patterns, boundary validation, structured error handling, pytest/ruff/mypy workflows.                              | `.agents/skills/ub-python/SKILL.md`         |
| ub-tailwind       | Tailwind CSS (latest stable): setup, migration, debugging across standalone HTML, Vue + Vite, and Nuxt projects.                                 | `.agents/skills/ub-tailwind/SKILL.md`       |
| ub-ts             | TypeScript (latest stable): typing, module/moduleResolution, compiler flags, tsconfig architecture.                                              | `.agents/skills/ub-ts/SKILL.md`             |
| ub-vuejs          | Vue (latest stable): SFCs, composables, reactivity, watchers, SSR/hydration, component contracts with strict TypeScript.                         | `.agents/skills/ub-vuejs/SKILL.md`          |
| ub-governance     | Governance routing for testing posture, evidence/ADR/claim decisions, repository controls, exception handling, and escalation boundaries.        | `.agents/skills/ub-governance/SKILL.md`     |
| ub-customizations | VS Code Copilot customization builder: creates skills, prompts, agents, hooks, MCP configs, plugins, and bundles.                                | `.agents/skills/ub-customizations/SKILL.md` |
| ub-workflow       | Direct work, lightweight specs, and initiatives with roadmaps, resumable sprints, audit, and archive flow.                                       | `.agents/skills/ub-workflow/SKILL.md`       |

## Agents

| Agent             | Description                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------------- |
| ub-teacher        | Teaching and explanation agent for readable, beginner-friendly code walkthroughs.             |

## Prompts

*No `.prompt.md` files defined yet.*

## Instructions

*No `.instructions.md` files defined yet.*
