"""Validate the CEPRAEA documentation registry and filesystem."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from . import approvals as approvals_module
from . import config
from . import contracts as contracts_module
from . import filesystem
from . import front_matter as front_matter_module
from . import ingestion as ingestion_module
from . import instances as instances_module
from . import links as links_module
from . import provenance as provenance_module
from . import reporter as reporter_module
from . import registry as registry_module
from . import workflow as workflow_module
from .gates import g_arch as g_arch_module
from .gates import g0 as g0_module
from .gates import g1 as g1_module
from .gates import g2 as g2_module
from .gates import g_fm as g_fm_module
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
validate_approval_cross_references = (
    approvals_module.validate_approval_cross_references
)
validate_provenance_packages = provenance_module.validate_provenance_packages
ingestion_records = ingestion_module.ingestion_records
validate_ingestion_consistency = (
    ingestion_module.validate_ingestion_consistency
)
validate_document_instances = instances_module.validate_document_instances
validate_workflow_instance = instances_module.validate_workflow_instance
validate_gate_result_instances = instances_module.validate_gate_result_instances
validate_evidence_instances = instances_module.validate_evidence_instances
validate_instances = instances_module.validate_instances
parse_front_matter = front_matter_module.parse_front_matter
validate_governed = front_matter_module.validate_governed
validate_feature_spec = front_matter_module.validate_feature_spec
normalize_link_target = links_module.normalize_link_target
validate_links = links_module.validate_links
validate_garch = g_arch_module.validate_garch
validate_g0 = g0_module.validate_g0
validate_g1 = g1_module.validate_g1
validate_g2 = g2_module.validate_g2
validate_front_matter = g_fm_module.validate_front_matter
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


def dispatch_gate(
    args: ValidatorArgs,
    documents: list[JsonObject],
    reporter: Reporter,
) -> None:
    """Dispatch one gate with its declared global or document scope."""
    if args.gate == "G-ARCH":
        g_arch_module.validate_garch(documents, reporter)
    elif args.gate == "G0":
        g0_module.validate_g0(documents, reporter)
    elif args.gate == "G1":
        g1_module.validate_g1(documents, reporter)
    elif args.gate == "G2":
        g2_module.validate_g2(
            documents,
            reporter,
            args.document_id,
            args.version,
        )
    elif args.gate == "G-FM":
        g_fm_module.validate_front_matter(
            documents,
            reporter,
            args.document_id,
            args.version,
        )


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
    instances_module.validate_instances(documents, reporter)
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

    links_module.validate_links(reporter)
    return finish()
