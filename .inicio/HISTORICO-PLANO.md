# Plano: Sistema Front Matter YAML — CEPRAEA Beach Pro

## Contexto

O projeto possui governança documental em `docs/` com registro mestre YAML e scripts Python de validação. Alguns documentos já têm front matter parcial e inconsistente. O objetivo é criar um sistema coerente onde arquivos `.md` no escopo abaixo sejam auto-descritivos, com front matter validado contra schema e processável pelos scripts Python e agentes de IA (Claude Code, Codex e futuros agentes).

**Princípio central:** `registro-documentos.yaml` é a fonte de verdade para metadados de governança. O front matter é o índice de triagem — contém apenas o necessário para decidir *se* o documento é relevante, sem ler o corpo.

---

## Escopo de arquivos `.md` cobertos

| Grupo | Localização | Tratamento |
| --- | --- | --- |
| Documentos governados | `docs/**/*.md` | Front matter + G-FM |
| Feature specs | `src/features/*/README.md` | Front matter + validação própria |
| Contexto de agentes | 3 novos documentos nos caminhos da tabela abaixo | Front matter desde a criação |

Fora do escopo nesta fase: `README.md` raiz, `CLAUDE.md`, arquivos em `.claude/`.

**Cobertura dos docs existentes** é determinada por manifesto gerado a partir do registro, armazenado em `docs/registry/front-matter-migration.yaml` (arquivo separado — não no schema de cada documento). Critério: todo registro com `current_path` começando em `docs/` e terminando em `.md`, excluindo `CANONICA_VIGENTE`. Cada entrada no manifesto:

```yaml
front_matter_migration:
  DOC-GOV-POL-ARQUITETURA:
    status: pending          # pending | migrated | explicitly_excluded
```

`reason` deve ser omitido para `pending` e `migrated`. Ele é obrigatório somente para exclusões explícitas:

```yaml
front_matter_migration:
  DOC-EXEMPLO:
    status: explicitly_excluded
    reason: "Exclusão autorizada pela decisão documental correspondente."
```

A Fase 7 só começa quando nenhuma entrada estiver com `status: pending`.

---

## Schema de front matter

### Documentos `docs/` — campos e regras de sincronização com o registro

```yaml
---
document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
title: "DEC-019 — Recorte e autorização do MVP sintético"
document_type: decisao
version: "0.1.1"
responsible: Davi Sermenho
permitted_uses:
  - decisao_vigente
prohibited_uses:
  - aprovacao_por_inferencia
  - dados_reais
---
```

**Regras de sincronização com `registro-documentos.yaml`** (todas verificadas pelo G-FM):

| Campo | Regra |
| --- | --- |
| `document_id` | Igual ao registro |
| `title` | Igual ao registro |
| `document_type` | Igual ao registro |
| `version` | Igual ao registro |
| `responsible` | Igual ao registro **quando o campo existe no registro**; omitido do front matter quando ausente do registro |
| `permitted_uses` | Subconjunto de `authority_scope.permitted_uses` do registro |
| `prohibited_uses` | Superconjunto ou igual a `authority_scope.prohibited_uses` do registro |

**Ficam somente no registro (nunca no front matter):**
`content_hash`, `current_path`, `canonical_path`, `workflow_status`, `registration_status`, `naming_conformance`, `directory_conformance`, `migration_required`, `relationships`.

`workflow_status` não integra o front matter porque é um estado mutável. Alterá-lo dentro de uma versão aprovada modificaria os bytes e o hash histórico do artefato. Agentes e scripts devem consultar o registro mestre para determinar o estado, a vigência e o caminho atuais do documento.

**Documentos sem `responsible` no registro** (front matter omite o campo):
`docs/README.md`, `politica-arquitetura-documental.md`, `relatorio-auditoria-acervo.md`, `workflow-documentacao.md`, `relatorio-migracao-arquitetura.md`, `relatorio-ingestao-legado.md`, `relatorio-g2-proveniencia-inicial.md`, `relatorio-g2-proveniencia-aprovada.md`.

### Feature specs `src/features/` — schema próprio

```yaml
---
feature_id: FT-ATLETAS
title: "Feature: Gestão de atletas"
document_type: feature_spec
mvp_status: INCLUIDO           # INCLUIDO | ADIADO | FORA_DO_ESCOPO
milestones:
  - M2
entities:
  - atleta
dependencies: []
decision_ref: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
decision_effect: INCLUDED      # INCLUDED | DEFERRED | OUT_OF_SCOPE
---
```

