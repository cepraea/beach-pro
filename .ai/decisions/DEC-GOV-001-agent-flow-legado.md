# DEC-GOV-001 — Remoção do workflow legado `.agent-flow`

**Data:** 2026-08-14
**Status:** APROVADO
**Aprovador:** Davi Sermenho
**Tipo:** governança documental — sem rebuild

## Decisão

`.agent-flow/**` foi substituído pelo workflow vigente definido em:

- `AGENT_POLICY.md` — política comum dos agentes;
- `CLAUDE.md` — adaptador do papel EXECUTOR (Claude Code);
- `AGENTS.md` — adaptador do papel REVIEWER (Codex);
- Git / working tree / `git diff` — estado e handoff operacionais.

Os artefatos do diretório `.agent-flow/` são removidos do HEAD para eliminar
ambiguidade normativa e evitar que agentes recuperem contexto desatualizado.
O histórico permanece recuperável por `git log` e `git show`.

## Artefatos removidos

```text
.agent-flow/STATE.md      → HISTÓRICO / NÃO NORMATIVO
.agent-flow/EXECUTOR.md   → SUBSTITUÍDO por CLAUDE.md
.agent-flow/REVIEWER.md   → SUBSTITUÍDO por AGENTS.md
.agent-flow/executions/** → HISTÓRICO
.agent-flow/review/**     → HISTÓRICO
```

## Referências normativas atualizadas

Os seguintes arquivos continham referências operacionais a `.agent-flow/**`
como `WRITE_SCOPE` do workflow antigo e foram anotados como legado:

- `docs/modelagem/decisoes/registro_decisoes.md`
- `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`

Referências históricas (narrativas de AC-000) foram mantidas com contexto.

## Consequência

Nenhum agente deve consultar `.agent-flow/**` como fonte normativa.
`WRITE_SCOPE` vigente do EXECUTOR é `docs/modelagem/**` conforme
`AGENT_POLICY.md` e `CLAUDE.md`.
