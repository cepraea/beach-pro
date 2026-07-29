---
document_id: DOC-GOV-WORKFLOW-PLANO
title: "Plano de operacionalização do workflow documental"
document_type: workflow
version: "0.1.1"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - orientacao_de_implementacao
prohibited_uses:
  - autocanonizacao
---

# Plano de operacionalização do workflow documental

- [Plano de operacionalização do workflow documental](#plano-de-operacionalização-do-workflow-documental)
  - [1. Resultado esperado](#1-resultado-esperado)
  - [2. Separação obrigatória dos workflows](#2-separação-obrigatória-dos-workflows)
    - [2.1 Workflow documental](#21-workflow-documental)
    - [2.2 Workflow posterior de especificação e produto](#22-workflow-posterior-de-especificação-e-produto)
  - [3. Definição operacional de canônico documental](#3-definição-operacional-de-canônico-documental)
  - [4. Objeto da canonização](#4-objeto-da-canonização)
  - [5. Estados documentais controlados](#5-estados-documentais-controlados)
  - [6. Transições autorizadas](#6-transições-autorizadas)
  - [7. Condições de transição](#7-condições-de-transição)
  - [8. Normalização obrigatória do acervo](#8-normalização-obrigatória-do-acervo)
    - [8.1 Arquitetura normativa de `/docs`](#81-arquitetura-normativa-de-docs)
    - [8.2 Contrato de cada diretório](#82-contrato-de-cada-diretório)
    - [8.3 Convenção para nomes físicos](#83-convenção-para-nomes-físicos)
    - [8.4 Identidade lógica versus nome físico](#84-identidade-lógica-versus-nome-físico)
    - [8.5 Migração do acervo atual](#85-migração-do-acervo-atual)
  - [9. Registro mestre de documentos](#9-registro-mestre-de-documentos)
  - [10. Autoridades e segregação de funções](#10-autoridades-e-segregação-de-funções)
  - [11. Contratos validáveis](#11-contratos-validáveis)
    - [11.1 Contrato de aprovação](#111-contrato-de-aprovação)
    - [11.2 Contrato de promoção canônica](#112-contrato-de-promoção-canônica)
    - [11.3 Contrato do registro canônico](#113-contrato-do-registro-canônico)
  - [12. Matrizes de controle](#12-matrizes-de-controle)
  - [13. Gates documentais bloqueantes](#13-gates-documentais-bloqueantes)
    - [13.1 Resultado obrigatório de gate](#131-resultado-obrigatório-de-gate)
    - [13.2 Condições obrigatórias do `G-CANON`](#132-condições-obrigatórias-do-g-canon)
  - [14. Definition of Done canônico documental](#14-definition-of-done-canônico-documental)
  - [15. Regras de consumo pelo agente de IA](#15-regras-de-consumo-pelo-agente-de-ia)
  - [16. Validadores automáticos](#16-validadores-automáticos)
  - [17. Proteção de versões e evidências](#17-proteção-de-versões-e-evidências)
  - [18. Testes negativos e de bypass](#18-testes-negativos-e-de-bypass)
  - [19. Observabilidade e auditoria](#19-observabilidade-e-auditoria)
  - [20. Ordem de implementação](#20-ordem-de-implementação)
  - [21. Entregáveis](#21-entregáveis)
    - [21.1 Normativos](#211-normativos)
    - [21.2 Processáveis](#212-processáveis)
    - [21.3 Matrizes](#213-matrizes)
    - [21.4 Evidências operacionais](#214-evidências-operacionais)
  - [22. Done da implantação do workflow](#22-done-da-implantação-do-workflow)
  - [23. Limites das garantias](#23-limites-das-garantias)
  - [24. Estado da implementação](#24-estado-da-implementação)

## 1. Resultado esperado

Este plano transforma as regras documentadas do CEPRAEA BEACH PRO em um
workflow executável cujo resultado terminal é:

```text
CANONICA_VIGENTE
```

Uma execução somente está concluída quando uma versão documental identificada,
validada e formalmente aprovada for declarada como referência oficial,
prevalente e vigente para um escopo determinado.

O workflow documental não termina em `CANDIDATA`, não termina apenas em
`APROVADA` e não concede autorização para implementação, dados reais, piloto ou
produção.

## 2. Separação obrigatória dos workflows

O ciclo documental e o ciclo de construção e validação do produto possuem
objetos, autoridades, evidências e riscos diferentes. Eles não podem compartilhar
um único estado terminal.

### 2.1 Workflow documental

```text
RASCUNHO
→ BASE_CONTROLADA
→ EM_VALIDACAO
→ VALIDADO
→ CANDIDATA
→ EM_APROVACAO
→ APROVADA
→ CANONICA_VIGENTE
```

Resultado: conteúdo oficial aprovado e prevalente para o escopo declarado.

### 2.2 Workflow posterior de especificação e produto

```text
CANONICA_VIGENTE
→ REQUISITOS_VALIDADOS
→ ESPECIFICACAO_APROVADA_PARA_IMPLEMENTACAO
→ IMPLEMENTACAO
→ V1_SINTETICA
→ AUTORIZACAO_DE_DADOS_REAIS
→ V2_PILOTO_CONTROLADO
→ V3_VALIDACAO_AMPLIADA
→ AUTORIZACAO_DE_PRODUCAO
→ BASELINE_OPERACIONAL_DE_PRODUCAO
```

`V1`, `V2`, `V3`, `D0`, piloto e produção ficam fora do workflow documental.
A saída canônica pode alimentar esses processos, mas não os autoriza.

## 3. Definição operacional de canônico documental

> Um documento canônico é uma versão identificada, validada e formalmente
> aprovada pela autoridade competente, publicada no repositório oficial e
> declarada como referência vigente e prevalente para um escopo determinado,
> com proveniência, vigência, precedência e histórico de substituição
> verificáveis.

```text
CANONICO_DOCUMENTAL =
    ARTEFATO_IDENTIFICADO
  ∧ CONTEUDO_DELIMITADO
  ∧ FONTES_RASTREAVEIS
  ∧ CONTRATOS_VALIDOS
  ∧ GATES_APROVADOS
  ∧ AUTORIDADE_COMPETENTE
  ∧ APROVACAO_FORMAL
  ∧ ESCOPO_DE_AUTORIDADE
  ∧ VIGENCIA_DEFINIDA
  ∧ PRECEDENCIA_DEFINIDA
  ∧ PUBLICACAO_CONTROLADA
  ∧ HISTORICO_PRESERVADO
```

A ausência de qualquer condição impede o estado `CANONICA_VIGENTE`.

## 4. Objeto da canonização

A canonização recai sobre uma versão imutável de um documento, e não sobre:

- um nome de arquivo sem versão;
- o conteúdo mutável de um branch;
- uma pasta inteira indistintamente;
- um assunto genérico;
- uma aprovação verbal;
- a versão “mais recente” sem ato formal.

Cada objeto deve ser identificado, no mínimo, por:

```text
document_id + version + content_hash
```

Podem existir vários documentos canônicos simultaneamente quando seus escopos
de autoridade forem distintos. Não podem existir duas versões
`CANONICA_VIGENTE` com regras incompatíveis para o mesmo assunto, escopo e
período sem uma regra explícita de precedência.

## 5. Estados documentais controlados

| Estado | Significado | Pode ser referência vigente? |
| --- | --- | --- |
| `RASCUNHO` | Conteúdo em elaboração, ainda não controlado | Não |
| `BASE_CONTROLADA` | Conteúdo consolidado, identificado e submetido a controle | Não |
| `EM_VALIDACAO` | Versão sob avaliação contra critérios definidos | Não |
| `CORRECAO_REQUERIDA` | Falha bloqueante exige alteração e nova validação | Não |
| `VALIDADO` | Critérios de validação satisfeitos; ainda sem aprovação | Não |
| `CANDIDATA` | Versão congelada, com hash, apta à decisão de aprovação | Não |
| `EM_APROVACAO` | Decisão formal da autoridade está pendente | Não |
| `APROVADA` | Aceita para a finalidade declarada; ainda não publicada como prevalente | Não |
| `CANONICA_VIGENTE` | Referência oficial, vigente e prevalente no escopo | Sim |
| `SUPERADA` | Substituída por outra versão canônica e preservada como histórico | Não |
| `REVOGADA` | Validade retirada por decisão formal | Não |

`CORRECAO_REQUERIDA`, `SUPERADA` e `REVOGADA` são estados de controle e não
etapas obrigatórias de toda execução.

## 6. Transições autorizadas

| Origem | Destino | Evento | Autoridade | Gate |
| --- | --- | --- | --- | --- |
| `RASCUNHO` | `BASE_CONTROLADA` | Consolidação registrada | Autor documental | `G-ARCH`, `G0–G3` |
| `BASE_CONTROLADA` | `EM_VALIDACAO` | Solicitação de validação | Responsável pelo workflow | `G3` |
| `EM_VALIDACAO` | `CORRECAO_REQUERIDA` | Falha bloqueante | Validador | `G4` falhou |
| `CORRECAO_REQUERIDA` | `EM_VALIDACAO` | Nova versão corrigida | Autor documental | `G0–G3` |
| `EM_VALIDACAO` | `VALIDADO` | Validação concluída | Validador | `G4–G6` |
| `VALIDADO` | `CANDIDATA` | Congelamento da versão | Responsável pelo workflow | `G7` |
| `CANDIDATA` | `EM_APROVACAO` | Submissão formal | Responsável pelo workflow | `G7` |
| `EM_APROVACAO` | `APROVADA` | Aceite formal | Autoridade aprovadora | `G8` |
| `APROVADA` | `CANONICA_VIGENTE` | Publicação e promoção | Autoridade de canonização | `G-CANON` |
| `CANONICA_VIGENTE` | `SUPERADA` | Nova canônica entra em vigor | Autoridade de canonização | `G-SUPERSEDE` |
| Qualquer estado vigente | `REVOGADA` | Revogação formal | Autoridade competente | `G-REVOGA` |

Uma edição material gera nova versão e reinicia o ciclo no estado determinado
pela política de mudanças. O conteúdo aprovado ou canônico nunca é alterado no
mesmo identificador de versão.

## 7. Condições de transição

Cada transição deve declarar:

- estado de origem;
- evento disparador;
- ator e papel autorizados;
- entradas;
- contratos aplicáveis;
- validações;
- evidências;
- resultado do gate;
- estado de destino;
- data e hora;
- motivo;
- ação de retorno ou correção.

Um documento não muda de estado porque seu texto declara que mudou. O estado
vigente vem do registro mestre e somente pode ser alterado por uma transição
válida do workflow.

## 8. Normalização obrigatória do acervo

Automatizar o estado atual sem normalização propagaria inconsistências.

Ações:

- escolher entre `DESC`, `DESCRICAO` e `DECISAO` como nomenclatura oficial;
- alinhar títulos internos, nomes físicos e referências;
- corrigir links para arquivos inexistentes;
- remover estados pré-promoção da versão candidata;
- sincronizar o resultado final da validação e das ações corretivas;
- definir qual documento substitui, complementa ou é fonte de qual documento;
- atribuir ID, versão, responsável, data, estado e hash a cada artefato;
- delimitar o escopo de autoridade de cada documento;
- registrar quais documentos são apenas históricos, informativos ou derivados;
- criar o registro mestre do acervo.

Entregável: `docs/registry/registro-documentos.yaml`.

Garantia obtida: cada artefato possui identidade única, função, estado e versão
verificáveis.

### 8.1 Arquitetura normativa de `/docs`

A arquitetura oficial deve separar governança, fontes, artefatos em elaboração,
documentos canônicos, derivações, validações, evidências e histórico:

```text
docs/
├── README.md
├── inventario-documentos.md
│
├── governance/
│   ├── workflows/
│   │   └── workflow-documentacao.md
│   ├── policies/
│   │   ├── politica-arquitetura-documental.md
│   │   ├── politica-autoridade-documental.md
│   │   ├── politica-versionamento-documental.md
│   │   └── politica-uso-ia-documental.md
│   ├── protocols/
│   │   └── protocolo-qualidade-documental.md
│   └── matrices/
│       ├── matriz-autoridade-documental.md
│       ├── matriz-precedencia-documental.md
│       ├── matriz-rastreabilidade-documental.md
│       ├── matriz-gates-evidencias.md
│       └── matriz-uso-ia-documental.md
│
├── registry/
│   ├── registro-documentos.yaml
│   └── workflow-documentacao.yaml
│
├── contracts/
│   └── schemas/
│
├── sources/
│   ├── primary/
│   └── supporting/
│
├── controlled/
│   ├── bases/
│   └── candidates/
│
├── canonical/
│   ├── context/
│   ├── decisions/
│   ├── glossary/
│   └── requirements/
│
├── derived/
│   └── requirements/
│
├── validation/
│   ├── reports/
│   └── corrective-actions/
│
├── evidence/
│   ├── approvals/
│   ├── promotions/
│   └── gates/
│
└── archive/
    ├── superseded/
    └── revoked/
```

Diretórios vazios não precisam ser criados antecipadamente. Eles passam a
existir quando houver um artefato válido para armazenar.

### 8.2 Contrato de cada diretório

| Caminho | Conteúdo permitido | Autoridade decorrente do caminho |
| --- | --- | --- |
| `docs/governance/` | Workflows, políticas, protocolos e matrizes | Nenhuma sem aprovação própria |
| `docs/registry/` | Estado mestre e definições processáveis do workflow | Fonte operacional do estado |
| `docs/contracts/schemas/` | Contratos estruturais validáveis | Define formato, não aprova conteúdo |
| `docs/sources/primary/` | Fontes primárias preservadas | Autoridade limitada à origem |
| `docs/sources/supporting/` | Fontes auxiliares e contextuais | Não prevalece sobre fonte primária |
| `docs/controlled/` | Bases controladas e versões candidatas | Não canônico |
| `docs/canonical/` | Cópias publicadas de versões canônicas vigentes | Depende de registro e `G-CANON` |
| `docs/derived/` | Requisitos e outros artefatos derivados | Não aprovado por derivação |
| `docs/validation/` | Relatórios e ações corretivas | Evidência de avaliação |
| `docs/evidence/` | Aprovações, promoções e resultados de gates | Evidência; não substitui o documento |
| `docs/archive/` | Versões superadas ou revogadas | Histórico, nunca vigente |

A presença física em `docs/canonical/` não concede canonicidade. O documento
somente é canônico quando o registro mestre aponta `CANONICA_VIGENTE`, o
`G-CANON` retornou `pass` e o hash publicado corresponde ao hash aprovado.

### 8.3 Convenção para nomes físicos

O formato geral é:

```text
<tipo>-<dominio-ou-escopo>[-<assunto>].<extensao>
```

Exemplos:

```text
contexto-cepraea-beach-pro.md
decisoes-cepraea-beach-pro.md
requisitos-funcionais-cepraea.md
workflow-documentacao.md
protocolo-qualidade-documental.md
matriz-autoridade-documental.md
registro-documentos.yaml
```

Regras obrigatórias:

- usar letras minúsculas;
- usar somente caracteres ASCII;
- remover acentos e sinais diacríticos;
- separar palavras com hífen;
- não usar espaços, sublinhados ou travessões tipográficos;
- usar termos em português, salvo identificadores técnicos controlados;
- usar um vocabulário controlado para o componente `<tipo>`;
- manter o nome físico estável durante o ciclo de vida do documento lógico;
- manter ID, versão, estado e data nos metadados, não no nome físico;
- não usar palavras como `final`, `novo`, `ultima`, `corrigido` ou equivalentes;
- não reutilizar o mesmo caminho para outro `document_id`;
- registrar todo caminho em `docs/registry/registro-documentos.yaml`;
- armazenar caminhos do registro relativos à raiz do repositório;
- validar correspondência exata entre caminho, `document_id` e hash;
- usar links Markdown relativos ao arquivo de origem e validar seu destino;
- respeitar maiúsculas e minúsculas em caminhos e links;
- criar redirecionamento ou mapa de migração quando um caminho legado mudar.

Tipos iniciais controlados:

```text
contexto
contrato
decisao
glossario
requisito
protocolo
workflow
politica
matriz
relatorio
registro
inventario
evidencia
```

`README.md` é a única exceção inicial de caixa por convenção de entrada do
repositório. Schemas JSON usam:

```text
<objeto>.schema.json
```

Evidências geradas usam identificadores estáveis:

```text
<tipo>-<document-id>-<event-id>.<extensao>
```

Datas, quando indispensáveis em evidências externas, usam `AAAA-MM-DD`. Elas não
substituem ID, versão, hash ou registro de evento.

### 8.4 Identidade lógica versus nome físico

Os elementos têm funções distintas:

| Elemento | Função | Pode mudar? |
| --- | --- | --- |
| `document_id` | Identidade permanente do documento lógico | Não |
| `title` | Nome legível apresentado ao usuário | Sim, com registro |
| `current_path` | Localização física atual | Por transição ou migração controlada |
| `canonical_path` | Local de publicação da versão canônica | Definido na canonização |
| `version` | Identifica uma revisão material | Aumenta a cada nova versão |
| `content_hash` | Identifica exatamente os bytes aprovados | Muda com o conteúdo |
| `status` | Estado vigente no workflow | Somente por transição válida |

O título interno não deve ser usado como identidade. O nome físico não deve
carregar versão ou estado do workflow. O diretório pode refletir a classe
operacional, como `candidates`, `canonical` ou `archive`, mas não concede o
estado: o registro mestre continua sendo a autoridade. A expressão “versão
candidata”, por exemplo, pode determinar o diretório durante a transição, mas
não integra o nome físico.

Ao canonizar, `current_path` e `canonical_path` devem apontar para o mesmo
artefato em `docs/canonical/`. Ao superar ou revogar a versão, `current_path`
passa a apontar para `docs/archive/`, enquanto `canonical_path` permanece no
registro histórico como o local em que aquela versão foi publicada.

### 8.5 Migração do acervo atual

Os nomes atuais são considerados legados até a execução de uma migração
controlada. O plano não autoriza renomeação isolada.

A migração deve:

1. inventariar caminhos atuais e referências recebidas;
2. atribuir `document_id` antes de renomear;
3. definir o caminho de destino conforme a arquitetura;
4. produzir uma tabela `caminho_anterior → canonical_path`;
5. atualizar links e referências de modo atômico;
6. executar o validador de links;
7. confirmar que não surgiram arquivos duplicados ou órfãos;
8. registrar o evento e o hash antes e depois;
9. preservar o histórico no repositório;
10. promover a mudança somente após aprovação do gate de migração.

O gate de migração deve falhar se houver link quebrado, caminho duplicado,
referência ambígua, arquivo não inventariado ou divergência entre o registro
mestre e o sistema de arquivos.

## 9. Registro mestre de documentos

O registro mestre é a fonte operacional do estado documental. O conteúdo de um
arquivo não pode se autodeclarar canônico.

Campos mínimos:

```yaml
document:
  document_id: DOC-CEPRAEA-CONTEXTO
  title: ""
  current_path: ""
  canonical_path: null
  version: ""
  content_hash: ""
  document_type: ""
  status: RASCUNHO
  owner: ""
  authority_scope:
    subjects: []
    permitted_uses: []
    prohibited_uses: []
  provenance:
    source_ids: []
  validity:
    effective_from: null
    effective_until: null
    review_due_at: null
  precedence:
    supersedes: []
    superseded_by: null
    complemented_by: []
    conflict_rule: ""
  records:
    validation_id: null
    approval_id: null
    promotion_id: null
    evidence_package_id: null
```

## 10. Autoridades e segregação de funções

Criar `docs/governance/matrices/matriz-autoridade-documental.md` e uma política
processável de autoridade.

| Objeto ou ação | Produz/declara | Valida | Aprova/promove |
| --- | --- | --- | --- |
| Fonte factual | Fonte identificada | Curador documental | Autoridade do assunto |
| Contexto documental | Autor documental | Validador | Davi |
| Requisito derivado | Analista ou agente | Revisor independente | Davi |
| Aprovação documental | Workflow prepara | Gate documental verifica | Davi |
| Canonização | Workflow prepara | `G-CANON` verifica | Davi |
| Produção | Processo posterior | Gates técnicos e legais | Autoridades aplicáveis |

A aprovação e a canonização devem exigir:

- identidade autenticada;
- papel exercido;
- competência sobre o escopo;
- documento, versão e hash;
- finalidade autorizada;
- data e hora;
- decisão inequívoca;
- registro de evidência.

No mínimo:

- o autor produz;
- o validador verifica;
- o revisor independente testa a derivação quando aplicável;
- Davi aprova e autoriza a canonização;
- a automação verifica contratos, autoridade e gates.

Quando uma pessoa acumular papéis, o registro deve indicar explicitamente qual
papel foi exercido em cada evento. A automação não substitui a autoridade
humana e a autoridade humana não pode declarar que uma validação automática
inexistente passou.

## 11. Contratos validáveis

Contratos mínimos:

1. `documento.schema.json`;
2. `fonte.schema.json`;
3. `alegacao.schema.json`;
4. `decisao.schema.json`;
5. `requisito.schema.json`;
6. `validacao.schema.json`;
7. `acao-corretiva.schema.json`;
8. `aprovacao.schema.json`;
9. `promocao.schema.json`;
10. `evidencia.schema.json`;
11. `registro-canonico.schema.json`;
12. `evento-workflow.schema.json`;
13. `resultado-gate.schema.json`.

Regras obrigatórias:

- nenhum claim sem fonte ou classificação de incerteza;
- nenhum requisito sem origem;
- nenhum requisito aprovado sem critério de aceitação;
- nenhuma decisão sem autoridade e escopo;
- nenhuma aprovação sem objeto, versão, hash e finalidade;
- nenhuma promoção sem versão imutável;
- nenhum gate concluído sem evidência;
- nenhum registro canônico sem vigência e precedência;
- nenhum documento pode se autodeclarar canônico;
- nenhum hash pode ser calculado antes da última alteração da candidata.

### 11.1 Contrato de aprovação

```yaml
approval:
  approval_id: APR-0001
  document_id: DOC-CEPRAEA-CONTEXTO
  version: ""
  content_hash: ""
  purpose: ""
  scope: []
  approved_by: ""
  authority_role: ""
  decision: approved
  reservations: []
  non_blocking_pending_items: []
  approved_at: ""
  evidence_ids: []
```

### 11.2 Contrato de promoção canônica

```yaml
promotion:
  promotion_id: PROM-CANON-0001
  document_id: DOC-CEPRAEA-CONTEXTO
  version: ""
  content_hash: ""
  from_status: APROVADA
  to_status: CANONICA_VIGENTE
  authority_scope:
    subjects: []
    permitted_uses: []
    prohibited_uses: []
  validity:
    effective_from: ""
    effective_until: null
    review_due_at: ""
  precedence:
    supersedes: []
    complemented_by: []
    conflicts_resolved_by: []
  approval_id: ""
  gate_result_id: ""
  evidence_package_id: ""
  promoted_by: ""
  authority_role: ""
  promoted_at: ""
```

### 11.3 Contrato do registro canônico

```yaml
canonical_record:
  canonical_record_id: CANON-0001
  document_id: DOC-CEPRAEA-CONTEXTO
  title: ""
  version: ""
  content_hash: ""
  status: CANONICA_VIGENTE
  authority:
    approved_by: ""
    role: ""
    approved_at: ""
    approval_id: ""
    promotion_id: ""
  authority_scope:
    subjects: []
    permitted_uses: []
    prohibited_uses: []
  provenance:
    source_ids: []
    validation_id: ""
    evidence_package_id: ""
  validity:
    effective_from: ""
    effective_until: null
    review_due_at: ""
  precedence:
    supersedes: []
    complemented_by: []
    conflicts_resolved_by: []
  repository:
    canonical_path: ""
    immutable_reference: ""
```

## 12. Matrizes de controle

Criar e manter:

- documento × versão × estado;
- documento × assunto × escopo de autoridade;
- documento × substitui × substituído por;
- documento × complementa × é complementado por;
- assunto × fonte canônica;
- assunto × regra de precedência;
- ator × papel × autoridade;
- documento × fonte × claim;
- problema × objetivo × requisito;
- requisito × origem × decisão;
- requisito × critério de aceitação;
- fase × entrada × gate × saída;
- gate × evidência;
- risco × controle;
- dado × visibilidade × retenção;
- documento canônico × usos permitidos × usos proibidos.

Garantia obtida: relações ausentes, órfãs, sobrepostas ou contraditórias tornam-se
detectáveis.

## 13. Gates documentais bloqueantes

| Gate | Condição mínima |
| --- | --- |
| `G-ARCH — Arquitetura` | Caminho, diretório e nome físico cumprem a convenção |
| `G0 — Identidade` | ID, tipo, versão, responsável, data e caminho |
| `G1 — Integridade` | Hash calculado sobre a versão exata e artefato preservado |
| `G2 — Evidência` | Claims críticos possuem fonte ou incerteza explícita |
| `G3 — Semântica e escopo` | Vocabulário, inclusão, exclusão e fases são consistentes |
| `G4 — Qualidade` | Critérios `PA-*` aplicáveis foram avaliados |
| `G5 — Remediação` | Nenhuma ação bloqueante permanece aberta |
| `G6 — Rastreabilidade` | Conteúdo, decisões e derivações possuem origens válidas |
| `G7 — Candidatura` | Versão congelada, contratos válidos e evidências completas |
| `G8 — Aprovação` | Aceite autenticado para documento, versão, hash e finalidade |
| `G-CANON — Canonização` | Publicação, vigência, precedência e autoridade confirmadas |
| `G-SUPERSEDE — Substituição` | Nova canônica válida e anterior preservada como histórica |
| `G-REVOGA — Revogação` | Motivo, autoridade, impacto e comunicação registrados |

`G9 — Implementação`, `G10 — Dados reais` e `G11 — Produção` pertencem ao
workflow posterior e não integram o `Done` canônico documental.

### 13.1 Resultado obrigatório de gate

```yaml
gate_result:
  gate_result_id: GATE-RESULT-0001
  gate_id: G-CANON
  document_id: DOC-CEPRAEA-CONTEXTO
  version: ""
  content_hash: ""
  status: blocked
  evaluated_at: ""
  evaluator: ""
  evaluator_role: ""
  evidence_ids: []
  failures: []
  next_actions: []
```

Estados permitidos para o resultado:

- `pass`;
- `fail`;
- `blocked`;
- `not_applicable`, acompanhado de justificativa e autoridade.

`pending`, ausência de resultado ou evidência incompleta bloqueiam a transição.

### 13.2 Condições obrigatórias do `G-CANON`

O gate somente retorna `pass` quando:

- a candidata aprovada está identificada por ID, versão e hash;
- o caminho e o nome físico cumprem o contrato de arquitetura;
- o hash atual corresponde ao conteúdo aprovado;
- todos os contratos aplicáveis são válidos;
- todos os gates anteriores retornaram `pass`;
- não há ação corretiva bloqueante aberta;
- o escopo de autoridade está definido;
- os usos permitidos e proibidos estão explícitos;
- a precedência sobre outros documentos está resolvida;
- a data inicial de vigência está registrada;
- a data de revisão está registrada;
- a aprovação identifica a autoridade competente;
- o ato de promoção identifica a autoridade de canonização;
- o caminho de publicação oficial está definido;
- a referência imutável foi gerada;
- o inventário e o registro mestre foram atualizados;
- versões anteriores foram marcadas como `SUPERADA`, quando aplicável;
- o pacote de evidências está completo;
- as regras de consumo por agentes de IA estão publicadas.

## 14. Definition of Done canônico documental

Uma execução do workflow está `DONE` somente quando:

```text
DONE_CANONICO_DOCUMENTAL =
    STATUS_CANONICA_VIGENTE
  ∧ ARQUITETURA_VALIDA
  ∧ NOME_FISICO_VALIDO
  ∧ G_CANON_PASS
  ∧ TODOS_OS_GATES_ANTERIORES_PASS
  ∧ ZERO_BLOQUEIOS_ABERTOS
  ∧ CONTRATOS_VALIDOS
  ∧ APROVACAO_AUTENTICADA
  ∧ PROMOCAO_AUTORIZADA
  ∧ HASH_CORRESPONDENTE
  ∧ ESCOPO_DE_AUTORIDADE_PUBLICADO
  ∧ VIGENCIA_PUBLICADA
  ∧ PRECEDENCIA_RESOLVIDA
  ∧ REGISTRO_MESTRE_ATUALIZADO
  ∧ INVENTARIO_ATUALIZADO
  ∧ HISTORICO_PRESERVADO
  ∧ EVIDENCIAS_IMUTAVEIS
  ∧ REGRAS_DE_USO_POR_IA_PUBLICADAS
```

Checklist verificável:

- [ ] O documento possui ID, versão e hash únicos.
- [ ] O diretório e o nome físico cumprem a arquitetura normativa.
- [ ] O caminho corresponde ao `canonical_path` do registro mestre.
- [ ] O conteúdo e o escopo estão delimitados.
- [ ] As fontes e derivações são rastreáveis.
- [ ] Os contratos aplicáveis são válidos.
- [ ] Todos os gates anteriores retornaram `pass`.
- [ ] Não existe ação corretiva bloqueante aberta.
- [ ] A aprovação corresponde exatamente ao hash publicado.
- [ ] A autoridade aprovadora está autenticada e é competente.
- [ ] A promoção canônica foi autorizada e registrada.
- [ ] O escopo de autoridade está publicado.
- [ ] Os usos permitidos e proibidos estão publicados.
- [ ] A vigência e a revisão estão definidas.
- [ ] A precedência e as relações de substituição estão resolvidas.
- [ ] O repositório oficial contém a versão imutável.
- [ ] O registro mestre aponta `CANONICA_VIGENTE`.
- [ ] O inventário aponta a mesma versão e o mesmo estado.
- [ ] A versão anterior está preservada e corretamente classificada.
- [ ] O pacote de evidências permite reconstruir a execução.
- [ ] As instruções para agentes de IA distinguem vigente, histórico e derivado.

Se qualquer item obrigatório estiver ausente, o resultado é `NOT_DONE`.

## 15. Regras de consumo pelo agente de IA

O pacote canônico deve publicar instruções processáveis para o agente:

1. usar primeiro a fonte canônica cujo escopo cobre o assunto;
2. verificar `document_id`, versão, hash, vigência e escopo;
3. não tratar documento histórico, superado, revogado ou derivado como vigente;
4. aplicar a matriz de precedência diante de conflito;
5. sinalizar conflito não resolvido em vez de escolher silenciosamente;
6. distinguir fato, claim, hipótese, decisão e requisito;
7. não converter requisito derivado em requisito aprovado;
8. não inferir autorização de implementação, dados reais, piloto ou produção;
9. citar a versão canônica usada em toda derivação material;
10. interromper a ação quando o uso pretendido estiver proibido ou fora do
    escopo de autoridade.

## 16. Validadores automáticos

Implementar verificações para:

- arquivo localizado em diretório incompatível com seu tipo;
- nome físico fora da convenção;
- espaço, acento, sublinhado, travessão tipográfico ou caixa inválida no nome;
- versão, estado ou data indevidamente incorporados ao nome documental;
- colisões de caminho que diferem apenas por caixa;
- caminho não registrado ou registrado para mais de um `document_id`;
- divergência entre caminho físico e `canonical_path`;
- contratos inválidos;
- IDs duplicados;
- links quebrados;
- fontes inexistentes;
- claims sem fonte ou incerteza;
- requisitos sem origem;
- decisões sem autoridade;
- estados ou transições incompatíveis;
- referências circulares;
- ações bloqueantes abertas;
- alteração posterior à aprovação;
- hash diferente do artefato aprovado;
- item simultaneamente dentro e fora do escopo;
- linguagem normativa em requisito não aprovado;
- duas canônicas conflitantes no mesmo assunto, escopo e vigência;
- canônica sem aprovação ou promoção;
- aprovação e promoção referentes a hashes diferentes;
- registro mestre divergente do inventário;
- documento superado ainda indicado como vigente;
- data de vigência inválida ou revisão vencida;
- uso por IA incompatível com o escopo autorizado.

Executar os validadores localmente, na integração contínua e imediatamente antes
da promoção.

Garantia obtida: erros conhecidos são detectados antes de merge, aprovação ou
canonização.

## 17. Proteção de versões e evidências

Ações:

- versionar todos os artefatos no repositório;
- exigir revisão por pull request;
- proteger o branch principal;
- registrar o hash do documento candidato, aprovado e promovido;
- impedir edição direta de versão aprovada ou canônica;
- criar nova versão para qualquer alteração material;
- armazenar evidências com ID e controle de acesso;
- preservar base, candidata, canônica e histórico;
- usar tag, commit ou objeto equivalente como referência imutável;
- registrar e controlar exceções;
- impedir que a publicação substitua silenciosamente a versão anterior.

Garantia obtida: o conteúdo aprovado pode ser reconstruído e não é alterado
silenciosamente.

## 18. Testes negativos e de bypass

Testes obrigatórios:

- tentar registrar arquivo em diretório incompatível com seu tipo;
- tentar registrar nome com espaço, acento, caixa ou separador inválido;
- tentar usar versão ou estado no nome físico;
- tentar registrar dois documentos no mesmo caminho;
- tentar alterar um caminho sem transição ou migração registrada;
- tentar promover documento sem fonte;
- tentar aprovar documento sem versão ou hash;
- tentar canonizar sem aprovação;
- tentar canonizar com hash diferente do aprovado;
- tentar canonizar sem escopo de autoridade;
- tentar canonizar sem vigência;
- tentar canonizar sem regra de precedência;
- tentar manter duas canônicas conflitantes vigentes;
- tentar alterar uma versão canônica;
- tentar usar ator sem autoridade;
- tentar fechar gate sem evidência;
- tentar reintroduzir item fora de escopo;
- tentar converter hipótese em fato;
- tentar pular diretamente de rascunho para candidata;
- tentar pular de candidata para canônica;
- tentar aprovar a própria derivação sem revisão independente;
- tentar usar a canonização como autorização para implementação;
- tentar usar dado real antes dos gates do workflow posterior;
- tentar fazer o agente de IA priorizar versão superada.

Todos os testes devem demonstrar bloqueio e produzir evento auditável.

Garantia obtida: os controles são comprovados inclusive diante de tentativa de
bypass.

## 19. Observabilidade e auditoria

Registrar em cada evento:

- ID do evento;
- ator e identidade;
- papel exercido;
- data e hora;
- documento, versão e hash;
- estado anterior;
- estado posterior;
- resultado do gate;
- evidências;
- motivo;
- exceção, quando houver;
- ação de retorno;
- referência imutável.

Indicadores:

- gates bloqueados;
- ações corretivas pendentes;
- claims sem fonte;
- requisitos sem aprovação;
- tempo por estado;
- documentos alterados após aprovação;
- falhas de validação;
- tentativas de bypass;
- canônicas com revisão vencida;
- conflitos de precedência;
- divergências entre registro mestre e inventário.

Garantia obtida: o processo pode ser reconstruído, acompanhado e auditado.

## 20. Ordem de implementação

1. Normalizar nomenclatura, links e estados do acervo.
2. Delimitar os tipos e escopos dos documentos canônicos.
3. Aprovar a arquitetura e a convenção de nomes físicos.
4. Criar `docs/registry/registro-documentos.yaml`.
5. Criar `docs/governance/workflows/workflow-documentacao.md` e
   `docs/registry/workflow-documentacao.yaml`.
6. Criar `docs/governance/matrices/matriz-autoridade-documental.md`.
7. Criar as matrizes de precedência, rastreabilidade e uso.
8. Criar os contratos e schemas.
9. Implementar validadores de arquitetura, nomes, contratos e conteúdo.
10. Executar a migração controlada do acervo legado.
11. Implementar os gates documentais, `G-ARCH` e `G-CANON`.
12. Proteger versões e evidências no repositório.
13. Executar testes negativos e de bypass.
14. Implantar eventos, indicadores e auditoria.
15. Executar um ciclo documental completo em ambiente controlado.
16. Canonizar a primeira versão somente após `G-CANON = pass`.
17. Abrir separadamente o workflow de especificação e produto.

## 21. Entregáveis

### 21.1 Normativos

- `docs/governance/workflows/workflow-documentacao.md`;
- `docs/governance/policies/politica-arquitetura-documental.md`;
- `docs/governance/policies/politica-autoridade-documental.md`;
- `docs/governance/policies/politica-versionamento-documental.md`;
- `docs/governance/policies/politica-uso-ia-documental.md`.

### 21.2 Processáveis

- `docs/registry/workflow-documentacao.yaml`;
- `docs/registry/registro-documentos.yaml`;
- schemas listados na seção 11;
- regras automatizadas de gates;
- suíte de testes negativos.

### 21.3 Matrizes

- `docs/governance/matrices/matriz-autoridade-documental.md`;
- `docs/governance/matrices/matriz-precedencia-documental.md`;
- `docs/governance/matrices/matriz-rastreabilidade-documental.md`;
- `docs/governance/matrices/matriz-gates-evidencias.md`;
- `docs/governance/matrices/matriz-uso-ia-documental.md`.

### 21.4 Evidências operacionais

- resultados dos validadores;
- resultados dos gates;
- registro de aprovação;
- registro de promoção;
- registro canônico;
- pacote de evidências;
- trilha de auditoria;
- referência imutável da versão canônica.

## 22. Done da implantação do workflow

O workflow, como mecanismo operacional, somente está implantado quando:

- a estrutura de diretórios e os nomes físicos são validados automaticamente;
- os contratos rejeitam registros inválidos;
- a máquina de estados rejeita transições não autorizadas;
- as autoridades são verificadas;
- o `G-CANON` bloqueia promoção incompleta;
- versões aprovadas e canônicas são imutáveis;
- os testes negativos comprovam os bloqueios;
- eventos e evidências permitem auditoria;
- um ciclo completo termina corretamente em `CANONICA_VIGENTE`;
- uma alteração material comprovadamente inicia uma nova versão;
- uma substituição preserva a canônica anterior como `SUPERADA`;
- o workflow posterior não pode interpretar canonização como autorização de
  implementação ou produção.

Somente depois disso existe garantia processual verificável:

```text
Contrato válido
+ autoridade autenticada
+ evidência preservada
+ gate bloqueante
+ versão imutável
+ teste de bloqueio
+ trilha de auditoria
= garantia processual verificável
```

## 23. Limites das garantias

O `Done` canônico documental garante, dentro do escopo declarado:

- identidade;
- autoridade;
- aprovação;
- integridade;
- proveniência;
- rastreabilidade;
- vigência;
- precedência;
- preservação histórica;
- referência operacional inequívoca.

Não garante automaticamente:

- verdade absoluta;
- ausência de erro factual;
- atualização permanente;
- conformidade jurídica integral;
- qualidade da implementação;
- requisitos aprovados para desenvolvimento;
- autorização de implementação;
- autorização de dados reais;
- autorização de piloto;
- autorização de produção;
- resultado esportivo ou operacional.

## 24. Estado da implementação

Estado registrado em 25 de julho de 2026:

| Componente | Estado | Evidência |
| --- | --- | --- |
| Arquitetura de `docs/` | Implementada parcialmente | Política e diretórios ativos |
| Registro mestre | Implementado | `docs/registry/registro-documentos.yaml` |
| Máquina de estados | Implementada em versão `0.1.0` | Markdown e YAML processável |
| Contratos | Implementados em versão inicial | Treze contratos operacionais e schema do workflow |
| `G-ARCH` | Implementado, bloqueante e aprovado | Código `0`, `status: pass` após migração |
| Migração do legado | Concluída | Dez artefatos movidos e referências atualizadas |
| `G0` a `G8` | Planejados | Sem executores completos |
| `G-CANON` | Planejado | Não executado |
| Documento canônico | Inexistente | `canonical_documents: []` |

O bloqueio inicial de `G-ARCH` comprovou a rejeição dos vinte desvios legados.
Após a migração controlada, a nova execução retornou `pass`. Esse resultado
satisfaz somente o gate de arquitetura; os demais gates continuam obrigatórios
para qualquer promoção documental.
