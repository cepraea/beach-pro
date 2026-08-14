# Registro de decisões

Um bloco `json` por `DEC-NNN`, validado contra `schema_decisao.json` (seção 5.2 do plano). Cada
entrada é precedida por um resumo em prosa para leitura humana; o bloco `json` é a fonte
verificável para `validar.mjs`.

## DEC-008 — Remoção da worktree irmã da modelagem

Durante `AC-000` (primeira e segunda tentativas, ver `.agent-flow/executions/AC-000.md`), dois
bloqueios operacionais reais impediram a criação da worktree irmã prevista na seção 4.7 original
do plano:

1. o `EXECUTOR` não tem permissão de escrita em `.git/refs/heads` (nem, mais amplamente, em
   `.git/` do repositório principal) — não consegue criar refs/branches;
2. a worktree irmã criada manualmente por Davi no host
   (`/home/davis/projetos/cepraea-modelagem-canonica`) não é visível dentro do devcontainer do
   `EXECUTOR` — só o próprio diretório do repositório é montado no container.

A worktree foi criada corretamente no host, apontando para o `BASE_SHA` aprovado
(`88394023d27f55fe11a7134a1b7762cf7abbf32f`), mas permaneceu inacessível ao ambiente do agente.
Nenhum artefato de modelagem havia sido criado até este ponto.

**Decisão:** remover o uso obrigatório de worktree irmã do processo de modelagem. A modelagem
passa a ser executada diretamente no repositório `cepraea-beach-pro`, exclusivamente na branch
dedicada `feat/cepraea-domain-modeling`. O isolamento passa a ser garantido por branch dedicada +
`WRITE_SCOPE` explícito e restrito + `SOURCE_ROOT` somente leitura + guardrails já existentes do
devcontainer + revisão independente pelo `REVIEWER` (`CODEX`), em vez de separação física de
diretório via worktree.

```json
{
  "id_decisao": "DEC-008",
  "data": "2026-08-12",
  "decisao": "Remoção da worktree irmã (<repo-parent>/cepraea-modelagem-canonica) como mecanismo obrigatório de isolamento da modelagem CEPRAEA-BEACH-PRO, prevista na seção 4.7 original do plano.",
  "alternativas": [
    "Manter a worktree irmã e reconfigurar o devcontainer para montar o diretório pai do repositório",
    "Relocar a worktree para um caminho já montado dentro do container",
    "Executar o bootstrap de AC-000 fora deste ambiente protegido, em uma sessão com acesso direto ao filesystem do host"
  ],
  "escolha": "Executar a modelagem diretamente no repositório cepraea-beach-pro, na branch dedicada feat/cepraea-domain-modeling, com isolamento garantido por branch dedicada + WRITE_SCOPE explícito + SOURCE_ROOT somente leitura + guardrails existentes do Dev Container + revisão independente, em vez de worktree irmã.",
  "justificativa": "A worktree irmã introduziu uma dependência de infraestrutura (mount do diretório pai do repositório no host) incompatível com o ambiente protegido atual do EXECUTOR, sem ser estritamente necessária para preservar o isolamento da modelagem. Branch dedicada + WRITE_SCOPE explícito + guardrails do devcontainer (main/master protegidas, .git somente leitura, hook de comandos privilegiados) + revisão independente pelo REVIEWER fornecem o isolamento necessário com menor complexidade operacional, sem enfraquecer nenhum controle existente.",
  "fonte": [
    "AC-000",
    ".agent-flow/executions/AC-000.md",
    "instrução direta de Davi Sermenho nesta sessão, 2026-08-12"
  ],
  "impacto": "AC-000 deixa de criar/validar uma worktree irmã; seus critérios de DONE passam a validar branch dedicada, BASE_SHA, SOURCE_ROOT, WRITE_SCOPE e ausência de escrita fora do escopo, em vez de existência de worktree. verificar_repositorio.mjs deverá verificar branch e paths permitidos em vez de existência de worktree irmã. Seção 4.7, itens 4/5 do critério de DONE (seção 10.1), GATE E (seção 11) e a tabela de papéis de arquivo (seção 12) do plano são atualizados para refletir esta decisão.",
  "riscos": [
    "Sem separação física de diretório, ferramentas do repositório principal podem, em tese, enxergar artefatos de modelagem como conteúdo operacional do projeto durante o desenvolvimento — mitigado por WRITE_SCOPE restrito a docs/modelagem/** e por nunca escrever em main/master. (.agent-flow/** removido em DEC-GOV-001, 2026-08-14)",
    "Nenhum guardrail, hook ou controle do Dev Container é removido ou enfraquecido por esta decisão — o isolamento anterior por diretório é substituído por isolamento por branch + escopo, não removido sem substituto."
  ],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": {
      "action_ref": "AC-000"
    }
  }
}
```

### Escopos formais (substituem os da seção 4.7 original)

