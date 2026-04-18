# Initiative Index

This directory is the canonical initiative index for work managed under the
repository operations root.

Start with `operation-guide.md` for the formal SOP and `user-guide.md` for the
human workflow, then open the initiative root you want to work on.

Use each initiative's `roadmap.md` as the small live progress document when
resuming work.

If you want to bootstrap a new initiative quickly, use
`python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>`.

If you want a bounded planning artifact without opening a full initiative, use
`python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create-spec <slug>`.

## Active Initiative Roots

REPLACE_ACTIVE_INITIATIVE_ROOTS

## Active Lightweight Specs

REPLACE_ACTIVE_LIGHTWEIGHT_SPECS

## Current State

1. The operation guide lives here as the canonical SOP for initiative work.
2. The human-facing workflow guide lives here as `user-guide.md`.
3. The scaffold helper can bootstrap the parent operations root and create new initiative roots or lightweight specs on demand.
4. The scaffold helper uses the skill's internal initiative, lightweight-spec, and sprint templates instead of requiring copied local scaffolding directories.
5. Historical initiative roots live under `../archive/`.
