# WCRA — Workflow de Contexto com Relay Assimétrico

Um workflow no qual o **repositório é a fonte canônica e memória compartilhada**, os agentes locais executam alterações, os modelos web atuam como consultores e o humano controla a transferência e validação do contexto.

## 1. Arquitetura

```text
                    ┌──────────────────────────┐
                    │   Repositório canônico   │
                    │ contexto, código, estado │
                    └────────────┬─────────────┘
                                 │ acesso direto
                    ┌────────────▼─────────────┐
                    │ Agentes locais executores│
                    │ Codex / Claude Code      │
                    └────────────┬─────────────┘
                                 │ gera handoff
                    ┌────────────▼─────────────┐
                    │       Relay humano       │
                    │ seleciona, envia, valida │
                    └────────────┬─────────────┘
                                 │ copiar/colar
                 ┌───────────────▼───────────────┐
                 │ Modelos web consultores       │
                 │ ChatGPT / Gemini              │
                 └───────────────┬───────────────┘
                                 │ resposta
                    ┌────────────▼─────────────┐
                    │       Relay humano       │
                    │ registra no repositório │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │ Validação e aplicação   │
                    │ por agente local        │
                    └──────────────────────────┘
```

## 2. Princípios

1. **O repositório é a única fonte de verdade.**
2. Respostas de modelos web nunca são automaticamente canônicas.
3. Modelos web aconselham; agentes locais analisam e executam.
4. O humano autoriza a saída e o retorno de informações.
5. Todo handoff deve ser autocontido, rastreável e versionável.
6. Conteúdo gerado por IA deve ser distinguido de conteúdo validado.
7. Alterações materiais devem terminar em verificação.
8. Contexto temporário não deve contaminar a documentação permanente.

## 3. Papéis

### Orquestrador humano

Responsável por:

- definir o objetivo;
- escolher o modelo consultor;
- revisar informações antes do envio;
- impedir exposição de dados sensíveis;
- transferir o pacote para o navegador;
- registrar a resposta;
- aprovar decisões e mudanças críticas.

### Agente local executor

Codex ou Claude Code:

- inspeciona o repositório;
- reúne o contexto relevante;
- produz o pacote de handoff;
- interpreta a resposta do modelo web;
- confronta sugestões com o estado real do projeto;
- implementa alterações autorizadas;
- executa testes e verificações;
- atualiza a documentação.

### Modelo web consultor

ChatGPT ou Gemini:

- analisa somente o contexto fornecido;
- propõe soluções;
- identifica riscos e alternativas;
- revisa decisões ou artefatos;
- produz uma resposta no formato solicitado;
- explicita hipóteses e informações ausentes.

O modelo web não deve presumir que conhece o restante do repositório.

### Repositório

Funciona como:

- blackboard;
- memória persistente;
- mecanismo de handoff;
- registro de decisões;
- trilha de auditoria;
- fonte canônica do estado do projeto.

## 4. Estrutura recomendada

```text
repositorio/
├── AGENTS.md
├── CLAUDE.md
├── README.md
│
├── .context/
│   ├── README.md
│   ├── project/
│   │   ├── overview.md
│   │   ├── architecture.md
│   │   ├── constraints.md
│   │   └── glossary.md
│   │
│   ├── governance/
│   │   ├── roles.md
│   │   ├── relay-policy.md
│   │   ├── data-classification.md
│   │   └── validation-policy.md
│   │
│   ├── decisions/
│   │   └── DEC-0001-example.md
│   │
│   ├── tasks/
│   │   └── TASK-0001/
│   │       ├── brief.md
│   │       ├── state.md
│   │       └── evidence.md
│   │
│   ├── handoffs/
│   │   ├── outgoing/
│   │   ├── incoming/
│   │   └── archive/
│   │
│   ├── sessions/
│   └── templates/
│       ├── handoff-request.md
│       ├── handoff-response.md
│       ├── decision.md
│       └── task-state.md
│
├── src/
└── tests/
```

A pasta `.context/` concentra os artefatos de coordenação sem misturá-los com o produto.

## 5. Fluxo operacional

### Fase 1 — Iniciar a tarefa

O humano ou agente local cria:

```text
.context/tasks/TASK-0042/
├── brief.md
├── state.md
└── evidence.md
```

O `brief.md` registra:

- objetivo;
- escopo;
- critérios de aceitação;
- restrições;
- arquivos relacionados;
- decisões que exigem aprovação humana.

### Fase 2 — Investigar localmente

O agente local:

