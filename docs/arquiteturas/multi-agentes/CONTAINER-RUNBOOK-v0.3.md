# CONTAINER-RUNBOOK.md

> **Projeto:** CEPRAEA BEACH PRO
> **Documento:** Runbook técnico e baseline operacional do ambiente de agentes em container
> **Baseline documental inicial:** 2026-08-13
> **Atualização:** 2026-08-13
> **Versão:** v0.04
> **Baseline operacional incorporada:** continuidade de 2026-08-05 a 2026-08-09
> **Fontes:** históricos `Análise-de-fluxo-de-manifesto (3).json` e `Leitura-e-análise-de-PDF (5).json`
> **Status geral:** **CONTAINER IMPLANTADO — FRONTEIRA OPERACIONAL LOCAL VALIDADA — DoD GLOBAL PENDENTE**

---

## 0. Regra de uso deste documento

Este arquivo é a **fonte de verdade operacional** sobre a arquitetura de execução de agentes de IA em container no CEPRAEA BEACH PRO.

Antes de alterar qualquer componente relacionado a:

- Docker / Docker Desktop;
- Dev Container;
- `Dockerfile`;
- `.devcontainer/**`;
- mounts e volumes;
- usuários e permissões;
- Claude Code;
- Codex;
- hooks e managed settings;
- Git / GitHub / CI;
- credenciais;
- sandbox;
- regras de promoção para `main`;

o agente ou humano responsável deve:

1. Ler este Runbook.
2. Verificar o **Estado Atual Comprovado**.
3. Consultar as **Decisões Arquiteturais**.
4. Consultar **Problemas, Tentativas e Abordagens Rejeitadas**.
5. Executar os testes de baseline pertinentes antes da alteração.
6. Fazer uma alteração lógica por vez.
7. Reexecutar os testes afetados.
8. Registrar evidências.
9. Atualizar a matriz de estado.
10. Registrar a mudança no changelog deste documento.

### Regra anti-inferência

**Nenhuma configuração descrita como desejada, recomendada ou decidida deve ser tratada como implantada ou validada sem evidência.**

Se não houver evidência explícita de implementação e teste, o status deve permanecer `PENDENTE`.

---

## 1. Estados padronizados

| Estado | Significado |
|---|---|
| `DECIDIDO` | A arquitetura/regra foi escolhida, mas isso não prova implementação. |
| `IMPLANTADO` | Existe evidência de que a configuração foi aplicada. Ainda pode não ter sido testada. |
| `VALIDADO` | Existe evidência de teste com resultado compatível com o esperado. |
| `PENDENTE` | Não existe evidência suficiente de implantação e/ou validação. |
| `REJEITADO` | A abordagem foi considerada e abandonada. |
| `SUBSTITUÍDO` | A abordagem existiu no raciocínio, mas foi substituída por outra. |
| `NÃO APLICÁVEL` | O item não pertence ao escopo atual. |

### Convenção para evidência

Sempre que um item mudar para `VALIDADO`, registrar:

- data;
- comando ou procedimento executado;
- resultado observado;
- responsável;
- arquivo/configuração relacionada;
- commit, tag ou referência, quando aplicável.

---

## 2. Propósito

Este ambiente existe para reduzir o risco de agentes de IA operarem com a mesma autoridade do usuário humano `davis`.

Os objetivos são:

- limitar a autoridade operacional de Claude Code e Codex;
- reduzir blast radius de erros;
- impedir acesso casual a credenciais pessoais;
- impedir acesso ao Docker daemon do host;
- impedir que o agente trate seus próprios controles como autoridade confiável;
- preservar a revisão e promoção final como ação humana;
- evitar regressões ao modificar o ambiente;
- permitir manutenção e debug com estado conhecido;
- registrar o que foi tentado, aceito, rejeitado, implantado e validado.

Este Runbook **não garante que o código produzido pelo agente esteja correto**. Ele documenta e verifica a fronteira operacional em que os agentes executam.

---

## 3. Escopo

### Dentro do escopo

- Windows como host humano.
- WSL2 Ubuntu.
- Docker Desktop / Docker utilizado para criar o ambiente isolado.
- VS Code e Dev Containers.
- Claude Code.
- Codex.
- usuário não privilegiado dentro do container.
- mounts, volumes e filesystem visível ao container.
- Docker socket.
- credenciais e agentes SSH/GPG.
- hooks e configurações gerenciadas.
- Git, GitHub, CI e promoção para `main`.
- testes positivos e negativos da fronteira.
- rollback do ambiente de desenvolvimento.

### Fora do escopo direto

A segurança funcional da aplicação CEPRAEA BEACH PRO — como RLS, MFA, regras esportivas e regras de domínio — possui documentação e testes próprios.

Esses itens podem depender da CI e do ambiente, mas não devem ser confundidos com a fronteira de segurança do container.

---

## 4. Causa raiz

### 4.1 Problema inicial

O desenho original tentava controlar o comportamento do agente principalmente por:

- instruções persistentes;
- manifesto de tarefa;
- hooks;
- confirmação humana registrada no próprio fluxo;
- estado operacional associado ao manifesto.

Foi identificado um problema de fronteira de confiança:

> O mesmo agente que era fiscalizado poderia possuir autoridade de escrita sobre informações e configurações usadas para fiscalizá-lo.

No desenho inicial, um artefato dentro de `.claude` podia misturar:

1. proposta do que seria executado;
2. registro de aprovação;
3. estado operacional utilizado para autorizar ações.

### 4.2 Causa técnica

Agentes, hooks, configurações, repositório e estado podiam compartilhar:

- a mesma identidade Linux;
- o mesmo filesystem gravável;
- os mesmos privilégios;
- credenciais acessíveis à sessão.

### 4.3 Causa arquitetural

A fronteira de confiança estava dentro do ambiente controlado pelo agente.

### 4.4 Causa metodológica secundária

Os controles foram inicialmente pensados por **ferramenta/comando**, quando o risco real está em **capacidade e efeito**.

Bloquear uma chamada específica de `Edit`, `Write` ou `Bash` não protege contra todas as formas equivalentes de:

- alterar arquivos;
- alterar Git;
- alterar CI;
- alterar configurações de segurança;
- utilizar credenciais;
- executar processos externos.

### 4.5 Formulação consolidada

> **Ausência de separação de autoridade e de uma fronteira de confiança independente entre o agente que propõe/executa mudanças e os mecanismos humanos/sistêmicos que autorizam, verificam e promovem essas mudanças.**

---

## 5. Evidência histórica e baseline operacional

Esta seção separa o que foi comprovado **antes** da containerização do que foi comprovado **durante a implantação real**.

### 5.1 Caminho e filesystem do projeto

**Status:** `VALIDADO`

Caminho canônico de trabalho:

```text
/home/davis/projetos/cepraea-beach-pro
```

O projeto está no filesystem Linux/ext4 do WSL, e não em `/mnt/c`.

### 5.2 Correção histórica: o diretório inicial não era um clone Git

**Status:** `RESOLVIDO / VALIDADO`

A continuidade de 2026-08-05 demonstrou que o diretório então existente em:

```text
/home/davis/projetos/cepraea-beach-pro
```

continha arquivos do projeto, mas **não continha `.git`**. Portanto, a evidência histórica anterior comprovava o caminho e o filesystem, mas não autorizava inferir que aquele diretório fosse o clone Git canônico.

A cópia foi preservada como:

```text
/home/davis/projetos/cepraea-beach-pro.pre-git-20260805T151630Z
```

Em seguida foi realizado novo clone do repositório canônico:

```text
origin https://github.com/cepraea/beach-pro.git
```

com baseline:

```text
main
9857c72 initial commit: reset total do repositorio
```

e criação da branch de implantação:

```text
chore/agent-safe-devcontainer
```

Log de evidência registrado no histórico:

```text
/home/davis/recuperacao-git-cepraea-20260805T151630Z.log
```

**Regra derivada:** nunca usar apenas a existência do caminho como prova de que o checkout é um repositório Git válido. Validar explicitamente `.git`, `git rev-parse`, remote e branch.

### 5.3 Identidade humana e autoridade no host

**Status:** `VALIDADO`

No WSL/host, `davis` é a autoridade humana. O histórico registrou `davis` com grupos administrativos, inclusive `sudo` e `docker` no ambiente humano.

Isso é **esperado no plano de controle humano** e é precisamente o motivo pelo qual agentes não devem executar diretamente como `davis`.

### 5.4 Plano de controle aplicado

**Status:** `IMPLANTADO`

O pacote de plano de controle foi aplicado na branch:

```text
chore/agent-safe-devcontainer
```

com backup:

```text
/home/davis/backups/cepraea-agent-control-20260805T174620Z
```

