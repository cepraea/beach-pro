# Índice de decisões do control plane

Somente decisões com status `ACTIVE` podem ser usadas como autoridade operacional.

| ID | Status | Arquivo | Escopo |
| --- | --- | --- | --- |
| DEC-ARQ-001 | ACTIVE | `DEC-ARQ-001-dev-container-como-sandbox-operacional.md` | sandbox operacional |
| DEC-CTR-013 | ACTIVE | `DEC-CTR-013-git-readonly-modelo-a.md` | Git read-only para agentes |
| DEC-CTR-015 | ACTIVE | `DEC-CTR-015-dois-contextos-dev-container.md` | contextos do Dev Container |
| DEC-GOV-001 | ACTIVE | `DEC-GOV-001-agent-flow-legado.md` | `.agent-flow` removido |
| DEC-GOV-002 | ACTIVE | `DEC-GOV-002-runbook-binding-modelagem-canonica.md` | binding da modelagem |
| DEC-GOV-003 | ACTIVE | `DEC-GOV-003-control-plane-canonico.md` | namespaces, lifecycle, contratos e modos |

## Regra

- `ACTIVE`: normativa.
- `SUPERSEDED`: não usar como autoridade; consultar apenas por histórico.
- `HISTORICAL`: evidência histórica.
- Contradição entre decisões `ACTIVE` → `BLOCKED` / `HUMAN_DECISION_REQUIRED`; não escolher silenciosamente pela data.
