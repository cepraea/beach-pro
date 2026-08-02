# Plano: Sistema Front Matter YAML — CEPRAEA Beach Pro
<!-- markdownlint-disable MD007 -->
- [Plano: Sistema Front Matter YAML — CEPRAEA Beach Pro](#plano-sistema-front-matter-yaml--cepraea-beach-pro)
  - [Contexto](#contexto)
  - [Schema de front matter (campos definidos)](#schema-de-front-matter-campos-definidos)
    - [Documentos `docs/` — campos obrigatórios](#documentos-docs--campos-obrigatórios)
  - [Fases de implementação](#fases-de-implementação)
    - [Fase 0 — Fundação de schema e tooling](#fase-0--fundação-de-schema-e-tooling)
    - [Fase 1 — Feature specs (sem impacto no registro existente)](#fase-1--feature-specs-sem-impacto-no-registro-existente)
    - [Fase 2 — Gate G-FM no script Python](#fase-2--gate-g-fm-no-script-python)
    - [Fase 3 — Front matter nos docs `RASCUNHO` (bulk)](#fase-3--front-matter-nos-docs-rascunho-bulk)
    - [Fase 4 — Front matter nos docs CANONICA\_VIGENTE (operação controlada)](#fase-4--front-matter-nos-docs-canonica_vigente-operação-controlada)
    - [Fase 5 — Documentos de contexto para agentes](#fase-5--documentos-de-contexto-para-agentes)
    - [Fase 6 — Encerramento](#fase-6--encerramento)
  - [Arquivos críticos](#arquivos-críticos)
  - [Riscos](#riscos)
  - [Verificação end-to-end](#verificação-end-to-end)

<!-- markdownlint-enable MD007 -->

>**Status normativo:** NORMA OBRIGATÓRIA.  
>**Contexto deste documento:** este documento governa toda formatação da documentação  de artefatos normativos do repositório. Seus termos `DEVE`, `NÃO DEVE`, `PODE` e `FALHA` têm sentido normativo. Uma tradução somente pode substituir sua origem quando cumprir todos os gates definidos nesta norma.

## Contexto

O projeto possui um sistema de governança documental robusto em docs/ com registro mestre em YAML (registro-documentos.yaml) e scripts Python de validação. Alguns documentos já têm front matter parcial e inconsistente. O objetivo é criar um sistema coerente e completo onde cada arquivo .md seja auto-descritivo, com front matter validado contra schema e processável pelos scripts Python e por agentes Claude.

**Princípio central**: o `registro-documentos.yaml` continua sendo a fonte de verdade para metadados de governança (hash, relacionamentos, caminhos). O front matter é o **índice de triagem** — contém apenas o necessário para decidir se o documento é relevante, sem ler o corpo.

## Schema de front matter (campos definidos)

### Documentos `docs/` — campos obrigatórios

```yaml
---
document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
title: "DEC-019 — Recorte e autorização do MVP sintético"
document_type: decisao
version: "0.1.1"
workflow_status: CANONICA_VIGENTE
responsible: Davi Sermenho
permitted_uses:
  - decisao_vigente
prohibited_uses:
  - aprovacao_por_inferencia
  - dados_reais
---
```

Ficam somente no registro (nunca no front matter): `content_hash` (paradoxo de auto-hash), `current_path`, `canonical_path`, `registration_status`, `naming_conformance`, `directory_conformance`, relationships completo.

Feature specs `src/features/` — schema próprio, mais leve

```yaml
---
feature_id: FT-ATLETAS
title: "Feature: Gestão de atletas"
type: feature_spec
mvp_status: INCLUIDO        # INCLUIDO | ADIADO | FORA_DO_ESCOPO
milestone: M1               # M0–M4 conforme DEC-019
entities:
  - atleta
dependencies: []
authorized_by: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
---
```

## Fases de implementação

### Fase 0 — Fundação de schema e tooling

1. Criar `docs/contracts/schemas/front-matter.schema.json` com os campos definidos acima (enums sincronizados com `documento.schema.json`)
2. Registrar `DOC-CONTRATO-FRONT-MATTER` em `registro-documentos.yaml`
3. Rodar `python3 scripts/documentation/validate_documentation.py` — confirmar zero regressões

### Fase 1 — Feature specs (sem impacto no registro existente)

1. Criar `src/features/<feature>/README.md` para as 6 features: atletas, treinadores, treinos (M0/M1), presencas (M2), jogos (M3/M4 — mvp_status: ADIADO), avaliacoes (M4 — mvp_status: ADIADO)
2. Não são registrados em `registro-documentos.yaml` — o validator não varre `src/`

### Fase 2 — Gate G-FM no script Python

1. Adicionar `validate_front_matter()` em `scripts/documentation/validate_documentation.py`
    - Verifica presença do bloco ---
    - Valida YAML contra `front-matter.schema.json`
    - Confere `document_id`, `version` e `workflow_status` contra o registro
    - Confere que `permitted_uses` no front matter é subconjunto do registro
  
2. Adicionar `G-FM` ao `--gate` choices do script
3. Adicionar `G-FM` a `docs/registry/workflow-documentacao.yaml`
4. Atualizar hash do workflow-documentacao.yaml no registro
5. Rodar `--gate` `G-FM` como baseline — esperar falha em tudo (sem front matter ainda)

### Fase 3 — Front matter nos docs `RASCUNHO` (bulk)

1. Por arquivo: adicionar front matter → calcular SHA-256 novo → atualizar content_hash no registro → `rodar o validator`
2. Ordem: `governance` → `sources` → `validation reports` → `derived` → `controlled bases`
3. Nunca em lote — cada arquivo deve passar o validator antes do próximo

### Fase 4 — Front matter nos docs CANONICA_VIGENTE (operação controlada)

1. Os dois documentos canônicos (contexto-`cepraea-beach-pro.md` e `decisao-019-mvp-sintetico.md`) devem ser atualizados em um único commit atômico com os hashes correspondentes no registro
2. Rodar o validator completo incluindo G-FM antes do commit

### Fase 5 — Documentos de contexto para agentes

1. Registrar primeiro em `registro-documentos.yaml`, depois criar os arquivos:
   - `docs/canonical/context/guia-triagem-agente.md` — mapa de documentos canônicos, regras de triagem, tabela - `permitted_uses/prohibited_uses`
   - `docs/canonical/context/mapa-decisoes-mvp.md` — `tabela RFs` × `milestone` × `feature` (condensado do `DEC-019` para consulta rápida)
   - `docs/canonical/context/vocabulario-dominio.md` — vocabulário controlado de entidades, extraído do contexto operacional

### Fase 6 — Encerramento

1. Atualizar `docs/README.md` com seção "Triagem por agentes de IA" explicando os campos de front matter
2. Atualizar `docs/inventario-documentos.md`
3. Rodar `validate_documentation.py` completo (todos os gates incluindo G-FM)

## Arquivos críticos

| Arquivo | Ação |
| :---: | :---: |
| `docs/contracts/schemas/front-matter.schema.json` | Criar (novo) |
| `docs/contracts/schemas/documento.schema.js` | on Referência para sincronizar enums |
| `docs/registry/registro-documentos.yaml` | Atualizar a cada front matter adicionado |
| `docs/registry/workflow-documentacao.yaml` | Adicionar gate `G-FM` |
| `scripts/documentation/validate_documentation.py` | Adicionar `validate_front_matter()` e gate `G-FM` |
| `src/features/*/README.md` | Criar (6 novos arquivos) |
| `docs/canonical/context/*.md` | Criar (3 novos arquivos, após registro) |

## Riscos

- Hash em cascata: front matter muda o hash de todos os .md. Mitigação: atualizar hash no registro na mesma operação, nunca separado.

- `CANONICA_VIGENTE`: documentos mais sensíveis. `build_provenance_catalog.py` falha se o hash divergir. Tratar na Fase 4, por último, de forma atômica.

- `documento.schema.json` não precisa mudar: o front matter tem schema próprio (`front-matter.schema.json`). São superfícies de validação distintas.

## Verificação end-to-end

```bash
python3 scripts/documentation/validate_documentation.py  # gates G-ARCH, G0, G1
python3 scripts/documentation/validate_documentation.py --gate G-FM  # novo gate
python3 scripts/documentation/build_provenance_catalog.py  # hash dos canônicos
```
