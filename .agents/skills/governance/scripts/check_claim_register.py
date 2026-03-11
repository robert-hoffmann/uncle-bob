#!/usr/bin/env python3
"""Validate governance claim register and policy-use constraints."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

BLOCKED_EXIT = 2


REQUIRED_FIELDS = [
    "claimId",
    "claimText",
    "status",
    "sourceTier",
    "sources",
    "verifiedAt",
    "reviewBy",
    "owner",
]

ALLOWED_STATUS = {"verified", "partial", "unverified"}
ALLOWED_TIERS = {"primary", "secondary", "social"}


def parse_date(value: str, field_name: str, errors: list[str], claim_id: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        errors.append(f"{claim_id}: invalid ISO date in {field_name}: {value}")
        return None


def validate_exception(exception: dict[str, Any], claim_id: str, errors: list[str]) -> tuple[bool, dt.date | None]:
    required = ["owner", "expiresAt", "followUp"]
    missing = [key for key in required if not str(exception.get(key, "")).strip()]
    if missing:
        errors.append(f"{claim_id}: exception missing fields: {', '.join(missing)}")
        return False, None

    expires_raw = str(exception.get("expiresAt", "")).strip()
    expires_at = parse_date(expires_raw, "exception.expiresAt", errors, claim_id)
    return expires_at is not None, expires_at


def validate_claim(
    claim: dict[str, Any],
    today: dt.date,
    errors: list[str],
    warnings: list[str],
    blocked_reasons: list[str],
) -> None:
    claim_id = str(claim.get("claimId") or "UNKNOWN")

    missing_fields = [field for field in REQUIRED_FIELDS if field not in claim]
    if missing_fields:
        errors.append(f"{claim_id}: missing required fields: {', '.join(missing_fields)}")
        return

    status = str(claim.get("status", "")).strip()
    if status not in ALLOWED_STATUS:
        errors.append(f"{claim_id}: invalid status '{status}'")

    source_tier = str(claim.get("sourceTier", "")).strip()
    if source_tier not in ALLOWED_TIERS:
        errors.append(f"{claim_id}: invalid sourceTier '{source_tier}'")

    sources = claim.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{claim_id}: sources must be a non-empty array")
    else:
        for idx, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"{claim_id}: source #{idx + 1} must be an object")
                continue
            title = str(source.get("title", "")).strip()
            url = str(source.get("url", "")).strip()
            if not title or not url:
                errors.append(f"{claim_id}: source #{idx + 1} requires title and url")

    verified_raw = str(claim.get("verifiedAt", "")).strip()
    review_raw = str(claim.get("reviewBy", "")).strip()
    verified_at = parse_date(verified_raw, "verifiedAt", errors, claim_id)
    review_by = parse_date(review_raw, "reviewBy", errors, claim_id)

    if verified_at and review_by and verified_at > review_by:
        errors.append(f"{claim_id}: verifiedAt cannot be after reviewBy")

    if review_by and review_by < today:
        blocked_reasons.append(
            f"{claim_id}: claim reviewBy date {review_by.isoformat()} is stale."
        )

    blocking_use = bool(claim.get("blockingUse", False))

    if status == "unverified" and blocking_use:
        blocked_reasons.append(
            f"{claim_id}: unverified claim cannot be used for blocking governance rationale."
        )

    if status == "partial" and blocking_use:
        exception = claim.get("exception")
        if not isinstance(exception, dict):
            blocked_reasons.append(
                f"{claim_id}: partial blocking claim requires exception metadata."
            )
        else:
            valid_exception, expires_at = validate_exception(exception, claim_id, errors)
            if valid_exception and expires_at and expires_at < today:
                blocked_reasons.append(
                    f"{claim_id}: partial blocking claim exception expired on {expires_at.isoformat()}."
                )

    if status == "verified" and source_tier == "social" and blocking_use:
        warnings.append(
            f"{claim_id}: verified social-tier claim is used for blocking policy; validate primary-source support."
        )


def write_output(path: Path | None, payload: dict[str, Any]) -> None:
    content = json.dumps(payload, indent=2) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(content, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-register", default="docs/adr/claim-register.json")
    parser.add_argument("--output")
    parser.add_argument("--today", help="Override ISO date for deterministic checks")
    args = parser.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    claim_path = Path(args.claim_register)

    if not claim_path.exists():
        payload = {
            "status": "fail",
            "errors": [f"Claim register not found: {claim_path.as_posix()}"]
        }
        write_output(Path(args.output) if args.output else None, payload)
        return 1

    try:
        payload_json = json.loads(claim_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        payload = {
            "status": "fail",
            "errors": [f"Invalid JSON in claim register: {exc}"]
        }
        write_output(Path(args.output) if args.output else None, payload)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    blocked_reasons: list[str] = []

    schema_version = str(payload_json.get("schemaVersion", ""))
    if schema_version != "1":
        errors.append("schemaVersion must be '1'")

    claims = payload_json.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be an array")
        claims = []

    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim entries must be objects")
            continue
        validate_claim(claim, today, errors, warnings, blocked_reasons)

    if errors:
        status = "fail"
    elif blocked_reasons:
        status = "blocked"
    else:
        status = "pass"

    output = {
        "status": status,
        "claimRegister": claim_path.as_posix(),
        "claimCount": len(claims),
        "errors": errors,
        "blockedReasons": blocked_reasons,
        "warnings": warnings,
        "generatedAt": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

    write_output(Path(args.output) if args.output else None, output)

    if status == "pass":
        return 0
    if status == "blocked":
        return BLOCKED_EXIT
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
