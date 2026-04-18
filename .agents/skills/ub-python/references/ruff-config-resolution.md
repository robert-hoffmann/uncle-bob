# Ruff Config Resolution

Use this reference when Ruff config discovery, command resolution, or starter
scaffolding matters.

Do not treat this file as the policy source of truth.
The real Ruff policy lives in the target repository's actual config files and
automation entrypoints.

## Resolution Order

Use these sources in order:

1. `ruff.toml`, `.ruff.toml`, or `[tool.ruff]` in `pyproject.toml`
2. task-runner or package entrypoints such as `Taskfile.yml`, `package.json`,
   `Makefile`, or local docs
3. CI workflows that show the enforced command shape
4. official Ruff docs when local config does not answer the question

## How To Inspect Live Repo Truth

Inspect the target repository directly for:

1. the active Ruff config file location
2. the package or environment manager that owns Python tooling
3. the lint command shape used in local automation
4. whether CI runs Ruff directly or through a wrapper

## Bundled Starter Assets

This skill ships:

- `assets/ruff-template/ruff.toml`
- `scripts/scaffold_ruff.py`

Use them only when a target repository wants this Ruff baseline and does not
already have active Ruff config.

The scaffold is a starter, not a silent policy override.

## Adaptation Points After Scaffolding

After copying the starter into another repository, review at least:

1. `target-version`
2. include and exclude globs
3. first-party package detection
4. any per-file ignores that should be repo-specific
5. the actual lint command used in local automation or CI

## Practical Guidance

1. Inspect real repo config first.
2. If the repo already has Ruff config, obey it rather than replacing it.
3. If the repo lacks Ruff config and the user wants this house style, scaffold
   the starter and explain the remaining local adaptation work.
4. Do not silently install Ruff or rewrite CI; leave those steps explicit.
