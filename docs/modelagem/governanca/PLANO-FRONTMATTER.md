# Plano completo para criação do fields-registry.md

**Versão**: `1.1`
**Status**: Proposto para implementação
**Arquivo-alvo**: `docs/modelagem/governanca/fields-registry.md`
**Responsável sugerido**: Davi Sermenho
**Data de criação**: 2026-08-15

***

## 1. Objetivo do plano

> Este plano define todas as ações necessárias para criar o fields-registry.md, o catálogo semântico e governamental dos campos dos registros JSON canônicos do Modelo Canônico do CEPRAEA BEACH PRO, definidos pelos seis JSON Schemas em docs/modelagem/schemas/.

O objetivo é **garantir que todo campo aceito** pelo sistema tenha:

- definição;
- finalidade;
- dono;
- regras de uso;
- status de governança;
- relação com o schema;
- exemplos válidos;
- exemplos inválidos;
- critérios de mudança.

O `fields-registry.md` deve impedir que campos sejam criados de forma invisível, informal, ambígua ou por conveniência local.

Regra central:

```text
campo não catalogado não existe
campo catalogado mas não aprovado não é aceito pelo schema
campo aceito pelo schema precisa estar no fields-registry.md
campo novo exige decisão, histórico de revisão, teste e owner
```

---

## 2. Resultado esperado

Ao final da implementação, o repositório deve conter:

```text
`docs/modelagem/governanca/fields-registry.md`
`"docs/modelagem/schemas/schema_fonte.json",`
`"docs/modelagem/schemas/schema_decisao.json",`
`"docs/modelagem/schemas/schema_evidencia.json",`
`"docs/modelagem/schemas/schema_elemento_modelo.json",`
`"docs/modelagem/schemas/schema_termo.json",`
`"docs/modelagem/schemas/schema_regra.json",`

"docs/modelagem/decisoes/registro_decisoes.md"
tests/test_fields_registry.py
```

O arquivo `fields-registry.md` deve funcionar como o catálogo humano e governamental dos campos.

O JSON Schema deve continuar sendo o contrato executável.

A relação correta é:

````py
```text
fields-registry.md                  explica o campo
"docs/modelagem/schemas/schema_fonte.json",
"docs/modelagem/schemas/schema_decisao.json",
"docs/modelagem/schemas/schema_evidencia.json",
"docs/modelagem/schemas/schema_elemento_modelo.json",
"docs/modelagem/schemas/schema_termo.json",
"docs/modelagem/schemas/schema_regra.json",





Os seis JSON Schemas acima validam os campos.
"docs/modelagem/decisoes/registro_decisoes.md"             justifica a criação ou mudança do campo
Histórico de Revisões do registry   registra quando o registry mudou
tests/                             provam que registry e schema estão sincronizados
```
````

---

## 3. Escopo do fields-registry.md

O `fields-registry.md` deve catalogar os campos aceitos pelos seis JSON Schemas que governam os registros JSON canônicos do Modelo Canônico em `docs/modelagem/schemas/`.

Inclui:

```json
- campos obrigatórios;
- campos opcionais;
- campos condicionais;
- campos aninhados;
- objetos aninhados definidos nos seis schemas, especialmente estruturas de `evidencia`;
- subcampos aninhados definidos por `properties`, `required`, `if` e `then` nos seis schemas;
- campos de governança já presentes nos schemas e campos futuros somente quando formalmente aprovados;
- campos propostos, quando ainda não aprovados;
- campos deprecated, quando existirem.
```

Fora do escopo:

- valores reais sensíveis;
- aprovações de documentos individuais;
- histórico completo de decisões;
- duplicação integral do JSON Schema;
- detalhes de linha de código de implementação;
- dados transitórios de execução de runs;
- campos hipotéticos sem necessidade operacional identificada.

---

## 4. Nome e localização oficial

```text
`docs/modelagem/governanca/fields-registry.md` como nome oficial.
```

## 5. Princípios de governança

* 5.1 Campo é ativo governado

Campos não são meros nomes de propriedades JSON.
Cada campo representa uma decisão de modelagem de informação.

Todo campo deve ter:

- nome oficial;
- definição;
- finalidade;
- tipo;
- obrigatoriedade;
- owner;
- status;
- versão de introdução;
- relação com schema;
- exemplos;
- regra de alteração.

* 5.2 Schema valida; registry explica

O JSON Schema decide se o registro JSON é válido.

O `fields-registry.md` explica por que o campo existe, como deve ser interpretado e quem pode alterá-lo.

* 5.3 Campo novo não nasce no documento

Campo novo nasce como proposta no registry ou em uma decisão de governança.

Fluxo correto:

```text
necessidade operacional
  ↓
proposta de campo
  ↓
avaliação de governança
  ↓
decisão aprovada
  ↓
atualização do fields-registry.md
  ↓
atualização do schema
  ↓
atualização dos testes
  ↓
atualização do Histórico de Revisões do registry
  ↓
uso permitido nos registros JSON canônicos
```

* 5.4 Campo não documentado é erro

Se um campo aparece em um registro JSON canônico governado pelos schemas da modelagem mas não está no `fields-registry.md`, ele deve ser tratado como não catalogado e a divergência deve ser corrigida.

Se um campo aparece no schema mas não está no registry, a implementação está incompleta.

Se um campo aparece no registry como ativo mas não está no schema, existe divergência entre documentação e contrato executável.

Estado atual: os seis schemas da modelagem não declaram `additionalProperties: false`, e o validador existente não rejeita automaticamente propriedades desconhecidas das instâncias. Portanto, a Fase 1 cria governança semântica e detecta divergências por revisão; o bloqueio determinístico de campos extras só pode ser afirmado depois de uma fase explícita de enforcement.

