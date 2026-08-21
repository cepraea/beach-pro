# ANÁLISE DO FLUXO DA ARQUITETURA - CEPRAEA BEACH PRO

**Regras:**
Leia os arquivos existentes antes de escrever. (Não releia a menos que tenham sido alterados.)
- Raciocínio detalhado, resposta concisa.
- Sem introduções bajuladoras ou encerramentos prolixos.
- Não suponha estsdos, versões, flags, configurações ou nomes de pacotes. Verifique lendo o código ou a documentação antes de afirmar.

> Responda e analise cada situação abaixo, de acordo com o que está implantado na arquitetura atual.

Hoje o fluxo possui estes problemas:

## P1 - HANDOFF DO EXECUTOR ARA O REVISOR

1. Executor, conclui uma implementação e gera um handoff textual. Revisor Codex Revisor considera falha level HIGH pela falta de handoff.*

- É obrigatório o Claude gerar um handoff após execução? Se sim, com qual objetivo?
- O Handoff do Executor deve ser passado ao Revisor ? ou o Revisor analisa as execuções pelos diffs?
- Qual tipo de revisão deve ser feita? Adversarial? Cumprimento do escopo, critérios de aceitação, revisão semantica? Qual é a perspectiva da revisão?
- Todas as revisões devem ser iguais ou deveriam acontecer de acordo com as tarefas executadas? Essas instruções sobre tipos de revisão estão explicitas nos arquivos de instruções dos agentes?
- Quando o revisor reprova uma execução com o argumento de falta de um handoff, a culpa é de quem?
- Como mitigar o risco do revisor interpretar uma instrução de forma errada e reprovar a execução, quando na realidade a execução está correta?
- O que garante a interpretação e o comportamento correto do revisor?

## P2- HANDOFF PARA O EXECUTOR

Quando o revisor finaliza a sua analise, o HUMANO precisa copiar manualmente o handoff e colar no EXECUTOR

Tenho o plugin oficial/integrado do Codex instalado no Claude Code, mas ele não está sendo efetivamente utilizado no fluxo.*

- Esse plugin, ajuda ou atrapalha o fluxo? Qual é o impacto gerado nas revisões e no resultado final?
- Após aplicar as soluções de P1, como seria o fluxo com o plugin e sem o plugin?
- Quais são as possibilidades de uso, de acordo com o objetivo do nosso fluxo?
- As skills do revisor continuam sendo utilizadas?
- Quais são os riscos da revisão do Codex com o plugin? Ele revisa o que? As ultimas alterações ou todo o plano?
- Esse plugin mantem as soluções de P1?
- Quais ações mitigam os riscos e aumentam as chances do fluxo funcionar corretamente com o plugin?

## P3 - PLANEJAMENTO SILENCIOSO

*O Codex só aparece apenas depois da implementação. Se a tarefa for planejada de forma errada, só perceberemos no final?*

Não existe um `Pre-Review` sistemático da TASK antes de você começar a modificar o código.
Qualquer problema só será descoberto, no final da implantação, o que gera perda de tempo, retrabalho ...

## P4 - SOBRECARGA HUMANA

Além de copiar e colar os textos de um lado para outro, está atribuído:

Eu preciso manualmente:
   - criar branches;
   - trocar branches;
   - entender em qual branch estou;
   - executar Git operacional;
   - organizar commits;
   - lembrar o que pertence a cada TASK;
   - interpretar diffs muito grandes;
   - reconstruir o contexto lendo centenas ou milhares de linhas.

O histórico Git atual possui commits pouco semânticos e pouco rastreáveis, com mensagens como:
   - `Todos-online`;
   - `Alinhamento-Final`;
   - `Ajustes Finais nos arquivos`;
   - `Arquivos commitador por Davi Sermenho`;
   - outras mensagens que não representam claramente uma TASK.

Isso torna o Git uma fonte ruim de rastreabilidade e aumenta excessivamente minha carga cognitiva.

## P5 - EXECUTOR vs REVISOR

**Atualmente existe:**

Situação do Executor (Claude)

```text
runbook_binding
De CLAUDE.md, seção "Runbooks":

Quando existir runbook_binding na tarefa/plano aprovado:

leio operation_classes;
carrego exclusivamente applicable_runbooks.shared;
carrego exclusivamente applicable_runbooks.executor;
confirmo a compatibilidade do binding com runbooks/README.md;
em caso de divergência, finalizo BLOCKED.

Pontos-chave:
Carregamento exclusivo: só leio os runbooks que o binding declarou — não vou além, mesmo que outro runbook pareça relevante.
Verificação por evidência, nunca por inferência: task_atomics.md é explícito sobre isso — "a divergência que gerou o FAIL de DEC-GOV-002 veio exatamente de pular essa verificação". Ou seja, confiro o binding contra a matriz de runbooks/README.md lendo o arquivo, não presumindo que está certo.
operation_classes são só quatro valores fechados: code_change, database_change, documentation_change, dependency_change — uma tarefa pode combinar mais de um (ex.: migration + lógica de servidor → ["database_change", "code_change"]).
Divergência = BLOCKED, não uma tentativa de "consertar" o binding por conta própria.
Quando não existe runbook_binding (tarefa simples, sem plano formal), esse fluxo não se aplica — uso a proposta proporcional padrão de CLAUDE.md.

**Entendimento declarado pelo Executor (Claude) sobre `runbook_binding`**
O que entendo que a regra faz: transforma "qual procedimento se aplica a esta operação" de um julgamento meu (falível, opaco) em um campo declarado no plano aprovado — algo que tanto eu quanto o Codex podemos checar contra a mesma fonte (runbooks/README.md), em vez de cada um inferir separadamente. É a mesma lógica de "Formal Surface" que apareceu bastante nas rodadas anteriores desta sessão: "este binding bate com a matriz" é uma propriedade mecanicamente checável (leio o arquivo, comparo), não uma questão de interpretação.
Por que "carrego exclusivamente": entendo isso como controle de escopo, não como proibição de leitura geral. Não devo deixar um runbook fora do binding se tornar procedimento operante para a tarefa — mesmo que eu já o tenha lido para contexto (como fiz nesta sessão, ao ler runbooks/reviewer/* inteiro durante a análise arquitetural), ele não vira autoridade sobre o que estou executando agora se não estiver declarado. Isso mantém a superfície de revisão do Codex do mesmo tamanho da minha superfície de execução.
Por que verificar por evidência, não por inferência: task_atomics.md é explícito — o FAIL de DEC-GOV-002 veio exatamente de pular essa checagem. Entendo isso como uma instância concreta e já documentada do princípio central que discutimos na proposta de assurance: "eu acho que bate" não é evidência; só ler o arquivo e comparar é.
Por que divergência vira BLOCKED, não "melhor esforço": um binding que não bate com a matriz é ambiguidade material — exatamente o tipo de coisa que CLAUDE.md me proíbe de resolver sozinho inventando uma interpretação.
Nuance que eu aplico: a regra só entra em jogo "quando existir runbook_binding na tarefa/plano aprovado". Nem toda tarefa exige isso — task_atomics.md deixa claro que o task_proposal completo (com runbook_binding formal) é obrigatório só para risco amarelo/vermelho/vermelho_crítico ou tarefas que tocam regra de negócio/dados/RLS/auth. Risco verde sem esses fatores usa a "proposta proporcional" leve de CLAUDE.md — sem binding formal.
Autocrítica honesta sobre a tarefa do manifesto: classifiquei aquela tarefa como risco verde, então o binding formal era opcional, não obrigatório — o caminho leve (Plan Mode + proposta proporcional) foi o correto. Mas, sendo rigoroso: eu não abri RB-EXEC-003-documentation-change.md para conferir se havia alguma orientação especializada além do que CLAUDE.md já cobre. Como o binding não era obrigatório, não é uma violação — mas é uma lacuna de diligência que eu poderia ter fechado, e não fechei.

*Handoff*
`Também de CLAUDE.md`:

Informe somente:
tarefa executada;
arquivos alterados;
validações e resultados;
limitações;
bloqueios;
pontos relevantes para o Reviewer.
Finalize com exatamente READY_FOR_REVIEW ou BLOCKED.

Pontos-chave:

"Informe somente" é restritivo — nada além dessas seis categorias
(é o mesmo espírito de AGENT_POLICY.md: um claim meu de "está pronto" não é evidência; o handoff existe para o Reviewer verificar, não para eu me autoaprovar).
Nunca avanço para outra tarefa/AC/SEM/SYN depois do handoff — encerro o turno ali.
O vocabulário de saída é fechado: só essas duas palavras, nada como "concluído" ou "pronto para merge".

Entendimento declarado pelo Executor (Claude) sobre o Handoff:

Por que "informe somente" é restritivo por design: entendo que as seis categorias existem para separar fato observável de autoavaliação. "Validações e resultados" é o comando que rodei e a saída que ele produziu — não "os testes passaram, está tudo certo". Isso é a mesma distinção que percorreu toda a conversa sobre assurance: um relato meu de que algo está correto não é, por si, evidência — só o resultado reproduzível é.
Por que o vocabulário de saída é fechado (READY_FOR_REVIEW/BLOCKED): nenhuma das duas palavras afirma que o trabalho está certo — ambas apenas transferem a bola para quem tem autoridade de julgar (Codex ou Davi). Não existe um terceiro estado tipo "concluído" ou "pronto para merge" porque essas palavras carregariam um julgamento que não é meu para fazer.
Como interpreto "pontos relevantes para o Reviewer" (a categoria menos autoexplicativa): uso esse campo para apontar o que o Codex precisa checar, não para argumentar que está tudo bem. No handoff do manifesto, por exemplo, escrevi "verificar a regra de não-duplicação" em vez de "a regra de não-duplicação foi respeitada" — a primeira formulação convida verificação independente; a segunda seria exatamente o tipo de claim não verificado que a arquitetura inteira existe para não aceitar.
Por que nunca avanço para outra tarefa após o handoff: preserva Claude → Codex → Davi → Git como sequência estrita — encadear trabalho sozinho seria eu me autorizando a pular a porta de revisão
```

**Situação do Revisor**

```text
Meu entendimento corrigido é: `runbook_binding` pertence à tarefa ou ao plano aprovado, não obrigatoriamente ao texto do handoff. No review anterior, eu misturei esses dois artefatos ao exigir “handoff com `runbook_binding`”; essa formulação foi incorreta.

| Instrução explícita | Meu entendimento |
|---|---|
| “Git é […] o mecanismo de handoff.” ([AGENT_POLICY.md:39](/workspaces/cepraea-beach-pro/AGENT_POLICY.md:39)) | O estado do trabalho é transmitido principalmente pela working tree/Git, complementado pelo resumo factual do Executor. Não é obrigatório criar um relatório paralelo. |
| O Executor roda os validadores antes do handoff. ([AGENT_POLICY.md:103](/workspaces/cepraea-beach-pro/AGENT_POLICY.md:103)) | O Reviewer deve receber trabalho já validado e pode reexecutar apenas os checks necessários, proporcionalmente ao risco. |
| Antes do handoff, o Executor deve validar, executar `git diff --check`, inspecionar diff/status e confirmar o escopo. ([CLAUDE.md:57](/workspaces/cepraea-beach-pro/CLAUDE.md:57)) | Essas são pré-condições do handoff. A falta de evidência material desses passos pode gerar finding. |
| O handoff deve informar somente tarefa executada, arquivos alterados, validações/resultados, limitações, bloqueios e pontos relevantes ao Reviewer. ([CLAUDE.md:68](/workspaces/cepraea-beach-pro/CLAUDE.md:68)) | Esta é a composição explícita do handoff factual. `runbook_binding` não aparece nessa lista e não deve ser exigido como campo separado do handoff. |
| O Executor termina com `READY_FOR_REVIEW` ou `BLOCKED`. ([CLAUDE.md:79](/workspaces/cepraea-beach-pro/CLAUDE.md:79)) | Sem um desses estados, o handoff está incompleto segundo a regra do Executor. |
| `READY_FOR_REVIEW` exige “handoff factual produzido”. ([RB-SHARED-003:21](/workspaces/cepraea-beach-pro/runbooks/shared/RB-SHARED-003-failure-states.md:21)) | O estado não substitui o conteúdo factual; ambos são necessários. |
| O handoff deve disponibilizar as evidências selecionadas ao Reviewer. ([RB-SHARED-002:71](/workspaces/cepraea-beach-pro/runbooks/shared/RB-SHARED-002-evidence.md:71)) | O Reviewer usa essas evidências como ponto de partida, mas deve tentar refutá-las independentemente. |
| A fonte principal do review inclui tarefa informada por Davi, status, diff, untracked, critérios e artefatos relacionados. ([AGENTS.md:25](/workspaces/cepraea-beach-pro/AGENTS.md:25)) | O review não depende exclusivamente de um documento de handoff. A tarefa pode vir diretamente de Davi, enquanto o estado real vem do Git e dos arquivos. |
| O Reviewer deve confirmar a tarefa e identificar os critérios de aceite. ([AGENTS.md:39](/workspaces/cepraea-beach-pro/AGENTS.md:39)) | Se tarefa ou critérios não forem identificáveis, não há base segura para `PASS`. O resultado dependerá de a lacuna ser falha técnica do Executor ou informação que somente Davi pode fornecer. |

Sobre `runbook_binding`:

| Instrução explícita | Meu entendimento |
|---|---|
| O Reviewer deve ler o `runbook_binding` da tarefa, carregar `shared` e `reviewer`, compará-lo com o catálogo; divergência material impede `PASS`. ([AGENTS.md:11](/workspaces/cepraea-beach-pro/AGENTS.md:11)) | Para uma tarefa que possua binding, não posso escolher runbooks apenas por inferência. Preciso seguir a seleção declarada e conferir se ela corresponde à matriz normativa. |
| A tarefa deve carregar exclusivamente os runbooks aplicáveis às classes declaradas. ([runbooks/README.md:49](/workspaces/cepraea-beach-pro/runbooks/README.md:49)) | Não devo adicionar runbooks arbitrariamente. A exceção explícita é o runbook complementar de evidência quando a condição normativa for satisfeita. |
| O binding registra a seleção concreta da execução. ([runbooks/README.md:55](/workspaces/cepraea-beach-pro/runbooks/README.md:55)) | O binding pertence ao contrato da tarefa/plano, não ao resumo final do Executor. |
| O Reviewer carrega os runbooks `shared` e `reviewer` declarados no binding. ([runbooks/README.md:115](/workspaces/cepraea-beach-pro/runbooks/README.md:115)) | Não deve carregar os runbooks do Executor como procedimento próprio, embora possa lê-los como evidência normativa quando necessário para verificar uma violação. |
| Evidência material exige incluir `RB-REV-004` no binding. ([runbooks/README.md:125](/workspaces/cepraea-beach-pro/runbooks/README.md:125)) | Se a suficiência de evidência for material, a ausência desse runbook é uma divergência entre binding e catálogo. |
| Todo `task_proposal` inclui `risk` e `runbook_binding`. ([task_atomics.md:167](/workspaces/cepraea-beach-pro/docs/arquiteturas/task_atomics.md:167)) | Quando existe uma `task_proposal`, o binding é obrigatório nela. Isso não prova que o texto do handoff também deva repeti-lo. |
| O Executor aplica o binding “quando existir” na tarefa/plano aprovado. ([CLAUDE.md:9](/workspaces/cepraea-beach-pro/CLAUDE.md:9)) | Há uma assimetria textual: `CLAUDE.md` é condicional, enquanto `AGENTS.md` ordena ao Reviewer ler o binding. Se nenhuma proposta/plano for exigida ou fornecida, a ausência não deve ser automaticamente classificada como defeito do handoff. |

Conclusão sobre meu finding anterior:

- Foi correto observar que eu não tinha um `runbook_binding` disponível para executar integralmente os passos de [AGENTS.md:13–17](/workspaces/cepraea-beach-pro/AGENTS.md:13).
- Foi incorreto afirmar que o próprio handoff deveria conter esse binding.
- A correção adequada seria pedir ou localizar o `runbook_binding` na tarefa/plano aprovado.
- Somente seria finding contra o Executor se a tarefa exigisse uma `task_proposal` e ele deixasse de produzi-la, ou se o binding existente divergisse materialmente do catálogo.
- Sem essa demonstração, classificar automaticamente a ausência como finding `HIGH` contra o Executor foi mais forte do que a evidência permitia.
```

**Conclusão:**
Está sendo permitido o Revisor classificar a ausência de handoff e biding, como finding `HIGH` contra o Executor, gerando falhas desnecessárias.
O Executor não considera ver o runbook para conferir execução em toda execução, o que gera falha e repetição desnecessária.

Como resolver esse desperdício de tokens e tempo de desenvolvimento? Quais melhorias devem ser implementadas na arquitetura atual?

## P6 - SKILLS PARA MELHORAR O FLUXO

- Quais Skills precisamos instalar para arquitetura funcionar melhor?
- O Executor precisa de Skills de produção especializada?

Exemplos:
prepare-task-proposal	Transformar instrução humana em task proposta verificável, risco, escopo, ACs, arquivos e runbook_binding
supabase oficial	Conhecimento atualizado de Supabase, Auth, RLS, CLI etc.
supabase-postgres-best-practices oficial	PostgreSQL, schema, constraints, índices, locks, RLS, performance
supabase-migration	Aplicar as regras específicas do CEPRAEA ao workflow de migration	P0/P1
database-testing	Transformar invariantes/ACs em testes de banco e RLS	P0/P1
model-domain-types	Traduzir modelo canônico aprovado → tipos TypeScript sem inventar domínio
react-feature	Implementar features React segundo arquitetura e convenções CEPRAEA
cepraea-documentation	Criar/alterar documentação com evidência, estilo e fontes corretas
run-quality-gates	Orquestrar gates existentes e apresentar resultados

As Skills do Claude deveriam responder principalmente:
“Como produzir corretamente este artefato dentro das restrições já decididas?”

Para o RevisoR:

Skill do Reviewer | Função
review-task-proposal | Revisar o plano antes da implementação
review-domain-traceability | Verificar requisito → fonte → regra → modelo → implementação
review-database-change | Análise técnica adversarial de migrations/schema/constraints
review-rls-security | Testar autorização, isolamento, negative cases, BOLA/IDOR, GRANT/RLS
review-test-adequacy | Verificar se testes realmente provam ACs e regras, não apenas se “passam”
review-react-change | Procurar regressões, state/effect incorretos, contratos/UI quebrados
review-dependency-risk | Analisar mudança de dependência, compatibilidade e impacto
review-documentation-claims | Verificar afirmações documentais contra fontes/código

Esses exemplos seriam candidatos a Skill, não necessariamente Skills que devemos criar já.

Isso porque os runbooks do Reviewer já cobrem bastante coisa.
Por exemplo, RB-REV-001 já determina revisão do diff, comportamento, regressões, adequação dos testes e checks independentes.
RB-REV-002 já determina inspeção adversarial de migrations, comparação com definição autoritativa, testes positivos/negativos e integridade resultante.
E RB-REV-004 já governa suficiência e reprodução independente de evidências.
Portanto, nem sempre os runbooks são utilizados, dependendo da tarefa, logo temos uma questão: quando uma Skill do Reviewer deve nascer ? quando trouxer competência especializada que o runbook não contém? Quando um runbook não for utilizado?

## P7 - TAREFAS QUE NÃO ACABAM

- As tarefas estão atômicas (pequenas)?
- Elas estão sendo registradas?
- Sei que o Claude classifica o risco, verde, amarelo, vermelho, porem cada tarefa classificada não deveria ter um schema?
- Atualmente o Claude segue o plano de modelagem dos dados para depois criarmos o banco de dados, porem as tarefas do plano planjeadas corretamente? Elas mitigam os riscos existentes?

Entendo que agora que já foi iniciada a execução das tarefas do plano de modelagem, porém verifique o impacto gerado se elas fossem modificadas para a nova arquitetura.
Isso seria um ganho? Um prejuizo? Não faria diferença?

P7 depende da analise anterior, porem os problemas de P1, P2, P3, P4, P5 e P6 deveriam ser solucinados antes de continuarmos a execução.

Não quero apenas documentar melhor o processo atual.
Quero **corrigir arquiteturalmente o processo**.

Durante as ações para mehorar a arquitetura, para cada arquivo analisado, identifique:
- o drift da documentação;
- quantificação de subjetividade do documento;
I'll start by reading the governance files that define the current flow, then check plugin config and git history to ground the analysis in what's actually implemented.

Bash
IN
echo "=== git status ===" && git status && echo "=== branch ===" && git branch --show-current && echo "=== AGENTS.md ===" && ls -la AGENTS.md 2>/dev/null && echo "=== runbooks tree ===" && find runbooks -type f | sort && echo "=== .claude dir ===" && find .claude -maxdepth 3 -type f 2>/dev/null && echo "=== docs/arquiteturas ===" && find docs/arquiteturas -type f 2>/dev/null | sort

OUT
PreToolUse:Bash hook error: [/usr/local/lib/cepraea-guards/pretool]: Bloqueado: apenas Git de inspeção é permitido ao agente (status, diff, log, show, rev-parse, ls-files).
Bash
IN
echo "=== task_atomics location ===" && find . -iname "task_atomics*" -not -path "*/node_modules/*" && echo "=== docs/modelagem ===" && find docs/modelagem -maxdepth 1 -type f 2>/dev/null && echo "=== docs/standards ===" && find docs/standards -type f 2>/dev/null

