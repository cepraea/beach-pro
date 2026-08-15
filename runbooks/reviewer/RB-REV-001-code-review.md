# RB-REV-001 — Revisão de código

## Objetivo

Definir o procedimento especializado de revisão independente para alterações normais de
código-fonte no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando o Reviewer receber um `git diff` resultante de:

- implementação de funcionalidade
- correção de comportamento
- refatoração autorizada
- alteração de comportamento observável de código

## Entradas

- `git diff` completo da alteração
- Critérios de aceite da tarefa
- Evidências produzidas pelo Executor

## Fontes de autoridade

- `AGENT_POLICY.md`
- `AGENTS.md`
- Critérios de aceite da tarefa
- Fontes normativas aplicáveis quando a tarefa referenciar modelagem

## Pré-condições

- `git diff` disponível e inspecionável
- Critérios de aceite identificados
- Reviewer operando com projeto read-only

## Escopo operacional

Somente leitura: `git diff`, `git status`, `git log`, arquivos do projeto.

Escrita efêmera exclusivamente em `/tmp` ou caches técnicos explicitamente autorizados.

Não alterar o working tree, não aplicar patches, não fazer commit.

## Procedimento

1. Confirmar a tarefa sob revisão e seus critérios de aceite.
2. Inspecionar `git status`.
3. Inspecionar o `git diff` completo.
4. Comparar o diff com o objetivo da tarefa.
5. Verificar o comportamento observável da alteração.
6. Procurar regressões diretamente relacionadas à área alterada.
7. Verificar os testes afetados: cobertura e adequação.
8. Executar verificações independentes proporcionais ao risco (lint, typecheck, testes selecionados).
9. Verificar alterações inesperadas fora do escopo autorizado.
10. Emitir o verdict com findings quando aplicável.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Finding requer decisão de domínio | `HUMAN_DECISION_REQUIRED` |
| Comportamento correto, mas escopo expandido sem autorização | `FAIL` com finding |
| Testes ausentes para comportamento novo | Finding LOW ou MEDIUM conforme impacto |
| Regressão confirmada | `FAIL` com finding HIGH ou CRITICAL |

## Validações independentes

Executar proporcionalmente ao risco e à área alterada:

- lint sem `--fix`
- typecheck com `noEmit`
- testes unitários selecionados para a área alterada

Caches redirecionados para `/tmp` quando necessário.

## Evidências

- Diff inspecionado
- Resultado das verificações independentes executadas
- Findings documentados com estrutura completa

## Handoff

Emitir verdict com:

- resumo da revisão
- findings classificados (quando existirem)
- verificações executadas e resultados
- questões para Davi quando aplicável

## Estados de saída

`PASS` — diff consistente com o objetivo, sem findings bloqueantes, evidências suficientes.

`FAIL` — finding CRITICAL ou HIGH, regressão confirmada, escopo violado ou evidência insuficiente
material.

`HUMAN_DECISION_REQUIRED` — questão de domínio ou decisão material exige autoridade humana.

## Referências

- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
- [`AGENTS.md`](/AGENTS.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
