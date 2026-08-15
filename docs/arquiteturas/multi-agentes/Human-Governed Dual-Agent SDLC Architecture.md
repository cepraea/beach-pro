# Human-Governed Dual-Agent SDLC Architecture

```yaml
---
date: 2026-08-13
title: "CEPRAEA-BEACH-PRO — Arquitetura Final do Fluxo Multiagente e do Dev Container"
template: "arc42 9.0"
status: "FINAL PARA ADOÇÃO — REVISÃO 2"
---
```

Documento baseado na estrutura **arc42 9.0**.

**Escopo:** arquitetura do fluxo multiagente utilizado no SDLC do CEPRAEA-BEACH-PRO e arquitetura do Dev Container que suporta e restringe esse fluxo.

**Fora de escopo:** arquitetura funcional completa do runtime do CEPRAEA-BEACH-PRO. O sistema multiagente pertence ao processo de desenvolvimento e não ao runtime utilizado por atletas e treinador.

***

## Introduction and Goals

## Requirements Overview

O CEPRAEA-BEACH-PRO é um sistema de gestão esportiva de handebol de areia. O fluxo multiagente deve apoiar modelagem, implementação, validação e revisão sem introduzir uma plataforma agentiva maior que o próprio produto.

A arquitetura deve:

1. manter a autoridade humana sobre domínio, decisões materiais, Git privilegiado e release;
2. usar um agente principal para produção de alterações;
3. usar um agente independente para revisão;
4. usar Git como state machine e handoff operacional;
5. executar validações determinísticas antes da revisão por IA;
6. proteger fontes operacionais, secrets e configurações de segurança;
7. permitir uso fluido do Source Control e terminal do VS Code pelo humano;
8. impedir que os agentes executem transições Git privilegiadas;
9. evitar `STATE.md`, logs obrigatórios de execução/revisão, banco de workflow, filas, brokers ou orquestradores LLM;
10. preservar rastreabilidade rigorosa de conhecimento, decisões e mudanças materiais;
11. permitir evolução futura para isolamento mais forte sem alterar a separação de papéis;
12. manter o runtime do CEPRAEA independente dos agentes.

Fluxo principal:

```text
Humano
  │ seleciona ação
  ▼
Claude Code
EXECUTOR
  │ produz
  │ executa validações
  ▼
working tree / git diff
  ▼
Codex
REVIEWER
  │
  ├─ FAIL ──────────────► Claude corrige
  │
  ├─ HUMAN_DECISION_REQUIRED ─► Humano decide
  │
  └─ PASS ──────────────► Humano aceita
                              │
                              ▼
                         stage/commit
                              │
                              ▼
                         próxima ação
```

## Quality Goals

| Prioridade | Objetivo | Consequência arquitetural |
|---|---|---|
| 1 | Correção do domínio | decisões materiais permanecem humanas; evidência antes de promoção |
| 2 | Segurança e privacidade | zero secrets de produção; corpus protegido; enforcement obrigatório por permissions/policies; hardening adicional quando compatível |
| 3 | Simplicidade | dois agentes permanentes, Git e um humano |
| 4 | Revisão independente | produção e assurance são funções diferentes |
| 5 | Reprodutibilidade | validadores determinísticos precedem revisão LLM |
| 6 | Auditabilidade útil | Git + decisões formais, sem burocracia de cada interação |
| 7 | Boa DevEx | Source Control e Git continuam utilizáveis pelo humano dentro do VS Code |
| 8 | Evolução incremental | maior isolamento pode ser adicionado sem redesenhar o workflow |

## Stakeholders

| Papel | Responsabilidade | Expectativa |
|---|---|---|
| Domain/Release Authority | Humano | controla significado, decisões, Git privilegiado, aprovação e release |
| Executor | Claude Code | produz alteração delimitada, executa validadores e entrega diff revisável |
| Reviewer | Codex | revisa independentemente com projeto read-only e escrita efêmera controlada para temp/cache técnico; emite PASS/FAIL/HUMAN_DECISION_REQUIRED |
| Meta-review / Escalation | ChatGPT | usado somente em conflitos, mudanças de arquitetura ou decisões materiais complexas |
| Challenger excepcional | Gemini | terceira opinião independente quando realmente necessária |
| Usuários do produto | atletas e treinador | runtime simples, previsível e independente de LLMs |

---

# Architecture Constraints

1. **Human-triggered:** não há pipeline agentiva autônoma obrigatória.
2. **Dois agentes permanentes:** Claude Code e Codex.
3. **Git é a state machine operacional.**
4. **Uma branch dedicada por fluxo de mudança** quando aplicável.
5. **O humano controla `git add`, `commit`, `push`, `merge`, `rebase`, branches e release.**
6. **O workspace deve continuar gravável pelo humano dentro do Dev Container.**
7. `.git/**` **não é montado read-only no Docker**.
8. O corpus operacional `.drive/CEPRAEA BEACH PRO/**` é read-only no container.
9. O container roda como usuário não-root.
10. `privileged=false`; nenhuma montagem do Docker socket.
11. Secrets de produção não entram no container.
12. Claude Code usa managed permissions e hooks obrigatórios; o nested Bash sandbox é condicional à validação de compatibilidade no ambiente real.
13. Codex opera como Reviewer com projeto/workspace read-only e escrita efêmera controlada em diretórios temporários/cache técnico explicitamente autorizados; usar permission profile customizado quando suportado pela versão instalada, sem misturá-lo com `sandbox_mode` legado.
14. As políticas dos agentes não substituem controles de filesystem/sandbox onde enforcement técnico é possível.
15. Falha de permissão ou sandbox resulta em `BLOCKED`/ação humana, nunca bypass.
16. O runtime do CEPRAEA não depende de Claude, Codex, ChatGPT ou Gemini.

