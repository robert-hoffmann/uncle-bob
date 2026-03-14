# Uncle Bob — Copilot Skills & Agents

<table>
<tr>
<td width="300">
<img src="docs/assets/uncle-bob.png" alt="Uncle Bob" width="280" />
</td>
<td>

A curated, production-grade collection of GitHub Copilot skills and custom agents, built by a developer with 27 years of full-stack experience. Every skill was co-written with AI using OpenAI GPT-5.4 Pro (extended thinking & research) to deliver the highest quality instructions possible.

Drop them into any project and your Copilot immediately gets smarter about the technologies you use.

</td>
</tr>
</table>

## What This Is

Uncle Bob is a framework of reusable **skills** and **agents** for [GitHub Copilot](https://github.com/features/copilot) in VS Code. Skills give Copilot deep, domain-specific knowledge it can draw on while assisting you — covering everything from code quality and TypeScript to Nuxt, Tailwind, governance, and more. Agents provide interactive, task-focused workflows on top of those skills.

## Skills

| Skill | Description |
| ----- | ----------- |
| **ub-quality** *(mandatory)* | Cross-language code quality: design patterns, formatting, documentation, structure, refactoring. |
| ub-css | Plain CSS and Vue/Nuxt style blocks with design tokens, cascade layers, and progressive enhancement. |
| ub-nuxt | Nuxt (latest stable): typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, app-directory semantics. |
| ub-python | Python (latest stable): typed patterns, boundary validation, structured error handling, pytest/ruff/mypy. |
| ub-tailwind | Tailwind CSS (latest stable): setup, migration, and debugging across HTML, Vue + Vite, and Nuxt projects. |
| ub-ts | TypeScript (latest stable): typing, module resolution, compiler flags, tsconfig architecture. |
| ub-vuejs | Vue (latest stable): SFCs, composables, reactivity, SSR/hydration, component contracts with strict TypeScript. |
| ub-governance | Unified governance: repo gates, testing/TDD, evidence/ADR/claim governance, shared contracts. |
| ub-customizations | VS Code Copilot customization builder for skills, agents, prompts, hooks, MCP configs, and bundles. |

## Agents

| Agent | Description |
| ----- | ----------- |
| Explore | Fast read-only codebase exploration and Q&A (quick / medium / thorough). |
| ub-governance | Governance assistance agent grounded in the ub-governance skill. |
| ub-teacher | Teaching and explanation agent for readable, beginner-friendly walkthroughs. |
| ub-customizations | Interactive Copilot customization builder with classify/generate/validate/iterate workflow. |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/robert-hoffmann/uncle-bob.git
```

### 2. Add skills and agents to your project

You have two options — **copy** or **symlink**. Symlinking is recommended so you always get the latest version by pulling the repo.

#### Option A — Symlink (recommended)

From your project root, create symlinks pointing into the cloned repository:

```bash
# Symlink the skills directory
ln -s /path/to/uncle-bob/.agents .agents

# Symlink the agent definitions
ln -s /path/to/uncle-bob/.github/agents .github/agents

# Symlink the root registry file
ln -s /path/to/uncle-bob/AGENTS.MD AGENTS.MD
```

To update, simply pull the latest changes:

```bash
cd /path/to/uncle-bob && git pull
```

#### Option B — Copy

Copy the directories directly into your project:

```bash
cp -r /path/to/uncle-bob/.agents .agents
cp -r /path/to/uncle-bob/.github/agents .github/agents
cp /path/to/uncle-bob/AGENTS.MD AGENTS.MD
```

> With this approach you will need to re-copy files after upstream updates.

### 3. Open your project in VS Code

Make sure [GitHub Copilot](https://github.com/features/copilot) is installed and enabled. Skills, agents, and prompts are auto-discovered from `AGENTS.MD` and the `.github/` directory — no additional configuration required.

## Repository Layout

```text
.agents/skills/        # Copilot skills (one SKILL.md per skill)
.github/agents/        # Custom agent definitions (.agent.md)
AGENTS.MD              # Skill & agent registry (auto-loaded by Copilot)
```

## License

This project is licensed under the [MIT License](LICENSE).