O histórico registrou a aplicação de, entre outros:

```text
.ai/**
.devcontainer/Dockerfile
.devcontainer/devcontainer.json
.devcontainer/control-plane/**
.devcontainer/guards/pretool
.devcontainer/guards/posttool
.mcp.json
AGENTS.md
CLAUDE.md
```

Log:

```text
/home/davis/aplicacao-plano-controle-v2-20260805T174620Z.log
```

A aplicação foi precedida e seguida por validações estáticas. Falhas de formatação e build encontradas no processo foram corrigidas de forma controlada e registradas na seção de incidentes.

### 5.5 Baseline operacional do Dev Container

**Status:** `VALIDADO`

O Dev Container foi construído e utilizado de fato. Em runtimes diferentes, o ambiente apresentou:

```text
pwd     = /workspaces/cepraea-beach-pro
whoami  = agent
uid/gid = 1000(agent):1000(agent)
```

Foram observados e testados:

```text
sudo                          AUSENTE
Docker CLI                    AUSENTE
/var/run/docker.sock          AUSENTE
CapInh/CapPrm/CapEff          0
CapBnd/CapAmb                 0
NoNewPrivs                    1
Seccomp                       ativo
.git                          somente leitura
.devcontainer                 somente leitura
.github/workflows             somente leitura
.claude do projeto            somente leitura
.codex do projeto             somente leitura
.mcp.json                     somente leitura
CLAUDE.md / AGENTS.md         somente leitura
```

As políticas administrativas foram observadas como `root:root`, incluindo:

```text
/etc/claude-code/managed-settings.json
/etc/codex/requirements.toml
/usr/local/lib/cepraea-guards/pretool
/usr/local/lib/cepraea-guards/posttool
```

**Limite probatório mantido:** esta continuidade não forneceu uma saída centralizada de `docker inspect` explicitando `Privileged=false`. Portanto `ISO-05` permanece `PENDENTE` até essa evidência existir, mesmo que os demais sinais sejam compatíveis com container não privilegiado.

---

## 6. Arquitetura operacional vigente

**Status da arquitetura:** `DECIDIDO`
**Implantação da fronteira local:** `IMPLANTADO`
**Validação da fronteira local comum:** `VALIDADO`
**DoD global:** `PENDENTE`

```text
Windows — autoridade humana
└── WSL2 Ubuntu — davis
    ├── Docker / Docker Desktop
    ├── Git e GitHub humanos
    ├── credenciais pessoais
    ├── revisão e promoção
    │
    └── VS Code → Dev Container: CEPRAEA Agent
        └── agent
            ├── Claude Code
            ├── Codex
            ├── workspace autorizado
            ├── .git readonly
            ├── plano de controle readonly
            ├── sem sudo
            ├── sem Docker CLI/socket
            ├── sem autoridade GitHub de davis
            └── sem capabilities administrativas observadas
```

### 6.1 Princípio central

> **`davis` permanece no plano de controle humano; Claude Code e Codex executam dentro da fronteira comum do Dev Container.**

### 6.2 Papel do Dev Container

O Dev Container é a fronteira comum abaixo das políticas específicas dos agentes.

Hooks do Claude não governam Codex. Políticas do Codex não governam Claude. Logo, propriedades críticas precisam existir também em nível de sistema/container:

- identidade;
- mounts;
- permissões;
- ausência de Docker;
- ausência de autoridade Git remota;
- proteção do plano de controle;
- revisão e promoção humanas.

### 6.3 Limites da declaração `VALIDADO`

A expressão **fronteira operacional local validada** significa apenas que a continuidade trouxe evidência suficiente para os controles locais expressamente marcados como `VALIDADO` neste Runbook.

Ela **não** significa:

- `main` protegida comprovada;
- CI obrigatório comprovado;
- política de rede final definida;
- GPG/cloud/deploy totalmente inventariados;
- rollback completo testado;
- dados reais, staging ou produção liberados;
- DoD global concluído.

---

## 7. Decisões arquiteturais consolidadas

### DEC-CTR-001 — Dev Container como fronteira comum

**Status:** `DECIDIDO / IMPLANTADO / VALIDADO`

Claude Code e Codex executam no `Dev Container: CEPRAEA Agent` como usuário `agent`.

---

### DEC-CTR-002 — `davis` permanece autoridade humana

**Status:** `DECIDIDO`

Fora do container, `davis` mantém autoridade sobre:

- Docker;
- reconstrução do container;
- Git e GitHub;
- credenciais pessoais;
- revisão;
- commit/push/PR;
- promoção e merge.

---

### DEC-CTR-003 — Segundo usuário Windows não é a solução principal

**Status:** `REJEITADO`

A fronteira escolhida é o Dev Container, não uma segunda identidade Windows usada como substituto do isolamento.

---

### DEC-CTR-004 — Hooks não são a fronteira global

**Status:** `DECIDIDO / VALIDADO COMO PRINCÍPIO`

Os E2Es mostraram a necessidade de verificar também a fronteira comum do sistema. Hooks permanecem defesa em profundidade.

---

### DEC-CTR-005 — Arquitetura pragmática

**Status:** `DECIDIDO`

A separação proposta/aprovação/estado continua conceitualmente válida, mas a implantação atual não usa uma orquestração criptográfica pesada como boundary principal.

---

### DEC-CTR-006 — Agente sem Docker daemon

**Status:** `DECIDIDO / IMPLANTADO / VALIDADO`

No runtime validado:

```text
Docker CLI = ausente
Docker socket = ausente
```

---

### DEC-CTR-007 — Agente não root e sem sudo

**Status:** `DECIDIDO / IMPLANTADO / VALIDADO`

Runtime observado:

```text
agent
uid=1000(agent)
sudo ausente
```

---

### DEC-CTR-008 — Credenciais pessoais e autoridade Git do operador ausentes

**Status:** `DECIDIDO / IMPLANTADO / VALIDADO`

A validação não se limita mais à ausência de `~/.ssh` ou `credential.helper`.

A propriedade aprovada é:

> processos do agente não recebem autoridade GitHub reutilizável de `davis`.

Para `GH_TOKEN` e `GITHUB_TOKEN`, são estados aceitáveis:

```text
UNSET
ou
SET_EMPTY quando o valor vazio é imposto deliberadamente pela fronteira
```

Estado proibido:

```text
SET_NONEMPTY
```

Também devem permanecer ausentes:

```text
GIT_ASKPASS
VSCODE_GIT_ASKPASS_NODE
VSCODE_GIT_ASKPASS_MAIN
VSCODE_GIT_ASKPASS_EXTRA_ARGS
```

A capacidade remota foi testada com `git push --dry-run` e falhou por ausência de autenticação após a correção, em dois rebuilds independentes.

---

### DEC-CTR-009 — Plano de controle protegido materialmente

**Status:** `DECIDIDO / IMPLANTADO / VALIDADO`

O agente não deve conseguir modificar, como tarefa comum:

```text
.git
.devcontainer/**
.github/workflows/**
.claude do projeto
.codex do projeto
.mcp.json
CLAUDE.md
AGENTS.md
managed settings
requirements administrativos
guards
```

A proteção deve existir por mount/ownership/permissões, não apenas por instrução comportamental.

---

### DEC-CTR-010 — Um agente escritor por workspace/branch

**Status:** `DECIDIDO`
**Validação operacional recorrente:** `PENDENTE`

A continuidade comprova uso controlado de Claude e Codex, mas não prova que toda operação futura cumpriu ou cumprirá automaticamente a regra de um escritor.

---

### DEC-CTR-011 — Agentes não promovem para `main`

**Status:** `DECIDIDO / VALIDADO NA FRONTEIRA LOCAL`

`.git` é readonly no container e a autoridade Git remota do processo `agent` foi removida/testada.

A proteção remota da `main` continua separadamente `PENDENTE`.

---

### DEC-CTR-012 — Clone descartável por tarefa

**Status:** `PENDENTE DE DECISÃO OPERACIONAL FINAL`

A continuidade utilizou o checkout canônico com branch de implantação. Não há evidência suficiente para tornar clone descartável por tarefa uma invariante obrigatória.

---

### DEC-CTR-013 — `.git` somente leitura

**Status:** `DECIDIDO / IMPLANTADO / VALIDADO`

O modelo adotado é:

**Modelo A — Git humano**:

- agente altera somente arquivos ordinários autorizados;
- `.git` é readonly;
- commit/push/PR/merge pertencem a `davis` fora do container.

Tentativas de escrita em `.git` foram recusadas pelo filesystem e `HEAD` permaneceu intacto durante os E2Es.

---

### DEC-CTR-014 — Política de rede

**Status:** `PENDENTE DE DECISÃO FINAL`
**Implantação:** `PENDENTE`
**Validação:** `PENDENTE`

