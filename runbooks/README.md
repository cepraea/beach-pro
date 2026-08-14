# Biblioteca de runbooks — CEPRAEA BEACH PRO

## Objetivo

Esta biblioteca define procedimentos especializados por classe de operação para o fluxo
Human-Governed Dual-Agent SDLC do CEPRAEA BEACH PRO.

Os runbooks complementam as políticas permanentes (`AGENT_POLICY.md`, `CLAUDE.md`, `AGENTS.md`) e
o enforcement técnico do Dev Container.

## Estrutura

```text
runbooks/
├── README.md                               ← este arquivo
├── shared/
│   ├── RB-SHARED-001-repository-baseline.md
│   ├── RB-SHARED-002-evidence.md
│   └── RB-SHARED-003-failure-states.md
├── executor/
│   ├── RB-EXEC-001-code-change.md
│   ├── RB-EXEC-002-database-change.md
│   ├── RB-EXEC-003-documentation-change.md
│   └── RB-EXEC-004-dependency-change.md
└── reviewer/
    ├── RB-REV-001-code-review.md
    ├── RB-REV-002-database-review.md
    ├── RB-REV-003-documentation-review.md
    └── RB-REV-004-evidence-review.md
```

## Seleção de runbooks

Uma tarefa DEVE carregar exclusivamente os runbooks aplicáveis à sua classe de operação.

A classe da operação determina quais procedimentos são necessários — não o número de agentes
envolvidos.

### Exemplo

Para uma tarefa que altere uma constraint de `memberships`:

**Executor:**

- `AGENT_POLICY.md`
- `CLAUDE.md`
- `runbooks/executor/RB-EXEC-002-database-change.md`
- runbook compartilhado aplicável, quando necessário
- normativa pertinente de `docs/modelagem/`
- fontes necessárias de `.drive/CEPRAEA BEACH PRO/`

**Reviewer:**

- `AGENT_POLICY.md`
- `AGENTS.md`
- `runbooks/reviewer/RB-REV-002-database-review.md`
- runbook compartilhado aplicável, quando necessário
- normativa pertinente de `docs/modelagem/`
- `git diff`
- evidências materiais aplicáveis

## Precedência

Os runbooks respeitam a autoridade das camadas superiores:

```text
Autoridade humana
        ↓
AGENT_POLICY.md
        ↓
Fontes canônicas de domínio e arquitetura
        ↓
CLAUDE.md / AGENTS.md
        ↓
Runbook especializado
        ↓
Execução concreta
```

Uma instrução de runbook possui validade somente dentro da autoridade concedida pelas fontes
superiores.

Quando uma contradição material impedir execução inequívoca:

- o Executor DEVE finalizar com `BLOCKED`
- o Reviewer DEVE emitir `HUMAN_DECISION_REQUIRED`

## Critério para criação de novos runbooks

Um novo runbook DEVERIA ser criado quando uma classe de operação possuir uma ou mais destas
características:

- recorrência
- risco material
- procedimento especializado
- decisões condicionais recorrentes
- validações específicas
- requisitos próprios de evidência
- necessidade observável de consistência entre execuções

A relação desejada é:

```text
um runbook → várias tarefas da mesma classe
```

e não:

```text
uma tarefa → um runbook exclusivo
```

## Estrutura mínima de um runbook especializado

Cada runbook DEVERIA usar as seções:

1. **Objetivo** — classe de operação governada
2. **Aplicabilidade** — condições objetivas para selecionar o runbook
3. **Entradas** — entradas necessárias exclusivamente
4. **Fontes de autoridade** — fontes que governam a operação
5. **Pré-condições** — estado necessário para iniciar
6. **Escopo operacional** — caminhos, recursos e ações autorizados
7. **Procedimento** — lista numerada quando a ordem for obrigatória
8. **Pontos de decisão** — condições observáveis para desvios de fluxo
9. **Validações** — checks determinísticos aplicáveis
10. **Evidências** — evidências necessárias para propriedades materiais
11. **Handoff** — saída destinada ao próximo papel
12. **Estados de saída** — exclusivamente os estados do papel correspondente
13. **Referências** — caminhos relativos quando adequado
