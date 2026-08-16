# Padrão de tarefas atômicas e critérios de aceitação — CEPRAEA BEACH PRO

AESDS 05 — Fundação v0.3

## Objetivo

Definir a menor unidade de trabalho suficientemente explícita para que um agente implemente sem
inventar requisito, alterar escopo ou depender de conversa extensa fora da tarefa.

Este documento é a instrução completa para o Executor preencher corretamente um `task_proposal`
antes de implementar uma tarefa de produto/engenharia, e para o Reviewer avaliar se esse
preenchimento está correto. O contrato verificável por máquina correspondente está em
[`.ai/control/task-proposal.schema.json`](../../.ai/control/task-proposal.schema.json), com um
exemplo completo em [`.ai/task-proposal.example.json`](../../.ai/task-proposal.example.json)
(tarefa `TASK-001`, Wellness Pré-Treino) e um validador reproduzível em
[`.ai/control/validate-task-proposal.mjs`](../../.ai/control/validate-task-proposal.mjs)
(`node .ai/control/validate-task-proposal.mjs` valida o exemplo canônico contra o schema; aceita
`<schema> <instância>` para checar outras propostas).

**Nota de escopo:** este padrão governa tarefas do produto CEPRAEA-BEACH-PRO (código, banco de
dados, dependências, documentação de produto). A fase de modelagem canônica do domínio
(`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`, tarefas `AC-NNN`) usa seu próprio
mecanismo de decisão e evidência, já formalizado em `DEC-GOV-002`, e não é afetada por este
documento.

## Princípio

Uma tarefa atômica deve possuir uma saída verificável e pequena o suficiente para permitir revisão
integral do diff e dos critérios. "Implementar módulo X" normalmente é grande demais.

## O ciclo de duas portas

Toda tarefa neste padrão passa por duas aprovações do Reviewer, não uma:

1. **Plano.** O Executor preenche um `task_proposal` (seção "Template canônico de task", abaixo) e
   entrega `READY_FOR_REVIEW`. O Reviewer avalia o plano — antes de qualquer linha de código ser
   escrita — e emite `PASS`, `FAIL` ou `HUMAN_DECISION_REQUIRED`, os mesmos três estados que já
   usa para revisar um diff (`AGENTS.md`). `PASS` autoriza o início da implementação.
2. **Implementação.** Só após `PASS` do plano o Executor implementa, seguindo os runbooks listados
   em `runbook_binding` (preenchido no próprio plano, seção "Risco e vinculação de runbook",
   abaixo) e entrega `READY_FOR_REVIEW`/`BLOCKED` como já define `CLAUDE.md`. O Reviewer avalia o
   diff resultante contra o plano aprovado e emite `PASS`, `FAIL` ou `HUMAN_DECISION_REQUIRED`.

Nenhum estado novo foi criado: o vocabulário fechado de `RB-SHARED-003-failure-states.md`
(`READY_FOR_REVIEW`/`BLOCKED` para o Executor; `PASS`/`FAIL`/`HUMAN_DECISION_REQUIRED` para o
Reviewer) se aplica às duas portas — muda o que está sendo avaliado (plano ou diff), não o
vocabulário.

`risk` e `runbook_binding` dentro do plano reaproveitam integralmente a taxonomia já existente e
usam **valores fixos em português**, mesmo com o restante do JSON em inglês — não traduzir:

- `risk.level` — `verde | amarelo | vermelho | vermelho_critico` (`AGENT_POLICY.md`).
- `risk.natures` — `ui | dependencia | rls | mfa | ci | dados` (`AGENT_POLICY.md`). Não existe
  categoria própria para "banco de dados" ou "regra de negócio" — uma tarefa de banco usa `dados`.
- `runbook_binding.operation_classes` — `code_change | database_change | documentation_change |
  dependency_change` (`runbooks/README.md`). Não existem classes como `backend_change`,
  `validation_change` ou `test_change` — decompor a tarefa nas 4 classes reais, combinando mais de
  uma quando necessário (ex.: uma tarefa que altera migration e lógica de servidor usa
  `["database_change", "code_change"]`, com os runbooks de ambas as classes).

