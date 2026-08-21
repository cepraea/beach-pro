# Inventário do repositório (manifest)



Este documento mapeia a estrutura atual do projeto `CEPRAEA Beach pro`.

Este é o mapa **narrativo/humano**, no nível de cada arquivo individual. O
mapa **estruturado/máquina**, no nível dos ativos principais (pastas e
arquivos-chave), fica em [`manifest.json`](./manifest.json) — os dois se
complementam: quando um ativo existe nos dois arquivos, as colunas
`Tipo de Ativo`, `Propósito`, `Consumidor` e `Status` da tabela abaixo
apontam para `manifest.json` em vez de repetir o valor, para não haver duas
fontes divergentes do mesmo fato. `Resumo Executivo` e `Link` são exclusivos
deste arquivo.

## Mapa de arquivos

**Correção de proveniência (achado do Reviewer, 2026-08-18):** o comando
abaixo, executado literalmente sobre a raiz do repositório hoje, produz 330
entradas (`find . -type d -name ".git" -prune -o -print | wc -l`), das quais
186 pertencem a diretórios ocultos de infraestrutura (`.ai/`,
`.devcontainer/`, `.codex/`, `.drive/`, `.vscode/`) — não reproduz a árvore
de 136 linhas abaixo. A árvore foi filtrada manualmente para o "projeto
visível" (governança na raiz, `docs/`, `runbooks/`, `test/`); os diretórios
de infraestrutura ficam fora por decisão de escopo, não por efeito do
comando, e estão mapeados separadamente em
[`manifest.json`](./manifest.json). O comando que efetivamente reproduz o
conjunto de caminhos abaixo (verificado: 134 entradas brutas, compatível com
as 136 linhas após numeração e formatação manual dos comentários) é:

```bash
find AGENT_POLICY.md AGENTS.md CLAUDE.md README.md docs runbooks test -print \
  | sed -e 's;[^/]*/;├── ;g;s;├── |;│   ;g'
```
<!-- Árvore original gerada em 18/08/2026 às 08:00; comentários adicionados em seguida -->

