#!/usr/bin/env python3
"""Rewrite local Markdown links after the controlled legacy migration."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
from urllib.parse import unquote


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
TARGET_RE = re.compile(
    r"^(.*?\.md)(:[0-9]+)?(#[^\s]+)?$",
    re.IGNORECASE,
)
MAPPING = {
    "CONTEUDO DESC-CEPRAEA.md":
        "docs/sources/supporting/diretriz-conteudo-contexto-cepraea.md",
    "DESCRICAO-CEPRAEA.md":
        "docs/sources/primary/contexto-operacional-cepraea.md",
    "DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md":
        "docs/controlled/bases/contexto-cepraea-beach-pro.md",
    "DESCRICAO-CEPRAEA — VERSÃO CANDIDATA 0.1.md":
        "docs/canonical/context/contexto-cepraea-beach-pro.md",
    "PROTOCOLO-QUALIDADE-DOC.md":
        "docs/governance/protocols/protocolo-qualidade-documental.md",
    "VALIDACAO-CEPRAEA-v0.1.md":
        "docs/validation/reports/relatorio-validacao-contexto-cepraea.md",
    "RF-CEPRAEA-v0.1.md":
        "docs/derived/requirements/requisitos-funcionais-cepraea.md",
    "INVENTARIO-DOCS.md":
        "docs/inventario-documentos.md",
    "FLUXO-DOCS.md":
        "docs/governance/workflows/fluxo-documentacao-inicial.md",
    "planofluxo.md":
        "docs/governance/workflows/workflow-operacionalizacao-documental.md",
    "CONTEUDO DECISAO-CEPRAEA.md":
        "docs/sources/supporting/diretriz-conteudo-contexto-cepraea.md",
    "DECISAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md":
        "docs/controlled/bases/contexto-cepraea-beach-pro.md",
    "DECISAO-CEPRAEA — VERSÃO CANDIDATA 0.1.md":
        "docs/canonical/context/contexto-cepraea-beach-pro.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes. Without this option the script performs a dry run.",
    )
    return parser.parse_args()


def mapped_path(raw_path: str) -> Path | None:
    decoded = unquote(raw_path)
    candidate = Path(decoded)
    basename = candidate.name
    if basename in MAPPING:
        return (WORKSPACE_ROOT / MAPPING[basename]).resolve()

    if candidate.is_absolute():
        try:
            candidate.relative_to(WORKSPACE_ROOT)
        except ValueError:
            return None
        return candidate.resolve()
    return None


def rewrite_target(markdown_path: Path, raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("#") or "://" in target or target.startswith("mailto:"):
        return raw_target

    wrapped = target.startswith("<") and target.endswith(">")
    if wrapped:
        target = target[1:-1]

    match = TARGET_RE.match(target)
    if not match:
        return raw_target
    path_part, line_part, anchor_part = match.groups()

    destination = mapped_path(path_part)
    if destination is None:
        relative_candidate = (markdown_path.parent / unquote(path_part)).resolve()
        basename = Path(unquote(path_part)).name
        if basename in MAPPING:
            destination = (WORKSPACE_ROOT / MAPPING[basename]).resolve()
        elif relative_candidate.exists():
            destination = relative_candidate
        else:
            return raw_target

    try:
        destination.relative_to(WORKSPACE_ROOT)
    except ValueError:
        return raw_target

    relative = Path(os.path.relpath(destination, markdown_path.parent)).as_posix()
    suffix = f"{line_part or ''}{anchor_part or ''}"
    rendered = f"{relative}{suffix}"
    if " " in rendered:
        return f"<{rendered}>"
    return rendered


def process(path: Path, apply_changes: bool) -> int:
    original = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        label, raw_target = match.groups()
        return f"{label}({rewrite_target(path, raw_target)})"

    updated = LINK_RE.sub(replace, original)
    if updated == original:
        return 0
    print(path.relative_to(WORKSPACE_ROOT))
    if apply_changes:
        path.write_text(updated, encoding="utf-8")
    return 1


def main() -> int:
    args = parse_args()
    changed = 0
    for path in sorted(WORKSPACE_ROOT.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(WORKSPACE_ROOT).parts):
            continue
        changed += process(path, args.apply)
    print(f"changed_files={changed} mode={'apply' if args.apply else 'dry-run'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
