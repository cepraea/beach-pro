"""Tests for fail-fast stage orchestration and gate dispatch."""

import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    contracts as contracts_module,
    instances as instances_module,
    links as links_module,
    registry as registry_module,
    reporter as reporter_module,
)


def _args(
    gate: str | None = None,
    document_id: str | None = None,
    version: str | None = None,
) -> validator.ValidatorArgs:
    args = validator.ValidatorArgs()
    args.registry = Path("/controlled/registry.yaml")
    args.strict_legacy = False
    args.gate = gate
    args.document_id = document_id
    args.version = version
    args.format = "text"
    args.result_id = None
    return args


def _registry_data() -> validator.JsonObject:
    return {
        "schema_version": "1.0.0",
        "registry": {"canonical_documents": []},
        "documents": [],
    }


class MainPipelineTests(unittest.TestCase):
    def test_main_stops_before_files_when_contract_stage_fails(self) -> None:
        def fail_contract(reporter: reporter_module.Reporter) -> None:
            reporter.error("contract stage failed")

        with (
            patch.object(validator, "parse_args", return_value=_args()),
            patch.object(
                registry_module,
                "load_registry",
                return_value=(_registry_data(), []),
            ),
            patch.object(
                contracts_module,
                "validate_contract_schemas",
                side_effect=fail_contract,
            ),
            patch.object(instances_module, "validate_instances"),
            patch.object(
                registry_module,
                "validate_registry_integrity",
            ) as registry_stage,
            patch.object(reporter_module.Reporter, "emit", return_value=1) as emit,
        ):
            status = validator.main()

        self.assertEqual(1, status)
        registry_stage.assert_not_called()
        emit.assert_called_once()

    def test_main_stops_before_gate_when_registry_stage_fails(self) -> None:
        def fail_registry(
            documents: list[validator.JsonObject],
            reporter: reporter_module.Reporter,
            strict_legacy: bool,
        ) -> None:
            del documents, strict_legacy
            reporter.error("registry stage failed")

        with (
            patch.object(validator, "parse_args", return_value=_args("G1")),
            patch.object(
                registry_module,
                "load_registry",
                return_value=(_registry_data(), []),
            ),
            patch.object(contracts_module, "validate_contract_schemas"),
            patch.object(instances_module, "validate_instances"),
            patch.object(
                registry_module,
                "validate_registry_integrity",
                side_effect=fail_registry,
            ),
            patch.object(
                validator,
                "dispatch_gate",
            ) as gate_stage,
            patch.object(reporter_module.Reporter, "emit", return_value=1),
        ):
            status = validator.main()

        self.assertEqual(1, status)
        gate_stage.assert_not_called()

    def test_main_stops_before_links_when_gate_fails(self) -> None:
        def fail_gate(
            args: validator.ValidatorArgs,
            documents: list[validator.JsonObject],
            reporter: reporter_module.Reporter,
        ) -> None:
            del args, documents
            reporter.error("gate failed")

        with (
            patch.object(validator, "parse_args", return_value=_args("G1")),
            patch.object(
                registry_module,
                "load_registry",
                return_value=(_registry_data(), []),
            ),
            patch.object(contracts_module, "validate_contract_schemas"),
            patch.object(instances_module, "validate_instances"),
            patch.object(registry_module, "validate_registry_integrity"),
            patch.object(registry_module, "validate_canonical_registry"),
            patch.object(
                validator,
                "dispatch_gate",
                side_effect=fail_gate,
            ),
            patch.object(links_module, "validate_links") as link_stage,
            patch.object(reporter_module.Reporter, "emit", return_value=1),
        ):
            status = validator.main()

        self.assertEqual(1, status)
        link_stage.assert_not_called()

    def test_main_uses_exact_scoped_record(self) -> None:
        documents: list[validator.JsonObject] = [
            {
                "document_id": "DOC-1",
                "version": "1.0.0",
                "content_hash": "a" * 64,
            },
            {
                "document_id": "DOC-1",
                "version": "2.0.0",
                "content_hash": "b" * 64,
            },
        ]
        observed: validator.JsonObject = {}

        def capture_gate(
            args: validator.ValidatorArgs,
            records: list[validator.JsonObject],
            reporter: reporter_module.Reporter,
        ) -> None:
            del args, records
            observed["version"] = reporter.version
            observed["content_hash"] = reporter.content_hash

        with (
            patch.object(
                validator,
                "parse_args",
                return_value=_args("G2", "DOC-1", "2.0.0"),
            ),
            patch.object(
                registry_module,
                "load_registry",
                return_value=(_registry_data(), documents),
            ),
            patch.object(contracts_module, "validate_contract_schemas"),
            patch.object(instances_module, "validate_instances"),
            patch.object(registry_module, "validate_registry_integrity"),
            patch.object(registry_module, "validate_canonical_registry"),
            patch.object(
                validator,
                "dispatch_gate",
                side_effect=capture_gate,
            ),
            patch.object(links_module, "validate_links"),
            patch.object(reporter_module.Reporter, "emit", return_value=0) as emit,
        ):
            status = validator.main()

        self.assertEqual(0, status)
        self.assertEqual("2.0.0", observed.get("version"))
        self.assertEqual("b" * 64, observed.get("content_hash"))
        emit.assert_called_once()

    def test_global_gate_emits_null_document_metadata(self) -> None:
        observed: validator.JsonObject = {}

        def capture_emit(
            reporter: reporter_module.Reporter,
            output_format: str,
            gate_id: str | None,
            result_id: str | None,
        ) -> int:
            del output_format, gate_id, result_id
            observed["document_id"] = reporter.document_id
            observed["version"] = reporter.version
            observed["content_hash"] = reporter.content_hash
            return 0

        with (
            patch.object(validator, "parse_args", return_value=_args("G1")),
            patch.object(
                registry_module,
                "load_registry",
                return_value=(_registry_data(), []),
            ),
            patch.object(contracts_module, "validate_contract_schemas"),
            patch.object(instances_module, "validate_instances"),
            patch.object(registry_module, "validate_registry_integrity"),
            patch.object(registry_module, "validate_canonical_registry"),
            patch.object(validator, "dispatch_gate"),
            patch.object(links_module, "validate_links"),
            patch.object(
                reporter_module.Reporter,
                "emit",
                autospec=True,
                side_effect=capture_emit,
            ),
        ):
            status = validator.main()

        self.assertEqual(0, status)
        self.assertIsNone(observed.get("document_id"))
        self.assertIsNone(observed.get("version"))
        self.assertIsNone(observed.get("content_hash"))

    def test_garch_has_explicit_dispatch(self) -> None:
        args = _args("G-ARCH")
        reporter = reporter_module.Reporter()
        with patch.object(validator, "validate_garch") as garch:
            validator.dispatch_gate(args, [], reporter)

        garch.assert_called_once_with([], reporter)


if __name__ == "__main__":
    unittest.main()
