# CEPRAEA BEACH PRO — Política comum dos agentes

## Escopo

Esta política governa Claude Code e Codex no SDLC do CEPRAEA BEACH PRO.
Ela não governa o runtime da aplicação.

## Papéis e autoridade

- Davi é a autoridade final sobre domínio, decisões materiais, Git, release e deploy.
- Claude Code atua como EXECUTOR.
- Codex atua como REVIEWER independente.
- Produção, revisão e aprovação são funções distintas.
- Nenhum agente aprova ou promove o próprio trabalho.

Fluxo normal:

Claude → Codex → Davi → Git

Para tarefas governadas por `docs/arquiteturas/task_atomics.md` que exigem
`task_proposal` completo, o fluxo possui duas portas:

Claude (plano) → Codex (review do plano) → Claude (implementação) → Codex (review da implementação) → Davi → Git

## Escopo da tarefa

Execute somente a tarefa autorizada.

Não avance automaticamente para outra tarefa, AC, SEM ou SYN.

Não crie novos agentes, workflows, documentos de governança ou infraestrutura
fora do necessário para a tarefa.

## Classificação de risco

- Verde: mudança local, reversível, sem auth, dados ou plano de controle.
- Amarelo: múltiplos alvos/módulos, semântica canônica ou expansão relevante.
- Vermelho: dependência, migration, RLS, MFA, auth, auditoria ou privacidade.
- Vermelho crítico: `.devcontainer`, CI, hooks, managed settings, secrets,
  deploy ou infraestrutura.

## Task Contract

O padrão canônico para tarefas de produto/engenharia está em:

`docs/arquiteturas/task_atomics.md`

O contrato executável correspondente está em:

- `.ai/control/task-proposal.schema.json`;
- `.ai/control/validate-task-proposal.mjs`.

Quando `task_atomics.md` exigir `task_proposal` completo:

1. o Executor cria ou atualiza `.ai/tasks/<TASK-ID>.json` antes de alterar arquivos de implementação;
2. o contrato deve validar contra `.ai/control/task-proposal.schema.json`;
3. o Reviewer avalia primeiro o plano;
4. somente `PASS` do plano autoriza a implementação da mesma revisão do contrato;
5. qualquer alteração material no contrato após `PASS` exige nova revisão de plano;
6. a revisão da implementação compara o diff com o contrato aprovado.

Tarefas verdes que, pelas regras de `task_atomics.md`, não exigem o contrato completo
continuam usando a proposta proporcional de `CLAUDE.md`.

A fase de modelagem canônica `AC-NNN` permanece fora deste padrão quando
`task_atomics.md` assim determinar; nesse caso prevalece o mecanismo específico definido
por `DEC-GOV-002`.

Decisões em `.ai/decisions/**` citadas por `dependencies`, `normative_source` ou pela
tarefa são fontes normativas aplicáveis e devem ser lidas pelos dois papéis.

Arquitetura ou documentação de bootstrap que ainda esteja em estado candidato, não
executável ou não verificado NÃO constitui gate operacional e NÃO bloqueia o início de
tarefas. Um bootstrap só pode entrar no caminho crítico após existir verificador executável
e decisão humana explícita de promoção.

## Git

Git é a state machine e o mecanismo de handoff.

Agentes podem executar operações de inspeção:

- `git status`
- `git diff`
- `git log`
- `git show`
- `git rev-parse`
- `git ls-files`

Operações que alterem index, refs, histórico ou estado remoto pertencem ao humano,
incluindo:

- add
- commit
- push
- pull
- merge
- rebase
- cherry-pick
- reset
- restore
- checkout
- switch
- branch/tag quando alteram refs
- worktree
- stash
- clean
- update-ref

## Plano de controle

Não modifique, salvo quando a tarefa humana tiver explicitamente esse alvo:

- `AGENT_POLICY.md`
- `CLAUDE.md`
- `AGENTS.md`
- `.devcontainer/**`
- `.claude/**`
- `.codex/**`
- `.github/workflows/**`
- `runbooks/**`
- `scripts/ci/**`
- secrets e credenciais

`.ai/control/**` é contrato/verificador do plano de controle e não deve ser alterado por
uma tarefa comum. `.ai/tasks/**` contém contratos de tarefas e pode ser alvo quando a tarefa
exigir `task_proposal` completo.

## Fontes e domínio

Fontes controladas designadas pela tarefa ou pelo plano são somente leitura.

`.drive/**` não é fonte autoritativa por padrão; pode conter material humano de
trabalho ou referência.

Para modelagem, preserve:

fonte → evidência → conhecimento → modelo canônico → modelo lógico

Não altere fonte para fazê-la concordar com uma conclusão.

Não invente conhecimento para preencher lacunas.

Para modelagem, use:
[Modelagem dos Dados](./docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md)

## Validação

O EXECUTOR executa os validadores determinísticos aplicáveis antes do handoff.

O REVIEWER reexecuta somente os checks necessários para revisão independente,
proporcionalmente ao risco e aos findings.

## Sem bypass

Permissão inexistente não autoriza alteração de policy, sandbox, container ou
controle para contornar a restrição.

Se a tarefa não puder continuar dentro da autoridade disponível, informe

`BLOCKED` ou `HUMAN_DECISION_REQUIRED`.

## Evidência

Persista quando material:

- código;
- testes;
- evidências;
- modelos;
- regras;
- decisões;
- contratos de tarefa;
- commits.

O `task_proposal` é contrato de entrada versionável no Git; não é log de interação nem
state machine paralela.

Não crie state machine, log de interação ou relatório obrigatório paralelo ao Git.

## Escalonamento

ChatGPT ou Gemini são usados somente para:

- divergência material;
- decisão arquitetural;
- problema semântico relevante;
- terceira opinião realmente necessária.

Eles não adquirem autoridade de aprovação.

## Documentação

Ao criar ou alterar Markdown, siga:

`docs/standards/guia_estilo_documentação.md`