---

## 6. Estrutura recomendada do fields-registry.md

O arquivo deve seguir esta estrutura:

```markdown
# fields-registry.md — Registro oficial de campos
## 1. Finalidade
## 2. Regras gerais
## 3. Estados de campo
## 4. Campos ativos
## 5. Campos condicionais
## 6. Campos aninhados
## 7. Campos propostos
## 8. Campos deprecated
## 9. Processo para propor campo novo
## 10. Matriz registry ↔ schema
## 11. Checklist de validação
## 12. Changelog do registry
## 13. Histórico do registry
```

***

## 7. Estados dos campos

>Todo campo deve ter um status de governança.

Estados recomendados:

```text
proposed
experimental
active
deprecated
removed
rejected
```

*Proposed*

Campo identificado como necessidade possível, mas ainda não aceito pelo schema.

** *experimental*

Campo aprovado para uso limitado, normalmente em branch, sandbox ou tipo documental restrito.

* active

Campo oficialmente aceito pelo schema e documentado no registry.

* deprecated

Campo ainda reconhecido por compatibilidade, mas não deve ser usado em novos registros canônicos.

* removed

Campo removido do schema em versão maior.

* rejected

Campo proposto e rejeitado. Deve permanecer registrado se houver risco de reaparecer com outro nome.

---

## 8. Informações obrigatórias para cada campo

Cada campo deve conter as seguintes informações:

```text
Nome oficial
Caminho
Definição
Finalidade
Tipo
Obrigatoriedade
Repetível
Valores permitidos
Formato
Escopo
Exemplos válidos
Exemplos inválidos
Regra de governança
Campo relacionado
Mapeamento externo, se existir
Dono
Status
Introduzido em
Decisão associada
Schema associado
Testes associados
```

---

## 9. Modelo de entrada de campo

Cada campo deve ser registrado usando este modelo:

```markdown
## Campo: `nome_do_campo`

* Nome oficial

`nome_do_campo`

* Caminho

`nome_do_campo` ou `objeto.subcampo`

* Definição

Explique o que o campo significa.

* Finalidade

Explique por que o campo existe e qual decisão operacional ele permite.

* Tipo

`string | array | object | boolean | integer | number | date | date-time`

* Obrigatoriedade

`obrigatório | opcional | condicional`

* Repetível

`sim | não`

* Valores permitidos

Liste valores quando houver vocabulário controlado.

* Formato

Regex, SemVer, ISO date, URI ou outro padrão aplicável.

* Escopo

Tipos de registro e schemas aos quais o campo se aplica.

**Exemplo válido**

```json
{ "nome_do_campo": "valor_valido" }
```

**Exemplo inválido**

```json
{ "nome_do_campo": "valor_invalido" }
```

```markdown
* Regra de governança

Explique quem pode alterar, aprovar ou usar o campo.

* Relações com outros campos

Liste campos relacionados ou dependentes.

* Mapeamento externo

Dublin Core, PREMIS, schema.org, PROV, SemVer ou outro vocabulário, se aplicável.

* Dono

Equipe responsável.

* Status

`proposed | experimental | active | deprecated | removed | rejected`

* Introduzido em

Versão do padrão.

* Decisão associada

Referência para `DECISOES.md` ou `decision-register.md`.

* Schema associado

Path do schema onde o campo é validado.


* Testes associados

Lista de testes que protegem o comportamento do campo.
```

***

## 10. Campos iniciais a catalogar

Com base na implementação atual do repositório `CEPRAEA BEACH PRO`, a criação mínima deve catalogar os campos obrigatórios incondicionais e condicionalmente obrigatórios de nível superior dos seis JSON Schemas vigentes. Para evitar colisão entre nomes iguais em schemas diferentes, a identidade de cada entrada do registry deve ser `<schema>::<path>`.

```text
schema_fonte.json — 14 obrigações
id_fonte
id_acao
nome_arquivo_original
hash_sha256
caminho_local
tipo_arquivo
tipo_fonte
autoridade_fonte
proveniencia_fonte
estado_fonte
estado_processamento
dado_sensivel_encontrado
evidencia
tratamento_dado_sensivel [condicional]

schema_evidencia.json — 8 obrigações
id_evidencia
id_fonte
id_acao
localizacao
trecho_literal
tipo_evidencia
dado_sensivel_encontrado
tratamento_dado_sensivel [condicional]

schema_termo.json — 9 obrigações
id_termo
termo_preferencial
nome_canonico
classificacao
definicao
fonte
estado_epistemologico
estado_tecnico
evidencia

schema_regra.json — 8 obrigações
id_regra
fonte
tipo
sujeito
acao
estado_epistemologico
estado_tecnico
evidencia

schema_decisao.json — 9 obrigações
id_decisao
data
decisao
escolha
justificativa
fonte
aprovador
estado
evidencia [condicional quando estado=RESOLVIDA]

schema_elemento_modelo.json — 12 obrigações
id_elemento
tipo
nome
estagio
fonte
estado_epistemologico
estado_tecnico
evidencia
maturidade [condicional]
promoted_from [condicional]
promoted_by [condicional]
promoted_to [condicional]