Para feature adiada:

```yaml
---
feature_id: FT-JOGOS
title: "Feature: Jogos"
document_type: feature_spec
mvp_status: ADIADO
milestones: []
entities:
  - jogo
dependencies: []
decision_ref: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
decision_effect: DEFERRED
---
```

`decision_ref` identifica o documento que governa a feature; `decision_effect` registra o efeito: `INCLUDED` (autorizado), `DEFERRED` (adiado), `OUT_OF_SCOPE` (fora do produto). O schema impõe coerência: `DEFERRED` exige `milestones: []`; `INCLUDED` exige pelo menos um milestone.

**Mapeamento técnico proposto a partir das unidades e marcos da DEC-019, sujeito a validação explícita de Davi antes da Fase 1:**

| Feature | Unidades MVP | Milestones | mvp_status | decision_effect |
| --- | --- | --- | --- | --- |
| `treinadores` | MVP-01 | `[M1]` | INCLUIDO | INCLUDED |
| `atletas` | MVP-02 | `[M2]` | INCLUIDO | INCLUDED |
| `treinos` | MVP-03 | `[M2]` | INCLUIDO | INCLUDED |
| `presencas` | MVP-04, MVP-05 | `[M2, M3]` | INCLUIDO | INCLUDED |
| `jogos` | — | `[]` | ADIADO | DEFERRED |
| `avaliacoes` | MVP-08 | `[M3]` | INCLUIDO | INCLUDED |

Esta tabela é uma derivação técnica: `treinadores → MVP-01` é interpretação arquitetural; `avaliacoes → MVP-08` é plausível mas MVP-08 não usa a palavra "avaliações". Requer aprovação de Davi.

A fonte processável aprovada será `docs/registry/feature-scope.yaml` (`document_type: registro`) com estrutura:

```yaml
feature_scope:
  FT-ATLETAS:
    mvp_units: [MVP-02]
    milestones: [M2]
    decision_ref: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
    decision_effect: INCLUDED
    mvp_status: INCLUIDO
```

### Documentos de contexto para agentes

Os três documentos são criados **já com front matter válido** — não passam por migração posterior. Cada um usa o tipo semântico correto.

O glossário nasce em `docs/controlled/bases/` enquanto estiver em `RASCUNHO`, passa para `docs/controlled/candidates/` ao alcançar `EM_REVISAO` e somente entra em `docs/canonical/glossary/` após alcançar `CANONICA_VIGENTE`. A regra é determinada conjuntamente pelo tipo documental e pelo estado registrado.

| Documento | Tipo | Caminho inicial (RASCUNHO) |
| --- | --- | --- |
| Guia de triagem para agentes | `protocolo` | `docs/governance/protocols/guia-triagem-agente.md` |
| Mapa RFs × feature × marco | `matriz` | `docs/governance/matrices/mapa-decisoes-mvp.md` |
| Vocabulário de domínio | `glossario` | `docs/controlled/bases/vocabulario-dominio.md` |

---

## Fases de implementação

### Fase preliminar — Autorização da extensão do LEAN

`NOVOS_CONTRATOS` e `NOVAS_MATRIZES` constam em `out_of_scope` em `workflow-documentacao.yaml`. Esta fase torna as extensões necessárias explicitamente autorizadas, com escopo restrito — não é autorização genérica para qualquer contrato ou matriz futura.

**Escopo autorizado:**

A extensão do perfil LEAN autoriza exclusivamente os seguintes artefatos:

**Contratos processáveis:**

- `front-matter.schema.json`
- `front-matter-feature-spec.schema.json`
- `front-matter-migration.schema.json`
- `feature-scope.schema.json`

**Artefatos de governança processáveis ou derivados:**

- `front-matter-migration.yaml` — manifesto de cobertura da migração
- `feature-scope.yaml` — fonte processável aprovada do escopo das features
- `mapa-decisoes-mvp.md` — matriz derivada entre features, RFs, unidades MVP e marcos

A autorização não se estende automaticamente a outros contratos, registros ou matrizes futuros.

A remoção de `NOVOS_CONTRATOS` e `NOVAS_MATRIZES` de `out_of_scope` deve ser acompanhada de registro narrativo explícito dessa limitação em `workflow-documentacao.md`.

**Ações:**

