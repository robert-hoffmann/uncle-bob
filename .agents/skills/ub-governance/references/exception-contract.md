# Exception Contract

This file is the canonical exception metadata contract for governance skills.

## 1) Common Required Fields

Every exception record must include:

1. `owner`
2. `rationale`
3. `created_at` (ISO date)
4. `expires_at` (ISO date)
5. `follow_up` (issue or task URL)

## 2) Common Rules

1. Exceptions are temporary and scoped.
2. Expired exceptions are blocking by default until renewed or resolved.
3. Renewal requires a new record with updated rationale and expiry.
4. Exceptions cannot become silent permanent policy.

## 3) Canonical Exception Templates

### Governance Exception

```yaml
governance_exception:
  owner: "@team-or-person"
  rationale: "Why baseline policy cannot be applied now"
  created_at: "2026-03-04"
  expires_at: "2026-03-18"
  follow_up: "https://tracker.example.com/GOV-101"
```

### TDD Exception

```yaml
tdd_exception:
  owner: "@team-or-person"
  rationale: "Why TDD-first cannot be applied for this change"
  created_at: "2026-03-04"
  expires_at: "2026-03-11"
  follow_up: "https://tracker.example.com/TST-123"
```

### Test Double Exception

Use this only when a risky test double is temporarily accepted as reviewer
guidance. It does not bypass missing bugfix regression evidence.

```yaml
test_double_exception:
  owner: "@team-or-person"
  scope: "test file, boundary, or changed behavior"
  rationale: "Why a real implementation, maintained fake, or functional guard cannot be used now"
  risk: "What false confidence this double could create"
  contract_evidence: "Path to contract, integration, or E2E evidence, or missing"
  created_at: "2026-03-04"
  expires_at: "2026-03-11"
  follow_up: "https://tracker.example.com/TST-124"
```

Rules:

1. Keep the exception narrowly scoped to the behavior or boundary.
2. Do not use it to justify mocking the reported bug path.
3. Pair local-source behavior mocks with a functional guard when accepted
   temporarily.

### ADR Waiver Exception

```yaml
adr_waiver_exception:
  owner: "@team-or-person"
  rationale: "Why ADR alignment cannot be completed before merge"
  created_at: "2026-03-04"
  expires_at: "2026-03-11"
  follow_up: "https://tracker.example.com/ADR-310"
```

### Partial Claim Exception

```yaml
partial_claim_exception:
  owner: "@team-or-person"
  rationale: "Why a partial-confidence claim is temporarily accepted for blocking rationale"
  created_at: "2026-03-04"
  expires_at: "2026-03-11"
  follow_up: "https://tracker.example.com/CLM-420"
```

### Release Exception

```yaml
release_exception:
  owner: "@team-or-person"
  rationale: "Why default release flow is bypassed"
  created_at: "2026-03-04"
  expires_at: "2026-03-18"
  follow_up: "https://tracker.example.com/REL-201"
```

### Legacy Retention Exception

```yaml
legacy_exception:
  owner: "@team-or-person"
  rationale: "Why legacy tool/pattern is retained temporarily"
  created_at: "2026-03-04"
  expires_at: "2026-04-03"
  follow_up: "https://tracker.example.com/GOV-102"
```

### E2E Exception

```yaml
e2e_exception:
  owner: "@team-or-person"
  rationale: "Why required E2E check cannot run deterministically"
  created_at: "2026-03-04"
  expires_at: "2026-03-11"
  follow_up: "https://tracker.example.com/E2E-201"
```

### Perf Budget Exception

```yaml
perf_budget_exception:
  owner: "@team-or-person"
  rationale: "Why temporary performance regression is accepted"
  created_at: "2026-03-04"
  expires_at: "2026-03-18"
  follow_up: "https://tracker.example.com/PERF-332"
```

### Freshness Exception

```yaml
freshness_exception:
  owner: "@team-or-person"
  rationale: "Why stale evidence cannot be re-generated yet"
  created_at: "2026-03-04"
  expires_at: "2026-03-11"
  follow_up: "https://tracker.example.com/FRS-301"
```
