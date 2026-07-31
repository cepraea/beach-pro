"""Validation of document, workflow, gate-result, and evidence instances."""

from __future__ import annotations

import yaml

from . import approvals as approvals_module
from . import config
from . import contracts as contracts_module
from . import filesystem
from . import ingestion as ingestion_module
from . import provenance as provenance_module
from . import reporter as reporter_module
from . import workflow as workflow_module
from .json_types import JsonObject, as_json_array, as_json_object


def validate_document_instances(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
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


def validate_workflow_instance(
    reporter: reporter_module.Reporter,
) -> None:
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
        workflow_module.validate_workflow_references(
            typed_workflow,
            reporter,
        )

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


def validate_gate_result_instances(
    reporter: reporter_module.Reporter,
) -> None:
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
    reporter: reporter_module.Reporter,
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
    ingestion_module.validate_ingestion_consistency(documents, reporter)
    provenance_module.validate_provenance_packages(reporter)
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
    approvals_module.validate_approval_cross_references(documents, reporter)


def validate_instances(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    """Orchestrate independent instance families in dependency order."""
    validate_document_instances(documents, reporter)
    validate_workflow_instance(reporter)
    validate_gate_result_instances(reporter)
    validate_evidence_instances(documents, reporter)
