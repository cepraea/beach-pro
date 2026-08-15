# RB-REV-002 — Revisão de banco de dados

## Objetivo

Definir o procedimento especializado de revisão independente para alterações de schema,
migrations e integridade persistente no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando o Reviewer receber um `git diff` resultante de:

- criação ou modificação de migration
- alteração de schema
- adição, remoção ou modificação de constraint
- alteração de índice ou modelo de persistência

## Entradas

- `git diff` completo da alteração
- Migration(s) produzidas pelo Executor
- Evidências de execução da migration em desenvolvimento
- Critérios de aceite da tarefa

## Fontes de autoridade

- `AGENT_POLICY.md`
- `AGENTS.md`
- `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` — quando envolver modelagem
- Fontes canônicas em `.drive/CEPRAEA BEACH PRO/**` — somente leitura
- Critérios de aceite da tarefa

## Pré-condições

- `git diff` da migration disponível
- Evidências de execução da migration produzidas pelo Executor
- Reviewer operando com projeto read-only

## Escopo operacional

Somente leitura: `git diff`, migrations, schema existente, modelo canônico, fontes normativas.

Escrita efêmera exclusivamente em `/tmp` quando necessário para execução de checks.

Não alterar o working tree, não aplicar patches, não fazer commit.

## Procedimento

1. Confirmar a tarefa sob revisão e seus critérios de aceite.
2. Identificar a norma aplicável (modelo canônico, constraint de domínio, instrução de Davi).
3. Inspecionar a migration: sequência, nome, conteúdo completo.
4. Verificar a semântica da alteração contra a definição autoritativa.
5. Verificar que migrations históricas não foram modificadas.
6. Executar teste adversarial quando apropriado (schema quebrado, dados incompatíveis).
7. Executar teste positivo quando apropriado (migration executa corretamente).
8. Verificar a integridade resultante do schema.
9. Confrontar as evidências do Executor com fatos observáveis.
10. Emitir o verdict com findings quando aplicável.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Migration modifica histórico existente | `FAIL` com finding CRITICAL |
| Semântica diverge da definição autoritativa | `FAIL` ou `HUMAN_DECISION_REQUIRED` conforme causa |
| Dados incompatíveis não tratados | `FAIL` com finding HIGH |
| Evidências do Executor insuficientes | Finding + solicitar evidências adicionais |
| Definição autoritativa ausente | `HUMAN_DECISION_REQUIRED` |

## Validações independentes

Executar proporcionalmente ao risco:

- inspecionar a sequência de migrations
- verificar que a migration executa sem erro (quando possível com projeto read-only)
- verificar constraints resultantes no schema

Caches redirecionados para `/tmp` quando necessário.

## Evidências

- Diff da migration inspecionado
- Resultado das verificações independentes executadas
- Findings documentados com estrutura completa

## Handoff

Emitir verdict com:

- resumo da revisão
- findings classificados (quando existirem)
- verificações executadas e resultados
- questões para Davi quando aplicável

## Estados de saída

`PASS` — migration correta, semântica alinhada com a definição autoritativa, histórico preservado.

`FAIL` — migration incorreta, histórico modificado, dados em risco ou evidências insuficientes
de forma material.

`HUMAN_DECISION_REQUIRED` — decisão de domínio ou semântica exige autoridade humana.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
- [`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`](../../docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md)
