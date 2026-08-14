# DEC-CTR-015 — Dois contextos de Dev Container (Executor / Reviewer)

**Data:** 2026-08-14
**Status da decisão:** PROPOSTA (rebaixado de "RATIFICADA" em 2026-08-14 —
ver nota de evidência abaixo)
**Estado do enforcement referenciado:** IMPLANTADO / EVIDÊNCIA PARCIAL (boundary
técnico, não fluxo dual-agent E2E completo)
**Data de materialização deste registro:** 2026-08-14
**Aprovador:** Davi Sermenho
**Tipo:** governança arquitetural — ratifica enforcement já implantado, sem rebuild

## Nota de evidência (2026-08-14)

Rebaixado de `RATIFICADA` para `PROPOSTA` após revisão independente: não
existe, neste checkout, artefato verificável da aprovação por Davi Sermenho
para esta materialização. O conteúdo normativo (separação em dois contextos
de Dev Container, `E2E-CODEX-BOUNDARY-01 = PASS`) permanece válido e
inalterado; apenas o status de governança reflete a ausência de lastro
auditável no repositório. Promoção de volta a `RATIFICADA` exige um
artefato de aprovação referenciável e verificável no repositório.

## Decisão

Fica formalmente adotada a separação em **dois contextos de Dev Container**:

```text
.devcontainer/devcontainer.json            → CEPRAEA Agent (Claude Code / EXECUTOR)
.devcontainer/reviewer/devcontainer.json   → CEPRAEA Codex Reviewer (Codex / REVIEWER)
```

O contexto Reviewer monta a árvore de trabalho inteira como `readonly`
(`workspaceMount ... type=bind,readonly`) e roda em volume/identidade
próprios (`cepraea-reviewer-codex`), sem compartilhar estado com o Claude.
O contexto Executor mantém o workspace gravável com exceções `readonly`
granulares por caminho protegido.

## Decisão supersedida

```text
ADR-AGENT-003 — "Um Dev Container no MVP"
(.drive/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md,
 Revisão 2, "FINAL PARA ADOÇÃO")

STATUS: SUPERSEDED
superseded_by: DEC-CTR-015
```

`ADR-AGENT-003` decidia um único container para evitar "sincronização e
manutenção desnecessárias" de dois containers, mas já previa a cláusula de
evolução: *"separar ambientes caso risco/compliance justifique"*. A
separação foi implementada mas nunca formalizada como o exercício dessa
cláusula. Este documento fecha essa lacuna sem desmontar nada.

## Motivação técnica observada

- Isolamento mais forte para o Reviewer (workspace inteiro RO) do que um
  único container sem sandbox interno funcional permitiria;
- volumes de estado independentes (`cepraea-agent-*` vs
  `cepraea-reviewer-codex`) reduzem compartilhamento acidental de estado
  entre os contextos;
- `postStartCommand` do Reviewer já verifica formalmente, no próprio
  devcontainer.json, que workspace e `.git` não são graváveis.

## Consequência

Referências à "arquitetura de um container" em `.drive/multi-agentes/**`
(Building Block View, `ADR-AGENT-003`, diagramas de Deployment View) devem
ser lidas como supersedidas por este documento numa eventual Revisão 3.

O contexto/boundary técnico do Reviewer já está construído e possui
evidência registrada como `E2E-CODEX-BOUNDARY-01 = PASS` — isolamento de
identidade, filesystem read-only, ausência de sudo/Docker/credenciais.
**Isso não equivale, por si só, à validação do fluxo dual-agent completo
Claude → Codex → Humano** (produção → revisão independente → aceite
humano → commit). Essa validação de fluxo permanece em aberto e é distinta
da validação de boundary aqui registrada.

**Correção de referência (revisão de 2026-08-14):** a versão anterior deste
documento citava esse item pendente como `CT-17` da Revisão 2. Não existe
`CT-17` — a seção "Container Acceptance Tests" da Revisão 2 de
`Human-Governed Dual-Agent SDLC Architecture.md` define apenas `CT-01` a
`CT-12` (todos sobre comportamento de container BASE/HARDENED), e nenhum
deles cobre o fluxo E2E dual-agent completo. Em vez de citar um
identificador inexistente, este documento registra formalmente o gate novo
abaixo:

```text
GATE-E2E-DUAL-AGENT-01 — validação do fluxo dual-agent completo
  Escopo: Claude produz → Codex revisa de forma independente → Davi aceita
  → Davi commita.
  Critério de PASS: ao menos uma execução real ponta a ponta, com
  evidência de cada etapa, registrada em decisão própria quando ocorrer.
  Status em 2026-08-14: PENDENTE — nenhuma execução completa registrada
  até esta data.
```

## Referências

- `.devcontainer/reviewer/devcontainer.json` (inspecionado em 2026-08-14).
- `.drive/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md`,
  `ADR-AGENT-003`, seção "Container Acceptance Tests" (`CT-01`–`CT-12`;
  nenhum cobre o fluxo E2E dual-agent — ver `GATE-E2E-DUAL-AGENT-01` acima,
  registrado por este documento).
- `.drive/multi-agentes/CONTAINER-RUNBOOK-v0.3.md`, `AGT-02`,
  `E2E-CODEX-BOUNDARY-01`.