1. Criar uma decisão documental específica, por exemplo `DOC-CEPRAEA-DEC-EXTENSAO-FRONT-MATTER`, para autorizar a extensão restrita do perfil LEAN.

2. A decisão deve identificar expressamente:
   - os quatro contratos autorizados;
   - os três artefatos processáveis ou derivados autorizados;
   - a futura criação do gate `G-FM`;
   - os documentos de governança que poderão ser alterados;
   - a proibição de interpretar a decisão como autorização genérica para novos contratos, registros, matrizes ou gates;
   - a obrigação de preservar `G-ARCH`, `G0` e `G1`.

3. Registrar a decisão, calcular seu hash e submetê-la ao workflow documental vigente. A extensão somente pode prosseguir depois da decisão explícita de Davi.

4. Remover `NOVOS_CONTRATOS` e `NOVAS_MATRIZES` da lista `out_of_scope` em `docs/registry/workflow-documentacao.yaml`, preservando no workflow uma limitação processável da autorização.

5. Registrar a limitação na estrutura já aceita `global_invariants`, por exemplo:

   ```yaml
   global_invariants:
     - invariant_id: INV-LEAN-FRONT-MATTER
       rule: >-
         A extensão do perfil LEAN autoriza exclusivamente os contratos
         front-matter, front-matter-feature-spec, front-matter-migration e
         feature-scope, além dos artefatos front-matter-migration.yaml,
         feature-scope.yaml e mapa-decisoes-mvp.md. Nenhum outro contrato,
         registro, matriz ou gate é autorizado por esta extensão.
   ```

6. Atualizar `DOC-REG-WF-DOCUMENTACAO`:
   - incrementar `workflow.version` e a versão documental para `0.3.0`;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro mestre.

7. Atualizar `DOC-GOV-WF-DOCUMENTACAO`:
   - registrar narrativamente a extensão restrita;
   - incrementar a versão documental para `0.3.0`;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro mestre.

8. Atualizar `DOC-REG-ENTRADA-DOCUMENTACAO`:
   - alterar `docs/README.md` para refletir a extensão restrita do LEAN;
   - incrementar sua versão para `0.3.0`;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro mestre.

9. Atualizar `docs/governance/policies/politica-arquitetura-documental.md`:
   - documentar a regra de caminho dependente de tipo e estado;
   - incrementar sua versão;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro.

10. Não criar aprovações documentais individuais somente porque esses arquivos foram editados. Uma aprovação documental deve ser criada apenas quando uma versão percorrer formalmente `RASCUNHO → EM_REVISAO → CANONICA_VIGENTE`.

11. Executar `python3 scripts/documentation/validate_documentation.py`.

12. Confirmar que `G-ARCH`, `G0` e `G1` passam sem divergência entre decisão, política, workflow narrativo, workflow processável, README e registro.

### Fase 0 — Fundação de schemas, manifesto e tooling

O status da migração permanece exclusivamente no manifesto `docs/registry/front-matter-migration.yaml`. O plano não altera `documento.schema.json` para armazenar esse status dentro de cada registro.

1. Criar `docs/contracts/schemas/front-matter.schema.json`:
   - schema dos documentos Markdown governados;
   - `additionalProperties: false`;
   - campos estáveis sincronizados com o registro;
   - ausência deliberada de `workflow_status`;
   - proibição explícita de `content_hash`, caminhos, estados e relacionamentos;
   - documentação de que estado e vigência são consultados exclusivamente no registro mestre.

2. Criar `docs/contracts/schemas/front-matter-feature-spec.schema.json`:
   - schema dos READMEs de features;
   - `milestones` como lista sem duplicidade;
   - regras condicionais entre `mvp_status`, `decision_effect` e `milestones`.

3. Criar `docs/contracts/schemas/front-matter-migration.schema.json`:
   - raiz `front_matter_migration`;
   - IDs documentais como chaves;
   - `status` limitado a `pending`, `migrated` e `explicitly_excluded`;
   - `reason` obrigatório quando o status for `explicitly_excluded`;
   - propriedades desconhecidas proibidas.

4. Criar `docs/contracts/schemas/feature-scope.schema.json`:
   - IDs de feature válidos e únicos;
   - unidades limitadas a `MVP-01` até `MVP-10`;
   - milestones limitados a `M0` até `M4`;
   - `decision_ref` obrigatório;
   - coerência entre `mvp_status`, `decision_effect` e `milestones`;
   - propriedades desconhecidas proibidas.

