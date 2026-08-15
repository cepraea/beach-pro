# Human-Governed Dual-Agent SDLC Architecture - Arquivos

>Ao todo são **nove arquivos** para materializar a arquitetura. O conteúdo abaixo segue a arquitetura arc42 revisada: humano controla Git/decisões, Claude produz, Codex revisa, `.git` permanece utilizável pelo humano e o corpus permanece protegido.

Há uma distinção importante:

- os cinco primeiros arquivos definem **comportamento e governança**;
- os quatro últimos implementam **enforcement e verificação técnica**.

***

## 1. `AGENT_POLICY.md`

É a constituição comum. Deve ser pequeno e relativamente estável.

```markdown
# CEPRAEA-BEACH-PRO — Agent Policy

## 1. Scope

Esta política governa agentes de IA utilizados no SDLC do
CEPRAEA-BEACH-PRO.

Ela não governa o runtime da aplicação.

Arquitetura:

HUMANO
→ CLAUDE CODE / EXECUTOR
→ validações determinísticas
→ git diff
→ CODEX / REVIEWER
→ HUMANO
→ Git

## 2. Human Authority

Davi é a autoridade final sobre:

- significado do domínio;
- decisões materiais;
- promoção de conhecimento;
- alterações desta política;
- Git privilegiado;
- merge;
- release;
- deploy;
- produção.

Nenhum agente pode substituir uma decisão humana quando ela for
exigida pelo processo.

## 3. Separation of Duties

Produção, revisão e aprovação são funções distintas.

### EXECUTOR

O EXECUTOR produz alterações.

Agente padrão:

CLAUDE_CODE

O EXECUTOR não:

- aprova o próprio trabalho;
- executa review formal do próprio trabalho;
- faz commit;
- faz push;
- faz merge;
- faz rebase;
- altera branches;
- altera tags;
- publica releases;
- faz deploy;
- contorna permissões ou sandbox.

###### REVIEWER

O REVIEWER verifica independentemente as alterações produzidas.

Agente padrão:

CODEX

O REVIEWER não:

- corrige silenciosamente os artefatos revisados;
- modifica o working tree durante review normal;
- promove conhecimento;
- substitui aprovação humana;
- faz Git privilegiado;
- faz deploy.

Verdicts permitidos:

PASS
FAIL
HUMAN_DECISION_REQUIRED

#### 4. Git Authority

Git é a state machine operacional do fluxo.

Operações privilegiadas pertencem ao humano, incluindo:

- git add;
- git commit;
- git push;
- git pull;
- git merge;
- git rebase;
- git cherry-pick;
- git reset;
- git restore;
- git checkout;
- git switch;
- git branch quando altera refs;
- git tag quando altera refs;
- git worktree;
- operações equivalentes que alterem refs, index ou histórico.

Agentes podem utilizar operações de inspeção necessárias, por exemplo:

- git status;
- git diff;
- git log;
- git show;
- git rev-parse;
- git ls-files.

#### 5. Protected Operational Sources

SOURCE_ROOT:

`.drive/CEPRAEA BEACH PRO/**`

SOURCE_ROOT é READ_ONLY.

Agentes podem ler fontes quando necessário à tarefa autorizada.

Agentes nunca modificam fontes operacionais.

Read-only protege integridade, não confidencialidade.

PII não deve ser:

- copiada desnecessariamente para prompts;
- reproduzida integralmente em documentação;
- persistida em relatórios operacionais sem necessidade.

#### 6. Production Secrets

Secrets de produção não pertencem ao Dev Container.

Agentes não devem receber:

- tokens de produção;
- service-role keys;
- private keys;
- credenciais de deploy;
- credenciais privilegiadas de banco;
- tokens Git privilegiados.

Se uma tarefa exigir credencial que não está disponível:

BLOCKED / HUMAN_ACTION_REQUIRED.

Nunca procurar bypass.

#### 7. Protected Control Plane

Agentes não modificam sem decisão humana explícita:

- `AGENT_POLICY.md`;
- `CLAUDE.md`;
- `AGENTS.md`;
- `.devcontainer/**`;
- `.claude/**`;
- `.codex/**`;
- configurações de CI/CD;
- hooks/policies administrados;
- secrets.

#### 8. Modeling Rules

Para modelagem CEPRAEA:

fonte real
→ evidência
→ conhecimento
→ modelo canônico
→ modelo lógico somente quando maduro

Nunca inferir mecanicamente:

arquivo = entidade
pasta = bounded context
aba = aggregate
coluna = atributo canônico

Distinções obrigatórias incluem:

availability != attendance
athlete registration != team membership
call-up != actual participation
scheduled match != realized result
competition != game
current rule != historical fact
authenticated user != athlete

Ambiguidades devem ser registradas.

Não inventar conhecimento para preencher lacunas.

#### 9. Deterministic First

Antes de revisão por IA, o EXECUTOR executa os validadores
determinísticos exigidos pela tarefa, por exemplo:

- lint;
- typecheck;
- unit tests;
- integration tests;
- schema validation;
- fixture validation;
- reference validation;
- git diff --check.

O REVIEWER reexecuta somente os checks necessários para revisão
independente, proporcionalmente ao risco e aos findings.

#### 10. No Bypass

Se:

ação necessária
+
permissão inexistente

então:

BLOCKED / HUMAN_ACTION_REQUIRED

Nunca alterar infraestrutura, policy, permissões ou controles para
contornar a restrição.

#### 11. Persistent Evidence

Persistir quando material:

- código;
- testes;
- evidências;
- regras;
- modelos;
- decisões;
- commits;
- reviews de segurança relevantes.

Não é obrigatório persistir:

- cada comando executado;
- cada turno entre agentes;
- cada review trivial;
- state machine paralela ao Git.

#### 12. Escalation

Fluxo normal:

CLAUDE
→ CODEX
→ HUMANO

ChatGPT ou Gemini entram somente quando houver:

- divergência material;
- decisão arquitetural;
- problema semântico relevante;
- necessidade de terceira opinião.

Eles não adquirem autoridade de aprovação.
```

---

## 2. `CLAUDE.md`

Deve ser **adaptador**, não duplicação da política.

Claude Code trata as permission rules como enforcement da ferramenta, enquanto instruções em `CLAUDE.md` apenas influenciam o comportamento do modelo; por isso este arquivo permanece intencionalmente curto. ([Claude][1])

```markdown
## CEPRAEA-BEACH-PRO — Claude Code

Leia e cumpra integralmente:

`AGENT_POLICY.md`

Seu papel padrão neste repositório é:

EXECUTOR

#### Antes de executar

1. identifique exatamente a tarefa solicitada pelo humano;
2. leia apenas os documentos normativos necessários à tarefa;
3. para modelagem, consulte:
   `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`;
4. confira a branch atual;
5. não execute trabalho em `main` ou `master`;
6. inspecione `git status`;
7. identifique as validações exigidas.

#### Durante a execução

Produza somente alterações necessárias à tarefa atual.

Não avance automaticamente para a próxima AC/SEM/SYN.

Nunca modifique:

- `.drive/CEPRAEA BEACH PRO/**`;
- `AGENT_POLICY.md`;
- `CLAUDE.md`;
- `AGENTS.md`;
- `.devcontainer/**`;
- `.claude/**`;
- `.codex/**`;

salvo instrução humana explícita destinada especificamente a alterar
a infraestrutura ou política.

Nunca execute Git privilegiado.

#### Validação

Antes de finalizar:

1. execute os validadores exigidos;
2. corrija erros mecânicos causados por sua alteração;
3. rode `git diff --check`;
4. inspecione `git diff`;
5. inspecione `git status`;
6. confirme que SOURCE_ROOT não foi alterado.

#### Handoff

Apresente de forma factual:

- tarefa executada;
- arquivos alterados;
- validações executadas;
- resultados;
- limitações;
- bloqueios;
- pontos que merecem revisão.

Não forneça narrativa de raciocínio privado.

Finalize exclusivamente com:

READY_FOR_REVIEW

ou:

BLOCKED
```

---

## 3. `AGENTS.md`

Esse é o adaptador permanente do Codex.

Codex suporta configuração project-scoped em `.codex/config.toml`; para revisão queremos que a instrução de papel e a sandbox trabalhem juntas. ([OpenAI Developers][2])

```markdown
## CEPRAEA-BEACH-PRO — Codex

Leia e cumpra integralmente:

`AGENT_POLICY.md`

Quando solicitado a revisar, seu papel é:

REVIEWER

Você não é o EXECUTOR.

#### Review source

A unidade primária sob revisão é:

`git diff`

complementada pelos arquivos relacionados e pelos critérios da tarefa
informada pelo humano.

Para modelagem, use como fonte normativa:

`docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`

#### Procedure

1. confirme a tarefa/AC/SEM/SYN sob revisão;
2. inspecione `git status`;
3. inspecione o `git diff` completo;
4. leia os artefatos relacionados;
5. identifique os critérios de aceite/DONE aplicáveis;
6. reexecute checks determinísticos relevantes quando útil;
7. procure regressões;
8. tente refutar conclusões materiais;
9. verifique evidência, rastreabilidade e estados epistemológicos;
10. procure inferências mais fortes que suas evidências;
11. confirme que fontes protegidas não foram modificadas;
12. confirme que nenhuma decisão humana foi simulada pelo Executor.

#### Independence

Durante o review:

- não edite o projeto;
- não aplique patches;
- não corrija findings;
- não altere Git;
- não faça commit;
- não avance para a próxima ação.

Um erro encontrado gera finding, não correção silenciosa.

#### Findings

Quando necessário, use:

CRITICAL
HIGH
MEDIUM
LOW

Todo finding deve conter:

- problema;
- evidência;
- impacto;
- correção requerida.

#### Verdict

Finalize exclusivamente com um dos seguintes:

PASS

FAIL

HUMAN_DECISION_REQUIRED
```

---

## 4. `.codex/config.toml`

Aqui vale usar um **permission profile customizado**. A configuração atual do Codex permite definir `:workspace_roots` como read, `/tmp` como write e rede desativada, exatamente o que queremos para o Reviewer. ([OpenAI Developers][3])

```toml
## CEPRAEA-BEACH-PRO — Codex Reviewer Policy

approval_policy = "never"
default_permissions = "cepraea-review"

## O Reviewer precisa conseguir ler binários e bibliotecas mínimas
## para executar ferramentas locais.
[permissions.cepraea-review.filesystem]
":root" = "deny"
":minimal" = "read"

## Projeto sob revisão: somente leitura.
[permissions.cepraea-review.filesystem.":workspace_roots"]
"." = "read"

## Escrita efêmera é permitida para testes e ferramentas que
## inevitavelmente usam diretórios temporários.
[permissions.cepraea-review.filesystem]
":tmpdir" = "write"
":slash_tmp" = "write"

## Review normal não necessita de rede.
[permissions.cepraea-review.network]
enabled = false
```

Eu usaria **esse profile em vez de simplesmente `sandbox_mode = "read-only"`** porque o read-only puro também restringe execução de comandos que precisam escrever temporários. Os permission profiles atuais foram feitos justamente para permitir boundaries mais granulares. ([OpenAI Developers][4])

> Observação: se a versão instalada do Codex ainda não reconhecer os permission profiles customizados, o fallback operacional é `sandbox_mode = "read-only"` até a versão ser atualizada. Não use `danger-full-access`.

---

## 5. `.devcontainer/security/claude-managed-settings.json`

Esse é o arquivo **versionado**. O Dockerfile o instala como:

```text
/etc/claude-code/managed-settings.json
```

Managed settings têm precedência sobre configuração local e podem impor permissions, hooks e bloqueio do modo bypass. ([Claude][5])

As regras `Edit(path)` são as corretas para proteger ferramentas internas de escrita; `Write(path)` não é a regra adequada para paths nas versões atuais. ([Claude][1])

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  "disableBypassPermissionsMode": "disable",

  "permissions": {
    "deny": [
      "Read(//workspaces/cepraea-beach-pro/.env)",
      "Read(//workspaces/cepraea-beach-pro/.env.*)",
      "Read(//workspaces/cepraea-beach-pro/secrets/**)",

      "Edit(//workspaces/cepraea-beach-pro/AGENT_POLICY.md)",
      "Edit(//workspaces/cepraea-beach-pro/CLAUDE.md)",
      "Edit(//workspaces/cepraea-beach-pro/AGENTS.md)",

      "Edit(//workspaces/cepraea-beach-pro/.devcontainer/**)",
      "Edit(//workspaces/cepraea-beach-pro/.claude/**)",
      "Edit(//workspaces/cepraea-beach-pro/.codex/**)",
      "Edit(//workspaces/cepraea-beach-pro/.drive/**)",

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
      "Bash(git branch *)",
      "Bash(git tag *)",
      "Bash(git worktree *)",
      "Bash(git stash *)",
      "Bash(git clean *)",
      "Bash(git rm *)",
      "Bash(git config *)",
      "Bash(git update-ref *)"
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

Claude Code é consciente de operadores compostos como `&&`, `||`, `;` e pipes ao avaliar regras Bash, o que torna suas rules melhores do que simples comparação textual. Ainda assim, padrões Bash não são uma sandbox completa, por isso mantemos o hook e o perfil HARDENED como defense-in-depth. ([Claude][1])

###### Quando o HARDENED for aprovado

**Só depois do acceptance test do nested sandbox**, acrescentaria ao mesmo JSON:

```json
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
        "/workspaces/cepraea-beach-pro/.drive/CEPRAEA BEACH PRO",
        "/workspaces/cepraea-beach-pro/AGENT_POLICY.md",
        "/workspaces/cepraea-beach-pro/CLAUDE.md",
        "/workspaces/cepraea-beach-pro/AGENTS.md"
      ]
    },

    "network": {
      "strictAllowlist": true,
      "allowedDomains": []
    }
  }
}
```

Não colocaria esse bloco no BASE antes de comprovar que o nested sandbox funciona dentro do Dev Container. A própria Anthropic distingue o Dev Container da sandbox Bash interna e documenta `failIfUnavailable` como hard gate quando sandboxing realmente é requisito. ([Claude][6])

---

## 6. `.devcontainer/security/claude-guard`

Aqui eu usaria Python pelo parsing mais limpo.

Ele **não é a fronteira de segurança**. O propósito é identificar rapidamente uma tentativa direta de usar Git para mutação e devolver uma mensagem clara.

```python
##!/usr/bin/env python3

import json
import os
import shlex
import sys


READ_ONLY_GIT_SUBCOMMANDS = {
    "status",
    "diff",
    "log",
    "show",
    "rev-parse",
    "ls-files",
    "describe",
    "version",
    "help",
}


def deny(reason: str) -> None:
    print(f"[CEPRAEA Claude Guard] BLOCKED: {reason}", file=sys.stderr)
    sys.exit(2)


def tokenize(command: str):
    try:
        lexer = shlex.shlex(
            command,
            posix=True,
            punctuation_chars=";&|()",
        )
        lexer.whitespace_split = True
        lexer.commenters = ""
        return list(lexer)
    except ValueError:
        ## O guard é fail-fast. Se há Git e não conseguimos interpretar
        ## o comando com segurança, não executamos.
        if "git" in command.lower():
            deny("comando envolvendo Git não pôde ser interpretado.")
        return []


def git_subcommand(tokens, git_index):
    i = git_index + 1

    while i < len(tokens):
        token = tokens[i]

        ## Separadores de shell antes do subcomando tornam a forma suspeita.
        if token in {";", "&&", "||", "|", "|&", "&", "(", ")"}:
            return None

        ## Opções globais que consomem o argumento seguinte.
        if token in {
            "-c",
            "-C",
            "--git-dir",
            "--work-tree",
            "--namespace",
            "--exec-path",
        }:
            i += 2
            continue

        ## Formas --option=value.
        if token.startswith(
            (
                "--git-dir=",
                "--work-tree=",
                "--namespace=",
                "--exec-path=",
            )
        ):
            i += 1
            continue

        ## Outras flags globais.
        if token.startswith("-"):
            i += 1
            continue

        return token

    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        ## Erro do hook não deve inventar uma decisão sobre ferramenta que
        ## não conseguimos identificar.
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    command = (
        payload.get("tool_input", {}).get("command", "")
        or ""
    )

    lower = command.lower()

    ## Wrappers óbvios com Git embutido: fail-fast.
    suspicious_wrappers = (
        "sh -c",
        "bash -c",
        "zsh -c",
        "eval ",
        "python -c",
        "python3 -c",
        "node -e",
    )

    if "git" in lower and any(x in lower for x in suspicious_wrappers):
        deny("execução indireta envolvendo Git não é permitida ao Executor.")

    tokens = tokenize(command)

    for i, token in enumerate(tokens):
        executable = os.path.basename(token)

        if executable != "git":
            continue

        subcommand = git_subcommand(tokens, i)

        if not subcommand:
            deny("comando Git não reconhecido como somente leitura.")

        if subcommand not in READ_ONLY_GIT_SUBCOMMANDS:
            deny(
                f"'git {subcommand}' não é autorizado ao EXECUTOR. "
                "Git privilegiado pertence ao humano."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
```

Os hooks `PreToolUse` recebem JSON por `stdin`, incluindo `tool_input.command`, e `exit 2` bloqueia a tool call. Isso é comportamento documentado atualmente pelo Claude Code. ([Claude][7])

Esse script deliberadamente **não promete impedir todas as execuções indiretas possíveis**. O objetivo dele é fail-fast; o isolamento estrutural forte pertence à sandbox HARDENED quando habilitada.

---

## 7. `.devcontainer/Dockerfile`

Este é o único arquivo em que eu **não substituiria cegamente o conteúdo atual**, porque precisamos preservar a imagem e toolchain reais do CEPRAEA.

O trecho de arquitetura que deve ser incorporado ao Dockerfile existente é:

```dockerfile
## ------------------------------------------------------------
## CEPRAEA agent security layer
## Incorporar ao Dockerfile EXISTENTE do projeto.
## Não substituir a toolchain atual apenas por este fragmento.
## ------------------------------------------------------------

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p \
    /etc/claude-code \
    /usr/local/lib/cepraea

COPY .devcontainer/security/claude-managed-settings.json \
    /etc/claude-code/managed-settings.json

COPY .devcontainer/security/claude-guard \
    /usr/local/lib/cepraea/claude-guard

RUN chown root:root \
        /etc/claude-code/managed-settings.json \
        /usr/local/lib/cepraea/claude-guard \
    && chmod 0444 \
        /etc/claude-code/managed-settings.json \
    && chmod 0555 \
        /usr/local/lib/cepraea/claude-guard

## Voltar para o usuário não-root usado pelo projeto.
USER vscode
```

Se o usuário atual do container não for `vscode`, a última linha deve usar **o usuário não-root já existente**, não criar outro arbitrariamente. VS Code recomenda desenvolvimento com usuário não-root e oferece `remoteUser`/`containerUser` para isso. ([Visual Studio Code][8])

###### Só para HARDENED

Se o acceptance test demonstrar compatibilidade:

```dockerfile
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bubblewrap \
        socat \
    && rm -rf /var/lib/apt/lists/*

USER vscode
```

Não instalaria isso como requisito funcional do BASE.

---

## 8. `.devcontainer/devcontainer.json`

Novamente: **mesclar com o arquivo existente**, não apagar extensões, ports ou configuração da aplicação.

O núcleo obrigatório da arquitetura é:

```jsonc
{
  "name": "CEPRAEA-BEACH-PRO",

  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },

  "workspaceFolder": "/workspaces/cepraea-beach-pro",

  "remoteUser": "vscode",
  "containerUser": "vscode",

  "mounts": [
    "source=${localWorkspaceFolder}/.drive/CEPRAEA BEACH PRO,target=${containerWorkspaceFolder}/.drive/CEPRAEA BEACH PRO,type=bind,readonly"
  ],

  "postCreateCommand": "bash .devcontainer/scripts/verify-agent-environment.sh"
}
```

`${containerWorkspaceFolder}` é uma variável suportada pelos Dev Containers, e `mounts` pode criar mounts direcionados dentro do workspace. ([Visual Studio Code][9])

###### Não adicionar

```jsonc
"privileged": true
```

nem mount de:

```text
/var/run/docker.sock
```

a menos que uma necessidade futura comprovada gere nova decisão arquitetural.

Também **não** sobreponha `.git` como read-only. O Dev Container é o ambiente completo do VS Code, e Git dentro dele deve continuar funcional para o humano. VS Code também suporta o uso das credenciais Git do host dentro do container. ([Visual Studio Code][10])

---

## 9. `.devcontainer/scripts/verify-agent-environment.sh`

Esse script verifica o **perfil BASE**. Não deve fingir verificar aquilo que só pode ser comprovado interativamente.

```bash
##!/usr/bin/env bash

set -u

FAILURES=0
WARNINGS=0

REPO="/workspaces/cepraea-beach-pro"
SOURCE_ROOT="$REPO/.drive/CEPRAEA BEACH PRO"
CLAUDE_POLICY="/etc/claude-code/managed-settings.json"
CLAUDE_GUARD="/usr/local/lib/cepraea/claude-guard"
CODEX_CONFIG="$REPO/.codex/config.toml"


pass() {
    printf 'PASS  %s\n' "$1"
}


fail() {
    printf 'FAIL  %s\n' "$1"
    FAILURES=$((FAILURES + 1))
}


warn() {
    printf 'WARN  %s\n' "$1"
    WARNINGS=$((WARNINGS + 1))
}


echo "CEPRAEA Agent Environment Verification"
echo "======================================="


## ------------------------------------------------------------
## User
## ------------------------------------------------------------

if [ "$(id -u)" -ne 0 ]; then
    pass "container session is non-root"
else
    fail "container session is running as root"
fi


## ------------------------------------------------------------
## Docker socket
## ------------------------------------------------------------

if [ ! -S /var/run/docker.sock ]; then
    pass "Docker socket is not mounted"
else
    fail "Docker socket is available inside the container"
fi


## ------------------------------------------------------------
## Repository / Git
## ------------------------------------------------------------

if cd "$REPO" 2>/dev/null; then
    pass "repository is accessible"
else
    fail "repository is not accessible at $REPO"
fi


if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    pass "Git repository detected"
else
    fail "Git repository not detected"
fi


GIT_DIR="$(git rev-parse --git-dir 2>/dev/null || true)"

if [ -n "$GIT_DIR" ]; then
    case "$GIT_DIR" in
        /*)
            RESOLVED_GIT_DIR="$GIT_DIR"
            ;;
        *)
            RESOLVED_GIT_DIR="$REPO/$GIT_DIR"
            ;;
    esac

    if [ -w "$RESOLVED_GIT_DIR" ]; then
        pass ".git is writable for the human VS Code session"
    else
        fail ".git is not writable; Source Control/commit may be broken"
    fi
else
    fail "unable to resolve Git directory"
fi


## ------------------------------------------------------------
## SOURCE_ROOT
## ------------------------------------------------------------

if [ -d "$SOURCE_ROOT" ]; then
    pass "SOURCE_ROOT exists"
else
    fail "SOURCE_ROOT not found"
fi


if command -v findmnt >/dev/null 2>&1 && [ -e "$SOURCE_ROOT" ]; then
    OPTIONS="$(findmnt -T "$SOURCE_ROOT" -n -o OPTIONS 2>/dev/null || true)"

    if printf '%s' "$OPTIONS" | tr ',' '\n' | grep -qx 'ro'; then
        pass "SOURCE_ROOT is mounted read-only"
    else
        fail "SOURCE_ROOT is not confirmed read-only"
    fi
else
    if [ -w "$SOURCE_ROOT" ]; then
        fail "SOURCE_ROOT appears writable"
    else
        pass "SOURCE_ROOT is not writable by current user"
    fi
fi


## ------------------------------------------------------------
## Claude managed policy
## ------------------------------------------------------------

if [ -f "$CLAUDE_POLICY" ]; then
    pass "Claude managed settings installed"
else
    fail "Claude managed settings missing"
fi


if [ -x "$CLAUDE_GUARD" ]; then
    pass "Claude guard installed and executable"
else
    fail "Claude guard missing or not executable"
fi


if [ -f "$CLAUDE_POLICY" ]; then
    OWNER="$(stat -c '%U' "$CLAUDE_POLICY" 2>/dev/null || true)"
    MODE="$(stat -c '%a' "$CLAUDE_POLICY" 2>/dev/null || true)"

    if [ "$OWNER" = "root" ]; then
        pass "Claude managed settings owned by root"
    else
        fail "Claude managed settings are not root-owned"
    fi

    if [ "$MODE" = "444" ]; then
        pass "Claude managed settings mode is 0444"
    else
        warn "Claude managed settings mode is $MODE; expected 444"
    fi
fi


## ------------------------------------------------------------
## Codex
## ------------------------------------------------------------

if [ -f "$CODEX_CONFIG" ]; then
    pass "Codex project config exists"
else
    fail "Codex project config missing"
fi


## ------------------------------------------------------------
## Obvious production credentials
## ------------------------------------------------------------

FORBIDDEN_VARS=(
    "GITHUB_TOKEN"
    "GH_TOKEN"
    "SUPABASE_SERVICE_ROLE_KEY"
    "VERCEL_TOKEN"
)

for name in "${FORBIDDEN_VARS[@]}"; do
    if [ -n "${!name:-}" ]; then
        fail "forbidden privileged credential is present: $name"
    else
        pass "credential not exposed: $name"
    fi
done


## ------------------------------------------------------------
## Result
## ------------------------------------------------------------

echo
echo "Failures: $FAILURES"
echo "Warnings: $WARNINGS"

if [ "$FAILURES" -eq 0 ]; then
    echo "BASE_CONTAINER_CHECK=PASS"
    exit 0
else
    echo "BASE_CONTAINER_CHECK=FAIL"
    exit 1
fi
```

**Não colocar CT-06/CT-08 automaticamente nesse script**, porque testar “Claude não consegue commit” e “Codex não consegue editar” exige executar **o processo real do agente sob sua política**, não simplesmente testar permissões do usuário `vscode`.

***

## 10. RUNBOOKS

Abaixo, a proposta B consolidada segundo a arquitetura real e o guia de autoria anexado. O guia exige português brasileiro, *sentence case*, linguagem direta, fidelidade às fontes canônicas e diretivas positivas restritivas.

# Arquitetura de runbooks do CEPRAEA BEACH PRO

## Estado da decisão

**A arquitetura DEVE adotar:**

- manter o runbook humano do fluxo;
- criar uma biblioteca especializada de runbooks;
- separar runbooks do Executor e do Reviewer;
- compartilhar apenas procedimentos realmente comuns;
- manter Git como state machine operacional;
- preservar `CLAUDE.md` e `AGENTS.md` como adaptadores permanentes dos papéis;
- utilizar runbooks exclusivamente para procedimentos especializados por classe de operação.

**Estado de implantação:**
<!-- PENDENTE DE EVIDÊNCIA -->

>A implantação somente poderá ser considerada comprovada depois que os arquivos forem materializados, integrados ao repositório e validados no fluxo real.

## Objetivo

A biblioteca de runbooks DEVE transformar classes recorrentes de operação em procedimentos explícitos, reutilizáveis e verificáveis.

Cada runbook DEVE complementar as políticas e instruções permanentes existentes.

O runbook DEVE responder:

> Dada esta classe específica de operação, qual procedimento o papel atual deve executar?

A biblioteca DEVE preservar a separação entre:

- autoridade;
- política;
- papel;
- procedimento;
- enforcement;
- evidência;
- decisão final.

## Posição arquitetural

A arquitetura DEVE permanecer organizada da seguinte forma:

```txt
AUTORIDADE HUMANA
        │
        ▼
AGENT_POLICY.md
invariantes e autoridade comuns
        │
        ├───────────────────────────┐
        ▼                           ▼
CLAUDE.md                       AGENTS.md
EXECUTOR                        REVIEWER
procedimento transversal        procedimento transversal
        │                           │
        ▼                           ▼
runbooks/executor/              runbooks/reviewer/
procedimentos                   procedimentos
especializados                  especializados
        │                           │
        └────────────┬──────────────┘
                     │ consulta
                     ▼
         fontes normativas aplicáveis
              ├── docs/modelagem/
              └── .drive/CEPRAEA BEACH PRO/
                     │
                     ▼
                  tarefa
                     │
                     ▼
              operação concreta
                     │
             ┌───────┴────────┐
             ▼                ▼
        working tree       evidências
        + git diff         materiais
             │                │
             └───────┬────────┘
                     ▼
                  REVIEW
                     │
                     ▼
       PASS | FAIL | HUMAN_DECISION_REQUIRED
                     │
                     ▼
                   HUMANO
                     │
                     ▼
            stage / commit / promoção
```

O Dev Container, as permissions, os guards e as configurações dos agentes permanecem como mecanismos de enforcement transversal.

## Estrutura física

A estrutura DEVE ser materializada desta forma:

cepraea-beach-pro/
│
├── AGENT_POLICY.md
│     └── invariantes e autoridade comuns
│
├── CLAUDE.md
│     └── papel EXECUTOR
│         + procedimento transversal permanente
│
├── AGENTS.md
│     └── papel REVIEWER
│         + procedimento transversal permanente
│
├── runbooks/
│   │
│   ├── README.md
│   │     └── catálogo, seleção, aplicabilidade e precedência
│   │
│   ├── shared/
│   │   ├── RB-SHARED-001-repository-baseline.md
│   │   ├── RB-SHARED-002-evidence.md
│   │   └── RB-SHARED-003-failure-states.md
│   │
│   ├── executor/
│   │   ├── RB-EXEC-001-code-change.md
│   │   ├── RB-EXEC-002-database-change.md
│   │   ├── RB-EXEC-003-documentation-change.md
│   │   └── RB-EXEC-004-dependency-change.md
│   │
│   └── reviewer/
│       ├── RB-REV-001-code-review.md
│       ├── RB-REV-002-database-review.md
│       ├── RB-REV-003-documentation-review.md
│       └── RB-REV-004-evidence-review.md
│
├── docs/
│   │
│   ├── operacao/
│   │   └── agent-workflow.md
│   │         └── runbook humano do fluxo
│   │
│   └── modelagem/
│       └── PLANO_CEPRAEA_Modelo_Canonico_FINAL.md
│             └── normativa da modelagem
│
├── .codex/
│   └── config.toml
│         └── enforcement do REVIEWER
│
├── .devcontainer/
│   ├── devcontainer.json
│   ├── Dockerfile
│   ├── security/
│   │   ├── claude-managed-settings.json
│   │   └── claude-guard
│   └── scripts/
│       └── verify-agent-environment.sh
│
└── .drive/
    └── CEPRAEA BEACH PRO/
          └── corpus operacional read-only

## Responsabilidades das camadas

### `AGENT_POLICY.md`

`AGENT_POLICY.md` DEVE permanecer como constituição comum.

Ele estabelece:

- autoridade humana;
- separação de funções;
- Git authority;
- proteção das fontes;
- proteção do control plane;
- deterministic first;
- tratamento de falta de permissão;
- regras comuns de evidência;
- escalonamento.

Os runbooks DEVEM operar dentro dessas invariantes.

### `CLAUDE.md`

`CLAUDE.md` DEVE permanecer como adaptador permanente do Executor.

Ele já estabelece o procedimento transversal de execução:

1. identificar a tarefa;
2. carregar as fontes normativas necessárias;
3. verificar branch;
4. inspecionar `git status`;
5. executar exclusivamente a alteração corrente;
6. executar validadores determinísticos;
7. executar `git diff --check`;
8. inspecionar `git diff`;
9. inspecionar `git status`;
10. entregar handoff factual;
11. finalizar com `READY_FOR_REVIEW` ou `BLOCKED`.

Os runbooks do Executor DEVEM acrescentar somente regras específicas da classe de operação.

### `AGENTS.md`

`AGENTS.md` DEVE permanecer como adaptador permanente do Reviewer.

Ele já estabelece o procedimento transversal de revisão:

1. identificar a tarefa sob revisão;
2. inspecionar `git status`;
3. inspecionar o `git diff` completo;
4. consultar artefatos relacionados;
5. identificar critérios de aceite;
6. executar verificações independentes proporcionais ao risco;
7. procurar regressões;
8. tentar refutar conclusões materiais;
9. verificar evidência e rastreabilidade;
10. verificar a força das inferências;
11. verificar proteção das fontes;
12. verificar preservação da autoridade humana;
13. emitir `PASS`, `FAIL` ou `HUMAN_DECISION_REQUIRED`.

Os runbooks do Reviewer DEVEM acrescentar somente verificações específicas da classe de alteração.

## Runbooks compartilhados

### `RB-SHARED-001-repository-baseline.md`

Este runbook DEVE definir somente verificações de baseline reutilizáveis quando a operação especializada depender delas.

Pode incluir:

- identificação do repositório;
- identificação do `HEAD`;
- identificação da branch;
- inspeção do estado inicial;
- identificação da área afetada;
- identificação das fontes normativas aplicáveis.

O carregamento DEVE ocorrer apenas quando essas verificações forem necessárias à classe de operação.

### `RB-SHARED-002-evidence.md`

Este runbook DEVE definir a forma mínima de evidência material utilizada pelos procedimentos especializados.

Pode abranger:

- `git diff`;
- `git diff --check`;
- lista de arquivos alterados;
- resultados de validadores;
- exit codes relevantes;
- relatórios gerados;
- evidência específica exigida pela tarefa.

A persistência DEVE ocorrer somente quando a evidência possuir valor material.

Git permanece como mecanismo primário de estado, handoff e histórico.

### `RB-SHARED-003-failure-states.md`

Este runbook DEVE padronizar a interpretação de estados operacionais entre os runbooks especializados.

Para o Executor:

READY_FOR_REVIEW
BLOCKED

Para o Reviewer:

PASS
FAIL
HUMAN_DECISION_REQUIRED

Cada runbook especializado DEVE utilizar esses estados de acordo com o papel correspondente.

## Runbooks do Executor

### `RB-EXEC-001-code-change.md`

Aplicabilidade:

alterações normais de código-fonte.

O procedimento específico PODE incluir:

1. identificar os componentes afetados;
2. identificar contratos públicos afetados;
3. localizar testes relacionados;
4. implementar exclusivamente a alteração requerida;
5. atualizar testes necessários;
6. executar os validadores aplicáveis;
7. verificar regressões diretamente relacionadas.

### `RB-EXEC-002-database-change.md`

Aplicabilidade:

- schema;
- migrations;
- constraints;
- índices;
- persistência.

O procedimento específico DEVE determinar, quando aplicável:

1. identificar a definição autoritativa;
2. identificar o estado atual das migrations;
3. identificar migrations previamente aplicadas;
4. verificar dados incompatíveis com a mudança;
5. produzir exclusivamente uma nova migration quando a mudança exigir evolução do schema;
6. implementar a constraint ou alteração autorizada;
7. executar validação da migration;
8. executar testes de integridade;
9. produzir as evidências materiais exigidas.

### `RB-EXEC-003-documentation-change.md`

Aplicabilidade:

criação ou alteração de documentação Markdown.

O procedimento DEVE:

1. localizar o guia canônico de documentação;
2. identificar fontes técnicas aplicáveis;
3. preservar decisões existentes;
4. limitar a mudança estritamente ao escopo documental;
5. aplicar as regras de autoria;
6. verificar links e referências afetados;
7. executar validações documentais disponíveis;
8. revisar o diff documental.

### `RB-EXEC-004-dependency-change.md`

Aplicabilidade:

- inclusão de dependência;
- remoção;
- atualização de versão;
- alteração de lockfile.

O procedimento específico DEVE:

1. identificar a necessidade da dependência;
2. identificar os manifests afetados;
3. identificar compatibilidade necessária;
4. alterar exclusivamente os arquivos relacionados;
5. atualizar lockfiles pela ferramenta canônica;
6. executar build, typecheck e testes aplicáveis;
7. registrar impacto material quando existir.

## Runbooks do Reviewer

### `RB-REV-001-code-review.md`

Aplicabilidade:

revisão de mudanças normais de código.

O Reviewer DEVE:

1. verificar o diff contra o objetivo da tarefa;
2. verificar comportamento observável;
3. procurar regressões;
4. verificar testes;
5. executar verificações independentes proporcionais ao risco;
6. verificar alterações inesperadas;
7. emitir o verdict correspondente.

### `RB-REV-002-database-review.md`

Aplicabilidade:

revisão de schema, migration ou integridade persistente.

O Reviewer DEVE:

1. identificar a regra normativa aplicável;
2. inspecionar a migration;
3. verificar a semântica da alteração;
4. verificar preservação das migrations históricas aplicáveis;
5. executar teste adversarial quando apropriado;
6. executar teste positivo quando apropriado;
7. verificar a integridade resultante;
8. confrontar evidências do Executor com fatos observáveis;
9. emitir o verdict correspondente.

### `RB-REV-003-documentation-review.md`

Aplicabilidade:

revisão de documentação.

O Reviewer DEVE:

1. identificar as fontes técnicas aplicáveis;
2. verificar preservação do significado;
3. verificar aderência ao guia de autoria;
4. procurar afirmações sem suporte;
5. verificar links e referências afetados;
6. verificar exemplos e comandos;
7. verificar separadamente forma e correção técnica;
8. emitir o verdict correspondente.

### `RB-REV-004-evidence-review.md`

Aplicabilidade:

operações em que a suficiência da evidência seja um aspecto material da aceitação.

O Reviewer DEVE:

1. identificar as alegações materiais;
2. identificar a evidência correspondente;
3. comparar alegações com o estado observável;
4. reproduzir verificações críticas quando proporcional;
5. classificar insuficiência material de evidência;
6. emitir o verdict correspondente.

## Runbook humano

O arquivo:

`docs/operacao/agent-workflow.md`

DEVE permanecer como runbook humano do ciclo completo.

Seu procedimento DEVE ser curto:

1. confirme a branch autorizada;
2. selecione uma única ACTION;
3. solicite ao Claude a execução dessa ACTION;
4. aguarde `READY_FOR_REVIEW`;
5. solicite ao Codex a revisão do `git diff`;
6. para `FAIL`, encaminhe os findings aplicáveis ao Claude;
7. para `HUMAN_DECISION_REQUIRED`, exerça a decisão humana e registre a decisão material quando necessário;
8. para `PASS`, revise o diff e execute o Git privilegiado;
9. inicie a próxima ACTION somente após concluir a anterior.

Esse arquivo orienta o operador humano.

Git permanece como state machine operacional.

## Regra de seleção

Uma tarefa DEVE carregar exclusivamente os runbooks aplicáveis.

A existência de um agente específico não determina automaticamente a criação ou o carregamento de um runbook.

A classe da operação determina o runbook.

Exemplo:

TASK-057
Alterar uma constraint de memberships.

EXECUTOR LOAD:
- AGENT_POLICY.md
- CLAUDE.md
- RB-EXEC-002-database-change.md
- runbook compartilhado necessário, quando aplicável
- normativa pertinente de `docs/modelagem/`
- fontes necessárias de `.drive/CEPRAEA BEACH PRO/`

REVIEWER LOAD:
- AGENT_POLICY.md
- AGENTS.md
- RB-REV-002-database-review.md
- runbook compartilhado necessário, quando aplicável
- normativa pertinente de `docs/modelagem/`
- `git diff`
- evidências materiais da execução

## Regra de precedência

Os runbooks DEVEM respeitar esta relação de autoridade:

AUTORIDADE HUMANA
        ↓
AGENT_POLICY.md
        ↓
fontes canônicas de domínio e arquitetura aplicáveis
        ↓
CLAUDE.md / AGENTS.md
        ↓
runbook especializado
        ↓
procedimento da execução concreta

Uma instrução de runbook somente possui validade dentro da autoridade concedida pelas camadas superiores.

Quando uma contradição material impedir a aplicação inequívoca das fontes:

Executor:
BLOCKED

Reviewer:
HUMAN_DECISION_REQUIRED

## Relação com o plano da tarefa

O plano da tarefa define:

- objetivo específico;
- escopo específico;
- entregáveis;
- sequência particular necessária;
- critérios de aceitação.

O runbook define:

- como a classe de operação deve ser conduzida;
- quais verificações operacionais devem ocorrer;
- quais evidências são relevantes;
- quais estados de saída são válidos.

A relação DEVE ser:

TASK
        ↓
PLAN / critérios
        +
RUNBOOK aplicável
        ↓
EXECUTOR
        ↓
working tree + validações + evidências
        ↓
REVIEWER

O runbook DEVE preservar o escopo e os critérios da tarefa.

## Relação com o enforcement

Os runbooks especificam procedimentos.

Os mecanismos técnicos aplicam limites.

A relação é:

AGENT_POLICY
    ↓
regra normativa

CLAUDE.md / AGENTS.md
    ↓
regra de papel

RUNBOOK
    ↓
procedimento especializado

DEV CONTAINER
PERMISSIONS
SANDBOX
GUARDS
VALIDATORS
    ↓
enforcement e verificação determinística

O runbook DEVE depender de enforcement já autorizado quando a propriedade puder ser aplicada tecnicamente.

## Relação com Git

Git DEVE permanecer como:

- estado operacional;
- handoff entre Executor e Reviewer;
- representação concreta da alteração;
- histórico persistente;
- identidade final das mudanças por commit.

A biblioteca de runbooks DEVE operar sobre esse modelo.

A persistência operacional DEVE ser limitada aos artefatos que possuam valor material.

Um `execution log` separado PODE ser produzido quando uma operação específica justificar esse registro.

A biblioteca de runbooks, por si só, NÃO estabelece um requisito de `executions/**`, `reviews/**`, `STATE.md` ou banco paralelo de workflow.

## Relação com o `CONTAINER_RUNBOOK`

O `CONTAINER_RUNBOOK` fornecido DEVE ser tratado exclusivamente como exemplo de outro tipo de runbook.

Ele demonstra uma estrutura possível para operações de infraestrutura que precisam preservar:

- baseline;
- estado comprovado;
- decisões;
- testes;
- evidências;
- rollback;
- histórico de mudanças.

Seu conteúdo e seus estados NÃO representam evidência do estado atual da arquitetura real considerada nesta decisão.

A biblioteca proposta aqui deriva dos documentos reais da Human-Governed Dual-Agent SDLC Architecture.

## Estrutura mínima de um runbook especializado

Cada novo runbook DEVERIA utilizar uma estrutura compatível com:

# Título do runbook

## Objetivo

Defina a classe de operação governada.

## Aplicabilidade

Defina as condições objetivas para selecionar o runbook.

## Entradas

Liste exclusivamente as entradas necessárias.

## Fontes de autoridade

Liste as fontes que governam a operação.

## Pré-condições

Defina o estado mínimo necessário para iniciar.

## Escopo operacional

Defina positivamente os caminhos, recursos e operações autorizados.

Exemplo:

Restrinja todas as alterações exclusivamente aos arquivos necessários à tarefa e aos caminhos autorizados pelo contrato corrente.

## Procedimento

Utilize uma lista numerada quando a ordem for significativa.

## Pontos de decisão

Defina condições observáveis para cada desvio de fluxo.

## Validações

Liste os checks determinísticos aplicáveis.

## Evidências

Defina somente evidências necessárias para comprovar propriedades materiais.

## Handoff

Defina a saída entregue ao próximo papel.

## Estados de saída

Utilize exclusivamente os estados pertencentes ao papel correspondente.

## Referências

Utilize caminhos relativos para arquivos do repositório quando adequado.

## Critério para criação de novos runbooks

Um novo runbook DEVERIA ser criado quando uma classe de operação possuir pelo menos uma destas características:

- repetição;
- risco material;
- procedimento especializado;
- decisões condicionais recorrentes;
- validações específicas;
- requisitos de evidência próprios;
- necessidade clara de consistência entre execuções.

Uma variação isolada de uma tarefa DEVERIA permanecer no plano da tarefa.

A biblioteca DEVE evitar um runbook por ACTION.

A relação desejada é:

1 RUNBOOK
        ↓
múltiplas tarefas da mesma classe

e não:

1 TASK
        ↓
1 RUNBOOK exclusivo

## Resultado arquitetural

Com a proposta B, a arquitetura consolidada passa a ser:

HUMANO
   │
   ├── controla domínio, decisões e Git privilegiado
   │
   ▼
AGENT_POLICY.md
   │
   ├───────────────┐
   ▼               ▼
CLAUDE.md       AGENTS.md
EXECUTOR        REVIEWER
   │               │
   ▼               ▼
RB-EXEC-*       RB-REV-*
   │               │
   └───────┬───────┘
           │
           ▼
 fontes normativas
           │
           ▼
      operação real
           │
           ▼
 working tree / git diff
 + validações
 + evidências materiais
           │
           ▼
        Codex
           │
    ┌──────┼──────────────────────────┐
    ▼      ▼                          ▼
  PASS    FAIL          HUMAN_DECISION_REQUIRED
    │      │                          │
    ▼      └──────► Claude            ▼
  HUMANO                         HUMANO decide
    │
    ▼
stage / commit / promoção

Essa estrutura mantém a arquitetura Human-Governed Dual-Agent SDLC, acrescenta procedimentos especializados reutilizáveis e preserva Git como state machine sem introduzir uma infraestrutura concorrente de workflow.
```

A separação entre Git como state machine, Executor produtor, Reviewer independente e autoridade humana está explicitamente estabelecida na arquitetura real.  A proposta de biblioteca `runbooks/shared`, `runbooks/executor` e `runbooks/reviewer` também consta no documento real de arquivos da arquitetura.

