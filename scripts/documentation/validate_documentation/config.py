"""Repository paths consumed by the documentation validator."""

from __future__ import annotations

from pathlib import Path


# This fixed depth preserves the behavior authorized for the current package
# layout. BEH-01 replaces it with marker-based discovery in the next change set.
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = WORKSPACE_ROOT / "docs/registry/registro-documentos.yaml"
DEFAULT_WORKFLOW = WORKSPACE_ROOT / "docs/registry/workflow-documentacao.yaml"
SCHEMA_ROOT = WORKSPACE_ROOT / "docs/contracts/schemas"
DOCUMENT_SCHEMA = SCHEMA_ROOT / "documento.schema.json"
WORKFLOW_SCHEMA = SCHEMA_ROOT / "workflow.schema.json"
GATE_RESULT_SCHEMA = SCHEMA_ROOT / "resultado-gate.schema.json"
INTEGRITY_MANIFEST_SCHEMA = SCHEMA_ROOT / "manifesto-integridade.schema.json"
INGESTION_SCHEMA = SCHEMA_ROOT / "ingestao.schema.json"
SOURCE_SCHEMA = SCHEMA_ROOT / "fonte.schema.json"
CLAIM_SCHEMA = SCHEMA_ROOT / "alegacao.schema.json"
PROVENANCE_SCHEMA = SCHEMA_ROOT / "proveniencia.schema.json"
DIVERGENCE_SCHEMA = SCHEMA_ROOT / "divergencia-integridade.schema.json"
CORRECTIVE_ACTION_SCHEMA = SCHEMA_ROOT / "acao-corretiva.schema.json"
WORKFLOW_EVENT_SCHEMA = SCHEMA_ROOT / "evento-workflow.schema.json"
APPROVAL_SCHEMA = SCHEMA_ROOT / "aprovacao.schema.json"
FM_GOVERNED_SCHEMA = SCHEMA_ROOT / "front-matter-governed.schema.json"
FM_FEATURE_SPEC_SCHEMA = SCHEMA_ROOT / "front-matter-feature-spec.schema.json"
INTEGRITY_MANIFEST = (
    WORKSPACE_ROOT / "docs/evidence/integrity/manifesto-integridade-legado.yaml"
)
