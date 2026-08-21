# Matriz de Arquitetura de Skills por Papel

sem transformar Skills em uma segunda camada de governança.

A regra estrutural deve ser:

**Autoridade humana → `AGENT_POLICY.md` → fontes/decisões canônicas → `CLAUDE.md` ou `AGENTS.md` → `runbook_binding`/Runbooks → Skill especializada → execução/revisão → enforcement/evidência.**

A Skill não deve ganhar autoridade própria. Isso preserva a precedência já definida pelos runbooks e a decisão da matriz técnica de tirar procedimentos especializados do contexto permanente dos agentes.

## 1. Claude Code — EXECUTOR

| Nome | Objetivo | Gatilho | Entradas | Saídas | Fontes obrigatórias | Runbook relacionado | Permissões | Proibições | Prioridade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **`prepare-task-proposal`** | Produzir o contrato executável da tarefa antes da implementação  | `task_atomics.md` exige `task_proposal` completo; ou tarefa humana exige plano formal | instrução original; estado do repo; risco; fontes normativas; decisões; catálogo de runbooks | `.ai/tasks/<TASK-ID>.json` válido; resultado do validator; handoff `PLAN`| `AGENT_POLICY.md`; `CLAUDE.md`; `task_atomics.md`; schema; `runbooks/README.md`; decisões/fontes citadas | **Pré-runbook**: consulta `runbooks/README.md` para construir `runbook_binding` | Ler repo/fontes; Git somente inspeção; escrever **somente** contrato autorizado; executar validator  | Não implementar; não inventar requisito; não esconder decisão humana pendente; não alterar `.ai/control/**`; não mutar Git | **P0 — criar agora** |
| **`supabase`** *(oficial)* | Fornecer conhecimento atualizado sobre Supabase, Auth, RLS, Data API, CLI etc. | Qualquer tarefa material envolvendo Supabase | task aprovada; configuração local; código/schema relevante; documentação atual| orientação técnica aplicada à tarefa; verificações pertinentes                  | Fontes CEPRAEA acima da Skill + Skill oficial + docs atuais Supabase | `RB-EXEC-001`, `002` ou `004`, conforme `operation_class` | Apenas as permissões concedidas pela tarefa/runbook | Não criar MCP/configuração por conta própria; não obter credenciais; não usar produção; não sobrepor policy CEPRAEA  | **P0 — adotar externa** |
| **`supabase-postgres-best-practices`** *(oficial)* | Fornecer heurísticas especializadas de PostgreSQL: schema, SQL, índices, RLS, locks, performance | Qualquer alteração que viva no PostgreSQL ou diagnóstico SQL                          | schema; SQL; migrations; policies; planos `EXPLAIN`; contexto da tarefa                      | recomendações técnicas aplicáveis e verificáveis                                | Skill oficial; referências específicas; docs PostgreSQL/Supabase; normativa CEPRAEA                      | Principalmente `RB-EXEC-002`                                                    | Ler referências sob demanda; aplicar somente dentro dos targets autorizados                          | Não converter heurística em requisito; não criar índice sem evidência; não tratar ganhos de performance como garantidos           | **P0 — adotar externa**                         |
| **`supabase-migration`**                           | Executar o workflow **específico do CEPRAEA** para evolução de banco                             | Tarefa aprovada com `database_change` envolvendo migration/schema                     | task aprovada; modelo lógico; migrations atuais; schema; constraints; skills Supabase        | nova migration; artefatos auxiliares autorizados; validação; evidência          | `AGENT_POLICY`; `CLAUDE`; task; `RB-EXEC-002`; modelo canônico/lógico; skills oficiais Supabase          | **`RB-EXEC-002`**                                                               | Escrever migrations/arquivos explicitamente target; executar ambiente sintético e checks autorizados | Não modificar migration histórica; não usar dados reais; não resolver ambiguidade de domínio; não fazer operação Git privilegiada | **P0/P1 — antes da próxima migration material** |
| **`database-testing`**                             | Converter invariantes, ACs, constraints e regras de acesso em testes independentes de banco      | Alteração de schema, constraint, RLS ou comportamento persistente                     | task aprovada; migration/schema; matriz de atores; regras; ACs                               | testes positivos/negativos; testes de constraints/RLS; resultados reproduzíveis | task; modelo; `RB-EXEC-002`; fontes Supabase/Postgres; normas de teste do projeto                        | `RB-EXEC-002`; também `RB-EXEC-001` se houver harness em código                 | Criar somente testes autorizados; executar DB sintético; produzir evidência                          | Não usar produção; não enfraquecer implementação para fazer teste passar; não copiar literalmente a implementação como oráculo    | **P0 — antes da comprovação Auth/RLS**          |
| **`model-domain-types`**                           | Traduzir semântica canônica já aprovada para tipos TypeScript                                    | Tarefa `code_change` que materialize conceitos/estados do domínio em TS               | modelo canônico/lógico; task; tipos existentes; contratos                                    | tipos; unions; guards/mapeamentos; testes pertinentes                           | modelo canônico; decisões; task; fontes TypeScript da matriz técnica                                     | **`RB-EXEC-001`**                                                               | Alterar targets TS/testes autorizados; usar LSP; typecheck                                           | Não inventar estado/regra; não colapsar distinções do domínio; não alterar modelo canônico para acomodar código                   | **P1**                                          |
| **`react-feature`**                                | Implementar comportamento React seguindo arquitetura e contratos já aprovados                    | `code_change` React/UI com runtime materializado                                      | task; tipos de domínio; AC/BDD; componentes existentes; padrões do projeto                   | componentes/hooks; testes; validações frontend                                  | task; `RB-EXEC-001`; React/TS/Vite oficiais da matriz; arquitetura frontend                              | **`RB-EXEC-001`**                                                               | Alterar frontend/testes target; LSP; lint/typecheck/test/build permitidos                            | Não mover regra crítica para UI; não expor segredo; não ampliar feature; não usar estado/effect como substituto de modelagem      | **P1 — quando runtime estiver materializado**   |
| **`cepraea-documentation`**                        | Produzir documentação baseada em fontes e separando fato, decisão e inferência                   | `documentation_change`                                                                | task; fontes normativas; código/modelos relevantes; documento atual                          | Markdown revisável; referências; validações documentais                         | `AGENT_POLICY`; task; `RB-EXEC-003`; guia de estilo; fontes técnicas/normativas                          | **`RB-EXEC-003`**                                                               | Alterar somente documentos target; validar links/markdown                                            | Não inventar afirmação; não alterar decisão existente; não criar governança paralela; não modificar control plane incidentalmente | **P1**                                          |
| **`run-quality-gates`**                            | Orquestrar gates **já existentes**, não inventá-los                                              | Implementação concluída e `mandatory_checks` exigem pipeline recorrente               | task; checks obrigatórios; scripts executáveis existentes                                    | resultados/exit codes/evidência consolidados   | task; scripts reais; runbooks aplicáveis; `RB-SHARED-002/003` | Todos os runbooks do binding + shared | Executar exclusivamente checks existentes | Não fabricar gate inexistente; não declarar sucesso de check não executado; não fazer `--fix` fora da autoridade | **P1/FUTURO — somente após gate executável** |

