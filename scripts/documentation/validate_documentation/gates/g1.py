"""Global preservation-integrity gate."""

from __future__ import annotations

import hashlib
import tarfile

import yaml

from .. import config
from .. import filesystem
from .. import ingestion as ingestion_module
from .. import reporter as reporter_module
from ..json_types import JsonObject, as_json_array, as_json_object


def validate_g1(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    """Validate the immutable global ingestion snapshot and preservation TAR."""
    candidates = ingestion_module.ingestion_records(documents)
    if not config.INTEGRITY_MANIFEST.is_file():
        reporter.error("G1 integrity manifest not found")
        return
    try:
        manifest = yaml.safe_load(
            config.INTEGRITY_MANIFEST.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        reporter.error(f"G1 cannot load integrity manifest: {error}")
        return
    typed_manifest = as_json_object(manifest)
    if typed_manifest is None:
        reporter.error("G1 integrity manifest must be a mapping")
        return

    manifest_items: dict[str, JsonObject] = {}
    for raw_item in as_json_array(typed_manifest.get("documents")) or []:
        item = as_json_object(raw_item)
        document_id = item.get("document_id") if item is not None else None
        if item is not None and isinstance(document_id, str):
            manifest_items[document_id] = item
    candidate_ids = {
        document_id
        for record in candidates
        if isinstance((document_id := record.get("document_id")), str)
    }
    if set(manifest_items) != candidate_ids:
        reporter.error("G1 manifest document set differs from ingestion batch")

    for record in candidates:
        document_id = record.get("document_id")
        item = (
            manifest_items.get(document_id)
            if isinstance(document_id, str)
            else None
        )
        if item is None:
            reporter.error(f"{document_id}: G1 manifest item missing")
            continue
        # The manifest proves ingested bytes preserved in the bundle, not a
        # mutable mirror of a later revision. Compare registry bytes only while
        # the registered version still denotes that historical snapshot.
        _terminal = record.get("workflow_status") in ("SUPERADA", "REVOGADA")
        if record.get("version") == item.get("version"):
            comparisons = {
                "content_hash": record.get("content_hash"),
            }
            if record.get("canonical_path") is None and not _terminal:
                comparisons["path"] = record.get("current_path")
            for field, expected in comparisons.items():
                if item.get(field) != expected:
                    reporter.error(
                        f"{document_id}: G1 manifest {field} differs from registry"
                    )

    bundle = as_json_object(typed_manifest.get("bundle"))
    if bundle is None:
        reporter.error("G1 bundle record missing")
        return
    bundle_path = filesystem.workspace_path(
        str(bundle.get("path", "")),
        reporter,
    )
    if bundle_path is None or not bundle_path.is_file():
        reporter.error("G1 preservation bundle not found")
        return
    if filesystem.sha256(bundle_path) != bundle.get("content_hash"):
        reporter.error("G1 preservation bundle hash mismatch")
        return

    try:
        with tarfile.open(bundle_path, "r") as archive:
            members = {
                member.name: member
                for member in archive.getmembers()
                if member.isfile()
            }
            expected_members = {
                member_name
                for item in manifest_items.values()
                if isinstance(
                    (member_name := item.get("archive_member")),
                    str,
                )
            }
            if set(members) != expected_members:
                reporter.error("G1 archive member set differs from manifest")
            for item in manifest_items.values():
                member_name = item.get("archive_member")
                if not isinstance(member_name, str):
                    reporter.error("G1 manifest archive_member is invalid")
                    continue
                member = members.get(member_name)
                if member is None:
                    continue
                extracted = archive.extractfile(member)
                if extracted is None:
                    reporter.error(f"G1 cannot read archive member {member_name}")
                    continue
                digest = hashlib.sha256(extracted.read()).hexdigest()
                if digest != item.get("content_hash"):
                    reporter.error(
                        f"G1 archive member hash mismatch: {member_name}"
                    )
    except (OSError, tarfile.TarError) as error:
        reporter.error(f"G1 cannot inspect preservation bundle: {error}")