TOTAL = 60 obrigações schema::campo
```

Campos opcionais, subcampos aninhados e documentação completa de enums pertencem à Fase 2. Campos ainda inexistentes nos seis schemas permanecem fora do conjunto ativo e só podem ser tratados como proposta nas fases de governança/evolução.

---

## 11. Ações para criação do fields-registry.md

* Ação 1 — Criar o arquivo

Criar:

```text
docs/modelagem/governanca/fields-registry.md
```

Critério de aceite:

- o arquivo existe;
- possui título;
- declara finalidade;
- declara regras gerais;
- na Fase 1, lista todos os campos obrigatórios incondicionais e condicionalmente obrigatórios dos seis schemas atuais.

* Ação 2 — Extrair campos dos seis schemas atuais

Ler:

```text
docs/modelagem/schemas/ ├── schema_fonte.json ├── schema_decisao.json ├── schema_evidencia.json ├── schema_elemento_modelo.json ├── schema_termo.json └── schema_regra.json
```

Extrair:

- campos em `required`;
- campos em `properties`;
- objetos aninhados;
- campos com `enum`;
- campos com `const`;
- campos com `pattern`;
- presença ou ausência de `additionalProperties: false`, sem presumir bloqueio de propriedades extras quando a keyword não estiver declarada.

Critério de aceite:

- todo campo do schema aparece no registry;
- todo subcampo aninhado aparece no registry;
- enums estão documentados.

* Ação 3 — Classificar campos por função

Classificar campos em grupos:

```text
Fonte (`schema_fonte.json`)
Evidência (`schema_evidencia.json`)
Termo (`schema_termo.json`)
Regra (`schema_regra.json`)
Decisão (`schema_decisao.json`)
Elemento do Modelo (`schema_elemento_modelo.json`)
Funções transversais: identidade, proveniência, estado epistemológico, estado técnico e evidência
```

Critério de aceite:

- cada campo tem uma categoria funcional;
- nenhuma categoria mistura conceitos incompatíveis.

* Ação 4 — Documentar campos obrigatórios

Catalogar com prioridade:

```text
Todos os 60 campos/obrigações `schema::campo` listados na seção 10, incluindo os campos condicionalmente obrigatórios de nível superior.
```

Critério de aceite:

- cada campo obrigatório tem definição;
- cada campo obrigatório tem finalidade;
- cada campo obrigatório tem exemplo válido;
- cada campo obrigatório tem regra de governança.

* Ação 5 — Documentar campos aninhados

Catalogar:

```text
Todos os subcampos definidos por `properties` nos seis schemas, incluindo as estruturas aninhadas de `evidencia`, `source_evidence`, `approval_evidence` e `repository_evidence`, preservando o caminho completo `<schema>::objeto.subcampo`.
```

Critério de aceite:

- cada subcampo tem caminho completo;
- cada subcampo tem tipo;
- cada subcampo tem relação com o objeto-pai.

* Ação 6 — Documentar enums e vocabulários controlados

Catalogar valores permitidos de:

```text
Todos os campos com `enum` nos seis schemas, incluindo `tipo_arquivo`, `tipo_fonte`, `autoridade_fonte`, `proveniencia_fonte`, `estado_fonte`, `estado_processamento`, `tipo_evidencia`, `classificacao`, `tipo`, `estado_epistemologico`, `estado_tecnico`, `estagio`, `maturidade`, `aprovador` e `estado`.
```

Critério de aceite:

- cada valor de enum tem significado;
- valores inválidos comuns são exemplificados;
- fica claro quando usar cada valor.

* Ação 7 — Documentar campos propostos

Criar seção:

```markdown
## Campos propostos
```

Incluir inicialmente:

```text
schema_version
approved_by
approved_at
approval_ref
owner_team
created_at
updated_at
risk_level
source_refs
```

Critério de aceite:

- campos propostos não são tratados como ativos;
- cada proposta tem problema associado;
- cada proposta informa se campo existente já resolve ou não.

* Ação 8 — Definir regra de aprovação de campos novos

Adicionar ao registry a regra:

```text
Nenhum campo novo pode ser usado em registros canônicos versionados antes de ser aprovado, documentado no registry, implementado no schema, coberto por teste e registrado no changelog.
```

Critério de aceite:

- regra aparece explicitamente no arquivo;
- processo de aprovação está descrito;
- papéis responsáveis estão definidos.

* Ação 9 — Criar matriz registry ↔ schema

Adicionar tabela:

```markdown
| Campo | Registry | Schema | Teste | Status |
|---|---:|---:|---:|---|
| schema_fonte.json::id_fonte | sim | sim | sim | active |
```

Critério de aceite:

- todo campo ativo tem linha na matriz;
- divergências são visíveis;
- campo ativo sem schema é erro;
- campo no schema sem registry é erro.

* Ação 10 — Atualizar governança

Atualizar ou criar referência em:

```text
docs/modelagem/schemas/
├── schema_fonte.json
├── schema_decisao.json
├── schema_evidencia.json
├── schema_elemento_modelo.json
├── schema_termo.json
└── schema_regra.json
```

Critério de aceite:

- documentos normativos apontam para `fields-registry.md` como catálogo oficial de campos;
- fica claro que o schema continua sendo o contrato executável.

* Ação 11 — Atualizar Histórico de Revisões

Registrar a criação e as mudanças do registry na seção final `Histórico de Revisões` do próprio `docs/modelagem/governanca/fields-registry.md`.

Critério de aceite:

- a mudança possui linha no histórico com Versão, Data, Descrição da Alteração, Autor e Aprovado por;
- não é criado `CHANGELOG.md` ou `change-control/structural-changes.jsonl` apenas para esta implantação;
- eventual adoção futura de um changelog central exige decisão explícita de governança.

overnança.

* Ação 12 — Registrar decisão

Criar ou atualizar decisão em:

```text
`docs/modelagem/decisoes/registro_decisoes.md`
```

Decisão recomendada:

```text
DEC-NNN — Criação do fields-registry como catálogo semântico e governamental dos campos
```

Critério de aceite:

- decisão explica por que o registry existe;
- decisão explica diferença entre registry e schema;
- decisão define que todo campo aceito precisa estar catalogado.

* Ação 13 — Criar teste de sincronização registry ↔ schema

Criar:

```text
tests/test_fields_registry.py
```

Objetivo:

- extrair campos do schema;
- extrair campos documentados no registry;
- comparar listas;
- falhar se campo do schema não estiver no registry;
- falhar se campo ativo do registry não estiver no schema.

Critério de aceite:

- teste roda com `python3 -m unittest discover -s tests -v`;
- CI executa o teste automaticamente.

* Ação 14 — Atualizar CI

Esta ação pertence à Fase 4 e altera o plano de controle; portanto, não deve ser executada na Fase 1. Quando a Fase 4 for explicitamente autorizada, o CI deve reutilizar os validadores reais do repositório e acrescentar o teste de sincronização somente depois que `tests/test_fields_registry.py` existir.

Validadores existentes:

```bash
node docs/modelagem/schemas/validar.mjs
node docs/modelagem/schemas/verificar_referencias.mjs
node docs/modelagem/schemas/verificar_repositorio.mjs
```

Após a criação do teste da Fase 4:

```bash
python3 -m unittest discover -s tests -v
```

Não usar `ferramentas/kb_compile.py`, `ferramentas/check_kb_consistency.py` ou `ferramentas/kb_validate.py`, pois esses caminhos não existem no estado atual validado do repositório.

Critério de aceite:

- a alteração de CI ocorre somente em tarefa explicitamente autorizada para plano de controle;
- os três validadores existentes continuam passando;
- o teste de sincronização é executado automaticamente quando a Fase 4 for implantada;
- divergência entre schema e registry produz falha determinística.

* Ação 15 — Criar exemplos de campo válido e inválido

Para cada campo crítico, incluir:

```text
exemplo válido
exemplo inválido
motivo da rejeição
```

Critério de aceite:

- `id_fonte`, `id_evidencia`, `id_termo`, `id_regra`, `id_decisao`, `id_elemento`, `estado_epistemologico`, `estado_tecnico` e `estagio` têm exemplos válidos e inválidos.

* Ação 16 — Definir política de campos propostos

Adicionar regra:

```text
Campos em proposed podem aparecer no fields-registry.md, mas não podem aparecer no schema nem em registros canônicos versionados.
```

Critério de aceite:

- proposta não cria aceitação automática;
- campo proposto tem owner e problema documentado;
- uso experimental exige decisão específica.

* Ação 17 — Definir política de depreciação

Adicionar regra:

```text
Campo deprecated continua documentado, mas não deve ser usado em novos registros canônicos.
```

Critério de aceite:

- campo deprecated tem substituto;
- campo deprecated tem versão de remoção planejada;
- migração é documentada.

* Ação 18 — Definir política de rejeição

Quando uma proposta for rejeitada, registrar em seção própria.

Critério de aceite:

- campo rejeitado tem motivo;
- nomes alternativos rejeitados são listados;
- evita reaparecimento com outro nome.

* Ação 19 — Definir owners dos campos

Cada campo deve ter owner.

Exemplos:

```text
Campos ativos dos seis schemas da modelagem — owner inicial: Davi Sermenho.
Delegações futuras de ownership exigem decisão registrada; não devem ser inferidas nem atribuídas a equipes inexistentes.
```

Critério de aceite:

- nenhum campo ativo fica sem owner.

* Ação 20 — Definir checklist de revisão

Adicionar checklist no final do registry:

```markdown
## Checklist para campo novo

