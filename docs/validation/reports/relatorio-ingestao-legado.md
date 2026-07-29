---
document_id: DOC-VAL-REL-INGESTAO-LEGADO
title: "Relatório de ingestão do lote documental legado"
document_type: relatorio
version: "0.1.0"
workflow_status: RASCUNHO
permitted_uses:
  - evidencia_de_ingestao
  - auditoria
  - orientacao
prohibited_uses:
  - aprovacao_de_conteudo
  - canonizacao
---

# Relatório de ingestão do lote documental legado

## Identificação

- **Lote:** `ING-LEGADO-001`
- **Evento:** `EVT-ING-LEGADO-001`
- **Workflow:** `WF-DOC-CEPRAEA`
- **Quantidade:** dez documentos
- **Estado resultante:** `RASCUNHO`
- **Data:** 25 de julho de 2026

## Resultado

Os dez documentos migrados foram formalmente admitidos na máquina de estados
após aprovação conjunta de `G-ARCH`, `G0 — Identidade` e `G1 — Integridade`.
Cada registro preserva o estado declarado no processo legado, mas passa a usar
`workflow_status: RASCUNHO` como estado operacional verificável.

## Garantias aplicadas

`G0` exige identidade documental completa: ID único, título, tipo, versão,
responsável, datas de registro e verificação, caminho atual, conformidade de
nome e diretório e escopo de autoridade.

`G1` exige correspondência entre registro mestre, manifesto, arquivo físico e
pacote de preservação. A verificação recalcula SHA-256 do lote, abre o arquivo
TAR, compara a lista exata de membros e recalcula o hash de cada membro
preservado.

## Evidências

- `docs/evidence/integrity/manifesto-integridade-legado.yaml`;
- `docs/evidence/integrity/pacote-integridade-legado.tar`;
- `docs/evidence/gates/resultado-g0-ingestao-legado.yaml`;
- `docs/evidence/gates/resultado-g1-ingestao-legado.yaml`;
- `docs/evidence/ingestion/ingestao-legado-inicial.yaml`.

## Limites

A ingestão autoriza apenas a entrada em `RASCUNHO`. Ela não comprova qualidade
semântica, aprovação humana, promoção, vigência ou precedência e não cria
documento canônico. O registro mestre permanece com
`canonical_documents: []`.

O pacote TAR e os hashes tornam alterações detectáveis, mas não constituem,
isoladamente, controle de acesso ou armazenamento externamente imutável.

## Próxima transição

Qualquer avanço de `RASCUNHO` depende dos gates e contratos da transição
correspondente. Os próximos controles de conteúdo são `G2 — Proveniência` e
`G3 — Classificação epistemológica`; nenhum deles foi executado por este ato.
