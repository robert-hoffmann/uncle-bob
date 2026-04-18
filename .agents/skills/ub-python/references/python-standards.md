# Python Standards (Project-Specific, Non-Formatting, Latest Stable)

> Verify these standards against the latest official Python documentation via web search.

This reference codifies Python standards for this repository and is aligned to
official Python and tooling guidance.

## 1. Platform and Environment

- Runtime baseline: latest stable Python (detect from project files and verify via web search).
- Use a project-local virtual environment and interpreter-explicit commands.
- Prefer `python -m ...` or `uv run ...` for command consistency.
- Prefer `pathlib.Path` for filesystem paths, and keep Windows portability in mind.

## 2. Implementation Strategy

- Enforce strong static typing with clean runtime behavior.
- Prefer modern language/stdlib patterns over legacy idioms.
- Implement against the project's currently supported Python version, but bias design toward the next stable upgrade path instead of preserving older-version behavior by default.
- Use streaming/generator-based processing for large datasets.
- Treat readability and maintainability as hard constraints.
- For non-trivial work, explicitly compare at least two approaches with pros/cons.

## 2A. Source Truth And Disclosure

- Treat repo truth as the shipping constraint: detect the active Python floor,
  runtime, and tooling before recommending implementation details.
- Treat official Python docs and official tool docs as the preferred guidance
  baseline for forward-looking design and migration-ready patterns.
- If official docs, repo truth, or live code reality materially disagree on a
  non-trivial recommendation, surface `OFFICIAL_CONFLICT`, implement the
  repo-safe path, and explain the forward migration path.
- If a non-trivial claim cannot be confirmed in official sources after targeted
  research, mark it `UNVERIFIED` or avoid presenting it as settled guidance.
- Keep these disclosures scoped to non-trivial, version-sensitive, or contested
  guidance rather than every trivial edit.

## 3. Typing Rules (Modern Python Defaults)

- Annotate non-trivial function parameters and return types.
- Use modern syntax: `list[str]`, `dict[str, int]`, `X | Y`.
- Prefer `collections.abc` interface types (`Iterable`, `Sequence`, `Mapping`, `Callable`) and `abc` or `Protocol` contracts when mutation or a concrete container type is not required.
- Prefer `typing_extensions` for newer typing features and backports when the project's supported version floor needs them or when the backport gives cleaner cross-version semantics and future-upgrade safety.
- Prefer modern typing tools where useful:
  - `type Alias = ...` and PEP 695 type parameter syntax in new code only when
    the project's active Python floor supports that syntax directly.
  - `override` for explicit override intent.
  - `Self`, `Protocol`, `TypeGuard`, `TypeIs`, `Required`, `NotRequired`, `ReadOnly`, and `assert_never` for correctness and safe refactors.
- Do not build custom typing compatibility shims when `typing_extensions` already provides the forward-compatible path.
- Keep `Any` out of public APIs unless unavoidable; if used, document why.
- Legacy typing aliases (`Optional`, `Union`, `List`, `Dict`) are migration-only, not new-code defaults.
- Prefer forward-compatible helpers and backports where they preserve the
  current repo floor while reducing future migration work, but do not emit
  syntax that the active runtime cannot parse.

## 4. Data Modeling and Boundary Validation

Choose a model explicitly by layer:

- External input (HTTP/files/env/queues): Pydantic v2 models or explicit manual validation.
- Internal domain containers: dataclasses.
- Configuration/state: validated model (`pydantic-settings` or validated dataclass).

### Option A: Dataclass-focused internals

Pros:

- Lightweight and fast.
- Minimal dependency overhead.
- Clear internal domain containers.

Cons:

- No automatic runtime validation.
- Serialization/parsing requires explicit code.

Defaults:

- `@dataclass(slots=True, kw_only=True)`
- `frozen=True` for value objects where immutability helps
- `field(default_factory=...)` for mutable defaults

### Option B: Pydantic v2-focused boundaries

Pros:

- Strong runtime validation and error messaging.
- Clean parsing/serialization for external data.
- Better contract enforcement at trust boundaries.

Cons:

- Additional dependency surface.
- More runtime overhead than plain dataclasses.

Use v2 APIs only:

- `ConfigDict(...)`
- `@field_validator` and `@model_validator`
- `model_dump()` / `model_dump_json()`
- `TypeAdapter` for non-model validations

## 5. Modern Python Features to Prefer

- `match`/`case` when it is clearer than chained conditionals.
- `asyncio.TaskGroup` for structured concurrency.
- `ExceptionGroup` and `except*` when concurrent tasks fail in groups.
- `pathlib.Path.walk()` instead of `os.walk()` for path-native traversal.
- `itertools.batched()` for standard chunking logic.
- `datetime.UTC` for explicit timezone-aware UTC usage.
- `str.removeprefix()` / `str.removesuffix()` for explicit string normalization.

Notes:

- f-string behavior improvements (PEP 701) should be used; keep f-strings readable.
- Comprehension inlining (PEP 709) is available, but readability still takes priority.

## 6. Concurrency Guidelines

- Use async only where it improves the I/O model; do not use async by default.
- For CPU-bound tasks, prefer process-based parallelism.
- For concurrent I/O, use `TaskGroup` (async) or threads where simpler.
- On Windows, guard multiprocessing entrypoints with `if __name__ == "__main__":`.

## 7. Imports and Dependency Hygiene

- Group imports as stdlib -> third-party -> local.
- If Ruff is configured, treat its active rules as the import/lint baseline, including import grouping and ordering.
- Remove unused imports quickly.
- Prefer stdlib-first solutions before adding dependencies.
- Add dependencies only when they provide clear correctness/DX/maintenance value.