- [ ] O campo resolve uma necessidade real?
- [ ] Já existe campo equivalente?
- [ ] O nome é claro e estável?
- [ ] O tipo é validável?
- [ ] Há owner definido?
- [ ] Há valores permitidos, se aplicável?
- [ ] O campo está no fields-registry.md?
- [ ] O campo está no JSON Schema?
- [ ] O campo tem teste?
- [ ] O campo tem decisão associada?
- [ ] O Histórico de Revisões do registry foi atualizado?
- [ ] Templates foram atualizados, se necessário?
```

Critério de aceite:

- checklist existe;
- PRs de campo novo usam esse checklist.

---

## 12. Estrutura inicial sugerida para o fields-registry.md

O conteúdo inicial deve começar assim:

```markdown
# fields-registry.md — Registro oficial de campos

## 1. Finalidade

Este arquivo é o catálogo semântico e governamental dos campos aceitos pelos JSON Schemas dos registros canônicos da modelagem do CEPRAEA BEACH PRO.

Ele explica o significado, finalidade, status, owner, regras de uso e critérios de mudança de cada campo.

O JSON Schema valida tecnicamente os campos. Este registry explica semanticamente e governa seu uso.

## 2. Regra central

Campo aceito pelo schema precisa estar documentado neste registry.
Campo ativo neste registry precisa estar validado pelo schema.
Campo novo exige decisão, histórico de revisão, teste e owner.

## 3. Estados de campo

- proposed
- experimental
- active
- deprecated
- removed
- rejected

## 4. Campos ativos
```

---

## 13. Exemplo de campo catalogado: schema_fonte.json::id_fonte

```markdown
## Campo: `schema_fonte.json::id_fonte`

* Nome oficial
`id_fonte`

* Caminho
`id_fonte`

* Definição
Identidade canônica interna e estável de uma fonte registrada pelo Modelo Canônico.

* Finalidade
Permitir referência inequívoca à fonte e sustentar rastreabilidade entre fonte, evidência e conhecimento.

* Tipo
`string`

* Obrigatoriedade
Obrigatório.

* Repetível
Não.

* Formato
```regex
^SRC-[0-9]{3}$
```

