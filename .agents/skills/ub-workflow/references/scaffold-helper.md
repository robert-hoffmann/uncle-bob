# Scaffold Helper

Use the helper script when you want deterministic initiative operations instead
of a manual copy workflow.

## Commands

1. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>`
2. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py prepare-sprints <initiative-root>`
3. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints <initiative-root>`
4. `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive <initiative-root>`
5. `python .agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py <initiative-root-or-scan-root>`

## What It Does

1. bootstraps `./.ub-workflows/` from the operations-root assets when needed
2. creates dated initiative roots under `./.ub-workflows/initiatives/`
3. copies a provided source PRD into the initiative root as `./prd.md` without rewriting it
4. renders the core placeholders into the initiative control files
5. prepares sprint PRDs from roadmap metadata when explicit sprint-pack preparation is requested
6. initializes the full sprint set from roadmap path entries on demand
7. archives completed initiatives on explicit request only
8. synchronizes the initiative-index `README.md` after create and archive actions

The current helper does not, by itself, guarantee execution-ready sprint PRDs.
Sprint content preparation remains a separate workflow step that must be
completed before Sprint 01 or any later sprint begins.

When `prepare-sprints` is used, the helper renders roadmap-derived sprint PRDs
and leaves only named pending handoff markers where prior closeout truth may
still need to flow forward.

The helper now also prints generated-output placeholder summaries after
`create`, `prepare-sprints`, and `init-sprints`.

Use `--strict-placeholders` on `create`, `prepare-sprints`, or `init-sprints`
when required unresolved generated-output placeholders should fail the command.

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
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py prepare-sprints ./.ub-workflows/initiatives/2026-04-02-parser-performance
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints ./.ub-workflows/initiatives/2026-04-02-parser-performance
python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive ./.ub-workflows/initiatives/2026-04-02-parser-performance
```

Optional arguments:

- `create --ops-root`: override the default operations root
- `create --initiative-name`: set a display name that differs from the slug
- `create --owner`: record the initial initiative owner
- `create --date`: override the date stamp used in generated paths
- `create --phase`: override the initial initiative phase text
- `create --gate-state`: override the initial workflow gate state
- `create --roadmap-status`: override the initial roadmap status string
- `create --next-action`: override the initial next-action value in
  `README.md`
- `create --prd-source`: copy the source PRD into the initiative root as
  `./prd.md`
- `create --prd-imported`: mark the PRD as already execution-ready after
  copy/import
- `create --strict-placeholders`: fail if generated output still has required
  unresolved placeholders after scaffold creation
- `prepare-sprints --strict-placeholders`: fail if required generated-output
  placeholders remain after sprint preparation
- `init-sprints --strict-placeholders`: fail if required generated-output
  placeholders remain after sprint initialization
- `--dry-run`: report the resolved action without writing files

Placeholder validation:

1. default scope is generated initiative output, not canonical internal
   templates
2. `check_scaffold_placeholders.py --strict` fails only on required findings
3. `PENDING_HANDOFF:` markers and generated closeout prompts remain advisory
4. see `references/placeholder-contract.md` for the exact required-versus-advisory rules

## Follow-On Adaptation

After scaffolding:

1. replace `./prd.md` with the real initiative PRD when it is not already copied yet
2. review or refine `./prd.md` until `prd_ready: pass`
3. generate the full `roadmap.md` in one pass from the PRD
4. approve the roadmap and record `roadmap_ready: pass` in the initiative `README.md`
5. ensure the roadmap lists every implementation sprint plus the final audit item
6. run `prepare-sprints` to render roadmap-derived sprint PRDs before any sprint begins
7. run `init-sprints` when you need directory-only materialization or validation of the sprint set
8. use `archive` only after the roadmap checklist, retained note, and initiative status are actually complete
