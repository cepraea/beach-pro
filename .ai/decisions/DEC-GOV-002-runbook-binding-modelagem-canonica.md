# DEC-GOV-002 — `runbook_binding` formal para as tarefas `AC-NNN`/`SEM-NNN`/`SYN-NNN` da modelagem canônica

**Data:** 2026-08-16
**Status:** APROVADO
**Aprovador:** Davi Sermenho
**Tipo:** governança documental — binding de runbooks, sem rebuild

## Contexto

Durante a revisão adversarial de `AC-001`, o Reviewer (Codex, `AGENTS.md`) apontou que nem
`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` nem `runbooks/README.md` declaram um
`runbook_binding` concreto para as tarefas desta fase — confirmado por inspeção direta (`grep` em
ambos os arquivos, zero ocorrências de `runbook_binding`/`operation_class`/`applicable_runbooks`).
A afirmação de handoffs anteriores do Executor (de que `RB-EXEC-003` seria o binding real desta
fase) era uma inferência não registrada como artefato verificável, o que `AGENTS.md` trata como
divergência material — bloqueia `PASS` até decisão de Davi (`HUMAN_DECISION_REQUIRED`).

## Decisão

Todas as tarefas `AC-NNN`, `SEM-NNN` e `SYN-NNN` da fase de modelagem canônica
(`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`) usam o seguinte `runbook_binding`
formal, válido para toda a fase:

```json
{
  "runbook_binding": {
    "operation_classes": ["documentation_change"],
    "applicable_runbooks": {
      "shared": [
        "runbooks/shared/RB-SHARED-001-repository-baseline.md",
        "runbooks/shared/RB-SHARED-002-evidence.md",
        "runbooks/shared/RB-SHARED-003-failure-states.md"
      ],
      "executor": [
        "runbooks/executor/RB-EXEC-003-documentation-change.md"
      ],
      "reviewer": [
        "runbooks/reviewer/RB-REV-003-documentation-review.md",
        "runbooks/reviewer/RB-REV-004-evidence-review.md"
      ]
    }
  }
}
```

### Justificativa da classe de operação

Todo artefato produzido por `AC-NNN`/`SEM-NNN`/`SYN-NNN` é Markdown com blocos JSON validados por
schema, sob `docs/modelagem/**` — corresponde diretamente a `documentation_change` na matriz de
seleção de `runbooks/README.md`.

### Justificativa da inclusão de `RB-REV-004`

`runbooks/README.md` exige `RB-REV-004-evidence-review.md` adicionalmente quando "a suficiência da
evidência for material para os critérios de aceite ou para a revisão independente". Nesta fase,
isso já se mostrou empiricamente verdadeiro em `AC-001`: quatro rodadas de revisão adversarial
identificaram problemas de suficiência/precisão de evidência (abas/linhas não lidas, localização
incorreta de fragmento, classificação incorreta de dado sensível) — não defeitos de sintaxe ou
formatação, mas exatamente o tipo de achado que `RB-REV-004` existe para cobrir. A inclusão é
permanente para toda a fase, não caso a caso por tarefa.

## Consequência

- O Executor carrega, a partir desta decisão, exatamente os runbooks listados acima em todo turno
  `AC-NNN`/`SEM-NNN`/`SYN-NNN`, além de `AGENT_POLICY.md`/`CLAUDE.md` e da normativa de
  `docs/modelagem/`.
- O Reviewer carrega os runbooks `shared`/`reviewer` acima em toda revisão desta fase, além de
  `AGENT_POLICY.md`/`AGENTS.md`.
- Handoffs de tarefas desta fase devem citar este binding (por número de decisão ou pelo bloco
  JSON acima) para que a vinculação seja verificável no repositório, não apenas declarada em
  prosa.
- Esta decisão não altera `runbooks/README.md` nem os runbooks especializados — apenas registra a
  seleção concreta já prevista pelo mecanismo do catálogo para esta fase.
