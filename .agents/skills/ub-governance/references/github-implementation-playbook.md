# GitHub Implementation Playbook

Use this file when translating repository policy to concrete GitHub controls.

## 1) Rulesets-First Governance

Prefer repository/organization rulesets over ad-hoc branch settings.

Apply to:

1. protected branches
2. protected tags
3. push restrictions for sensitive patterns

References:

- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>

## 2) Actions Hardening

Baseline:

1. minimal permissions at workflow/job scope
2. avoid broad default token scopes
3. pin critical actions to immutable refs for higher-assurance repos

Reference:

- <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>

## 3) Dependency Governance

Baseline:

1. enable Dependabot updates for active ecosystems
2. add dependency review in PR workflows
3. document dependency exception process using governance contract

Reference:

- <https://docs.github.com/en/code-security/dependabot>

## 4) Decision Gate Integration

Repository policy must include a blocking decision-governance workflow for high-risk changes.
Implementation details are owned by the decision-governance workflow and associated scripts.

## 5) Contribution Governance Artifacts

Recommended:

1. `.github/CODEOWNERS`
2. `.github/pull_request_template.md`
3. issue templates in `.github/ISSUE_TEMPLATE/`

Conventions:

1. branch prefixes: `feat/*`, `fix/*`, `chore/*`, `docs/*`
2. commits: Conventional Commits
3. PR titles: Conventional Commits when squash-merge is default

## 6) Provider Extension Model

Keep policy intent portable.
Document provider-specific mechanics separately when needed.
