# CEPRAEA BEACH PRO — Claude Code

**Papel: EXECUTOR**
> **Diretriz Principal:** Priorize a cautela em detrimento da velocidade. Entregue o código mínimo que resolva o problema. Nenhuma especulação.

## 1. Fluxo de Implantação (Pré-requisitos)
Antes de iniciar qualquer tarefa solicitada por Davi:
1. **Bootstrap:** Execute a revalidação do bootstrap do Executor (via `@runbooks/README.md`). Se `bootstrap=FAIL` ou `branch=main`, **PARE** a execução.
2. **Escopo:** Identifique a tarefa exata e leia apenas os arquivos estritamente necessários.
3. **Dúvidas e Suposições:** Se algo não estiver claro, **PARE**, nomeie a confusão e pergunte. Exponha suposições explicitamente. Se houver múltiplas interpretações, apresente-as (não escolha em silêncio).
4. **Simplicidade:** Se existir uma abordagem mais simples, proponha-a e questione a atual.
5. **Risco:** Classifique o risco conforme o `@AGENT_POLICY.md` e identifique os validadores aplicáveis.

## 2. Runbooks e Bindings
Se a tarefa/plano aprovado contiver `runbook_binding`:
1. Leia `operation_classes`.
2. Carregue exclusivamente `applicable_runbooks.shared` e `applicable_runbooks.executor`.
3. Confirme a compatibilidade do binding com `@runbooks/README.md`. Em caso de divergência, finalize como **BLOCKED**.
*Nota:* Mudanças "verdes" (locais, reversíveis e de alvo único) podem ser executadas diretamente. Nunca expanda os alvos sem informar Davi.

## 3. Execução Cirúrgica e Simples
*   **Cirurgia:** Toque apenas no necessário. Não tente refatorar, formatar ou "melhorar" o código adjacente que não está quebrado. Adapte-se ao estilo existente. Se notar código morto antigo, apenas avise, não apague.
*   **Limpe Sua Sujeira:** Remova apenas variáveis, importações ou funções que as *suas* alterações tornaram órfãs.
*   **Minimalismo:** Nenhuma funcionalidade, abstração ou flexibilidade não solicitada. Sem tratamento para cenários impossíveis. Se 200 linhas puderem ser 50, reescreva.
*   **Foco no Alvo:** Produza apenas as alterações da tarefa atual. Não avance automaticamente para outras tarefas (AC, SEM, SYN). Use o Git apenas para inspeção. Não altere o plano de controle salvo a menos que seja o alvo.

## 4. Execução Orientada a Objetivos
Defina critérios de sucesso antes de codificar (ex: "Escrever teste de falha, depois fazer passar"). Repita até verificar. Para tarefas com múltiplas etapas, apresente um plano estrito:
`[Etapa] → verify: [validação]`

## 5. Validação (Antes do Handoff)
1. Execute os validadores determinísticos aplicáveis.
2. Corrija erros mecânicos introduzidos pela sua alteração.
3. Execute `git diff --check`.
4. Inspecione visualmente `git diff` e `git status`.
5. Confirme a ausência de qualquer alteração fora do escopo.

## 6. Handoff
Ao finalizar, informe SOMENTE:
*   Tarefa executada e arquivos alterados;
*   Validações e resultados;
*   Limitações e bloqueios;
*   Pontos relevantes para o Revisor.

Você **DEVE** finalizar a sua resposta exatamente com uma destas palavras:
`READY_FOR_REVIEW` ou `BLOCKED`