O `Task Contract` já está formalmente incorporado no control plane: para tarefas que exigem contrato completo, Claude cria `.ai/tasks/<TASK-ID>.json`, valida contra o schema, entrega `PLAN` e não implementa até o `PASS` do Reviewer. Isso torna `prepare-task-proposal` uma **refatoração natural de procedimento atualmente residente em `CLAUDE.md`**, e não uma nova regra.

As duas Skills da Supabase permanecem subordinadas ao CEPRAEA. A `supabase` cobre explicitamente Auth, RLS, migrations, Data API, CLI, segurança etc.; `supabase-postgres-best-practices` cobre schema, migrations, RLS, SQL, índices, locks e performance.

---

# 2. Codex — REVIEWER independente

Aqui a semântica muda. As Skills devem otimizar **refutação**, não produção.

| Nome                                                               | Objetivo                                                                                             | Gatilho                                                                           | Entradas                                                                                      | Saídas                                                                         | Fontes obrigatórias                                                                          | Runbook relacionado                                                                  | Permissões                                                                                 | Proibições                                                                                                                                                        | Prioridade                             |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **`review-task-proposal`**                                         | Tentar provar que o contrato proposto é insuficiente, inconsistente ou contém decisão não autorizada | Etapa `PLAN` com `task_proposal` obrigatório                                      | task JSON; instrução original; schema; `task_atomics`; fontes; decisões; catálogo de runbooks | validações; findings; insumos para `PASS` / `FAIL` / `HUMAN_DECISION_REQUIRED` | `AGENT_POLICY`; `AGENTS`; `task_atomics`; schema; `runbooks/README`; fontes/decisões citadas | Runbooks **Reviewer propostos no binding**, conforme necessário para avaliar o plano | Somente leitura; validator; Git inspection; `/tmp` quando necessário                       | Não corrigir contrato; não escrever plano; não inventar decisão; não exigir diff na porta PLAN; não mutar Git                                                     | **P0 — criar agora**                   |
| **`supabase`** *(oficial, knowledge-only)*                         | Fornecer ao Reviewer fatos/armadilhas atuais de Supabase para confrontar a implementação             | Review envolvendo Supabase/Auth/RLS/Data API/client                               | task aprovada; diff; schema/policies; evidência                                               | hipóteses de refutação e checks técnicos                                       | fontes CEPRAEA + Skill Supabase + docs atuais                                                | `RB-REV-001`, `002` ou `005` conforme classe                                         | Consultar conhecimento; executar checks read-only autorizados                              | Não seguir passos de implementação da Skill; não editar config/MCP; não corrigir finding; não acessar produção                                                    | **P0 — compartilhada**                 |
| **`supabase-postgres-best-practices`** *(oficial, knowledge-only)* | Ampliar conhecimento PostgreSQL usado para procurar defeitos                                         | Migration/schema/query/RLS/performance em review                                  | diff; schema; SQL; migrations; evidência                                                      | hipóteses adversariais; problemas de schema/query/security                     | fontes CEPRAEA + Skill/referências PostgreSQL                                                | **`RB-REV-002`** principalmente                                                      | Leitura; análise; checks independentes permitidos                                          | Não aplicar “best practice” como lei; não recomendar mudança sem demonstrar problema; não editar SQL                                                              | **P0 — compartilhada**                 |
| **`review-domain-traceability`**                                   | Demonstrar ou refutar a cadeia requisito → regra → modelo → implementação → teste                    | Semântica de domínio/material; business rule; dados; mudança documental normativa | task; normative sources; decisões; modelo; diff; testes/evidência                             | mapa de rastreabilidade; gaps; overclaims; findings                            | fontes citadas na task; modelo canônico; decisões; `AGENT_POLICY`                            | `RB-REV-001/002/003`; `RB-REV-004` quando evidência for material                     | Leitura ampla das fontes necessárias; validators/read-only checks                          | Não preencher lacuna semântica; não escolher regra preferida; não alterar fonte/modelo                                                                            | **P1**                                 |
| **`review-rls-security`**                                          | Tentar quebrar autorização e isolamento de dados de forma sistemática                                | `risk.natures` inclui `rls` ou alteração material de Auth/acesso a dados          | task; atores; policies; GRANTs; migrations; schema; testes do Executor                        | matriz ator × operação; negative/positive checks; findings de autorização      | task/modelo; `RB-REV-002`; `RB-REV-004` quando material; Skills oficiais Supabase            | **`RB-REV-002` + `RB-REV-004` quando aplicável**                                     | Read-only; executar checks contra ambiente sintético autorizado; saídas efêmeras em `/tmp` | Não corrigir policy; não elevar privilégio; não acessar dados reais; não considerar `authenticated` sinônimo de autorizado; não confiar só nos testes do Executor | **P0 — antes da comprovação Auth/RLS** |
| **`review-test-adequacy`**                                         | Verificar se os testes realmente provam os critérios, regras e negative cases                        | Comportamento novo/material ou evidência baseada em testes                        | task aprovada; ACs; BDD; testes; diff; resultados                                             | lacunas de oráculo/cobertura; falsos positivos; findings                       | task; business rules; AC/BDD; runbook especializado; `RB-REV-004` quando material            | `RB-REV-001/002` + eventualmente `RB-REV-004`                                        | Ler/reexecutar testes sem alteração persistente                                            | Não escrever teste; não mudar implementação; não considerar “suite verde” prova suficiente; não derivar o oráculo do código sob teste                             | **P1**                                 |
| **`review-react-change`**                                          | Procurar regressões e problemas semânticos específicos de React/TypeScript                           | Review `code_change` React após runtime estar operacional                         | task; diff; componentes; tipos; testes; diagnostics LSP                                       | findings de estado, effects, contratos, tipos, regressão                       | task; `RB-REV-001`; React/TS/Vite oficiais; arquitetura frontend                             | **`RB-REV-001`**                                                                     | Read-only; LSP; typecheck/lint/test sem fix                                                | Não refatorar; não sugerir preferência estética como bug; não aplicar patch; não expandir review para reescrita da feature                                        | **P1 — quando runtime existir**        |