5. Registrar individualmente os quatro contratos em `registro-documentos.yaml`, cada um com:
   - `document_id`;
   - versão;
   - caminho;
   - tipo `contrato`;
   - hash calculado;
   - autoridade e usos aplicáveis.

6. Criar `docs/registry/front-matter-migration.yaml`:
   - gerar as entradas a partir de todos os registros cujo `current_path` começa em `docs/` e termina em `.md`;
   - excluir temporariamente os documentos `CANONICA_VIGENTE`, tratados na Fase 5;
   - inicializar os demais com `status: pending`;
   - validar o arquivo contra `front-matter-migration.schema.json`.

7. Registrar o manifesto como `DOC-REG-FRONT-MATTER-MIGRATION`, incluindo versão, caminho e `content_hash`.

8. Implementar no G-ARCH a regra de caminho dependente de tipo e estado já aprovada e documentada em `docs/governance/policies/politica-arquitetura-documental.md`:

   ```text
   glossario + RASCUNHO        → docs/controlled/bases/
   glossario + EM_REVISAO      → docs/controlled/candidates/
   glossario + CANONICA_VIGENTE → docs/canonical/glossary/
   ```

9. A alteração não deve se limitar a ampliar `EXPECTED_PATH_RE`. O validador deve:
   - consultar `document_type` e `workflow_status` no registro;
   - verificar o caminho esperado para a combinação;
   - produzir erro quando tipo, estado e caminho forem incompatíveis;
   - possuir testes positivos e negativos para cada transição.

10. Confirmar que o código de enforcement corresponde exatamente à política documental aprovada.

11. Criar `requirements-dev.txt`:

    ```text
    PyYAML>=6.0,<7
    jsonschema>=4.0,<5
    pytest>=8.0,<9
    ```

12. Executar o validador documental completo e confirmar zero regressões.

### Fase 1 — Feature specs

**Pré-requisito:** Davi valida e aprova a tabela de mapeamento proposta. O resultado é `docs/registry/feature-scope.yaml` registrado e aprovado.

1. Criar `docs/registry/feature-scope.yaml` com o mapeamento aprovado por Davi.
2. Validar `feature-scope.yaml` contra `docs/contracts/schemas/feature-scope.schema.json`.
3. Registrar `DOC-REG-FEATURE-SCOPE` em `registro-documentos.yaml`, com versão, caminho, tipo `registro` e `content_hash`.
4. Criar e registrar a aprovação individual de `DOC-REG-FEATURE-SCOPE`, vinculada à versão e ao hash exatos do arquivo.
5. Criar `src/features/<feature>/README.md` para as seis features usando exclusivamente `feature-scope.yaml` como fonte processável.
6. Criar `scripts/documentation/validate_feature_specs.py` que:
   - valida primeiro `feature-scope.yaml` contra `feature-scope.schema.json`;
   - interrompe a execução se a fonte processável for estruturalmente inválida;
   - varre `src/features/*/README.md`;
   - valida cada Front Matter contra `front-matter-feature-spec.schema.json`;
   - confronta `feature_id`, `milestones`, `mvp_status`, `decision_ref` e `decision_effect` com `feature-scope.yaml`;
   - verifica que `decision_ref` referencia um `document_id` existente no registro;
   - detecta `feature_id` duplicado entre os READMEs.
7. Criar `scripts/documentation/tests/test_validate_feature_specs.py` com casos:
   - `feature_id` inexistente no mapa → erro
   - `milestones` divergentes do mapa → erro
   - `mvp_status` divergente do mapa → erro
   - Feature adiada com `milestones` preenchidos → erro
   - `decision_ref` inexistente no registro → erro
   - `decision_effect` incompatível com `mvp_status` → erro
   - README sem front matter → erro
   - `feature_id` duplicado → erro
   - Feature spec válida → passa
8. Atualizar `package.json`: adicionar `"validate:docs"` e integrar ao `validate`

### Fase 2 — Implementação e testes do G-FM

G-FM ainda não é adicionado ao workflow processável. Nesta fase ele existe como função, gate invocável e mecanismo de auditoria progressiva.

