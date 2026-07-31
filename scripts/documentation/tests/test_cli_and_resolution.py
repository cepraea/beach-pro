"""Tests for CLI scope, version identity, and local-link boundaries."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    cli as cli_module,
    config,
    links as links_module,
    pipeline as pipeline_module,
    registry as registry_module,
    reporter as reporter_module,
)


def _args(**overrides: object) -> validator.ValidatorArgs:
    args = validator.ValidatorArgs()
    args.registry = config.DEFAULT_REGISTRY
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
    def test_parse_args_accepts_explicit_argv(self) -> None:
        args = cli_module.parse_args(["--gate", "G1", "--format", "yaml"])

        self.assertEqual("G1", args.gate)
        self.assertEqual("yaml", args.format)

    def test_main_accepts_explicit_argv_and_emits_once(self) -> None:
        with (
            patch.object(pipeline_module, "run_validation") as pipeline,
            patch.object(
                reporter_module.Reporter,
                "emit",
                return_value=0,
            ) as emit,
        ):
            status = cli_module.main(["--gate", "G1"])

        self.assertEqual(0, status)
        pipeline.assert_called_once()
        parsed_args = pipeline.call_args.args[0]
        self.assertEqual("G1", parsed_args.gate)
        emit.assert_called_once()

    def test_invalid_explicit_argv_skips_pipeline_and_emits_once(self) -> None:
        with (
            patch.object(pipeline_module, "run_validation") as pipeline,
            patch.object(
                reporter_module.Reporter,
                "emit",
                return_value=1,
            ) as emit,
        ):
            status = cli_module.main(["--version", "1.0.0"])

        self.assertEqual(1, status)
        pipeline.assert_not_called()
        emit.assert_called_once()

    def test_version_without_document_id_is_rejected(self) -> None:
        reporter = reporter_module.Reporter()

        accepted = cli_module.validate_cli_args(
            _args(gate="G2", version="0.1.2"),
            reporter,
        )

        self.assertFalse(accepted)
        self.assertIn("--version requires --document-id", reporter.errors)

    def test_global_gate_rejects_document_scope(self) -> None:
        reporter = reporter_module.Reporter()

        accepted = cli_module.validate_cli_args(
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
        reporter = reporter_module.Reporter()

        selected = registry_module.resolve_document_version(
            self.documents,
            "DOC-1",
            "0.1.2",
            reporter,
        )

        self.assertIsNotNone(selected)
        self.assertEqual("0.1.2", reporter.version)
        self.assertEqual("b" * 64, reporter.content_hash)

    def test_resolver_rejects_unknown_version(self) -> None:
        reporter = reporter_module.Reporter()

        selected = registry_module.resolve_document_version(
            self.documents,
            "DOC-1",
            "9.9.9",
            reporter,
        )

        self.assertIsNone(selected)
        self.assertIsNone(reporter.version)
        self.assertTrue(reporter.errors)

    def test_resolver_rejects_ambiguous_id(self) -> None:
        reporter = reporter_module.Reporter()

        selected = registry_module.resolve_document_version(
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
            reporter = reporter_module.Reporter()
            with patch.object(config, "WORKSPACE_ROOT", root):
                links_module.validate_links(reporter)
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

    def test_markdown_read_failure_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            source = docs / "source.md"
            source.write_text("# source\n", encoding="utf-8")
            reporter = reporter_module.Reporter()

            with (
                patch.object(config, "WORKSPACE_ROOT", root),
                patch.object(
                    Path,
                    "read_text",
                    side_effect=OSError("permission denied"),
                ),
            ):
                links_module.validate_links(reporter)

            self.assertTrue(
                any(
                    "docs/source.md" in error
                    and "cannot read Markdown" in error
                    and "permission denied" in error
                    for error in reporter.errors
                )
            )


if __name__ == "__main__":
    unittest.main()
