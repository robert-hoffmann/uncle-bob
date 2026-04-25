# Workflow Documentation

This directory contains the repository's active GitHub Actions workflows.

Use this file as the source of truth for:

- what each workflow is responsible for
- which events trigger it
- which local Taskfile tasks correspond to CI behavior
- where GitHub-specific orchestration still lives in YAML instead of the Taskfile

## Workflow Inventory

| Workflow File | Workflow Name | Purpose | Local Parity |
| ------------- | ------------- | ------- | ------------ |
| `quality.yml` | `quality` | Repository quality gates: Python, YAML, repository integrity, and regression checks. | `task check` |
| `decision-governance.yml` | `decision-governance` | Pull-request governance gate for ADR, claim-register, and decision-report enforcement. | Partial: individual governance scripts, not a single Taskfile task |
| `build-docs.yml` | `build-docs` | VitePress documentation build and GitHub Pages deployment. | `npm run check:docs-sync` and `npm run docs:build` |

## Quality Workflow

File: `.github/workflows/quality.yml`

### Purpose

This workflow is the main fast-feedback quality gate for the repository. It is designed to stay closely aligned with local development commands.

### Triggers

- push to `main`
- pull requests on `opened`, `synchronize`, `reopened`, and `ready_for_review`

### Job Model

The workflow uses multiple jobs instead of one large serial job.

- `python-quality` matrix
  Runs ten independent Python-backed checks:
  - `task lint-py`
  - `task lint-yaml`
  - `task test-repo-catalog`
  - `task test-package-metadata`
  - `task test-repo-paths`
  - `task test-skill-schema`
  - `task test-governance-integrity`
  - `task test-governance`
  - `task test-repo-maintenance`
  - `task test-workflow`

This keeps job output focused, preserves parallelism, and still centralizes the actual commands in the Taskfile.

### Runtime Setup

- Python-backed jobs:
  - check out the repo
  - install Python 3.12
  - install `uv` with `astral-sh/setup-uv`
  - install Task with `arduino/setup-task`
  - run `uv sync`
  - execute the relevant Taskfile task

### Local Equivalent

- Full parity check: `task check`
- Individual checks:
  - `task lint-py`
  - `task lint-yaml`
  - `task test-repo-catalog`
  - `task test-package-metadata`
  - `task test-repo-paths`
  - `task test-skill-schema`
  - `task test-governance-integrity`
  - `task test-governance`
  - `task test-repo-maintenance`
  - `task test-workflow`
  - `task test-integrity`

### Why This Workflow Uses Taskfile

This workflow intentionally delegates shared command logic to the Taskfile so local development and CI use the same entrypoints.

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

That behavior belongs in workflow YAML, or in dedicated scripts called by the workflow, rather than in the Taskfile.

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

There is no single `task` command for this workflow because part of its behavior depends on GitHub PR context.

The closest local commands are the underlying governance scripts:

- `uv run python .agents/skills/ub-governance/scripts/build_adr_registry.py`
- `uv run python .agents/skills/ub-governance/scripts/check_adr_gate.py`
- `uv run python .agents/skills/ub-governance/scripts/check_claim_register.py`

Use `task check` for normal quality validation, and use the governance scripts directly when you need to reproduce decision-gate behavior outside GitHub Actions.

## Build-Docs Workflow

File: `.github/workflows/build-docs.yml`

### Purpose

This workflow builds the VitePress documentation site and deploys the root
`dist/` artifact to GitHub Pages.

### Triggers

- push to `main`
- manual `workflow_dispatch`

### Main Flow

1. Check out the repository.
2. Set up Node 24 with npm caching.
3. Install dependencies with `npm ci`.
4. Run `npm run check:docs-sync`.
5. Run `npm run docs:build`.
6. Upload `dist/` as the Pages artifact.
7. Deploy to GitHub Pages.

### Local Equivalent

- Drift check: `npm run check:docs-sync`
- Production docs build: `npm run docs:build`

## Editing Guidelines

When changing workflows in this directory:

- prefer Taskfile tasks for shared repo commands used both locally and in CI
- keep GitHub event handling, artifacts, matrix strategy, and conditional orchestration in workflow YAML
- update this file whenever workflow names, triggers, or responsibilities change
- keep the root README workflow list aligned with the actual files in this directory
