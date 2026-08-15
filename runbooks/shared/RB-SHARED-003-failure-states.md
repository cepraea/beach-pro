# RB-SHARED-003 — Estados de saída

## Objetivo

Padronizar a interpretação e o uso dos estados de saída nos runbooks especializados.

## Aplicabilidade

Aplicar a todos os runbooks especializados. Este runbook é normativo, não procedural.

## Fontes de autoridade

- `AGENT_POLICY.md` — separação de funções, Executor e Reviewer
- `CLAUDE.md` — estados de saída do Executor
- `AGENTS.md` — verdicts do Reviewer

## Estados do Executor

O Executor finaliza exclusivamente com:

### `READY_FOR_REVIEW`

Condições obrigatórias:

- tarefa executada conforme o escopo autorizado
- validadores determinísticos executados sem falhas bloqueantes
- `git diff --check` limpo
- `git diff` inspecionado
- `git status` inspecionado
- SOURCE_ROOT não foi modificado
- handoff factual produzido

### `BLOCKED`

Usar quando qualquer condição impedir a conclusão correta:

- capacidade necessária sem permissão disponível
- branch é `main` ou `master`
- contradição material sem resolução humana
- validador falha de forma bloqueante
- tarefa exige decisão fora da autoridade do Executor

Ao usar `BLOCKED`, reportar: o que bloqueou, o que foi feito até o momento, o que Davi precisa
decidir ou fornecer.

Nunca contornar uma restrição para evitar `BLOCKED`.

## Verdicts do Reviewer

O Reviewer finaliza exclusivamente com:

### `PASS`

Condições:

- diff consistente com o objetivo da tarefa
- sem regressões identificadas
- evidências suficientes para as alegações materiais
- validações independentes executadas sem findings bloqueantes
- fontes protegidas não foram modificadas
- autoridade humana não foi simulada pelo Executor

### `FAIL`

Usar quando identificar:

- comportamento incorreto ou inconsistente com o objetivo
- regressão
- insuficiência material de evidência
- violação de policy pelo Executor
- finding CRITICAL ou HIGH que impeça aceitação

Todo `FAIL` DEVE incluir findings estruturados:

```text
Severidade: CRITICAL | HIGH | MEDIUM | LOW
Problema:   descrição objetiva
Evidência:  trecho ou resultado observável
Impacto:    consequência se não corrigido
Correção:   o que o Executor deve fazer
```

### `HUMAN_DECISION_REQUIRED`

Usar quando:

- questão material exige autoridade humana
- contradição entre fontes normativas
- ambiguidade de domínio sem resolução técnica
- finding que não pode ser classificado como `FAIL` técnico mas impede `PASS`

Ao usar `HUMAN_DECISION_REQUIRED`, descrever: a questão específica, as alternativas identificadas,
o que Davi precisa decidir e o impacto de cada opção.

## Uso pelos runbooks especializados

Cada runbook especializado DEVE usar exclusivamente os estados correspondentes ao seu papel:

- runbooks do Executor: `READY_FOR_REVIEW` ou `BLOCKED`
- runbooks do Reviewer: `PASS`, `FAIL` ou `HUMAN_DECISION_REQUIRED`

## Referências

- [`CLAUDE.md`](..../../CLAUDE.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
