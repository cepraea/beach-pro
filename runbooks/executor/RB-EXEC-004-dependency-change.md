# RB-EXEC-004 — Alteração de dependência

## Objetivo

Definir o procedimento especializado para inclusão, remoção, atualização de dependências e
alteração de lockfiles no CEPRAEA BEACH PRO.

## Aplicabilidade

Usar este runbook quando a tarefa envolver:

- inclusão de nova dependência
- remoção de dependência existente
- atualização de versão de dependência
- alteração deliberada de lockfile

## Entradas

- Tarefa autorizada com a dependência e justificativa identificadas
- Branch dedicada diferente de `main` e `master`

## Fontes de autoridade

- `AGENT_POLICY.md`
- `CLAUDE.md`
- `package.json` e lockfile existentes
- Critérios de aceite da tarefa

## Pré-condições

- Branch correta confirmada
- Necessidade da dependência identificada e comunicada
- Manifests afetados identificados

## Escopo operacional

Alterar exclusivamente os arquivos relacionados à dependência autorizada:

- `package.json`
- lockfile (`package-lock.json` ou equivalente)
- arquivos de configuração que referenciam a dependência, somente quando necessário

## Procedimento

1. Identificar a necessidade da dependência e confirmar que não existe alternativa já disponível.
2. Identificar os manifests afetados (`package.json` e lockfile).
3. Identificar os requisitos de compatibilidade (versões do Node, runtime, outras dependências).
4. Alterar exclusivamente os artefatos relacionados à dependência.
5. Atualizar o lockfile usando a ferramenta canônica (`npm install`, `npm ci` ou equivalente).
6. Executar build, typecheck e testes aplicáveis.
7. Registrar o impacto material quando existir (tamanho do bundle, compatibilidade, licença).

## Pontos de decisão

| Condição | Ação |
|---|---|
| Dependência introduz licença incompatível com o projeto | `BLOCKED`; comunicar a Davi |
| Dependência requer alteração de runtime ou Node version | Comunicar antes de prosseguir |
| Lockfile fora de sincronia após instalação | Investigar causa; não suprimir conflito |
| Dependência de desenvolvimento adicionada em produção | Comunicar e corrigir antes de finalizar |

## Validações

- `npm run build` (ou equivalente) sem erros
- `npm run typecheck` (ou equivalente) sem erros
- Testes aplicáveis passam após a alteração
- `git diff --check` limpo
- Diff do `package.json` e lockfile inspecionados

## Evidências

- Diff do `package.json` e lockfile (`git diff`)
- Resultado do build e testes
- Impacto material registrado quando relevante

## Handoff

Apresentar de forma factual:

- tarefa executada
- dependência adicionada/removida/atualizada
- versão anterior e nova (quando aplicável)
- justificativa
- validações executadas e resultados
- impacto material identificado

Finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.

## Estados de saída

`READY_FOR_REVIEW` — alteração completa, build e testes passando, diff revisável.

`BLOCKED` — qualquer condição impede a conclusão correta.

## Referências

- [`AGENT_POLICY.md`](/AGENT_POLICY.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