1. lê as instruções do repositório;
2. inspeciona código e documentação;
3. identifica a fonte canônica;
4. registra evidências;
5. separa fatos, hipóteses e dúvidas;
6. decide se uma consulta externa agrega valor.

Consultas web não devem substituir a inspeção local.

### Fase 3 — Gerar o pacote de handoff

O agente cria:

```text
.context/handoffs/outgoing/
└── HO-0042-chatgpt-architecture-review.md
```

O pacote deve ser suficiente para que o modelo web trabalhe sem acesso ao repositório.

### Fase 4 — Revisar e transmitir

O humano:

1. verifica o conteúdo;
2. remove segredos e dados desnecessários;
3. aprova o destinatário;
4. copia o pacote para ChatGPT ou Gemini;
5. aguarda a resposta.

Esse é o principal checkpoint humano.

### Fase 5 — Capturar a resposta

A resposta é salva sem ser tratada como verdade:

```text
.context/handoffs/incoming/
└── HO-0042-chatgpt-architecture-review-response.md
```

Deve preservar:

- modelo utilizado;
- data;
- identificador do handoff;
- resposta original;
- observações do humano;
- status de validação.

### Fase 6 — Validar localmente

O agente local compara a resposta com:

- código real;
- documentação;
- restrições;
- dependências;
- testes;
- decisões anteriores.

Cada recomendação recebe uma classificação:

| Classificação | Significado |
| --- | --- |
| Aceita | Compatível e sustentada por evidências |
| Aceita com adaptação | Ideia válida, mas exige ajuste local |
| Pendente | Faltam evidências ou aprovação |
| Rejeitada | Incompatível, incorreta ou fora do escopo |
| Substituída | Outra solução foi considerada superior |

### Fase 7 — Aplicar

O agente local:

- apresenta ou registra o plano;
- altera somente arquivos dentro do escopo;
- preserva mudanças existentes;
- atualiza testes;
- documenta decisões relevantes;
- relaciona alterações ao ID da tarefa e do handoff.

### Fase 8 — Verificar

A verificação pode incluir:

- testes automatizados;
- lint;
- compilação;
- inspeção do diff;
- validação de segurança;
- revisão humana;
- teste funcional;
- comparação com os critérios de aceitação.

### Fase 9 — Consolidar e encerrar

Depois da aprovação:

- decisões permanentes vão para `.context/decisions/`;
- documentação canônica é atualizada;
- informações temporárias são arquivadas;
- o estado da tarefa passa para `closed`;
- o handoff permanece como evidência, não como fonte canônica.

## 6. Máquina de estados

```text
draft
  ↓
locally_investigated
  ↓
ready_for_relay
  ↓ aprovação humana
sent_to_web
  ↓
response_captured
  ↓
under_validation
  ├── rejected
  ├── needs_clarification ──→ ready_for_relay
  └── approved_for_application
                         ↓
                      applied
                         ↓
                      verified
                         ↓
                       closed
```

Estados recomendados:

| Estado | Responsável principal |
| --- | --- |
| `draft` | Humano ou agente local |
| `locally_investigated` | Agente local |
| `ready_for_relay` | Agente local |
| `sent_to_web` | Humano |
| `response_captured` | Humano |
| `under_validation` | Agente local |
| `approved_for_application` | Humano/agente, conforme risco |
| `applied` | Agente local |
| `verified` | Agente local e/ou humano |
| `closed` | Humano ou responsável pela tarefa |

## 7. Contrato do handoff

Um pacote de saída pode usar este formato:

```markdown
---
id: HO-0042
task: TASK-0042
status: ready_for_relay
created_at: 2026-07-24
created_by: codex
target: chatgpt-web
purpose: architecture-review
classification: internal
human_approval_required: true
source_commit: abc1234
---

# Objetivo

Revisar a proposta de arquitetura descrita abaixo.

# Papel do modelo

Atue como revisor técnico. Não presuma acesso ao repositório.

# Estado confirmado

- Fato confirmado 1
- Fato confirmado 2

# Contexto

Conteúdo mínimo necessário para a análise.

# Restrições

- Restrição técnica
- Restrição organizacional
- Não sugerir alterações fora do escopo

# Evidências

- Arquivo ou trecho relevante
- Resultado de teste
- Decisão anterior

# Questões

1. Pergunta específica.
2. Pergunta específica.

# Formato esperado

- Recomendação
- Justificativa
- Riscos
- Alternativas
- Informações ausentes
```

## 8. Contrato da resposta