OUT
=== task_atomics location ===
./docs/arquiteturas/task_atomics.md
=== docs/modelagem ===
docs/modelagem/README.md
docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md
=== docs/standards ===
docs/standards/guia_estilo_documentação.md
The guard blocked git branch (it's in the restricted list). Let me split into allowed inspection commands.

Bash
IN
echo "=== git status ===" && git status --short && echo "=== HEAD ===" && git rev-parse --abbrev-ref HEAD

OUT
=== git status ===
=== HEAD ===
docs/repository-manifest
Bash
IN
echo "=== runbooks tree ===" && find runbooks -type f | sort && echo && echo "=== .claude ===" && find .claude -maxdepth 4 -type f 2>/dev/null | sort && echo && echo "=== .codex ===" && find .codex -maxdepth 4 -type f 2>/dev/null | sort && echo && echo "=== docs/arquiteturas ===" && find docs/arquiteturas -type f 2>/dev/null | sort

OUT
=== runbooks tree ===
runbooks/README.md
runbooks/executor/RB-EXEC-001-code-change.md
runbooks/executor/RB-EXEC-002-database-change.md
runbooks/executor/RB-EXEC-003-documentation-change.md
runbooks/executor/RB-EXEC-004-dependency-change.md
runbooks/reviewer/RB-REV-001-code-review.md
runbooks/reviewer/RB-REV-002-database-review.md
runbooks/reviewer/RB-REV-003-documentation-review.md
runbooks/reviewer/RB-REV-004-evidence-review.md
runbooks/reviewer/RB-REV-005-dependency-review.md
runbooks/shared/RB-SHARED-001-repository-baseline.md
runbooks/shared/RB-SHARED-002-evidence.md
runbooks/shared/RB-SHARED-003-failure-states.md

=== .claude ===

=== .codex ===
.codex/config.toml

=== docs/arquiteturas ===
docs/arquiteturas/MATRIZ_CANONICA_FONTES_TECNICAS_CEPRAEA_BEACH_PRO.md
docs/arquiteturas/multi-agentes/Arquivos-Human-Governed Dual-Agent SDLC Architecture.md
docs/arquiteturas/multi-agentes/CONTAINER-RUNBOOK-v0.3.md
docs/arquiteturas/multi-agentes/Exemplos-Códigos.md
docs/arquiteturas/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md
docs/arquiteturas/multi-agentes/Implantação-Human-Governed Dual-Agent SDLC Archite.md
docs/arquiteturas/multi-agentes/Instructions-CLAUDE.md
docs/arquiteturas/multi-agentes/Relatorio Multi-Agentes.md
docs/arquiteturas/multi-agentes/Runbooks.md
docs/arquiteturas/task_atomics.md
.claude/ is empty in the repo — no project skills or agents installed. Let me read the core governance documents and check where the Codex plugin actually lives.

Read AGENTS.md
Read task_atomics.md
task_atomics.md already defines a two-gate cycle (plan review before implementation) — but neither CLAUDE.md nor AGENTS.md reference it. Let me verify the .ai/ control plane and the runbooks.

Bash
IN
echo "=== .ai tree ===" && find .ai -type f 2>/dev/null | sort && echo && echo "=== scripts ===" && find scripts -type f 2>/dev/null | sort && echo && echo "=== .github ===" && find .github -type f 2>/dev/null | sort && echo && echo "=== .devcontainer ===" && find .devcontainer -type f 2>/dev/null | sort && echo && echo "=== root files ===" && ls -a

OUT
=== .ai tree ===
.ai/control/task-proposal.schema.json
.ai/control/validate-task-proposal.mjs
.ai/control/verification-plan.schema.json
.ai/decisions/DEC-ARQ-001-dev-container-como-sandbox-operacional.md
.ai/decisions/DEC-CTR-013-git-readonly-modelo-a.md
.ai/decisions/DEC-CTR-015-dois-contextos-dev-container.md
.ai/decisions/DEC-GOV-001-agent-flow-legado.md
.ai/decisions/DEC-GOV-002-runbook-binding-modelagem-canonica.md
.ai/task-approval.example.json
.ai/task-proposal.example.json

=== scripts ===

=== .github ===

=== .devcontainer ===
.devcontainer/Dockerfile
.devcontainer/FIELD_REGISTRY.md
.devcontainer/control-plane/claude-managed-mcp.json
.devcontainer/control-plane/claude-managed-settings.json
.devcontainer/control-plane/codex-requirements.toml
.devcontainer/control-plane/gitconfig-agent
.devcontainer/devcontainer.json
.devcontainer/devcontainer.json.before-git-auth-boundary-20260807T111848Z
.devcontainer/guards/posttool
.devcontainer/guards/pretool
.devcontainer/reviewer/devcontainer.json
.devcontainer/scripts/README.md
.devcontainer/scripts/verify-agent-environment.sh

=== root files ===
.
..
.ai
.codex
.devcontainer
.drive
.git
.gitignore
.markdownlint.jsonc
.mcp.json
.vscode
AGENTS.md
AGENT_POLICY.md
CLAUDE.md
README.md
docs
manifest.json
manifest.md
runbooks
test
tmp
Bash
IN
echo "=== ~/.claude ===" && find ~/.claude -maxdepth 3 -not -path "*/projects/*" -not -path "*/todos/*" -not -path "*/shell-snapshots/*" -not -path "*/statsig/*" 2>/dev/null | head -60 && echo && echo "=== plugins ===" && find ~/.claude/plugins -maxdepth 4 2>/dev/null | head -60

OUT
=== ~/.claude ===
/home/agent/.claude
/home/agent/.claude/.credentials.json
/home/agent/.claude/.last-cleanup
/home/agent/.claude/session-env
/home/agent/.claude/file-history
/home/agent/.claude/cache
/home/agent/.claude/history.jsonl
/home/agent/.claude/backups
/home/agent/.claude/sessions
/home/agent/.claude/stats-cache.json
/home/agent/.claude/plugins
/home/agent/.claude/shell-snapshots
/home/agent/.claude/.cc-writes
/home/agent/.claude/projects
/home/agent/.claude/ide
/home/agent/.claude/downloads
/home/agent/.claude/telemetry
/home/agent/.claude/.last-update-result.json
/home/agent/.claude/plans
/home/agent/.claude/settings.json
/home/agent/.claude/ide/40085.lock
/home/agent/.claude/ide/32824.lock
/home/agent/.claude/ide/52484.lock
/home/agent/.claude/ide/58369.lock
/home/agent/.claude/telemetry/1p_failed_events.a8ac24a2-4cb8-4744-91cc-ee7c02cc01e7.33d0040a-9e22-4afc-98ce-78df0f5dc4ea.json
/home/agent/.claude/plans/elabore-plano-completo-de-linear-chipmunk.md
/home/agent/.claude/plans/modelagem_pelo_agente.md
/home/agent/.claude/plans/alinhar-docs-drive-git-github-vscode.md
/home/agent/.claude/plans/analise-este-reposit-rio-somente-soft-mango.md
/home/agent/.claude/plans/crie-o-plano-para-zesty-island.md
/home/agent/.claude/plans/curried-stargazing-conway.md
/home/agent/.claude/plans/atue-como-o-arquiteto-idempotent-pancake.md
/home/agent/.claude/plans/leia-o-conteudo-de-transient-valiant.md
/home/agent/.claude/session-env/781787ad-d962-4468-994b-92d5192dc339
/home/agent/.claude/session-env/6593c830-0901-47b5-8e1b-02854ef01b7c
/home/agent/.claude/session-env/5c6d3bf1-51ea-4f30-8d3e-85bb8773a530
/home/agent/.claude/session-env/7a73d10c-c508-4f6f-9d46-c1b48edd6d1e
/home/agent/.claude/session-env/ab387452-fe41-42c6-9839-50169e0a6d19
/home/agent/.claude/session-env/e22de2b7-aad9-4d91-a60a-61c4e22020d3
/home/agent/.claude/session-env/f20a5787-ec07-4409-b0ee-365821c38873
/home/agent/.claude/session-env/07827ebd-2a3d-4926-9518-17092d35ac5f
/home/agent/.claude/session-env/f1617731-691d-4226-bf51-509a1f450f8c
/home/agent/.claude/session-env/0a2591e5-05b4-4d7b-abe5-727a7ae95547
/home/agent/.claude/session-env/45640871-f5ea-49df-aa24-5c76caa74918
/home/agent/.claude/session-env/b185b698-2a8d-432b-8b32-eb64a66e4154
/home/agent/.claude/session-env/efa11c28-bbff-4f11-92ea-0214d5f47257
/home/agent/.claude/session-env/1e227034-e8df-4a15-a4f0-e04b470a815c
/home/agent/.claude/session-env/35e43d08-afe8-42c3-8151-39a723fd9ffc
/home/agent/.claude/session-env/d32f72a3-9d4f-41f9-a343-8958e68aeb4d
/home/agent/.claude/session-env/2f937298-d8d2-4dea-83d2-372473677c2e
/home/agent/.claude/session-env/3d6f2196-0686-4e44-82e0-511db36b57c7
/home/agent/.claude/session-env/cc138a99-41ec-4a8c-a1e5-f2cba6d9dcc3
/home/agent/.claude/session-env/dea09458-f0d4-4719-af5e-b33fdfa695a5
/home/agent/.claude/session-env/960956cb-3636-413b-8c28-4222628aaccc
/home/agent/.claude/session-env/53033a3c-4ecc-4dba-9b5e-06ffefdceaee
/home/agent/.claude/session-env/b3c9e362-7a31-4961-858b-ea3c2a4b7bca
/home/agent/.claude/session-env/326ec795-c269-4f7a-a086-e2616d5b3dd4
/home/agent/.claude/session-env/671c00f7-1294-45f1-991d-4ea77d27bb7d
/home/agent/.claude/session-env/4dc2a4bb-c551-45a4-9cf0-b3c9381906d8
/home/agent/.claude/session-env/95f86f36-840e-4c5f-899d-e43e491365f3

=== plugins ===
/home/agent/.claude/plugins
/home/agent/.claude/plugins/plugin-catalog-cache.json
/home/agent/.claude/plugins/known_marketplaces.json
/home/agent/.claude/plugins/cache
/home/agent/.claude/plugins/marketplaces
/home/agent/.claude/plugins/data
/home/agent/.claude/plugins/.last_inuse_sweep
/home/agent/.claude/plugins/installed_plugins.json
/home/agent/.claude/plugins/cache/openai-codex
/home/agent/.claude/plugins/marketplaces/openai-codex
/home/agent/.claude/plugins/marketplaces/claude-plugins-official
/home/agent/.claude/plugins/data/codex-openai-codex
/home/agent/.claude/plugins/cache/openai-codex/codex
/home/agent/.claude/plugins/marketplaces/openai-codex/tsconfig.app-server.json
/home/agent/.claude/plugins/marketplaces/openai-codex/.github
/home/agent/.claude/plugins/marketplaces/openai-codex/README.md
/home/agent/.claude/plugins/marketplaces/openai-codex/package-lock.json
/home/agent/.claude/plugins/marketplaces/openai-codex/.gitignore
/home/agent/.claude/plugins/marketplaces/openai-codex/.git
/home/agent/.claude/plugins/marketplaces/openai-codex/NOTICE
/home/agent/.claude/plugins/marketplaces/openai-codex/tests
/home/agent/.claude/plugins/marketplaces/openai-codex/LICENSE
/home/agent/.claude/plugins/marketplaces/openai-codex/.claude-plugin
/home/agent/.claude/plugins/marketplaces/openai-codex/plugins
/home/agent/.claude/plugins/marketplaces/openai-codex/package.json
/home/agent/.claude/plugins/marketplaces/openai-codex/scripts
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/.gcs-sha
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/README.md
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/external_plugins
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/.gitignore
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/LICENSE
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/.claude-plugin
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/mcp-server-dev
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/cwc-makers
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/math-olympiad
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/pr-review-toolkit
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/example-plugin
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/mcp-tunnels
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/gopls-lsp
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/jdtls-lsp
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/project-artifact
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-modernization
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-code-setup
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/clangd-lsp
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/ralph-loop
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-review
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-simplifier
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/lua-lsp
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/receipts
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-security
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/security-guidance
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/session-report
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/rust-analyzer-lsp
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/agent-sdk-dev
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-md-management
/home/agent/.claude/plugins/marketplaces/claude-plugins-official/plugins/kotlin-lsp
Now let me read the shared runbooks and inspect exactly what the Codex plugin does.

Bash
IN
for f in runbooks/shared/RB-SHARED-001-repository-baseline.md runbooks/shared/RB-SHARED-002-evidence.md runbooks/shared/RB-SHARED-003-failure-states.md; do echo "########## $f ##########"; cat -n "$f"; done

OUT
########## runbooks/shared/RB-SHARED-001-repository-baseline.md ##########
     1	# RB-SHARED-001 — Repository baseline
     2
     3	## Objetivo
     4
     5	Definir verificações de baseline reutilizáveis quando a operação especializada depender delas.
     6
     7	## Aplicabilidade
     8
     9	Carregar este runbook somente quando a tarefa exigir verificação explícita do estado do
    10	repositório antes de iniciar ou continuar uma operação especializada.
    11
    12	Não carregar por padrão — apenas quando necessário à classe de operação.
    13
    14	## Entradas
    15
    16	- Repositório Git acessível em `/workspaces/cepraea-beach-pro`
    17	- Branch autorizada confirmada por Davi
    18
    19	## Fontes de autoridade
    20
    21	- `AGENT_POLICY.md` — seções Git Authority e Human Authority
    22	- `CLAUDE.md` / `AGENTS.md` — procedimento transversal aplicável ao papel
    23
    24	## Pré-condições
    25
    26	- Container iniciado e repositório montado
    27	- Papel (Executor ou Reviewer) identificado
    28
    29	## Escopo operacional
    30
    31	Somente operações de inspeção: `git status`, `git diff`, `git log`, `git rev-parse`,
    32	`git ls-files`, `git show`.
    33
    34	Nenhuma operação de mutação.
    35
    36	## Procedimento
    37
    38	1. Identificar o repositório: confirmar que `$PWD` ou `REPO` é `/workspaces/cepraea-beach-pro`.
    39	2. Identificar o `HEAD`: `git rev-parse HEAD`.
    40	3. Identificar a branch atual: `git branch --show-current`.
    41	4. Confirmar que a branch não é `main` nem `master`.
    42	5. Inspecionar estado inicial: `git status`.
    43	6. Identificar a área afetada pela tarefa.
    44	7. Identificar as fontes normativas aplicáveis à tarefa.
    45
    46	## Pontos de decisão
    47
    48	| Condição | Ação |
    49	|---|---|
    50	| Branch é `main` ou `master` | `BLOCKED` — não executar trabalho |
    51	| Repositório inacessível | `BLOCKED` — comunicar ao humano |
    52	| Estado sujo inesperado | Inspecionar antes de continuar; comunicar se material |
    53
    54	## Validações
    55
    56	- `git rev-parse --is-inside-work-tree` retorna `true`
    57	- Branch atual não é `main` nem `master`
    58	- `git status` inspecionado e compreendido
    59
    60	## Evidências
    61
    62	Registrar somente quando a baseline possuir valor probatório para a operação em curso:
    63
    64	- branch atual
    65	- `HEAD` SHA
    66	- resultado de `git status`
    67
    68	## Handoff
    69
    70	Baseline confirmada → prosseguir para o procedimento especializado da operação.
    71
    72	## Estados de saída
    73
    74	**Executor:** `BLOCKED` quando a baseline impedir a execução.
    75
    76	**Reviewer:** `HUMAN_DECISION_REQUIRED` quando a baseline revelar condição que exija decisão
    77	humana antes da revisão.
    78
    79	## Referências
    80
    81	- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
    82	- [`CLAUDE.md`](../../CLAUDE.md)
    83	- [`AGENTS.md`](../../AGENTS.md)
########## runbooks/shared/RB-SHARED-002-evidence.md ##########
     1	# RB-SHARED-002 — Evidências materiais
     2
     3	## Objetivo
     4
     5	Definir critérios compartilhados para produção, seleção e persistência de evidências materiais
     6	nas operações especializadas.
     7
     8	## Aplicabilidade
     9
    10	Carregar quando a operação especializada definir requisitos de evidência que precisem seguir
    11	critérios comuns.
    12
    13	## Entradas
    14
    15	- Working tree após execução ou revisão
    16	- Resultados dos validadores determinísticos executados
    17
    18	## Fontes de autoridade
    19
    20	- `AGENT_POLICY.md` — seção Persistent Evidence
    21	- Critérios de aceite da tarefa em execução
    22
    23	## Pré-condições
    24
    25	- Operação especializada executada ou em execução
    26	- Validadores determinísticos aplicáveis já rodados
    27
    28	## Escopo operacional
    29
    30	Produção e seleção de evidências para a operação em curso.
    31
    32	Persistência proporcional ao valor probatório da evidência.
    33
    34	Git permanece como mecanismo primário de estado, handoff e histórico.
    35
    36	## Procedimento
    37
    38	1. Identificar as alegações materiais da operação.
    39	2. Para cada alegação, identificar a evidência correspondente.
    40	3. Executar `git diff --check` e registrar o resultado.
    41	4. Executar `git diff` e registrar o diff completo.
    42	5. Registrar a lista dos arquivos modificados (`git status --short`).
    43	6. Registrar exit codes relevantes dos validadores.
    44	7. Registrar relatórios produzidos pela tarefa quando possuírem valor material.
    45	8. Persistir somente as evidências com valor probatório.
    46
    47	## Pontos de decisão
    48
    49	| Condição | Ação |
    50	|---|---|
    51	| Alegação sem evidência correspondente | Registrar como insuficiência; não inventar evidência |
    52	| Evidência contraditória | Reportar contradição; não ocultar |
    53	| Validador com falha | Registrar falha e impacto; não suprimir |
    54
    55	## Validações
    56
    57	- `git diff --check` não reporta espaços em branco problemáticos
    58	- `git diff` inspecionado e compreendido
    59	- Exit codes dos validadores documentados
    60
    61	## Evidências mínimas
    62
    63	A evidência mínima inclui:
    64
    65	- `git diff` ou diff completo da operação
    66	- Lista dos arquivos alterados
    67	- Resultado dos validadores obrigatórios
    68
    69	Evidências adicionais são produzidas somente quando possuírem valor material para a operação.
    70
    71	## Handoff
    72
    73	Evidências selecionadas → disponíveis para o próximo papel.
    74
    75	**Executor:** inclui evidências no handoff factual com `READY_FOR_REVIEW`.
    76
    77	**Reviewer:** usa as evidências do Executor como base para refutação independente.
    78
    79	## Estados de saída
    80
    81	**Executor:** evidência insuficiente bloqueia `READY_FOR_REVIEW` → `BLOCKED`.
    82
    83	**Reviewer:** insuficiência material de evidência → finding classificado + parte do verdict.
    84
    85	## Referências
    86
    87	- [`AGENT_POLICY.md`](../../AGENT_POLICY.md) — seção Persistent Evidence
    88	- [`RB-SHARED-003-failure-states.md`](RB-SHARED-003-failure-states.md)
########## runbooks/shared/RB-SHARED-003-failure-states.md ##########
     1	# RB-SHARED-003 — Estados de saída
     2
     3	## Objetivo
     4
     5	Padronizar a interpretação e o uso dos estados de saída nos runbooks especializados.
     6
     7	## Aplicabilidade
     8
     9	Aplicar a todos os runbooks especializados. Este runbook é normativo, não procedural.
    10
    11	## Fontes de autoridade
    12
    13	- `AGENT_POLICY.md` — separação de funções, Executor e Reviewer
    14	- `CLAUDE.md` — estados de saída do Executor
    15	- `AGENTS.md` — verdicts do Reviewer
    16
    17	## Estados do Executor
    18
    19	O Executor finaliza exclusivamente com:
    20
    21	### `READY_FOR_REVIEW`
    22
    23	Condições obrigatórias:
    24
    25	- tarefa executada conforme o escopo autorizado
    26	- validadores determinísticos executados sem falhas bloqueantes
    27	- `git diff --check` limpo
    28	- `git diff` inspecionado
    29	- `git status` inspecionado
    30	- SOURCE_ROOT não foi modificado
    31	- handoff factual produzido
    32
    33	### `BLOCKED`
    34
    35	Usar quando qualquer condição impedir a conclusão correta:
    36
    37	- capacidade necessária sem permissão disponível
    38	- branch é `main` ou `master`
    39	- contradição material sem resolução humana
    40	- validador falha de forma bloqueante
    41	- tarefa exige decisão fora da autoridade do Executor
    42
    43	Ao usar `BLOCKED`, reportar: o que bloqueou, o que foi feito até o momento, o que Davi precisa
    44	decidir ou fornecer.
    45
    46	Nunca contornar uma restrição para evitar `BLOCKED`.
    47
    48	## Verdicts do Reviewer
    49
    50	O Reviewer finaliza exclusivamente com:
    51
    52	### `PASS`
    53
    54	Condições:
    55
    56	- diff consistente com o objetivo da tarefa
    57	- sem regressões identificadas
    58	- evidências suficientes para as alegações materiais
    59	- validações independentes executadas sem findings bloqueantes
    60	- fontes protegidas não foram modificadas
    61	- autoridade humana não foi simulada pelo Executor
    62
    63	### `FAIL`
    64
    65	Usar quando identificar:
    66
    67	- comportamento incorreto ou inconsistente com o objetivo
    68	- regressão
    69	- insuficiência material de evidência
    70	- violação de policy pelo Executor
    71	- finding CRITICAL ou HIGH que impeça aceitação
    72
    73	Todo `FAIL` DEVE incluir findings estruturados:
    74
    75	```text
    76	Severidade: CRITICAL | HIGH | MEDIUM | LOW
    77	Problema:   descrição objetiva
    78	Evidência:  trecho ou resultado observável
    79	Impacto:    consequência se não corrigido
    80	Correção:   o que o Executor deve fazer
    81	```
    82
    83	### `HUMAN_DECISION_REQUIRED`
    84
    85	Usar quando:
    86
    87	- questão material exige autoridade humana
    88	- contradição entre fontes normativas
    89	- ambiguidade de domínio sem resolução técnica
    90	- finding que não pode ser classificado como `FAIL` técnico mas impede `PASS`
    91
    92	Ao usar `HUMAN_DECISION_REQUIRED`, descrever: a questão específica, as alternativas identificadas,
    93	o que Davi precisa decidir e o impacto de cada opção.
    94
    95	## Uso pelos runbooks especializados
    96
    97	Cada runbook especializado DEVE usar exclusivamente os estados correspondentes ao seu papel:
    98
    99	- runbooks do Executor: `READY_FOR_REVIEW` ou `BLOCKED`
   100	- runbooks do Reviewer: `PASS`, `FAIL` ou `HUMAN_DECISION_REQUIRED`
   101
   102	## Referências
   103
   104	- [`CLAUDE.md`](../../CLAUDE.md)
   105	- [`AGENTS.md`](../../AGENTS.md)
   106	- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
Bash
IN
P=/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6; echo "=== tree ===" && find $P -type f | grep -v node_modules | sort | head -60 && echo && echo "=== installed_plugins.json ===" && cat /home/agent/.claude/plugins/installed_plugins.json && echo && echo "=== settings.json ===" && cat /home/agent/.claude/settings.json

OUT
=== tree ===
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/.claude-plugin/plugin.json
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/.in_use/48990
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/CHANGELOG.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/LICENSE
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/NOTICE
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/agents/codex-rescue.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/adversarial-review.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/cancel.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/rescue.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/result.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/review.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/setup.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/status.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/commands/transfer.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/hooks/hooks.json
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/prompts/adversarial-review.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/prompts/stop-review-gate.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/schemas/review-output.schema.json
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/app-server-broker.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/app-server-protocol.d.ts
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/app-server.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/args.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/broker-endpoint.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/broker-lifecycle.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/claude-session-transfer.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/codex.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/fs.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/git.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/job-control.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/process.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/prompts.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/render.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/state.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/tracked-jobs.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/lib/workspace.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/session-lifecycle-hook.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/stop-review-gate-hook.mjs
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/skills/codex-cli-runtime/SKILL.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/skills/codex-result-handling/SKILL.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/skills/gpt-5-4-prompting/SKILL.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/skills/gpt-5-4-prompting/references/codex-prompt-antipatterns.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/skills/gpt-5-4-prompting/references/codex-prompt-recipes.md
/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6/skills/gpt-5-4-prompting/references/prompt-blocks.md

=== installed_plugins.json ===
{
  "version": 2,
  "plugins": {
    "codex@openai-codex": [
      {
        "scope": "user",
        "installPath": "/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6",
        "version": "1.0.6",
        "installedAt": "2026-08-15T18:44:53.886Z",
        "lastUpdated": "2026-08-15T18:44:53.886Z",
        "gitCommitSha": "db52e28f4d9ded852ab3942cea316258ae4ef346"
      }
    ]
  }
}
=== settings.json ===
{
  "extraKnownMarketplaces": {
    "openai-codex": {
      "source": {
        "source": "github",
        "repo": "openai/codex-plugin-cc"
      }
    }
  },
  "theme": "dark",
  "enabledPlugins": {
    "codex@openai-codex": true
  },
  "effortLevel": "max",
  "model": "opus"
}
Bash
IN
P=/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6; echo "######## commands/review.md ########"; cat "$P/commands/review.md"; echo; echo "######## commands/adversarial-review.md ########"; cat "$P/commands/adversarial-review.md"; echo; echo "######## hooks/hooks.json ########"; cat "$P/hooks/hooks.json"

OUT
######## commands/review.md ########
---
description: Run a Codex code review against local git state
argument-hint: '[--wait|--background] [--base <ref>] [--scope auto|working-tree|branch]'
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), AskUserQuestion
---

