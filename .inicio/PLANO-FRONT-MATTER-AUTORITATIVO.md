# Plano autoritativo: Sistema Front Matter YAML — CEPRAEA Beach Pro

## Identificação

| Campo            | Valor                                              |
| ---------------- | -------------------------------------------------- |
| Natureza         | Plano autoritativo — revisão estrutural v3         |
| Data             | 2026-07-28                                         |
| Autoridade       | Davi Sermenho                                      |
| Fonte de verdade | `docs/registry/registro-documentos.yaml`           |
| Estado           | Não autorizado para execução automática            |

## 1. Princípios

1. `registro-documentos.yaml` é a fonte de verdade global: hash,
   relacionamentos, caminhos e histórico vivem somente ali.
2. O front matter é o **índice de triagem** local — contém apenas o necessário
   para decidir se o documento é relevante sem ler o corpo nem o registro.
3. Agentes não devem ler o registro inteiro para determinar o estado de um
   documento. `workflow_status` é incluído no front matter com sincronização
   obrigatória em operação atômica (ver seção 4.3).
4. `content_hash` nunca entra no front matter (paradoxo de auto-hash).
5. O schema de front matter é JSON Schema padrão, independente de fornecedor.
6. `documento.schema.json` não muda — front matter e documento governado são
   superfícies de validação independentes.
7. Arquivos `.ts` e `.tsx` não recebem front matter em nenhuma circunstância.
8. A Fase −1 exige autorização corretiva explícita e deve passar sem erros antes
   de qualquer outra fase começar. A falha esperada do G-FM é tratada
   separadamente das falhas preexistentes.

## 2. Cobertura documental

Documentos governados: registrados em `registro-documentos.yaml`, cujo
`current_path` termine em `.md`, e não listados nas exclusões abaixo.

| Perfil         | Padrão de caminho      | Schema                                  |
| -------------- | ---------------------- | --------------------------------------- |
| `governed`     | `docs/**/*.md`         | `front-matter-governed.schema.json`     |
| `feature-spec` | `src/features/**/*.md` | `front-matter-feature-spec.schema.json` |

Exclusões explícitas do perfil `governed`:

- `CLAUDE.md`, `README.md` da raiz
- `.inicio/**/*.md`
- `src/**/*.ts`, `src/**/*.tsx`
- `node_modules/**`

`docs/README.md` está **incluído** no perfil `governed`: é registrado e será
alterado na Fase 10. Feature specs não são registradas — o validador as
descobre via glob `src/features/**/*.md`, não pelo registro.

## 3. Consumidores

| Camada     | Consumidores                                          | Uso principal                                          |
| ---------- | ----------------------------------------------------- | ------------------------------------------------------ |
| Normativo  | Scripts Python de governança, validação, proveniência | Validação de schema, sincronização com registro, gates |
| Descoberta | Claude Code, Codex, agentes e subagentes              | Triagem, seleção de contexto, verificação documental   |
| Humano     | Davi Sermenho e colaboradores                         | Leitura, edição, revisão                               |
| Pipeline   | TypeScript/Vite                                       | Não consome front matter nesta fase                    |

## 4. Schemas de front matter

### 4.1 Perfil `governed` — `docs/**/*.md`

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

Regras de sincronização com `registro-documentos.yaml`:

| Campo             | Regra                                                        |
| ----------------- | ------------------------------------------------------------ |
| `document_id`     | Igualdade exata com o registro                               |
| `title`           | Igualdade exata com o registro                               |
| `document_type`   | Igualdade exata com o registro                               |
| `version`         | Igualdade exata com o registro                               |
| `workflow_status` | Igualdade exata com o registro                               |
| `responsible`     | Igual ao registro quando existir; omitido quando não existir |
| `permitted_uses`  | Subconjunto dos usos permitidos no registro                  |
| `prohibited_uses` | Deve conter todas as proibições do registro                  |

Campos exclusivos do registro — nunca no front matter:

- `content_hash` — paradoxo de auto-hash
- `current_path`, `canonical_path`, `target_path`
- `registration_status`, `naming_conformance`, `directory_conformance`
- `relationships` completo, `evidence`, `approvals`

### 4.2 Perfil `feature-spec` — `src/features/**/*.md`

