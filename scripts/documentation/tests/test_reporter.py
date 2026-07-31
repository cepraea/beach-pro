"""Tests for the validator's single output boundary."""

import io
import unittest
from contextlib import redirect_stdout

import yaml

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    config,
    contracts as contracts_module,
    reporter as reporter_module,
)


class ReporterTests(unittest.TestCase):
    def _emit_yaml(
        self,
        reporter: reporter_module.Reporter,
        result_id: str | None = None,
    ) -> validator.JsonObject:
        output = io.StringIO()
        with redirect_stdout(output):
            status = reporter.emit("yaml", "G1", result_id)
        self.assertEqual(1 if reporter.errors else 0, status)
        payload = validator.as_json_object(yaml.safe_load(output.getvalue()))
        self.assertIsNotNone(payload)
        return payload or {}

    def test_yaml_result_matches_gate_result_schema(self) -> None:
        reporter = reporter_module.Reporter()
        reporter.document_id = "DOC-TESTE"
        reporter.version = "0.1.0"
        reporter.content_hash = "a" * 64

        payload = self._emit_yaml(
            reporter,
            "GATE-RESULT-G1-TESTE-001",
        )
        schema = validator.as_json_object(
            contracts_module.load_json(
                config.GATE_RESULT_SCHEMA,
                reporter_module.Reporter(),
            )
        )
        self.assertIsNotNone(schema)
        gate_result = payload.get("gate_result")
        errors = contracts_module.schema_validation_errors(
            schema or {},
            gate_result,
        )

        self.assertEqual([], errors)

    def test_explicit_result_id_replaces_runtime_identity(self) -> None:
        payload = self._emit_yaml(
            reporter_module.Reporter(),
            "GATE-RESULT-G1-AUDITORIA-001",
        )
        gate_result = validator.as_json_object(payload.get("gate_result"))

        self.assertIsNotNone(gate_result)
        self.assertEqual(
            "GATE-RESULT-G1-AUDITORIA-001",
            (gate_result or {}).get("gate_result_id"),
        )

    def test_failure_returns_nonzero_and_sorted_failures(self) -> None:
        reporter = reporter_module.Reporter()
        reporter.error("zeta")
        reporter.error("alfa")

        payload = self._emit_yaml(reporter)
        gate_result = validator.as_json_object(payload.get("gate_result"))

        self.assertEqual(
            ["alfa", "zeta"],
            (gate_result or {}).get("failures"),
        )


if __name__ == "__main__":
    unittest.main()
