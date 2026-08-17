# Matriz Canônica de Fontes Técnicas — CEPRAEA BEACH PRO

> **Status:** Base técnica canônica inicial
> **Escopo:** Claude Code + Codex + VS Code/WSL + Vite + TypeScript + React + Supabase/PostgreSQL + PWA + testes
> **Objetivo:** Definir quais fontes oficiais fundamentam as decisões técnicas do CEPRAEA BEACH PRO, quando cada agente deve consultá-las e onde cada conhecimento deve ser materializado.

---

## 1. Princípio estrutural

A matriz canônica deve impedir que `CLAUDE.md` e `AGENTS.md` se tornem duas especificações concorrentes do mesmo PWA.

`CLAUDE.md` e `AGENTS.md` devem funcionar como adaptadores finos para uma documentação normativa comum. Regras críticas não devem depender apenas de instruções em Markdown: devem ser materializadas por mecanismos executáveis sempre que possível.

Fluxo canônico:

```text
REALIDADE / DECISÃO HUMANA
          ↓
DOCUMENTAÇÃO NORMATIVA DO PROJETO
          ↓
    ┌─────┴─────┐
    │           │
CLAUDE.md    AGENTS.md
    │           │
    └─────┬─────┘
          ↓
        Skills
          ↓
    implementação
          ↓
ENFORCEMENT EXECUTÁVEL
          ↓
       evidência
```

### 1.1 Destinos de materialização

- `C` = `CLAUDE.md`: contexto e instruções persistentes específicas do Claude Code.
- `A` = `AGENTS.md`: contexto e instruções persistentes específicas do Codex.
- `S` = Skill: procedimento reutilizável, carregado quando a classe de tarefa exigir.
- `E` = enforcement executável: TypeScript, SQL, constraints, RLS, testes, scripts, hooks, sandbox, CI etc.

***

# 2. Agentes de desenvolvimento

