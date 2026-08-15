# RB-SHARED-001 — Repository baseline

## Objetivo

Definir verificações de baseline reutilizáveis quando a operação especializada depender delas.

## Aplicabilidade

Carregar este runbook somente quando a tarefa exigir verificação explícita do estado do
repositório antes de iniciar ou continuar uma operação especializada.

Não carregar por padrão — apenas quando necessário à classe de operação.

## Entradas

- Repositório Git acessível em `/workspaces/cepraea-beach-pro`
- Branch autorizada confirmada por Davi

## Fontes de autoridade

- `AGENT_POLICY.md` — seções Git Authority e Human Authority
- `CLAUDE.md` / `AGENTS.md` — procedimento transversal aplicável ao papel

## Pré-condições

- Container iniciado e repositório montado
- Papel (Executor ou Reviewer) identificado

## Escopo operacional

Somente operações de inspeção: `git status`, `git diff`, `git log`, `git rev-parse`,
`git ls-files`, `git show`.

Nenhuma operação de mutação.

## Procedimento

1. Identificar o repositório: confirmar que `$PWD` ou `REPO` é `/workspaces/cepraea-beach-pro`.
2. Identificar o `HEAD`: `git rev-parse HEAD`.
3. Identificar a branch atual: `git branch --show-current`.
4. Confirmar que a branch não é `main` nem `master`.
5. Inspecionar estado inicial: `git status`.
6. Identificar a área afetada pela tarefa.
7. Identificar as fontes normativas aplicáveis à tarefa.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Branch é `main` ou `master` | `BLOCKED` — não executar trabalho |
| Repositório inacessível | `BLOCKED` — comunicar ao humano |
| Estado sujo inesperado | Inspecionar antes de continuar; comunicar se material |

## Validações

- `git rev-parse --is-inside-work-tree` retorna `true`
- Branch atual não é `main` nem `master`
- `git status` inspecionado e compreendido

## Evidências

Registrar somente quando a baseline possuir valor probatório para a operação em curso:

- branch atual
- `HEAD` SHA
- resultado de `git status`

## Handoff

Baseline confirmada → prosseguir para o procedimento especializado da operação.

## Estados de saída

**Executor:** `BLOCKED` quando a baseline impedir a execução.

**Reviewer:** `HUMAN_DECISION_REQUIRED` quando a baseline revelar condição que exija decisão
humana antes da revisão.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`CLAUDE.md`](..../../CLAUDE.md)
- [`AGENTS.md`](../../AGENTS.md)
