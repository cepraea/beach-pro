"""Registry identity, filesystem, and canonicality validation."""

from __future__ import annotations

from pathlib import Path
import re

import yaml

from . import config
from . import filesystem
from . import reporter as reporter_module
from .json_types import JsonObject, as_json_array, as_json_object


MANAGED_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".tar"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+\.(?:md|ya?ml)$")
SCHEMA_NAME_RE = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*\.schema\.json$"
)
EXPECTED_PATH_RE = {
    "contexto": re.compile(
        r"^docs/(?:sources/(?:primary|supporting)|"
        r"controlled/(?:bases|candidates)|canonical/context)/"
    ),
    "contrato": re.compile(r"^docs/contracts/schemas/"),
    "decisao": re.compile(r"^docs/(?:controlled|canonical/decisions)/"),
    "evidencia": re.compile(r"^docs/evidence/"),
    "fluxo": re.compile(r"^docs/governance/workflows/"),
    "glossario": re.compile(r"^docs/canonical/glossary/"),
    "inventario": re.compile(
        r"^docs/(?:README\.md|inventario-documentos\.md)$"
    ),
    "matriz": re.compile(r"^docs/governance/matrices/"),
    "politica": re.compile(
        r"^docs/(?:governance/policies|sources/supporting)/"
    ),
    "protocolo": re.compile(r"^docs/governance/protocols/"),
    "registro": re.compile(r"^docs/registry/"),
    "relatorio": re.compile(r"^docs/validation/reports/"),
    "requisito": re.compile(
        r"^docs/(?:derived/requirements|canonical/requirements)/"
    ),
    "workflow": re.compile(r"^docs/governance/workflows/"),
}
REQUIRED_FIELDS = {
    "document_id",
    "title",
    "document_type",
    "version",
    "registration_status",
    "workflow_status",
    "legacy_declared_status",
    "current_path",
    "target_path",
    "canonical_path",
    "content_hash",
    "self_hash_exempt",
    "naming_conformance",
    "directory_conformance",
    "migration_required",
    "authority_scope",
    "relationships",
}


def valid_name(path: Path) -> bool:
    if path.name == "README.md":
        return True
    if path.name.endswith(".schema.json"):
        return bool(SCHEMA_NAME_RE.fullmatch(path.name))
    if path.suffix == ".tar":
        return bool(
            re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+\.tar", path.name)
        )
    return bool(NAME_RE.fullmatch(path.name))


def validate_top_level(
    data: object,
    reporter: reporter_module.Reporter,
) -> list[JsonObject]:
    """Validate the registry envelope without hiding malformed documents."""
    typed_data = as_json_object(data)
    if typed_data is None:
        reporter.error("registry root must be a mapping")
        return []
    if not isinstance(typed_data.get("schema_version"), str):
        reporter.error("schema_version must be a string")
    registry = typed_data.get("registry")
    if not isinstance(registry, dict):
        reporter.error("registry metadata must be a mapping")
    raw_documents = as_json_array(typed_data.get("documents"))
    if raw_documents is None:
        reporter.error("documents must be a list")
        return []
    documents: list[JsonObject] = []
    for index, item in enumerate(raw_documents):
        typed_item = as_json_object(item)
        if typed_item is None:
            # Continue after the error so valid siblings still receive diagnostics.
            reporter.error(f"documents[{index}] must be a mapping")
            continue
        documents.append(typed_item)
    return documents