| ID | Tópico | Fonte oficial — página exata | Decisão arquitetural que fundamenta | Claude deve consultar quando | Codex deve consultar quando | Materialização |
|---|---|---|---|---|---|---|
| **AG-01** | Claude Code no VS Code | Anthropic — **Use Claude Code in VS Code** — https://code.claude.com/docs/en/vs-code | O VS Code é uma superfície do Claude Code; configurações, ferramentas, hooks e permissões não devem ser inventados especificamente para a GUI. | Ao configurar ou depurar operação do Claude dentro do VS Code. | Não é fonte normativa do Codex; consultar apenas ao revisar comportamento específico do Claude. | `C`: registrar que execução ocorre via VS Code/WSL. `S`: não. `E`: configurações versionadas quando cabível. |
| **AG-02** | Funcionamento do agentic loop | Anthropic — **How Claude Code works** — https://code.claude.com/docs/en/how-claude-code-works | O agente trabalha iterativamente com ferramentas e resultados; contexto deve ser controlado. | Ao projetar tarefas, investigação, execução ou troubleshooting. | Somente se estiver avaliando interoperabilidade com Claude. | `C`: regras de contexto. `S`: workflows complexos. `E`: testes independentes da autodeclaração do agente. |
| **AG-03** | `CLAUDE.md` | Anthropic — **How Claude remembers your project** — https://code.claude.com/docs/en/memory | `CLAUDE.md` é contexto, não barreira de segurança. | Em toda sessão do repositório. | Apenas ao verificar simetria das instruções entre agentes. | `C`: arquitetura, comandos, convenções, limites e ponteiros para fontes canônicas. `E`: toda regra crítica mencionada ali. |
| **AG-04** | Estrutura `.claude/` | Anthropic — **Explore the .claude directory** — https://code.claude.com/docs/en/claude-directory | Configuração específica do projeto deve estar no repositório; configuração pessoal não é fonte de autoridade do projeto. | Ao criar skills, rules, agents, hooks ou settings do projeto. | Ao revisar a configuração do Claude. | `C` + `.claude/`; `E`: arquivos versionados. |
| **AG-05** | Permissões Claude | Anthropic — **Configure permissions** — https://code.claude.com/docs/en/permissions | Princípio de menor privilégio; autonomia não deve significar acesso irrestrito ao host. | Antes de liberar shell, Git, rede ou operações destrutivas. | Ao revisar limites de execução do Claude. | `C`: princípio. `E`: permission rules/settings. |
| **AG-06** | Hooks Claude | Anthropic — **Automate actions with hooks / Hooks reference** — https://code.claude.com/docs/en/hooks-guide | Quando algo precisa ocorrer obrigatoriamente em determinado lifecycle point, não confiar apenas em prompt. | Para checks pré/pós-tool, bloqueios, validações e geração de evidência. | Ao revisar a barreira determinística usada pelo Claude. | `C`: declarar obrigação. `S`: procedimento complementar. `E`: hook/script real. |
| **AG-07** | Skills Claude | Anthropic — **Extend Claude with skills** — https://code.claude.com/docs/en/skills | Procedimentos especializados devem sair do `CLAUDE.md` quando não precisam ocupar permanentemente o contexto. | Para migration, RLS, testes, PWA offline, revisão etc. | Ao verificar equivalência com Skills do Codex. | `S`: principal. `C`: apenas regra de quando usá-la. |
| **AG-08** | Subagents Claude | Anthropic — **Create custom subagents** — https://code.claude.com/docs/en/sub-agents | Pesquisa ou análise volumosa pode ser isolada do contexto principal. | Exploração de arquitetura, análise de logs, investigação paralela. | Não como autoridade do Codex. | `S`/subagent; não usar para substituir validação independente. |
| **AG-09** | Codex IDE | OpenAI — **Codex IDE extension** — https://developers.openai.com/codex/ide | Arquivos abertos, seleção, workspace e diffs fazem parte do contexto operacional do Codex no editor. | Apenas se Claude estiver revisando trabalho do Codex. | Sempre que a tarefa for conduzida pela extensão VS Code. | `A`: orientação de uso do repo. `E`: permissões e checks continuam externos. |
| **AG-10** | `AGENTS.md` | OpenAI — **Custom instructions with AGENTS.md** — https://developers.openai.com/codex/agent-configuration/agents-md | Orientação durável deve viajar com o repositório e pode ter escopo por diretório. | Ao revisar instruções específicas dadas ao Codex. | Em toda sessão relevante. | `A`: arquitetura, comandos, convenções, critérios de revisão e ponteiros canônicos. `E`: regras críticas. |
| **AG-11** | Customização Codex | OpenAI — **Customization** — https://developers.openai.com/codex/customization/overview | `AGENTS.md`, Skills, MCP e Subagents resolvem problemas diferentes e não devem ser usados como sinônimos. | Ao revisar desenho cross-agent. | Ao decidir onde colocar uma nova orientação/capacidade. | `A`, `S`, MCP conforme função; `E` quando regra obrigatória. |
| **AG-12** | Skills Codex | OpenAI — **Build skills** — https://developers.openai.com/codex/build-skills | Workflow repetível deve ser encapsulado em Skill, com instruções, referências e scripts opcionais. | Ao verificar se os dois agentes recebem procedimentos equivalentes. | Quando determinada classe de tarefa possui processo repetível. | `S`: principal. `A`: apenas regra de descoberta/uso. |
| **AG-13** | Subagents Codex | OpenAI — **Subagents** — https://developers.openai.com/codex/subagents | Trabalho independente e ruidoso pode ser delegado sem poluir a thread principal. | Ao revisar uma entrega produzida com subagentes. | Exploração, testes, triagem ou investigações independentes. | Configuração de subagents; não substituir reviewer humano/determinístico. |
| **AG-14** | Sandbox e approvals Codex | OpenAI — **Agent approvals & security / Sandbox** — https://developers.openai.com/codex/agent-approvals-security | Sandbox e aprovação são controles distintos: fronteira técnica ≠ decisão de autorização. | Ao revisar segurança operacional do Codex. | Antes de conceder acesso ao filesystem, rede ou comandos externos. | `A`: princípio. `E`: sandbox/approval configuration. |
| **AG-15** | Rules Codex | OpenAI — **Rules** — https://developers.openai.com/codex/rules | Comandos que escapam do sandbox devem ter tratamento explícito. | Ao revisar segurança cross-agent. | Ao configurar exceções de comandos. | `E`: `.rules`; não duplicar como mera recomendação textual. |
| **AG-16** | Hooks Codex | OpenAI — **Hooks** — https://developers.openai.com/codex/hooks | Eventos de lifecycle podem acionar automações independentemente do prompt da tarefa. | Ao desenhar checks equivalentes entre agentes. | Para checks automáticos ligados ao lifecycle do Codex. | `E`: hook. `A`: somente descrição da política. |
| **AG-17** | MCP Codex | OpenAI — **Model Context Protocol** — https://developers.openai.com/codex/mcp | Integração com sistemas externos deve ocorrer por interface explícita de ferramentas/contexto. | Quando Claude precisar operar integração equivalente. | Quando a tarefa realmente exigir dados/ferramentas externas. | MCP/configuração; não embutir credenciais em `A` ou `C`. |

