# Registro de decisões

Um bloco `json` por `DEC-NNN`, validado contra `schema_decisao.json` (seção 5.2 do plano). Cada
entrada é precedida por um resumo em prosa para leitura humana; o bloco `json` é a fonte
verificável para `validar.mjs`.

## DEC-001 — Estado do arquivo Wellness Apps Script Mobile e de sua cópia (D-01)

Durante esta sessão, `CEPRAEA — Wellness — Apps Script Mobile.txt` foi apagado acidentalmente por
Davi e já foi restaurado por ele — confirmado presente. A cópia
`Cópia de CEPRAEA — Wellness — Apps Script Mobile.txt` continua ausente; Davi decidiu que ela não é
necessária, já que o original já supre a fonte.

```json
{
  "id_decisao": "DEC-001",
  "data": "2026-08-15",
  "decisao": "Estado do arquivo 'CEPRAEA — Wellness — Apps Script Mobile.txt' e de sua cópia, após exclusão acidental durante a sessão (D-01).",
  "alternativas": [
    "Restaurar também a cópia 'Cópia de CEPRAEA — Wellness — Apps Script Mobile.txt'",
    "Tratar o original restaurado como suficiente e não restaurar a cópia"
  ],
  "escolha": "O original foi restaurado por Davi e está confirmado presente. A cópia não foi restaurada — Davi decidiu que ela não é necessária, já que o original já supre a fonte.",
  "justificativa": "O conteúdo relevante para a modelagem está no original; a cópia não acrescenta evidência distinta.",
  "fonte": ["REF:D-01, seção 0 de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md"],
  "impacto": "AC-020 processa o original normalmente; AC-021 nasce estado_processamento=NAO_APLICAVEL, sem conteúdo a analisar.",
  "riscos": [],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": { "action_ref": "AC-000" }
  }
}
```

## DEC-002 — Não reaproveitamento dos schemas físicos da tentativa anterior (D-02)

O fluxo de modelagem anterior foi declarado falho por Davi. Consequência: nenhum dos dois schemas
físicos anteriores — as 23 tabelas de `BancoCEPRAEA.docx` e as 13 tabelas citadas pelo "Glossário
v0.2" — é reaproveitado como base do modelo lógico desta fase.

```json
{
  "id_decisao": "DEC-002",
  "data": "2026-08-15",
  "decisao": "Reaproveitamento (ou não) dos schemas físicos da tentativa de modelagem anterior como base do modelo lógico desta fase.",
  "alternativas": [
    "Reaproveitar as 23 tabelas de BancoCEPRAEA.docx como ponto de partida",
    "Reaproveitar as 13 tabelas citadas pelo 'Glossário v0.2' como ponto de partida",
    "Não reaproveitar nenhum dos dois; derivar o modelo lógico exclusivamente do Modelo Canônico desta fase"
  ],
  "escolha": "Nenhum dos dois schemas físicos anteriores é reaproveitado como base do modelo lógico desta fase. O modelo lógico nasce do Modelo Canônico sustentado pelas fontes relevantes segundo autoridade e finalidade, não desses documentos.",
  "justificativa": "O fluxo de modelagem anterior foi declarado falho por Davi (D-02) — os dois schemas físicos ficaram incompatíveis entre si e sem resolução.",
  "fonte": ["REF:D-02, seção 0 de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md"],
  "impacto": "BancoCEPRAEA.docx, CEPRAEA-DB.docx, DESC-CEPRAEA.docx, Glossário de Dados — CEPRAEA v0.1.xlsx e o REGISTRO MESTRE nascem autoridade_fonte=AUXILIAR e estado_fonte=SUBSTITUIDA em seus dossiês, independente de completude técnica (melhoria d).",
  "riscos": [],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": { "action_ref": "AC-000" }
  }
}
```

## DEC-003 — "STOP GATE fechado" vs. "DDL completo escrito" não se contradizem (D-03)

