# RB-SHARED-002 — Evidências materiais

## Objetivo

Definir critérios compartilhados para produção, seleção e persistência de evidências materiais
nas operações especializadas.

## Aplicabilidade

Carregar quando a operação especializada definir requisitos de evidência que precisem seguir
critérios comuns.

## Entradas

- Working tree após execução ou revisão
- Resultados dos validadores determinísticos executados

## Fontes de autoridade

- `AGENT_POLICY.md` — seção Persistent Evidence
- Critérios de aceite da tarefa em execução

## Pré-condições

- Operação especializada executada ou em execução
- Validadores determinísticos aplicáveis já rodados

## Escopo operacional

Produção e seleção de evidências para a operação em curso.

Persistência proporcional ao valor probatório da evidência.

Git permanece como mecanismo primário de estado, handoff e histórico.

## Procedimento

1. Identificar as alegações materiais da operação.
2. Para cada alegação, identificar a evidência correspondente.
3. Executar `git diff --check` e registrar o resultado.
4. Executar `git diff` e registrar o diff completo.
5. Registrar a lista dos arquivos modificados (`git status --short`).
6. Registrar exit codes relevantes dos validadores.
7. Registrar relatórios produzidos pela tarefa quando possuírem valor material.
8. Persistir somente as evidências com valor probatório.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Alegação sem evidência correspondente | Registrar como insuficiência; não inventar evidência |
| Evidência contraditória | Reportar contradição; não ocultar |
| Validador com falha | Registrar falha e impacto; não suprimir |

## Validações

- `git diff --check` não reporta espaços em branco problemáticos
- `git diff` inspecionado e compreendido
- Exit codes dos validadores documentados

## Evidências mínimas

A evidência mínima inclui:

- `git diff` ou diff completo da operação
- Lista dos arquivos alterados
- Resultado dos validadores obrigatórios

Evidências adicionais são produzidas somente quando possuírem valor material para a operação.

## Handoff

Evidências selecionadas → disponíveis para o próximo papel.

**Executor:** inclui evidências no handoff factual com `READY_FOR_REVIEW`.

**Reviewer:** usa as evidências do Executor como base para refutação independente.

## Estados de saída

**Executor:** evidência insuficiente bloqueia `READY_FOR_REVIEW` → `BLOCKED`.

**Reviewer:** insuficiência material de evidência → finding classificado + parte do verdict.

## Referências

- [`AGENT_POLICY.md`](../AGENT_POLICY.md) — seção Persistent Evidence
- [`RB-SHARED-003-failure-states.md`](RB-SHARED-003-failure-states.md)
