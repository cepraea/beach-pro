# CEPRAEA BEACH PRO — Claude Code

**Papel:** PLANNER ou EXECUTOR, nunca Reviewer.

Leia `AGENT_POLICY.md` e `.ai/control/README.md` antes de iniciar.

## 1. Selecionar a fase

A instrução humana deve deixar claro se a atividade é:

- `PLAN`: elaborar/atualizar um `TaskProposal`;
- `EXECUTE`: implementar um `TaskProposal` aprovado.

Se a fase não puder ser determinada sem alterar significado, finalize `BLOCKED`.

## 2. Fase PLAN

### Permissões

Pode:

- ler o repositório, fontes normativas, decisões e runbooks;
- criar/atualizar somente `.ai/tasks/<TASK-ID>/proposal.json` da tarefa corrente.

Não pode:

- alterar código do produto;
- criar/alterar `approval.json`;
- alterar `.ai/control/**` ou `.ai/decisions/**`, salvo quando a própria tarefa humana de governança os declarar como targets;
- aprovar o próprio plano.

### Procedimento

1. Preserve `original_instruction` literalmente.
2. Derive Goal, outputs, boundaries, fontes normativas, ACs e Actions.
3. Dê IDs estáveis a outputs (`OUT-*`), critérios (`AC-*`) e ações (`A-*`).
4. Garanta cobertura bidirecional:
   - toda Action referencia pelo menos um AC;
   - todo AC é coberto por pelo menos uma Action.
5. Declare dependências entre Actions sem ciclos.
6. Declare `files` com `target | reference | read_only | forbidden`.
7. Classifique risco conforme `AGENT_POLICY.md`.
8. Declare apenas `operation_classes` e flags em `runbook_binding`; não copie paths de runbooks.
9. Não converta desconhecido em fato ou permissão.
10. Execute:

```bash
node .ai/control/validate-task-proposal.mjs .ai/tasks/<TASK-ID>/proposal.json
```

### Saída

- validação passou e não há decisão humana pendente → `READY_FOR_REVIEW`;
- qualquer lacuna material, contradição, referência inválida ou decisão humana pendente → `BLOCKED`.

## 3. Gate entre PLAN e EXECUTE

Não implemente até existirem, para a mesma TASK:

```text
.ai/tasks/<TASK-ID>/proposal.json
.ai/tasks/<TASK-ID>/approval.json
```

e o comando abaixo retornar `PASS`:

```bash
node .ai/control/validate-task-approval.mjs \
  .ai/tasks/<TASK-ID>/proposal.json \
  .ai/tasks/<TASK-ID>/approval.json
```

A aprovação deve:

- registrar `plan_review.verdict = PASS`;
- ser emitida por `actor_type = human`;
- vincular `proposal_id`, `revision` e SHA-256 exato dos bytes da proposta;
- vincular repository, branch e base commit;
- estar `decision = approved`.

Qualquer mismatch → `BLOCKED`.

## 4. Fase EXECUTE — preflight

Antes da primeira escrita:

1. valide proposta e aprovação;
2. confirme que a branch não é `main` nem `master`;
3. confirme o `RuntimeAnchor`;
4. carregue runbooks por `.ai/control/runbook-catalog.json`;
5. confirme preconditions e dependências;
6. confirme a superfície `files.target`;
7. confirme que `.ai/control/**`, `.ai/decisions/**` e `approval.json` permanecem read-only;
8. registre os checks de preflight no futuro `execution-result.json`.

Enquanto `bootstrap_mode=DESIGN`, o bootstrap é diagnóstico; não o trate como autoridade para conceder ou negar execução. Em modo `ENFORCE_BASE`, siga a decisão ativa que promoveu o gate.

## 5. Execução

Para cada Action:

```text
Action
→ Preconditions
→ Dependencies
→ Authority
→ Execute
→ Validate
→ Evidence
```

- Não altere Goal, ACs, Actions, boundaries, risco ou decisões humanas.
- Não expanda targets.
- Não adicione dependência, migration, RLS/auth/MFA ou mudança arquitetural sem autorização explícita.
- Falha de AC pode ser corrigida localmente somente se a correção permanecer na mesma Action, no mesmo escopo e na mesma autoridade.
- Divergência semântica, de escopo, dependência, risco ou autoridade → `BLOCKED`.

## 6. Evidence e ExecutionResult

Produza:

```text
.ai/tasks/<TASK-ID>/execution-result.json
```

Ele deve registrar:

- proposal/approval bindings;
- RuntimeAnchor;
- preflight;
- Actions e status;
- mudanças e hashes;
- evidências observadas;
- final checks;
- mudanças não autorizadas;
- `handoff_status`;
- `termination_reason`.

Nunca escreva evidência simulada.

Antes do handoff execute:

```bash
node .ai/control/validate-execution-result.mjs \
  .ai/tasks/<TASK-ID>/proposal.json \
  .ai/tasks/<TASK-ID>/approval.json \
  .ai/tasks/<TASK-ID>/execution-result.json
```

e também os validadores da TASK, `git diff --check`, `git diff` e `git status`.

## 7. Handoff

Informe fatos, não aprovação final:

- TASK e Actions executadas;
- arquivos alterados;
- checks e exit codes;
- evidências materiais;
- limitações/bloqueios;
- pontos relevantes ao Reviewer.

Finalize exatamente com:

`READY_FOR_REVIEW`

ou

`BLOCKED`
