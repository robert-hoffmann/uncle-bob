# Scaffold Adaptation

The scaffold is intentionally neutral. Adapt it explicitly after copying it into
the target repository.

## Required Adaptation Inputs

Replace or confirm these values early:

1. initiative name
2. initiative owner
3. initiative root path
4. repository-specific validation commands
5. docs or architecture paths that must stay synchronized
6. governance bridge level
7. evidence expectations

## Placeholder Rules

1. Keep placeholders obvious and easy to search.
2. Replace placeholders directly; do not leave implied local knowledge.
3. Do not copy examples, repository names, commands, or file paths from the
   source repository unless they were deliberately adapted.

## Portability Rules

1. Prefer relative paths inside initiative artifacts.
2. Treat validation commands as repository inputs, not workflow defaults.
3. Keep the scaffold usable even without ADRs, claim registers, or CI.
4. Keep local conventions in repository instructions, not hardcoded into the
   portable scaffold.

## Canonical Copy Rule

When starting a new initiative:

1. copy `assets/initiative-template/`, or run `scripts/scaffold_initiative.py`
2. rename the copied root for the new initiative
3. replace placeholders in `README.md`, `prd.md`, and `roadmap.md`
4. initialize the sprint set from `sprint-template/`
5. adapt validation and governance details to repository truth

## Anti-Patterns

Do not:

1. edit the canonical asset templates for one initiative
2. leave repository-specific placeholders unresolved after setup
3. hardcode one repository's validation commands into the portable scaffold
4. assume every repository uses the same docs, CI, or governance structure