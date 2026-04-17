# Sprint 07 Evidence

## Taskfile Parity Mapping

Sprint 07 added first-class Task targets for each repository-integrity checker:

1. `task test-repo-catalog`
2. `task test-package-metadata`
3. `task test-repo-paths`
4. `task test-skill-schema`
5. `task test-governance-integrity`

Aggregate parity targets after Sprint 07:

1. `task test-integrity` runs the 5 integrity targets above.
2. `task test-governance` runs the governance script regression suite.
3. `task test-workflow` runs the ub-workflow scaffold regression suite.
4. `task check` now runs authoritative markdown lint, Python lint, YAML lint,
   all integrity checks, the governance regression suite, and the workflow
   regression suite.

## CI Parity Mapping

`.github/workflows/quality.yml` now runs these Python-quality matrix targets:

1. `lint-py`
2. `lint-yaml`
3. `test-repo-catalog`
4. `test-package-metadata`
5. `test-repo-paths`
6. `test-skill-schema`
7. `test-governance-integrity`
8. `test-governance`
9. `test-workflow`

The standalone markdown job still runs `task lint-md`, so CI and local `task
check` now cover the same authoritative surfaces.

## Authoritative Lint Scope

Sprint 07 tightened the lint scope to keep parity low-noise and reproducible:

1. `lint-md` now targets authoritative root docs, docs content, custom agent
   docs, skill docs, skill references, skill assets, and `.ub-workflows/`.
2. `lint-yaml` now targets authoritative root YAML files, workflow YAML,
   skill `agents/openai.yaml` files, `high-risk-paths.yaml`, and the workflow
   exception-template YAML.
3. Scratch `tmp/` content and repo-snapshot fixture trees are intentionally not
   part of the lint baseline.

## Fixture Coverage

Static repository-integrity fixtures now live under:

`./.agents/skills/ub-governance/tests/governance_scripts/fixtures/repo_integrity/`

Covered cases:

1. `pass/`:
   authoritative pass-state repo snapshot with ignored `tmp/` noise
2. `fail-readme-agent-drift/`:
   README inventory drift
3. `fail-package-metadata-drift/`:
   version and marketplace count drift
4. `fail-legacy-root-registry/`:
   legacy `AGENTS.MD` path-case mismatch
5. `fail-skill-schema/`:
   missing frontmatter and broken local skill reference

## Validation Proof

Passed commands for Sprint 07:

1. `uv run python -m unittest discover -s .agents/skills/ub-governance/tests/governance_scripts -p 'test_*.py' -v`
2. `task test-repo-catalog`
3. `task test-package-metadata`
4. `task test-repo-paths`
5. `task test-skill-schema`
6. `task test-governance-integrity`
7. `task test-governance`
8. `task test-workflow`
9. `task check`
