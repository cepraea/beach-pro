# `.ai/tasks` — Instâncias materiais de TASK

Estrutura canônica:

```text
.ai/tasks/
└── <TASK-ID>/
    ├── proposal.json
    ├── approval.json
    └── execution-result.json
```

## Regras

- `proposal.json`: criado pelo Planner; imutável para agentes após aprovação.
- `approval.json`: criado/alterado somente pelo humano; vincula o SHA-256 exato da proposta.
- `execution-result.json`: criado pelo Executor após aprovação válida e preflight.
- Reviewer é read-only.
- Não criar `STATE.md`, chat logs, filas, history logs, executor logs ou reviewer logs.
- Git fornece histórico e estado operacional.

Uma TASK pode existir apenas com `proposal.json` enquanto estiver em planejamento. Ausência de `approval.json` significa **não autorizada para execução**.
