# Decision-Memory and Claim Policy

This file defines decision checks for ADR and claim governance.

## 1) Gate Decision Inputs

1. required artifact inventory for scope
2. high-risk path matches
3. ADR registry alignment state
4. claim-register status for blocking rationale
5. active exception validity from governance contract

## 2) Decision-Memory Rules

1. high-risk path changes require ADR alignment or active ADR waiver
2. confidence/release completion cannot rely on expired waivers
3. structural/high-risk runs require non-empty `decision.adrRefs` in validation record

## 3) Claim-Verification Rules

1. `verified`: allowed for blocking rationale
2. `partial`: allowed for blocking rationale only with active bounded exception
3. `unverified`: not allowed for blocking rationale

## 4) Gate Decision Process

1. inventory required artifacts
2. verify deterministic presence and freshness
3. evaluate ADR alignment state
4. evaluate claim-confidence constraints
5. evaluate exception validity
6. declare `pass`, `fail`, or `blocked` with explicit reasons and artifact paths
