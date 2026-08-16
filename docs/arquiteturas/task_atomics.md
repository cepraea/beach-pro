# PADRÃO DE TAREFAS ATÔMICAS E CRITÉRIOS DE ACEITAÇÃO — CEPRAEA BEACH PRO
AESDS 05 — Fundação v0.1

## 1. OBJETIVO
Definir a menor unidade de trabalho suficientemente explícita para que um agente implemente sem inventar requisito, alterar escopo ou depender de conversa extensa fora da tarefa.

## 2. PRINCÍPIO
Uma tarefa atômica deve possuir uma saída verificável e pequena o suficiente para permitir revisão integral do diff e dos critérios. “Implementar módulo X” normalmente é grande demais.

## 3. TEMPLATE CANÔNICO DE TASK

- ID
- Título
Objetivo
Ator
Contexto válido
Pré-condições
Dependências
Fonte normativa
Entrada/contratos
Comportamento esperado
Estados relevantes
Ações permitidas
Ações proibidas
Edge cases incluídos
Fora de escopo
Arquivos esperados ou área de escrita
Decisões humanas já tomadas
Decisões humanas pendentes
Autonomia técnica permitida
Stop conditions
Critérios de aceitação
Checks obrigatórios
Evidência esperada
Definição de DONE
```

4. REGRA DE TAMANHO
A tarefa deve ser dividida quando:
- possui mais de um resultado independente;
- mistura decisão de produto com execução;
- exige vários fluxos de usuário distintos;
- não cabe em um diff revisável integralmente;
- depende de duas decisões humanas não relacionadas;
- possui critérios que podem passar/falhar independentemente e não compartilham a mesma unidade funcional.

Não dividir artificialmente um fluxo simples em microtarefas que criem handoff sem valor.

5. CRITÉRIOS COMPORTAMENTAIS — BDD
Use Given/When/Then quando o critério descreve comportamento observável.

Exemplo:
Given uma solicitação de disponibilidade aberta
And a atleta ainda não respondeu
When ela abre o treino
Then a interface exibe “Não respondida”
And não representa o estado como resposta “Não”.

6. RESTRIÇÕES — MUST / MUST NOT
Use requisitos declarativos quando não houver benefício em cenário BDD.

MUST: preservar dados preenchidos após erro recuperável.
MUST NOT: exibir UUID interno à atleta sem requisito explícito.
MUST NOT: preencher presença automaticamente a partir de disponibilidade.

7. QUALIDADE MENSURÁVEL
Critérios de performance, acessibilidade ou cobertura precisam de métrica/condição objetiva quando aplicável. Evitar “rápido”, “bonito”, “intuitivo”, “moderno” sem definição verificável.

8. CLASSIFICAÇÃO DE CRITÉRIO
CRITICAL: falha viola segurança, autorização, integridade de domínio ou requisito essencial.
MUST: obrigatório para DONE.
SHOULD: esperado, mas pode admitir exceção documentada e aprovada.
OPTIONAL: melhoria não bloqueante e explicitamente fora do caminho crítico.

9. ORÁCULO DE ACEITAÇÃO
Cada critério deve indicar, direta ou indiretamente, como será provado: teste automatizado, typecheck, build, inspeção de contrato, runtime, acessibilidade, dispositivo real ou validação humana.

Critério sem mecanismo de prova deve ser refinado antes de implementação quando a ambiguidade puder alterar o resultado.

10. EXEMPLO DE TASK ATÔMICA
ID: FE-AVAIL-003
Objetivo: implementar seleção da resposta da própria atleta.
Ator: atleta.
Entrada: status UNANSWERED | YES | NO | UNCERTAIN e prazo vigente.
Comportamento: apresentar opções permitidas, refletir resposta atual, permitir alteração dentro do prazo e persistir somente por ação explícita.
MUST NOT: tratar UNANSWERED como NO; editar resposta de outra atleta; transformar resposta em presença.
Estados de interação: IDLE, DIRTY, SUBMITTING, SUCCESS, ERROR, EXPIRED.
Checks: testes comportamentais relevantes + validação da aplicação.
DONE: todos os MUST PASS e nenhum finding alto aberto.

11. STOP CONDITIONS DO EXECUTOR
Parar somente a parte afetada se descobrir: decisão material ausente; contrato incompatível; fonte canônica conflitante; dependência nova material; necessidade de ampliar escopo; comportamento não especificado que altera o produto.

12. REGRA PARA REFERÊNCIAS
Se a task exige escolha visual ou técnica ainda não homologada, não embutir a escolha como implementação. Criar um ponto de decisão com as opções obtidas segundo o AESDS 08.

13. META DE PRIMEIRA REVISÃO
As tasks devem ser especificadas em granularidade suficiente para buscar >=90% de critérios PASS na primeira revisão independente. Se uma classe de task falhar repetidamente, corrigir o template/contexto antes de aumentar governança.
