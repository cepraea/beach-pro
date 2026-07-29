---
document_id: DOC-CEPRAEA-DEC-MODELO-VERSOES
title: "Autorização do modelo de versões simultâneas"
document_type: decisao
version: "0.1.0"
workflow_status: CANONICA_VIGENTE
responsible: Davi Sermenho
permitted_uses:
  - extensao_do_registro_para_versoes_simultaneas
  - autorizacao_fase7
prohibited_uses:
  - autorizacao_de_implementacao
  - dados_reais
  - canonizacao_automatica
---

# Autorização do modelo de versões simultâneas

## 1. Identificação

| Campo | Valor |
| --- | --- |
| ID | `DOC-CEPRAEA-DEC-MODELO-VERSOES` |
| Versão | `0.1.0` |
| Estado | `RASCUNHO` |
| Responsável | Davi Sermenho |
| Data | 2026-07-28 |
| Motivação | Fase 7 do PLANO-FRONT-MATTER-AUTORITATIVO |

## 2. Contexto

O registro mestre (`registro-documentos.yaml`) exige `document_id` único por
entrada. A Fase 7 precisa criar uma nova revisão de dois documentos
`CANONICA_VIGENTE` para adicionar front matter sem modificar os bytes
aprovados. Durante o ciclo `RASCUNHO → EM_REVISAO → CANONICA_VIGENTE` da nova
revisão, a versão vigente e a nova devem coexistir no registro com o mesmo
`document_id` e versões diferentes.

Esta decisão autoriza a extensão do modelo de unicidade do registro.

## 3. Extensão autorizada

1. `document_id` continua sendo a identidade permanente do documento.
2. A unicidade operacional passa a ser o par `(document_id, version)`.
3. `current_path` continua globalmente único em todas as versões simultâneas.
4. Pode existir uma versão `CANONICA_VIGENTE` e uma versão nova em `RASCUNHO`
   ou `EM_REVISAO` para o mesmo `document_id`.
5. Evidências e aprovações identificam sempre `document_id`, `version` e
   `content_hash`.
6. Somente uma versão por `document_id` pode estar `CANONICA_VIGENTE`.
7. `validate_documentation.py` desambigua registros por versão em todas as
   funções de verificação de unicidade e de consistência de ingestão.
8. `docs/archive/superseded/` é aceito para versões `SUPERADA`;
   `docs/archive/revoked/` para versões `REVOGADA`.

## 4. Escopo

Esta decisão autoriza exclusivamente:

- A coexistência temporária de versões `CANONICA_VIGENTE` e `RASCUNHO`/`EM_REVISAO`
  para `DOC-CEPRAEA-CANDIDATA-CONTEXTO` e `DOC-CEPRAEA-DEC-019-MVP-SINTETICO`
  durante a Fase 7.
- A atualização de `validate_documentation.py` para implementar as regras
  acima.

Esta decisão não autoriza:

- Implementação de produto.
- Uso de dados reais.
- Canonização automática de qualquer versão.
- Coexistência de mais de uma versão `CANONICA_VIGENTE` para o mesmo
  `document_id`.

## 5. Fora do escopo

- Alteração de `documento.schema.json`.
- Alteração do workflow YAML.
- Qualquer operação além das 4 alterações cirúrgicas no validador descritas
  no plano autoritativo.
