# Python Task Bundle

Use this reference only when the target repository wants an optional Task-based
automation overlay for the `ub-python` Ruff starter profile.

This is an adoption bundle, not part of the core Ruff scaffold contract.

## Purpose

The bundle gives the host repository a small Task wrapper for the Ruff baseline
that `ub-python` already scaffolds with `ruff.toml`.

It is meant for repositories that want Task-based local automation without
making Task part of the core Python skill contract.

## When To Use

Use this bundle when:

1. the target repository wants a Task wrapper for Ruff
2. the repository does not already expose equivalent Ruff automation
3. the team wants a small starting point they can adapt locally

## When Not To Use

Do not use this bundle when:

1. the repository already has adequate Python lint automation
2. the repository does not use Task and does not want to adopt it
3. the repository already has a root `Taskfile.yml` and overlapping task names
   would create confusion without a reconciliation plan

## Files Shipped

This bundle ships:

1. `assets/task-bundle/ub-python.Taskfile.yml`

The file is source material for adoption, not a live runtime dependency.

## Reconciliation Rules

Before recommending or adopting this bundle, inspect:

1. whether `Taskfile.yml` already exists
2. whether package scripts or CI already expose Ruff
3. whether the host repo wants repo-wide or narrow-file lint commands
4. whether `lint-py` and `lint-py-files` fit local naming cleanly

Decision rule:

1. if equivalent automation already exists, prefer reusing host-repo truth
2. if Ruff automation is absent or weak, this bundle may be adapted

## Adoption Guidance

Default fallback:

```bash
ruff check .
```

Task bundle task surface:

1. `lint-py`
2. `lint-py-files`

Recommended usage:

1. copy or adapt the bundle task definitions into the host repository's own
   automation surface
2. keep or rename the tasks so they match host-repo conventions
3. adjust command scope if the host repo needs narrower or broader default
   targets

Do not treat the installed skill asset path itself as the portable runtime
contract, especially under `skills.sh`.

## Pros / Cons

Using the bundle:

Pros:

1. faster Ruff adoption for repos that want Task
2. very small and easy to adapt
3. stays optional and decoupled from the core skill

Cons:

1. does not solve test or typecheck automation
2. still needs local reconciliation
3. redundant in repos that already have Ruff wrappers
