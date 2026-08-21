# RB-SHARED-002 — Evidências materiais

## Objetivo

Definir evidência suficiente, observável e não simulada para claims materiais.

## Autoridade

- `AGENT_POLICY.md` — seção "Evidência e claims";
- TaskProposal aprovado;
- `.ai/control/execution-result.schema.json`.

## Regras

1. `NO EVIDENCE → NO PASS`.
2. Evidência deve referenciar Action e AC.
3. Evidência simulada é inválida.
4. Comando material registra comando, exit code e instante.
5. Diff prova mudança, não correção.
6. Contradição entre evidências deve ser preservada e reportada.
7. Evidência não autoriza decisão humana.

## Mínimo antes de READY_FOR_REVIEW

- cada Action `PASS` possui `evidence_refs`;
- cada AC requerido pela DoD possui evidência `PASS`;
- mandatory checks possuem resultado;
- `git diff --check`, diff e status foram inspecionados;
- `unauthorized_changes=[]`.

A persistência material é `.ai/tasks/<TASK-ID>/execution-result.json`; não criar logs narrativos obrigatórios paralelos ao Git.

## Reviewer

Reviewer usa a evidência do Executor como entrada, mas tenta refutá-la independentemente. Insuficiência material impede `PASS`.
