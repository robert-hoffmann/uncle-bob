# Scaffold Adaptation

This repository uses a repo-default initiative workflow under `./.ub-workflows/`.

The helper bootstraps that operations root from the skill's internal assets, so
the adaptation work is about filling in initiative-specific content, not about
manually copying local templates into place.

## Required Adaptation Inputs

Replace or confirm these values early:

1. initiative name
2. initiative owner
3. initiative root path
4. repository-specific validation commands or checks
5. docs or architecture paths that must stay synchronized
6. governance bridge level and profile when governance applies
7. evidence expectations

## Placeholder Rules

1. Keep placeholders obvious and easy to search.
2. Replace placeholders directly; do not leave implied local knowledge.
3. Do not copy examples, repository names, commands, or file paths from the
   source repository unless they were deliberately adapted.
4. Distinguish blocking machine placeholders from human-authored reasoning
   prompts.

Plain-language `Replace with ...` placeholders are intentional in these
workflow documents.

Use them as human-readable authoring prompts rather than converting the entire
workflow surface to `AGENT_TODO` markers.

Interpretation rules:

1. Machine placeholders that prevent execution readiness must be resolved
   before the sprint or initiative artifact is considered ready.
2. Human-authored reasoning prompts are acceptable in canonical templates, but
   they must not remain in prepared sprint artifacts.
3. Do not treat every placeholder-like phrase as equivalent when validating a
   generated initiative.

Generated-output enforcement rules:

1. Treat `REPLACE_*` tokens as required wherever they appear in generated
   initiative output.
2. Treat plain-language `Replace with ...` prompts in `roadmap.md` and
   `sprints/*/sprint.md` as required generated-output placeholders.
3. Treat plain-language `Replace with ...` prompts in `prd.md` and generated
   `closeout.md` files as advisory unless a later phase tightens them.
4. Treat `PENDING_HANDOFF:` markers as advisory carry-forward reminders.
5. Use `references/placeholder-contract.md` as the canonical source for the
   generated-output placeholder severity model.

## Repository Adaptation Rules

1. Prefer relative paths inside initiative artifacts.
2. Keep generated initiative roots under `./.ub-workflows/initiatives/YYYY-MM-DD-slug/`.
3. Copy a provided source PRD into `./prd.md` as-is during scaffold creation.
4. Generate the full roadmap before initializing sprint folders.
5. Keep the final audit as the last roadmap item.
6. Use archive only when the user explicitly asks for it and the initiative is complete.
7. Prepare sprint content explicitly before sprint execution begins, even when
   helper support for full sprint preparation is still evolving.

## Canonical Create Rule

When starting a new initiative:

1. run `scripts/scaffold_initiative.py create <initiative-slug>`
2. import or refine the real PRD in `./prd.md`
3. replace any remaining placeholders in `README.md` and `roadmap.md`
4. stop after PRD import when the roadmap has not yet been planned and approved
5. generate the complete roadmap, including all implementation sprints and the final audit sprint
6. set `roadmap_ready: pass` only after the roadmap is execution-ready
7. run `scripts/scaffold_initiative.py prepare-sprints <initiative-root>` to render roadmap-derived sprint PRDs before Sprint 01 or any later sprint begins
8. materialize sprint folders with `scripts/scaffold_initiative.py init-sprints <initiative-root>` when needed
9. record governance bridge level and profile when governance coordination is active

## Anti-Patterns

Do not:

1. copy a local `initiative-template/` into the generated operations root just to create one initiative
2. leave repository-specific placeholders unresolved after setup
3. initialize sprint folders before the roadmap is complete and approved
4. start sprint execution from placeholder-only sprint shells
5. archive an initiative before the retained note and checklist are complete
