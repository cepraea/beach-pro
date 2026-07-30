"""Deterministic result collection and output for documentation validation."""

from __future__ import annotations

from datetime import datetime, timezone

import yaml

from .json_types import JsonObject


class Reporter:
    """Collect deterministic validation results."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.document_id: str | None = None
        self.version: str | None = None
        self.content_hash: str | None = None

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def emit(
        self,
        output_format: str = "text",
        gate_id: str | None = None,
        result_id: str | None = None,
    ) -> int:
        """Emit the only user-facing output and return the process status.

        Sorting failures makes repeated runs comparable even when filesystem
        discovery order differs.  ``result_id`` is explicit because the
        ``RUNTIME`` fallback is diagnostic output, not a persistable identity.
        """
        if output_format == "yaml":
            status = "pass" if not self.errors else "fail"
            effective_gate_id = gate_id or "G-VALIDATION"
            result: JsonObject = {
                "gate_result": {
                    "gate_result_id": (
                        result_id
                        or f"GATE-RESULT-{effective_gate_id}-RUNTIME"
                    ),
                    "gate_id": effective_gate_id,
                    "document_id": self.document_id,
                    "version": self.version,
                    "content_hash": self.content_hash,
                    "status": status,
                    "evaluated_at": datetime.now(timezone.utc).isoformat(),
                    "evaluator": "scripts.documentation.validate_documentation",
                    "evaluator_role": "AUTOMACAO",
                    "evidence_ids": [],
                    "failures": sorted(self.errors),
                    "next_actions": (
                        []
                        if not self.errors
                        else ["Corrigir todas as falhas antes de nova execução."]
                    ),
                }
            }
            print(
                yaml.safe_dump(
                    result,
                    allow_unicode=True,
                    sort_keys=False,
                ).rstrip()
            )
            return 1 if self.errors else 0

        for message in sorted(self.errors):
            print(f"ERROR: {message}")
        for message in sorted(self.warnings):
            print(f"WARNING: {message}")
        print(
            "SUMMARY: "
            f"errors={len(self.errors)} warnings={len(self.warnings)}"
        )
        return 1 if self.errors else 0
