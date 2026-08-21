# Planner v1 — Especificação Conceitual Fechada

**Status:** `CLOSED`  
**Artefato:** Especificação conceitual do fluxo de planejamento  
**Fase:** 1 — Human Request → Task Proposal  
**Data de fechamento:** 2026-08-20

---

## 1. Propósito

O Planner existe para transformar uma instrução humana potencialmente ambígua em uma proposta de tarefa formal, estruturada, rastreável e verificável antes de qualquer alteração no sistema.

O Planner **não executa implementação**.

A fronteira arquitetural principal é:

\[
HumanRequest \rightarrow Planner \rightarrow TaskProposal
\]

A execução só pode acontecer depois de validação estrutural, revisão semântica humana e preflight do Executor.

---

## 2. Princípio arquitetural central

\[
Planejar \rightarrow Validar \rightarrow Autorizar \rightarrow Executar
\]

É proibido misturar planejamento e implementação.

O Planner não deve:

- alterar código-fonte;
- tomar decisões reservadas ao humano;
- expandir escopo silenciosamente;
- preencher lacunas sem declarar a inferência;
- aprovar o próprio plano;
- iniciar execução.

---

## 3. Modelo semântico do Planner

### 3.1 Variáveis

\[
H = HumanRequest
\]

Pedido humano original.

\[
G = Goal
\]

Estado final desejado.

\[
C = Context
\]

Estado relevante conhecido do sistema, domínio e ambiente.

\[
O = Output
\]

Artefato ou resultado concreto que deve existir ao final.

\[
B = Boundaries
\]

Limites, restrições, proibições, autoridade e espaço permitido de solução.

\[
AC^+ = AcceptanceCriteriaValid
\]

Critérios de aceitação válidos que constituem prova objetiva de sucesso.

\[
A = CandidateActions
\]

Ações candidatas derivadas da decomposição do problema.

\[
A_v = ValidActions
\]

Ações necessárias, permitidas e verificáveis.

\[
P = Plan
\]

Conjunto ordenado de ações válidas, dependências e evidências esperadas.

---

## 4. Operadores semânticos

Os símbolos matemáticos são operadores semânticos, não operações numéricas.

### Agregação

\[
X + Y := Merge(X,Y)
\]

Combina informação relevante no mesmo espaço de planejamento.

### Subtração

\[
X - Y := Exclude(X,Y)
\]

Remove desperdícios, elementos proibidos, fora de escopo, contraditórios ou inválidos.

### Divisão

\[
X / Y := Decompose(X,Y)
\]

Decompõe `X` usando `Y` como princípio estruturante.

### Multiplicação

\[
X \times Y := Validate(X,Y)
\]

Mantém ou aceita `X` somente quando `Y` o valida.

---

## 5. Fórmula conceitual do planejamento

A forma compacta do Planner é:

\[
P =
\left[
\frac{G + C + O + B}{AC^+}
\right]
\times AC^+
\]

Leitura operacional:

1. compreender Goal, Context, Output e Boundaries;
2. definir critérios válidos de aceitação;
3. decompor o espaço planejável a partir desses critérios;
4. validar as ações geradas pelos mesmos critérios;
5. remover ações órfãs, proibidas, redundantes ou não verificáveis;
6. ordenar as ações segundo dependências;
7. produzir o `TaskProposal`.

Forma funcional:

\[
P =
Order(
Validate(
Decompose(
Merge(G,C,O,B),
AC^+
),
AC^+
)
)
\]

---

## 6. Normalização da entrada

Antes da derivação de `G`, `C`, `O` e `B`, o pedido humano deve ser normalizado.

\[
H \rightarrow Normalize(H) \rightarrow (G,C,O,B)
\]

A normalização deve:

- preservar a instrução original;
- reduzir variações linguísticas irrelevantes;
- separar fatos, hipóteses, restrições e pedidos;
- distinguir problema de solução sugerida;
- representar ausência de informação explicitamente;
- impedir que desconhecido seja convertido silenciosamente em fato.

Regra:

\[
UNKNOWN \neq ASSUMPTION
\]

e:

\[
UNKNOWN \neq PERMISSION
\]

---

## 7. Critérios de aceitação

Critérios de aceitação são definidos antes da decomposição final das ações.

Um critério candidato só se torna válido quando comprova relação com Goal, Output e Boundaries.

\[
AC^* = AC \times G \times O \times B
\]

Um critério válido deve ser:

- observável;
- verificável;
- objetivo;
- relacionado ao resultado;
- compatível com o escopo;
- acompanhado de método de verificação;
- acompanhado de resultado esperado.

Critério de atividade não é automaticamente critério de sucesso.

---

## 8. Decomposição em ações

As ações são derivadas do espaço planejável usando os critérios válidos:

