"""Global architectural-conformance gate."""

from __future__ import annotations

from .. import reporter as reporter_module
from ..json_types import JsonObject


def validate_garch(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
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
