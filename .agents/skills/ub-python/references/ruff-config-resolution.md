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

## Repo Truth In This Repository

Current repository truth:

1. active Ruff config is in `ruff.toml`
2. Python packaging and dev dependencies live in `pyproject.toml`
3. common local validation uses `uv run ruff check .`
4. CI also runs Ruff directly

Useful inspection commands:

```bash
sed -n '1,240p' ruff.toml
sed -n '1,220p' pyproject.toml
rg -n "ruff" Taskfile.yml .github/workflows
```

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