* Exemplo válido
```json
{ "id_fonte": "SRC-001" }
```

* Exemplo inválido
```json
{ "id_fonte": "FONTE-001" }
```

* Escopo
Registros validados por `docs/modelagem/schemas/schema_fonte.json`.

* Regra de governança
O significado e o padrão do campo derivam do schema vigente. O registry documenta essa semântica e não pode alterar o contrato executável unilateralmente.

* Dono
Davi Sermenho.

* Status
active

* Schema associado
`docs/modelagem/schemas/schema_fonte.json`

* Testes associados
`node docs/modelagem/schemas/validar.mjs`; teste específico de sincronização somente na Fase 4.
```

---

## 14. Exemplo de campo catalogado: schema_elemento_modelo.json::estado_epistemologico

```markdown
## Campo: `schema_elemento_modelo.json::estado_epistemologico`

* Nome oficial
`estado_epistemologico`

* Caminho
`estado_epistemologico`

* Definição
Estado que expressa a condição epistemológica do elemento do Modelo Canônico.

* Finalidade
Distinguir observação, inferência, ambiguidade, conflito, validação e rejeição sem misturar essa dimensão com o estado técnico.

* Tipo
`string` com vocabulário controlado.

* Obrigatoriedade
Obrigatório.

* Valores permitidos
`OBSERVADO | INFERIDO | AMBIGUO | CONFLITANTE | VALIDADO | REJEITADO`

* Exemplo válido
```json
{ "estado_epistemologico": "VALIDADO" }
```

* Exemplo inválido
```json
{ "estado_epistemologico": "APROVADO" }
```

* Regra de governança
O registry deve reproduzir o significado definido pelo schema e pelas decisões da modelagem. Não pode criar valores adicionais. Regras condicionais do schema que exigem `VALIDADO` permanecem autoritativas.

* Dono
Davi Sermenho.

* Status
active

* Schema associado
`docs/modelagem/schemas/schema_elemento_modelo.json`

* Testes associados
`node docs/modelagem/schemas/validar.mjs`; teste específico de sincronização somente na Fase 4.
```

---

## 15. Exemplo de campo proposto: schema_version

```markdown
## Proposta: `schema_version`

* Status
proposed

* Problema
Os seis schemas da modelagem possuem metadados `$schema` e `$id`, mas as instâncias atuais não carregam um campo próprio que identifique explicitamente a versão do contrato de metadados que as validou. Isso não é requisito da Fase 1.

* Campo existente resolve?
Não há campo ativo equivalente nos seis schemas da modelagem.

* Tipo proposto
`string`

* Formato proposto
A definir somente em decisão de governança; nenhum formato deve ser incorporado ao contrato executável por este plano sem aprovação específica.

* Exemplo meramente ilustrativo
```json
{ "schema_version": "1.0" }
```

* Uso operacional potencial
Permitir migração, auditoria e validação explícita por versão de contrato, caso a necessidade seja aprovada.

* Dono proposto
Davi Sermenho.

* Decisão necessária
Sim. Esta proposta pertence à Fase 5 e não pode ser tratada como campo ativo nem adicionada aos seis schemas durante a criação mínima.
```

---

## 16. Informações que não devem entrar no fields-registry.md

O registry não deve conter:

- aprovações específicas de documentos individuais;
- e-mails pessoais ou dados sensíveis;
- tokens, URLs privadas ou credenciais;
- logs completos de execução;
- histórico completo de runs;
- justificativas longas que pertencem ao registro de decisões;
- cópia integral do JSON Schema;
- valores hipotéticos sem necessidade validada;
- regras de implementação amarradas a linhas de código.

Exemplo incorreto:

```text
O documento domain.customer foi aprovado por João em tal data.
```

Isso pertence ao documento específico, ao ledger ou ao registro de decisão, não ao registry do campo.

---

## 17. Como descobrir se um campo novo precisa ser catalogado

Um campo ainda não usado deve ser avaliado quando houver evidência de necessidade operacional.

Sinais de necessidade:

1. A mesma informação aparece repetidamente no corpo Markdown.
2. Revisores fazem a mesma pergunta em vários documentos.
3. O pipeline precisa decidir com base nessa informação.
4. Agentes precisam filtrar, recuperar ou priorizar usando esse atributo.
5. Surgem variações informais concorrentes.
6. O campo corresponde a conceito reconhecido em padrão externo.
7. Há risco de ambiguidade sem esse campo.
8. Há necessidade de auditoria ou aprovação explícita.

Exemplo de variações concorrentes:

```yaml
priority: high
importance: alta
criticality: critical
risk: severe
```

Campo governado recomendado:

```yaml
risk_level: critical
```

---

## 18. Critérios para aprovar campo novo

Um campo novo só deve ser aprovado se responder sim à maioria destas perguntas:

```text
O campo resolve uma necessidade real?
A necessidade é recorrente?
O campo será usado por pipeline, busca, IA, auditoria ou governança?
O campo é validável por tipo, enum, padrão ou regra?
O campo não duplica outro campo existente?
O nome é claro e estável?
O owner está definido?
Há impacto de migração conhecido?
Há decisão registrada?
Há teste planejado?
```

Se o campo serve apenas para anotação ocasional, ele não deve entrar no padrão.

---

## 19. Critérios de aceite da implementação

A criação do `fields-registry.md` estará completa quando:

```text
1. O arquivo `docs/modelagem/governanca/fields-registry.md` existir.
2. Na cobertura completa, todos os campos dos seis schemas atuais estiverem catalogados.
3. Todos os campos obrigatórios tiverem definição e finalidade.
4. Todos os enums tiverem valores explicados.
5. Todos os objetos aninhados tiverem subcampos catalogados.
6. Campos propostos estiverem separados de campos ativos.
7. O registry apontar para o schema oficial.
8. O estado de enforcement de propriedades extras estiver explicitamente documentado; a Fase 1 não presume `additionalProperties: false`.
9. Houver teste de sincronização registry ↔ schema.
10. O CI executar esse teste.
11. A criação do registry estiver registrada em decisão de governança.
12. A criação estiver registrada no changelog ou histórico estrutural.
13. O README ou protocolo apontar para o registry como catálogo oficial.
```

---

## 20. Sequência de implementação recomendada

* Fase 1 — Criação mínima

- Criar `docs/modelagem/governanca/fields-registry.md`.
- Documentar finalidade, regra central e estados de campo.
- Catalogar as 60 obrigações `schema::campo` de nível superior dos seis schemas atuais, incluindo as condicionalmente obrigatórias.

* Fase 2 — Cobertura completa

- Catalogar campos opcionais.
- Catalogar subcampos aninhados.
- Documentar enums.
- Criar matriz registry ↔ schema.

* Fase 3 — Governança

- Criar decisão `DEC-NNN`.
- Atualizar o Histórico de Revisões do registry.
- Atualizar protocolo e inventário.
- Definir owners.

* Fase 4 — Automação

- Criar `tests/test_fields_registry.py`.
- Garantir execução no CI.
- Bloquear divergência entre registry e schema.

* Fase 5 — Evolução

- Adicionar seção de campos propostos.
- Avaliar `schema_version`, `approved_by`, `approved_at`, `approval_ref`, `owner_team`, `created_at`, `updated_at`, `risk_level`.
- Criar decisões e migrações conforme necessário.

---

## 21. Teste de sincronização recomendado

Criar teste que verifique:

```text
Campos no schema estão no registry.
Campos ativos no registry estão no schema.
Campos proposed no registry não precisam estar no schema.
Campos deprecated têm substituto ou plano de remoção.
Enums do schema estão documentados no registry.
```

Pseudocódigo:

````py
```python
schema_fields = extract_fields([
"docs/modelagem/schemas/schema_fonte.json",
"docs/modelagem/schemas/schema_decisao.json",
"docs/modelagem/schemas/schema_evidencia.json",
"docs/modelagem/schemas/schema_elemento_modelo.json",
"docs/modelagem/schemas/schema_termo.json",
"docs/modelagem/schemas/schema_regra.json",






])
registry_active_fields = extract_active_fields("docs/modelagem/governanca/fields-registry.md")
registry_proposed_fields = extract_proposed_fields("docs/modelagem/governanca/fields-registry.md")

