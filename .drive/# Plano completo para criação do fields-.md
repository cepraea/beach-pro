# Plano completo para criação do fields-registry.md

Versão: 1.0
Status: Proposto para implementação
Arquivo-alvo: `governanca/fields-registry.md`
Responsável sugerido: Metadata Governance / Docs Platform
Data de criação: 2026-07-07

***

## 1. Objetivo do plano

Este plano define todas as ações necessárias para criar o `fields-registry.md`, o catálogo semântico e governamental dos campos aceitos pelo padrão de Front Matter da base de conhecimento.

O objetivo é garantir que todo campo aceito pelo sistema tenha definição, finalidade, dono, regras de uso, status de governança, relação com o schema, exemplos válidos e critérios de mudança.

O `fields-registry.md` deve impedir que campos sejam criados de forma invisível, informal, ambígua ou por conveniência local.

Regra central:

```text
campo não catalogado não existe
campo catalogado mas não aprovado não é aceito pelo schema
campo aceito pelo schema precisa estar no fields-registry.md
campo novo exige decisão, changelog, teste e owner
```

***

## 2. Resultado esperado

Ao final da implementação, o repositório deve conter:

```text
governanca/fields-registry.md
schemas/domain_knowledge.schema.json
CHANGELOG.md ou change-control/structural-changes.jsonl
governanca/DECISOES.md ou governanca/decision-register.md
tests/test_fields-registry.py
```

O arquivo `fields-registry.md` deve funcionar como o catálogo humano e governamental dos campos.

O JSON Schema deve continuar sendo o contrato executável.

A relação correta é:

```text
fields-registry.md                  explica o campo
schemas/domain_knowledge.schema.json valida o campo
governanca/DECISOES.md             justifica a criação ou mudança do campo
CHANGELOG.md                       registra quando o campo mudou
tests/                             provam que registry e schema estão sincronizados
```

***

## 3. Escopo do fields-registry.md

O `fields-registry.md` deve catalogar todos os campos aceitos pelo Front Matter e pelo artefato JSON canônico derivado.

Inclui:

- campos obrigatórios;
- campos opcionais;
- campos condicionais;
- campos aninhados;
- objetos como `relationships`, `retrieval` e `content`;
- subcampos como `relationships.dependsOn`, `relationships.relatedTo`, `retrieval.searchable`, `retrieval.priority`, `retrieval.canonical`;
- campos de governança como `status`, `approved_by`, `approved_at`, `approval_ref`, quando forem adicionados;
- campos propostos, quando ainda não aprovados;
- campos deprecated, quando existirem.

Fora do escopo:

- valores reais sensíveis;
- aprovações de documentos individuais;
- histórico completo de decisões;
- duplicação integral do JSON Schema;
- detalhes de linha de código de implementação;
- dados transitórios de execução de runs;
- campos hipotéticos sem necessidade operacional identificada.

***

## 4. Nome e localização oficial

```text
governance/fields-registry.md como nome oficial.
```

## 5. Princípios de governança

### 5.1 Campo é ativo governado

Campos não são meros nomes em YAML.
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

### 5.2 Schema valida; registry explica

O JSON Schema decide se o documento é válido.

O `fields-registry.md` explica por que o campo existe, como deve ser interpretado e quem pode alterá-lo.

### 5.3 Campo novo não nasce no documento

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
atualização do changelog
  ↓
uso permitido no Front Matter
```

### 5.4 Campo não documentado é erro

Se um campo aparece no Front Matter mas não está no `fields-registry.md`, ele deve ser tratado como inválido.

Se um campo aparece no schema mas não está no registry, a implementação está incompleta.

Se um campo aparece no registry como ativo mas não está no schema, existe divergência entre documentação e contrato executável.

***

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
```

***

## 7. Estados dos campos

Todo campo deve ter um status de governança.

Estados recomendados:

```text
proposed
experimental
active
deprecated
removed
rejected
```

### proposed

Campo identificado como necessidade possível, mas ainda não aceito pelo schema.

### experimental

Campo aprovado para uso limitado, normalmente em branch, sandbox ou tipo documental restrito.

### active

Campo oficialmente aceito pelo schema e documentado no registry.

### deprecated

Campo ainda reconhecido por compatibilidade, mas não deve ser usado em novos documentos.

### removed

Campo removido do schema em versão maior.

### rejected

Campo proposto e rejeitado. Deve permanecer registrado se houver risco de reaparecer com outro nome.

