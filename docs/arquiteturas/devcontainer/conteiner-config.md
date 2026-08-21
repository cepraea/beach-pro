# Por que este devcontainer existe assim

> Auditoria dos mecanismos técnicos do `.devcontainer/`, feita porque a configuração foi
> construída silenciosamente ao longo do desenvolvimento e ninguém conseguia mais explicar,
> arquivo por arquivo, qual problema cada peça resolve. Este documento é a justificativa —
> escrita para ainda fazer sentido anos depois, quando os detalhes tiverem sido esquecidos.
>
> Este arquivo vive fora de `.devcontainer/` porque esse diretório é zona intocável para
> agentes (ver DCFG-003, abaixo) — não é possível gravar nem este próprio registro lá dentro.

## Como ler este documento

Cada registro tem **dois eixos independentes de avaliação** — não confundir um com o outro:

- **Estado de documentação** — o mecanismo está escrito em alguma política legível
  (`AGENT_POLICY.md`/`CLAUDE.md`) ou só existe implícito no código?
  - ✅ **Coerente e documentado** — bate com o que está escrito.
  - ⚠️ **Real, mas não documentado** — existe e é intencional, mas nenhuma política escrita
    avisa que ele existe, então o comportamento observado surpreende.
  - 🔴 **Defeito conhecido** — não faz o que deveria fazer.
- **Classificação de governança** — dado o algoritmo abaixo, calibrado para o estágio atual
  do CEPRAEA BEACH PRO (pré-implantação: nada ainda está em produção), o mecanismo é
  `ESSENCIAL`, `NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS`, ou `EXCESSO DE GOVERNANÇA`?

Um mecanismo pode ser essencial e ainda assim não documentado — são perguntas diferentes.

## Algoritmo de classificação

Aplicado a cada registro, nesta ordem, parando na primeira pergunta que responder "sim":

1. **A proteção é proporcional ao risco real neste estágio do projeto, e não existe forma
   mais simples de obter a mesma proteção com menos custo?**
   → **ESSENCIAL**.
2. **A proteção em si é necessária — existe risco real que a justifica — mas a implementação
   atual está incorreta, incompleta, ou mais restritiva/permissiva do que precisa ser para
   esse risco?**
   → **NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS**.
3. **O risco mitigado é desproporcional ao estágio atual (ex.: protege contra cenários de
   produção/deploy que ainda não existem), tornando o custo de fricção maior que o benefício
   real hoje?**
   → **EXCESSO DE GOVERNANÇA**.

As três perguntas acima pressupõem que o mecanismo é, em si, uma proteção (mitiga algum
risco). Quando o mecanismo é puramente funcional — não mitiga risco nem impõe fricção de
segurança — nenhuma das três perguntas se aplica, e o resultado é **FUNCIONAL/NÃO APLICÁVEL**,
não ESSENCIAL por padrão (ESSENCIAL continua reservado a proteções proporcionais sem
alternativa mais simples — pergunta 1).

Se nenhum registro cair numa categoria, isso é um resultado válido do algoritmo, não motivo
para forçar um item nela — ver o resumo abaixo.

---

## DCFG-001 — Isolamento de credenciais

**Arquivos:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json) (`containerEnv`/`remoteEnv`),
[`control-plane/gitconfig-agent`](../../../.devcontainer/control-plane/gitconfig-agent)

**Snapshot (2026-08-21):**

```json-nolint
// devcontainer.json — containerEnv / remoteEnv (idênticos)
{
  "GIT_CONFIG_GLOBAL": "/dev/null",
  "GIT_TERMINAL_PROMPT": "0",
  "GH_CONFIG_DIR": "/home/agent/.config/gh-empty",
  "SSH_AUTH_SOCK": "",
  "GITHUB_TOKEN": "",
  "GH_TOKEN": "",
  "DOCKER_HOST": "",
  "GIT_CONFIG_NOSYSTEM": "1"
}
```

```text
# control-plane/gitconfig-agent — conteúdo integral
# CEPRAEA BEACH PRO — Git configuration intentionally empty.
# Agents must not receive user identity, credential helpers, or signing configuration.
```

**Por que foi adotado:** mitigar especificamente os canais de credencial conhecidos e
verificados — Git config, tokens do GitHub, SSH agent, Docker host. Toda saída do agente é um
diff que Davi revisa e aplica.

**Limitações conhecidas (não cobertas por este mecanismo — correção de 2026-08-21):** a
versão anterior deste registro afirmava que "não existe caminho técnico" para o agente afetar
algo fora do checkout — garantia mais forte do que os controles aqui descritos sustentam. A
matriz de estado do
[`CONTAINER-RUNBOOK-v0.3.md` §8](../multi-agentes/containers/CONTAINER-RUNBOOK-v0.3.md), linha
676, registra `NET-01` (política de rede final) como `PENDENTE`; linhas 685-686 registram
`MNT-01`/`MNT-02` (mounts de diretórios pessoais) como `PENDENTE`; linha 690 registra `CRE-04`
(ausência de cloud/deploy secrets) com "sanitização parcial comprovada" e "inventário amplo
ausente". Este mecanismo garante os quatro canais listados acima — não garante isolamento de
rede nem inventário completo de segredos.

**Decisão que levou à escolha:** o próprio `gitconfig-agent` documenta a intenção em
comentário ("Agents must not receive user identity..."). Não há registro formal (ADR/ticket)
adicional além do código, para as variáveis específicas — a escolha é inferida do risco que
cada uma mitiga (push, assinatura, autenticação, Docker).

**Classificação:** ESSENCIAL para os quatro canais que efetivamente cobre — pergunta 1: sim,
é a forma mais simples de fechar esses canais específicos. Rede e inventário de segredos são
lacunas separadas (`NET-01`/`CRE-04`, `PENDENTE` no runbook), não resolvidas por este
mecanismo — não devem ser lidas como cobertas por ele.

**Estado de documentação:** ✅ coerente para o escopo real da garantia, corrigido nesta
revisão (ver changelog).

---

## DCFG-002 — Mounts read-only do plano de controle

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json) (`mounts`)

**Snapshot (2026-08-21):**

```json-nolint
"mounts": [
  "source=${localWorkspaceFolder}/.git,target=/workspaces/cepraea-beach-pro/.git,type=bind,readonly",
  "source=${localWorkspaceFolder}/.devcontainer,target=/workspaces/cepraea-beach-pro/.devcontainer,type=bind,readonly",
  "source=${localWorkspaceFolder}/.github/workflows,target=/workspaces/cepraea-beach-pro/.github/workflows,type=bind,readonly",
  "source=${localWorkspaceFolder}/.claude,target=/workspaces/cepraea-beach-pro/.claude,type=bind,readonly",
  "source=${localWorkspaceFolder}/.codex,target=/workspaces/cepraea-beach-pro/.codex,type=bind,readonly",
  "source=${localWorkspaceFolder}/.mcp.json,target=/workspaces/cepraea-beach-pro/.mcp.json,type=bind,readonly",
  "source=${localWorkspaceFolder}/CLAUDE.md,target=/workspaces/cepraea-beach-pro/CLAUDE.md,type=bind,readonly",
  "source=${localWorkspaceFolder}/AGENTS.md,target=/workspaces/cepraea-beach-pro/AGENTS.md,type=bind,readonly",
  // ... + scripts/ci, AGENT_POLICY.md, runbooks — mesmo padrão, todos readonly
]
```

**Por que foi adotado:** mesmo que um agente tentasse escrever nesses caminhos por alguma
rota que o guard de aplicação (DCFG-003) não previsse, o filesystem já recusa a escrita — é
a camada estrutural por trás do guard, não depende de nenhum script continuar correto.

