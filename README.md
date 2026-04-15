# Uncle Bob

<table>
<tr>
<td width="300">
<img src="docs/assets/uncle-bob.png" alt="Uncle Bob" width="280" />
</td>
<td>

Uncle Bob is a practical collection of skills and custom agents for GitHub Copilot in VS Code. It gives Copilot stronger defaults for code quality, framework work, governance, and planning without forcing a large setup or a new workflow.

I use these skills in an actual corporate production environment for supply-chain management in the aerospace industry.

</td>
</tr>
</table>

## What This Is

This repository packages reusable Copilot skills, agent definitions, and supporting project metadata. You can bring them into another repository to give Copilot better instructions for TypeScript, Python, Vue, Nuxt, Tailwind, CSS, governance, and multi-step delivery work.

## Why Use It

Use it when you want GitHub Copilot in VS Code to be more consistent, more opinionated, and more useful on real project work. The repo combines a mandatory quality baseline with targeted skills and focused agents, so Copilot can help with implementation, review, teaching, customization, and workflow orchestration from the same set of conventions.

## What's Included

| Skill             | Description                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| ub-quality        | Mandatory baseline for code quality, formatting, documentation, and refactoring.                 |
| ub-css            | CSS and Vue/Nuxt styling with design tokens, cascade layers, and progressive enhancement.        |
| ub-nuxt           | Nuxt patterns for typed composables, rendering modes, runtime config, and server routes.         |
| ub-python         | Typed Python patterns, boundary validation, and structured error handling.                       |
| ub-tailwind       | Tailwind setup, migration, and debugging across HTML, Vue, and Nuxt.                             |
| ub-ts             | TypeScript typing, module resolution, compiler flags, and tsconfig structure.                    |
| ub-vuejs          | Vue SFCs, composables, reactivity, SSR and hydration, and strict TypeScript contracts.           |
| ub-governance     | Repository, testing, and evidence governance with shared contracts.                              |
| ub-customizations | Builder skill for Copilot skills, agents, prompts, instructions, hooks, MCP, and plugin bundles. |
| ub-workflow       | Initiative planning, roadmaps, resumable sprints, and final audit flow.                          |

| Agent             | Description                                                         |
| ----------------- | ------------------------------------------------------------------- |
| Explore           | Fast read-only codebase exploration and Q&A.                        |
| ub-governance     | Interactive guide for repository, testing, and evidence governance. |
| ub-teacher        | Beginner-friendly explanations and code walkthroughs.               |
| ub-customizations | Interactive builder for Copilot customization artifacts.            |
| ub-workflow       | Interactive planning and sprint orchestration for larger work.      |

## Quick Start

```bash
git clone https://github.com/robert-hoffmann/uncle-bob.git
```

In the target project, either copy or symlink these paths from the clone:

- `.agents/`
- `.github/agents/`
- `AGENTS.MD`

Symlink:

```bash
mkdir -p .github
ln -s /path/to/uncle-bob/.agents .agents
ln -s /path/to/uncle-bob/.github/agents .github/agents
ln -s /path/to/uncle-bob/AGENTS.MD AGENTS.MD
```

Copy:

```bash
mkdir -p .github
cp -r /path/to/uncle-bob/.agents .agents
cp -r /path/to/uncle-bob/.github/agents .github/agents
cp /path/to/uncle-bob/AGENTS.MD AGENTS.MD
```

Open the target project in VS Code with GitHub Copilot enabled. Copilot will discover `AGENTS.MD` and `.github/agents` automatically.

Update with:

```bash
git -C /path/to/uncle-bob pull
```

If you copied files, copy them again after pulling. If you symlinked them, the update is already in place.

## Repository Layout

| Path                 | Purpose                                        |
| -------------------- | ---------------------------------------------- |
| `.agents/skills/`    | Skill definitions and supporting assets.       |
| `.github/agents/`    | Custom agent definitions.                      |
| `.github/plugin/`    | Plugin-related assets.                         |
| `.github/workflows/` | GitHub workflow automation.                    |
| `docs/`              | Documentation and images.                      |
| `tmp/`               | Temporary workspace content and test material. |
| `AGENTS.MD`          | Root registry and repository instructions.     |
| `plugin.json`        | Plugin metadata.                               |
| `Taskfile.yml`       | Common local lint and test commands.           |

## Philosophy

Keep Copilot practical. Start with strong quality defaults, add focused domain knowledge only where it helps, and prefer reusable instructions over one-off prompting. The goal is to make Copilot more dependable for day-to-day engineering work, not just better at generating snippets.

## License

MIT. See [LICENSE](LICENSE).
