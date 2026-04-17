# Freshness Policy

This document defines the repository's warning-only freshness discipline for
high-volatility skill guidance.

## Purpose

The repository contains some guidance surfaces that move faster than the core
governance, workflow, and packaging contracts.

Examples:

1. Tailwind setup and migration guidance
2. Nuxt and Vue framework conventions
3. TypeScript module and compiler defaults
4. Python tooling guidance
5. Copilot customization feature guidance

The goal of freshness review is to make likely review targets explicit without
turning volatile guidance into noisy blocking theater.

## Advisory-Only Contract

Freshness is warning-only in this repository.

Rules:

1. freshness markers must not create a new blocking integrity or CI gate
2. stale volatile guidance is a review signal, not automatic failure
3. contributors should use freshness markers to prioritize review, not to block
   unrelated work by default

This is a deliberate phase-1 choice. The repository may tighten freshness only
after maintainers can prove the advisory layer is trusted, low-noise, and worth
enforcing.

## Freshness Review Marker

High-volatility skills may include a `Freshness Review` section with these
fields:

1. `Volatility`: expected change rate, usually `high` for framework/setup-heavy guidance
2. `Review recommendation`: when maintainers should revisit the skill
3. `Trigger signals`: events that suggest the guidance may need refresh
4. `Enforcement`: always advisory unless repository policy changes later
5. `Stable core`: principles that should remain useful even when recipes evolve

These markers are documentation aids. They are not machine-read policy inputs.

## Review Recommendation

For the current high-volatility skills:

1. review on touch whenever the skill is edited for other reasons
2. review during periodic maintenance, targeting a quarterly rhythm when practical
3. review immediately when official docs, migrations, or repository toolchain
   changes make the current guidance suspect

## Trigger Signals

Common signals that a volatile skill should be reviewed:

1. official migration guides or deprecation notices
2. framework or tool major releases
3. repo-level toolchain or packaging-policy changes
4. repeated user confusion caused by outdated setup recipes
5. integrity, lint, or workflow issues that trace back to stale guidance

## Policy Versus Defaults

Freshness review should help maintainers separate repository policy from strong
house defaults.

Repository policy means a rule is explicitly documented as repository contract
and is usually backed by validation, integrity checks, or mandatory skill
guidance.

Strong defaults mean the repository recommends an approach because it currently
fits best, but downstream adopters may adapt it deliberately.

Examples of strong defaults:

1. latest-stable framework bias
2. primary tool preferences such as `uv` or CSS-first Tailwind
3. ecosystem preferences such as VueUse-first guidance

Examples of repository policy:

1. required package surfaces in `docs/packaging-policy.md`
2. blocking integrity checks wired through `task check`
3. mandatory `ub-quality` alignment rules when that skill is loaded in this repo

## Current High-Volatility Skills

The current advisory freshness layer applies to:

1. `ub-tailwind`
2. `ub-nuxt`
3. `ub-vuejs`
4. `ub-ts`
5. `ub-python`
6. `ub-customizations`

Other skills may adopt the same marker later if their guidance becomes volatile
enough to justify it.

## Non-Goals

This policy does not:

1. add a freshness timestamp registry
2. introduce new CI blockers
3. require repository-wide monthly reviews
4. force every skill to use identical metadata or section layouts
5. weaken the existing integrity and packaging baseline
