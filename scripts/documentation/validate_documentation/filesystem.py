"""Filesystem boundaries shared by documentation validation stages."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from . import config

if TYPE_CHECKING:
    from . import reporter as reporter_module


def workspace_path(
    raw_path: str,
    reporter: reporter_module.Reporter,
) -> Path | None:
    """Resolve a repository path without allowing it to escape the workspace."""
    candidate = (config.WORKSPACE_ROOT / raw_path).resolve()
    try:
        candidate.relative_to(config.WORKSPACE_ROOT)
    except ValueError:
        reporter.error(f"path escapes workspace: {raw_path}")
        return None
    return candidate


def sha256(path: Path) -> str:
    """Calculate SHA-256 in bounded chunks to avoid loading large TARs."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
