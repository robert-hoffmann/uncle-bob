# Workflow Documentation

This directory contains the repository's active GitHub Actions workflows.

Use this file as the source of truth for:

- what each workflow is responsible for
- which events trigger it
- which local Make targets correspond to CI behavior
- where GitHub-specific orchestration still lives in YAML instead of Make

## Workflow Inventory

| Workflow File | Workflow Name | Purpose | Local Parity |
| ------------- | ------------- | ------- | ------------ |
| `quality.yml` | `quality` | Repository quality gates: Markdown, Python, YAML, governance integrity, and governance regression checks. | `make check` |
| `decision-governance.yml` | `decision-governance` | Pull-request governance gate for ADR, claim-register, and decision-report enforcement. | Partial: individual governance scripts, not a single Make target |

## Quality Workflow

File: `.github/workflows/quality.yml`

### Purpose

This workflow is the main fast-feedback quality gate for the repository. It is designed to stay closely aligned with local development commands.

### Triggers

- push to `main`
- pull requests on `opened`, `synchronize`, `reopened`, and `ready_for_review`

### Job Model

The workflow uses multiple jobs instead of one large serial job.

- `markdownlint`
  Runs Markdown linting through `make lint-md`.
- `python-quality` matrix
  Runs four independent Python-backed checks:
  - `make lint-py`
  - `make lint-yaml`
  - `make test-integrity`
  - `make test-governance`

This keeps job output focused, preserves parallelism, and still centralizes the actual commands in the Makefile.

### Runtime Setup

- Markdown job:
  - checks out the repo
  - installs Node 22
  - runs `make lint-md`
- Python-backed jobs:
  - check out the repo
  - install Python 3.12
  - install `uv` with `astral-sh/setup-uv`
  - run `uv sync`
  - execute the relevant Make target

### Local Equivalent

- Full parity check: `make check`
- Individual checks:
  - `make lint-md`
  - `make lint-py`
  - `make lint-yaml`
  - `make test-integrity`
  - `make test-governance`

### Why This Workflow Uses Make

This workflow intentionally delegates shared command logic to the Makefile so local development and CI use the same entrypoints.

Benefits:

- less duplication between local and CI commands
- easier command discovery for contributors
- lower risk of CI drift from local validation behavior

## Decision-Governance Workflow

File: `.github/workflows/decision-governance.yml`

### Purpose

This workflow enforces governance-specific PR rules around ADR updates, registry freshness, and claim-register validation.

### Triggers

- pull requests on `opened`, `synchronize`, `reopened`, and `ready_for_review`

### Why This Workflow Is Separate

Unlike `quality.yml`, this workflow is not just a thin wrapper around repo commands. It contains GitHub-specific orchestration that depends on pull-request metadata and step-to-step state.

It is kept separate because it needs to:

- diff PR branches using GitHub-provided SHAs
- decide conditionally whether claim checks should run
- capture step exit codes without failing early
- upload decision artifacts
- enforce combined governance outcomes at the end of the workflow

That behavior belongs in workflow YAML, or in dedicated scripts called by the workflow, rather than in the Makefile.

### Main Flow

1. Check out the repo with full history needed for diffing.
2. Build the changed-file list for the PR.
3. Decide whether governance reference/script changes require claim checks.
4. Rebuild `docs/adr/registry.json` and fail if the committed file is stale.
5. Run the ADR gate.
6. Run the claim gate only when relevant files changed.
7. Upload decision-governance artifacts.
8. Enforce final workflow status from the collected step exit codes.

### Artifacts

This workflow uploads `decision-governance-artifacts`, which may include:

- changed file lists
- ADR gate output
- claim gate output
- registry build output

### Local Equivalent

There is no single `make` target for this workflow because part of its behavior depends on GitHub PR context.

The closest local commands are the underlying governance scripts:

- `python3 .agents/skills/ub-governance/scripts/build_adr_registry.py`
- `python3 .agents/skills/ub-governance/scripts/check_adr_gate.py`
- `python3 .agents/skills/ub-governance/scripts/check_claim_register.py`

Use `make check` for normal quality validation, and use the governance scripts directly when you need to reproduce decision-gate behavior outside GitHub Actions.

## Editing Guidelines

When changing workflows in this directory:

- prefer Make targets for shared repo commands used both locally and in CI
- keep GitHub event handling, artifacts, matrix strategy, and conditional orchestration in workflow YAML
- update this file whenever workflow names, triggers, or responsibilities change
- keep the root README workflow list aligned with the actual files in this directory
