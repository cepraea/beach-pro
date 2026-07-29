#!/usr/bin/env python3
"""Extract the legacy CEPRAEA source/claim matrix into a G2 package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re

import yaml


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_ID = "DOC-CEPRAEA-CANDIDATA-CONTEXTO"
REGISTRY_PATH = (
    WORKSPACE_ROOT / "docs/registry/registro-documentos.yaml"
)
OUTPUT_PATH = (
    WORKSPACE_ROOT
    / "docs/evidence/provenance/proveniencia-contexto-cepraea.yaml"
)
VERIFICATION_PATH = (
    WORKSPACE_ROOT
    / "docs/evidence/verifications/verificacoes-fontes-contexto-cepraea.yaml"
)
SOURCE_ENTRY_RE = re.compile(
    r"^- `(?P<id>SRC-[0-9]{3})` — (?P<body>.*?)(?=^- `SRC-[0-9]{3}` — |^## 13\.)",
    re.MULTILINE | re.DOTALL,
)
CLAIM_ENTRY_RE = re.compile(
    r"^### `(?P<id>CLAIM-[0-9]{3})`\n(?P<body>.*?)(?=^### `CLAIM-[0-9]{3}`|^## 14\.)",
    re.MULTILINE | re.DOTALL,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())


def field(body: str, label: str) -> str:
    match = re.search(
        rf"^- \*\*{re.escape(label)}:\*\* (?P<value>.*?)(?=^- \*\*|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    return normalize(match.group("value")) if match else ""


def source_authority(source_id: str) -> dict:
    known = {
        "SRC-001": (
            "Davi Sermenho",
            "AUTORIDADE_INTERNA",
            ["operacao_cepraea", "decisoes_documentais"],
        ),
        "SRC-013": (
            "Mapa das OSC/IPEA",
            "REGISTRO_PUBLICO",
            ["identidade_cadastral"],
        ),
        "SRC-014": (
            "Confederação Brasileira de Handebol",
            "REGISTRO_ESPORTIVO",
            ["identidade_esportiva"],
        ),
        "SRC-015": (
            "CEPRAEA no Instagram",
            "PUBLICACAO_PUBLICA",
            ["identidade_publica"],
        ),
        "SRC-016": (
            "CEPRAEA no Facebook",
            "PUBLICACAO_PUBLICA",
            ["identidade_publica"],
        ),
        "SRC-017": (
            "Cloudflare",
            "DOCUMENTACAO_OFICIAL",
            ["hospedagem"],
        ),
        "SRC-018": (
            "Supabase",
            "DOCUMENTACAO_OFICIAL",
            ["banco_auth_seguranca"],
        ),
        "SRC-019": (
            "Brevo",
            "DOCUMENTACAO_OFICIAL",
            ["email_smtp"],
        ),
        "SRC-020": (
            "GitHub",
            "DOCUMENTACAO_OFICIAL",
            ["repositorio_automacao"],
        ),
    }
    name, role, scope = known.get(
        source_id,
        ("Emissor não verificado", "FONTE_LEGADA", ["escopo_nao_verificado"]),
    )
    return {"name": name, "role": role, "scope": scope}


def source_type(source_id: str) -> str:
    if source_id == "SRC-001":
        return "human"
    if source_id in {"SRC-013", "SRC-014", "SRC-017", "SRC-018", "SRC-019", "SRC-020"}:
        return "official_record"
    return "document"


def source_location(
    source_id: str,
    body: str,
    document_path: str,
) -> str:
    file_id = re.search(r"\bArquivo ([A-Za-z0-9_-]+)", body)
    if file_id:
        return f"gdrive:{file_id.group(1)}"
    if source_id == "SRC-001":
        return f"{document_path}#src-001"
    return f"unresolved:{source_id}"


def source_classification(source_id: str) -> str:
    if source_id == "SRC-001":
        return "primary"
    if source_id == "SRC-002":
        return "candidate"
    if source_id in {"SRC-003", "SRC-004", "SRC-005"}:
        return "historical"
    return "supporting"


def build_sources(
    text: str,
    captured_at: str,
    document_path: str,
) -> list[dict]:
    sources: list[dict] = []
    for match in SOURCE_ENTRY_RE.finditer(text):
        source_id = match.group("id")
        description = normalize(match.group("body"))
        title = description.split(". Uso:", 1)[0].rstrip(".")
        sources.append(
            {
                "source_id": source_id,
                "title": title,
                "description": description,
                "source_type": source_type(source_id),
                "location": source_location(
                    source_id,
                    description,
                    document_path,
                ),
                "authority": source_authority(source_id),
                "captured_at": captured_at,
                "classification": source_classification(source_id),
                "content_hash": None,
                "status": "unverified",
                "immutable_reference": None,
                "verified_at": None,
                "verified_by": None,
                "permitted_uses": ["provenance_candidate"],
                "prohibited_uses": [
                    "use_as_verified_source_until_preserved"
                ],
            }
        )
    return sources


def claim_classification(legacy_state: str) -> str:
    if "INFERENCIA" in legacy_state:
        return "inference"
    if "PROBLEMA" in legacy_state or "IDENTIDADE_PUBLICA" in legacy_state:
        return "observation"
    return "fact"


def claim_subject(claim_id: str) -> str:
    subjects = {
        "CLAIM-001": "identidade_equipe",
        "CLAIM-002": "composicao_operacional",
        "CLAIM-003": "governanca_interna",
        "CLAIM-004": "operacao_as_is",
        "CLAIM-005": "incerteza_operacional",
        "CLAIM-006": "estado_operacional",
        "CLAIM-007": "disponibilidade_presenca",
        "CLAIM-008": "ciclo_participacao",
        "CLAIM-009": "governanca_interna",
        "CLAIM-010": "estado_de_propostas",
        "CLAIM-011": "integridade_de_fontes",
        "CLAIM-012": "decisoes_aprovadas",
        "CLAIM-013": "identidade_cadastral",
        "CLAIM-014": "identidade_esportiva",
        "CLAIM-015": "identidade_publica",
        "CLAIM-016": "perfis_e_acessos",
        "CLAIM-017": "capacidades_do_produto",
        "CLAIM-018": "escopo_fase_1",
        "CLAIM-019": "fronteiras_de_escopo",
        "CLAIM-020": "plataforma_cliente",
        "CLAIM-021": "identidade_e_acesso",
        "CLAIM-022": "privacidade_e_dados",
        "CLAIM-023": "integracoes_e_migracao",
        "CLAIM-024": "restricoes_operacionais",
        "CLAIM-025": "comunicacao_interna",
        "CLAIM-026": "modelo_de_respostas",
        "CLAIM-027": "privacidade_e_dados",
        "CLAIM-028": "arquitetura_inicial",
        "CLAIM-029": "entrega_e_continuidade",
        "CLAIM-030": "perfis_e_acessos",
    }
    return subjects[claim_id]


def apply_verification_overrides(package: dict) -> None:
    if not VERIFICATION_PATH.is_file():
        return
    data = yaml.safe_load(VERIFICATION_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("verification override must be a mapping")
    source_overrides = data.get("source_overrides", {})
    claim_overrides = data.get("claim_overrides", {})
    if not isinstance(source_overrides, dict) or not isinstance(
        claim_overrides, dict
    ):
        raise RuntimeError("verification overrides must be mappings")
    for source in package["sources"]:
        override = source_overrides.get(source["source_id"])
        if isinstance(override, dict):
            source.update(override)
    for claim in package["claims"]:
        override = claim_overrides.get(claim["claim_id"])
        if isinstance(override, dict):
            claim.update(override)


def build_claims(
    text: str,
    version: str,
    document_hash: str,
    document_path: str,
) -> list[dict]:
    claims: list[dict] = []
    for match in CLAIM_ENTRY_RE.finditer(text):
        claim_id = match.group("id")
        body = match.group("body")
        statement = field(body, "Descrição")
        legacy_state = field(body, "Estado")
        source_text = field(body, "Fontes / Evidências")
        source_ids = sorted(set(re.findall(r"SRC-[0-9]{3}", source_text)))
        decision_ids = sorted(
            set(re.findall(r"DEC-[0-9]{3}(?:-[A-Z])?", source_text))
        )
        evidence_ids = sorted(set(re.findall(r"EVID-[0-9]{3}", source_text)))
        uncertainty = (
            "controlled" if "INFERENCIA" in legacy_state else "none"
        )
        claims.append(
            {
                "claim_id": claim_id,
                "document_id": DOCUMENT_ID,
                "document_version": version,
                "document_hash": document_hash,
                "location": f"{document_path}#{claim_id.lower()}",
                "statement": statement,
                "legacy_state": legacy_state,
                "source_reference_text": source_text,
                "classification": claim_classification(legacy_state),
                "criticality": "critical",
                "subjects": [claim_subject(claim_id)],
                "source_ids": source_ids,
                "decision_ids": decision_ids,
                "evidence_ids": evidence_ids,
                "uncertainty": uncertainty,
                "uncertainty_reason": (
                    "Inferência controlada declarada no documento legado."
                    if uncertainty == "controlled"
                    else None
                ),
                "status": "candidate",
                "verified_at": None,
                "verified_by": None,
            }
        )
    return claims


def registry_record() -> dict:
    data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    for record in data["documents"]:
        if record.get("document_id") == DOCUMENT_ID:
            return record
    raise RuntimeError(f"document not registered: {DOCUMENT_ID}")


def registered_source_path(record: dict) -> tuple[Path, str]:
    current_path = record.get("current_path")
    if not isinstance(current_path, str):
        raise RuntimeError("registered document has no current_path")
    source_path = (WORKSPACE_ROOT / current_path).resolve()
    if not source_path.is_relative_to(WORKSPACE_ROOT):
        raise RuntimeError("registered current_path escapes the workspace")
    if not source_path.is_file():
        raise RuntimeError(
            f"registered source document does not exist: {current_path}"
        )
    return source_path, current_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    record = registry_record()
    source_path, document_path = registered_source_path(record)
    actual_hash = sha256(source_path)
    if record.get("content_hash") != actual_hash:
        raise RuntimeError("source document differs from G1 registry hash")
    created_at = datetime.now(timezone.utc).isoformat()
    if OUTPUT_PATH.is_file():
        existing = yaml.safe_load(OUTPUT_PATH.read_text(encoding="utf-8"))
        existing_package = (
            existing.get("provenance_package")
            if isinstance(existing, dict)
            else None
        )
        if (
            isinstance(existing_package, dict)
            and isinstance(existing_package.get("created_at"), str)
        ):
            created_at = existing_package["created_at"]
    text = source_path.read_text(encoding="utf-8")
    package = {
        "provenance_package": {
            "provenance_id": "PROV-CEPRAEA-CONTEXTO-001",
            "document_id": DOCUMENT_ID,
            "document_version": record["version"],
            "document_hash": actual_hash,
            "created_at": created_at,
            "created_by": "AUTOMACAO",
            "policy": {
                "critical_coverage_percent": 100,
                "require_active_sources": True,
                "reject_ambiguous_references": True,
            },
            "sources": build_sources(text, created_at, document_path),
            "claims": build_claims(
                text,
                record["version"],
                actual_hash,
                document_path,
            ),
        }
    }
    apply_verification_overrides(package["provenance_package"])
    rendered = yaml.safe_dump(
        package,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )
    if args.apply:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(rendered, encoding="utf-8")
        mode = "apply"
    else:
        mode = "dry-run"
    package_data = package["provenance_package"]
    print(
        f"sources={len(package_data['sources'])} "
        f"claims={len(package_data['claims'])} mode={mode}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