1. Implementar `validate_front_matter()` em `scripts/documentation/validate_documentation.py`:
   - exigir Front Matter no início lógico do arquivo;
   - admitir apenas BOM UTF-8 antes do delimitador inicial;
   - detectar delimitador final ausente;
   - rejeitar YAML inválido;
   - rejeitar raiz diferente de objeto;
   - rejeitar chaves duplicadas;
   - validar contra `front-matter.schema.json`;
   - aplicar as regras de sincronização dos campos estáveis;
   - rejeitar `workflow_status`, `content_hash`, caminhos e relacionamentos;
   - consultar o registro separadamente para estado, vigência e integridade.

2. Adicionar `G-FM` às opções aceitas por `--gate`, sem adicioná-lo ainda ao workflow.

3. Adicionar seleção localizada:

   ```bash
   python3 scripts/documentation/validate_documentation.py \
     --gate G-FM \
     --document-id DOC-GOV-POL-ARQUITETURA
   ```

4. Adicionar dois modos globais:

   ```bash
   # Migração progressiva: pending gera achado informativo
   python3 scripts/documentation/validate_documentation.py \
     --gate G-FM \
     --front-matter-mode audit

   # Cobertura concluída: ausência ou divergência gera falha
   python3 scripts/documentation/validate_documentation.py \
     --gate G-FM \
     --front-matter-mode enforce
   ```

5. Em modo `audit`:
   - documentos `migrated` devem ser integralmente validados;
   - documentos `pending` devem ser reportados sem impedir os gates LEAN ativos;
   - documentos `explicitly_excluded` devem exigir motivo e decisão de exclusão.

6. Em modo `enforce`:
   - nenhum documento do escopo pode permanecer `pending`;
   - ausência, parsing inválido ou divergência deve falhar;
   - exceções somente são aceitas quando formalmente registradas.

7. Criar `scripts/documentation/tests/test_validate_front_matter.py`.

8. Cobrir os casos de sincronização:
   - divergência de `document_id`;
   - divergência de `title`;
   - divergência de `document_type`;
   - divergência de `version`;
   - `responsible` indevido ou divergente;
   - `permitted_uses` excessivo;
   - `prohibited_uses` insuficiente;
   - presença proibida de `workflow_status`.

9. Cobrir os casos de parsing:
   - Front Matter ausente;
   - YAML inválido;
   - delimitador final ausente;
   - Front Matter fora do início lógico;
   - raiz que não seja objeto;
   - chave duplicada;
   - `content_hash` presente;
   - propriedade desconhecida.

10. Cobrir os modos operacionais:
    - seleção válida por `--document-id`;
    - ID inexistente;
    - `audit` com documentos pendentes;
    - `enforce` com documento pendente;
    - `enforce` com cobertura total.

11. Cobrir os casos positivos:
    - documento sincronizado com `responsible`;
    - documento sincronizado sem `responsible`;
    - corpo Markdown preservado byte a byte.

12. Executar:

    ```bash
    python3 -m pytest scripts/documentation/tests/test_validate_front_matter.py
    ```

13. A Fase 2 somente termina quando todos os testes passarem.

### Fase 3 — Baseline de auditoria

1. Executar:

   ```bash
   python3 scripts/documentation/validate_documentation.py \
     --gate G-FM \
     --front-matter-mode audit
   ```

2. Registrar separadamente:
   - documentos que já passam;
   - documentos sem Front Matter;
   - documentos com Front Matter inválido;
   - divergências entre Front Matter e registro.

3. Atualizar o manifesto inicial somente depois de comparar a baseline com o conjunto de documentos registrado.

4. A baseline é informativa e não altera o workflow ativo nem bloqueia os gates LEAN existentes.

### Fase 4 — Front matter nos docs RASCUNHO (sequencial)

Escopo determinado pelo `docs/registry/front-matter-migration.yaml`. Para cada entrada com `status: pending`, executar uma única operação atômica:

1. Adicionar o Front Matter ao arquivo `.md`.
2. Confirmar que o corpo Markdown anterior foi preservado byte a byte.
3. Calcular o novo SHA-256 do documento.
4. Atualizar o `content_hash` do documento em `registro-documentos.yaml`.
5. Alterar sua entrada no manifesto de `pending` para `migrated`.
6. Validar o manifesto contra `front-matter-migration.schema.json`.
7. Recalcular o SHA-256 de `front-matter-migration.yaml`.
8. Atualizar o `content_hash` de `DOC-REG-FRONT-MATTER-MIGRATION` no registro.
9. Executar G-FM somente para o documento migrado:

   ```bash
   python3 scripts/documentation/validate_documentation.py \
     --gate G-FM \
     --document-id <DOCUMENT_ID>
   ```