```markdown
---
handoff_id: HO-0042
task: TASK-0042
source: chatgpt-web
captured_at: 2026-07-24
captured_by: human
validation_status: unverified
---

# Resposta original

Conteúdo retornado pelo modelo.

# Declarações identificadas

- Recomendação A
- Recomendação B

# Hipóteses do modelo

- Hipótese não confirmada A

# Validação local

| Recomendação | Resultado | Evidência |
|---|---|---|
| A | aceita | teste ou arquivo |
| B | rejeitada | incompatibilidade encontrada |

# Decisão humana

Pendente.
```

## 9. Matriz de autoridade

| Ação | Agente local | Modelo web | Humano |
| --- | ---: | ---: | ---: |
| Ler repositório | Sim | Não | Sim |
| Criar handoff | Sim | Somente sugerir | Sim |
| Editar código | Sim | Não | Sim |
| Propor solução | Sim | Sim | Sim |
| Transferir dados para web | Não automaticamente | Não | Sim |
| Aprovar exposição de dados | Não | Não | Sim |
| Validar tecnicamente | Sim | Parcialmente | Sim |
| Aprovar mudança crítica | Não isoladamente | Não | Sim |
| Tornar conteúdo canônico | Conforme política | Não | Sim/agente autorizado |

## 10. Regras de governança

O workflow deve impedir que:

- uma conversa web seja tratada como documentação oficial;
- o modelo web invente contexto ausente;
- uma resposta seja aplicada sem validação contra o repositório;
- arquivos sensíveis sejam incluídos automaticamente no handoff;
- dois agentes alterem simultaneamente o mesmo artefato canônico sem coordenação;
- resumos substituam evidências primárias;
- conteúdo antigo permaneça ativo sem indicação de validade.

Classificação mínima dos dados:

```text
public       → pode ser enviado
internal     → requer revisão humana
confidential → requer autorização explícita
secret       → não deve integrar handoffs web
```

## 11. Implementação mínima viável

Uma primeira versão precisa apenas de:

```text
AGENTS.md
.context/
├── README.md
├── project/
│   └── overview.md
├── tasks/
├── handoffs/
│   ├── outgoing/
│   ├── incoming/
│   └── archive/
├── decisions/
└── templates/
    ├── handoff-request.md
    └── handoff-response.md
```

O MVP deve suportar:

1. criação de tarefa;
2. geração de handoff;
3. revisão humana;
4. captura da resposta;
5. validação local;
6. aplicação;
7. verificação;
8. arquivamento.

A identificação arquitetural final é:

> **WCRA: uma arquitetura blackboard baseada em repositório, com agentes locais executores, modelos web consultores, memória persistente em arquivos e relay humano responsável por segurança, transferência, validação e autoridade final.**

Para executar o WCRA, as ações devem ser divididas entre preparação inicial do repositório e execução recorrente de cada tarefa.

## 1. Preparar o repositório

| Ação | Responsável | Resultado |
| --- | --- | --- |
| Definir o repositório como fonte canônica | Humano | Regra registrada |
| Criar a estrutura `.context/` | Agente local | Diretórios de contexto |
| Criar `AGENTS.md` e, se necessário, `CLAUDE.md` | Humano + agente | Instruções operacionais |
| Definir papéis e responsabilidades | Humano | Matriz de autoridade |
| Definir classificação de dados | Humano | Política de segurança |
| Definir estados das tarefas e handoffs | Agente + humano | Máquina de estados |
| Criar templates | Agente local | Formatos padronizados |
| Definir critérios de aprovação | Humano | Checkpoints explícitos |
| Definir métodos de verificação | Agente + humano | Testes e validações |
| Versionar a estrutura | Humano/agente autorizado | Baseline rastreável |

Estrutura mínima:

```text
.context/
├── README.md
├── project/
├── governance/
├── tasks/
├── handoffs/
│   ├── outgoing/
│   ├── incoming/
│   └── archive/
├── decisions/
├── sessions/
└── templates/
```

## 2. Registrar a tarefa

O humano ou agente local deve:

1. atribuir um identificador, como `TASK-0042`;
2. descrever o objetivo;
3. definir o escopo;
4. indicar o que está fora do escopo;
5. registrar restrições;
6. estabelecer critérios de aceitação;
7. relacionar arquivos relevantes;
8. identificar decisões que exigem aprovação;
9. definir o nível de sensibilidade dos dados;
10. marcar o estado como `draft`.

Artefatos:

```text
.context/tasks/TASK-0042/
├── brief.md
├── state.md
└── evidence.md
```

## 3. Investigar o repositório

O agente local deve:

