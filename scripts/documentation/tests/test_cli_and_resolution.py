"""Tests for CLI scope, version identity, and local-link boundaries."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.documentation import validate_documentation as validator


def _args(**overrides: object) -> validator.ValidatorArgs:
    args = validator.ValidatorArgs()
    args.registry = validator.DEFAULT_REGISTRY
    args.strict_legacy = False
    args.gate = None
    args.document_id = None
    args.version = None
    args.format = "text"
    args.result_id = None
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


class CliScopeTests(unittest.TestCase):
    def test_version_without_document_id_is_rejected(self) -> None:
        reporter = validator.Reporter()

        accepted = validator.validate_cli_args(
            _args(gate="G2", version="0.1.2"),
            reporter,
        )

        self.assertFalse(accepted)
        self.assertIn("--version requires --document-id", reporter.errors)

    def test_global_gate_rejects_document_scope(self) -> None:
        reporter = validator.Reporter()

        accepted = validator.validate_cli_args(
            _args(gate="G0", document_id="DOC-1"),
            reporter,
        )

        self.assertFalse(accepted)
        self.assertTrue(
            any("global" in message for message in reporter.errors)
        )


class DocumentResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents: list[validator.JsonObject] = [
            {
                "document_id": "DOC-1",
                "version": "0.1.1",
                "content_hash": "a" * 64,
            },
            {
                "document_id": "DOC-1",
                "version": "0.1.2",
                "content_hash": "b" * 64,
            },
        ]

    def test_resolver_does_not_return_first_version(self) -> None:
        reporter = validator.Reporter()

        selected = validator.resolve_document_version(
            self.documents,
            "DOC-1",
            "0.1.2",
            reporter,
        )

        self.assertIsNotNone(selected)
        self.assertEqual("0.1.2", reporter.version)
        self.assertEqual("b" * 64, reporter.content_hash)

    def test_resolver_rejects_unknown_version(self) -> None:
        reporter = validator.Reporter()

        selected = validator.resolve_document_version(
            self.documents,
            "DOC-1",
            "9.9.9",
            reporter,
        )

        self.assertIsNone(selected)
        self.assertIsNone(reporter.version)
        self.assertTrue(reporter.errors)

    def test_resolver_rejects_ambiguous_id(self) -> None:
        reporter = validator.Reporter()

        selected = validator.resolve_document_version(
            self.documents,
            "DOC-1",
            None,
            reporter,
        )

        self.assertIsNone(selected)
        self.assertTrue(
            any("--version is required" in error for error in reporter.errors)
        )


class LinkBoundaryTests(unittest.TestCase):
    def _validate(self, markdown: str, existing: str | None = None) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "source.md").write_text(markdown, encoding="utf-8")
            if existing is not None:
                (docs / existing).write_text("# target\n", encoding="utf-8")
            reporter = validator.Reporter()
            with patch.object(validator, "WORKSPACE_ROOT", root):
                validator.validate_links(reporter)
            return reporter.errors

    def test_markdown_link_cannot_escape_workspace(self) -> None:
        errors = self._validate("[outside](../../outside.md)")

        self.assertTrue(any("escapes workspace" in error for error in errors))

    def test_absolute_external_path_is_rejected(self) -> None:
        errors = self._validate("[outside](/etc/passwd)")

        self.assertTrue(any("escapes workspace" in error for error in errors))

    def test_existing_internal_line_reference_passes(self) -> None:
        errors = self._validate("[target](target.md:12)", "target.md")

        self.assertEqual([], errors)

    def test_broken_internal_link_fails(self) -> None:
        errors = self._validate("[missing](missing.md)")

        self.assertTrue(any("broken local link" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
