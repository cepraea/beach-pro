# RESULTADO DA ANALISE DA ARQUITETURA

Análise concluída. Li os arquivos de governança:

- os 13 runbooks,
- o control plane .ai/,
- o plugin Codex instalado
- o histórico Git.

*Nenhum arquivo foi alterado.*

## Diagnóstico central

**A arquitetura tem Reviewer, mas não tem Verifier.**

P1, P3 e P5 são o mesmo defeito visto de ângulos diferentes:
*Fatos que deveriam ser calculados estão sendo argumentados entre dois LLMs em linguagem natural.*

**Duas evidências fecham isso:**

1. A camada de "validadores determinísticos" está vazia.
    - Não existe `package.json`, node_modules nem `markdownlint` no repositório.
    - `RB-EXEC-001`:67-68 prescreve `npm run lint` e `npm run typecheck`;
    - `RB-EXEC-003`:6 e `RB-REV-003`:69 prescrevem `markdownlint`.
    - Nenhum existe.
    - O único validador executável é `validate-task-proposal.mjs` (rodei: exit 0).
    E `RB-SHARED-003`:26 exige **"validadores determinísticos executados sem falhas bloqueantes"** como pré-condição de `READY_FOR_REVIEW` — uma condição que hoje é **logicamente vazia.**
2. O diagnóstico já está escrito no próprio repositório.
    - `01-ESTADO-ATUAL-ARQUITETURA.md` lista `R-001` — Critérios de aceite textuais permitem interpretação diferente entre Executor e Reviewer e `R-005` — Reviewer ainda precisa recalcular fatos que poderiam ser decididos mecanicamente. Isso é literalmente `P1` e `P5`.
    - E `02-ESTADO-ARQUITETURA-FINAL.md` já projeta a correção:

    > **Executor ≠ Verifier ≠ Reviewer ≠ Autoridade Humana**, com a regra `FormalResult` != `PASS` ⟹ Reviewer não pode emitir `PASS`.

A solução não precisa ser inventada. Precisa sair de `docs/backlog/`.

***

## `P1` — Handoff para o Revisor

**O handoff é obrigatório?**

Sim, mas por uma razão mais estreita do que o fluxo assume hoje.
`CLAUDE.md`:68-79 define seis categorias e `RB-SHARED-003`:31 torna "handoff factual produzido" pré-condição de `READY_FOR_REVIEW`.

O objetivo real do `handoff` não é transmitir estado — `AGENT_POLICY.md`:39 já diz que *"Git é a state machine e o mecanismo de handoff"*. O handoff carrega exatamente o que o diff não carrega:
- o que foi tentado e falhou,
- o que ficou fora de escopo por decisão,
- qual limitação é conhecida,
- onde o Executor não conseguiu provar algo.

> **É um registro de incerteza, não um resumo.**
Hoje ele é usado como resumo — e um resumo é redundante com o diff, o que explica por que a discussão sobre sua ausência foi possível.

***

### Handoff ou diff?

Ambos, com papéis distintos e não intercambiáveis:

Fonte | Autoridade sobre
--- | ---
`git diff` / `git status` | O que mudou. Autoritativo.
`Handoff` | O que o Executor não conseguiu provar, e por quê. Não autoritativo, mas insubstituível.
`task_proposal` / plano aprovado  | O que deveria ter mudado. Contrato.

> O erro do **Reviewer** foi tratar o handoff como fonte de contrato (`runbook_binding`). Contrato é o terceiro artefato, que naquele turno não existia.

***

### Que tipo de revisão?

A arquitetura já diferencia — o problema é que a diferenciação não é acionável. `AGENTS.md`:39-52 define um procedimento único de 12 passos, mas runbooks/README.md seleciona runbooks por `operation_class`, e cada `RB-REV` traz uma perspectiva própria:

`RB-REV-001` — regressão, adequação de testes, comportamento observável.
`RB-REV-002` — adversarial sobre migrations, casos positivos e negativos.
`RB-REV-003` — separa explicitamente forma de correção técnica (RB-REV-003:54).
`RB-REV-004` — suficiência de evidência e reprodução independente.

Então:

>As revisões não devem ser iguais, e a instrução já existe — mas só é alcançada via `runbook_binding`, que só existe quando há `task_proposal`, que só é obrigatória para risco amarelo ou superior.

- Para risco verde, o **Reviewer** cai no procedimento genérico de `AGENTS.md` sem perspectiva definida. Essa é a lacuna.

