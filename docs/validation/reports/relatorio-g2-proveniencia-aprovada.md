---
document_id: DOC-VAL-REL-G2-PROVENIENCIA-APROVADA
title: "Relatório de G2 — Proveniência aprovada"
document_type: relatorio
version: "0.1.0"
workflow_status: RASCUNHO
permitted_uses:
  - orientacao_para_g3
  - auditoria
prohibited_uses:
  - promocao_automatica
  - aprovacao
  - canonizacao
---

# Relatório de G2 — Proveniência aprovada

## Identificação

- **Gate:** `G2 — Proveniência`
- **Documento:** `DOC-CEPRAEA-CANDIDATA-CONTEXTO`
- **Versão:** `0.1`
- **Hash avaliado:** `71bd2695280f0cdd5c41b83c7e433d5a84a803b527a7e09d7dfd7eecaaeab847`
- **Pacote:** `PROV-CEPRAEA-CONTEXTO-001`
- **Resultado:** `pass`
- **Cobertura crítica:** `100%`

## Regularização executada

As fontes internas acessíveis foram exportadas e preservadas, as páginas
técnicas oficiais foram capturadas, cada captura recebeu hash SHA-256 e todas
foram consolidadas em pacote TAR determinístico. O catálogo passou a manter
referência imutável, data, responsável, autoridade e usos permitidos e
proibidos.

As referências genéricas de `CLAIM-001`, `CLAIM-008`, `CLAIM-011` e
`CLAIM-012` foram substituídas, no pacote processável, por identificadores
explícitos. `SRC-006` deixou de ser usada como suporte de `CLAIM-004` porque
não possui identificação física suficiente.

## Autoridade e escopo

O contrato de alegação passou a exigir `subjects`. O avaliador somente considera
uma alegação coberta quando pelo menos uma fonte ativa e verificada possui
`authority.scope` compatível com o assunto da alegação. A existência de um hash,
isoladamente, não concede autoridade temática à fonte.

Dos 30 claims críticos, 27 possuem fonte verificada com escopo compatível. Os
três claims sobre identidade cadastral, registro esportivo e perfis sociais
(`CLAIM-013` a `CLAIM-015`) permanecem candidatos com incerteza `unknown`
explicitamente justificada, pois não houve confirmação autoritativa acessível.

## Proteção de dados

As imagens pessoais `SRC-011` e `SRC-012` não foram copiadas para o pacote.
Essa exclusão evita replicação desnecessária de dados pessoais. As alegações
que dependiam delas não foram tratadas como confirmadas.

## Resultado operacional

A execução de G2 terminou com `errors=0` e `warnings=0`. O resultado não
canoniza nem promove o documento: ele remove exclusivamente o bloqueio de
proveniência. A próxima avaliação aplicável é `G3 — Semântica e escopo`.
