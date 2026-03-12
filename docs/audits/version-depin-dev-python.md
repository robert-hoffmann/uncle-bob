# Version De-Pinning — dev-python

## SKILL.md Changes

- Frontmatter `description`: "Python 3.12.x" → "Python (latest stable)"
- Overview: "Python 3.12.x modern defaults" → "Python modern defaults for the latest stable release"
- Replace "Version Contract" section with "Version & Research Policy"
- Remove `>=3.12,<3.13` range references
- "Python 3.13+" → "pre-release/next-version"
- Tool mentions: keep "uv (or pip)" style per tooling decision
- Keep `Pydantic v2` as "latest stable Pydantic (v2+)"

## python-standards.md Content Changes

- Title: "Python Standards (Project-Specific, Non-Formatting, Python 3.12.x)" → "Python Standards (Project-Specific, Non-Formatting, Latest Stable)"
- "Python 3.12.x" → "latest stable Python" throughout
- ">=3.12,<3.13" → "latest stable (detect from pyproject.toml)"
- "3.12" in feature descriptions → "modern Python" (keep PEP refs as immutable)
- Python docs URLs: `/3.12/` → `/3/` (latest stable docs)
- Keep PEP references as-is (immutable identifiers)
- Add header note: verify against latest Python docs via web search