## 2.1 Decisão canônica resultante

Não manter:

```text
CLAUDE.md
→ centenas de linhas explicando arquitetura, Supabase, React,
  banco, testes, invariantes e workflow.

AGENTS.md
→ outra cópia semelhante com pequenas diferenças.
```

Preferir:

```text
docs/
├── architecture/
├── domain/
├── database/
├── pwa/
├── security/
└── testing/

CLAUDE.md
└── papel do Claude + comandos + limites + ponteiros

AGENTS.md
└── papel do Codex + comandos + limites + ponteiros
```

---

# 3. Ambiente VS Code + WSL

| ID | Tópico | Fonte oficial — página exata | Decisão CEPRAEA | Claude | Codex | Materialização |
|---|---|---|---|---|---|---|
| ENV-01 | VS Code sobre WSL | VS Code — **Developing in WSL** — https://code.visualstudio.com/docs/remote/wsl | O workspace, toolchain Linux e processos de desenvolvimento devem ter localização inequívoca. | Ao executar Node/npm/Git/Supabase/testes. | Idem. | `C/A`: declarar ambiente canônico. `E`: scripts devem funcionar no WSL. |
| ENV-02 | Setup WSL | Microsoft — **Set up a WSL development environment** — https://learn.microsoft.com/en-us/windows/wsl/setup/environment | PATH, Git, filesystem e ferramentas devem ser instalados/configurados deliberadamente no ambiente Linux. | Troubleshooting e bootstrap. | Idem. | `S`: `environment-bootstrap`/diagnóstico. `E`: scripts de preflight. |
| ENV-03 | VS Code Server remoto | VS Code — **Visual Studio Code Server** — https://code.visualstudio.com/docs/remote/vscode-server | Diferenciar UI local do VS Code do runtime/extensões no ambiente remoto evita diagnósticos errados. | Problemas de extensão, PATH ou runtime. | Idem. | `C/A`: nota curta. `S`: diagnóstico WSL. |

Regra recomendada para os dois agentes:

```text
Canonical development environment: WSL.
Commands, package manager, Git, Node, Supabase CLI and tests
MUST be resolved relative to the WSL workspace unless a task
explicitly establishes another environment.
```

O preflight real deve testar essa propriedade.

---

# 4. TypeScript, React e Vite