Verificar `runbook_binding` contra a matriz de `runbooks/README.md` por evidência (ler o arquivo),
nunca por inferência — a divergência que gerou o `FAIL` de `DEC-GOV-002` veio exatamente de pular
essa verificação.

## Template canônico de task

Cada campo abaixo corresponde a uma propriedade de `task-proposal.schema.json`. O nome entre
crases é o campo JSON exato. Os campos são em inglês; os valores de `risk`/`runbook_binding` que
referenciam um enum já estabelecido (acima) permanecem em português.

- **ID** (`task_id`) — identificador estável da tarefa (ex.: `FE-AVAIL-003`, `TASK-001`).
- **Título** (`title`) — frase curta e descritiva, não um resumo técnico da implementação.
- **Instrução original** (`original_instruction`) — texto literal recebido de Davi que originou
  esta proposta.
- **Objetivo** (`objective`) — o resultado que a tarefa produz, em uma frase.
- **Problema** (`problem`) — o problema que a tarefa resolve, distinto do objetivo (que é a
  solução). Uma tarefa sem problema identificável é candidata a questionamento antes de virar
  plano.
- **Ator** (`actor`) — quem realiza ou é afetado pelo comportamento descrito. Uma tarefa com mais
  de um ator relevante costuma ser grande demais — ver "Regra de tamanho".
- **Contexto válido** (`valid_context`) — em que situação esta tarefa/comportamento se aplica.
- **Contexto inválido** (`invalid_context`) — em que situação este comportamento explicitamente
  não se aplica. Usar "Não aplicável" quando não houver contexto inválido relevante — o campo é
  obrigatório porque a ausência de um contexto inválido registrado é, ela mesma, informação (nada
  foi excluído por omissão).
- **Pré-condições** (`preconditions`) — o que precisa ser verdade antes da tarefa começar.
- **Dependências** (`dependencies`) — outras tarefas, decisões (`DEC-NNN`) ou artefatos dos quais
  esta tarefa depende. Usar "Nenhuma" quando não houver.
- **Fonte normativa** (`normative_source`) — o(s) documento(s)/seções (business rules, decisions,
  constraints, `bdd`) que definem o requisito. Uma tarefa sem fonte normativa identificável é
  candidata a `HUMAN_DECISION_REQUIRED`, não a uma suposição do Executor.
- **Entrada/contratos** (`inputs_and_contracts`) — os dados/contratos de entrada, com seus valores
  possíveis quando forem um enum fechado.
- **Comportamento atual** (`current_behavior`) — o comportamento existente antes desta tarefa. Usar
  "N/A - nova feature" quando não houver.