\[
A = \frac{G+C+O+B}{AC^+}
\]

Cada ação deve representar uma transformação observável e suficientemente atômica.

Uma ação só pertence ao plano quando:

\[
A_v = A \times AC^+
\]

Regra fundamental:

\[
\forall A_i \in P,\ \exists AC_j : A_i \rightarrow AC_j
\]

Nenhuma ação pode existir sem pelo menos um critério de aceitação associado.

---

## 9. Cobertura bidirecional

O plano deve satisfazer simultaneamente:

### Nenhuma ação órfã

\[
\forall A_i \in P,\ \exists AC_j : A_i \rightarrow AC_j
\]

### Nenhum critério órfão

\[
\forall AC_j,\ \exists A_i \in P : A_i \rightarrow AC_j
\]

Portanto:

\[
NoOrphanAction \times NoOrphanCriterion = 1
\]

Também deve existir cobertura do Output:

\[
\forall O_i,\ \exists AC_j : AC_j \rightarrow O_i
\]

---

## 10. Rastreabilidade causal

Toda ação deve ser rastreável até a intenção original.

Cadeia mínima:

\[
Action \rightarrow AC \rightarrow Output \rightarrow Goal \rightarrow HumanRequest
\]

Idealmente, qualquer alteração futura de implementação deve permitir rastreabilidade reversa:

\[
FileChange
\leftarrow Action
\leftarrow AC
\leftarrow Output
\leftarrow Goal
\]

Mudanças sem ancestral no plano são consideradas expansão indevida de escopo.

---

## 11. Task Proposal como contrato de saída

O `task_proposal.json` é o artefato formal de saída do Planner.

\[
Planner(HumanRequest) \rightarrow TaskProposal
\]

Ele deve conter informação suficiente para que fases posteriores não precisem reinterpretar a intenção humana.

O Executor não deve depender da instrução original para redefinir semântica.

---

## 12. Identidade de ações e critérios

Cada critério deve possuir identidade estável, por exemplo:

```text
AC-001
AC-002
AC-003
```

Cada ação deve possuir identidade estável:

```text
A-001
A-002
A-003
```

As relações devem ser explícitas:

```text
A-001 -> AC-001
A-002 -> AC-001, AC-003
```

Isso permite validação determinística por código.

---

## 13. Estrutura mínima de uma ação

Cada ação planejada deve possuir, no mínimo:

```json
{
  "action_id": "A-001",
  "action": "...",
  "purpose": "...",
  "depends_on": [],
  "acceptance_criteria_refs": ["AC-001"],
  "target_files": ["..."],
  "expected_evidence": "..."
}
```

A ação deve responder:

1. o que será feito;
2. por que é necessário;
3. de que depende;
4. qual AC valida sua necessidade/conclusão;
5. quais arquivos ou áreas pode afetar;
6. qual evidência comprovará o resultado.

---

## 14. Dependências e ordem

O plano não é apenas uma lista.

Ele deve representar ordem e dependências entre ações.

\[
A_1 \prec A_2
\]

indica dependência sequencial.

\[
A_1 \parallel A_2
\]

indica possibilidade de execução independente.

Quando aplicável, as ações formam um DAG de execução.

O plano deve ser livre de ciclos inválidos de dependência.

---

## 15. Autoridade

A autonomia do Executor é determinada pelo contrato, não inferida livremente.

\[
ExecutorAuthority =
AllowedActions
-
ProhibitedActions
-
HumanOnlyDecisions
\]

Decisões humanas pendentes bloqueiam readiness:

\[
PendingHumanDecision > 0
\Rightarrow
READY = 0
\]

Decisões já tomadas pelo humano tornam-se constraints para agentes posteriores.

---

## 16. Boundaries

`Boundaries` define o espaço permitido de solução.

Inclui:

- `in_scope`;
- `out_of_scope`;
- constraints;
- allowed actions;
- prohibited actions;
- files e operações permitidas;
- limites de autonomia técnica;
- stop conditions;
- decisões humanas já tomadas.

Toda ação válida deve permanecer dentro desse espaço.

\[
A_i \not\subseteq B_{allowed}
\Rightarrow Reject(A_i)
\]

---

## 17. Evidência e Definition of Done

Conclusão não equivale a código escrito.

\[
Done =
Implementation
\times Validation
\times Evidence
\]

Cada AC deve ter:

\[
AC_i
\rightarrow Method_i
\rightarrow Evidence_i
\]

A Definition of Done deve ser satisfeita apenas quando todos os critérios obrigatórios forem comprovados.

---

## 18. Validação estrutural local

A validação determinística do plano será feita por código tradicional local, sem depender de outra chamada de IA.

Exemplo de componente:

```text
validate_plan.py
```

Responsabilidades mínimas:

