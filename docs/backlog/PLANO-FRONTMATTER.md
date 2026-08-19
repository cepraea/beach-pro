# Plano reconciliado para criação do `fields-registry.md`

> **Reativado e reconciliado em 2026-08-19.** O arquivamento de 2026-08-17 deixa de valer. O
> repositório já possui seis JSON Schemas canônicos, validadores, fixtures e documentação de
> modelagem suficientes para justificar um catálogo formal de campos. Este plano foi reduzido ao
> mínimo necessário para implementação e reconciliado com o estado real de `main`.

**Versão:** 2.0  
**Status:** REATIVADO — PRONTO PARA IMPLEMENTAÇÃO  
**Arquivo físico deste plano:** `docs/backlog/PLANO-FRONTMATTER.md` (nome legado; não renomear nesta tarefa)  
**Arquivo-alvo:** `docs/modelagem/governanca/fields-registry.md`  
**Responsável humano:** Davi Sermenho  
**Data original:** 2026-08-15  
**Data da reconciliação:** 2026-08-19

---

## 1. Objetivo

Criar `docs/modelagem/governanca/fields-registry.md` como catálogo humano e semântico dos campos
aceitos pelos contratos de modelagem do CEPRAEA BEACH PRO.

O registry deve responder, para cada campo:

- qual é sua identidade;
- em qual schema e caminho ele existe;
- qual é seu significado;
- qual é sua finalidade;
- qual é seu tipo e sua obrigatoriedade;
- quais restrições relevantes o contrato executável impõe;
- qual é seu estado de governança;
- qual evidência ou fonte sustenta sua definição quando houver significado de domínio.

O registry **não substitui** os schemas executáveis. Ele explica e governa semanticamente o que os
schemas aceitam.

Regra central reconciliada:

```text
schema executável define o que é estruturalmente aceito
fields-registry.md define o que cada campo significa e por que existe
campo ativo no schema deve existir no registry
campo ativo no registry deve existir no schema
campo novo não pode ser introduzido silenciosamente
```

---

## 2. Estado real verificado do repositório

### 2.1 Artefatos existentes

Em `main`, existem atualmente os seis schemas:

```text
docs/modelagem/schemas/schema_fonte.json
docs/modelagem/schemas/schema_evidencia.json
docs/modelagem/schemas/schema_termo.json
docs/modelagem/schemas/schema_regra.json
docs/modelagem/schemas/schema_decisao.json
docs/modelagem/schemas/schema_elemento_modelo.json
```

Também existem os validadores:

```text
docs/modelagem/schemas/validar.mjs
docs/modelagem/schemas/verificar_referencias.mjs
docs/modelagem/schemas/verificar_repositorio.mjs
```

E já existe um conjunto amplo de fixtures em:

```text
docs/modelagem/schemas/fixtures/
```

Logo, a razão original para arquivar o plano — falta de massa crítica de contratos executáveis —
não se aplica mais.

### 2.2 Modelo Canônico ainda incompleto

O Modelo Canônico de domínio ainda não está consolidado integralmente. O arquivo
`docs/modelagem/dominio/modelo_canonico_dominio.md` continua sem as seções finais por `CTX-NNN`, e
`INV-001` permanece como elemento de domínio pré-semeado explicitamente validado.

Isso **não bloqueia** a criação do registry porque o objeto deste plano são os campos dos contratos
que já existem, não a conclusão de toda a modelagem do domínio.

### 2.3 Artefatos ainda inexistentes

No estado atual de `main`:

```text
docs/modelagem/governanca/                  NÃO EXISTE
docs/modelagem/governanca/fields-registry.md NÃO EXISTE
tests/test_fields_registry.py               NÃO EXISTE
metadata/cepraea_profile.yaml                NÃO EXISTE
```

Nenhum desses artefatos deve ser tratado como implantado antes de sua criação e validação.

### 2.4 `additionalProperties`

Os seis schemas atuais não estabelecem globalmente `additionalProperties: false` no objeto raiz.
Portanto, este plano não declara que propriedades desconhecidas já são bloqueadas de forma
determinística em todas as instâncias.

A criação do registry é uma camada de governança e sincronização. Alterar
`additionalProperties` é outra decisão e está fora do escopo desta implementação.

---

## 3. Posição arquitetural do `fields-registry`

### 3.1 Arquitetura executável atual

Enquanto `metadata/cepraea_profile.yaml` não existir no repositório, os seis JSON Schemas listados
na seção 2 são a fonte executável de campos desta fase de modelagem.

