# Runbook do operador humano — Fluxo multiagente

## Objetivo

Conduzir uma TASK completa mantendo autoridade humana, revisão independente e Git privilegiado fora dos agentes.

## Fluxo

```text
1. Confirmar branch não-main
2. Solicitar PLAN ao Claude
3. Claude cria .ai/tasks/<TASK-ID>/proposal.json
4. Validar proposal
5. Solicitar Codex review_stage=PLAN
6. PASS → humano decide aprovação
7. Humano cria approval.json vinculado ao SHA-256 da proposta
8. Solicitar EXECUTE ao Claude
9. Claude faz preflight, implementa, valida e cria execution-result.json
10. Solicitar Codex review_stage=IMPLEMENTATION
11. PASS → humano revisa diff e executa Git privilegiado
```

## PLAN

Comando de validação:

```bash
node .ai/control/validate-task-proposal.mjs .ai/tasks/<TASK-ID>/proposal.json
```

Se Codex retornar:

- `FAIL`: Claude corrige somente a proposta;
- `HUMAN_DECISION_REQUIRED`: humano decide; proposta é revisada e passa por novo review;
- `PASS`: ainda não executar.

## Aprovação humana

O humano cria `approval.json` contendo:

- `plan_review.verdict = PASS`;
- `issued_by.actor_type = human`;
- proposal ID/revision;
- SHA-256 dos bytes exatos do proposal;
- repository, branch e base commit.

Validar:

```bash
node .ai/control/validate-task-approval.mjs \
  .ai/tasks/<TASK-ID>/proposal.json \
  .ai/tasks/<TASK-ID>/approval.json
```

## EXECUTE

Somente após aprovação válida.

Claude retorna `READY_FOR_REVIEW` ou `BLOCKED` e persiste `execution-result.json`.

Validar:

```bash
node .ai/control/validate-execution-result.mjs \
  .ai/tasks/<TASK-ID>/proposal.json \
  .ai/tasks/<TASK-ID>/approval.json \
  .ai/tasks/<TASK-ID>/execution-result.json
```

## IMPLEMENTATION REVIEW

Solicite ao Codex:

```text
review_stage = IMPLEMENTATION
```

Verdicts:

- `FAIL`: devolver findings ao Claude;
- `HUMAN_DECISION_REQUIRED`: decidir materialmente e, se alterar contrato, gerar nova revision + novo PLAN review + nova aprovação;
- `PASS`: humano revisa diff e pode executar Git privilegiado.

## Git

Somente humano executa `git add`, `commit`, `push`, `merge`, `rebase` ou mudança de branch/ref.

Git continua sendo state machine e histórico. `.ai/tasks/` contém contratos/evidência material, não logs de conversa.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`.ai/control/README.md`](../../.ai/control/README.md)
- [`runbooks/README.md`](../../runbooks/README.md)
