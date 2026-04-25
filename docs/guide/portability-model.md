# Portability Model

Uncle Bob is designed to travel as skills, not as a copy of this repository’s
maintenance workflow.

## Portable Skill Payload

The portable surface is the skill content itself:

- each skill’s `SKILL.md`
- skill-owned references
- skill-owned assets
- skill-owned helper scripts
- explicitly named sibling-skill relationships

That content should make sense after installation in another project.

## What Should Not Leak Into Skill Docs

Public skill docs should avoid centering this repository’s internal build,
validation, CI, or release mechanics. Those details are useful for
maintainers, but not for users trying to understand how to use the skills.

## User-Facing Contract

The public site should answer:

- What does the skill do?
- When should I use it?
- What behavior changes after it activates?
- What tradeoffs or boundaries matter?
- How does it combine with sibling skills?

It should not require a reader to understand this repository’s factory setup
before they can use the skills.
