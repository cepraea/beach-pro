# RB-EXEC-001 — Alteração de código

## Objetivo

Definir o procedimento especializado para implementação, correção, refatoração autorizada e
alteração de comportamento de código-fonte no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando a tarefa envolver:

- implementação de funcionalidade nova
- correção de comportamento incorreto
- refatoração explicitamente autorizada
- alteração de comportamento observável de código

## Entradas

- Tarefa autorizada por Davi com escopo definido
- Branch dedicada diferente de `main` e `master`
- `git status` limpo ou com alterações pertencentes à tarefa em curso

## Fontes de autoridade

- `AGENT_POLICY.md`
- `CLAUDE.md`
- Critérios de aceite da tarefa

## Pré-condições

- Branch correta confirmada
- `git status` inspecionado
- Escopo da tarefa identificado

## Escopo operacional

Alterar exclusivamente os arquivos necessários à tarefa autorizada.

Não modificar:

- `AGENT_POLICY.md`, `CLAUDE.md`, `AGENTS.md`
- `.devcontainer/**`, `.claude/**`, `.codex/**`
- `.drive/**`
- arquivos fora do escopo da tarefa

## Procedimento

1. Identificar os componentes afetados pela tarefa.
2. Identificar contratos públicos (APIs, tipos exportados, interfaces) relacionados.
3. Localizar os testes existentes para os componentes afetados.
4. Implementar exclusivamente a alteração requerida pela tarefa.
5. Atualizar os testes necessários para cobrir a alteração.
6. Executar os validadores aplicáveis: lint, typecheck, testes unitários, testes de integração.
7. Corrigir erros mecânicos causados pela alteração.
8. Verificar regressões diretamente relacionadas à mudança.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Alteração exige segundo arquivo fora do escopo original | Parar; comunicar e obter checkpoint de Davi antes de expandir |
| Teste falha por causa externa à alteração | Registrar e comunicar; não suprimir |
| Contrato público afetado de forma inesperada | Comunicar antes de prosseguir |

## Validações

- `npm run lint` (ou equivalente) sem erros bloqueantes
- `npm run typecheck` (ou equivalente) sem erros
- Testes unitários aplicáveis: sem falhas novas
- `git diff --check` limpo
- `git diff` inspecionado

## Evidências

- Diff completo da alteração (`git diff`)
- Resultado dos validadores (exit codes e saída relevante)
- Lista dos arquivos modificados

## Handoff

Apresentar de forma factual:

- tarefa executada
- arquivos alterados
- validações executadas e resultados
- riscos residuais ou limitações identificadas
- pontos que merecem atenção do Reviewer

Finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.

## Estados de saída

`READY_FOR_REVIEW` — alteração completa, validadores passando, diff revisável.

`BLOCKED` — qualquer condição impede a conclusão correta.

## Referências

- [`AGENT_POLICY.md`](../AGENT_POLICY.md)
- [`CLAUDE.md`](../CLAUDE.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
