# RB-REV-003 — Revisão de documentação

## Objetivo

Definir o procedimento de revisão independente para alterações de documentação Markdown.

## Aplicabilidade

Usar quando a `operation_class` da TASK incluir `documentation_change`.

## Entradas

- `proposal.json` aprovado;
- `approval.json` válido;
- `execution-result.json`;
- `git diff` e `git status`;
- guia canônico `docs/linters/guia_estilo_documentação.md`;
- fontes normativas e evidências materiais aplicáveis.

## Fontes de autoridade

- `AGENT_POLICY.md`;
- `AGENTS.md`;
- `.ai/control/runbook-catalog.json`;
- `docs/linters/guia_estilo_documentação.md`;
- fontes normativas declaradas no `proposal.json`.

## Pré-condições

- `review_stage = IMPLEMENTATION`;
- Reviewer em modo read-only;
- proposal/approval/result resolvíveis;
- diff inspecionável.

## Procedimento

1. Validar proposal, approval e execution result.
2. Inspecionar `git status` e `git diff` completos.
3. Confirmar que cada arquivo alterado está dentro da superfície autorizada.
4. Comparar afirmações do documento com suas fontes normativas.
5. Verificar aderência ao guia canônico de documentação.
6. Verificar links e referências afetados.
7. Tentar refutar alegações materiais do Executor usando evidência observável.
8. Reexecutar checks compatíveis com read-only e proporcionais ao risco.
9. Emitir findings estruturados quando necessário.

## Pontos de decisão

| Condição | Ação |
| --- | --- |
| Conteúdo contradiz fonte normativa | `FAIL` |
| Decisão material foi simulada pelo Executor | `FAIL` ou `HUMAN_DECISION_REQUIRED`, conforme a correção possível |
| Afirmação material sem evidência suficiente | `FAIL` |
| Semântica depende de decisão humana não resolvida | `HUMAN_DECISION_REQUIRED` |
| Erro apenas editorial, sem impacto material | finding proporcional; não inventar nova exigência |

## Validações independentes

Quando aplicável:

- lint Markdown sem `--fix`;
- links internos afetados;
- comandos/documentação técnica confrontados com a implementação atual;
- integridade do `execution-result.json`.

## Handoff

Finalizar exclusivamente com:

- `PASS`;
- `FAIL`; ou
- `HUMAN_DECISION_REQUIRED`.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`docs/linters/guia_estilo_documentação.md`](../../docs/linters/guia_estilo_documentação.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