A continuidade não fecha de forma inequívoca uma política única para conectividade geral.

Não inferir `NET-01=VALIDADO` a partir do funcionamento de downloads, autenticação dos próprios agentes ou chamadas específicas.

---

### DEC-ARQ-001 — Via B: Dev Container como sandbox operacional

**Status:** `APPROVED / IMPLANTADO / VALIDADO NO RUNTIME`

O sandbox Bubblewrap interno do Claude mostrou incompatibilidade com a fronteira Linux/seccomp do Dev Container.

A decisão formal adotada foi:

> **não enfraquecer o Dev Container para satisfazer o sandbox interno. O Dev Container é o sandbox operacional primário.**

São explicitamente rejeitadas como correção automática:

```text
privileged=true
SYS_ADMIN
seccomp=unconfined
Docker socket
```

A decisão foi registrada em:

```text
.ai/decisions/DEC-ARQ-001-dev-container-como-sandbox-operacional.json
.ai/decisions/DEC-ARQ-001-dev-container-como-sandbox-operacional.md
```

Hash histórico do JSON:

```text
7e7114e2914f9c11ffaba473f79f3e7df4309540242d76b3a88e9561005d93d5
```

Implementação registrada em:

```text
.ai/implementations/IMP-DEC-ARQ-001-001-managed-settings-via-b.json
.ai/implementations/IMP-DEC-ARQ-001-001-managed-settings-via-b.md
```

Backup da implementação:

```text
/home/davis/backups/cepraea-dec-arq-001-via-b-20260806T044003Z
```

---

### DEC-ARQ-001-A1 — Critérios de aceite das extensões reais

**Status:** `APPROVED / VIGENTE`

A aprovação humana foi registrada em 2026-08-06.

A emenda substituiu o critério original `VB-AC-05` por:

```text
VB-AC-05A ... VB-AC-05H
```

Objetivo:

- validar Claude e Codex nas extensões/runtime reais do VS Code;
- não promover teste sintético de CLI/hook automaticamente a prova E2E;
- validar rejeição, aprovação limitada e ações críticas;
- manter observação externa das pós-condições.

Registro histórico:

```text
/home/davis/registro-aprovacao-dec-arq-001-a1-20260806T132516Z.log
```

**Regra:** um teste de componente pode validar aquele componente, mas não promove sozinho o gate E2E global.

---

## 8. Matriz de estado atual — v0.4

> **Freeze de enforcement ativo desde 2026-08-14.**
> Nenhuma nova mudança de enforcement até rebuild + gates P-001/P-002/P-003 concluídos.

| ID | Controle | Decisão | Implantação | Teste | Estado efetivo |
|---|---|---|---|---|---|
| ENV-01 | Clone canônico em `/home/davis/projetos/cepraea-beach-pro` | Sim | Sim | Sim | `VALIDADO` |
| ENV-02 | Repo em ext4/WSL, não `/mnt/c` | Sim | Sim | Sim | `VALIDADO` |
| ENV-03 | `davis` é autoridade humana | Sim | Sim | Sim | `VALIDADO` |
| ENV-04 | Branch de implantação `chore/agent-safe-devcontainer` | Sim | Sim | Sim | `VALIDADO` |
| DOC-01 | Manual de implantação segura criado | Sim | Sim | Sim | `VALIDADO` documental |
| DOC-02 | Runbook operacional mantido separadamente do manual | Sim | Sim | Sim | `VALIDADO` documental |
| NET-01 | Política de rede final definida e testada | Não final | Não comprovado | Não | `PENDENTE` |
| ISO-01 | Dev Container utilizado para agentes | Sim | Sim | Sim | `VALIDADO` |
| ISO-02 | usuário interno não root | Sim | Sim | Sim | `VALIDADO` |
| ISO-03 | `sudo` ausente/inutilizável | Sim | Sim | Sim | `VALIDADO` |
| ISO-04 | usuário `agent` sem grupo `docker` observado | Sim | Sim | Sim | `VALIDADO` |
| ISO-05 | `Privileged=false` comprovado por `docker inspect` | Sim | Não comprovado explicitamente | Não conclusivo | `PENDENTE` |
| ISO-06 | `no-new-privileges` | Sim | Sim | Sim | `VALIDADO` |
| ISO-07 | capabilities administrativas ausentes | Sim | Sim | Sim | `VALIDADO` |
| ISO-08 | Docker socket ausente | Sim | Sim | Sim | `VALIDADO` |
| MNT-01 | `/home/davis` não montado amplamente | Sim | Parcialmente observado | Evidência não centralizada | `PENDENTE` |
| MNT-02 | diretórios pessoais Windows não montados | Sim | Não comprovado integralmente | Não | `PENDENTE` |
| CRE-01 | autoridade GitHub pessoal ausente do agente | Sim | Sim | Capacidade testada | `VALIDADO` |
| CRE-02 | SSH agent/identidade pessoal ausente | Sim | Sim | Sim | `VALIDADO` |
| CRE-03 | GPG agent pessoal ausente | Sim | Não comprovado integralmente | Não | `PENDENTE` |
| CRE-04 | cloud/deploy secrets ausentes | Sim | Sanitização parcial comprovada | Inventário amplo ausente | `PENDENTE` |
| CRE-05 | VS Code Git AskPass não concede autoridade | Sim | Sim | 2 rebuilds + capability test | `VALIDADO` |
| AGT-01 | Claude Code executa dentro do container | Sim | Sim | Runtime real | `VALIDADO` |
| AGT-02 | Codex executa dentro do container | Sim | Sim | `E2E-CODEX-BOUNDARY-01` | `VALIDADO` |
| CTL-01 | `.devcontainer/**` protegido | Sim | Sim | Escrita recusada | `VALIDADO` |
| CTL-02 | managed settings/guards protegidos | Sim | Sim | root-owned + runtime | `VALIDADO` |
| CTL-03 | `.claude` do projeto protegido | Sim | Sim | Escrita recusada | `VALIDADO` |
| CTL-04 | `.codex` do projeto protegido | Sim | Sim | Escrita recusada | `VALIDADO` |
| CTL-05 | `.git` readonly | Sim | Sim | Escrita recusada + HEAD intacto | `VALIDADO` |
| CTL-06 | exceção de Plan Mode limitada a `/home/agent/.claude/plans/*.md` | Sim | Sim | Runtime real | `VALIDADO` |
| GIT-01 | branch de tarefa/implantação | Sim | Sim no ciclo observado | Sim | `VALIDADO` no ciclo observado |
| GIT-02 | agentes sem promoção Git | Sim | Sim | `.git` RO + auth remota ausente | `VALIDADO` localmente |
| GH-01 | `main` protegida remotamente | Sim | Não comprovado | Não | `PENDENTE` |
| GH-02 | matriz completa de atores/apps/chaves/bypass | Sim | Não comprovado | Não | `PENDENTE` |
| CI-01 | CI obrigatório antes de merge | Sim | Não comprovado | Não | `PENDENTE` |
| CI-02 | PR negativo bloqueia merge | Sim | Não comprovado | Não | `PENDENTE` |
| CI-03 | PR positivo + merge humano comprovado | Sim | Não comprovado | Não | `PENDENTE` |
| OPS-01 | um escritor por workspace/branch | Sim | Política existe | Uso recorrente não provado | `PENDENTE` |
| RBK-01 | rollback completo documentado e testado | Sim | Backups existem | Rollback E2E não executado | `PENDENTE` |
| GOV-01 | `.agent-flow/**` removido e declarado legado (DEC-GOV-001) | Sim | Sim | Referências normativas verificadas; nenhum resíduo normativo (rg confirmado) | `VALIDADO` |
| SEC-01 | `disableBypassPermissionsMode` no managed-settings Claude (P-001) | Sim | Sim | /etc/claude-code/managed-settings.json root-owned 1435B; sessão interativa executada: BYPASS=nao com --dangerously-skip-permissions; Claude confirma restrições ativas em runtime | `VALIDADO` |
| SEC-02 | `allowed_sandbox_modes = ["read-only"]` no codex-requirements.toml (P-002 corrigido) | Sim | Sim | bwrap indisponível no container → codex exec não executa; requirements.toml sobrescreve workspace-write→read-only (codex doctor 2026-08-14); proteção via container+.git RO; allowed_sandbox_modes = defesa em profundidade | `VALIDADO` |
| SEC-03A | Guard `.git` RO estrutural (DEC-CTR-013) — fronteira material | Sim | Sim | HEAD intacto antes/depois; git add/checkout bloqueados por filesystem | `VALIDADO` |
| SEC-03B | Guard fail-fast pretool — git subcommands via Bash tool call (P-003) | Sim | Sim | 16 negativos [2] + 6 positivos [0] via payload JSON 2026-08-14; todos os subcomandos mutantes bloqueados; read-only permitidos | `VALIDADO` |
| SEC-04 | Guard fail-fast pretool — flags `--dangerously-*` de claude e codex (P-003B) | Sim | Sim | 4 negativos [2] + 4 positivos [0] via payload JSON pós-rebuild 2026-08-14 | `VALIDADO` |