assert schema_fields <= registry_active_fields
assert registry_active_fields <= schema_fields
assert not proposed_fields_required_in_schema
````

```

---

## 22. Riscos mitigados

A criação do `fields-registry.md` mitiga:

- campos inventados por agentes;
- divergência entre schema e documentação;
- metadados decorativos sem função operacional;
- enums mal compreendidos;
- duplicidade semântica;
- campos sem owner;
- mudanças invisíveis no padrão;
- aprovação informal de campos;
- acúmulo de metadados genéricos;
- inconsistência entre documentos.

---

## 23. Regra final

O `fields-registry.md` deve ser tratado como o catálogo semântico e governamental dos campos.

A regra final é:

```text
fields-registry.md governa o significado.
JSON Schema governa a validade.
docs/modelagem/decisoes/registro_decisoes.md governa o motivo.
O Histórico de Revisões do registry governa o registro da mudança.
CI governa a conformidade.
```

Sem esse arquivo, o schema valida estrutura, mas o sistema ainda não governa plenamente o significado dos campos.

---

## 24. Base científica e normativa para a escolha dos campos

Esta seção documenta as evidências que justificam a importância real da escolha dos campos nos registros estruturados do Modelo Canônico do CEPRAEA BEACH PRO. Os exemplos desta fundamentação são ilustrativos e não definem o conjunto de campos vigente; a autoridade executável permanece nos seis schemas de `docs/modelagem/schemas/`.

A conclusão técnica é:

```text
A eficiência dos registros estruturados não vem da sintaxe de serialização.
A eficiência vem da seleção, definição, validação e governança dos campos.
```

A literatura e os padrões abaixo sustentam semanticamente essa conclusão.

---

* 24.1 Metadados tornam objetos digitais acionáveis por máquinas

Fonte principal:

```text
Wilkinson et al. — The FAIR Guiding Principles for scientific data management and stewardship
Scientific Data / Nature, 2016
URL: https://www.nature.com/articles/sdata201618
```

Evidência usada:

```text
O artigo afirma que agentes computacionais precisam descobrir, acessar, interoperar e reutilizar dados com pouca ou nenhuma intervenção humana. Também afirma que agentes precisam de informação detalhada para identificar o tipo de objeto, decidir se é útil, se é utilizável e que ação tomar.
```

Aplicação ao registro estruturado do CEPRAEA:

```text
Campos como id, type, status, retrieval, relationships e schema_version são os mecanismos que tornam documentos Markdown acionáveis por máquinas, pipelines e agentes.
```

Afirmação validada:

```text
Campos definem o que o sistema consegue entender e automatizar.
```

---

* 24.2 Campos claros reduzem ambiguidade semântica

Fonte principal:

```text
DCMI Metadata Terms
Dublin Core Metadata Initiative
URL: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
```

Evidência usada:

```text
A especificação DCMI documenta atributos mínimos de termos de metadados, como nome, label, URI, definição e tipo do termo.
```

Aplicação ao registro estruturado do CEPRAEA:

```text
Todo campo do fields-registry.md deve ter nome oficial, definição, tipo, finalidade e regra de uso. Sem isso, o campo pode ser interpretado de formas diferentes por pessoas, scripts e agentes.
```

Afirmação validada:

```text
Campos bons reduzem ambiguidade; campos mal definidos criam interpretações concorrentes.
```

---

* 24.3 Schema transforma campo em contrato executável

Fonte principal:

```text
JSON Schema Draft 2020-12
URL: https://json-schema.org/draft/2020-12/json-schema-core
```

Evidência usada:

```text
A especificação JSON Schema define um vocabulário para descrever estrutura de dados JSON e impor restrições que podem passar ou falhar em validação.
```

Aplicação ao registro estruturado do CEPRAEA:

```text
O fields-registry.md explica o significado do campo, mas o JSON Schema decide se o documento é válido. A combinação registry + schema transforma metadados em contrato operacional.
```

Afirmação validada:

```text
Campos devem ser validáveis; caso contrário, viram apenas decoração documental.
```

---

* 24.4 Bloqueio de campos inventados evita corrupção do sistema

Fonte principal:

```text
JSON Schema Draft 2020-12 — additionalProperties
URL: https://json-schema.org/draft/2020-12/json-schema-core
```

Evidência usada:

```text
A especificação define additionalProperties como mecanismo para controlar propriedades que não foram declaradas por properties ou patternProperties. Quando additionalProperties é false, propriedades não previstas são rejeitadas.
```

Aplicação ao registro estruturado do CEPRAEA:

```json
{
  "additionalProperties": false
}
```

Afirmação validada:

```text
Campos inventados por pessoas ou agentes devem ser bloqueados. Campo não documentado não existe.
```

---

* 24.5 Vocabulários controlados melhoram consistência e recuperação

Fonte principal:

```text
Bird & Simons — The OLAC Metadata Set and Controlled Vocabularies
Apresentado em workshop ACL/EACL; relacionado a metadados, descoberta e vocabulários controlados
URL: https://arxiv.org/abs/cs/0105030
```

Evidência usada:

```text
O trabalho argumenta que conjuntos de metadados e vocabulários controlados facilitam descrição consistente e busca focada de recursos.
```

Aplicação ao registro estruturado do CEPRAEA:

```yaml
status: approved
retrieval:
  priority: high
