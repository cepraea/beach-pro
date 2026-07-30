"""Tests for exact version selection in document-scoped gates."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.documentation import validate_documentation as validator


class FrontMatterScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents: list[validator.JsonObject] = [
            {
                "document_id": "DOC-FM",
                "version": "1.0.0",
                "content_hash": "a" * 64,
                "current_path": "docs/controlled/first.md",
            },
            {
                "document_id": "DOC-FM",
                "version": "2.0.0",
                "content_hash": "b" * 64,
                "current_path": "docs/controlled/second.md",
            },
        ]

    def test_scoped_front_matter_unknown_version_fails(self) -> None:
        reporter = validator.Reporter()

        validator.validate_front_matter(
            self.documents,
            reporter,
            "DOC-FM",
            "9.0.0",
        )

        self.assertTrue(
            any("unknown document version" in error for error in reporter.errors)
        )

    def test_scoped_front_matter_ambiguous_version_fails(self) -> None:
        reporter = validator.Reporter()

        validator.validate_front_matter(
            self.documents,
            reporter,
            "DOC-FM",
        )

        self.assertTrue(
            any("--version is required" in error for error in reporter.errors)
        )


class ProvenanceScopeTests(unittest.TestCase):
    document_id = "DOC-G2"
    version = "1.0.0"
    content_hash = "a" * 64

    def _run(
        self,
        package_hash: str | None = None,
        sources: list[validator.JsonObject] | None = None,
        claims: list[validator.JsonObject] | None = None,
        coverage: int = 0,
    ) -> validator.Reporter:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            provenance_root = root / "docs/evidence/provenance"
            provenance_root.mkdir(parents=True)
            package: validator.JsonObject = {
                "provenance_id": "PROV-G2-001",
                "document_id": self.document_id,
                "document_version": self.version,
                "document_hash": package_hash or self.content_hash,
                "sources": sources or [],
                "claims": claims or [],
                "policy": {
                    "require_active_sources": True,
                    "reject_ambiguous_references": True,
                    "critical_coverage_percent": coverage,
                },
            }
            (provenance_root / "package.yaml").write_text(
                yaml.safe_dump({"provenance_package": package}),
                encoding="utf-8",
            )
            documents: list[validator.JsonObject] = [
                {
                    "document_id": self.document_id,
                    "version": self.version,
                    "content_hash": self.content_hash,
                },
                {
                    "document_id": self.document_id,
                    "version": "2.0.0",
                    "content_hash": "b" * 64,
                },
            ]
            reporter = validator.Reporter()
            with patch.object(validator, "WORKSPACE_ROOT", root):
                validator.validate_g2(
                    documents,
                    reporter,
                    self.document_id,
                    self.version,
                )
            return reporter

    def test_g2_does_not_overwrite_versions_by_document_id(self) -> None:
        reporter = self._run()

        self.assertEqual([], reporter.errors)
        self.assertEqual(self.version, reporter.version)
        self.assertEqual(self.content_hash, reporter.content_hash)

    def test_g2_package_hash_mismatch_fails(self) -> None:
        reporter = self._run(package_hash="f" * 64)

        self.assertTrue(
            any("document hash differs" in error for error in reporter.errors)
        )

    def test_g2_archive_escape_fails(self) -> None:
        source_hash = "c" * 64
        sources: list[validator.JsonObject] = [
            {
                "source_id": "SRC-001",
                "status": "active",
                "location": "../outside.tar#member.md",
                "immutable_reference": f"sha256:{source_hash}",
                "content_hash": source_hash,
                "verified_at": "2026-07-29T00:00:00Z",
                "verified_by": "AUTOMACAO",
                "authority": {"scope": ["subject"]},
            }
        ]
        claims: list[validator.JsonObject] = [
            {
                "claim_id": "CLM-001",
                "criticality": "critical",
                "document_id": self.document_id,
                "document_version": self.version,
                "document_hash": self.content_hash,
                "source_ids": ["SRC-001"],
                "subjects": ["subject"],
                "source_reference_text": "SRC-001",
            }
        ]

        reporter = self._run(
            sources=sources,
            claims=claims,
            coverage=100,
        )

        self.assertTrue(
            any("archive escapes workspace" in error for error in reporter.errors)
        )


if __name__ == "__main__":
    unittest.main()