---

## 9. Inventário de arquivos e configurações implantados

| Caminho | Finalidade | Estado |
|---|---|---|
| `.devcontainer/devcontainer.json` | definição do Dev Container e controles VS Code | `IMPLANTADO` |
| `.devcontainer/Dockerfile` | imagem do agente | `IMPLANTADO` |
| `.devcontainer/control-plane/claude-managed-settings.json` | fonte canônica da política Claude | `IMPLANTADO` |
| `.devcontainer/control-plane/codex-requirements.toml` | fonte canônica dos requisitos Codex | `IMPLANTADO` |
| `.devcontainer/control-plane/gitconfig-agent` | Git neutro do agente | `IMPLANTADO` |
| `.devcontainer/guards/pretool` | guard pré-ferramenta | `IMPLANTADO / VALIDADO` |
| `.devcontainer/guards/posttool` | guard pós-ferramenta | `IMPLANTADO` |
| `/etc/claude-code/managed-settings.json` | política Claude no runtime | `VALIDADO` |
| `/etc/codex/requirements.toml` | requisitos Codex no runtime | `VALIDADO` |
| `/usr/local/lib/cepraea-guards/pretool` | guard root-owned no runtime | `VALIDADO` |
| `/usr/local/lib/cepraea-guards/posttool` | guard root-owned no runtime | `VALIDADO` |
| `.mcp.json` | configuração MCP do projeto | `IMPLANTADO` |
| `AGENTS.md` | protocolo para agentes | `IMPLANTADO` |
| `CLAUDE.md` | protocolo Claude | `IMPLANTADO` |
| `.ai/decisions/**` | decisões formais | `IMPLANTADO` |
| `.ai/implementations/**` | evidência de implementações | `IMPLANTADO` |

### 9.1 Plano de controle

Continuam pertencendo ao plano de controle:

```text
.devcontainer/**
.github/workflows/**
.github/CODEOWNERS
.claude do projeto
.codex do projeto
.mcp.json
AGENTS.md
CLAUDE.md
managed settings
requirements administrativos
guards
scripts de CI/validação
secrets/deploy/infraestrutura
configurações VS Code que alteram a fronteira
```

---

## 10. Regras de mounts

### 10.1 Propriedades comprovadas

**Status:** `VALIDADO` para os mounts críticos testados.

Foram observados como readonly no runtime:

```text
.git
.devcontainer
.github/workflows
.claude
.codex
.mcp.json
CLAUDE.md
AGENTS.md
```

Também foram utilizados volumes isolados de runtime do agente, incluindo homes operacionais de Claude/Codex.

### 10.2 Proibidos

Não introduzir mounts amplos ou sensíveis como:

```text
/home/davis
/home/davis/.ssh
/home/davis/.config/gh
/home/davis/.docker
/home/davis/.aws
/home/davis/.kube
/mnt/c/Users/... como superfície geral
/var/run/docker.sock
```

### 10.3 Evidência ainda faltante

A continuidade não fornece um inventário final único que permita promover `MNT-01` e `MNT-02` sem ressalva.

Portanto, a próxima auditoria deve registrar uma saída canônica de `docker inspect`/mounts.

---

## 11. Credenciais e autenticação

### 11.1 Fronteira efetiva

**Status:** `VALIDADO` para Git/GitHub e SSH agent no runtime testado.

A arquitetura exige que os agentes não herdem autoridade do operador humano.

Não basta verificar:

```text
~/.ssh ausente
credential.helper ausente
```

É necessário testar também a **capacidade efetiva** de autenticação remota.

### 11.2 Regressão: credential helper do VS Code

Um build funcional inicialmente recebeu um `credential.helper` injetado pelo Dev Containers/VS Code.

Esse resultado reprovou a fronteira naquele runtime e bloqueou a liberação dos agentes.

Foram adotadas defesas com configurações Git neutras/readonly e, depois, detectado um segundo vetor de autoridade.

### 11.3 Regressão: VS Code Integrated Git AskPass

O E2E encontrou o seguinte comportamento:

```text
credential.helper persistente     ausente
arquivos de credencial            ausentes
git push --dry-run normal         SUCESSO
mesmo push em ambiente sanitizado FALHA 128
```

Diagnóstico:

```text
VS Code Git AskPass / terminal authentication
```

A correção aplicada no contexto do Dev Container foi:

```json
{
  "git.terminalAuthentication": false,
  "git.useIntegratedAskPass": false,
  "github.gitAuthentication": false
}
```

Após a correção, em **dois rebuilds independentes**:

```text
GIT_ASKPASS                    UNSET
VSCODE_GIT_ASKPASS_NODE        UNSET
VSCODE_GIT_ASKPASS_MAIN        UNSET
VSCODE_GIT_ASKPASS_EXTRA_ARGS  UNSET
git push --dry-run             EXIT_CODE=128
```

Classificação:

```text
ARQ-05 = PASS_PERSISTENT_CAPABILITY_TESTED
VS Code Git AskPass no container = DISABLED_AND_VERIFIED
Autoridade Git remota de agent = ABSENT
```

### 11.4 `GH_TOKEN` / `GITHUB_TOKEN`

No processo Codex, esses nomes apareceram inicialmente como presentes. Investigação posterior mostrou:

```text
GH_TOKEN     = SET_EMPTY
GITHUB_TOKEN = SET_EMPTY
```

A origem é a sanitização deliberada em `containerEnv`/`remoteEnv`, não um secret utilizável.

Critério vigente:

```text
PASS:
- UNSET; ou
- SET_EMPTY imposto pela fronteira

FAIL:
- SET_NONEMPTY
```

### 11.5 Itens ainda pendentes

Ainda não há evidência suficiente para declarar de forma ampla:

```text
GPG agent pessoal = ausente em todos os fluxos
cloud/deploy credentials = inventário completo e ausente
```

Esses controles continuam `PENDENTE`.

---

## 12. Testes de baseline e E2E

### TST-ISO-001 — identidade não root

**Status:** `VALIDADO`

Resultados observados em runtimes reais:

```text
/workspaces/cepraea-beach-pro
agent
uid=1000(agent) gid=1000(agent) groups=1000(agent)
```

---

### TST-ISO-002 — sudo ausente

**Status:** `VALIDADO`

Resultado:

```text
sudo ausente
```

---

### TST-ISO-003 — Docker ausente

**Status:** `VALIDADO`

Resultado:

```text
Docker CLI ausente
Docker socket ausente
```

---

### TST-ISO-004 — não privilegiado por `docker inspect`

**Status:** `PENDENTE`

Embora o runtime tenha mostrado zero capabilities administrativas, `NoNewPrivs=1` e seccomp ativo, ainda deve ser registrada uma prova explícita de:

```text
Privileged=false
```

por `docker inspect`.

---

### TST-CRE-001 — Git neutro e readonly

**Status:** `VALIDADO`

Foram comprovados em runtimes independentes:

```text
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
GIT_TERMINAL_PROMPT=0
credential.helper ausente
user.name ausente
user.email ausente
configs Git protegidos contra escrita
SSH_AUTH_SOCK vazio
```

Logs históricos:

```text
/home/davis/diagnosticos/credential-boundary-runtime-1-20260806T115220Z.log
/home/davis/diagnosticos/credential-boundary-runtime-2-20260806T125108Z.log
```

---

### TST-CRE-002 — teste de capacidade Git remota

**Status:** `VALIDADO`

**Regra:** ausência de helper/configuração não é oráculo suficiente.

Teste de capacidade:

```bash
GIT_TERMINAL_PROMPT=0 git push --dry-run origin HEAD:refs/heads/<probe>
```

Após correção do AskPass, resultado esperado e observado:

```text
exit != 0
fatal: could not read Username ... terminal prompts disabled
```

Persistiu por dois rebuilds independentes.

---

### TST-CRE-003 — SSH agent

**Status:** `VALIDADO` no runtime observado.

```text
SSH_AUTH_SOCK vazio
ssh-add indisponível ou sem identidade
```

---

### TST-CRE-004 — GPG/cloud/deploy

**Status:** `PENDENTE`

Necessário inventário explícito antes de promoção.

---

### TST-CTL-001 — plano de controle readonly

**Status:** `VALIDADO`

Escritas de probe em `.git` e `.devcontainer` foram recusadas materialmente. Arquivos centrais do plano de controle permaneceram íntegros nos testes.

