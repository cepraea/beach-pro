# CEPRAEA BEACH PRO — Política Comum dos Agentes

> **Escopo:** governa o SDLC agentivo do repositório. Não se aplica ao runtime do produto.
> **Princípio:** produção, revisão e aprovação são funções distintas. Nenhum agente aprova ou promove o próprio trabalho.

## 1. Papéis e autoridade

- **Humano:** autoridade final sobre intenção, domínio, decisões materiais, aprovação de plano, Git privilegiado, release e deploy.
- **Claude Code:** atua em duas fases mutuamente exclusivas:
  - **PLANNER:** transforma a instrução humana em `TaskProposal`.
  - **EXECUTOR:** implementa somente um `TaskProposal` aprovado e íntegro.
- **Codex:** **REVIEWER** independente, em dois estágios:
  - `PLAN`: revisa o `TaskProposal`.
  - `IMPLEMENTATION`: revisa implementação, evidências e `ExecutionResult`.

ChatGPT/Gemini podem ser usados como meta-review excepcional, sem autoridade automática.

## 2. Control plane canônico

Os únicos namespaces persistentes do control plane são:

```text
.ai/control/    contratos, catálogos, validadores e fixtures
.ai/decisions/  decisões humanas de arquitetura/governança
.ai/tasks/      instâncias materiais de tarefas
```

São proibidos como mecanismos operacionais concorrentes:

```text
.agent-flow/
.agent_rules/
.planning/
```

`Git` permanece a state machine e o histórico operacional. `.ai/tasks/` não é fila, banco de workflow, log de conversa nem substituto do Git.

## 3. Hierarquia normativa

1. decisão humana explícita atual;
2. `AGENT_POLICY.md`;
3. decisões `ACTIVE` em `.ai/decisions/INDEX.md`;
4. contratos executáveis em `.ai/control/`;
5. adaptadores de papel `CLAUDE.md` e `AGENTS.md`;
6. `runbooks/README.md` e runbooks aplicáveis;
7. instância corrente em `.ai/tasks/<TASK-ID>/`;
8. documentação arquitetural explicativa.

Contradição material não é resolvida silenciosamente por precedência:

- Executor/Planner → `BLOCKED`;
- Reviewer → `HUMAN_DECISION_REQUIRED`.

## 4. Ciclo canônico

```text
Human Request
    ↓
Claude / PLANNER
    ↓
.ai/tasks/<TASK-ID>/proposal.json
    ↓
validação determinística
    ↓
Codex / PLAN REVIEW
    ↓ PASS
aprovação humana vinculada ao SHA-256 exato da proposta
    ↓
.ai/tasks/<TASK-ID>/approval.json
    ↓
Claude / EXECUTOR PREFLIGHT
    ↓
implementação + validações + evidência
    ↓
.ai/tasks/<TASK-ID>/execution-result.json
    ↓
Codex / IMPLEMENTATION REVIEW
    ↓
PASS | FAIL | HUMAN_DECISION_REQUIRED
    ↓
Humano
    ↓
Git privilegiado / promoção
```

`Codex PASS` no estágio `PLAN` é necessário, mas não autoriza execução por si só. O Executor só é autorizado quando `approval.json` é válido, humano, corresponde ao `proposal.json` byte a byte por SHA-256 e o `RuntimeAnchor` continua válido.

## 5. Estados externos fechados

### Planner/Executor

Somente:

- `READY_FOR_REVIEW`
- `BLOCKED`

Diagnósticos internos devem usar `termination_reason`; não criar novos estados de handoff.

### Reviewer

Somente:

- `PASS`
- `FAIL`
- `HUMAN_DECISION_REQUIRED`

Toda saída do Reviewer deve declarar `review_stage = PLAN | IMPLEMENTATION`.

## 6. Evidência e claims

- Ausência de evidência nunca significa `PASS`.
- Agentes não podem fabricar, simular ou inferir resultado de teste, log, comando ou aprovação.
- Evidência material deve ser vinculável a `TASK`, `Action` e `Acceptance Criterion`.
- Resultado de comando material preserva comando, exit code e instante observado.
- `git diff` é evidência de mudança; não é prova automática de correção.
- Evidência marcada como simulada é inválida para aprovação.
- Uma `Action` em `PASS` exige evidência material.
- `READY_FOR_REVIEW` exige zero mudança não autorizada.

## 7. Risco

Valores normativos de `risk.level`:

- `verde`
- `amarelo`
- `vermelho`
- `vermelho_critico`

Valores normativos de `risk.natures`:

- `ui`
- `dependencia`
- `rls`
- `mfa`
- `ci`
- `dados`

Mudanças de control plane, Dev Container, CI, secrets, deploy ou enforcement são `vermelho_critico` por padrão.

## 8. Git

Agentes podem executar somente inspeção read-only, incluindo:

```text
git status
git diff
git diff --check
git log
git show
git rev-parse
git ls-files
git branch --show-current
```

Mutações de Git são exclusivas do humano: `add`, `commit`, `push`, `merge`, `rebase`, criação/movimentação de branch/ref, alteração de index, histórico ou remoto.

## 9. Zonas de escrita

| Path | Planner | Executor | Reviewer | Humano |
| --- | --- | --- | --- | --- |
| `.ai/control/**` | RO | RO | RO | RW |
| `.ai/decisions/**` | RO | RO | RO | RW |
| `.ai/tasks/<TASK>/proposal.json` antes da aprovação | RW | — | RO | RW |
| `.ai/tasks/<TASK>/proposal.json` após aprovação | RO | RO | RO | RW |
| `.ai/tasks/<TASK>/approval.json` | RO | RO | RO | RW |
| `.ai/tasks/<TASK>/execution-result.json` | — | RW | RO | RW |
| targets declarados na TASK | RO | RW | RO | RW |
| Git privilegiado | proibido | proibido | proibido | permitido |

Uma tarefa de arquitetura explicitamente aprovada pelo humano pode autorizar alteração do control plane; nesse caso os paths devem aparecer como `target` no próprio `TaskProposal`, com risco `vermelho_critico`.

## 10. Runbooks

A TASK declara apenas classes de operação e flags semânticas. Os paths dos runbooks são resolvidos por:

```text
.ai/control/runbook-catalog.json
```

Não duplicar manualmente a matriz de paths dentro da TASK.

Classes permitidas:

- `code_change`
- `database_change`
- `documentation_change`
- `dependency_change`

## 11. Bootstrap e FVR

O estado operacional é definido por `.ai/control/control-plane.json`.

Enquanto:

```text
bootstrap_mode = DESIGN
```

o bootstrap é diagnóstico e seu `FAIL` não é autorização nem gate global.

Enquanto:

```text
fvr_mode = PILOT_ONLY
```

o FVR/Verification Plan pode ser executado como piloto, mas não substitui os validadores obrigatórios nem concede `PASS` de produção.

A promoção para modo obrigatório exige decisão humana `ACTIVE` em `.ai/decisions/`.

## 12. Modelagem

Para a modelagem canônica de domínio, preservar o pipeline existente:

```text
fonte → evidência → conhecimento → modelo canônico → modelo lógico
```

Não inventar fatos para preencher lacunas. O plano canônico permanece em `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`.
