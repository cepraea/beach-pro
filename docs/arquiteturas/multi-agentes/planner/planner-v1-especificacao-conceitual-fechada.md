# Planner v1 — Especificação Canônica

**Status:** CLOSED
**Contrato executável:** `.ai/control/task-proposal.schema.json` v3

## Propósito

```text
HumanRequest → Planner → TaskProposal
```

Planner é uma fase do Claude Code. Não implementa produto e não aprova o próprio plano.

## Diretórios

Durante PLAN:

- `.ai/control/**`: read-only;
- `.ai/decisions/**`: read-only;
- `.ai/tasks/<TASK-ID>/proposal.json`: read/write;
- targets do produto: read-only;
- Git: read-only.

`.agent_rules/` e `.planning/` não fazem parte da arquitetura.

## Modelo

O TaskProposal deve preservar:

```text
HumanRequest
→ Goal
→ Outputs
→ Acceptance Criteria
→ Actions
```

Rastreabilidade mínima:

```text
Action → AC → Output → Goal → HumanRequest
```

Cobertura obrigatória:

```text
∀ Action, ∃ AC
∀ AC, ∃ Action
```

Ações formam DAG acíclico.

## Readiness

O validador determinístico verifica forma, referências, cobertura, dependências, targets, runbook classes e decisões humanas pendentes.

```bash
node .ai/control/validate-task-proposal.mjs .ai/tasks/<TASK-ID>/proposal.json
```

PASS estrutural não é aprovação semântica.

## Review e aprovação

1. Codex revisa com `review_stage=PLAN`.
2. Somente `PASS` permite o humano considerar aprovação.
3. Humano cria `approval.json` vinculando `proposal_id`, `revision` e SHA-256 dos bytes.
4. Executor só inicia se `validate-task-approval.mjs` retornar PASS.

`Codex PASS ≠ Human Approval`.

## Imutabilidade

Após aprovação:

```text
SHA256(proposal bytes) != approval.proposal_sha256
→ BLOCKED
```

Qualquer mudança relevante exige nova revision, novo PLAN review e nova aprovação.
