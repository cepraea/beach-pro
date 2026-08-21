# Executor v1 — Especificação Formal

**Status:** `CLOSED`  
**Fase:** 2 — Approved Task Proposal → Implementation + Evidence  
**Dependência:** Planner v1 `CLOSED`  
**Data:** 2026-08-20

---

## 1. Propósito

O Executor transforma um `TaskProposal` aprovado em implementação verificável sem redefinir a intenção, o escopo, os critérios de aceitação ou a autoridade definidos pelo Planner.

A fronteira é:

\[
READY\_FOR\_IMPLEMENTATION
\rightarrow
Executor
\rightarrow
ExecutionResult
\]

O Executor é responsável pelo **HOW**, mas somente dentro do **WHAT** autorizado:

\[
\boxed{HOW \subseteq WHAT}
\]

---

## 2. Princípio central

O contrato recebido pelo Executor é imutável.

\[
SemanticFreedom_{Executor}=0
\]

O Executor pode escolher detalhes técnicos equivalentes, mas não pode alterar Goal, Output, Acceptance Criteria, Scope, Boundaries, Business Rules, Human Decisions, Definition of Done, Stop Conditions, arquivos proibidos ou evidências obrigatórias.

\[
ContractMismatch \Rightarrow STOP
\]

---

## 3. Contrato de entrada

O Executor recebe um `ExecutionContract` composto por:

\[
EC = TaskProposal_{approved} + ApprovalProof + RuntimeAnchor
\]

### 3.1 TaskProposal aprovado

Fonte de verdade semântica, em modo somente leitura. Deve conter as decisões fechadas pelo Planner, incluindo ações e critérios identificados e rastreáveis.

### 3.2 ApprovalProof

A aprovação é vinculada à versão exata do plano:

\[
Approve(proposal\_id,revision,hash)
\]

O Executor só aceita `READY_FOR_IMPLEMENTATION` quando `proposal_id`, `revision` e `hash` correspondem exatamente ao artefato recebido.

### 3.3 RuntimeAnchor

O contrato também é vinculado ao estado do repositório:

```text
repository
branch
base_commit
working_tree_policy
```

Se o estado material relevante divergir do estado aprovado:

\[
RuntimeDrift \Rightarrow STOP
\]

---

## 4. Preflight obrigatório

Nenhuma alteração pode ocorrer antes de:

\[
\boxed{EXECUTABLE = RFI \times Preflight}
\]

O Preflight deve confirmar:

1. `TaskProposal` válido;
2. status `READY_FOR_IMPLEMENTATION`;
3. `proposal_id` correto;
4. `revision` correta;
5. hash aprovado corresponde ao conteúdo atual;
6. RuntimeAnchor corresponde ao repositório atual;
7. regras e schemas confiáveis permanecem íntegros;
8. nenhuma decisão humana pendente;
9. preconditions satisfeitas;
10. dependencies satisfeitas ou corretamente ordenadas;
11. DAG de ações válido;
12. todos os IDs e referências resolvem;
13. arquivos autorizados estão acessíveis;
14. arquivos proibidos permanecem inacessíveis para escrita;
15. runbooks aplicáveis estão disponíveis;
16. não existe mudança de risco não prevista.

Se qualquer condição obrigatória falhar, `Preflight=BLOCKED` e nenhuma implementação começa.

---

## 5. Autoridade técnica

\[
ExecutorAuthority = AllowedTechnicalAutonomy \cap Boundaries \cap TargetFiles
\]

### 5.1 Permitido por padrão, quando não altera semântica

Dentro de arquivos e ações já autorizados, o Executor pode decidir:

- nomes de variáveis e funções internas;
- organização local de código;
- escolha entre algoritmos semanticamente equivalentes;
- pequenas funções auxiliares;
- ordem interna entre passos independentes;
- estrutura interna de testes;
- detalhes idiomáticos da linguagem;
- refatoração local estritamente necessária à ação autorizada.

### 5.2 Não permitido sem autorização explícita

O Executor não pode autonomamente:

