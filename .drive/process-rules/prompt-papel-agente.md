# Convenções de estrutura de prompt de agente

- [Convenções de estrutura de prompt de agente](#convenções-de-estrutura-de-prompt-de-agente)
  - [1. Princípios de design](#1-princípios-de-design)
  - [2. Estrutura das seções](#2-estrutura-das-seções)
  - [3. Definição de cada seção](#3-definição-de-cada-seção)
    - [3.0 S0: Frontmatter em YAML](#30-s0-frontmatter-em-yaml)
    - [3.1 S1: Identity](#31-s1-identity)
    - [3.2 S2: Activation](#32-s2-activation)
      - [Purpose](#purpose)
      - [Start Conditions](#start-conditions)
      - [End Conditions](#end-conditions)
    - [3.3 S3: Ownership](#33-s3-ownership)
      - [In (entrada)](#in-entrada)
      - [Out (saída)](#out-saída)
      - [Work (trabalho temporário)](#work-trabalho-temporário)
    - [3.4 S4: Procedure](#34-s4-procedure)
    - [3.5 S5: Rules](#35-s5-rules)
    - [3.6 S6: Exception](#36-s6-exception)
  - [4. Obrigatório / opcional](#4-obrigatório--opcional)
  - [5. Razão da ordem das seções](#5-razão-da-ordem-das-seções)

> **Contexto deste documento:** Definição única da estrutura (*Single Source of Truth*) para prompts de agente a serem colocados em .claude/agents/*.md. 
> Deve ser consultado ao criar novos agentes e ao alterar agentes existentes.
> **Documentos relacionados:** Regras de processo §7 Definição de agentes, Regras de gerenciamento de documentos

***

## 1. Princípios de design

1. **A IA deve ler de cima para baixo.** As informações lidas primeiro passam a servir como 
contexto para a interpretação das posteriores. Coloque o que deve ser conhecido primeiro no topo.
2. **Conheça a meta antes de entrar no procedimento.** Não se deve dirigir sem saber o destino.
3. **Separe o fluxo normal do fluxo excepcional.** O procedimento é o fluxo normal; a exceção é o fluxo anormal.
4. **Padronize os nomes das seções com conceitos abstratos.** Não use nomes de soluções específicas como títulos de seção.
5. **Agente = função.** Entrada (argumentos) → Procedimento → Saída (retorno). O trabalho é uma variável local e deve ser removido quando a saída for produzida.

***

## 2. Estrutura das seções

```markdown
---                          ← S0: Frontmatter em YAML (formato externo definido pelo Claude Code)
name / description / tools / model
---

{declaração de papel em 1-3 linhas} ← S1: Identity (quem é)

## Activation                   ← S2: por que / quando começar / quando terminar
### Purpose                      por que este agente existe
### Start Conditions             pré-condições para iniciar o trabalho
### End Conditions               critérios de conclusão (correspondem à lista de Out)

## Ownership                 ← S3: definição de In / Out / Work
### In                           entradas existentes antes do início do trabalho. Somente leitura; não são alteradas
### Out                          artefatos finais produzidos ao término do trabalho. Correspondem aos End Conditions
### Work                         arquivos temporários usados apenas durante o trabalho. Devem ser removidos após a conclusão

## Procedure                 ← S4: o que fazer (fluxo normal)

## Rules                     ← S5: como decidir (opcional; subseções livres)

## Exception                 ← S6: como agir em caso de anomalia
```

***

## 3. Definição de cada seção

### 3.0 S0: Frontmatter em YAML

Formato externo definido pelo Claude Code. 
Este framework não deve alterá-lo.

```yaml
---
name: agent-name
description: descrição de uma linha das condições de ativação
tools: "
  - read
  - write
  - edit
  - glob
  - grep
  - bash"
model: "opus | sonnet | haiku | inherit"
---
```

| Campo | Descrição |
| ------- | ----------- |
| name | Nome identificador do agente (kebab-case) |
| description | Descrição de uma linha usada pelo Claude Code na seleção do agente |
| tools | Ferramentas disponíveis para este agente |
| model | Modelo a ser usado. opus (alta qualidade) / sonnet (equilíbrio) / haiku (rápido) / inherit (herda do pai) |

### 3.1 S1: Identity

**Objetivo:** Declarar quem este agente é.

**Formato:** Imediatamente após o frontmatter em YAML, colocar um texto simples de 1 a 3 linhas, sem título de seção.

```markdown
Você é {nome do papel}.
{resumo de uma linha de suas responsabilidades}.
```

**Regras:**

- A primeira frase deve começar com “Você é ___.”
- A partir da segunda frase, resumir o escopo das responsabilidades
- Não ultrapassar 3 linhas. Detalhes devem ser colocados em Procedure ou Rules

### 3.2 S2: Activation

**Objetivo:** Definir o contrato do trabalho. Purpose = responsabilidade; Start Conditions = pré-condições; End Conditions = pós-condições.

#### Purpose

O motivo de existência deste agente. 1 a 2 linhas. Não descreve “o que fazer”, mas “por que fazer”.

```markdown
### Purpose

{por que este agente é chamado. Qual problema ele resolve. 1-2 linhas.}
```

#### Start Conditions

Pré-condições para iniciar o trabalho. Formato de checklist. O trabalho só pode começar se todas as condições forem atendidas. Se não estiverem, siga o que estiver em Exception.

```markdown
### Start Conditions

- [ ] {condição 1: o que precisa estar concluído/existente}
- [ ] {condição 2: o que precisa estar concluído/existente}
```

#### End Conditions

Critérios para considerar o trabalho concluído. Formato de checklist. O trabalho é encerrado quando todas as condições forem atendidas. Devem corresponder às saídas em Ownership.

```markdown
### End Conditions

- [ ] {condição de conclusão 1: o que deve estar produzido}
- [ ] {condição de conclusão 2: o que deve passar na validação}
```

**Regras:**

- Cada item de End Conditions deve corresponder a uma saída listada em Ownership (OBRIGATÓRIO)
- O agente principal deve validar as End Conditions ao transitar de fase

### 3.3 S3: Ownership

**Objetivo:** Definir as entradas e saídas de arquivos. O agente = função, então In (entrada), Out (saída) e Work (trabalho temporário) devem ficar explícitos.

#### In (entrada)

Arquivos que já existem antes do início do trabalho. Este agente apenas lê e não altera (imutável).

```markdown
### In

| file_type | fornecido por | uso |
| ----------- | --------------- | ----- |
| {file_type} | {criador: user / nome do agente / framework} | {para que serve a leitura} |
```

#### Out (saída)

Artefatos finais produzidos ao término do trabalho. Correspondem aos itens listados em End Conditions. Tornam-se a entrada do próximo agente.

```markdown
### Out

| file_type | destino de saída | próximo consumidor |
| ----------- | ------------------ | ------------------- |
| {file_type} | {caminho/padrão de nomeação} | {agente que receberá isso como In} |
```

#### Work (trabalho temporário)

Arquivos usados apenas durante a execução do trabalho. Devem aparecer apenas quando existirem.

```markdown
### Work

| arquivo | uso |
| --------- | ----- |
| {nome/padrão do arquivo} | {para que será usado} |
```

**Princípios de Work:**

- Após a conclusão do Out, o Work deve ser **removido**. Não deixar lixo
- Outros agentes não devem consultar o Work. Se for necessário, ele deve ser promovido para **Out**
- Não deve ser reutilizado. Em cada execução, deve-se criar um novo Work
- Se não houver Work, registrar “nenhum”

**Critérios para decidir In / Out / Work:**

| Pergunta | Resposta | Classificação |
| ---------- | ---------- | :------------: |
| O item já existia antes do trabalho e eu não vou alterá-lo? | Sim | **In** |
| É um artefato incluído em End Conditions? | Sim | **Out** |
| É usado apenas durante o trabalho e não será necessário depois? | Sim | **Work** |

### 3.4 S4: Procedure

**Objetivo:** Definir o fluxo de trabalho do caso normal.

```markdown
## Procedure

1. {etapa 1: verbo + objeto}
2. {etapa 2: verbo + objeto}
   - {subetapa ou observação}
3. ...
```

**Regras:**

- Deve ser descrito em etapas numeradas
- Cada etapa deve começar com um verbo
- Procedure é apenas o fluxo normal. Os desvios em caso de anomalia devem ir para Exception

### 3.5 S5: Rules

**Objetivo:** Definir regras específicas do domínio, critérios de decisão, limites e convenções.

```markdown
## Rules

### {nome da categoria da regra}

{definição da regra em tabela, lista ou parágrafo}
```

**Regras:**

- A estrutura de subseções é livre para cada agente
- Pode-se incluir uma subseção chamada `### Constraints` (o que não deve ser feito), se necessário
- Regras grandes demais podem ser separadas em documentos externos e referenciadas por link (por exemplo: review-agent → review-standards-ja.md)

### 3.6 S6: Exception

**Objetivo:** Definir condições anormais e as respostas adequadas.

```markdown
## Exception

| Anomalia | Resposta |
| ---------- | ---------- |
| {descrição da condição anormal} | {ação segura. Princípio: não avançar por suposição. Reportar ao lead} |
```

**Princípio comum:** Quando não se souber, não avançar por suposição. Reportar ao lead.

**Regras:**

- Deve cobrir os 3 tipos: pré-condições não atendidas, imprevistos durante o Procedure e impossibilidade de atingir End Conditions
- O destinatário do relatório é, em princípio, o lead. Se o lead decidir perguntar ao usuário, isso fica a cargo do lead
- A resposta deve descrever uma ação “segura”, como parar, delegar a decisão ou apresentar opções

***

## 4. Obrigatório / opcional

| Seção | Obrigatória | Motivo |
| ------- | :-----------: | -------- |
| S0: Frontmatter em YAML | Sim | Formato externo exigido pelo Claude Code |
| S1: Identity | Sim | Sem declaração de papel, o prompt não funciona |
| S2: Activation | Sim | Define o contrato do trabalho. Sem isso, não existe uma função válida |
| S3: Ownership | Sim | Definição de In/Out/Work. É a única fonte correta de propriedade de arquivos |
| S4: Procedure | Sim | Corpo das instruções de trabalho |
| S5: Rules | Opcional | Específico do domínio; alguns agentes podem não precisar |
| S6: Exception | Sim | A ausência de tratamento de exceções pode levar a comportamento inadequado |

***

## 5. Razão da ordem das seções

| Ordem | Seção | Motivo: por que essa posição |
<!-- | :---: | :---: | ----: | :---: | -->
| S1 | Identity | Primeiro, entender quem é o agente |
| S2 | Activation | Em seguida, entender por que foi chamado (Purpose), se pode começar (Start) e qual é o objetivo (End) |
| S3 | Ownership | Depois de conhecer a meta, verificar In/Out/Work. Não faz sentido ler uma lista de arquivos sem saber o objetivo |
| S4 | Procedure | Após entender a meta e os arquivos, entrar no procedimento |
| S5 | Rules | Se surgirem dúvidas durante a execução, consultar as regras |
| S6 | Exception | Consultar em caso de anomalia. Colocá-la após o fluxo normal deixa claro que o normal e o excepcional são separados |