```yaml
---
feature_id: FT-PRESENCAS
title: "Feature: Controle de presenças"
type: feature_spec
mvp_status: INCLUIDO
milestones: [M3]
entities:
  - presenca
dependencies: []
authorized_units: [MVP-05]
authorized_requirements: [RF-018]
authorized_by: DOC-CEPRAEA-DEC-MAPA-FEATURES
derived_from: [DOC-CEPRAEA-DEC-019-MVP-SINTETICO]
---
```

Valores válidos para `mvp_status`: `INCLUIDO`, `ADIADO`, `FORA_DO_ESCOPO`.
Valores válidos por item de `milestones`: `M0`, `M1`, `M2`, `M3`, `M4`.

Condição: quando `mvp_status` for `ADIADO` ou `FORA_DO_ESCOPO`, `milestones`
deve ser `[]` ou o campo deve ser omitido — não atribuir milestone autorizado a
funcionalidade adiada. Valores compostos como `M0/M1` são inválidos; usar
array `[M0, M1]`.

Feature specs não são registradas em `registro-documentos.yaml`.

`authorized_by` aponta para a decisão humana produzida na Fase 4.
`derived_from` preserva o DEC-019 como fonte normativa anterior. Para
`mvp_status: INCLUIDO`, `authorized_units` e `authorized_requirements` são arrays
não vazios e sem duplicatas. O exemplo acima é uma proposta sujeita à aprovação
e à confirmação da rastreabilidade na Fase 4.

### 4.3 Protocolo de sincronização de `workflow_status`

Toda transição de estado de um documento governado exige operação atômica:

1. Determinar `workflow_status` e `version` de destino sem persistir estado
   intermediário.
2. Atualizar `workflow_status` e `version` no front matter.
3. Calcular `content_hash` sobre os bytes resultantes.
4. Preparar no registro os mesmos `workflow_status` e `version`, além do novo
   `content_hash`.
5. Produzir a evidência da transição com identidade, versão e hash de destino
   (quando exigida pelo workflow).
6. Persistir arquivo, registro e evidência na mesma operação.
7. Executar G-FM para o documento alterado. G-FM global é executado somente em
   fases cuja cobertura completa já seja esperada.

Nenhuma etapa intermediária divergente pode ser gravada no repositório.

Para documentos `CANONICA_VIGENTE`: alteração direta dos bytes aprovados é
proibida. Qualquer mudança — incluindo adição de front matter — exige nova
revisão, nova validação e nova aprovação, preservando ou arquivando a versão
anterior conforme a política. O hash aprovado da versão anterior é registrado
como relacionamento histórico.

### 4.4 Arquitetura do parser

`validate_front_matter()` em `validate_documentation.py` é composta por três
funções com responsabilidades distintas:

- `parse_front_matter(path, profile)` — função pura: lê o arquivo, extrai o
  bloco YAML, valida contra o schema do perfil, retorna objeto ou lista de
  erros. Não acessa o registro. Usa `SafeLoader` customizado que detecta chaves
  duplicadas durante a construção do mapping (ver Fase 1).
- `validate_governed(registered_doc)` — recebe um documento do registro cujo
  `current_path` termine em `.md` e não esteja nas exclusões; chama
  `parse_front_matter` e verifica sincronização com os campos do registro.
- `validate_feature_spec(path)` — recebe um caminho de `src/features/**/*.md`
  descoberto via glob; chama `parse_front_matter` com perfil `feature-spec`.
  Não depende do registro.

G-FM executa ambos os validadores. As exclusões são aplicadas de modo
centralizado antes de qualquer chamada.

O gate aceita escopo opcional:

```bash
python3 scripts/documentation/validate_documentation.py \
  --gate G-FM \
  --document-id DOC-...
```

Com `--document-id`, valida somente o documento governado indicado.
`--version` torna-se obrigatório quando houver duas versões registradas para a
mesma identidade. Sem escopo, G-FM valida todos os documentos governados e todas
as feature specs descobertas.

## 5. Estado atual verificado

Em 2026-07-28, após a execução autorizada da Fase −1:

- baseline pré-FM sem erros ou avisos em G-ARCH, G0 e G1
- `proposta-mvp-sintetico-cepraea.md` regularizada como versão `0.1.3`;
  versão `0.1.2` e hash referenciado preservados no histórico do registro
- artefato vazio residual
  `docs/controlled/candidates/contexto-cepraea-beach-pro.md` removido; documento
  vigente permanece no caminho canônico registrado
