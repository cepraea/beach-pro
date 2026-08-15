# Runbook do operador — Fluxo multiagente

## Objetivo

Orientar Davi na condução do ciclo completo de uma ACTION no fluxo
Human-Governed Dual-Agent SDLC.

## Fluxo

```text
Confirmar branch
        ↓
Selecionar uma ACTION
        ↓
Solicitar execução ao Claude
        ↓
Claude retorna READY_FOR_REVIEW
        ↓
Solicitar revisão do git diff ao Codex
        ↓
           ┌──────────────────┬───────────────────────────┐
         FAIL          HUMAN_DECISION_REQUIRED           PASS
           │                  │                           │
           ▼                  ▼                           ▼
  Encaminhar findings   Decidir e registrar       Revisar o diff
  aplicáveis ao Claude  decisão material          Executar Git
           │            quando necessária         privilegiado
           ▼                  │                           │
  Claude corrige              ▼                           ▼
           │             Claude retoma             Próxima ACTION
           ▼
  Novo review Codex
```

## Procedimento

1. Confirmar a branch autorizada para a ACTION (deve ser diferente de `main` e `master`).
2. Selecionar exclusivamente **uma** ACTION para execução — não iniciar a próxima antes de
   concluir a anterior.
3. Solicitar ao Claude a execução dessa ACTION, informando o escopo e os critérios de aceite.
4. Aguardar `READY_FOR_REVIEW` do Claude. Não prosseguir se receber `BLOCKED`.
5. Solicitar ao Codex a revisão do `git diff` produzido pelo Claude.
6. Processar o verdict do Codex:
   - `FAIL` → encaminhar os findings aplicáveis ao Claude para correção; solicitar novo review.
   - `HUMAN_DECISION_REQUIRED` → exercer a decisão humana; registrar a decisão como DEC-NNN
     quando for material; comunicar ao Claude para retomar.
   - `PASS` → revisar o diff; executar Git privilegiado (`git add`, `git commit`).
7. Iniciar a próxima ACTION somente após concluir a anterior com commit.

## Convenção de mensagem de commit

```text
AC-NNN: descrição da action
SEM-NNN: descrição da sintetização semântica
SYN-NNN: descrição da sintetização
```

Git é a state machine operacional. O commit é o registro formal da conclusão de cada ACTION.

## Regras

- Davi controla Git privilegiado: `git add`, `git commit`, `git push`, `git merge`.
- Um agente escritor por branch. Claude não avança automaticamente para a próxima ACTION.
- `PASS` do Codex não produz commit automaticamente. Davi revisa e comita.
- Para decisão material sem precedente, registrar em
  `docs/modelagem/decisoes/registro_decisoes.md`.

## Quando acionar ChatGPT ou Gemini

- Divergência material entre Claude e Codex.
- Decisão arquitetural sem precedente.
- Necessidade de terceira opinião independente.

Eles não adquirem autoridade de aprovação.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`CLAUDE.md`](../..../../CLAUDE.md)
- [`AGENTS.md`](../../../AGENTS.md)
- [`runbooks/README.md`](../../runbooks/README.md)
- [`docs/modelagem/decisoes/registro_decisoes.md`](../modelagem/decisoes/registro_decisoes.md)