Fluxo atual:

```text
fontes/evidências/decisões
        ↓
Modelo Canônico e artefatos de modelagem
        ↓
seis JSON Schemas
        ↓
fields-registry.md
        ↓
validação de sincronização
```

### 3.2 Arquitetura de metadados futura já selecionada, mas ainda não materializada

O trabalho arquitetural corrente prevê um futuro `CEPRAEA Metadata Profile` em LinkML. Como esse
profile ainda não existe em `main`, este plano NÃO deve inventá-lo nem antecipar seu conteúdo.

Quando `metadata/cepraea_profile.yaml` for implementado e validado, haverá uma tarefa explícita de
reconciliação para decidir quais campos passam a ser derivados do profile LinkML e quais continuam
pertencendo aos seis contratos de modelagem existentes.

Até essa tarefa ocorrer:

```text
LinkML = arquitetura futura selecionada, não autoridade executável deste registry
JSON Schemas atuais = contratos executáveis existentes
fields-registry.md = catálogo humano sincronizado com esses contratos existentes
```

### 3.3 Não duplicar metamodelos

O registry não deve recriar `ClassDefinition`, `SlotDefinition` ou qualquer metamodelo LinkML.
Quando a integração LinkML existir, o registry deve consumir ou referenciar metadados já expressos
no profile, não criar uma segunda linguagem concorrente.

---

## 4. Escopo

### 4.1 Dentro do escopo

Catalogar campos definidos pelos seis schemas atuais, incluindo:

- propriedades obrigatórias;
- propriedades opcionais;
- propriedades condicionalmente obrigatórias;
- propriedades aninhadas;
- `enum`;
- `const`;
- `pattern`;
- `format`;
- cardinalidades relevantes (`minItems`, quando existente);
- relações condicionais expressas por `if`/`then`/`allOf`.

### 4.2 Fora do escopo

Não fazer nesta implementação:

- alterar significado de campos existentes;
- adicionar campos novos aos seis schemas;
- alterar `additionalProperties`;
- alterar migrations ou Supabase;
- alterar RLS;
- criar `cepraea_profile.yaml`;
- adicionar LinkML ao runtime do projeto;
- alterar CI na primeira implantação;
- criar changelog global novo;
- criar workflow genérico de aprovação;
- duplicar todos os detalhes dos schemas no Markdown;
- registrar dados reais ou sensíveis das atletas.

---

## 5. Fontes de autoridade e precedência

Para esta implementação, a precedência é:

```text
1. decisão humana explícita e vigente de Davi Sermenho
2. docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md
3. docs/modelagem/decisoes/registro_decisoes.md
4. seis JSON Schemas atuais
5. documentação canônica em docs/modelagem/**
6. fields-registry.md
7. exemplos e fixtures
```

O registry nunca deve alterar silenciosamente um significado já estabelecido em fonte superior.

Quando o schema não possuir informação suficiente para escrever uma definição semântica precisa,
usar estado explícito `PENDING_DEFINITION` no registry em vez de inventar significado.

---

## 6. Identidade canônica de um campo

A identidade de cada entrada é:

```text
<schema>::<json-path>
```

Exemplos:

```text
schema_fonte.json::id_fonte
schema_fonte.json::evidencia.repository_evidence.action_ref
schema_termo.json::evidencia.approval_evidence.aprovador
schema_elemento_modelo.json::promoted_by
```

Isso evita colisões entre propriedades homônimas em schemas distintos.

Não usar apenas o nome terminal do campo como identidade global.

---

## 7. Estrutura mínima do `fields-registry.md`

Criar somente as seções necessárias:

```markdown
# Fields Registry — CEPRAEA BEACH PRO

## 1. Finalidade e autoridade
## 2. Regras de sincronização
## 3. Estados
## 4. Campos
## 5. Pendências semânticas
## 6. Histórico de revisões
```

### 7.1 Estados mínimos

Usar apenas:

```text
ACTIVE
PROPOSED
DEPRECATED
REMOVED
REJECTED
PENDING_DEFINITION
```

Não criar `experimental` nesta fase sem caso real que o exija.

### 7.2 Tabela canônica de campos

Cada campo deve possuir uma linha na tabela principal com estas colunas:

```text
Field ID
Schema
Path
Type
Requirement
Constraints
Definition
Purpose
Status
Source
```

Onde:

