# Biblioteca de runbooks — CEPRAEA BEACH PRO

## Autoridade

A seleção canônica de paths está em:

```text
.ai/control/runbook-catalog.json
```

O `TaskProposal` declara somente:

- `operation_classes`;
- `repository_baseline_required`;
- `evidence_review_required`.

Não duplicar paths de runbooks na TASK.

## Classes

| operation_class | Executor | Reviewer |
| --- | --- | --- |
| `code_change` | `RB-EXEC-001-code-change.md` | `RB-REV-001-code-review.md` |
| `database_change` | `RB-EXEC-002-database-change.md` | `RB-REV-002-database-review.md` |
| `documentation_change` | `RB-EXEC-003-documentation-change.md` | `RB-REV-003-documentation-review.md` |
| `dependency_change` | `RB-EXEC-004-dependency-change.md` | `RB-REV-005-dependency-review.md` |

Sempre aplicáveis ao handoff/evidência conforme o catálogo:

- `RB-SHARED-002-evidence.md`
- `RB-SHARED-003-failure-states.md`

Condicionais:

- baseline explícita → `RB-SHARED-001-repository-baseline.md`;
- revisão material adicional de evidência → `RB-REV-004-evidence-review.md`.

## Resolução

```text
TaskProposal.operation_classes
→ .ai/control/runbook-catalog.json
→ runbooks concretos
```

Divergência entre TASK e catálogo:

- Planner/Executor → `BLOCKED`;
- Reviewer → `HUMAN_DECISION_REQUIRED`.

## Precedência

```text
Humano
→ AGENT_POLICY.md
→ .ai/decisions ACTIVE
→ .ai/control
→ CLAUDE.md / AGENTS.md
→ runbooks
→ execução concreta
```

Arquitetura principal:

`docs/arquiteturas/multi-agentes/main/Human-Governed Dual-Agent SDLC Architecture.md`

## Estados

Runbooks do Planner/Executor usam somente `READY_FOR_REVIEW | BLOCKED`.

Runbooks do Reviewer usam somente `PASS | FAIL | HUMAN_DECISION_REQUIRED`.
