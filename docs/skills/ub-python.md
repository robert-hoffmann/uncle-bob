# UB Python

Source: `.agents/skills/ub-python/SKILL.md`

`ub-python` guides Python implementation, tests, typing, packaging, validation,
and repository logic.

## When To Use It

Use it for Python files, pytest or unittest work, Ruff, type checking,
dataclasses, Pydantic, API boundaries, service logic, or Python project setup.

## What It Changes

- detects project tooling before changing code
- prefers typed boundaries and structured error handling
- favors behavior-focused tests
- aligns commands with the project’s Python workflow
- modernizes incrementally instead of adding broad compatibility layers

## Common Prompts

- “Use `ub-python` to add tests for this behavior.”
- “Review this script for typing and boundary validation.”
- “Update this Python helper without changing its public contract.”

## Boundaries

Do not use it as a general documentation or workflow-planning skill. Pair it
with `ub-workflow` when the Python change itself needs planning artifacts.

## Tradeoffs

Strength: makes Python changes safer and easier to validate.

Cost: strict boundary work can reveal follow-up modernization outside the
initial task.
