# RB-SHARED-001 — Repository baseline

## Objetivo

Definir a verificação read-only do baseline do repositório quando a TASK exigir ancoragem explícita do estado Git.

## Aplicabilidade

Carregar somente quando `proposal.runbook_binding.repository_baseline_required = true`.

## Fontes de autoridade

- `AGENT_POLICY.md`, seções **Papéis e autoridade**, **Git** e **Zonas de escrita**;
- `CLAUDE.md` ou `AGENTS.md`, conforme o papel;
- `approval.json`, para `runtime_anchor` após a aprovação do plano.

## Operações permitidas

Somente inspeção Git, incluindo:

```text
git rev-parse
git branch --show-current
git status
git diff
git log
git show
git ls-files
```

Nenhuma mutação de index, refs, histórico ou remoto.

## Procedimento

1. Confirmar que o checkout é `cepraea/beach-pro`.
2. Capturar `HEAD` com `git rev-parse HEAD`.
3. Capturar a branch atual.
4. Confirmar que a branch não é `main` nem `master` para trabalho agentivo gravável.
5. Inspecionar `git status` e compreender qualquer mudança preexistente.
6. No Executor, comparar branch e `HEAD` com `approval.runtime_anchor`.
7. Se houver drift material não autorizado, não executar escrita.

## Resultado

- Planner/Executor: condição incompatível → `BLOCKED`.
- Reviewer: condição material que dependa de autoridade humana → `HUMAN_DECISION_REQUIRED`; violação técnica comprovada → `FAIL`.

## Evidência

Quando material para a TASK, preservar:

- branch observada;
- `HEAD` SHA;
- estado relevante de `git status`;
- divergência encontrada, se houver.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`RB-SHARED-002-evidence.md`](RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](RB-SHARED-003-failure-states.md)