- `Field ID` = `<schema>::<json-path>`;
- `Requirement` = `required | optional | conditional`;
- `Constraints` resume apenas `enum`, `const`, `pattern`, `format`, cardinalidade e condição material;
- `Definition` descreve significado, não sintaxe;
- `Purpose` explica por que o campo existe;
- `Source` aponta para schema, decisão, evidência ou documento que sustenta a definição.

Não repetir exemplos válidos/inválidos em todos os campos por padrão. Exemplos só são obrigatórios
quando ajudam a distinguir um caso não óbvio ou quando um teste depende deles.

---

## 8. Inventário: não usar a contagem histórica de 60 como autoridade

A versão 1.1 fixava manualmente `TOTAL = 60 obrigações schema::campo` para a Fase 1.

Essa contagem é agora tratada apenas como dado histórico do plano antigo.

A implementação deve derivar o inventário diretamente dos seis schemas no commit/branch em que a
tarefa for executada.

Regra:

```text
EXPECTED_FIELDS = recursive_properties(all six schemas)
```

O algoritmo deve percorrer, no mínimo:

- `properties`;
- objetos aninhados;
- `required`;
- `if`/`then`;
- `allOf`;
- `enum`;
- `const`;
- `pattern`;
- `format`.

A quantidade final de campos deve ser **resultado da extração**, nunca requisito hard-coded.

---

## 9. Regra de sincronização

O registry e os schemas devem satisfazer:

```text
ACTIVE_SCHEMA_FIELDS == ACTIVE_REGISTRY_FIELDS
```

Com estas interpretações:

```text
campo existente no schema e ausente do registry
→ FAIL: UNCATALOGUED_SCHEMA_FIELD

campo ACTIVE no registry e ausente do schema
→ FAIL: ORPHAN_ACTIVE_REGISTRY_FIELD

campo PROPOSED no registry e ausente do schema
→ permitido

campo DEPRECATED ainda existente no schema
→ permitido, se documentado

campo REMOVED ausente do schema
→ permitido
```

O teste não deve tentar validar decisões de negócio que os schemas não expressam.

---

## 10. Implementação atômica

### FR-001 — Criar registry e inventário estrutural

**Operation class:** `documentation_change`

Criar:

```text
docs/modelagem/governanca/fields-registry.md
```

Ações:

1. criar `docs/modelagem/governanca/`;
2. ler os seis schemas atuais;
3. extrair recursivamente todos os campos;
4. criar uma linha por `<schema>::<path>`;
5. preencher `Schema`, `Path`, `Type`, `Requirement` e `Constraints` somente a partir do contrato real;
6. marcar `Definition`/`Purpose` como `PENDING_DEFINITION` quando o significado não estiver sustentado.

Critérios de aceitação:

```text
FR-001-AC-01 registry existe
FR-001-AC-02 nenhum campo é inventado
FR-001-AC-03 nenhum campo atual do schema é omitido
FR-001-AC-04 identidade usa schema::path
FR-001-AC-05 required/optional/conditional deriva do schema real
FR-001-AC-06 nenhuma definição sem fonte é apresentada como fato
```

### FR-002 — Reconciliar significado dos campos

**Operation class:** `documentation_change`

Para cada entrada:

1. usar `description` do próprio schema quando suficiente;
2. consultar `docs/modelagem/decisoes/registro_decisoes.md`;
3. consultar os artefatos de domínio/conhecimento relevantes;
4. preencher `Definition`, `Purpose` e `Source`;
5. manter `PENDING_DEFINITION` se houver lacuna real.

Não acessar dados pessoais das atletas para produzir exemplos.

Critérios de aceitação:

```text
FR-002-AC-01 definição não repete apenas o nome do campo
FR-002-AC-02 definição e finalidade permanecem distintas
FR-002-AC-03 fonte é identificável
FR-002-AC-04 lacunas permanecem explícitas
FR-002-AC-05 nenhuma decisão nova é inventada pelo Executor
```

### FR-003 — Criar teste determinístico de sincronização

**Operation classes:** `code_change`, `documentation_change`

Criar:

```text
tests/test_fields_registry.py
```

O teste deve:

1. carregar os seis schemas;
2. extrair recursivamente os field IDs esperados;
3. ler a tabela canônica do `fields-registry.md`;
4. comparar os conjuntos;
5. falhar com lista explícita de campos ausentes ou órfãos;
6. não depender de rede;
7. não depender de pacote novo se a biblioteca padrão do Python for suficiente.

Critérios de aceitação:

