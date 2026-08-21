# RB-REV-004 — Revisão de evidências

## Objetivo

Definir a revisão independente da suficiência, autenticidade e rastreabilidade de evidências materiais.

## Aplicabilidade

Carregar adicionalmente quando `proposal.runbook_binding.evidence_review_required = true`.

## Entradas

- `proposal.json` aprovado;
- `approval.json` válido;
- `execution-result.json`;
- `git diff` e estado observável do repositório;
- evidências referenciadas pelo resultado de execução.

## Fontes de autoridade

- `AGENT_POLICY.md`, seção **Evidência e claims**;
- `AGENTS.md`;
- ACs e Actions do `proposal.json`.

## Regras de suficiência

Uma evidência material só pode sustentar `PASS` quando:

1. existe e é resolvível;
2. não é simulada;
3. identifica Actions e ACs existentes;
4. é consistente com o estado observável;
5. quando deriva de comando, preserva comando e exit code;
6. quando depende de artefato, o artefato referenciado existe e corresponde à alegação;
7. não é contradita por observação independente mais forte.

`git diff` prova que houve mudança; não prova que a mudança está correta.

## Procedimento

1. Enumerar alegações materiais do Executor.
2. Mapear alegação → Action → AC → Evidence.
3. Rejeitar referências órfãs ou evidência simulada.
4. Reproduzir checks críticos quando compatíveis com read-only e proporcionais ao risco.
5. Comparar os resultados independentes com o `execution-result.json`.
6. Classificar qualquer insuficiência como finding.

## Pontos de decisão

| Condição | Ação |
| --- | --- |
| Action em PASS sem evidência material | `FAIL` |
| AC obrigatório sem evidência PASS | `FAIL` |
| Evidência contradiz estado observável | `FAIL` |
| Evidência crítica não pode ser reproduzida por limitação legítima | registrar limitação; não converter em PASS |
| Critério de suficiência depende de escolha humana | `HUMAN_DECISION_REQUIRED` |

## Handoff

Finalizar exclusivamente com o verdict do Reviewer:

- `PASS`;
- `FAIL`; ou
- `HUMAN_DECISION_REQUIRED`.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