```

é melhor do que:

```yaml
status: pronto
important: yes
```

Afirmação validada:

```text
A seleção dos campos e dos valores permitidos afeta diretamente a qualidade da busca, recuperação e automação.
```

---

* 24.6 Identidade estável sustenta rastreabilidade e deduplicação

Fontes principais:

```text
W3C PROV-DM — Provenance Data Model
URL: https://www.w3.org/TR/prov-dm/

FAIR Principles — Scientific Data / Nature
URL: https://www.nature.com/articles/sdata201618
```

Evidência usada:

```text
PROV-DM modela entidades, atividades e agentes envolvidos na produção de dados, permitindo avaliar qualidade, confiabilidade e confiança. FAIR enfatiza identificadores persistentes e metadados ricos para descoberta e reuso.
```

Aplicação ao registro estruturado do CEPRAEA:

```yaml
id: domain.customer
relationships:
  dependsOn:
    - domain.person
```

Afirmação validada:

```text
Campos como id e relationships não são decorativos; eles sustentam identidade, relacionamento, deduplicação e auditoria.
```

---

* 24.7 Proveniência sustenta origem, decisão e destino

Fonte principal:

```text
W3C PROV-DM — Provenance Data Model
URL: https://www.w3.org/TR/prov-dm/
```

Evidência usada:

```text
PROV descreve proveniência como informação sobre entidades, atividades e agentes envolvidos na produção ou influência de um dado ou recurso.
```

Aplicação ao registro estruturado do CEPRAEA:

Campos como estes permitem rastreabilidade operacional:

```yaml
source_refs:
  - FONTE-2026-EXEMPLO
approved_by: architecture-board
approval_ref: governanca/decisoes/DEC-2026-010.md
```

Afirmação validada:

```text
Campos devem permitir rastrear origem, decisão, aprovação e destino do artefato.
```

---

* 24.8 JSON canônico melhora comparação, hash e auditoria

Fonte principal:

```text
RFC 8785 — JSON Canonicalization Scheme (JCS)
URL: https://www.rfc-editor.org/rfc/rfc8785
```

Evidência usada:

```text
O RFC explica que operações criptográficas, como hashing e assinatura digital, dependem de uma representação invariável dos dados.
```

Aplicação ao registro estruturado do CEPRAEA:

```text
Markdown + YAML Front Matter
  ↓
parser
  ↓
JSON validado
  ↓
JSON canônico
  ↓
hash / assinatura / comparação / auditoria
```

Afirmação validada:

```text
Campos bem estruturados permitem gerar artefato canônico estável, comparável e auditável.
```

---

* 24.9 Campos demais aumentam custo e campos de menos reduzem contexto

Fonte principal:

```text
FAIR Principles — Scientific Data / Nature
URL: https://www.nature.com/articles/sdata201618
```

Evidência usada:

```text
FAIR apresenta princípios mínimos e incrementais, com baixa barreira de entrada, mas suficientes para descoberta, interoperabilidade e reuso.
```

Aplicação ao registro estruturado do CEPRAEA:

```text
Campo obrigatório demais reduz adesão.
Campo opcional demais vira lixo semântico.
Campo de menos deixa o sistema sem contexto operacional.
```

Afirmação validada:

```text
A seleção de campos precisa equilibrar suficiência operacional e simplicidade de manutenção.
```

---

* 24.10 O campo certo elimina inferência frágil

Fonte principal:

```text
FAIR Principles — Scientific Data / Nature
URL: https://www.nature.com/articles/sdata201618
```

Evidência usada:

```text
FAIR enfatiza que máquinas precisam de metadados explícitos para descobrir, avaliar e reutilizar recursos sem depender de interpretação humana contínua.
```

Aplicação ao registro estruturado do CEPRAEA:

Texto humano:

```markdown
Este documento foi aprovado pela equipe de arquitetura.
```

Controle operacional:

```yaml
status: approved
approved_by: architecture-board
approved_at: 2026-07-07T16:22:32Z
approval_ref: governanca/decisoes/DEC-2026-010.md
```

Afirmação validada:

```text
Campos explícitos reduzem inferência, ambiguidade e erro de agentes.
```

---

* 24.11 fields-registry.md é necessário para governar significado

Fontes principais:

```text
DCMI Metadata Terms
URL: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