---

# Context and Scope

## Business Context

```text
                 ┌──────────────────────┐
                 │ CEPRAEA-BEACH-PRO    │
                 │ runtime da aplicação │
                 └──────────┬───────────┘
                            │
                     usado pelos usuários
                            │
                  atletas / treinador


                 SDLC / DEVELOPMENT

                ┌──────────────────┐
                │      HUMANO      │
                └────────┬─────────┘
                         │ tarefa
                         ▼
                 ┌──────────────┐
                 │ Claude Code  │
                 │   Executor   │
                 └──────┬───────┘
                        │ diff
                        ▼
                 ┌──────────────┐
                 │    Codex     │
                 │   Reviewer   │
                 └──────┬───────┘
                        │ verdict
                        ▼
                ┌──────────────────┐
                │      HUMANO      │
                │ Git / decisão    │
                └──────────────────┘
```

O fluxo multiagente não é uma interface de negócio do CEPRAEA. É uma capacidade de engenharia.

## Technical Context

```text
Host
└── VS Code
    └── Dev Container
        ├── workspace Git
        │   ├── código/modelagem       RW no container
        │   ├── .git/                  RW no container
        │   └── .drive/...             RO no container
        │
        ├── Claude Code
        │   ├── EXECUTOR
        │   ├── managed permissions
        │   ├── PreToolUse guard
        │   └── nested Bash sandbox [condicional]
        │
        └── Codex
            ├── REVIEWER
            └── project RO + ephemeral temp/cache RW
```

### Canais de handoff

| Origem | Destino | Canal |
|---|---|---|
| Humano | Claude | prompt com ação explícita |
| Claude | Codex | working tree + `git diff` |
| Codex | Humano/Claude | verdict + findings |
| Humano | Git | stage/commit/push |
| Git | próxima ação | novo HEAD / histórico |

---

# Solution Strategy

A solução adota **Human-Governed Dual-Agent Development Workflow**.

Princípios:

1. **deterministic first**;
2. **produção ≠ revisão ≠ aprovação**;
3. **Git como state machine**;
4. **least privilege por papel**;
5. **Defense in Depth**:
   - container;
   - managed permissions do Claude;
   - policies/hooks;
   - nested sandbox do Claude, quando compatível e validado;
   - sandbox do Codex;
   - Git/review humano;
6. **zero-governance-extra**: nenhuma infraestrutura agentiva sem necessidade comprovada;
7. **persistir conhecimento, não conversas operacionais**.

Arquitetura-mãe:

```text
                  CONTROL / AUTHORITY
                       HUMANO
                         │
                         ▼
              ┌─────────────────────┐
              │   EXECUTION PLANE   │
              │    Claude Code      │
              └──────────┬──────────┘
                         │ git diff
                         ▼
              ┌─────────────────────┐
              │   ASSURANCE PLANE   │
              │       Codex         │
              └──────────┬──────────┘
                         │ verdict
                         ▼
                       HUMANO
                         │
                         ▼
                        Git
```

---

# Building Block View

## Whitebox Overall System

### Overview

```text
┌────────────────────────────────────────────────────┐
│                   DEV CONTAINER                    │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │                 WORKSPACE                    │  │
│  │ código/modelagem             RW              │  │
│  │ .git                         RW              │  │
│  │ .drive/CEPRAEA BEACH PRO     RO              │  │
│  └──────────────────────────────────────────────┘  │
│                       ▲                            │
│          ┌────────────┴─────────────┐              │
│          │                          │              │
│ ┌────────┴────────┐        ┌────────┴─────────┐    │
│ │ Claude Code     │        │ Codex            │    │
│ │ EXECUTOR        │        │ REVIEWER         │    │
│ │                 │        │                  │    │
│ │ permissions      │        │ project RO       │    │
│ │ + guard          │        │ temp/cache RW    │    │
│ │ + sandbox opt.   │        │ controlado       │    │
│ └─────────────────┘        └──────────────────┘    │
│                                                    │
│ root-owned policy                                  │
│ /etc/claude-code/managed-settings.json             │
│ /usr/local/lib/cepraea/claude-guard                │
└────────────────────────────────────────────────────┘
```

### Motivation

O container fornece o ambiente reproduzível e um limite externo de segurança. As diferenças entre Executor e Reviewer são aplicadas nas sandboxes específicas das ferramentas, evitando a necessidade de dois usuários Linux ou dois containers no MVP.

### Contained Building Blocks

#### Human Control / Domain / Release Authority

Responsabilidades:

- selecionar AC/SEM/SYN ou tarefa;
- aprovar decisões materiais;
- aceitar/rejeitar findings que exijam autoridade humana;
- executar Git privilegiado;
- autorizar release/deploy;
- alterar políticas de governança.

Não é substituído por LLM.

#### Claude Code — Executor

Responsabilidades:

- produzir alterações;
- respeitar a tarefa corrente;
- executar lint/typecheck/tests/schemas;
- corrigir erros mecânicos;
- entregar working tree revisável;
- terminar com `READY_FOR_REVIEW` ou `BLOCKED`.

Não pode:

- autoaprovar;
- fazer Git privilegiado;
- modificar corpus de fontes;
- modificar política administrada;
- contornar sandbox;
- avançar automaticamente.

#### Codex — Reviewer

Responsabilidades:

- inspecionar `git diff`;
- ler artefatos relacionados;
- reexecutar validações compatíveis com read-only;
- procurar regressões e insuficiência de evidência;
- tentar refutar conclusões;
- emitir `PASS`, `FAIL` ou `HUMAN_DECISION_REQUIRED`.