10. Executar G1 para confirmar os hashes do documento e do manifesto.

11. Executar G-FM em modo `audit` para confirmar que todos os documentos já marcados como `migrated` continuam válidos.

12. Consolidar a alteração somente se todas as verificações passarem.

Ordem sugerida: governance → sources → validation reports → derived → controlled bases → inventário → README documental.

Ao fim, nenhuma entrada no manifesto pode estar com `status: pending`.

### Fase 5 — Front matter nos docs CANONICA_VIGENTE

**Esta fase permanece bloqueada** até que a autoridade documental (Davi) decida se a adição de front matter a documentos `CANONICA_VIGENTE` é:

- **alteração material de conteúdo** → exige nova versão, nova revisão, nova aprovação individual por documento; ou
- **migração de metadata com procedimento excepcional** → exige decisão formal de Davi.

Nenhuma presunção é adotada. A fase não pode ser executada antes dessa decisão.

**A Fase 7 depende obrigatoriamente da conclusão desta fase.** Se Davi decidir não migrar os canônicos, é necessária exceção formal e explícita que altera o escopo do plano e o critério do manifesto.

### Fase 6 — Documentos de contexto para agentes

Os três documentos são criados com Front Matter válido desde o nascimento. Eles não entram no manifesto como `pending`; são inseridos diretamente como `migrated`. Cada documento é registrado e criado no mesmo commit atômico.

1. Criar `docs/governance/protocols/guia-triagem-agente.md`:
   - `document_type: protocolo` no Front Matter;
   - `workflow_status: RASCUNHO` somente no registro;
   - Front Matter completo desde o primeiro commit.

2. Criar `docs/governance/matrices/mapa-decisoes-mvp.md`:
   - `document_type: matriz` no Front Matter;
   - `workflow_status: RASCUNHO` somente no registro;
   - Front Matter completo desde o primeiro commit.

3. Criar `docs/controlled/bases/vocabulario-dominio.md`:
   - `document_type: glossario` no Front Matter;
   - `workflow_status: RASCUNHO` somente no registro;
   - Front Matter completo desde o primeiro commit.

4. Registrar os três documentos em `registro-documentos.yaml` no mesmo commit em que forem criados.

5. Inserir os três documentos em `front-matter-migration.yaml` com:

   ```yaml
   status: migrated
   reason: "Documento criado originalmente com Front Matter válido."
   ```

6. Recalcular o SHA-256 do manifesto e atualizar o hash de `DOC-REG-FRONT-MATTER-MIGRATION`.

7. Executar o validador documental completo e G-FM.

8. Aplicar as transições de caminho do glossário:

   ```text
   RASCUNHO        → docs/controlled/bases/vocabulario-dominio.md
   EM_REVISAO      → docs/controlled/candidates/vocabulario-dominio.md
   CANONICA_VIGENTE → docs/canonical/glossary/vocabulario-dominio.md
   ```

9. Em cada movimentação, atualizar atomicamente:
   - `current_path`;
   - `canonical_path`, quando aplicável;
   - links locais;
   - hash;
   - estado;
   - evidência da transição.

### Fase 7 — Encerramento

**Pré-requisitos obrigatórios:**

- Fase 4 completa (nenhuma entrada `pending` no manifesto de migração)
- Fase 5 concluída (decisão tomada e executada para os canônicos, ou exceção formal registrada)
- Fase 6 completa
- Testes das Fases 1 e 2 passando

G-FM entra no workflow **somente nesta fase**, diretamente como `blocking: true`.

1. Adicionar G-FM a `docs/registry/workflow-documentacao.yaml`:
   - Na seção `gates`: novo entry com `blocking: true` e `implementation_status: IMPLEMENTED`
   - Nas transições T-DOC-001 e T-DOC-003: adicionar `G-FM` a `required_gates`
2. Adicionar o contrato de front matter à seção `contracts` do workflow:

   ```yaml
   contracts:
     - contract_id: front_matter
       schema_path: docs/contracts/schemas/front-matter.schema.json
   ```

3. Adicionar `front_matter` a `required_contracts` nas transições T-DOC-001 e T-DOC-003
4. Atualizar `DOC-REG-WF-DOCUMENTACAO`:
   - incrementar `workflow.version` e a versão documental para `0.4.0`;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro.