| ID | Tópico | Fonte oficial — página exata | Decisão arquitetural | Claude | Codex | Materialização |
|---|---|---|---|---|---|---|
| FE-01 | TypeScript `strict` | TypeScript — **TSConfig Reference** — https://www.typescriptlang.org/tsconfig/ | O projeto deve operar com tipagem estrita; `null`/`undefined` não podem ser tratados implicitamente como valores válidos. | Toda mudança `.ts/.tsx`. | Toda mudança `.ts/.tsx`. | `C/A`: `strict` é invariante da stack. `E`: `tsconfig.json` + `tsc --noEmit`. |
| FE-02 | Narrowing e unions | TypeScript — **Narrowing** — https://www.typescriptlang.org/docs/handbook/2/narrowing.html | Estados de domínio fechados devem preferir unions discriminadas e exhaustive checking a strings livres. | Entidades, commands, status, reducers. | Idem. | `S`: modelagem TS. `E`: tipos + `never`/typecheck. |
| FE-03 | Composição React | React — **Thinking in React** — https://react.dev/learn/thinking-in-react | Decompor UI a partir de responsabilidades e fluxo de dados, não misturar regras críticas de domínio em componentes visuais. | Feature/UI nova. | Idem. | `C/A`: boundary arquitetural. `S`: criar/refatorar feature React. `E`: testes e lint. |
| FE-04 | Estrutura do estado | React — **Managing State / Choosing the State Structure** — https://react.dev/learn/managing-state | Evitar estado redundante/duplicado; derivar valores quando possível. | Alterações de estado ou formulários. | Idem. | `S`: React state. `E`: testes. |
| FE-05 | Compartilhamento de estado | React — **Sharing State Between Components** — https://react.dev/learn/sharing-state-between-components | Deve haver fonte responsável identificável para cada estado compartilhado. | Ao alterar fluxo entre componentes. | Idem. | `S` + testes; não precisa ocupar `C/A` salvo regra arquitetural global. |
| FE-06 | Effects | React — **Synchronizing with Effects** — https://react.dev/learn/synchronizing-with-effects | `Effect` é para sincronização com sistemas externos, não depósito genérico de lógica de domínio. | Ao adicionar `useEffect`. | Idem. | `S`: revisão React. `E`: ESLint/tests quando possível. |
| FE-07 | Vite + TypeScript | Vite — **Features → TypeScript → Transpile Only** — https://vite.dev/guide/features | `vite build` não substitui `tsc`; Vite transpila TypeScript, mas não faz type checking. | Toda entrega frontend. | Toda entrega frontend. | `C/A`: comando obrigatório. `E`: `tsc --noEmit` em script/CI. |
| FE-08 | Variáveis de ambiente | Vite — **Env Variables and Modes** — https://vite.dev/guide/env-and-mode | Tudo exposto por `import.meta.env` com prefixo cliente deve ser considerado público; segredos não podem entrar no bundle. | Ao tocar `.env`, Vite config ou Supabase client. | Idem. | `C/A`: proibição de segredo no frontend. `E`: secret scanning/tests/config. |

Pipeline mínimo:

```text
tsc --noEmit
      ↓
lint
      ↓
unit tests
      ↓
vite build
```

Não assumir:

```text
vite build == TypeScript validado
```

---

# 5. Supabase e PostgreSQL

| ID | Tópico | Fonte oficial — página exata | Decisão arquitetural | Claude | Codex | Materialização |
|---|---|---|---|---|---|---|
| DB-01 | Supabase Database | Supabase — **Database** — https://supabase.com/docs/guides/database/overview | O banco é PostgreSQL; integridade de domínio não deve depender exclusivamente de React. | Toda mudança de persistência/schema. | Idem. | `C/A`: DB é autoridade de integridade física. `E`: PostgreSQL. |
| DB-02 | Constraints | PostgreSQL — **Constraints** — https://www.postgresql.org/docs/current/ddl-constraints.html | Propriedades representáveis fisicamente devem usar `NOT NULL`, `CHECK`, `UNIQUE`, PK, FK, `EXCLUDE` quando aplicável. | Migration/schema. | Migration/schema/review. | `S`: `database-migration`. `E`: constraints SQL. |
| DB-03 | Integridade referencial | PostgreSQL — **Foreign Keys** — https://www.postgresql.org/docs/current/tutorial-fk.html | Relações atleta, atividade, presença etc. devem usar FKs reais quando houver identidade relacional. | Schema. | Idem. | `E`: FK. |
| DB-04 | Concorrência | PostgreSQL — **Transaction Isolation** — https://www.postgresql.org/docs/current/transaction-iso.html | Operações multi-registro críticas precisam de política transacional explícita; pequena escala de usuários não elimina concorrência. | Command handlers/migrations críticas. | Idem/revisão. | `S`: transações. `E`: transaction/locking/constraints + tests. |
| DB-05 | Supabase Auth | Supabase — **Auth** — https://supabase.com/docs/guides/auth | Autenticação responde “quem é o usuário”; não substitui autorização de dados. | Login/session/user mapping. | Idem. | `C/A`: distinção Auth ≠ RLS. `E`: Auth config + DB. |
| DB-06 | RLS | Supabase — **Row Level Security** — https://supabase.com/docs/guides/database/postgres/row-level-security | Tabelas expostas devem ser protegidas no banco; frontend não pode ser a fronteira de autorização. | Toda tabela/policy nova. | Toda tabela/policy/review. | `C/A`: princípio. `S`: `design-rls`. `E`: RLS policies + pgTAP. |
| DB-07 | Segurança da Data API | Supabase — **Securing your API** — https://supabase.com/docs/guides/api/securing-your-api | Grants e RLS são camadas distintas e ambas devem ser deliberadas. | Mudança de schema/API. | Idem. | `S`: database-security. `E`: GRANT/REVOKE + RLS. |
| DB-08 | API keys | Supabase — **Understanding API keys** — https://supabase.com/docs/guides/api/api-keys | Browser só pode receber chave publicável; secret key possui privilégio elevado e não pode aparecer no cliente. | Qualquer integração Supabase frontend. | Idem. | `C/A`: proibição absoluta. `E`: env separation + secret scanning. |
| DB-09 | Migrations | Supabase — **Local Development / Database migrations** — https://supabase.com/docs/guides/local-development/overview | Toda mudança estrutural persistente deve ser reproduzível e versionada. | Mudança de banco. | Mudança/review de banco. | `C/A`: regra. `S`: `supabase-migration`. `E`: `supabase/migrations/` + CI. |
| DB-10 | Desenvolvimento local | Supabase — **Local Development & CLI** — https://supabase.com/docs/guides/local-development | Mudanças devem ser exercitadas em stack local antes de produção quando tecnicamente possível. | Banco/Auth/RLS/testes. | Idem. | `S`: local-db workflow. `E`: CLI/scripts. |
| DB-11 | Tipos gerados | Supabase — **Generating TypeScript Types** — https://supabase.com/docs/guides/api/rest/generating-types | Tipos da camada de acesso ao banco devem derivar do schema real em vez de serem reescritos manualmente. | Depois de migration. | Idem/revisão. | `S`: regeneration. `E`: generated types + drift check. |
| DB-12 | Testes de banco/RLS | Supabase — **Testing Overview** — https://supabase.com/docs/guides/local-development/testing/overview | Constraints, functions e RLS precisam ser testáveis como propriedades do banco. | Mudança de DB ou política. | Idem. | `S`: database-testing. `E`: pgTAP/test scripts/CI. |

