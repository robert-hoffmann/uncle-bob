# itech-agents

> Repository-level agent instructions and skill registry.

## Version & Tooling Policy

Skills MUST NOT hardcode version numbers. Detect the project's actual versions from `package.json`, lockfiles, and `pyproject.toml`. Use web search to verify latest stable patterns. When the project's version differs from latest stable, note the gap and recommend an upgrade path.

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

| Skill            | Description                                                                                                            | Path                                   |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **ub-quality**   | Cross-language code quality standards for design patterns, formatting, documentation, code structure, and refactoring. | `.agents/skills/ub-quality/SKILL.md`   |

## Skills

| Skill             | Description                                                                                                                      | Path                                                |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| ub-quality        | Cross-language code quality: design patterns, formatting, documentation, structure, refactoring.                                 | `.agents/skills/ub-quality/SKILL.md`                |
| ub-css            | Plain CSS & Vue/Nuxt style blocks: design tokens, cascade layers, native nesting, container queries, progressive enhancement.    | `.agents/skills/ub-css/SKILL.md`                    |
| ub-nuxt           | Nuxt (latest stable): typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, app-directory semantics. | `.agents/skills/ub-nuxt/SKILL.md`                   |
| ub-python         | Python (latest stable): typed patterns, boundary validation, structured error handling, pytest/ruff/mypy workflows.              | `.agents/skills/ub-python/SKILL.md`                 |
| ub-tailwind       | Tailwind CSS (latest stable): setup, migration, debugging across standalone HTML, Vue + Vite, and Nuxt projects.                 | `.agents/skills/ub-tailwind/SKILL.md`               |
| ub-ts             | TypeScript (latest stable): typing, module/moduleResolution, compiler flags, tsconfig architecture.                              | `.agents/skills/ub-ts/SKILL.md`                     |
| ub-vuejs          | Vue (latest stable): SFCs, composables, reactivity, watchers, SSR/hydration, component contracts with strict TypeScript.         | `.agents/skills/ub-vuejs/SKILL.md`                  |
| ub-governance     | Unified governance: repo governance, testing/TDD, evidence/ADR/claim governance, shared contracts.                               | `.agents/skills/ub-governance/SKILL.md`             |
| ub-customizations | VS Code Copilot customization builder: creates skills, prompts, agents, instructions, hooks, MCP configs, plugins, and bundles.  | `.agents/skills/ub-customizations/SKILL.md`         |

## Agents

| Agent             | Description                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| Explore           | Fast read-only codebase exploration and Q&A subagent. Supports quick / medium / thorough modes. |
| ub-governance     | Interactive governance guide grounded in the ub-governance skill and references.                |
| ub-teacher        | Teaching and explanation agent for readable, beginner-friendly code walkthroughs.               |
| ub-customizations | Interactive Copilot customization builder with classify/generate/validate/iterate workflow.     |

## Prompts

*No `.prompt.md` files defined yet.*

## Instructions

*No `.instructions.md` files defined yet.*