```txt
├── AGENTS.md                 ← Papel operacional do Reviewer (Codex) — ver manifest.json
├── AGENT_POLICY.md           ← Política comum dos três agentes — ver manifest.json
├── CLAUDE.md                 ← Papel operacional do Executor (Claude Code) — ver manifest.json
├── README.md                 ← Apresentação do projeto, stack e setup — ver manifest.json
├── docs
|  ├── arquiteturas
|  |  ├── assurance          ← Estado atual/alvo do fluxo de assurance — ver manifest.json
|  |  |  ├── ESTADO-ARQUITETURA-FINAL.md      ← Estado-alvo pretendido (ainda não implantado)
|  |  |  ├── ESTADO-ATUAL-ARQUITETURA.md      ← Estado operacional vigente
|  |  |  ├── GUIA-0-IDENTIFICAÇÃO-BASELINE-ESCOPO.md ← Baseline/branch/escopo da implantação
|  |  |  ├── PLANO-COMPLETO-TASKS-ATÔMICAS.md ← Tasks da implantação, por fase, com gate
|  |  |  ├── REGISTRO-DECISÕES-HUMANAS.md     ← Decisões humanas confirmadas (HDEC-xxx)
|  |  |  └── RUNBOOK-IMPLEMENTAÇÃO.md         ← Runbook de execução das TASK-ARCH
|  |  ├── multi-agentes      ← Arquitetura do Dual-Agent SDLC e do dev container — ver manifest.json
|  |  |  ├── Arquivos-Human-Governed Dual-Agent SDLC Architecture.md ← Especifica os arquivos que materializam a arquitetura
|  |  |  ├── CONTAINER-RUNBOOK-v0.3.md        ← Fonte de verdade técnica do dev container
|  |  |  ├── Human-Governed Dual-Agent SDLC Architecture.md ← Documento arquitetural principal (arc42)
|  |  |  ├── Implantação-Human-Governed Dual-Agent SDLC Archite.md ← Checklist de validação real (CT-01..CT-17)
|  |  |  ├── Relatorio Multi-Agentes.md       ← Enforcement real vs. política escrita, lacunas
|  |  |  └── Runbooks.md                      ← Arquitetura da biblioteca de runbooks
|  |  └── task_atomics.md    ← Padrão de task atômica (contrato Task Proposal v2) — ver manifest.json
|  ├── modelagem
|  |  ├── PLANO_CEPRAEA_Modelo_Canonico_FINAL.md ← Documento canônico normativo — ver manifest.json
|  |  ├── README.md          ← Ponto de entrada operacional da modelagem — ver manifest.json
|  |  ├── candidatos         ← Hipóteses estruturais ainda não promovidas — ver manifest.json
|  |  |  ├── agregados.md              ← Stub — nenhum agregado candidato ainda
|  |  |  ├── bounded_contexts.md       ← 8 Bounded Contexts pré-semeados (CTX-001..008), hipótese
|  |  |  ├── ciclos_de_vida.md         ← Stub — vazio
|  |  |  ├── fronteiras_transacionais.md ← Stub — vazio
|  |  |  ├── identidades.md            ← Stub — vazio
|  |  |  └── invariantes.md            ← Invariantes candidatas, com evidência e ambiguidades
|  |  ├── conhecimento       ← Glossário e regras extraídas — ver manifest.json
|  |  |  ├── conflitos_semanticos.md   ← Stub — índice de conflitos a resolver em AC-029
|  |  |  ├── glossario.md              ← Glossário de termos, um bloco por TERMO-NNN
|  |  |  └── registro_regras.md        ← Regras extraídas, um bloco por REGRA-NNN
|  |  ├── decisoes
|  |  |  └── registro_decisoes.md      ← Registro formal de decisões (DEC-NNN) — ver manifest.json
|  |  ├── dominio            ← Modelo Canônico — elementos promovidos — ver manifest.json
|  |  |  ├── agregados.md              ← Stub — nenhum agregado promovido ainda
|  |  |  ├── bounded_contexts.md       ← Stub — nenhum BC promovido ainda
|  |  |  ├── ciclos_de_vida.md         ← Stub — vazio
|  |  |  ├── fronteiras_transacionais.md ← Stub — vazio
|  |  |  ├── identidades_definitivas.md ← Stub — vazio
|  |  |  ├── invariantes.md            ← INV-001 validado (rota PRE-SEED, aprovado por Davi)
|  |  |  └── modelo_canonico_dominio.md ← Estrutura do produto final; nenhuma seção CTX ainda
|  |  ├── evidencias
|  |  |  └── registro_evidencias.md    ← Fragmentos de evidência (EVD-NNNN) — ver manifest.json
|  |  ├── fontes             ← Inventário e dossiês das fontes — ver manifest.json
|  |  |  ├── dossies
|  |  |  |  ├── bancocepraea.docx.md        ← Dossiê SRC-002, substituída por DEC-002
|  |  |  |  ├── cepraea_agosto_2026.xlsx.md ← Dossiê SRC-001, planilha operacional, 45 abas
|  |  |  |  └── cepraea_db.docx.md          ← Dossiê SRC-003, framework de governança (não é schema físico)
|  |  |  └── inventario_fontes.md      ← Tabela mestra das 28 entradas de fontes privadas
|  |  ├── logico             ← Modelo lógico relacional — ver manifest.json
|  |  |  ├── areas_pendentes.md            ← Stub por design (até classificação de maturidade)
|  |  |  └── modelo_logico_relacional.md   ← Stub por design (até BC atingir maturidade suficiente)
|  |  ├── processo           ← Critérios de maturidade e taxonomias — ver manifest.json
|  |  |  ├── criterios_maturidade.md   ← Critérios de maturidade por Bounded Context
|  |  |  ├── fluxo_de_modelagem.md     ← Checklist de processo, estados permitidos
|  |  |  ├── perguntas_competencia.md  ← Perguntas de competência que orientam o modelo
|  |  |  └── taxonomias.md             ← Classificação de fontes e estados epistemológicos
|  |  └── schemas
|  |     ├── fixtures        ← ~37 instâncias de teste por schema (não confundir com o manifest.json da raiz — este é um manifesto interno da suíte de testes)
|  |     |  ├── decisao_invalida_resolvida_fonte_vazia.json
|  |     |  ├── decisao_invalida_resolvida_sem_action_ref.json
|  |     |  ├── decisao_invalida_resolvida_sem_aprovador.json
|  |     |  ├── decisao_valida_bloqueada.json
|  |     |  ├── decisao_valida_resolvida_com_action_ref.json
|  |     |  ├── elemento_invalido_bc_sem_maturidade.json
|  |     |  ├── elemento_invalido_dominio_sem_promocao.json
|  |     |  ├── elemento_invalido_dominio_sem_validacao.json
|  |     |  ├── elemento_invalido_preseed_sem_aprovacao.json
|  |     |  ├── elemento_invalido_preseed_sem_ref.json
|  |     |  ├── elemento_invalido_promocao_sem_candidato.json
|  |     |  ├── elemento_invalido_promovido_sem_destino.json
|  |     |  ├── elemento_invalido_promovido_sem_sem_ref.json
|  |     |  ├── elemento_invalido_validado_sem_aprovador.json
|  |     |  ├── elemento_valido_bc.json
|  |     |  ├── elemento_valido_preseed.json
|  |     |  ├── elemento_valido_promocao_sem.json
|  |     |  ├── evidencia_invalida_sensivel_sem_tratamento.json
|  |     |  ├── evidencia_valida.json
|  |     |  ├── fonte_invalida_action_ref_divergente_de_id_acao.json
|  |     |  ├── fonte_invalida_concluida_sem_action_ref.json
|  |     |  ├── fonte_invalida_concluida_sem_hash.json
|  |     |  ├── fonte_invalida_sem_evidencia.json
|  |     |  ├── fonte_invalida_sem_hash.json
|  |     |  ├── fonte_invalida_sensivel_sem_tratamento.json
|  |     |  ├── fonte_valida_bloqueada.json
|  |     |  ├── fonte_valida_bloqueada_ausente_sem_hash.json
|  |     |  ├── fonte_valida_concluida.json
|  |     |  ├── fonte_valida_concluida_com_action_ref.json
|  |     |  ├── manifest.json       ← Manifesto da suíte (schema→fixture→resultado esperado), local a schemas/
|  |     |  ├── regra_invalida_sem_sujeito_acao.json
|  |     |  ├── regra_invalida_validada_sem_aprovador.json
|  |     |  ├── regra_valida_observada.json
|  |     |  ├── termo_invalido_fonte_ac_bruto.json
|  |     |  ├── termo_invalido_modelado_sem_validacao.json
|  |     |  ├── termo_invalido_validado_sem_aprovador.json
|  |     |  └── termo_valido_observado.json
|  |     ├── schema_decisao.json          ← ver manifest.json
|  |     ├── schema_elemento_modelo.json  ← ver manifest.json
|  |     ├── schema_evidencia.json        ← ver manifest.json
|  |     ├── schema_fonte.json            ← ver manifest.json
|  |     ├── schema_regra.json            ← ver manifest.json
|  |     ├── schema_termo.json            ← ver manifest.json
|  |     ├── validar.mjs                  ← ver manifest.json
|  |     ├── verificar_referencias.mjs    ← ver manifest.json
|  |     └── verificar_repositorio.mjs    ← ver manifest.json
|  ├── operacao
|  |  └── agent-workflow.md   ← ver manifest.json
|  └── standards
|     └── guia_estilo_documentação.md        ← ver manifest.json
├── runbooks
|  ├── README.md                             ← ver manifest.json
|  ├── executor                              ← ver manifest.json
|  |  ├── RB-EXEC-001-code-change.md         ← Mudança de código
|  |  ├── RB-EXEC-002-database-change.md     ← Mudança de banco de dados
|  |  ├── RB-EXEC-003-documentation-change.md ← Mudança de documentação
|  |  └── RB-EXEC-004-dependency-change.md   ← Mudança de dependência
|  ├── reviewer                              ← ver manifest.json
|  |  ├── RB-REV-001-code-review.md          ← Revisão de mudança de código
|  |  ├── RB-REV-002-database-review.md      ← Revisão de mudança de banco de dados
|  |  ├── RB-REV-003-documentation-review.md ← Revisão de mudança de documentação
|  |  ├── RB-REV-004-evidence-review.md      ← Revisão de suficiência de evidência (complementar)
|  |  └── RB-REV-005-dependency-review.md    ← Revisão de mudança de dependência
|  └── shared                                ← ver manifest.json
|     ├── RB-SHARED-001-repository-baseline.md ← Baseline de repositório
|     ├── RB-SHARED-002-evidence.md            ← Padrão de evidência
|     └── RB-SHARED-003-failure-states.md      ← Vocabulário fechado de estados de falha
└── test
    └── fixtures
       └── synthetic
          └── agent-plan-smoke.txt             ← ver manifest.json
```

