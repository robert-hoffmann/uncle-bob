from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


def find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "pyproject.toml").exists() and (candidate / ".agents").exists():
            return candidate
    msg = "Could not locate repository root for governance tests"
    raise RuntimeError(msg)


PROJECT_ROOT = find_repo_root()
SKILL_ROOT = PROJECT_ROOT / ".agents" / "skills" / "ub-governance"
SCRIPTS = PROJECT_ROOT / ".agents" / "skills" / "ub-governance" / "scripts"
PYTHON_BIN = sys.executable
FIXTURES = Path(__file__).resolve().parent / "fixtures"
REPO_INTEGRITY_FIXTURES = FIXTURES / "repo_integrity"
EXPECTED_FIXTURE_SKILLS = ["alpha-skill", "beta-skill"]
EXPECTED_FIXTURE_AGENTS = ["alpha-agent", "beta-agent"]


def write_repo_integrity_fixture(repo_root: Path, fixture_name: str) -> None:
    fixture_root = REPO_INTEGRITY_FIXTURES / fixture_name
    for source in fixture_root.rglob("*"):
        if source.is_dir():
            continue
        destination = repo_root / source.relative_to(fixture_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


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

    def test_check_repo_catalog_passes_and_ignores_tmp_noise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "pass")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_repo_catalog.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["skills"]["disk"], EXPECTED_FIXTURE_SKILLS)
            self.assertEqual(payload["agents"]["disk"], EXPECTED_FIXTURE_AGENTS)

    def test_check_repo_catalog_fails_when_readme_inventory_drifts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "fail-readme-agent-drift")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_repo_catalog.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn("README.md agents table does not match disk agents", "\n".join(payload["errors"]))

    def test_check_package_metadata_passes_with_aligned_versions_and_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "pass")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_package_metadata.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["versions"]["pyproject"], "1.0.0")

    def test_check_package_metadata_fails_with_version_and_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "fail-package-metadata-drift")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_package_metadata.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            error_text = "\n".join(payload["errors"])
            self.assertIn("Version mismatch", error_text)
            self.assertIn("Marketplace description claims 99 skills", error_text)

    def test_check_repo_paths_passes_with_exact_case_and_ignores_tmp_noise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "pass")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_repo_paths.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")

    def test_check_repo_paths_fails_for_legacy_root_registry_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "fail-legacy-root-registry")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_repo_paths.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            error_text = "\n".join(payload["errors"])
            self.assertIn("Canonical path missing or mis-cased: AGENTS.md", error_text)
            self.assertIn("Legacy path must not exist: AGENTS.MD", error_text)

    def test_check_skill_schema_passes_with_valid_frontmatter_and_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "pass")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_skill_schema.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["checkedSkills"], EXPECTED_FIXTURE_SKILLS)

    def test_check_skill_schema_fails_with_invalid_frontmatter_and_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_repo_integrity_fixture(repo_root, "fail-skill-schema")

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPTS / "check_skill_schema.py"), "--repo-root", str(repo_root)]
            )

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            error_text = "\n".join(payload["errors"])
            self.assertIn("alpha-skill: SKILL.md must start with valid YAML frontmatter", error_text)
            self.assertIn("beta-skill: unresolved local reference 'references/missing.md'", error_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

