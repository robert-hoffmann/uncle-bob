# itech-agents

A curated collection of GitHub Copilot skills, agents, prompts, and governance workflows for consistent, high-quality AI-assisted development.

## Repository Structure

```
.agents/
  skills/              # Copilot skills (SKILL.md per skill)
.github/
  agents/              # Custom agent definitions (.agent.md)
  prompts/             # Reusable prompt files (.prompt.md)
  plugin/              # Copilot agent plugin manifests
  workflows/           # GitHub Actions CI/CD workflows
.vscode/               # Workspace settings, MCP config, extensions
AGENTS.MD              # Skill & agent registry (auto-loaded by Copilot)
TODO.md                # Roadmap & open items
ruff.toml              # Python linter config
```

## Skills

Skills are domain-specific instruction sets that Copilot loads on demand.

| Skill | Description |
|-------|-------------|
| **code-quality** *(mandatory)* | Cross-language code quality: design patterns, formatting, documentation, structure, refactoring. |
| dev-css | Plain CSS & Vue/Nuxt style blocks with design tokens, cascade layers, and progressive enhancement. |
| dev-nuxt | Nuxt 4: typed composables, SSR/SSG/hybrid rendering, Nitro/server routes, app-directory semantics. |
| dev-python | Python 3.12.x: typed patterns, boundary validation, structured error handling, pytest/ruff/mypy. |
| dev-tailwind | Tailwind CSS v4: setup, migration, and debugging across HTML, Vue + Vite, and Nuxt projects. |
| dev-ts | TypeScript 5.9.3: typing, module resolution, compiler flags, tsconfig architecture. |
| dev-vuejs | Vue 3.5.x: SFCs, composables, reactivity, SSR/hydration, component contracts with strict TypeScript. |
| governance | Unified governance: repo gates, testing/TDD, evidence/ADR/claim governance, shared contracts. |
| skill-creator | Guide for creating and updating skills that extend agent capabilities. |

## Agents

| Agent | Location | Description |
|-------|----------|-------------|
| Explore | Built-in subagent | Fast read-only codebase exploration and Q&A (quick / medium / thorough). |
| governance-help | `.github/agents/governance-help.agent.md` | Governance assistance agent. |
| teacher | `.github/agents/teacher.agent.md` | Teaching / explanation agent. |

## Prompts

| Prompt | Location |
|--------|----------|
| governance-help | `.github/prompts/governance-help.prompt.md` |

## CI / Workflows

| Workflow | Purpose |
|----------|---------|
| lint | Linting gates |
| deploy | Deployment pipeline |
| release-please | Automated release management |
| decision-governance | Governance decision checks |
| governance-skill-integrity | Skill integrity validation |

## Getting Started

1. Clone the repository into your workspace (or add it as a submodule / symlink `.agents/` into another project).
2. Open the workspace in VS Code with [GitHub Copilot](https://github.com/features/copilot) enabled.
3. Skills, agents, and prompts are auto-discovered from `AGENTS.MD` and the `.github/` directories.

## Linting & Tooling

- **Python** — [Ruff](https://docs.astral.sh/ruff/) configured via `ruff.toml`.
- **Markdown** — markdownlint configured via `.markdownlint.jsonc`.
- **YAML** — yamllint configured via `.yamllint.yaml`.
- **Editor** — shared settings in `.editorconfig`.

## License

Private repository — all rights reserved.