- mudar API pública;
- alterar schema de banco;
- adicionar ou remover dependência;
- mudar autenticação, autorização, RLS ou MFA;
- alterar arquitetura compartilhada;
- mudar regras de negócio;
- criar superfície de escrita fora de `files.target`;
- ampliar escopo;
- excluir comportamento não solicitado;
- substituir Acceptance Criteria;
- alterar decisões humanas;
- alterar Definition of Done.

\[
UnauthorizedDecisionRequired \Rightarrow STOP
\]

---

## 6. Superfície de arquivos

`files` é enforcement de superfície de mudança.

- `target`: pode sofrer a operação autorizada.
- `reference`: somente leitura.
- `read_only`: somente leitura.
- `forbidden`: nenhuma mudança permitida.

\[
FileChange_x \notin TargetSurface
\Rightarrow STOP\_FORBIDDEN\_FILE\_ACCESS
\]

O Executor não pode tratar melhoria fora dos targets como oportunidade de refatoração.

---

## 7. Unidade de execução

O Executor trabalha ação por ação:

\[
A_i
\rightarrow Preconditions_i
\rightarrow Dependencies_i
\rightarrow Authority_i
\rightarrow Execute_i
\rightarrow Validate_i
\rightarrow Evidence_i
\]

Uma ação só é elegível quando:

\[
Eligible_i = A_i \times Preconditions_i \times Dependencies_i \times Authority_i \times Boundaries_i
\]

Se `Eligible_i=0`, a ação não pode iniciar.

---

## 8. Conclusão de ação

Código escrito não significa ação concluída.

\[
\boxed{PASS_i = Implementation_i \times Validation_i \times Evidence_i \times BoundaryIntegrity_i}
\]

Uma ação `PASS` exige implementação correspondente, critérios relacionados verificados, evidência registrada e nenhuma violação de boundaries.

---

## 9. Rastreabilidade de execução

O Executor estende a rastreabilidade do Planner:

\[
FileChange \rightarrow Action \rightarrow AC \rightarrow Output \rightarrow Goal
\]

Toda mudança precisa apontar para pelo menos uma ação autorizada.

\[
FileChange_x \nrightarrow A_i \Rightarrow UnauthorizedChange
\]

Uma mudança tecnicamente boa, mas sem ancestral contratual, continua inválida.

---

## 10. Dependências e ordem

O Executor não redefine semanticamente o DAG do Planner. Pode escolher ordem entre ações independentes, mas deve preservar dependências declaradas.

Descoberta de dependência semântica nova:

\[
NewRequiredDependency \Rightarrow STOP
\]

salvo quando estiver explicitamente dentro da autonomia técnica e da superfície autorizada.

---

## 11. Divergências

### `MINOR_TECHNICAL_VARIANCE`

Diferença interna sem alteração de significado, escopo, AC, autoridade ou superfície de mudança. Pode continuar dentro da autonomia técnica.

### `CONTRACT_AMBIGUITY`

Contrato permite interpretações semanticamente diferentes. `STOP`.

### `SEMANTIC_VARIANCE`

A realidade exige mudar o significado do plano. `STOP`.

### `SCOPE_VARIANCE`

A solução exige trabalho fora do escopo. `STOP`.

### `DEPENDENCY_VARIANCE`

A solução exige dependência não autorizada. `STOP`.

### `HUMAN_DECISION_REQUIRED`

É necessária decisão reservada ao humano. `STOP`.

### `RISK_VARIANCE`

O risco observado é maior ou de natureza diferente do aprovado. `STOP`.

---

## 12. STOP Conditions

Códigos fechados do Executor v1:

```text
STOP_CONTRACT_INVALID
STOP_APPROVAL_MISMATCH
STOP_RUNTIME_DRIFT
STOP_PRECONDITION_FAILED
STOP_DEPENDENCY_UNSATISFIED
STOP_SCOPE_VARIANCE
STOP_SEMANTIC_VARIANCE
STOP_CONTRACT_AMBIGUITY
STOP_HUMAN_DECISION_REQUIRED
STOP_FORBIDDEN_FILE_ACCESS
STOP_UNAUTHORIZED_DEPENDENCY_CHANGE
STOP_UNAUTHORIZED_DATABASE_CHANGE
STOP_RUNBOOK_VIOLATION
STOP_RISK_ESCALATION
STOP_EVIDENCE_IMPOSSIBLE
STOP_RULES_INTEGRITY_FAILURE
```

