# Inventário do repositório (manifest)

> **Fonte estruturada autoritativa:** [`manifest.json`](./manifest.json).
> Este arquivo é uma visão humana derivada; não deve ser editado independentemente.

Projeto: **CEPRAEA BEACH PRO**
Versão do inventário: **0.2.0**
Atualizado em: **2026-08-21**

| Path | Tipo | Status | Consumidores | Propósito |
| --- | --- | --- | --- | --- |
| `AGENT_POLICY.md` | governance | active | human, agent:planner, agent:executor, agent:reviewer | Política comum canônica: autoridade, namespaces .ai, lifecycle PLAN/APPROVAL/EXECUTION/REVIEW, estados, evidência e modos. |
| `CLAUDE.md` | governance | active | human, agent:planner, agent:executor | Adaptador operacional do Claude nas fases PLANNER e EXECUTOR. |
| `AGENTS.md` | governance | active | human, agent:reviewer | Adaptador do Codex Reviewer para PLAN e IMPLEMENTATION review. |
| `README.md` | governance | active | human | Apresentação e estado do produto; autorização de produção do produto é separada do control plane. |
| `runbooks/README.md` | runbook | active | human, agent:planner, agent:executor, agent:reviewer | Entrada da biblioteca; paths normativos são resolvidos por .ai/control/runbook-catalog.json. |
| `runbooks/shared/` | runbook | active | agent:planner, agent:executor, agent:reviewer | Runbooks compartilhados de baseline, evidência e estados. |
| `runbooks/executor/` | runbook | active | agent:executor | Runbooks especializados do Executor. |
| `runbooks/reviewer/` | runbook | active | agent:reviewer | Runbooks especializados do Reviewer. |
| `docs/arquiteturas/multi-agentes/main/Human-Governed Dual-Agent SDLC Architecture.md` | architecture | active | human, agent:planner, agent:executor, agent:reviewer | Arquitetura canônica explicativa do SDLC agentivo. |
| `docs/arquiteturas/multi-agentes/planner/planner-v1-especificacao-conceitual-fechada.md` | architecture | active | human, agent:planner, agent:reviewer | Especificação do Planner alinhada a .ai/control e .ai/tasks. |
| `docs/arquiteturas/multi-agentes/revisor/executor-v1-especificacao-formal.md` | architecture | active | human, agent:executor, agent:reviewer | Especificação do Executor: proposal aprovado + approval + RuntimeAnchor → ExecutionResult. |
| `docs/arquiteturas/multi-agentes/executor/task_atomics.md` | architecture | active | human, agent:planner, agent:executor, agent:reviewer | Padrão de TASK atômica alinhado ao Task Proposal v3. |
| `docs/arquiteturas/multi-agentes/README.md` | architecture | active | human, agent:planner, agent:executor, agent:reviewer | Índice de autoridade dos documentos multiagente; separa canônicos de reference/historical. |
| `docs/arquiteturas/multi-agentes/` | architecture | reference | human | Demais análises e materiais de arquitetura; não redefinem contratos executáveis de .ai/control. |
| `docs/linters/guia_estilo_documentação.md` | standard | active | human, agent:executor, agent:reviewer | Guia canônico de documentação Markdown. |
| `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` | domain_model | active | human, agent:executor, agent:reviewer | Plano canônico normativo da modelagem. |
| `docs/modelagem/README.md` | domain_model | active | human, agent:executor | Ponto de entrada operacional da modelagem. |
| `docs/modelagem/dominio/` | domain_model | stub | human, agent:executor, agent:reviewer | Elementos promovidos do Modelo Canônico. |
| `docs/modelagem/candidatos/` | domain_model | in_progress | agent:executor, agent:reviewer | Hipóteses estruturais não promovidas. |
| `docs/modelagem/conhecimento/` | domain_model | active | human, agent:executor, agent:reviewer | Glossário e regras extraídas com rastreabilidade. |
| `docs/modelagem/decisoes/registro_decisoes.md` | domain_model | active | human, agent:executor, agent:reviewer | Registro formal de decisões da modelagem. |
| `docs/modelagem/evidencias/registro_evidencias.md` | domain_model | active | agent:executor, agent:reviewer | Registro de evidências da modelagem. |
| `docs/modelagem/fontes/` | domain_model | active | human, agent:executor | Inventário e dossiês de fontes. |
| `docs/modelagem/logico/` | domain_model | stub | agent:executor, agent:reviewer | Modelo lógico relacional e áreas pendentes. |
| `docs/modelagem/processo/` | domain_model | active | human, agent:executor, agent:reviewer | Critérios de maturidade e processo. |
| `docs/modelagem/governanca/fields-registry.md` | domain_model | in_progress | human, agent:executor, agent:reviewer | Catálogo semântico dos campos de modelagem. |
| `docs/modelagem/schemas/schema_decisao.json` | schema | active | agent:executor, agent:reviewer, ci-cd | Schema de decisão da modelagem. |
| `docs/modelagem/schemas/schema_elemento_modelo.json` | schema | active | agent:executor, agent:reviewer, ci-cd | Schema de elemento do Modelo Canônico. |
| `docs/modelagem/schemas/schema_evidencia.json` | schema | active | agent:executor, agent:reviewer, ci-cd | Schema de evidência da modelagem. |
| `docs/modelagem/schemas/schema_fonte.json` | schema | active | agent:executor, agent:reviewer, ci-cd | Schema de fonte da modelagem. |
| `docs/modelagem/schemas/schema_regra.json` | schema | active | agent:executor, agent:reviewer, ci-cd | Schema de regra da modelagem. |
| `docs/modelagem/schemas/schema_termo.json` | schema | active | agent:executor, agent:reviewer, ci-cd | Schema de termo da modelagem. |
| `docs/modelagem/schemas/validar.mjs` | script | active | agent:executor, agent:reviewer, ci-cd | Validador determinístico da modelagem. |
| `docs/modelagem/schemas/verificar_referencias.mjs` | script | active | agent:executor, agent:reviewer, ci-cd | Validador de referências cruzadas da modelagem. |
| `docs/modelagem/schemas/verificar_repositorio.mjs` | script | active | agent:executor, agent:reviewer, ci-cd | Validador de action_ref/commits da modelagem. |
| `docs/operacao/agent-workflow.md` | standard | active | human | Runbook humano do ciclo agentivo. |
| `test/fixtures/synthetic/agent-plan-smoke.txt` | fixture | active | ci-cd | Fixture sintética canário. |
| `.ai/control/` | config | active | human, agent:planner, agent:executor, agent:reviewer, ci-cd | Control plane canônico: config, schemas, catálogo, validators, examples e conformance fixtures. |
| `.ai/decisions/` | config | active | human, agent:planner, agent:executor, agent:reviewer | Decisões humanas de arquitetura/governança e índice de status. |
| `.ai/tasks/` | config | active | human, agent:planner, agent:executor, agent:reviewer | Instâncias materiais por TASK: proposal, approval e execution-result. |
| `.devcontainer/` | config | active | human | Sandbox e enforcement do ambiente de agentes. |
| `.codex/config.toml` | config | active | agent:reviewer, human | Política project-level do Codex Reviewer read-only. |
| `.mcp.json` | config | active | human, agent:executor, agent:reviewer | Configuração MCP; nenhum servidor implicitamente autoritativo. |
| `.markdownlint.jsonc` | config | active | agent:executor, agent:reviewer, ci-cd | Regras de lint Markdown. |
| `.github/workflows/validate-control-plane.yml` | ci | active | ci-cd, human | Gate dependency-free do control plane em PR/push. |

## Regra de manutenção

1. Atualize `manifest.json`.
2. Execute `node .ai/control/generate-manifest-md.mjs`.
3. Execute `node .ai/control/validate-control-plane.mjs`.
