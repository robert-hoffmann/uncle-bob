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
| **code-quality** | Cross-language code quality standards for design patterns, formatting, documentation, code structure, and refactoring. | `.agents/skills/code-quality/SKILL.md` |

## Skills

| Skill         | Description                                                                                                                      | Path                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| code-quality  | Cross-language code quality: design patterns, formatting, documentation, structure, refactoring.                                 | `.agents/skills/code-quality/SKILL.md`  |
| dev-css       | Plain CSS & Vue/Nuxt style blocks: design tokens, cascade layers, native nesting, container queries, progressive enhancement.    | `.agents/skills/dev-css/SKILL.md`       |
| dev-nuxt      | Nuxt (latest stable): typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, app-directory semantics. | `.agents/skills/dev-nuxt/SKILL.md`      |
| dev-python    | Python (latest stable): typed patterns, boundary validation, structured error handling, pytest/ruff/mypy workflows.              | `.agents/skills/dev-python/SKILL.md`    |
| dev-tailwind  | Tailwind CSS (latest stable): setup, migration, debugging across standalone HTML, Vue + Vite, and Nuxt projects.                 | `.agents/skills/dev-tailwind/SKILL.md`  |
| dev-ts        | TypeScript (latest stable): typing, module/moduleResolution, compiler flags, tsconfig architecture.                              | `.agents/skills/dev-ts/SKILL.md`        |
| dev-vuejs     | Vue (latest stable): SFCs, composables, reactivity, watchers, SSR/hydration, component contracts with strict TypeScript.         | `.agents/skills/dev-vuejs/SKILL.md`     |
| governance    | Unified governance: repo governance, testing/TDD, evidence/ADR/claim governance, shared contracts.                               | `.agents/skills/governance/SKILL.md`    |
| skill-creator | Guide for creating and updating skills that extend agent capabilities with specialized knowledge and workflows.                  | `.agents/skills/skill-creator/SKILL.md` |

## Agents

| Agent   | Description                                                                                     |
| ------- | ----------------------------------------------------------------------------------------------- |
| Explore | Fast read-only codebase exploration and Q&A subagent. Supports quick / medium / thorough modes. |

## Prompts

*No `.prompt.md` files defined yet.*

## Instructions

*No `.instructions.md` files defined yet.*
