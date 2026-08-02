"""Fail-fast orchestration of documentary validation stages."""

from __future__ import annotations

from . import contracts as contracts_module
from . import instances as instances_module
from . import links as links_module
from . import registry as registry_module
from . import reporter as reporter_module
from .gates import dispatcher as dispatcher_module
from .models import ValidatorArgs


def run_validation(
    args: ValidatorArgs,
    reporter: reporter_module.Reporter,
) -> None:
    """Run documentary stages without creating or emitting a Reporter.

    Each stage collects all of its own findings. Returning before the next
    stage prevents secondary errors from inputs whose prerequisites failed;
    emission remains exclusively under CLI control.
    """
    strict_legacy = args.strict_legacy or args.gate == "G-ARCH"

    typed_data, documents = registry_module.load_registry(
        args.registry.resolve(),
        reporter,
    )
    if reporter.errors or typed_data is None:
        return

    if args.document_id and registry_module.resolve_document_version(
        documents,
        args.document_id,
        args.version,
        reporter,
    ) is None:
        return

    contracts_module.validate_contract_schemas(reporter)
    instances_module.validate_instances(documents, reporter)
    if reporter.errors:
        return

    registry_module.validate_registry_integrity(
        documents,
        reporter,
        strict_legacy,
    )
    if reporter.errors:
        return

    registry_module.validate_canonical_registry(
        typed_data,
        documents,
        reporter,
    )
    if reporter.errors:
        return

    dispatcher_module.dispatch_gate(args, documents, reporter)
    if reporter.errors:
        return

    links_module.validate_links(reporter)