def resolve_document_version(
    documents: list[JsonObject],
    document_id: str,
    version: str | None,
    reporter: reporter_module.Reporter,
) -> JsonObject | None:
    """Resolve one immutable document version without first-match ambiguity.

    ``document_id`` is permanent and can legitimately coexist in the registry
    at several versions.  Therefore absence of ``version`` is accepted only
    when exactly one record matches.
    """
    matches = [
        record
        for record in documents
        if record.get("document_id") == document_id
    ]
    if not matches:
        reporter.error(f"unknown document_id: {document_id}")
        return None

    if version is None:
        if len(matches) != 1:
            reporter.error(
                f"{document_id} has multiple versions; --version is required"
            )
            return None
        selected = matches[0]
    else:
        exact_matches = [
            record for record in matches if record.get("version") == version
        ]
        if len(exact_matches) != 1:
            reporter.error(
                f"unknown document version: {document_id} v{version}"
            )
            return None
        selected = exact_matches[0]

    selected_version = selected.get("version")
    selected_hash = selected.get("content_hash")
    reporter.document_id = document_id
    reporter.version = (
        selected_version if isinstance(selected_version, str) else None
    )
    reporter.content_hash = (
        selected_hash if isinstance(selected_hash, str) else None
    )
    return selected


def validate_record(
    record: JsonObject,
    reporter: reporter_module.Reporter,
    strict_legacy: bool,
) -> tuple[str | None, str | None]:
    """Validate one registry record while retaining sibling diagnostics.

    Missing metadata is accumulated whenever later checks remain safe. Path
    failures return early because hash, naming, and directory conclusions would
    otherwise be derived from bytes that were not resolved inside the
    workspace.
    """
    missing = REQUIRED_FIELDS - record.keys()
    raw_document_id = record.get("document_id")
    document_id = (
        raw_document_id
        if isinstance(raw_document_id, str)
        else "<missing-id>"
    )
    for field in sorted(missing):
        reporter.error(f"{document_id}: missing field {field}")

    current_path = record.get("current_path")
    if not isinstance(current_path, str):
        reporter.error(f"{document_id}: current_path must be a string")
        return None, None

    absolute_path = filesystem.workspace_path(current_path, reporter)
    if absolute_path is None:
        return document_id, current_path
    if not absolute_path.is_file():
        reporter.error(f"{document_id}: file not found: {current_path}")
        return document_id, current_path

    registration_status = record.get("registration_status")
    is_legacy = registration_status == "LEGADO_INVENTARIADO"
    workflow_status = record.get("workflow_status")
    if is_legacy and workflow_status is not None:
        reporter.error(
            f"{document_id}: legacy record must not infer workflow_status"
        )
    if not is_legacy and workflow_status is None:
        reporter.error(
            f"{document_id}: controlled record requires workflow_status"
        )

    expected_hash = record.get("content_hash")
    self_hash_exempt = record.get("self_hash_exempt") is True
    if self_hash_exempt:
        if current_path != "docs/registry/registro-documentos.yaml":
            reporter.error(
                f"{document_id}: self_hash_exempt is restricted to the registry"
            )
    elif not isinstance(expected_hash, str):
        reporter.error(f"{document_id}: content_hash must be a SHA-256 string")
    else:
        actual_hash = filesystem.sha256(absolute_path)
        if expected_hash != actual_hash:
            reporter.error(
                f"{document_id}: hash mismatch for {current_path}; "
                f"expected {expected_hash}, actual {actual_hash}"
            )

    actual_name_conformance = valid_name(absolute_path)
    declared_name_conformance = record.get("naming_conformance")
    if declared_name_conformance is not actual_name_conformance:
        reporter.error(
            f"{document_id}: naming_conformance does not match filename"
        )
    if not actual_name_conformance:
        message = (
            f"{document_id}: legacy filename requires migration: "
            f"{current_path}"
        )
        if strict_legacy or not is_legacy and not record.get(
            "migration_required"
        ):
            reporter.error(message)
        else:
            reporter.warning(message)

    document_type = record.get("document_type")
    expected_path_re = (
        EXPECTED_PATH_RE.get(document_type)
        if isinstance(document_type, str)
        else None
    )
    _terminal = workflow_status in ("SUPERADA", "REVOGADA")
    if record.get("directory_conformance") is True and expected_path_re:
        if not _terminal and not expected_path_re.match(current_path):
            reporter.error(
                f"{document_id}: directory incompatible with document_type"
            )
    if record.get("directory_conformance") is False:
        message = (
            f"{document_id}: legacy directory requires migration: "
            f"{current_path}"
        )
        if strict_legacy or not record.get("migration_required"):
            reporter.error(message)
        else:
            reporter.warning(message)

    canonical_path = record.get("canonical_path")
    if workflow_status == "CANONICA_VIGENTE":
        if not isinstance(canonical_path, str):
            reporter.error(
                f"{document_id}: canonical document requires canonical_path"
            )
        elif canonical_path != current_path:
            reporter.error(
                f"{document_id}: active canonical paths must be identical"
            )
    elif canonical_path is not None and workflow_status not in {
        "SUPERADA",
        "REVOGADA",
    }:
        reporter.error(
            f"{document_id}: canonical_path set without canonical history"
        )

    return document_id, current_path