- `build_provenance_catalog.py` resolve a fonte pelo `current_path` do registro
- nenhum arquivo `docs/**/*.md` possui front matter válido
- nenhum arquivo `src/features/**/*.md` existe
- `validate_documentation.py` não implementa G-FM
- nenhum schema de front matter existe
- `workflow-documentacao.yaml` mantém `NOVOS_CONTRATOS` em `out_of_scope`

## 6. Decisão mínima de autorização

O workflow mantém `NOVOS_CONTRATOS` em `out_of_scope`. A Fase 0 exige que
Davi decida explicitamente:

> Autorizar a criação de dois contratos:
> `front-matter-governed.schema.json` e `front-matter-feature-spec.schema.json`,
> limitados aos perfis definidos neste plano, sem autorizar matrizes, manifestos,
> schemas auxiliares ou ativação obrigatória de G-FM.

Se negativa: plano encerra sem alterar `docs/`, `src/` ou `scripts/`.
Se positiva: definir como reconciliar com `NOVOS_CONTRATOS` em `out_of_scope`
(exceção explícita limitada ou atualização mínima do workflow).

## 7. Fases de implementação

### Fase −1 — Saneamento do baseline

**Condição de entrada:** autorização corretiva explícita de Davi, limitada ao
saneamento do baseline. Esta fase precede a autorização dos novos schemas, mas
não autoriza alteração automática do registro ou aceitação de bytes divergentes.

1. Investigar a divergência de `proposta-mvp-sintetico-cepraea.md`:
   - comparar os bytes atuais com as versões e hashes anteriores
   - identificar a origem da alteração
   - confirmar com Davi qual revisão é válida
   - somente então corrigir arquivo, `version` e/ou `content_hash`
   - registrar a correção como evidência
2. Decidir e registrar o destino de
   `docs/controlled/candidates/contexto-cepraea-beach-pro.md`: canonizar,
   revogar ou manter como candidato com estado explícito.
3. Reconciliar o registro `DOC-CEPRAEA-CANDIDATA-CONTEXTO` com a fonte
   especializada usada por `build_provenance_catalog.py`.
4. Executar `validate_documentation.py` (G-ARCH, G0, G1).
5. Executar `build_provenance_catalog.py` somente para a proveniência do
   contexto, seu único escopo nesta revisão do plano.
6. Registrar o resultado como **baseline pré-FM** — evidência do estado do
   repositório antes de qualquer alteração de front matter.

**Condição de saída:** G-ARCH, G0 e G1 passando sem erros. `build_provenance_catalog.py`
sem divergências. G-FM não é executado aqui.

**Resultado em 2026-07-28:** condição de saída atendida. A execução foi
registrada por `AR-002` e pelos resultados
`GATE-RESULT-G-ARCH-BASELINE-PRE-FM`, `GATE-RESULT-G0-BASELINE-PRE-FM` e
`GATE-RESULT-G1-BASELINE-PRE-FM`. A Fase 0 continua dependendo da autorização
específica definida na seção 6.

### Fase 0 — Autorização

1. Registrar a decisão humana sobre os dois schemas.
2. Reconciliar com `NOVOS_CONTRATOS` em `out_of_scope`.
3. Verificar pelos gates vigentes (G-ARCH, G0, G1).
4. Interromper se os gates não permitirem prosseguir.

**Saída:** autorização verificável ou encerramento sem implementação.

### Fase 1 — Schemas, parser e testes

1. Criar `docs/contracts/schemas/front-matter-governed.schema.json`:
   - `document_type: contrato` ao ser registrado
   - enum de `workflow_status` copiado integralmente de `documento.schema.json`
     (13 valores; documentos em estados intermediários não devem ser rejeitados)
   - enum de `document_type` copiado integralmente de `documento.schema.json`
   - `milestones` ausente neste schema (campo exclusivo do perfil feature-spec)
2. Criar `docs/contracts/schemas/front-matter-feature-spec.schema.json`:
   - `milestones` como array com itens `enum: [M0, M1, M2, M3, M4]`
   - `milestones`, `authorized_units` e `authorized_requirements` com
     `uniqueItems: true`
   - condição: quando `mvp_status` é `ADIADO` ou `FORA_DO_ESCOPO`,
     `milestones` deve ser `[]` ou ausente
   - condição: quando `mvp_status` é `INCLUIDO`, `authorized_units`,
     `authorized_requirements`, `authorized_by` e `derived_from` são
     obrigatórios; os dois arrays de autorização têm `minItems: 1`
   - `authorized_by` referencia a decisão humana da Fase 4; `derived_from`
     contém o DEC-019