Regra arquitetural:

```text
REGRA DE NEGÓCIO CRÍTICA

NÃO:
React component
    └── if (...) { ... }

PREFERIR, conforme a propriedade:

TypeScript type
      +
Domain validation
      +
PostgreSQL constraint
      +
RLS
      +
transaction
      +
automated test
```

Nem toda regra exige todas as camadas; deve-se usar a camada mais forte que represente corretamente a propriedade.

---

# 6. PWA e offline-first

| ID | Tópico | Fonte oficial — página exata | Decisão arquitetural | Claude | Codex | Materialização |
|---|---|---|---|---|---|---|
| PWA-01 | Arquitetura PWA | web.dev — **Learn PWA / Progressive Web Apps** — https://web.dev/learn/pwa | PWA não é sinônimo de “React instalado no celular”; instalação, offline e lifecycle são subsistemas próprios. | Feature que afete shell, instalação ou offline. | Idem. | `C/A`: offline-first é atributo arquitetural. `S`: PWA implementation. |
| PWA-02 | Web App Manifest | web.dev — **Web app manifest** — https://web.dev/learn/pwa/web-app-manifest | Identidade e comportamento instalável do aplicativo devem ser declarados em manifest controlado pelo projeto. | Ícones, nome, instalação, display etc. | Idem. | `S`: manifest. `E`: manifest + teste de build. |
| PWA-03 | Service Worker | web.dev — **Service workers** / MDN — **Using Service Workers** — https://web.dev/learn/pwa/service-workers | Cache/offline de recursos possui lifecycle próprio (`install`, `activate`, `fetch`); atualizações precisam de política explícita. | Mudança de cache/offline/update. | Idem. | `S`: service-worker. `E`: implementação + E2E/offline tests. |
| PWA-04 | Persistência local | MDN — **IndexedDB API** — https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API | Dados operacionais estruturados offline não devem ser confundidos com cache de assets. | Formulários ou operações offline. | Idem. | `S`: offline-storage. `E`: schema/local repository/tests. |
| PWA-05 | Sincronização offline | MDN — **Using Service Workers** + IndexedDB | A política de conflito/sync é responsabilidade da aplicação. | Toda mutation offline. | Toda mutation offline/review. | `C/A`: invariantes resumidas. `S`: `offline-sync`. `E`: IDs, versioning, transactions, queue e testes. |

Perguntas obrigatórias para qualquer mutation offline:

