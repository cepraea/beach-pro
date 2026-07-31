"""Scope-aware dispatcher for blocking documentation gates."""

from __future__ import annotations

from .. import reporter as reporter_module
from ..json_types import JsonObject
from ..models import ValidatorArgs
from . import g_arch as g_arch_module
from . import g0 as g0_module
from . import g1 as g1_module
from . import g2 as g2_module
from . import g_fm as g_fm_module


def dispatch_gate(
    args: ValidatorArgs,
    documents: list[JsonObject],
    reporter: reporter_module.Reporter,
) -> None:
    """Dispatch one gate with its declared global or document scope."""
    if args.gate == "G-ARCH":
        g_arch_module.validate_garch(documents, reporter)
    elif args.gate == "G0":
        g0_module.validate_g0(documents, reporter)
    elif args.gate == "G1":
        g1_module.validate_g1(documents, reporter)
    elif args.gate == "G2":
        g2_module.validate_g2(
            documents,
            reporter,
            args.document_id,
            args.version,
        )
    elif args.gate == "G-FM":
        g_fm_module.validate_front_matter(
            documents,
            reporter,
            args.document_id,
            args.version,
        )