1. ler `AGENTS.md`, `CLAUDE.md` e instruções aplicáveis;
2. verificar o estado do Git;
3. identificar alterações já existentes;
4. localizar arquivos relacionados à tarefa;
5. inspecionar código, configuração, testes e documentação;
6. consultar decisões anteriores;
7. executar verificações diagnósticas;
8. distinguir fatos de hipóteses;
9. registrar evidências;
10. identificar lacunas que justifiquem consulta a um modelo web.

Saída esperada:

- fatos confirmados;
- dúvidas não resolvidas;
- arquivos relevantes;
- riscos;
- necessidade ou não de relay.

Se a consulta externa não for necessária, o agente pode seguir diretamente para planejamento e execução local.

## 4. Selecionar o modelo consultor

Quando houver necessidade de relay, o humano ou agente prepara a decisão sobre:

- ChatGPT ou Gemini;
- finalidade da consulta;
- tipo de especialização necessária;
- quantidade de contexto;
- formato esperado da resposta;
- sensibilidade das informações;
- necessidade de comparação entre modelos.

O modelo deve ser escolhido pela função, não apenas pela disponibilidade.

## 5. Construir o pacote de contexto

O agente local deve:

1. criar um identificador, como `HO-0042`;
2. indicar a tarefa associada;
3. declarar o objetivo da consulta;
4. explicar o papel esperado do modelo;
5. informar que o modelo não possui acesso ao repositório;
6. incluir somente fatos relevantes;
7. adicionar trechos necessários de código ou documentação;
8. listar restrições;
9. apresentar evidências;
10. formular perguntas específicas;
11. solicitar um formato de resposta;
12. registrar fontes e versão do repositório;
13. salvar o pacote em `handoffs/outgoing/`.

O pacote precisa ser:

- autocontido;
- mínimo;
- não ambíguo;
- rastreável;
- seguro para transmissão.

## 6. Revisar segurança e qualidade

Antes do envio, o humano deve verificar:

- presença de senhas, tokens ou credenciais;
- dados pessoais;
- informações confidenciais;
- arquivos desnecessários;
- instruções maliciosas copiadas de fontes externas;
- contexto incorreto ou desatualizado;
- perguntas excessivamente abertas;
- ausência de critérios de resposta.

Possíveis decisões:

```text
Aprovar → enviar
Corrigir → retornar ao agente
Reduzir → remover dados desnecessários
Anonimizar → substituir informações sensíveis
Bloquear → não realizar o relay
```

Após aprovação, o estado muda para `ready_for_relay`.

## 7. Realizar o relay para o modelo web

O humano deve:

1. abrir uma conversa adequada;
2. informar que o conteúdo constitui um pacote autocontido;
3. colar o handoff integralmente;
4. evitar acrescentar contexto contraditório informalmente;
5. solicitar que o modelo declare hipóteses;
6. solicitar que indique informações insuficientes;
7. registrar qual modelo e, se disponível, qual versão foi usado;
8. marcar o handoff como `sent_to_web`.

Se houver anexos, o humano deve conferir se realmente foram processados pelo modelo.

## 8. Capturar a resposta

O humano deve:

1. copiar a resposta integral;
2. evitar corrigi-la silenciosamente;
3. registrar data, modelo e conversa de origem;
4. preservar a resposta original;
5. separar eventuais observações humanas;
6. salvar em `handoffs/incoming/`;
7. relacionar a resposta ao handoff e à tarefa;
8. marcar `validation_status: unverified`;
9. mudar o estado para `response_captured`.

A resposta ainda é uma contribuição não validada.

## 9. Validar a resposta localmente

O agente local deve decompor a resposta em declarações verificáveis:

- fatos;
- hipóteses;
- recomendações;
- decisões sugeridas;
- riscos;
- comandos;
- alterações propostas.

Depois deve:

1. confrontar cada declaração com o repositório;
2. consultar documentação ou fontes primárias quando necessário;
3. verificar compatibilidade com dependências e versões;
4. testar exemplos ou comandos relevantes;
5. identificar sugestões fora do escopo;
6. detectar contradições com decisões anteriores;
7. estimar impacto e risco;
8. registrar evidências;
9. classificar cada recomendação;
10. produzir uma síntese de validação.

Classificações:

```text
accepted
accepted_with_changes
pending_evidence
requires_human_decision
rejected
superseded
```

## 10. Resolver dúvidas ou conflitos

Se a resposta não for suficiente, deve-se:

1. registrar exatamente o que ficou indefinido;
2. buscar evidências localmente;
3. solicitar decisão humana, quando pertinente;
4. preparar um novo handoff vinculado ao anterior;
5. evitar sobrescrever a resposta anterior;
6. repetir o relay somente com perguntas incrementais.

O workflow retorna para `ready_for_relay`, mantendo o histórico.

## 11. Aprovar a execução

