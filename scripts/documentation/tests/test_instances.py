"""Tests for the instance-validation units extracted from the orchestrator."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    config,
    contracts as contracts_module,
    reporter as reporter_module,
    workflow as workflow_module,
)


class InstanceValidationTests(unittest.TestCase):
    def test_invalid_document_instance_fails(self) -> None:
        reporter = reporter_module.Reporter()

        validator.validate_document_instances(
            [{"document_id": "DOC-INCOMPLETE"}],
            reporter,
        )

        self.assertTrue(
            any("document contract failure" in error for error in reporter.errors)
        )

    def test_invalid_workflow_instance_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workflow_path = Path(directory) / "workflow.yaml"
            workflow_path.write_text("{}\n", encoding="utf-8")
            reporter = reporter_module.Reporter()
            with patch.object(
                config,
                "DEFAULT_WORKFLOW",
                workflow_path,
            ):
                validator.validate_workflow_instance(reporter)

        self.assertTrue(
            any("workflow contract failure" in error for error in reporter.errors)
        )

    def test_invalid_gate_result_instance_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gate_root = root / "docs/evidence/gates"
            gate_root.mkdir(parents=True)
            (gate_root / "invalid.yaml").write_text(
                "gate_result:\n  gate_id: G1\n",
                encoding="utf-8",
            )
            reporter = reporter_module.Reporter()
            with patch.object(config, "WORKSPACE_ROOT", root):
                validator.validate_gate_result_instances(reporter)

        self.assertTrue(
            any("gate result contract failure" in error for error in reporter.errors)
        )
        self.assertTrue(any("invalid.yaml" in error for error in reporter.errors))

    def test_schema_valid_but_unknown_reference_still_fails(self) -> None:
        raw_workflow = yaml.safe_load(
            config.DEFAULT_WORKFLOW.read_text(encoding="utf-8")
        )
        workflow = validator.as_json_object(raw_workflow)
        self.assertIsNotNone(workflow)
        transitions = validator.as_json_array(
            (workflow or {}).get("transitions")
        )
        self.assertTrue(transitions)
        transition = validator.as_json_object((transitions or [None])[0])
        self.assertIsNotNone(transition)
        (transition or {})["required_gates"] = ["G-UNKNOWN"]

        schema = validator.as_json_object(
            contracts_module.load_json(
                config.WORKFLOW_SCHEMA,
                reporter_module.Reporter(),
            )
        )
        self.assertIsNotNone(schema)
        schema_errors = contracts_module.schema_validation_errors(
            schema or {},
            workflow,
        )
        reporter = reporter_module.Reporter()
        workflow_module.validate_workflow_references(workflow or {}, reporter)

        self.assertEqual([], schema_errors)
        self.assertTrue(
            any("unknown required gate" in error for error in reporter.errors)
        )


if __name__ == "__main__":
    unittest.main()
