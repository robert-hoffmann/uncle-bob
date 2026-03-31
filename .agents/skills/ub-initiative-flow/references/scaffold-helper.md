# Scaffold Helper

Use the helper script when you want deterministic scaffold creation instead of a
manual copy.

## Script

`python .agents/skills/ub-initiative-flow/scripts/scaffold_initiative.py <target-root>`

## What It Does

1. copies `assets/initiative-template/` into the target root
2. renders core placeholders into the copied files
3. leaves optional placeholders untouched when values were not supplied
4. blocks reruns against populated targets to avoid clobbering in-progress work

## Safe Rerun Behavior

The helper is intentionally conservative.

Rules:

1. if the target root does not exist, it is created by copying the template
2. if the target root exists but is empty, the helper can still scaffold it
3. if the target root already contains files, the helper exits with an error
4. use a new target root or move the existing initiative before rerunning

## Recommended Usage

```bash
python .agents/skills/ub-initiative-flow/scripts/scaffold_initiative.py ./tmp/sprints/initiatives/2026-04-01-example-initiative --owner "Platform Team"
```

Optional arguments:

1. `--initiative-name`
2. `--owner`
3. `--phase`
4. `--gate-state`
5. `--roadmap-status`
6. `--validation-commands`
7. `--evidence-pointers`
8. `--current-step`
9. `--next-action`
10. `--dry-run`

## Follow-On Adaptation

After scaffolding:

1. replace the PRD placeholders with real initiative content
2. adapt validation commands to repository truth
3. finalize the roadmap and sprint sequence
4. initialize sprint-specific content before execution begins