# DEC-GOV-003 — Control Plane Canônico `.ai`

**Data:** 2026-08-21
**Status:** ACTIVE
**Aprovador:** autoridade humana do repositório
**Baseline observado:** `2c182858a42854ae3890f8d490679b61f9592bf6`

## Contexto

A reorganização arquitetural introduziu divergências entre policies, Task Proposal v2, Planner v1, Executor v1, runbooks, examples e paths de documentação. A decisão humana é manter `.ai/control`, `.ai/decisions` e `.ai/tasks`.

## Decisão

1. Namespaces canônicos:
   - `.ai/control/`: contratos/oráculos;
   - `.ai/decisions/`: decisões humanas;
   - `.ai/tasks/`: instâncias materiais.
2. `.agent-flow/` permanece legado; `.agent_rules/` e `.planning/` não serão adotados.
3. Git permanece state machine e histórico operacional.
4. Claude possui duas fases, não dois agentes: `PLANNER` e `EXECUTOR`.
5. Codex possui dois estágios de review: `PLAN` e `IMPLEMENTATION`.
6. O `TaskProposal` aprovado é o contrato semântico; não existe `TaskContract` obrigatório separado.
7. `TaskApproval` é humano e vincula a proposta por SHA-256 dos bytes exatos.
8. `Codex PASS` no PLAN é necessário, mas não suficiente; a autorização de execução depende do `TaskApproval`.
9. Estados externos do Planner/Executor: `READY_FOR_REVIEW | BLOCKED`.
10. Verdicts do Reviewer: `PASS | FAIL | HUMAN_DECISION_REQUIRED`.
11. `.ai/tasks/` não armazenará conversas, queues, `STATE.md`, logs narrativos obrigatórios ou review logs.
12. `execution-result.json` é evidência material estruturada, não state machine.
13. `bootstrap_mode=DESIGN` permanece diagnóstico até nova decisão.
14. `fvr_mode=PILOT_ONLY` permanece não obrigatório até conformance comprovada e nova decisão.
15. A matriz de runbooks é canônica em `.ai/control/runbook-catalog.json`; TASKs não duplicam paths.
16. Contratos executáveis ficam em `.ai/control`; documentação apenas os explica.

## Consequências

- `task-proposal.schema.json` evolui para v3 com IDs de outputs, ACs e Actions e referências determinísticas.
- `task-approval.schema.json` passa a existir como contrato real, sem approval-service/signature fictícios.
- `execution-result.schema.json` passa para `.ai/control/`.
- Examples mudam para `.ai/control/examples/`.
- `.ai/tasks/<TASK-ID>/` contém somente `proposal.json`, `approval.json` e `execution-result.json`, conforme aplicável.
- `manifest.json` torna-se inventário estruturado e `manifest.md` passa a ser derivado.
