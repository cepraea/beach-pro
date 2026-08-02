"""JSON Schema loading and validation boundaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
import yaml

from . import config
from . import reporter as reporter_module
from .json_types import JsonObject, as_json_object


def load_json(path: Path, reporter: reporter_module.Reporter) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        reporter.error(
            "cannot load JSON "
            f"{path.relative_to(config.WORKSPACE_ROOT)}: {error}"
        )
        return None


def validate_schema_definition(
    schema: JsonObject,
    schema_path: Path,
    reporter: reporter_module.Reporter,
) -> None:
    """Check a schema while isolating incomplete jsonschema type metadata."""
    validator_class = cast(Any, Draft202012Validator)
    try:
        validator_class.check_schema(schema)
    except SchemaError as error:
        relative = schema_path.relative_to(config.WORKSPACE_ROOT)
        reporter.error(f"invalid JSON Schema {relative}: {error.message}")


def schema_validation_errors(
    schema: JsonObject,
    instance: Any,
) -> list[Any]:
    """Return deterministic errors from the dynamically typed library edge."""
    validator_class = cast(Any, Draft202012Validator)
    format_checker = cast(Any, FormatChecker())
    validator: Any = validator_class(
        schema,
        format_checker=format_checker,
    )
    errors: list[Any] = list(validator.iter_errors(instance))
    return sorted(errors, key=lambda item: list(item.absolute_path))


def validate_contract_schemas(reporter: reporter_module.Reporter) -> None:
    if not config.SCHEMA_ROOT.is_dir():
        reporter.error("schema directory not found")
        return
    for schema_path in sorted(config.SCHEMA_ROOT.glob("*.schema.json")):
        schema = as_json_object(load_json(schema_path, reporter))
        if schema is None:
            continue
        validate_schema_definition(schema, schema_path, reporter)


def validate_yaml_instance(
    instance_path: Path,
    schema_path: Path,
    wrapper_key: str | None,
    label: str,
    reporter: reporter_module.Reporter,
) -> None:
    if not instance_path.is_file():
        return
    schema = as_json_object(load_json(schema_path, reporter))
    if schema is None:
        return
    try:
        data = yaml.safe_load(instance_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        reporter.error(f"cannot load {label} {instance_path}: {error}")
        return
    data_mapping = as_json_object(data)
    instance = (
        data_mapping.get(wrapper_key)
        if wrapper_key and data_mapping is not None
        else data
    )
    for error in schema_validation_errors(schema, instance):
        relative = instance_path.relative_to(config.WORKSPACE_ROOT)
        location = ".".join(str(part) for part in error.absolute_path)
        reporter.error(
            f"{relative}: {label} contract failure at "
            f"{location or '<root>'}: {error.message}"
        )