Não modifica os artefatos sob revisão.

#### Git

Responsabilidades:

- estado operacional;
- diff de handoff;
- histórico;
- identidade das ações por commit;
- base para rastreabilidade.

Git substitui `STATE.md`, `executions/**` e `reviews/**` como infraestrutura obrigatória de workflow.

#### Deterministic Validators

Exemplos:

- lint;
- typecheck;
- unit tests;
- integration tests;
- schema validation;
- reference validation;
- `git diff --check`;
- validações específicas de modelagem.

Claude executa **todas as validações exigidas pela ação** antes do handoff. Codex reexecuta independentemente apenas os checks necessários para refutação, findings, área alterada e nível de risco; não há obrigação de duplicar integralmente a suíte por ritual.

#### Agent Policy

Conjunto mínimo:

```text
AGENT_POLICY.md
CLAUDE.md
AGENTS.md
```

- `AGENT_POLICY.md`: invariantes comuns;
- `CLAUDE.md`: adaptador do Executor;
- `AGENTS.md`: adaptador do Reviewer.

---

## Level 2

### White Box Claude Code Executor

```text
Humano
  │ tarefa
  ▼
CLAUDE.md
  │
  ├─► AGENT_POLICY.md
  ├─► plano/seção aplicável
  │
  ▼
Claude Code
  │
  ├─ Edit/Write
  ├─ Bash sandbox
  └─ validators
       │
       ▼
working tree
```

Enforcement:

1. managed settings em `/etc/claude-code/managed-settings.json`;
2. managed permissions obrigatórias para proteger paths e operações sensíveis;
3. PreToolUse guard obrigatório como fail-fast e feedback operacional;
4. container externo não-root, `privileged=false`, sem Docker socket e sem secrets de produção;
5. nested Bash sandbox é opcional no perfil BASE e só é promovido ao perfil HARDENED após acceptance test no host/container reais;
6. quando o perfil HARDENED estiver ativo: `sandbox.failIfUnavailable=true`;
7. quando o perfil HARDENED estiver ativo: `sandbox.allowUnsandboxedCommands=false`;
8. quando o perfil HARDENED estiver ativo: `enableWeakerNestedSandbox=true` apenas se necessário e explicitamente aceito como trade-off;
9. quando o perfil HARDENED estiver ativo: `filesystem.denyWrite` para `.git` e control plane, deny de credenciais e rede em allowlist estrita.

**Importante:** o guard não é tratado como a única barreira de segurança.

### White Box Codex Reviewer

```text
Humano
  │ "revise o diff"
  ▼
AGENTS.md
  │
  ├─► AGENT_POLICY.md
  └─► plano/critérios
       │
       ▼
Codex
project root = READ_ONLY
/tmp = READ_WRITE
approval_policy=never
       │
       ├─ lê repo
       ├─ lê diff
       └─ executa checks compatíveis
       │
       ▼
PASS | FAIL | HUMAN_DECISION_REQUIRED
```

O Reviewer não recebe write access aos artefatos do projeto durante o gate normal. Escrita efêmera é permitida apenas em `/tmp` e, quando necessário, em diretórios de cache técnico explicitamente autorizados, sem alterar o `git diff` sob revisão.

---

# Runtime View

## Scenario 1 — Execução normal com PASS

```text
1. Humano seleciona AC-NNN.
2. Claude lê política + seção aplicável.
3. Claude produz alteração.
4. Claude roda validadores determinísticos.
5. Claude corrige falhas mecânicas.
6. Claude informa READY_FOR_REVIEW.
7. Humano solicita review ao Codex.
8. Codex inspeciona working tree e git diff com o projeto em read-only.
9. Codex reexecuta checks selecionados de forma independente, proporcionais ao risco, aos findings e à área alterada, podendo usar somente escrita efêmera autorizada.
10. Codex emite PASS.
11. Humano revisa e faz stage/commit.
12. HEAD avança.
13. Próxima ação pode iniciar.
```

## Scenario 2 — Reviewer retorna FAIL

```text
Claude
  ↓
READY_FOR_REVIEW
  ↓
Codex
  ↓
FAIL + findings
  ↓
Claude corrige apenas os findings aplicáveis
  ↓
validadores
  ↓
novo review Codex
```

Não há novo agente nem arquivo de estado.

## Scenario 3 — HUMAN_DECISION_REQUIRED

```text
Claude/Codex detectam decisão material
  ↓
HUMAN_DECISION_REQUIRED
  ↓
Humano decide
  ↓
se necessário:
  DEC-NNN / registro_decisoes
  ↓
execução retoma
```

ChatGPT/Gemini podem ser consultados, mas não adquirem autoridade.

## Scenario 4 — Tentativa de Git privilegiado pelo Claude

Exemplo:

```text
git commit
git push
git switch
git restore
```

Camadas:

1. PreToolUse pode negar a chamada;
2. managed permissions e o PreToolUse guard bloqueiam intenções explícitas proibidas;
3. se o perfil HARDENED estiver ativo, write em `.git` também é negado pelo nested sandbox;
4. se o perfil HARDENED estiver ativo, rede/credenciais do Bash permanecem restritas e não há fallback unsandboxed;
5. resultado esperado: `BLOCKED` ou ação humana requerida, nunca bypass.

O humano continua podendo usar Git pelo terminal e Source Control do VS Code porque `.git` permanece RW no container geral.

## Scenario 5 — Humano faz commit pelo VS Code