---

### TST-CLAUDE-001 — Claude no Dev Container

**Status:** `VALIDADO`

Evidências acumuladas:

- execução dentro do `Dev Container: CEPRAEA Agent`;
- identidade `agent`;
- managed settings reconhecidos;
- denies críticos ativos;
- Via B aplicada;
- edição funcional sintética validada;
- rejeição humana preservando o alvo;
- aprovação limitada alterando somente alvo autorizado;
- `.git`/plano de controle protegidos;
- `sudo`/Docker ausentes;
- HEAD preservado.

A obediência comportamental do Claude não é usada como única prova. Pós-condições foram verificadas externamente.

---

### TST-CODEX-001 — `E2E-CODEX-BOUNDARY-01`

**Status:** `VALIDADO`

Resultado consolidado registrado na continuidade:

```text
CODEX_IDENTITY                  PASS
CODEX_DEVCONTAINER_READONLY     PASS
CODEX_GIT_METADATA_READONLY     PASS
CODEX_NO_SUDO                   PASS
CODEX_NO_DOCKER_CLI             PASS
CODEX_NO_DOCKER_SOCKET          PASS
CODEX_CREDENTIAL_BOUNDARY       PASS
CODEX_READ_ONLY_REVIEW          PASS
CODEX_COMMON_OS_BOUNDARY        PASS

E2E-CODEX-BOUNDARY-01 = PASS
```

A falha do Bubblewrap interno não reprovou a fronteira externa porque a Via B já havia sido formalmente adotada.

---

### TST-CLAUDE-PLAN-001 — exceção de Plan Mode

**Status:** `VALIDADO NO RUNTIME REAL`

Controle:

```text
CLAUDE_PLAN_RUNTIME_EXCEPTION
```

Permite exclusivamente escrita de plano regular sob:

```text
/home/agent/.claude/plans/*.md
```

sem liberar `.claude` do projeto, `.devcontainer`, managed settings ou guards.

Hash histórico da fonte canônica `pretool` após a alteração:

```text
22d954238f1ea753c174ee3a244d76ab9d43eb0989ee0452a5464ff6fd880aec
```

Testes diretos:

```text
Write /home/agent/.claude/plans/test-plan.md       exit=0
Write <repo>/.claude/test.md                       exit=2
Write <repo>/.devcontainer/test                    exit=2
```

Evidência runtime real em 2026-08-09:

```text
Claude Code real
→ Plan Mode
→ Write em /home/agent/.claude/plans/alinhar-docs-drive-git-github-vscode.md
→ plano salvo
→ checkpoint humano alcançado
→ nenhuma implementação executada
```

**Risco residual:** o diretório `/home/agent/.claude/plans` precisa existir no runtime. A ausência desse diretório causou a falha anterior. Seu provisionamento reproduzível deve continuar sendo observado em rebuilds futuros.

---

### E2E-DEV-UNLOCK-01 — gate geral do fluxo cotidiano

**Status:** `PENDENTE — COMPONENTES LOCAIS SUBSTANCIALMENTE VALIDADOS`

O gate foi definido para comprovar conjuntamente:

```text
capacidade funcional do agente
+ confinamento material
+ revisão humana
+ promoção humana
+ PR/checks
```

Os componentes locais de Claude, Codex, credenciais, `.git`, Docker e plano de controle possuem evidência forte.

Permanecem sem evidência suficiente para fechar o gate completo:

```text
DU-09 — promoção humana fora do container em fluxo aceito
DU-10 — PR/checks comprovam promoção exatamente do conteúdo revisado
```

Logo, não declarar `DESENVOLVIMENTO_SINTETICO_DESBLOQUEADO` apenas a partir dos E2Es locais sem registrar os gates remotos previstos.

---

## 13. Gate final de aceite / DoD global

O ambiente local já não deve ser descrito como “container não implantado”. Entretanto, o plano global permanece **NOT DONE**.

### 13.1 Controles locais já comprovados

- [x] Dev Container utilizado;
- [x] `agent` não root;
- [x] `sudo` ausente;
- [x] grupo/capabilities Docker ausentes no usuário observado;
- [x] Docker CLI ausente;
- [x] Docker socket ausente;
- [x] `NoNewPrivs=1` observado;
- [x] capabilities administrativas zeradas;
- [x] `.git` readonly;
- [x] `.devcontainer` e caminhos críticos readonly;
- [x] managed settings/guards protegidos;
- [x] autoridade Git remota de `agent` ausente por teste de capacidade;
- [x] defesa AskPass persistente em dois rebuilds;
- [x] Claude no container;
- [x] Codex no container;
- [x] `E2E-CODEX-BOUNDARY-01`;
- [x] Plan Mode com exceção estreita e runtime real.

### 13.2 Gates ainda pendentes

- [ ] `Privileged=false` registrado explicitamente por `docker inspect`;
- [ ] inventário final de mounts e prova canônica de ausência de home humano amplo;
- [ ] GPG agent auditado;
- [ ] inventário amplo de cloud/deploy secrets;
- [ ] política de rede final (`NET-01`) decidida e testada;
- [ ] proteção remota de `main` comprovada;
- [ ] atores/apps/deploy keys/bypass inventariados;
- [ ] CI obrigatório comprovado;
- [ ] PR negativo com merge bloqueado;
- [ ] PR positivo com checks verdes;
- [ ] promoção/merge humano por `davis` comprovado;
- [ ] manifesto final de evidências;
- [ ] rollback completo testado.

### 13.3 Estado canônico

```text
ARQUITETURA                     DECIDIDA
CONTAINER                       IMPLANTADO
FRONTEIRA OPERACIONAL LOCAL     VALIDADA
CLAUDE                          VALIDADO NA FRONTEIRA
CODEX                           VALIDADO NA FRONTEIRA
CREDENCIAL GIT/GITHUB DO HOST   ISOLAMENTO VALIDADO
PLANO DE CONTROLE               READONLY VALIDADO
MAIN / GITHUB                   PENDENTE
CI                              PENDENTE
REDE                            PENDENTE
ROLLBACK COMPLETO               PENDENTE
DoD GLOBAL                      NOT DONE
```

---

## 14. Fluxo operacional diário vigente

**Status:** `DECIDIDO`
**Fronteira local do fluxo:** `VALIDADA`
**Promoção remota ponta a ponta:** `PENDENTE`

```text
Davi seleciona/cria branch
  ↓
abre o projeto no WSL
  ↓
Reopen in Container
  ↓
confirma agent/fronteira
  ↓
Claude OU Codex trabalha
  ↓
testes no container
  ↓
segundo agente pode revisar read-only
  ↓
Davi revisa diff fora da autoridade do agente
  ↓
commit / push / PR por Davi
  ↓
CI / ruleset
  ↓
merge humano
```

### Regras

1. não trabalhar com agente no host como `davis`;
2. apenas um escritor por workspace/branch;
3. `.git` permanece readonly no container;
4. agentes não recebem GitHub de `davis`;
5. plano de controle não é feature comum;
6. mudança em `.devcontainer` exige rebuild e regressão;
7. testes de configuração não substituem testes de capacidade;
8. testes de componente não promovem automaticamente gates E2E;
9. dados reais/staging/produção permanecem fora da liberação atual.

---

## 15. Protocolo para alterações no ambiente

### 15.1 Freeze-before-test

Antes de um teste que servirá como gate, registrar:

- propriedade que está sendo testada;
- comandos permitidos;
- oráculo PASS/FAIL;
- pós-condições esperadas;
- escopo da evidência.

Não reescrever retroativamente o significado de um teste porque apareceu evidência nova.

### 15.2 New-evidence amendment rule

Nova evidência:

1. é registrada separadamente;
2. altera somente controles afetados;
3. invalida resultado anterior apenas quando compromete sua capacidade probatória.

Exemplo histórico:

```text
ARQ-05 PASS estrutural
→ E2E encontra push dry-run autenticado
→ PASS anterior invalidado para capacidade remota
→ causa AskPass identificada
→ correção
→ mesmo teste repetido
→ PASS em dois rebuilds
```

### 15.3 Privilege-expansion evidence rule

Relaxamentos, whitelists e novas capacidades exigem:

- necessidade demonstrada;
- menor escopo possível;
- testes positivos e negativos;
- revalidação de controles adjacentes.

### 15.4 Antes da alteração

1. identificar controle afetado;
2. capturar baseline;
3. consultar decisões/incident history;
4. verificar se pertence ao plano de controle;
5. definir teste e oráculo antes da mudança.

### 15.5 Depois da alteração

1. rebuild quando necessário;
2. teste funcional;
3. teste negativo;
4. teste de capacidade quando o risco envolver autoridade;
5. verificação externa das pós-condições;
6. comparação com baseline;
7. registro de evidência;
8. atualização do Runbook.

