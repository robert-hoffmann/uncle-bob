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
