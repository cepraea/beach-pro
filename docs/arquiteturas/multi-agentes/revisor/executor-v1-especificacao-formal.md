# Executor v1 — Especificação Canônica

**Status:** CLOSED
**Entrada:** `proposal.json` + `approval.json` válidos
**Saída:** `execution-result.json`

## Fonte de verdade

O `TaskProposal` aprovado é o contrato semântico.

Não existe etapa obrigatória `TaskProposal → TaskContract`.

```text
ExecutionContract = ApprovedTaskProposal + TaskApproval + RuntimeAnchor
```

## Preflight

Nenhuma escrita antes de:

1. proposta válida;
2. PLAN review PASS registrado na aprovação;
3. aprovação humana válida;
4. proposal SHA-256 exato;
5. repository/branch/base commit válidos;
6. branch diferente de main/master;
7. preconditions/dependencies satisfeitas;
8. targets e runbooks resolvidos;
9. control plane íntegro.

Falha → `BLOCKED` com `termination_reason`.

## Autoridade

```text
ExecutorAuthority =
AllowedTechnicalAutonomy
∩ Boundaries
∩ Files.target
```

Executor não altera Goal, Outputs, ACs, Actions, decisões, constraints, risco, runbook classes ou DoD.

## Unidade de execução

```text
Action
→ Preconditions
→ Dependencies
→ Authority
→ Execute
→ Validate
→ Evidence
```

Action concluída exige implementação, validação, evidência e boundary integrity.

## Evidência

Toda Action `PASS` deve referenciar evidência observada. Evidência simulada é inválida.

## Mudanças

Toda mudança deve:

- estar sob `files.target`;
- referenciar Action autorizada;
- ocorrer após preflight;
- possuir hash anterior/posterior quando aplicável.

## Saída externa

```text
READY_FOR_REVIEW
BLOCKED
```

Detalhes:

```text
termination_reason
```

não criam estados de handoff adicionais.

## ExecutionResult

Contrato em:

```text
.ai/control/execution-result.schema.json
```

Validação semântica:

```bash
node .ai/control/validate-execution-result.mjs \
  proposal.json approval.json execution-result.json
```

O Executor nunca concede aceitação final.
