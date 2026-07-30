"""Integration test for the validator against the repository evidence."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MODULE_NAME = "scripts.documentation.validate_documentation"


class RepositoryEntrypointIntegrationTests(unittest.TestCase):
    """Exercise G-ARCH with the ignored TAR packages materialized."""

    def test_garch_entrypoint_operates_against_repository(self) -> None:
        # Missing TARs must fail instead of skipping: their verified presence is
        # the operational precondition that distinguishes integration from unit.
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                MODULE_NAME,
                "--gate",
                "G-ARCH",
                "--format",
                "text",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual("SUMMARY: errors=0 warnings=0\n", result.stdout)
        self.assertEqual("", result.stderr)


if __name__ == "__main__":
    unittest.main()