3. Registrar os dois contratos em `registro-documentos.yaml` **na mesma
   operação** que cria os arquivos dos passos 1 e 2 (qualquer `.json` em
   `docs/contracts/schemas/` não registrado é classificado como órfão).
   Executar `validate_documentation.py` imediatamente após.
4. Implementar `parse_front_matter(path, profile)`:
   - aceita front matter apenas no início lógico do arquivo
   - tolera somente BOM UTF-8 antes do delimitador `---`
   - detecta delimitador final ausente
   - usa `SafeLoader` customizado que detecta chaves duplicadas durante a
     construção do mapping, com erro identificando arquivo e chave
   - rejeita YAML inválido, raiz não-objeto e chaves duplicadas
   - valida contra o schema do perfil detectado
   - preserva o corpo Markdown sem alteração
5. Implementar `validate_governed(registered_doc)` e
   `validate_feature_spec(path)` conforme seção 4.4.
6. Implementar a função de gate `validate_front_matter()` que aplica as
   exclusões centralizadas e chama os dois validadores.
7. Implementar escopo G-FM por `--document-id`, preservando execução global
   quando o argumento não for informado.
8. Adicionar `G-FM` ao `--gate choices` do script.
9. Criar `scripts/documentation/tests/test_front_matter.py` com `unittest`:

   ```bash
   python3 -m unittest discover scripts/documentation/tests
   ```

   Cobertura obrigatória por perfil:
   - documento válido
   - front matter ausente
   - YAML inválido, delimitador final ausente, chave duplicada no primeiro
     nível e em objeto aninhado
   - campo desconhecido
   - campo divergente do registro (`governed`)
   - `workflow_status` divergente (`governed`)
   - `responsible` presente e ausente (`governed`)
   - permissão excessiva e proibição omitida (`governed`)
   - campo exclusivo do registro presente (`governed`)
   - `milestones` inválido para `mvp_status: ADIADO` (`feature-spec`)
   - item duplicado nos arrays com `uniqueItems: true`
   - autorização e derivação ausentes em feature `INCLUIDO`
   - preservação byte a byte do corpo

**Saída:** schemas registrados, parser e testes passando, G-FM disponível no
script. Nenhum documento Markdown alterado.

### Fase 2 — Registro de G-FM (modo não obrigatório)

**Pré-condição verificada:** `gate_id` é string livre em
`docs/contracts/schemas/workflow.schema.json`; nenhuma alteração desse schema é
necessária para registrar G-FM.

1. Adicionar G-FM ao **catálogo de gates** em `workflow-documentacao.yaml`.
   Não adicionar a `required_gates` ainda.
2. Incrementar a versão do workflow no YAML e no registro e atualizar seu
   `content_hash`.
3. Executar `validate_documentation.py` (G-ARCH, G0, G1) para confirmar zero
   regressões na adição do gate ao catálogo.

**Saída:** G-FM registrado no catálogo, hash atualizado, sem enforcement.

### Fase 3 — Baseline de G-FM

1. Executar `validate_documentation.py --gate G-FM`.
2. Verificar que todas as falhas são "front matter ausente" — nenhum outro
   tipo de erro deve aparecer aqui. Qualquer erro diferente indica problema
   não previsto e interrompe o plano.
3. Registrar o resultado como evidência de não-conformidade esperada:
   - arquivo:
     `docs/evidence/gates/resultado-g-fm-baseline-pre-migracao.yaml`
   - wrapper YAML: `gate_result`
   - schema: `docs/contracts/schemas/resultado-gate.schema.json`
   - `gate_result_id: GATE-RESULT-G-FM-BASELINE-PRE-MIGRACAO`
   - `gate_id: G-FM`, `status: fail`, falhas esperadas e próximas ações
   - `document_id: null`, `version: null` e `content_hash: null`, pois o baseline
     é global
   - entrada no registro com `document_type: evidencia`, versão, hash e
     relacionamentos com G-FM, workflow e migração
   - criar arquivo e entrada no registro na mesma operação

**Saída:** baseline documentado como evidência registrada. A não-conformidade
de G-FM é esperada e não é regressão.

### Fase 4 — Autorização do mapa de features

O DEC-019 autoriza unidades MVP e RFs, não o mapa de seis features. O mapa
abaixo é **proposta pendente de aprovação humana**. A decisão resultante recebe
o identificador reservado `DOC-CEPRAEA-DEC-MAPA-FEATURES`.