***

### Postura adversarial

`AGENTS.md:48-50` já manda *"tentar refutar conclusões materiais" e "procurar afirmações mais fortes que suas evidências".*

- Isso é adversarial por design e está correto.
- O que falta não é mais adversarialidade — é delimitação do que é legitimamente atacável.

***

### De quem é a culpa quando o **Reviewer** reprova por falta de handoff?

Da arquitetura, e consigo demonstrar isso mecanicamente. Existe uma **assimetria textual real** entre os dois **arquivos de papel**:

- `CLAUDE.md`:9 — *"Quando existir `runbook_binding` na tarefa/plano aprovado"* → condicional.

- `AGENTS.md`:13 — *"leia o `runbook_binding` da tarefa sob revisão"* → imperativo incondicional.

Lido literalmente, o **Reviewer** tem uma obrigação que o **Executor** não tem o dever correspondente de satisfazer. Ele executou a instrução dele corretamente.

**Pior**: a regra que ele estava lembrando existe de verdade. `DEC-GOV-002`:93-95 diz textualmente:

> *"Handoffs de tarefas desta fase devem citar este binding [...] para que a vinculação seja verificável no repositório, não apenas declarada em prosa."*

Só que essa obrigação é escopada a `AC-001–AC-029`/`SEM-NNN`/`SYN-NNN`. A tarefa do manifesto não é dessas. O **Reviewer** aplicou uma regra real fora do escopo dela — e não tinha como saber o escopo, porque:

```bash
grep -rn "DEC-GOV|.ai/decisions" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/
→ zero ocorrências
```

Nenhum dos dois agentes carrega `.ai/decisions/` em nenhum momento. Existe uma decisão aprovada, normativa e vinculante que é invisível para ambos os papéis. Não é erro de julgamento do Codex; é uma **fonte normativa órfã**.

***

## Como mitigar interpretação errada do Reviewer?

**Três mecanismos, em ordem de força:**

1. **Mover fatos para fora do julgamento.**
    - *"O binding bate com a matriz"* não deveria ser uma leitura comparativa de dois Markdown por dois LLMs. Deveria ser um script que sai `0` ou `1`. Enquanto for prosa, dois modelos vão divergir — e divergir é o comportamento correto de um revisor adversarial diante de texto ambíguo.

2. Tornar o contrato da tarefa um artefato obrigatório e versionado, não um turno de conversa.
    - Se cada tarefa tem um arquivo com `task_id`, `risk`, `runbook_binding` e *critérios* com *ID estável*, o **Reviewer** para de inferir escopo.

3. Criar uma classe de *finding* que o **Reviewer** não pode emitir contra o **Executor**.
    - Ausência de artefato de contrato é falha de entrada da tarefa, não defeito de execução. O verdict correto já existe e é `HUMAN_DECISION_REQUIRED` — `AGENTS.md`:86-88. O que falta é a regra explícita mandando usá-lo nesse caso.

### O que garante o comportamento correto do **Reviewer**?

Hoje: nada mecânico.

`AGENTS.md` é um prompt, e `.codex/config.toml` só garante `read-only` e *sem rede* — restringe o que ele pode fazer, não o que ele pode concluir. E confirmei que o plugin não lê `AGENTS.md` (`grep -rn` "AGENTS" no plugin → zero), então quando você usa `/codex:review`, essas **garantias não estão nem carregadas.**

***

## P2 — O plugin Codex

Inspecionei a versão instalada: `codex@openai-codex v1.0.6`, `enabledPlugins`: true em `~/.claude/settings.json`.

### Ajuda ou atrapalha?

*Do jeito que está configurado hoje, **atrapalha** — e de forma silenciosa, que é o modo pior.*

Aspecto	Codex | CLI direto (fluxo atual) | Plugin / `codex:review` | Plugin / `codex:adversarial-review`
:--- | :---: | :---: | :--- |
|Carrega `AGENTS.md` | Sim (Codex CLI lê nativamente) | Não | Não |
Prompt usado | AGENTS.md do projeto | Reviewer nativo do Codex | prompts/`adversarial-review.md` do plugin
Vocabulário de verdict | `PASS`/`FAIL`/`HUMAN_DECISION_REQUIRED` | `approve`/`needs-attention` | `approve`/`needs-attention` |
Severidades | `CRITICAL`/`HIGH`/`MEDIUM`/`LOW`| `critical`/`high`/`medium`/`low` | `idem`
Runbooks | Sim | Não | Não
Sandbox | `.codex/config.toml` | `read-only` (hardcoded) | `read-only` (hardcoded)

