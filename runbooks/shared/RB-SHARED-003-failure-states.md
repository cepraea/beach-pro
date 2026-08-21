# RB-SHARED-003 — Estados externos e motivos de terminação

## Planner/Executor

Estados externos fechados:

- `READY_FOR_REVIEW`
- `BLOCKED`

`READY_FOR_REVIEW` exige validações/evidências requeridas e zero violação de boundary.

`BLOCKED` é usado para incapacidade legítima, contradição, decisão humana, mismatch de aprovação, drift, falha bloqueante ou violação de autoridade.

Detalhes técnicos ficam em `termination_reason` do `ExecutionResult`; não criar novos estados externos.

## Reviewer

Verdicts fechados:

- `PASS`
- `FAIL`
- `HUMAN_DECISION_REQUIRED`

Toda revisão declara `review_stage = PLAN | IMPLEMENTATION`.

- `PASS`: evidência suficiente e nenhuma correção obrigatória.
- `FAIL`: correção obrigatória está dentro da autoridade do Executor.
- `HUMAN_DECISION_REQUIRED`: questão material exige autoridade humana ou reconciliação normativa.

## Anti-bypass

Nunca contornar restrição para evitar `BLOCKED` ou `HUMAN_DECISION_REQUIRED`.
