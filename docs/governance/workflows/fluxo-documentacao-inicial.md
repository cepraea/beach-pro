---
document_id: DOC-GOV-FLUXO-INICIAL
title: "Fluxo de criação da documentação inicial"
document_type: fluxo
version: "0.1.1-ingestao"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - orientacao
  - rastreabilidade
prohibited_uses:
  - execucao_automatica
  - canonizacao
---

# FLUXO DE CRIAÇÃO DA DOCUMENTAÇÃO — CEPRAEA BEACH PRO

- [FLUXO DE CRIAÇÃO DA DOCUMENTAÇÃO — CEPRAEA BEACH PRO](#fluxo-de-criação-da-documentação--cepraea-beach-pro)
  - [1. Resposta executiva](#1-resposta-executiva)
  - [2. Método e limites da reconstrução](#2-método-e-limites-da-reconstrução)
    - [2.1 Evidências utilizadas](#21-evidências-utilizadas)
    - [2.2 Limites](#22-limites)
  - [3. Arquivos iniciais](#3-arquivos-iniciais)
    - [3.1 Raiz factual — `DESCRICAO-CEPRAEA.md`](#31-raiz-factual--descricao-cepraeamd)
    - [3.2 Raiz normativa — `CONTEUDO DESC-CEPRAEA.md`](#32-raiz-normativa--conteudo-desc-cepraeamd)
    - [3.3 Raiz metodológica — `PROTOCOLO-QUALIDADE-DOC.md`](#33-raiz-metodológica--protocolo-qualidade-docmd)
  - [4. Relação entre os arquivos](#4-relação-entre-os-arquivos)
    - [4.1 Relações comprovadas](#41-relações-comprovadas)
      - [Conteúdo obrigatório](#conteúdo-obrigatório)
      - [Objeto da validação](#objeto-da-validação)
      - [Origem dos requisitos](#origem-dos-requisitos)
      - [Promoção](#promoção)
      - [Inventário](#inventário)
  - [5. Fases do fluxo](#5-fases-do-fluxo)
    - [Fase 0 — Descoberta factual](#fase-0--descoberta-factual)
    - [Fase 1 — Definição do conteúdo obrigatório](#fase-1--definição-do-conteúdo-obrigatório)
    - [Fase 2 — Consolidação controlada](#fase-2--consolidação-controlada)
    - [Fase 3 — Preparação da validação](#fase-3--preparação-da-validação)
    - [Fase 4 — Validação e remediação V0](#fase-4--validação-e-remediação-v0)
    - [Fase 5 — Derivação independente](#fase-5--derivação-independente)
    - [Fase 6 — Aprovação e promoção documental](#fase-6--aprovação-e-promoção-documental)
    - [Fase 7 — Inventário e orientação](#fase-7--inventário-e-orientação)
    - [Próxima fase declarada](#próxima-fase-declarada)
  - [6. Procedimento correto para repetir o fluxo](#6-procedimento-correto-para-repetir-o-fluxo)
    - [Passo 1 — Registrar o objeto e as fontes](#passo-1--registrar-o-objeto-e-as-fontes)
    - [Passo 2 — Classificar cada afirmação](#passo-2--classificar-cada-afirmação)
    - [Passo 3 — Documentar o `AS-IS`](#passo-3--documentar-o-as-is)
    - [Passo 4 — Separar problema, necessidade e solução](#passo-4--separar-problema-necessidade-e-solução)
    - [Passo 5 — Definir atores e autoridade](#passo-5--definir-atores-e-autoridade)
    - [Passo 6 — Construir a base controlada](#passo-6--construir-a-base-controlada)
    - [Passo 7 — Aplicar o protocolo](#passo-7--aplicar-o-protocolo)
    - [Passo 8 — Tratar achados](#passo-8--tratar-achados)
    - [Passo 9 — Executar derivação independente](#passo-9--executar-derivação-independente)
    - [Passo 10 — Registrar aprovação](#passo-10--registrar-aprovação)
    - [Passo 11 — Promover sem sobrescrever](#passo-11--promover-sem-sobrescrever)
    - [Passo 12 — Atualizar inventário e fluxo](#passo-12--atualizar-inventário-e-fluxo)
  - [7. Regras para uso correto por agentes de IA](#7-regras-para-uso-correto-por-agentes-de-ia)
    - [7.1 Ordem recomendada de leitura](#71-ordem-recomendada-de-leitura)
    - [7.2 Precedência por assunto](#72-precedência-por-assunto)
    - [7.3 Ações obrigatórias](#73-ações-obrigatórias)
    - [7.4 Ações que exigem confirmação](#74-ações-que-exigem-confirmação)
    - [7.5 Ações proibidas](#75-ações-proibidas)
  - [8. Informação mínima necessária em cada fase](#8-informação-mínima-necessária-em-cada-fase)
  - [9. Gates do fluxo](#9-gates-do-fluxo)
  - [10. Relação de precedência e substituição](#10-relação-de-precedência-e-substituição)
    - [10.1 Precedência documental recomendada](#101-precedência-documental-recomendada)
    - [10.2 Substituição](#102-substituição)
  - [11. Inconsistências que afetam a execução](#11-inconsistências-que-afetam-a-execução)
    - [11.1 Nomenclatura `DESC`, `DESCRICAO` e `DECISAO`](#111-nomenclatura-desc-descricao-e-decisao)
    - [11.2 Estados pré-promoção na candidata](#112-estados-pré-promoção-na-candidata)
    - [11.3 Estados inconsistentes na validação](#113-estados-inconsistentes-na-validação)
    - [11.4 Link incorreto no inventário](#114-link-incorreto-no-inventário)
    - [11.5 Metadados incompletos](#115-metadados-incompletos)
  - [12. Checklist operacional](#12-checklist-operacional)
    - [Antes de criar ou editar](#antes-de-criar-ou-editar)
    - [Durante a edição](#durante-a-edição)
    - [Antes da validação](#antes-da-validação)
    - [Antes da promoção](#antes-da-promoção)
    - [Antes de uso por IA](#antes-de-uso-por-ia)
  - [13. Conclusão](#13-conclusão)
    - [13.1 Arquivos que deram origem ao fluxo](#131-arquivos-que-deram-origem-ao-fluxo)
    - [13.2 Primeira consolidação](#132-primeira-consolidação)
    - [13.3 Fluxo confirmado](#133-fluxo-confirmado)
    - [13.4 Estado atual documentado](#134-estado-atual-documentado)
    - [13.5 Regra final para agentes](#135-regra-final-para-agentes)

## 1. Resposta executiva

É possível identificar o fluxo lógico de criação e edição da documentação
inicial do CEPRAEA BEACH PRO.

Não é possível comprovar, somente pelos metadados internos, qual foi o primeiro
arquivo criado cronologicamente. É possível, porém, identificar três raízes
funcionais:

| Raiz | Arquivo | Contribuição |
| --- | --- | --- |
| Factual e operacional | `DESCRICAO-CEPRAEA.md` | Descreve o CEPRAEA, as planilhas, o domínio e os problemas observados |
| Normativa de conteúdo | `CONTEUDO DESC-CEPRAEA.md` | Define o que o documento de contexto deve conter e como deve ser interpretado |
| Metodológica de qualidade | `PROTOCOLO-QUALIDADE-DOC.md` | Define critérios, métodos, estados e regra de aprovação |

A primeira convergência dessas contribuições é:

> `DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md`

A partir dela ocorreram:

1. validação pelo protocolo;
2. correções `AR-001` a `AR-015`;
3. derivação independente dos requisitos;
4. autorização humana;
5. promoção para versão candidata;
6. inventário retrospectivo do acervo.

O fluxo consolidado é:

```text
DESCRICAO-CEPRAEA.md ───────────────┐
                                    │
CONTEUDO DESC-CEPRAEA.md ───────────┼─→ BASE CONTROLADA v0.1
                                    │             │
Fontes humanas, planilhas e         │             │
documentos oficiais ────────────────┘             │
                                                  ├─→ VALIDACAO-CEPRAEA-v0.1.md
PROTOCOLO-QUALIDADE-DOC.md ───────────────────────┘             │
                                                                │
BASE CONTROLADA v0.1 ──→ RF-CEPRAEA-v0.1.md ←─ AR-012 ─────────┤
                                                                │
BASE + validação + derivação + aprovação de Davi ───────────────┘
                                │
                                ▼
              VERSÃO CANDIDATA 0.1
                                │
                                ▼
                     V1 — testes sintéticos

Todos os artefatos ──→ INVENTARIO-DOCS.md
```

## 2. Método e limites da reconstrução

### 2.1 Evidências utilizadas

A relação foi reconstruída por meio de:

- declarações de finalidade;
- campos `Documento-fonte`;
- registros de governança;
- identificadores `SRC-*`, `DEC-*`, `AR-*` e `RF-*`;
- registro de promoção;
- matriz de rastreabilidade;
- estados documentais;
- referências explícitas entre arquivos.

### 2.2 Limites

Os horários de modificação do sistema de arquivos não provam a ordem original de
criação, pois os documentos foram editados posteriormente.

Também não existe nos três arquivos-raiz um histórico comum com:

- data original de criação;
- identificador da primeira revisão;
- relação formal `derivado_de`;
- hash da versão utilizada;
- autor de cada transformação.

Assim:

- a **ordem lógica** é verificável;
- a **ordem de promoção em 2026-07-24** é verificável;
- a **ordem cronológica absoluta dos arquivos iniciais** permanece não
  comprovada.

## 3. Arquivos iniciais

### 3.1 Raiz factual — `DESCRICAO-CEPRAEA.md`

O arquivo [DESCRICAO-CEPRAEA.md](../../sources/primary/contexto-operacional-cepraea.md:1)
é a raiz factual e operacional do fluxo.

Ele fornece:

- definição operacional do CEPRAEA;
- composição humana;
- responsabilidades;
- ambiente de planilhas;
- arquitetura da informação;
- modelo conceitual;
- estado observado em 23 de julho de 2026;
- inconsistências;
- estado desejado;
- prioridades de correção;
- fontes consultadas.

Sua finalidade declarada é descrever o CEPRAEA, o contexto operacional e o
sistema de informação da temporada de 2026
([identificação](../../sources/primary/contexto-operacional-cepraea.md:60)).

Esse arquivo não deve ser usado como fonte de estado atual sem revalidação,
porque contém uma auditoria datada.

### 3.2 Raiz normativa — `CONTEUDO DESC-CEPRAEA.md`

O arquivo [CONTEUDO DESC-CEPRAEA.md](../../sources/supporting/diretriz-conteudo-contexto-cepraea.md:1)
é a raiz normativa do conteúdo.

Ele determina que o documento canônico deve:

- descrever a realidade do CEPRAEA;
- descrever a operação atual por planilhas;
- identificar atores e autoridades;
- registrar dados, processos e problemas;
- separar capacidades atuais de requisitos futuros;
- descrever `AS-IS` e necessidades `TO-BE`;
- preservar restrições e desconhecidos;
- permitir derivação documental posterior.

Ele também separa quatro objetos:

1. CEPRAEA;
2. planilhas atuais;
3. documento canônico de contexto;
4. PWA futura ([finalidade](../../sources/supporting/diretriz-conteudo-contexto-cepraea.md:27)).

Sua regra principal é:

> Objetivos, funcionalidades e soluções das planilhas não podem ser convertidos
> diretamente em requisitos da PWA.

### 3.3 Raiz metodológica — `PROTOCOLO-QUALIDADE-DOC.md`

O arquivo
[PROTOCOLO-QUALIDADE-DOC.md](../protocols/protocolo-qualidade-documental.md:1)
é a raiz metodológica de qualidade.

Ele define:

- 16 fatores críticos de sucesso;
- critérios `PA-*`;
- métodos de validação;
- evidências mínimas;
- validações transversais;
- seis estados de avaliação;
- registro mínimo;
- dez condições finais de aprovação.

O protocolo não produz conteúdo do CEPRAEA. Ele define como julgar se esse
conteúdo é confiável, completo, rastreável e executável
([finalidade](../protocols/protocolo-qualidade-documental.md:137)).

## 4. Relação entre os arquivos

| Arquivo | Recebe de | Entrega para | Tipo de relação |
| --- | --- | --- | --- |
| `DESCRICAO-CEPRAEA.md` | Planilhas, documentos e auditoria | Base controlada | Evidência e contexto operacional |
| `CONTEUDO DESC-CEPRAEA.md` | Necessidade de estruturar o contexto | Base controlada | Regras de conteúdo e interpretação |
| `PROTOCOLO-QUALIDADE-DOC.md` | Princípios de qualidade | Validação | Critérios e método |
| Base controlada v0.1 | Conteúdo, contexto, fontes e decisões | Validação e RF | Primeira consolidação controlada |
| `VALIDACAO-CEPRAEA-v0.1.md` | Base + protocolo + autoridade | Correções e promoção | Auditoria, gates e aprovação |
| `RF-CEPRAEA-v0.1.md` | Base controlada | Validação e promoção | Prova de executabilidade e derivação |
| Versão candidata 0.1 | Base corrigida + validação + RF + aprovação | V1 sintética | Documento promovido e canônico |
| `INVENTARIO-DOCS.md` | Todos os arquivos | Leitores e agentes | Catálogo analítico retrospectivo |

### 4.1 Relações comprovadas

#### Conteúdo obrigatório

A base controlada declara que o arquivo de conteúdo define o conteúdo
obrigatório. A nomenclatura interna foi alterada para `CONTEUDO
DECISAO-CEPRAEA.md`, mas o arquivo físico existente é `CONTEUDO
DESC-CEPRAEA.md`.

#### Objeto da validação

O registro de validação identifica explicitamente:

- documento avaliado: base controlada v0.1;
- protocolo aplicado: `PROTOCOLO-QUALIDADE-DOC.md`
  ([identificação](../../validation/reports/relatorio-validacao-contexto-cepraea.md:30)).

#### Origem dos requisitos

O catálogo RF identifica explicitamente a base controlada como
`Documento-fonte` e a derivação `DERIVACAO_INDEPENDENTE_V0`
([nota de derivação](../../derived/requirements/requisitos-funcionais-cepraea.md:5)).

#### Promoção

A versão candidata declara:

- origem na base controlada;
- resolução de `AR-001` a `AR-015`;
- validação formal;
- autorização de Davi;
- preservação da base como registro histórico
  ([contexto documental](../../canonical/context/contexto-cepraea-beach-pro.md:115)).

#### Inventário

O inventário reúne análises secundárias de todos os artefatos. Ele não participa
da aprovação original e não substitui as fontes.

## 5. Fases do fluxo

### Fase 0 — Descoberta factual

**Entrada:**

- planilhas;
- banco estruturado;
- documentos oficiais;
- declarações humanas;
- materiais técnicos;
- registros históricos.

**Atividade:**

- ler;
- auditar;
- comparar;
- identificar o domínio;
- registrar fatos datados;
- detectar contradições.

**Saída principal:**

- `DESCRICAO-CEPRAEA.md`.

**Gate:**

- fatos com fonte;
- data de observação;
- distinção entre entidade real e sistema de informação.

### Fase 1 — Definição do conteúdo obrigatório

**Entrada:**

- necessidade de transformar a descoberta em contexto de produto.

**Atividade:**

- definir as seções necessárias;
- separar os quatro objetos;
- definir o que a IA deve aprender;
- separar capacidades, necessidades, hipóteses e requisitos;
- definir estados de incerteza.

**Saída principal:**

- `CONTEUDO DESC-CEPRAEA.md`.

**Gate:**

- nenhuma observação ou solução é promovida automaticamente a requisito.

### Fase 2 — Consolidação controlada

**Entrada:**

- descoberta factual;
- estrutura obrigatória;
- fontes humanas e documentais;
- decisões de Davi.

**Atividade:**

- consolidar identidade;
- formular problema;
- mapear atores;
- descrever `AS-IS`;
- classificar capacidades;
- definir objetivos;
- delimitar escopo;
- construir domínio;
- registrar restrições;
- controlar decisões, claims e fontes.

**Saída principal:**

- `DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md`.

**Gate:**

- todo conteúdo confirmado ou explicitamente classificado;
- desconhecidos preservados;
- contradições registradas;
- autoridade identificada;
- conteúdo ainda marcado como base, não especificação.

### Fase 3 — Preparação da validação

**Entrada:**

- princípios de qualidade documental.

**Atividade:**

- converter princípios em critérios;
- definir métodos;
- definir evidências;
- estabelecer estados;
- definir regra final de aprovação.

**Saída principal:**

- `PROTOCOLO-QUALIDADE-DOC.md`.

**Gate:**

- critérios verificáveis e aplicáveis por seção e ao documento completo.

Essa fase pertence à trilha metodológica e pode ocorrer antes ou em paralelo às
fases 0 a 2. O acervo não comprova sua posição cronológica absoluta.

### Fase 4 — Validação e remediação V0

**Entrada:**

- base controlada;
- protocolo;
- fontes e decisões;
- autoridade de Davi.

**Atividade:**

- avaliar critérios `PA-*`;
- atribuir estados;
- registrar achados;
- executar validações transversais;
- criar ações `AR-001` a `AR-015`;
- corrigir a base;
- registrar evidências de conclusão.

**Saída principal:**

- `VALIDACAO-CEPRAEA-v0.1.md`;
- base controlada corrigida.

**Gate:**

- ações bloqueantes concluídas;
- ausência de contradição material;
- aprovação formal;
- executabilidade comprovada.

### Fase 5 — Derivação independente

**Entrada:**

- base controlada;
- critérios `CRIT-FASE1-*`;
- decisões, capacidades, regras e objetivos.

**Atividade:**

- derivar comportamentos funcionais;
- atribuir ID;
- registrar origem;
- agrupar por domínio;
- separar fases posteriores;
- preservar exclusões;
- verificar cobertura.

**Saída principal:**

- `RF-CEPRAEA-v0.1.md`;
- 53 RFs da primeira fase;
- 4 RFs posteriores.

**Gate:**

- cada RF com origem;
- 16 critérios cobertos;
- nenhuma inferência não controlada;
- nenhuma exclusão reintroduzida.

Essa fase atende à ação `AR-012` e comprova a executabilidade exigida pelo
protocolo. O RF continua sendo insumo, não especificação aprovada.

### Fase 6 — Aprovação e promoção documental

**Entrada:**

- base corrigida;
- validação;
- derivação independente;
- `approval_record`;
- autorização de Davi.

**Atividade:**

- confirmar conclusão das ações;
- registrar versão, data, escopo e ressalvas;
- preservar a base histórica;
- criar o documento promovido;
- definir próxima etapa.

**Saída principal:**

- `DESCRICAO-CEPRAEA — VERSÃO CANDIDATA 0.1.md`.

**Gate:**

- promoção autorizada por Davi;
- status `VERSAO_CANDIDATA`;
- dados reais, D0, piloto e produção ainda bloqueados.

### Fase 7 — Inventário e orientação

**Entrada:**

- todos os artefatos anteriores.

**Atividade:**

- analisar;
- classificar;
- relacionar;
- registrar limites;
- facilitar navegação.

**Saída principal:**

- `INVENTARIO-DOCS.md`;
- este `FLUXO-DOCS.md`.

**Gate:**

- não substituir as fontes;
- não converter síntese em autoridade;
- manter links e estados atualizados.

### Próxima fase declarada

A próxima fase declarada pela versão candidata é:

> V1 — testes sintéticos conforme `DEC-018`.

Ela não foi executada pelos arquivos analisados.

## 6. Procedimento correto para repetir o fluxo

### Passo 1 — Registrar o objeto e as fontes

Criar um registro mínimo para cada fonte:

```yaml
source:
  id: SRC-000
  name: ""
  type: ""
  authority_for: []
  location: ""
  observed_at: "AAAA-MM-DD"
  version_or_hash: ""
  limitations: []
```

Não iniciar a consolidação sem distinguir:

- pessoa;
- organização;
- sistema atual;
- documento;
- produto futuro.

### Passo 2 — Classificar cada afirmação

Usar estados controlados:

- `CONFIRMADO_HUMANO`;
- `CONFIRMADO_FONTE`;
- `ESTADO_TEMPORAL`;
- `PROBLEMA_OBSERVADO`;
- `INFERENCIA_CONTROLADA`;
- `NECESSIDADE_CANDIDATA`;
- `DECISAO_PENDENTE`;
- `CONTRADITORIO`;
- `DESCONHECIDO`;
- `FORA_DE_ESCOPO`.

Uma lacuna nunca deve ser preenchida silenciosamente.

### Passo 3 — Documentar o `AS-IS`

Registrar:

- processos;
- pessoas;
- entradas;
- transformações;
- saídas;
- ferramentas;
- dados;
- dependências;
- falhas;
- evidências;
- data de observação.

Problema estrutural e evidência datada devem permanecer distintos.

### Passo 4 — Separar problema, necessidade e solução

Usar a cadeia:

```text
Fato ou evidência
→ causa
→ problema
→ consequência
→ necessidade
→ objetivo
→ decisão
→ requisito candidato
→ requisito aprovado
```

Não inverter a cadeia começando por uma tecnologia.

### Passo 5 — Definir atores e autoridade

Para cada informação, registrar:

- quem declara;
- quem valida;
- quem decide;
- quem pode alterar;
- qual fonte prevalece;
- quem é afetado.

No CEPRAEA:

| Informação | Autoridade |
| --- | --- |
| Disponibilidade e justificativa pessoal | A própria atleta |
| Elenco, planejamento, convocação e decisão tática | Davi |
| Calendário e resultado oficial | Documento oficial e validação aplicável |
| Participação e fatos internos | Registro validado por Davi |
| Aprovação do contexto e promoção | Davi |
| Método de qualidade | Protocolo |

### Passo 6 — Construir a base controlada

A base deve conter, no mínimo:

- identidade;
- problema;
- pessoas e atores;
- ambiente;
- objetivos;
- resultados;
- escopo;
- fora de escopo;
- domínio;
- restrições;
- pergunta central;
- fontes;
- claims;
- decisões;
- desconhecidos;
- contradições;
- rastreabilidade.

### Passo 7 — Aplicar o protocolo

Avaliar:

1. identidade;
2. problema;
3. pessoas;
4. ambiente;
5. objetivos;
6. resultados;
7. escopo;
8. domínio;
9. restrições;
10. pergunta central.

Depois executar:

- rastreabilidade;
- revisão de afirmações;
- executabilidade;
- consistência;
- viabilidade;
- validação por autoridade.

### Passo 8 — Tratar achados

Cada achado deve gerar:

```yaml
action:
  id: AR-000
  source_criterion: ""
  description: ""
  criticality: ""
  status: pending
  evidence_of_completion: ""
  completed_at: ""
  approved_by: ""
```

Não promover enquanto existir ação bloqueante aberta.

### Passo 9 — Executar derivação independente

Um revisor ou agente sem contexto anterior deve:

- derivar requisitos apenas da base;
- registrar origem por item;
- marcar informação ausente;
- excluir itens fora de escopo;
- separar fases;
- relatar qualquer invenção necessária.

Se for necessário inventar informação crítica, a base retorna à remediação.

### Passo 10 — Registrar aprovação

O registro mínimo deve conter:

```yaml
approval_record:
  item_id: ""
  document_version: ""
  status: ""
  approved_by: ""
  approval_date: "AAAA-MM-DD"
  scope_approved: ""
  reservations: []
  next_action: ""
```

### Passo 11 — Promover sem sobrescrever

- preservar a base;
- criar versão candidata distinta;
- registrar `derivado_de`;
- registrar data e autoridade;
- registrar o que a promoção não autoriza;
- atualizar a próxima ação;
- substituir todos os estados pré-promoção obsoletos.

### Passo 12 — Atualizar inventário e fluxo

- marcar arquivo como avaliado;
- verificar links;
- registrar estado atual;
- registrar relação `substitui/substituído por`;
- atualizar precedência;
- preservar a análise histórica;
- registrar nova data e hash.

## 7. Regras para uso correto por agentes de IA

### 7.1 Ordem recomendada de leitura

1. `FLUXO-DOCS.md` — orientação sobre proveniência e uso.
2. Versão candidata 0.1 — contexto promovido atual.
3. `CONTEUDO DESC-CEPRAEA.md` — regras sobre o conteúdo obrigatório.
4. `PROTOCOLO-QUALIDADE-DOC.md` — critérios de qualidade.
5. `VALIDACAO-CEPRAEA-v0.1.md` — evidência da validação e ressalvas.
6. `RF-CEPRAEA-v0.1.md` — derivação funcional preliminar.
7. Base controlada v0.1 — registro histórico anterior à promoção.
8. `DESCRICAO-CEPRAEA.md` — auditoria operacional datada.
9. `INVENTARIO-DOCS.md` — síntese secundária e navegação.

Essa ordem não significa que `FLUXO-DOCS.md` ou o inventário tenham autoridade
sobre fatos do produto. Eles orientam qual fonte consultar.

### 7.2 Precedência por assunto

| Assunto | Fonte preferencial | Limite |
| --- | --- | --- |
| Contexto promovido do produto | Versão candidata | Corrigir mentalmente ou confirmar resíduos pré-promoção |
| Decisão esportiva | Davi e decisão registrada | Nunca automatizar |
| Declaração de atleta | Registro da própria atleta | Nunca inferir ou sobrescrever |
| Calendário e resultado oficial | Documento oficial aplicável | Exigir vigência e validação |
| Conteúdo obrigatório da documentação | `CONTEUDO DESC-CEPRAEA.md` | Resolver nomenclatura `DESC/DECISAO` |
| Critério de qualidade | `PROTOCOLO-QUALIDADE-DOC.md` | Protocolo não aprova sozinho |
| Estado da validação | Validação + `approval_record` da candidata | Há resíduos contraditórios no resumo |
| Requisitos funcionais | RF + origem na candidata/base | RF não está aprovado para implementação |
| Estado operacional histórico | `DESCRICAO-CEPRAEA.md` | Revalidar fatos datados |
| Navegação | Inventário | Fonte secundária |

### 7.3 Ações obrigatórias

O agente deve:

- citar fonte, seção e data;
- preservar autoria humana;
- distinguir estado vigente de histórico;
- verificar o assunto antes de escolher a fonte;
- usar somente transformações determinísticas sem nova decisão;
- manter rastreabilidade;
- registrar alterações;
- marcar desconhecidos;
- solicitar decisão quando a autoridade não estiver documentada;
- manter escopo da primeira fase separado das fases posteriores.

### 7.4 Ações que exigem confirmação

O agente deve confirmar com Davi antes de:

- criar ou alterar decisão de produto;
- promover documento;
- aprovar requisito;
- alterar escopo;
- alterar estado de atleta;
- sobrescrever dado humano;
- publicar dado pessoal;
- iniciar D0;
- usar dados reais;
- executar piloto;
- autorizar produção.

### 7.5 Ações proibidas

O agente nunca deve:

- inventar fatos;
- resolver contradição por preferência própria;
- transformar hipótese em decisão;
- transformar RF derivado em requisito aprovado;
- tratar disponibilidade como presença;
- tratar convocação como participação;
- tratar previsão como fato;
- atribuir decisão esportiva à IA;
- expor justificativas;
- enviar dados reais a ferramentas externas de IA;
- usar informação datada como atual sem revalidação;
- considerar promoção documental como autorização operacional.

## 8. Informação mínima necessária em cada fase

| Fase | Informação obrigatória |
| --- | --- |
| Descoberta | Fonte, autoridade, data, fato, limitação |
| Conteúdo | Objeto, seção exigida, estado e regra de interpretação |
| Consolidação | Problema, ator, objetivo, escopo, domínio, decisão e evidência |
| Validação | Critério, método, evidência, achado, limitação e ação |
| Remediação | ID, criticidade, estado e prova de conclusão |
| Derivação | ID do requisito, descrição, origem, fase e exclusão aplicável |
| Aprovação | Versão, data, escopo, ressalvas, autoridade e próxima ação |
| Promoção | Origem, destino, data, substituição, preservação e gates |
| Inventário | Caminho, tipo, estado, precedência, data e relação |

## 9. Gates do fluxo

| Gate | Condição de passagem | Bloqueio |
| --- | --- | --- |
| `G0 — Evidência` | Fontes e autoridades identificadas | Fato sem origem |
| `G1 — Conteúdo` | Seções obrigatórias completas | Lacuna crítica |
| `G2 — Semântica` | Conceitos distintos e estáveis | Ambiguidade |
| `G3 — Escopo` | Inclusões, exclusões e fases explícitas | Expansão implícita |
| `G4 — Qualidade` | Critérios locais avaliados | Seção reprovada |
| `G5 — Transversal` | Rastreabilidade, consistência e viabilidade | Contradição bloqueante |
| `G6 — Executabilidade` | Derivação sem invenção | RF sem origem |
| `G7 — Autoridade` | Aprovação formal de Davi | Decisão ausente |
| `G8 — Promoção` | Base preservada e candidata criada | Sobrescrita ou estado obsoleto |
| `G9 — Uso real` | Portões jurídicos, técnicos e humanos | Dados reais, piloto ou produção |

## 10. Relação de precedência e substituição

### 10.1 Precedência documental recomendada

```text
Decisão humana ou fonte oficial aplicável
        ↓
Versão candidata vigente
        ↓
Base controlada histórica
        ↓
Descrição operacional datada
        ↓
Inventário e análises secundárias
```

O protocolo, o conteúdo obrigatório e a validação governam dimensões
específicas; eles não competem com a fonte esportiva no mesmo assunto.

### 10.2 Substituição

| Documento | Estado na relação |
| --- | --- |
| Base controlada v0.1 | Preservada como histórico |
| Versão candidata 0.1 | Substitui a base como contexto promovido |
| RF v0.1 | Deriva da base; não a substitui |
| Validação | Valida e registra promoção; não substitui o contexto |
| Inventário | Resume; não substitui nenhum documento |

## 11. Inconsistências que afetam a execução

### 11.1 Nomenclatura `DESC`, `DESCRICAO` e `DECISAO`

O acervo usa:

- `CONTEUDO DESC-CEPRAEA.md` como nome físico;
- `DECISAO-CEPRAEA.md` no conteúdo interno;
- `DESCRICAO-CEPRAEA — ...` nos nomes físicos da base e da candidata;
- `DECISAO-CEPRAEA — ...` nos títulos internos.

**Risco:** links quebrados e escolha do artefato errado.

**Correção necessária:** escolher um nome canônico e registrar aliases e
renomeações.

### 11.2 Estados pré-promoção na candidata

A versão candidata ainda contém:

- `PENDENTE_DE_PROMOÇÃO`;
- texto dizendo que a base ainda precisa ser promovida;
- resultado V0 anterior à promoção.

O cabeçalho, o `approval_record` e `PROMOCAO_PARA_CANDIDATA_0.1` confirmam que a
promoção foi concluída.

**Risco:** agente interromper ou repetir uma promoção já concluída.

**Correção necessária:** atualizar todos os estados para o momento
pós-promoção.

### 11.3 Estados inconsistentes na validação

O registro de validação declara promoção concluída, mas conserva:

- frase indicando `AR-012` pendente;
- resumo com pendências anteriores;
- estado global `Aprovado com ressalvas`.

**Risco:** interpretação divergente sobre o gate de promoção.

**Correção necessária:** recalcular e sincronizar o resumo final.

### 11.4 Link incorreto no inventário

O inventário contém uma seção e um link para `CONTEUDO DECISAO-CEPRAEA.md`, que
não existe. O arquivo físico é `CONTEUDO DESC-CEPRAEA.md`.

**Risco:** agente não localizar a regra de conteúdo.

**Correção necessária:** corrigir o link e manter `DECISAO-CEPRAEA.md` somente
como alias, caso seja formalmente aprovado.

### 11.5 Metadados incompletos

Faltam, em alguns artefatos:

- versão controlada;
- data;
- responsável;
- hash da fonte;
- relação formal de derivação.

**Risco:** reconstrução histórica imprecisa.

**Correção necessária:** adotar front matter ou bloco de metadados comum.

## 12. Checklist operacional

### Antes de criar ou editar

- [ ] Identificar o documento e sua função.
- [ ] Confirmar a fonte canônica por assunto.
- [ ] Registrar versão ou hash.
- [ ] Registrar data da observação.
- [ ] Confirmar autoridade.
- [ ] Identificar o estado documental.

### Durante a edição

- [ ] Preservar fatos, decisões e desconhecidos.
- [ ] Separar `AS-IS` e `TO-BE`.
- [ ] Manter problema, necessidade e solução distintos.
- [ ] Registrar origem de novas afirmações.
- [ ] Não expandir escopo silenciosamente.
- [ ] Não alterar dado humano como se fosse do autor original.
- [ ] Atualizar links e rastreabilidade.

### Antes da validação

- [ ] Responder à pergunta central.
- [ ] Completar seções obrigatórias.
- [ ] Definir domínio e vocabulário.
- [ ] Identificar restrições.
- [ ] Construir matriz de rastreabilidade.
- [ ] Registrar contradições e pendências.

### Antes da promoção

- [ ] Concluir ações bloqueantes.
- [ ] Executar derivação independente.
- [ ] Confirmar ausência de fatos inventados.
- [ ] Obter aprovação formal.
- [ ] Preservar documento-base.
- [ ] Criar versão candidata distinta.
- [ ] Remover estados obsoletos.
- [ ] Registrar o que a promoção não autoriza.

### Antes de uso por IA

- [ ] Informar a ordem de leitura.
- [ ] Informar precedência por assunto.
- [ ] Informar limites de autoridade.
- [ ] Informar dados proibidos.
- [ ] Informar gates ainda fechados.
- [ ] Confirmar que links existem.
- [ ] Confirmar que o estado é vigente.

## 13. Conclusão

### 13.1 Arquivos que deram origem ao fluxo

Não existe evidência suficiente para nomear um único primeiro arquivo
cronológico.

Os arquivos iniciais por função são:

1. `DESCRICAO-CEPRAEA.md` — raiz factual;
2. `CONTEUDO DESC-CEPRAEA.md` — raiz normativa;
3. `PROTOCOLO-QUALIDADE-DOC.md` — raiz metodológica.

### 13.2 Primeira consolidação

A primeira consolidação integral identificável é:

> `DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md`

### 13.3 Fluxo confirmado

```text
Descoberta factual
→ regra de conteúdo
→ base controlada
→ validação
→ remediação
→ derivação independente
→ aprovação humana
→ versão candidata
→ V1 sintética
```

O protocolo forma uma trilha metodológica que alimenta a validação. O inventário
e este documento formam uma trilha posterior de orientação e governança do
acervo.

### 13.4 Estado atual documentado

- V0 documental: concluída;
- derivação independente: concluída;
- promoção para candidata 0.1: concluída;
- próxima etapa declarada: V1 sintética;
- D0: não iniciado;
- dados reais: não autorizados;
- piloto: não autorizado;
- produção: não autorizada.

### 13.5 Regra final para agentes

> O agente deve usar a versão candidata como contexto promovido, consultar as
> fontes especializadas conforme o assunto, tratar o RF como derivação ainda não
> aprovada, preservar autoridade humana e nunca interpretar promoção documental
> como autorização para implementação ou operação real.
