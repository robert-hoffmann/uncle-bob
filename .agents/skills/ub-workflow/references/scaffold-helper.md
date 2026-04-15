# Scaffold Helper

Use the helper script when you want deterministic initiative operations instead
of a manual copy workflow.

## Commands

1. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>`
2. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints <initiative-root>`
3. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive <initiative-root>`

## What It Does

1. bootstraps `./.ub-workflows/` from the operations-root assets when needed
2. creates dated initiative roots under `./.ub-workflows/initiatives/`
3. copies a provided source PRD into the initiative root as `./prd.md` without rewriting it
4. renders the core placeholders into the initiative control files
5. initializes the full sprint set from roadmap path entries on demand
6. archives completed initiatives on explicit request only
7. synchronizes the initiative-index `README.md` after create and archive actions

## Safe Rerun Behavior

The helper is intentionally conservative.

Rules:

1. if the operations root does not exist, `create` bootstraps it automatically
2. if the initiative root already contains files, `create` exits with an error
3. if a sprint directory already exists but is missing template files, `init-sprints` exits with an error
4. `archive` refuses to move incomplete initiatives
5. use `--dry-run` when you want to inspect the resolved action before writing files

## Recommended Usage

```bash
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source ./tmp/todo/parser-performance-prd.md --owner "Platform Team"
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints ./.ub-workflows/initiatives/2026-04-02-parser-performance
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive ./.ub-workflows/initiatives/2026-04-02-parser-performance
```

Optional arguments:

| Argument                 | Purpose |
| ------------------------ | ------- |
| `create --ops-root`      | Override the default operations root. |
| `create --initiative-name` | Set a display name that differs from the slug. |
| `create --owner`         | Record the initial initiative owner. |
| `create --date`          | Override the date stamp used in generated paths. |
| `create --phase`         | Override the initial initiative phase text. |
| `create --gate-state`    | Override the initial workflow gate state. |
| `create --roadmap-status` | Override the initial roadmap status string. |
| `create --next-action`   | Override the initial next-action value in `README.md`. |
| `create --prd-source`    | Copy the source PRD into the initiative root as `./prd.md`. |
| `create --prd-imported`  | Mark the PRD as already execution-ready after copy/import. |
| `--dry-run`              | Report the resolved action without writing files. |

## Follow-On Adaptation

After scaffolding:

1. replace `./prd.md` with the real initiative PRD when it is not already copied yet
2. review or refine `./prd.md` until `prd_ready: pass`
3. generate the full `roadmap.md` in one pass from the PRD
4. approve the roadmap and record `roadmap_ready: pass` in the initiative `README.md`
5. ensure the roadmap lists every implementation sprint plus the final audit item
6. run `init-sprints` to materialize every numbered sprint directory from the roadmap
7. use `archive` only after the roadmap checklist, retained note, and initiative status are actually complete
