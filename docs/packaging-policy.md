# Packaging Policy

This document defines the packaging contract for this repository's Copilot
skills, agents, and plugin metadata.

## Purpose

The policy answers only the packaging questions that the repository currently
needs answered:

1. which assets are required for a skill package
2. which assets are optional enhancements
3. how custom agents fit into the package
4. how plugin metadata should stay synchronized
5. what status skill-local provider metadata has in this repository

This policy is intentionally minimal. It does not create new mandatory assets
unless the repository already depends on them operationally.

## Repository Package Surfaces

The repository package is defined by these top-level authoritative surfaces:

1. `AGENTS.md`
2. `README.md`
3. `plugin.json`
4. `.github/plugin/marketplace.json`
5. `.agents/skills/`
6. `.github/agents/`

The integrity baseline validates those surfaces directly. Packaging policy must
not require additional assets unless the repository is willing to enforce them.

## Skill Packaging Contract

### Required skill assets

Every skill package under `./.agents/skills/<skill-name>/` must include:

1. `SKILL.md`

`SKILL.md` is the canonical required skill artifact because it is the entry
surface used by the repository inventory, repository docs, and integrity
checks.

### Optional skill assets

These assets are optional and should exist only when they add real value:

1. `references/`
2. `assets/`
3. `agents/`
4. `docs/`
5. `scripts/`
6. `tests/`

Optional means:

1. contributors may omit them when the skill does not need them
2. the repository should not treat their absence as packaging failure
3. when present, they should be internally coherent and lintable

Repository convention note:

1. skill-local `tests/` remain optional in principle
2. this repository prefers centralized repo-level tests for validation
   infrastructure because downstream users copy or symlink `.agents/` as live
   skill payload
3. repo-only tests should not be treated as distributed skill content unless a
   specific distribution model explicitly requires that coupling

### Recommended, but not universally required

These patterns are recommended when they improve operability:

1. a `references/` folder when the skill has source-backed policy or detailed
   procedures that should not overload `SKILL.md`
2. `tests/` when the skill includes scripts or deterministic workflow behavior
3. `assets/` when the skill scaffolds reusable project or document structures

## Custom Agent Packaging Contract

Every custom agent under `./.github/agents/` must be represented by a single
`*.agent.md` file.

Additional agent support files may exist elsewhere when needed, but the agent
registry contract for this repository is the `.agent.md` file itself.

## Skill-Local Provider Metadata Policy

Status: optional in principle, currently unused

Decision:

1. provider-specific metadata files such as `agents/openai.yaml` are optional
   per-skill enhancements
2. they are not required for a valid skill package in this repository
3. their absence must not be treated as packaging drift or integrity failure
4. this repository currently ships no skill-local `agents/openai.yaml` files

Rationale:

1. the current integrity baseline does not depend on skill-local provider
   metadata for package validity
2. forcing it to be required would create bureaucracy without improving the
   core inventory or governance contracts
3. keeping the path optional preserves flexibility if a future skill develops a
   real provider-specific need

Operational rule:

1. if a skill develops a concrete provider-specific interface need,
   `agents/openai.yaml` or an equivalent metadata file may be added
2. if a skill does not need that metadata, do not add the file just for
   symmetry
3. when present, provider-specific metadata should stay lintable and
   consistent with the skill's actual purpose

## Plugin Metadata Synchronization

These files are the canonical package-metadata set:

1. `pyproject.toml`
2. `plugin.json`
3. `.github/plugin/marketplace.json`

Rules:

1. version values must stay aligned across the canonical metadata set
2. package descriptions should remain directionally aligned even when written
   for different audiences
3. skill and custom-agent counts surfaced in marketplace or README language
   must reflect the disk truth closely enough for the integrity checks to pass

## Documentation Structure Expectations

The repository does not require every skill to have identical section layouts.
It does require contributor-facing guidance to be explicit where structure
materially affects use.

Minimum expectation for mature skills:

1. clear overview or mission
2. explicit reference-loading guidance when references exist
3. actionable workflow or operating rules
4. output expectations or output contract when the skill produces artifacts or
   structured guidance
5. completion or validation checklist when the skill has deterministic review
   criteria

This is a documentation quality expectation, not a hard package-integrity gate.

## Repository Validation Infrastructure

The repository may keep validation-only assets outside `.agents/skills/` when
they support authoring, CI, pre-commit, or integrity workflows rather than
downstream skill usage.

Current preferred example:

1. centralized repository tests under `./tests/`

Those validation assets are part of repository maintenance, not part of the
minimum downstream skill payload.

## Policy Restraint

This policy intentionally does not require:

1. a `references/` directory for every skill
2. a `tests/` directory for every skill
3. skill-local provider metadata for every skill
4. identical section headings across every `SKILL.md`
5. repo-wide normalization work unrelated to operational clarity

Future policy should stay minimal unless the repository adds new integrity
checks that actually depend on stricter packaging rules.
