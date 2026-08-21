# CEPRAEA `.ai/control` — Control Plane Canônico

Este diretório contém contratos executáveis, catálogos e validadores do SDLC agentivo.

## Responsabilidades

- **`.ai/control/`** define contratos e oráculos.
- **`.ai/decisions/`** registra decisões humanas que alteram ou interpretam esses contratos.
- **`.ai/tasks/`** contém instâncias materiais por TASK.
- **Git** continua sendo estado/histórico operacional.

Não criar state machine, fila, log de conversa ou banco de workflow dentro de `.ai/`.

## Contratos ativos

| Arquivo | Objeto | Status |
| --- | --- | --- |
| `task-proposal.schema.json` | `task_proposal` v3 | ACTIVE |
| `task-approval.schema.json` | `task_approval` v1 | ACTIVE |
| `execution-result.schema.json` | `execution_result` v2 | ACTIVE |
| `runbook-catalog.json` | seleção de runbooks | ACTIVE |
| `verification-plan.schema.json` | FVR Verification Plan | PILOT_ONLY |

`TaskProposal` aprovado é o contrato semântico. Não existe transformação obrigatória `TaskProposal → TaskContract`.

## Modos

A fonte única para modos é `control-plane.json`.

- `bootstrap_mode=DESIGN`: bootstrap é diagnóstico, não gate global.
- `fvr_mode=PILOT_ONLY`: FVR não concede verdict de produção.

Qualquer promoção exige decisão humana `ACTIVE`.

## Validação

```bash
node .ai/control/validate-control-plane.mjs
```

TASK específica:

```bash
node .ai/control/validate-task-proposal.mjs .ai/tasks/<TASK-ID>/proposal.json

node .ai/control/validate-task-approval.mjs \
  .ai/tasks/<TASK-ID>/proposal.json \
  .ai/tasks/<TASK-ID>/approval.json

node .ai/control/validate-execution-result.mjs \
  .ai/tasks/<TASK-ID>/proposal.json \
  .ai/tasks/<TASK-ID>/approval.json \
  .ai/tasks/<TASK-ID>/execution-result.json
```

## Hashes

Bindings de aprovação usam SHA-256 dos **bytes UTF-8 exatos** do arquivo, sem canonicalização implícita.

Alterar whitespace altera o hash e invalida a aprovação. Isso é deliberado.

## Fail-closed

- referência ausente → FAIL/BLOCKED;
- Action órfã → FAIL;
- AC órfão → FAIL;
- ciclo de dependências → FAIL;
- pending human decision → BLOCKED;
- approval hash mismatch → BLOCKED;
- approval não humano → BLOCKED;
- mudança fora de target → BLOCKED;
- evidência simulada → FAIL;
- ausência de evidência obrigatória → BLOCKED;
- unknown não é convertido em PASS.
