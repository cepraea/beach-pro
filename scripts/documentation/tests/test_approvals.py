"""Isolated tests for approval and gate-result cross-references."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import config


class ApprovalCrossReferenceTests(unittest.TestCase):
    document_id = "DOC-TARGET"
    version = "1.0.0"
    content_hash = "a" * 64
    approval_id = "APR-TARGET-001"
    required_gates = ("G-ARCH", "G0", "G1", "G-FM")

    def _run(
        self,
        approval_overrides: validator.JsonObject | None = None,
        gate_overrides: dict[str, validator.JsonObject] | None = None,
        artifact_relationships: validator.JsonObject | None = None,
        duplicate_gate_id: bool = False,
    ) -> validator.Reporter:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gate_root = root / "docs/evidence/gates"
            approval_root = root / "docs/evidence/approvals"
            gate_root.mkdir(parents=True)
            approval_root.mkdir(parents=True)

            evidence_ids: list[str] = []
            for index, gate_id in enumerate(self.required_gates):
                result_id = f"GATE-RESULT-{gate_id}-TARGET"
                evidence_ids.append(result_id)
                gate_result: validator.JsonObject = {
                    "gate_result_id": result_id,
                    "gate_id": gate_id,
                    "document_id": self.document_id,
                    "version": self.version,
                    "content_hash": self.content_hash,
                    "status": "pass",
                }
                if gate_overrides and gate_id in gate_overrides:
                    gate_result.update(gate_overrides[gate_id])
                (gate_root / f"gate-{index}.yaml").write_text(
                    yaml.safe_dump({"gate_result": gate_result}),
                    encoding="utf-8",
                )
            if duplicate_gate_id:
                duplicate: validator.JsonObject = {
                    "gate_result_id": evidence_ids[0],
                    "gate_id": "G-ARCH",
                    "document_id": self.document_id,
                    "version": self.version,
                    "content_hash": self.content_hash,
                    "status": "pass",
                }
                (gate_root / "gate-duplicate.yaml").write_text(
                    yaml.safe_dump({"gate_result": duplicate}),
                    encoding="utf-8",
                )

            approval: validator.JsonObject = {
                "approval_id": self.approval_id,
                "document_id": self.document_id,
                "version": self.version,
                "content_hash": self.content_hash,
                "evidence_ids": evidence_ids,
            }
            if approval_overrides:
                approval.update(approval_overrides)
            approval_path = approval_root / "approval.yaml"
            approval_path.write_text(
                yaml.safe_dump({"approval": approval}),
                encoding="utf-8",
            )

            target: validator.JsonObject = {
                "document_id": self.document_id,
                "version": self.version,
                "content_hash": self.content_hash,
                "workflow_status": "CANONICA_VIGENTE",
                "relationships": {"approval_id": [self.approval_id]},
            }
            artifact: validator.JsonObject = {
                "document_id": "DOC-APPROVAL",
                "version": "1.0.0",
                "content_hash": "b" * 64,
                "current_path": (
                    "docs/evidence/approvals/approval.yaml"
                ),
                "relationships": {"approves": [self.document_id]},
            }
            if artifact_relationships is not None:
                artifact["relationships"] = artifact_relationships

            documents = [target, artifact]
            if artifact_relationships and artifact_relationships.get(
                "superseded_by"
            ) == ["DOC-APPROVAL-NEW"]:
                documents.append(
                    {
                        "document_id": "DOC-APPROVAL-NEW",
                        "version": "1.0.0",
                        "content_hash": "c" * 64,
                    }
                )

            reporter = validator.Reporter()
            with patch.object(config, "WORKSPACE_ROOT", root):
                validator.validate_approval_cross_references(
                    documents,
                    reporter,
                )
            return reporter

    def test_valid_approval_with_four_exact_gates_passes(self) -> None:
        reporter = self._run()

        self.assertEqual([], reporter.errors)

    def test_approval_unknown_target_fails(self) -> None:
        reporter = self._run(
            {"document_id": "DOC-UNKNOWN"},
            artifact_relationships={"approves": ["DOC-UNKNOWN"]},
        )

        self.assertTrue(
            any("target is not registered" in error for error in reporter.errors)
        )

    def test_approval_hash_mismatch_fails(self) -> None:
        reporter = self._run({"content_hash": "f" * 64})

        self.assertTrue(any("hash" in error for error in reporter.errors))

    def test_missing_evidence_id_fails(self) -> None:
        reporter = self._run(
            {"evidence_ids": ["GATE-RESULT-G0-DOES-NOT-EXIST"]}
        )

        self.assertTrue(
            any("unknown gate result" in error for error in reporter.errors)
        )

    def test_duplicate_gate_result_id_fails(self) -> None:
        reporter = self._run(duplicate_gate_id=True)

        self.assertTrue(
            any("duplicate gate_result_id" in error for error in reporter.errors)
        )

    def test_null_scoped_gate_metadata_fails(self) -> None:
        reporter = self._run(
            gate_overrides={"G1": {"document_id": None}}
        )

        self.assertTrue(
            any("lacks non-null" in error for error in reporter.errors)
        )

    def test_non_passing_gate_fails(self) -> None:
        reporter = self._run(gate_overrides={"G0": {"status": "fail"}})

        self.assertTrue(
            any("non-passing" in error for error in reporter.errors)
        )

    def test_wrong_gate_set_fails(self) -> None:
        reporter = self._run(
            {
                "evidence_ids": [
                    "GATE-RESULT-G-ARCH-TARGET",
                    "GATE-RESULT-G0-TARGET",
                    "GATE-RESULT-G1-TARGET",
                ]
            }
        )

        self.assertTrue(any("gate set" in error for error in reporter.errors))

    def test_unresolved_superseded_by_fails(self) -> None:
        reporter = self._run(
            artifact_relationships={
                "approves": [self.document_id],
                "superseded_by": ["DOC-MISSING"],
            }
        )

        self.assertTrue(
            any("unresolved superseded_by" in error for error in reporter.errors)
        )

    def test_resolved_superseded_approval_is_preserved(self) -> None:
        reporter = self._run(
            artifact_relationships={
                "approves": [self.document_id],
                "superseded_by": ["DOC-APPROVAL-NEW"],
            }
        )

        self.assertEqual([], reporter.errors)


if __name__ == "__main__":
    unittest.main()