STOP significa que a execução não pode continuar legitimamente sob o contrato atual. STOP não autoriza replanejamento silencioso.

---

## 13. Falha de validação não é automaticamente STOP

Uma implementação pode ser autorizada e falhar no AC:

\[
ValidationFailure \Rightarrow FAILED\_VALIDATION
\]

O Executor pode corrigir a implementação enquanto permanecer na mesma ação, sem alterar Goal, Scope, AC ou Boundaries, sem nova decisão e sem ampliar a superfície autorizada.

Se a correção exigir qualquer uma dessas mudanças, ocorre `STOP`.

---

## 14. Evidências

Toda ação executada deve produzir evidência referenciável.

Tipos admitidos:

```text
test
build
lint
typecheck
schema_validation
command
diff
file_snapshot
runtime_log
query_result
migration_check
dependency_audit
other
```

Cada evidência registra `evidence_id`, ações, ACs, tipo, status, resumo, origem, artefatos e, quando aplicável, comando e exit code.

\[
EveryExecutedActionHasEvidence = 1
\]

---

## 15. Mudanças de arquivo

Toda mudança registra path, operação, ações que a autorizam, status de autorização e hashes anterior/posterior quando aplicável.

Operações:

```text
create
modify
delete
rename
```

Para resultado pronto para revisão:

\[
UnauthorizedChanges = \varnothing
\]

---

## 16. Estados do Executor

```text
READY_FOR_IMPLEMENTATION
          |
          v
       PREFLIGHT
     +----+----+
     |         |
     v         v
PREFLIGHT_   EXECUTABLE
 BLOCKED        |
                v
            EXECUTING
                |
        +-------+-------+
        |               |
        v               v
     STOPPED       ACTION_RESULT
                       |
                +------+------+
                |             |
                v             v
             FAILED          PASS
                               |
                               v
                          NEXT_ACTION
                               |
                               v
                          FINAL_CHECKS
                         +-----+------+
                         |            |
                         v            v
                FAILED_VALIDATION  IMPLEMENTATION_
                                   READY_FOR_REVIEW
```

Estados finais válidos:

```text
IMPLEMENTATION_READY_FOR_REVIEW
FAILED_VALIDATION
PREFLIGHT_BLOCKED
STOPPED
```

---

## 17. Final Checks

Depois de todas as ações:

\[
ExecutionValid =
\left(\prod_{i=1}^{n} PASS_i\right)
\times NoUnauthorizedChanges
\times ContractIntegrity
\times FinalChecks
\]

Somente `ExecutionValid=1` permite `IMPLEMENTATION_READY_FOR_REVIEW`.

O Executor não declara aceitação final do sistema.

---

## 18. Invariantes do Executor v1

- **EXE-I01 — ContractImmutable:** contrato não é modificado.
- **EXE-I02 — NoWriteBeforePreflight:** nenhuma escrita antes do preflight.
- **EXE-I03 — EveryChangeHasAction:** toda mudança possui ação ancestral.
- **EXE-I04 — EveryExecutedActionHasEvidence:** toda ação executada possui evidência.
- **EXE-I05 — BoundariesPreserved:** boundaries são preservados.
- **EXE-I06 — NoSemanticReplanning:** Executor não replaneja semanticamente.
- **EXE-I07 — StopOnSemanticVariance:** divergência semântica causa STOP.
- **EXE-I08 — ContractHashStable:** hash do contrato permanece estável.
- **EXE-I09 — DependencyOrderValid:** dependências declaradas são respeitadas.
- **EXE-I10 — NoUnauthorizedChanges:** resultado pronto possui zero mudanças não autorizadas.
- **EXE-I11 — FinalChecksPassed:** todos os checks finais obrigatórios passam.
- **EXE-I12 — ExecutorCannotFinalApprove:** Executor não concede aceitação final.

