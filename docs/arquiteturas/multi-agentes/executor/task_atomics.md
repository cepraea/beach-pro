# Padrão canônico de TASK atômica — CEPRAEA BEACH PRO

**Contrato:** `.ai/control/task-proposal.schema.json` v3

## Quando é obrigatório

TaskProposal completo é obrigatório para:

- risco `amarelo`, `vermelho` ou `vermelho_critico`;
- regra de negócio, cálculo ou decisão que afete atleta/treino/jogo/dado pessoal;
- modelo de dados, RLS, auth, MFA, auditoria;
- dependências;
- Dev Container, CI, control plane ou infraestrutura.

Tarefa `verde` estritamente local pode usar proposta proporcional somente se não exigir nenhum item acima. Se houver dúvida, use TaskProposal completo.

## Atomicidade

Dividir quando houver resultados independentes, decisões humanas independentes, fluxos distintos ou ACs que possam passar/falhar de forma independente sem compartilhar a mesma unidade funcional.

## Campos normativos

O schema v3 é a fonte de verdade dos campos. Em particular:

- `outputs[].output_id = OUT-NNN`
- `acceptance_criteria[].criterion_id = AC-NNN`
- `actions[].action_id = A-NNN`
- `actions[].acceptance_criteria_refs`
- `actions[].depends_on`
- `files[]`
- `risk`
- `runbook_binding`
- `mandatory_checks`
- `definition_of_done`

Não duplicar lista de runbook paths na TASK. O catálogo canônico é `.ai/control/runbook-catalog.json`.

## Duas revisões e uma aprovação humana

```text
proposal
→ deterministic validation
→ Codex PLAN review
→ Human approval by hash
→ implementation
→ ExecutionResult
→ Codex IMPLEMENTATION review
```

O PLAN Reviewer usa `PASS | FAIL | HUMAN_DECISION_REQUIRED`.

`PASS` do Reviewer não é autorização de execução sem `approval.json` humano válido.

## Critério de aceite

Cada AC deve possuir:

- ID estável;
- output(s) que comprova;
- condição;
- método;
- expected;
- verification owner.

Sem mecanismo de prova, o AC deve ser refinado.

## Actions

Toda Action deve declarar:

- ID;
- transformação;
- propósito;
- dependências;
- ACs cobertos;
- target files;
- evidência esperada.

Validador exige:

```text
NoOrphanAction
NoOrphanCriterion
AcyclicDependencies
TargetCoverage
```

## DONE

`definition_of_done` é verificável e referencia ACs e checks obrigatórios.

DONE não é auto-declaração do Executor. O Executor chega no máximo a `READY_FOR_REVIEW`; Codex revisa; humano controla promoção Git/release.