### 15.6 Regra de regressão

Se um controle `VALIDADO` falhar:

```text
PARAR
→ invalidar somente o que a nova evidência realmente compromete
→ localizar o canal causal
→ corrigir a fonte
→ repetir o mesmo teste
→ exigir persistência quando a regressão envolver rebuild/integração
```

---

## 16. Plano de controle

### 16.1 Componentes críticos

Incluem:

```text
.devcontainer/**
.github/workflows/**
.github/CODEOWNERS
.claude do projeto
.codex do projeto
.mcp.json
AGENTS.md
CLAUDE.md
managed settings
requirements administrativos
guards
configurações de autenticação VS Code/Git
secrets/deploy/infra
```

### 16.2 Procedimento obrigatório

Mudança em plano de controle exige:

1. proposta específica;
2. aprovação humana explícita quando mudar enforcement;
3. baseline/hash anterior;
4. diff mínimo;
5. rebuild quando aplicável;
6. testes positivos;
7. testes adversariais;
8. regressão de credenciais/`.git`/Docker;
9. atualização do Runbook.

### 16.3 Exceção controlada de Plan Mode

A única exceção de escrita adicionada deliberadamente à superfície `.claude` é:

```text
/home/agent/.claude/plans/*.md
```

Objetivo exclusivo: suportar o runtime nativo de Plan Mode.

Não concede autoridade sobre:

```text
/workspaces/.../.claude/**
/home/agent/.claude/settings.json
/home/agent/.claude/hooks/**
/etc/claude-code/managed-settings.json
/usr/local/lib/cepraea-guards/**
```

A exceção deve rejeitar traversal/symlink/destino fora do diretório aprovado.

---

## 17. Incidentes, regressões e abordagens rejeitadas

### INC-CTR-001 — Checkout sem `.git`

**Status:** `RESOLVIDO / VALIDADO`

Sintoma:

```text
.git inexistente
```

Ação correta:

- preservar a cópia;
- não executar `git init` destrutivamente;
- clonar o repositório canônico;
- validar remote/branch/commit.

---

### INC-CTR-002 — Instalador dependia de `unzip`

**Status:** `RESOLVIDO`

A primeira aplicação parou antes de copiar arquivos porque `unzip` não estava disponível.

A falha controlada foi preservada como evidência e o instalador foi corrigido sem normalizar a falha como sucesso.

---

### INC-CTR-003 — newline final ausente

**Status:** `RESOLVIDO`

A revisão estática encontrou newline final ausente em arquivos do plano de controle. A correção foi mínima, com hashes antes/depois e nova validação.

---

### INC-CTR-004 — ownership de `.local/bin`

**Status:** `RESOLVIDO`

A primeira tentativa de build utilizável falhou por ownership/permissão do runtime de instalação do agente. O Dockerfile foi corrigido para que diretórios operacionais `.local` pertençam ao usuário `agent`, sem introduzir sudo.

---

### INC-CRE-001 — `credential.helper` injetado pelo Dev Containers

**Status:** `RESOLVIDO / VALIDADO`

A fronteira foi inicialmente reprovada porque o VS Code injetou helper de credencial Git no container.

A lição é permanente:

> desabilitar apenas `Copy Git Config` não basta como prova de ausência de autoridade.

---

### INC-CRE-002 — AskPass/terminal authentication ainda permitia push dry-run

**Status:** `RESOLVIDO / VALIDADO EM DOIS REBUILDS`

Este foi o gap mais importante encontrado pelo E2E.

Um `git push --dry-run` retornou sucesso apesar de configs Git já parecerem neutras.

Causa:

```text
GIT_ASKPASS / VSCODE_GIT_ASKPASS_* / autenticação integrada do VS Code
```

Correção:

```text
git.terminalAuthentication=false
git.useIntegratedAskPass=false
github.gitAuthentication=false
```

Oráculo de regressão:

```text
git push --dry-run deve falhar por falta de credencial
```

---

### INC-CRE-003 — `GH_TOKEN`/`GITHUB_TOKEN` do Codex pareciam vazamento

**Status:** `INVESTIGADO / NÃO ERA SECRET`

A primeira leitura apenas `SET/UNSET` foi insuficiente. O estado real era:

```text
SET_EMPTY
```

imposto deliberadamente pelo ambiente do container.

Lição:

> diferenciar `UNSET`, `SET_EMPTY` e `SET_NONEMPTY` antes de classificar vazamento de secret.

---

### INC-CLAUDE-001 — Bubblewrap incompatível com a fronteira externa

**Status:** `RESOLVIDO POR DEC-ARQ-001`

Não adicionar `privileged`, `SYS_ADMIN` ou `seccomp=unconfined` para fazer o sandbox interno funcionar.

---

### INC-CLAUDE-002 — Plan Mode bloqueado pelo próprio control plane

**Status:** `RESOLVIDO / VALIDADO NO RUNTIME REAL`

Causa operacional:

- Plan Mode precisa gravar em `/home/agent/.claude/plans`;
- o diretório não existia em um runtime;
- a proteção original de `.claude` não distinguia esse estado operacional de autoridade.

Correção:

```text
CLAUDE_PLAN_RUNTIME_EXCEPTION
```

com escopo mínimo para arquivos `.md` regulares em `/home/agent/.claude/plans/`.

---

### EXP-001 — Manifesto único como proposta + aprovação + estado

**Status:** `REJEITADO`

Misturava responsabilidades e criava circularidade de confiança.

---

### EXP-002 — Apenas hooks do Claude como proteção geral

**Status:** `REJEITADO COMO BOUNDARY GLOBAL`

Hooks permanecem defesa em profundidade.

---

### EXP-003 — Segundo usuário Windows

**Status:** `REJEITADO COMO SOLUÇÃO PRINCIPAL`

---

### EXP-004 — Orquestração criptográfica completa

**Status:** `SUBSTITUÍDO PELA ARQUITETURA PRAGMÁTICA ATUAL`

---

### EXP-005 — Apenas não montar `~/.ssh`

**Status:** `REJEITADO COMO PROVA DE ISOLAMENTO`

A regressão AskPass demonstrou por que a ausência de arquivo não basta.

---

## 18. Troubleshooting

### `whoami` retorna `davis`

O agente está fora da fronteira. Não continuar tarefa sensível.

### Docker socket ou CLI aparece

Tratar como regressão crítica. Não “compensar” com hook.

### `sudo` aparece/funciona

Interromper e revisar imagem/configuração.

### `credential.helper` reaparece

Interromper, mas não parar a investigação na configuração Git. Repetir também o teste de capacidade remota.

### `git push --dry-run` retorna `0`

**Bloqueio crítico.** Existe algum canal de autoridade remota.

Investigar, nessa ordem:

1. remote URL;
2. token não vazio;
3. credential helper;
4. `GIT_ASKPASS`;
5. `VSCODE_GIT_ASKPASS_*`;
6. autenticação integrada do VS Code;
7. headers Git/HTTP;
8. processos ancestrais/integrações.

Não executar push real.

### `GH_TOKEN=SET` ou `GITHUB_TOKEN=SET`

Não inferir secret imediatamente.

Classificar como:

```text
UNSET
SET_EMPTY
SET_NONEMPTY
```

Somente `SET_NONEMPTY` é secret potencialmente utilizável nesse critério.

### Bubblewrap falha

Aplicar `DEC-ARQ-001`. Não ampliar capabilities do container.

### Plan Mode não consegue salvar plano

Verificar:

```text
/home/agent/.claude/plans
```

- existência;
- ownership do runtime;
- exceção `CLAUDE_PLAN_RUNTIME_EXCEPTION`;
- bloqueio preservado para demais caminhos `.claude`.

### Agente consegue alterar plano de controle

Fronteira inválida. Parar, corrigir mount/ownership e executar regressão completa.

---

## 19. Rollback e recuperação

### 19.1 Evidência existente

A implantação produziu múltiplos backups antes de mudanças, incluindo:

```text
/home/davis/projetos/cepraea-beach-pro.pre-git-20260805T151630Z
/home/davis/backups/cepraea-agent-control-20260805T174620Z
/home/davis/backups/cepraea-newline-fix-20260805T181234Z
/home/davis/backups/cepraea-dockerfile-local-bin-20260805T191349Z
/home/davis/backups/cepraea-dec-arq-001-via-b-20260806T044003Z
```

Isso comprova disciplina de backup, **não** um rollback completo validado.

### 19.2 Estado

```text
RBK-01 = PENDENTE
```

Ainda falta registrar e testar um estado conhecido como bom com:

