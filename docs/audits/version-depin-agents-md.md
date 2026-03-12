# Version De-Pinning — AGENTS.MD

## Changes

### 1. Add Version & Tooling Policy Section

New section after Mandatory Skills, before Skills table:

| Technology   | Version Policy      | Primary Tool     | Fallback |
| ------------ | ------------------- | ---------------- | -------- |
| Node.js      | Latest LTS          | bun              | npm/node |
| Python       | Latest stable       | uv               | pip      |
| TypeScript   | Latest stable       | (via bun or npm) | —        |
| Vue          | Latest stable       | —                | —        |
| Nuxt         | Latest stable       | —                | —        |
| Tailwind CSS | Latest stable       | —                | —        |
| Pydantic     | Latest stable (v2+) | —                | —        |

Policy note: Skills MUST NOT hardcode version numbers. Detect actual project versions from package.json, lockfiles, pyproject.toml. Use web search to verify latest patterns. When project version differs from latest, note the gap and recommend upgrade path.

### 2. Update Skill Description Table

| Skill         | Old Description                   | New Description                                                                                                                  |
| ------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| dev-vuejs     | Vue 3.5.x: SFCs, composables...   | Vue (latest stable): SFCs, composables, reactivity, watchers, SSR/hydration, component contracts with strict TypeScript.         |
| dev-nuxt      | Nuxt 4 apps: typed composables... | Nuxt (latest stable): typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, app-directory semantics. |
| dev-ts        | TypeScript 5.9.3: typing...       | TypeScript (latest stable): typing, module/moduleResolution, compiler flags, tsconfig architecture.                              |
| dev-tailwind  | Tailwind CSS v4: setup...         | Tailwind CSS (latest stable): setup, migration, debugging across standalone HTML, Vue + Vite, and Nuxt projects.                 |
| dev-python    | Python 3.12.x: typed patterns...  | Python (latest stable): typed patterns, boundary validation, structured error handling, pytest/ruff/mypy workflows.              |
| dev-css       | (no version)                      | (unchanged)                                                                                                                      |
| governance    | (no version)                      | (unchanged)                                                                                                                      |
| code-quality  | (no version)                      | (unchanged)                                                                                                                      |
| skill-creator | (no version)                      | (unchanged)                                                                                                                      |