```text
Source Control / terminal integrado
  ↓
git add
git commit
  ↓
.git RW no container
  ↓
commit criado normalmente
```

As restrições do Claude e Codex são específicas aos processos dos agentes, não ao usuário humano no container.

---

# Deployment View

## Infrastructure Level 1

```text
HOST
└── VS Code
    └── Dev Container
        ├── usuário não-root
        ├── privileged=false
        ├── no Docker socket
        ├── no production secrets
        │
        ├── workspace bind mount RW
        │   ├── .git RW
        │   └── .drive/CEPRAEA BEACH PRO RO
        │
        ├── Claude Code
        │   ├── managed permissions + guard [BASE]
        │   └── nested sandbox [HARDENED, condicional]
        │
        └── Codex
            └── project RO + ephemeral temp/cache RW
```

### Motivation

Preservar DevEx para o humano e ainda aplicar least privilege aos agentes.

### Quality and Performance Features

- ambiente reproduzível;
- dependências instaladas no build;
- mínimo de privilégios no runtime;
- testes executáveis localmente;
- segurança em camadas;
- ausência de infraestrutura agentiva adicional.

### Mapping of Building Blocks to Infrastructure

| Bloco | Infraestrutura |
|---|---|
| Humano | VS Code/host + terminal integrado |
| Claude | extensão/CLI executando dentro do Dev Container |
| Codex | extensão/CLI dentro do Dev Container |
| Git | workspace montado no container |
| Corpus | submount read-only |
| Claude managed policy | `/etc/claude-code/managed-settings.json` |
| Claude guard | `/usr/local/lib/cepraea/claude-guard` |
| Codex config | camada de configuração que aplica projeto read-only + escrita efêmera controlada |

## Infrastructure Level 2

### Dev Container

Requisitos:

```text
remoteUser = não-root
containerUser = não-root
privileged = false
Docker socket = ausente
secrets produção = ausentes
workspace = RW
.git = RW
corpus .drive = RO
```

`--cap-drop=ALL` e `no-new-privileges` são controles de hardening **condicionais**. Só devem ser promovidos ao perfil HARDENED após teste de compatibilidade com a toolchain, o kernel do host e qualquer nested sandbox utilizado.

### Perfis de Segurança do Container

#### Perfil BASE — obrigatório

```text
container: non-root, privileged=false, sem Docker socket, sem production secrets
workspace: RW
.git: RW para DevEx humano
.drive/CEPRAEA BEACH PRO: RO
Claude: managed permissions + hooks + no bypass
Codex: projeto RO + /tmp RW + caches técnicos explícitos
```

O perfil BASE é suficiente para declarar o ambiente operacional quando os acceptance tests obrigatórios passam.

#### Perfil HARDENED — condicional

```text
BASE
+ nested Bash sandbox Claude
+ filesystem denyWrite para .git/control plane em subprocessos
+ network allowlist
+ credential deny
+ failIfUnavailable=true
+ allowUnsandboxedCommands=false
```

O perfil HARDENED só pode ser habilitado após capability test bem-sucedido no host/container reais. Sua indisponibilidade não invalida o perfil BASE.

### Dockerfile

Responsabilidades:

- instalar toolchain da aplicação;
- instalar a toolchain necessária ao perfil BASE;
- instalar `bubblewrap` e `socat` somente se o perfil HARDENED for adotado após testes de compatibilidade;
- opcionalmente instalar runtime seccomp da Anthropic quando compatível;
- criar usuário não-root;
- copiar managed policy;
- copiar guard;
- root-own/chmod policy e guard;
- não instalar credenciais de produção.

Exemplo conceitual:

```dockerfile
USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git jq \
 && rm -rf /var/lib/apt/lists/*

# Somente no perfil HARDENED, após capability test:
# RUN apt-get update \
#  && apt-get install -y --no-install-recommends bubblewrap socat \
#  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/claude-code /usr/local/lib/cepraea

COPY managed-settings.json /etc/claude-code/managed-settings.json
COPY claude-guard /usr/local/lib/cepraea/claude-guard

RUN chown root:root \
      /etc/claude-code/managed-settings.json \
      /usr/local/lib/cepraea/claude-guard \
 && chmod 0444 /etc/claude-code/managed-settings.json \
 && chmod 0555 /usr/local/lib/cepraea/claude-guard

USER vscode
```

### `devcontainer.json`

Princípios:

- não sobrepor `.git` como RO;
- manter workspace normal;
- montar corpus operacional como RO;
- não montar Docker socket;
- não colocar secrets de produção em `containerEnv`/`remoteEnv`.

Exemplo parcial:

```jsonc
{
  "name": "CEPRAEA-BEACH-PRO",
  "workspaceFolder": "/workspaces/cepraea-beach-pro",
  "remoteUser": "vscode",
  "containerUser": "vscode",
  "mounts": [
    "source=${localWorkspaceFolder}/.drive/CEPRAEA BEACH PRO,target=${containerWorkspaceFolder}/.drive/CEPRAEA BEACH PRO,type=bind,readonly"
  ]
}
```

A configuração real deve preservar a stack já existente.

### Claude Managed Settings

O conteúdo de `managed-settings.json` usa o mesmo formato de settings do Claude Code; **não** é encapsulado em uma chave `managedSettings`.

A configuração é dividida em dois perfis:

- **BASE (obrigatório):** managed permissions + hooks + no bypass;
- **HARDENED (condicional):** acrescenta nested Bash sandbox, filesystem denyWrite para subprocessos, controle de rede/credenciais e fail-closed do sandbox após acceptance test bem-sucedido.

