---
document_id: DOC-CEPRAEA-DEC-ENFORCEMENT-G-FM
title: "DEC — Ativação do G-FM como gate obrigatório"
document_type: decisao
version: "0.1.0"
workflow_status: CANONICA_VIGENTE
responsible: Davi Sermenho
permitted_uses:
  - enforcement_g_fm
  - autorizacao_fase8
prohibited_uses:
  - aprovacao_por_inferencia
  - dados_reais
  - canonizacao_automatica
---

# DEC — Ativação do G-FM como gate obrigatório

## 1. Identificação

| Campo | Valor |
| --- | --- |
| ID | `DOC-CEPRAEA-DEC-ENFORCEMENT-G-FM` |
| Versão | `0.1.0` |
| Estado | `RASCUNHO` |
| Responsável | Davi Sermenho |
| Data | 2026-07-29 |
| Motivação | Fase 8 do PLANO-FRONT-MATTER-AUTORITATIVO |

## 2. Contexto

O G-FM foi implementado e registrado no catálogo de gates do workflow
(`workflow-documentacao.yaml` v0.2.1) como `IMPLEMENTED` e `blocking: true`,
mas não figura em `required_gates` de nenhuma transição. As Fases 1 a 7 foram
concluídas: todos os documentos governados possuem front matter válido, os seis
feature specs existem e passam G-FM, e o baseline global registrado em
`GATE-RESULT-G-FM-BASELINE-PRE-MIGRACAO` foi totalmente resolvido. O resultado
do G-FM global em 2026-07-29 confirmou `errors=0, warnings=0`.

Esta decisão autoriza a ativação do G-FM como gate obrigatório nos pontos
definidos pelo plano autoritativo (Fase 8).

## 3. Autorização

Adicionar `G-FM` ao campo `required_gates` exclusivamente em:

- `INIT-DOC-001` — inicialização de documento (LEGADO_INVENTARIADO → RASCUNHO)
- `T-DOC-001` — transição RASCUNHO → EM_REVISAO
- `T-DOC-003` — transição EM_REVISAO → CANONICA_VIGENTE

Resultado: `required_gates: [G-ARCH, G0, G1, G-FM]` nas três entradas acima.

## 4. Escopo

Esta decisão autoriza exclusivamente:

- A adição de `G-FM` aos `required_gates` das três entradas especificadas
- O incremento da versão de `workflow-documentacao.yaml` de `0.2.1` para `0.2.2`
- A atualização do `content_hash` de `DOC-REG-WF-DOCUMENTACAO` no registro

## 5. Restrições

- Não autoriza alteração dos `required_gates` de T-DOC-002, T-DOC-004 ou T-DOC-005
- Não autoriza alteração de `documento.schema.json` ou `workflow.schema.json`
- Não autoriza implementação, dados reais, piloto ou produção
- Não cria novos contratos, schemas auxiliares ou gates adicionais