- O plugin substitui seu **Reviewer** em vez de operá-lo.
- O schema em `schemas/review-output.schema.json` força `verdict: enum["approve","needs-attention"]` — não existe `HUMAN_DECISION_REQUIRED`.
- A saída do plugin não consegue representar o estado mais importante da sua arquitetura: o caso em que só Davi pode decidir.
Ele vira `needs-attention`, indistinguível de um defeito técnico do **Executor.**

**Ponto positivo real**: as `reviews` são hardcoded sandbox: "`read-only`", alinhado com `AGENTS.md`:9.

Risco não óbvio: `codex:rescue`
O subagente `codex-rescue` instrui:

*"Default to a write-capable Codex run by adding --write".*

Se acionado, o Codex vira **Executor** — viola `AGENT_POLICY.md` ("Produção, revisão e aprovação são funções distintas"), e o `.codex/config.toml` `read-only` não se aplica porque o plugin passa `sandbox` explicitamente.
**Essa é a maior exposição de governança do plugin hoje.**

O que o plugin revisa: últimas alterações ou o plano?

Só diff. `commands/review.md` suporta `--scope auto`|`working-tree`|`branch` e `--base <ref>`. Não existe modo "revisar o plano". Portanto o plugin não resolve `P3` e não pode resolver — a porta de plano é anterior a qualquer diff.

**Nota importante**: em modo `working-tree`, o escopo é o estado acumulado da árvore. Se você tem duas TASKs não commitadas, ele revisa as duas juntas — perde a atomicidade de `task_atomics.md`. Use `--base` com a branch, ou commite por `TASK`.

***

## As skills do **Reviewer** continuam sendo usadas?

Não existem skills de **Reviewer**. `.claude/` está vazio no repositório — zero skills, zero agents, zero settings versionados. As três skills do plugin (`codex-cli-runtime`, `codex-result-handling`, `gpt-5-4-prompting`) são infraestrutura interna do plugin, não do CEPRAEA.

### O plugin mantém as soluções de P1?
Não. Ele remove o carregamento de `AGENTS.md` e dos runbooks. Qualquer correção que você fizer em `AGENTS.md` fica inerte sob `/codex:review`.

### Como usar o plugin corretamente
O plugin resolve um problema real de P2 (o `copy-paste`) e não deve ser descartado — mas precisa de escopo definido:

- `/codex:review` — não usar como porta de governança. Serve como pré-check barato antes de acionar o Reviewer formal. Saída dele nunca é verdict.
`/codex:adversarial-review` "<instruções>" — aceita texto livre de foco. É o único canal viável para injetar `AGENTS.md` + runbooks aplicáveis. Ainda assim o verdict volta no vocabulário errado.
Review formal (Codex CLI direto) — continua sendo a porta que emite `PASS`/`FAIL`/`HUMAN_DECISION_REQUIRED`.
Desabilitar codex:rescue, ou registrar decisão explícita de que Codex nunca roda com `--write`.

**Retorno honesto**: o plugin elimina o `copy-paste` do **Reviewer** para o **Executor**, mas custa o carregamento da governança. É um trade-off ruim enquanto a governança viver só em prompt. Depois que `P1`/`P5` forem resolvidos com verificação determinística, o custo cai muito — porque o essencial passa a estar em arquivo verificável, não em prompt.

## P3 — Planejamento silencioso
Este problema já está resolvido no papel e a solução está inalcançável.

`task_atomics.md`:50-66 define o ciclo de duas portas:

Plano. O Executor preenche um task_proposal [...] O Reviewer avalia o plano — antes de qualquer linha de código ser escrita [...] PASS autoriza o início da implementação.
Implementação. Só após PASS do plano o Executor implementa.
E o documento nota explicitamente que nenhum estado novo foi criado — o vocabulário fechado se aplica às duas portas.

Agora o problema:


grep -rn "task_atomics|task_proposal" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/
→ zero ocorrências
Nem CLAUDE.md nem AGENTS.md mencionam a existência da porta de plano. Eu, como Executor, só descobri esse documento porque você o citou na sua pergunta. O Codex, como Reviewer, também não o carrega. O ciclo de duas portas está escrito, tem schema (task-proposal.schema.json), tem exemplo (task-proposal.example.json), tem validador funcionando — e nenhum dos dois agentes sabe que ele existe.