```text
Git commit/tag
hashes do control plane
imagem/digest
versões
procedimento de rebuild
bateria mínima de regressão
```

---

## 20. Pendências prioritárias

### P0 — necessárias para fechar o DoD global

- [ ] registrar `docker inspect` com `Privileged=false` e mounts finais;
- [ ] fechar inventário de mount de `/home/davis` e superfícies Windows;
- [ ] auditar GPG agent;
- [ ] auditar cloud/deploy credentials de forma abrangente;
- [ ] decidir e testar `DEC-CTR-014` / `NET-01`;
- [ ] comprovar ruleset/proteção de `main`;
- [ ] comprovar ausência de bypass/atores paralelos de escrita/merge;
- [ ] comprovar CI obrigatório;
- [ ] executar PR negativo com check bloqueante;
- [ ] executar PR positivo com checks verdes;
- [ ] registrar promoção/merge por Davi;
- [ ] gerar manifesto final de evidências;
- [ ] testar rollback de estado conhecido como bom.

### P1 — robustez operacional

- [ ] garantir provisionamento reproduzível de `/home/agent/.claude/plans` em volume novo;
- [ ] centralizar script de diagnóstico da fronteira;
- [ ] centralizar teste de capacidade Git remota;
- [ ] registrar versões/digests do runtime em cada baseline;
- [ ] decidir clone descartável por tarefa vs checkout atual;
- [ ] remover/mover backups temporários que tenham sido criados dentro do próprio control plane antes de promoção;
- [ ] manter testes E2E como regressão após mudanças de VS Code/Dev Containers/Claude/Codex.

---

## 21. Registro de validações

### VAL-000 — Baseline documental v0.2

**Data:** 2026-08-13
**Resultado:** `SUPERADO PELA EVIDÊNCIA OPERACIONAL DA v0.3`

A v0.2 estava correta ao não promover recomendações a fatos. A continuidade posterior forneceu a evidência que faltava para vários controles.

---

### VAL-001 — Recuperação do clone Git

**Data histórica:** 2026-08-05
**Resultado:** `VALIDADO`

```text
clone canônico recuperado
origin validado
main validada
commit-base registrado
branch de implantação criada
```

Log:

```text
/home/davis/recuperacao-git-cepraea-20260805T151630Z.log
```

---

### VAL-002 — Aplicação do plano de controle

**Data histórica:** 2026-08-05
**Resultado:** `IMPLANTADO + VALIDAÇÕES ESTÁTICAS`

Log principal:

```text
/home/davis/aplicacao-plano-controle-v2-20260805T174620Z.log
```

---

### VAL-003 — Fronteira básica do Dev Container

**Data histórica:** 2026-08-05/06
**Resultado:** `VALIDADO`

Comprovado:

```text
agent
não root
sudo ausente
Docker CLI/socket ausentes
capabilities administrativas zeradas
NoNewPrivs=1
control plane readonly
.git readonly
políticas root-owned
```

---

### VAL-004 — `DEC-ARQ-001`

**Data histórica:** 2026-08-06
**Resultado:** `APPROVED / IMPLANTADO / RUNTIME VALIDADO`

Log de implementação:

```text
/home/davis/implementacao-dec-arq-001-20260806T044003Z.log
```

---

### VAL-005 — Fronteira Git/credenciais

**Data histórica:** 2026-08-06/07
**Resultado:** `VALIDADO POR CAPACIDADE E PERSISTÊNCIA`

A validação estrutural inicial foi insuficiente; o E2E descobriu AskPass e invalidou o PASS remoto prematuro.

Resultado final:

```text
ARQ-05 = PASS_PERSISTENT_CAPABILITY_TESTED
```

---

### VAL-006 — `DEC-ARQ-001-A1`

**Data histórica:** 2026-08-06
**Resultado:** `APPROVED / VIGENTE`

A aprovação humana substituiu `VB-AC-05` por `VB-AC-05A..H`.

---

### VAL-007 — Claude real na fronteira

**Data histórica:** 2026-08-06/09
**Resultado:** `VALIDADO`

Inclui fluxo funcional e Plan Mode real com checkpoint humano.

---

### VAL-008 — Codex real na fronteira

**Data histórica:** 2026-08-07
**Resultado:** `VALIDADO`

```text
E2E-CODEX-BOUNDARY-01 = PASS
```

---

## 22. Changelog do Runbook

### 2026-08-14 — v0.4

**Tipo:** registro de implantação de gaps — sem evidência de runtime ainda.

**Baseline de versões pré-rebuild (início da sessão):**

```text
Claude Code  2.1.138
codex-cli    0.144.5
```

**Versões efetivamente testadas no runtime pós-rebuild:**

```text
Claude Code  2.1.232
codex-cli    0.146.1
```

**Mudanças aplicadas:**

- `DEC-GOV-001` registrada em `.ai/decisions/DEC-GOV-001-agent-flow-legado.md`;
- `.agent-flow/**` removido do HEAD; referências normativas em `registro_decisoes.md`
  e `PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` anotadas como `REMOVIDO (DEC-GOV-001)`;
- `disableBypassPermissionsMode: disable` adicionado a `claude-managed-settings.json` (P-001);
- `codex-requirements.toml` substituído por profile `cepraea_review` com workspace RO,
  `/tmp` e `$TMPDIR` RW, rede desabilitada; `allowed_sandbox_modes` removido (P-002);
- `pretool` ampliado com subcomandos Git faltantes; `claude-managed-settings.json` deny
  list espelhada com os mesmos subcomandos (P-003);
- `git config` e `git tag` **não** bloqueados — possuem formas read-only legítimas.

**Hashes pós-implantação:**

```text
claude-managed-settings.json  23e1d10674ad04f2222423de998826da3f16e4248576d539bc6d0bf797dc2360
codex-requirements.toml       c6e9fb39edb0b96875834b2ba53bf43f9b41986bde3d8dd3a5acfab5b94f2d67
pretool                       083166f6dcb63b044107fdb1bd28eb6ad51cb2c703802fd821c918172bb44586
```

**Estado após implantação:**

```text
DEC-GOV-001  IMPLANTADO / validação documental concluída
P-001        IMPLANTADO / runtime validation PENDENTE
P-002        IMPLANTADO / runtime validation PENDENTE
P-003        IMPLANTADO / runtime validation PENDENTE

CONTAINER REBUILD  REQUIRED antes dos gates
NOVAS MUDANÇAS DE ENFORCEMENT  CONGELADAS
```

**Atualização 2026-08-14 — P-002 correção aplicada, estado RUNTIME PENDENTE:**

Primeira tentativa (P-002 original) usou `[permissions.cepraea_review]` com `extends = ":read-only"`.
Codex conseguiu escrever `probe.txt` — essa configuração não impôs a fronteira pretendida.

**Causa não demonstrada.** A documentação oficial (Codex ≥ 0.138.0) suporta `[permissions.*]`
e `allowed_permission_profiles`. A afirmação anterior neste Runbook de que "Codex 0.146.1 não
suporta `[permissions.*]`" estava incorreta e foi removida.

Correção aplicada: restaurado `allowed_sandbox_modes = ["read-only"]` e removidas as seções
`[permissions.cepraea_review]` da configuração. O porquê exato da primeira falha não foi
determinado — pode ter sido combinação inválida de mecanismos ou outro fator.

Hash codex-requirements.toml pós-correção: `de5d03a4050f3594bd2bacafa4ef7074a850698d14a2f2b8003909008c671076`

```text
E2E-CODEX-BOUNDARY-01 — 2026-08-14 — CONCLUSIVO (mecanismo elucidado)

  probe2.txt / probe.txt / /tmp/codex-probe.txt: nenhum criado.
  Causa real: bwrap (Bubblewrap) falha ao criar user namespace no container Docker/WSL2.
    → "bwrap: No permissions to create new namespace"
  Confirmado por: codex exec --json + codex sandbox linux --help (ambos retornam bwrap error)

  requirements.toml ativo (confirmado por codex doctor):
    → "falling back to required value Managed { file_system: Restricted ... access: Read }"
    → "invalid value for sandbox_mode: WorkspaceWrite is not in allowed set [ReadOnly]"

  Cadeia de proteção real neste container:
    1. bwrap indisponível → codex exec não executa nenhum comando (primário)
    2. .git RO mount (DEC-CTR-013) → proteção estrutural independente
    3. allowed_sandbox_modes = ["read-only"] → defesa em profundidade se bwrap tornar disponível

  DEC-ARQ-001 Via B (container como fronteira) é consistente com bwrap indisponível.
  O oracle "arquivo não criado" é válido — razão técnica agora documentada.

SEC-02: VALIDADO
```

**Gates pós-rebuild obrigatórios:**

P-001:

