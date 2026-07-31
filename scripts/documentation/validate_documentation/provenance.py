"""Structural validation for provenance packages, sources, and claims."""

from __future__ import annotations

import yaml

from . import config
from . import contracts as contracts_module
from . import reporter as reporter_module
from .json_types import as_json_array, as_json_object


def validate_provenance_packages(
    reporter: reporter_module.Reporter,
) -> None:
    """Validate nested provenance contracts before G2 resolves relationships."""
    provenance_root = config.WORKSPACE_ROOT / "docs/evidence/provenance"
    package_schema = as_json_object(
        contracts_module.load_json(config.PROVENANCE_SCHEMA, reporter)
    )
    source_schema = as_json_object(
        contracts_module.load_json(config.SOURCE_SCHEMA, reporter)
    )
    claim_schema = as_json_object(
        contracts_module.load_json(config.CLAIM_SCHEMA, reporter)
    )
    if (
        package_schema is None
        or source_schema is None
        or claim_schema is None
    ):
        return
    for package_path in sorted(provenance_root.glob("*.yaml")):
        try:
            data = yaml.safe_load(package_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            reporter.error(f"cannot load provenance package: {error}")
            continue
        data_mapping = as_json_object(data)
        package = as_json_object(
            data_mapping.get("provenance_package")
            if data_mapping is not None
            else None
        )
        relative = package_path.relative_to(config.WORKSPACE_ROOT)
        for error in contracts_module.schema_validation_errors(
            package_schema,
            package,
        ):
            location = ".".join(str(part) for part in error.absolute_path)
            reporter.error(
                f"{relative}: provenance contract failure at "
                f"{location or '<root>'}: {error.message}"
            )
        if package is None:
            continue
        sources = as_json_array(package.get("sources")) or []
        for index, source in enumerate(sources):
            for error in contracts_module.schema_validation_errors(
                source_schema,
                source,
            ):
                location = ".".join(str(part) for part in error.absolute_path)
                reporter.error(
                    f"{relative}: source[{index}] contract failure at "
                    f"{location or '<root>'}: {error.message}"
                )
        claims = as_json_array(package.get("claims")) or []
        for index, claim in enumerate(claims):
            for error in contracts_module.schema_validation_errors(
                claim_schema,
                claim,
            ):
                location = ".".join(str(part) for part in error.absolute_path)
                reporter.error(
                    f"{relative}: claim[{index}] contract failure at "
                    f"{location or '<root>'}: {error.message}"
                )
