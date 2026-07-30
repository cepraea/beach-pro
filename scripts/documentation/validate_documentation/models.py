"""Domain models shared by the documentation validator."""

from __future__ import annotations

import argparse
from pathlib import Path


class ValidatorArgs(argparse.Namespace):
    """Typed command-line values consumed by the validation orchestrator."""

    registry: Path
    strict_legacy: bool
    gate: str | None
    document_id: str | None
    version: str | None
    format: str
    result_id: str | None
