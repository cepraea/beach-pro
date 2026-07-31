"""Validate the CEPRAEA documentation registry and filesystem."""

from __future__ import annotations

from . import approvals as approvals_module
from . import cli as cli_module
from . import config
from . import contracts as contracts_module
from . import filesystem
from . import front_matter as front_matter_module
from . import ingestion as ingestion_module
from . import instances as instances_module
from . import links as links_module
from . import provenance as provenance_module
from . import pipeline as pipeline_module
from . import reporter as reporter_module
from . import registry as registry_module
from . import workflow as workflow_module
from .gates import g_arch as g_arch_module
from .gates import g0 as g0_module
from .gates import g1 as g1_module
from .gates import g2 as g2_module
from .gates import g_fm as g_fm_module
from .gates import dispatcher as dispatcher_module
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
dispatch_gate = dispatcher_module.dispatch_gate
run_validation = pipeline_module.run_validation
parse_args = cli_module.parse_args
validate_cli_args = cli_module.validate_cli_args
main = cli_module.main