directory: 26 file: 111

## Dicionário dos arquivos

| Diretório / Arquivo | Tipo de Ativo | Propósito | Consumidor | Resumo Executivo | Link | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | ver manifest.json | ver manifest.json | ver manifest.json | Define o procedimento de revisão independente do Codex: runbooks, fonte do review, findings (CRITICAL/HIGH/MEDIUM/LOW), vereditos fechados (PASS/FAIL/HUMAN_DECISION_REQUIRED). | [AGENTS.md](./AGENTS.md) | ver manifest.json |
| `AGENT_POLICY.md` | ver manifest.json | ver manifest.json | ver manifest.json | Define papéis (Davi/Claude/Codex), classificação de risco (verde/amarelo/vermelho/vermelho crítico), escopo de Git permitido e a lista de control-plane read-only. | [AGENT_POLICY.md](./AGENT_POLICY.md) | ver manifest.json |
| `CLAUDE.md` | ver manifest.json | ver manifest.json | ver manifest.json | Define o fluxo do Executor: proposta proporcional antes de escrever, execução restrita ao escopo, validações antes do handoff. | [CLAUDE.md](./CLAUDE.md) | ver manifest.json |
| `README.md` | ver manifest.json | ver manifest.json | ver manifest.json | Apresentação do projeto CEPRAEA BEACH PRO (MVP sintético), stack técnica, instruções de setup/validação local. | [README.md](./README.md) | ver manifest.json |
| `docs/arquiteturas/assurance/` | ver manifest.json | ver manifest.json | ver manifest.json | Seis documentos que juntos descrevem o estado atual, o estado-alvo, o baseline/escopo, o plano de tasks, o registro de decisões humanas (HDEC-xxx) e o runbook de implantação da nova arquitetura de assurance. | [docs/arquiteturas/assurance/](./docs/arquiteturas/assurance/) | ver manifest.json |
| `docs/arquiteturas/assurance/ESTADO-ARQUITETURA-FINAL.md` | Documento de arquitetura | Descreve o fluxo-alvo (Task Contract, Verification Plan, Verifier formal) ainda não implantado. | agent, human | Serve como referência do "para onde" a implantação caminha — não confundir com o estado real hoje. | [ESTADO-ARQUITETURA-FINAL.md](./docs/arquiteturas/assurance/ESTADO-ARQUITETURA-FINAL.md) | Substantivo |
| `docs/arquiteturas/assurance/ESTADO-ATUAL-ARQUITETURA.md` | Documento de arquitetura | Descreve o fluxo operacional vigente (Executor → validações → Reviewer → Humano), sem a camada formal ainda. | agent, human | Baseline do "como é hoje", usado para medir o gap até o estado-alvo. | [ESTADO-ATUAL-ARQUITETURA.md](./docs/arquiteturas/assurance/ESTADO-ATUAL-ARQUITETURA.md) | Substantivo |
| `docs/arquiteturas/assurance/GUIA-0-IDENTIFICAÇÃO-BASELINE-ESCOPO.md` | Documento de processo | Fixa repositório, branch, baseline e fontes de autoridade para iniciar a implantação. | human | Ponto de partida procedural antes de qualquer TASK-ARCH ser executada. | [GUIA-0-IDENTIFICAÇÃO-BASELINE-ESCOPO.md](./docs/arquiteturas/assurance/GUIA-0-IDENTIFICAÇÃO-BASELINE-ESCOPO.md) | Substantivo |
| `docs/arquiteturas/assurance/PLANO-COMPLETO-TASKS-ATÔMICAS.md` | Plano de execução | Decompõe a implantação em tasks atômicas por fase, cada uma com owner, ação, saída e gate. | human, agent | Roadmap operacional da implantação da arquitetura de assurance. | [PLANO-COMPLETO-TASKS-ATÔMICAS.md](./docs/arquiteturas/assurance/PLANO-COMPLETO-TASKS-ATÔMICAS.md) | Substantivo |
| `docs/arquiteturas/assurance/REGISTRO-DECISÕES-HUMANAS.md` | Registro de decisão | Registra formalmente as decisões humanas confirmadas (HDEC-xxx) que governam a implantação. | human, agent | Fonte de verdade de decisões já fechadas — não deve ser reaberta sem novo HDEC. | [REGISTRO-DECISÕES-HUMANAS.md](./docs/arquiteturas/assurance/REGISTRO-DECISÕES-HUMANAS.md) | Substantivo |
| `docs/arquiteturas/assurance/RUNBOOK-IMPLEMENTAÇÃO.md` | Runbook | Runbook para executar as TASK-ARCH com blast radius controlado, fail-closed. | agent | Procedimento operacional passo a passo para quem executa a implantação. | [RUNBOOK-IMPLEMENTAÇÃO.md](./docs/arquiteturas/assurance/RUNBOOK-IMPLEMENTAÇÃO.md) | Substantivo |
| `docs/arquiteturas/multi-agentes/` | ver manifest.json | ver manifest.json | ver manifest.json | Seis documentos sobre a arquitetura Dual-Agent SDLC e o dev container — inclui inconsistências internas conhecidas entre alguns deles (ex.: topologia de container). | [docs/arquiteturas/multi-agentes/](./docs/arquiteturas/multi-agentes/) | ver manifest.json |
| `docs/arquiteturas/multi-agentes/Arquivos-Human-Governed Dual-Agent SDLC Architecture.md` | Documento de arquitetura | Especifica o conteúdo dos arquivos que materializam a arquitetura (ex.: `AGENT_POLICY.md`), separando governança de enforcement técnico. | agent, human | Explica por que cada arquivo de governança existe e o que deveria conter. | [Arquivos-Human-Governed Dual-Agent SDLC Architecture.md](<./docs/arquiteturas/multi-agentes/Arquivos-Human-Governed Dual-Agent SDLC Architecture.md>) | Substantivo |
| `docs/arquiteturas/multi-agentes/CONTAINER-RUNBOOK-v0.3.md` | Runbook técnico | Fonte de verdade sobre a arquitetura do dev container (Docker, mounts, permissões, estado comprovado vs. pendente). | agent, human | Documento mais extenso e técnico sobre o sandbox — usar como referência de detalhe de mounts/permissões. | [CONTAINER-RUNBOOK-v0.3.md](./docs/arquiteturas/multi-agentes/CONTAINER-RUNBOOK-v0.3.md) | Substantivo |
| `docs/arquiteturas/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md` | Documento de arquitetura | Documento arquitetural principal (arc42) do fluxo multiagente e do dev container, marcado "final para adoção". | agent, human | Documento de maior peso normativo do grupo — mas contém pontos já identificados como desatualizados frente ao runtime real. | [Human-Governed Dual-Agent SDLC Architecture.md](<./docs/arquiteturas/multi-agentes/main/Human-Governed Dual-Agent SDLC Architecture.md>) | Substantivo (conter drift conhecido) |
| `docs/arquiteturas/multi-agentes/Implantação-Human-Governed Dual-Agent SDLC Archite.md` | Checklist de validação | Checklist e plano prático de validação real da arquitetura (testes CT-01 a CT-17), gaps entre configurado e comprovado. | agent, human | Usado para verificar empiricamente o que a arquitetura promete vs. o que o container realmente faz. | [Implantação-Human-Governed Dual-Agent SDLC Archite.md](<./docs/arquiteturas/multi-agentes/Implantação-Human-Governed Dual-Agent SDLC Archite.md>) | Substantivo |
| `docs/arquiteturas/multi-agentes/Relatorio Multi-Agentes.md` | Relatório de verificação | Cruza enforcement técnico real (mounts, hooks, sandbox) com as políticas escritas, aponta lacunas (ex.: `.drive` sem readonly). | agent, human | Relatório de auditoria — ponto de partida para saber o que já foi verificado e o que ainda é lacuna conhecida. | [Relatorio Multi-Agentes.md](<./docs/arquiteturas/multi-agentes/Relatorio Multi-Agentes.md>) | Substantivo |
| `docs/arquiteturas/multi-agentes/Runbooks.md` | Documento de arquitetura | Define a arquitetura da biblioteca de runbooks (runbook humano + biblioteca especializada por papel). | agent, human | Explica a lógica por trás da estrutura `runbooks/shared|executor|reviewer/` hoje em vigor. | [Runbooks.md](./docs/arquiteturas/multi-agentes/Runbooks.md) | Substantivo |
| `docs/arquiteturas/task_atomics.md` | ver manifest.json | ver manifest.json | ver manifest.json | Padrão de task atômica (`task_proposal`), ciclo de duas portas de revisão (plano e implementação), oráculo de aceitação. | [docs/arquiteturas/task_atomics.md](./docs/arquiteturas/multi-agentes/executor/task_atomics.md) | ver manifest.json |
| `docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` | ver manifest.json | ver manifest.json | ver manifest.json | Especificação normativa completa da fase de modelagem: decisões fechadas (D-01/02/03), os 6 schemas formais, ordem das 28 fontes, critérios GATE A–E. | [docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md](./docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md) | ver manifest.json |
| `docs/modelagem/README.md` | ver manifest.json | ver manifest.json | ver manifest.json | Registra variáveis de `AC-000` (branch, SHAs, `CEPRAEA_SOURCE_ROOT`), escopos de escrita/leitura, comandos de validação. | [docs/modelagem/README.md](./docs/modelagem/README.md) | ver manifest.json |
| `docs/modelagem/candidatos/` | ver manifest.json | ver manifest.json | ver manifest.json | Seis arquivos de hipótese, um por tipo de elemento — só `bounded_contexts.md` e `invariantes.md` têm conteúdo real hoje, os outros quatro são stubs. | [docs/modelagem/candidatos/](./docs/modelagem/candidatos/) | ver manifest.json |
| `docs/modelagem/candidatos/agregados.md` | Elemento candidato | Hipóteses candidatas de AGREGADO. | agent | Vazio — nenhum agregado candidato registrado ainda. | [agregados.md](./docs/modelagem/candidatos/agregados.md) | Stub |
| `docs/modelagem/candidatos/bounded_contexts.md` | Elemento candidato | Oito Bounded Contexts pré-semeados (CTX-001–008) a partir de `modelagem_dominio_dados.md` §10.3. | agent, human | Único arquivo de `candidatos/` com conteúdo extenso hoje (219 linhas) — hipóteses ainda `INFERIDO`, não promovidas. | [bounded_contexts.md](./docs/modelagem/candidatos/bounded_contexts.md) | Substantivo |
| `docs/modelagem/candidatos/ciclos_de_vida.md` | Elemento candidato | Hipóteses candidatas de CICLO_DE_VIDA. | agent | Vazio — nenhum registrado ainda. | [ciclos_de_vida.md](./docs/modelagem/candidatos/ciclos_de_vida.md) | Stub |
| `docs/modelagem/candidatos/fronteiras_transacionais.md` | Elemento candidato | Hipóteses candidatas de FRONTEIRA_TRANSACIONAL. | agent | Vazio — nenhuma registrada ainda. | [fronteiras_transacionais.md](./docs/modelagem/candidatos/fronteiras_transacionais.md) | Stub |
| `docs/modelagem/candidatos/identidades.md` | Elemento candidato | Hipóteses candidatas de IDENTIDADE. | agent | Vazio — nenhuma registrada ainda. | [identidades.md](./docs/modelagem/candidatos/identidades.md) | Stub |
| `docs/modelagem/candidatos/invariantes.md` | Elemento candidato | Hipóteses candidatas de INVARIANTE (ex.: `INV-002`, `INV-003`). | agent, human | Documento com conteúdo real (184 linhas), incluindo evidência e ambiguidades documentadas. | [invariantes.md](./docs/modelagem/candidatos/invariantes.md) | Substantivo |
| `docs/modelagem/conhecimento/` | ver manifest.json | ver manifest.json | ver manifest.json | Glossário e regras extraídas — o índice de conflitos é o único stub do grupo. | [docs/modelagem/conhecimento/](./docs/modelagem/conhecimento/) | ver manifest.json |
| `docs/modelagem/conhecimento/conflitos_semanticos.md` | Índice de trabalho | Termos/regras/elementos em estado `AMBIGUO`/`CONFLITANTE`, a percorrer em `AC-029`. | agent | Vazio hoje — "nenhum conflito registrado ainda". | [conflitos_semanticos.md](./docs/modelagem/conhecimento/conflitos_semanticos.md) | Stub |
| `docs/modelagem/conhecimento/glossario.md` | Glossário | Um bloco JSON por `TERMO-NNN` (`schema_termo.json`) — só significado, não modelo conceitual. | agent, human | Documento substantivo (460 linhas). | [glossario.md](./docs/modelagem/conhecimento/glossario.md) | Substantivo |
| `docs/modelagem/conhecimento/registro_regras.md` | Registro de regras | Um bloco JSON por `REGRA-NNN` (`schema_regra.json`), rastreável a `EVD-NNNN`. | agent, human | Documento substantivo (287 linhas). | [registro_regras.md](./docs/modelagem/conhecimento/registro_regras.md) | Substantivo |
| `docs/modelagem/decisoes/registro_decisoes.md` | ver manifest.json | ver manifest.json | ver manifest.json | Decisões `DEC-001`–`DEC-011`+, resumo em prosa + bloco JSON verificável (`schema_decisao.json`). | [docs/modelagem/decisoes/registro_decisoes.md](./docs/modelagem/decisoes/registro_decisoes.md) | ver manifest.json |
| `docs/modelagem/dominio/` | ver manifest.json | ver manifest.json | ver manifest.json | Seis dos sete arquivos são stub; `invariantes.md` já tem `INV-001` validado; `modelo_canonico_dominio.md` é "o produto principal da fase" mas ainda não tem nenhuma seção `CTX-NNN`. | [docs/modelagem/dominio/](./docs/modelagem/dominio/) | ver manifest.json |
| `docs/modelagem/dominio/agregados.md` | Elemento do domínio | AGREGADOs promovidos ao Modelo Canônico. | agent | Vazio — nenhum promovido ainda. | [agregados.md](./docs/modelagem/dominio/agregados.md) | Stub |
| `docs/modelagem/dominio/bounded_contexts.md` | Elemento do domínio | Bounded Contexts promovidos. | agent | Vazio — os CTX-001–008 seguem só como candidatos. | [bounded_contexts.md](./docs/modelagem/dominio/bounded_contexts.md) | Stub |
| `docs/modelagem/dominio/ciclos_de_vida.md` | Elemento do domínio | CICLOS_DE_VIDA promovidos. | agent | Vazio — nenhum promovido ainda. | [ciclos_de_vida.md](./docs/modelagem/dominio/ciclos_de_vida.md) | Stub |
| `docs/modelagem/dominio/fronteiras_transacionais.md` | Elemento do domínio | FRONTEIRAS_TRANSACIONAIS promovidas. | agent | Vazio — nenhuma promovida ainda. | [fronteiras_transacionais.md](./docs/modelagem/dominio/fronteiras_transacionais.md) | Stub |
| `docs/modelagem/dominio/identidades_definitivas.md` | Elemento do domínio | IDENTIDADEs promovidas. | agent | Vazio — nenhuma promovida ainda. | [identidades_definitivas.md](./docs/modelagem/dominio/identidades_definitivas.md) | Stub |
| `docs/modelagem/dominio/invariantes.md` | Elemento do domínio | Invariantes promovidas — contém `INV-001` ("Papel operacional único por usuário"). | agent, human | Único arquivo de `dominio/` com um elemento real (50 linhas); `VALIDADO` por Davi Sermenho em `AC-000`, rota PRE-SEED. | [invariantes.md](./docs/modelagem/dominio/invariantes.md) | Substantivo (1 elemento) |
| `docs/modelagem/dominio/modelo_canonico_dominio.md` | Documento síntese | Reúne por referência os elementos de `dominio/*.md` por Bounded Context. | agent, human | Descrito como "o produto intelectual principal da fase", mas hoje só define a estrutura futura — consolidação real só em `AC-029`. | [modelo_canonico_dominio.md](./docs/modelagem/dominio/modelo_canonico_dominio.md) | Stub (estrutura futura) |
| `docs/modelagem/evidencias/registro_evidencias.md` | ver manifest.json | ver manifest.json | ver manifest.json | Elo rastreável entre fonte e conceito/regra, com localização literal (aba/coluna/linha, página/parágrafo). | [docs/modelagem/evidencias/registro_evidencias.md](./docs/modelagem/evidencias/registro_evidencias.md) | ver manifest.json |
| `docs/modelagem/fontes/` | ver manifest.json | ver manifest.json | ver manifest.json | Tabela mestra + três dossiês individuais das fontes já processadas (`SRC-001`, `SRC-002`, `SRC-003`). | [docs/modelagem/fontes/](./docs/modelagem/fontes/) | ver manifest.json |
| `docs/modelagem/fontes/dossies/bancocepraea.docx.md` | Dossiê de fonte | Dossiê `SRC-002` de `BancoCEPRAEA.docx` — 23 tabelas físicas propostas, migrations, RLS, RPCs. | agent, human | Classificado `TÉCNICA·AUXILIAR·ORIGINAL`/`SUBSTITUÍDA` por `DEC-002` — não é a fonte final. | [bancocepraea.docx.md](./docs/modelagem/fontes/dossies/bancocepraea.docx.md) | Substantivo |
| `docs/modelagem/fontes/dossies/cepraea_agosto_2026.xlsx.md` | Dossiê de fonte | Dossiê `SRC-001` de `CEPRAEA AGOSTO 2026.xlsx` — 45 abas (4 visíveis, 41 ocultas). | agent, human | Fonte operacional primária (disponibilidade, presença, jogos, feedback). | [cepraea_agosto_2026.xlsx.md](./docs/modelagem/fontes/dossies/cepraea_agosto_2026.xlsx.md) | Substantivo |
| `docs/modelagem/fontes/dossies/cepraea_db.docx.md` | Dossiê de fonte | Dossiê `SRC-003` de `CEPRAEA-DB.docx`. | agent, human | Apesar do nome, não é um schema físico — é o framework de governança/método ("PLANO MESTRE") de uma tentativa de modelagem anterior, sem nenhum `CREATE TABLE`. | [cepraea_db.docx.md](./docs/modelagem/fontes/dossies/cepraea_db.docx.md) | Substantivo |
| `docs/modelagem/fontes/inventario_fontes.md` | Inventário mestre | Tabela das 28 entradas de `.drive/CEPRAEA BEACH PRO/` (27 arquivos + 1 registro de bloqueio). | agent | Espelha o `estado_processamento` dos dossiês individuais. | [inventario_fontes.md](./docs/modelagem/fontes/inventario_fontes.md) | Substantivo |
| `docs/modelagem/logico/` | ver manifest.json | ver manifest.json | ver manifest.json | Ambos os arquivos vazios por design — modelo lógico só é derivado após um Bounded Context atingir maturidade suficiente. | [docs/modelagem/logico/](./docs/modelagem/logico/) | ver manifest.json |
| `docs/modelagem/logico/areas_pendentes.md` | Modelo lógico | Bounded Contexts que permanecem `IMATURA`/`PARCIALMENTE_MADURA` ao final da fase. | agent | Vazio até `AC-029` classificar maturidade — vazio por design, não descuido. | [areas_pendentes.md](./docs/modelagem/logico/areas_pendentes.md) | Stub (por design) |
| `docs/modelagem/logico/modelo_logico_relacional.md` | Modelo lógico | Entidades/tabelas/relações de Bounded Contexts `MADURA_PARA_MODELO_LOGICO`. | agent | Nenhuma migration/schema físico é gerado aqui ainda — vazio por design. | [modelo_logico_relacional.md](./docs/modelagem/logico/modelo_logico_relacional.md) | Stub (por design) |
| `docs/modelagem/processo/` | ver manifest.json | ver manifest.json | ver manifest.json | Quatro documentos de processo: critérios de maturidade, fluxo, perguntas de competência, taxonomias. | [docs/modelagem/processo/](./docs/modelagem/processo/) | ver manifest.json |
| `docs/modelagem/processo/criterios_maturidade.md` | Documento de processo | Critérios de maturidade por Bounded Context (`IMATURA`/`PARCIALMENTE_MADURA`/`MADURA_PARA_MODELO_LOGICO`). | agent | Extraído da seção 4.4 do plano canônico. | [criterios_maturidade.md](./docs/modelagem/processo/criterios_maturidade.md) | Substantivo |
| `docs/modelagem/processo/fluxo_de_modelagem.md` | Documento de processo | Checklist de processo, estados permitidos, regra de progressão, critério de conclusão de ação. | agent | Adaptado do "Guia 1" (`.drive/BEACH HANDBALL/`). | [fluxo_de_modelagem.md](./docs/modelagem/processo/fluxo_de_modelagem.md) | Substantivo |
| `docs/modelagem/processo/perguntas_competencia.md` | Documento de processo | Perguntas de competência que orientam o modelo e evitam entidades sem finalidade. | agent | União do checklist original com `modelagem_dominio_dados.md` §22. | [perguntas_competencia.md](./docs/modelagem/processo/perguntas_competencia.md) | Substantivo |
| `docs/modelagem/processo/taxonomias.md` | Documento de processo | Taxonomias de classificação de fontes, estados epistemológicos/técnicos. | agent | Explica o significado dos enums que os schemas realmente aplicam. | [taxonomias.md](./docs/modelagem/processo/taxonomias.md) | Substantivo |
| `docs/modelagem/schemas/fixtures/` | Suíte de testes | ~37 instâncias de teste (válidas/inválidas) por schema, dirigidas por um `manifest.json` interno a esta pasta. | agent, ci-cd | **Não confundir** com o `manifest.json` da raiz do repositório — mesmo nome, propósitos completamente diferentes (este é local à suíte de fixtures de `validar.mjs`). | [docs/modelagem/schemas/fixtures/](./docs/modelagem/schemas/fixtures/) | Substantivo |
| `docs/modelagem/schemas/schema_decisao.json` | ver manifest.json | ver manifest.json | ver manifest.json | Exige `id_decisao`, `data`, `decisao`, `escolha`, `justificativa`, `fonte`, `aprovador`; se `estado=RESOLVIDA`, exige aprovador `"Davi Sermenho"`. | [schema_decisao.json](./docs/modelagem/schemas/schema_decisao.json) | ver manifest.json |
| `docs/modelagem/schemas/schema_elemento_modelo.json` | ver manifest.json | ver manifest.json | ver manifest.json | Valida BC/Identidade/Agregado/Invariante/Ciclo de vida/Fronteira transacional e as rotas de promoção `candidatos/`↔`dominio/`. | [schema_elemento_modelo.json](./docs/modelagem/schemas/schema_elemento_modelo.json) | ver manifest.json |
| `docs/modelagem/schemas/schema_evidencia.json` | ver manifest.json | ver manifest.json | ver manifest.json | Exige localização literal específica e `tratamento_dado_sensivel` quando aplicável. | [schema_evidencia.json](./docs/modelagem/schemas/schema_evidencia.json) | ver manifest.json |
| `docs/modelagem/schemas/schema_fonte.json` | ver manifest.json | ver manifest.json | ver manifest.json | Exige hash SHA-256 e `action_ref` correspondente quando `estado_processamento=CONCLUIDO`. | [schema_fonte.json](./docs/modelagem/schemas/schema_fonte.json) | ver manifest.json |
| `docs/modelagem/schemas/schema_regra.json` | ver manifest.json | ver manifest.json | ver manifest.json | 13 valores de `tipo` (DEFINICAO/OBRIGACAO/PROIBICAO/...). | [schema_regra.json](./docs/modelagem/schemas/schema_regra.json) | ver manifest.json |
| `docs/modelagem/schemas/schema_termo.json` | ver manifest.json | ver manifest.json | ver manifest.json | 13 valores de `classificacao` (ENTIDADE/ATRIBUTO/VALOR_OBJETO/PAPEL/...). | [schema_termo.json](./docs/modelagem/schemas/schema_termo.json) | ver manifest.json |
| `docs/modelagem/schemas/validar.mjs` | ver manifest.json | ver manifest.json | ver manifest.json | Sem dependência externa; roda sobre o corpus real ou sobre `fixtures/manifest.json` como suíte de regressão. | [validar.mjs](./docs/modelagem/schemas/validar.mjs) | ver manifest.json |
| `docs/modelagem/schemas/verificar_referencias.mjs` | ver manifest.json | ver manifest.json | ver manifest.json | Saída `orfaos=N`, exit 1 se `N>0`. | [verificar_referencias.mjs](./docs/modelagem/schemas/verificar_referencias.mjs) | ver manifest.json |
| `docs/modelagem/schemas/verificar_repositorio.mjs` | ver manifest.json | ver manifest.json | ver manifest.json | Só usa subcomandos Git de leitura, nunca `merge-base`. | [verificar_repositorio.mjs](./docs/modelagem/schemas/verificar_repositorio.mjs) | ver manifest.json |
| `docs/operacao/agent-workflow.md` | ver manifest.json | ver manifest.json | ver manifest.json | Runbook do operador humano (Davi) para o ciclo de uma ACTION, do disparo ao Git privilegiado. | [docs/operacao/agent-workflow.md](./docs/operacao/agent-workflow.md) | ver manifest.json |
| `docs/standards/guia_estilo_documentação.md` | ver manifest.json | ver manifest.json | ver manifest.json | Guia canônico de autoria/edição/validação de Markdown, aplicável a humanos, Codex e Claude Code. | [docs/standards/guia_estilo_documentação.md](./docs/standards/guia_estilo_documentação.md) | ver manifest.json |
| `runbooks/README.md` | ver manifest.json | ver manifest.json | ver manifest.json | Matriz de seleção `operation_class` → runbooks aplicáveis (Executor/Reviewer); catálogo normativo. | [runbooks/README.md](./runbooks/README.md) | ver manifest.json |
| `runbooks/executor/` | ver manifest.json | ver manifest.json | ver manifest.json | Quatro runbooks, um por classe de operação (code/database/documentation/dependency). | [runbooks/executor/](./runbooks/executor/) | ver manifest.json |
| `runbooks/executor/RB-EXEC-001-code-change.md` | Runbook (Executor) | Procedimento para mudança de código. | agent:executor | — | [RB-EXEC-001-code-change.md](./runbooks/executor/RB-EXEC-001-code-change.md) | Substantivo |
| `runbooks/executor/RB-EXEC-002-database-change.md` | Runbook (Executor) | Procedimento para mudança de banco de dados. | agent:executor | — | [RB-EXEC-002-database-change.md](./runbooks/executor/RB-EXEC-002-database-change.md) | Substantivo |
| `runbooks/executor/RB-EXEC-003-documentation-change.md` | Runbook (Executor) | Procedimento para mudança de documentação. | agent:executor | — | [RB-EXEC-003-documentation-change.md](./runbooks/executor/RB-EXEC-003-documentation-change.md) | Substantivo |
| `runbooks/executor/RB-EXEC-004-dependency-change.md` | Runbook (Executor) | Procedimento para mudança de dependência. | agent:executor | — | [RB-EXEC-004-dependency-change.md](./runbooks/executor/RB-EXEC-004-dependency-change.md) | Substantivo |
| `runbooks/reviewer/` | ver manifest.json | ver manifest.json | ver manifest.json | Cinco runbooks: quatro espelham os do Executor, mais um de revisão de evidência (`RB-REV-004`, complementar). | [runbooks/reviewer/](./runbooks/reviewer/) | ver manifest.json |
| `runbooks/reviewer/RB-REV-001-code-review.md` | Runbook (Reviewer) | Revisão de mudança de código. | agent:reviewer | — | [RB-REV-001-code-review.md](./runbooks/reviewer/RB-REV-001-code-review.md) | Substantivo |
| `runbooks/reviewer/RB-REV-002-database-review.md` | Runbook (Reviewer) | Revisão de mudança de banco de dados. | agent:reviewer | — | [RB-REV-002-database-review.md](./runbooks/reviewer/RB-REV-002-database-review.md) | Substantivo |
| `runbooks/reviewer/RB-REV-003-documentation-review.md` | Runbook (Reviewer) | Revisão de mudança de documentação. | agent:reviewer | — | [RB-REV-003-documentation-review.md](./runbooks/reviewer/RB-REV-003-documentation-review.md) | Substantivo |
| `runbooks/reviewer/RB-REV-004-evidence-review.md` | Runbook (Reviewer) | Revisão de suficiência de evidência — carregado adicionalmente quando a evidência é material para o critério de aceite. | agent:reviewer | Único runbook "complementar" da matriz — não é selecionado por `operation_class`, e sim por condição. | [RB-REV-004-evidence-review.md](./runbooks/reviewer/RB-REV-004-evidence-review.md) | Substantivo |
| `runbooks/reviewer/RB-REV-005-dependency-review.md` | Runbook (Reviewer) | Revisão de mudança de dependência. | agent:reviewer | — | [RB-REV-005-dependency-review.md](./runbooks/reviewer/RB-REV-005-dependency-review.md) | Substantivo |
| `runbooks/shared/` | ver manifest.json | ver manifest.json | ver manifest.json | Três runbooks comuns aos dois papéis: baseline, evidência, estados de falha. | [runbooks/shared/](./runbooks/shared/) | ver manifest.json |
| `runbooks/shared/RB-SHARED-001-repository-baseline.md` | Runbook (Shared) | Baseline de repositório. | agent | — | [RB-SHARED-001-repository-baseline.md](./runbooks/shared/RB-SHARED-001-repository-baseline.md) | Substantivo |
| `runbooks/shared/RB-SHARED-002-evidence.md` | Runbook (Shared) | Padrão de evidência exigido em handoffs. | agent | — | [RB-SHARED-002-evidence.md](./runbooks/shared/RB-SHARED-002-evidence.md) | Substantivo |
| `runbooks/shared/RB-SHARED-003-failure-states.md` | Runbook (Shared) | Vocabulário fechado de estados de falha (`READY_FOR_REVIEW`/`BLOCKED`; `PASS`/`FAIL`/`HUMAN_DECISION_REQUIRED`). | agent | Vocabulário reaproveitado por `task_atomics.md` para as duas portas de revisão. | [RB-SHARED-003-failure-states.md](./runbooks/shared/RB-SHARED-003-failure-states.md) | Substantivo |
| `test/fixtures/synthetic/agent-plan-smoke.txt` | ver manifest.json | ver manifest.json | ver manifest.json | Fixture canário de smoke test (`CEPRAEA_AGENT_PLAN_SMOKE=PASS`). | [test/fixtures/synthetic/agent-plan-smoke.txt](./test/fixtures/synthetic/agent-plan-smoke.txt) | ver manifest.json |

