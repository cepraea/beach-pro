"""Validation of immutable ingestion snapshots and their registered lineage."""

from __future__ import annotations

import yaml

from . import config
from . import reporter as reporter_module
from .json_types import JsonObject, as_json_array, as_json_object


def ingestion_records(documents: list[JsonObject]) -> list[JsonObject]:
    return [
        record
        for record in documents
        if (
            (relationships := as_json_object(record.get("relationships")))
            is not None
            and relationships.get("previous_paths")
        )
    ]


def validate_ingestion_consistency(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    """Compare the immutable ingestion snapshot with its registered lineage.

    A later version can replace the working document without rewriting the
    historical event. The same version, however, must retain the snapshot hash.
    """
    ingestion_root = config.WORKSPACE_ROOT / "docs/evidence/ingestion"
    if not ingestion_root.is_dir():
        return
    records: dict[tuple[str, str], JsonObject] = {}
    for record in documents:
        document_id = record.get("document_id")
        version = record.get("version")
        if isinstance(document_id, str) and isinstance(version, str):
            records[(document_id, version)] = record
    manifest: JsonObject = {}
    if config.INTEGRITY_MANIFEST.is_file():
        try:
            loaded = yaml.safe_load(
                config.INTEGRITY_MANIFEST.read_text(encoding="utf-8")
            )
            loaded_manifest = as_json_object(loaded)
            if loaded_manifest is not None:
                manifest = loaded_manifest
        except (OSError, UnicodeError, yaml.YAMLError):
            return
    manifest_documents: set[tuple[str, str, str]] = set()
    for raw_item in as_json_array(manifest.get("documents")) or []:
        item = as_json_object(raw_item)
        if item is None:
            continue
        document_id = item.get("document_id")
        version = item.get("version")
        content_hash = item.get("content_hash")
        if (
            isinstance(document_id, str)
            and isinstance(version, str)
            and isinstance(content_hash, str)
        ):
            manifest_documents.add((document_id, version, content_hash))

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
            gate_results[result_id] = result

    for ingestion_path in sorted(ingestion_root.glob("*.yaml")):
        try:
            data = yaml.safe_load(ingestion_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        data_mapping = as_json_object(data)
        event = as_json_object(
            data_mapping.get("ingestion_event")
            if data_mapping is not None
            else None
        )
        if event is None:
            continue
        event_id = event.get("event_id", "<missing-event-id>")
        if event.get("manifest_id") != manifest.get("manifest_id"):
            reporter.error(f"{event_id}: ingestion manifest does not match")
        event_documents: set[tuple[str, str, str]] = set()
        for raw_item in as_json_array(event.get("documents")) or []:
            item = as_json_object(raw_item)
            if item is None:
                continue
            document_id = item.get("document_id")
            version = item.get("version")
            content_hash = item.get("content_hash")
            if (
                isinstance(document_id, str)
                and isinstance(version, str)
                and isinstance(content_hash, str)
            ):
                event_documents.add((document_id, version, content_hash))
        if event_documents != manifest_documents:
            reporter.error(
                f"{event_id}: ingestion document set differs from manifest"
            )
        expected_gate_ids = {"G-ARCH", "G0", "G1"}
        observed_gate_ids: set[str] = set()
        for result_id in as_json_array(event.get("gate_result_ids")) or []:
            if not isinstance(result_id, str):
                reporter.error(f"{event_id}: invalid gate result ID")
                continue
            result = gate_results.get(result_id)
            if not result:
                reporter.error(
                    f"{event_id}: unknown gate result {result_id}"
                )
                continue
            if result.get("status") != "pass":
                reporter.error(
                    f"{event_id}: gate result {result_id} is not pass"
                )
            gate_id = result.get("gate_id")
            if isinstance(gate_id, str):
                observed_gate_ids.add(gate_id)
        if not expected_gate_ids.issubset(observed_gate_ids):
            reporter.error(
                f"{event_id}: ingestion lacks passing G-ARCH, G0 or G1"
            )
        for document_id, version, content_hash in event_documents:
            record = records.get((document_id, version))
            if record is None:
                # Fall back to any version of this document_id for the
                # ingestion relationship check (document may have advanced).
                record = next(
                    (r for k, r in records.items() if k[0] == document_id),
                    None,
                )
            if not record:
                reporter.error(
                    f"{event_id}: unknown ingested document {document_id}"
                )
                continue
            # O evento de ingestão é um snapshot histórico. Uma revisão
            # posterior pode manter o mesmo document_id e avançar a versão sem
            # reescrever a evidência original. Se a versão ainda for a mesma,
            # porém, o hash também deve permanecer idêntico.
            if (
                record.get("version") == version
                and record.get("content_hash") != content_hash
            ):
                reporter.error(
                    f"{event_id}: hash differs for {document_id}"
                )
            relationships = as_json_object(record.get("relationships"))
            linked_events = (
                as_json_array(relationships.get("ingestion_event_id"))
                if relationships is not None
                else None
            ) or []
            if event_id not in linked_events:
                reporter.error(
                    f"{event_id}: {document_id} lacks ingestion relationship"
                )