| `feature_id` | Título | `mvp_status` | `milestones` | `authorized_units` | `authorized_requirements` |
| --- | --- | --- | --- | --- | --- |
| `FT-ATLETAS` | Gestão de atletas | `INCLUIDO` | pendente | pendente | pendente |
| `FT-TREINADORES` | Gestão de treinadores | `INCLUIDO` | pendente | pendente | pendente |
| `FT-TREINOS` | Registro de treinos | `INCLUIDO` | `[M2]` | `[MVP-03, MVP-04]` | pendente |
| `FT-PRESENCAS` | Controle de presenças | `INCLUIDO` | `[M3]` | `[MVP-05]` | pendente |
| `FT-JOGOS` | Gestão de jogos | `ADIADO` | `[]` | `[]` | `[RF-015, RF-016, RF-017]` |
| `FT-AVALIACOES` | Avaliações | `ADIADO` | `[]` | `[]` | localizar rastreabilidade |

Antes de criar qualquer arquivo:

1. Preencher separadamente `authorized_units` e `authorized_requirements` com
   referências verificáveis ao DEC-019.
2. Demonstrar a derivação feature → MVP → RF → milestone.
3. Corrigir o mapa se a derivação revelar inconsistências.
4. Obter aprovação explícita de Davi sobre o mapa completo.
5. Criar `docs/controlled/candidates/decisao-mapa-features.md` e registrar
   `DOC-CEPRAEA-DEC-MAPA-FEATURES` na mesma operação, com front matter
   `governed`.
6. Validar por `--document-id` e percorrer
   `RASCUNHO → EM_REVISAO → CANONICA_VIGENTE`, publicando em
   `docs/canonical/decisions/decisao-mapa-features.md`.
7. Prosseguir para a Fase 5 somente depois da aprovação.

**Saída:** mapa de features aprovado por humano, com derivação DEC-019
documentada.

### Fase 5 — Feature specs

Após aprovação da Fase 4, criar `src/features/<feature>/README.md` para as
6 features aprovadas:

1. Criar o arquivo com front matter do perfil `feature-spec`.
2. Executar `validate_feature_spec(path)` antes de criar o próximo arquivo.
3. Não registrar em `registro-documentos.yaml` — G-FM descobre feature specs
   explicitamente pelo glob `src/features/**/*.md`.

**Saída:** 6 arquivos criados e validados individualmente.

### Fase 6 — Migração dos documentos não canônicos

Escopo preciso: documentos registrados, cujo `current_path` termine em `.md`,
perfil `governed`, `workflow_status` diferente de `CANONICA_VIGENTE`, não
listados nas exclusões da seção 2.

Por documento, na ordem `governance` → `sources` → `validation/reports` →
`derived` → `controlled` (incluindo `docs/README.md`):

1. Adicionar front matter mínimo do perfil `governed`.
2. Determinar a nova `version` e gravá-la no front matter e no registro.
3. Calcular o SHA-256 dos bytes resultantes.
4. Atualizar `content_hash` no registro na mesma operação.
5. Executar G-FM com `--document-id` para o documento recém-migrado.
6. Ao concluir, verificar a cobertura de todos os documentos não canônicos sem
   exigir ainda os dois canônicos pré-FM da Fase 7.
7. Interromper na primeira regressão. Nunca processar em lote.

**Saída:** todos os documentos não canônicos com front matter válido e hashes
sincronizados. G-FM passa para cada um antes de avançar.

### Fase 7 — Novas revisões dos documentos canônicos

Alteração direta dos bytes aprovados é proibida. O workflow LEAN admite, para
uma nova revisão, somente `RASCUNHO → EM_REVISAO → CANONICA_VIGENTE`.

#### Fase 7A — Autorizar o modelo de versões simultâneas

O registro atual exige `document_id` único e não representa simultaneamente uma
versão canônica vigente e sua revisão em andamento. Antes de alterar qualquer
canônico, Davi deve registrar e aprovar
`DOC-CEPRAEA-DEC-MODELO-VERSOES`, autorizando a seguinte extensão:

1. `document_id` continua sendo a identidade permanente.
2. A unicidade operacional passa a ser o par `(document_id, version)`.
3. `current_path` continua globalmente único.
4. Pode existir uma versão `CANONICA_VIGENTE` e uma versão nova em `RASCUNHO` ou
   `EM_REVISAO` para o mesmo `document_id`.