***

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

***

## 9. Modelo de entrada de campo

Cada campo deve ser registrado usando este modelo:

```markdown
## Campo: `nome_do_campo`

### Nome oficial

`nome_do_campo`

### Caminho

`nome_do_campo` ou `objeto.subcampo`

### Definição

Explique o que o campo significa.

### Finalidade

Explique por que o campo existe e qual decisão operacional ele permite.

### Tipo

`string | array | object | boolean | integer | number | date | date-time`

### Obrigatoriedade

`obrigatório | opcional | condicional`

### Repetível

`sim | não`

### Valores permitidos

Liste valores quando houver vocabulário controlado.

### Formato

Regex, SemVer, ISO date, URI ou outro padrão aplicável.

### Escopo

Tipos de documento aos quais o campo se aplica.

### Exemplo válido

```yaml
nome_do_campo: "valor_valido"
```

### Exemplo inválido

```yaml
nome_do_campo: "valor_invalido"
```

### Regra de governança

Explique quem pode alterar, aprovar ou usar o campo.

### Relações com outros campos

Liste campos relacionados ou dependentes.

### Mapeamento externo

Dublin Core, PREMIS, schema.org, PROV, SemVer ou outro vocabulário, se aplicável.

### Dono

Equipe responsável.

### Status

`proposed | experimental | active | deprecated | removed | rejected`

### Introduzido em

Versão do padrão.

### Decisão associada

Referência para `DECISOES.md` ou `decision-register.md`.

### Schema associado

Path do schema onde o campo é validado.

### Testes associados

Lista de testes que protegem o comportamento do campo.
```

***

## 10. Campos iniciais a catalogar

Com base na implementação atual do repositório `kb`, os primeiros campos a catalogar devem ser:

```text
id
title
type
version
status
domain
boundedContext
aliases
tags
relationships
relationships.dependsOn
relationships.relatedTo
retrieval
retrieval.searchable
retrieval.priority
retrieval.canonical
content
content.markdown
content.summary
content.concepts
content.businessRules
content.examples
```

Campos recomendados para proposta de governança futura:

```text
schema_version
approved_by
approved_at
approval_ref
owner_team
created_at
updated_at
source_refs
risk_level
```

***

## 11. Ações para criação do fields-registry.md

### Ação 1 — Criar o arquivo

Criar:

```text
governanca/fields-registry.md
```

Critério de aceite:

- o arquivo existe;
- possui título;
- declara finalidade;
- declara regras gerais;
- lista todos os campos ativos do schema atual.

### Ação 2 — Extrair campos do schema atual

Ler:

```text
schemas/domain_knowledge.schema.json
```

Extrair:

- campos em `required`;
- campos em `properties`;
- objetos aninhados;
- campos com `enum`;
- campos com `const`;
- campos com `pattern`;
- campos bloqueados por `additionalProperties: false`.

Critério de aceite:

- todo campo do schema aparece no registry;
- todo subcampo aninhado aparece no registry;
- enums estão documentados.

### Ação 3 — Classificar campos por função

Classificar campos em grupos:

```text
Identidade
Versão
Tipo documental
Estado de governança
Domínio e contexto
Classificação e recuperação
Relações
Conteúdo
Campos derivados ou futuros
```

Critério de aceite:

- cada campo tem uma categoria funcional;
- nenhuma categoria mistura conceitos incompatíveis.

### Ação 4 — Documentar campos obrigatórios

Catalogar com prioridade:

```text
id
title
type
version
status
domain
boundedContext
aliases
tags
relationships
retrieval
content
```

Critério de aceite:

- cada campo obrigatório tem definição;
- cada campo obrigatório tem finalidade;
- cada campo obrigatório tem exemplo válido;
- cada campo obrigatório tem regra de governança.




Extrair:

- campos em `required`;
- campos em `properties`;
- objetos aninhados;
- campos com `enum`;
- campos com `const`;
- campos com `pattern`;
- campos bloqueados por `additionalProperties: false`.

Critério de aceite:

- todo campo do schema aparece no registry;
- todo subcampo aninhado aparece no registry;
- enums estão documentados.

### Ação 3 — Classificar campos por função

Classificar campos em grupos:

```text
Identidade
Versão
Tipo documental
Estado de governança
Domínio e contexto
Classificação e recuperação
Relações
Conteúdo
Campos derivados ou futuros
```