O `AGENTS.md` atual já distingue explicitamente `PLAN` de `IMPLEMENTATION`, proíbe edição/patch/Git mutável e exige que Codex procure regressões, **tente refutar conclusões**, confronte evidências e detecte decisões humanas simuladas. Portanto, essas Skills devem aprofundar essa postura, não criar um segundo Reviewer.

---

# 3. O que deliberadamente **não** vira Skill

Essa parte é tão importante quanto a matriz positiva.

| Capacidade                        | Decisão definitiva | Motivo                                                                                                               |
| --------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `inspect-repository`              | **NÃO CRIAR**      | Baseline + Git inspection já pertencem a policy/runbooks/guards                                                      |
| `produce-evidence`                | **NÃO CRIAR**      | `RB-SHARED-002/003` já governam evidência/handoff                                                                    |
| `review-code` genérica            | **NÃO CRIAR**      | `RB-REV-001` já é procedimento especializado de code review                                                          |
| `review-database-change` genérica | **NÃO CRIAR**      | `RB-REV-002` já cobre migration/schema/integridade/adversarial testing                                               |
| `review-documentation` genérica   | **NÃO CRIAR**      | `RB-REV-003` já verifica fontes, significado, claims, estilo, links e comandos                                       |
| `review-evidence`                 | **NÃO CRIAR**      | `RB-REV-004` já existe como runbook complementar                                                                     |
| `review-dependency-risk` genérica | **NÃO CRIAR**      | `RB-REV-005` já é bastante especializado: manifest, lockfile, transitivas, runtime, licença e checks independentes   |
| `design-rls` Executor             | **CANDIDATE**      | Primeiro usar `supabase` + `postgres-best-practices` + `RB-EXEC-002`; criar só se aparecer lacuna CEPRAEA recorrente |
| `offline-storage`                 | **BLOCKED**        | Não criar enquanto a arquitetura offline permanecer divergente                                                       |
| `offline-sync`                    | **BLOCKED**        | Idem                                                                                                                 |
| `run-quality-gates`               | **FUTURO**         | Skill só deve orquestrar gate executável real; não criar gate por prompt                                             |

