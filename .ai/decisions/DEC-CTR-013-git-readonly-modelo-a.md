# DEC-CTR-013 — `.git` somente leitura nos containers de agentes (Modelo A)

**Data:** 2026-08-14
**Status da decisão:** PROPOSTA (rebaixado de "RATIFICADA" em 2026-08-14 —
ver nota de evidência abaixo)
**Estado do enforcement referenciado:** IMPLANTADO / VALIDADO
**Data de materialização deste registro:** 2026-08-14
**Aprovador:** Davi Sermenho
**Tipo:** governança arquitetural — materializa em `.ai/decisions/` uma decisão
canônica que já constava implantada e validada em
`CONTAINER-RUNBOOK-v0.3.md`; nenhum enforcement é criado por este documento.

## Nota de evidência (2026-08-14)

Rebaixado de `RATIFICADA` para `PROPOSTA` após revisão independente: não
existe, neste checkout, artefato verificável da aprovação por Davi Sermenho
para esta materialização. O conteúdo normativo (enforcement técnico já
implantado e confirmado via `findmnt`) permanece válido e inalterado;
apenas o status de governança reflete a ausência de lastro auditável no
repositório. Promoção de volta a `RATIFICADA` exige um artefato de
aprovação referenciável e verificável no repositório.

## Decisão

Fica formalmente adotado o **Modelo A — Git humano**, já implantado e validado
operacionalmente conforme `CONTAINER-RUNBOOK-v0.3.md` (`DEC-CTR-013`):

- `.git` é montado **read-only** dentro dos containers de agentes
  (`.devcontainer/devcontainer.json`, `.devcontainer/reviewer/devcontainer.json`);
- agentes (Claude Code, Codex) nunca alteram index, refs ou histórico;
- `git add`, `commit`, `push`, `pull`, `merge`, `rebase`, `checkout`, `switch`,
  `restore`, `reset`, `worktree`, `stash` e operações equivalentes que alterem
  refs/index/histórico pertencem exclusivamente a Davi;
- Git privilegiado ocorre **fora** dos containers de agentes.

## Decisão supersedida

```text
ADR-CONTAINER-001 — ".git RW no Container"
(.drive/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md,
 Revisão 2, "FINAL PARA ADOÇÃO")

STATUS: SUPERSEDED
superseded_by: DEC-CTR-013
```

`ADR-CONTAINER-001` decidia o oposto — `.git` gravável no container para uso
via VS Code Source Control — e define `CT-02` como acceptance test
obrigatório do perfil BASE nesse sentido. Essa premissa está tecnicamente
superada: o mount `.git` já está implantado como `readonly`, confirmado em
runtime via `findmnt`:

```text
/workspaces/cepraea-beach-pro/.git  ro,relatime,discard,errors=remount-ro,data=ordered
```

## Consequência sobre `CT-02`

`CT-02` da Revisão 2 não é mais um teste de aceite válido e deve ser
substituído, não reportado como falha permanente:

```text
CT-02' — Git privilegiado (add/commit/push/merge) é executado por Davi
         FORA dos containers de agentes. `.git` permanece read-only e
         intacto (HEAD inalterado) durante toda sessão de Claude/Codex
         dentro do container.
```

## Referências

- `.drive/multi-agentes/CONTAINER-RUNBOOK-v0.3.md`, §7 `DEC-CTR-013`,
  §8 `CTL-05`, §12 `TST-CTL-001`.
- `.drive/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md`,
  Constraint #7, `ADR-CONTAINER-001`, Scenario 5, `QS-004`.
- `.devcontainer/devcontainer.json` (mount `.git` readonly, confirmado em
  runtime 2026-08-14).

## Nada de enforcement muda

Este documento não altera `.devcontainer/**`, managed settings, guards ou
qualquer configuração ativa. Apenas materializa em `.ai/decisions/` uma
decisão que já estava implantada e validada.
