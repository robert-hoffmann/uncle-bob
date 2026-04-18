# Repository Python Workflows

This reference records the Python tooling and validation truth for this
repository.

## Runtime and Packaging Baseline

Current repository truth:

1. `pyproject.toml` declares `requires-python = ">=3.10,<4"`
2. repository dependency management uses `uv`
3. the repository is not packaged as an installable Python library; `tool.uv`
   sets `package = false`
4. Python support in this repository is primarily for helper scripts,
   governance tooling, and workflow tooling
5. active Ruff policy lives in `ruff.toml`

## Enforced Validation Baseline

Current enforced Python-oriented checks:

1. `uv run ruff check .`
2. targeted `uv run python -m unittest ...` for governance and workflow suites
3. direct script execution via `uv run python <script>.py` for integrity and
   workflow helper checks

## Not Yet Repository-Wired

These tools may still be good recommendations in general, but they are not
currently enforced repository gates here:

1. `mypy`
2. `pyright`
3. `pytest`

When advising users inside this repository:

1. treat Ruff and targeted `unittest` runs as the actual baseline
2. recommend mypy or pytest only as a tooling-gap suggestion, not as existing
   repository truth
3. keep Python guidance consistent with helper-script and repository-tooling use
   rather than service-backend assumptions
4. treat the detected repo Python floor as the shipping constraint even when
   official docs describe newer features
5. prefer forward-compatible helpers such as `typing_extensions` when they let
   the repo stay on its current floor while reducing future migration work
6. do not recommend backward-compatibility layers or parser-incompatible newer
   syntax as if they were currently shippable in this repository

## Practical Command Patterns

Use these command shapes by default in this repository:

1. `uv run ruff check <scope>`
2. `uv run python -m unittest discover -s <suite-dir> -p 'test_*.py' -v`
3. `uv run python <script-path>`
4. `task check` when a full repository validation pass is needed

## Starter Scaffolding

This skill now ships a reusable Ruff starter profile and helper:

1. `assets/ruff-template/ruff.toml`
2. `scripts/scaffold_ruff.py`

Use them only when a target repository wants this Ruff baseline and does not
already have active Ruff config. Adapt the copied file to local repo truth
after scaffolding.

## Packaging Guidance

Because this repository ships Copilot skills and tooling rather than a Python
application package:

1. prefer small, direct scripts over unnecessary framework layering
2. keep script CLIs deterministic and easy to run with `uv run python`
3. align generated Python with Ruff's configured rule set, including security,
   datetime, and modernization rules