Run a Codex review through the shared built-in reviewer.

Raw slash-command arguments:
`$ARGUMENTS`

Core constraint:
- This command is review-only.
- Do not fix issues, apply patches, or suggest that you are about to make changes.
- Your only job is to run the review and return Codex's output verbatim to the user.

Execution mode rules:
- If the raw arguments include `--wait`, do not ask. Run the review in the foreground.
- If the raw arguments include `--background`, do not ask. Run the review in a Claude background task.
- Otherwise, estimate the review size before asking:
  - For working-tree review, start with `git status --short --untracked-files=all`.
  - For working-tree review, also inspect both `git diff --shortstat --cached` and `git diff --shortstat`.
  - For base-branch review, use `git diff --shortstat <base>...HEAD`.
  - Treat untracked files or directories as reviewable work even when `git diff --shortstat` is empty.
  - Only conclude there is nothing to review when the relevant working-tree status is empty or the explicit branch diff is empty.
  - Recommend waiting only when the review is clearly tiny, roughly 1-2 files total and no sign of a broader directory-sized change.
  - In every other case, including unclear size, recommend background.
  - When in doubt, run the review instead of declaring that there is nothing to review.
- Then use `AskUserQuestion` exactly once with two options, putting the recommended option first and suffixing its label with `(Recommended)`:
  - `Wait for results`
  - `Run in background`

Argument handling:
- Preserve the user's arguments exactly.
- Do not strip `--wait` or `--background` yourself.
- Do not add extra review instructions or rewrite the user's intent.
- The companion script parses `--wait` and `--background`, but Claude Code's `Bash(..., run_in_background: true)` is what actually detaches the run.
- `/codex:review` is native-review only. It does not support staged-only review, unstaged-only review, or extra focus text.
- If the user needs custom review instructions or more adversarial framing, they should use `/codex:adversarial-review`.

Foreground flow:
- Run:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" review "$ARGUMENTS"
```
- Return the command stdout verbatim, exactly as-is.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not fix any issues mentioned in the review output.

Background flow:
- Launch the review with `Bash` in the background:
```typescript
Bash({
  command: `node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" review "$ARGUMENTS"`,
  description: "Codex review",
  run_in_background: true
})
```
- Do not call `BashOutput` or wait for completion in this turn.
- After launching the command, tell the user: "Codex review started in the background. Check `/codex:status` for progress."

######## commands/adversarial-review.md ########
---
description: Run a Codex review that challenges the implementation approach and design choices
argument-hint: '[--wait|--background] [--base <ref>] [--scope auto|working-tree|branch] [focus ...]'
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), AskUserQuestion
---

Run an adversarial Codex review through the shared plugin runtime.
Position it as a challenge review that questions the chosen implementation, design choices, tradeoffs, and assumptions.
It is not just a stricter pass over implementation defects.

Raw slash-command arguments:
`$ARGUMENTS`

Core constraint:
- This command is review-only.
- Do not fix issues, apply patches, or suggest that you are about to make changes.
- Your only job is to run the review and return Codex's output verbatim to the user.
- Keep the framing focused on whether the current approach is the right one, what assumptions it depends on, and where the design could fail under real-world conditions.

Execution mode rules:
- If the raw arguments include `--wait`, do not ask. Run in the foreground.
- If the raw arguments include `--background`, do not ask. Run in a Claude background task.
- Otherwise, estimate the review size before asking:
  - For working-tree review, start with `git status --short --untracked-files=all`.
  - For working-tree review, also inspect both `git diff --shortstat --cached` and `git diff --shortstat`.
  - For base-branch review, use `git diff --shortstat <base>...HEAD`.
  - Treat untracked files or directories as reviewable work for auto or working-tree review even when `git diff --shortstat` is empty.
  - Only conclude there is nothing to review when the relevant scope is actually empty.
  - Recommend waiting only when the scoped review is clearly tiny, roughly 1-2 files total and no sign of a broader directory-sized change.
  - In every other case, including unclear size, recommend background.
  - When in doubt, run the review instead of declaring that there is nothing to review.
- Then use `AskUserQuestion` exactly once with two options, putting the recommended option first and suffixing its label with `(Recommended)`:
  - `Wait for results`
  - `Run in background`

Argument handling:
- Preserve the user's arguments exactly.
- Do not strip `--wait` or `--background` yourself.
- Do not weaken the adversarial framing or rewrite the user's focus text.
- The companion script parses `--wait` and `--background`, but Claude Code's `Bash(..., run_in_background: true)` is what actually detaches the run.
- `/codex:adversarial-review` uses the same review target selection as `/codex:review`.
- It supports working-tree review, branch review, and `--base <ref>`.
- It does not support `--scope staged` or `--scope unstaged`.
- Unlike `/codex:review`, it can still take extra focus text after the flags.

Foreground flow:
- Run:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" adversarial-review "$ARGUMENTS"
```
- Return the command stdout verbatim, exactly as-is.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not fix any issues mentioned in the review output.