5. Atualizar `DOC-GOV-WF-DOCUMENTACAO`:
   - documentar G-FM, seus contratos e suas transições;
   - incrementar a versão documental para `0.4.0`;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro.

6. Atualizar `DOC-REG-ENTRADA-DOCUMENTACAO`:
   - adicionar a seção operacional de Front Matter ao `docs/README.md`;
   - incrementar a versão documental para `0.4.0`;
   - recalcular o SHA-256;
   - atualizar `version` e `content_hash` no registro.

7. Para cada documento que deva alcançar `CANONICA_VIGENTE`, executar formalmente:
   - transição `RASCUNHO → EM_REVISAO`;
   - gates exigidos para revisão;
   - produção das evidências correspondentes;
   - transição `EM_REVISAO → CANONICA_VIGENTE`;
   - atualização de estado, caminho e registro.

8. Não criar artefato de aprovação para um documento que permaneça em `RASCUNHO`. A aprovação documental somente existe quando vinculada a uma promoção formal.

9. Para cada promoção, criar um arquivo em `docs/evidence/approvals/` com a raiz:

   ```yaml
   approval:
     approval_id: <APPROVAL_ID>
     document_id: <DOCUMENT_ID>
     version: "<VERSION>"
     content_hash: <SHA256>
     purpose: "<PURPOSE>"
     scope:
       - <SCOPE_ITEM>
     approved_by: Davi Sermenho
     authority_role: AUTORIDADE_APROVADORA
     decision: approved
     reservations: []
     non_blocking_pending_items: []
     approved_at: "<RFC3339_TIMESTAMP>"
     evidence_ids:
       - <G_ARCH_EVIDENCE_ID>
       - <G0_EVIDENCE_ID>
       - <G1_EVIDENCE_ID>
       - <G_FM_EVIDENCE_ID>
   ```

10. Validar cada aprovação contra `aprovacao.schema.json`.

11. Confirmar que todos os `evidence_ids` referenciam evidências existentes e registradas. IDs declarados sem artefatos correspondentes constituem falha.

12. Registrar cada aprovação, calcular seu hash e associá-la à versão e ao hash exatos do documento promovido.

13. Executar:

    ```bash
    python3 scripts/documentation/validate_documentation.py
    python3 scripts/documentation/validate_documentation.py \
      --gate G-FM \
      --front-matter-mode enforce
    python3 scripts/documentation/validate_feature_specs.py
    python3 scripts/documentation/build_provenance_catalog.py
    python3 -m pytest scripts/documentation/tests/
    ```

14. A Fase 7 somente termina quando:
    - G-ARCH, G0, G1 e G-FM passam;
    - todas as feature specs passam;
    - o catálogo de proveniência é gerado sem divergência;
    - o manifesto não contém `pending`;
    - todas as aprovações referenciam versões e hashes atuais.

---

## Arquivos críticos

| Arquivo | Ação |
| --- | --- |
| `docs/contracts/schemas/documento.schema.json` | Referência; não alterar para armazenar status de migração |
| `docs/contracts/schemas/front-matter.schema.json` | Criar (Fase 0) |
| `docs/contracts/schemas/front-matter-feature-spec.schema.json` | Criar (Fase 0) |
| `docs/contracts/schemas/front-matter-migration.schema.json` | Criar (Fase 0) |
| `docs/contracts/schemas/feature-scope.schema.json` | Criar (Fase 0) |
| `docs/registry/registro-documentos.yaml` | Atualizar a cada front matter + novos artefatos |
| `docs/registry/workflow-documentacao.yaml` | Fase preliminar (out_of_scope, v0.3.0) + Fase 7 (G-FM, contratos, v0.4.0) |
| `docs/registry/front-matter-migration.yaml` | Criar (Fase 0) — manifesto de cobertura |
| `docs/registry/feature-scope.yaml` | Criar (Fase 1) — fonte processável do mapeamento |
| `docs/governance/workflows/workflow-documentacao.md` | Fase preliminar + Fase 7 (narrativo sincronizado) |
| `docs/governance/policies/politica-arquitetura-documental.md` | Documentar e versionar regra tipo × estado × caminho |
| `docs/README.md` | Fase preliminar (extensão LEAN restrita) + Fase 7 (uso operacional do front matter) |
| `scripts/documentation/validate_documentation.py` | Fase 0: validação de caminho estado-dependente no G-ARCH; Fase 2: adicionar `validate_front_matter()` e G-FM |
| `scripts/documentation/validate_feature_specs.py` | Criar (Fase 1) |
| `scripts/documentation/tests/test_validate_front_matter.py` | Criar (Fase 2) |
| `scripts/documentation/tests/test_validate_feature_specs.py` | Criar (Fase 1) |
| `src/features/*/README.md` | Criar 6 arquivos (Fase 1) |
| `docs/governance/protocols/guia-triagem-agente.md` | Criar com front matter (Fase 6) |
| `docs/governance/matrices/mapa-decisoes-mvp.md` | Criar com front matter (Fase 6) |
| `docs/controlled/bases/vocabulario-dominio.md` | Criar com Front Matter em RASCUNHO; mover conforme transições |
| `package.json` | Adicionar `validate:docs` e integrar ao `validate` (Fase 1) |
| `requirements-dev.txt` | Criar (Fase 0) |

