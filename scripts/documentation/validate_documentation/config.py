"""Repository paths consumed by the documentation validator."""

from __future__ import annotations

from pathlib import Path


_WORKSPACE_FILE_MARKERS = (
    Path("docs/registry/registro-documentos.yaml"),
    Path("docs/registry/workflow-documentacao.yaml"),
    Path("docs/contracts/schemas/documento.schema.json"),
)
_WORKSPACE_DIRECTORY_MARKERS = (
    Path("scripts/documentation/validate_documentation"),
)
_WORKSPACE_MARKERS = (
    *_WORKSPACE_FILE_MARKERS,
    *_WORKSPACE_DIRECTORY_MARKERS,
)


def find_workspace_root(start: Path | None = None) -> Path:
    """Find the nearest complete documentation workspace.

    Requiring the registry, workflow, base schema, and validator package
    together prevents an unrelated ancestor with a generic ``docs`` directory
    from being accepted as the repository root.
    """
    current = (start if start is not None else Path(__file__)).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        has_files = all(
            (candidate / marker).is_file()
            for marker in _WORKSPACE_FILE_MARKERS
        )
        has_directories = all(
            (candidate / marker).is_dir()
            for marker in _WORKSPACE_DIRECTORY_MARKERS
        )
        if has_files and has_directories:
            return candidate

    markers = ", ".join(str(marker) for marker in _WORKSPACE_MARKERS)
    raise RuntimeError(
        "Não foi possível localizar o workspace documental. "
        f"Marcadores obrigatórios: {markers}"
    )


WORKSPACE_ROOT = find_workspace_root()
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