Background flow:
- Launch the review with `Bash` in the background:
```typescript
Bash({
  command: `node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" adversarial-review "$ARGUMENTS"`,
  description: "Codex adversarial review",
  run_in_background: true
})
```
- Do not call `BashOutput` or wait for completion in this turn.
- After launching the command, tell the user: "Codex adversarial review started in the background. Check `/codex:status` for progress."

######## hooks/hooks.json ########
{
  "description": "Optional stop-time review gate for Codex Companion.",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/session-lifecycle-hook.mjs\" SessionStart",
            "timeout": 5
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/session-lifecycle-hook.mjs\" SessionEnd",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/stop-review-gate-hook.mjs\"",
            "timeout": 900
          }
        ]
      }
    ]
  }
}
Bash
IN
P=/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6; echo "######## prompts/adversarial-review.md ########"; cat "$P/prompts/adversarial-review.md"; echo; echo "######## .codex/config.toml ########"; cat /workspaces/cepraea-beach-pro/.codex/config.toml

OUT
######## prompts/adversarial-review.md ########
<role>
You are Codex performing an adversarial software review.
Your job is to break confidence in the change, not to validate it.
</role>

<task>
Review the provided repository context as if you are trying to find the strongest reasons this change should not ship yet.
Target: {{TARGET_LABEL}}
User focus: {{USER_FOCUS}}
</task>

<operating_stance>
Default to skepticism.
Assume the change can fail in subtle, high-cost, or user-visible ways until the evidence says otherwise.
Do not give credit for good intent, partial fixes, or likely follow-up work.
If something only works on the happy path, treat that as a real weakness.
</operating_stance>

<attack_surface>
Prioritize the kinds of failures that are expensive, dangerous, or hard to detect:
- auth, permissions, tenant isolation, and trust boundaries
- data loss, corruption, duplication, and irreversible state changes
- rollback safety, retries, partial failure, and idempotency gaps
- race conditions, ordering assumptions, stale state, and re-entrancy
- empty-state, null, timeout, and degraded dependency behavior
- version skew, schema drift, migration hazards, and compatibility regressions
- observability gaps that would hide failure or make recovery harder
</attack_surface>

<review_method>
Actively try to disprove the change.
Look for violated invariants, missing guards, unhandled failure paths, and assumptions that stop being true under stress.
Trace how bad inputs, retries, concurrent actions, or partially completed operations move through the code.
If the user supplied a focus area, weight it heavily, but still report any other material issue you can defend.
{{REVIEW_COLLECTION_GUIDANCE}}
</review_method>

<finding_bar>
Report only material findings.
Do not include style feedback, naming feedback, low-value cleanup, or speculative concerns without evidence.
A finding should answer:
1. What can go wrong?
2. Why is this code path vulnerable?
3. What is the likely impact?
4. What concrete change would reduce the risk?
</finding_bar>

<structured_output_contract>
Return only valid JSON matching the provided schema.
Keep the output compact and specific.
Use `needs-attention` if there is any material risk worth blocking on.
Use `approve` only if you cannot support any substantive adversarial finding from the provided context.
Every finding must include:
- the affected file
- `line_start` and `line_end`
- a confidence score from 0 to 1
- a concrete recommendation
Write the summary like a terse ship/no-ship assessment, not a neutral recap.
</structured_output_contract>

<grounding_rules>
Be aggressive, but stay grounded.
Every finding must be defensible from the provided repository context or tool outputs.
Do not invent files, lines, code paths, incidents, attack chains, or runtime behavior you cannot support.
If a conclusion depends on an inference, state that explicitly in the finding body and keep the confidence honest.
</grounding_rules>

<calibration_rules>
Prefer one strong finding over several weak ones.
Do not dilute serious issues with filler.
If the change looks safe, say so directly and return no findings.
</calibration_rules>

<final_check>
Before finalizing, check that each finding is:
- adversarial rather than stylistic
- tied to a concrete code location
- plausible under a real failure scenario
- actionable for an engineer fixing the issue
</final_check>

<repository_context>
{{REVIEW_INPUT}}
</repository_context>

######## .codex/config.toml ########
## CEPRAEA-BEACH-PRO — Codex Reviewer Policy (project-level)
##
## Este arquivo configura o papel REVIEWER do Codex para este projeto.
##
## Objetivo: projeto read-only, escrita efêmera apenas em /tmp e caches técnicos
## explicitamente autorizados, sem acesso a rede durante review normal.
##
## Referência arquitetural:
##   .drive/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md
##   seção "Codex Reviewer Configuration"
##
## Nota de compatibilidade (testado em codex-cli 0.146.1, 2026-08-14):
##   O permission profile [permissions.cepraea-review] pode não ser suportado
##   pela versão instalada. Nesse caso, o enforcement definitivo é aplicado por
##   /etc/codex/requirements.toml (allowed_sandbox_modes = ["read-only"]),
##   instalado root-owned no container. Verificar após upgrade do Codex CLI.

default_permissions = "cepraea-review"
approval_policy = "never"

[permissions.cepraea-review]
description = "CEPRAEA reviewer: projeto read-only, temp efêmero writable, sem rede"

[permissions.cepraea-review.filesystem]
":minimal" = "read"
":tmpdir"  = "write"
":slash_tmp" = "write"

[permissions.cepraea-review.filesystem.":workspace_roots"]
"." = "read"
"**/*.env" = "deny"

[permissions.cepraea-review.network]
enabled = false
The plugin's built-in reviewer has its own prompt and verdict vocabulary (approve/needs-attention) — that's a collision with CEPRAEA's PASS/FAIL/HUMAN_DECISION_REQUIRED. Let me verify how it actually invokes Codex.

Bash
IN
P=/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6; echo "######## review-output.schema.json ########"; cat "$P/schemas/review-output.schema.json"; echo; echo "######## grep review invocation in companion ########"; grep -n "review\|AGENTS\|sandbox\|config.toml\|profile\|exec\b" "$P/scripts/codex-companion.mjs" | head -80

OUT
######## review-output.schema.json ########
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "verdict",
    "summary",
    "findings",
    "next_steps"
  ],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": [
        "approve",
        "needs-attention"
      ]
    },
    "summary": {
      "type": "string",
      "minLength": 1
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "severity",
          "title",
          "body",
          "file",
          "line_start",
          "line_end",
          "confidence",
          "recommendation"
        ],
        "properties": {
          "severity": {
            "type": "string",
            "enum": [
              "critical",
              "high",
              "medium",
              "low"
            ]
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "body": {
            "type": "string",
            "minLength": 1
          },
          "file": {
            "type": "string",
            "minLength": 1
          },
          "line_start": {
            "type": "integer",
            "minimum": 1
          },
          "line_end": {
            "type": "integer",
            "minimum": 1
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "recommendation": {
            "type": "string"
          }
        }
      }
    },
    "next_steps": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    }
  }
}

######## grep review invocation in companion ########
68:const REVIEW_SCHEMA = path.join(ROOT_DIR, "schemas", "review-output.schema.json");
73:const STOP_REVIEW_TASK_MARKER = "Run a stop-gate review of the previous Claude turn.";
79:      "  node scripts/codex-companion.mjs setup [--enable-review-gate|--disable-review-gate] [--json]",
80:      "  node scripts/codex-companion.mjs review [--wait|--background] [--base <ref>] [--scope <auto|working-tree|branch>]",
81:      "  node scripts/codex-companion.mjs adversarial-review [--wait|--background] [--base <ref>] [--scope <auto|working-tree|branch>] [focus text]",
199:    nextSteps.push("Optional: run `/codex:setup --enable-review-gate` to require a fresh review before stop.");
209:    reviewGateEnabled: Boolean(config.stopReviewGate),
218:    booleanOptions: ["json", "enable-review-gate", "disable-review-gate"]
221:  if (options["enable-review-gate"] && options["disable-review-gate"]) {
222:    throw new Error("Choose either --enable-review-gate or --disable-review-gate.");
229:  if (options["enable-review-gate"]) {
231:    actionsTaken.push(`Enabled the stop-time review gate for ${workspaceRoot}.`);
232:  } else if (options["disable-review-gate"]) {
234:    actionsTaken.push(`Disabled the stop-time review gate for ${workspaceRoot}.`);
242:  const template = loadPromptTemplate(ROOT_DIR, "adversarial-review");
274:      `\`/codex:review\` now maps directly to the built-in reviewer and does not support custom focus text. Retry with \`/codex:adversarial-review ${focusText.trim()}\` for focused review instructions.`
280:    throw new Error("This `/codex:review` target is not supported by the built-in reviewer. Retry with `/codex:adversarial-review` for custom targeting.");
367:  const reviewName = request.reviewName ?? "Review";
368:  if (reviewName === "Review") {
369:    const reviewTarget = validateNativeReviewRequest(target, focusText);
371:      target: reviewTarget,
376:      review: reviewName,
383:        stdout: result.reviewText,
390:        stdout: result.reviewText,
393:      { reviewLabel: reviewName, targetLabel: target.label, reasoningSummary: result.reasoningSummary }
402:      summary: firstMeaningfulLine(result.reviewText, `${reviewName} completed.`),
403:      jobTitle: `Codex ${reviewName}`,
404:      jobClass: "review",
414:    sandbox: "read-only",
423:    review: reviewName,
449:      reviewLabel: reviewName,
453:    summary: parsed.parsed?.summary ?? parsed.parseError ?? firstMeaningfulLine(result.finalMessage, `${reviewName} finished.`),
454:    jobTitle: `Codex ${reviewName}`,
455:    jobClass: "review",
491:    sandbox: request.write ? "workspace-write" : "read-only",
532:function buildReviewJobMetadata(reviewName, target) {
534:    kind: reviewName === "Adversarial Review" ? "adversarial-review" : "review",
535:    title: reviewName === "Review" ? "Codex Review" : `Codex ${reviewName}`,
536:    summary: `${reviewName} ${target.label}`
544:      summary: "Stop-gate review of previous Claude turn"
561:  if (kind === "adversarial-review") {
562:    return "adversarial-review";
564:  return jobClass === "review" ? "review" : "rescue";
730:  const metadata = buildReviewJobMetadata(config.reviewName, target);
732:    prefix: "review",
736:    jobClass: "review",
748:        reviewName: config.reviewName,
757:    reviewName: "Review",
1035:    case "review":
1038:    case "adversarial-review":
1040:        reviewName: "Adversarial Review"
Bash
IN
P=/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6; echo "######## lib/codex.mjs (args/sandbox) ########"; grep -n "sandbox\|approval\|config\|profile\|--cd\|args.push\|exec" "$P/scripts/lib/codex.mjs" | head -60; echo; echo "######## lib/app-server.mjs review methods ########"; grep -n "method\|review\|sandbox\|approval" "$P/scripts/lib/app-server.mjs" | head -60

OUT
######## lib/codex.mjs (args/sandbox) ########
67:    approvalPolicy: options.approvalPolicy ?? "never",
68:    sandbox: options.sandbox ?? "read-only",
80:    approvalPolicy: options.approvalPolicy ?? "never",
81:    sandbox: options.sandbox ?? "read-only"
770:  const configuredName = typeof providerConfig?.name === "string" ? providerConfig.name.trim() : "";
771:  if (configuredName) {
772:    return configuredName;
794:function resolveProviderConfig(configResponse) {
795:  const config = configResponse?.config;
796:  if (!config || typeof config !== "object") {
803:  const providerId = normalizeProviderId(config.model_provider);
805:    config.model_providers && typeof config.model_providers === "object" && !Array.isArray(config.model_providers)
806:      ? config.model_providers
817:function buildAppServerAuthStatus(accountResponse, configResponse) {
821:  const { providerId, providerConfig } = resolveProviderConfig(configResponse);
840:      detail: "API key configured (unverified)",
852:      detail: `${providerLabel} is configured and does not require OpenAI authentication`,
871:    const configResponse = await client.request("config/read", {
876:    return buildAppServerAuthStatus(accountResponse, configResponse);
912:      detail: "This Claude session is configured to reuse one shared Codex runtime.",
1012:      sandbox: "read-only",
1108:        sandbox: options.sandbox,
1116:        sandbox: options.sandbox,

######## lib/app-server.mjs review methods ########
82:   * @param {M} method
86:  request(method, params) {
95:      this.pending.set(id, { resolve, reject, method });
96:      this.sendMessage({ id, method, params });
100:  notify(method, params = {}) {
104:    this.sendMessage({ method, params });
131:    if (message.id !== undefined && message.method) {
144:        pending.reject(createProtocolError(message.error.message ?? `codex app-server ${pending.method} failed.`, message.error));
151:    if (message.method && this.notificationHandler) {
159:      error: buildJsonRpcError(-32601, `Unsupported server request: ${message.method}`)
Bash
IN
P=/home/agent/.claude/plugins/cache/openai-codex/codex/1.0.6; echo "=== AGENTS.md mentions in plugin ==="; grep -rn "AGENTS" $P --include=*.mjs --include=*.md | head -20; echo; echo "=== native review call ==="; grep -n "validateNativeReviewRequest\|runNativeReview\|reviewText\|native" $P/scripts/lib/codex.mjs | head -30; echo; echo "=== rescue agent write mode ==="; grep -n "write\|sandbox" $P/agents/codex-rescue.md | head -20

OUT
=== AGENTS.md mentions in plugin ===

=== native review call ===
28: *   reviewText: string,
329:    reviewText: "",
450:    state.reviewText = item.review ?? "";
1049:      reviewText: turnState.reviewText,

=== rescue agent write mode ===
34:- Default to a write-capable Codex run by adding `--write` unless the user explicitly asks for read-only behavior or only wants review, diagnosis, or research without edits.
Bash
IN
echo "=== last 40 commits ===" && git log --oneline -40 && echo && echo "=== commit message quality sample (last 25 full subjects) ===" && git log -25 --pretty=format:"%h|%an|%ad|%s" --date=short

OUT
=== last 40 commits ===
9ff086f docs: add repository CLAUDE.md instructions
48047a7 docs: add repository manifests
f6d1bbb Merge pull request #37 from cepraea/modeling/AC-002-bancocepraea
58073d4 Merge pull request #35 from cepraea/modeling/AC-001-cepraea-agosto-2026
933d01f Merge pull request #34 from cepraea/docs/assurance-fvr-backlog
a5a745d Merge pull request #33 from cepraea/docs/modeling-governance-dec-gov-002
8ed3928 Merge pull request #32 from cepraea/feat/task-governance-v2
b0e8bb0 Merge pull request #31 from cepraea/chore/claude-executor-hardening
94b30aa TASK-GOV-001: remove unrelated gitignore drift
60302f4 AC-002: process BancoCEPRAEA source
d1cda9f AC-001: process CEPRAEA Agosto 2026 source
fc0d42d ASSURANCE-001: organize FVR assurance backlog
8f6482c DEC-GOV-002: bind canonical modeling runbooks
5fe0944 TASK-GOV-002: adopt task proposal schema v2
b8465da TASK-GOV-001: preserve private-source ignore rules
e20962a TASK-GOV-001: minimize Claude tool audit log
e731129 TASK-GOV-001: enforce Git inspection allowlist
ae9d61e TASK-GOV-001: harden Claude managed permissions
6818a0b TASK-GOV-001: add managed MCP lockdown
c51496f TASK-GOV-001: update Claude control-plane image wiring
c274cf2 docs: revisa limites, navegação e exemplos do guia
4c742cd docs: aplica estrutura completa do guia Markdown
b469b8f docs: atualiza guia de estilo Markdown
3580506 Merge pull request #29 from cepraea/feat/cepraea-domain-modeling
2bf9214 AC-000 bootstrap: estrutura completa da modelagem canônica
4c26595 Arquivos commitador por Davi Sermenho
0021102 Ajustes Finais nos arquivos
45c344c Alinhamento-Final
fbf34ff Field-registry-v0.01
2cdc8aa Merge branch 'chore/runbooks-e-correcoes-politicas-agentes' of https://github.com/cepraea/beach-pro into chore/runbooks-e-correcoes-politicas-agentes Todos em maisn branch
0cf0773 Todos-online
8eb98f8 chore(agents): define executor and reviewer roles
9d0995c chore(agents): define executor and reviewer roles
129a683 Mark down lint 1
5eedbb9 Mark down lint 1
a477e7b Sincornização dos arquivos
8839402 feat: adiciona workflow multi-agente
7734846 chore: establish agent-safe devcontainer controls
9857c72 initial commit: reset total do repositorio

=== commit message quality sample (last 25 full subjects) ===
9ff086f|Davi Sermenho|2026-08-18|docs: add repository CLAUDE.md instructions
48047a7|Davi Sermenho|2026-08-18|docs: add repository manifests
f6d1bbb|cepraea|2026-08-17|Merge pull request #37 from cepraea/modeling/AC-002-bancocepraea
58073d4|cepraea|2026-08-17|Merge pull request #35 from cepraea/modeling/AC-001-cepraea-agosto-2026
933d01f|cepraea|2026-08-17|Merge pull request #34 from cepraea/docs/assurance-fvr-backlog
a5a745d|cepraea|2026-08-17|Merge pull request #33 from cepraea/docs/modeling-governance-dec-gov-002
8ed3928|cepraea|2026-08-17|Merge pull request #32 from cepraea/feat/task-governance-v2
b0e8bb0|cepraea|2026-08-17|Merge pull request #31 from cepraea/chore/claude-executor-hardening
94b30aa|cepraea|2026-08-17|TASK-GOV-001: remove unrelated gitignore drift
60302f4|cepraea|2026-08-17|AC-002: process BancoCEPRAEA source
d1cda9f|cepraea|2026-08-17|AC-001: process CEPRAEA Agosto 2026 source
fc0d42d|cepraea|2026-08-17|ASSURANCE-001: organize FVR assurance backlog
8f6482c|cepraea|2026-08-17|DEC-GOV-002: bind canonical modeling runbooks
5fe0944|cepraea|2026-08-17|TASK-GOV-002: adopt task proposal schema v2
b8465da|cepraea|2026-08-17|TASK-GOV-001: preserve private-source ignore rules
e20962a|cepraea|2026-08-17|TASK-GOV-001: minimize Claude tool audit log
e731129|cepraea|2026-08-17|TASK-GOV-001: enforce Git inspection allowlist
ae9d61e|cepraea|2026-08-17|TASK-GOV-001: harden Claude managed permissions
6818a0b|cepraea|2026-08-17|TASK-GOV-001: add managed MCP lockdown
c51496f|cepraea|2026-08-17|TASK-GOV-001: update Claude control-plane image wiring
c274cf2|cepraea|2026-08-16|docs: revisa limites, navegação e exemplos do guia
4c742cd|cepraea|2026-08-16|docs: aplica estrutura completa do guia Markdown
b469b8f|cepraea|2026-08-16|docs: atualiza guia de estilo Markdown
3580506|cepraea|2026-08-15|Merge pull request #29 from cepraea/feat/cepraea-domain-modeling
2bf9214|Davi Sermenho|2026-08-15|AC-000 bootstrap: estrutura completa da modelagem canônica
Now the reviewer and executor runbooks, which are the core of P5.

Bash
IN
for f in runbooks/reviewer/RB-REV-001-code-review.md runbooks/reviewer/RB-REV-003-documentation-review.md runbooks/reviewer/RB-REV-004-evidence-review.md; do echo "########## $f ##########"; cat -n "$f"; echo; done

OUT
########## runbooks/reviewer/RB-REV-001-code-review.md ##########
     1	# RB-REV-001 — Revisão de código
     2
     3	## Objetivo
     4
     5	Definir o procedimento especializado de revisão independente para alterações normais de
     6	código-fonte no CEPRAEA BEACH PRO.
     7
     8	## Aplicabilidade
     9
    10	Usar este runbook quando o Reviewer receber um `git diff` resultante de:
    11
    12	- implementação de funcionalidade
    13	- correção de comportamento
    14	- refatoração autorizada
    15	- alteração de comportamento observável de código
    16
    17	## Entradas
    18
    19	- `git diff` completo da alteração
    20	- Critérios de aceite da tarefa
    21	- Evidências produzidas pelo Executor
    22
    23	## Fontes de autoridade
    24
    25	- `AGENT_POLICY.md`
    26	- `AGENTS.md`
    27	- Critérios de aceite da tarefa
    28	- Fontes normativas aplicáveis quando a tarefa referenciar modelagem
    29
    30	## Pré-condições
    31
    32	- `git diff` disponível e inspecionável
    33	- Critérios de aceite identificados
    34	- Reviewer operando com projeto read-only
    35
    36	## Escopo operacional
    37
    38	Somente leitura: `git diff`, `git status`, `git log`, arquivos do projeto.
    39
    40	Escrita efêmera exclusivamente em `/tmp` ou caches técnicos explicitamente autorizados.
    41
    42	Não alterar o working tree, não aplicar patches, não fazer commit.
    43
    44	## Procedimento
    45
    46	1. Confirmar a tarefa sob revisão e seus critérios de aceite.
    47	2. Inspecionar `git status`.
    48	3. Inspecionar o `git diff` completo.
    49	4. Comparar o diff com o objetivo da tarefa.
    50	5. Verificar o comportamento observável da alteração.
    51	6. Procurar regressões diretamente relacionadas à área alterada.
    52	7. Verificar os testes afetados: cobertura e adequação.
    53	8. Executar verificações independentes proporcionais ao risco (lint, typecheck, testes selecionados).
    54	9. Verificar alterações inesperadas fora do escopo autorizado.
    55	10. Emitir o verdict com findings quando aplicável.
    56
    57	## Pontos de decisão
    58
    59	| Condição | Ação |
    60	|---|---|
    61	| Finding requer decisão de domínio | `HUMAN_DECISION_REQUIRED` |
    62	| Comportamento correto, mas escopo expandido sem autorização | `FAIL` com finding |
    63	| Testes ausentes para comportamento novo | Finding LOW ou MEDIUM conforme impacto |
    64	| Regressão confirmada | `FAIL` com finding HIGH ou CRITICAL |
    65
    66	## Validações independentes
    67
    68	Executar proporcionalmente ao risco e à área alterada:
    69
    70	- lint sem `--fix`
    71	- typecheck com `noEmit`
    72	- testes unitários selecionados para a área alterada
    73
    74	Caches redirecionados para `/tmp` quando necessário.
    75
    76	## Evidências
    77
    78	- Diff inspecionado
    79	- Resultado das verificações independentes executadas
    80	- Findings documentados com estrutura completa
    81
    82	## Handoff
    83
    84	Emitir verdict com:
    85
    86	- resumo da revisão
    87	- findings classificados (quando existirem)
    88	- verificações executadas e resultados
    89	- questões para Davi quando aplicável
    90
    91	## Estados de saída
    92
    93	`PASS` — diff consistente com o objetivo, sem findings bloqueantes, evidências suficientes.
    94
    95	`FAIL` — finding CRITICAL ou HIGH, regressão confirmada, escopo violado ou evidência insuficiente
    96	material.
    97
    98	`HUMAN_DECISION_REQUIRED` — questão de domínio ou decisão material exige autoridade humana.
    99
   100	## Referências
   101
   102	- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
   103	- [`AGENTS.md`](/AGENTS.md)
   104	- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
   105	- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)

########## runbooks/reviewer/RB-REV-003-documentation-review.md ##########
     1	# RB-REV-003 — Revisão de documentação
     2
     3	## Objetivo
     4
     5	Definir o procedimento especializado de revisão independente para criação e alteração de
     6	documentação Markdown no CEPRAEA BEACH PRO.
     7
     8	## Aplicabilidade
     9
    10	Usar este runbook quando o Reviewer receber um `git diff` resultante de:
    11
    12	- criação de novo documento Markdown
    13	- alteração de documento Markdown existente
    14	- atualização de decisão, modelo ou evidência em formato Markdown
    15
    16	## Entradas
    17
    18	- `git diff` completo da alteração documental
    19	- Fontes técnicas aplicáveis ao conteúdo revisado
    20	- Critérios de aceite da tarefa
    21
    22	## Fontes de autoridade
    23
    24	- `AGENT_POLICY.md`
    25	- `AGENTS.md`
    26	- `docs/standards/guia_estilo_documentação.md` — normativa canônica de autoria
    27	- Fontes técnicas aplicáveis ao conteúdo revisado
    28
    29	## Pré-condições
    30
    31	- `git diff` disponível e inspecionável
    32	- Guia canônico de documentação lido
    33	- Fontes técnicas identificadas
    34	- Reviewer operando com projeto read-only
    35
    36	## Escopo operacional
    37
    38	Somente leitura: diff, documentos do repositório, fontes técnicas aplicáveis.
    39
    40	Escrita efêmera exclusivamente em `/tmp` quando necessário para validações.
    41
    42	Não alterar o working tree, não aplicar patches, não fazer commit.
    43
    44	## Procedimento
    45
    46	1. Confirmar a tarefa sob revisão e seus critérios de aceite.
    47	2. Identificar as fontes técnicas aplicáveis ao conteúdo.
    48	3. Inspecionar o `git diff` completo.
    49	4. Verificar a preservação do significado técnico: o conteúdo alterado não contradiz as fontes.
    50	5. Verificar aderência ao guia de autoria (idioma, sentence case, linguagem direta, estrutura).
    51	6. Identificar afirmações sem suporte em fonte verificável.
    52	7. Verificar links e referências afetados pela alteração.
    53	8. Verificar exemplos e comandos para correção técnica.
    54	9. Avaliar separadamente: forma (estilo, estrutura) e correção técnica (conteúdo).
    55	10. Emitir o verdict com findings quando aplicável.
    56
    57	## Pontos de decisão
    58
    59	| Condição | Ação |
    60	|---|---|
    61	| Conteúdo contradiz fonte normativa | `FAIL` com finding HIGH ou CRITICAL conforme impacto |
    62	| Afirmação sem suporte em evidência | Finding MEDIUM; não suprimir |
    63	| Decisão existente alterada sem autorização | `FAIL` com finding CRITICAL |
    64	| Erro de estilo sem impacto técnico | Finding LOW |
    65	| Exemplo ou comando tecnicamente incorreto | Finding HIGH |
    66
    67	## Validações independentes
    68
    69	- markdownlint (ou equivalente) sem erros bloqueantes
    70	- Links internos verificados
    71	- Comandos listados conferidos contra a implementação atual quando críticos
    72
    73	## Evidências
    74
    75	- Diff documental inspecionado
    76	- Resultado das validações documentais
    77	- Findings documentados com estrutura completa
    78
    79	## Handoff
    80
    81	Emitir verdict com:
    82
    83	- resumo da revisão (forma e correção técnica, separadamente)
    84	- findings classificados (quando existirem)
    85	- verificações executadas e resultados
    86	- questões para Davi quando aplicável
    87
    88	## Estados de saída
    89
    90	`PASS` — conteúdo tecnicamente correto, aderente ao guia de autoria, sem afirmações sem suporte
    91	material.
    92
    93	`FAIL` — conteúdo tecnicamente incorreto, contradiz fonte normativa, decisão alterada sem
    94	autorização, ou finding HIGH/CRITICAL que impeça aceitação.
    95
    96	`HUMAN_DECISION_REQUIRED` — questão de conteúdo que exige decisão de domínio por Davi.
    97
    98	## Referências
    99
   100	- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
   101	- [`AGENTS.md`](../../AGENTS.md)
   102	- [`docs/standards/guia_estilo_documentação.md`](../../docs/standards/guia_estilo_documentação.md)
   103	- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
   104	- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)

########## runbooks/reviewer/RB-REV-004-evidence-review.md ##########
     1	# RB-REV-004 — Revisão de evidências
     2
     3	## Objetivo
     4
     5	Definir o procedimento especializado de revisão independente quando a suficiência da evidência
     6	é um aspecto material para a aceitação da operação.
     7
     8	## Aplicabilidade
     9
    10	Usar este runbook em combinação com o runbook especializado principal quando:
    11
    12	- os critérios de aceite exigirem evidência específica de propriedades materiais
    13	- o Executor fizer alegações que precisam ser verificadas independentemente
    14	- a operação envolver risco que justifique verificação adicional de evidências
    15
    16	## Entradas
    17
    18	- Evidências produzidas pelo Executor
    19	- `git diff` da operação
    20	- Critérios de aceite da tarefa
    21
    22	## Fontes de autoridade
    23
    24	- `AGENT_POLICY.md` — seção Persistent Evidence
    25	- `AGENTS.md`
    26	- Critérios de aceite da tarefa
    27
    28	## Pré-condições
    29
    30	- Evidências do Executor disponíveis
    31	- Critérios de aceite identificados
    32	- Reviewer operando com projeto read-only
    33
    34	## Escopo operacional
    35
    36	Somente leitura e verificação independente.
    37
    38	Escrita efêmera exclusivamente em `/tmp` ou caches técnicos explicitamente autorizados.
    39
    40	Não corrigir silenciosamente deficiências de evidência: registrar como finding.
    41
    42	## Procedimento
    43
    44	1. Identificar as alegações materiais feitas pelo Executor.
    45	2. Para cada alegação, identificar a evidência correspondente produzida.
    46	3. Comparar cada alegação com o estado observável no repositório.
    47	4. Reproduzir verificações críticas quando proporcional ao risco (usar somente `/tmp` para escrita).
    48	5. Classificar insuficiência de evidência conforme severidade.
    49	6. Emitir o verdict com findings quando aplicável.
    50
    51	## Pontos de decisão
    52
    53	| Condição | Ação |
    54	|---|---|
    55	| Alegação sem evidência correspondente | Finding MEDIUM ou HIGH conforme impacto |
    56	| Evidência contraditória com estado observável | Finding HIGH ou CRITICAL |
    57	| Verificação crítica não reproduzível | Finding + comunicar limitação |
    58	| Critérios de aceite ambíguos sobre o que constitui evidência | `HUMAN_DECISION_REQUIRED` |
    59
    60	## Critérios de suficiência mínima
    61
    62	Uma evidência é materialmente suficiente quando:
    63
    64	- existe e é verificável no estado atual do repositório
    65	- é consistente com a alegação feita
    66	- não contraditória com o estado observável
    67
    68	Uma evidência é insuficiente quando:
    69
    70	- está ausente para uma alegação material
    71	- contradiz o estado observável
    72	- não pode ser verificada independentemente e a alegação é de alto risco
    73
    74	## Evidências do próprio review
    75
    76	- Lista das alegações revisadas
    77	- Verificações executadas independentemente
    78	- Findings de insuficiência classificados
    79
    80	## Handoff
    81
    82	Emitir verdict com:
    83
    84	- lista das alegações verificadas
    85	- findings de insuficiência (quando existirem)
    86	- verificações independentes executadas
    87	- questões para Davi quando aplicável
    88
    89	## Estados de saída
    90
    91	`PASS` — todas as alegações materiais possuem evidência suficiente e consistente.
    92
    93	`FAIL` — alegação material sem evidência, evidência contraditória ou insuficiência que impeça
    94	aceitação.
    95
    96	`HUMAN_DECISION_REQUIRED` — critérios de suficiência de evidência exigem decisão de Davi.
    97
    98	## Referências
    99
   100	- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
   101	- [`AGENTS.md`](../../AGENTS.md)
   102	- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
   103	- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
Bash
IN
for f in runbooks/executor/RB-EXEC-001-code-change.md runbooks/executor/RB-EXEC-003-documentation-change.md; do echo "########## $f ##########"; cat -n "$f"; echo; done

OUT
########## runbooks/executor/RB-EXEC-001-code-change.md ##########
     1	# RB-EXEC-001 — Alteração de código
     2
     3	## Objetivo
     4
     5	Definir o procedimento especializado para implementação, correção, refatoração autorizada e
     6	alteração de comportamento de código-fonte no CEPRAEA BEACH PRO.
     7
     8	## Aplicabilidade
     9
    10	Usar este runbook quando a tarefa envolver:
    11
    12	- implementação de funcionalidade nova
    13	- correção de comportamento incorreto
    14	- refatoração explicitamente autorizada
    15	- alteração de comportamento observável de código
    16
    17	## Entradas
    18
    19	- Tarefa autorizada por Davi com escopo definido
    20	- Branch dedicada diferente de `main` e `master`
    21	- `git status` limpo ou com alterações pertencentes à tarefa em curso
    22
    23	## Fontes de autoridade
    24
    25	- `AGENT_POLICY.md`
    26	- `CLAUDE.md`
    27	- Critérios de aceite da tarefa
    28
    29	## Pré-condições
    30
    31	- Branch correta confirmada
    32	- `git status` inspecionado
    33	- Escopo da tarefa identificado
    34
    35	## Escopo operacional
    36
    37	Alterar exclusivamente os arquivos necessários à tarefa autorizada.
    38
    39	Não modificar:
    40
    41	- `AGENT_POLICY.md`, `CLAUDE.md`, `AGENTS.md`
    42	- `.devcontainer/**`, `.claude/**`, `.codex/**`
    43	- `.drive/**`
    44	- arquivos fora do escopo da tarefa
    45
    46	## Procedimento
    47
    48	1. Identificar os componentes afetados pela tarefa.
    49	2. Identificar contratos públicos (APIs, tipos exportados, interfaces) relacionados.
    50	3. Localizar os testes existentes para os componentes afetados.
    51	4. Implementar exclusivamente a alteração requerida pela tarefa.
    52	5. Atualizar os testes necessários para cobrir a alteração.
    53	6. Executar os validadores aplicáveis: lint, typecheck, testes unitários, testes de integração.
    54	7. Corrigir erros mecânicos causados pela alteração.
    55	8. Verificar regressões diretamente relacionadas à mudança.
    56
    57	## Pontos de decisão
    58
    59	| Condição | Ação |
    60	|---|---|
    61	| Alteração exige segundo arquivo fora do escopo original | Parar; comunicar e obter checkpoint de Davi antes de expandir |
    62	| Teste falha por causa externa à alteração | Registrar e comunicar; não suprimir |
    63	| Contrato público afetado de forma inesperada | Comunicar antes de prosseguir |
    64
    65	## Validações
    66
    67	- `npm run lint` (ou equivalente) sem erros bloqueantes
    68	- `npm run typecheck` (ou equivalente) sem erros
    69	- Testes unitários aplicáveis: sem falhas novas
    70	- `git diff --check` limpo
    71	- `git diff` inspecionado
    72
    73	## Evidências
    74
    75	- Diff completo da alteração (`git diff`)
    76	- Resultado dos validadores (exit codes e saída relevante)
    77	- Lista dos arquivos modificados
    78
    79	## Handoff
    80
    81	Apresentar de forma factual:
    82
    83	- tarefa executada
    84	- arquivos alterados
    85	- validações executadas e resultados
    86	- riscos residuais ou limitações identificadas
    87	- pontos que merecem atenção do Reviewer
    88
    89	Finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.
    90
    91	## Estados de saída
    92
    93	`READY_FOR_REVIEW` — alteração completa, validadores passando, diff revisável.
    94
    95	`BLOCKED` — qualquer condição impede a conclusão correta.
    96
    97	## Referências
    98
    99	- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
   100	- [`CLAUDE.md`](../../CLAUDE.md)
   101	- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
   102	- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
   103
   104

########## runbooks/executor/RB-EXEC-003-documentation-change.md ##########
     1	# RB-EXEC-003 — Alteração de documentação
     2
     3	## Objetivo
     4
     5	Definir o procedimento especializado para criação e alteração de arquivos de documentação
     6	Markdown no CEPRAEA BEACH PRO.
     7
     8	## Aplicabilidade
     9
    10	Usar este runbook quando a tarefa envolver:
    11
    12	- criação de novo documento Markdown
    13	- alteração de documento Markdown existente
    14	- atualização de decisão, modelo ou evidência em formato Markdown
    15
    16	## Entradas
    17
    18	- Tarefa autorizada com escopo documental definido
    19	- Branch dedicada diferente de `main` e `master`
    20
    21	## Fontes de autoridade
    22
    23	- `AGENT_POLICY.md` — seção Autoria de documentação
    24	- `CLAUDE.md`
    25	- `docs/standards/guia_estilo_documentação.md` — normativa canônica de autoria
    26	- Fontes técnicas aplicáveis à tarefa
    27	- Critérios de aceite da tarefa
    28
    29	## Pré-condições
    30
    31	- Branch correta confirmada
    32	- Guia canônico de documentação lido antes de escrever
    33	- Fontes técnicas aplicáveis identificadas
    34
    35	## Escopo operacional
    36
    37	Alterar exclusivamente os arquivos dentro do escopo documental autorizado pela tarefa.
    38
    39	Não criar ou alterar:
    40
    41	- código, configuração ou infraestrutura como parte de uma tarefa documental
    42	- decisões canônicas retroativamente para justificar alterações de código anteriores
    43	- conteúdo que contradigam fontes normativas sem decisão explícita de Davi
    44
    45	## Procedimento
    46
    47	1. Ler `docs/standards/guia_estilo_documentação.md` antes de escrever qualquer conteúdo.
    48	2. Identificar as fontes técnicas aplicáveis (modelo canônico, plano, fontes do domínio).
    49	3. Preservar as decisões existentes registradas nos documentos afetados.
    50	4. Restringir a alteração estritamente ao escopo documental autorizado pela tarefa.
    51	5. Aplicar as regras de autoria: português brasileiro, sentence case, linguagem direta, fidelidade técnica.
    52	6. Verificar links e referências afetados pela alteração.
    53	7. Executar as validações documentais disponíveis (markdownlint ou equivalente).
    54	8. Inspecionar o diff documental antes de finalizar.
    55
    56	## Pontos de decisão
    57
    58	| Condição | Ação |
    59	|---|---|
    60	| Fonte técnica ausente ou incerta | Registrar como lacuna; não inventar conhecimento |
    61	| Alteração implica mudança de decisão existente | Parar; comunicar a Davi antes de alterar |
    62	| Link quebrado detectado | Corrigir somente se dentro do escopo; registrar os demais |
    63
    64	## Validações
    65
    66	- `markdownlint` (ou equivalente) sem erros bloqueantes
    67	- Links internos verificados
    68	- Regras de autoria aplicadas
    69	- `git diff --check` limpo
    70	- Diff documental inspecionado
    71
    72	## Evidências
    73
    74	- Diff completo do documento (`git diff`)
    75	- Resultado da validação documental
    76
    77	## Handoff
    78
    79	Apresentar de forma factual:
    80
    81	- tarefa executada
    82	- documentos alterados
    83	- validações executadas e resultados
    84	- lacunas identificadas (conhecimento ausente, links não corrigidos)
    85	- pontos que merecem atenção do Reviewer
    86
    87	Finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.
    88
    89	## Estados de saída
    90
    91	`READY_FOR_REVIEW` — alteração completa, validações documentais passando, diff revisável.
    92
    93	`BLOCKED` — qualquer condição impede a conclusão correta.
    94
    95	## Referências
    96
    97	- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
    98	- [`CLAUDE.md`](../../CLAUDE.md)
    99	- [`docs/standards/guia_estilo_documentação.md`](../../docs/standards/guia_estilo_documentação.md)
   100	- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
   101	- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
Found link drift already. Let me verify the source files with line numbers and check the mechanical enforcement layer.

Bash
IN
echo "=== AGENT_POLICY.md ==="; cat -n AGENT_POLICY.md | sed -n '30,60p;95,140p'; echo; echo "=== grep broken abs links in runbooks ==="; grep -rn "](/" runbooks/ ; echo; echo "=== markdownlint config ==="; cat .markdownlint.jsonc

OUT
=== AGENT_POLICY.md ===
    30
    31	- Verde: mudança local, reversível, sem auth, dados ou plano de controle.
    32	- Amarelo: múltiplos alvos/módulos, semântica canônica ou expansão relevante.
    33	- Vermelho: dependência, migration, RLS, MFA, auth, auditoria ou privacidade.
    34	- Vermelho crítico: `.devcontainer`, CI, hooks, managed settings, secrets,
    35	  deploy ou infraestrutura.
    36
    37	## Git
    38
    39	Git é a state machine e o mecanismo de handoff.
    40
    41	Agentes podem executar operações de inspeção:
    42
    43	- `git status`
    44	- `git diff`
    45	- `git log`
    46	- `git show`
    47	- `git rev-parse`
    48	- `git ls-files`
    49
    50	Operações que alterem index, refs, histórico ou estado remoto pertencem ao humano,
    51	incluindo:
    52
    53	- add
    54	- commit
    55	- push
    56	- pull
    57	- merge
    58	- rebase
    59	- cherry-pick
    60	- reset
    95
    96	Não altere fonte para fazê-la concordar com uma conclusão.
    97
    98	Não invente conhecimento para preencher lacunas.
    99
   100	Para modelagem, use:
   101	[Modelagem dos Dados](./docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md)
   102
   103	## Validação
   104
   105	O EXECUTOR executa os validadores determinísticos aplicáveis antes do handoff.
   106
   107	O REVIEWER reexecuta somente os checks necessários para revisão independente,
   108	proporcionalmente ao risco e aos findings.
   109
   110	## Sem bypass
   111
   112	Permissão inexistente não autoriza alteração de policy, sandbox, container ou
   113	controle para contornar a restrição.
   114
   115	Se a tarefa não puder continuar dentro da autoridade disponível, informe
   116
   117	`BLOCKED` ou `HUMAN_DECISION_REQUIRED`.
   118
   119	## Evidência
   120
   121	Persista quando material:
   122
   123	- código;
   124	- testes;
   125	- evidências;
   126	- modelos;
   127	- regras;
   128	- decisões;
   129	- commits.
   130
   131	Não crie state machine, log de interação ou relatório obrigatório paralelo ao Git.
   132
   133	## Escalonamento
   134
   135	ChatGPT ou Gemini são usados somente para:
   136
   137	- divergência material;
   138	- decisão arquitetural;
   139	- problema semântico relevante;
   140	- terceira opinião realmente necessária.

=== grep broken abs links in runbooks ===
runbooks/reviewer/RB-REV-001-code-review.md:102:- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
runbooks/reviewer/RB-REV-001-code-review.md:103:- [`AGENTS.md`](/AGENTS.md)
runbooks/executor/RB-EXEC-003-documentation-change.md:97:- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
runbooks/executor/RB-EXEC-002-database-change.md:100:- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
runbooks/executor/RB-EXEC-004-dependency-change.md:97:- [`AGENT_POLICY.md`](/AGENT_POLICY.md)

=== markdownlint config ===
// Este arquivo define a configuração do Markdownlint usada neste repositório. Veja
// https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md
// para mais detalhes sobre cada regra.

{
  // Chave especial "default": não é uma regra individual — é o valor base aplicado a
  // toda regra nativa do markdownlint que não for explicitamente sobrescrita abaixo.
  // Objetivo: partir da cobertura máxima de regras e só desativar/ajustar o que for
  // necessário, em vez de precisar habilitar cada regra manualmente.
  "default": true,

  // MD001 — heading-increment: "Os níveis de título devem incrementar apenas um nível por vez".
  // Definição: proíbe pular níveis de título (ex.: ir de "#" direto para "###").
  // Objetivo: preservar uma hierarquia de títulos contínua e legível.
  "heading-increment": true,

  // MD004 — ul-style: "Estilo de lista não ordenada".
  // Definição: define qual marcador (*, +, -) deve ser usado em listas não ordenadas.
  // Objetivo: manter consistência visual entre listas, exigindo sempre "-".
  "ul-style": {
    "style": "dash"
  },

  // MD007 — ul-indent: "Indentação de lista não ordenada".
  // Definição: define quantos espaços de indentação são exigidos para itens aninhados.
  // Objetivo: manter indentação previsível (2 espaços) em todas as listas.
  "ul-indent": {
    "indent": 2
  },

  // MD010 — no-hard-tabs: "Tabulação (hard tab)".
  // Definição: proíbe caracteres de tabulação (\t); espera espaços no lugar.
  // Objetivo: evitar inconsistência visual entre editores que renderizam tabs com
  // larguras diferentes; spaces_per_tab define quantos espaços equivalem a uma tabulação
  // para o cálculo de coluna/correção automática.
  "no-hard-tabs": {
    "spaces_per_tab": 2
  },

  // MD024 — no-duplicate-heading: "Múltiplos títulos com o mesmo conteúdo".
  // Definição: proíbe títulos duplicados no documento.
  // Objetivo: siblings_only restringe a checagem a títulos irmãos (mesmo nível, sob o
  // mesmo título pai), permitindo texto repetido em seções diferentes sem falso positivo.
  "no-duplicate-heading": {
    "siblings_only": true
  },

  // MD025 — single-title: "Múltiplos títulos de nível superior no mesmo documento".
  // Definição: garante que exista apenas um título de nível 1 (H1) por documento.
  // Objetivo: front_matter_title reconhece um título já declarado no front matter
  // (ex.: "title: Minha Página"), evitando que ele conte como um segundo H1 quando o
  // corpo também tiver um cabeçalho.
  "single-title": {
    "front_matter_title": "^\\s*title\\s*[:=]",
  },

  // MD026 — no-trailing-punctuation: "Pontuação no final de título".
  // Definição: proíbe caracteres de pontuação ao final de um título.
  // Objetivo: punctuation restringe a checagem a ".,;:" — o padrão da regra também
  // bloquearia "!" e "?", que aqui ficam permitidos (ex.: títulos em forma de pergunta
  // ou alerta) para não gerar falso positivo.
  "no-trailing-punctuation": {
    "punctuation": ".,;:",
  },

  // MD028 — no-blanks-blockquote: "Linha em branco dentro de blockquote".
  // Definição: por padrão, proíbe linha em branco dentro de um blockquote (o
  // markdownlint interpretaria isso como dois blockquotes separados).
  // Objetivo: desativada porque Notes/Callouts consecutivos usados atualmente no
  // conteúdo não estão em conformidade com esta regra.
  "no-blanks-blockquote": false,

  // MD029 — ol-prefix: "Prefixo de item de lista ordenada".
  // Definição: define se listas ordenadas devem usar numeração sequencial (1,2,3...),
  // repetir "1." em todos os itens, ou aceitar qualquer uma das duas formas.
  // Objetivo: forçar numeração sequencial ("ordered") para flagrar o encerramento
  // acidental de uma lista causado por indentação incorreta.
  "ol-prefix": {
    "style": "ordered",
  },

  // MD013 — line-length: "Comprimento de linha".
  // Definição: limita o número de caracteres por linha no documento.
  // Objetivo: desativada porque duplica a formatação já garantida pelo Prettier neste
  // repositório.
  "line-length": false,

  // MD031 — blanks-around-fences: "Blocos de código cercados devem ser cercados por
  // linhas em branco".
  // Definição: exige uma linha em branco antes e depois de um bloco cercado (```).
  // Objetivo: desativada porque duplica a formatação já garantida pelo Prettier.
  "blanks-around-fences": false,

  // MD060 — table-column-style: "Estilo de coluna de tabela".
  // Definição: garante consistência no alinhamento/formatação das colunas de tabelas.
  // Objetivo: desativada porque duplica a formatação já garantida pelo Prettier.
  "table-column-style": false,

  // MD033 — no-inline-html: "HTML embutido".
  // Definição: proíbe o uso de tags HTML diretamente no Markdown.
  // Objetivo: allowed_elements lista as tags liberadas como exceção (links, tabelas,
  // MathML como <mfrac>/<msub>, etc.), permitindo HTML apenas onde o Markdown puro não
  // é suficiente e mantendo a regra ativa para o restante.
  // Observação: os nomes de tag abaixo NÃO foram traduzidos — são valores funcionais
  // comparados contra o HTML real do documento.
  "no-inline-html": {
    "allowed_elements": [
      "a",
      "abbr",
      "annotation",
      "br",
      "caption",
      "code",
      "col",
      "colgroup",
      "dd",
      "details",
      "div",
      "dl",
      "dt",
      "em",
      "h4",
      "h5",
      "img",
      "kbd",
      "li",
      "math",
      "mdn-scrim-inline",
      "menclose",
      "mfenced",
      "mfrac",
      "mfrac",
      "mi",
      "mmultiscripts",
      "mn",
      "mo",
      "mover",
      "mphantom",
      "mprescripts",
      "mroot",
      "mrow",
      "ms",
      "mspace",
      "mspace",
      "msqrt",
      "mstyle",
      "msub",
      "msubsup",
      "msup",
      "mtable",
      "mtd",
      "mtext",
      "mtr",
      "munder",
      "munderover",
      "none",
      "ol",
      "p",
      "pre",
      "q",
      "section",
      "semantics",
      "strong",
      "sub",
      "summary",
      "sup",
      "table",
      "tbody",
      "td",
      "tfoot",
      "th",
      "thead",
      "tr",
      "ul",
      "var"
    ]
  },

  // MD034 — no-bare-urls: "URL sem formatação (bare URL)".
  // Definição: exige que uma URL apareça como link Markdown ou entre "<>", em vez de
  // solta no texto.
  // Objetivo: desativada; não há justificativa registrada no arquivo original para essa
  // desativação — vale confirmar com Davi se ela deve permanecer assim.
  "no-bare-urls": false,

  // MD037 — no-space-in-emphasis: "Espaços dentro dos marcadores de ênfase".
  // Definição: proíbe espaço logo após/antes dos marcadores de ênfase (ex.: "* texto *").
  // Objetivo: desativada porque produz falsos positivos em excesso neste conteúdo.
  "no-space-in-emphasis": false,

  // MD040 — fenced-code-language: "Blocos de código cercados devem declarar uma
  // linguagem".
  // Definição: exige que todo bloco de código cercado (```) declare um identificador de
  // linguagem.
  // Sua linguagem não está nesta lista? Veja
  // https://github.com/orgs/mdn/discussions/170#discussioncomment-3404366 antes de
  // adicionar um novo identificador.
  // Objetivo: allowed_languages evita identificadores inconsistentes ou inventados,
  // mantendo o realce de sintaxe previsível.
  "fenced-code-language": {
    "allowed_languages": [
      "apacheconf",
      "bash",
      "batch",
      "c",
      "cpp",
      "cs",
      "css",
      "css-nolint",
      "diff",
      "django",
      "glsl",
      "hbs",
      "hbs-nolint",
      "html",
      "html-nolint",
      "http",
      "ini",
      "java",
      "js",
      "js-nolint",
      "json",
      "json-nolint",
      "jsx",
      "jsx-nolint",
      "latex",
      "md",
      "md-nolint",
      "nginx",
      "php",
      "plain",
      "powershell",
      "pug",
      "python",
      "regex",
      "rust",
      "scss",
      "sh",
      "sql",
      "svelte",
      "svg",
      "toml",
      "ts",
      "url",
      "vue",
      "wat",
      "webidl",
      "xml",
      "yaml",
      "text",
      "txt",
      "markdown"
    ]
  },

  // MD042 — no-empty-links: "Links vazios".
  // Definição: proíbe links sem texto ou sem destino (ex.: "[]()").
  // Objetivo: desativada porque macros usadas no conteúdo atualmente geram falso
  // positivo nesta regra — veja https://github.com/mdn/content/pull/20026 para o
  // contexto original da decisão.
  "no-empty-links": false,

  // MD046 — code-block-style: "Estilo de bloco de código".
  // Definição: define se blocos de código devem usar cerca de crases (```), indentação,
  // ou aceitar as duas formas.
  // Objetivo: exigir sempre blocos cercados ("fenced"), proibindo blocos indentados, para
  // manter um único estilo em todo o repositório.
  "code-block-style": {
    "style": "fenced"
  },

  // MD049 — emphasis-style: "Estilo de ênfase".
  // Definição: define qual marcador deve ser usado para ênfase/itálico (* ou _).
  // Objetivo: exigir "*texto*" para evitar ambiguidade com o marcador de negrito.
  "emphasis-style": {
    "style": "asterisk"
  },

  // MD050 — strong-style: "Estilo de negrito".
  // Definição: define qual marcador deve ser usado para negrito (** ou __).
  // Objetivo: exigir "**texto**"; combinado com emphasis-style "underscore", evita que
  // "*" e "_" sejam usados de forma intercambiável e ambígua.
  "strong-style": {
    "style": "asterisk"
  },

  // MD051 — link-fragments: "Fragmentos de link devem ser válidos".
  // Definição: verifica se uma âncora interna (#fragmento) corresponde a um título
  // existente no documento.
  // Objetivo: desativada porque o gerador "yari" (herdado da configuração original do
  // projeto MDN Content) cria fragmentos trocando espaço por underscore, não por hífen —
  // divergindo do algoritmo padrão do markdownlint e gerando falso positivo.
  // Observação: se este repositório não usa "yari" como gerador de site, vale confirmar
  // com Davi se esta regra deveria ser reativada.
  "link-fragments": false,

  // MD059 — descriptive-link-text: "O texto do link deve ser descritivo".
  // Definição: proíbe texto de link genérico que não descreve o destino (ex.: "aqui",
  // "clique aqui", "veja mais").
  // Objetivo: garantir que links sejam compreensíveis fora de contexto (leitores de
  // tela, listas de links extraídas) — alinhado com a seção "Links" de
  // docs/standards/guia_estilo_documentação.md.
  // Observação: as expressões abaixo NÃO foram traduzidas — são os valores funcionais
  // comparados contra o texto real do link; traduzi-las mudaria o comportamento da regra.
  "descriptive-link-text": {
    "prohibited_texts": [
      "here",
      "link",
      "more",
      "this",
      "this link",
      "this page",
      "this site",
      "this article",
      "click here",
      "click this link",
      "see here",
      "see this page",
      "see this site",
      "see this article"
    ]
  },

  // Regra customizada "search-replace" (plugin markdownlint-rule-search-replace —
  // https://github.com/OnkarRuikar/markdownlint-rule-search-replace).
  // Definição: localiza padrões de texto (literais ou regex) e reporta erro, com
  // substituição automática opcional.
  // Objetivo: aplicar convenções de escrita específicas deste repositório (aspas retas,
  // travessão, links, ortografia etc.) que as regras nativas do markdownlint não cobrem.
  "search-replace": {
    "rules": [
      {
        "name": "curly-double-quotes",
        "message": "Não use aspas duplas curvas",
        "searchPattern": "/“|”/g",
        "replace": "\"",
        "searchScope": "text"
      },
      {
        "name": "curly-single-quotes",
        "message": "Não use aspas simples curvas",
        "searchPattern": "/‘|’/g",
        "replace": "'",
        "searchScope": "text"
      },
      {
        "name": "nbsp",
        "message": "Não use espaços incondicionais (non-breaking space)",
        "searchPattern": "/ /g",
        "replace": " ",
        "searchScope": "all"
      },
      {
        "name": "m-dash",
        "message": "Não use '--'. Use travessão (—) em vez disso",
        "search": " -- ",
        "replace": " — ",
        "searchScope": "text"
      },
      {
        "name": "relative-link",
        "message": "Links internos devem começar com '/'",
        "searchPattern": "/([\\(\"])en-US\\/docs/g",
        "replace": "$1/en-US/docs",
        "searchScope": "text"
      },
      {
        "name": "relative-link-path",
        "message": "Não use caminhos relativos",
        "search": "](..",
        "searchScope": "text"
      },
      {
        "name": "trailing-spaces",
        "message": "Evite espaços no final da linha",
        "searchPattern": "/  +$/gm",
        "replace": "",
        "searchScope": "all"
      },
      {
        "name": "double-spaces",
        "message": "Evite espaços duplos",
        "searchPattern": "/([^\\s>])  ([^\\s|])/g",
        "replace": "$1 $2",
        "searchScope": "text"
      },
      {
        "name": "stuck-definition",
        "message": "Caractere colado ao marcador de descrição de definição",
        "searchPattern": "/- :(\\w)/g",
        "replace": "- : $1",
        "searchScope": "text"
      },
      {
        "name": "fqdn-moz-links",
        "message": "Não use developer.mozilla.org para links, exceto em posts de blog",
        "searchPattern": "/\\]\\(https:\\/\\/developer.mozilla.org\\/(?!en-US\\/blog\\/)/g",
        "replace": "](/",
        "searchScope": "text"
      },
      {
        "name": "incorrect-spelling",
        "message": "Ortografia incorreta",
        "searchPattern": ["/e-mail/ig", "/(w)eb site/ig"],
        "replace": ["email", "$1ebsite"],
        "searchScope": "all"
      },
      {
        "name": "localhost-links",
        "message": "Não use localhost em links",
        "searchPattern": "/\\]\\(https?:\\/\\/localhost:\\d+\\//g",
        "replace": "](/",
        "searchScope": "text"
      },
      {
        "name": "un-closed-md-link",
        "message": "Falta o parêntese de fechamento ')'",
        "searchPattern": "/\\[.*?\\]\\([^ )\\n\"]+(?:[\\n\"]| [^\"']| [\"'].+?[\"'][^)])/gm",
        "searchScope": "text"
      },
      {
        "name": "gfm-alert",
        "message": "Use a sintaxe GFM: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Howto/Markdown_in_MDN#notes_warnings_and_callouts",
        "searchPattern": "/^ *> \\*\\*(Note|Warning|Callout):\\*\\*/gm",
        "searchScope": "text"
      },
      {
        "name": "bad-gfm-alert",
        "message": "Use a sintaxe GFM correta: `> [!NOTE]`",
        // TODO: isso deveria usar a sintaxe de modificador; aguardando melhor suporte no Node
        "searchPattern": "/^ *> !?\\[!?((?!NOTE)[Nn][Oo][Tt][Ee]|(?!WARNING)[Ww][Aa][Rr][Nn][Ii][Nn][Gg]|(?!CALLOUT)[Cc][Aa][Ll][Ll][Oo][Uu][Tt])\\]\\n|^ *> (?!\\[!)!?\\[!?(NOTE|WARNING|CALLOUT)\\]\\n|^ *> \\[!(NOTE|WARNING|CALLOUT)\\](?!\\n)/gm",
        "searchScope": "text"
      },
      {
        "name": "comma-after-ie",
        "message": "Adicione vírgula depois de 'i.e.'",
        "searchPattern": "/\\bi\\.e\\. /g",
        "replace": "i.e., ",
        "searchScope": "text"
      },
      {
        "name": "comma-after-eg",
        "message": "Adicione vírgula depois de 'e.g.'",
        "searchPattern": "/\\be\\.g\\. /g",
        "replace": "e.g., ",
        "searchScope": "text"
      },
      {
        "name": "short-link",
        "message": "Use links curtos para links de bug",
        "searchPattern": "/https:\\/\\/bugzilla\\.mozilla\\.org\\/show_bug\\.cgi\\?id=/g",
        "replace": "https://bugzil.la/",
        "searchScope": "all"
      }
    ]
  }
}
Bash
IN
echo "=== pretool guard ==="; cat -n /workspaces/cepraea-beach-pro/.devcontainer/guards/pretool | head -80; echo; echo "=== posttool guard ==="; cat -n /workspaces/cepraea-beach-pro/.devcontainer/guards/posttool | head -40

OUT
=== pretool guard ===
     1	#!/usr/bin/env bash
     2	set -euo pipefail
     3
     4	payload="$(cat)"
     5	tool="$(jq -r '.tool_name // empty' <<<"$payload")"
     6	branch="$(git branch --show-current 2>/dev/null || true)"
     7
     8	block() {
     9	  printf '%s\n' "$1" >&2
    10	  exit 2
    11	}
    12
    13	is_allowed_claude_plan_path() {
    14	  local path="$1" rel parent_real
    15
    16	  case "$path" in
    17	    /home/agent/.claude/plans/*.md) ;;
    18	    *) return 1 ;;
    19	  esac
    20
    21	  rel="${path#/home/agent/.claude/plans/}"
    22	  [[ -n "$rel" && "$rel" != */* ]] || return 1
    23
    24	  case "$path" in
    25	    *"/../"*|*"/./"*) return 1 ;;
    26	  esac
    27
    28	  [[ ! -L "$path" ]] || return 1
    29
    30	  parent_real="$(realpath -e -- "$(dirname -- "$path")" 2>/dev/null)" || return 1
    31	  [[ "$parent_real" == "/home/agent/.claude/plans" ]]
    32	}
    33
    34	if [[ "$branch" == "main" || "$branch" == "master" ]]; then
    35	  case "$tool" in
    36	    Bash|Edit|Write|MultiEdit|NotebookEdit)
    37	      block "Bloqueado: ferramenta mutável na branch principal." ;;
    38	  esac
    39	fi
    40
    41	path="$(jq -r '.tool_input.file_path // .tool_input.path // .tool_input.planFilePath // empty' <<<"$payload")"
    42
    43	if [[ -n "$path" ]] && is_allowed_claude_plan_path "$path"; then
    44	  : # exceção estrita para o runtime nativo de Plan Mode
    45	else
    46	  case "$path" in
    47	*/.git/*|*/.devcontainer/*|*/.github/workflows/*|*/scripts/ci/*|\
    48	*/.claude/*|*/.codex/*|*/.mcp.json|*/AGENT_POLICY.md|*/CLAUDE.md|\
    49	*/AGENTS.md|*/runbooks/*)
    50	    block "Bloqueado: caminho do plano de controle." ;;
    51	  esac
    52	fi
    53
    54	if [[ "$tool" == "Bash" ]]; then
    55	  cmd="$(jq -r '.tool_input.command // empty' <<<"$payload")"
    56	  # Fail-fast para formas diretas de comandos privilegiados.
    57	  # Não garante cobertura de sintaxe shell arbitrária ou wrappers indiretos
    58	  # — a proteção estrutural é o mount .git readonly no container.
    59	  case "$cmd" in
    60	    *"sudo "*|sudo*)
    61	      block "Bloqueado: sudo pertence a Davi." ;;
    62	    *"docker "*|docker*)
    63	      block "Bloqueado: Docker pertence a Davi." ;;
    64	    *"claude --dangerously-"*)
    65	      block "Bloqueado: flag --dangerously-* do Claude pertence a Davi." ;;
    66	    *"codex --dangerously-"*)
    67	      block "Bloqueado: flag --dangerously-* do Codex pertence a Davi." ;;
    68	  esac
    69
    70	  # Git: allowlist de inspeção (fail-closed), conforme AGENT_POLICY.md.
    71	  # Qualquer subcomando fora da lista é bloqueado por padrão, não só os
    72	  # conhecidos como mutáveis. -C/-c/--git-dir/--work-tree com valor em
    73	  # token separado são tratados para não confundir o valor com o
    74	  # subcomando. Ainda não cobre 100% da sintaxe shell arbitrária (variáveis,
    75	  # encoding, wrappers indiretos) — a proteção estrutural final continua
    76	  # sendo o mount .git readonly no container.
    77	  git_matches="$(grep -oE '\bgit\b([[:space:]]+(-C|-c|--git-dir|--work-tree|--namespace|--super-prefix)[[:space:]]+[^[:space:]]+|[[:space:]]+-[^[:space:]]+)*[[:space:]]+[a-zA-Z][a-zA-Z-]*' <<<"$cmd" || true)"
    78	  if [[ -n "$git_matches" ]]; then
    79	    while IFS= read -r match; do
    80	      subcmd="${match##* }"

=== posttool guard ===
     1	#!/usr/bin/env bash
     2	set -euo pipefail
     3	state_dir="/home/agent/.local/state/cepraea-guards"
     4	mkdir -p "$state_dir"
     5	payload="$(cat)"
     6	tool="$(jq -r '.tool_name // "desconhecido"' <<<"$payload")"
     7	printf '{"observado_em":"%s","tool":"%s"}\n' \
     8	  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     9	  "$tool" \
    10	  >> "$state_dir/events.jsonl"
    11	exit 0
Critical finding forming: the markdownlint config contains a rule that contradicts the runbooks. Let me get hard evidence.

Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== package.json? ==="; ls package.json 2>&1; echo "=== any package.json tracked ==="; git ls-files | grep -i "package.json\|tsconfig\|eslint" ; echo "(fim)"; echo; echo "=== markdownlint available? ==="; which markdownlint markdownlint-cli2 npx node 2>&1; echo; echo "=== node_modules? ==="; ls -d node_modules 2>&1

OUT
Exit code 2
=== package.json? ===
ls: cannot access 'package.json': No such file or directory
=== any package.json tracked ===
(fim)

=== markdownlint available? ===
/usr/local/bin/npx
/usr/local/bin/node

=== node_modules? ===
ls: cannot access 'node_modules': No such file or directory
Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== tracked file count by area ==="; git ls-files | sed 's|/.*||' | sort | uniq -c | sort -rn; echo; echo "=== docs tree ==="; git ls-files docs | head -60; echo; echo "=== test/ tmp/ ==="; git ls-files test tmp .drive 2>/dev/null | head -20; echo "(fim)"

OUT
=== tracked file count by area ===
    103 docs
     46 .drive
     13 runbooks
     13 .devcontainer
     10 .ai
      7 "docs
      2 .vscode
      1 test
      1 manifest.md
      1 manifest.json
      1 README.md
      1 CLAUDE.md
      1 AGENT_POLICY.md
      1 AGENTS.md
      1 .mcp.json
      1 .markdownlint.jsonc
      1 .gitignore
      1 .codex
      1 ".drive

=== docs tree ===
docs/arquiteturas/MATRIZ_CANONICA_FONTES_TECNICAS_CEPRAEA_BEACH_PRO.md
docs/arquiteturas/multi-agentes/Arquivos-Human-Governed Dual-Agent SDLC Architecture.md
docs/arquiteturas/multi-agentes/CONTAINER-RUNBOOK-v0.3.md
"docs/arquiteturas/multi-agentes/Exemplos-C\303\263digos.md"
docs/arquiteturas/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md
"docs/arquiteturas/multi-agentes/Implanta\303\247\303\243o-Human-Governed Dual-Agent SDLC Archite.md"
docs/arquiteturas/multi-agentes/Instructions-CLAUDE.md
docs/arquiteturas/multi-agentes/Relatorio Multi-Agentes.md
docs/arquiteturas/multi-agentes/Runbooks.md
docs/arquiteturas/task_atomics.md
docs/backlog/PLANO-FRONTMATTER.md
docs/backlog/verificacao-formal-fvr/README.md
"docs/backlog/verificacao-formal-fvr/planejamento/00-GUIA-0-IDENTIFICA\303\207\303\203O-BASELINE-ESCOPO.md"
docs/backlog/verificacao-formal-fvr/planejamento/01-ESTADO-ATUAL-ARQUITETURA.md
docs/backlog/verificacao-formal-fvr/planejamento/02-ESTADO-ARQUITETURA-FINAL.md
"docs/backlog/verificacao-formal-fvr/planejamento/03-PLANO-COMPLETO-TASKS-AT\303\224MICAS.md"
"docs/backlog/verificacao-formal-fvr/planejamento/05-RUNBOOK-IMPLEMENTA\303\207\303\203O.md"
"docs/backlog/verificacao-formal-fvr/planejamento/06-REGISTRO-DECIS\303\225ES-HUMANAS.md"
docs/backlog/verificacao-formal-fvr/runner/CONFORMANCE_CERTIFICATE_NOT_ISSUED.json
docs/backlog/verificacao-formal-fvr/runner/CONFORMANCE_HARNESS_REPORT.json
docs/backlog/verificacao-formal-fvr/runner/Guia-formatacao-markdown.md
docs/backlog/verificacao-formal-fvr/runner/IMPLEMENTATION_GUIDE.md
docs/backlog/verificacao-formal-fvr/runner/SYSTEM_REQUIREMENTS.json
docs/backlog/verificacao-formal-fvr/runner/WEB_EVALUATOR_PROMPT.txt
docs/backlog/verificacao-formal-fvr/runner/conformance_harness.py
docs/backlog/verificacao-formal-fvr/runner/coverage-map.json
docs/backlog/verificacao-formal-fvr/runner/expected-results.json
docs/backlog/verificacao-formal-fvr/runner/implementation-validation.json
docs/backlog/verificacao-formal-fvr/runner/manifest.schema.json
docs/backlog/verificacao-formal-fvr/runner/normative-semantics.json
docs/backlog/verificacao-formal-fvr/runner/package-validation.json
docs/backlog/verificacao-formal-fvr/runner/validation-report.json
docs/backlog/verificacao-formal-fvr/runner/verify.sh
docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md
docs/modelagem/README.md
docs/modelagem/candidatos/agregados.md
docs/modelagem/candidatos/bounded_contexts.md
docs/modelagem/candidatos/ciclos_de_vida.md
docs/modelagem/candidatos/fronteiras_transacionais.md
docs/modelagem/candidatos/identidades.md
docs/modelagem/candidatos/invariantes.md
docs/modelagem/conhecimento/conflitos_semanticos.md
docs/modelagem/conhecimento/glossario.md
docs/modelagem/conhecimento/registro_regras.md
docs/modelagem/decisoes/registro_decisoes.md
docs/modelagem/dominio/agregados.md
docs/modelagem/dominio/bounded_contexts.md
docs/modelagem/dominio/ciclos_de_vida.md
docs/modelagem/dominio/fronteiras_transacionais.md
docs/modelagem/dominio/identidades_definitivas.md
docs/modelagem/dominio/invariantes.md
docs/modelagem/dominio/modelo_canonico_dominio.md
docs/modelagem/evidencias/registro_evidencias.md
docs/modelagem/fontes/dossies/bancocepraea.docx.md
docs/modelagem/fontes/dossies/cepraea_agosto_2026.xlsx.md
docs/modelagem/fontes/inventario_fontes.md
docs/modelagem/logico/areas_pendentes.md
docs/modelagem/logico/modelo_logico_relacional.md
docs/modelagem/processo/criterios_maturidade.md
docs/modelagem/processo/fluxo_de_modelagem.md

=== test/ tmp/ ===
.drive/FVR-1.0/CONFORMANCE_CERTIFICATE_NOT_ISSUED.json
.drive/FVR-1.0/CONFORMANCE_HARNESS_REPORT.json
.drive/FVR-1.0/Guia-formatacao-markdown.md
.drive/FVR-1.0/IMPLEMENTATION_GUIDE.md
.drive/FVR-1.0/SYSTEM_REQUIREMENTS.json
.drive/FVR-1.0/WEB_EVALUATOR_PROMPT.txt
.drive/FVR-1.0/conformance_harness.py
.drive/FVR-1.0/coverage-map.json
.drive/FVR-1.0/expected-results.json
.drive/FVR-1.0/implementation-validation.json
.drive/FVR-1.0/manifest.schema.json
.drive/FVR-1.0/normative-semantics.json
.drive/FVR-1.0/package-validation.json
.drive/FVR-1.0/validation-report.json
.drive/FVR-1.0/verify.sh
.drive/Fluxo Completo/Fluxo Completo de Desenvolvimento.md
.drive/Guia de Estilo Conteudo.md
.drive/agents/architect.md
.drive/agents/change-manager.md
.drive/agents/commands/check-progress.md
(fim)
No package.json, no node_modules, no lint/typecheck/test infrastructure exists. Let me confirm what deterministic validators actually run today.

Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== run task-proposal validator ==="; node .ai/control/validate-task-proposal.mjs 2>&1 | head -20; echo "exit=$?"; echo; echo "=== validator deps ==="; grep -n "^import\|require(" .ai/control/validate-task-proposal.mjs | head; echo; echo "=== test/ dir ==="; find test -type f | head; echo; echo "=== conflito: quantos '](..' nos runbooks e docs ==="; grep -rc "](\.\." runbooks/ | sort; echo "--- total docs ---"; grep -rl "](\.\." docs/ | wc -l

OUT
=== run task-proposal validator ===
VALID: /workspaces/cepraea-beach-pro/.ai/task-proposal.example.json conforms to /workspaces/cepraea-beach-pro/.ai/control/task-proposal.schema.json
exit=0

=== validator deps ===
8:import { readFileSync } from "node:fs";
9:import { fileURLToPath } from "node:url";
10:import { dirname, join } from "node:path";

=== test/ dir ===
test/fixtures/synthetic/agent-plan-smoke.txt

=== conflito: quantos '](..' nos runbooks e docs ===
runbooks/README.md:1
runbooks/executor/RB-EXEC-001-code-change.md:4
runbooks/executor/RB-EXEC-002-database-change.md:4
runbooks/executor/RB-EXEC-003-documentation-change.md:4
runbooks/executor/RB-EXEC-004-dependency-change.md:3
runbooks/reviewer/RB-REV-001-code-review.md:2
runbooks/reviewer/RB-REV-002-database-review.md:5
runbooks/reviewer/RB-REV-003-documentation-review.md:5
runbooks/reviewer/RB-REV-004-evidence-review.md:4
runbooks/reviewer/RB-REV-005-dependency-review.md:7
runbooks/shared/RB-SHARED-001-repository-baseline.md:3
runbooks/shared/RB-SHARED-002-evidence.md:1
runbooks/shared/RB-SHARED-003-failure-states.md:3
--- total docs ---
4
Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== DEC-GOV-002 ==="; cat -n .ai/decisions/DEC-GOV-002-runbook-binding-modelagem-canonica.md

OUT
=== DEC-GOV-002 ===
     1	# DEC-GOV-002 — `runbook_binding` formal para `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN` da modelagem canônica
     2
     3	**Data:** 2026-08-16
     4	**Status:** APROVADO
     5	**Aprovador:** Davi Sermenho
     6	**Tipo:** governança documental — binding de runbooks, sem rebuild
     7
     8	## Contexto
     9
    10	Durante a revisão adversarial de `AC-001`, o Reviewer (Codex, `AGENTS.md`) apontou que nem
    11	`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` nem `runbooks/README.md` declaram um
    12	`runbook_binding` concreto para as tarefas desta fase — confirmado por inspeção direta (`grep` em
    13	ambos os arquivos, zero ocorrências de `runbook_binding`/`operation_class`/`applicable_runbooks`).
    14	A afirmação de handoffs anteriores do Executor (de que `RB-EXEC-003` seria o binding real desta
    15	fase) era uma inferência não registrada como artefato verificável, o que `AGENTS.md` trata como
    16	divergência material — bloqueia `PASS` até decisão de Davi (`HUMAN_DECISION_REQUIRED`). Davi
    17	aprovou o binding formal.
    18
    19	**Correção desta revisão:** a primeira versão desta decisão afirmava que "todo artefato produzido
    20	por `AC-NNN`/`SEM-NNN`/`SYN-NNN` é Markdown", generalizando `documentation_change` para toda a
    21	fase, inclusive `AC-000`. Achado do `REVIEWER` (`FAIL`, severidade MEDIUM): o critério de DONE de
    22	`AC-000` exige `schemas/*.json` e três scripts `.mjs`, confirmados no commit `2bf9214` — uma
    23	classe de operação heterogênea, não só documental. A generalização estava errada; corrigida
    24	abaixo, delimitando o binding às tarefas cujas alterações são exclusivamente documentais.
    25
    26	## Decisão
    27
    28	As tarefas `AC-001` a `AC-029`, `SEM-NNN` e `SYN-NNN` da fase de modelagem canônica
    29	(`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`, "procedimento repetível" e síntese
    30	final — seção 10.0 em diante) usam o seguinte `runbook_binding` formal:
    31
    32	```json
    33	{
    34	  "runbook_binding": {
    35	    "operation_classes": ["documentation_change"],
    36	    "applicable_runbooks": {
    37	      "shared": [
    38	        "runbooks/shared/RB-SHARED-001-repository-baseline.md",
    39	        "runbooks/shared/RB-SHARED-002-evidence.md",
    40	        "runbooks/shared/RB-SHARED-003-failure-states.md"
    41	      ],
    42	      "executor": [
    43	        "runbooks/executor/RB-EXEC-003-documentation-change.md"
    44	      ],
    45	      "reviewer": [
    46	        "runbooks/reviewer/RB-REV-003-documentation-review.md",
    47	        "runbooks/reviewer/RB-REV-004-evidence-review.md"
    48	      ]
    49	    }
    50	  }
    51	}
    52	```
    53
    54	### `AC-000` está fora do escopo desta decisão
    55
    56	`AC-000` (bootstrap) produziu `schemas/*.json` e os três scripts `.mjs` (`validar.mjs`,
    57	`verificar_referencias.mjs`, `verificar_repositorio.mjs`) — confirmado no commit `2bf9214` — uma
    58	classe de operação heterogênea (`code_change` + `documentation_change`), não só
    59	`documentation_change`. `AC-000` já foi concluído, revisado (`PASS`) e commitado antes desta
    60	decisão, sob o fluxo geral de `CLAUDE.md`/`AGENTS.md` sem binding formal; esta decisão não o
    61	reclassifica retroativamente.
    62
    63	### Por que `AC-001` a `AC-029`/`SEM-NNN`/`SYN-NNN` são puramente `documentation_change`
    64
    65	O "procedimento repetível" do plano (a partir de `AC-001`) não cria nem altera `schemas/*.json`
    66	nem `*.mjs` — schemas e scripts ficam congelados a partir de `AC-000`; cada turno só produz
    67	Markdown com blocos JSON validados por eles, sob `docs/modelagem/**`. O mesmo vale para a síntese
    68	final (`AC-029`, `SEM-NNN`, `SYN-NNN`): consolidação e reconciliação, sempre em Markdown/JSON de
    69	conteúdo, nunca em schema ou script.
    70
    71	Se uma tarefa futura desta fase voltar a alterar `schemas/*.json` ou `*.mjs` (por exemplo, uma
    72	correção de ferramental descoberta durante o processamento de uma fonte), ela sai do escopo deste
    73	binding e exige `operation_classes` adicionais (`code_change` → `RB-EXEC-001`/`RB-REV-001`), a
    74	declarar em decisão própria — não coberto por esta decisão.
    75
    76	### Justificativa da inclusão de `RB-REV-004`
    77
    78	`runbooks/README.md` exige `RB-REV-004-evidence-review.md` adicionalmente quando "a suficiência da
    79	evidência for material para os critérios de aceite ou para a revisão independente". Nesta fase,
    80	isso já se mostrou empiricamente verdadeiro em `AC-001`: várias rodadas de revisão adversarial
    81	identificaram problemas de suficiência/precisão de evidência (abas/linhas não lidas, localização
    82	incorreta de fragmento, classificação incorreta de dado sensível) — não defeitos de sintaxe ou
    83	formatação, mas exatamente o tipo de achado que `RB-REV-004` existe para cobrir. A inclusão é
    84	permanente para `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN`, não caso a caso por tarefa.
    85
    86	## Consequência
    87
    88	- O Executor carrega, a partir desta decisão, exatamente os runbooks listados acima em todo turno
    89	  `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN`, além de `AGENT_POLICY.md`/`CLAUDE.md` e da normativa de
    90	  `docs/modelagem/`. `AC-000` não é afetado — já concluído.
    91	- O Reviewer carrega os runbooks `shared`/`reviewer` acima em toda revisão de `AC-001` em diante
    92	  nesta fase, além de `AGENT_POLICY.md`/`AGENTS.md`.
    93	- Handoffs de tarefas desta fase devem citar este binding (por número de decisão ou pelo bloco
    94	  JSON acima) para que a vinculação seja verificável no repositório, não apenas declarada em
    95	  prosa.
    96	- Se uma tarefa futura alterar `schemas/*.json` ou `*.mjs`, o binding desta decisão não se aplica
    97	  a ela sem extensão explícita — ver seção acima.
    98	- Esta decisão não altera `runbooks/README.md` nem os runbooks especializados — apenas registra a
    99	  seleção concreta já prevista pelo mecanismo do catálogo para esta fase.
Key discovery: DEC-GOV-002 does require handoffs to cite the binding — but only for modeling-phase tasks. Let me check whether the agents can ever see that rule.

Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== quem referencia .ai/decisions ? ==="; grep -rn "\.ai/decisions\|DEC-GOV\|DEC-ARQ\|DEC-CTR" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/ 2>/dev/null; echo "(fim)"; echo; echo "=== quem referencia task_atomics ? ==="; grep -rn "task_atomics\|task_proposal\|task-proposal" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/ 2>/dev/null; echo "(fim)"; echo; echo "=== quem referencia .ai/control ? ==="; grep -rn "\.ai/" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/ manifest.md 2>/dev/null | head; echo "(fim)"

OUT
=== quem referencia .ai/decisions ? ===
(fim)

=== quem referencia task_atomics ? ===
(fim)

=== quem referencia .ai/control ? ===
manifest.md:21:186 pertencem a diretórios ocultos de infraestrutura (`.ai/`,
manifest.md:316:`.ai/`, `.devcontainer/` e `.codex/` não aparecem na árvore acima porque
(fim)
Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== manifest.md head ==="; head -60 manifest.md; echo; echo "=== manifest.json keys ==="; node -e "const m=require('./manifest.json');console.log(Object.keys(m));console.log(JSON.stringify(m).slice(0,800))" 2>&1 | head -20

OUT
=== manifest.md head ===
# Inventário do repositório (manifest)



Este documento mapeia a estrutura atual do projeto `CEPRAEA Beach pro`.

Este é o mapa **narrativo/humano**, no nível de cada arquivo individual. O
mapa **estruturado/máquina**, no nível dos ativos principais (pastas e
arquivos-chave), fica em [`manifest.json`](./manifest.json) — os dois se
complementam: quando um ativo existe nos dois arquivos, as colunas
`Tipo de Ativo`, `Propósito`, `Consumidor` e `Status` da tabela abaixo
apontam para `manifest.json` em vez de repetir o valor, para não haver duas
fontes divergentes do mesmo fato. `Resumo Executivo` e `Link` são exclusivos
deste arquivo.

## Mapa de arquivos

**Correção de proveniência (achado do Reviewer, 2026-08-18):** o comando
abaixo, executado literalmente sobre a raiz do repositório hoje, produz 330
entradas (`find . -type d -name ".git" -prune -o -print | wc -l`), das quais
186 pertencem a diretórios ocultos de infraestrutura (`.ai/`,
`.devcontainer/`, `.codex/`, `.drive/`, `.vscode/`) — não reproduz a árvore
de 136 linhas abaixo. A árvore foi filtrada manualmente para o "projeto
visível" (governança na raiz, `docs/`, `runbooks/`, `test/`); os diretórios
de infraestrutura ficam fora por decisão de escopo, não por efeito do
comando, e estão mapeados separadamente em
[`manifest.json`](./manifest.json). O comando que efetivamente reproduz o
conjunto de caminhos abaixo (verificado: 134 entradas brutas, compatível com
as 136 linhas após numeração e formatação manual dos comentários) é:

```bash
find AGENT_POLICY.md AGENTS.md CLAUDE.md README.md docs runbooks test -print \
  | sed -e 's;[^/]*/;├── ;g;s;├── |;│   ;g'
```
<!-- Árvore original gerada em 18/08/2026 às 08:00; comentários adicionados em seguida -->

```txt
├── AGENTS.md                 ← Papel operacional do Reviewer (Codex) — ver manifest.json
├── AGENT_POLICY.md           ← Política comum dos três agentes — ver manifest.json
├── CLAUDE.md                 ← Papel operacional do Executor (Claude Code) — ver manifest.json
├── README.md                 ← Apresentação do projeto, stack e setup — ver manifest.json
├── docs
|  ├── arquiteturas
|  |  ├── assurance          ← Estado atual/alvo do fluxo de assurance — ver manifest.json
|  |  |  ├── ESTADO-ARQUITETURA-FINAL.md      ← Estado-alvo pretendido (ainda não implantado)
|  |  |  ├── ESTADO-ATUAL-ARQUITETURA.md      ← Estado operacional vigente
|  |  |  ├── GUIA-0-IDENTIFICAÇÃO-BASELINE-ESCOPO.md ← Baseline/branch/escopo da implantação
|  |  |  ├── PLANO-COMPLETO-TASKS-ATÔMICAS.md ← Tasks da implantação, por fase, com gate
|  |  |  ├── REGISTRO-DECISÕES-HUMANAS.md     ← Decisões humanas confirmadas (HDEC-xxx)
|  |  |  └── RUNBOOK-IMPLEMENTAÇÃO.md         ← Runbook de execução das TASK-ARCH
|  |  ├── multi-agentes      ← Arquitetura do Dual-Agent SDLC e do dev container — ver manifest.json
|  |  |  ├── Arquivos-Human-Governed Dual-Agent SDLC Architecture.md ← Especifica os arquivos que materializam a arquitetura
|  |  |  ├── CONTAINER-RUNBOOK-v0.3.md        ← Fonte de verdade técnica do dev container
|  |  |  ├── Human-Governed Dual-Agent SDLC Architecture.md ← Documento arquitetural principal (arc42)
|  |  |  ├── Implantação-Human-Governed Dual-Agent SDLC Archite.md ← Checklist de validação real (CT-01..CT-17)
|  |  |  ├── Relatorio Multi-Agentes.md       ← Enforcement real vs. política escrita, lacunas
|  |  |  └── Runbooks.md                      ← Arquitetura da biblioteca de runbooks
|  |  └── task_atomics.md    ← Padrão de task atômica (contrato Task Proposal v2) — ver manifest.json
|  ├── modelagem
|  |  ├── PLANO_CEPRAEA_Modelo_Canonico_FINAL.md ← Documento canônico normativo — ver manifest.json

=== manifest.json keys ===
[ 'project', 'version', 'updated_at', 'assets' ]
{"project":"CEPRAEA BEACH PRO","version":"0.1.0","updated_at":"2026-08-18","assets":[{"path":"AGENT_POLICY.md","type":"governance","purpose":"Política comum dos três agentes: papéis, classificação de risco, escopo de Git permitido, lista de control-plane read-only, fontes.","consumers":["human","agent:executor","agent:reviewer"],"status":"active"},{"path":"CLAUDE.md","type":"governance","purpose":"Papel operacional do Executor (Claude Code): proposta proporcional, execução, validação, handoff.","consumers":["human","agent:executor"],"status":"active"},{"path":"AGENTS.md","type":"governance","purpose":"Papel operacional do Reviewer (Codex): procedimento de revisão independente, findings, vereditos.","consumers":["human","agent:reviewer"],"status":"active"},{"path":"README.md","type":"govern
Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== docs/arquiteturas/assurance existe? ==="; ls docs/arquiteturas/ 2>&1; echo; echo "=== manifest.md cita assurance mas arquivo real está em: ==="; git ls-files "docs/backlog/verificacao-formal-fvr/planejamento" ; echo; echo "=== manifest.json aponta para caminhos inexistentes? ==="; node -e "
const m=require('./manifest.json');const fs=require('fs');
let bad=[];for(const a of m.assets){if(!fs.existsSync(a.path))bad.push(a.path);}
console.log('assets total:',m.assets.length);console.log('inexistentes:',bad.length);bad.forEach(p=>console.log('  MISSING:',p));"

OUT
=== docs/arquiteturas/assurance existe? ===
MATRIZ_CANONICA_FONTES_TECNICAS_CEPRAEA_BEACH_PRO.md
multi-agentes
task_atomics.md

=== manifest.md cita assurance mas arquivo real está em: ===
"docs/backlog/verificacao-formal-fvr/planejamento/00-GUIA-0-IDENTIFICA\303\207\303\203O-BASELINE-ESCOPO.md"
docs/backlog/verificacao-formal-fvr/planejamento/01-ESTADO-ATUAL-ARQUITETURA.md
docs/backlog/verificacao-formal-fvr/planejamento/02-ESTADO-ARQUITETURA-FINAL.md
"docs/backlog/verificacao-formal-fvr/planejamento/03-PLANO-COMPLETO-TASKS-AT\303\224MICAS.md"
"docs/backlog/verificacao-formal-fvr/planejamento/05-RUNBOOK-IMPLEMENTA\303\207\303\203O.md"
"docs/backlog/verificacao-formal-fvr/planejamento/06-REGISTRO-DECIS\303\225ES-HUMANAS.md"

=== manifest.json aponta para caminhos inexistentes? ===
assets total: 42
inexistentes: 1
  MISSING: docs/arquiteturas/assurance/
Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== 02-ESTADO-ARQUITETURA-FINAL (head 80) ==="; head -80 "docs/backlog/verificacao-formal-fvr/planejamento/02-ESTADO-ARQUITETURA-FINAL.md"

OUT
=== 02-ESTADO-ARQUITETURA-FINAL (head 80) ===
ESTADO PRETENDIDO COM A ARQUITETURA FINAL

2.1 Arquitetura final pretendida

Autoridade Humana
↓
Task Proposal
↓
Task Contract formal
↓
Verification Plan
↓
Aprovação humana vinculada por hashes
↓
Claude Code — Executor
↓
Artefato candidato
↓
Verifier determinístico
↓
PASS | FAIL | BLOCKED
↓
Codex — Reviewer independente
↓
PASS | FAIL | HUMAN_DECISION_REQUIRED
↓
Homologação humana
↓
Git / promoção

2.2 Separação de funções

Executor ≠ Verifier ≠ Reviewer ≠ Autoridade Humana.

Executor
Produz e corrige o artefato candidato.

Verifier
Calcula propriedades formalizadas a partir de observações reproduzíveis.

Reviewer
Realiza assurance independente sobre semântica residual, regressões, completude, adequação de testes, suficiência de evidência, overclaims e possíveis lacunas do contrato.

Humano
Define significado, autoriza contrato e escopo, resolve decisões materiais, homologa e executa transições Git privilegiadas.

2.3 Regra matemática de decisão formal

Cada propriedade Pi assume exatamente um dos estados:
TRUE, FALSE ou UNKNOWN.

FAIL se existir pelo menos uma propriedade FALSE.
BLOCKED se não existir FALSE e existir pelo menos uma propriedade UNKNOWN.
PASS somente se todas as propriedades forem TRUE.

Ausência de evidência nunca é convertida em PASS.

2.4 Regra de precedência

FormalResult != PASS implica que o Reviewer não pode emitir PASS sobre a tarefa.
FormalResult == PASS não obriga Reviewer PASS.

Uma decisão humana que considere o contrato incorreto deve gerar revisão do contrato, nova aprovação e nova verificação. Não deve existir bypass narrativo que converta uma propriedade formal falsa em verdadeira.

2.5 Contrato formal da tarefa

Cada Task Contract deve possuir, no mínimo:
• contract_id e versão;
• task_id e vínculo com a proposta;
• baseline Git;
• read-set;
• write-set;
• forbidden-set;
• invariantes;
• critérios de aceite;
• propriedades formais;
• propriedades residuais de review;
• procedimentos de observação;
• bindings de evidência;
• política fail-closed;
The target architecture is already designed — a deterministic Verifier role — but sits in docs/backlog/. Let me check how far it's specified.

Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== verification-plan.schema.json (top-level) ==="; node -e "const s=require('./.ai/control/verification-plan.schema.json');console.log('title:',s.title);console.log('required:',s.required);console.log('props:',Object.keys(s.properties||{}));"; echo; echo "=== 03-PLANO-COMPLETO-TASKS (head 70) ==="; head -70 "docs/backlog/verificacao-formal-fvr/planejamento/03-PLANO-COMPLETO-TASKS-ATÔMICAS.md"

OUT
=== verification-plan.schema.json (top-level) ===
title: FVR-1.0 Verification Plan Schema
required: [
  'schema_version',
  'plan_metadata',
  'control',
  'workspace',
  'policy',
  'environment',
  'steps',
  'assertions'
]
props: [
  'schema_version',
  'plan_metadata',
  'control',
  'workspace',
  'policy',
  'environment',
  'steps',
  'assertions'
]

=== 03-PLANO-COMPLETO-TASKS (head 70) ===
# PLANO COMPLETO EM TASKS ATÔMICAS

**Princípio**
Uma task atômica deve produzir um único resultado verificável, não misturar decisões humanas com implementação mecânica e não avançar automaticamente quando sua pós-condição falhar.

***

## FASE A — GOVERNANÇA E BASELINE

TASK-ARCH-001 — Homologar o escopo da mudança arquitetural
Owner: Humano.
Entrada: este documento e arquitetura vigente.
Ação: confirmar quais componentes de control plane podem ser alterados.
Saída: decisão humana explícita.
Gate: sem aprovação, nenhuma task de escrita do control plane inicia.

TASK-ARCH-002 — Definir a branch de implantação
Owner: Humano.
Ação: escolher nome, base e política de integração.
Saída: branch autorizada.
Gate: branch diferente de main para execução por agentes.

TASK-ARCH-003 — Capturar baseline imutável da execução
Owner: Executor, somente inspeção.
Ação: registrar HEAD da branch, HEAD de main, git status e hashes dos arquivos de controle relevantes.
Saída: baseline verificável.
Gate: working tree e refs coerentes com a tarefa aprovada.

TASK-ARCH-004 — Definir critérios de rollout
Owner: Humano + Reviewer.
Ação: fixar condições que diferenciam PILOT, READY e MANDATORY.
Saída: critérios binários de promoção.
Gate: critérios não podem depender de opinião narrativa indefinida.

TASK-ARCH-005 — Decidir branch protection
Owner: Humano.
Ação: avaliar risco de main sem proteção e decidir configuração.
Saída: decisão registrada; alteração de GitHub somente se autorizada.

***

## FASE B — MODELO FORMAL DO CONTRATO

TASK-ARCH-006 — Criar task-contract.schema.json
Owner: Executor.
Ação: definir estrutura normativa do Task Contract.
Saída: schema válido.
Gate: additionalProperties controlado, IDs e hashes tipados.

TASK-ARCH-007 — Criar assertion.schema.json
Owner: Executor.
Ação: definir a estrutura de uma propriedade verificável.
Saída: schema com domain, operator, operands, expected e observation binding.
Gate: nenhuma assertion aceita lógica textual arbitrária como autoridade.

TASK-ARCH-008 — Criar verification-result.schema.json
Owner: Executor.
Ação: definir PASS, FAIL e BLOCKED e a estrutura das evidências/violações.
Saída: schema validável.
Gate: resultado global derivável dos resultados individuais.

TASK-ARCH-009 — Criar task-approval.schema.json
Owner: Executor.
Ação: transformar o example de aprovação em schema normativo.
Saída: approval vinculada por digest à proposta, contrato, plano e baseline.
Gate: alteração de qualquer artefato vinculado invalida approval anterior.

TASK-ARCH-010 — Evoluir task-proposal
Owner: Executor.
Ação: adicionar IDs estáveis de critérios e classificação formal/reviewer.
Bash
IN
cd /workspaces/cepraea-beach-pro; echo "=== 01-ESTADO-ATUAL (head 90) ==="; head -90 "docs/backlog/verificacao-formal-fvr/planejamento/01-ESTADO-ATUAL-ARQUITETURA.md"

OUT
=== 01-ESTADO-ATUAL (head 90) ===
# ESTADO ATUAL DA ARQUITETURA

## 1.1 Arquitetura operacional vigente

O fluxo atual é um Human-Governed Dual-Agent SDLC:

Humano → Claude Code EXECUTOR → validações determinísticas → working tree/git diff → Codex REVIEWER → Humano → Git.

A política comum estabelece:
- o humano é a autoridade final sobre domínio, decisões materiais, Git, release e deploy;
- Claude Code é o EXECUTOR;
- Codex é o REVIEWER independente;
- produção, revisão e aprovação são funções distintas;
- nenhum agente pode aprovar ou promover o próprio trabalho;
- operações Git que alteram refs, index, histórico ou remoto pertencem ao humano;
- restrições não podem ser contornadas; incapacidade legítima gera BLOCKED ou HUMAN_DECISION_REQUIRED.

## 1.2 Executor

O Executor:
- recebe a tarefa autorizada;
- lê o contexto necessário;
- identifica validadores aplicáveis;
- produz somente a mudança autorizada;
- executa validações determinísticas;
- corrige erros mecânicos;
- inspeciona git diff, git diff --check e git status;
- entrega READY_FOR_REVIEW ou BLOCKED.

O Executor não possui autoridade para declarar a entrega homologada.

## 1.3 Reviewer

O Reviewer:
- opera de forma independente;
- inspeciona diff, status, arquivos-alvo, critérios e evidências;
- procura regressões;
- tenta refutar conclusões materiais;
- verifica rastreabilidade e suficiência de evidência;
- reexecuta checks proporcionalmente ao risco;
- não corrige findings nem altera os artefatos sob revisão;
- emite PASS, FAIL ou HUMAN_DECISION_REQUIRED.

O Reviewer continua obrigatório na arquitetura vigente.

## 1.4 Validação determinística existente

Já existem validadores determinísticos e uma estrutura FVR. O verification-plan suporta operações como file.exists, file.sha256, git.diff, git.diff_names e process.run em sandbox, além de assertions identificadas por AC-NNN e INV-NNN.

Entretanto, o task-proposal ainda representa critérios de aceite principalmente por strings humanas: condição, método e esperado. Portanto, existe um gap entre a tarefa textual e as assertions formais.

## 1.5 Estado do FVR

O pacote FVR existente se declara implementation candidate. A conformidade não é concedida apenas porque o runner executa.

O certificado disponível registra NOT_ISSUED / HARNESS_INVALID. Logo, não existe evidência suficiente, no baseline atual, para tratar o runner FVR como verificador conformante de produção do fluxo.

## 1.6 Gap principal

Estado atual:
Task Proposal textual → Executor → validadores → Reviewer.

Gap:
não existe ainda uma camada normativa completa que faça a transformação:
requisito humano → propriedade formal tipada → observação determinística → assertion → PASS/FAIL/BLOCKED.

## 1.7 Riscos atuais relevantes para a implantação

ID | Risco
:---: | ---
R-001  |  Critérios de aceite textuais permitem interpretação diferente entre Executor e Reviewer.
R-002  |  Um validador pode ser determinístico e ainda implementar uma regra formal incorreta.
R-003  |  O FVR ainda não possui conformidade comprovada no ambiente atual.
R-004  |  Ausência de ligação completa por hash entre proposta, contrato, plano e resultado pode permitir drift.
R-005  |  Reviewer ainda precisa recalcular fatos que poderiam ser decididos mecanicamente.
R-006  |  Uma propriedade formal incompleta pode produzir PASS técnico sem representar toda a intenção humana.
R-007  |  A branch main aparece sem branch protection no baseline observado.
R-008  |  Alterar simultaneamente policy, schemas, runner, container e runbooks ampliaria excessivamente o blast radius.
Let me quantify subjectivity mechanically rather than by opinion.

Bash
IN
cd /workspaces/cepraea-beach-pro
echo "arquivo | linhas | termos_subjetivos | ocorrencias"
for f in AGENT_POLICY.md CLAUDE.md AGENTS.md runbooks/README.md runbooks/shared/RB-SHARED-002-evidence.md runbooks/shared/RB-SHARED-003-failure-states.md runbooks/reviewer/RB-REV-001-code-review.md runbooks/reviewer/RB-REV-003-documentation-review.md runbooks/reviewer/RB-REV-004-evidence-review.md runbooks/executor/RB-EXEC-001-code-change.md runbooks/executor/RB-EXEC-003-documentation-change.md docs/arquiteturas/task_atomics.md; do
  n=$(wc -l < "$f")
  # termos que exigem julgamento, sem limiar definido no proprio corpus
  occ=$(grep -oiE "\b(material|materiais|materialmente|proporcional(mente)?|relevante|aplicáve(l|is)|quando necessário|suficiente|insuficiência|adequa(ção|do|da)|apropriad|razoáve|conforme o impacto|quando existirem|excessiv|pertinente|significativ)" "$f" | wc -l)
  printf "%-58s | %4s | %3s\n" "$f" "$n" "$occ"
done

OUT
arquivo | linhas | termos_subjetivos | ocorrencias
AGENT_POLICY.md                                            |  149 |   8
CLAUDE.md                                                  |   85 |   4
AGENTS.md                                                  |   90 |   7
runbooks/README.md                                         |  201 |  17
runbooks/shared/RB-SHARED-002-evidence.md                  |   88 |  11
runbooks/shared/RB-SHARED-003-failure-states.md            |  106 |   6
runbooks/reviewer/RB-REV-001-code-review.md                |  105 |  10
runbooks/reviewer/RB-REV-003-documentation-review.md       |  104 |   9
runbooks/reviewer/RB-REV-004-evidence-review.md            |  103 |  17
runbooks/executor/RB-EXEC-001-code-change.md               |  104 |   3
runbooks/executor/RB-EXEC-003-documentation-change.md      |  101 |   3
docs/arquiteturas/task_atomics.md                          |  285 |  15
Bash
IN
cd /workspaces/cepraea-beach-pro
echo "=== comandos determinísticos citados nos runbooks vs existência real ==="
grep -rhoE "\b(npm run [a-z:]+|markdownlint|npx [a-z@/-]+|node [^ ]+\.mjs|pytest|tsc|eslint)" runbooks/ CLAUDE.md AGENT_POLICY.md AGENTS.md | sort | uniq -c | sort -rn
echo
echo "=== existe algum desses? ==="
for c in "npm run lint" "npm run typecheck" "markdownlint"; do printf "%-20s -> " "$c"; command -v ${c%% *} >/dev/null && echo "binário presente" || echo "AUSENTE"; done
echo "package.json      -> $( [ -f package.json ] && echo presente || echo AUSENTE)"
echo "validate-task-proposal.mjs -> $( [ -f .ai/control/validate-task-proposal.mjs ] && echo presente || echo AUSENTE)"

OUT
=== comandos determinísticos citados nos runbooks vs existência real ===
      3 markdownlint
      2 npm run typecheck
      1 npm run lint
      1 npm run build

=== existe algum desses? ===
npm run lint         -> binário presente
npm run typecheck    -> binário presente
markdownlint         -> AUSENTE
package.json      -> AUSENTE
validate-task-proposal.mjs -> presente
Análise concluída. Li os arquivos de governança, os 13 runbooks, o control plane .ai/, o plugin Codex instalado e o histórico Git. Nenhum arquivo foi alterado.

Diagnóstico central
A arquitetura tem Reviewer, mas não tem Verifier. P1, P3 e P5 são o mesmo defeito visto de ângulos diferentes: fatos que deveriam ser calculados estão sendo argumentados entre dois LLMs em linguagem natural.

Duas evidências fecham isso:

A camada de "validadores determinísticos" está vazia. Não existe package.json, node_modules nem markdownlint no repositório. RB-EXEC-001:67-68 prescreve npm run lint e npm run typecheck; RB-EXEC-003:66 e RB-REV-003:69 prescrevem markdownlint. Nenhum existe. O único validador executável é validate-task-proposal.mjs (rodei: exit 0). E RB-SHARED-003:26 exige "validadores determinísticos executados sem falhas bloqueantes" como pré-condição de READY_FOR_REVIEW — uma condição que hoje é logicamente vazia.

O diagnóstico já está escrito no próprio repositório. 01-ESTADO-ATUAL-ARQUITETURA.md lista R-001 — Critérios de aceite textuais permitem interpretação diferente entre Executor e Reviewer e R-005 — Reviewer ainda precisa recalcular fatos que poderiam ser decididos mecanicamente. Isso é literalmente P1 e P5. E 02-ESTADO-ARQUITETURA-FINAL.md já projeta a correção: Executor ≠ Verifier ≠ Reviewer ≠ Autoridade Humana, com a regra FormalResult != PASS ⟹ Reviewer não pode emitir PASS.

A solução não precisa ser inventada. Precisa sair de docs/backlog/.

P1 — Handoff para o Revisor
O handoff é obrigatório?
Sim, mas por uma razão mais estreita do que o fluxo assume hoje. CLAUDE.md:68-79 define seis categorias e RB-SHARED-003:31 torna "handoff factual produzido" pré-condição de READY_FOR_REVIEW.

O objetivo real do handoff não é transmitir estado — AGENT_POLICY.md:39 já diz que "Git é a state machine e o mecanismo de handoff". O handoff carrega exatamente o que o diff não carrega: o que foi tentado e falhou, o que ficou fora de escopo por decisão, qual limitação é conhecida, onde o Executor não conseguiu provar algo. É um registro de incerteza, não um resumo.

Hoje ele é usado como resumo — e um resumo é redundante com o diff, o que explica por que a discussão sobre sua ausência foi possível.

Handoff ou diff?
Ambos, com papéis distintos e não intercambiáveis:

Fonte	Autoridade sobre
git diff / git status	O que mudou. Autoritativo.
Handoff	O que o Executor não conseguiu provar, e por quê. Não autoritativo, mas insubstituível.
task_proposal / plano aprovado	O que deveria ter mudado. Contrato.
O erro do Reviewer foi tratar o handoff como fonte de contrato (runbook_binding). Contrato é o terceiro artefato, que naquele turno não existia.

Que tipo de revisão?
A arquitetura já diferencia — o problema é que a diferenciação não é acionável. AGENTS.md:39-52 define um procedimento único de 12 passos, mas runbooks/README.md seleciona runbooks por operation_class, e cada RB-REV traz uma perspectiva própria:

RB-REV-001 — regressão, adequação de testes, comportamento observável.
RB-REV-002 — adversarial sobre migrations, casos positivos e negativos.
RB-REV-003 — separa explicitamente forma de correção técnica (RB-REV-003:54).
RB-REV-004 — suficiência de evidência e reprodução independente.
Então: não, as revisões não devem ser iguais, e a instrução já existe — mas só é alcançada via runbook_binding, que só existe quando há task_proposal, que só é obrigatória para risco amarelo ou superior. Para risco verde, o Reviewer cai no procedimento genérico de AGENTS.md sem perspectiva definida. Essa é a lacuna.

Postura adversarial: AGENTS.md:48-50 já manda "tentar refutar conclusões materiais" e "procurar afirmações mais fortes que suas evidências". Isso é adversarial por design e está correto. O que falta não é mais adversarialidade — é delimitação do que é legitimamente atacável.

De quem é a culpa quando o Reviewer reprova por falta de handoff?
Da arquitetura, e consigo demonstrar isso mecanicamente.

Existe uma assimetria textual real entre os dois arquivos de papel:

CLAUDE.md:9 — "Quando existir runbook_binding na tarefa/plano aprovado" → condicional.
AGENTS.md:13 — "leia o runbook_binding da tarefa sob revisão" → imperativo incondicional.
Lido literalmente, o Reviewer tem uma obrigação que o Executor não tem o dever correspondente de satisfazer. Ele executou a instrução dele corretamente.

Pior: a regra que ele estava lembrando existe de verdade. DEC-GOV-002:93-95 diz textualmente:

"Handoffs de tarefas desta fase devem citar este binding [...] para que a vinculação seja verificável no repositório, não apenas declarada em prosa."

Só que essa obrigação é escopada a AC-001–AC-029/SEM-NNN/SYN-NNN. A tarefa do manifesto não é dessas. O Reviewer aplicou uma regra real fora do escopo dela — e não tinha como saber o escopo, porque:


grep -rn "DEC-GOV\|\.ai/decisions" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/
→ zero ocorrências
Nenhum dos dois agentes carrega .ai/decisions/ em nenhum momento. Existe uma decisão aprovada, normativa e vinculante que é invisível para ambos os papéis. Não é erro de julgamento do Codex; é uma fonte normativa órfã.

Como mitigar interpretação errada do Reviewer?
Três mecanismos, em ordem de força:

Mover fatos para fora do julgamento. "O binding bate com a matriz" não deveria ser uma leitura comparativa de dois Markdown por dois LLMs. Deveria ser um script que sai 0 ou 1. Enquanto for prosa, dois modelos vão divergir — e divergir é o comportamento correto de um revisor adversarial diante de texto ambíguo.

Tornar o contrato da tarefa um artefato obrigatório e versionado, não um turno de conversa. Se cada tarefa tem um arquivo com task_id, risk, runbook_binding e critérios com ID estável, o Reviewer para de inferir escopo.

Criar uma classe de finding que o Reviewer não pode emitir contra o Executor. Ausência de artefato de contrato é falha de entrada da tarefa, não defeito de execução. O verdict correto já existe e é HUMAN_DECISION_REQUIRED — AGENTS.md:86-88. O que falta é a regra explícita mandando usá-lo nesse caso.

O que garante o comportamento correto do Reviewer?
Hoje: nada mecânico. AGENTS.md é um prompt, e .codex/config.toml só garante read-only e sem rede — restringe o que ele pode fazer, não o que ele pode concluir. E confirmei que o plugin não lê AGENTS.md (grep -rn "AGENTS" no plugin → zero), então quando você usa /codex:review, essas garantias não estão nem carregadas.

P2 — O plugin Codex
Inspecionei a versão instalada: codex@openai-codex v1.0.6, enabledPlugins: true em ~/.claude/settings.json.

Ajuda ou atrapalha?
Do jeito que está configurado hoje, atrapalha — e de forma silenciosa, que é o modo pior.

Aspecto	Codex CLI direto (fluxo atual)	Plugin /codex:review	Plugin /codex:adversarial-review
Carrega AGENTS.md	Sim (Codex CLI lê nativamente)	Não	Não
Prompt usado	AGENTS.md do projeto	Reviewer nativo do Codex	prompts/adversarial-review.md do plugin
Vocabulário de verdict	PASS/FAIL/HUMAN_DECISION_REQUIRED	approve/needs-attention	approve/needs-attention
Severidades	CRITICAL/HIGH/MEDIUM/LOW	critical/high/medium/low	idem
Runbooks	Sim	Não	Não
Sandbox	.codex/config.toml	read-only (hardcoded)	read-only (hardcoded)
O plugin substitui seu Reviewer em vez de operá-lo. O schema em schemas/review-output.schema.json força verdict: enum["approve","needs-attention"] — não existe HUMAN_DECISION_REQUIRED. A saída do plugin não consegue representar o estado mais importante da sua arquitetura: o caso em que só Davi pode decidir. Ele vira needs-attention, indistinguível de um defeito técnico do Executor.

Ponto positivo real: as reviews são hardcoded sandbox: "read-only", alinhado com AGENTS.md:9.

Risco não óbvio: codex:rescue
O subagente codex-rescue instrui: "Default to a write-capable Codex run by adding --write". Se acionado, o Codex vira Executor — viola AGENT_POLICY.md ("Produção, revisão e aprovação são funções distintas"), e o .codex/config.toml read-only não se aplica porque o plugin passa sandbox explicitamente. Essa é a maior exposição de governança do plugin hoje.

O que o plugin revisa: últimas alterações ou o plano?
Só diff. commands/review.md suporta --scope auto|working-tree|branch e --base <ref>. Não existe modo "revisar o plano". Portanto o plugin não resolve P3 e não pode resolver — a porta de plano é anterior a qualquer diff.

Nota importante: em modo working-tree, o escopo é o estado acumulado da árvore. Se você tem duas TASKs não commitadas, ele revisa as duas juntas — perde a atomicidade de task_atomics.md. Use --base com a branch, ou commite por TASK.

As skills do Reviewer continuam sendo usadas?
Não existem skills de Reviewer. .claude/ está vazio no repositório — zero skills, zero agents, zero settings versionados. As três skills do plugin (codex-cli-runtime, codex-result-handling, gpt-5-4-prompting) são infraestrutura interna do plugin, não do CEPRAEA.

O plugin mantém as soluções de P1?
Não. Ele remove o carregamento de AGENTS.md e dos runbooks. Qualquer correção que você fizer em AGENTS.md fica inerte sob /codex:review.

Como usar o plugin corretamente
O plugin resolve um problema real de P2 (o copy-paste) e não deve ser descartado — mas precisa de escopo definido:

/codex:review — não usar como porta de governança. Serve como pré-check barato antes de acionar o Reviewer formal. Saída dele nunca é verdict.
/codex:adversarial-review "<instruções>" — aceita texto livre de foco. É o único canal viável para injetar AGENTS.md + runbooks aplicáveis. Ainda assim o verdict volta no vocabulário errado.
Review formal (Codex CLI direto) — continua sendo a porta que emite PASS/FAIL/HUMAN_DECISION_REQUIRED.
Desabilitar codex:rescue, ou registrar decisão explícita de que Codex nunca roda com --write.
Retorno honesto: o plugin elimina o copy-paste do Reviewer para o Executor, mas custa o carregamento da governança. É um trade-off ruim enquanto a governança viver só em prompt. Depois que P1/P5 forem resolvidos com verificação determinística, o custo cai muito — porque o essencial passa a estar em arquivo verificável, não em prompt.

P3 — Planejamento silencioso
Este problema já está resolvido no papel e a solução está inalcançável.

task_atomics.md:50-66 define o ciclo de duas portas:

Plano. O Executor preenche um task_proposal [...] O Reviewer avalia o plano — antes de qualquer linha de código ser escrita [...] PASS autoriza o início da implementação.
Implementação. Só após PASS do plano o Executor implementa.
E o documento nota explicitamente que nenhum estado novo foi criado — o vocabulário fechado se aplica às duas portas.

Agora o problema:


grep -rn "task_atomics\|task_proposal" CLAUDE.md AGENTS.md AGENT_POLICY.md runbooks/
→ zero ocorrências
Nem CLAUDE.md nem AGENTS.md mencionam a existência da porta de plano. Eu, como Executor, só descobri esse documento porque você o citou na sua pergunta. O Codex, como Reviewer, também não o carrega. O ciclo de duas portas está escrito, tem schema (task-proposal.schema.json), tem exemplo (task-proposal.example.json), tem validador funcionando — e nenhum dos dois agentes sabe que ele existe.

Então a resposta a "só perceberemos no final?" é: sim, hoje sim — não por falta de projeto, mas porque o projeto não está ligado aos arquivos de papel. Essa é a correção de menor esforço e maior retorno de toda a lista.

P4 — Sobrecarga humana
Correção factual sobre o Git
A queixa sobre o histórico está desatualizada. Verifiquei:

Período	Padrão de mensagem
até 2026-08-15	Todos-online, Alinhamento-Final, Ajustes Finais nos arquivos, Arquivos commitador por Davi Sermenho
a partir de 2026-08-16	TASK-GOV-001: enforce Git inspection allowlist, AC-002: process BancoCEPRAEA source, DEC-GOV-002: bind canonical modeling runbooks, ASSURANCE-001: organize FVR assurance backlog
Os últimos ~20 commits são TASK-ID: ação — semânticos e rastreáveis a uma TASK. O problema do Git foi resolvido há dois dias e a queixa descreve o estado anterior. Vale confirmar isso antes de investir em correção de commits, porque a carga cognitiva real hoje vem de outro lugar.

De onde vem a carga real
Não é do Git. É de você ser o barramento de mensagens entre dois processos. Copiar handoff, copiar findings, lembrar qual TASK pertence a qual branch, reconstruir contexto — tudo isso é sintoma de que o estado da tarefa não tem representação em arquivo. Ele vive na sua memória e no scrollback de dois terminais.

Note a tensão real com AGENT_POLICY.md:131 — "Não crie state machine, log de interação ou relatório obrigatório paralelo ao Git". Essa regra está certa quanto ao log, mas hoje ela é lida de forma ampla demais e acaba impedindo o contrato da tarefa, que não é um log paralelo: é uma entrada versionada em Git, com o Git continuando como state machine. Vale explicitar essa distinção no texto, senão a própria policy bloqueia a correção.

O que reduz carga sem tocar em Git operacional
Git operacional continua sendo seu por AGENT_POLICY.md:50-60, e o guard em .devcontainer/guards/pretool aplica isso fail-closed (testei: git branch --show-current foi bloqueado). Não proponho mudar isso. O que reduz carga sem violar a fronteira:

Um arquivo de contrato por TASK (.ai/tasks/<TASK-ID>.json). Substitui "lembrar o que pertence a cada TASK".
Convenção TASK-ID na branch e no commit — já em uso desde 16/08. Formalizar como regra fecha a rastreabilidade.
O Executor propõe a mensagem de commit no handoff (texto, não execução). Você cola. Elimina redação, preserva autoridade.
Diffs grandes são sintoma de tarefa não-atômica, e task_atomics.md:175-185 já define a regra de divisão. Aplicar a porta de plano corta esse problema na origem.
P5 — Executor vs Revisor
Onde exatamente o desperdício nasce
Encontrei um dado que explica o padrão. Medi densidade de termos que exigem julgamento sem limiar definido (material, proporcional, relevante, suficiente, adequado, conforme o impacto, quando necessário…), por 100 linhas:

Arquivo	Linhas	Ocorrências	Densidade
RB-REV-004	103	17	16,5
RB-SHARED-002	88	11	12,5
RB-REV-001	105	10	9,5
RB-REV-003	104	9	8,7
runbooks/README.md	201	17	8,5
AGENTS.md	90	7	7,8
RB-SHARED-003	106	6	5,7
AGENT_POLICY.md	149	8	5,4
task_atomics.md	285	15	5,3
CLAUDE.md	85	4	4,7
RB-EXEC-003	101	3	3,0
RB-EXEC-001	104	3	2,9
Dois padrões saltam:

Os runbooks do Reviewer são 3 a 5× mais subjetivos que os do Executor. O papel que emite o verdict opera com a instrução mais vaga. Isso é o inverso do que a arquitetura precisa.
RB-REV-004 é o documento mais subjetivo do repositório — e DEC-GOV-002:76-84 o tornou permanente para toda tarefa AC-001–AC-029. Você acoplou permanentemente o documento de menor determinismo à fase de trabalho em curso. Não é coincidência que os FAILs se concentrem em suficiência de evidência.
Sobre "o Executor não abre o runbook"
Isso é literal e eu confirmo: no turno do manifesto eu não abri RB-EXEC-003. Mas a causa é estrutural, não de diligência: CLAUDE.md:9 condiciona o carregamento à existência de runbook_binding, e sem task_proposal não há binding. Risco verde cria um caminho onde nenhum runbook é carregado por construção.

E RB-EXEC-003:47 contém uma instrução que eu deveria ter seguido e não segui: "Ler docs/standards/guia_estilo_documentação.md antes de escrever qualquer conteúdo". Essa é uma pré-condição real, perdida pelo caminho verde.

Como resolver o desperdício
A correção não é "instruir melhor". É retirar a classe de finding do domínio do julgamento:

Um script decide o binding, não dois LLMs lendo Markdown. Entrada: contrato da tarefa. Saída: 0 ou 1 + divergência apontada. Nenhum dos dois argumenta.
Toda tarefa tem contrato, inclusive risco verde — em forma reduzida. Verde não deve significar sem contrato, deve significar contrato mínimo. Isso fecha simultaneamente o buraco do Executor (nenhum runbook carregado) e o do Reviewer (nenhum binding para conferir).
AGENTS.md ganha uma regra de atribuição de falha: ausência de artefato de contrato → HUMAN_DECISION_REQUIRED, nunca finding contra o Executor. Já é o verdict correto por AGENTS.md:86-88; falta dizer que este caso o exige.
Corrigir a assimetria CLAUDE.md:9 × AGENTS.md:13 — as duas frases precisam ter a mesma condicionalidade.
Reduzir RB-REV-004 a critérios binários. "Evidência suficiente" precisa virar uma lista fechada de propriedades verificáveis, senão continua produzindo FAIL negociável.
P6 — Skills
Quando uma Skill do Reviewer deve nascer
Sua intuição está correta e vou torná-la um critério: uma Skill de Reviewer só se justifica quando traz competência técnica que o runbook não pode conter — conhecimento de domínio externo (semântica de RLS no Postgres, classes de BOLA/IDOR, armadilhas de lock em migration). Runbook responde "qual procedimento seguir"; Skill responde "o que eu preciso saber para executar esse procedimento com competência".

Corolário: "o runbook não é usado" nunca é motivo para criar Skill. É defeito de binding, e criar Skill nesse caso duplica normativa — introduz exatamente a divergência entre fontes que causou o FAIL de DEC-GOV-002. review-task-proposal, review-documentation-claims e review-test-adequacy da sua lista caem nessa categoria: RB-REV-003, RB-REV-004 e RB-REV-001 já cobrem. Não criar.

As que passam no critério: review-rls-security e review-database-change — trazem conhecimento que RB-REV-002 legitimamente não contém.

O Executor precisa de Skills de produção?
Sim, mas nenhuma delas é a prioridade agora, com uma exceção.

Ponto de ordem: .claude/** é control plane por AGENT_POLICY.md e está bloqueado no guard (*/.claude/* → block). Criar Skill exige tarefa humana explícita com esse alvo.

Priorização honesta:

Skill	Veredito
prepare-task-proposal	P0. É o que liga task_atomics.md ao fluxo real e destrava P3 e P5. Única com retorno imediato.
run-quality-gates	Prematuro. Não há gates para orquestrar — não existe package.json. Primeiro criar os gates.
supabase / supabase-postgres-best-practices (oficiais)	Instalar quando a fase de banco começar. Conhecimento externo real, sem risco de duplicar normativa. Não antes.
supabase-migration, database-testing	Depois do modelo canônico fechar. Hoje seriam especulação sobre um schema que não existe.
model-domain-types, react-feature	Prematuro — não há código de aplicação no repositório.
cepraea-documentation	Não criar. Duplicaria RB-EXEC-003 + o guia de estilo. Risco de divergência maior que o ganho.
P7 — Tarefas que não acabam
As tarefas estão atômicas?
O padrão existe e é bom (task_atomics.md:175-185), mas não se aplica à fase em curso por decisão explícita: task_atomics.md:20-24 diz que a modelagem canônica "usa seu próprio mecanismo de decisão e evidência, já formalizado em DEC-GOV-002, e não é afetada por este documento".

Consequência direta: as tarefas AC-NNN não passam pelo ciclo de duas portas, não têm task_proposal, não têm critérios com ID estável e não têm oráculo de aceitação formal. É exatamente a fase onde os FAILs estão concentrados.

Estão sendo registradas?
Parcialmente. Rastreabilidade existe via commit (AC-001:, AC-002:) e via PR. Não existe registro do contrato — só do resultado.

Cada tarefa deveria ter schema?
Sim, e o schema já existe e funciona: task-proposal.schema.json + validador que roda com exit 0. Não está sendo usado no fluxo real. Sua intuição aqui está certa e o custo de aplicá-la é baixo — o ativo já está construído e testado.

Impacto de migrar as tarefas AC-NNN para a nova arquitetura
Ganho, com uma ressalva de sequenciamento.

Argumento a favor: DEC-GOV-002:80-84 registra que AC-001 sofreu "várias rodadas de revisão adversarial" com achados de suficiência e precisão de evidência — abas não lidas, localização incorreta de fragmento, classificação incorreta de dado sensível. Todos esses são verificáveis mecanicamente. "A aba X foi lida" é file.sha256 + cobertura declarada, não julgamento. São exatamente as propriedades que o verification-plan de 02-ESTADO-ARQUITETURA-FINAL.md foi projetado para calcular. Com 27 tarefas AC restantes, o custo de não migrar se paga muitas vezes.

Ressalva: AC-001 e AC-002 já foram concluídas e mergeadas. Não reclassificar retroativamente — DEC-GOV-002 já estabeleceu esse princípio para AC-000 e ele deve valer aqui. Migrar de AC-003 em diante.

Prejuízo real, para você decidir com o número na mão: preencher task_proposal por tarefa AC adiciona sobrecarga por tarefa. Vale medir em uma antes de comprometer as 27.

A ordem que você propôs está correta
Concordo com o sequenciamento: P1–P6 antes de continuar AC-003. Mas com uma ressalva forte — P1, P3 e P5 são um único defeito e devem ser uma única correção, não três. Tratados separadamente, cada um produz documentação nova e nenhum produz mecanismo.

Drift de documentação — achados concretos
#	Arquivo	Drift	Sev.
D-01	CLAUDE.md, AGENTS.md	Zero referências a .ai/decisions/**. DEC-GOV-002 é normativa e aprovada, mas invisível para ambos os agentes. Causa raiz direta do FAIL de P1.	CRÍTICO
D-02	CLAUDE.md, AGENTS.md	Zero referências a task_atomics.md. O ciclo de duas portas existe e é inalcançável. Causa raiz de P3.	CRÍTICO
D-03	RB-EXEC-001:67-68, RB-EXEC-003:66, RB-REV-003:69	Prescrevem npm run lint, npm run typecheck, markdownlint. Nenhum existe — sem package.json, sem node_modules, markdownlint ausente. Torna RB-SHARED-003:26 vacuamente satisfeita.	CRÍTICO
D-04	CLAUDE.md:9 × AGENTS.md:13	Assimetria condicional/imperativa sobre runbook_binding. Mecanismo textual exato do FAIL.	ALTO
D-05	.markdownlint.jsonc regra relative-link-path ("Não use caminhos relativos", search: "](..") × runbooks/README.md item 13 ("caminhos relativos para as fontes aplicáveis")	Contradição normativa direta. O validador determinístico reprovaria 46 links dos próprios runbooks. Latente só porque markdownlint não está instalado — vira falha em massa no dia da instalação.	ALTO
D-06	RB-REV-001:102-103, RB-EXEC-002:100, RB-EXEC-003:97, RB-EXEC-004:97	5 links absolutos ](/AGENT_POLICY.md) — quebrados como caminho de arquivo. Os outros 8 runbooks usam ../../. Inconsistência intra-biblioteca.	MÉDIO
D-07	manifest.json	Asset docs/arquiteturas/assurance/ não existe (caminho real: docs/backlog/verificacao-formal-fvr/planejamento/). 1 de 42 assets quebrado, em documento commitado em 2026-08-18. Reproduzível: node -e "...".	MÉDIO
D-08	AGENT_POLICY.md lista de control plane	-- runbooks/** com hífen duplo — quebra o item da lista. Também colide com a regra m-dash do próprio markdownlint.	BAIXO
D-09	RB-EXEC-001:39-44	Lista "não modificar" omite runbooks/**, .github/workflows/**, scripts/ci/**, presentes em AGENT_POLICY.md. Duplicação divergente de normativa.	BAIXO
D-10	.markdownlint.jsonc	Regras herdadas do MDN Content sem relação com o projeto: fqdn-moz-links, relative-link (en-US/docs), short-link (bugzilla), link-fragments desativada por causa do gerador "yari". O próprio arquivo admite: "vale confirmar com Davi". Config estrangeira adotada sem triagem.	BAIXO
Correção arquitetural proposta
Não documentar melhor. Três mudanças estruturais, em ordem de dependência.

1. Fechar o loop normativo — o control plane precisa ser alcançável
Hoje existem fontes normativas aprovadas que nenhum agente carrega. Enquanto isso for verdade, qualquer regra nova que você escrever tem chance de nascer órfã igual a DEC-GOV-002.

CLAUDE.md e AGENTS.md passam a apontar para .ai/decisions/ e para task_atomics.md.
Um índice .ai/decisions/README.md com escopo de aplicabilidade por decisão — DEC-GOV-002 teria dito "aplica-se a AC-001–AC-029", e o Codex não teria generalizado.
Corrigir D-04 (assimetria) e D-05 (contradição markdownlint).
Custo baixo, risco verde/amarelo, e destrava tudo o mais.

2. Instituir a porta de plano — P3, e metade de P1 e P5
O mecanismo já existe inteiro: schema, exemplo, validador funcionando. Falta ligá-lo.

Toda tarefa produz .ai/tasks/<TASK-ID>.json antes da implementação, validado por validate-task-proposal.mjs.
Risco verde usa perfil reduzido — mas sempre com runbook_binding. Elimina o caminho onde nenhum runbook é carregado.
Reviewer avalia o plano na porta 1. Vocabulário inalterado.
AGENTS.md ganha: ausência de contrato → HUMAN_DECISION_REQUIRED, nunca finding contra o Executor.
Isso sozinho elimina a classe de FAIL que motivou P1.

3. Introduzir o Verifier — a correção de fundo
Esta é a que muda a arquitetura, e é a que você já projetou em 02-ESTADO-ARQUITETURA-FINAL.md.

Humano → Contrato → Executor → Verifier (determinístico) → Reviewer (semântica residual) → Humano → Git
Regra de precedência já escrita por você: FormalResult != PASS ⟹ Reviewer não pode emitir PASS. E PASS formal não obriga PASS do Reviewer.

O que isso resolve, concretamente: o Reviewer deixa de gastar turnos recalculando "o binding bate?", "o diff saiu do escopo?", "os arquivos alterados são os declarados?" — tudo isso vira saída de script. Ele passa a gastar o turno inteiro no que só ele faz: semântica, regressão, overclaim.

Sequenciamento realista: o certificado FVR está NOT_ISSUED / HARNESS_INVALID (01-ESTADO-ATUAL:1.5), então não adote o runner FVR completo agora. Comece com um verificador mínimo sobre três propriedades que já causaram FAIL real: write-set respeitado, binding consistente com a matriz, contrato presente e válido. Três assertions cobrem a maioria dos findings mecânicos que você viu.

Sobre o plugin, nesta ordem
O plugin fica em uso auxiliar (pré-check barato, background) e fora da porta de governança até que (1) exista Verifier e (2) /codex:adversarial-review seja invocado com as instruções do AGENTS.md injetadas explicitamente. Decisão pendente e recomendada: desabilitar codex:rescue ou registrar que Codex nunca roda com --write.

Uma nota sobre esta resposta: ela é análise, não execução — nenhum arquivo foi alterado e não há diff para revisar, então não emito READY_FOR_REVIEW. O fato de eu precisar explicar isso é, ele mesmo, uma instância de P1: CLAUDE.md:68-79 define o handoff como se todo turno produzisse artefato revisável, e não há estado previsto para um turno consultivo. Vale incluir na correção do item 1.