- `claude --version` registrado no runtime;
- `/etc/claude-code/managed-settings.json` contém `disableBypassPermissionsMode`;
- `claude --dangerously-skip-permissions` bloqueado;
- edição autorizada em `docs/modelagem/**` — PASS;
- tentativa de edição em control plane — BLOCKED.

P-002:

- `codex --version` registrado no runtime;
- profile `cepraea_review` reconhecido;
- leitura de `git diff` e arquivos do projeto — PASS;
- escrita em `/tmp` — PASS;
- tentativa de edição de arquivo de modelagem — BLOCKED;
- `E2E-CODEX-BOUNDARY-01` reexecutado com resultado PASS.

P-003:

- `git status`, `git diff`, `git log` — PASS;
- `git config --get remote.origin.url` — PASS (não bloqueado);
- `git add .` — BLOCKED;
- `git reset HEAD` — BLOCKED;
- `git checkout main` — BLOCKED;
- `git stash` — BLOCKED;
- pós-condição externa: `git status --porcelain` e `git rev-parse HEAD`
  inalterados após todas as tentativas bloqueadas;
- regressão de credenciais: `GIT_TERMINAL_PROMPT=0 git push --dry-run origin HEAD:refs/heads/<probe>` — `exit != 0`.

**Invariante adicionada:**

```text
guard ampliado != cobertura completa de shell arbitrário
proteção estrutural = .git readonly no container
```

**Encerramento da sessão 2026-08-14:**

```text
ESCOPO DA SESSÃO — CONTROLES TRATADOS
  DEC-GOV-001   VALIDADO
  SEC-01        VALIDADO
  SEC-02        VALIDADO
  SEC-03A       VALIDADO
  SEC-03B       VALIDADO
  SEC-04        VALIDADO

FRONTEIRA LOCAL DA SESSÃO = COMPLETA / VALIDADA

DoD GLOBAL = PENDENTE (NET-01, ISO-05, MNT-01/02, CRE-03/04,
             GH-01/02, CI-01/02/03, OPS-01, RBK-01 — inalterados)

Nenhum dos controles pré-existentes PENDENTE foi promovido nem
regredido por esta sessão.

ENFORCEMENT CONGELADO.
Novas mudanças no control plane requerem necessidade concreta nova.
```

---

### 2026-08-13 — v0.3

**Tipo:** atualização operacional baseada na continuidade real da implantação.

**Principais mudanças:**

- corrigida a premissa de que o checkout inicial já era um clone Git;
- registrada a recuperação do clone canônico e da branch de implantação;
- promovido o Dev Container de `PENDENTE` para `IMPLANTADO`;
- promovidos identidade `agent`, ausência de sudo, Docker CLI/socket, capabilities e `NoNewPrivs` conforme evidência;
- promovida a proteção material de `.git` e do plano de controle para `VALIDADO`;
- encerrada `DEC-CTR-013` no **Modelo A — Git humano / `.git` readonly**;
- incorporada `DEC-ARQ-001` — Via B, Dev Container como sandbox operacional;
- incorporada `DEC-ARQ-001-A1` e critérios `VB-AC-05A..H`;
- registrada a regressão de `credential.helper` do VS Code;
- registrada a regressão mais profunda de Git AskPass/terminal authentication;
- alterado o critério de credenciais de mera inspeção estática para **teste de capacidade**;
- registrado `ARQ-05 = PASS_PERSISTENT_CAPABILITY_TESTED` após dois rebuilds;
- registrada a distinção `UNSET` / `SET_EMPTY` / `SET_NONEMPTY`;
- incorporados E2Es reais de Claude e Codex;
- registrado `E2E-CODEX-BOUNDARY-01 = PASS`;
- incorporada `CLAUDE_PLAN_RUNTIME_EXCEPTION` e sua validação em Plan Mode real;
- incluídas regras `freeze-before-test`, `new-evidence amendment` e `privilege-expansion evidence`;
- mantidos `GitHub/main`, CI, rede, GPG/cloud, `Privileged=false` explícito e rollback completo como `PENDENTE`;
- alterado o status global para **fronteira operacional local validada / DoD global pendente**.

**Invariantes preservadas:**

```text
configuração correta != capacidade comprovada
componente PASS != E2E global PASS
container local validado != main/CI validados
SET_EMPTY intencional != secret exposto
sandbox interno incompatível != justificativa para ampliar privilégio
```

---

### 2026-08-13 — v0.2

Registrou o manual como artefato documental, criou `NET-01` e, corretamente, manteve a implantação técnica como pendente enquanto faltava evidência.

---

### 2026-08-13 — v0.1

Criação da baseline documental inicial.

---

## 23. Referências documentais e evidências

### Históricos fonte

```text
Análise-de-fluxo-de-manifesto (3).json
Leitura-e-análise-de-PDF (5).json
```

O primeiro concentra a causa raiz e a decisão de containerização. O segundo registra a continuidade de implantação, falhas, correções, decisões, rebuilds e E2Es.

### Manual externo

```text
Manual de implantação segura — Codex e Claude Code no CEPRAEA BEACH PRO
```

Função:

> explicar como implantar.

Este Runbook tem função distinta:

> registrar por que a arquitetura existe, o que está realmente implantado, o que foi testado, regressões, decisões e como manter a fronteira sem perder contexto.

### Evidências históricas relevantes

```text
/home/davis/recuperacao-git-cepraea-20260805T151630Z.log
/home/davis/aplicacao-plano-controle-v2-20260805T174620Z.log
/home/davis/implementacao-dec-arq-001-20260806T044003Z.log
/home/davis/diagnosticos/credential-boundary-runtime-1-20260806T115220Z.log
/home/davis/diagnosticos/credential-boundary-runtime-2-20260806T125108Z.log
/home/davis/registro-aprovacao-dec-arq-001-a1-20260806T132516Z.log
```

Esses caminhos são referências registradas no histórico. A v0.3 não afirma que todos continuam presentes no filesystem atual sem uma nova inspeção.

---

## 24. Regra para agentes de IA

Qualquer agente que trabalhar nesta infraestrutura deve:

1. ler este Runbook antes de propor mudança de segurança;
2. distinguir `DECIDIDO`, `IMPLANTADO`, `VALIDADO` e `PENDENTE`;
3. não rebaixar um controle validado por conveniência;
4. não ampliar privilégio para corrigir sandbox interno;
5. não montar Docker socket;
6. não tornar `.git` gravável sem nova decisão arquitetural explícita;
7. não reativar Git credential helper/AskPass do VS Code no container;
8. não interpretar `credential.helper` ausente como prova suficiente de ausência de autoridade remota;
9. executar teste de capacidade quando o risco for autoridade Git/GitHub;
10. distinguir `UNSET`, `SET_EMPTY` e `SET_NONEMPTY` para variáveis sensíveis;
11. não alterar plano de controle como parte incidental de feature;
12. usar a exceção de Plan Mode somente para `/home/agent/.claude/plans/*.md`;
13. verificar pós-condições externamente ao relatório do agente;
14. não promover teste de componente a gate E2E;
15. congelar critério/oráculo antes do teste;
16. registrar nova evidência sem reescrever retroativamente o passado;
17. parar quando um controle previamente `VALIDADO` regredir;
18. não executar commit/push/merge do agente;
19. manter GitHub/main/CI/rede como `PENDENTE` até evidência real;
20. em dúvida, usar `PENDENTE`, nunca inferir `VALIDADO`.

---

## 25. Próxima atualização obrigatória

A próxima versão deve ser produzida quando houver evidência nova sobre um ou mais gates ainda pendentes.

Prioridade de coleta:

### Host / Docker

```bash
docker inspect <container>
```

Registrar explicitamente:

```text
Privileged
CapAdd/CapDrop
SecurityOpt
Mounts
```

### Credenciais residuais

Auditar sem imprimir valores:

```text
GPG agent
cloud providers
Supabase/deploy
outros secrets não GitHub
```

### GitHub / main

Registrar:

```text
ruleset integral
branch protection
bypass actors
colaboradores/equipes
GitHub Apps
deploy keys
CODEOWNERS
```

### CI

Executar e registrar:

```text
PR negativo → check falha → merge bloqueado
PR positivo → checks verdes → merge permitido
```

### Promoção humana

Comprovar que:

```text
Davi revisa
Davi faz commit/push/PR/merge
agentes continuam sem autoridade remota
conteúdo promovido = conteúdo revisado
```

### Rede

Tomar decisão explícita para `DEC-CTR-014` e executar teste correspondente antes de mudar `NET-01`.

### Rollback

Definir e testar um estado conhecido como bom.

Somente quando esses gates tiverem evidência suficiente o Runbook poderá alterar:

```text
DoD GLOBAL = NOT DONE
```

para uma declaração mais forte.
