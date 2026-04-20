from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


def find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "pyproject.toml").exists() and (candidate / ".agents").exists():
            return candidate
    msg = "Could not locate repository root for repo-maintenance tests"
    raise RuntimeError(msg)


PROJECT_ROOT = find_repo_root()
SCRIPTS = PROJECT_ROOT / "scripts" / "repo-maintenance"
PYTHON_BIN = sys.executable
FIXTURES = PROJECT_ROOT / "tests" / "skills" / "ub-governance" / "fixtures"
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


class RepoMaintenanceScriptRegressionTests(unittest.TestCase):
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