Antes de aplicar alterações, deve ser definido quem possui autoridade.

O agente pode prosseguir diretamente quando:

- a mudança está no escopo;
- é reversível;
- não afeta sistemas externos;
- não envolve dados sensíveis;
- está autorizada pelas instruções do repositório.

É necessária aprovação humana quando houver:

- alteração arquitetural significativa;
- mudança destrutiva;
- migração de dados;
- exposição de informações;
- custo externo;
- publicação;
- alteração de segurança;
- decisão de negócio;
- conflito entre fontes canônicas.

O estado passa para `approved_for_application`.

## 12. Planejar a implementação

O agente local deve:

1. converter recomendações aceitas em ações;
2. ordenar as ações por dependência;
3. identificar arquivos afetados;
4. definir verificações para cada mudança;
5. preservar alterações preexistentes;
6. estabelecer critérios de interrupção;
7. registrar riscos e possibilidade de reversão.

O plano deve manter a rastreabilidade:

```text
Recomendação → Decisão → Alteração → Verificação
```

## 13. Aplicar as alterações

O agente local deve:

1. editar somente o necessário;
2. seguir as convenções do projeto;
3. não sobrescrever trabalho não relacionado;
4. atualizar código, configuração e documentação;
5. criar ou atualizar testes;
6. registrar decisões permanentes;
7. manter referências à tarefa e ao handoff;
8. mudar o estado para `applied`.

O conteúdo da resposta web não deve ser copiado indiscriminadamente. Apenas as recomendações validadas entram no produto ou na documentação canônica.

## 14. Verificar o resultado

A verificação deve incluir, conforme o projeto:

- inspeção do diff;
- testes unitários;
- testes de integração;
- lint;
- verificação de tipos;
- compilação;
- validação de configuração;
- análise de segurança;
- teste funcional;
- revisão documental;
- comparação com critérios de aceitação.

Devem ser registrados:

- comandos executados;
- resultados;
- falhas;
- limitações;
- verificações não realizadas;
- evidências finais.

Se houver falha:

```text
Falha de implementação → corrigir localmente
Premissa incorreta → retornar à validação
Contexto insuficiente → novo handoff
Decisão necessária → escalar ao humano
```

## 15. Realizar a revisão humana final

O humano deve confirmar:

- atendimento ao objetivo;
- respeito ao escopo;
- adequação das decisões;
- ausência de exposição indevida;
- qualidade das alterações;
- suficiência das verificações;
- necessidade de revisão adicional.

Após aprovação, o estado passa para `verified`.

## 16. Consolidar o conhecimento

O agente local deve separar:

| Conteúdo | Destino |
| --- | --- |
| Decisão permanente | `.context/decisions/` |
| Conhecimento estável | Documentação canônica |
| Estado da tarefa | `tasks/TASK-ID/state.md` |
| Evidências | `evidence.md` |
| Conversa temporária | `handoffs/archive/` |
| Pendências | Nova tarefa ou backlog |
| Informação inválida | Marcação de rejeição ou obsolescência |

Não se deve transformar todo o histórico do handoff em documentação permanente.

## 17. Encerrar a tarefa

Para encerramento:

1. atualizar o estado para `closed`;
2. registrar a decisão final;
3. confirmar os critérios de aceitação;
4. arquivar handoffs;
5. registrar pendências;
6. remover ou marcar contexto temporário;
7. verificar que a documentação canônica está atualizada;
8. registrar a versão ou commit resultante;
9. apresentar ao humano um resumo do resultado.

## Checklist operacional resumido


- [ ] Criar e classificar a tarefa
- [ ] Ler instruções do repositório
- [ ] Inspecionar o estado local
- [ ] Reunir evidências
- [ ] Decidir se o relay é necessário
- [ ] Escolher o modelo consultor
- [ ] Gerar pacote autocontido
- [ ] Revisar dados e segurança
- [ ] Aprovar o envio
- [ ] Enviar ao modelo web
- [ ] Capturar a resposta integral
- [ ] Registrar proveniência
- [ ] Validar cada recomendação
- [ ] Resolver conflitos e lacunas
- [ ] Aprovar ações de maior risco
- [ ] Planejar a implementação
- [ ] Aplicar alterações
- [ ] Executar verificações
- [ ] Realizar revisão humana
- [ ] Atualizar fontes canônicas
- [ ] Arquivar artefatos temporários
- [ ] Encerrar a tarefa

A unidade fundamental de execução do workflow é:

> **Tarefa → investigação local → handoff → relay humano → consulta web → captura → validação local → aprovação → aplicação → verificação → consolidação.**