# CEPRAEA BEACH PRO — Human-Governed Dual-Agent SDLC

**Status:** CANONICAL
**Control plane:** `.ai/control/`, `.ai/decisions/`, `.ai/tasks/`

## Escopo

Arquitetura do processo de desenvolvimento. Não faz parte do runtime usado por atletas/treinador.

## Objetivos

1. autoridade humana final;
2. planejamento separado de execução;
3. revisão independente;
4. validadores determinísticos antes de claims de sucesso;
5. evidência material rastreável;
6. Git como state machine/histórico;
7. ausência de infraestrutura agentiva paralela desnecessária.

## Building blocks

- **Humano:** intenção, semântica, aprovação, Git privilegiado, release.
- **Claude / PLANNER:** Human Request → TaskProposal.
- **Codex / PLAN REVIEW:** refuta e revisa TaskProposal.
- **Humano / APPROVAL:** vincula a revisão e o SHA-256 exato da proposta.
- **Claude / EXECUTOR:** implementação dentro do contrato aprovado.
- **Codex / IMPLEMENTATION REVIEW:** refutação independente de diff/evidência.
- **Git:** estado, handoff, histórico e promoção.
- **`.ai/control`:** contratos/oráculos.
- **`.ai/decisions`:** decisões humanas.
- **`.ai/tasks`:** instâncias materiais.

## Lifecycle

```text
Human Request
→ Planner
→ proposal.json
→ deterministic proposal validation
→ Codex PLAN review
→ Human approval.json (hash-bound)
→ Executor preflight
→ Actions
→ deterministic checks + evidence
→ execution-result.json
→ Codex IMPLEMENTATION review
→ Human
→ Git
```

## Invariantes

- Planner não escreve produto.
- Executor não altera contrato aprovado.
- Reviewer não corrige artefatos.
- Agente não cria `approval.json`.
- Aprovação não vale se o hash da proposta mudou.
- Toda Action possui AC.
- Todo AC possui Action.
- Toda mudança possui Action.
- Toda Action `PASS` possui evidência.
- `NO EVIDENCE → NO PASS`.
- Git privilegiado pertence ao humano.
- Contradição material bloqueia; agente não escolhe silenciosamente.
- Bootstrap `DESIGN` e FVR `PILOT_ONLY` não concedem autorização.

## Estados

### Planner/Executor
`READY_FOR_REVIEW | BLOCKED`

### Reviewer
`PASS | FAIL | HUMAN_DECISION_REQUIRED`

O detalhe de falha fica em `termination_reason`, não em novos estados externos.

## Autoridade dos artefatos

```text
Humano
↓
AGENT_POLICY.md
↓
.ai/decisions ACTIVE
↓
.ai/control contracts
↓
CLAUDE.md / AGENTS.md
↓
runbooks
↓
.ai/tasks instance
↓
docs explicativos
```

Documentos arquiteturais não redefinem enums, schemas ou paths executáveis. Eles referenciam `.ai/control`.

## Segurança

- Reviewer read-only.
- Git mutável humano-only.
- control plane read-only para agentes em tarefas normais.
- filesystem/sandbox devem implementar as permissões declaradas; prompt não substitui enforcement.
- falha de enforcement → `BLOCKED`, nunca bypass.

## Produção

"Produção" neste documento significa maturidade do **control plane do SDLC**. O status de produção do produto CEPRAEA BEACH PRO é decisão separada e continua sujeito ao `README.md`, decisões de domínio, segurança, dados e release.