JSON Schema Draft 2020-12
URL: https://json-schema.org/draft/2020-12/json-schema-core
```

Evidência usada:

```text
DCMI mostra que termos de metadados precisam de atributos semânticos como nome, URI, definição e tipo. JSON Schema mostra como validar estruturalmente os dados.
```

Aplicação ao registro estruturado do CEPRAEA:

```text
fields-registry.md governa o significado.
JSON Schema governa a validade.
```

Afirmação validada:

```text
O registry é necessário porque o schema sozinho valida estrutura, mas não explica integralmente intenção, owner, governança e motivo do campo.
```

---

* 24.12 Síntese das evidências

As fontes acima sustentam estas decisões do plano:

```text
1. Todo campo aceito precisa estar documentado.
2. Todo campo documentado como ativo precisa estar no schema.
3. Campos novos precisam de governança antes do uso.
4. Campos inventados devem ser rejeitados.
5. Campos precisam ter definição, finalidade, tipo, owner e exemplos.
6. Campos controlados melhoram busca, automação, interoperabilidade e reuso.
7. Identificadores e relações sustentam rastreabilidade.
8. JSON canônico sustenta auditoria, hash e comparação.
9. Metadados bem escolhidos reduzem inferência frágil para agentes.
10. A eficiência dos registros estruturados depende da qualidade semântica dos campos escolhidos.
```

---

## 25. Como usar essas evidências no repositório

Ao criar o `fields-registry.md`, incluir uma seção curta chamada:

```text
## Fundamentação científica e normativa
```

Essa seção deve apontar para:

```text
FAIR Principles — metadados ricos, ação por máquinas, descoberta e reuso
DCMI Metadata Terms — definição formal de termos de metadados
JSON Schema — validação estrutural e bloqueio de propriedades extras
W3C PROV-DM — proveniência, entidades, atividades e agentes
RFC 8785 JCS — JSON canônico, hashing e assinatura
OLAC / controlled vocabularies — consistência semântica e recuperação
```

Critério de aceite:

```text
O fields-registry.md não deve justificar campos apenas por preferência local.
Cada campo estrutural deve ter finalidade operacional e, quando aplicável, referência a padrão ou princípio reconhecido.
```

---

## 26. Nota editorial sobre a subguia de perguntas estratégicas

As perguntas estratégicas e suas respostas consolidadas foram movidas para a subguia própria do documento, para não misturar três naturezas diferentes de conteúdo:

```text
plano principal        → o que implementar e em que ordem
fundamentação/fontes   → por que o padrão é justificável
subguia estratégica    → perguntas respondidas para testar a eficiência dos campos
```

***

## 27. Histórico curto do registry

No final da documentação, crie a tabela curta, para tratar do registro do histórico do registry.

Escreva as diretrizes para os agentes que trabalharem no registry mantenham o histórico atualizado, como mostra o exemplo abaixo

Exemplo:

```text
## Geração do Histórico de Alterações
Sempre que este documento for modificado, editado ou revisado por você,  atualize uma tabela de histórico de alterações no final do documento, seguindo estritamente as regras abaixo:

1. Localização: Insira a tabela sob o cabeçalho final `**Histórico de Revisões**`.
2. Formato: Utilize uma tabela Markdown padrão.
3. Colunas: A tabela deve conter exatamente as colunas: `Versão`, `Data`, `Descrição da Alteração`, `Autor` e `Aprovado por`.
4. Regra de Versão:
   - Incremente o decimal (ex: de 1.0 para 1.1) para correções menores ou ajustes de texto.
   - Incremente o inteiro (ex: de 1.0 para 2.0) para novas seções ou mudanças estruturais.
5. Autor: Preencha o campo "Autor" como `Assistente de IA`.

| Versão | Data | Descrição da Alteração | Autor | Aprovado por |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | 10/02/2026 | Criação inicial do documento. | Ana Silva | Carlos M. |
| 1.1 | 15/04/2026 | Correção de links e atualização do telefone. | João Lima | Carlos M. |
| 2.0 | 16/08/2026 | Inclusão das novas regras de reembolso. | Ana Silva | Carla Souza |

***

Assim, este plano principal termina com a implementação, a regra final e a fundamentação. A subguia fica responsável apenas pelas perguntas e respostas estratégicas.

**Histórico de Revisões**

| Versão | Data | Descrição da Alteração | Autor | Aprovado por |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | 15/08/2026 | Criação inicial do documento. | Davi Sermenho | Davi Sermenho |
| 1.1 | 16/08/2026 | Correções de aderência ao estado real do CEPRAEA BEACH PRO: escopo JSON canônico, seis schemas autoritativos, campos reais, enforcement de propriedades extras, governança, validadores e exemplos. | Assistente de IA | Davi Sermenho |