Critério de aceite:

- cada campo tem uma categoria funcional;
- nenhuma categoria mistura conceitos incompatíveis.

### Ação 4 — Documentar campos obrigatórios

Catalogar com prioridade:

```text
id
title
type
version
status
domain
boundedContext
aliases
tags
relationships
retrieval
content
```

Critério de aceite:

- cada campo obrigatório tem definição;
- cada campo obrigatório tem finalidade;
- cada campo obrigatório tem exemplo válido;
- cada campo obrigatório tem regra de governança.

### Ação 5 — Documentar campos aninhados

Catalogar:

```text
relationships.dependsOn
relationships.relatedTo
retrieval.searchable
retrieval.priority
retrieval.canonical
content.markdown
content.summary
content.concepts
content.businessRules
content.examples
```

Critério de aceite:

- cada subcampo tem caminho completo;
- cada subcampo tem tipo;
- cada subcampo tem relação com o objeto-pai.

### Ação 6 — Documentar enums e vocabulários controlados

Catalogar valores permitidos de:

```text
type
status
retrieval.priority
```

Critério de aceite:

- cada valor de enum tem significado;
- valores inválidos comuns são exemplificados;
- fica claro quando usar cada valor.

### Ação 7 — Documentar campos propostos

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

### Ação 8 — Definir regra de aprovação de campos novos

Adicionar ao registry a regra:

```text
Nenhum campo novo pode ser usado em documentos publicados antes de ser aprovado, documentado no registry, implementado no schema, coberto por teste e registrado no changelog.
```

Critério de aceite:

- regra aparece explicitamente no arquivo;
- processo de aprovação está descrito;
- papéis responsáveis estão definidos.

### Ação 9 — Criar matriz registry ↔ schema

Adicionar tabela:

```markdown
| Campo | Registry | Schema | Teste | Status |
|***|***:|***:|***:|***|
| id | sim | sim | sim | active |
```

Critério de aceite:

- todo campo ativo tem linha na matriz;
- divergências são visíveis;
- campo ativo sem schema é erro;
- campo no schema sem registry é erro.

### Ação 10 — Atualizar governança

Atualizar ou criar referência em:

```text
governanca/PROTOCOLO.md
governanca/REGISTRO_FONTES.md
governanca/LEDGER_KB_VERIFY.md
```

Critério de aceite:

- documentos normativos apontam para `fields-registry.md` como catálogo oficial de campos;
- fica claro que o schema continua sendo o contrato executável.

### Ação 11 — Atualizar changelog

Registrar criação do registry em:

```text
CHANGELOG.md
```

ou, se o repositório usar histórico estrutural:

```text
change-control/structural-changes.jsonl
```

Critério de aceite:

- criação do registry aparece como mudança estrutural;
- impacto é classificado;
- não há mudança silenciosa de governança.

### Ação 12 — Registrar decisão

Criar ou atualizar decisão em:

```text
governanca/DECISOES.md
```

ou:

```text
governanca/decision-register.md
```

Decisão recomendada:

```text
DR-XXX — Criar fields-registry.md como catálogo semântico e governamental dos campos
```

Critério de aceite:

- decisão explica por que o registry existe;
- decisão explica diferença entre registry e schema;
- decisão define que todo campo aceito precisa estar catalogado.

### Ação 13 — Criar teste de sincronização registry ↔ schema

Criar:

