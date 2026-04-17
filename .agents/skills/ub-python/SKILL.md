---
name: ub-python
description: Design, review, refactor, and test repository Python code using typed Python (latest stable) patterns, boundary validation, and structured error handling. Use when tasks involve Python files, pytest/ruff/mypy workflows, packaging/tooling decisions, dataclass or Pydantic modeling, or Python service/repository logic.
---

# UB Python

## Overview

Use this skill to enforce latest stable Python modern defaults, strict typing, boundary validation, and migration-aware legacy handling.

Generate modern patterns for new code and refactor legacy patterns incrementally when touching existing code.

Write against the project's currently supported Python version, but structure code so it can move cleanly toward newer stable releases instead of accumulating compatibility layers.

## Load References On Demand

- Load and apply `references/python-standards.md` for canonical Python rules and toolchain policy.
- Load and apply `references/repository-python-workflows.md` for this repository's actual Python validation and packaging-tooling baseline.

## Forward-Compatibility Contract

- Implement for the project's actual supported Python version, runtime, and library floor.
- Bias design toward the next stable upgrade path rather than preserving older-version behavior by default.
- Prefer `typing_extensions`, `collections.abc`, and `abc` as forward-compatible tools when they reduce future rewrite cost and avoid custom compatibility layers.
- Add backward-compatibility shims, fallbacks, or bridge code only when an explicit support contract or staged migration plan requires them.

## Core Workflow

1. Detect runtime and tooling truth from project files (`pyproject.toml`, lockfiles, CI, existing configs).
2. Confirm Python scope and version contract before proposing implementation.
3. Propose at least two viable implementation paths for non-trivial Python work, with concise pros/cons.
4. Choose the simplest path that satisfies correctness, maintainability, and project constraints.
5. Write or adjust tests first for behavior changes.
6. Implement minimal changes to pass tests, then refactor while preserving behavior and boundaries.
7. Run repository-configured validation after modifying Python code, starting with the smallest relevant scope.
8. Report outcomes, bounded exceptions, and any missing tooling gaps that materially reduce confidence.

## Version & Research Policy

- Target the latest stable release of Python for guidance, but implement against the project's actual supported version contract.
- Detect the project's actual Python version from `pyproject.toml`, `.python-version`, lockfiles, and CI configuration.
- Use web search to verify current best practices, API availability, and migration guidance against official Python documentation.
- Do not generate syntax or stdlib behavior only available in unreleased Python versions unless the user explicitly requests it.
- When the project's installed version is behind latest stable, note the version gap, recommend an upgrade path, and prefer patterns that will survive that upgrade cleanly.
- Refer to AGENTS.md for centralized version policy and default tooling.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: Python release changes, tooling maturity shifts, packaging guidance updates, or repository validation changes that alter the real enforced baseline.
- Enforcement: advisory only; freshness should highlight review targets without pretending missing mypy or pytest wiring is a blocker in this repository.
- Stable core: strong typing, boundary validation, structured errors, and repository-truth validation remain the durable baseline even when tooling preferences evolve.

## Implementation Rules

### Runtime and Environment

- Use project-local virtual environments and interpreter-explicit commands.
- Prefer `python -m ...` and/or `uv run ...` so command execution matches the intended interpreter.
- Prefer `pathlib.Path` for filesystem operations, with Windows-safe path handling.

### Typing and API Design

- Type annotate non-trivial functions and all public interfaces.
- Prefer modern syntax: `list[str]`, `dict[str, int]`, `X | Y`, `type Alias = ...`.
- Prefer interface types from `collections.abc` (`Iterable`, `Sequence`, `Mapping`, `Callable`) and abstract contracts from `abc` or `Protocol` when concrete mutation behavior is not required.
- Prefer `typing_extensions` for newer typing features when the project's supported version floor does not provide them, or when the backport gives cleaner cross-version semantics and future-upgrade safety.
- Use `Protocol`, `Self`, `override`, `TypeGuard`, `TypeIs`, `Required`, `NotRequired`, `ReadOnly`, `TypeAliasType`, and `assert_never` when they improve correctness and refactor safety.
- Do not invent custom typing compatibility shims when `typing_extensions` already provides the migration path.
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

### Post-Edit Validation Contract

- After generating or modifying Python code, run the repository-configured checks that are relevant to the touched scope.
- Minimum expectation: run Ruff when Ruff is configured, run a type checker when mypy/pyright/basedpyright is configured, and run targeted pytest coverage when tests exist or behavior changed.
- Start narrow (`ruff check` on touched files, targeted tests, scoped type checks) and widen only when failures indicate broader impact.
- Fix newly introduced lint/type/test failures before finalizing when they are within the task scope.
- If a configured check cannot be run, state exactly why it was skipped or blocked.

Repository truth note:

- Current repository baseline is `uv` + `ruff` + stdlib `unittest` plus workflow-specific direct script checks.
- `mypy` and `pytest` are preferred patterns for Python-heavy repos, but they are not currently repository-wired gates here.
- When working in this repository, report that gap explicitly instead of pretending those checks are already part of the enforced baseline.

### Tooling Gap Warning Policy

- If repository Python tooling for linting, type checking, or testing is missing, weakly configured, or clearly not wired into normal workflows, warn the user explicitly.
- Recommend concrete additions when relevant: Ruff for linting, mypy/pyright for type checking, pytest for tests, and pre-commit or CI wiring for automatic enforcement.
- Treat missing quality gates as a reported risk, not as silent permission to skip validation.

### Error Handling, Logging, and Boundaries

- Fail with specific exceptions and preserve causal chains (`raise ... from err`).
- Log decisions and failures with actionable context, not noise.
- Preserve layered boundaries: presentation -> service -> repository -> data.

## Toolchain Strategy (Primary + Fallback)

- Treat repository-configured tooling as the source of truth. If Ruff, mypy, pytest, pre-commit, or other checks are configured, generate code that satisfies their active rules instead of relying on generic defaults.
- If Ruff, mypy, pytest, pre-commit, or equivalent checks are configured, run the relevant ones after edits instead of stopping at code generation.
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
- Do not preserve support for older Python behavior "just in case" when the project no longer targets it.
- Do not add custom backward-compatibility layers for typing features when `typing_extensions` or the standard library already covers the intended migration path.

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
6. Tooling gap note: missing or weak lint/type/test enforcement that the user should consider adding or wiring in.

## References

- Core rules and source-backed policy: `references/python-standards.md`
- Repository-specific workflow and validation baseline: `references/repository-python-workflows.md`

## Completion Checklist

- Latest stable Python baseline is enforced intentionally.
- Modern typing and boundary validation are applied where relevant.
- Data model choice (dataclass vs Pydantic v2) is explicit.
- Concurrency and error handling patterns are structured and observable.
- Repository-configured lint/type/test checks were run after edits, or an explicit reason was reported.
- No new legacy output is introduced.
- Missing lint/type/test enforcement was reported when relevant.
- Any retained legacy behavior is documented with a migration path.