## 8. Packaging and Toolchain Policy

### Packaging Baseline

- Use `pyproject.toml` as the source of truth for metadata and tool config.
- Include `[build-system]` explicitly to avoid ambiguous builds.
- Keep `requires-python` aligned with project runtime policy (detect from existing configuration).
- Avoid deprecated `python setup.py ...` command execution; use modern build/install commands.
- Nuance: `setup.py` may still exist in some projects, but CLI invocation is no longer the recommended workflow.

### Tooling Stance (Primary + Fallback)

Primary stack:

- Dependency/environment: `uv`
- Lint + format: `ruff`
- Type check: `mypy`
- Tests: `pytest`
- Hooks: `pre-commit`

Fallback options when constraints require them:

- Dependency locking: `pip-tools`
- Type checking: `pyright` or `basedpyright`
- Editor diagnostics: Pylance with `python.analysis.typeCheckingMode = "standard"` for local feedback loops

Operational guidance:

- Prefer one-command workflows for local + CI (`lint`, `format`, `typecheck`, `test`).
- For Ruff, set `target-version` and keep it aligned with `project.requires-python`.
- Treat actual Ruff config files as the policy source of truth when they exist;
  use starter scaffolds only when a repo wants this house style and does not
  already have active Ruff config.
- Keep repository-shared VS Code settings minimal and policy-oriented. Put personal UX preferences (hover summaries, inlay hint style, diagnostics language, UI ergonomics) in user settings.
- If a `pyrightconfig.json` or `[tool.pyright]` exists, treat it as source of truth because it overrides some Pylance analysis settings.
- After generating or modifying Python code, run the configured checks that apply to the touched scope instead of assuming code generation is sufficient.
- Minimum expectation: Ruff when configured, a configured type checker when present, and targeted pytest coverage when tests exist or behavior changed.
- Start with changed files or targeted tests, then widen only when failures indicate broader impact.
- If configured tooling cannot be run, report the exact blocker.
- If linting, type checking, or testing is missing or not wired into routine workflows, warn the user and recommend concrete additions rather than silently accepting the gap.

## 9. Function and API Design

- Keep functions focused, composable, and testable.
- Use narrow signatures with meaningful return types.
- Validate boundary data near entry points, not deep in domain logic.
- Add concise docstrings for non-trivial behavior (intent, params, returns, errors, example).

## 10. Architecture and Boundaries

- Preserve layered flow: presentation -> service -> repository -> data.
- Keep domain language consistent between implementation and tests.
- Avoid leaking storage/transport details into domain logic.
- Prefer composition over inheritance when both are viable.

## 11. Error Handling and Observability

- Use specific exception types.
- Preserve root cause (`raise NewError(...) from err`).
- Log decisions and failures with actionable context.
- Use structured logging/context where available.
- Use log levels intentionally (`debug`, `info`, `warning`, `error`).

## 12. Testing and Refactoring Practice

- Follow TDD when practical: tests first for behavior changes.
- Keep fast unit tests for logic and integration tests for boundaries.
- Refactor in small, behavior-preserving steps.
- Use guard clauses to reduce nesting and improve readability.
- Use pre-commit hooks to keep routine quality checks automatic.
- Treat missing tests, missing type checks, or missing lint wiring as explicit quality risks worth reporting.

## 13. Legacy Patterns to Avoid (Migration-Only Exceptions)

- Legacy typing aliases in new code (`Optional`, `Union`, `List`, `Dict`).
- Pydantic v1 APIs (`@validator`, `@root_validator`, `.dict()`, `.json()`).
- New `python setup.py ...` command usage.
- Unstructured dict-heavy contracts where typed models are feasible.
- Backward-compatibility layers for older Python behavior that the project no longer supports.
- Custom shims for typing features already available through `typing_extensions`.

Exception policy:

- Temporary retention is allowed only for explicit compatibility constraints.
- Document what is retained, why it remains, and the follow-up modernization step.

## 14. Source Map (Official References)

- Python release notes: <https://docs.python.org/3/whatsnew/index.html>
- `typing` docs (`override`, aliases, modern typing): <https://docs.python.org/3/library/typing.html>
- `pathlib` docs (`Path.walk`): <https://docs.python.org/3/library/pathlib.html>
- `itertools` docs (`batched`): <https://docs.python.org/3/library/itertools.html>
- PEP 695 (`type` statement, type params): <https://peps.python.org/pep-0695/>
- PEP 698 (`@override`): <https://peps.python.org/pep-0698/>
- PEP 701 (f-strings): <https://peps.python.org/pep-0701/>
- PEP 709 (inlined comprehensions): <https://peps.python.org/pep-0709/>
- PEP 688 (buffer protocol typing): <https://peps.python.org/pep-0688/>
- Packaging guide (`[build-system]`): <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>
- Setuptools deprecation of setup.py commands: <https://setuptools.pypa.io/en/stable/deprecated/commands.html>
- Ruff settings (`target-version` and inference): <https://docs.astral.sh/ruff/settings/>
- Mypy changelog (PEP 695 support maturity): <https://mypy.readthedocs.io/en/stable/changelog.html>
- Pydantic v2 migration guide: <https://docs.pydantic.dev/latest/migration/>
- Pytest good practices (`python -m pytest`): <https://docs.pytest.org/en/stable/explanation/goodpractices.html>
- Pre-commit docs: <https://pre-commit.com/>
- pip-tools docs: <https://pip-tools.readthedocs.io/en/stable/>
- basedpyright docs: <https://docs.basedpyright.com/latest/>
- Pyright configuration (official source): <https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md>