```text
WRITE_SCOPE_EXECUTOR
  docs/modelagem/**
  # .agent-flow/executions/** — REMOVIDO (DEC-GOV-001, 2026-08-14)

WRITE_SCOPE_REVIEWER
  # .agent-flow/reviews/** — REMOVIDO (DEC-GOV-001, 2026-08-14)
  # Reviewer não produz artefatos de escrita; emite verdict ao humano.

READ_SCOPE
  repositório cepraea-beach-pro, quando necessário à ação
  .drive/CEPRAEA BEACH PRO/**

CEPRAEA_SOURCE_ROOT
  .drive/CEPRAEA BEACH PRO

MODO (CEPRAEA_SOURCE_ROOT)
  READ_ONLY
```

### Isolamento substituto (em vez de worktree irmã)

1. branch dedicada `feat/cepraea-domain-modeling`, diferente de `main`/`master`;
2. `WRITE_SCOPE` explícito e restrito (acima);
3. `SOURCE_ROOT` em modo somente leitura;
4. guardrails existentes do Dev Container (hook `pretool`, `.git` protegido, branches de plano de
   controle protegidas);
5. proteção do plano de controle e de `.git` (já em vigor, não alterada por esta decisão);
6. validação de `git diff`/`git status` a cada ação, como já exigido pelo processo (seção 7,
   `EXECUTOR.md`);
7. revisão independente pelo `REVIEWER` (`CODEX`);
8. operações Git privilegiadas (commit, push, merge, rebase, criação de branch/ref) executadas
   somente por Davi — inalterado, já era a regra (`AGENT_POLICY.md` §Autoridade).

## DEC-GOV-001 — Substituição do workflow .agent-flow por Git como state machine operacional

Durante `AC-000` (ver `DEC-008`), a arquitetura baseada em `.agent-flow/STATE.md`,
`EXECUTOR.md`, `REVIEWER.md` e diretórios `executions/**` / `reviews/**` como mecanismo de
workflow foi identificada como fonte redundante de estado paralela ao Git.

A revisão arquitetural produzida em `.drive/multi-agentes/` (2026-08-13, status FINAL PARA
ADOÇÃO — REVISÃO 2) define Git como a única state machine operacional, substituindo os
adaptadores de papel e a infraestrutura de estado anterior.

**Decisão:** remover `.agent-flow/**` como mecanismo obrigatório de workflow. Os artefatos
históricos são preservados no histórico Git, mas não são mais autoridade operacional.

```json
{
  "id_decisao": "DEC-GOV-001",
  "data": "2026-08-14",
  "decisao": "Substituição do workflow baseado em .agent-flow/STATE.md, EXECUTOR.md, REVIEWER.md e executions/**/reviews/** por Git como única state machine operacional, conforme arquitetura Human-Governed Dual-Agent SDLC (FINAL PARA ADOÇÃO — REVISÃO 2).",
  "alternativas": [
    "Manter .agent-flow como mecanismo de estado paralelo ao Git",
    "Arquivar .agent-flow como referência sem uso operacional (escolhida)"
  ],
  "escolha": "Git como state machine operacional. .agent-flow removido do fluxo ativo. Histórico preservado no Git. EXECUTOR.md substituído por CLAUDE.md. REVIEWER.md substituído por AGENTS.md. executions/** e reviews/** não são obrigatórios.",
  "justificativa": "STATE.md e os diretórios de execução/revisão criavam duas fontes de verdade paralelas ao Git, introduzindo risco de divergência sem adicionar rastreabilidade que Git não forneça. A arquitetura revisada unifica estado, handoff e histórico em Git, eliminando infraestrutura desnecessária.",
  "fonte": [
    "DEC-008",
    ".drive/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md",
    ".drive/multi-agentes/Implantação-Human-Governed Dual-Agent SDLC Archite.md",
    "instrução direta de Davi Sermenho, 2026-08-14"
  ],
  "impacto": {
    "STATE.md": "não mais autoridade operacional",
    "EXECUTOR.md": "substituído por CLAUDE.md",
    "REVIEWER.md": "substituído por AGENTS.md",
    "executions/**": "não obrigatório; pode ser produzido quando evidência possuir valor material próprio",
    "reviews/**": "não obrigatório; Reviewer emite verdict ao humano",
    "Git": "state machine operacional, mecanismo de handoff e histórico persistente"
  },
  "riscos": [
    "Agentes que lerem artefatos antigos de .agent-flow podem interpretar STATE.md como autoridade — mitigado por esta decisão e pela atualização de CLAUDE.md e AGENTS.md.",
    "Ausência de log estruturado de execução pode dificultar auditoria retroativa — mitigado por convenção de mensagem de commit (AC-NNN, SEM-NNN, SYN-NNN) e pela política de evidência material."
  ],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": {
      "action_ref": "AC-000",
      "branch": "feat/cepraea-domain-modeling"
    }
  }
}
```