**Decisão que levou à escolha:** sem registro formal além do código. Inferida diretamente da
[matriz de risco do AGENT_POLICY.md §3](../../../AGENT_POLICY.md#3-matriz-de-classificação-de-risco),
que classifica `.devcontainer`, CI e infraestrutura como 🚨 Crítico — para risco crítico,
redundância de camada (filesystem + script) é prática esperada, não acidente.

**Classificação:** ESSENCIAL — pergunta 1: sim; é o nível de risco mais alto da matriz
própria do repositório, e a redundância com DCFG-003 tem custo zero de fricção (não pede
aprovação, é silenciosa).

**Estado de documentação:** ✅ coerente.

---

## DCFG-003 — Guard de caminho (zonas intocáveis)

**Arquivo:** [`guards/pretool`](../../../.devcontainer/guards/pretool)

**Snapshot (2026-08-21):**

```bash
path="$(jq -r '.tool_input.file_path // .tool_input.path // .tool_input.planFilePath // empty' <<<"$payload")"

if [[ -n "$path" ]] && is_allowed_claude_plan_path "$path"; then
  : # exceção estrita para o runtime nativo de Plan Mode
else
  case "$path" in
*/.git/*|*/.devcontainer/*|*/.github/workflows/*|*/scripts/ci/*|\
*/.claude/*|*/.codex/*|*/.mcp.json|*/AGENT_POLICY.md|*/CLAUDE.md|\
*/AGENTS.md|*/runbooks/*)
    block "Bloqueado: caminho do plano de controle." ;;
  esac
fi
```

**Por que foi adotado:** implementa em software a seção "Zonas Intocáveis" do
[AGENT_POLICY.md §4](../../../AGENT_POLICY.md#4-git-e-zonas-de-controle). Sem isso, a regra
seria só uma instrução que o agente poderia, mesmo que por engano, ignorar. Foi o mecanismo
que impediu este próprio documento de ser salvo dentro de `.devcontainer/`.

**Decisão que levou à escolha:** sem registro formal além do código. Bloqueio por padrão de
caminho (allowlist implícita via exceção única para planos de Plan Mode) é a tradução direta
da lista de caminhos já nomeada no `AGENT_POLICY.md §4`.

**Classificação:** ESSENCIAL — pergunta 1: sim; é a aplicação em runtime de uma regra já
escrita como obrigatória, sem a qual a regra escrita não tem efeito prático.

**Estado de documentação:** ✅ coerente.

---

## DCFG-004 — Bloqueio total de Bash/Edit/Write na branch `main`/`master`

**Arquivo:** [`guards/pretool`](../../../.devcontainer/guards/pretool), linhas 34-39

**Snapshot (2026-08-21):**

```bash
if [[ "$branch" == "main" || "$branch" == "master" ]]; then
  case "$tool" in
    Bash|Edit|Write|MultiEdit|NotebookEdit)
      block "Bloqueado: ferramenta mutável na branch principal." ;;
  esac
fi
```

Bloqueia a ferramenta **inteira**, não o comando. Um `git status` sozinho, um `ls`, qualquer
chamada de `Bash` — é recusada em `main`, mesmo sendo somente leitura.

**Por que foi adotado (design pretendido):** em vez de reconhecer todo comando de shell que
poderia, direta ou indiretamente, alterar o estado de `main` (variáveis, encoding, wrappers,
`&&` encadeado), o guard corta a ferramenta inteira nessa branch — fail-closed.

**Decisão que levou à escolha:** sem registro formal além do código — nenhum comentário no
próprio script explica por que a exceção de leitura (a allowlist Git off-`main`, no mesmo
`guards/pretool`, linhas 70-86) não foi estendida a `main`. É a lacuna mais visível deste
documento.

**Classificação:** NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS — pergunta 1: não (existe forma
mais simples: reaplicar em `main` a mesma allowlist de leitura que já existe para comandos
Git off-`main`, em vez de cortar `Bash` inteiro). Pergunta 2: sim — a proteção contra mutação
de `main` é necessária, mas a implementação atual também bloqueia leitura, que é exatamente o
que um agente precisa fazer para auditar/planejar antes de agir — o custo é mais alto do que
o risco justifica neste estágio, onde a atividade principal do repositório é inspeção e
planejamento, não mutação.

**Estado de documentação:** ⚠️ real, mas não documentado até este arquivo.

---

## DCFG-005 — Bypass de permissão desativado no build da imagem

**Arquivo:** [`control-plane/claude-managed-settings.json`](../../../.devcontainer/control-plane/claude-managed-settings.json)

**Snapshot (2026-08-21):**

```json
{
  "allowManagedHooksOnly": true,
  "allowManagedPermissionRulesOnly": true,
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

Copiado pelo [`Dockerfile`](../../../.devcontainer/Dockerfile) para
`/etc/claude-code/managed-settings.json`, propriedade de `root`, `chmod 0644` — gravado na
imagem, não no workspace.

**Por que foi adotado:** impede que qualquer sessão, mesmo por engano, afrouxe permissões via
`settings.local.json` ou via flag `--dangerously-skip-permissions`.

**Decisão que levou à escolha:** implementa diretamente o
[AGENT_POLICY.md §2](../../../AGENT_POLICY.md#2-escopo-e-anti-bypass) — "Falta de permissão
não autoriza contornar restrições". Sem registro formal adicional além dessa cláusula e do
próprio arquivo de configuração.

**Classificação:** ESSENCIAL — pergunta 1: sim; é o único mecanismo que garante que a
proibição de bypass do §2 não possa ser contornada por uma sessão local — não existe forma
mais simples de dar essa garantia sem fixá-la no build da imagem.

**Estado de documentação:** ⚠️ real (a cláusula de anti-bypass está no `AGENT_POLICY.md`, mas
a consequência prática — que isso é irreversível de dentro de uma sessão rodando, exigindo
rebuild da imagem para qualquer ajuste — não estava documentada até este arquivo).

---

## DCFG-006 — Sandbox interno do Claude desativado (`sandbox.enabled: false`)

**Arquivo:** [`control-plane/claude-managed-settings.json`](../../../.devcontainer/control-plane/claude-managed-settings.json), linha 40-42

**Snapshot (2026-08-21):**

```json
"sandbox": {
  "enabled": false
}
```

**Correção material (revisão de 2026-08-21):** a versão anterior deste registro classificava
isto como defeito sem justificativa localizável. Isso estava errado — a justificativa existe
e não foi encontrada na primeira passada desta auditoria por falta de uma busca mais ampla no
repositório.

**Por que foi adotado:** esta flag desliga o sandbox **interno** do Claude Code (baseado em
Bubblewrap) — mecanismo diferente do "Dev Container como sandbox operacional" tratado abaixo.
A [`DEC-ARQ-001`](../../../.ai/decisions/DEC-ARQ-001-dev-container-como-sandbox-operacional.md),
linha 91, determina explicitamente: *"Não enfraquecer o Dev Container para satisfazer o
sandbox interno do Claude. O Dev Container é o sandbox operacional primário."* — rejeitando
`privileged=true`, `CAP_SYS_ADMIN`, `seccomp=unconfined` e Docker socket como correção para o
Bubblewrap não funcionar (linhas 94-108 do mesmo arquivo). O
[`CONTAINER-RUNBOOK-v0.3.md`, linha 591](../multi-agentes/containers/CONTAINER-RUNBOOK-v0.3.md)
registra a causa técnica: `bwrap` não consegue criar user namespace neste container
Docker/WSL2 — a mesma causa raiz documentada e validada para o Codex em `SEC-02`/
`E2E-CODEX-BOUNDARY-01` (ver DCFG-007). Em vez de enfraquecer o container para viabilizar o
Bubblewrap, a decisão foi manter o Dev Container não-privilegiado como fronteira e desligar o
sandbox interno, que não funcionaria de qualquer forma neste ambiente.

**Ressalvas de estado (não esconder):** a própria `DEC-ARQ-001.md` está com **status
rebaixado para `PROPOSTA`** (não `RATIFICADO`) desde 2026-08-14, por não haver, neste
checkout, artefato verificável da aprovação formal por Davi Sermenho (nota de evidência,
linhas 17-27 do arquivo da decisão — o conteúdo normativo é mantido, só o status de
ratificação foi rebaixado). A comprovação central de que o container roda de fato
`Privileged=false` (`ISO-05`) segue `PENDENTE` no runbook (linha 681). O raciocínio técnico é
sólido e a causa raiz está documentada, mas a cadeia de evidência formal — ratificação da
decisão + comprovação centralizada de `ISO-05` — não está fechada dentro deste repositório.

**Decisão que levou à escolha:** `DEC-ARQ-001`, reconstituída em 2026-08-14 a partir de fonte
histórica externa citada por Davi Sermenho; conteúdo normativo mantido, status de ratificação
pendente de artefato auditável.

**Classificação:** ESSENCIAL — pergunta 1: sim; é a consequência pretendida de uma decisão
arquitetural documentada, com causa técnica comprovada (mesma causa validada para o Codex em
`SEC-02`), e não existe forma mais simples de obter a mesma proteção sem ampliar os
privilégios do próprio Dev Container — o que a decisão rejeita explicitamente (`privileged=true`,
`CAP_SYS_ADMIN`, `seccomp=unconfined`, Docker socket). Ressalva: esta
classificação assume `DEC-ARQ-001` como intenção vigente; ela está em status `PROPOSTA`, não
`RATIFICADO`, e `ISO-05` segue `PENDENTE` — fechar essas duas lacunas de evidência é o
refinamento pendente, não a flag em si.

**Estado de documentação:** ⚠️ fundamentada, mas a fundamentação (`DEC-ARQ-001`) não estava
referenciada a partir deste documento antes desta revisão, e a decisão em si ainda carrega
status `PROPOSTA` — não tratar como encerrado.

---

## DCFG-007 — Boundary de sandbox do Codex (P-002 / SEC-02)

**Arquivo:** [`control-plane/codex-requirements.toml`](../../../.devcontainer/control-plane/codex-requirements.toml)

**Snapshot (2026-08-21):**

```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_approvals_reviewers = ["user"]
allowed_sandbox_modes = ["read-only"]
allow_managed_hooks_only = true
allow_remote_control = false
allow_login_shell = false
allowed_web_search_modes = ["cached", "indexed"]

# Esta configuração usa allowed_sandbox_modes para enforcement de sandbox.
# A primeira tentativa com [permissions.cepraea_review] não impôs a fronteira pretendida;
# causa exata não determinada. Testado em 2026-08-14 com codex-cli 0.146.1.
# Gates definitivos de P-002 ainda pendentes (codex exec com saída completa).

[features]
computer_use = false
browser_use_external = false
browser_use_full_cdp_access = false
```

**Correção material (revisão de 2026-08-21):** a versão anterior deste registro afirmava que
"P-002" não foi localizada em nenhum outro lugar do repositório e que o boundary "nunca foi
concluído". Ambas as afirmações estavam erradas — a busca anterior não alcançou
`docs/arquiteturas/multi-agentes/containers/CONTAINER-RUNBOOK-v0.3.md`, onde P-002 está
extensamente documentada. O comentário dentro do próprio `.toml` acima está **desatualizado**:
descreve a primeira tentativa como inconclusiva sem mencionar a investigação que a sucedeu.
É exatamente o tipo de lacuna que motiva este documento — o código de configuração, sozinho,
não conta a história completa.

**Histórico real, reconstituído do `CONTAINER-RUNBOOK-v0.3.md`:**

1. **Tentativa original (P-002):** perfil `[permissions.cepraea_review]` com
   `extends = ":read-only"`. Codex conseguiu escrever `probe.txt` — não impôs a fronteira
   pretendida; causa não determinada nesse momento (linhas 1887-1888, 1894-1896).
2. **Correção aplicada:** removido `[permissions.cepraea_review]`, restaurado
   `allowed_sandbox_modes = ["read-only"]` — é o estado do snapshot acima.
3. **Investigação conclusiva — `E2E-CODEX-BOUNDARY-01`, 2026-08-14 (linhas 1900-1921):** causa
   raiz identificada — `bwrap` (Bubblewrap) falha ao criar user namespace neste container
   Docker/WSL2 (`"bwrap: No permissions to create new namespace"`). Cadeia de proteção real
   documentada: (1) `bwrap` indisponível → `codex exec` não executa nenhum comando — proteção
   primária; (2) mount `.git` RO (`DEC-CTR-013`) → proteção estrutural independente;
   (3) `allowed_sandbox_modes = ["read-only"]` → defesa em profundidade, caso `bwrap` volte a
   funcionar.
4. **Resultado na matriz de estado:** `SEC-02`, linha 711 do runbook = **`VALIDADO`** —
   "`allowed_sandbox_modes = ["read-only"]` no codex-requirements.toml (P-002 corrigido)".

**O que esta auditoria não confirma:** o runbook lista, em "Gates pós-rebuild obrigatórios",
um checklist P-002 que referencia o perfil `cepraea_review` já abandonado no passo 2 — não
verifiquei se esse checklist específico foi reexecutado após o rebuild mais recente. Não
afirmo que está pendente nem que está concluído além do que `SEC-02: VALIDADO` já registra.

**Por que foi adotado:** restringir o Codex a `read-only` é defesa em profundidade sobre uma
proteção primária que já existe por outro motivo (`bwrap` indisponível) — cobre o cenário em
que essa indisponibilidade deixar de ser verdade.

**Decisão que levou à escolha:** documentada e rastreável no `CONTAINER-RUNBOOK-v0.3.md`, com
causa técnica identificada e teste conclusivo — ao contrário do que o comentário isolado do
próprio arquivo `.toml` sugere.

**Classificação:** ESSENCIAL — pergunta 1: sim; é defesa em profundidade de custo zero sobre
uma proteção primária já comprovada, e a investigação que a sustenta está concluída e
registrada (`SEC-02: VALIDADO`).

**Estado de documentação:** ⚠️ o mecanismo está correto e validado no runbook, mas o
comentário dentro do próprio arquivo de configuração está desatualizado em relação a isso —
deveria ser corrigido para não sugerir "investigação abandonada", que foi exatamente o erro
cometido na primeira versão deste documento.

---

## DCFG-008 — Log de auditoria (`posttool`)

**Arquivo:** [`guards/posttool`](../../../.devcontainer/guards/posttool)

**Snapshot (2026-08-21):**

```bash
#!/usr/bin/env bash
set -euo pipefail
state_dir="/home/agent/.local/state/cepraea-guards"
mkdir -p "$state_dir"
payload="$(cat)"
tool="$(jq -r '.tool_name // "desconhecido"' <<<"$payload")"
printf '{"observado_em":"%s","tool":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "$tool" \
  >> "$state_dir/events.jsonl"
exit 0
```

**Por que foi adotado:** dá visibilidade de quais ferramentas um agente usou e quando, sem
interferir em nada — não bloqueia, não pede aprovação, não duplica o histórico do Git (não é
o "log paralelo ao Git" que o `AGENT_POLICY.md §4` proíbe; é log de uso de ferramenta, não de
estado versionado).

**Correção de terminologia (revisão de 2026-08-21):** a versão anterior chamava
`events.jsonl` de "append-only", termo que sugere imutabilidade garantida pelo sistema. É
impreciso: o `posttool` cria o diretório de estado sob
`/home/agent/.local/state/cepraea-guards` (linhas 3-4), que é gravável pelo próprio usuário
`agent` (`install -d -o agent -g agent ...` no `Dockerfile`); a escrita é um `>>` convencional
(linha 10) — sem `chattr +a`, sem processo separado, sem mount somente-escrita. É um arquivo
local gravado por append, sem garantia de integridade, retenção ou completude —
observabilidade best-effort, não trilha de auditoria à prova de adulteração.

**Decisão que levou à escolha:** sem registro formal além do código — é a forma mais direta
possível de obter esse tipo de observabilidade leve.

**Classificação:** ESSENCIAL — pergunta 1: sim, mas com escopo restrito ao que o mecanismo
realmente entrega (visibilidade best-effort para depuração), não a uma garantia de auditoria
íntegra. Custo de fricção é zero; não existe forma mais simples de obter esse nível (limitado)
de rastro.

**Estado de documentação:** ✅ coerente, com terminologia corrigida nesta revisão.

---

## DCFG-009 — `Dockerfile` completo (imagem, pacotes, usuário, instalação root-owned)

**Arquivo:** [`Dockerfile`](../../../.devcontainer/Dockerfile)

**Snapshot (2026-08-21, pós-adição de `python3`):**

```text
FROM node:22-bookworm-slim

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash bubblewrap ca-certificates curl git jq less passwd procps socat python3 \
    && rm -rf /var/lib/apt/lists/*

# A imagem Node já possui UID/GID 1000. Renomeie sem conceder sudo.
RUN groupmod -n agent node \
    && usermod -l agent -d /home/agent -m node \
    && install -d -o agent -g agent /home/agent/.local /home/agent/.local/state \
    && install -d -o agent -g agent \
       /home/agent/.cache /home/agent/.claude /home/agent/.codex \
       /home/agent/.local/bin \
       /home/agent/.config/git /home/agent/.config/gh-empty \
       /home/agent/.local/state/cepraea-guards \
       /workspaces/cepraea-beach-pro

 RUN install -d -o root -g root /etc/claude-code /etc/codex \
     /usr/local/lib/cepraea-guards
 COPY .devcontainer/control-plane/claude-managed-settings.json \
      /etc/claude-code/managed-settings.json
COPY .devcontainer/control-plane/claude-managed-mcp.json \
     /etc/claude-code/managed-mcp.json
 COPY .devcontainer/control-plane/codex-requirements.toml \
      /etc/codex/requirements.toml
 COPY .devcontainer/guards/ /usr/local/lib/cepraea-guards/
 RUN chown -R root:root /etc/claude-code /etc/codex \
       /usr/local/lib/cepraea-guards \
     && chmod 0644 /etc/claude-code/managed-settings.json \
      /etc/claude-code/managed-mcp.json \
       /etc/codex/requirements.toml \
     && chmod 0755 /usr/local/lib/cepraea-guards/*

USER agent
ENV HOME=/home/agent
ENV PATH=/home/agent/.local/bin:$PATH
RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh \
    && curl -fsSL https://claude.ai/install.sh | bash \
    && codex --version \
    && claude --version
WORKDIR /workspaces/cepraea-beach-pro
```

**Correção material (revisão de 2026-08-21):** a versão anterior deste registro incluía
DCFG-002 (mounts read-only) na lista de mecanismos dependentes deste `Dockerfile`. Isso está
errado: os mounts de DCFG-002 são declarados inteiramente no array `mounts` de
`devcontainer.json` e apontam para arquivos/diretórios do host — nenhuma instrução deste
`Dockerfile` os cria ou é pré-requisito para eles existirem.

**Por que foi adotado:** é o único lugar onde a fronteira root/`agent` é criada e onde os
arquivos de controle (`managed-settings.json`, `managed-mcp.json`, `requirements.toml`,
`guards/*`) viram `root`-owned dentro da imagem — sem isso, DCFG-003/005/006/007 não teriam
como existir tecnicamente. `python3` foi adicionado em 2026-08-21 (pedido de Davi,
ver seção sobre `Bootstrap.py` no histórico deste repositório) porque, sem runtime Python na
imagem, `test/scripts/bootstrap/Bootstrap.py` era código morto — instalação em build, versão
não pinada, consistente com `bootstrap-arquitetura.md DEC-BOOT-010` (provisionar no build, não
em runtime).

**Decisão que levou à escolha:** sem registro formal além do código para a maior parte do
arquivo. A escolha de `node:22-bookworm-slim` como base provavelmente decorre de o Codex/Claude
CLI serem distribuídos via `npm`/instaladores Node — inferência, não confirmada em nenhum
documento.

**Classificação:** ESSENCIAL — pergunta 1: sim; é a única forma de obter a separação
root/`agent` e a instalação `root`-owned dos arquivos de controle que todos os outros
mecanismos deste documento dependem.

**Estado de documentação:** ⚠️ real e coerente com os demais mecanismos, mas nunca havia sido
tratado como registro próprio até esta revisão — só era citado de passagem dentro de outros
DCFGs.

---

## DCFG-010 — `runArgs`: hardening de privilégios do container

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json) (`runArgs`)

**Snapshot (2026-08-21):**

```json-nolint
"runArgs": [
  "--security-opt=no-new-privileges:true",
  "--cap-drop=ALL",
  "--add-host=host.docker.internal:host-gateway"
]
```

**Por que foi adotado:** `no-new-privileges` impede que qualquer processo dentro do container
eleve privilégios via binários setuid/setgid; `cap-drop=ALL` remove todas as capabilities Linux
do container (inclusive as que um `root` de container normalmente teria). Corresponde
diretamente a `ISO-06`/`ISO-07` da matriz de estado do
[`CONTAINER-RUNBOOK-v0.3.md` §8](../multi-agentes/containers/CONTAINER-RUNBOOK-v0.3.md)
("no-new-privileges" e "capabilities administrativas ausentes", ambos `VALIDADO`).
`add-host=host.docker.internal` é conveniência de rede (resolver o host a partir do
container), sem relação com hardening.

**Decisão que levou à escolha:** sem registro formal além do código; consistente com
`DEC-ARQ-001` (ver DCFG-006) — o Dev Container como fronteira de isolamento primária, não o
sandbox interno do Claude.

**Classificação:** ESSENCIAL — pergunta 1: sim; é o mecanismo de nível de kernel/Docker mais
barato e direto para impedir escalonamento de privilégio dentro do container, sem o qual
`USER agent` (DCFG-009) seria uma barreira mais fraca (contornável por capabilities residuais).

**Estado de documentação:** ⚠️ real e coerente com `DEC-ARQ-001`/`CONTAINER-RUNBOOK-v0.3.md`,
mas nunca citado neste documento até esta revisão.

---

## DCFG-011 — Identidade de usuário e montagem do workspace

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json)

**Snapshot (2026-08-21):**

```json-nolint
"workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/cepraea-beach-pro,type=bind",
"workspaceFolder": "/workspaces/cepraea-beach-pro",
"remoteUser": "agent",
"containerUser": "agent",
"updateRemoteUserUID": false
```

**Por que foi adotado:** fixa `agent` (não-root, criado em DCFG-009) como usuário efetivo do
VS Code Server e do container, e desativa o remapeamento automático de UID que o VS Code faria
por padrão para casar com o usuário do host — evitando que esse remapeamento amplie
silenciosamente privilégios do usuário do container. O `workspaceMount` aqui **não** é
`readonly` (diferente de `reviewer/devcontainer.json`, ver DCFG-019) — o Executor precisa
escrever no checkout; o Reviewer não.

**Decisão que levou à escolha:** sem registro formal além do código. Corresponde a `ISO-02`
("usuário interno não root") na matriz do `CONTAINER-RUNBOOK-v0.3.md §8`, `VALIDADO`.

**Classificação:** ESSENCIAL — pergunta 1: sim; é a forma padrão do Dev Containers de fixar
identidade não-privilegiada, sem alternativa mais simples.

**Estado de documentação:** ⚠️ real, coerente, nunca registrado como mecanismo próprio até
esta revisão.

---

## DCFG-012 — `postStartCommand`: diretório de planos do Claude Code

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json) (`postStartCommand`)

**Snapshot (2026-08-21):**

```json-nolint
"postStartCommand": "install -d -m 0700 /home/agent/.claude/plans && test -w /home/agent/.claude/plans"
```

**Por que foi adotado:** garante, a cada início do container, que `/home/agent/.claude/plans`
existe com permissão restrita (`0700`, só o próprio `agent` lê/escreve) e é gravável — é onde o
runtime nativo de Plan Mode grava arquivos de plano (ver a exceção estrita em
`guards/pretool`, `is_allowed_claude_plan_path`, citada em DCFG-003). Sem isso, a primeira
tentativa de Plan Mode numa sessão nova falharia por diretório ausente.

**Decisão que levou à escolha:** sem registro formal além do código; é a contraparte funcional
da exceção que `guards/pretool` já concede a esse caminho específico.

**Classificação:** ESSENCIAL — pergunta 1: sim; sem custo de fricção (silencioso, no start do
container), e é o único lugar onde esse diretório é garantido.

**Estado de documentação:** ✅ coerente com o mecanismo de exceção do Plan Mode já descrito em
DCFG-003.

---

## DCFG-013 — `customizations.vscode`: hardening de autenticação Git no editor e extensões

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json) (`customizations.vscode`)

**Snapshot (2026-08-21):**

```json-nolint
"settings": {
  "terminal.integrated.defaultProfile.linux": "bash",
  "git.autofetch": false,
  "git.confirmSync": true,
  "git.terminalAuthentication": false,
  "git.useIntegratedAskPass": false,
  "github.gitAuthentication": false,
  "claudeCode.initialPermissionMode": "default"
},
"extensions": [
  "anthropic.claude-code",
  "openai.chatgpt"
]
```

**Por que foi adotado:** `git.terminalAuthentication`/`git.useIntegratedAskPass`/
`github.gitAuthentication` desligados impedem que a extensão Git do VS Code ofereça um fluxo de
autenticação próprio (askpass, OAuth do GitHub) que poderia se tornar um canal lateral de
credencial real dentro do container — reforça, na camada do editor, o mesmo objetivo de
DCFG-001 (nenhuma credencial real disponível ao agente). `claudeCode.initialPermissionMode:
"default"` garante que a extensão não inicie já num modo de permissão afrouxado.
`git.autofetch: false` evita chamadas de rede automáticas para remotes. As `extensions`
instalam as duas integrações de agente (Claude Code, Codex/ChatGPT) — sem elas, os agentes não
têm UI nativa no VS Code deste container.

**Decisão que levou à escolha:** sem registro formal além do código; consistente com o
objetivo de DCFG-001 (isolamento de credenciais), aplicado agora à camada do editor, não só ao
ambiente de processo.

**Classificação:** ESSENCIAL — pergunta 1: sim; é a única forma de impedir que a própria UI do
VS Code reabra um canal de autenticação que o resto do container fecha deliberadamente.

**Estado de documentação:** ⚠️ real e coerente com DCFG-001, nunca registrado como mecanismo
próprio até esta revisão.

---

## DCFG-014 — `forwardPorts`/`portsAttributes`: encaminhamento de porta do Vite

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json)

**Snapshot (2026-08-21):**

```json-nolint
"forwardPorts": [5173],
"portsAttributes": {
  "5173": { "label": "Vite", "onAutoForward": "notify" }
}
```

**Por que foi adotado:** conveniência de desenvolvimento — permite visualizar um servidor Vite
rodando dentro do container a partir do navegador do host. Não é um mecanismo de proteção; é o
único registro deste documento que existe puramente por funcionalidade, não por risco.

**Decisão que levou à escolha:** sem registro formal; inferida do nome da porta (`Vite`) e do
fato de o projeto usar esse bundler (não confirmado a partir deste documento).

**Correção material (revisão de 2026-08-21):** a versão anterior deste registro classificava
isto como ESSENCIAL "por ausência de alternativa melhor no esquema", contradizendo o próprio
algoritmo — que já previa este caso ("Se nenhum registro cair numa categoria, isso é um
resultado válido") sem definir um rótulo para ele. Corrigido: o algoritmo de classificação
agora nomeia esse resultado explicitamente como FUNCIONAL/NÃO APLICÁVEL (ver seção acima), e
este registro passa a usá-lo.

**Classificação:** FUNCIONAL/NÃO APLICÁVEL — as três perguntas do algoritmo pressupõem um
mecanismo de proteção; aqui não há risco sendo mitigado nem fricção sendo imposta, então
nenhuma das três categorias de risco se aplica.

**Estado de documentação:** ✅ coerente — não há política que precise mencionar isto.

---

## DCFG-015 — `claude-managed-settings.json`: lista `deny`

**Arquivo:** [`control-plane/claude-managed-settings.json`](../../../.devcontainer/control-plane/claude-managed-settings.json)

**Snapshot (2026-08-21):**

```json-nolint
"deny": [
  "Bash(sudo *)", "Bash(docker *)",
  "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)", "Bash(git pull *)",
  "Bash(git merge *)", "Bash(git rebase *)", "Bash(git cherry-pick *)", "Bash(git reset *)",
  "Bash(git restore *)", "Bash(git checkout *)", "Bash(git switch *)", "Bash(git worktree *)",
  "Bash(git clean *)", "Bash(git rm *)", "Bash(git stash *)", "Bash(git update-ref *)",
  "Read(//home/agent/.ssh/**)", "Read(//home/agent/.aws/**)",
  "Read(//home/agent/.config/gh/**)",
  "Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)",
  "Read(./.drive/CEPRAEA BEACH PRO/**)", "Read(./.drive/BEACH HANDBALL/**)"
]
```

**Por que foi adotado:** é a lista que, dentro do próprio Claude Code (independente do guard
`pretool` em shell), bloqueia as mesmas mutações Git já vedadas por `AGENT_POLICY.md §4`, e
adicionalmente proíbe **leitura** de credenciais reais do host (`.ssh`, `.aws`, `gh` config) e
de dados sensíveis do produto (`.env`, `secrets/`, e as duas pastas `.drive/` — dados pessoais
de atletas, conforme o `.gitignore` do repositório). É uma camada independente do `pretool`:
mesmo que o guard de shell falhasse, o Claude Code recusaria a chamada por conta própria.

**Decisão que levou à escolha:** sem registro formal além do código; a parte Git espelha
`AGENT_POLICY.md §4` e o `pretool` (redundância deliberada, ver DCFG-002 sobre por que
redundância em risco 🚨 Crítico é esperada). A parte de `Read` de credenciais/dados sensíveis
não tem contraparte declarada em nenhuma política escrita — é a lacuna mais concreta encontrada
nesta expansão.

**Classificação:** ESSENCIAL — pergunta 1: sim; impedir leitura de segredos reais e dados
pessoais é proporcional ao risco, e uma allowlist declarativa no próprio Claude Code é a forma
mais simples de fazer isso sem depender só do shell.

**Estado de documentação:** ⚠️ real — a parte de bloqueio de leitura de credenciais/dados
sensíveis nunca foi declarada em `AGENT_POLICY.md`, só existe aqui.

---

## DCFG-016 — `claude-managed-settings.json`: lista `ask`

**Arquivo:** [`control-plane/claude-managed-settings.json`](../../../.devcontainer/control-plane/claude-managed-settings.json)

**Snapshot (2026-08-21):**

```json-nolint
"ask": [
  "Bash(npm install *)",
  "Bash(npx *)"
]
```

**Por que foi adotado:** `npm install`/`npx` podem executar código arbitrário (scripts
`postinstall`, pacotes remotos via `npx`) — exigir confirmação explícita antes de cada execução
é a mitigação mais leve possível para esse risco de supply chain, sem bloquear o fluxo de
desenvolvimento normal.

**Decisão que levou à escolha:** sem registro formal além do código.

**Classificação:** ESSENCIAL — pergunta 1: sim; risco real de execução de código de terceiros,
mitigação proporcional (pedir confirmação, não bloquear). **Nota:** este é provavelmente o
mecanismo individual que mais contribui para a sensação de "autorizar cada ação" relatada no
início desta auditoria — é essencial e ainda assim é fricção sentida; as duas coisas não se
contradizem (ver "Como ler este documento").

**Estado de documentação:** ⚠️ real, sem contrapartida em `AGENT_POLICY.md`/`CLAUDE.md`.

---

## DCFG-017 — `claude-managed-mcp.json` (vazio)

**Arquivo:** [`control-plane/claude-managed-mcp.json`](../../../.devcontainer/control-plane/claude-managed-mcp.json)

**Snapshot (2026-08-21):**

```json
{
  "mcpServers": {}
}
```

**Por que foi adotado:** é o arquivo gerenciado de configuração MCP do Claude Code, montado
`root`-owned pelo mesmo mecanismo de DCFG-009 — hoje declara zero servidores MCP. A existência
do arquivo (mesmo vazio) é o que impede o Claude Code de cair de volta em uma configuração MCP
não gerenciada/local.

**Decisão que levou à escolha:** sem registro formal além do código.

**Classificação:** ESSENCIAL — pergunta 1: sim; é o estado mínimo necessário para que
`allowManagedHooksOnly`/config gerenciada (DCFG-005) cubra também MCP, sem adicionar nenhuma
superfície nova enquanto nenhum MCP for necessário.

**Estado de documentação:** ✅ coerente, nunca mencionado antes por não ter conteúdo — mas a
ausência de conteúdo é, em si, uma configuração intencional que vale registrar.

---

## DCFG-018 — `codex-requirements.toml`: restrições adicionais além do sandbox

**Arquivo:** [`control-plane/codex-requirements.toml`](../../../.devcontainer/control-plane/codex-requirements.toml)

**Snapshot (2026-08-21):**

```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_approvals_reviewers = ["user"]
allow_managed_hooks_only = true
allow_remote_control = false
allow_login_shell = false
allowed_web_search_modes = ["cached", "indexed"]

[features]
computer_use = false
browser_use_external = false
browser_use_full_cdp_access = false
```

**Por que foi adotado:** `allowed_approval_policies`/`allowed_approvals_reviewers` restringem
quem pode aprovar ações do Codex (só o usuário humano, nunca automático/outro agente);
`allow_remote_control = false` e `allow_login_shell = false` fecham dois canais que
permitiriam controlar a sessão do Codex remotamente ou abrir um shell de login fora do fluxo
normal; `allowed_web_search_modes` restringe busca web a modos `cached`/`indexed` (sem
navegação ao vivo); o bloco `[features]` desliga `computer_use` e as duas variantes de
`browser_use` — o Codex não pode operar um navegador nem "usar o computador" de forma genérica.
Em conjunto, é o mesmo princípio de DCFG-007 (Reviewer sem canais além do necessário para ler
diff e emitir veredito) aplicado às demais superfícies do Codex.

**Decisão que levou à escolha:** sem registro formal além do código; mesma lógica de
privilégio mínimo do Reviewer já documentada em `AGENT_POLICY.md` (papel Reviewer é read-only)
e em DCFG-007.

**Classificação:** ESSENCIAL — pergunta 1: sim; cada uma dessas flags fecha um canal que o
Reviewer não precisa para sua função (revisar diff, emitir veredito) e não há forma mais
simples de negar cada canal individualmente do que declará-lo `false`/restrito.

**Estado de documentação:** ⚠️ real, consistente com o papel Reviewer descrito em
`AGENT_POLICY.md`, mas essas flags específicas nunca foram citadas antes deste documento.

---

## DCFG-019 — `reviewer/devcontainer.json`: configuração separada para o papel Reviewer

**Arquivo:** [`reviewer/devcontainer.json`](../../../.devcontainer/reviewer/devcontainer.json)

**Snapshot (2026-08-21) — só o que difere do `devcontainer.json` do Executor:**

```json-nolint
"workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/cepraea-beach-pro,type=bind,readonly",
"mounts": [
  "source=cepraea-reviewer-codex,target=/home/agent/.codex,type=volume",
  "source=${localWorkspaceFolder}/.devcontainer/control-plane/gitconfig-agent,target=/etc/gitconfig,type=bind,readonly",
  "source=${localWorkspaceFolder}/.devcontainer/control-plane/gitconfig-agent,target=/home/agent/.gitconfig,type=bind,readonly",
  "source=${localWorkspaceFolder}/.devcontainer/control-plane/gitconfig-agent,target=/home/agent/.config/git/config,type=bind,readonly"
],
"customizations": { "vscode": { "extensions": ["openai.chatgpt"] } },
"postStartCommand": "test \"$(id -un)\" = agent && test ! -w /workspaces/cepraea-beach-pro && test ! -w /workspaces/cepraea-beach-pro/.git"
```

**Por que foi adotado:** existe um `devcontainer.json` inteiro separado para o Reviewer, não só
uma variação de configuração — a diferença mais material é `workspaceMount` com `readonly`
(**o checkout inteiro**, não só `.git`/`.devcontainer`/etc. como no Executor), e o
`postStartCommand` que **ativamente testa e falha** se o workspace ou `.git` estiverem
graváveis pelo usuário `agent` — uma auto-checagem executada a cada início de container, não
só uma declaração. Só a extensão `openai.chatgpt` é instalada (sem `anthropic.claude-code`),
reforçando que esta imagem é para o papel Reviewer, não Executor. Corresponde a `AGT-02`
(`VALIDADO`, `E2E-CODEX-BOUNDARY-01`) na matriz do `CONTAINER-RUNBOOK-v0.3.md §8`.

**Decisão que levou à escolha:** implementa diretamente `AGENT_POLICY.md` (Reviewer é
read-only no projeto) e a separação de papéis do `docs/arquiteturas/multi-agentes/`
Human-Governed Dual-Agent SDLC. Sem registro formal adicional além dessas fontes.

**Classificação:** ESSENCIAL — pergunta 1: sim; é a única forma de garantir, no nível do
mount (não só de política), que o processo do Reviewer não pode escrever no checkout —
mais forte que qualquer guard de aplicação, e o `postStartCommand` converte essa garantia em
um teste que falha ruidosamente se algo mudar.

**Estado de documentação:** ⚠️ real, coerente com `AGENT_POLICY.md`, mas nunca citado neste
documento até esta revisão — a auditoria original só examinou o `devcontainer.json` do
Executor.

---

## DCFG-020 — `scripts/verify-agent-environment.sh`: verificação manual do perfil BASE

**Arquivos:** [`scripts/verify-agent-environment.sh`](../../../.devcontainer/scripts/verify-agent-environment.sh),
[`scripts/README.md`](../../../.devcontainer/scripts/README.md)

**Snapshot (2026-08-21) — checagens principais do script:**

```bash
# usuário não-root, ausência de Docker socket, repositório acessível e é Git,
# SOURCE_ROOT (.drive/CEPRAEA BEACH PRO) existe e é read-only,
# managed-settings.json existe/root-owned/mode aceitável, guard pretool existe e é executável,
# .codex/config.toml (WARN se ausente) e /etc/codex/requirements.toml (FAIL se ausente),
# GITHUB_TOKEN / GH_TOKEN / SUPABASE_SERVICE_ROLE_KEY / VERCEL_TOKEN vazias
# → BASE_CONTAINER_CHECK=PASS|FAIL, exit 0|1
```

**Por que foi adotado:** é um verificador de pré-condições independente dos guards em
runtime — não substitui `pretool`/`claude-managed-settings.json`, confirma que eles *estão
presentes e configurados* (o próprio `scripts/README.md` diz isso explicitamente: "Não é uma
fronteira de segurança"). É também a única fonte, em todo `.devcontainer/`, que revela que o
produto usa **Supabase** e **Vercel** como credenciais de produção a manter fora do agente
(`SUPABASE_SERVICE_ROLE_KEY`, `VERCEL_TOKEN`) — informação de arquitetura do produto que não
aparece em nenhum outro lugar auditado neste documento.

**Achado de inconsistência (não corrigido nesta revisão — fora do escopo de um documento
somente-leitura):** `scripts/README.md` declara o modo de execução como "Manual ou via
`postStartCommand` do devcontainer". O `postStartCommand` real de
[`devcontainer.json`](../../../.devcontainer/devcontainer.json) (DCFG-012) **não invoca este
script** — só cria o diretório de planos do Claude Code. Ou seja: hoje este verificador só
roda se um humano ou agente o executar manualmente; a alegação "via postStartCommand" no
próprio README do script está desatualizada ou nunca foi implementada.

**Decisão que levou à escolha:** o script cita sua própria referência arquitetural:
`.drive/multi-agentes/Arquivos-Human-Governed Dual-Agent SDLC Architecture.md`, seção 9 — não
lida nesta auditoria (fora do escopo de `.devcontainer/`, e `.drive/` é dado sensível
bloqueado por DCFG-015).

**Classificação:** NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS — pergunta 1: não (a verificação
em si é útil, mas não roda automaticamente apesar de o próprio README alegar que pode).
Pergunta 2: sim — o mecanismo é necessário (dá visibilidade extra, incluindo as duas
credenciais de produto que nenhum outro registro cobre), mas a lacuna entre "documentado como
automático" e "só roda manualmente" é exatamente o tipo de divergência que motiva todo este
documento.

**Estado de documentação:** 🔴 defeito conhecido — o próprio `scripts/README.md` faz uma
alegação (`postStartCommand`) que o `devcontainer.json` real não sustenta.

---

## DCFG-021 — `devcontainer.json.before-git-auth-boundary-20260807T111848Z` (backup histórico)

**Arquivo:** [`devcontainer.json.before-git-auth-boundary-20260807T111848Z`](../../../.devcontainer/devcontainer.json.before-git-auth-boundary-20260807T111848Z)

**Snapshot (2026-08-21) — diferenças em relação ao `devcontainer.json` atual, via `diff`:**

```diff
- (versão anterior não tinha) mounts de scripts/ci, AGENT_POLICY.md, runbooks
- (versão anterior não tinha) git.terminalAuthentication / git.useIntegratedAskPass /
  github.gitAuthentication / claudeCode.initialPermissionMode
- (versão anterior não tinha) extensions (anthropic.claude-code, openai.chatgpt)
- (versão anterior não tinha) postStartCommand
```

**Por que foi adotado:** é um snapshot do `devcontainer.json` tirado antes do hardening de
autenticação Git descrito em DCFG-013 (nome do arquivo indica 2026-08-07) — preservado
provavelmente para permitir comparação ou rollback manual. **Não é configuração ativa**: não é
referenciado por nenhum outro arquivo, mount, ou script auditado neste documento.

**Decisão que levou à escolha:** sem registro formal — não há explicação, em nenhum lugar do
repositório verificado nesta auditoria, de por que o backup foi mantido versionado em vez de,
por exemplo, só existir no histórico do Git (`git show` de um commit anterior já cumpriria o
mesmo papel sem duplicar o arquivo no working tree).

**Classificação:** NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS — pergunta 1: não (o Git já
preserva esse histórico; manter uma cópia paralela no working tree não é a forma mais simples
de obter rastreabilidade). Pergunta 2: sim — preservar o estado pré-hardening tem valor de
auditoria, mas a forma escolhida (arquivo solto, sem explicação, sem convenção de nomes
declarada) é mais frágil do que necessário.

**Estado de documentação:** 🔴 defeito conhecido — arquivo presente no repositório sem
nenhuma explicação registrada em política, comentário ou README.

---

## DCFG-022 — Volumes nomeados: persistência de `.claude`/`.codex`/`.npm` do Executor

**Arquivo:** [`devcontainer.json`](../../../.devcontainer/devcontainer.json) (`mounts`),
contraponto em
[`reviewer/devcontainer.json`](../../../.devcontainer/reviewer/devcontainer.json) (`mounts`).

**Achado desta revisão:** o levantamento de 2026-08-21 que adicionou DCFG-009 a DCFG-021
("levantamento completo de `.devcontainer/`") não cobriu estes três volumes, apesar de já
estarem presentes em `devcontainer.json` antes dessa passada. É um mecanismo real, ausente do
documento até agora — não um mecanismo novo.

**Snapshot (2026-08-21) — Executor (`devcontainer.json`, mounts):**

```json-nolint
"source=cepraea-agent-claude,target=/home/agent/.claude,type=volume",
"source=cepraea-agent-codex,target=/home/agent/.codex,type=volume",
"source=cepraea-agent-npm,target=/home/agent/.npm,type=volume",
```

**Snapshot (2026-08-21) — Reviewer (`reviewer/devcontainer.json`, mounts, integral):**

```json-nolint
"mounts": [
  "source=cepraea-reviewer-codex,target=/home/agent/.codex,type=volume",
  // ... + 3 binds read-only de gitconfig (ver DCFG-019)
]
```

**Por que foi adotado:** volumes nomeados do Docker persistem entre reconstruções/reinícios do
container — diferente do restante do filesystem do container, que é efêmero. Sem eles, cada
rebuild perderia sessões e planos salvos do Claude Code, estado/autenticação de uso do Codex
CLI, e o cache de pacotes npm já baixados, forçando reautenticação/reinstalação a cada rebuild.
Diferem estruturalmente dos mounts de DCFG-002: aqueles são bind mounts read-only apontando
para arquivos do host; estes são volumes Docker geridos pelo próprio Docker (não existem no
host fora dele) e graváveis pelo usuário `agent`.

**Isolamento Executor/Reviewer:** os nomes são distintos por perfil (`cepraea-agent-*` vs.
`cepraea-reviewer-*`) — nenhum volume é compartilhado entre os dois containers; uma sessão do
Reviewer não pode ler nem escrever o estado persistido pelo Executor, nem vice-versa. O
Reviewer só persiste `.codex` — sem volume equivalente para `.claude` nem `.npm`, coerente com
não instalar a extensão `anthropic.claude-code` nem depender de pacotes npm no fluxo de
revisão (só `openai.chatgpt`, ver DCFG-019).

**Riscos conhecidos (não cobertos por nenhum outro registro):** estes volumes podem reter,
entre execuções, estado de sessão/autenticação de uso das CLIs (Claude Code, Codex — não
credenciais de Git/GitHub, que seguem vazias por DCFG-001) e cache de pacotes npm. Nenhum
registro deste documento descreve o ciclo de vida desses volumes — quando são criados, se são
apagados em algum fluxo, se sobrevivem a uma limpeza de containers (`docker system prune` sem
`--volumes` não os remove, por padrão do Docker). É lacuna análoga a `MNT-01`/`MNT-02`
(`PENDENTE` no runbook, já citada em DCFG-001), mas para volumes nomeados em vez de bind mounts
de diretórios pessoais.

**Decisão que levou à escolha:** sem registro formal além do código.

**Classificação:** NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS — pergunta 1: não (a persistência
de sessão em si não tem alternativa mais simples com o mesmo benefício, mas isso não é o que
falta). Pergunta 2: sim — a persistência é necessária, mas falta o mesmo tipo de inventário e
definição de ciclo de vida que `MNT-01`/`MNT-02` já cobram para mounts de diretórios pessoais;
sem isso, não há como confirmar por quanto tempo e com que alcance esse estado de sessão fica
retido.

**Estado de documentação:** 🔴 defeito conhecido até esta revisão — mecanismo real, presente em
`devcontainer.json` desde antes desta auditoria, nunca registrado em nenhuma passada anterior
apesar da alegação de "levantamento completo" (ver changelog).

---

## Resumo

| ID | Mecanismo | Estado de documentação | Classificação |
|---|---|---|---|
| DCFG-001 | Isolamento de credenciais | ✅ coerente | ESSENCIAL |
| DCFG-002 | Mounts read-only do plano de controle | ✅ coerente | ESSENCIAL |
| DCFG-003 | Guard de caminho (zonas intocáveis) | ✅ coerente | ESSENCIAL |
| DCFG-004 | Bloqueio total de Bash/Edit/Write em `main` | ⚠️ não documentado até este arquivo | NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS |
| DCFG-005 | Bypass de permissão desativado no build | ⚠️ não documentado até este arquivo | ESSENCIAL |
| DCFG-006 | Sandbox interno do Claude desativado | ⚠️ fundamentada (DEC-ARQ-001), decisão em status PROPOSTA | ESSENCIAL, com 2 lacunas de evidência pendentes |
| DCFG-007 | Boundary do Codex (P-002 / SEC-02) | ⚠️ validado no runbook, comentário do `.toml` desatualizado | ESSENCIAL |
| DCFG-008 | Log de auditoria | ✅ coerente (terminologia corrigida) | ESSENCIAL, escopo limitado a observabilidade best-effort |
| DCFG-009 | `Dockerfile` completo | ⚠️ real, nunca tratado como registro próprio (atribuição a DCFG-002 corrigida nesta revisão) | ESSENCIAL |
| DCFG-010 | `runArgs` (hardening de privilégios) | ⚠️ real, coerente com DEC-ARQ-001 | ESSENCIAL |
| DCFG-011 | Identidade de usuário e montagem do workspace | ⚠️ real, coerente | ESSENCIAL |
| DCFG-012 | `postStartCommand` (diretório de planos) | ✅ coerente com DCFG-003 | ESSENCIAL |
| DCFG-013 | `customizations.vscode` (hardening + extensões) | ⚠️ real, coerente com DCFG-001 | ESSENCIAL |
| DCFG-014 | `forwardPorts`/`portsAttributes` (Vite) | ✅ coerente — não é mecanismo de proteção | FUNCIONAL/NÃO APLICÁVEL (reclassificado nesta revisão, era ESSENCIAL) |
| DCFG-015 | `claude-managed-settings.json`: lista `deny` | ⚠️ real, sem contrapartida em AGENT_POLICY.md | ESSENCIAL |
| DCFG-016 | `claude-managed-settings.json`: lista `ask` | ⚠️ real, sem contrapartida em AGENT_POLICY.md | ESSENCIAL |
| DCFG-017 | `claude-managed-mcp.json` (vazio) | ✅ coerente | ESSENCIAL |
| DCFG-018 | `codex-requirements.toml`: restrições adicionais | ⚠️ real, coerente com AGENT_POLICY.md | ESSENCIAL |
| DCFG-019 | `reviewer/devcontainer.json` | ⚠️ real, coerente com AGENT_POLICY.md | ESSENCIAL |
| DCFG-020 | `scripts/verify-agent-environment.sh` | 🔴 defeito conhecido (README alega automação que não existe) | NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS |
| DCFG-021 | Backup `devcontainer.json.before-git-auth-boundary-*` | 🔴 defeito conhecido (sem explicação registrada) | NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS |
| DCFG-022 | Volumes nomeados (`cepraea-agent-claude/codex/npm`) | 🔴 defeito conhecido (ausente do levantamento anterior) | NECESSÁRIA PORÉM PRECISA DE REFINAMENTOS |

*Nenhum registro caiu em "excesso de governança" em nenhuma das passadas.* Um registro
(DCFG-014) caiu no resultado "nenhuma das três categorias de risco se aplica", já previsto no
próprio algoritmo (ver seção "Algoritmo de classificação") e agora nomeado explicitamente como
FUNCIONAL/NÃO APLICÁVEL — não é "excesso de governança" (não existe fricção de segurança para
reduzir) nem uma quarta categoria de risco. Se a classificação de algum registro mudar no
futuro (ex.: um mecanismo que hoje é proporcional deixar de ser quando o projeto sair do
estágio de pré-implantação), isso deve virar uma nova entrada no changelog abaixo, não uma
edição silenciosa dos registros existentes.

Correções de configuração/documentação ficam identificadas e pendentes de decisão separada:
**DCFG-004** (allowlist de leitura também em `main`), **DCFG-020** (fazer o `postStartCommand`
realmente invocar `verify-agent-environment.sh`, ou corrigir o `README.md` do script para não
alegar automação inexistente), **DCFG-021** (explicar por que o backup é mantido versionado,
ou removê-lo em favor do histórico do Git), **DCFG-022** (definir e documentar o ciclo de vida
dos três volumes nomeados do Executor — criação, retenção, limpeza). **DCFG-006** e **DCFG-007**
continuam como mecanismos corretos e fundamentados, com lacunas de **evidência/governança**
pendentes: ratificação auditável de `DEC-ARQ-001`, comprovação centralizada de `ISO-05`, e
atualização do comentário desatualizado em `codex-requirements.toml` (corrigido nesta revisão).
Nenhuma correção de *configuração* foi aplicada em nenhuma das passadas deste documento — só
leitura, registro e, nesta revisão, correção de afirmações incorretas dentro do próprio
documento (DCFG-009, DCFG-014) e cobertura de um mecanismo antes ausente (DCFG-022).

## Changelog documental

| Data | Mudança |
|: ---: | --- |
| 2026-08-21 | Criação inicial — auditoria dos 8 mecanismos, estado de documentação (✅/⚠️/🔴). |
| 2026-08-21 | Reestruturação: IDs únicos (`DCFG-00N`), snapshot literal por registro, campos "por que foi adotado" / "decisão que levou à escolha" separados, algoritmo de classificação de governança (essencial / necessária porém precisa de refinamentos / excesso de governança) aplicado a cada registro, changelog documental. |
| 2026-08-21 | Correção pós-revisão do Reviewer (FAIL): DCFG-006 e DCFG-007 estavam classificados como defeito sem justificativa localizável — busca ampliada encontrou `.ai/decisions/DEC-ARQ-001-dev-container-como-sandbox-operacional.md` e `docs/arquiteturas/multi-agentes/containers/CONTAINER-RUNBOOK-v0.3.md`, que fundamentam ambos e mudam sua classificação para ESSENCIAL (com ressalvas de evidência explícitas). DCFG-001 teve o escopo da garantia restringido (não cobre rede nem inventário completo de segredos, per `NET-01`/`CRE-04` `PENDENTE`). DCFG-008 teve o termo "append-only" corrigido para descrever a garantia real (sem imutabilidade). |
| 2026-08-21 | Ampliação de cobertura, a pedido de Davi ("identifique se todas as configurações atuais do container estão registradas"): levantamento completo de `.devcontainer/` encontrou 13 mecanismos ausentes ou só parcialmente cobertos pelos 8 registros originais. Adicionados `DCFG-009` a `DCFG-021`, mesma numeração sequencial, mesma estrutura de campos: `Dockerfile` completo (009), `runArgs`/hardening (010), identidade de usuário/mount (011), `postStartCommand` (012), `customizations.vscode` (013), `forwardPorts` (014), listas `deny`/`ask` do Claude (015/016), `claude-managed-mcp.json` (017), restrições adicionais do Codex (018), `reviewer/devcontainer.json` (019), `scripts/verify-agent-environment.sh` (020 — defeito encontrado: seu próprio README alega execução via `postStartCommand`, que não acontece), e o backup `devcontainer.json.before-git-auth-boundary-*` (021 — sem explicação registrada em lugar nenhum). Nenhuma configuração foi alterada; só leitura e registro. |
| 2026-08-21 | Correção pós-revisão (FAIL): (1) adicionado `DCFG-022`, cobrindo os três volumes nomeados (`cepraea-agent-claude/codex/npm`) que a passada anterior alegou ter coberto por completo mas não cobriu; (2) `DCFG-014` reclassificado de ESSENCIAL para FUNCIONAL/NÃO APLICÁVEL, e o "Algoritmo de classificação" passou a nomear esse resultado explicitamente, em vez de deixá-lo implícito e depois contradizê-lo; (3) `DCFG-009` corrigido — a lista de mecanismos dependentes do `Dockerfile` incluía indevidamente `DCFG-002` (mounts), que é declarado inteiramente em `devcontainer.json` e não depende do `Dockerfile`. Nenhuma configuração real foi alterada — só correção de afirmações incorretas dentro do próprio documento e registro do mecanismo ausente. |

*Entradas futuras devem ser adicionadas por quem editar o documento depois* — não numerar
retroativamente nem reescrever entradas já registradas.
