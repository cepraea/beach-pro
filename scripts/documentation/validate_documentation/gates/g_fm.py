"""Document-scoped Front Matter gate."""

from __future__ import annotations

from .. import config
from .. import front_matter as front_matter_module
from .. import registry as registry_module
from .. import reporter as reporter_module
from ..json_types import JsonObject


def validate_front_matter(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
    document_id: str | None = None,
    version: str | None = None,
) -> None:
    """Gate G-FM: validate front matter for governed docs and feature specs."""
    governed_docs = [
        rec
        for rec in documents
        if isinstance(rec.get("current_path"), str)
        and rec["current_path"].endswith(".md")
        and not front_matter_module.FM_EXCLUSIONS.match(rec["current_path"])
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
        front_matter_module.validate_governed(selected, reporter)
        return

    for rec in governed_docs:
        front_matter_module.validate_governed(rec, reporter)

    for spec_path in sorted(
        config.WORKSPACE_ROOT.glob(
            front_matter_module.FM_FEATURE_SPEC_GLOB
        )
    ):
        front_matter_module.validate_feature_spec(spec_path, reporter)
