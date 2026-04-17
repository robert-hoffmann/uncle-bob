# Sprint 05 Evidence

## Inventory Alignment Result

Verified on-disk custom agents under `./.github/agents/`:

1. `ub-customizations.agent.md`
2. `ub-governance.agent.md`
3. `ub-teacher.agent.md`
4. `ub-workflow.agent.md`

Published repository inventory now matches that disk truth:

1. `README.md` lists 4 custom agents and no longer publishes `Explore` as a
   repository agent.
2. `AGENTS.md` lists the same 4 custom agents and no longer publishes
   `Explore` as a repository agent.
3. `.github/plugin/marketplace.json` now describes `4 custom agents` instead
   of `5 agents` and no longer counts `explore` as a repository agent.

Built-in subagent references were preserved where they remain legitimate local
implementation details:

1. `agents: ["Explore"]` in local `.agent.md` files
2. explanatory text that delegates read-only exploration to the built-in
   `Explore` subagent

## Root Registry Filename Result

The root registry file is now `./AGENTS.md` on disk.

The rename required a case-only filesystem-safe transition through a temporary
filename so the repository would no longer preserve the legacy `AGENTS.MD`
entry on the default macOS filesystem.

Updated public references now point to `AGENTS.md`:

1. quick-start copy and symlink commands in `README.md`
2. repository layout text in `README.md`
3. centralized version-policy references in the touched skill files

## Version Reconciliation Result

The chosen repository version baseline is now `1.0.0` across the tracked
metadata surfaces:

1. `pyproject.toml`: `1.0.0`
2. `plugin.json`: `1.0.0`
3. `.github/plugin/marketplace.json`: `1.0.0`

`uv lock` was rerun so `uv.lock` now records the same project version.

## Temporary Exception Result

No temporary exception was needed.

`Explore` remains valid only as a built-in subagent reference inside local
agent definitions, not as a published repository custom agent.