## Contexto dos arquivos e diretórios principais

### Raiz — governança

`AGENT_POLICY.md`, `CLAUDE.md` e `AGENTS.md` formam o núcleo normativo dos
três agentes (política comum, papel do Executor, papel do Reviewer — ver
`manifest.json` para o detalhe estruturado de cada um). `README.md`
apresenta o projeto para humanos. Este par (`manifest.md` +
`manifest.json`) é o mapa de contexto que complementa esses três, sem
repetir seu conteúdo.

### docs/arquiteturas/

Documentação de arquitetura em dois eixos: `assurance/` descreve o estado
atual e o estado-alvo do próprio fluxo de garantia (Executor/Reviewer/
Humano) e como chegar de um ao outro; `multi-agentes/` descreve a
arquitetura do Dual-Agent SDLC e do dev container que a sustenta — com
inconsistências internas já conhecidas entre alguns desses documentos
(nenhum deles deve ser lido isoladamente como autoridade única; o
`ESTADO-ATUAL-ARQUITETURA.md` e o `CONTAINER-RUNBOOK-v0.3.md` são os mais
próximos do runtime real). `task_atomics.md`, na raiz de `arquiteturas/`,
é o contrato que qualquer nova tarefa de produto/engenharia precisa seguir.

### docs/modelagem/