---

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Hash em cascata | Atualizar `content_hash` no registro na mesma operação atômica |
| `CANONICA_VIGENTE` — INV-LEAN-003 | Fase 5 e Fase 7 bloqueadas até decisão explícita de Davi |
| Estado intermediário (registro com doc inexistente) | Sempre criar registro + arquivo no mesmo commit |
| G-FM adicionado ao workflow antes da migração completa | G-FM entra no workflow somente na Fase 7 |
| Mapeamento de features incorreto | Validado por Davi antes da Fase 1; `feature-scope.yaml` é fonte autoritativa |
| Glossário RASCUNHO em caminho canônico | Criado em `docs/controlled/bases/`; caminho evolui por estado conforme G-ARCH |
| Autorização genérica para contratos/matrizes | Fase preliminar registra escopo restrito explicitamente no narrativo e no processável |
| Aprovação insuficiente (por conjunto em vez de por documento) | Cada documento modificado recebe aprovação individual com seu hash |
| Manifesto de migração estruturalmente inválido | Validar `front-matter-migration.yaml` contra schema próprio antes de cada consolidação |
| Hash do manifesto desatualizado após mudança de status | Recalcular o hash do manifesto e atualizar seu registro em toda operação de migração |
| `feature-scope.yaml` estruturalmente inválido | Validar contra `feature-scope.schema.json` antes de consumir o mapeamento |
| `feature-scope.yaml` violando G-ARCH | Manter o arquivo em `docs/registry/` com `document_type: registro` |
| Divergência do README durante a implementação | README atualizado já na Fase preliminar |
| Divergência narrativo × processável | Ambos atualizados na mesma operação nas Fases preliminar e 7 |
| Estado mutável dentro de artefato imutável | `workflow_status` permanece somente no registro mestre |
| Migração sequencial bloqueada por documentos pendentes | Usar `--document-id` por arquivo e modo global `audit` |
| G-FM ativado sem cobertura integral | Usar modo `enforce` somente na Fase 7 |
| Aprovação sem transição válida | Criar aprovação apenas após revisão, gates, evidências e promoção formal |
| IDs de evidência sem artefatos correspondentes | Validar existência e registro de cada evidência referenciada |
| Enforcement divergente da política | Atualizar política de arquitetura antes de alterar G-ARCH |

---

## Verificação end-to-end

```bash
python3 scripts/documentation/validate_documentation.py
python3 scripts/documentation/validate_documentation.py \
  --gate G-FM \
  --front-matter-mode enforce
python3 scripts/documentation/validate_feature_specs.py
python3 scripts/documentation/build_provenance_catalog.py
python3 -m pytest scripts/documentation/tests/
```

---

## Condicionamentos para execução

O plano está aprovado para implementação condicionado a:

1. **Decisão explícita de Davi sobre os documentos `CANONICA_VIGENTE`** — desbloqueia a Fase 5 e, por dependência, a Fase 7.

2. **Decisão documental específica autorizando a extensão restrita do perfil LEAN** — deve identificar exatamente os contratos, artefatos e o futuro gate autorizados, sem produzir autorização genérica.

3. **Validação do mapeamento de features** — Davi aprova a tabela antes da Fase 1; `feature-scope.yaml` passa a ser a fonte processável autoritativa.

4. **Remoção de `workflow_status` do Front Matter** — estado, vigência, caminho e integridade permanecem consultáveis exclusivamente no registro mestre.

5. **Aprovações vinculadas a transições formais** — nenhum artefato de aprovação pode existir sem revisão, gates, evidências e promoção correspondentes.
