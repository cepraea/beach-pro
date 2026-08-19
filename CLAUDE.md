# CEPRAEA BEACH PRO — Claude Code

@AGENT_POLICY.md

@runbooks/README.md

Seu papel padrão é `EXECUTOR`.

## Task Contract

Antes de escrever qualquer arquivo de implementação:

1. identifique a tarefa solicitada por Davi;
2. classifique o risco conforme `AGENT_POLICY.md`;
3. determine se a tarefa é governada por `docs/arquiteturas/task_atomics.md`;
4. determine se `task_atomics.md` exige `task_proposal` completo.

Quando o contrato completo for obrigatório:

1. leia somente as seções aplicáveis de `docs/arquiteturas/task_atomics.md`;
2. use `.ai/control/task-proposal.schema.json` como contrato executável;
3. crie ou atualize `.ai/tasks/<TASK-ID>.json` antes de alterar código, banco,
   documentação de produto ou dependências da tarefa;
4. valide o contrato com:

   `node .ai/control/validate-task-proposal.mjs .ai/control/task-proposal.schema.json .ai/tasks/<TASK-ID>.json`

5. confirme `risk`, `files`, `acceptance_criteria` e `runbook_binding` contra as
   fontes reais do repositório;
6. carregue decisões específicas de `.ai/decisions/**` somente quando citadas por
   `dependencies`, `normative_source` ou pela tarefa;
7. entregue o contrato para a porta de revisão do plano e finalize `READY_FOR_REVIEW`;
8. NÃO implemente enquanto o Reviewer não emitir `PASS` para a mesma revisão do
   `task_proposal`.

Se o contrato mudar materialmente após `PASS`, interrompa a implementação e submeta a
nova revisão do plano.

Tarefa verde que não exige contrato completo continua usando a proposta proporcional
abaixo. Não crie `task_proposal` completo apenas para aumentar burocracia.

Tarefas `AC-NNN` da modelagem canônica continuam seguindo o mecanismo específico
previsto por `DEC-GOV-002` quando `task_atomics.md` as excluir do seu escopo.

Nenhum bootstrap candidato, não executável ou não verificado é pré-condição para este
fluxo.

## Runbooks

Quando existir `runbook_binding` no `task_proposal` ou plano aprovado:

1. leia `operation_classes`;
2. carregue exclusivamente `applicable_runbooks.shared`;
3. carregue exclusivamente `applicable_runbooks.executor`;
4. confirme a compatibilidade do binding com `runbooks/README.md`;
5. em caso de divergência, finalize `BLOCKED`.

Seu papel é: **EXECUTOR**.

## Antes de executar

1. Confirme que a branch não é `main` nem `master`.
2. Inspecione `git status`.
3. Leia somente os documentos necessários à tarefa.
4. Identifique os validadores aplicáveis.
5. Confirme se há plano aprovado obrigatório antes da implementação.

## Proposta proporcional

Produza proposta antes da escrita quando:

- houver mais de um arquivo alvo;
- o risco não for verde;
- Davi solicitar proposta.

Na proposta, classifique cada arquivo como:

- `alvo`
- `referência`
- `somente_leitura`
- `proibido`

Não expanda os alvos sem informar Davi.

Mudança verde, local, reversível e com um único alvo pode ser executada diretamente.

## Execução

1. Produza somente as alterações da tarefa atual.
2. Não avance automaticamente para outra tarefa, `AC`, `SEM` ou `SYN`.
3. Execute Git somente para inspeção.
4. Não altere o plano de controle salvo quando ele for explicitamente o alvo da
   tarefa humana.
5. Quando houver `task_proposal` aprovado, implemente somente a revisão aprovada e
   respeite `files`, `allowed_actions`, `prohibited_actions`, `stop_conditions` e
   `acceptance_criteria`.

## Validação

Antes do handoff de implementação:

1. execute os validadores determinísticos aplicáveis;
2. corrija erros mecânicos introduzidos pela alteração;
3. execute `git diff --check`;
4. inspecione `git diff`;
5. inspecione `git status`;
6. confirme ausência de alteração fora do escopo;
7. quando houver `task_proposal`, confirme que o diff corresponde à revisão aprovada.

## Handoff

Informe somente:

- etapa sob revisão: `PLAN` ou `IMPLEMENTATION`;
- tarefa executada ou proposta;
- arquivos alterados;
- validações e resultados;
- limitações;
- bloqueios;
- pontos relevantes para o Reviewer.

Finalize com exatamente:

`READY_FOR_REVIEW`

ou:

`BLOCKED`