```text
FR-003-AC-01 teste positivo passa com registry sincronizado
FR-003-AC-02 remover uma entrada do registry faz o teste falhar
FR-003-AC-03 adicionar ACTIVE inexistente no schema faz o teste falhar
FR-003-AC-04 PROPOSED inexistente no schema não gera falso FAIL
FR-003-AC-05 mensagem de erro identifica field IDs divergentes
```

### FR-004 — Executar validação existente + novo teste

**Operation class:** `code_change`

Executar localmente:

```bash
node docs/modelagem/schemas/validar.mjs
node docs/modelagem/schemas/verificar_referencias.mjs
node docs/modelagem/schemas/verificar_repositorio.mjs
python3 -m unittest discover -s tests -v
```

Se o projeto usar outra forma canônica de executar unittest no momento da implementação, registrar o
comando realmente executado.

Critérios de aceitação:

```text
FR-004-AC-01 três validadores existentes continuam PASS
FR-004-AC-02 novo teste passa
FR-004-AC-03 teste negativo controlado demonstra FAIL esperado
FR-004-AC-04 nenhuma alteração de schema foi feita apenas para fazer o teste passar
```

### FR-005 — Integrar documentação

**Operation class:** `documentation_change`

Atualizar `docs/modelagem/README.md` para indicar:

```text
fields-registry.md = catálogo humano/semântico de campos
seis JSON Schemas = contratos executáveis atuais
```

Não criar nova decisão material apenas para repetir esta instrução humana de implementação.

Criar/atualizar `registro_decisoes.md` somente se, durante FR-002, surgir uma decisão semântica nova
ou alteração material do significado de um campo.

Critérios de aceitação:

```text
FR-005-AC-01 README aponta para o registry
FR-005-AC-02 hierarquia schema/registry é inequívoca
FR-005-AC-03 nenhuma burocracia documental paralela foi criada
```

---

## 11. Runbook binding

O `fields-registry` não é uma alteração de banco de dados. Não usar `database_change` apenas porque
os artefatos descrevem dados.

### FR-001, FR-002 e FR-005

```json
{
  "operation_classes": ["documentation_change"],
  "applicable_runbooks": {
    "shared": [
      "runbooks/shared/RB-SHARED-001-repository-baseline.md",
      "runbooks/shared/RB-SHARED-002-evidence.md",
      "runbooks/shared/RB-SHARED-003-failure-states.md"
    ],
    "executor": [
      "runbooks/executor/RB-EXEC-003-documentation-change.md"
    ],
    "reviewer": [
      "runbooks/reviewer/RB-REV-003-documentation-review.md",
      "runbooks/reviewer/RB-REV-004-evidence-review.md"
    ]
  }
}
```

### FR-003 e FR-004

```json
{
  "operation_classes": ["code_change", "documentation_change"],
  "applicable_runbooks": {
    "shared": [
      "runbooks/shared/RB-SHARED-001-repository-baseline.md",
      "runbooks/shared/RB-SHARED-002-evidence.md",
      "runbooks/shared/RB-SHARED-003-failure-states.md"
    ],
    "executor": [
      "runbooks/executor/RB-EXEC-001-code-change.md",
      "runbooks/executor/RB-EXEC-003-documentation-change.md"
    ],
    "reviewer": [
      "runbooks/reviewer/RB-REV-001-code-review.md",
      "runbooks/reviewer/RB-REV-003-documentation-review.md",
      "runbooks/reviewer/RB-REV-004-evidence-review.md"
    ]
  }
}
```

O `runbook_binding` deve ser copiado para a task/proposal correspondente quando a implementação for
iniciada.

---

## 12. Regras para o Executor

O Executor deve:

- inspecionar a branch antes de alterar arquivos;
- trabalhar em branch dedicada diferente de `main`;
- limitar escrita aos paths autorizados pela task;
- usar os schemas atuais como fatos, não memória;
- manter alterações pequenas e revisáveis;
- executar validação local antes do handoff;
- entregar diff e resultados dos checks.

O Executor não deve:

- alterar `.devcontainer/**`;
- alterar `runbooks/**`;
- alterar `.ai/**`;
- fazer commit/push/merge no container;
- alterar os seis schemas sem autorização explícita adicional;
- introduzir dependência nova apenas para parsear Markdown;
- consultar `.drive/CEPRAEA BEACH PRO/**` se a política do container impedir essa leitura;
- bloquear a tarefa inteira por não conseguir ler `.drive` quando as fontes versionadas em
  `docs/modelagem/**` forem suficientes para o field sendo documentado.