```text
tests/test_fields-registry.py
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

### Ação 14 — Atualizar CI

Garantir que o workflow rode:

```bash
python3 -m unittest discover -s tests -v
python3 ferramentas/kb_compile.py exemplos/domain_customer.md --schema schemas/domain_knowledge.schema.json --check-only
python3 ferramentas/check_kb_consistency.py .
python3 ferramentas/kb_validate.py .
```

Se `test_fields-registry.py` for adicionado, ele entra automaticamente no discover.

Critério de aceite:

- pull request com campo novo sem registry falha;
- pull request com registry sem schema falha;
- pull request com schema alterado sem documentação falha.

### Ação 15 — Criar exemplos de campo válido e inválido

Para cada campo crítico, incluir:

```text
exemplo válido
exemplo inválido
motivo da rejeição
```

Critério de aceite:

- `status`, `type`, `id`, `relationships` e `retrieval.priority` têm exemplos válidos e inválidos.

### Ação 16 — Definir política de campos propostos

Adicionar regra:

```text
Campos em proposed podem aparecer no fields-registry.md, mas não podem aparecer no schema nem em documentos publicados.
```

Critério de aceite:

- proposta não cria aceitação automática;
- campo proposto tem owner e problema documentado;
- uso experimental exige decisão específica.

### Ação 17 — Definir política de depreciação

Adicionar regra:

```text
Campo deprecated continua documentado, mas não deve ser usado em novos documentos.
```

Critério de aceite:

- campo deprecated tem substituto;
- campo deprecated tem versão de remoção planejada;
- migração é documentada.

### Ação 18 — Definir política de rejeição

Quando uma proposta for rejeitada, registrar em seção própria.

Critério de aceite:

- campo rejeitado tem motivo;
- nomes alternativos rejeitados são listados;
- evita reaparecimento com outro nome.

### Ação 19 — Definir owners dos campos

Cada campo deve ter owner.

Exemplos:

```text
id                    Metadata Governance
status                Metadata Governance
relationships         Knowledge Architecture
retrieval             Search / Retrieval
content               Docs Platform
approved_by           Governance Board
```

Critério de aceite:

- nenhum campo ativo fica sem owner.

### Ação 20 — Definir checklist de revisão

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
- [ ] O changelog foi atualizado?
- [ ] Templates foram atualizados, se necessário?
```

Critério de aceite:

- checklist existe;
- PRs de campo novo usam esse checklist.

***

## 12. Estrutura inicial sugerida para o fields-registry.md

O conteúdo inicial deve começar assim:

```markdown
# fields-registry.md — Registro oficial de campos

## 1. Finalidade

Este arquivo é o catálogo semântico e governamental dos campos aceitos pelo padrão de Front Matter da base de conhecimento.

Ele explica o significado, finalidade, status, owner, regras de uso e critérios de mudança de cada campo.

O JSON Schema valida tecnicamente os campos. Este registry explica semanticamente e governa seu uso.

## 2. Regra central

Campo aceito pelo schema precisa estar documentado neste registry.
Campo ativo neste registry precisa estar validado pelo schema.
Campo novo exige decisão, changelog, teste e owner.

## 3. Estados de campo

- proposed
- experimental
- active
- deprecated
- removed
- rejected

## 4. Campos ativos

## 13. Exemplo de campo catalogado: id

```markdown
## Campo: `id`

### Nome oficial

`id`

### Caminho

`id`

### Definição

Identificador único, estável e legível por máquina para o artefato de conhecimento.

### Finalidade

Permitir rastreamento, deduplicação, relacionamento, referência cruzada e auditoria.

### Tipo

`string`

### Obrigatoriedade

Obrigatório.

### Repetível

Não.

### Formato

```regex
^[a-z]+\.[a-z0-9_-]+$
```

### Exemplos válidos

```yaml
id: domain.customer
id: process.customer_registration
```

### Exemplos inválidos

```yaml
id: Cliente
id: FONTE-001
id: domain customer
```

### Escopo

Aplica-se a todos os artefatos `domain_knowledge`.

### Regra de governança

O `id` não deve ser reaproveitado para outro conceito. Mudança substancial de conceito exige novo ID ou decisão de migração.

### Dono

Metadata Governance.

### Status

active

### Introduzido em

1.0.0

### Decisão associada

DR-XXX

### Schema associado

`schemas/domain_knowledge.schema.json`

### Testes associados

`tests/test_domain_schema.py`
`tests/test_kb_compile.py`
```

***

## 14. Exemplo de campo catalogado: status

```markdown
## Campo: `status`

### Nome oficial

`status`

### Caminho

`status`

### Definição

Estado de governança do artefato dentro do ciclo de vida documental.

### Finalidade

Controlar se o artefato está em rascunho, revisão, aprovado ou obsoleto.

### Tipo

`string`

### Obrigatoriedade

Obrigatório.

### Valores permitidos

| Valor | Significado |
|***|***|
| `draft` | Artefato em elaboração |
| `review` | Artefato em revisão |
| `approved` | Artefato aprovado formalmente |
| `deprecated` | Artefato obsoleto, mantido por histórico |

### Regra de governança

`approved` deve exigir evidência formal de aprovação quando os campos `approved_by`, `approved_at` e `approval_ref` forem incorporados ao schema.

### Exemplos válidos

```yaml
status: approved
```

### Exemplos inválidos

```yaml
status: pronto
status: ok
status: finalizado
```

### Dono

