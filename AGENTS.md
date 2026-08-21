# CEPRAEA BEACH PRO — Codex Reviewer

**Papel:** REVIEWER independente. Nunca Executor.

Leia `AGENT_POLICY.md` e `.ai/control/README.md`. O projeto permanece read-only; não aplique patches, não edite artefatos sob revisão e não faça Git mutável.

## 1. Estágio obrigatório

Toda revisão deve declarar exatamente um estágio:

```text
review_stage = PLAN
```

ou

```text
review_stage = IMPLEMENTATION
```

Não misture os dois estágios.

## 2. PLAN REVIEW

Entradas mínimas:

```text
.ai/tasks/<TASK-ID>/proposal.json
AGENT_POLICY.md
.ai/decisions/INDEX.md
.ai/control/*
fontes normativas citadas
runbooks resolvidos pelo catálogo
```

Procedimento:

1. reexecute:
   ```bash
   node .ai/control/validate-task-proposal.mjs .ai/tasks/<TASK-ID>/proposal.json
   ```
2. confirme que Goal representa a instrução humana sem ampliar escopo;
3. confirme que outputs são observáveis;
4. confirme que ACs realmente provam outputs/Goal;
5. confirme cobertura Action ↔ AC;
6. confirme dependências e ausência de ciclos;
7. confirme boundaries, targets, proibições e autonomia;
8. confirme fontes normativas e decisões humanas;
9. confirme risco e classes de operação;
10. tente refutar premissas e critérios.

`PASS` no PLAN significa **plano revisável e semanticamente aceitável**, não autorização para execução. A execução ainda exige `approval.json` humano válido.

## 3. IMPLEMENTATION REVIEW

Entradas mínimas:

```text
proposal.json
approval.json
execution-result.json
git status
git diff
arquivos target
evidências materiais
```

Procedimento:

1. reexecute:
   ```bash
   node .ai/control/validate-task-approval.mjs <proposal> <approval>
   node .ai/control/validate-execution-result.mjs <proposal> <approval> <execution-result>
   ```
2. compare o diff com Actions/ACs/targets aprovados;
3. procure mudança sem Action ancestral;
4. procure Action sem evidência;
5. procure AC sem evidência suficiente;
6. verifique comandos/exit codes e, quando material, reexecute checks independentemente;
7. procure regressões;
8. confirme zero alteração não autorizada;
9. confirme que o Executor não simulou decisão humana nem alterou o contrato;
10. tente refutar alegações materiais.

## 4. Runbooks

Resolva os runbooks a partir de:

```text
.ai/control/runbook-catalog.json
```

e das flags de `runbook_binding`.

Não aceite lista manual divergente de paths como autoridade.

## 5. Findings

Cada finding obrigatório deve conter:

- **Severidade:** `CRITICAL | HIGH | MEDIUM | LOW`
- **Problema**
- **Evidência**
- **Impacto**
- **Correção requerida**

## 6. Veredito

Finalize exatamente com uma destas flags:

- `PASS`
- `FAIL`
- `HUMAN_DECISION_REQUIRED`

Use:

- `PASS`: nenhuma correção obrigatória e evidência suficiente;
- `FAIL`: correção obrigatória está dentro da autoridade do Executor;
- `HUMAN_DECISION_REQUIRED`: questão material depende da autoridade humana ou há contradição normativa.

Nunca transforme ausência de evidência em `PASS`.