```text
Quem gera o ID?
Qual timestamp vale?
O que acontece se houver dois updates?
Existe retry?
A operação é idempotente?
Como detectar sincronização incompleta?
Qual versão vence?
Pode haver perda de dados?
```

---

# 7. Testes e evidência

| ID | Tópico | Fonte oficial — página exata | Decisão arquitetural | Claude | Codex | Materialização |
|---|---|---|---|---|---|---|
| TEST-01 | Unit/integration TS | Vitest — **Getting Started / Writing Tests** — https://vitest.dev/guide/ | Regras puras e lógica de aplicação devem produzir evidência automatizada rápida. | Mudança de domínio/application/frontend. | Idem. | `C/A`: comando oficial. `S`: test-authoring. `E`: Vitest + CI. |
| TEST-02 | E2E | Playwright — **Installation / Writing tests** — https://playwright.dev/docs/intro | Fluxos críticos precisam ser verificáveis no navegador real. | Feature completada. | Idem/review. | `S`: E2E. `E`: Playwright. |
| TEST-03 | Boas práticas E2E | Playwright — **Best Practices** — https://playwright.dev/docs/best-practices | Testes devem usar locators resilientes e observar comportamento visível ao usuário. | Criar/reparar E2E. | Idem. | `S`: Playwright skill. `E`: suite. |
| TEST-04 | Auth no E2E | Playwright — **Authentication** — https://playwright.dev/docs/auth | Testes dos papéis atleta/treinador precisam de ambientes de autenticação isolados e reproduzíveis. | Fluxos autenticados. | Idem. | `S`: auth-test fixtures. `E`: Playwright contexts/fixtures. |
| TEST-05 | Banco | Supabase — **Testing Overview** — https://supabase.com/docs/guides/local-development/testing/overview | RLS/constraints/functions são verificadas diretamente no banco, não indiretamente pela UI. | Alteração SQL. | Idem. | `E`: pgTAP. |

Gate de entrega:

```text
SOURCE CHANGE
     ↓
TypeScript typecheck
     ↓
lint
     ↓
Vitest
     ↓
Supabase DB tests / pgTAP
     ↓
Vite build
     ↓
Playwright critical flows
     ↓
evidence
```

---

# 8. Conteúdo recomendado para `CLAUDE.md`

Não copiar documentação externa para o arquivo.

```text
# CLAUDE.md

## Role
Papel do Claude Code no SDLC.

## Canonical Sources
Onde estão arquitetura, domínio, banco, PWA e testes.

## Runtime Stack
Vite
React
TypeScript strict
Supabase/PostgreSQL
PWA offline-first
WSL

## Non-negotiable Project Rules
- não redefinir domínio para acomodar implementação;
- não expor secret keys;
- não tratar frontend como barreira de autorização;
- não modificar schema remoto sem migration reproduzível;
- não considerar vite build equivalente a typecheck;
- não declarar PASS sem executar checks exigidos;
- respeitar limites do escopo da TASK.

## Commands
typecheck
lint
test
db test
build
e2e

## Skill Routing
Quando utilizar cada Skill.

## Environment
WSL é o ambiente canônico.

## Evidence
O que deve acompanhar a entrega.
```

---

# 9. Conteúdo recomendado para `AGENTS.md`

```text
# AGENTS.md

## Role
Papel do Codex no SDLC.

## Canonical Sources
Mesmas fontes normativas do Claude.

## Repository Commands
Mesmos comandos oficiais.

## Repository Invariants
Mesmas invariantes técnicas.

## Review Expectations
Critérios objetivos da entrega.

## Skill Routing
Skills aplicáveis.

## Environment
WSL.

## Scope Rules
O que pode e não pode ser alterado.
```

`CLAUDE.md` e `AGENTS.md` devem ser equivalentes em fatos, mas não precisam ser byte-a-byte iguais.

---

# 10. Skills canônicas iniciais

Criar apenas Skills cuja repetição já seja previsível:

```text
skills/
├── implement-task/
├── inspect-repository/
├── model-domain-types/
├── react-feature/
├── supabase-migration/
├── design-rls/
├── database-testing/
├── offline-storage/
├── offline-sync/
├── run-quality-gates/
└── produce-evidence/
```

Critério para criação de uma Skill:

```text
atividade recorrente
+
procedimento estável
+
sequência operacional relevante
+
benefício real de reutilização
```

