# RB-EXEC-002 — Alteração de banco de dados

## Objetivo

Definir o procedimento especializado para alterações de schema, migrations, constraints,
índices e persistência no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando a tarefa envolver:

- alteração de schema
- criação ou modificação de migration
- adição, remoção ou modificação de constraint
- criação ou remoção de índice
- alteração de modelo de persistência

## Entradas

- Tarefa autorizada com definição normativa da alteração
- Branch dedicada diferente de `main` e `master`
- Acesso às migrations existentes e ao estado atual do schema

## Fontes de autoridade

- `AGENT_POLICY.md`
- `CLAUDE.md`
- `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` — quando a alteração envolver modelagem
- Fontes canônicas de domínio em `.drive/CEPRAEA BEACH PRO/**` — somente leitura
- Critérios de aceite da tarefa

## Pré-condições

- Branch correta confirmada
- Estado atual das migrations identificado
- Definição autoritativa da alteração identificada

## Escopo operacional

Alterar exclusivamente os arquivos necessários à evolução autorizada do schema.

Nunca modificar migrations já aplicadas em produção.

Nunca inferir atributos canônicos de colunas existentes sem evidência normativa.

## Procedimento

1. Identificar a definição autoritativa da alteração (fonte canônica, modelo canônico ou instrução de Davi).
2. Identificar o estado atual das migrations (última migration aplicada, sequência existente).
3. Verificar se existem dados incompatíveis com a alteração proposta.
4. Produzir exclusivamente uma nova migration quando a evolução do schema exigir.
5. Implementar a alteração autorizada na migration.
6. Executar a validação da migration em ambiente de desenvolvimento.
7. Executar testes de integridade relevantes.
8. Produzir as evidências materiais exigidas pelos critérios de aceite.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Alteração pode causar perda de dados | Parar e comunicar; exige decisão humana |
| Migration existente precisaria ser modificada | `BLOCKED` — migrations aplicadas não são modificadas; criar nova |
| Definição normativa ausente ou ambígua | `BLOCKED` — não inferir mecanicamente; comunicar a Davi |
| Dados incompatíveis detectados | Comunicar antes de prosseguir; não aplicar destructively sem aprovação |

## Validações

- Migration executa sem erro em ambiente de desenvolvimento
- Schema resultante é compatível com os critérios de aceite
- Testes de integridade aplicáveis passam
- `git diff --check` limpo
- `git diff` da migration inspecionado

## Evidências

- Diff completo da migration (`git diff`)
- Resultado da execução da migration em desenvolvimento
- Resultado dos testes de integridade

## Handoff

Apresentar de forma factual:

- tarefa executada
- migration produzida
- validações executadas e resultados
- impacto esperado em dados existentes
- pontos que merecem atenção do Reviewer

Finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.

## Estados de saída

`READY_FOR_REVIEW` — migration completa, validada, diff revisável.

`BLOCKED` — qualquer condição impede a conclusão correta.

## Referências

- [`AGENT_POLICY.md`](../AGENT_POLICY.md)
- [`CLAUDE.md`](../CLAUDE.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
- [`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`](../../docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md)
