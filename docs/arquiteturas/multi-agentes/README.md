# Arquitetura multiagente — índice de autoridade

## Canônicos ativos

1. `main/Human-Governed Dual-Agent SDLC Architecture.md`
2. `planner/planner-v1-especificacao-conceitual-fechada.md`
3. `revisor/executor-v1-especificacao-formal.md`
4. `executor/task_atomics.md`

Os contratos executáveis correspondentes vivem em `.ai/control/`.

## Regra de autoridade

Documentos deste diretório explicam o sistema; não redefinem enums, paths ou schemas de `.ai/control`.

Conteúdos em `pipeline/`, `runbooks/`, `skills/`, `containers/` e relatórios históricos podem registrar análises, alternativas e estados anteriores. Quando divergirem do control plane atual, são **reference/historical**, não fonte operacional.

Contradição material em um documento marcado canônico deve bloquear o fluxo e gerar reconciliação humana.
