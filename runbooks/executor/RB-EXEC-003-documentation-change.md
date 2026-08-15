# RB-EXEC-003 — Alteração de documentação

## Objetivo

Definir o procedimento especializado para criação e alteração de arquivos de documentação
Markdown no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando a tarefa envolver:

- criação de novo documento Markdown
- alteração de documento Markdown existente
- atualização de decisão, modelo ou evidência em formato Markdown

## Entradas

- Tarefa autorizada com escopo documental definido
- Branch dedicada diferente de `main` e `master`

## Fontes de autoridade

- `AGENT_POLICY.md` — seção Autoria de documentação
- `CLAUDE.md`
- `docs/standards/guia_estilo_documentação.md` — normativa canônica de autoria
- Fontes técnicas aplicáveis à tarefa
- Critérios de aceite da tarefa

## Pré-condições

- Branch correta confirmada
- Guia canônico de documentação lido antes de escrever
- Fontes técnicas aplicáveis identificadas

## Escopo operacional

Alterar exclusivamente os arquivos dentro do escopo documental autorizado pela tarefa.

Não criar ou alterar:

- código, configuração ou infraestrutura como parte de uma tarefa documental
- decisões canônicas retroativamente para justificar alterações de código anteriores
- conteúdo que contradigam fontes normativas sem decisão explícita de Davi

## Procedimento

1. Ler `docs/standards/guia_estilo_documentação.md` antes de escrever qualquer conteúdo.
2. Identificar as fontes técnicas aplicáveis (modelo canônico, plano, fontes do domínio).
3. Preservar as decisões existentes registradas nos documentos afetados.
4. Restringir a alteração estritamente ao escopo documental autorizado pela tarefa.
5. Aplicar as regras de autoria: português brasileiro, sentence case, linguagem direta, fidelidade técnica.
6. Verificar links e referências afetados pela alteração.
7. Executar as validações documentais disponíveis (markdownlint ou equivalente).
8. Inspecionar o diff documental antes de finalizar.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Fonte técnica ausente ou incerta | Registrar como lacuna; não inventar conhecimento |
| Alteração implica mudança de decisão existente | Parar; comunicar a Davi antes de alterar |
| Link quebrado detectado | Corrigir somente se dentro do escopo; registrar os demais |

## Validações

- `markdownlint` (ou equivalente) sem erros bloqueantes
- Links internos verificados
- Regras de autoria aplicadas
- `git diff --check` limpo
- Diff documental inspecionado

## Evidências

- Diff completo do documento (`git diff`)
- Resultado da validação documental

## Handoff

Apresentar de forma factual:

- tarefa executada
- documentos alterados
- validações executadas e resultados
- lacunas identificadas (conhecimento ausente, links não corrigidos)
- pontos que merecem atenção do Reviewer

Finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.

## Estados de saída

`READY_FOR_REVIEW` — alteração completa, validações documentais passando, diff revisável.

`BLOCKED` — qualquer condição impede a conclusão correta.

## Referências

- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`docs/standards/guia_estilo_documentação.md`](../../docs/standards/guia_estilo_documentação.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
