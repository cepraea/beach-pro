"""Validate the CEPRAEA documentation registry and filesystem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile
from typing import Any, cast
from urllib.parse import unquote, urlparse

import yaml

from . import config
from . import contracts as contracts_module
from . import filesystem
from . import reporter as reporter_module
from . import registry as registry_module
from . import workflow as workflow_module
from .json_types import (
    JsonObject as JsonObject,
    as_json_array as as_json_array,
    as_json_object as as_json_object,
)
from .models import ValidatorArgs as ValidatorArgs


# Transitional re-exports preserve the package API while implementations consult
# ``config`` directly so tests can patch the canonical lookup location.
WORKSPACE_ROOT = config.WORKSPACE_ROOT
DEFAULT_REGISTRY = config.DEFAULT_REGISTRY
DEFAULT_WORKFLOW = config.DEFAULT_WORKFLOW
SCHEMA_ROOT = config.SCHEMA_ROOT
DOCUMENT_SCHEMA = config.DOCUMENT_SCHEMA
WORKFLOW_SCHEMA = config.WORKFLOW_SCHEMA
GATE_RESULT_SCHEMA = config.GATE_RESULT_SCHEMA
INTEGRITY_MANIFEST_SCHEMA = config.INTEGRITY_MANIFEST_SCHEMA
INGESTION_SCHEMA = config.INGESTION_SCHEMA
SOURCE_SCHEMA = config.SOURCE_SCHEMA
CLAIM_SCHEMA = config.CLAIM_SCHEMA
PROVENANCE_SCHEMA = config.PROVENANCE_SCHEMA
DIVERGENCE_SCHEMA = config.DIVERGENCE_SCHEMA
CORRECTIVE_ACTION_SCHEMA = config.CORRECTIVE_ACTION_SCHEMA
WORKFLOW_EVENT_SCHEMA = config.WORKFLOW_EVENT_SCHEMA
APPROVAL_SCHEMA = config.APPROVAL_SCHEMA
INTEGRITY_MANIFEST = config.INTEGRITY_MANIFEST
workspace_path = filesystem.workspace_path
sha256 = filesystem.sha256
Reporter = reporter_module.Reporter
load_json = contracts_module.load_json
validate_schema_definition = contracts_module.validate_schema_definition
schema_validation_errors = contracts_module.schema_validation_errors
validate_contract_schemas = contracts_module.validate_contract_schemas
validate_yaml_instance = contracts_module.validate_yaml_instance
valid_name = registry_module.valid_name
validate_top_level = registry_module.validate_top_level
resolve_document_version = registry_module.resolve_document_version
validate_record = registry_module.validate_record
validate_uniqueness = registry_module.validate_uniqueness
managed_files = registry_module.managed_files
validate_canonical_registry = registry_module.validate_canonical_registry
load_registry = registry_module.load_registry
validate_registry_integrity = registry_module.validate_registry_integrity
validate_workflow_references = workflow_module.validate_workflow_references
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
LINE_REFERENCE_RE = re.compile(
    r"^(.*\.(?:md|yaml|yml|json))(?::[0-9]+)?(?:#.*)?$",
    re.IGNORECASE,
)
GLOBAL_GATES = {"G-ARCH", "G0", "G1"}


def parse_args() -> ValidatorArgs:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=config.DEFAULT_REGISTRY,
        help="Registry path; defaults to the controlled CEPRAEA registry.",
    )
    parser.add_argument(
        "--strict-legacy",
        action="store_true",
        help="Treat known legacy naming and directory deviations as errors.",
    )
    parser.add_argument(
        "--gate",
        choices=["G-ARCH", "G0", "G1", "G2", "G-FM"],
        help="Execute a named blocking gate.",
    )
    parser.add_argument(
        "--document-id",
        help="Restrict a document-scoped gate to this document ID.",
    )
    parser.add_argument(
        "--version",
        help="Restrict a document-scoped gate to this version.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "yaml"],
        default="text",
        help="Output format; YAML emits a processable gate result.",
    )
    parser.add_argument(
        "--result-id",
        help=(
            "Explicit GATE-RESULT-* identity for YAML that will be persisted; "
            "the default RUNTIME identity is diagnostic only."
        ),
    )
    args = ValidatorArgs()
    parser.parse_args(namespace=args)
    return args


def validate_cli_args(args: ValidatorArgs, reporter: Reporter) -> bool:
    """Reject argument combinations whose scope has no defined semantics."""
    if args.version and not args.document_id:
        reporter.error("--version requires --document-id")
    if args.gate in GLOBAL_GATES and (args.document_id or args.version):
        reporter.error(f"{args.gate} is global and does not accept document scope")
    if args.document_id and args.gate not in {"G2", "G-FM"}:
        reporter.error("--document-id requires gate G2 or G-FM")
    if args.result_id and not re.fullmatch(
        r"GATE-RESULT-[A-Z0-9-]+", args.result_id
    ):
        reporter.error("--result-id must match GATE-RESULT-[A-Z0-9-]+")
    return not reporter.errors


def normalize_link_target(markdown_path: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = unquote(target)
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("#"):
        return None

    match = LINE_REFERENCE_RE.match(target)
    if match:
        target = match.group(1)
    else:
        target = target.split("#", 1)[0]

    candidate = Path(target)
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (markdown_path.parent / candidate).resolve()
    )
    return resolved


def validate_links(reporter: Reporter) -> None:
    for markdown_path in sorted(
        (config.WORKSPACE_ROOT / "docs").rglob("*.md")
    ):
        text = markdown_path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = normalize_link_target(markdown_path, raw_target)
            if target is None:
                continue
            try:
                target.relative_to(config.WORKSPACE_ROOT)
            except ValueError:
                relative_source = markdown_path.relative_to(
                    config.WORKSPACE_ROOT
                )
                reporter.error(
                    f"{relative_source}: local link escapes workspace: "
                    f"{raw_target}"
                )
                continue
            if not target.exists():
                relative_source = markdown_path.relative_to(
                    config.WORKSPACE_ROOT
                )
                reporter.error(
                    f"{relative_source}: broken local link: {raw_target}"
                )


def validate_document_instances(
    documents: list[JsonObject],
    reporter: Reporter,
) -> None:
    """Validate registry records against the document contract."""
    document_schema = as_json_object(
        contracts_module.load_json(config.DOCUMENT_SCHEMA, reporter)
    )
    if document_schema is None:
        return
    for record in documents:
        document_id = record.get("document_id", "<missing-id>")
        for error in contracts_module.schema_validation_errors(
            document_schema,
            record,
        ):
            location = ".".join(str(part) for part in error.absolute_path)
            reporter.error(
                f"{document_id}: document contract failure at "
                f"{location or '<root>'}: {error.message}"
            )


def validate_workflow_instance(reporter: Reporter) -> None:
    """Validate workflow shape before resolving its internal references."""
    workflow_schema = as_json_object(
        contracts_module.load_json(config.WORKFLOW_SCHEMA, reporter)
    )
    try:
        workflow_data = yaml.safe_load(
            config.DEFAULT_WORKFLOW.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        reporter.error(f"cannot load processable workflow: {error}")
        return
    if workflow_schema is not None:
        for error in contracts_module.schema_validation_errors(
            workflow_schema,
            workflow_data,
        ):
            location = ".".join(str(part) for part in error.absolute_path)
            reporter.error(
                "workflow contract failure at "
                f"{location or '<root>'}: {error.message}"
            )

    typed_workflow = as_json_object(workflow_data)
    if typed_workflow is not None:
        workflow_module.validate_workflow_references(typed_workflow, reporter)

    contract_paths: set[str] = set()
    contracts = (
        as_json_array(typed_workflow.get("contracts"))
        if typed_workflow is not None
        else None
    )
    for raw_contract in contracts or []:
        contract = as_json_object(raw_contract)
        schema_path = contract.get("schema_path") if contract else None
        if isinstance(schema_path, str):
            contract_paths.add(schema_path)
    for raw_path in sorted(contract_paths):
        path = filesystem.workspace_path(raw_path, reporter)
        if path is not None and not path.is_file():
            reporter.error(f"workflow contract not found: {raw_path}")


def validate_gate_result_instances(reporter: Reporter) -> None:
    """Validate each persisted gate result independently of approvals."""
    gate_result_schema = as_json_object(
        contracts_module.load_json(config.GATE_RESULT_SCHEMA, reporter)
    )
    if gate_result_schema is None:
        return
    gate_root = config.WORKSPACE_ROOT / "docs/evidence/gates"
    for result_path in sorted(gate_root.glob("*.yaml")):
        try:
            result_data = yaml.safe_load(
                result_path.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            reporter.error(f"cannot load gate result {result_path}: {error}")
            continue
        result_mapping = as_json_object(result_data)
        instance = (
            result_mapping.get("gate_result")
            if result_mapping is not None
            else None
        )
        for error in contracts_module.schema_validation_errors(
            gate_result_schema,
            instance,
        ):
            relative = result_path.relative_to(config.WORKSPACE_ROOT)
            location = ".".join(str(part) for part in error.absolute_path)
            reporter.error(
                f"{relative}: gate result contract failure at "
                f"{location or '<root>'}: {error.message}"
            )


def validate_evidence_instances(
    documents: list[JsonObject],
    reporter: Reporter,
) -> None:
    """Validate evidence shapes, then enforce their cross-file identities.

    Schema validation proves local structure only. Cross-reference validators
    remain mandatory because a well-formed ID can still point to no artifact.
    """
    contracts_module.validate_yaml_instance(
        config.INTEGRITY_MANIFEST,
        config.INTEGRITY_MANIFEST_SCHEMA,
        None,
        "integrity manifest",
        reporter,
    )
    ingestion_root = config.WORKSPACE_ROOT / "docs/evidence/ingestion"
    for ingestion_path in sorted(ingestion_root.glob("*.yaml")):
        contracts_module.validate_yaml_instance(
            ingestion_path,
            config.INGESTION_SCHEMA,
            "ingestion_event",
            "ingestion event",
            reporter,
        )
    validate_ingestion_consistency(documents, reporter)
    validate_provenance_packages(reporter)
    for divergence_path in sorted(
        (config.WORKSPACE_ROOT / "docs/evidence/integrity").glob(
            "divergencia-*.yaml"
        )
    ):
        contracts_module.validate_yaml_instance(
            divergence_path,
            config.DIVERGENCE_SCHEMA,
            "integrity_divergence",
            "integrity divergence",
            reporter,
        )
    for action_path in sorted(
        (config.WORKSPACE_ROOT / "docs/evidence/corrections").glob("*.yaml")
    ):
        contracts_module.validate_yaml_instance(
            action_path,
            config.CORRECTIVE_ACTION_SCHEMA,
            "corrective_action",
            "corrective action",
            reporter,
        )
    for event_path in sorted(
        (config.WORKSPACE_ROOT / "docs/evidence/events").glob("*.yaml")
    ):
        contracts_module.validate_yaml_instance(
            event_path,
            config.WORKFLOW_EVENT_SCHEMA,
            "workflow_event",
            "workflow event",
            reporter,
        )
    for approval_path in sorted(
        (config.WORKSPACE_ROOT / "docs/evidence/approvals").glob("*.yaml")
    ):
        contracts_module.validate_yaml_instance(
            approval_path,
            config.APPROVAL_SCHEMA,
            "approval",
            "approval",
            reporter,
        )
    validate_approval_cross_references(documents, reporter)


def validate_instances(
    documents: list[JsonObject],
    reporter: Reporter,
) -> None:
    """Orchestrate independent instance families in dependency order."""
    validate_document_instances(documents, reporter)
    validate_workflow_instance(reporter)
    validate_gate_result_instances(reporter)
    validate_evidence_instances(documents, reporter)


def validate_approval_cross_references(
    documents: list[JsonObject], reporter: Reporter
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
        if isinstance(doc_id, str) and isinstance(version, str) and isinstance(content_hash, str):
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
                    f"{gr_version!r} does not match approval version {version!r}"
                )
            if (
                isinstance(approval_hash, str)
                and gr_hash != approval_hash
            ):
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


def validate_provenance_packages(reporter: Reporter) -> None:
    provenance_root = config.WORKSPACE_ROOT / "docs/evidence/provenance"
    package_schema = as_json_object(
        contracts_module.load_json(config.PROVENANCE_SCHEMA, reporter)
    )
    source_schema = as_json_object(
        contracts_module.load_json(config.SOURCE_SCHEMA, reporter)
    )
    claim_schema = as_json_object(
        contracts_module.load_json(config.CLAIM_SCHEMA, reporter)
    )
    if (
        package_schema is None
        or source_schema is None
        or claim_schema is None
    ):
        return
    for package_path in sorted(provenance_root.glob("*.yaml")):
        try:
            data = yaml.safe_load(package_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            reporter.error(f"cannot load provenance package: {error}")
            continue
        data_mapping = as_json_object(data)
        package = as_json_object(
            data_mapping.get("provenance_package")
            if data_mapping is not None
            else None
        )
        relative = package_path.relative_to(config.WORKSPACE_ROOT)
        for error in contracts_module.schema_validation_errors(
            package_schema,
            package,
        ):
            location = ".".join(str(part) for part in error.absolute_path)
            reporter.error(
                f"{relative}: provenance contract failure at "
                f"{location or '<root>'}: {error.message}"
            )
        if package is None:
            continue
        sources = as_json_array(package.get("sources")) or []
        for index, source in enumerate(sources):
            for error in contracts_module.schema_validation_errors(
                source_schema,
                source,
            ):
                location = ".".join(str(part) for part in error.absolute_path)
                reporter.error(
                    f"{relative}: source[{index}] contract failure at "
                    f"{location or '<root>'}: {error.message}"
                )
        claims = as_json_array(package.get("claims")) or []
        for index, claim in enumerate(claims):
            for error in contracts_module.schema_validation_errors(
                claim_schema,
                claim,
            ):
                location = ".".join(str(part) for part in error.absolute_path)
                reporter.error(
                    f"{relative}: claim[{index}] contract failure at "
                    f"{location or '<root>'}: {error.message}"
                )


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
    reporter: Reporter,
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


def validate_g0(documents: list[JsonObject], reporter: Reporter) -> None:
    """Validate the identity and migration completeness of the global batch."""
    candidates = ingestion_records(documents)
    if len(candidates) != 10:
        reporter.error(
            f"G0 requires exactly 10 ingestion records; found {len(candidates)}"
        )
    for record in candidates:
        document_id = record.get("document_id", "<missing-id>")
        required = {
            "document_id",
            "title",
            "document_type",
            "version",
            "responsible",
            "registered_at",
            "last_verified_at",
            "current_path",
        }
        for field in sorted(required):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                reporter.error(f"{document_id}: G0 missing identity field {field}")
        if record.get("naming_conformance") is not True:
            reporter.error(f"{document_id}: G0 requires naming_conformance")
        if record.get("directory_conformance") is not True:
            reporter.error(f"{document_id}: G0 requires directory_conformance")
        if record.get("migration_required") is not False:
            reporter.error(f"{document_id}: G0 requires completed migration")
        scope = as_json_object(record.get("authority_scope"))
        if scope is None or not scope.get("subjects"):
            reporter.error(f"{document_id}: G0 requires authority scope")


def validate_g1(documents: list[JsonObject], reporter: Reporter) -> None:
    """Validate the immutable global ingestion snapshot and preservation TAR."""
    candidates = ingestion_records(documents)
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
        # O manifesto comprova os bytes da versão ingerida, preservados no
        # bundle. Ele não é um espelho mutável da revisão corrente. Enquanto a
        # versão registrada não avançar, exigimos igualdade com o snapshot; em
        # versão posterior, a integridade corrente é verificada pelo hash do
        # registro e a integridade histórica pelo bundle abaixo.
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


def validate_garch(
    documents: list[JsonObject],
    reporter: Reporter,
) -> None:
    """Enforce architectural conformance globally across registered records.

    G-ARCH is deliberately global: emitting document-scoped metadata would
    imply that uninspected records had no effect on the result.
    """
    for record in documents:
        document_id = record.get("document_id", "<missing-id>")
        if record.get("naming_conformance") is not True:
            reporter.error(
                f"{document_id}: G-ARCH requires naming_conformance"
            )
        if record.get("directory_conformance") is not True:
            reporter.error(
                f"{document_id}: G-ARCH requires directory_conformance"
            )
        if record.get("migration_required") is not False:
            reporter.error(
                f"{document_id}: G-ARCH requires completed migration"
            )


def validate_g2(
    documents: list[JsonObject],
    reporter: Reporter,
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


# ── G-FM: Front Matter ────────────────────────────────────────────────────────

FM_FEATURE_SPEC_GLOB = "src/features/**/*.md"

# Paths whose current_path matches are excluded from the governed profile.
_FM_EXCLUSIONS = re.compile(
    r"^(?:CLAUDE\.md|README\.md|\.inicio/|node_modules/|docs/archive/)"
)


class _DuplicateKeyLoader(yaml.SafeLoader):
    """SafeLoader that raises on duplicate mapping keys."""

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Any, Any]:
        seen: dict[Any, Any] = {}
        loader = cast(Any, self)
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in seen:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key: '{key}'",
                    key_node.start_mark,
                )
            seen[key] = True
        return super().construct_mapping(node, deep=deep)


def parse_front_matter(
    path: Path, profile: str, reporter: Reporter
) -> JsonObject | None:
    """Extract and validate the YAML front matter block from a Markdown file.

    Accepts only BOM-UTF-8 before the opening ``---``.  Returns the parsed
    mapping on success, or None after reporting every error found.
    """
    try:
        raw = path.read_bytes()
    except OSError as exc:
        reporter.error(f"{path}: cannot read: {exc}")
        return None

    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]

    if not raw.startswith(b"---"):
        reporter.error(f"{path}: front matter absent")
        return None

    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines(keepends=True)

    if lines[0].rstrip("\r\n") != "---":
        reporter.error(f"{path}: front matter absent")
        return None

    close_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            close_idx = i
            break

    if close_idx is None:
        reporter.error(f"{path}: front matter missing closing delimiter")
        return None

    yaml_block = "".join(lines[1:close_idx])

    try:
        data = yaml.load(yaml_block, Loader=_DuplicateKeyLoader)
    except yaml.YAMLError as exc:
        reporter.error(f"{path}: invalid YAML in front matter: {exc}")
        return None

    if data is None:
        reporter.error(f"{path}: front matter is empty")
        return None

    typed_data = as_json_object(data)
    if typed_data is None:
        reporter.error(f"{path}: front matter root must be a mapping")
        return None

    if profile == "governed":
        schema_path = config.FM_GOVERNED_SCHEMA
    elif profile == "feature-spec":
        schema_path = config.FM_FEATURE_SPEC_SCHEMA
    else:
        reporter.error(f"{path}: unknown front matter profile: {profile}")
        return None

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reporter.error(f"{path}: cannot load schema {schema_path.name}: {exc}")
        return None

    typed_schema = as_json_object(schema)
    if typed_schema is None:
        reporter.error(f"{path}: schema {schema_path.name} is not a mapping")
        return None
    schema_errors = contracts_module.schema_validation_errors(
        typed_schema,
        typed_data,
    )
    for err in schema_errors:
        field = ".".join(str(p) for p in err.absolute_path) or "(root)"
        reporter.error(f"{path}: front matter {field}: {err.message}")

    return typed_data if not schema_errors else None


def validate_governed(
    registered_doc: JsonObject, reporter: Reporter
) -> None:
    """Validate front matter of a governed .md document against the registry."""
    document_id = registered_doc.get("document_id", "<missing-id>")
    current_path = registered_doc.get("current_path", "")
    if not isinstance(current_path, str):
        reporter.error(f"{document_id}: governed current_path must be a string")
        return

    if _FM_EXCLUSIONS.match(current_path):
        return

    path = config.WORKSPACE_ROOT / current_path
    fm = parse_front_matter(path, "governed", reporter)
    if fm is None:
        return

    sync_fields = ("document_id", "title", "document_type", "version", "workflow_status")
    for field in sync_fields:
        expected = registered_doc.get(field)
        actual = fm.get(field)
        if actual != expected:
            reporter.error(
                f"{document_id}: front matter {field} '{actual}'"
                f" differs from registry '{expected}'"
            )

    reg_responsible = registered_doc.get("responsible")
    fm_responsible = fm.get("responsible")
    if reg_responsible and fm_responsible != reg_responsible:
        reporter.error(
            f"{document_id}: front matter responsible '{fm_responsible}'"
            f" differs from registry '{reg_responsible}'"
        )
    if fm_responsible and not reg_responsible:
        reporter.error(
            f"{document_id}: front matter has responsible but registry does not"
        )

    reg_scope = as_json_object(registered_doc.get("authority_scope")) or {}
    reg_permitted = {
        item
        for item in as_json_array(reg_scope.get("permitted_uses")) or []
        if isinstance(item, str)
    }
    reg_prohibited = {
        item
        for item in as_json_array(reg_scope.get("prohibited_uses")) or []
        if isinstance(item, str)
    }

    fm_permitted = {
        item
        for item in as_json_array(fm.get("permitted_uses")) or []
        if isinstance(item, str)
    }
    fm_prohibited = {
        item
        for item in as_json_array(fm.get("prohibited_uses")) or []
        if isinstance(item, str)
    }

    excess = fm_permitted - reg_permitted
    if excess:
        reporter.error(
            f"{document_id}: front matter permitted_uses contains"
            f" unauthorized entries: {sorted(excess)}"
        )

    missing = reg_prohibited - fm_prohibited
    if missing:
        reporter.error(
            f"{document_id}: front matter prohibited_uses missing"
            f" registry entries: {sorted(missing)}"
        )


def validate_feature_spec(path: Path, reporter: Reporter) -> None:
    """Validate front matter of a feature spec discovered via glob."""
    parse_front_matter(path, "feature-spec", reporter)


def validate_front_matter(
    documents: list[JsonObject],
    reporter: Reporter,
    document_id: str | None = None,
    version: str | None = None,
) -> None:
    """Gate G-FM: validate front matter for governed docs and feature specs."""
    governed_docs = [
        rec
        for rec in documents
        if isinstance(rec.get("current_path"), str)
        and rec["current_path"].endswith(".md")
        and not _FM_EXCLUSIONS.match(rec["current_path"])
    ]

    if document_id:
        selected = registry_module.resolve_document_version(
            documents,
            document_id,
            version,
            reporter,
        )
        if selected is None:
            return
        if selected not in governed_docs:
            reporter.error(
                f"G-FM found no governed Markdown for {document_id}"
                + (f" v{version}" if version else "")
            )
            return
        validate_governed(selected, reporter)
        return

    for rec in governed_docs:
        validate_governed(rec, reporter)

    for spec_path in sorted(
        config.WORKSPACE_ROOT.glob(FM_FEATURE_SPEC_GLOB)
    ):
        validate_feature_spec(spec_path, reporter)


def dispatch_gate(
    args: ValidatorArgs,
    documents: list[JsonObject],
    reporter: Reporter,
) -> None:
    """Dispatch one gate with its declared global or document scope."""
    if args.gate == "G-ARCH":
        validate_garch(documents, reporter)
    elif args.gate == "G0":
        validate_g0(documents, reporter)
    elif args.gate == "G1":
        validate_g1(documents, reporter)
    elif args.gate == "G2":
        validate_g2(
            documents,
            reporter,
            args.document_id,
            args.version,
        )
    elif args.gate == "G-FM":
        validate_front_matter(documents, reporter, args.document_id, args.version)


def main() -> int:
    """Run validation stages with fail-fast boundaries and one final emission.

    Each stage collects all of its own findings. Stopping before the next stage
    avoids producing secondary errors from inputs whose prerequisites already
    failed, while the single ``emit`` call keeps CLI output deterministic.
    """
    args = parse_args()
    reporter = reporter_module.Reporter()

    def finish() -> int:
        return reporter.emit(args.format, args.gate, args.result_id)

    if not validate_cli_args(args, reporter):
        return finish()
    strict_legacy = args.strict_legacy or args.gate == "G-ARCH"

    typed_data, documents = registry_module.load_registry(
        args.registry.resolve(),
        reporter,
    )
    if reporter.errors or typed_data is None:
        return finish()

    if args.document_id and registry_module.resolve_document_version(
        documents,
        args.document_id,
        args.version,
        reporter,
    ) is None:
        return finish()

    contracts_module.validate_contract_schemas(reporter)
    validate_instances(documents, reporter)
    if reporter.errors:
        return finish()

    registry_module.validate_registry_integrity(
        documents,
        reporter,
        strict_legacy,
    )
    if reporter.errors:
        return finish()

    registry_module.validate_canonical_registry(
        typed_data,
        documents,
        reporter,
    )
    if reporter.errors:
        return finish()

    dispatch_gate(args, documents, reporter)
    if reporter.errors:
        return finish()

    validate_links(reporter)
    return finish()