Exemplo arquitetural do perfil BASE:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  "permissions": {
    "disableBypassPermissionsMode": "disable",
    "disableAutoMode": "disable",
    "deny": [
      "Read(//workspaces/cepraea-beach-pro/.env)",
      "Read(//workspaces/cepraea-beach-pro/.env.*)",
      "Read(//workspaces/cepraea-beach-pro/secrets/**)",

      "Edit(//workspaces/cepraea-beach-pro/.git/**)",
      "Edit(//workspaces/cepraea-beach-pro/.devcontainer/**)",
      "Edit(//workspaces/cepraea-beach-pro/.claude/**)",
      "Edit(//workspaces/cepraea-beach-pro/.codex/**)",
      "Edit(//workspaces/cepraea-beach-pro/AGENT_POLICY.md)",
      "Edit(//workspaces/cepraea-beach-pro/CLAUDE.md)",
      "Edit(//workspaces/cepraea-beach-pro/AGENTS.md)",
      "Edit(//workspaces/cepraea-beach-pro/.drive/CEPRAEA BEACH PRO/**)",

      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(git pull *)",
      "Bash(git merge *)",
      "Bash(git rebase *)",
      "Bash(git cherry-pick *)",
      "Bash(git reset *)",
      "Bash(git restore *)",
      "Bash(git checkout *)",
      "Bash(git switch *)",
      "Bash(git worktree *)",
      "Bash(git clean *)",
      "Bash(git rm *)"
    ]
  },

  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/local/lib/cepraea/claude-guard"
          }
        ]
      }
    ]
  }
}
```

Notas:

- `Read(...)`/`Edit(...)` em managed permissions são enforcement do Claude Code para suas ferramentas internas; `Edit` também cobre `Write`, mas subprocessos arbitrários exigem sandbox para enforcement em nível de SO;
- em managed settings fora do projeto, paths absolutos das permission rules usam o prefixo `//`;
- padrões `Bash(...)` e o hook fornecem bloqueio direto/fail-fast para Git privilegiado, mas não substituem um sandbox de filesystem contra subprocessos indiretos;
- o perfil BASE não depende do nested sandbox para considerar o container operacional;
- o perfil HARDENED só pode ser ativado após validar `/status`, `/sandbox` e `/hooks` no ambiente real;
- a lista real de rede do perfil HARDENED deve ser derivada da toolchain;
- `enableWeakerNestedSandbox=true`, se necessário, deve ser tratado como concessão explícita e não como default;
- se o nested sandbox estiver indisponível, o perfil BASE continua válido e o risco residual deve permanecer documentado.

### Claude HARDENED Settings — extensão condicional

Somente após acceptance test bem-sucedido, o perfil HARDENED acrescenta ao perfil BASE, conceitualmente:

```jsonc
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "enableWeakerNestedSandbox": true,
    "filesystem": {
      "denyWrite": [
        "/workspaces/cepraea-beach-pro/.git",
        "/workspaces/cepraea-beach-pro/.devcontainer",
        "/workspaces/cepraea-beach-pro/.claude",
        "/workspaces/cepraea-beach-pro/.codex",
        "/workspaces/cepraea-beach-pro/AGENT_POLICY.md",
        "/workspaces/cepraea-beach-pro/CLAUDE.md",
        "/workspaces/cepraea-beach-pro/AGENTS.md",
        "/workspaces/cepraea-beach-pro/.drive/CEPRAEA BEACH PRO"
      ]
    },
    "network": {
      "strictAllowlist": true,
      "allowedDomains": []
    }
  }
}
```

Os valores reais devem ser validados contra a versão instalada do Claude Code antes da implantação. `enableWeakerNestedSandbox=true` não é default universal; só é usado se o ambiente exigir e o trade-off tiver sido aceito.

### Claude Guard

O guard é **defesa adicional**, não fronteira única.

O hook recebe **JSON via stdin**. Ele deve extrair:

```text
.tool_name
.tool_input.command
```

Não deve assumir que o comando chega em `"$*"`.

Requisitos:

1. fail-fast para comandos Git de mutação direta e outras intenções explicitamente proibidas;
2. negar pelo menos:
   - add
   - commit
   - push
   - pull
   - merge
   - rebase
   - cherry-pick
   - reset
   - restore
   - checkout
   - switch
   - worktree
   - tag mutável
   - clean
   - rm;
3. usar stderr + `exit 2` para bloquear `PreToolUse`;
4. não tentar interpretar shell arbitrário, aliases, `eval`, wrappers, codificações ou execução indireta como fronteira formal de segurança;
5. não alegar ser "à prova de balas": o guard é fail-fast/feedback operacional; a segurança estrutural depende das managed permissions e, quando HARDENED, do sandbox de filesystem/rede.

Exemplo mínimo de leitura correta da entrada:

```bash
#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"
command="$(jq -r '.tool_input.command // ""' <<<"$input")"

# política de inspeção aqui

echo "[Claude Guard] BLOCKED: operação não autorizada" >&2
exit 2
```

A implementação final deve permanecer simples e orientada a intenções óbvias. Não deve evoluir para um parser geral de shell. Qualquer requisito de segurança que dependa de interpretar shell arbitrário deve ser movido para managed permissions, sandbox ou outra fronteira técnica apropriada.

### Codex Reviewer Configuration

Para versões do Codex com **permission profiles**, a configuração-alvo é um profile específico para review. Permission profiles não devem ser misturados com o mecanismo antigo `sandbox_mode` na mesma configuração.

Exemplo:

```toml
default_permissions = "cepraea-review"
approval_policy = "never"

[permissions.cepraea-review]
description = "CEPRAEA reviewer: projeto read-only, temp efêmero writable, sem rede"

[permissions.cepraea-review.filesystem]
":minimal" = "read"
":tmpdir" = "write"
":slash_tmp" = "write"

[permissions.cepraea-review.filesystem.":workspace_roots"]
"." = "read"
"**/*.env" = "deny"

[permissions.cepraea-review.network]
enabled = false
```

Caches adicionais devem ser adicionados somente como paths concretos e writable quando um acceptance test demonstrar necessidade. O perfil é beta e deve ser validado contra a versão instalada do Codex.

Princípios:

- Reviewer lê os artefatos do projeto e não os edita;
- sem elevação automática;
- escrita efêmera é permitida somente em `/tmp` e caches técnicos explicitamente autorizados;
- essa escrita nunca pode alterar o working tree/diff sob revisão;
- testes de review devem preferir: lint sem `--fix`, typecheck `noEmit`, caches redirecionados para temp e validações puras.

---

# Cross-cutting Concepts

## Separation of Duties

```text
PRODUÇÃO
≠
REVISÃO
≠
APROVAÇÃO
```

- Claude produz.
- Codex revisa.
- Humano aprova e transiciona Git.

## Git as State Machine

Não existe `STATE.md` obrigatório.

Estados observáveis:

```text
HEAD limpo
→ tarefa iniciada
→ working tree dirty
→ validadores passam
→ review
→ PASS
→ commit humano
→ novo HEAD
```

A identidade da ação é preservada por convenção de commit:

```text
AC-001: ...
SEM-001: ...
SYN-001: ...
```

## Deterministic First

Antes do Reviewer:

```text
lint
typecheck
tests
schema validation
reference validation
git diff --check
```

Reviewer não é linter.

## Data Protection

1. production secrets não entram no container;
2. `.drive` é read-only;
3. read-only não implica confidencialidade;
4. PII não deve ser copiada para prompts ou artefatos sem necessidade;
5. se o corpus contiver informação que não pode ser processada pelos modelos, aplicar sanitização/redação ou política específica de dados.

## Policy Protection

Arquivos de política no workspace permanecem editáveis pelo humano, mas:

- Claude: managed permissions obrigatórias para ferramentas internas; `denyWrite` do nested sandbox apenas quando o perfil HARDENED estiver ativo;
- Codex: projeto read-only; `/tmp` e cache técnico explicitamente autorizado podem ser writable;
- policy administrada real do Claude: root-owned fora do workspace.

Isso preserva segurança sem quebrar a DevEx.

## Network

No perfil BASE, não se presume isolamento de rede do Bash além das restrições efetivamente disponíveis na ferramenta/ambiente. No perfil HARDENED, a rede do Bash segue default-deny/allowlist.

A conectividade do próprio cliente Claude não exige conceder ao shell acesso irrestrito à rede.

Git remoto não deve ser necessário durante execução normal do agente.

## No Bypass

```text
capacidade necessária
+
permissão inexistente
=
BLOCKED / HUMAN ACTION
```

Nunca workaround para vencer policy.

## Persistent Evidence

Persistir:

- decisões;
- evidências;
- conceitos/regras;
- modelo;
- código;
- testes;
- commits;
- security reviews materiais.

Não persistir obrigatoriamente:

- cada comando;
- cada ciclo de chat;
- receipt de cada review trivial;
- state machine paralela em Markdown.

---

# Architecture Decisions

## ADR-AGENT-001 — Human-Governed Dual-Agent Workflow

**Decisão:** Claude Code = Executor; Codex = Reviewer; humano = Domain/Release Authority.

**Motivo:** máxima separação útil com mínima coordenação.

## ADR-AGENT-002 — Git como State Machine

**Decisão:** remover `STATE.md`, `executions/**` e `reviews/**` do núcleo obrigatório.

**Motivo:** evitar duas fontes de verdade.

## ADR-AGENT-003 — Um Dev Container

**Decisão:** um Dev Container no MVP.

**Motivo:** dois containers criariam sincronização e manutenção desnecessárias.

**Evolução:** separar ambientes caso risco/compliance justifique.

## ADR-CONTAINER-001 — `.git` RW no Container

**Decisão:** `.git` não será montado read-only pelo Docker.

**Motivo:** VS Code Source Control, terminal e humano precisam de Git funcional dentro do container.

**Controle substituto:** sandbox específico dos agentes + hook + autoridade humana.

## ADR-CONTAINER-002 — Corpus Read-Only

**Decisão:** `.drive/CEPRAEA BEACH PRO/**` permanece RO no nível do container.

**Motivo:** nenhum ator do fluxo de desenvolvimento precisa modificar a fonte operacional durante modelagem.

## ADR-CONTAINER-003 — Claude Permission Enforcement Obrigatório; Nested Bash Sandbox Condicional

**Decisão:** managed permissions e hooks são requisitos do perfil BASE. O nested Bash sandbox só é ativado no perfil HARDENED após acceptance test bem-sucedido no host/container reais. Quando habilitado, opera fail-closed e sem fallback unsandboxed.

**Motivo:** preservar enforcement obrigatório sem transformar uma capability potencialmente incompatível com Docker não privilegiado em pré-requisito de DevEx.

## ADR-CONTAINER-004 — Guard é Defense in Depth

**Decisão:** PreToolUse guard complementa managed permissions e, no perfil HARDENED, o sandbox de filesystem/rede; não constitui security boundary isolada.

**Motivo:** parsing de shell por blacklist não constitui fronteira de segurança completa.

## ADR-CONTAINER-005 — Codex Project Read-Only + Ephemeral Write

