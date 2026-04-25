# References And Progressive Disclosure

Uncle Bob skills are intentionally layered. The main `SKILL.md` gives the
agent a compact operating contract. Deeper `references/`, assets, and helper
scripts stay available for the moments when the task actually needs them.

## Why This Matters

Progressive disclosure keeps the installed skill system useful in two
directions:

1. simple tasks do not pay the cost of reading every detailed rule
2. complex tasks still have durable, reviewable guidance when details matter

That is why a skill page should explain the main behavior and surface the most
important ideas from the reference surfaces without copying every reference
into the public docs.

## Main Skill Surface

The main `SKILL.md` usually carries:

- activation rules
- non-use boundaries
- core workflow
- required output or validation expectations
- reference-loading triggers

This is the part the agent needs immediately after a skill activates.

## Reference Surfaces

References carry deeper detail that would be too heavy in the main skill:

- exact patterns and anti-patterns
- migration maps
- configuration resolution rules
- validation checklists
- glossary or schema details
- optional adoption bundles

For example, `ub-quality` keeps design principles, formatting, documentation,
readability, and portability in separate references. `ub-workflow` keeps
artifact contracts, lifecycle details, and scaffold helper behavior separate.
Specialist skills keep framework patterns and legacy-to-modern migration rules
in references so the main page can stay readable.

## How The Agent Uses Them

The intended behavior is selective loading:

1. load the skill when the task matches its routing description
2. read the main `SKILL.md` first
3. load only the references whose triggers apply
4. use skill-owned assets or helper scripts only when the task needs them
5. report relevant constraints without treating every optional reference as
   always active

This protects both speed and correctness. A tiny CSS tweak should not load an
entire migration guide, but a Tailwind upgrade absolutely should.

## What Public Docs Should Do

Public docs should make the model easy to understand:

- explain what the skill does
- surface the important principles, tradeoffs, and patterns from the references
- name the references that are worth knowing about after the ideas are clear
- explain when deeper references become relevant during real work
- avoid copying reference files verbatim
- keep repository-only maintenance details out of the public site

The source skill files remain the operational truth. These docs are the
reader-facing map.

## Related Pages

- [Skill System](/guide/skill-system)
- [Routing Model](/guide/routing-model)
- [Portability Model](/guide/portability-model)
- [Skill Catalog](/skills/)
