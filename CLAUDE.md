# CEPRAEA BEACH PRO — Claude Code

@AGENT_POLICY.md

@runbooks/README.md

Seu papel padrão é `EXECUTOR`.

## Runbooks

Quando existir runbook_binding na tarefa/plano aprovado:

1. leia `operation_classes`;
2. carregue exclusivamente `applicable_runbooks.shared`;
3. carregue exclusivamente `applicable_runbooks.executor`;
4. confirme a compatibilidade do binding com `runbooks/README.md`;
5. em caso de divergência, finalize BLOCKED.

Seu papel é: **EXECUTOR**.

## Antes de executar

1. Identifique exatamente a tarefa solicitada por Davi.
2. Confirme que a branch não é `main` nem `master`.
3. Inspecione `git status`.
4. Leia somente os documentos necessários à tarefa.
5. Identifique os validadores aplicáveis.
6. Classifique o risco conforme `AGENT_POLICY.md`.

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

## Validação

Antes do handoff:

1. execute os validadores determinísticos aplicáveis;
2. corrija erros mecânicos introduzidos pela alteração;
3. execute `git diff --check`;
4. inspecione `git diff`;
5. inspecione `git status`;
6. confirme ausência de alteração fora do escopo.

## Handoff

Informe somente:

- tarefa executada;
- arquivos alterados;
- validações e resultados;
- limitações;
- bloqueios;
- pontos relevantes para o Reviewer.

Finalize com exatamente:

`READY_FOR_REVIEW`

ou:

`BLOCKED`
