# RB-EXEC-003 — Alteração de documentação

## Objetivo

Definir o procedimento especializado para criação e alteração de documentação Markdown no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar quando a `operation_class` da TASK incluir `documentation_change`.

## Entradas

- `proposal.json` aprovado e íntegro;
- `approval.json` válido;
- arquivos `target` autorizados;
- guia canônico `docs/linters/guia_estilo_documentação.md`;
- critérios de aceitação e evidências esperadas da TASK.

## Fontes de autoridade

- `AGENT_POLICY.md`;
- `CLAUDE.md`;
- `.ai/control/runbook-catalog.json`;
- `docs/linters/guia_estilo_documentação.md`;
- fontes normativas declaradas no `proposal.json`.

## Pré-condições

1. O preflight do Executor passou.
2. A branch aprovada não é `main` nem `master`.
3. O guia canônico foi lido.
4. As fontes normativas necessárias estão acessíveis.
5. Não há decisão humana pendente.

## Escopo operacional

Alterar exclusivamente arquivos `target` autorizados pelo `proposal.json`.

Não usar uma tarefa documental para alterar código, configuração, infraestrutura, decisão humana ou control plane sem que esses paths estejam explicitamente autorizados no contrato aprovado.

## Procedimento

1. Ler o guia canônico de documentação.
2. Resolver as fontes normativas declaradas na TASK.
3. Preservar significado técnico, proveniência e decisões existentes.
4. Alterar somente o conteúdo necessário para satisfazer os ACs vinculados às Actions autorizadas.
5. Verificar links e referências internas afetados.
6. Executar os checks documentais declarados em `mandatory_checks`.
7. Executar `git diff --check`.
8. Inspecionar `git diff` e `git status`.
9. Registrar evidência material no `execution-result.json`.

## Pontos de decisão

| Condição | Ação |
| --- | --- |
| Fonte normativa ausente, contraditória ou incerta | `BLOCKED` |
| Alteração exige decisão humana não registrada | `BLOCKED` |
| Alteração exige path fora dos targets aprovados | `BLOCKED` |
| Check documental falha por erro introduzido pela alteração | corrigir dentro da mesma Action, sem ampliar escopo |
| Correção exige mudança semântica do contrato | `BLOCKED` |

## Validações e evidências

No mínimo, quando aplicáveis:

- lint Markdown configurado pelo repositório;
- links internos afetados;
- `git diff --check`;
- diff completo;
- exit codes dos checks materiais.

Ausência de evidência não pode ser convertida em sucesso.

## Handoff

Produzir `execution-result.json` e finalizar exclusivamente com:

- `READY_FOR_REVIEW`; ou
- `BLOCKED`.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`docs/linters/guia_estilo_documentação.md`](../../docs/linters/guia_estilo_documentação.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
