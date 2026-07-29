---
document_id: DOC-CEPRAEA-DEC-AUTORIZACAO-SCHEMAS-FM
title: "DEC-FM-000 — Autorização dos schemas de front matter"
document_type: decisao
version: "0.1.0"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - autorizacao_fase0
  - criacao_schema_front_matter_governed
  - criacao_schema_front_matter_feature_spec
prohibited_uses:
  - autorizacao_outros_schemas
  - ativacao_g_fm_obrigatorio
  - alteracao_documento_schema
  - alteracao_workflow_schema
---

# DEC-FM-000 — Autorização dos schemas de front matter

## Identificação

| Campo         | Valor                                       |
| ------------- | ------------------------------------------- |
| Decisão       | DEC-FM-000                                  |
| Data          | 2026-07-28                                  |
| Autoridade    | Davi Sermenho                               |
| Status        | RASCUNHO                                    |

## Objeto da decisão

Autorizar a criação de dois contratos de schema JSON limitados ao sistema de
front matter YAML descrito em `.inicio/PLANO-FRONT-MATTER-AUTORITATIVO.md`:

1. `docs/contracts/schemas/front-matter-governed.schema.json`
   — schema de front matter para documentos do perfil `governed`
   (`docs/**/*.md` não excluídos).

2. `docs/contracts/schemas/front-matter-feature-spec.schema.json`
   — schema de front matter para feature specs do perfil `feature-spec`
   (`src/features/**/*.md`).

## Escopo

Esta autorização é estritamente limitada a estes dois schemas. Não autoriza:

- matrizes adicionais de schema
- manifesto de schemas
- schemas auxiliares não listados acima
- ativação obrigatória do gate G-FM (requer decisão separada — Fase 8)
- alteração de `documento.schema.json` ou `workflow.schema.json`

## Reconciliação com NOVOS_CONTRATOS

`NOVOS_CONTRATOS` permanece em `out_of_scope` no workflow
`docs/registry/workflow-documentacao.yaml`. Esta decisão constitui exceção
explícita e limitada: os dois schemas listados acima são autorizados como
contratos de infraestrutura do sistema de front matter, sem alterar o perfil
LEAN nem remover `NOVOS_CONTRATOS` do escopo geral.

Nenhuma outra criação de contrato está autorizada por esta decisão.

## Referências

- Plano autoritativo: `.inicio/PLANO-FRONT-MATTER-AUTORITATIVO.md`
- Seção 6 (Decisão mínima de autorização) e Seção 7, Fase 0
- Workflow vigente: `DOC-GOV-WF-DOCUMENTACAO` (`WF-DOC-CEPRAEA` v0.2.0)
