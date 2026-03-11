---
name: dev-python
description: Design, review, refactor, and test repository Python code using typed Python 3.12.x patterns, boundary validation, and structured error handling. Use when tasks involve Python files, pytest/ruff/mypy workflows, packaging/tooling decisions, dataclass or Pydantic modeling, or Python service/repository logic.
---

# Dev Python

## Overview

Use this skill to enforce Python 3.12.x modern defaults, strict typing, boundary validation, and migration-aware legacy handling.

Generate modern patterns for new code and refactor legacy patterns incrementally when touching existing code.

## Load References On Demand

- Read `references/python-standards.md` for canonical Python 3.12.x rules and toolchain policy.

## Core Workflow

1. Detect runtime and tooling truth from project files (`pyproject.toml`, lockfiles, CI, existing configs).
2. Confirm Python scope and version contract before proposing implementation.
3. Propose at least two viable implementation paths for non-trivial Python work, with concise pros/cons.
4. Choose the simplest path that satisfies correctness, maintainability, and project constraints.
5. Write or adjust tests first for behavior changes.
6. Implement minimal changes to pass tests, then refactor while preserving behavior and boundaries.
7. Run available checks and report outcomes plus any bounded exceptions.

## Version Contract

- Treat Python `3.12.x` as the default baseline.
- Do not generate Python `3.13+`-only syntax or stdlib behavior unless the user explicitly requests a forward-compatibility experiment.
- Keep default runtime guidance aligned with `>=3.12,<3.13`.

## Implementation Rules

### Runtime and Environment

- Use project-local virtual environments and interpreter-explicit commands.
- Prefer `python -m ...` and/or `uv run ...` so command execution matches the intended interpreter.
- Prefer `pathlib.Path` for filesystem operations, with Windows-safe path handling.

### Typing and API Design

- Type annotate non-trivial functions and all public interfaces.
- Prefer modern syntax: `list[str]`, `dict[str, int]`, `X | Y`, `type Alias = ...`.
- Prefer interface types from `collections.abc` (`Iterable`, `Sequence`, `Mapping`, `Callable`) when mutation is not required.
- Use `Protocol`, `Self`, `typing.override`, `TypeGuard`, and `assert_never` when they improve correctness and refactor safety.
- Keep `Any` contained to boundaries and document why when unavoidable.

### Data Modeling and Validation

- Validate boundary data (HTTP, file, env, queue payloads) with Pydantic v2 or explicit manual validation.
- Prefer dataclasses for internal domain containers.
- Dataclass defaults: `@dataclass(slots=True, kw_only=True)` and `field(default_factory=...)` for mutable fields.
- Pydantic v2 defaults: `ConfigDict`, `@field_validator`, `@model_validator`, `model_dump()`.

### Concurrency and Structured Errors

- Prefer `asyncio.TaskGroup` for concurrent async work.
- Handle grouped failures using `ExceptionGroup` and `except*` where relevant.
- Use explicit cancellation and timeout behavior for network or external I/O.

### Packaging and Toolchain Hygiene

- Keep project metadata in `pyproject.toml` and include `[build-system]` for build backend clarity.
- Prefer modern build/install commands (`python -m pip`, `python -m build`) over deprecated `python setup.py ...` command execution.
- Favor standard library first; add dependencies only when they materially improve correctness, maintainability, or DX.

### Error Handling, Logging, and Boundaries

- Fail with specific exceptions and preserve causal chains (`raise ... from err`).
- Log decisions and failures with actionable context, not noise.
- Preserve layered boundaries: presentation -> service -> repository -> data.

## Toolchain Strategy (Primary + Fallback)

- Primary stack: `uv`, `ruff`, `mypy`, `pytest`, `pre-commit`.
- Fallback stack when constraints require it:
  - dependency management: `pip-tools`
  - type checker: `pyright` or `basedpyright`
  - editor feedback: Pylance (Pyright engine) with `python.analysis.typeCheckingMode = "standard"` when team/editor policy prefers standard-mode diagnostics
- Keep one-command check workflows discoverable in project docs/automation when possible.

## Tradeoff Handling

- For major design or tooling choices, always present at least two options with concise pros/cons.
- Default to the safest modern option unless compatibility, policy, or delivery constraints justify an alternative.
- Document any intentionally deferred cleanup or technical debt retained for compatibility.

## Legacy-Avoidance Guardrails

- Do not generate legacy typing aliases in new code (`Optional`, `Union`, `List`, `Dict`) unless required by compatibility constraints.
- Do not generate Pydantic v1 validator/style APIs in new code.
- Do not introduce new `python setup.py ...` command usage.
- Do not add untyped dict-heavy contracts when typed models are practical.

Migration-aware exception policy:
- Allow temporary legacy retention only for explicit compatibility constraints in existing code.
- Document exactly what is retained, why it is retained, and the next modernization step.

## Output Requirements

When generating or reviewing Python code, include:

1. Environment note: detected runtime, interpreter strategy, and relevant tooling context.
2. Decision note: chosen approach and at least one alternative.
3. Tradeoff note: concise pros/cons for chosen and rejected paths.
4. Legacy note: removed legacy patterns or bounded exceptions with rationale.
5. Validation note: checks run (lint/type/test/build) and outcomes.

## References

- Core rules and source-backed policy: `references/python-standards.md`

## Completion Checklist

- Python 3.12.x baseline is enforced intentionally.
- Modern typing and boundary validation are applied where relevant.
- Data model choice (dataclass vs Pydantic v2) is explicit.
- Concurrency and error handling patterns are structured and observable.
- No new legacy output is introduced.
- Any retained legacy behavior is documented with a migration path.
