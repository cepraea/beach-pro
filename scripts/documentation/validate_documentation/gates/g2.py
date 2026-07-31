"""Document-scoped provenance gate."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import tarfile

import yaml

from .. import config
from .. import registry as registry_module
from .. import reporter as reporter_module
from ..json_types import JsonObject, as_json_array, as_json_object


def validate_g2(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
    document_id_filter: str | None,
    version_filter: str | None,
) -> None:
    """Validate provenance against the exact registered document bytes.

    Indexing by both ID and version prevents a later revision from silently
    replacing the target against which sources and critical claims were proven.
    """
    if document_id_filter and registry_module.resolve_document_version(
        documents,
        document_id_filter,
        version_filter,
        reporter,
    ) is None:
        return
    records: dict[tuple[str, str], JsonObject] = {}
    for record in documents:
        document_id = record.get("document_id")
        version = record.get("version")
        if isinstance(document_id, str) and isinstance(version, str):
            records[(document_id, version)] = record
    provenance_root = config.WORKSPACE_ROOT / "docs/evidence/provenance"
    selected: list[tuple[Path, JsonObject]] = []
    for package_path in sorted(provenance_root.glob("*.yaml")):
        try:
            data = yaml.safe_load(package_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            reporter.error(f"G2 cannot load {package_path}: {error}")
            continue
        data_mapping = as_json_object(data)
        package = as_json_object(
            data_mapping.get("provenance_package")
            if data_mapping is not None
            else None
        )
        if package is None:
            continue
        if (
            document_id_filter
            and package.get("document_id") != document_id_filter
        ):
            continue
        if version_filter and package.get("document_version") != version_filter:
            continue
        selected.append((package_path, package))
    if not selected:
        reporter.error("G2 found no provenance package for the requested scope")
        return

    ambiguous_reference_re = re.compile(
        r"(?:SRC-[0-9]{3}\s+(?:a|até)\s+SRC-[0-9]{3}|"
        r"documentos oficiais|decisões de Davi|metadados de)",
        re.IGNORECASE,
    )
    for package_path, package in selected:
        provenance_id = package.get("provenance_id", "<missing-provenance-id>")
        document_id = package.get("document_id")
        document_version = package.get("document_version")
        record = (
            records.get((document_id, document_version))
            if isinstance(document_id, str)
            and isinstance(document_version, str)
            else None
        )
        if not record:
            reporter.error(f"{provenance_id}: target document is not registered")
            continue
        if package.get("document_version") != record.get("version"):
            reporter.error(f"{provenance_id}: document version differs from registry")
        if package.get("document_hash") != record.get("content_hash"):
            reporter.error(f"{provenance_id}: document hash differs from registry")

        source_items: list[JsonObject] = []
        for raw_source in as_json_array(package.get("sources")) or []:
            source = as_json_object(raw_source)
            if source is not None:
                source_items.append(source)
        claim_items: list[JsonObject] = []
        for raw_claim in as_json_array(package.get("claims")) or []:
            claim = as_json_object(raw_claim)
            if claim is not None:
                claim_items.append(claim)
        source_ids = [
            source_id
            for item in source_items
            if isinstance((source_id := item.get("source_id")), str)
        ]
        claim_ids = [
            claim_id
            for item in claim_items
            if isinstance((claim_id := item.get("claim_id")), str)
        ]
        for value in sorted(
            {value for value in source_ids if source_ids.count(value) > 1}
        ):
            reporter.error(f"{provenance_id}: duplicate source ID {value}")
        for value in sorted(
            {value for value in claim_ids if claim_ids.count(value) > 1}
        ):
            reporter.error(f"{provenance_id}: duplicate claim ID {value}")
        sources: dict[str, JsonObject] = {}
        for item in source_items:
            source_id = item.get("source_id")
            if isinstance(source_id, str):
                sources[source_id] = item
        policy = as_json_object(package.get("policy")) or {}
        require_active = (
            policy.get("require_active_sources") is True
        )
        reject_ambiguous = (
            policy.get("reject_ambiguous_references") is True
        )
        referenced_ids: set[str] = set()
        for claim in claim_items:
            for source_id in as_json_array(claim.get("source_ids")) or []:
                if isinstance(source_id, str):
                    referenced_ids.add(source_id)
        archive_hashes: dict[tuple[Path, str], str | None] = {}
        for source_id in sorted(referenced_ids):
            source = sources.get(source_id)
            if not source:
                reporter.error(f"{provenance_id}: unresolved source {source_id}")
                continue
            if require_active and source.get("status") != "active":
                reporter.error(f"{provenance_id}: source {source_id} is not active")
            if str(source.get("location", "")).startswith("unresolved:"):
                reporter.error(
                    f"{provenance_id}: source {source_id} location is unresolved"
                )
            if source.get("status") == "active":
                immutable_reference = source.get("immutable_reference")
                content_hash = source.get("content_hash")
                if not immutable_reference:
                    reporter.error(
                        f"{provenance_id}: source {source_id} lacks immutable reference"
                    )
                elif content_hash and immutable_reference != f"sha256:{content_hash}":
                    reporter.error(
                        f"{provenance_id}: source {source_id} immutable reference "
                        "differs from content hash"
                    )
                if not source.get("verified_at") or not source.get("verified_by"):
                    reporter.error(
                        f"{provenance_id}: source {source_id} lacks verification"
                    )
                location = str(source.get("location", ""))
                if "#" in location:
                    archive_name, member_name = location.split("#", 1)
                    archive_path = (
                        config.WORKSPACE_ROOT / archive_name
                    ).resolve()
                    try:
                        archive_path.relative_to(config.WORKSPACE_ROOT)
                    except ValueError:
                        reporter.error(
                            f"{provenance_id}: source {source_id} archive "
                            "escapes workspace"
                        )
                        continue
                    cache_key = (archive_path, member_name)
                    if cache_key not in archive_hashes:
                        try:
                            with tarfile.open(archive_path, "r") as archive:
                                member = archive.getmember(member_name)
                                extracted = archive.extractfile(member)
                                archive_hashes[cache_key] = (
                                    hashlib.sha256(extracted.read()).hexdigest()
                                    if extracted is not None
                                    else None
                                )
                        except (OSError, KeyError, tarfile.TarError):
                            archive_hashes[cache_key] = None
                    if archive_hashes[cache_key] is None:
                        reporter.error(
                            f"{provenance_id}: source {source_id} preserved "
                            "artifact cannot be read"
                        )
                    elif archive_hashes[cache_key] != content_hash:
                        reporter.error(
                            f"{provenance_id}: source {source_id} preserved "
                            "artifact hash mismatch"
                        )

        critical_claims: list[JsonObject] = [
            claim
            for claim in claim_items
            if claim.get("criticality") == "critical"
        ]
        covered = 0
        for claim in critical_claims:
            claim_id = claim.get("claim_id", "<missing-claim-id>")
            if claim.get("document_id") != document_id:
                reporter.error(f"{provenance_id}: {claim_id} targets another document")
            if claim.get("document_version") != package.get("document_version"):
                reporter.error(f"{provenance_id}: {claim_id} targets another version")
            if claim.get("document_hash") != package.get("document_hash"):
                reporter.error(f"{provenance_id}: {claim_id} targets another hash")
            reference_text = str(claim.get("source_reference_text", ""))
            if reject_ambiguous and ambiguous_reference_re.search(reference_text):
                reporter.error(
                    f"{provenance_id}: {claim_id} has ambiguous source reference"
                )
            active_sources: list[JsonObject] = []
            for source_id in as_json_array(claim.get("source_ids")) or []:
                if not isinstance(source_id, str):
                    continue
                source = sources.get(source_id)
                if (
                    source is not None
                    and source.get("status") == "active"
                    and source.get("immutable_reference")
                    and source.get("verified_at")
                    and source.get("verified_by")
                ):
                    active_sources.append(source)
            claim_subjects = {
                subject
                for subject in as_json_array(claim.get("subjects")) or []
                if isinstance(subject, str)
            }
            scoped_sources: list[JsonObject] = []
            for source in active_sources:
                authority = as_json_object(source.get("authority")) or {}
                authority_scope = {
                    subject
                    for subject in as_json_array(authority.get("scope")) or []
                    if isinstance(subject, str)
                }
                if claim_subjects.intersection(authority_scope):
                    scoped_sources.append(source)
            explicit_uncertainty = (
                claim.get("uncertainty")
                in {"controlled", "unknown", "contradictory"}
                and bool(claim.get("uncertainty_reason"))
            )
            if scoped_sources or explicit_uncertainty:
                covered += 1
            else:
                reporter.error(
                    f"{provenance_id}: {claim_id} lacks verified source "
                    "with matching authority scope or explicit uncertainty"
                )
        raw_required_coverage = policy.get("critical_coverage_percent", 100)
        required_coverage = (
            raw_required_coverage
            if isinstance(raw_required_coverage, (int, float))
            else 100
        )
        actual_coverage = (
            100 * covered / len(critical_claims) if critical_claims else 0
        )
        if actual_coverage < required_coverage:
            reporter.error(
                f"{provenance_id}: critical provenance coverage "
                f"{actual_coverage:.2f}% is below {required_coverage}%"
            )


