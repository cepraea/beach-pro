"""Global ingestion-identity gate."""

from __future__ import annotations

from .. import ingestion as ingestion_module
from .. import reporter as reporter_module
from ..json_types import JsonObject, as_json_object


def validate_g0(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    """Validate the identity and migration completeness of the global batch."""
    candidates = ingestion_module.ingestion_records(documents)
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