Contém toda a modelagem canônica do domínio. Importante para qualquer
agente: a maturidade é **muito heterogênea** — `PLANO_CEPRAEA_Modelo_
Canonico_FINAL.md`, `conhecimento/`, `evidencias/`, `decisoes/` e
`fontes/` têm conteúdo real e substantivo; já a maior parte de `dominio/`
(seis dos sete arquivos) e todo `logico/` são **stubs vazios por design**
— não por descuido — porque a promoção de candidato a domínio, e de
domínio a modelo lógico, só ocorre quando critérios de maturidade
explícitos (`processo/criterios_maturidade.md`) são satisfeitos. Um agente
que encontrar esses arquivos vazios não deve tratá-los como lacuna a
preencher por conta própria.

### runbooks/

Armazena os guias operacionais e fluxos de execução/revisão, divididos por
papel (`executor/`, `reviewer/`) mais os comuns aos dois (`shared/`).
`runbooks/README.md` é o catálogo normativo — a seleção do runbook
aplicável a uma tarefa deve sempre ser verificada ali por evidência
(lendo o arquivo), nunca por inferência.

### test/

Contém arquivos sintéticos e fixtures para validação do sistema — hoje
apenas um fixture canário de smoke test, sem suíte de testes real ainda.

### Infraestrutura / control-plane (fora da árvore acima)

`.ai/`, `.devcontainer/` e `.codex/` não aparecem na árvore acima porque
este documento mapeia o "projeto visível" (a mesma árvore gerada por
`find` sobre `docs/`, `runbooks/`, `test/` e a governança na raiz). Esses
diretórios de infraestrutura/control-plane existem, são reais e têm papel
crítico (contrato Task Proposal v2, decisões de arquitetura de container,
sandbox do Executor e do Reviewer) — estão mapeados em `manifest.json`,
que tem escopo mais amplo que este arquivo. `.drive/**` fica de fora dos
dois mapas: contém fontes privadas protegidas e material de referência não
autoritativo por padrão (`AGENT_POLICY.md`).