O catálogo atual de runbooks já possui exatamente quatro classes de operação — `code_change`, `database_change`, `documentation_change`, `dependency_change` — e exige seleção exclusiva pelo `runbook_binding`. Isso é justamente o que impede a proliferação de Skills genéricas concorrentes.

---

# 4. Relação Executor ↔ Reviewer

A matriz definitiva dos pares fica:

| Domínio              | Claude Executor                        | Codex Reviewer                                     |
| -------------------- | -------------------------------------- | -------------------------------------------------- |
| Contrato da tarefa   | **`prepare-task-proposal`**            | **`review-task-proposal`**                         |
| Supabase geral       | **`supabase`**                         | **`supabase` — knowledge-only**                    |
| PostgreSQL           | **`supabase-postgres-best-practices`** | **mesma Skill — knowledge-only**                   |
| Migration            | **`supabase-migration`**               | `RB-REV-002` + conhecimento PostgreSQL             |
| Teste DB             | **`database-testing`**                 | **`review-test-adequacy`** + `review-rls-security` |
| RLS                  | Skills oficiais + `supabase-migration` | **`review-rls-security`**                          |
| Domínio → TypeScript | **`model-domain-types`**               | **`review-domain-traceability`**                   |
| React                | **`react-feature`**                    | **`review-react-change`**                          |
| Documentação         | **`cepraea-documentation`**            | `RB-REV-003`                                       |
| Evidência            | Runbooks shared                        | `RB-REV-004`                                       |
| Dependências         | `RB-EXEC-004`                          | `RB-REV-005`                                       |
| Quality gates        | **`run-quality-gates` futuro**         | reexecução independente pelos runbooks             |