5. Evidências e aprovações identificam sempre `document_id`, `version` e
   `content_hash`.
6. Somente uma versão por `document_id` pode estar `CANONICA_VIGENTE`.
7. `validate_documentation.py`, consultas ao registro e scripts de proveniência
   devem desambiguar registros por versão.
8. A validação de caminho deve aceitar `docs/archive/superseded/` para versões
   `SUPERADA` e `docs/archive/revoked/` para versões `REVOGADA`, conforme a
   política.

Essa extensão não muda os campos de `documento.schema.json`, mas exige alteração
autorizada das regras de unicidade e resolução de referências no validador.
Se a extensão for rejeitada, a Fase 7 para sem modificar canônicos.

#### Fase 7B — Revisar e substituir cada canônico

Para cada um dos dois documentos canônicos pré-FM listados nesta fase:

1. Manter a versão vigente e seus bytes intactos durante toda a revisão.
2. Criar registro de nova versão com o mesmo `document_id`, nova `version`,
   `workflow_status: RASCUNHO` e caminho em `docs/controlled/candidates/`.
3. Criar a nova revisão e seu registro na mesma operação, com front matter.
4. Validar a nova versão com G-FM por `--document-id` e `--version`.
5. Transitar a nova versão de `RASCUNHO` para `EM_REVISAO` por T-DOC-001.
6. Executar G-ARCH, G0, G1 e G-FM para a versão em revisão.
7. Produzir nova aprovação vinculada ao novo hash.
8. Em uma operação autorizada e atômica:
   - transitar a versão anterior por T-DOC-004 para `SUPERADA`
   - mover a versão anterior para `docs/archive/superseded/`
   - preservar seu `canonical_path` histórico
   - transitar a nova versão por T-DOC-003 para `CANONICA_VIGENTE`
   - mover a nova versão ao caminho canônico
   - atualizar caminhos, relacionamentos e hashes
9. Executar G-FM global depois que os dois canônicos forem substituídos.

`build_provenance_catalog.py` é executado somente quando a revisão do contexto
afetar a fonte especializada que ele processa; não verifica a DEC-019.

Documentos canônicos atuais:

- `docs/canonical/context/contexto-cepraea-beach-pro.md`
- `docs/canonical/decisions/decisao-019-mvp-sintetico.md`

Cada canônico é um commit atômico independente.

**Saída:** canônicos migrados com nova revisão, nova aprovação, integridade
verificada e versão anterior arquivada.

### Fase 8 — Enforcement de G-FM

**Condição de entrada:** decisão humana específica de Davi autorizando G-FM
como gate obrigatório. A autorização da Fase 0 cobre os schemas e não substitui
esta decisão. A autorização é registrada como
`DOC-CEPRAEA-DEC-ENFORCEMENT-G-FM`.

1. Verificar que todos os documentos governados passam G-FM sem erros.
2. Autorizar e registrar G-FM exatamente nestes pontos:
   - `INIT-DOC-001`
   - `T-DOC-001` — `RASCUNHO` para `EM_REVISAO`
   - `T-DOC-003` — `EM_REVISAO` para `CANONICA_VIGENTE`
3. Adicionar G-FM a `required_gates` da inicialização e das transições em
   `workflow-documentacao.yaml`.
4. Incrementar a versão do workflow no YAML e no registro e atualizar seu
   `content_hash`.
5. Executar `validate_documentation.py` completo para confirmar zero regressões.

**Saída:** G-FM ativo como gate obrigatório nas transições definidas.

### Fase 9 — Novos documentos de contexto para agentes

Os três documentos começam como `RASCUNHO` em caminhos não canônicos e
percorrem o workflow normal. Nenhum nasce diretamente em `docs/canonical/`.

**Condição de entrada:** Davi autoriza os três documentos e a atualização mínima
da política e do validador para suportar caminhos de revisão de `matriz` e
`glossario`, além do destino `docs/canonical/matrices/`. A autorização é
registrada como `DOC-CEPRAEA-DEC-CONTEXTO-AGENTES`.

