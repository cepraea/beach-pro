"""Cross-reference validation for documentary approvals and gate evidence."""

from __future__ import annotations

import yaml

from . import config
from . import reporter as reporter_module
from .json_types import JsonObject, as_json_array, as_json_object


def validate_approval_cross_references(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    """Validate the complete identity chain of every active approval.

    Historical approvals are skipped only when ``superseded_by`` resolves to a
    registered successor. Active approvals must link in both directions and
    carry the exact four passing gates for the same document bytes.
    """
    registry_hashes: dict[tuple[str, str], str] = {}
    registry_targets: dict[tuple[str, str], JsonObject] = {}
    registry_by_id: dict[str, JsonObject] = {}
    path_to_registry: dict[str, JsonObject] = {}
    for record in documents:
        doc_id = record.get("document_id")
        version = record.get("version")
        content_hash = record.get("content_hash")
        if isinstance(doc_id, str):
            registry_by_id[doc_id] = record
        if (
            isinstance(doc_id, str)
            and isinstance(version, str)
            and isinstance(content_hash, str)
        ):
            registry_hashes[(doc_id, version)] = content_hash
            registry_targets[(doc_id, version)] = record
        cp = record.get("current_path")
        if isinstance(cp, str):
            path_to_registry[cp] = record

    gate_results: dict[str, JsonObject] = {}
    for result_path in sorted(
        (config.WORKSPACE_ROOT / "docs/evidence/gates").glob("*.yaml")
    ):
        try:
            data = yaml.safe_load(result_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        data_mapping = as_json_object(data)
        result = as_json_object(
            data_mapping.get("gate_result")
            if data_mapping is not None
            else None
        )
        result_id = result.get("gate_result_id") if result else None
        if result is not None and isinstance(result_id, str):
            if result_id in gate_results:
                reporter.error(f"duplicate gate_result_id: {result_id}")
                continue
            gate_results[result_id] = result

    for approval_path in sorted(
        (config.WORKSPACE_ROOT / "docs/evidence/approvals").glob("*.yaml")
    ):
        relative = approval_path.relative_to(
            config.WORKSPACE_ROOT
        ).as_posix()
        reg_entry = path_to_registry.get(relative)
        if reg_entry is not None:
            rels = as_json_object(reg_entry.get("relationships"))
            superseded_by = (
                as_json_array(rels.get("superseded_by"))
                if rels is not None
                else None
            )
            if superseded_by:
                unresolved = [
                    successor
                    for successor in superseded_by
                    if not isinstance(successor, str)
                    or successor not in registry_by_id
                ]
                if unresolved:
                    reporter.error(
                        f"{relative}: unresolved superseded_by: {unresolved}"
                    )
                else:
                    # Historical approval remains auditable, but only its
                    # registered successor can satisfy a current promotion.
                    continue
        try:
            data = yaml.safe_load(approval_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        data_mapping = as_json_object(data)
        approval = as_json_object(
            data_mapping.get("approval")
            if data_mapping is not None
            else None
        )
        if approval is None:
            continue
        doc_id = approval.get("document_id")
        version = approval.get("version")
        approval_hash = approval.get("content_hash")
        evidence_ids = as_json_array(approval.get("evidence_ids")) or []
        if not (isinstance(doc_id, str) and isinstance(version, str)):
            continue
        expected_hash = registry_hashes.get((doc_id, version))
        target_record = registry_targets.get((doc_id, version))
        if expected_hash is None:
            reporter.error(
                f"{relative}: approval target is not registered: "
                f"{doc_id} v{version}"
            )
        elif approval_hash != expected_hash:
            reporter.error(
                f"{relative}: approval content_hash does not match registry "
                f"hash for {doc_id} v{version}"
            )
        if target_record is None:
            continue

        artifact_relationships = (
            as_json_object(reg_entry.get("relationships"))
            if reg_entry is not None
            else None
        )
        approved_targets = (
            as_json_array(artifact_relationships.get("approves"))
            if artifact_relationships is not None
            else None
        ) or []
        if doc_id not in approved_targets:
            reporter.error(
                f"{relative}: registry approval artifact does not approve "
                f"{doc_id}"
            )

        approval_id = approval.get("approval_id")
        target_relationships = as_json_object(
            target_record.get("relationships")
        )
        linked_approvals = (
            as_json_array(target_relationships.get("approval_id"))
            if target_relationships is not None
            else None
        ) or []
        if approval_id not in linked_approvals:
            reporter.error(
                f"{relative}: target {doc_id} v{version} does not link "
                f"approval {approval_id}"
            )

        if target_record.get("workflow_status") in {"SUPERADA", "REVOGADA"}:
            continue

        if len(evidence_ids) != len(
            {item for item in evidence_ids if isinstance(item, str)}
        ):
            reporter.error(f"{relative}: approval has duplicate evidence_ids")
        observed_gate_ids: set[str] = set()
        for evidence_id in evidence_ids:
            if not isinstance(evidence_id, str):
                continue
            gate_result = gate_results.get(evidence_id)
            if gate_result is None:
                reporter.error(
                    f"{relative}: approval references unknown gate result "
                    f"{evidence_id}"
                )
                continue
            if gate_result.get("status") != "pass":
                reporter.error(
                    f"{relative}: approval references non-passing gate result "
                    f"{evidence_id}"
                )
            gate_id = gate_result.get("gate_id")
            if isinstance(gate_id, str):
                observed_gate_ids.add(gate_id)
            gr_doc_id = gate_result.get("document_id")
            gr_version = gate_result.get("version")
            gr_hash = gate_result.get("content_hash")
            if not all(
                isinstance(value, str)
                for value in (gr_doc_id, gr_version, gr_hash)
            ):
                reporter.error(
                    f"{relative}: gate result {evidence_id} lacks non-null "
                    "document_id, version or content_hash"
                )
                continue
            if gr_doc_id != doc_id:
                reporter.error(
                    f"{relative}: gate result {evidence_id} document_id "
                    f"{gr_doc_id!r} does not match approval document_id "
                    f"{doc_id!r}"
                )
            if gr_version != version:
                reporter.error(
                    f"{relative}: gate result {evidence_id} version "
                    f"{gr_version!r} does not match approval version "
                    f"{version!r}"
                )
            if isinstance(approval_hash, str) and gr_hash != approval_hash:
                reporter.error(
                    f"{relative}: gate result {evidence_id} content_hash does "
                    f"not match approval content_hash for {doc_id} v{version}"
                )
        required_gate_ids = {"G-ARCH", "G0", "G1", "G-FM"}
        if observed_gate_ids != required_gate_ids:
            reporter.error(
                f"{relative}: approval gate set must be "
                f"{sorted(required_gate_ids)}; found "
                f"{sorted(observed_gate_ids)}"
            )
