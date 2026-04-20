# Initiative Index

This directory is the canonical initiative index for work managed under the
repository operations root.

Start with `operation-guide.md` for the durable workflow SOP, then open the
initiative root you want to work on.

Use each initiative's `roadmap.md` as the small live progress document when
resuming work.

If you want to bootstrap a new initiative quickly, use
`uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>`.

If you want a bounded planning artifact without opening a full initiative, use
`uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create-spec <slug>`.

## Active Initiative Roots

1. `none`

## Current State

1. The operation guide lives here as the canonical SOP for initiative work.
2. The scaffold helper can bootstrap the parent operations root and create new initiative roots or lightweight specs on demand.
3. The scaffold helper uses the skill's internal initiative, lightweight-spec, and sprint templates instead of requiring copied local scaffolding directories.
4. Historical initiative roots live under `../archive/`.

## Active Lightweight Specs

1. `none`

