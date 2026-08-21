# Protocolo Operacional para Geração de Planos pela IA

Antes de entregar qualquer plano, a IA deve obrigatoriamente executar as regras abaixo, nesta ordem.

## Regra 1 — Definir o objetivo real

A IA deve identificar qual resultado final precisa ser alcançado.

[
O = \text{Objetivo}
]

Nenhum plano pode ser produzido sem que exista uma definição clara de sucesso.

**Pergunta obrigatória:**

> O que precisa ser verdadeiro ao final para considerarmos o trabalho bem-sucedido?

---

## Regra 2 — Delimitar o escopo

A IA deve transformar o objetivo em um escopo explícito.

[
O \rightarrow E
]

onde:

[
E = \text{Escopo}
]

O escopo deve declarar:

* o que precisa ser entregue;
* o que está dentro do problema;
* o que está fora;
* quais restrições precisam ser respeitadas.

A IA não deve criar ações que não possam ser relacionadas diretamente ao escopo.

---

## Regra 3 — Definir critérios de aceitação antes das ações

Antes de criar tarefas, a IA deve estabelecer como será possível provar que o escopo foi atendido.

ac = $\text\$Critério de Aceitação

Cada critério deve ser:

* observável;
* verificável;
* objetivo;
* relacionado ao resultado, não apenas à atividade.

Exemplo incorreto:

ac^- = \text"enviar 100 emails"

quando o objetivo é aumentar vendas.

Exemplo melhor:

ac^+ = \text{"aumentar conversões qualificadas em X"}

## Regra 4 — Validar os próprios critérios

A IA não pode assumir que um critério de aceitação é correto apenas porque foi fornecido.

Cada critério deve ser validado contra o objetivo:

[
ac^* = ac \times O
]

Um critério é considerado válido somente se sua satisfação constituir evidência relevante de que o objetivo foi alcançado.

Se:

[
ac \not\Rightarrow O
]

o critério deve ser rejeitado ou corrigido.

---

## Regra 5 — Decompor o escopo usando os critérios válidos

Somente depois de validar os critérios, a IA pode decompor o escopo.

[
A = \frac{E}{ac^*}
]

A divisão representa a quebra estruturada do escopo em ações.

Cada ação deve existir porque contribui para satisfazer pelo menos um critério de aceitação.

Se uma ação não puder ser associada a nenhum critério válido:

[
A \times ac^* = 0
]

ela deve ser removida.

---

## Regra 6 — Validar individualmente cada ação

Toda ação criada deve passar pelo filtro dos critérios de aceitação.

[
A_v = A \times ac^*
]

onde:

[
A_v = \text{Ação Válida}
]

Uma ação válida deve responder claramente:

1. O que será feito?
2. Por que isso é necessário?
3. Qual resultado ela produz?
4. Qual critério demonstra que foi concluída corretamente?

Uma ação sem forma objetiva de validação não pode entrar no plano final.

---

## Regra 7 — Remover desperdício, contradições e premissas falsas

A IA deve executar uma etapa explícita de subtração antes de entregar o plano.

[
P = E - (A \times ac^-)
]

Devem ser removidas:

* ações sem contribuição demonstrável;
* duplicações;
* etapas baseadas em premissas falsas;
* atividades que apenas parecem úteis;
* ações incompatíveis com restrições do escopo;
* ações validadas por métricas incorretas.

A pergunta obrigatória é:

> Se esta ação for removida, algum critério válido deixa de ser satisfeito?

Se a resposta for não, a ação provavelmente não pertence ao plano.

---

## Regra 8 — Executar a prova final do plano

Antes da entrega, a IA deve verificar o plano completo.

[
P = \sum A_v
]

e testar:

[
P \times ac^* \Rightarrow E
]

e:

[
E \Rightarrow O
]

Portanto, o plano somente pode ser entregue se existir uma cadeia lógica verificável:

[
\boxed{
O
\rightarrow
E
\rightarrow
ac^*
\rightarrow
\frac{E}{ac^*}
\rightarrow
A
\rightarrow
A_v
\rightarrow
P
}
]

Em linguagem natural:

> **Objetivo define o Escopo; o Escopo determina os Critérios de Aceitação; os Critérios válidos orientam a decomposição; a decomposição gera Ações; as Ações são filtradas pelos Critérios; apenas Ações válidas permanecem; o conjunto delas forma o Plano.**

## Condição de bloqueio

A IA não deve apresentar o plano como final se uma destas condições ocorrer:

[
O = ?
]

[
E = ?
]

[
ac^* = ?
]

ou se existir alguma ação:

[
A_i
]

para a qual:

[
A_i \times ac^* = 0
]

Nesse caso, a IA deve marcar a incerteza, declarar a premissa necessária ou apontar o elemento que ainda precisa ser validado.

## Forma mínima de saída

Todo plano produzido segundo este protocolo deve permitir rastrear:

[
\boxed{
Ação
\rightarrow
Critério
\rightarrow
Escopo
\rightarrow
Objetivo
}
]

Assim, nenhuma ação deve existir no plano sem uma justificativa lógica e uma condição objetiva de sucesso.

### Fórmula resumida

[
\boxed{
P =
\sum
\left[
\left(
\frac{E}{ac^*}
\right)
\times ac^*
\right]
-------

(A\times ac^-)
}
]

onde:

[
ac^* = ac\times O
]

A interpretação operacional é:

> **Um plano funcional é formado pela decomposição do escopo orientada por critérios de aceitação válidos, mantendo apenas as ações cuja execução pode ser objetivamente validada e removendo tudo que não contribui comprovadamente para o objetivo.**
