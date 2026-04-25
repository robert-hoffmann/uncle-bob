# UB Python

Source: `.agents/skills/ub-python/SKILL.md`

`ub-python` guides Python implementation, tests, typing, packaging, validation,
and repository logic. It favors modern Python patterns while still
implementing against the target project's real supported runtime and tooling.
It treats repository truth as the shipping boundary for every recommendation.

## Core Principles

- Detect repository Python truth before choosing commands, syntax, runtime
  assumptions, or validation gates.
- Write modern Python against the project floor: current syntax where allowed,
  forward-compatible helpers where useful, and no unreleased features.
- Type public interfaces and meaningful internal boundaries; keep `Any`
  contained, justified, and away from public contracts.
- Use precise interface types, protocols, type aliases, `Self`, `override`,
  type guards, and exhaustive checks when they improve correctness.
- Validate boundary data with Pydantic v2 or explicit manual validation, then
  keep domain logic typed and simpler behind that boundary.
- Use dataclasses for internal domain containers where they fit, with safe
  defaults such as keyword-only initialization and factories for mutable
  values.
- Preserve structured error chains, grouped failures, and explicit
  cancellation or timeout behavior for concurrent or external I/O.
- Prefer behavior-focused tests and run the checks the project actually wires.
- Modernize incrementally instead of adding broad compatibility layers or
  retaining legacy Python patterns by habit.

## Behavior In Practice

- Starts by reading `pyproject.toml`, lockfiles, `.python-version`, CI, task
  wrappers, and repo instructions before saying which Python command or syntax
  is safe.
- Compares repo truth with official Python and tool guidance. If they disagree
  materially, it implements the repo-safe path and reports the migration path
  instead of pretending there is no conflict.
- Moves untrusted data parsing to boundaries: HTTP payloads, files, env vars,
  queues, CLI input, and external API responses get validated before domain
  logic relies on them.
- Chooses data modeling deliberately: dataclasses for internal domain state;
  Pydantic v2 models for boundary validation, serialization, and schema-shaped
  data.
- Uses modern typing as a design tool, not decoration: `collections.abc`
  interfaces, `Protocol`, narrow return types, discriminating helpers, and
  `assert_never` make refactors safer.
- Keeps error handling observable and causal with specific exceptions,
  `raise ... from err`, useful log context, `TaskGroup`, `ExceptionGroup`, and
  `except*` when the concurrency model calls for them.
- Treats Ruff, mypy or pyright, pytest, pre-commit, and CI as detected repo
  truth. Missing lint, type, or test wiring is reported as a tooling gap, not
  silently ignored.
- Avoids new legacy output: no fresh `Optional`/`Union`/`List`/`Dict` aliases
  unless compatibility requires them, no Pydantic v1 validators for new code,
  no new `python setup.py ...` workflows, and no custom typing shims when
  `typing_extensions` or the standard library already covers the path.

## Reference Highlights

- `.agents/skills/ub-python/references/python-standards.md`: encodes the
  modern Python baseline: interpreter-explicit commands, `pathlib`, modern
  generics, `X | Y`, `collections.abc`, `Protocol`, `typing_extensions`,
  dataclass versus Pydantic choices, structured errors, async guidance,
  `pyproject.toml`, dependency restraint, and legacy-avoidance rules.
- `.agents/skills/ub-python/references/repository-python-workflows.md`: how to
  discover the target repository's actual Python workflow, active test
  commands, configured type checkers, lint policy, packaging entrypoints, and
  CI truth before presenting any command as required.
- `.agents/skills/ub-python/references/ruff-config-resolution.md`: Ruff config
  discovery order, what counts as real Ruff policy, when the bundled starter
  can be scaffolded, and which settings remain repo-local decisions.
- `.agents/skills/ub-python/references/task-bundle.md`: optional Task-based
  automation overlay for repositories that want repeatable lint, format,
  typecheck, and test entrypoints without pretending Task is universal.
- `.agents/skills/ub-python/assets/ruff-template/ruff.toml`: starter Ruff
  profile used only when a repository explicitly wants the house baseline and
  lacks an active local config.

## Progressive Disclosure

The main skill sets the Python posture. Deeper references load when the task
needs specifics: Python standards for implementation, workflow discovery for
repo validation, Ruff resolution for lint setup, and the task bundle only when
the target repository wants optional automation.

## Common Invocation Examples

- “Use `ub-python` to add tests for this behavior.”
- “Review this script for typing and boundary validation.”
- “Update this Python helper without changing its public contract.”
- “Scaffold the Ruff baseline for a repo that has no lint config yet.”

## Boundaries

Do not use it as a general documentation or workflow-planning skill. Pair it
with `ub-workflow` when the Python change itself needs planning artifacts.

## Tradeoffs

Strength: makes Python changes safer by aligning modern language practice with
the repository's actual validation surface.

Cost: strict boundary work can reveal follow-up modernization outside the
initial task, especially in older or weakly typed projects.
