# Modelagem do domínio CEPRAEA-BEACH-PRO

Este diretório contém a execução de `PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`: a descoberta
orientada por evidências e a construção do Modelo Canônico do Domínio do CEPRAEA-BEACH-PRO a
partir do acervo em `CEPRAEA_SOURCE_ROOT`.

## Variáveis registradas por `AC-000`

| Variável | Valor |
| --- | --- |
| `base_ref` | `feat/cepraea-domain-modeling`, atualizada por fast-forward a partir de `chore/runbooks-e-correcoes-politicas-agentes` antes do início de `AC-000` |
| `base_sha` | `0021102f4a10257f1349990ee3b9db7d1ab0e591` |
| `main_sha_before` | `9857c7214d6afbe830c5850b430600af086d2d69` |
| `branch_modelagem` | `feat/cepraea-domain-modeling` |
| `cepraea_source_root` | `.drive/CEPRAEA BEACH PRO` |
| `data_ac_000` | 2026-08-15 |

`git rev-parse main` DEVE permanecer igual a `main_sha_before` ao final da fase (GATE E, seção 11
do plano).

## Escopos formais

Os escopos abaixo substituem os da seção 4.7 original do plano, conforme `DEC-008` em
`decisoes/registro_decisoes.md`.

```text
WRITE_SCOPE_EXECUTOR
  docs/modelagem/**

WRITE_SCOPE_REVIEWER
  # Reviewer não produz artefatos de escrita; emite verdict ao humano.

READ_SCOPE
  repositório cepraea-beach-pro, quando necessário à ação
  .drive/CEPRAEA BEACH PRO/**

CEPRAEA_SOURCE_ROOT
  .drive/CEPRAEA BEACH PRO

MODO (CEPRAEA_SOURCE_ROOT)
  READ_ONLY
```

Escrita fora de `WRITE_SCOPE_EXECUTOR` (ou `WRITE_SCOPE_REVIEWER`, para o `REVIEWER`) é proibida.
Leitura fora de `READ_SCOPE` é proibida.

**Nota:** `CEPRAEA_SOURCE_ROOT` e os três documentos de referência citados abaixo estão listados em
`.gitignore` — existem apenas neste ambiente local. Um clone novo do repositório não os reproduz
automaticamente; eles precisam ser copiados separadamente antes de qualquer `AC-NNN` que dependa
deles.

## Estrutura

```text
docs/modelagem/
├── README.md
├── processo/           — checklist adaptado, taxonomias, critérios de maturidade, perguntas de competência
├── fontes/              — inventário e dossiês, um por fonte (schema_fonte.json)
├── evidencias/          — fragmentos de evidência EVD-NNNN (schema_evidencia.json)
├── conhecimento/        — glossário, regras extraídas, conflitos semânticos
├── candidatos/          — hipóteses estruturais ainda não promovidas (schema_elemento_modelo.json, estagio=CANDIDATO)
├── dominio/             — Modelo Canônico e elementos promovidos (schema_elemento_modelo.json, estagio=DOMINIO)
├── logico/              — modelo lógico relacional, só para Bounded Contexts maduros
├── decisoes/            — registro de decisões materiais (schema_decisao.json)
└── schemas/             — schemas formais e scripts de validação
```

## Fontes de autoridade

- `PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` — especificação normativa desta fase.
- `decisoes/registro_decisoes.md` — decisões já resolvidas/aprovadas: `DEC-001`–`DEC-003`,
  `DEC-006`, `DEC-008` (incluídas por `AC-000`); `DEC-GOV-001` (referência, registro canônico em
  `.ai/decisions/`); `DEC-011` (separação de decisões de governança do SDLC das decisões de
  modelagem); `DEC-GOV-002` (`runbook_binding` formal para `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN`,
  referência, registro canônico em `.ai/decisions/`). `DEC-007` permanece `BLOQUEADA`, aprovador
  `PENDENTE`.
- `.drive/modelagem_dados_agente.md` e `.drive/modelagem_dominio_dados.md` — modelagem de
  referência citada pelo plano.
- `.drive/BEACH HANDBALL/Fluxo de Modelagem.gdoc.docx` — checklist original ("Guia 1"/"Guia 2")
  adaptado em `processo/`.

## Validação

```sh
node docs/modelagem/schemas/validar.mjs
node docs/modelagem/schemas/verificar_referencias.mjs
node docs/modelagem/schemas/verificar_repositorio.mjs
```

Critério de pronto da fase: seção 11 do plano (`GATE A` a `GATE E`).
