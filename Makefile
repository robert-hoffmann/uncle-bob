SHELL := /bin/bash

UV            := uv run
MARKDOWNLINT  := npx --yes markdownlint-cli2
MARKDOWN_GLOB := "**/*.md" "**/*.mdx"

.PHONY: help sync lint-md lint-py lint-yaml lint test-integrity test-governance test check ci

help:
	@printf "Targets:\n"
	@printf "  make sync            Install or update local Python tooling via uv\n"
	@printf "  make lint-md         Run markdownlint-cli2 via npx\n"
	@printf "  make lint-py         Run Ruff\n"
	@printf "  make lint-yaml       Run yamllint in strict mode\n"
	@printf "  make lint            Run all local lint checks\n"
	@printf "  make test-integrity  Run governance integrity checks\n"
	@printf "  make test-governance Run governance script regression tests\n"
	@printf "  make test            Run local test checks\n"
	@printf "  make check           Run lint + test (closest local CI parity)\n"

sync:
	uv sync

lint-md:
	$(MARKDOWNLINT) $(MARKDOWN_GLOB)

lint-py:
	$(UV) ruff check .

lint-yaml:
	$(UV) yamllint --strict .

lint: lint-md lint-py lint-yaml

test-integrity:
	$(UV) python .agents/skills/governance/scripts/check_skill_integrity.py

test-governance:
	$(UV) python -m unittest discover -s .agents/skills/governance/tests/governance_scripts -p 'test_*.py' -v

test: test-integrity test-governance

check: lint test

ci: check
