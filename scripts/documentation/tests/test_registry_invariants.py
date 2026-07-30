"""Tests for registry identity, path, and canonicality invariants."""

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    config,
    registry as registry_module,
    reporter as reporter_module,
)


class RegistryInvariantTests(unittest.TestCase):
    def test_duplicate_document_version_fails(self) -> None:
        reporter = reporter_module.Reporter()

        registry_module.validate_uniqueness(
            [("DOC-1", "1.0.0"), ("DOC-1", "1.0.0")],
            ["docs/one.md", "docs/two.md"],
            reporter,
        )

        self.assertTrue(
            any("duplicate (document_id, version)" in error for error in reporter.errors)
        )

    def test_two_distinct_versions_are_accepted(self) -> None:
        reporter = reporter_module.Reporter()

        registry_module.validate_uniqueness(
            [("DOC-1", "1.0.0"), ("DOC-1", "2.0.0")],
            ["docs/one.md", "docs/two.md"],
            reporter,
        )

        self.assertEqual([], reporter.errors)

    def test_duplicate_path_casefold_fails(self) -> None:
        reporter = reporter_module.Reporter()

        registry_module.validate_uniqueness(
            [("DOC-1", "1.0.0"), ("DOC-2", "1.0.0")],
            ["docs/Test.md", "docs/test.md"],
            reporter,
        )

        self.assertTrue(
            any("case-insensitive path collision" in error for error in reporter.errors)
        )

    def _validate_record(
        self,
        overrides: validator.JsonObject,
    ) -> reporter_module.Reporter:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative_path = "docs/evidence/test-document.md"
            path = root / relative_path
            path.parent.mkdir(parents=True)
            content = b"# controlled\n"
            path.write_bytes(content)
            record: validator.JsonObject = {
                "document_id": "DOC-TEST",
                "title": "Test document",
                "document_type": "evidencia",
                "version": "1.0.0",
                "registration_status": "ATIVO_CONTROLADO",
                "workflow_status": "RASCUNHO",
                "legacy_declared_status": None,
                "current_path": relative_path,
                "target_path": relative_path,
                "canonical_path": None,
                "content_hash": hashlib.sha256(content).hexdigest(),
                "self_hash_exempt": False,
                "naming_conformance": True,
                "directory_conformance": True,
                "migration_required": False,
                "authority_scope": {},
                "relationships": {},
            }
            record.update(overrides)
            reporter = reporter_module.Reporter()
            with patch.object(config, "WORKSPACE_ROOT", root):
                registry_module.validate_record(record, reporter, False)
            return reporter

    def test_self_hash_exemption_outside_registry_fails(self) -> None:
        reporter = self._validate_record({"self_hash_exempt": True})

        self.assertTrue(
            any("self_hash_exempt is restricted" in error for error in reporter.errors)
        )

    def test_canonical_path_must_equal_current_path(self) -> None:
        reporter = self._validate_record(
            {
                "workflow_status": "CANONICA_VIGENTE",
                "canonical_path": "docs/evidence/another-document.md",
            }
        )

        self.assertTrue(
            any("canonical paths must be identical" in error for error in reporter.errors)
        )

    def test_terminal_document_preserves_historical_canonical_path(self) -> None:
        reporter = self._validate_record(
            {
                "workflow_status": "SUPERADA",
                "canonical_path": "docs/canonical/historical-document.md",
            }
        )

        self.assertEqual([], reporter.errors)


if __name__ == "__main__":
    unittest.main()