Metadata Governance.

### Status

active

### Introduzido em

1.0.0

### Decisão associada

DR-XXX
```

***

## 15. Exemplo de campo proposto: schema_version

```markdown
## Proposta: `schema_version`

### Status

proposed

### Problema

O schema atual possui `version`, mas não explicita qual versão do contrato de metadados validou o documento.

### Campo existente resolve?

Não. `version` representa a versão do artefato/conteúdo, não a versão do schema.

### Tipo proposto

`string`

### Formato proposto

```regex
^[0-9]+\.[0-9]+$
```

### Exemplo proposto

```yaml
schema_version: "1.0"
```

### Uso operacional

Permitir migração, auditoria e validação por versão de contrato.

### Dono proposto

Metadata Governance.

### Decisão necessária

Sim.
```

***

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

***

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

***

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

***

## 19. Critérios de aceite da implementação

A criação do `fields-registry.md` estará completa quando:

```text
1. O arquivo governanca/fields-registry.md existir.
2. Todos os campos do schema atual estiverem catalogados.
3. Todos os campos obrigatórios tiverem definição e finalidade.
4. Todos os enums tiverem valores explicados.
5. Todos os objetos aninhados tiverem subcampos catalogados.
6. Campos propostos estiverem separados de campos ativos.
7. O registry apontar para o schema oficial.
8. O schema continuar bloqueando campos extras.
9. Houver teste de sincronização registry ↔ schema.
10. O CI executar esse teste.
11. A criação do registry estiver registrada em decisão de governança.
12. A criação estiver registrada no changelog ou histórico estrutural.
13. O README ou protocolo apontar para o registry como catálogo oficial.
```

***

## 20. Sequência de implementação recomendada

### Fase 1 — Criação mínima

- Criar `governanca/fields-registry.md`.
- Documentar finalidade, regra central e estados de campo.
- Catalogar campos obrigatórios do schema atual.

### Fase 2 — Cobertura completa

- Catalogar campos opcionais.
- Catalogar subcampos aninhados.
- Documentar enums.
- Criar matriz registry ↔ schema.

### Fase 3 — Governança

- Criar decisão `DR-XXX`.
- Atualizar changelog.
- Atualizar protocolo e inventário.
- Definir owners.

### Fase 4 — Automação

- Criar `tests/test_fields-registry.py`.
- Garantir execução no CI.
- Bloquear divergência entre registry e schema.

### Fase 5 — Evolução

- Adicionar seção de campos propostos.
- Avaliar `schema_version`, `approved_by`, `approved_at`, `approval_ref`, `owner_team`, `created_at`, `updated_at`, `risk_level`.
- Criar decisões e migrações conforme necessário.

***

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

```python
schema_fields = extract_fields("schemas/domain_knowledge.schema.json")
registry_active_fields = extract_active_fields("governanca/fields-registry.md")
registry_proposed_fields = extract_proposed_fields("governanca/fields-registry.md")

