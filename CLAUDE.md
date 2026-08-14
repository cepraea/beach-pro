# CEPRAEA BEACH PRO — Claude Code

@AGENT_POLICY.md

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

Produza somente as alterações da tarefa atual.

Não avance automaticamente para outra tarefa, AC, SEM ou SYN.

Execute Git somente para inspeção.

Não altere o plano de controle salvo quando ele for explicitamente o alvo da
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