Esse desenho produz a assimetria desejada:

**Claude:** `especificar → construir → testar → demonstrar`

**Codex:** `validar contrato → desconfiar → refutar → reproduzir → classificar finding`

---

## 5. Conjunto-alvo final

Eu fecharia a arquitetura inicialmente assim:

```text
CLAUDE — EXECUTOR
│
├── P0
│   ├── prepare-task-proposal              [custom CEPRAEA]
│   ├── supabase                           [oficial]
│   ├── supabase-postgres-best-practices   [oficial]
│   └── database-testing                   [custom CEPRAEA]
│
├── P0/P1
│   └── supabase-migration                 [custom CEPRAEA]
│
├── P1
│   ├── model-domain-types                 [custom CEPRAEA]
│   ├── react-feature                      [custom CEPRAEA]
│   └── cepraea-documentation              [custom CEPRAEA]
│
└── FUTURO
    └── run-quality-gates


CODEX — REVIEWER
│
├── P0
│   ├── review-task-proposal               [custom CEPRAEA]
│   ├── supabase                           [oficial / knowledge-only]
│   ├── supabase-postgres-best-practices   [oficial / knowledge-only]
│   └── review-rls-security                [custom CEPRAEA]
│
└── P1
    ├── review-domain-traceability          [custom CEPRAEA]
    ├── review-test-adequacy                [custom CEPRAEA]
    └── review-react-change                 [custom CEPRAEA]
```

Há ainda uma implicação operacional importante: `.claude/**` e `.codex/**` estão atualmente classificados como **plano de controle protegido**. Portanto, esta matriz pode ser adotada como arquitetura, mas a criação material dessas Skills deve ocorrer em uma **tarefa humana explicitamente autorizada para modificar o control plane**, e não incidentalmente durante uma tarefa de produto.

E manteria a fronteira sintética como requisito transversal das Skills de banco e segurança: o `README.md` atual determina exclusivamente dados sintéticos, sem migração real/piloto/produção, e proíbe conectar o repositório a projeto com dados reais.

Essa, para mim, é a **matriz definitiva v1**: pequena o suficiente para ser governável, assimétrica por papel e sem duplicar o que policy, runbooks e enforcement já resolvem.
