"""Typed boundaries for dynamic JSON and YAML values."""

from __future__ import annotations

from typing import Any


JsonObject = dict[str, Any]


def _accept_dynamic_value(value: Any) -> Any:
    """Keep third-party parser and schema values inside one typed boundary."""
    return value


def _accept_dynamic_mapping(value: Any) -> JsonObject:
    """Mark a runtime-checked mapping as the YAML/JSON typing boundary."""
    return _accept_dynamic_value(value)


def as_json_object(value: Any) -> JsonObject | None:
    """Return a typed mapping only after its dynamic container is checked.

    PyYAML and ``json.loads`` intentionally return dynamic values. Centralizing
    this transition prevents ``Unknown`` from leaking through the validator
    while retaining the runtime check required for malformed input.
    """
    if not isinstance(value, dict):
        return None
    return _accept_dynamic_mapping(value)


def _accept_dynamic_array(value: Any) -> list[Any]:
    """Type a list only after the caller has checked its runtime container."""
    return _accept_dynamic_value(value)


def as_json_array(value: Any) -> list[Any] | None:
    """Return a dynamic JSON/YAML array after checking its container."""
    if not isinstance(value, list):
        return None
    return _accept_dynamic_array(value)
