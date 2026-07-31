"""Command-line interface for the documentation validator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
import re

from . import config
from . import pipeline as pipeline_module
from . import reporter as reporter_module
from .models import ValidatorArgs


GLOBAL_GATES = {"G-ARCH", "G0", "G1"}


def parse_args(argv: Sequence[str] | None = None) -> ValidatorArgs:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=config.DEFAULT_REGISTRY,
        help="Registry path; defaults to the controlled CEPRAEA registry.",
    )
    parser.add_argument(
        "--strict-legacy",
        action="store_true",
        help="Treat known legacy naming and directory deviations as errors.",
    )
    parser.add_argument(
        "--gate",
        choices=["G-ARCH", "G0", "G1", "G2", "G-FM"],
        help="Execute a named blocking gate.",
    )
    parser.add_argument(
        "--document-id",
        help="Restrict a document-scoped gate to this document ID.",
    )
    parser.add_argument(
        "--version",
        help="Restrict a document-scoped gate to this version.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "yaml"],
        default="text",
        help="Output format; YAML emits a processable gate result.",
    )
    parser.add_argument(
        "--result-id",
        help=(
            "Explicit GATE-RESULT-* identity for YAML that will be persisted; "
            "the default RUNTIME identity is diagnostic only."
        ),
    )
    args = ValidatorArgs()
    parser.parse_args(argv, namespace=args)
    return args


def validate_cli_args(
    args: ValidatorArgs,
    reporter: reporter_module.Reporter,
) -> bool:
    """Reject argument combinations whose scope has no defined semantics."""
    if args.version and not args.document_id:
        reporter.error("--version requires --document-id")
    if args.gate in GLOBAL_GATES and (args.document_id or args.version):
        reporter.error(f"{args.gate} is global and does not accept document scope")
    if args.document_id and args.gate not in {"G2", "G-FM"}:
        reporter.error("--document-id requires gate G2 or G-FM")
    if args.result_id and not re.fullmatch(
        r"GATE-RESULT-[A-Z0-9-]+", args.result_id
    ):
        reporter.error("--result-id must match GATE-RESULT-[A-Z0-9-]+")
    return not reporter.errors


def main(argv: Sequence[str] | None = None) -> int:
    """Validate CLI input, run the pipeline, and emit exactly once."""
    args = parse_args(argv)
    reporter = reporter_module.Reporter()

    if validate_cli_args(args, reporter):
        pipeline_module.run_validation(args, reporter)

    return reporter.emit(args.format, args.gate, args.result_id)
