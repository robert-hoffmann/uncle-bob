# Repository Python Workflows

Use this reference to resolve a repository's actual Python runtime, packaging,
and validation truth before recommending commands or tooling.

It should help the agent inspect local reality, not hardcode one repository's
workflow into a distributable skill.

## Runtime and Packaging Baseline

Inspect the target repository for:

1. `requires-python` or equivalent version floors in `pyproject.toml`,
   `.python-version`, runtime manifests, or CI
2. the active environment and dependency manager such as `uv`, `pip`, `poetry`,
   `pdm`, or a plain virtualenv workflow
3. whether the repo is an application, a library, a tooling repo, or a mixed
   workspace
4. the active Ruff config location, if any
5. the actual execution surfaces for scripts, tests, and helper tooling

## Enforced Validation Baseline

Treat the repository's wired checks as the real baseline.
Inspect task runners, package scripts, pre-commit, and CI for the actual
Python-oriented gates.

Common examples:

1. Ruff linting
2. targeted or full test commands
3. direct script execution through the repo's chosen environment tool
4. optional type checking or build validation

## Not Yet Repository-Wired

Recommend extra tools only as explicit gaps when they are not already wired
into the repository.

Typical examples:

1. `mypy`
2. `pyright`
3. `pytest`

When advising users inside any repository:

1. treat the detected Python floor as the shipping constraint even when
   official docs describe newer features
2. recommend missing tools as improvements, not as if they were already part
   of the enforced baseline
3. keep guidance consistent with the repo's actual workload instead of
   assuming a service-backend shape
4. prefer forward-compatible helpers such as `typing_extensions` when they let
   the repo stay on its current floor while reducing future migration work
5. do not recommend backward-compatibility layers or parser-incompatible newer
   syntax as if they were currently shippable in that repository

## Practical Command Patterns

Use the command shape that matches the target repository's tooling.

Recommended resolution order:

1. a repo wrapper such as `task`, `make`, `npm run`, or another documented
   helper entrypoint
2. the repo's environment-aware Python runner such as `uv run python`,
   `poetry run python`, or an activated venv with `python -m ...`
3. direct script or test commands only after confirming they match the local
   interpreter and dependency environment

Shell-entrypoint guidance:

1. prefer interpreter-explicit commands such as `python -m ...`
2. follow the repo's active environment tool instead of assuming `uv`
3. do not assume bare `python` exists on `PATH`

## Starter Scaffolding

This skill now ships a reusable Ruff starter profile and helper:

1. `assets/ruff-template/ruff.toml`
2. `scripts/scaffold_ruff.py`

Use them only when a target repository wants this Ruff baseline and does not
already have active Ruff config. Adapt the copied file to local repo truth
after scaffolding.

## Packaging Guidance

Because many adopting repositories use Python mainly for tooling, scripts, or
automation rather than application packaging:

1. prefer small, direct scripts over unnecessary framework layering when that
   matches repo scope
2. keep script CLIs deterministic and easy to run with the repo's chosen
   environment tool
3. align generated Python with the active Ruff rule set, including security,
   datetime, and modernization rules
