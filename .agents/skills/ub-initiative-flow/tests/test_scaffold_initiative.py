from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SCRIPT = PROJECT_ROOT / ".agents" / "skills" / "ub-initiative-flow" / "scripts" / "scaffold_initiative.py"
PYTHON_BIN = sys.executable


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


class ScaffoldInitiativeScriptTests(unittest.TestCase):
    def test_scaffold_copies_template_and_renders_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "2026-04-01-my-new-initiative"

            result = run_cmd([PYTHON_BIN, str(SCRIPT), str(target)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((target / "README.md").exists())
            self.assertTrue((target / "roadmap.md").exists())
            self.assertTrue((target / "sprint-template" / "sprint.md").exists())

            readme = (target / "README.md").read_text(encoding="utf-8")
            roadmap = (target / "roadmap.md").read_text(encoding="utf-8")

            self.assertIn("My New Initiative", readme)
            self.assertIn("discovery-and-research", readme)
            self.assertIn("blocked", readme)
            self.assertIn("adapt-the-scaffold-and-replace-the-prd-placeholders", roadmap)
            self.assertIn(
                "replace-prd-placeholders-then-generate-the-final-roadmap-and-sprint-set",
                roadmap,
            )
            self.assertIn("REPLACE_OWNER", readme)

    def test_optional_fields_are_rendered_when_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "initiative-root"

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    str(target),
                    "--initiative-name",
                    "Parser Modernization",
                    "--owner",
                    "Platform Team",
                    "--validation-commands",
                    "python -m pytest tests/engine/ -v",
                    "--evidence-pointers",
                    "./sprints/01-discovery/evidence/",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

            readme = (target / "README.md").read_text(encoding="utf-8")

            self.assertIn("Parser Modernization", readme)
            self.assertIn("Platform Team", readme)
            self.assertIn("python -m pytest tests/engine/ -v", readme)
            self.assertIn("./sprints/01-discovery/evidence/", readme)

    def test_script_blocks_rerun_against_populated_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing-initiative"
            target.mkdir(parents=True, exist_ok=True)
            (target / "README.md").write_text("existing", encoding="utf-8")

            result = run_cmd([PYTHON_BIN, str(SCRIPT), str(target)])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("already contains files", result.stderr)
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "existing")

    def test_script_allows_existing_empty_target_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "empty-initiative"
            target.mkdir(parents=True, exist_ok=True)

            result = run_cmd([PYTHON_BIN, str(SCRIPT), str(target)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((target / "README.md").exists())

    def test_dry_run_reports_without_writing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "dry-run-initiative"

            result = run_cmd([PYTHON_BIN, str(SCRIPT), str(target), "--dry-run"])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("dry-run: scaffold would be copied", result.stdout)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)