- validar JSON contra o Schema;
- validar IDs e referências;
- verificar ausência de decisões humanas pendentes;
- verificar ações órfãs;
- verificar critérios órfãos;
- verificar dependências;
- verificar existência de evidência;
- verificar consistência de arquivos e permissões;
- verificar invariantes estruturais.

O agente gera o plano.

O validator decide se a estrutura está apta para revisão.

---

## 19. Validação semântica humana

A semântica final não será considerada determinística por script local.

O humano valida:

\[
M = SemanticValidity
\]

Perguntas de revisão:

- o Goal representa corretamente a intenção?
- o plano resolve realmente o problema?
- os ACs provam o Goal?
- as ações são necessárias?
- existem premissas falsas ou omissões relevantes?
- os Boundaries representam corretamente a autoridade e o escopo?

A aprovação humana é condição necessária para implementação.

---

## 20. Readiness

Definições:

\[
S = SchemaValid
\]

\[
T = TraceabilityValid
\]

\[
A = AuthorityResolved
\]

\[
D = DependenciesValid
\]

\[
V = ValidationEvidenceDefined
\]

\[
C = InternalConsistency
\]

\[
M = HumanSemanticValidation
\]

\[
H = ApprovedRevisionIntegrity
\]

### Ready for Review

\[
\boxed{
RFR =
S \times T \times A \times D \times V \times C
}
\]

Quando:

\[
RFR = 1
\]

o status pode se tornar:

```text
READY_FOR_REVIEW
```

### Ready for Implementation

\[
\boxed{
RFI =
RFR \times M \times H
}
\]

Quando:

\[
RFI = 1
\]

o status pode se tornar:

```text
READY_FOR_IMPLEMENTATION
```

---

## 21. Autoridade sobre estados

O Planner não pode aprovar o próprio plano.

Responsabilidades:

```text
DRAFT
  -> Planner

READY_FOR_REVIEW
  -> Local Validator

READY_FOR_IMPLEMENTATION
  -> Human Approval / Gate

EXECUTABLE
  -> Executor Preflight
```

Regra:

\[
Planner \not\rightarrow READY\_FOR\_IMPLEMENTATION
\]

---

## 22. Imutabilidade após aprovação

A aprovação humana deve estar vinculada à versão exata do plano.

Identidade mínima:

```json
{
  "proposal_id": "PROP-...",
  "revision": 1,
  "content_hash": "..."
}
```

A aprovação vale para:

\[
Approve(proposal\_id, revision, hash)
\]

Qualquer alteração relevante invalida a aprovação:

\[
hash_{current} \neq hash_{approved}
\Rightarrow
READY\_FOR\_IMPLEMENTATION = 0
\]

---

## 23. Gestão de diretórios e sandbox

A separação deve existir também por enforcement técnico.

### Durante o Planner

| Diretório | Permissão | Propósito |
|---|---|---|
| `.agent_rules/` | somente leitura | Schema, políticas, regras e scripts confiáveis |
| `.planning/` | leitura/escrita | Propostas geradas pelo Planner |
| `src/` | bloqueado ou somente leitura | Implementação fora da autoridade do Planner |

### Durante o Executor

| Diretório | Permissão | Propósito |
|---|---|---|
| `.agent_rules/` | somente leitura | Regras imutáveis |
| `.planning/` | somente leitura | Contrato aprovado |
| `src/targets` | leitura/escrita | Superfície de implementação autorizada |

Princípio:

\[
Policy \neq Enforcement
\]

Regras no prompt são policy.

Permissões de filesystem/sandbox são enforcement.

---

## 24. Máquina de estados

Fluxo conceitual fechado:

```text
HUMAN_REQUEST
      |
      v
PLANNING
      |
      v
DRAFT
      |
      v
STRUCTURAL_VALIDATION
   +--+----------------+
   |                   |
   v                   v
INVALID         READY_FOR_REVIEW
                       |
                       v
             HUMAN_SEMANTIC_REVIEW
                 +-----+------+
                 |            |
                 v            v
             REJECTED      APPROVED
                              |
                              v
                  READY_FOR_IMPLEMENTATION
                              |
                              v
                           PREFLIGHT
                       +------+------+
                       |             |
                       v             v
                    BLOCKED      EXECUTABLE
                                     |
                                     v
                                  EXECUTOR
```

---

## 25. Preflight do Executor

Mesmo um plano aprovado não é executado automaticamente.

Antes da execução:

\[
EXECUTE = RFI \times Preflight
\]

O preflight deve confirmar, no mínimo:

- proposal_id;
- revision;
- hash aprovado;
- schema ainda válido;
- arquivos autorizados;
- dependências;
- preconditions;
- estado esperado do repositório;
- ausência de decisões humanas pendentes;
- compatibilidade entre plano e realidade atual.

Somente:

\[
Preflight = PASS
\]

permite execução.

---

## 26. Divergência entre plano e realidade

O Executor não recebe autorização implícita para replanejar.

Se:

\[
Reality \neq PlannedContext
\]

a política deve classificar a divergência.

Exemplo:

```text
minor_technical_variance -> autonomia técnica permitida
semantic_variance        -> STOP
scope_variance           -> STOP
human_decision_required  -> STOP
forbidden_surface_change -> STOP
```

Regra:

\[
Unknown \neq PermissionToGuess
\]

e:

\[
SemanticVariance \Rightarrow STOP
\]

---

## 27. Invariantes do Planner

O Planner v1 é considerado válido somente se preservar estas invariantes:

### I-01 — Goal definido

\[
GoalValid = 1
\]

### I-02 — Boundaries satisfeitos

\[
BoundariesSatisfied = 1
\]

### I-03 — Nenhuma ação órfã

\[
NoOrphanAction = 1
\]

### I-04 — Nenhum critério órfão

\[
NoOrphanCriterion = 1
\]

### I-05 — Nenhuma decisão humana pendente para execução

\[
PendingHumanDecision = 0
\]

### I-06 — Evidência definida

\[
EvidenceDefined = 1
\]

### I-07 — Dependências consistentes

\[
DependenciesValid = 1
\]

### I-08 — Rastreabilidade completa

\[
Action \rightarrow AC \rightarrow Output \rightarrow Goal
\]

### I-09 — Schema válido

\[
SchemaValid = 1
\]

### I-10 — Sem autoaprovação

\[
PlannerCannotApprove = 1
\]

### I-11 — Alteração invalida aprovação

\[
ChangedProposal \Rightarrow ApprovalInvalid
\]

### I-12 — Planejamento não altera implementação

\[
PlannerWrite(src/) = DENIED
\]

---

## 28. Decisões arquiteturais registradas

### DEC-PLN-001 — Separação entre planejamento e execução

O Planner produz somente proposta de tarefa.

### DEC-PLN-002 — Validação estrutural local

Schema, rastreabilidade, dependências, authority e evidência são verificadas por script local determinístico.

### DEC-PLN-003 — Validação semântica humana

A correção semântica final do plano é certificada pelo humano.

### DEC-PLN-004 — Gate de duas fases

`READY_FOR_REVIEW` e `READY_FOR_IMPLEMENTATION` são estados distintos.

### DEC-PLN-005 — Planner não controla aprovação

O Planner não pode promover seu próprio plano para estados aprovados.

### DEC-PLN-006 — Sandbox por fase

Permissões de filesystem diferem entre Planner e Executor.

### DEC-PLN-007 — Ações e critérios possuem IDs

A rastreabilidade deve ser estrutural, não apenas textual.

### DEC-PLN-008 — Cobertura bidirecional obrigatória

Nenhuma ação ou critério pode permanecer órfão.

### DEC-PLN-009 — Aprovação vinculada a revisão e hash

Qualquer alteração posterior invalida readiness de implementação.

### DEC-PLN-010 — Executor executa contrato aprovado

O Executor não redefine a intenção, Goal ou semântica do plano.

### DEC-PLN-011 — Preflight obrigatório

`READY_FOR_IMPLEMENTATION` é necessário, mas não suficiente para execução.

### DEC-PLN-012 — Divergência semântica causa STOP

O Executor não improvisa diante de divergência de escopo, significado ou autoridade.

---

## 29. Critério de fechamento conceitual

O Planner v1 é considerado **conceitualmente fechado** porque estão definidos:

- propósito;
- entradas;
- saídas;
- modelo semântico;
- operadores;
- invariantes;
- regras de inferência;
- critérios de aceitação;
- decomposição em ações;
- rastreabilidade;
- autoridade;
- estados;
- validação estrutural;
- validação semântica;
- sandbox;
- imutabilidade de aprovação;
- readiness;
- fronteira com Executor;
- política de STOP.

Status:

\[
\boxed{
Planner\ v1 = CLOSED
}
\]

---

## 30. Contrato conceitual da fronteira com o Executor

Premissa para a próxima fase:

\[
\boxed{
Executor\ recebe\ somente\ um\ TaskProposal\ aprovado,\ imutável,\ estruturalmente\ válido\ e\ semanticamente\ aceito
}
\]

Ou:

\[
HumanRequest
\rightarrow Planner
\rightarrow TaskProposal
\rightarrow StructuralValidator
\rightarrow HumanSemanticReview
\rightarrow READY\_FOR\_IMPLEMENTATION
\rightarrow Preflight
\rightarrow Executor
\]

A partir deste ponto, novas decisões pertencem ao **Contrato do Executor**, sem reabrir o modelo conceitual do Planner, salvo mudança arquitetural explícita e versionada.