- **Comportamento esperado** (`expected_behavior`) — o que o sistema deve fazer, em prosa direta.
  Quando o comportamento for observável por um usuário, expandir em BDD (seção "Critérios
  comportamentais — BDD").
- **Estados relevantes** (`relevant_states`) — os estados de interação/processamento distintos que
  a implementação precisa cobrir.
- **Dentro do escopo** (`in_scope`) — o que esta tarefa cobre, em prosa. Complementa
  `out_of_scope`, não o substitui.
- **Fora de escopo** (`out_of_scope`) — o que esta tarefa explicitamente não cobre, mesmo que
  relacionado. Existe para impedir que o Executor amplie o escopo por conta própria.
- **Edge cases incluídos** (`included_edge_cases`) — os casos de borda que fazem parte do escopo
  desta tarefa (não uma lista exaustiva de todos os edge cases possíveis do domínio).
- **Three amigos** (`three_amigos.domain_business` / `.development` / `.quality`) — a mesma
  informação vista por três perspectivas: o que o domínio/negócio exige; o que a implementação
  precisa respeitar; o que a qualidade/teste precisa cobrir. As três costumam se sobrepor
  parcialmente — isso é esperado, não redundância a eliminar.
- **Business rules** (`business_rules[]`, `{rule_id, rule}`) — regras de negócio atômicas,
  numeradas (`R-01`, `R-02`, ...) para serem referenciadas por `normative_source` e por
  `acceptance_criteria`.
- **Decisions** (`decisions[]`, `{decision_id, decision}`) — decisões técnicas/de produto já
  tomadas que restringem a implementação, numeradas (`D-01`, `D-02`, ...). Diferente de
  `human_decisions_already_made` (resumo em prosa): aqui cada decisão é atômica e referenciável.
- **Constraints** (`constraints[]`, `{constraint_id, scope, constraint}`) — restrições técnicas
  formais (ex.: `CHECK` de banco de dados), numeradas (`C-01`, `C-02`, ...). `scope` identifica
  onde a constraint se aplica (ex.: `database`).
- **Ações permitidas** (`allowed_actions`) — o que a implementação deve permitir.
- **Ações proibidas** (`prohibited_actions`) — o equivalente a MUST NOT (seção "Restrições — MUST /
  MUST NOT"). Cada item aqui é uma restrição negativa que a implementação nunca deve violar.
- **Autonomia técnica permitida** (`allowed_technical_autonomy`) — até onde o Executor pode decidir
  detalhes de implementação sem novo checkpoint.
- **Arquivos esperados ou área de escrita** (`files[]`, `{path, role, operation}`) — mesma
  classificação de `CLAUDE.md` ("Proposta proporcional"), em inglês: `role` é `target` |
  `reference` | `read_only` | `forbidden`; `operation` é `change` | `read` | `none` (o schema já
  força a combinação correta entre os dois — `target` sempre exige `change`; `reference`/
  `read_only` sempre exigem `read`; `forbidden` sempre exige `none`).
- **Decisões humanas já tomadas** (`human_decisions_already_made`) — resumo em prosa das decisões
  que já resolvem parte da ambiguidade da tarefa. Referenciar `DEC-NNN`/`DEC-GOV-NNN` ou os
  `decision_id` de `decisions[]` quando existir.
- **Decisões humanas pendentes** (`pending_human_decisions`) — toda pendência real aqui impede
  `PASS` do plano até ser resolvida ou até o Reviewer emitir `HUMAN_DECISION_REQUIRED` sobre ela.
  Usar "Nenhuma" quando não houver. Não é um espaço para hipóteses do Executor.
- **Stop conditions** (`stop_conditions`) — condições que interrompem a parte afetada da
  implementação (seção "Stop conditions do Executor").
- **Critérios de aceitação** (`acceptance_criteria[]`, `{condition, method, expected}`). Cada
  critério precisa de um oráculo de aceitação (seção "Oráculo de aceitação") — sem mecanismo de
  prova, o critério deve ser refinado antes da implementação.
- **Checks obrigatórios** (`mandatory_checks`) — os checks que o Executor deve rodar antes do
  handoff (testes, typecheck, build, lint, validação de contrato).
- **Evidência esperada** (`expected_evidence`) — o que o Executor deve anexar ao handoff para
  provar que os checks/critérios foram satisfeitos.
- **Definição de DONE** (`definition_of_done`) — a condição de fechamento da tarefa, tipicamente
  "todos os critérios de aceite passam e nenhum finding [classe] aberto".

### Risco e vinculação de runbook

Todo `task_proposal` inclui `risk` e `runbook_binding` — ver os valores fixos na seção "O ciclo de
duas portas", acima. `risk.justification` precisa citar o motivo real (ex.: "afeta fluxo usado por
todas as atletas"), não repetir o nível escolhido.

## Regra de tamanho

A tarefa deve ser dividida quando:

- possui mais de um resultado independente;
- mistura decisão de produto com execução;
- exige vários fluxos de usuário distintos;
- não cabe em um diff revisável integralmente;
- depende de duas decisões humanas não relacionadas;
- possui critérios que podem passar/falhar independentemente e não compartilham a mesma unidade
  funcional.

Não dividir artificialmente um fluxo simples em microtarefas que criem handoff sem valor.

## Critérios comportamentais — BDD

Use Gherkin (`Given`/`When`/`Then`/`And`/`But`) quando o critério descreve comportamento
observável. No `task_proposal`, isso vai no campo opcional `bdd`
(`{feature, background?, rules: [{rule, scenarios: [{name, kind, steps, examples}]}]}`) —
preencher somente quando pelo menos um critério de aceite for comportamental; omitir quando não
aplicável.

- `background` — passos comuns a todos os cenários da feature; omitir quando não houver.
- Cada item de `rules[]` agrupa os cenários que demonstram uma mesma regra de negócio.
- `kind: "scenario"` — cenário único; `examples` fica como array vazio (`[]`).
- `kind: "scenario_outline"` — cenário parametrizado; `examples` precisa de pelo menos uma tabela
  `{headers, rows}`.

**Exemplo (cenário único):**

```text
Given uma solicitação de disponibilidade aberta
And a atleta ainda não respondeu
When ela abre o treino
Then a interface exibe "Não respondida"
And não representa o estado como resposta "Não".
```

**Exemplo (scenario outline, ver `.ai/task-proposal.example.json` para o bloco `bdd` completo):**

```text
Given fadiga_geral recebe <valor>
When a submissão é enviada
Then a operação deve ser rejeitada com BAD_REQUEST

Examples:
  | valor |
  | 0     |
  | 8     |
  | 6.5   |
```

## Restrições — MUST / MUST NOT

Use requisitos declarativos quando não houver benefício em cenário BDD. No `task_proposal`, MUST
NOT vai em `prohibited_actions`; MUST vai em `allowed_actions` ou `expected_behavior`, conforme o
que descrever melhor.

**Exemplo:**

- MUST: preservar dados preenchidos após erro recuperável.
- MUST NOT: exibir UUID interno à atleta sem requisito explícito.
- MUST NOT: preencher presença automaticamente a partir de disponibilidade.

## Qualidade mensurável

Critérios de performance, acessibilidade ou cobertura precisam de métrica/condição objetiva quando
aplicável. Evitar "rápido", "bonito", "intuitivo", "moderno" sem definição verificável.

## Classificação de critério

- **CRITICAL** — falha viola segurança, autorização, integridade de domínio ou requisito
  essencial.
- **MUST** — obrigatório para DONE.
- **SHOULD** — esperado, mas pode admitir exceção documentada e aprovada.
- **OPTIONAL** — melhoria não bloqueante e explicitamente fora do caminho crítico.

## Oráculo de aceitação

Cada critério em `acceptance_criteria` deve indicar, no campo `method`, como será provado: teste
automatizado, typecheck, build, inspeção de contrato, runtime, acessibilidade, dispositivo real ou
validação humana.

Um critério sem mecanismo de prova deve ser refinado antes da implementação quando a ambiguidade
puder alterar o resultado.

## Exemplo de task atômica

O `task_proposal` completo deste exemplo está em
[`.ai/task-proposal.example.json`](../../.ai/task-proposal.example.json) — `TASK-001`,
persistência e classificação de risco do Wellness Pré-Treino: validação estrita de entrada (Zod,
sem coerção), cálculo server-side de uma flag de risco a partir de gatilhos numéricos, janela
temporal autoritativa do servidor e UPSERT sequencial. Cobre `business_rules`, `decisions`,
`constraints`, `three_amigos` e um bloco `bdd` completo com `background`, múltiplas `rules` e um
`scenario_outline` — use-o como referência estrutural para novas propostas.

## Stop conditions do Executor

Parar somente a parte afetada se descobrir: decisão material ausente; contrato incompatível; fonte
canônica conflitante; dependência nova material; necessidade de ampliar escopo; comportamento não
especificado que altera o produto.

## Regra para referências

Se a task exige escolha visual ou técnica ainda não homologada, não embutir a escolha como
implementação. Criar um ponto de decisão com as opções obtidas segundo o AESDS 08.

## Meta de primeira revisão

As tasks devem ser especificadas em granularidade suficiente para buscar >=90% de critérios PASS
na primeira revisão independente — na porta de plano e na porta de implementação. Se uma classe de
task falhar repetidamente na mesma porta, corrigir o template/contexto antes de aumentar
governança.