| Arquivo | `document_type` | Caminho de revisão | Caminho canônico |
| --- | --- | --- | --- |
| `guia-triagem-agente.md` | `contexto` | `docs/controlled/candidates/guia-triagem-agente.md` | `docs/canonical/context/guia-triagem-agente.md` |
| `mapa-decisoes-mvp.md` | `matriz` | `docs/governance/matrices/mapa-decisoes-mvp.md` | `docs/canonical/matrices/mapa-decisoes-mvp.md` |
| `vocabulario-dominio.md` | `glossario` | `docs/controlled/candidates/vocabulario-dominio.md` | `docs/canonical/glossary/vocabulario-dominio.md` |

Antes de criar os arquivos:

1. Atualizar, com autorização, a política arquitetural para incluir
   `docs/canonical/matrices/`.
2. Atualizar `EXPECTED_PATH_RE` para aceitar:
   - `matriz` em revisão em `docs/governance/matrices/` e canônica em
     `docs/canonical/matrices/`
   - `glossario` em revisão em `docs/controlled/candidates/` e canônico em
     `docs/canonical/glossary/`
3. Atualizar hashes, versões e evidências dos artefatos normativos alterados.

Por documento:

1. Criar arquivo **e** registrá-lo no registro na mesma operação.
2. Adicionar front matter do perfil `governed` com `workflow_status: RASCUNHO`.
3. Verificar antes do commit:
   - ausência de `previous_paths` nas `relationships` — `validate_g0()` exige
     exatamente 10 registros com esse campo (contagem hardcoded); novo documento
     com `previous_paths` quebraria G0
   - todos os links locais apontam para caminhos existentes —
     `validate_links()` varre `docs/**/*.md` e falha em links quebrados
4. Validar individualmente por `--document-id`.
5. Percorrer `RASCUNHO → EM_REVISAO → CANONICA_VIGENTE` antes de criar o
   próximo documento.

**Saída:** três documentos registrados, aprovados e `CANONICA_VIGENTE` em
caminhos compatíveis com seus tipos.

### Fase 10 — Encerramento

1. Executar todos os testes: `python3 -m unittest discover scripts/documentation/tests`.
2. Executar `validate_documentation.py` completo (todos os gates, incluindo G-FM).
3. Executar `build_provenance_catalog.py` somente se a fonte especializada de
   contexto tiver sido alterada.
4. Atualizar `docs/README.md` com seção "Triagem por agentes de IA", aplicando o
   protocolo atômico da seção 4.3 e G-FM por `--document-id`.
5. Atualizar `docs/inventario-documentos.md` pelo mesmo protocolo.
6. Produzir relatório final de cobertura por perfil.

**Saída:** sistema implantado, documentado e verificado.

## 8. Verificação end-to-end

```bash
python3 -m unittest discover scripts/documentation/tests
python3 scripts/documentation/validate_documentation.py
python3 scripts/documentation/validate_documentation.py --gate G-FM
# Somente para a proveniência especializada do contexto:
python3 scripts/documentation/build_provenance_catalog.py
markdownlint-cli2 .inicio/PLANO-FRONT-MATTER-AUTORITATIVO.md
git diff --check
```

`build_provenance_catalog.py` não é verificador genérico dos canônicos. A
verificação global de hashes pertence a `validate_documentation.py`.

O plano está em `.inicio/`, fora do lint e da formatação automáticos. A chamada
ao markdownlint acima é manual. Prettier não é executado sobre este plano.

## 9. Riscos

| Risco | Mitigacao |
| ----- | --------- |
| Hash em cascata — front matter muda SHA-256 de todos os `.md` | Atualizar `content_hash` no registro na mesma operacao, nunca separado |
| `CANONICA_VIGENTE` — aprovacao invalidada por alteracao de bytes | Criar nova revisao (Fase 7); nunca alterar diretamente os bytes aprovados |
| `workflow_status` desatualizado no front matter | Protocolo atomico da secao 4.3 obrigatorio em toda transicao |
| Mapa de features invalido antes de Fase 4 | Fase 4 bloqueia criacao de arquivos sem aprovacao humana do mapa |
| `validate_g0()` quebra com novo documento contendo `previous_paths` | Verificar ausencia de `previous_paths` antes de cada commit na Fase 9 |
| Baseline pré-FM com erros preexistentes mascara regressoes de G-FM | Fase -1 obrigatoria: baseline limpo antes de qualquer alteracao |
| G-FM global impede migracao sequencial enquanto restam arquivos sem front matter | Validar por documento durante a fase e executar o gate global somente ao final |
| Registro atual não representa duas versões simultaneas do mesmo documento | Fase 7A exige autorizacao do modelo composto `(document_id, version)` |

