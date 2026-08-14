# RB-REV-003 — Revisão de documentação

## Objetivo

Definir o procedimento especializado de revisão independente para criação e alteração de
documentação Markdown no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando o Reviewer receber um `git diff` resultante de:

- criação de novo documento Markdown
- alteração de documento Markdown existente
- atualização de decisão, modelo ou evidência em formato Markdown

## Entradas

- `git diff` completo da alteração documental
- Fontes técnicas aplicáveis ao conteúdo revisado
- Critérios de aceite da tarefa

## Fontes de autoridade

- `AGENT_POLICY.md`
- `AGENTS.md`
- `docs/standards/guia_estilo_documentação.md` — normativa canônica de autoria
- Fontes técnicas aplicáveis ao conteúdo revisado

## Pré-condições

- `git diff` disponível e inspecionável
- Guia canônico de documentação lido
- Fontes técnicas identificadas
- Reviewer operando com projeto read-only

## Escopo operacional

Somente leitura: diff, documentos do repositório, fontes técnicas aplicáveis.

Escrita efêmera exclusivamente em `/tmp` quando necessário para validações.

Não alterar o working tree, não aplicar patches, não fazer commit.

## Procedimento

1. Confirmar a tarefa sob revisão e seus critérios de aceite.
2. Identificar as fontes técnicas aplicáveis ao conteúdo.
3. Inspecionar o `git diff` completo.
4. Verificar a preservação do significado técnico: o conteúdo alterado não contradiz as fontes.
5. Verificar aderência ao guia de autoria (idioma, sentence case, linguagem direta, estrutura).
6. Identificar afirmações sem suporte em fonte verificável.
7. Verificar links e referências afetados pela alteração.
8. Verificar exemplos e comandos para correção técnica.
9. Avaliar separadamente: forma (estilo, estrutura) e correção técnica (conteúdo).
10. Emitir o verdict com findings quando aplicável.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Conteúdo contradiz fonte normativa | `FAIL` com finding HIGH ou CRITICAL conforme impacto |
| Afirmação sem suporte em evidência | Finding MEDIUM; não suprimir |
| Decisão existente alterada sem autorização | `FAIL` com finding CRITICAL |
| Erro de estilo sem impacto técnico | Finding LOW |
| Exemplo ou comando tecnicamente incorreto | Finding HIGH |

## Validações independentes

- markdownlint (ou equivalente) sem erros bloqueantes
- Links internos verificados
- Comandos listados conferidos contra a implementação atual quando críticos

## Evidências

- Diff documental inspecionado
- Resultado das validações documentais
- Findings documentados com estrutura completa

## Handoff

Emitir verdict com:

- resumo da revisão (forma e correção técnica, separadamente)
- findings classificados (quando existirem)
- verificações executadas e resultados
- questões para Davi quando aplicável

## Estados de saída

`PASS` — conteúdo tecnicamente correto, aderente ao guia de autoria, sem afirmações sem suporte
material.

`FAIL` — conteúdo tecnicamente incorreto, contradiz fonte normativa, decisão alterada sem
autorização, ou finding HIGH/CRITICAL que impeça aceitação.

`HUMAN_DECISION_REQUIRED` — questão de conteúdo que exige decisão de domínio por Davi.

## Referências

- [`AGENT_POLICY.md`](../AGENT_POLICY.md)
- [`AGENTS.md`](../AGENTS.md)
- [`docs/standards/guia_estilo_documentação.md`](../../docs/standards/guia_estilo_documentação.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