def validate_uniqueness(
    id_version_pairs: list[tuple[str, str]],
    paths: list[str],
    reporter: reporter_module.Reporter,
) -> None:
    duplicates = sorted(
        {p for p in id_version_pairs if id_version_pairs.count(p) > 1}
    )
    for doc_id, version in duplicates:
        reporter.error(
            f"duplicate (document_id, version): ({doc_id}, {version})"
        )

    for value in sorted({v for v in paths if paths.count(v) > 1}):
        reporter.error(f"duplicate current_path: {value}")

    folded: dict[str, str] = {}
    for path in paths:
        key = path.casefold()
        if key in folded and folded[key] != path:
            reporter.error(
                f"case-insensitive path collision: {folded[key]} <> {path}"
            )
        folded[key] = path


def managed_files() -> set[str]:
    docs_root = config.WORKSPACE_ROOT / "docs"
    return {
        path.relative_to(config.WORKSPACE_ROOT).as_posix()
        for path in docs_root.rglob("*")
        if (
            path.is_file()
            and not path.is_symlink()
            and path.suffix.lower() in MANAGED_SUFFIXES
        )
    }


def validate_canonical_registry(
    data: JsonObject,
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    registry = as_json_object(data.get("registry")) or {}
    declared = as_json_array(registry.get("canonical_documents"))
    if declared is None:
        reporter.error("registry.canonical_documents must be a list")
        return
    actual: list[str] = []
    for record in documents:
        document_id = record.get("document_id")
        if (
            record.get("workflow_status") == "CANONICA_VIGENTE"
            and isinstance(document_id, str)
        ):
            actual.append(document_id)
    declared_ids: list[str] = [
        item for item in declared if isinstance(item, str)
    ]
    if sorted(declared_ids) != sorted(actual):
        reporter.error(
            "canonical_documents differs from CANONICA_VIGENTE records"
        )


def load_registry(
    registry_path: Path,
    reporter: reporter_module.Reporter,
) -> tuple[JsonObject | None, list[JsonObject]]:
    """Load and narrow the registry before any downstream validation."""
    if not registry_path.is_file():
        reporter.error(f"registry not found: {registry_path}")
        return None, []
    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        reporter.error(f"cannot load registry: {error}")
        return None, []

    documents = validate_top_level(data, reporter)
    typed_data = as_json_object(data)
    return typed_data, documents


def validate_registry_integrity(
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
    strict_legacy: bool,
) -> None:
    """Validate record bytes, uniqueness, and filesystem registration."""
    id_version_pairs: list[tuple[str, str]] = []
    paths: list[str] = []
    for record in documents:
        document_id, current_path = validate_record(
            record,
            reporter,
            strict_legacy,
        )
        if document_id:
            version = record.get("version", "")
            id_version_pairs.append((document_id, str(version)))
        if current_path:
            paths.append(current_path)

    validate_uniqueness(id_version_pairs, paths, reporter)

    registered_files = set(paths)
    for orphan in sorted(managed_files() - registered_files):
        reporter.error(f"unregistered documentation file: {orphan}")
    for missing in sorted(registered_files - managed_files()):
        reporter.error(f"registered path outside managed files: {missing}")
