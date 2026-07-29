---
document_id: DOC-GOV-POL-ARQUITETURA
title: "Política de arquitetura e nomenclatura documental"
document_type: politica
version: "0.1.0"
workflow_status: RASCUNHO
permitted_uses:
  - implementacao_controlada
  - validacao
prohibited_uses:
  - canonizacao_automatica
---

# Política de arquitetura e nomenclatura documental

- [Política de arquitetura e nomenclatura documental](#política-de-arquitetura-e-nomenclatura-documental)
  - [1. Identificação](#1-identificação)
  - [2. Finalidade](#2-finalidade)
  - [3. Termos normativos](#3-termos-normativos)
  - [4. Arquitetura oficial](#4-arquitetura-oficial)
  - [5. Contrato dos diretórios](#5-contrato-dos-diretórios)
  - [6. Convenção de nomes físicos](#6-convenção-de-nomes-físicos)
    - [6.1 Regras obrigatórias](#61-regras-obrigatórias)
    - [6.2 Tipos controlados iniciais](#62-tipos-controlados-iniciais)
  - [7. Identidade e localização](#7-identidade-e-localização)
  - [8. Tratamento do acervo legado](#8-tratamento-do-acervo-legado)
  - [9. Migração controlada](#9-migração-controlada)
  - [10. Gate de arquitetura](#10-gate-de-arquitetura)
  - [11. Critérios de aceitação](#11-critérios-de-aceitação)
  - [12. Fora do escopo](#12-fora-do-escopo)

## 1. Identificação

| Campo | Valor |
| --- | --- |
| ID | `DOC-GOV-POL-ARQUITETURA` |
| Versão | `0.1.0` |
| Estado | `RASCUNHO` |
| Responsável | Davi Sermenho |
| Data de criação | 2026-07-25 |
| Escopo | Diretório `docs/` do CEPRAEA BEACH PRO |
| Origem | `docs/planofluxo.md`, seção 8 |

Este documento materializa a primeira política derivada do plano. Seu estado
`RASCUNHO` não concede autoridade canônica. A aprovação e a promoção devem
ocorrer pelo workflow documental.

## 2. Finalidade

Definir uma arquitetura verificável para `docs/` e uma convenção única para
nomes físicos, caminhos, identidades e movimentações documentais.

## 3. Termos normativos

- **DEVE** indica uma condição obrigatória.
- **NÃO DEVE** indica uma condição proibida.
- **PODE** indica uma alternativa permitida.
- **LEGADO_INVENTARIADO** identifica um arquivo anterior ao workflow que ainda
  não recebeu estado válido pela nova máquina de estados.

## 4. Arquitetura oficial

```text
docs/
├── README.md
├── inventario-documentos.md
├── governance/
│   ├── workflows/
│   ├── policies/
│   ├── protocols/
│   └── matrices/
├── registry/
├── contracts/
│   └── schemas/
├── sources/
│   ├── primary/
│   └── supporting/
├── controlled/
│   ├── bases/
│   └── candidates/
├── canonical/
│   ├── context/
│   ├── decisions/
│   ├── glossary/
│   └── requirements/
├── derived/
│   └── requirements/
├── validation/
│   ├── reports/
│   └── corrective-actions/
├── evidence/
│   ├── approvals/
│   ├── promotions/
│   └── gates/
└── archive/
    ├── superseded/
    └── revoked/
```

Diretórios vazios NÃO DEVEM ser criados apenas para reproduzir a árvore. Um
diretório passa a existir quando recebe seu primeiro artefato válido.

## 5. Contrato dos diretórios

| Caminho | Conteúdo permitido |
| --- | --- |
| `docs/governance/workflows/` | Fluxos narrativos e workflows executáveis |
| `docs/governance/policies/` | Políticas documentais |
| `docs/governance/protocols/` | Protocolos de avaliação e operação |
| `docs/governance/matrices/` | Matrizes de autoridade, precedência e rastreabilidade |
| `docs/registry/` | Registro mestre e definições processáveis |
| `docs/contracts/schemas/` | Schemas de contratos |
| `docs/sources/primary/` | Evidências e fontes primárias preservadas |
| `docs/sources/supporting/` | Fontes auxiliares e análises contextuais |
| `docs/controlled/bases/` | Bases controladas ainda não candidatas |
| `docs/controlled/candidates/` | Versões congeladas submetidas à aprovação |
| `docs/canonical/` | Versões canônicas vigentes publicadas |
| `docs/derived/` | Requisitos e outros artefatos derivados |
| `docs/validation/reports/` | Relatórios de validação e auditoria |
| `docs/validation/corrective-actions/` | Registros de ações corretivas |
| `docs/evidence/` | Evidências de gates, aprovações e promoções |
| `docs/archive/superseded/` | Versões canônicas substituídas |
| `docs/archive/revoked/` | Versões formalmente revogadas |

A localização de um arquivo NÃO DEVE ser interpretada isoladamente como
autoridade ou estado. O registro mestre é a fonte operacional do estado.

## 6. Convenção de nomes físicos

O nome físico de um documento DEVE obedecer ao formato:

```text
<tipo>-<dominio-ou-escopo>[-<assunto>].<extensao>
```

Para Markdown e YAML, as expressões iniciais são:

```regex
^[a-z0-9]+(?:-[a-z0-9]+)+\.md$
^[a-z0-9]+(?:-[a-z0-9]+)+\.ya?ml$
```

Schemas JSON DEVEM obedecer a:

```regex
^[a-z0-9]+(?:-[a-z0-9]+)*\.schema\.json$
```

### 6.1 Regras obrigatórias

- usar letras minúsculas;
- usar somente caracteres ASCII;
- separar palavras com hífen;
- não usar espaços, sublinhados ou travessões tipográficos;
- manter o nome físico estável durante o ciclo de vida;
- manter versão, estado e data fora do nome físico;
- não usar `final`, `novo`, `ultima`, `corrigido` ou equivalentes;
- não reutilizar um caminho para outro `document_id`;
- registrar `current_path` e, quando aplicável, `canonical_path`;
- validar links com sensibilidade a maiúsculas e minúsculas.

`README.md` é a única exceção inicial de caixa.

### 6.2 Tipos controlados iniciais

```text
contexto
contrato
decisao
evidencia
fluxo
glossario
inventario
matriz
politica
protocolo
registro
relatorio
requisito
workflow
```

Um novo tipo exige alteração aprovada desta política antes do uso.

## 7. Identidade e localização

| Campo | Regra |
| --- | --- |
| `document_id` | Identidade permanente; não muda |
| `title` | Nome legível; pode mudar com registro |
| `current_path` | Localização física atual |
| `canonical_path` | Local de publicação canônica |
| `version` | Identifica revisão material |
| `content_hash` | Identifica os bytes da versão |
| `workflow_status` | Estado atribuído por transição válida |

Ao canonizar, `current_path` e `canonical_path` DEVEM apontar para o mesmo
artefato em `docs/canonical/`.

Ao superar ou revogar uma versão, `current_path` DEVE passar para
`docs/archive/`. O `canonical_path` histórico DEVE ser preservado no registro.

## 8. Tratamento do acervo legado

Arquivos anteriores a esta política:

- DEVEM ser cadastrados como `LEGADO_INVENTARIADO`;
- DEVEM preservar seu caminho até a migração controlada;
- NÃO DEVEM receber `workflow_status` por equivalência textual;
- NÃO DEVEM ser declarados canônicos pelo registro inicial;
- DEVEM registrar o estado legado declarado separadamente;
- DEVEM receber caminho de destino proposto;
- DEVEM permanecer utilizáveis conforme sua autoridade histórica documentada.

`LEGADO_INVENTARIADO` é estado de cadastro, não estado do workflow.

## 9. Migração controlada

Uma migração DEVE:

1. atribuir `document_id`;
2. registrar caminho atual e caminho de destino;
3. mapear todas as referências recebidas;
4. atualizar caminhos e links de forma atômica;
5. recalcular hashes;
6. executar os validadores;
7. impedir duplicidade e orfandade;
8. registrar o evento;
9. preservar o histórico;
10. obter `G-MIGRACAO = pass`.

## 10. Gate de arquitetura

`G-ARCH` retorna `pass` somente quando:

- o documento está no diretório compatível com seu tipo e estado;
- o nome físico obedece à convenção;
- o caminho está registrado;
- o `document_id` é único;
- não existe colisão de caixa;
- o hash corresponde ao conteúdo;
- os links locais possuem destino válido;
- nenhuma versão ou estado aparece indevidamente no nome;
- o registro e o sistema de arquivos são consistentes.

Arquivos `LEGADO_INVENTARIADO` podem produzir avisos de nomenclatura durante a
fase de migração, mas caminho inexistente, hash divergente, ID duplicado e link
quebrado continuam sendo falhas.

## 11. Critérios de aceitação

| ID | Condição | Verificação | Resultado esperado |
| --- | --- | --- | --- |
| `AC-ARCH-001` | Todos os Markdown de `docs/` estão registrados | Validador do acervo | Zero arquivo órfão |
| `AC-ARCH-002` | IDs e caminhos são únicos | Validador do registro | Zero duplicidade |
| `AC-ARCH-003` | Hashes registrados correspondem aos arquivos | SHA-256 | Zero divergência |
| `AC-ARCH-004` | Novos nomes obedecem à convenção | Expressão regular | Zero nome inválido |
| `AC-ARCH-005` | Links locais possuem destino | Validador de links | Zero link quebrado |
| `AC-ARCH-006` | Legado não é promovido por inferência | Revisão do registro | `workflow_status: null` |
| `AC-ARCH-007` | Nenhum documento é canônico no início | Revisão do registro | Lista canônica vazia |

## 12. Fora do escopo

Esta política não:

- aprova ou canoniza documentos;
- autoriza implementação do produto;
- autoriza dados reais, piloto ou produção;
- define o conteúdo semântico do CEPRAEA;
- substitui contratos, gates ou decisões humanas;
- executa automaticamente a migração dos nomes legados.
