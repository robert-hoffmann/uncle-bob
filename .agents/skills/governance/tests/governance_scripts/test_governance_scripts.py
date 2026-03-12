from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

SKILL_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = PROJECT_ROOT / ".agents" / "skills" / "governance" / "scripts"
PYTHON_BIN = sys.executable
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_cmd(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd or PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


class GovernanceScriptRegressionTests(unittest.TestCase):
    def test_build_adr_registry_passes_with_valid_adr(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            adr_dir = tmp_path / "docs" / "adr"
            adr_dir.mkdir(parents=True, exist_ok=True)

            (adr_dir / "0001-valid-governance.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    id: ADR-0001
                    title: Valid ADR
                    status: accepted
                    date: 2026-03-04
                    supersedes: []
                    tags:
                      - governance
                    paths:
                      - src/auth/**
                    constraints_refs:
                      - docs/architecture/constraints.md#governance
                    source_claims:
                      - CLM-20260001
                    review_by: 2026-06-30
                    ---

                    # ADR-0001: Valid ADR
                    """
                ),
                encoding="utf-8",
            )

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPTS / "build_adr_registry.py"),
                    "--repo-root",
                    str(tmp_path),
                    "--adr-dir",
                    "docs/adr",
                    "--output",
                    "docs/adr/registry.json",
                    "--strict",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            registry = json.loads((tmp_path / "docs" / "adr" / "registry.json").read_text(encoding="utf-8"))
            self.assertEqual(registry["schemaVersion"], "1")
            self.assertEqual(len(registry["entries"]), 1)

    def test_build_adr_registry_fails_with_missing_required_front_matter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            adr_dir = tmp_path / "docs" / "adr"
            adr_dir.mkdir(parents=True, exist_ok=True)

            (adr_dir / "0001-invalid-governance.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    id: ADR-0001
                    title: Invalid ADR
                    status: accepted
                    date: 2026-03-04
                    supersedes: []
                    tags:
                      - governance
                    paths:
                      - src/auth/**
                    constraints_refs:
                      - docs/architecture/constraints.md#governance
                    source_claims:
                      - CLM-20260001
                    ---

                    # ADR-0001: Invalid ADR
                    """
                ),
                encoding="utf-8",
            )

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPTS / "build_adr_registry.py"),
                    "--repo-root",
                    str(tmp_path),
                    "--adr-dir",
                    "docs/adr",
                    "--output",
                    "docs/adr/registry.json",
                    "--strict",
                ]
            )

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)

    def test_check_adr_gate_blocks_high_risk_change_without_alignment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changed = tmp_path / "changed-files.txt"
            high_risk = tmp_path / "high-risk-paths.yaml"
            registry = tmp_path / "registry.json"
            waivers = tmp_path / "waivers.json"

            changed.write_text("src/auth/session.ts\n", encoding="utf-8")
            high_risk.write_text(
                "version: 1\nupdated_at: 2026-03-04\nhigh_risk_paths:\n  - 'src/auth/**'\n",
                encoding="utf-8",
            )
            registry.write_text(
                json.dumps({"schemaVersion": "1", "generatedAt": "2026-03-04T09:00:00Z", "entries": []}),
                encoding="utf-8",
            )
            waivers.write_text("[]", encoding="utf-8")

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPTS / "check_adr_gate.py"),
                    "--gate",
                    "merge",
                    "--changed-files-file",
                    str(changed),
                    "--high-risk-config",
                    str(high_risk),
                    "--adr-registry",
                    str(registry),
                    "--waivers",
                    str(waivers),
                ]
            )

            self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)

    def test_check_adr_gate_passes_with_high_risk_change_and_adr_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changed = tmp_path / "changed-files.txt"
            high_risk = tmp_path / "high-risk-paths.yaml"
            registry = tmp_path / "registry.json"
            waivers = tmp_path / "waivers.json"

            changed.write_text("src/auth/session.ts\ndocs/adr/0001-auth-boundary.md\n", encoding="utf-8")
            high_risk.write_text(
                "version: 1\nupdated_at: 2026-03-04\nhigh_risk_paths:\n  - 'src/auth/**'\n",
                encoding="utf-8",
            )
            registry.write_text(
                json.dumps(
                    {
                        "schemaVersion": "1",
                        "generatedAt": "2026-03-04T09:00:00Z",
                        "entries": [
                            {
                                "id": "ADR-0001",
                                "title": "Auth boundary",
                                "status": "accepted",
                                "date": "2026-03-04",
                                "supersedes": [],
                                "tags": ["governance"],
                                "paths": ["src/auth/**"],
                                "constraintsRefs": ["docs/architecture/constraints.md#governance"],
                                "sourceClaims": ["CLM-20260001"],
                                "reviewBy": "2026-06-30",
                                "adrPath": "docs/adr/0001-auth-boundary.md",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            waivers.write_text("[]", encoding="utf-8")

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPTS / "check_adr_gate.py"),
                    "--gate",
                    "merge",
                    "--changed-files-file",
                    str(changed),
                    "--high-risk-config",
                    str(high_risk),
                    "--adr-registry",
                    str(registry),
                    "--waivers",
                    str(waivers),
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_check_claim_register_pass_blocked_and_fail(self) -> None:
        pass_case = FIXTURES / "claims" / "pass_claim_register.json"
        blocked_case = FIXTURES / "claims" / "blocked_claim_register.json"
        fail_case = FIXTURES / "claims" / "fail_claim_register.json"

        pass_result = run_cmd(
            [PYTHON_BIN, str(SCRIPTS / "check_claim_register.py"), "--claim-register", str(pass_case)]
        )
        blocked_result = run_cmd(
            [PYTHON_BIN, str(SCRIPTS / "check_claim_register.py"), "--claim-register", str(blocked_case)]
        )
        fail_result = run_cmd(
            [PYTHON_BIN, str(SCRIPTS / "check_claim_register.py"), "--claim-register", str(fail_case)]
        )

        self.assertEqual(pass_result.returncode, 0, msg=pass_result.stdout + pass_result.stderr)
        self.assertEqual(blocked_result.returncode, 2, msg=blocked_result.stdout + blocked_result.stderr)
        self.assertEqual(fail_result.returncode, 1, msg=fail_result.stdout + fail_result.stderr)

    def test_check_test_signal_passes_and_fails_expected_cases(self) -> None:
        good_test = FIXTURES / "test_signal" / "good_behavior.test.ts"
        bad_test = FIXTURES / "test_signal" / "bad_type_signal.test.ts"

        good_result = run_cmd(
            [
                PYTHON_BIN,
                str(SCRIPTS / "check_test_signal.py"),
                "--path",
                str(good_test),
                "--language",
                "auto",
                "--strict",
            ]
        )

        bad_result = run_cmd(
            [
                PYTHON_BIN,
                str(SCRIPTS / "check_test_signal.py"),
                "--path",
                str(bad_test),
                "--language",
                "auto",
                "--strict",
            ]
        )

        self.assertEqual(good_result.returncode, 0, msg=good_result.stdout + good_result.stderr)
        self.assertEqual(bad_result.returncode, 1, msg=bad_result.stdout + bad_result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