assert schema_fields <= registry_active_fields
assert registry_active_fields <= schema_fields
assert not proposed_fields_required_in_schema
```

***

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

***

## 23. Regra final

O `fields-registry.md` deve ser tratado como o catálogo semântico e governamental dos campos.

A regra final é:

```text
fields-registry.md governa o significado.
JSON Schema governa a validade.
DECISOES.md governa o motivo.
CHANGELOG.md governa a mudança.
CI governa a conformidade.
```

Sem esse arquivo, o schema valida estrutura, mas o sistema ainda não governa plenamente o significado dos campos.


***

## 24. Base científica e normativa para a escolha dos campos

Esta seção documenta as evidências que justificam a importância real da escolha dos campos no sistema de Front Matter YAML.

A conclusão técnica é:

```text
A eficiência do Front Matter não vem do YAML como sintaxe.
A eficiência vem da seleção, definição, validação e governança dos campos.
```

A literatura e os padrões abaixo sustentam semanticamente essa conclusão.

***

### 24.1 Metadados tornam objetos digitais acionáveis por máquinas

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

Aplicação ao Front Matter:

```text
Campos como id, type, status, retrieval, relationships e schema_version são os mecanismos que tornam documentos Markdown acionáveis por máquinas, pipelines e agentes.
```

Afirmação validada:

```text
Campos definem o que o sistema consegue entender e automatizar.
```

***

### 24.2 Campos claros reduzem ambiguidade semântica

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

Aplicação ao Front Matter:

```text
Todo campo do fields-registry.md deve ter nome oficial, definição, tipo, finalidade e regra de uso. Sem isso, o campo pode ser interpretado de formas diferentes por pessoas, scripts e agentes.
```

Afirmação validada:

```text
Campos bons reduzem ambiguidade; campos mal definidos criam interpretações concorrentes.
```

***

### 24.3 Schema transforma campo em contrato executável

Fonte principal:

```text
JSON Schema Draft 2020-12
URL: https://json-schema.org/draft/2020-12/json-schema-core
```

Evidência usada:

```text
A especificação JSON Schema define um vocabulário para descrever estrutura de dados JSON e impor restrições que podem passar ou falhar em validação.
```

Aplicação ao Front Matter:

```text
O fields-registry.md explica o significado do campo, mas o JSON Schema decide se o documento é válido. A combinação registry + schema transforma metadados em contrato operacional.
```

Afirmação validada:

```text
Campos devem ser validáveis; caso contrário, viram apenas decoração documental.
```

***

### 24.4 Bloqueio de campos inventados evita corrupção do sistema

Fonte principal:

```text
JSON Schema Draft 2020-12 — additionalProperties
URL: https://json-schema.org/draft/2020-12/json-schema-core
```

Evidência usada:

```text
A especificação define additionalProperties como mecanismo para controlar propriedades que não foram declaradas por properties ou patternProperties. Quando additionalProperties é false, propriedades não previstas são rejeitadas.
```

Aplicação ao Front Matter:

```json
{
  "additionalProperties": false
}
```

Afirmação validada:

```text
Campos inventados por pessoas ou agentes devem ser bloqueados. Campo não documentado não existe.
```

***

### 24.5 Vocabulários controlados melhoram consistência e recuperação

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

Aplicação ao Front Matter:

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

***

### 24.6 Identidade estável sustenta rastreabilidade e deduplicação

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

Aplicação ao Front Matter:

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

***

### 24.7 Proveniência sustenta origem, decisão e destino

Fonte principal:

```text
W3C PROV-DM — Provenance Data Model
URL: https://www.w3.org/TR/prov-dm/
```

Evidência usada:

```text
PROV descreve proveniência como informação sobre entidades, atividades e agentes envolvidos na produção ou influência de um dado ou recurso.
```

Aplicação ao Front Matter:

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

***

### 24.8 JSON canônico melhora comparação, hash e auditoria

Fonte principal:

```text
RFC 8785 — JSON Canonicalization Scheme (JCS)
URL: https://www.rfc-editor.org/rfc/rfc8785
```

Evidência usada:

```text
O RFC explica que operações criptográficas, como hashing e assinatura digital, dependem de uma representação invariável dos dados.
```

Aplicação ao Front Matter:

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

***

### 24.9 Campos demais aumentam custo e campos de menos reduzem contexto

Fonte principal:

```text
FAIR Principles — Scientific Data / Nature
URL: https://www.nature.com/articles/sdata201618
```

Evidência usada:

```text
FAIR apresenta princípios mínimos e incrementais, com baixa barreira de entrada, mas suficientes para descoberta, interoperabilidade e reuso.
```

Aplicação ao Front Matter:

```text
Campo obrigatório demais reduz adesão.
Campo opcional demais vira lixo semântico.
Campo de menos deixa o sistema sem contexto operacional.
```

Afirmação validada:

```text
A seleção de campos precisa equilibrar suficiência operacional e simplicidade de manutenção.
```

***

### 24.10 O campo certo elimina inferência frágil

Fonte principal:

```text
FAIR Principles — Scientific Data / Nature
URL: https://www.nature.com/articles/sdata201618
```

Evidência usada:

```text
FAIR enfatiza que máquinas precisam de metadados explícitos para descobrir, avaliar e reutilizar recursos sem depender de interpretação humana contínua.
```

Aplicação ao Front Matter:

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

***

### 24.11 fields-registry.md é necessário para governar significado

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

Aplicação ao Front Matter:

```text
fields-registry.md governa o significado.
JSON Schema governa a validade.
```

Afirmação validada:

```text
O registry é necessário porque o schema sozinho valida estrutura, mas não explica integralmente intenção, owner, governança e motivo do campo.
```

***

### 24.12 Síntese das evidências

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
10. A eficiência do Front Matter depende da qualidade semântica dos campos escolhidos.
```

***

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