## 10. Arquivos previstos

### Criar, se autorizado

- `docs/contracts/schemas/front-matter-governed.schema.json`
- `docs/contracts/schemas/front-matter-feature-spec.schema.json`
- `scripts/documentation/tests/test_front_matter.py`
- `docs/evidence/gates/resultado-g-fm-baseline-pre-migracao.yaml`
- Documento de decisão `DOC-CEPRAEA-DEC-MAPA-FEATURES` em caminho definido
  pelo workflow
- Decisões registradas `DOC-CEPRAEA-DEC-MODELO-VERSOES`,
  `DOC-CEPRAEA-DEC-ENFORCEMENT-G-FM` e
  `DOC-CEPRAEA-DEC-CONTEXTO-AGENTES`
- `src/features/atletas/README.md`
- `src/features/treinadores/README.md`
- `src/features/treinos/README.md`
- `src/features/presencas/README.md`
- `src/features/jogos/README.md`
- `src/features/avaliacoes/README.md`
- Revisões e versões canônicas dos três documentos da Fase 9, nos caminhos
  definidos naquela fase

### Alterar, se autorizado

- `scripts/documentation/validate_documentation.py`
- `docs/governance/policies/politica-arquitetura-documental.md` (Fase 9,
  mediante autorização específica)
- `docs/registry/registro-documentos.yaml`
- `docs/registry/workflow-documentacao.yaml`
- Todos os documentos do escopo da Fase 6 (migração sequencial)
- `docs/README.md`
- `docs/inventario-documentos.md`
- Documentos canônicos (via nova revisão na Fase 7)

### Não alterar por este plano

- `docs/contracts/schemas/documento.schema.json`
- `docs/contracts/schemas/workflow.schema.json`
- `src/**/*.ts`, `src/**/*.tsx`
- `CLAUDE.md`, `README.md` da raiz

## 11. Critérios de conclusão

O plano termina quando:

- Fase −1 passou: baseline limpo, sem erros preexistentes
- os dois schemas existem e estão registrados
- `test_front_matter.py` passa com toda a cobertura obrigatória
- G-FM ativo em modo registro com baseline documentado
- mapa de features aprovado por
  `DOC-CEPRAEA-DEC-MAPA-FEATURES`, com derivação DEC-019
- 6 feature specs criadas e validadas
- todos os documentos não canônicos do escopo migrados sequencialmente
- modelo `(document_id, version)` autorizado e validado
- documentos `CANONICA_VIGENTE` migrados por nova revisão, nova aprovação e
  arquivamento da versão anterior
- G-FM ativo como gate obrigatório nas transições definidas
- três documentos para agentes aprovados e `CANONICA_VIGENTE`
- `build_provenance_catalog.py` passa quando aplicável à fonte especializada
- relatório final com cobertura e exclusões declaradas com precisão
- hashes sincronizados em todo o registro

## 12. Regra de parada

Bloqueia a execução:

- Fase −1 não passou (erros preexistentes ativos)
- ausência de autorização corretiva para a Fase −1
- violação de schema vigente
- divergência entre front matter e registro
- falha em `build_provenance_catalog.py` quando a fonte especializada estiver
  no escopo
- alteração direta de bytes de documento `CANONICA_VIGENTE`
- modelo de versões simultâneas não autorizado antes da Fase 7
- enforcement de G-FM não autorizado antes da Fase 8
- arquitetura de caminhos de matriz e glossário não autorizada antes da Fase 9
- hash desatualizado após alteração de conteúdo
- criação de feature spec sem mapa aprovado na Fase 4
- etapa tecnicamente inexequível

Não bloqueia:

- preferência de nomenclatura
- arquitetura alternativa mais sofisticada
- melhoria sem evidência de necessidade
- recomendação para trabalho futuro

## 13. Relação com os planos anteriores

Este documento substitui para fins de execução:

- `PLANO-FRONT-MATTER-CORRIGIDO.md` — revisão de escopo
- `Sistema Front Matter YAML CEPRAEA Beach Pro.md` — plano operacional original
- `PLANO-FRONT-MATTER-AUTORITATIVO.md` v1 (2026-07-27) — revisão estrutural v1
- `PLANO-FRONT-MATTER-AUTORITATIVO.md` v2 (2026-07-28) — revisão estrutural v2

Todos permanecem como evidência histórica da orquestração. Em caso de
conflito, este plano é autoritativo.
