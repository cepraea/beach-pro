---
document_id: DOC-VAL-REL-MIGRACAO-ARQUITETURA
title: "Relatório da migração controlada do acervo legado"
document_type: relatorio
version: "0.1.0"
workflow_status: RASCUNHO
permitted_uses:
  - evidencia_de_migracao
  - auditoria
prohibited_uses:
  - aprovacao_de_conteudo
  - canonizacao
---

# Relatório da migração controlada do acervo legado

## 1. Identificação

| Campo | Valor |
| --- | --- |
| ID | `DOC-VAL-REL-MIGRACAO-ARQUITETURA` |
| Evidência | `EVID-MIGRACAO-ARQUITETURA-INICIAL` |
| Versão | `0.1.0` |
| Estado | `RASCUNHO` |
| Data | 2026-07-25 |
| Escopo | Dez artefatos legados registrados |
| Gate | `G-ARCH` |

## 2. Objetivo

Mover os dez artefatos legados para a arquitetura controlada, aplicar a
convenção de nomes físicos, preservar os caminhos anteriores e atualizar
referências sem atribuir estado canônico.

## 3. Preflight

Antes da movimentação:

```text
validator_exit=0
errors=0
warnings=20
destination_collisions=0
```

Os hashes correspondiam ao registro mestre e todos os destinos estavam livres.

## 4. Mapa de migração

| ID | Caminho anterior | Caminho atual |
| --- | --- | --- |
| `DOC-CEPRAEA-FONTE-OPERACIONAL` | `docs/DESCRICAO-CEPRAEA.md` | `docs/sources/primary/contexto-operacional-cepraea.md` |
| `DOC-CEPRAEA-DIRETRIZ-CONTEXTO` | `docs/CONTEUDO DESC-CEPRAEA.md` | `docs/sources/supporting/diretriz-conteudo-contexto-cepraea.md` |
| `DOC-CEPRAEA-BASE-CONTEXTO` | `docs/DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md` | `docs/controlled/bases/contexto-cepraea-beach-pro.md` |
| `DOC-CEPRAEA-CANDIDATA-CONTEXTO` | `docs/DESCRICAO-CEPRAEA — VERSÃO CANDIDATA 0.1.md` | `docs/controlled/candidates/contexto-cepraea-beach-pro.md` |
| `DOC-GOV-PROT-QUALIDADE` | `docs/PROTOCOLO-QUALIDADE-DOC.md` | `docs/governance/protocols/protocolo-qualidade-documental.md` |
| `DOC-VAL-REL-CONTEXTO-V01` | `docs/VALIDACAO-CEPRAEA-v0.1.md` | `docs/validation/reports/relatorio-validacao-contexto-cepraea.md` |
| `DOC-CEPRAEA-REQ-DERIVADOS-V01` | `docs/RF-CEPRAEA-v0.1.md` | `docs/derived/requirements/requisitos-funcionais-cepraea.md` |
| `DOC-REG-INVENTARIO-LEGADO` | `docs/INVENTARIO-DOCS.md` | `docs/inventario-documentos.md` |
| `DOC-GOV-FLUXO-INICIAL` | `docs/FLUXO-DOCS.md` | `docs/governance/workflows/fluxo-documentacao-inicial.md` |
| `DOC-GOV-WORKFLOW-PLANO` | `docs/planofluxo.md` | `docs/governance/workflows/workflow-operacionalizacao-documental.md` |

O registro mestre preserva cada caminho anterior em
`relationships.previous_paths`.

## 5. Referências

O atualizador controlado:

- converteu links para caminhos relativos;
- atualizou links nos documentos de governança, inventário e entrada;
- atualizou referências externas ao diretório `docs/` quando apontavam para os
  artefatos movidos;
- preservou menções históricas não clicáveis aos nomes legados;
- não alterou títulos conceituais como `DECISAO-CEPRAEA`.

## 6. Resultado

Primeira execução posterior à movimentação e à atualização do registro:

```text
validator_exit=0
errors=0
warnings=0
g_arch_exit=0
g_arch_status=pass
```

## 7. Garantias obtidas nesta etapa

- nenhum destino foi sobrescrito;
- nenhum arquivo registrado ficou órfão;
- nenhum hash registrado divergiu;
- nenhum link local validado ficou quebrado;
- não existem colisões de ID, caminho ou caixa;
- os dez nomes e diretórios cumprem a política;
- `G-ARCH` não permite mais exceções legadas no estado migrado;
- o histórico dos caminhos foi preservado.

## 8. Limites

A migração e o `G-ARCH = pass` não:

- atribuem `workflow_status` aos documentos legados;
- aprovam ou canonizam conteúdo;
- implementam `G0` a `G8`;
- implementam `G-CANON`;
- autorizam desenvolvimento, dados reais, piloto ou produção;
- criam referência imutável por commit ou tag.