**Decisão:** o projeto permanece read-only durante review. Codex pode escrever somente em `/tmp` e caches técnicos explicitamente autorizados, sem alterar o working tree. Não há escalation automática.

**Motivo:** preservar independência do Reviewer sem quebrar linters, typecheckers e testes que necessitam de armazenamento temporário.

## ADR-CONTAINER-006 — Progressive Hardening by Capability Test

**Decisão:** nenhum hardening opcional se torna requisito de implantação sem passar em acceptance tests no host/container reais.

**Motivo:** evitar segurança nominal que quebra a toolchain ou o fluxo de desenvolvimento.

## ADR-AGENT-004 — Escalation Agents Fora do Caminho Normal

ChatGPT/Gemini são usados somente em divergências materiais, revisão de arquitetura ou terceira opinião.

---

# Quality Requirements

## Quality Requirements Overview

| ID | Requisito |
|---|---|
| QR-001 | Claude não consegue modificar paths protegidos usando suas ferramentas normais de edição |
| QR-002 | Codex não consegue modificar arquivos do projeto durante review normal |
| QR-003 | Davi consegue usar Source Control e Git no terminal do VS Code |
| QR-004 | corpus `.drive` não pode ser alterado dentro do container |
| QR-005 | nested sandbox Claude só pode ser habilitado após acceptance test bem-sucedido |
| QR-006 | quando o nested sandbox estiver habilitado, falha de inicialização é fail-closed e não existe fallback unsandboxed |
| QR-007 | production secrets não estão presentes no ambiente |
| QR-008 | Claude executa as validações exigidas pela ação antes do review |
| QR-009 | Codex pode usar armazenamento efêmero sem alterar o working tree sob review |
| QR-010 | PASS do Reviewer não produz commit automaticamente |
| QR-011 | runtime do CEPRAEA funciona sem agentes |

## Quality Scenarios

### QS-001 — Claude tenta commit

**Quando:** Claude executa `git commit`.

**Esperado:** managed permissions e/ou hook bloqueiam; se HARDENED, `.git` denyWrite adiciona barreira de filesystem. Nenhum commit é criado; sessão reporta bloqueio.

### QS-002 — Claude tenta `git -c ... commit`

**Quando:** Claude adiciona flags globais ao Git.

**Esperado:** não deve depender de parser Bash ingênuo. A política não trata o hook como security boundary; se HARDENED, write em `.git` é adicionalmente negado pelo sandbox.

### QS-003 — Claude tenta push

**Quando:** Claude tenta publicar mudança.

**Esperado:** PreToolUse/permissions negam a intenção explícita. No perfil HARDENED, rede/credenciais do sandbox também não fornecem caminho alternativo.

### QS-004 — Humano faz commit pelo VS Code

**Quando:** Davi usa Source Control.

**Esperado:** operação funciona porque `.git` é RW no container geral e o sandbox Claude não se aplica ao processo humano.

### QS-005 — Codex tenta editar

**Quando:** Reviewer tenta aplicar fix.

**Esperado:** read-only bloqueia; Reviewer retorna finding em vez de patch.

### QS-006 — Claude tenta alterar `.drive`

**Esperado:** o mount RO do container impede a alteração em todos os perfis; managed `Edit(...)` deny fornece bloqueio adicional nas ferramentas internas do Claude e, se HARDENED, o nested sandbox adiciona enforcement para subprocessos.

### QS-007 — Capability test do nested sandbox Claude

**Quando:** o perfil HARDENED é avaliado no host/container reais.

**Esperado:** resultado `PASS` habilita HARDENED; resultado `UNAVAILABLE/FAIL` mantém o perfil BASE operacional e registra risco residual, sem fallback silencioso do sandbox dentro de uma sessão HARDENED.

### QS-008 — Ferramenta de teste precisa gravar cache

**Esperado:** Claude Executor pode fazê-lo dentro do workspace/temp conforme a tarefa; Codex Reviewer grava apenas em `/tmp` ou cache técnico explicitamente autorizado, sem alterar o working tree.

---

## Container Acceptance Tests

A implantação do ambiente deve ser validada no host/container reais.

| ID | Teste | Resultado esperado | Gate |
|---|---|---|---|
| CT-01 | Davi edita arquivo permitido no workspace | PASS | BASE |
| CT-02 | Davi executa `git add`/`git commit` pelo terminal ou Source Control | PASS | BASE |
| CT-03 | Claude edita arquivo autorizado pela tarefa | PASS | BASE |
| CT-04 | Claude tenta alterar `AGENT_POLICY.md`/control plane | BLOCKED | BASE |
| CT-05 | Claude tenta alterar `.drive/CEPRAEA BEACH PRO/**` | BLOCKED | BASE |
| CT-06 | Claude tenta `git commit` | BLOCKED | BASE |
| CT-07 | Codex lê `git diff` e arquivos do projeto | PASS | BASE |
| CT-08 | Codex tenta alterar source/modelagem | BLOCKED | BASE |
| CT-09 | Codex grava artefato temporário em `/tmp` | PASS | BASE |
| CT-10 | Codex executa check que usa temp/cache autorizado sem alterar working tree | PASS | BASE |
| CT-11 | production secrets disponíveis aos agentes | ZERO | BASE |
| CT-12 | nested sandbox Claude funciona no host/container reais | PASS ou UNAVAILABLE | HARDENED |

Regras de promoção:

```text
CT-01..CT-11 PASS
→ PROFILE=BASE READY

CT-12 PASS
→ PROFILE=HARDENED pode ser habilitado

CT-12 UNAVAILABLE/FAIL
→ BASE permanece operacional
→ HARDENED não é ativado
→ risco residual documentado
```

