"""Parsing and validation of governed Markdown front matter."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, cast

import yaml

from . import config
from . import contracts as contracts_module
from . import reporter as reporter_module
from .json_types import JsonObject, as_json_array, as_json_object


FM_FEATURE_SPEC_GLOB = "src/features/**/*.md"

# Paths whose current_path matches are excluded from the governed profile.
_FM_EXCLUSIONS = re.compile(
    r"^(?:CLAUDE\.md|README\.md|\.inicio/|node_modules/|docs/archive/)"
)
# G-FM remains in the package facade until Phase 9 and needs a public,
# patch-stable lookup without reaching into this module's private namespace.
FM_EXCLUSIONS = _FM_EXCLUSIONS


class _DuplicateKeyLoader(yaml.SafeLoader):
    """SafeLoader that raises on duplicate mapping keys."""

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Any, Any]:
        seen: dict[Any, Any] = {}
        loader = cast(Any, self)
        for key_node, _ in node.value:
            # YAML permits collection keys, but the controlled front matter
            # contract requires scalar field names and duplicate tracking
            # cannot safely index mutable collection values.
            if not isinstance(key_node, yaml.ScalarNode):
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unsupported complex mapping key",
                    key_node.start_mark,
                )
            key = loader.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unhashable mapping key",
                    key_node.start_mark,
                ) from exc
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
    path: Path,
    profile: str,
    reporter: reporter_module.Reporter,
) -> JsonObject | None:
    """Extract and validate the YAML front matter block from a Markdown file.

    Accepts only BOM-UTF-8 before the opening ``---``. Returns the parsed
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

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        # Replacement characters would allow different source bytes to be
        # validated as if they represented the same governed text.
        reporter.error(f"{path}: invalid UTF-8: {exc}")
        return None
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
    registered_doc: JsonObject,
    reporter: reporter_module.Reporter,
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

    sync_fields = (
        "document_id",
        "title",
        "document_type",
        "version",
        "workflow_status",
    )
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


def validate_feature_spec(
    path: Path,
    reporter: reporter_module.Reporter,
) -> None:
    """Validate front matter of a feature spec discovered via glob."""
    parse_front_matter(path, "feature-spec", reporter)