Então a resposta a "só perceberemos no final?" é: sim, hoje sim — não por falta de projeto, mas porque o projeto não está ligado aos arquivos de papel. Essa é a correção de menor esforço e maior retorno de toda a lista.

## P4 — Sobrecarga humana

**Correção factual sobre o Git**

A queixa sobre o histórico está desatualizada.

Verifiquei:

Período | Padrão de mensagem
--- | ---
até `2026-08-15` | Todos-online, Alinhamento-Final, Ajustes Finais nos arquivos, Arquivos commitador por Davi Sermenho
a partir de `2026-08-16` | `TASK-GOV-001`: `enforce Git inspection allowlist`, `AC-002: process BancoCEPRAEA source`, `DEC-GOV-002: bind canonical modeling runbooks`, `ASSURANCE-001: organize FVR assurance backlog`

Os últimos ~20 commits são `TASK-ID: ação — semânticos e rastreáveis a uma TASK`. O problema do Git foi resolvido há dois dias e a queixa descreve o estado anterior. Vale confirmar isso antes de investir em correção de commits, porque a carga cognitiva real hoje vem de outro lugar.

### De onde vem a carga real

Não é do Git. É de você ser o barramento de mensagens entre dois processos. Copiar `handoff`, copiar findings, lembrar qual `TASK` pertence a qual `branch`, reconstruir contexto — tudo isso é sintoma de que o estado da tarefa não tem representação em arquivo. Ele vive na sua memória e no scrollback de dois terminais.

Note a tensão real com `AGENT_POLICY.md`:131 — *"Não crie state machine, log de interação ou relatório obrigatório paralelo ao Git"*.

Essa regra está certa quanto ao log, mas hoje ela é lida de forma ampla demais e acaba impedindo o contrato da tarefa, que não é um log paralelo: **é uma entrada versionada em Git, com o Git continuando como state machine. Vale explicitar essa distinção no texto, senão a própria policy bloqueia a correção.**

### O que reduz carga sem tocar em Git operacional

Git operacional continua sendo seu por `AGENT_POLICY.md`:50-60, e o guard em `.devcontainer/guards/pretool` aplica isso `fail-closed` (testei: `git branch --show-current` foi bloqueado). Não proponho mudar isso.

O que reduz carga sem violar a fronteira:

