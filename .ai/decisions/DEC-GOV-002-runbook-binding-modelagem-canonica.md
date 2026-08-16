# DEC-GOV-002 — `runbook_binding` formal para `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN` da modelagem canônica

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
divergência material — bloqueia `PASS` até decisão de Davi (`HUMAN_DECISION_REQUIRED`). Davi
aprovou o binding formal.

**Correção desta revisão:** a primeira versão desta decisão afirmava que "todo artefato produzido
por `AC-NNN`/`SEM-NNN`/`SYN-NNN` é Markdown", generalizando `documentation_change` para toda a
fase, inclusive `AC-000`. Achado do `REVIEWER` (`FAIL`, severidade MEDIUM): o critério de DONE de
`AC-000` exige `schemas/*.json` e três scripts `.mjs`, confirmados no commit `2bf9214` — uma
classe de operação heterogênea, não só documental. A generalização estava errada; corrigida
abaixo, delimitando o binding às tarefas cujas alterações são exclusivamente documentais.

## Decisão

As tarefas `AC-001` a `AC-029`, `SEM-NNN` e `SYN-NNN` da fase de modelagem canônica
(`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`, "procedimento repetível" e síntese
final — seção 10.0 em diante) usam o seguinte `runbook_binding` formal:

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

### `AC-000` está fora do escopo desta decisão

`AC-000` (bootstrap) produziu `schemas/*.json` e os três scripts `.mjs` (`validar.mjs`,
`verificar_referencias.mjs`, `verificar_repositorio.mjs`) — confirmado no commit `2bf9214` — uma
classe de operação heterogênea (`code_change` + `documentation_change`), não só
`documentation_change`. `AC-000` já foi concluído, revisado (`PASS`) e commitado antes desta
decisão, sob o fluxo geral de `CLAUDE.md`/`AGENTS.md` sem binding formal; esta decisão não o
reclassifica retroativamente.

### Por que `AC-001` a `AC-029`/`SEM-NNN`/`SYN-NNN` são puramente `documentation_change`

O "procedimento repetível" do plano (a partir de `AC-001`) não cria nem altera `schemas/*.json`
nem `*.mjs` — schemas e scripts ficam congelados a partir de `AC-000`; cada turno só produz
Markdown com blocos JSON validados por eles, sob `docs/modelagem/**`. O mesmo vale para a síntese
final (`AC-029`, `SEM-NNN`, `SYN-NNN`): consolidação e reconciliação, sempre em Markdown/JSON de
conteúdo, nunca em schema ou script.

Se uma tarefa futura desta fase voltar a alterar `schemas/*.json` ou `*.mjs` (por exemplo, uma
correção de ferramental descoberta durante o processamento de uma fonte), ela sai do escopo deste
binding e exige `operation_classes` adicionais (`code_change` → `RB-EXEC-001`/`RB-REV-001`), a
declarar em decisão própria — não coberto por esta decisão.

### Justificativa da inclusão de `RB-REV-004`

`runbooks/README.md` exige `RB-REV-004-evidence-review.md` adicionalmente quando "a suficiência da
evidência for material para os critérios de aceite ou para a revisão independente". Nesta fase,
isso já se mostrou empiricamente verdadeiro em `AC-001`: várias rodadas de revisão adversarial
identificaram problemas de suficiência/precisão de evidência (abas/linhas não lidas, localização
incorreta de fragmento, classificação incorreta de dado sensível) — não defeitos de sintaxe ou
formatação, mas exatamente o tipo de achado que `RB-REV-004` existe para cobrir. A inclusão é
permanente para `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN`, não caso a caso por tarefa.

## Consequência

- O Executor carrega, a partir desta decisão, exatamente os runbooks listados acima em todo turno
  `AC-001`–`AC-029`/`SEM-NNN`/`SYN-NNN`, além de `AGENT_POLICY.md`/`CLAUDE.md` e da normativa de
  `docs/modelagem/`. `AC-000` não é afetado — já concluído.
- O Reviewer carrega os runbooks `shared`/`reviewer` acima em toda revisão de `AC-001` em diante
  nesta fase, além de `AGENT_POLICY.md`/`AGENTS.md`.
- Handoffs de tarefas desta fase devem citar este binding (por número de decisão ou pelo bloco
  JSON acima) para que a vinculação seja verificável no repositório, não apenas declarada em
  prosa.
- Se uma tarefa futura alterar `schemas/*.json` ou `*.mjs`, o binding desta decisão não se aplica
  a ela sem extensão explícita — ver seção acima.
- Esta decisão não altera `runbooks/README.md` nem os runbooks especializados — apenas registra a
  seleção concreta já prevista pelo mecanismo do catálogo para esta fase.
