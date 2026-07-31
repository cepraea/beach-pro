"""Tests for workflow references and immutable ingestion snapshots."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    config,
    ingestion as ingestion_module,
    reporter as reporter_module,
    workflow as workflow_module,
)


def _workflow() -> validator.JsonObject:
    gates: list[validator.JsonObject] = [
        {
            "gate_id": gate_id,
            "implementation_status": "IMPLEMENTED",
            "blocking": True,
            "evaluator": {"command": f"validate --gate {gate_id}"},
        }
        for gate_id in ("G-ARCH", "G0", "G1")
    ]
    return {
        "workflow": {
            "initial_state": "S0",
            "successful_terminal_state": "S1",
            "owner_role": "OWNER",
            "approval_authority_role": "OWNER",
            "canonization_authority_role": "OWNER",
        },
        "states": [{"state_id": "S0"}, {"state_id": "S1"}],
        "roles": [{"role_id": "OWNER"}],
        "gates": gates,
        "contracts": [],
        "transitions": [
            {
                "transition_id": "T1",
                "from_state": "S0",
                "to_state": "S1",
                "authorized_roles": ["OWNER"],
                "required_gates": ["G0"],
                "required_contracts": [],
            }
        ],
        "initialization": {
            "authorized_roles": ["OWNER"],
            "required_gates": ["G-ARCH"],
            "required_contracts": [],
        },
    }


class WorkflowReferenceTests(unittest.TestCase):
    def test_valid_workflow_resolves_all_references(self) -> None:
        reporter = reporter_module.Reporter()

        workflow_module.validate_workflow_references(_workflow(), reporter)

        self.assertEqual([], reporter.errors)

    def test_workflow_unknown_gate_reference_fails(self) -> None:
        workflow = _workflow()
        transitions = validator.as_json_array(workflow.get("transitions"))
        transition = validator.as_json_object((transitions or [None])[0])
        self.assertIsNotNone(transition)
        (transition or {})["required_gates"] = ["G-UNKNOWN"]
        reporter = reporter_module.Reporter()

        workflow_module.validate_workflow_references(workflow, reporter)

        self.assertTrue(
            any("unknown required gate" in error for error in reporter.errors)
        )

    def test_duplicate_workflow_identifier_fails(self) -> None:
        workflow = _workflow()
        states = validator.as_json_array(workflow.get("states"))
        self.assertIsNotNone(states)
        (states or []).append({"state_id": "S0"})
        reporter = reporter_module.Reporter()

        workflow_module.validate_workflow_references(workflow, reporter)

        self.assertIn("duplicate workflow state: S0", reporter.errors)


class IngestionConsistencyTests(unittest.TestCase):
    document_id = "DOC-INGESTED"
    event_id = "ING-001"
    snapshot_version = "1.0.0"
    snapshot_hash = "a" * 64

    def _run(
        self,
        record_version: str = snapshot_version,
        record_hash: str = snapshot_hash,
        event_gate_ids: list[str] | None = None,
    ) -> reporter_module.Reporter:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestion_root = root / "docs/evidence/ingestion"
            gate_root = root / "docs/evidence/gates"
            integrity_root = root / "docs/evidence/integrity"
            ingestion_root.mkdir(parents=True)
            gate_root.mkdir(parents=True)
            integrity_root.mkdir(parents=True)

            manifest_path = integrity_root / "manifest.yaml"
            manifest: validator.JsonObject = {
                "manifest_id": "MANIFEST-001",
                "documents": [
                    {
                        "document_id": self.document_id,
                        "version": self.snapshot_version,
                        "content_hash": self.snapshot_hash,
                    }
                ],
            }
            manifest_path.write_text(
                yaml.safe_dump(manifest),
                encoding="utf-8",
            )

            persisted_ids: list[str] = []
            for gate_id in ("G-ARCH", "G0", "G1"):
                result_id = f"GATE-RESULT-{gate_id}-INGESTION"
                persisted_ids.append(result_id)
                result: validator.JsonObject = {
                    "gate_result_id": result_id,
                    "gate_id": gate_id,
                    "status": "pass",
                }
                (gate_root / f"{gate_id}.yaml").write_text(
                    yaml.safe_dump({"gate_result": result}),
                    encoding="utf-8",
                )

            event: validator.JsonObject = {
                "event_id": self.event_id,
                "manifest_id": "MANIFEST-001",
                "documents": [
                    {
                        "document_id": self.document_id,
                        "version": self.snapshot_version,
                        "content_hash": self.snapshot_hash,
                    }
                ],
                "gate_result_ids": (
                    event_gate_ids
                    if event_gate_ids is not None
                    else persisted_ids
                ),
            }
            (ingestion_root / "event.yaml").write_text(
                yaml.safe_dump({"ingestion_event": event}),
                encoding="utf-8",
            )

            documents: list[validator.JsonObject] = [
                {
                    "document_id": self.document_id,
                    "version": record_version,
                    "content_hash": record_hash,
                    "relationships": {
                        "ingestion_event_id": [self.event_id]
                    },
                }
            ]
            reporter = reporter_module.Reporter()
            with (
                patch.object(config, "WORKSPACE_ROOT", root),
                patch.object(
                    config,
                    "INTEGRITY_MANIFEST",
                    manifest_path,
                ),
            ):
                ingestion_module.validate_ingestion_consistency(
                    documents,
                    reporter,
                )
            return reporter

    def test_ingestion_unknown_gate_result_fails(self) -> None:
        reporter = self._run(event_gate_ids=["GATE-RESULT-UNKNOWN"])

        self.assertTrue(
            any("unknown gate result" in error for error in reporter.errors)
        )

    def test_ingestion_snapshot_changed_same_version_fails(self) -> None:
        reporter = self._run(record_hash="b" * 64)

        self.assertTrue(any("hash differs" in error for error in reporter.errors))

    def test_later_revision_preserves_historical_snapshot(self) -> None:
        reporter = self._run(
            record_version="2.0.0",
            record_hash="b" * 64,
        )

        self.assertEqual([], reporter.errors)


if __name__ == "__main__":
    unittest.main()