# Risks and Technical Debts

## R-001 — Compatibilidade do Nested Sandbox em Docker

O nested sandbox pode depender de user namespaces, AppArmor/kernel e capacidades incompatíveis com determinados hosts/containers. `enableWeakerNestedSandbox=true` também reduz a força do isolamento interno.

Mitigação:

- perfil BASE não depende do nested sandbox;
- HARDENED é ativado somente por capability test;
- outer container não privilegiado;
- no Docker socket;
- no production secrets;
- risco residual documentado quando HARDENED não estiver disponível.

## R-002 — PII legível por agentes

Mount RO evita alteração, não leitura.

Mitigação:

- política de minimização;
- sanitização/redação quando necessário;
- evitar cópia de conteúdo integral em prompts/logs.

## R-003 — Hook shell parsing

Hooks que parseiam comandos não são prova formal contra todas as formas de execução indireta.

Mitigação:

- hook apenas fail-fast/defense-in-depth;
- managed permissions são obrigatórias;
- não construir parser geral de shell;
- `.git` denyWrite, network allowlist, credenciais negadas e no-unsandboxed-fallback pertencem ao perfil HARDENED.

## R-004 — Source Control e credenciais Git

Dev Containers podem reutilizar credenciais Git/SSH do host.

Mitigação:

- não confiar em ausência de credencial como única barreira;
- Claude sandbox restringe rede/credenciais;
- Git privilegiado permanece humano.

## R-005 — Testes no Reviewer

Alguns runners escrevem cache/coverage.

Mitigação:

- projeto permanece read-only;
- `/tmp` é writable desde a configuração inicial;
- caches técnicos adicionais só são liberados explicitamente;
- nunca conceder workspace write ao Reviewer por conveniência.

## R-006 — Complexidade futura

Mais agentes/containers podem parecer atraentes.

Mitigação:

- adicionar apenas se houver caso de risco/custo mensurável.

## R-007 — Política desatualizada

Mudanças nas extensões podem alterar schemas e capacidades.

Mitigação:

- verificar documentação oficial antes de mudar configuração;
- validar `/status`, `/sandbox`, `/hooks` e settings do Codex após upgrades.

---

# Glossary

| Termo | Definição |
|---|---|
| Executor | agente autorizado a produzir alteração: Claude Code |
| Reviewer | agente independente autorizado a revisar, não corrigir: Codex |
| Human Authority | autoridade sobre domínio, Git privilegiado, decisões e release |
| Control Plane | políticas, decisão humana e Git que governam mudanças |
| Git privileged | operações como stage, commit, push, merge, rebase, branch/release |
| State Machine | estados do workflow inferidos de HEAD/working tree/review/commit |
| Handoff | `git diff`/working tree entregue do Executor ao Reviewer |
| Container Boundary | isolamento comum do Dev Container: non-root, sem privileged, sem Docker socket, sem secrets de produção |
| Claude Nested Sandbox | hardening opcional para Bash/subprocessos do Executor, ativado somente após capability test |
| Reviewer Sandbox | isolamento do Codex com projeto read-only e escrita efêmera controlada |
| Ephemeral Write | escrita permitida apenas em `/tmp` ou cache técnico autorizado, sem alterar o working tree |
| Sandbox | mecanismo de isolamento técnico aplicado a um processo do agente |
| Managed Settings | configuração Claude Code administrada e não sobrescrevível por projeto/usuário |
| PreToolUse | hook executado antes de uma tool call do Claude |
| Defense in Depth | múltiplas camadas independentes de proteção |
| Deterministic First | testes e validadores tradicionais antes de julgamento por LLM |
| SOURCE_ROOT | corpus operacional usado como fonte de modelagem |
| PII | informação pessoal identificável |
| BLOCKED | agente não consegue cumprir ação sem violar policy/permissão |
| HUMAN_DECISION_REQUIRED | conclusão depende de autoridade humana |

---

## Implementation Compatibility Notes

- Claude Code: `Read`/`Edit` deny rules são enforcement da ferramenta; `Edit(path)` governa as ferramentas internas de modificação, enquanto subprocessos arbitrários requerem sandbox para uma barreira em nível de SO.
- Claude Code: padrões Bash têm limitações conhecidas; hooks são recomendados para validação adicional, mas não devem substituir permissions/sandbox como hard boundary.
- Codex: permission profiles atuais permitem definir `:workspace_roots`, `:tmpdir`, `:slash_tmp` e regras de rede. Eles substituem, para essa finalidade, a combinação legada `sandbox_mode`/`sandbox_workspace_write` e não devem ser misturados na mesma configuração.
- As configurações exemplificadas neste documento devem ser verificadas novamente após upgrades relevantes das extensões/CLIs.

## Referências técnicas para implementação

- arc42 9.0 — template de documentação arquitetural.
- Claude Code — Settings: https://code.claude.com/docs/en/settings
- Claude Code — Hooks: https://code.claude.com/docs/en/hooks
- Claude Code — Permissions: https://code.claude.com/docs/en/permissions
- Claude Code — Sandboxing: https://code.claude.com/docs/en/sandboxing
- Claude Code — Sandbox environments: https://code.claude.com/docs/en/sandbox-environments
- OpenAI Codex — Agent approvals & security: https://developers.openai.com/codex/agent-approvals-security
- OpenAI Codex — Sandbox: https://developers.openai.com/codex/sandboxing
- OpenAI Codex — Config: https://developers.openai.com/codex/config-reference
- VS Code Dev Containers — source mount: https://code.visualstudio.com/remote/advancedcontainers/change-default-source-mount
- VS Code Dev Containers — Git credentials: https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