Uma investigação anterior nesta sessão havia caracterizado como contradição direta a frase do
REGISTRO MESTRE ("STOP GATE físico permaneceu fechado; nenhum SQL, schema, migration, RLS ou banco
externo foi criado") frente à frase de `BancoCEPRAEA.docx` ("o repositório atual contém... mas não
possui migrations de domínio implementadas"). Verificação direta dos dois documentos-fonte mostrou
que isso é impreciso.

```json
{
  "id_decisao": "DEC-003",
  "data": "2026-08-15",
  "decisao": "Se \"STOP GATE físico permaneceu fechado\" (REGISTRO MESTRE) contradiz \"o repositório atual contém... dependência Supabase, mas não possui migrations de domínio implementadas\" (BancoCEPRAEA.docx).",
  "alternativas": [
    "Tratar como contradição direta entre as duas fontes, exigindo resolução de precedência",
    "Reler os dois textos-fonte diretamente e verificar se as frases realmente se referem ao mesmo fato"
  ],
  "escolha": "As duas frases provavelmente não se contradizem. 'SQL foi escrito como proposta dentro de um documento' e 'nenhum SQL foi criado [executado contra um banco real]' podem ser verdadeiras ao mesmo tempo — o REGISTRO MESTRE audita o ecossistema de planilhas, não todos os documentos da pasta; e o próprio REGISTRO MESTRE instrui, na aba 00, não promover documento REVIEWED/rascunho/cópia/predecessor/evidência a estado APPROVED/CURRENT, exatamente a regra que a investigação anterior não aplicou ao DDL de BancoCEPRAEA.docx.",
  "justificativa": "Verificação direta dos dois documentos-fonte (REGISTRO MESTRE DE ARTEFATOS E FUNCIONAMENTO — SISTEMA CEPRAEA.docx, linha 864 do texto extraído; BancoCEPRAEA.docx, linha 45 do texto extraído), não apenas do resumo de uma investigação anterior.",
  "fonte": [
    "REF:D-03, seção 0 de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md",
    ".drive/CEPRAEA BEACH PRO/REGISTRO MESTRE DE ARTEFATOS E FUNCIONAMENTO — SISTEMA CEPRAEA.docx",
    ".drive/CEPRAEA BEACH PRO/BancoCEPRAEA.docx"
  ],
  "impacto": "Nenhum — D-03 fecha como não-contradição, sem alterar a classificação de nenhuma fonte. Fica registrada, sem bloquear nada, uma curiosidade residual de baixa prioridade: a menção a 'dependência Supabase' em BancoCEPRAEA.docx não tem informação suficiente, nos dois textos, para determinar se é só um package.json com @supabase/supabase-js (baixo risco) ou algo mais.",
  "riscos": [],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": { "action_ref": "AC-000" }
  }
}
```

## DEC-006 — Contagem atual de atletas e treinador

Davi confirmou diretamente, como especialista do domínio, a contagem de 19 atletas e 1 treinador
no estado atual do CEPRAEA-BEACH-PRO (`modelagem_dominio_dados.md` §7 já registrava o mesmo
número). Aceita como válida a partir desta decisão, não como candidata a confirmar.

```json
{
  "id_decisao": "DEC-006",
  "data": "2026-08-15",
  "decisao": "Contagem atual de atletas e treinador no CEPRAEA-BEACH-PRO, para orientar (sem determinar sozinha) a modelagem de identidades e papéis operacionais.",
  "alternativas": [
    "Tratar a contagem como candidata a confirmar por AC-001/AC-004/AC-008–AC-010/AC-016–AC-019",
    "Aceitar a contagem já confirmada por Davi como válida a partir desta decisão"
  ],
  "escolha": "Davi confirmou diretamente, como especialista do domínio, a contagem de 19 atletas e 1 treinador no estado atual do CEPRAEA-BEACH-PRO (modelagem_dominio_dados.md §7 já registrava o mesmo número). Aceita como válida a partir desta decisão, não como candidata a confirmar.",
  "justificativa": "Confirmação direta de Davi Sermenho nesta sessão, coerente com o número já registrado em modelagem_dominio_dados.md §7.",
  "fonte": ["REF:modelagem_dominio_dados.md §7", "REF:seção 4.2 de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md"],
  "impacto": "Nota operacional: se AC-001, AC-004, AC-008–AC-010, AC-016–AC-019 contarem um número diferente, isso é divergência temporal/operacional (elenco muda ao longo do tempo), registrada como novo item em decisoes/registro_decisoes.md — não uma contradição do que já foi validado, e não substituída silenciosamente.",
  "riscos": [],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": { "action_ref": "AC-000" }
  }
}
```

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

## DEC-GOV-001 — Substituição do workflow .agent-flow por Git como state machine operacional (referência)

Durante `AC-000` (ver `DEC-008`), a arquitetura baseada em `.agent-flow/STATE.md`,
`EXECUTOR.md`, `REVIEWER.md` e diretórios `executions/**` / `reviews/**` como mecanismo de
workflow foi identificada como fonte redundante de estado paralela ao Git.

**Esta entrada é referência, não o registro canônico** (resolução de `DEC-011`, achado do
`REVIEWER` em `AC-000`): `DEC-GOV-001` é uma decisão de governança do SDLC do CEPRAEA BEACH PRO —
domínio distinto das decisões de modelagem que este arquivo registra, com prefixo (`DEC-GOV-NNN`)
e forma de dados (`impacto` estruturado por componente) próprios. Misturá-la ao namespace `DEC-NNN`
sequencial e ao `schema_decisao.json` desta fase forçaria o schema a acomodar dois domínios com
condicionais ad-hoc — por isso ela não valida contra `schema_decisao.json` e não deveria. O
registro canônico, completo e já aprovado está em
[`.ai/decisions/DEC-GOV-001-agent-flow-legado.md`](../../../.ai/decisions/DEC-GOV-001-agent-flow-legado.md).

Resumo para contexto desta fase: Git passa a ser a única state machine operacional, substituindo
`.agent-flow/STATE.md`/`EXECUTOR.md`/`REVIEWER.md`/`executions/**`/`reviews/**`. `EXECUTOR.md` foi
substituído por `CLAUDE.md`; `REVIEWER.md` por `AGENTS.md`. Consequência direta para `AC-000`: os
escopos formais desta fase (seção "Escopos formais", acima) já refletem essa decisão.

## DEC-GOV-002 — `runbook_binding` formal da fase de modelagem canônica (referência)

Durante a revisão adversarial de `AC-001`, o `REVIEWER` apontou que nenhum `runbook_binding`
concreto para as tarefas `AC-NNN`/`SEM-NNN`/`SYN-NNN` desta fase estava registrado em local
verificável do repositório (`HUMAN_DECISION_REQUIRED`). Davi aprovou o binding formal.

Mesmo motivo de `DEC-GOV-001` acima: é uma decisão de governança do SDLC (vinculação de runbooks a
uma classe de operação), não uma decisão de modelagem do domínio CEPRAEA — não valida contra
`schema_decisao.json` e não deveria (precedente de `DEC-011`, abaixo). O registro canônico está em
[`.ai/decisions/DEC-GOV-002-runbook-binding-modelagem-canonica.md`](../../../.ai/decisions/DEC-GOV-002-runbook-binding-modelagem-canonica.md).

Resumo para contexto desta fase: toda tarefa `AC-NNN`/`SEM-NNN`/`SYN-NNN` usa
`operation_class=documentation_change` → Executor: `RB-EXEC-003`; Reviewer: `RB-REV-003` +
`RB-REV-004` (evidência é material nesta fase, ver justificativa no registro canônico); Shared:
`RB-SHARED-001/002/003`.

## DEC-011 — Forma de `id_decisao`/`impacto` de decisões de governança dentro de `schema_decisao.json`

Durante a validação de `AC-000`, `DEC-GOV-001` (já `RESOLVIDA`/commitada antes deste `AC-000`) não
conforma ao `schema_decisao.json` extraído literalmente da seção 5.2 do plano:
`id_decisao="DEC-GOV-001"` não corresponde a `^DEC-[0-9]{3}$`, e `impacto` é um objeto estruturado
por componente, não `string`/`null`.

O `EXECUTOR` tentou inicialmente resolver isso estendendo o schema unilateralmente
(`id_decisao` passando a aceitar `DEC-GOV-NNN`; `impacto` passando a aceitar `object` sem validar
sua estrutura interna). Revisão independente do `REVIEWER` apontou, corretamente, que isso é uma
decisão material sobre a forma do próprio contrato de dados — não uma correção mecânica que o
`EXECUTOR` possa fazer sozinho, mesmo sinalizando a extensão como pendente de confirmação. A
extensão foi revertida; `schema_decisao.json` está, nesta revisão, fiel ao texto literal da seção
5.2.

```json
{
  "id_decisao": "DEC-011",
  "data": "2026-08-15",
  "decisao": "Como schema_decisao.json deve tratar o formato de DEC-GOV-001 (id_decisao fora do padrão DEC-NNN; impacto como objeto estruturado por componente, não string) — decisão já RESOLVIDA e commitada antes deste AC-000, cujo formato diverge do schema desta fase.",
  "alternativas": [
    "Incorporar formalmente o padrão DEC-GOV-NNN ao contrato de schema_decisao.json, com impacto aceitando string ou objeto (com estrutura validada)",
    "Separar decisões de governança do SDLC (DEC-GOV-NNN) do corpus de decisões de modelagem — realocar para um registro próprio, fora de schema_decisao.json",
    "Manter schema_decisao.json fiel à seção 5.2 do plano e aceitar que validar.mjs sobre o corpus real reporte 1 erro conhecido e rastreado sobre DEC-GOV-001 até esta decisão ser tomada"
  ],
  "escolha": "Alternativa 2 — separar decisões de governança do SDLC (DEC-GOV-NNN) do corpus de decisões de modelagem. O prefixo diferente (GOV) e a forma de dados diferente (impacto como objeto estruturado, não string) são sinal de que a decisão pertence a outro domínio; forçá-la no mesmo schema criaria condicionais ad-hoc (\"se id começa com GOV então impacto deve ser objeto\") que comprometeriam a escalabilidade do modelo de documentação. DEC-GOV-001 já tinha registro canônico próprio, em formato de prosa, em .ai/decisions/DEC-GOV-001-agent-flow-legado.md — a entrada dentro de decisoes/registro_decisoes.md vira referência textual a esse registro, sem bloco json, sem tentar validar contra schema_decisao.json.",
  "justificativa": "Confirmado diretamente por Davi Sermenho: prefixo e estrutura de dados divergentes são code smell de domínio distinto, não uma variação a acomodar dentro do mesmo contrato.",
  "fonte": [
    "REF:docs/modelagem/decisoes/registro_decisoes.md — DEC-GOV-001",
    "REF:docs/modelagem/schemas/schema_decisao.json",
    "REF:.ai/decisions/DEC-GOV-001-agent-flow-legado.md",
    "instrução direta de Davi Sermenho, 2026-08-15"
  ],
  "impacto": "schema_decisao.json permanece fiel ao texto literal da seção 5.2 do plano, sem extensão. A seção DEC-GOV-001 em decisoes/registro_decisoes.md vira referência em prosa para .ai/decisions/DEC-GOV-001-agent-flow-legado.md, sem bloco json — validar.mjs sobre o corpus real volta a reportar errors=0. Precedente para qualquer futura decisão de governança que apareça referenciada nesta pasta: registrar como referência, nunca como bloco schema_decisao.json.",
  "riscos": [],
  "aprovador": "Davi Sermenho",
  "estado": "RESOLVIDA",
  "evidencia": {
    "repository_evidence": { "action_ref": "AC-000" }
  }
}
```

## DEC-007 — Resultado de `AD-03` em `AC-001`

`AD-03` (seção 8 do plano): "cabeçalho de coluna de planilha tentando virar termo canônico só por
existir." Executado sobre os 11 `TERMO-NNN` registrados em `AC-001`
(`conhecimento/glossario.md`): cada um tem `evidencia.semantic_evidence` com justificativa real —
recorrência em múltiplas abas independentes, regra explícita de metadados/contrato citando o
conceito, ou consequência operacional documentada (correção humana registrada, proibição de
cálculo manual) — nunca apenas "existe uma coluna com esse nome". Nenhum termo nasceu só por nome
de coluna.

Registrado como decisão formal (não apenas nota de dossiê) para manter o mesmo padrão de
auditoria dos demais testes adversariais (`AD-01` → `DEC-004`, em `AC-002`). Segue o mesmo
mecanismo já usado em `DEC-011`: rascunho com `aprovador=PENDENTE`/`estado=BLOQUEADO`, porque é
uma verificação nova que ninguém revisou ainda — nunca autoaprovada pelo `EXECUTOR` (melhoria f).

```json
{
  "id_decisao": "DEC-007",
  "data": "2026-08-15",
  "decisao": "Resultado de AD-03 (seção 8 do plano) sobre os 11 termos registrados em AC-001 — nenhum termo deveria nascer apenas por existir uma coluna com esse nome, sem semantic_evidence real.",
  "alternativas": [],
  "escolha": "AD-03 passou: todos os 11 TERMO-NNN de AC-001 têm semantic_evidence com justificativa real (recorrência em múltiplas abas, regra de metadados/contrato citando o conceito, ou consequência operacional documentada), nenhum baseado só em nome de coluna. Nenhuma correção foi necessária.",
  "justificativa": "Verificação executada linha a linha contra os 11 registros em conhecimento/glossario.md; cada semantic_evidence cita evidência estrutural ou textual específica, não apenas a existência do cabeçalho.",
  "fonte": [
    "REF:docs/modelagem/conhecimento/glossario.md — TERMO-001 a TERMO-011",
    "REF:docs/modelagem/fontes/dossies/cepraea_agosto_2026.xlsx.md"
  ],
  "impacto": "Nenhuma ação corretiva necessária em AC-001. Precedente de verificação para os demais AD-NNN ainda pendentes (AD-01/AC-002, AD-02+AD-04/AC-008-010, AD-05/AC-028, AD-06/AC-029).",
  "riscos": [],
  "aprovador": "PENDENTE",
  "estado": "BLOQUEADO",
  "evidencia": {
    "repository_evidence": { "action_ref": "AC-001" }
  }
}
```