Não criar uma Skill apenas porque existe uma página de documentação relacionada.

---

# 11. Enforcement mínimo derivado da matriz

```text
DECISÃO                              ENFORCEMENT

TypeScript estrito
    → tsconfig.json
    → tsc --noEmit

Estados fechados
    → discriminated unions
    → exhaustive checking

Integridade relacional
    → PK/FK/UNIQUE/CHECK/EXCLUDE

Autorização
    → Supabase RLS
    → grants
    → pgTAP

Segredos
    → env separation
    → .gitignore
    → secret scanning
    → CI

Mudanças de banco
    → supabase/migrations/*.sql
    → db reset
    → database tests

PWA offline
    → Service Worker
    → IndexedDB
    → synchronization contract
    → offline E2E tests

React
    → ESLint
    → Vitest
    → Playwright

Agentes
    → sandbox
    → permissions
    → hooks
    → command rules

Entrega
    → quality-gate script
    → exit codes
    → evidence
```

Diferença essencial:

```text
"O agente foi instruído a fazer corretamente."
```

não é equivalente a:

```text
"O sistema consegue rejeitar uma entrega que viola a propriedade."
```

---

# 12. Conjunto canônico mínimo de páginas oficiais

## Agentes

1. Claude Code — VS Code
2. Claude Code — Memory / `CLAUDE.md`
3. Claude Code — Permissions
4. Claude Code — Skills
5. Claude Code — Hooks
6. Codex — IDE Extension
7. Codex — `AGENTS.md`
8. Codex — Skills
9. Codex — Agent approvals & security

## Ambiente

10. VS Code — Developing in WSL
11. Microsoft — WSL Development Environment

## Frontend

12. TypeScript — TSConfig / strict
13. TypeScript — Narrowing
14. React — Thinking in React
15. React — Managing State
16. React — Synchronizing with Effects
17. Vite — Features / TypeScript
18. Vite — Env Variables and Modes

## PWA

19. web.dev — Web App Manifest
20. web.dev / MDN — Service Workers
21. MDN — IndexedDB

## Dados

22. Supabase — Database
23. PostgreSQL — Constraints
24. PostgreSQL — Transaction Isolation
25. Supabase — Auth
26. Supabase — Row Level Security
27. Supabase — Understanding API Keys
28. Supabase — Database Migrations
29. Supabase — Generating TypeScript Types
30. Supabase — Testing Overview

## Testes

31. Vitest — Getting Started / Writing Tests
32. Playwright — Writing Tests
33. Playwright — Best Practices
34. Playwright — Authentication

---

# 13. Arquitetura de conhecimento resultante

```text
DOCUMENTAÇÃO EXTERNA OFICIAL
          │
          │ fundamenta
          ▼
DECISÕES CANÔNICAS DO CEPRAEA
          │
          ├───────────────┐
          ▼               ▼
     CLAUDE.md         AGENTS.md
          │               │
          └───────┬───────┘
                  ▼
                Skills
                  │
                  ▼
             implementação
                  │
                  ▼
     ENFORCEMENT DETERMINÍSTICO
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
       TS       PostgreSQL  RLS
      tests       tests     hooks
        └─────────┼─────────┘
                  ▼
               evidence
                  │
                  ▼
             HUMAN REVIEW
```

---

# 14. Decisão consolidada

Claude Code e Codex não devem ser tratados como fontes de autoridade sobre React, TypeScript, Supabase ou o domínio do CEPRAEA.

A hierarquia de autoridade deve ser:

```text
REALIDADE DO CEPRAEA
        ↓
DECISÃO HUMANA HOMOLOGADA
        ↓
DOCUMENTAÇÃO CANÔNICA DO PROJETO
        ↓
DOCUMENTAÇÃO TÉCNICA OFICIAL
        ↓
CLAUDE.md / AGENTS.md
        ↓
SKILLS / PROCEDIMENTOS
        ↓
IMPLEMENTAÇÃO
        ↓
ENFORCEMENT DETERMINÍSTICO
        ↓
EVIDÊNCIAS
        ↓
REVISÃO / HOMOLOGAÇÃO HUMANA
```

As documentações oficiais fundamentam as decisões técnicas; a documentação canônica do CEPRAEA registra as decisões homologadas; os agentes executam essas decisões; e mecanismos determinísticos verificam o que for tecnicamente verificável.