---

## 19. Decisões arquiteturais

### DEC-EXE-001 — Planner permanece fechado
O Executor não reabre decisões do Planner.

### DEC-EXE-002 — TaskProposal aprovado é fonte de verdade
A instrução humana original não substitui o contrato.

### DEC-EXE-003 — Contrato é imutável
Mudança exige nova revisão e aprovação.

### DEC-EXE-004 — Preflight obrigatório
Nenhuma escrita antes do PASS.

### DEC-EXE-005 — Autonomia técnica, não semântica
O Executor escolhe HOW somente dentro do WHAT autorizado.

### DEC-EXE-006 — Superfície de escrita default-deny
Somente targets autorizados podem ser alterados.

### DEC-EXE-007 — Execução ação por ação
Cada ação possui validação e evidência próprias.

### DEC-EXE-008 — Toda mudança é rastreável
Nenhuma alteração órfã é válida.

### DEC-EXE-009 — STOP não significa improvisar
STOP encerra a autoridade do contrato atual.

### DEC-EXE-010 — Falha de AC pode ser corrigida localmente
Somente dentro da mesma ação e autonomia.

### DEC-EXE-011 — Divergência de risco bloqueia execução
Aumento ou mudança de natureza de risco exige nova autoridade.

### DEC-EXE-012 — Executor produz `ExecutionResult`
O artefato formal de saída é `execution_result.json`.

### DEC-EXE-013 — Executor não é Reviewer
Seu estado máximo é `IMPLEMENTATION_READY_FOR_REVIEW`.

### DEC-EXE-014 — RuntimeAnchor vincula contrato à realidade executada
Mudança material do estado-base invalida o preflight.

---

## 20. `execution_result.json`

O resultado da execução é validado por `execution_result.schema.json` e deve:

- vincular execução ao plano aprovado;
- registrar preflight;
- registrar ações e status;
- registrar mudanças;
- registrar evidências;
- registrar divergências;
- registrar STOP quando houver;
- registrar checks finais;
- registrar integridade do contrato;
- declarar o estado final do Executor.

---

## 21. Validação além do JSON Schema

O `execution_result.schema.json` valida forma, enums e algumas invariantes condicionais, mas não substitui o validator local.

O validator determinístico deve verificar relações que JSON Schema não expressa de forma suficiente, incluindo:

- `proposal_id == approval_binding.approved_proposal_id`;
- `proposal_revision == approval_binding.approved_revision`;
- `proposal_hash == approval_binding.approved_hash`;
- unicidade de `action_id`, `evidence_id`, `change_id`, `check_id` e `deviation_id`;
- toda referência `action_refs` resolve para uma ação existente;
- toda referência `acceptance_criteria_refs` resolve para um AC do `TaskProposal` aprovado;
- todo `evidence_ref` resolve para evidência existente;
- todo `files_changed` possui `changeEntry` correspondente;
- toda mudança pertence a `files.target` e à operação permitida;
- nenhuma mudança ocorreu antes do PASS do preflight;
- DAG de ações é acíclico e respeitado;
- hashes correspondem aos arquivos reais;
- RuntimeAnchor corresponde ao estado real do repositório;
- todos os mandatory checks do contrato aparecem nos `final_checks`;
- todos os ACs exigidos pela ação possuem evidência suficiente.

Portanto:

\[
ExecutionResultValid = SchemaValid \times ExecutorValidatorValid
\]

---

## 22. Critério de fechamento

O Executor v1 está conceitualmente fechado porque estão definidos contrato de entrada, autoridade, autonomia, preflight, superfície de escrita, unidade de execução, validação, evidência, rastreabilidade, dependências, divergências, STOP conditions, estados, invariantes, resultado formal e limite de autoridade final.

\[
\boxed{Executor\ v1 = CLOSED}
\]

Próxima fronteira:

\[
ExecutionResult \rightarrow Reviewer
\]

O Reviewer poderá certificar implementação e evidências contra o contrato aprovado sem reabrir Planner ou Executor.