Um arquivo de contrato por `TASK` (`.ai/tasks/<TASK-ID>.json`). Substitui
*"lembrar o que pertence a cada `TASK"`.*
Convenção `TASK-ID` na branch e no `commit` — já em uso desde `16/08`. Formalizar como regra fecha a rastreabilidade.

1. O Executor propõe a mensagem de commit no handoff (texto, não execução).
2. Você cola. Elimina redação, preserva autoridade.
3. Diffs grandes são sintoma de tarefa não-atômica, e `task_atomics.md`:(175-185) já define a regra de divisão.
4. Aplicar a porta de plano corta esse problema na origem.

***

## P5 — Executor vs Revisor

**Onde exatamente o desperdício nasce**

Encontrei um dado que explica o padrão. Medi densidade de termos que exigem julgamento sem limiar definido (material, proporcional, relevante, suficiente, adequado, conforme o impacto, quando necessário…), por 100 linhas:

Arquivo | Linhas | Ocorrências | Densidade
--- | --- | --- | ---
RB-REV-004 | 103 | 17 | 16,5
RB-SHARED-002 | 88 | 11 | 12,5
RB-REV-001 | 105 | 10 | 9,5
RB-REV-003 |	104 |	9  |	8,7
runbooks/README.md	 |201	 |17 |	8,5
AGENTS.md	 |90 |	7	 |7,8
RB-SHARED-003 |	106 | 6	| 5,7
AGENT_POLICY.md	| 149 |	8 |5,4
task_atomics.md	| 285 | 15  | 5,3
CLAUDE.md |	85 | 4 | 4,7
RB-EXEC-003 |	101 |	3  | 3,0
RB-EXEC-001	 |104 | 3 |	2,9

Dois padrões saltam:
- Os runbooks do **Reviewer** são **3 a 5×** mais subjetivos que os do **Executor**.
- O papel que emite o  |verdict | opera com a **instrução mais vaga**. Isso é o inverso do que a arquitetura precisa.
`RB-REV-004` é o documento mais subjetivo do repositório — e `DEC-GOV-002`:(76-84) o tornou permanente para toda tarefa `AC-001–AC-029`.

>Você acoplou permanentemente o documento de menor determinismo à fase de trabalho em curso. Não é coincidência que os FAILs se concentrem em suficiência de evidência.

### Sobre "o Executor não abre o runbook"

Isso é literal e eu confirmo: no turno do manifesto eu não abri RB-EXEC-003. Mas a causa é estrutural, não de diligência: `CLAUDE.md`:9 condiciona o carregamento à existência de `runbook_binding`, e sem `task_proposal` não há binding. Risco verde cria um caminho onde nenhum runbook é carregado por construção.

E RB-EXEC-003:47 contém uma instrução que eu deveria ter seguido e não segui: "Ler docs/standards/guia_estilo_documentação.md antes de escrever qualquer conteúdo". Essa é uma pré-condição real, perdida pelo caminho verde.

Como resolver o desperdício
A correção não é "instruir melhor". É retirar a classe de finding do domínio do julgamento:

Um script decide o binding, não dois LLMs lendo Markdown. Entrada: contrato da tarefa. Saída: 0 ou 1 + divergência apontada. Nenhum dos dois argumenta.
Toda tarefa tem contrato, inclusive risco verde — em forma reduzida. Verde não deve significar sem contrato, deve significar contrato mínimo. Isso fecha simultaneamente o buraco do Executor (nenhum runbook carregado) e o do Reviewer (nenhum binding para conferir).
AGENTS.md ganha uma regra de atribuição de falha: ausência de artefato de contrato → HUMAN_DECISION_REQUIRED, nunca finding contra o Executor. Já é o verdict correto por AGENTS.md:86-88; falta dizer que este caso o exige.
Corrigir a assimetria CLAUDE.md:9 × AGENTS.md:13 — as duas frases precisam ter a mesma condicionalidade.
Reduzir RB-REV-004 a critérios binários. "Evidência suficiente" precisa virar uma lista fechada de propriedades verificáveis, senão continua produzindo FAIL negociável.

## P6 — Skills

### Quando uma Skill do Reviewer deve nascer

Sua intuição está correta e vou torná-la um critério:

>uma Skill de Reviewer só se justifica quando traz competência técnica que o runbook não pode conter — conhecimento de domínio externo (semântica de RLS no Postgres, classes de BOLA/IDOR, armadilhas de lock em migration). Runbook responde "qual procedimento seguir"; Skill responde "o que eu preciso saber para executar esse procedimento com competência".

**Corolário:**

> *"o runbook não é usado"* nunca é motivo para criar Skill. É defeito de binding, e criar Skill nesse caso duplica normativa — introduz exatamente a divergência entre fontes que causou o FAIL de `DEC-GOV-002`. review-task-proposal, review-documentation-claims e review-test-adequacy da sua lista caem nessa categoria: RB-REV-003, RB-REV-004 e RB-REV-001 já cobrem. Não criar.

As que passam no critério: `review-rls-security` e `review-database-change` — trazem conhecimento que `RB-REV-002` legitimamente não contém.

### O Executor precisa de Skills de produção?

Sim, mas nenhuma delas é a prioridade agora, com uma exceção.

Ponto de ordem: .claude/** é control plane por AGENT_POLICY.md e está bloqueado no guard (*/.claude/* → block).

**Criar Skill exige tarefa humana explícita com esse alvo.**

Priorização honesta:

Skill	Veredito
prepare-task-proposal	P0. É o que liga task_atomics.md ao fluxo real e destrava P3 e P5. Única com retorno imediato.
run-quality-gates	Prematuro. Não há gates para orquestrar — não existe package.json. Primeiro criar os gates.
supabase / supabase-postgres-best-practices (oficiais)	Instalar quando a fase de banco começar. Conhecimento externo real, sem risco de duplicar normativa. Não antes.
supabase-migration, database-testing	Depois do modelo canônico fechar. Hoje seriam especulação sobre um schema que não existe.
model-domain-types, react-feature	Prematuro — não há código de aplicação no repositório.
cepraea-documentation	Não criar. Duplicaria RB-EXEC-003 + o guia de estilo. Risco de divergência maior que o ganho.

***

## P7 — Tarefas que não acabam

**As tarefas estão atômicas?**

O padrão existe e é bom (task_atomics.md:175-185), mas não se aplica à fase em curso por decisão explícita: task_atomics.md:20-24 diz que a modelagem canônica "usa seu próprio mecanismo de decisão e evidência, já formalizado em DEC-GOV-002, e não é afetada por este documento".

**Consequência direta:** as tarefas AC-NNN não passam pelo ciclo de duas portas, não têm task_proposal, não têm critérios com ID estável e não têm oráculo de aceitação formal. É exatamente a fase onde os FAILs estão concentrados.

**Estão sendo registradas?**

Parcialmente. Rastreabilidade existe via commit (AC-001:, AC-002:) e via PR. Não existe registro do contrato — só do resultado.

**Cada tarefa deveria ter schema?**

Sim, e o schema já existe e funciona: task-proposal.schema.json + validador que roda com exit 0. Não está sendo usado no fluxo real. Sua intuição aqui está certa e o custo de aplicá-la é baixo — o ativo já está construído e testado.

### Impacto de migrar as tarefas AC-NNN para a nova arquitetura

Ganho, com uma ressalva de sequenciamento.

Argumento a favor:
- DEC-GOV-002:80-84 registra que AC-001 sofreu "várias rodadas de revisão adversarial" com achados de suficiência e precisão de evidência — abas não lidas, localização incorreta de fragmento, classificação incorreta de dado sensível.
- Todos esses são verificáveis mecanicamente. "A aba X foi lida" é file.sha256 + cobertura declarada, não julgamento. São exatamente as propriedades que o verification-plan de 02-ESTADO-ARQUITETURA-FINAL.md foi projetado para calcular.
- Com 27 tarefas AC restantes, o custo de não migrar se paga muitas vezes.

Ressalva: AC-001 e AC-002 já foram concluídas e mergeadas. Não reclassificar retroativamente — DEC-GOV-002 já estabeleceu esse princípio para AC-000 e ele deve valer aqui. Migrar de AC-003 em diante.

Prejuízo real, para você decidir com o número na mão:
**preencher task_proposal por tarefa AC adiciona sobrecarga por tarefa. Vale medir em uma antes de comprometer as 27.**

### A ordem que você propôs está correta

**Concordo com o sequenciamento:**

>P1–P6 antes de continuar AC-003. Mas com uma ressalva forte — P1, P3 e P5 são um único defeito e devem ser uma única correção, não três. Tratados separadamente, cada um produz documentação nova e nenhum produz mecanismo.

## Drift de documentação — achados concretos
# | Arquivo |	Drift |	Sev. |
:---: | --- | --- | --- |
D-01 |	CLAUDE.md, AGENTS.md | Zero referências a .ai/decisions/**.|
DEC-GOV-002 | é normativa e aprovada, mas invisível para ambos os agentes. | Causa raiz direta do FAIL de P1. | CRÍTICO |
D-02 | CLAUDE.md, AGENTS.md | Zero referências a task_atomics.md. O ciclo de duas portas existe e é inalcançável. Causa raiz de P3.	| CRÍTICO |
D-03 | RB-EXEC-001:67-68, RB-EXEC-003:66, RB-REV-003:69	Prescrevem npm run lint, npm run typecheck, markdownlint. Nenhum existe — sem package.json, sem node_modules, markdownlint ausente. | Torna RB-SHARED-003:26 vacuamente satisfeita.| CRÍTICO |
D-04 | CLAUDE.md:9 × AGENTS.md:13 | Assimetria condicional/imperativa sobre runbook_binding. Mecanismo textual exato do FAIL. | ALTO |
D-05 | .markdownlint.jsonc regra relative-link-path ("Não use caminhos relativos", search: "](..") × runbooks/README.md item 13 ("caminhos relativos para as fontes aplicáveis") | Contradição normativa direta. O validador determinístico reprovaria 46 links dos próprios runbooks. Latente só porque markdownlint não está instalado — vira falha em massa no dia da instalação. | ALTO |
D-06 | RB-REV-001:102-103, RB-EXEC-002:100, RB-EXEC-003:97, RB-EXEC-004:97 | 5 links absolutos (/AGENT_POLICY.md) — quebrados como caminho de arquivo. Os outros 8 runbooks usam ../../. Inconsistência intra-biblioteca. | MÉDIO
D-07 | manifest.json | Asset docs/arquiteturas/assurance/ não existe (caminho real: docs/backlog/verificacao-formal-fvr/planejamento/). 1 de 42 assets quebrado, em documento commitado em 2026-08-18. Reproduzível: node -e "...".	|MÉDIO
D-08 | AGENT_POLICY.md lista de control plane | -- runbooks/** com hífen duplo — quebra o item da lista. Também colide com a regra m-dash do próprio markdownlint.| BAIXO
D-09 | RB-EXEC-001:39-44 | Lista "não modificar" omite runbooks/**, .github/workflows/**, scripts/ci/**, presentes em AGENT_POLICY.md. Duplicação divergente de normativa. | BAIXO
D-10| .markdownlint.jsonc | Regras herdadas do MDN Content sem relação com o projeto: fqdn-moz-links, relative-link (en-US/docs), short-link (bugzilla), link-fragments desativada por causa do gerador "yari". O próprio arquivo admite: "vale confirmar com Davi". Config estrangeira adotada sem triagem. | BAIXO |

### Correção arquitetural proposta

Não documentar melhor. Três mudanças estruturais, em ordem de dependência.

1. Fechar o loop normativo — o control plane precisa ser alcançável
  **Hoje existem fontes normativas aprovadas que nenhum agente carrega.**

   - Enquanto isso for verdade, qualquer regra nova que você escrever tem chance de nascer órfã igual a `DEC-GOV-002`.
   - `CLAUDE.md` e AGENTS.md passam a apontar para .ai/decisions/ e para task_atomics.md.
   - Um índice .ai/decisions/README.md com escopo de aplicabilidade por decisão — DEC-GOV-002 teria dito "aplica-se a AC-001–AC-029", e o Codex não teria generalizado.
   - Corrigir D-04 (assimetria) e D-05 (contradição markdownlint).
   - Custo baixo, risco verde/amarelo, e destrava tudo o mais.


2. Instituir a porta de plano — P3, e metade de P1 e P5
   O mecanismo já existe inteiro: schema, exemplo, validador funcionando. Falta ligá-lo.
   - Toda tarefa produz .ai/tasks/<TASK-ID>.json antes da implementação, validado por validate-task-proposal.mjs.
   - Risco verde usa perfil reduzido — mas sempre com runbook_binding. Elimina o caminho onde nenhum runbook é carregado.
   - Reviewer avalia o plano na porta 1. Vocabulário inalterado.
   - AGENTS.md ganha: ausência de contrato → HUMAN_DECISION_REQUIRED, nunca finding contra o Executor.

    **Isso sozinho elimina a classe de FAIL que motivou P1.**

3. Introduzir o Verifier — a correção de fundo
  Esta é a que muda a arquitetura, e é a que você já projetou em 02-ESTADO-ARQUITETURA-FINAL.md.

   >Humano → Contrato → Executor → Verifier (determinístico) → Reviewer (semântica residual) → Humano → Git

   **Regra de precedência já escrita por você:**

   >FormalResult != PASS ⟹ Reviewer não pode emitir PASS. E PASS formal não obriga PASS do Reviewer.

**O que isso resolve, concretamente:**

*O Reviewer deixa de gastar turnos recalculando "o binding bate?", "o diff saiu do escopo?", "os arquivos alterados são os declarados?" — tudo isso vira saída de script. Ele passa a gastar o turno inteiro no que só ele faz: semântica, regressão, overclaim.*

**Sequenciamento realista**:

>*o certificado FVR está NOT_ISSUED / HARNESS_INVALID (01-ESTADO-ATUAL:1.5), então não adote o runner FVR completo agora. Comece com um verificador mínimo sobre três propriedades que já causaram FAIL real: write-set respeitado, binding consistente com a matriz, contrato presente e válido. Três assertions cobrem a maioria dos findings mecânicos que você viu.*

Sobre o plugin, nesta ordem

>*O plugin fica em uso auxiliar (pré-check barato, background) e fora da porta de governança até que (1) exista Verifier e (2) /codex:adversarial-review seja invocado com as instruções do AGENTS.md injetadas explicitamente. Decisão pendente e recomendada: desabilitar codex:rescue ou registrar que Codex nunca roda com --write.*

**Uma nota sobre esta resposta:**

>*Ela é análise, não execução — nenhum arquivo foi alterado e não há diff para revisar, então não emito READY_FOR_REVIEW. O fato de eu precisar explicar isso é, ele mesmo, uma instância de P1: CLAUDE.md:68-79 define o handoff como se todo turno produzisse artefato revisável, e não há estado previsto para um turno consultivo. Vale incluir na correção do item 1.*