Se uma definição só puder ser obtida de uma fonte bloqueada pela política, usar
`PENDING_DEFINITION` e registrar o bloqueio.

---

## 13. Regras para o Reviewer

O Reviewer deve operar em read-only e verificar independentemente:

- inventário dos seis schemas;
- cobertura registry ↔ schema;
- ausência de campos inventados;
- coerência de `required | optional | conditional`;
- constraints resumidas corretamente;
- suficiência das fontes semânticas;
- resultado dos testes;
- inexistência de alteração de schema não autorizada.

O Reviewer deve emitir:

```text
PASS
FAIL
HUMAN_DECISION_REQUIRED
```

conforme os runbooks aplicáveis.

---

## 14. Critério de pronto da implementação

A implementação do fields registry é `DONE` somente quando:

```text
[ ] docs/modelagem/governanca/fields-registry.md existe
[ ] inventário foi derivado dos seis schemas atuais
[ ] todos os paths de properties estão catalogados
[ ] required/optional/conditional estão reconciliados
[ ] enums/patterns/formats/consts relevantes estão registrados
[ ] definições sem evidência estão marcadas PENDING_DEFINITION
[ ] nenhum campo foi criado por conveniência do Executor
[ ] tests/test_fields_registry.py existe
[ ] teste positivo passa
[ ] teste negativo demonstra detecção de divergência
[ ] validar.mjs passa
[ ] verificar_referencias.mjs passa
[ ] verificar_repositorio.mjs passa
[ ] README de modelagem aponta para o registry
[ ] schemas não foram alterados sem autorização específica
[ ] CI não foi alterado nesta primeira implantação
[ ] Reviewer independente emitiu verdict
```

---

## 15. Stop conditions

Interromper e emitir `HUMAN_DECISION_REQUIRED` quando:

- dois artefatos canônicos atribuírem significados incompatíveis ao mesmo campo;
- for necessário alterar semanticamente um schema para concluir o registry;
- um campo ativo não possuir significado determinável e `PENDING_DEFINITION` não for aceitável para
  o uso pretendido;
- a tarefa exigir alteração de `.devcontainer/**`, `.ai/**`, `runbooks/**` ou CI;
- surgir decisão sobre LinkML que precise mudar a autoridade atual dos seis schemas;
- dados pessoais/sensíveis forem necessários para documentar um campo.

Não interromper por:

- contagem diferente das antigas 60 obrigações;
- ausência do futuro `cepraea_profile.yaml`;
- ausência de CI para o novo teste na primeira implantação;
- ausência de acesso a `.drive` quando a informação necessária já estiver versionada no
  repositório.

---

## 16. Reconciliação futura com o CEPRAEA Metadata Profile

Após a implementação e validação de `metadata/cepraea_profile.yaml`, executar uma tarefa separada.

Essa tarefa deve responder, por campo:

```text
este campo continua governado diretamente por um dos seis schemas?
ou
passa a ser definido no profile LinkML e projetado para JSON Schema?
```

A transição futura deve obedecer:

```text
semântica canônica CEPRAEA
        ↓
profile LinkML validado
        ↓
artefato executável derivado, quando aplicável
        ↓
fields-registry.md sincronizado
```

O registry continua sendo catálogo de interpretação humana; não deve virar uma fonte concorrente do
LinkML.

Nenhuma parte desta seção autoriza hoje a criação ou promoção do profile LinkML.

---

## 17. Ordem de execução

```text
FR-001  criar registry + inventário
  ↓
FR-002  reconciliar significado
  ↓
FR-003  implementar teste de sincronização
  ↓
FR-004  executar validações
  ↓
FR-005  integrar README
  ↓
Reviewer independente
  ↓
Humano decide promoção/commit conforme fluxo Git vigente
```

Essa é a sequência mínima. Não adicionar novas fases sem uma necessidade demonstrada.

---

## 18. Estado do plano após esta reconciliação

```text
PLAN_ARCHIVED = false
PLAN_STATUS = READY_FOR_IMPLEMENTATION
CURRENT_EXECUTABLE_SOURCES = 6_JSON_SCHEMAS
FIELDS_REGISTRY_EXISTS = false
SYNC_TEST_EXISTS = false
LINKML_PROFILE_EXISTS = false
DATABASE_CHANGE_REQUIRED = false
CI_CHANGE_REQUIRED_FOR_FIRST_IMPLEMENTATION = false
```

A próxima ação é `FR-001`.