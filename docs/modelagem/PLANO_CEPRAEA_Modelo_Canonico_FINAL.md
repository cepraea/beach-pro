# Plano: descoberta orientada por evidências e construção do Modelo Canônico do CEPRAEA-BEACH-PRO

- [Plano: descoberta orientada por evidências e construção do Modelo Canônico do CEPRAEA-BEACH-PRO](#plano-descoberta-orientada-por-evidências-e-construção-do-modelo-canônico-do-cepraea-beach-pro)
  - [Identidade e objetivo do plano](#identidade-e-objetivo-do-plano)
  - [0. Decisões e fatos já fechados (registrados para não haver regressão)](#0-decisões-e-fatos-já-fechados-registrados-para-não-haver-regressão)
    - [D-03 em detalhe, com citação exata e localização](#d-03-em-detalhe-com-citação-exata-e-localização)
  - [1. Contexto](#1-contexto)
  - [2. Resultado esperado desta fase](#2-resultado-esperado-desta-fase)
  - [3. Escopo](#3-escopo)
  - [4. Metodologia: checklist existente + melhorias (decisão fixada, não uma pergunta)](#4-metodologia-checklist-existente--melhorias-decisão-fixada-não-uma-pergunta)
    - [4.11 Invariantes executáveis do próprio processo](#411-invariantes-executáveis-do-próprio-processo)
  - [5. Schemas formais](#5-schemas-formais)
    - [5.1 `docs/modelagem/schemas/schema_fonte.json`](#51-docsmodelagemschemasschema_fontejson)
    - [5.2 `docs/modelagem/schemas/schema_decisao.json`](#52-docsmodelagemschemasschema_decisaojson)
    - [5.3 Validação mecânica dos schemas e das referências](#53-validação-mecânica-dos-schemas-e-das-referências)
    - [5.4 Por que validação estrutural não basta — testes de instância dos schemas](#54-por-que-validação-estrutural-não-basta--testes-de-instância-dos-schemas)
  - [6. Estrutura de arquivos (escolhas fixadas, não perguntas)](#6-estrutura-de-arquivos-escolhas-fixadas-não-perguntas)
  - [7. Definição formal de ação — usada para todas as 28 entradas de fonte](#7-definição-formal-de-ação--usada-para-todas-as-28-entradas-de-fonte)
  - [8. Casos adversariais](#8-casos-adversariais)
  - [9. Catálogo de edge cases](#9-catálogo-de-edge-cases)
  - [10. Ordem de execução](#10-ordem-de-execução)
    - [10.0 Sequência de IDs (ordem única, estritamente sequencial)](#100-sequência-de-ids-ordem-única-estritamente-sequencial)
    - [10.1 Critério de DONE do `AC-000` (bootstrap)](#101-critério-de-done-do-ac-000-bootstrap)
  - [11. Critério de pronto desta fase](#11-critério-de-pronto-desta-fase)
  - [12. Classificação de risco e papéis de arquivo (AGENT\_POLICY.md)](#12-classificação-de-risco-e-papéis-de-arquivo-agent_policymd)
  - [13. Verificação](#13-verificação)
  - [14. Decisões que ainda dependem de você](#14-decisões-que-ainda-dependem-de-você)

**ESTE PLANO SEGUE A POLÍTICA DO AGENTES SENDO OS COMMITS E PUSHS REALIZADOS POR DAVI SERMENHO**

## Identidade e objetivo do plano

**ID do plano:** `PLANO-CEPRAEA-MODELO-CANONICO-002`

**Versão:** final ajustada após patch de arquitetura, rastreabilidade, worktree, maturidade e
executabilidade; revisada por `DEC-008` (`decisoes/registro_decisoes.md`) — a worktree irmã da
seção 4.7 original foi removida e substituída por execução direta na branch dedicada
`feat/cepraea-domain-modeling`, com isolamento por `WRITE_SCOPE` explícito.

**Objetivo:** descobrir e formalizar o **Modelo Canônico do Domínio CEPRAEA-BEACH-PRO** —
`dominio/modelo_canonico_dominio.md` — a partir das evidências do acervo em
`.drive/CEPRAEA BEACH PRO/`, de forma verificável e rastreável até o fragmento exato da fonte que
sustenta cada afirmação (`EVD-NNNN`, seção 4.5) — sem inferência não sustentada e sem transcrever
dado sensível. Em uma frase: **produzindo evidências estruturadas e conhecimento reconciliado
para construção do Modelo Canônico do Domínio CEPRAEA-BEACH-PRO e, somente para suas áreas
semanticamente maduras, derivação posterior do modelo lógico relacional.** O Modelo Canônico é o
produto intelectual principal desta fase; inventário, glossário, os seis objetos obrigatórios
(seção 4.1) e o modelo lógico são insumos e derivações dele, não substitutos. O modelo lógico só
é derivado para as áreas que atingirem maturidade suficiente (seção 4.4); nenhuma migration ou
schema físico Supabase é gerado nesta fase, e esta fase não repete os erros que levaram a
tentativa anterior de modelagem a ser considerada falha (D-02).

O processamento das fontes constitui o mecanismo de aquisição de evidências desta fase, não o produto intelectual final. O produto intelectual principal é o **Modelo Canônico do Domínio**.

**Estado atual — antes deste plano executar:**

- 27 arquivos reais em `.drive/CEPRAEA BEACH PRO/`, mais 1 arquivo referenciado por eles porém
  ausente do disco (ver D-01); nenhum tem registro estruturado de conteúdo.
- `docs/modelagem/` não existe neste repositório.
- Uma tentativa anterior de modelagem existe (REGISTRO MESTRE, Glossário v0.1, BancoCEPRAEA.docx,
  CEPRAEA-DB.docx) e foi declarada falha por você (D-02): dois schemas físicos incompatíveis
  ficaram sem resolução, e uma alegação de governança ("STOP GATE fechado") não está totalmente
  esclarecida (D-03).
- Nenhum schema formal (`schema_fonte.json`/`schema_decisao.json`) existe ainda; nenhum mecanismo
  de evidência obrigatória está em vigor.
- Branch de trabalho ainda não criada — repositório na branch `chore/agent-safe-devcontainer`
  (não `main`), que trata de outro assunto (controles do devcontainer).

**Estado desejado — ao final desta fase:**

- Todo arquivo de `.drive/CEPRAEA BEACH PRO/` tem estado conhecido e rastreável — `CONCLUIDO`,
  `BLOQUEADO` ou `NAO_APLICAVEL`, nunca "não olhado" — cada um com evidência verificável
  (seção 7) e validado contra `schema_fonte.json`.
- Existe um `dominio/modelo_canonico_dominio.md` cobrindo os conceitos, identidades, Bounded Contexts,
  agregados, invariantes, ciclos de vida e fronteiras transacionais sustentados pelas fontes
  relevantes segundo tipo, autoridade, proveniência e vigência, sem depender dos schemas da tentativa anterior; um glossário separado
  (o que os termos significam); e um modelo lógico relacional **apenas para as áreas que
  atingirem maturidade `MADURA_PARA_MODELO_LOGICO`** (seção 4.4) — cobertura parcial é o
  resultado esperado, não uma falha.
- As contradições conhecidas (D-03) e os dois schemas físicos conflitantes seguem registrados e
  visíveis em `decisoes/registro_decisoes.md` — não escondidos nem resolvidos por suposição.
- Nenhuma decisão de schema físico Supabase foi tomada — isso pertence a uma fase seguinte, fora
  deste plano.
- Lista completa de artefatos entregues: seção 2.

## 0. Decisões e fatos já fechados (registrados para não haver regressão)

| ID | Fato/decisão | Estado |
|---|---|---|
| D-01 | `CEPRAEA — Wellness — Apps Script Mobile.txt` foi apagado acidentalmente por Davi durante esta sessão e já foi restaurado por ele. Confirmado: **presente**. A cópia `Cópia de CEPRAEA — Wellness — Apps Script Mobile.txt` continua **ausente**; Davi decidiu que ela não é necessária, já que o original supre a fonte (`AC-020`). | Resolvido — ver `AC-020`/`AC-021` |
| D-02 | O fluxo de modelagem anterior falhou (decisão de Davi). Consequência: nenhum dos dois schemas físicos anteriores — as 23 tabelas de `BancoCEPRAEA.docx` e as 13 tabelas citadas pelo "Glossário v0.2" — é reaproveitado como base do modelo lógico desta fase. O modelo lógico nasce do Modelo Canônico sustentado pelas fontes relevantes segundo autoridade e finalidade, não desses documentos. | Fechado |
| D-03 | Contradição "STOP GATE fechado" vs. "DDL completo escrito" — reexplicada com evidência direta abaixo. Davi aceitou a leitura corrigida: as duas frases não se contradizem. | Resolvido — ver análise abaixo |

### D-03 em detalhe, com citação exata e localização

Verifiquei diretamente os dois documentos-fonte (não apenas o resumo de uma investigação
anterior), extraindo o texto de
`.drive/CEPRAEA BEACH PRO/REGISTRO MESTRE DE ARTEFATOS E FUNCIONAMENTO — SISTEMA CEPRAEA.docx` e
`.drive/CEPRAEA BEACH PRO/BancoCEPRAEA.docx`.

**REGISTRO MESTRE** (linha 864 do texto extraído, seção "Regressão final"; identidade
`REG-CEPRAEA-ARTIFACTS-001 v1.1`, "Data de verificação: ago. 9, 2026"):

> "STOP GATE físico permaneceu fechado; nenhum SQL, schema, migration, RLS ou banco externo foi
> criado."

Essa frase está dentro de uma seção que audita o ecossistema de planilhas (menciona "13
respostas nominais", "Wellness reconciliado em nove respondidos e dois pendentes") — ou seja, é
uma auditoria do estado operacional das planilhas, não uma auditoria de todos os documentos da
pasta.

**BancoCEPRAEA.docx** (linha 45 do texto extraído, seção "2. Evidências e correções aplicadas"):

> "O repositório atual contém o esqueleto funcional e dependência Supabase, mas não possui
> migrations de domínio implementadas; este documento define a base inicial."

E seu próprio cabeçalho se autodescreve como "Documento técnico para implementação **e revisão**
de domínio" — ou seja, uma proposta a revisar, não um registro de algo já aplicado.

**Minha leitura corrigida** (a investigação anterior nesta sessão havia caracterizado isto como
uma contradição direta — depois de ler as duas fontes eu mesmo, isso parece impreciso): as duas
frases provavelmente **não se contradizem**. "SQL foi escrito como proposta dentro de um
documento" e "nenhum SQL foi criado [executado contra um banco real]" podem ser verdadeiras ao
mesmo tempo. O próprio REGISTRO MESTRE instrui explicitamente, na sua aba 00: "Não promover
documento REVIEWED, rascunho, cópia, predecessor ou evidência a estado APPROVED/CURRENT" — o que
é exatamente a regra que a investigação anterior não aplicou ao tratar o DDL de
`BancoCEPRAEA.docx` como se contradissesse o STOP GATE.

**Resolução:** Davi aceitou a leitura corrigida — as duas frases não se contradizem. D-03 está
**fechado** como contradição. Fica registrada, só como nota de baixa prioridade e não bloqueante,
uma curiosidade residual sem informação suficiente para responder sozinho: a mesma frase de
`BancoCEPRAEA.docx` menciona "o repositório atual contém... dependência Supabase" — não está
registrado em nenhum dos dois textos se isso é só um `package.json` com `@supabase/supabase-js`
(baixo risco) ou algo mais. Não impede nem exige nada desta fase.

Em `decisoes/registro_decisoes.md`, D-01/D-02/D-03 recebem `id_decisao` formal
`DEC-001`/`DEC-002`/`DEC-003` respectivamente, lançados já em `AC-000` (seção 10), todos
`estado=RESOLVIDA`, `aprovador="Davi Sermenho"`.

## 1. Contexto

Você tentou modelar os dados do CEPRAEA BEACH PRO antes; considerou essa tentativa falha (D-02)
e pediu para refazer o entendimento e registro das fontes com um mecanismo que impeça a IA de
tratar como verdade algo que a fonte não sustenta. Esse mecanismo já existe, escrito por/para
você em `.drive/BEACH HANDBALL/Fluxo de Modelagem.gdoc.docx` — um checklist de 13 seções com
taxonomia de autoridade, schema de extração por regra e por termo, estados de conhecimento e
proibições explícitas contra inferência. Você confirmou: reaproveitar esse checklist aplicando
melhorias.

## 2. Resultado esperado desta fase

Ao final, `docs/modelagem/` contém:

- 28 dossiês (27 fontes hoje presentes + 1 registro de bloqueio para a fonte ainda ausente),
  cada um validado contra `schema_fonte.json`, com identidade canônica interna (`id_fonte = SRC-NNN`),
  `id_acao = AC-NNN` reservado à ação de processamento e `hash_sha256`/`caminho_local`/`id_drive`/nome
  tratados como identificadores ou locators da representação física; tipo/autoridade/proveniência/ciclo de vida da fonte e conteúdo relevante rastreável até
  fragmentos de evidência específicos (não o arquivo inteiro).
- Um inventário mestre com o status de cada uma das 28 entradas.
- Um registro de fragmentos de evidência (`evidencias/registro_evidencias.md`, `EVD-NNNN`) — o elo que faltava
  entre "fonte" e "conceito/regra" na cadeia de rastreabilidade (seção 4.3/4.5).
- Um registro de regras extraídas, cada uma rastreável até fragmentos de evidência específicos.
- Um **glossário** (`conhecimento/glossario.md`) — só significado dos termos — separado do **Modelo Canônico do
  Domínio** (`dominio/modelo_canonico_dominio.md`) — que existe, identidade, relações, regras e
  comportamento —, que é o produto intelectual principal desta fase (ver "Objetivo" acima).
- Os seis objetos obrigatórios de descoberta (seção 4.1), agora com schema formal único
  (`schema_elemento_modelo.json`, seção 4.5): `bounded_contexts.md`, `identidades_definitivas.md`,
  `agregados.md`, `invariantes.md`, `ciclos_de_vida.md`, `fronteiras_transacionais.md` — partes
  constituintes do Modelo Canônico, cada candidato rastreável até a evidência que o sustenta, sem
  nada presumido antecipadamente.
- Uma avaliação de maturidade por Bounded Context (`IMATURA`/`PARCIALMENTE_MADURA`/
  `MADURA_PARA_MODELO_LOGICO`, seção 4.4) e um modelo lógico relacional cobrindo **apenas** as
  áreas `MADURA_PARA_MODELO_LOGICO` — cobertura parcial é o resultado esperado (seção 4.4).
  Nenhuma migration é escrita nesta fase.
- Um registro de decisões com D-01, D-02, D-03 e qualquer bloqueio novo encontrado durante a
  execução.
- Seis testes adversariais (AD-01 a AD-06, seção 8) executados, com resultado e correções
  registrados — incluindo o teste central desta fase (AD-06): 100% das entradas em estado terminal (`CONCLUIDO`,
  `BLOQUEADO` ou `NAO_APLICAVEL`) não autoriza sozinho liberar o modelo lógico se restar ambiguidade semântica.
- `schema_fonte.json`, `schema_decisao.json`, `schema_termo.json`, `schema_regra.json`,
  `schema_evidencia.json` e `schema_elemento_modelo.json`, que todo registro respeita.

Nenhuma linha de SQL, migration, policy ou schema físico é gerada nesta fase — isso é a seção 7+
do checklist original, fora de escopo aqui.

## 3. Escopo

**Dentro:**

- os 27 arquivos reais hoje presentes em `.drive/CEPRAEA BEACH PRO/` + 1 entrada de bloqueio
  para o arquivo ausente;
- checklist adaptado; inventário; fragmentos de evidência; extração de regras; glossário
  (separado do modelo conceitual — seção 4.6);
- o **Modelo Canônico do Domínio** (`dominio/modelo_canonico_dominio.md`, seção 4.6) — produto principal
  desta fase — e os seis objetos obrigatórios de descoberta que o compõem (seção 4.1): Bounded
  Contexts, identidades definitivas, agregados, invariantes, ciclos de vida, fronteiras
  transacionais — por serem, segundo `modelagem_dominio_dados.md` §15.3, pré-físicos (tudo antes
  de "mecanismo PostgreSQL");
- avaliação de maturidade por área e modelo lógico relacional **só das áreas maduras** (seção 4.4;
  fim da seção 6 do checklist original);
- seis testes adversariais definidos na seção 8.

**Fora:**

- `.drive/BEACH HANDBALL/` (mesmo checklist, fase separada);
- a "pasta canônica" do Drive (fora de escopo por decisão sua já registrada);
- modelo físico PostgreSQL/Supabase, migrations, RLS, testes SQL, mecanismo transacional
  (transações, locks, isolation, concorrência — seções 7-8 do checklist original);
- rotação da credencial em texto plano encontrada em `CEPRAEA 2026(1).xlsx` (ação operacional
  seguinte, não de modelagem).

## 4. Metodologia: checklist existente + melhorias (decisão fixada, não uma pergunta)

Adoto as seções 1-6, 9, 11-13 do "Guia 1" e as taxonomias do "Guia 2" de
`Fluxo de Modelagem.gdoc.docx` como texto de referência, com seis melhorias — cada uma motivada
por um problema real já observado, e cada uma **implementada como campo obrigatório ou regra
`if/then` dentro de `schema_fonte.json`/`schema_decisao.json` (seção 6), não apenas como texto**:

| # | Melhoria | Motivo concreto | Onde vira regra verificável |
|---|---|---|---|
| a | `id_fonte=SRC-NNN` é a identidade canônica estável; `hash_sha256`+`caminho_local` são locators obrigatórios quando a fonte existe; `id_drive` é locator opcional | `CEPRAEA 2026.xlsx`/`(1)`/`(2)` colidem de nome — mas nem todo arquivo tem `id_drive` recuperável neste ambiente | `schema_fonte.json.required` (seção 5.1) |
| b | Dado sensível nunca é transcrito literalmente | senha em texto plano para 18 atletas em `CEPRAEA 2026(1).xlsx` | `schema_fonte.json` regra `if dado_sensivel_encontrado=true then tratamento_dado_sensivel obrigatório` |
| c | Conflito entre fontes "autoritativas" vira `BLOQUEADO` na mesma passada | contradição D-03 | `schema_decisao.json.estado` |
| d | Documento da tentativa anterior nasce com `autoridade_fonte=AUXILIAR` e `estado_fonte=SUBSTITUIDA`, nunca `OFICIAL`/`PRIMARIA`/`VIGENTE`, mesmo se tecnicamente completo | `BancoCEPRAEA.docx` tem DDL completo mas não é autoritativo (D-02) | `schema_fonte.json.autoridade_fonte`/`estado_fonte` fixados por regra editorial, testado em AD-01 |
| e | Nenhuma etapa escreve/move/apaga dentro de `.drive/**`; scratch só em `/tmp` da sessão | D-01 | regra de execução (seção 7) |
| f | Toda decisão `RESOLVIDA` exige `aprovador = "Davi Sermenho"` — nunca a própria IA | evitar repetição do que causou D-02 | `schema_decisao.json` regra `if estado=RESOLVIDA then aprovador=Davi Sermenho` |

### 4.1 Seis objetos obrigatórios de descoberta

`modelagem_dados_agente.md` e `modelagem_dominio_dados.md` §9 exigem, como entregável formal —
não presumido antecipadamente, cada candidato distinguindo evidência/interpretação/inferência/
hipótese/conflito/decisão validada/decisão pendente —, seis objetos que meu plano original não
tinha como artefato próprio:

| Objeto | Arquivo novo | Campos de formalização (condensado das fontes canônicas) |
|---|---|---|
| Bounded Context | `bounded_contexts.md` | id canônico, nome, finalidade, conceitos internos, conceitos externos referenciados, regras próprias, eventos relevantes, dados sob responsabilidade, dependências com outros contextos, fontes, ambiguidades, estado de validação |
| Identidade definitiva | `identidades_definitivas.md` | nome canônico, definição, critérios de identidade, atributos identificadores, identificadores naturais, identificador técnico candidato, regras de unicidade, aliases, possíveis duplicidades, critérios de reconciliação, temporalidade, fontes, incertezas, estado de validação |
| Agregado | `agregados.md` | nome, Aggregate Root, componentes internos, identidades internas, referências externas, invariantes protegidas, operações permitidas, eventos produzidos, ciclo de vida, fontes, justificativa, estado de validação |
| Invariante | `invariantes.md` | identificador, declaração formal, linguagem natural, conceitos afetados, contexto, condição, consequência, exceções, período de validade, fonte, evidência, autoridade, impacto, implementação candidata, teste positivo, teste negativo, estado de validação |
| Ciclo de vida | `ciclos_de_vida.md` | objeto, estado inicial, estados possíveis, estados terminais, transições, evento causador, condições, ator autorizado, invariantes envolvidas, temporalidade, comportamento histórico, regras de correção, fontes, exceções, estado de validação |
| Fronteira transacional | `fronteiras_transacionais.md` | operação, agregado(s) envolvido(s), alterações que precisam ocorrer juntas, invariantes garantidas imediatamente, inconsistência temporária aceitável (sim/não), mecanismo candidato (transação/evento — sem decidir ainda o mecanismo físico), fontes, estado de validação |

O campo `estado de validação` dos seis usa o mesmo enum epistemológico formalizado em
`schema_termo.json`/`schema_regra.json` (seção 5.5/5.6): `OBSERVADO / INFERIDO / AMBÍGUO /
CONFLITANTE / VALIDADO / REJEITADO`. Os seis objetos usam `schema_elemento_modelo.json` (seção
4.5), discriminado pelo campo `tipo` — um schema único para os seis, não seis schemas quase
idênticos nem prosa sem validação mecânica.

**Ordem de dependência** (`modelagem_dominio_dados.md` §15.3): conceitos → identidades → relações
→ invariantes → ciclos de vida → agregados → operações → fronteiras transacionais → mecanismo
PostgreSQL. Os seis objetos ficam **dentro** do escopo desta fase (tudo até "fronteiras
transacionais" é pré-físico); só "mecanismo PostgreSQL" continua fora (seção 3).

**Quando são preenchidos:** não é um lote à parte. Cada dossiê (`AC-NNN`, seção 7) já pode gerar
ou atualizar entradas nesses seis arquivos, do mesmo jeito que já atualiza `conhecimento/glossario.md`/
`conhecimento/registro_regras.md` — oportunisticamente, conforme a evidência aparece em cada fonte. `AC-029`
(síntese) faz a consolidação final: avalia a maturidade de cada Bounded Context (seção 4.4) e
escreve `dominio/modelo_canonico_dominio.md` — a direção é sempre Modelo Canônico maduro → modelo lógico,
nunca o inverso; nenhum objeto é justificado retroativamente pelo que o modelo lógico "usa".

### 4.2 Fatos de domínio pré-semeados

Correção do ponto 12 da sua revisão: fatos que **você já validou como especialista do domínio**
não devem nascer `OBSERVADO` como se ainda fossem hipótese — isso finge que uma validação humana
que já aconteceu não aconteceu. Distinção que este plano agora faz entre os três pré-semeados:

**INV-001** em `dominio/invariantes.md` (`schema_elemento_modelo.json`, `tipo=INVARIANTE`,
`estagio=DOMINIO` — nasce direto em `dominio/`, não passa por `candidatos/`, porque já chega
`VALIDADO`) — **`VALIDADO` desde `AC-000`**, porque você confirmou isso diretamente, não porque o
canônico afirma com confiança:

- Declaração formal: `papel_operacional ∈ {ATLETA, TREINADOR} ∧ ∀ usuário: |papéis(usuário)| = 1`.
- Linguagem natural: cada usuário operacional do CEPRAEA-BEACH-PRO tem exatamente um papel —
  `ATLETA` ou `TREINADOR`; uma atleta nunca acumula outra função no sistema.
- `fonte: ["REF:modelagem_dados_agente.md — Identidade humana, autenticação e papel", "REF:modelagem_dominio_dados.md §7/§13.2"]`
  — citação direta, não `EVD-NNNN`, porque a fonte é um documento referência (seção 12), não um
  dossiê desta pasta.
- `estagio=DOMINIO`, `estado_epistemologico=VALIDADO`, `estado_tecnico=NAO_MODELADO`,
  `promoted_from`: a mesma citação `REF:` do campo `fonte` (não há `candidatos/invariantes.md`
  de origem — nasce direto em `dominio/`), `promoted_by="PRE-SEED"` (exceção documentada, seção
  4.5 — decisão humana direta, não reconciliação de hipótese),
  `evidencia.approval_evidence={"aprovador":"Davi Sermenho","data":<data desta decisão>}`,
  `evidencia.source_evidence`: método = "decisão humana direta + documentos REF listados em fonte"; resultado = "regra explicitamente confirmada por Davi Sermenho";,
  `evidencia.semantic_evidence`: "confirmado diretamente por Davi Sermenho, especialista do domínio, nesta conversa.",
  `evidencia.repository_evidence.action_ref="AC-000"`
- Nota — **não é imutável**: se `AC-004`/`AC-008`–`AC-010`/`AC-016`–`AC-019` revelarem um papel
  operacional diferente ou divergência temporal, isso vira novo registro em
  `decisoes/registro_decisoes.md` (conflito, melhoria c) para você decidir — não uma reversão
  silenciosa do que já foi validado.

**`CTX-001` a `CTX-008`** em `candidatos/bounded_contexts.md` (`estagio=CANDIDATO`), permanecem
`INFERIDO` — são hipóteses estruturais derivadas da modelagem de referência, não observações diretas nem fatos que você
confirmou; a distinção do ponto 12 é justamente essa: só o que você validou entra `VALIDADO` e
`dominio/`, o resto continua candidato:

- `CTX-001` — Identidade e Participantes
- `CTX-002` — Equipe e Vínculos
- `CTX-003` — Treinamentos
- `CTX-004` — Disponibilidade e Convocação
- `CTX-005` — Competições
- `CTX-006` — Jogos e Resultados
- `CTX-007` — Fontes Normativas e Proveniência
- `CTX-008` — Identidade Digital e Autorização

Cada um com `fonte: ["REF:modelagem_dominio_dados.md §10.3"]`, `maturidade=IMATURA` (ainda
hipótese, seção 4.4), e a nota do próprio canônico anexada literalmente: "hipóteses de
organização... a confirmar, subdividir, agrupar ou rejeitar conforme as evidências."

**`DEC-006`** em `decisoes/registro_decisoes.md` — **`estado=RESOLVIDA`, `aprovador="Davi Sermenho"`**
desde `AC-000`, com `evidencia.repository_evidence.action_ref="AC-000"`: *"Você confirmou diretamente, como especialista do domínio, a contagem de 19
atletas e 1 treinador no estado atual do CEPRAEA-BEACH-PRO (`modelagem_dominio_dados.md` §7 já
registrava o mesmo número). Aceito como válido a partir desta decisão, não como candidato a
confirmar."* Continua com nota operacional: se `AC-001`, `AC-004`, `AC-008`–`AC-010`,
`AC-016`–`AC-019` contarem um número diferente, isso é divergência temporal/operacional (elenco
muda), registrada como novo item em `decisoes/registro_decisoes.md` — não uma contradição do que já foi
validado, e não silenciosamente substituída.

### 4.3 Enriquecimentos de conteúdo para `fluxo_de_modelagem.md`/`taxonomias.md`

Baixo impacto — não muda schema, tabela nem sequência de IDs; é conteúdo que `AC-000` copia
(adaptado, não literal) para dentro desses dois arquivos de referência, hoje só descritos em
prosa na seção 6. Registro aqui para não se perder entre sessões.

**Rastreabilidade — cadeia adotada.** As fontes têm três variantes da mesma ideia, de
especificidade crescente. Adoto a mais geral, que `modelagem_dominio_dados.md` §24 chama
explicitamente de "metamodelo mínimo" — as outras duas (`fonte → regra → conceito → tabela →
constraint → teste`, do Guia 2 original; `fonte → evidência → conceito → regra → invariante →
implementação → teste`, de `modelagem_dados_agente.md`) são casos particulares dela, não
alternativas concorrentes:

```text
Fonte → Fragmento/Evidência → Conceito → Regra → Elemento do Modelo → Implementação → Teste
```

— percorrível também no sentido inverso. "Elemento do Modelo" cobre, conforme o caso: um termo do
glossário, ou qualquer um dos seis objetos da seção 4.1 (invariante, agregado, Bounded Context
etc.) que a regra sustente. Nesta fase a cadeia para na prática em "Elemento do Modelo" —
"Implementação"/"Teste" pertencem ao modelo físico (fora de escopo, seção 3).

A rastreabilidade não é amostral: `verificar_referencias.mjs` valida 100% das relações `EVD.id_fonte→SRC`, `EVD.id_acao→AC`, `TERMO/REGRA/elemento.fonte→EVD|REF`, `bounded_context_id→CTX`, promoção candidato↔domínio, referências do Modelo Canônico e `derived_from[]` do modelo lógico. A amostragem manual existe apenas como sanity check humano.


**Perguntas de competência — união das duas listas, sem duplicar:**

- Do checklist original: qual era o vínculo de uma atleta em determinada data? qual foi a última
  resposta de disponibilidade? quais versões anteriores existiram? quem registrou a presença?
  qual documento sustenta um resultado? qual regulamento estava vigente? uma atleta pode
  consultar dados de outra atleta?
- Acrescentadas por `modelagem_dominio_dados.md` §22, específicas da descoberta: de quais fontes
  surge este conceito? há mais de uma definição? o termo possui significados diferentes? esta
  estrutura possui identidade? o histórico é necessário? há uma invariante associada? o objeto
  pertence a qual contexto? a alteração precisa ocorrer atomicamente? o dado é factual ou
  derivado?

**Critérios de qualidade — 15, não 14.** `modelagem_dominio_dados.md` §38 diz explicitamente que
"amplia os 14 critérios já apresentados no documento original", não que os substitui. União:
semanticamente correta, **evidenciável** (critério novo — "as conclusões materiais possuem
suporte identificável"), rastreável, temporalmente correta, proporcional, normalizada
adequadamente, executável, íntegra, segura, testável, evolutiva, reproduzível, auditável,
independente da confiança na IA, orientada à operação.

### 4.4 Gate de maturidade (corrige a inversão do Definition of Done)

Correção estrutural pedida por você: a dependência correta é **Modelo Canônico maduro → modelo
lógico**, nunca o inverso. A versão anterior deste plano avaliava os seis objetos "na medida em
que o modelo lógico final os usa" — invertido. Fica assim:

Cada `BOUNDED_CONTEXT` (seção 4.5) ganha um campo `maturidade`:

| Maturidade | Critério (condensado de `modelagem_dominio_dados.md` §39, 16 itens) |
|---|---|
| `IMATURA` | Conceitos ainda não definidos, ou identidades não resolvidas, ou existe termo/regra `AMBIGUO`/`CONFLITANTE` sem resolução dentro deste Bounded Context, ou o próprio Bounded Context ainda não possui `estado_epistemologico=VALIDADO` |
| `PARCIALMENTE_MADURA` | Conceitos definidos e identidades resolvidas; mas invariantes, ciclos de vida, agregados ou fronteiras transacionais deste contexto ainda incompletos, ou há pendência não crítica registrada |
| `MADURA_PARA_MODELO_LOGICO` | Os 16 critérios de `modelagem_dominio_dados.md` §39 satisfeitos para este contexto: conceitos definidos; identidades resolvidas; aliases/sinônimos reconciliados; relações com significado; cardinalidades conhecidas; invariantes identificadas; ciclos de vida formalizados quando necessário; Bounded Context confirmado (não mais hipótese); agregados determinados; fronteiras transacionais justificadas; regras com evidência; conflitos materiais resolvidos; pendências remanescentes somente quando classificadas explicitamente como não bloqueantes e incapazes de alterar identidade, definição, relação, cardinalidade, invariante, ciclo de vida, agregado, fronteira transacional ou estrutura lógica derivada; decisões com `estado_epistemologico`; histórico tratado corretamente; perguntas de competência respondíveis; testes deriváveis |

**Regra adicional de bloqueio de maturidade:** qualquer `AMBIGUO` ou `CONFLITANTE` com impacto estrutural obriga o contexto a permanecer `IMATURA` ou `PARCIALMENTE_MADURA`; nunca pode ser `MADURA_PARA_MODELO_LOGICO`.

**Regra de derivação:** `logico/modelo_logico_relacional.md` só recebe entidades/tabelas/relações de
Bounded Contexts em `MADURA_PARA_MODELO_LOGICO`. Um Bounded Context `IMATURA`/
`PARCIALMENTE_MADURA` ao final da fase **não é erro** — é um resultado válido, registrado como tal
em `dominio/modelo_canonico_dominio.md`, sem entrada correspondente no modelo lógico. Isso é reavaliado em
`AC-029` (seção 10), não presumido em nenhum ponto anterior.

### 4.5 Fragmento de evidência e schema único dos seis objetos

**Problema que isso resolve:** até aqui, `fonte` em `schema_termo.json`/`schema_regra.json`
apontava para `AC-NNN` — o arquivo inteiro. Uma planilha de 30 abas podia "sustentar" um conceito
sem indicar qual célula, linha ou trecho. Falta o nó que a própria cadeia da seção 4.3 já previa
("Fragmento/Evidência") como elo entre Fonte e Conceito.

#### `docs/modelagem/schemas/schema_evidencia.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cepraea.local/schemas/schema_evidencia.json",
  "title": "Fragmento de evidência (EvidenceFragment)",
  "type": "object",
  "required": [
    "id_evidencia",
    "id_fonte",
    "id_acao",
    "localizacao",
    "trecho_literal",
    "tipo_evidencia",
    "dado_sensivel_encontrado"
  ],
  "properties": {
    "id_evidencia": {
      "type": "string",
      "pattern": "^EVD-[0-9]{4}$"
    },
    "id_fonte": {
      "type": "string",
      "pattern": "^SRC-[0-9]{3}$",
      "description": "Identidade estável da fonte (schema_fonte.json.id_fonte) — o elo semântico permanente. Nesta fase, SRC-NNN e id_acao compartilham o mesmo número (1:1), mas são conceitos diferentes: SRC-NNN é a fonte; id_acao é a ação de processá-la."
    },
    "id_acao": {
      "type": "string",
      "pattern": "^AC-[0-9]{3}$",
      "description": "Qual ação de aquisição (seção 4.8) capturou este fragmento — provenance operacional, não a identidade da fonte."
    },
    "localizacao": {
      "type": "string",
      "minLength": 1,
      "description": "Localização literal e específica — aba+coluna+linha, página+parágrafo, célula, seção. NUNCA 'o arquivo inteiro' ou vazio."
    },
    "trecho_literal": {
      "type": "string",
      "minLength": 1,
      "description": "Excerto literal curto do fragmento. Quando dado_sensivel_encontrado=true, descreve o tipo/formato, nunca o valor real (melhoria b)."
    },
    "tipo_evidencia": {
      "enum": [
        "TEXTO",
        "TABELA",
        "CELULA",
        "IMAGEM",
        "METADADO"
      ]
    },
    "dado_sensivel_encontrado": {
      "type": "boolean"
    },
    "tratamento_dado_sensivel": {
      "type": [
        "string",
        "null"
      ]
    }
  },
  "if": {
    "properties": {
      "dado_sensivel_encontrado": {
        "const": true
      }
    }
  },
  "then": {
    "required": [
      "tratamento_dado_sensivel"
    ]
  }
}
```

`evidencias/registro_evidencias.md` (seção 6) acumula todos os `EVD-NNNN`, um bloco `json` por fragmento,
validado por este schema. `fonte` em `schema_termo.json`/`schema_regra.json`/
`schema_elemento_modelo.json` passa a exigir `EVD-NNNN` (não mais `AC-NNN` bruto) — ver seções
5.5/5.6 e abaixo.

#### `docs/modelagem/schemas/schema_elemento_modelo.json` — substitui os seis schemas informais

Resolve a assimetria: termos/regras tinham JSON Schema rigoroso, os seis objetos da seção 4.1
ficavam em prosa. Um único schema, discriminado por `tipo`, cobre os seis — sem exigir seis
schemas quase idênticos:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cepraea.local/schemas/schema_elemento_modelo.json",
  "title": "Elemento do Modelo Canônico (Bounded Context / Identidade / Agregado / Invariante / Ciclo de vida / Fronteira transacional)",
  "type": "object",
  "required": [
    "id_elemento",
    "tipo",
    "nome",
    "estagio",
    "fonte",
    "estado_epistemologico",
    "estado_tecnico",
    "evidencia"
  ],
  "properties": {
    "id_elemento": {
      "type": "string",
      "pattern": "^(CTX|IDN|AGG|INV|LFC|TRX)-[0-9]{3}$",
      "description": "Namespace por tipo (seção 4.8): CTX=Bounded Context, IDN=Identidade, AGG=Agregado, INV=Invariante, LFC=Ciclo de vida, TRX=Fronteira transacional."
    },
    "tipo": {
      "enum": [
        "BOUNDED_CONTEXT",
        "IDENTIDADE",
        "AGREGADO",
        "INVARIANTE",
        "CICLO_DE_VIDA",
        "FRONTEIRA_TRANSACIONAL"
      ]
    },
    "nome": {
      "type": "string",
      "minLength": 1
    },
    "estagio": {
      "enum": [
        "CANDIDATO",
        "PROMOVIDO",
        "DOMINIO"
      ],
      "description": "Em qual diretório este elemento vive fisicamente (seção 4.7) e seu papel ali. CANDIDATO: hipótese em candidatos/, ainda não promovida — pode ser editada. PROMOVIDO: o registro ORIGINAL em candidatos/ depois que sua contraparte foi criada em dominio/ — vira histórico congelado da hipótese, nunca mais editado, nunca apagado. DOMINIO: a representação canônica em dominio/, sempre VALIDADO. Nunca existem duas versões concorrentes 'igualmente válidas' do mesmo elemento — candidatos/ com PROMOVIDO é explicitamente passado, dominio/ é a única versão ativa."
    },
    "promoted_from": {
      "type": [
        "string",
        "null"
      ],
      "description": "Obrigatório quando estagio=DOMINIO. Promoção normal: candidatos/<arquivo>#<ID>. PRE-SEED: REF:<documento>..."
    },
    "promoted_by": {
      "type": [
        "string",
        "null"
      ],
      "pattern": "^(SEM-[0-9]{3}|PRE-SEED)$",
      "description": "Identificador da ação semântica SEM-NNN que promoveu o elemento. PRE-SEED é a única exceção para decisão humana direta já validada em AC-000."
    },
    "promoted_to": {
      "type": [
        "string",
        "null"
      ],
      "description": "Obrigatório quando estagio=PROMOVIDO: caminho e id de destino, ex.: 'dominio/invariantes.md#INV-003' — o inverso de promoted_from, fecha a rastreabilidade nos dois sentidos."
    },
    "bounded_context_id": {
      "type": [
        "string",
        "null"
      ],
      "pattern": "^CTX-[0-9]{3}$",
      "description": "A qual Bounded Context este elemento pertence. Null quando tipo=BOUNDED_CONTEXT (é o próprio) ou ainda não determinado."
    },
    "detalhes": {
      "type": "object",
      "description": "Campos específicos do tipo, conforme a tabela da seção 4.1 (ex.: Aggregate Root para AGREGADO; estados possíveis/transições para CICLO_DE_VIDA; critérios de identidade/aliases para IDENTIDADE)."
    },
    "maturidade": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "IMATURA",
        "PARCIALMENTE_MADURA",
        "MADURA_PARA_MODELO_LOGICO",
        null
      ],
      "description": "Obrigatório quando tipo=BOUNDED_CONTEXT (seção 4.4); null para os outros tipos."
    },
    "fonte": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^(EVD-[0-9]{4}|REF:.+)$"
      },
      "minItems": 1,
      "description": "Fragmentos de evidência (EVD-NNNN) do corpus de dossiês, seção 4.5 — não SRC-NNN/AC-NNN bruto. Exceção: elementos pré-semeados a partir de documento referência (não dossiê), citam 'REF:<documento> §<seção>' (ex.: 'REF:modelagem_dominio_dados.md §7') — caso de INV-001/CTX-001..008 (seção 4.2), que não têm fonte no corpus de dossiês."
    },
    "estado_epistemologico": {
      "enum": [
        "OBSERVADO",
        "INFERIDO",
        "AMBIGUO",
        "CONFLITANTE",
        "VALIDADO",
        "REJEITADO"
      ]
    },
    "estado_tecnico": {
      "enum": [
        "NAO_MODELADO",
        "MODELADO",
        "IMPLEMENTADO",
        "TESTADO",
        "ATIVO",
        "SUBSTITUIDO"
      ]
    },
    "ambiguidades": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "evidencia": {
      "type": "object",
      "required": [
        "source_evidence"
      ],
      "properties": {
        "source_evidence": {
          "type": "object",
          "required": [
            "comando_ou_metodo",
            "resultado"
          ],
          "properties": {
            "comando_ou_metodo": {
              "type": "string",
              "minLength": 1
            },
            "resultado": {
              "type": "string",
              "minLength": 1
            },
            "limitacoes": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "semantic_evidence": {
          "type": [
            "string",
            "null"
          ],
          "description": "Por que esta interpretação é a correta — o raciocínio, não só o método de extração."
        },
        "approval_evidence": {
          "type": "object",
          "properties": {
            "aprovador": {
              "type": "string",
              "enum": [
                "Davi Sermenho",
                "PENDENTE"
              ]
            },
            "data": {
              "type": [
                "string",
                "null"
              ],
              "format": "date"
            }
          }
        },
        "repository_evidence": {
          "type": "object",
          "properties": {
            "action_ref": {
              "type": "string",
              "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
            }
          }
        }
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "tipo": {
            "const": "BOUNDED_CONTEXT"
          }
        }
      },
      "then": {
        "required": [
          "maturidade"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "estado_tecnico": {
            "enum": [
              "MODELADO",
              "IMPLEMENTADO",
              "TESTADO",
              "ATIVO",
              "SUBSTITUIDO"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        }
      },
      "then": {
        "properties": {
          "evidencia": {
            "properties": {
              "semantic_evidence": {
                "type": "string",
                "minLength": 1
              },
              "approval_evidence": {
                "type": "object",
                "properties": {
                  "aprovador": {
                    "const": "Davi Sermenho"
                  },
                  "data": {
                    "type": "string",
                    "format": "date"
                  }
                },
                "required": [
                  "aprovador",
                  "data"
                ]
              },
              "repository_evidence": {
                "type": "object",
                "properties": {
                  "action_ref": {
                    "type": "string",
                    "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
                  }
                },
                "required": [
                  "action_ref"
                ]
              }
            },
            "required": [
              "semantic_evidence",
              "approval_evidence",
              "repository_evidence"
            ]
          }
        },
        "required": [
          "evidencia"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "estagio": {
            "const": "DOMINIO"
          }
        }
      },
      "then": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        },
        "required": [
          "promoted_from",
          "promoted_by"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "estagio": {
            "const": "PROMOVIDO"
          }
        }
      },
      "then": {
        "properties": {
          "promoted_by": {
            "type": "string",
            "pattern": "^SEM-[0-9]{3}$"
          },
          "promoted_to": {
            "type": "string",
            "pattern": "^dominio/.+#(CTX|IDN|AGG|INV|LFC|TRX)-[0-9]{3}$"
          }
        },
        "required": [
          "promoted_to",
          "promoted_by"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "promoted_by": {
            "const": "PRE-SEED"
          }
        },
        "required": [
          "promoted_by"
        ]
      },
      "then": {
        "properties": {
          "promoted_from": {
            "type": "string",
            "pattern": "^REF:.+"
          },
          "evidencia": {
            "properties": {
              "approval_evidence": {
                "type": "object",
                "properties": {
                  "aprovador": {
                    "const": "Davi Sermenho"
                  },
                  "data": {
                    "type": "string",
                    "format": "date"
                  }
                },
                "required": [
                  "aprovador",
                  "data"
                ]
              },
              "repository_evidence": {
                "type": "object",
                "properties": {
                  "action_ref": {
                    "const": "AC-000"
                  }
                },
                "required": [
                  "action_ref"
                ]
              }
            },
            "required": [
              "approval_evidence",
              "repository_evidence"
            ]
          }
        },
        "required": [
          "promoted_from",
          "evidencia"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "promoted_by": {
            "pattern": "^SEM-[0-9]{3}$"
          }
        },
        "required": [
          "promoted_by"
        ]
      },
      "then": {
        "properties": {
          "promoted_from": {
            "type": "string",
            "pattern": "^candidatos/.+#(CTX|IDN|AGG|INV|LFC|TRX)-[0-9]{3}$"
          }
        },
        "required": [
          "promoted_from"
        ]
      }
    }
  ]
}
```

A terceira regra `allOf` é a correção central do ponto 7 da sua revisão: antes, `VALIDADO` podia confundir prova de versionamento com prova semântica. Agora `VALIDADO` exige quatro eixos distintos: `source_evidence`, `semantic_evidence`, `approval_evidence` com aprovador/data e `repository_evidence.action_ref`. O SHA real é resolvido externamente por Git; nunca é autorreferenciado dentro do próprio commit. Mecanicamente, a IA não consegue marcar algo `VALIDADO` sozinha — o schema rejeita `aprovador=PENDENTE` nesse estado.

### 4.6 Modelo Canônico do Domínio — artefato central, separado do glossário

Correção dos pontos 1 e 3 da sua revisão. Dois arquivos, não um:

- **`conhecimento/glossario.md`** — só significado. Responde "o que este termo quer dizer?". Um bloco `json`
  por `TERMO-NNN`, valida contra `schema_termo.json` (seção 5.5).
- **`dominio/modelo_canonico_dominio.md`** — existência, identidade, relações, regras, comportamento.
  Responde "o que existe, qual sua identidade, como se relaciona, que regras protege, como muda".
  Estrutura: uma seção por `CTX-NNN` (Bounded Context), cada uma reunindo — por referência, não
  duplicando o conteúdo — os elementos de `bounded_contexts.md`, `identidades_definitivas.md`,
  `agregados.md`, `invariantes.md`, `ciclos_de_vida.md`, `fronteiras_transacionais.md` que
  declaram aquele `bounded_context_id`, mais os termos de `conhecimento/glossario.md` e regras de
  `conhecimento/registro_regras.md` que o contexto usa, mais a `maturidade` atual do contexto (seção 4.4).

Os seis arquivos da seção 4.1 continuam existindo como **registros detalhados** por tipo (mais
fácil de raspar/validar em lote); `dominio/modelo_canonico_dominio.md` é a **síntese estrutural** —
o Modelo Canônico propriamente dito, não um sétimo arquivo solto. `AC-029` (seção 10) é quem
escreve essa síntese, depois de avaliar a maturidade de cada `CTX-NNN`. A localização exata de
cada um dos seis (dois arquivos por tipo — candidato e promovido) está na seção 4.7.

### 4.7 Estrutura da branch dedicada e bootstrap obrigatório da modelagem

> **Nota — `DEC-008` (`decisoes/registro_decisoes.md`):** a versão original desta seção exigia uma
> worktree Git irmã do repositório (`<repo-parent>/cepraea-modelagem-canonica`) como mecanismo de
> isolamento. Essa exigência foi removida por decisão de Davi Sermenho durante `AC-000`: o
> `EXECUTOR` não tem permissão de escrita em `.git/` do repositório principal (não consegue criar
> a branch/worktree) e, mesmo quando a worktree foi criada manualmente por Davi no host, ela não
> era visível dentro do devcontainer do agente (só o diretório do próprio repositório é montado).
> O isolamento agora é feito por **branch dedicada + `WRITE_SCOPE` explícito**, não por diretório
> físico separado. O texto abaixo já reflete essa decisão.

Antes do processamento da primeira fonte, a fase cria, dentro do próprio repositório
`cepraea-beach-pro`, a hierarquia de diretórios abaixo em `docs/modelagem/` — não uma pasta plana
— na branch dedicada `feat/cepraea-domain-modeling`. Objetivo: nenhum artefato salta direto de
fonte para modelo lógico:

```text
fontes → evidências → conhecimento → candidatos → modelo canônico → modelo lógico
```

**Branch dedicada:**

```text
repositório: cepraea-beach-pro   (mesmo checkout, sem worktree separada)
branch:      feat/cepraea-domain-modeling
```

`main`/`master` não recebe nenhuma escrita desta fase (regra do `AGENT_POLICY.md`, seção 12).
Toda escrita de modelagem acontece exclusivamente dentro de `docs/modelagem/**` (`WRITE_SCOPE`,
abaixo) na branch `feat/cepraea-domain-modeling` — nunca em `main`/`master`, nunca fora desse
escopo. Isso impede duas branches estabelecerem modelos canônicos incompatíveis ao mesmo tempo — o
mesmo problema que gerou os dois schemas físicos conflitantes de D-02.

**Base imutável, origem das fontes e escopos de acesso:**

`AC-000` registra explicitamente:

```text
BASE_REF=<ref aprovada no início do AC-000>
BASE_SHA=$(git rev-parse "$BASE_REF")
MAIN_SHA_BEFORE=$(git rev-parse main)
CEPRAEA_SOURCE_ROOT=<realpath do diretório real .drive/CEPRAEA BEACH PRO>
```

A branch `feat/cepraea-domain-modeling` nasce exatamente de `BASE_SHA`, nunca implicitamente de
qualquer branch aberta no momento — operação de criação de branch/ref reservada a Davi
(`AGENT_POLICY.md` §Autoridade; o `EXECUTOR` não tem permissão de escrita em `.git/refs/heads`). O
`README.md` de `docs/modelagem/` registra `base_ref`, `base_sha`, `main_sha_before`,
`branch_modelagem` e `cepraea_source_root`.

Escopos formais (`DEC-008`):

```text
WRITE_SCOPE_EXECUTOR
  docs/modelagem/**
  # .agent-flow/executions/** — REMOVIDO (DEC-GOV-001, 2026-08-14)

WRITE_SCOPE_REVIEWER
  # .agent-flow/reviews/** — REMOVIDO (DEC-GOV-001, 2026-08-14)
  # Reviewer não produz artefatos de escrita; emite verdict ao humano.

READ_SCOPE
  repositório cepraea-beach-pro, quando necessário à ação
  $CEPRAEA_SOURCE_ROOT/**
  documentos de referência explicitamente listados na seção 12

CEPRAEA_SOURCE_ROOT — modo READ_ONLY
```

Escrita fora de `WRITE_SCOPE_EXECUTOR` (ou `WRITE_SCOPE_REVIEWER`, para o `REVIEWER`) é proibida.
Leitura fora de `READ_SCOPE` é proibida.

**Guardas antes da criação da branch:**

1. `feat/cepraea-domain-modeling` não existe, ou seu estado é explicitamente reconhecido antes de reutilização;
2. `BASE_SHA` existe;
3. `CEPRAEA_SOURCE_ROOT` existe e as 27 fontes presentes são legíveis;
4. nenhuma limpeza destrutiva (`rm -rf`, remoção silenciosa de branch) é permitida.

Falha em qualquer guarda deixa `AC-000=BLOQUEADO`; nunca autoriza apagar ou reutilizar silenciosamente uma branch antiga.


**Estrutura obrigatória**, criada por `AC-000` dentro de `docs/modelagem/` (branch
`feat/cepraea-domain-modeling`):

```text
docs/modelagem/
├── README.md
│
├── processo/
│   ├── fluxo_de_modelagem.md
│   ├── taxonomias.md
│   ├── criterios_maturidade.md        (seção 4.4, extraído para arquivo próprio)
│   └── perguntas_competencia.md       (seção 4.3)
│
├── fontes/
│   ├── inventario_fontes.md
│   └── dossies/
│       └── <slug-literal>.md          (28 no total, seção 6 original)
│
├── evidencias/
│   └── registro_evidencias.md         (EVD-NNNN, schema_evidencia.json)
│
├── conhecimento/
│   ├── glossario.md                   (TERMO-NNN, schema_termo.json)
│   ├── registro_regras.md             (REGRA-NNN, schema_regra.json)
│   └── conflitos_semanticos.md        (AMBIGUO/CONFLITANTE consolidados, ligado a AD-04/AD-05)
│
├── candidatos/
│   ├── identidades.md
│   ├── bounded_contexts.md
│   ├── invariantes.md
│   ├── ciclos_de_vida.md
│   ├── agregados.md
│   └── fronteiras_transacionais.md
│   (todos schema_elemento_modelo.json, estagio=CANDIDATO)
│
├── dominio/
│   ├── modelo_canonico_dominio.md     (síntese, seção 4.6)
│   ├── identidades_definitivas.md
│   ├── bounded_contexts.md
│   ├── invariantes.md
│   ├── ciclos_de_vida.md
│   ├── agregados.md
│   └── fronteiras_transacionais.md
│   (todos schema_elemento_modelo.json, estagio=DOMINIO)
│
├── logico/
│   ├── modelo_logico_relacional.md    (só CTX-NNN em MADURA_PARA_MODELO_LOGICO)
│   └── areas_pendentes.md             (CTX-NNN que ficaram IMATURA/PARCIALMENTE_MADURA e por quê)
│
├── decisoes/
│   └── registro_decisoes.md           (DEC-NNN, schema_decisao.json)
│
└── schemas/
    ├── schema_fonte.json
    ├── schema_evidencia.json
    ├── schema_termo.json
    ├── schema_regra.json
    ├── schema_elemento_modelo.json
    ├── schema_decisao.json
    ├── validar.mjs
    ├── verificar_referencias.mjs
    ├── verificar_repositorio.mjs
    └── fixtures/
        └── manifest.json
```

**Regra de responsabilidade por diretório:**

- `fontes/` — o corpus analisado: inventário, identidade das fontes, dossiês. Nunca contém
  conclusão canônica.
- `evidencias/` — observações verificáveis extraídas das fontes, cada uma um `EVD-NNNN` apontando
  para `id_fonte` + localização + natureza + limitações + sensibilidade. Uma evidência não é
  automaticamente uma conclusão do domínio.
- `conhecimento/` — conhecimento extraído e reconciliado (termos, regras, relações candidatas,
  conflitos, aliases). Cada elemento tem `estado_epistemologico` (seção 4.5).
- `candidatos/` — hipóteses estruturais ainda não promovidas ao Modelo Canônico. A existência de
  um candidato não significa validação — é exatamente o que `estagio=CANDIDATO` (seção 4.5)
  expressa no schema, e a localização física reforça isso.
- `dominio/` — só o que foi aceito para compor o Modelo Canônico (`estagio=DOMINIO`, o que o
  schema já exige vir com `estado_epistemologico=VALIDADO`, `promoted_from` e `promoted_by`
  preenchidos). Nenhum agente escreve aqui só porque encontrou uma estrutura numa fonte —
  promoção exige reconciliação prévia em `candidatos/`.
- `logico/` — derivação relacional do Modelo Canônico. Proibido derivar diretamente
  `fonte → logico/` ou `candidato → logico/`; só `dominio/` maduro (seção 4.4) entra aqui.
- `schemas/verificar_referencias.mjs` — valida 100% das referências cruzadas (`SRC→EVD→TERMO/REGRA→elementos→dominio→logico`), sem órfãos.
- `schemas/verificar_repositorio.mjs` — resolve `action_ref` para exatamente um commit real da branch da fase e verifica a imutabilidade de `main` por SHA antes/depois.


**Regra de promoção** — única direção permitida, sem pular etapa:

```text
.drive/CEPRAEA BEACH PRO/ → fontes/ → evidencias/ → conhecimento/ → candidatos/ → dominio/ → logico/
```

Promoção nunca é automática por simples existência na etapa anterior — precisa de reconciliação e
`estado_epistemologico` compatível, registrada como decisão (`SEM-NNN`, seção 4.9). Promoção
**não** é uma cópia que deixa duas versões igualmente válidas do mesmo elemento: o registro
original em `candidatos/*.md` muda para `estagio=PROMOVIDO` (histórico congelado, nunca mais
editado, `promoted_to` aponta para o destino) enquanto a nova entrada em `dominio/*.md` nasce
`estagio=DOMINIO` (`promoted_from`/`promoted_by` apontam de volta) — só essa é a versão ativa.

Existem exatamente duas rotas de entrada em `dominio/`:

```text
ROTA A — promoção normal
CANDIDATO --SEM-NNN--> PROMOVIDO + DOMINIO

ROTA B — PRE-SEED
REF + aprovação humana + AC-000 --> DOMINIO
```

Na ROTA A, `promoted_from` aponta para `candidatos/<arquivo>#<ID>`, o candidato fica `PROMOVIDO`, `promoted_to` aponta para `dominio/` e ambos registram o mesmo `SEM-NNN`. Na ROTA B, `promoted_by=PRE-SEED`, `promoted_from` começa por `REF:`, não existe candidato anterior e `approval_evidence` humana é obrigatória.


### 4.8 Namespaces de identificador

| Prefixo | Entidade | Schema |
|---|---|---|
| `SRC-NNN` | Fonte (identidade estável) | `schema_fonte.json.id_fonte` |
| `AC-NNN` | Ação de aquisição (processamento de uma fonte) | `schema_fonte.json.id_acao` |
| `EVD-NNNN` | Fragmento de evidência (4 dígitos — mais volume esperado que fontes) | `schema_evidencia.json` |
| `TERMO-NNN` | Termo/conceito do glossário | `schema_termo.json` |
| `REGRA-NNN` | Regra | `schema_regra.json` |
| `IDN-NNN` | Identidade definitiva | `schema_elemento_modelo.json` (`tipo=IDENTIDADE`) |
| `CTX-NNN` | Bounded Context | `schema_elemento_modelo.json` (`tipo=BOUNDED_CONTEXT`) |
| `INV-NNN` | Invariante | `schema_elemento_modelo.json` (`tipo=INVARIANTE`) |
| `LFC-NNN` | Ciclo de vida | `schema_elemento_modelo.json` (`tipo=CICLO_DE_VIDA`) |
| `AGG-NNN` | Agregado | `schema_elemento_modelo.json` (`tipo=AGREGADO`) |
| `TRX-NNN` | Fronteira transacional | `schema_elemento_modelo.json` (`tipo=FRONTEIRA_TRANSACIONAL`) |
| `DEC-NNN` | Decisão material | `schema_decisao.json` |

Todos permitem rastreabilidade cruzada — é a mesma cadeia da seção 4.3, agora com um prefixo por
elo: `SRC → EVD → TERMO/REGRA → IDN/CTX/INV/LFC/AGG/TRX (candidatos/ → dominio/) → logico/`.

### 4.9 Tipos de commit

Três tipos, não um só. "Uma ação = um dossiê = um commit" (seção 7) continua valendo só para
`AC-NNN`:

- **`AC-NNN`** — aquisição: processamento de uma fonte. Ex.: `AC-001 source: process SRC-001
  CEPRAEA Agosto 2026`.
- **`SEM-NNN`** — reconciliação semântica: quando uma conclusão vem de comparar múltiplas fontes,
  promove `candidatos/ → dominio/`, ou resolve `AMBIGUO`/`CONFLITANTE`. Ex.: `SEM-001 reconcile
  Pessoa and Atleta identity`, `SEM-002 formalize availability vs attendance invariant`. Decisões
  semânticas não ficam artificialmente presas ao commit do último arquivo processado — ganham
  commit próprio.
- **`SYN-NNN`** — síntese: consolidação do Modelo Canônico e derivação lógica. `AC-029` (seção 10)
  produz pelo menos um `SYN-NNN` (ex.: `SYN-001 consolidate canonical domain model`).

`AC-NNN`, `SEM-NNN` e `SYN-NNN` são **action refs**, não SHAs. O subject do commit correspondente deve começar exatamente por `<ACTION_REF> `; `verificar_repositorio.mjs` resolve a referência para o SHA real externamente. O SHA do próprio commit nunca é escrito dentro do artefato que esse commit contém.

`verificar_repositorio.mjs` exige para cada `action_ref`: exatamente um commit cujo subject comece por `<ACTION_REF> `, pertencente à branch da fase e posterior a `BASE_SHA`; falha em referência inexistente, duplicada ou ambígua.


**`SEM-NNN` não é exclusivo de `AC-029`.** Se, por exemplo, ao terminar `AC-010` já houver
evidência suficiente entre `AC-008`–`AC-010` para resolver uma identidade ambígua (é literalmente
o que AD-04 testa), o `SEM-NNN` correspondente roda ali mesmo, entre `AC-010` e `AC-011` — não
espera `AC-029`. `AC-029` reconcilia **o que sobrou**, não gera todas as decisões semânticas de
uma vez no fim ("big bang"). Isso mantém "uma ação = um dossiê = um commit" para `AC-NNN` e, ao
mesmo tempo, dá à reconciliação semântica o momento certo — assim que a evidência permite, não
artificialmente adiada nem artificialmente antecipada.

### 4.10 Regra de não regressão

O processo falha (BLOQUEADO, registrado em `decisoes/registro_decisoes.md`) se qualquer ação tentar
executar, sem os elos intermediários da cadeia de promoção:

```text
fonte → atributo canônico definitivo
fonte → tabela lógica
candidato não validado → modelo lógico
100% das fontes processadas → modelo lógico automaticamente pronto
```

O último caso é exatamente o que AD-06 (seção 8) testa. Cobertura documental (100% das entradas em estado terminal)
e maturidade semântica (seção 4.4) são métricas independentes — uma nunca substitui a outra.

### 4.11 Invariantes executáveis do próprio processo

- `INV-PROC-001` — fonte nunca determina diretamente tabela lógica.
- `INV-PROC-002` — elemento não `VALIDADO` nunca entra em `dominio/`.
- `INV-PROC-003` — elemento `DOMINIO` normal possui candidato `PROMOVIDO` correspondente; a única exceção é `PRE-SEED` formalmente autorizado.
- `INV-PROC-004` — `PRE-SEED` exige `REF:` + aprovação humana + `repository_evidence.action_ref=AC-000`.
- `INV-PROC-005` — todo `action_ref` resolve para exatamente um commit real.
- `INV-PROC-006` — nenhum SHA do próprio commit é persistido dentro do artefato para provar aquele mesmo commit.
- `INV-PROC-007` — 100% de cobertura documental não implica maturidade semântica.
- `INV-PROC-008` — nenhum `CTX-NNN` com conflito estrutural pendente é `MADURA_PARA_MODELO_LOGICO`.
- `INV-PROC-009` — nenhum elemento lógico existe sem `derived_from[]`.
- `INV-PROC-010` — nenhuma escrita ocorre fora de `WRITE_SCOPE`.

Essas invariantes são verificadas pelo conjunto `validar.mjs`, `verificar_referencias.mjs`, `verificar_repositorio.mjs`, AD-01..AD-06 e revisão humana.


## 5. Schemas formais

### 5.1 `docs/modelagem/schemas/schema_fonte.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cepraea.local/schemas/schema_fonte.json",
  "title": "Registro de fonte (dossiê)",
  "type": "object",
  "required": [
    "id_fonte",
    "id_acao",
    "nome_arquivo_original",
    "hash_sha256",
    "caminho_local",
    "tipo_arquivo",
    "tipo_fonte",
    "autoridade_fonte",
    "proveniencia_fonte",
    "estado_fonte",
    "estado_processamento",
    "dado_sensivel_encontrado",
    "evidencia"
  ],
  "properties": {
    "id_fonte": {
      "type": "string",
      "pattern": "^SRC-[0-9]{3}$",
      "description": "Identidade canônica interna e estável da fonte (seção 4.8) — o que EvidenceFragment/elementos citam. Nesta fase, SRC-NNN compartilha o número de id_acao (1:1), mas são conceitos diferentes: SRC-NNN é a fonte em si; id_acao é a ação de processá-la (poderia, em tese, haver mais de uma ação sobre a mesma fonte no futuro)."
    },
    "id_acao": {
      "type": "string",
      "pattern": "^AC-[0-9]{3}$",
      "description": "Identificador da ação de aquisição (commit tipo AC-NNN, seção 4.8) que processou esta fonte. id_drive/hash/caminho/nome são identificadores/locators que apontam para o arquivo; nem id_acao nem id_fonte dependem deles."
    },
    "nome_arquivo_original": {
      "type": "string",
      "minLength": 1
    },
    "caminho_local": {
      "type": "string",
      "minLength": 1,
      "description": "Caminho do arquivo dentro de .drive/CEPRAEA BEACH PRO/ — locator, sempre obtível."
    },
    "hash_sha256": {
      "type": [
        "string",
        "null"
      ],
      "pattern": "^[a-f0-9]{64}$",
      "description": "Locator de conteúdo. Null apenas para fonte ausente/bloqueada; CONCLUIDO exige hash válido."
    },
    "id_drive": {
      "type": [
        "string",
        "null"
      ],
      "description": "Locator preferencial quando obtível (nem sempre está — sem acesso à API do Drive neste ambiente, alguns arquivos não têm ID recuperável). Ausência de id_drive NÃO bloqueia sozinha — só bloqueia se, mesmo com hash_sha256+caminho_local+nome_arquivo_original, a identidade da fonte permanecer ambígua (ex.: colisão de nome real, seção 9)."
    },
    "tipo_arquivo": {
      "enum": [
        "docx",
        "xlsx",
        "pdf",
        "txt"
      ]
    },
    "idioma": {
      "enum": [
        "pt-BR",
        "en",
        "outro"
      ]
    },
    "tipo_fonte": {
      "enum": [
        "NORMATIVA",
        "OPERACIONAL",
        "CIENTIFICA",
        "ADMINISTRATIVA",
        "TECNICA",
        "INDETERMINADO"
      ],
      "description": "Gênero da fonte — modelagem_dominio_dados.md §16.1, com HISTORICA removido: temporalidade pertence só a estado_fonte (§16.4), não a este campo — evita reintroduzir a mistura gênero/temporalidade que o item 1 já corrigiu. INDETERMINADO é extensão própria (o canônico não previu esse caso), para não forçar uma classificação prematura quando o gênero ainda não está claro."
    },
    "autoridade_fonte": {
      "enum": [
        "OFICIAL",
        "PRIMARIA",
        "AUXILIAR",
        "INDETERMINADA"
      ],
      "description": "modelagem_dominio_dados.md §16.2."
    },
    "proveniencia_fonte": {
      "enum": [
        "ORIGINAL",
        "DERIVADA",
        "INDETERMINADA"
      ],
      "description": "ORIGINAL/DERIVADA vêm de modelagem_dominio_dados.md §16.3; INDETERMINADA é extensão própria, mesma justificativa de tipo_fonte."
    },
    "estado_fonte": {
      "enum": [
        "VIGENTE",
        "SUBSTITUIDA",
        "OBSOLETA",
        "INDETERMINADA"
      ],
      "description": "Ciclo de vida da fonte — modelagem_dominio_dados.md §16.4. Substitui o enum anterior (VIGENTE/COMPLEMENTAR/SUBSTITUIDA/HISTORICA/EM_VERIFICACAO): COMPLEMENTAR virou autoridade_fonte=AUXILIAR; EM_VERIFICACAO já é coberto por estado_processamento (workflow, não propriedade da fonte)."
    },
    "estado_processamento": {
      "enum": [
        "NAO_INICIADO",
        "EM_EXECUCAO",
        "BLOQUEADO",
        "CONCLUIDO",
        "NAO_APLICAVEL"
      ]
    },
    "dado_sensivel_encontrado": {
      "type": "boolean"
    },
    "tratamento_dado_sensivel": {
      "type": [
        "string",
        "null"
      ]
    },
    "conceitos_encontrados": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "regras_encontradas": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "conflitos_ou_duvidas": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "evidencia": {
      "type": "object",
      "description": "Prova verificável de que a ação foi de fato executada, não apenas descrita.",
      "required": [
        "comando_ou_metodo",
        "resultado"
      ],
      "properties": {
        "comando_ou_metodo": {
          "type": "string",
          "minLength": 1,
          "description": "Comando ou passo literal executado, ex.: 'perl -MIO::Uncompress::Unzip=unzip ...' ou 'Read direto do arquivo'."
        },
        "resultado": {
          "type": "string",
          "minLength": 1,
          "description": "Trecho literal do resultado, contagem de linhas/abas, ou hash — nunca um resumo vago como 'ok'."
        },
        "repository_evidence": {
          "type": "object",
          "properties": {
            "action_ref": {
              "type": "string",
              "pattern": "^AC-[0-9]{3}$"
            }
          }
        },
        "limitacoes": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "O que não pôde ser verificado, se houver."
        }
      }
    },
    "proxima_acao": {
      "type": [
        "string",
        "null"
      ]
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "dado_sensivel_encontrado": {
            "const": true
          }
        }
      },
      "then": {
        "required": [
          "tratamento_dado_sensivel"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "estado_processamento": {
            "const": "CONCLUIDO"
          }
        }
      },
      "then": {
        "properties": {
          "hash_sha256": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$"
          },
          "evidencia": {
            "properties": {
              "repository_evidence": {
                "type": "object",
                "properties": {
                  "action_ref": {
                    "type": "string",
                    "pattern": "^AC-[0-9]{3}$"
                  }
                },
                "required": [
                  "action_ref"
                ]
              }
            },
            "required": [
              "repository_evidence"
            ]
          }
        }
      }
    }
  ]
}
```

Regra complementar aplicada por `validar.mjs`: quando `estado_processamento=CONCLUIDO`, `hash_sha256` deve ser string válida de 64 caracteres, `caminho_local` deve estar preenchido e `evidencia.repository_evidence.action_ref` deve ser igual a `id_acao`. Quando a fonte está ausente e `BLOQUEADO`, `hash_sha256=null` é permitido.

### 5.2 `docs/modelagem/schemas/schema_decisao.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cepraea.local/schemas/schema_decisao.json",
  "title": "Registro de decisão material",
  "type": "object",
  "required": [
    "id_decisao",
    "data",
    "decisao",
    "escolha",
    "justificativa",
    "fonte",
    "aprovador",
    "estado"
  ],
  "properties": {
    "id_decisao": {
      "type": "string",
      "pattern": "^DEC-[0-9]{3}$"
    },
    "data": {
      "type": "string",
      "format": "date"
    },
    "decisao": {
      "type": "string",
      "minLength": 1
    },
    "alternativas": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "escolha": {
      "type": "string",
      "minLength": 1
    },
    "justificativa": {
      "type": "string",
      "minLength": 1
    },
    "fonte": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "impacto": {
      "type": [
        "string",
        "null"
      ]
    },
    "riscos": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "aprovador": {
      "type": "string",
      "enum": [
        "Davi Sermenho",
        "PENDENTE"
      ]
    },
    "estado": {
      "enum": [
        "BLOQUEADO",
        "RESOLVIDA",
        "REGISTRADA_SEM_ACAO"
      ]
    },
    "evidencia": {
      "type": "object",
      "description": "Prova verificável de registro/aplicação da decisão, sem SHA autorreferencial.",
      "properties": {
        "repository_evidence": {
          "type": "object",
          "properties": {
            "action_ref": {
              "type": "string",
              "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
            }
          }
        }
      }
    }
  },
  "if": {
    "properties": {
      "estado": {
        "const": "RESOLVIDA"
      }
    }
  },
  "then": {
    "properties": {
      "aprovador": {
        "const": "Davi Sermenho"
      },
      "fonte": {
        "minItems": 1
      },
      "evidencia": {
        "properties": {
          "repository_evidence": {
            "type": "object",
            "properties": {
              "action_ref": {
                "type": "string",
                "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
              }
            },
            "required": [
              "action_ref"
            ]
          }
        },
        "required": [
          "repository_evidence"
        ]
      }
    },
    "required": [
      "evidencia"
    ]
  }
}
```

### 5.3 Validação mecânica dos schemas e das referências

Os schemas declaram `"$schema": "https://json-schema.org/draft/2020-12/schema"`, mas esta fase **não depende de instalar uma biblioteca externa** para ser executável. `docs/modelagem/schemas/validar.mjs` valida instâncias contra o subconjunto de JSON Schema efetivamente usado neste projeto:

```text
type
required
properties
items
enum
const
pattern
minLength
minItems
allOf
if
then
format=date
```

Regra de segurança: se qualquer schema passar a utilizar uma keyword fora desse subconjunto, `validar.mjs` **falha explicitamente**; nunca ignora silenciosamente uma keyword desconhecida. O script não se declara um validador JSON Schema genérico nem afirma validar o meta-schema oficial. Uma dependência como AJV pode ser adicionada futuramente como melhoria independente, mas **não é necessária para executar este plano**.

Além dele, `AC-000` cria:

- `verificar_referencias.mjs` — verifica 100% das referências semânticas e estruturais, sem órfãos;
- `verificar_repositorio.mjs` — resolve `action_ref` para commit real e verifica branch/base/main;
- `schemas/fixtures/manifest.json` — fonte única da expectativa de todas as fixtures.

### 5.4 Por que validação estrutural não basta — testes de instância dos schemas

Validar contra o meta-schema (seção 5.3, com `ajv` ou com `validar.mjs`) prova só conformidade
estrutural/sintática — que o documento é um JSON Schema bem-formado e utilizável. Não prova
correção semântica (que o schema captura corretamente as regras de negócio das melhorias a-f).
Isso exige revisão humana e testes de instância direcionados: casos válidos e inválidos
representativos do domínio, verificando que o schema aceita o que deveria aceitar e rejeita o que
deveria rejeitar. Nenhuma ferramenta de meta-schema garante isso sozinha.

Fixtures obrigatórias, criadas em `AC-000` — `validar.mjs` só é confiável para os 28 dossiês reais
depois de passar nelas:

| Arquivo em `schemas/fixtures/` | Esperado | O que testa |
|---|---|---|
| `fonte_valida_concluida.json` | aceito | dossiê completo, `CONCLUIDO`, `hash_sha256`/`caminho_local` preenchidos, `evidencia.repository_evidence.action_ref` preenchido, `id_drive=null` (permitido — seção 4/5.1) |
| `fonte_valida_bloqueada.json` | aceito | `BLOQUEADO` sem `repository_evidence` (permitido nesse estado) |
| `fonte_invalida_sem_hash.json` | rejeitado | falta `hash_sha256` — deve falhar por `required` (identidade real, não `id_drive`) |
| `fonte_invalida_sem_evidencia.json` | rejeitado | falta `evidencia` — deve falhar por `required` |
| `fonte_invalida_sensivel_sem_tratamento.json` | rejeitado | `dado_sensivel_encontrado=true` sem `tratamento_dado_sensivel` — regra `if/then` da melhoria b |
| `decisao_valida_bloqueada.json` | aceito | `estado=BLOQUEADO`, `fonte=[]`, `aprovador=PENDENTE` (permitido) |
| `decisao_invalida_resolvida_sem_aprovador.json` | rejeitado | `estado=RESOLVIDA` com `aprovador=PENDENTE` — melhoria f |
| `decisao_invalida_resolvida_fonte_vazia.json` | rejeitado | `estado=RESOLVIDA` com `fonte=[]` — regra `minItems` |
| `evidencia_valida.json` | aceito | `EVD-NNNN` com `localizacao`/`trecho_literal` específicos (não "o arquivo inteiro") |
| `evidencia_invalida_sensivel_sem_tratamento.json` | rejeitado | `dado_sensivel_encontrado=true` sem `tratamento_dado_sensivel` — mesma regra da melhoria b, aplicada a fragmentos |
| `termo_valido_observado.json` | aceito | `fonte=["EVD-0001"]`, `estado_epistemologico=OBSERVADO`, `estado_tecnico=NAO_MODELADO` |
| `termo_invalido_modelado_sem_validacao.json` | rejeitado | `estado_tecnico=MODELADO` com `estado_epistemologico=INFERIDO` — regra `if/then` da seção 5.5 |
| `termo_invalido_fonte_ac_bruto.json` | rejeitado | `fonte=["AC-001"]` em vez de `EVD-NNNN` — viola o `pattern` do item (ponto 5 da revisão: arquivo inteiro não é evidência) |
| `termo_invalido_validado_sem_aprovador.json` | rejeitado | `estado_epistemologico=VALIDADO` com `evidencia.approval_evidence.aprovador=PENDENTE` — regra `if/then` nova (ponto 7 da revisão) |
| `regra_valida_observada.json` | aceito | `fonte=["EVD-0002"]`, `sujeito`/`acao` preenchidos, `estado_epistemologico=OBSERVADO` |
| `regra_invalida_sem_sujeito_acao.json` | rejeitado | falta `sujeito`/`acao` — deve falhar por `required` |
| `regra_invalida_validada_sem_aprovador.json` | rejeitado | `estado_epistemologico=VALIDADO` sem `evidencia.approval_evidence.aprovador="Davi Sermenho"` — regra `if/then` da seção 5.6 |
| `elemento_valido_bc.json` | aceito | `tipo=BOUNDED_CONTEXT`, `estagio=CANDIDATO`, `maturidade=IMATURA`, `fonte=["EVD-0003"]` |
| `elemento_invalido_bc_sem_maturidade.json` | rejeitado | `tipo=BOUNDED_CONTEXT` sem `maturidade` — regra `if/then` da seção 4.5 |
| `elemento_invalido_validado_sem_aprovador.json` | rejeitado | `estado_epistemologico=VALIDADO` sem `approval_evidence.aprovador="Davi Sermenho"` — mesma regra do termo, aplicada aos seis objetos |
| `elemento_invalido_dominio_sem_validacao.json` | rejeitado | `estagio=DOMINIO` com `estado_epistemologico=OBSERVADO` — regra `if/then` da seção 4.5/4.7: só entra em `dominio/` o que já é `VALIDADO` |
| `elemento_invalido_dominio_sem_promocao.json` | rejeitado | `estagio=DOMINIO`, `estado_epistemologico=VALIDADO`, mas sem `promoted_from`/`promoted_by` — toda entrada em `dominio/` segue promoção `SEM-NNN` ou `PRE-SEED` formal |
| `elemento_invalido_promovido_sem_destino.json` | rejeitado | `estagio=PROMOVIDO` sem `promoted_to` — o registro histórico em `candidatos/` tem que apontar para onde foi promovido |
| `fonte_valida_bloqueada_ausente_sem_hash.json` | aceito | fonte ausente, `BLOQUEADO`, `hash_sha256=null`, identidade esperada e causa registradas |
| `fonte_invalida_concluida_sem_hash.json` | rejeitado | `CONCLUIDO` exige hash válido |
| `fonte_valida_concluida_com_action_ref.json` | aceito | `repository_evidence.action_ref=id_acao` |
| `fonte_invalida_concluida_sem_action_ref.json` | rejeitado | `CONCLUIDO` sem action_ref |
| `fonte_invalida_action_ref_divergente_de_id_acao.json` | rejeitado | `action_ref` de aquisição deve coincidir com `id_acao` |
| `decisao_valida_resolvida_com_action_ref.json` | aceito | decisão resolvida com aprovação e action_ref verificável |
| `decisao_invalida_resolvida_sem_action_ref.json` | rejeitado | decisão resolvida sem action_ref |
| `elemento_valido_preseed.json` | aceito | `PRE-SEED` com `REF:`, aprovação humana e `action_ref=AC-000` |
| `elemento_invalido_preseed_sem_ref.json` | rejeitado | `PRE-SEED` sem origem `REF:` |
| `elemento_invalido_preseed_sem_aprovacao.json` | rejeitado | `PRE-SEED` sem aprovação humana |
| `elemento_valido_promocao_sem.json` | aceito | promoção normal com candidato histórico e `SEM-NNN` |
| `elemento_invalido_promocao_sem_candidato.json` | rejeitado | `SEM-NNN` em domínio sem candidato correspondente |
| `elemento_invalido_promovido_sem_sem_ref.json` | rejeitado | candidato `PROMOVIDO` sem `promoted_by=SEM-NNN` |

Critério: `schemas/fixtures/manifest.json` declara **todas** as fixtures, o resultado esperado (`ACCEPT`/`REJECT`) e, para rejeições, um `expected_reason`. `validar.mjs` executa o manifest e reporta dinamicamente `total`, `accept_expected`, `reject_expected`, `passed` e `failed`; nenhuma contagem é duplicada manualmente no plano. Todas as fixtures devem produzir exatamente o resultado e o motivo declarados no manifest antes de qualquer dossiê real ser processado. Se qualquer fixture divergir, `AC-000` não está `CONCLUIDO`.

Isso continua sendo só o mínimo mecânico. A correção semântica completa — se as regras capturadas
são as regras de negócio certas, não só regras que passam nas fixtures — continua sendo
revisão sua; nenhum teste automatizado deste plano substitui isso.

### 5.5 `docs/modelagem/schemas/schema_termo.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cepraea.local/schemas/schema_termo.json",
  "title": "Registro de termo do glossário (glossario.md) — só significado, não modelo conceitual",
  "type": "object",
  "required": [
    "id_termo",
    "termo_preferencial",
    "nome_canonico",
    "classificacao",
    "definicao",
    "fonte",
    "estado_epistemologico",
    "estado_tecnico",
    "evidencia"
  ],
  "properties": {
    "id_termo": {
      "type": "string",
      "pattern": "^TERMO-[0-9]{3}$"
    },
    "termo_preferencial": {
      "type": "string",
      "minLength": 1
    },
    "nome_canonico": {
      "type": "string",
      "minLength": 1
    },
    "classificacao": {
      "enum": [
        "ENTIDADE",
        "ATRIBUTO",
        "VALOR_OBJETO",
        "PAPEL",
        "ASSOCIACAO",
        "EVENTO",
        "ESTADO",
        "REGRA",
        "FATO_HISTORICO",
        "PROJECAO",
        "INDICADOR",
        "CATALOGO",
        "SNAPSHOT"
      ],
      "description": "União das três taxonomias-fonte, nenhuma delas se declarou substituta da outra: Fluxo de Modelagem Guia 1 §5, Fluxo de Modelagem Guia 2 §3.2, modelagem_dominio_dados.md §8."
    },
    "definicao": {
      "type": "string",
      "minLength": 1
    },
    "contexto_valido": {
      "type": [
        "string",
        "null"
      ]
    },
    "contexto_invalido": {
      "type": [
        "string",
        "null"
      ]
    },
    "inclusoes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "exclusoes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "sinonimos": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "termos_relacionados": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "fonte": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^EVD-[0-9]{4}$"
      },
      "minItems": 1,
      "description": "Fragmentos de evidência (EVD-NNNN, seção 4.5) que sustentam este termo — nunca AC-NNN bruto (um arquivo inteiro não é evidência de um conceito) nem só o nome do arquivo (melhoria a)."
    },
    "valores_permitidos": {
      "type": [
        "string",
        "null"
      ]
    },
    "temporalidade": {
      "type": [
        "string",
        "null"
      ]
    },
    "natureza_e_privacidade": {
      "type": [
        "string",
        "null"
      ]
    },
    "ativos_tecnicos": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "estado_epistemologico": {
      "enum": [
        "OBSERVADO",
        "INFERIDO",
        "AMBIGUO",
        "CONFLITANTE",
        "VALIDADO",
        "REJEITADO"
      ],
      "description": "modelagem_dominio_dados.md §17. Nunca promovido automaticamente para VALIDADO — exige autoridade humana adequada (ver evidencia.approval_evidence abaixo)."
    },
    "estado_tecnico": {
      "enum": [
        "NAO_MODELADO",
        "MODELADO",
        "IMPLEMENTADO",
        "TESTADO",
        "ATIVO",
        "SUBSTITUIDO"
      ],
      "description": "modelagem_dominio_dados.md §18 — dimensão separada do estado epistemológico ('VALIDADO ≠ IMPLEMENTADO'). Nesta fase só NAO_MODELADO/MODELADO são alcançáveis; IMPLEMENTADO/TESTADO/ATIVO pertencem ao modelo físico (fora de escopo, seção 3)."
    },
    "limitacoes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "evidencia": {
      "type": "object",
      "description": "Quatro eixos separados — action_ref prova vínculo com uma ação versionada; não prova significado correto.",
      "required": [
        "source_evidence"
      ],
      "properties": {
        "source_evidence": {
          "type": "object",
          "required": [
            "comando_ou_metodo",
            "resultado"
          ],
          "properties": {
            "comando_ou_metodo": {
              "type": "string",
              "minLength": 1
            },
            "resultado": {
              "type": "string",
              "minLength": 1
            },
            "limitacoes": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "semantic_evidence": {
          "type": [
            "string",
            "null"
          ],
          "description": "Por que esta interpretação é a correta — o raciocínio, não só o método de extração."
        },
        "approval_evidence": {
          "type": "object",
          "properties": {
            "aprovador": {
              "type": "string",
              "enum": [
                "Davi Sermenho",
                "PENDENTE"
              ]
            },
            "data": {
              "type": [
                "string",
                "null"
              ],
              "format": "date"
            }
          }
        },
        "repository_evidence": {
          "type": "object",
          "properties": {
            "action_ref": {
              "type": "string",
              "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
            }
          }
        }
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "estado_tecnico": {
            "enum": [
              "MODELADO",
              "IMPLEMENTADO",
              "TESTADO",
              "ATIVO",
              "SUBSTITUIDO"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        }
      },
      "then": {
        "properties": {
          "evidencia": {
            "properties": {
              "semantic_evidence": {
                "type": "string",
                "minLength": 1
              },
              "approval_evidence": {
                "type": "object",
                "properties": {
                  "aprovador": {
                    "const": "Davi Sermenho"
                  },
                  "data": {
                    "type": "string",
                    "format": "date"
                  }
                },
                "required": [
                  "aprovador",
                  "data"
                ]
              },
              "repository_evidence": {
                "type": "object",
                "properties": {
                  "action_ref": {
                    "type": "string",
                    "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
                  }
                },
                "required": [
                  "action_ref"
                ]
              }
            },
            "required": [
              "semantic_evidence",
              "approval_evidence",
              "repository_evidence"
            ]
          }
        },
        "required": [
          "evidencia"
        ]
      }
    }
  ]
}
```

A primeira regra `allOf` é extensão própria, não texto literal do canônico — é a consequência
direta de combinar duas frases que os documentos afirmam separadamente ("nunca promover
INFERIDO/AMBÍGUO/CONFLITANTE a VALIDADO automaticamente" + "VALIDADO ≠ IMPLEMENTADO"): um termo
só pode começar a virar modelo lógico (`estado_tecnico` além de `NAO_MODELADO`) depois de
`estado_epistemologico=VALIDADO`, nunca antes. A terceira regra fecha a lacuna do ponto 7 da sua
revisão: `VALIDADO` agora exige aprovação humana registrada **e** commit, não só commit.

### 5.6 `docs/modelagem/schemas/schema_regra.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cepraea.local/schemas/schema_regra.json",
  "title": "Registro de regra extraída",
  "type": "object",
  "required": [
    "id_regra",
    "fonte",
    "tipo",
    "sujeito",
    "acao",
    "estado_epistemologico",
    "estado_tecnico",
    "evidencia"
  ],
  "properties": {
    "id_regra": {
      "type": "string",
      "pattern": "^REGRA-[0-9]{3}$"
    },
    "fonte": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^EVD-[0-9]{4}$"
      },
      "minItems": 1,
      "description": "Fragmentos de evidência (EVD-NNNN, seção 4.5) — cada um já carrega a localização exata (página/seção/célula); não AC-NNN bruto."
    },
    "texto_original": {
      "type": [
        "string",
        "null"
      ],
      "description": "Preservado literalmente quando a redação for material (Guia 1 §4)."
    },
    "tipo": {
      "enum": [
        "DEFINICAO",
        "OBRIGACAO",
        "PROIBICAO",
        "PERMISSAO",
        "CONDICAO",
        "EXCECAO",
        "CLASSIFICACAO",
        "CALCULO",
        "REGRA_TEMPORAL",
        "CARDINALIDADE",
        "UNICIDADE",
        "AUTORIZACAO",
        "TRANSICAO_DE_ESTADO"
      ],
      "description": "União de Fluxo de Modelagem Guia 1 §4 e modelagem_dominio_dados.md §20 (atomização de regras) — nenhum dos dois se declarou substituto do outro."
    },
    "sujeito": {
      "type": "string",
      "minLength": 1
    },
    "acao": {
      "type": "string",
      "minLength": 1
    },
    "objeto": {
      "type": [
        "string",
        "null"
      ]
    },
    "condicoes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "excecoes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "cardinalidade_minima": {
      "type": [
        "string",
        "null"
      ]
    },
    "cardinalidade_maxima": {
      "type": [
        "string",
        "null"
      ]
    },
    "vigencia": {
      "type": [
        "string",
        "null"
      ]
    },
    "contexto_valido": {
      "type": [
        "string",
        "null"
      ]
    },
    "contexto_invalido": {
      "type": [
        "string",
        "null"
      ]
    },
    "conceitos_afetados": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "implementacao_candidata": {
      "type": [
        "string",
        "null"
      ]
    },
    "estado_epistemologico": {
      "enum": [
        "OBSERVADO",
        "INFERIDO",
        "AMBIGUO",
        "CONFLITANTE",
        "VALIDADO",
        "REJEITADO"
      ],
      "description": "modelagem_dominio_dados.md §17 — substitui a escada específica EXTRAÍDA/VERIFICADA/VALIDADA/REJEITADA do Guia 1 §4, para usar um único vocabulário epistemológico em todo o plano (termos, regras e os seis objetos da seção 4.1)."
    },
    "estado_tecnico": {
      "enum": [
        "NAO_MODELADO",
        "MODELADO",
        "IMPLEMENTADO",
        "TESTADO",
        "ATIVO",
        "SUBSTITUIDO"
      ]
    },
    "duvidas": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "evidencia": {
      "type": "object",
      "description": "Quatro eixos separados — action_ref prova vínculo com uma ação versionada; não prova significado correto.",
      "required": [
        "source_evidence"
      ],
      "properties": {
        "source_evidence": {
          "type": "object",
          "required": [
            "comando_ou_metodo",
            "resultado"
          ],
          "properties": {
            "comando_ou_metodo": {
              "type": "string",
              "minLength": 1
            },
            "resultado": {
              "type": "string",
              "minLength": 1
            },
            "limitacoes": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "semantic_evidence": {
          "type": [
            "string",
            "null"
          ]
        },
        "approval_evidence": {
          "type": "object",
          "properties": {
            "aprovador": {
              "type": "string",
              "enum": [
                "Davi Sermenho",
                "PENDENTE"
              ]
            },
            "data": {
              "type": [
                "string",
                "null"
              ],
              "format": "date"
            }
          }
        },
        "repository_evidence": {
          "type": "object",
          "properties": {
            "action_ref": {
              "type": "string",
              "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
            }
          }
        }
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "estado_tecnico": {
            "enum": [
              "MODELADO",
              "IMPLEMENTADO",
              "TESTADO",
              "ATIVO",
              "SUBSTITUIDO"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "estado_epistemologico": {
            "const": "VALIDADO"
          }
        }
      },
      "then": {
        "properties": {
          "evidencia": {
            "properties": {
              "semantic_evidence": {
                "type": "string",
                "minLength": 1
              },
              "approval_evidence": {
                "type": "object",
                "properties": {
                  "aprovador": {
                    "const": "Davi Sermenho"
                  },
                  "data": {
                    "type": "string",
                    "format": "date"
                  }
                },
                "required": [
                  "aprovador",
                  "data"
                ]
              },
              "repository_evidence": {
                "type": "object",
                "properties": {
                  "action_ref": {
                    "type": "string",
                    "pattern": "^(AC|SEM|SYN)-[0-9]{3}$"
                  }
                },
                "required": [
                  "action_ref"
                ]
              }
            },
            "required": [
              "semantic_evidence",
              "approval_evidence",
              "repository_evidence"
            ]
          }
        },
        "required": [
          "evidencia"
        ]
      }
    }
  ]
}
```

## 6. Estrutura de arquivos (escolhas fixadas, não perguntas)

A árvore completa e autoritativa é a da seção 4.7 (hierarquia `processo/`/`fontes/`/`evidencias/`/
`conhecimento/`/`candidatos/`/`dominio/`/`logico/`/`decisoes/`/`schemas/`, dentro de
`docs/modelagem/` na branch dedicada `feat/cepraea-domain-modeling` — worktree irmã removida por
`DEC-008`). Esta seção só resume o mapeamento arquivo → schema, para não duplicar a árvore em dois
lugares e arriscar divergência:

| Arquivo | Diretório (seção 4.7) | Formato | Schema |
|---|---|---|---|
| `inventario_fontes.md` | `fontes/` | tabela mestra das 28 entradas | — |
| `dossies/<slug>.md` | `fontes/dossies/` | 1 por fonte (28 no total) | `schema_fonte.json` |
| `registro_evidencias.md` | `evidencias/` | 1 bloco `json` por `EVD-NNNN` | `schema_evidencia.json` |
| `glossario.md` | `conhecimento/` | 1 bloco `json` por `TERMO-NNN` | `schema_termo.json` |
| `registro_regras.md` | `conhecimento/` | 1 bloco `json` por `REGRA-NNN` | `schema_regra.json` |
| `identidades.md`, `bounded_contexts.md`, `invariantes.md`, `ciclos_de_vida.md`, `agregados.md`, `fronteiras_transacionais.md` | `candidatos/` (`estagio=CANDIDATO`) | 1 bloco `json` por elemento | `schema_elemento_modelo.json` |
| `identidades_definitivas.md`, `bounded_contexts.md`, `invariantes.md`, `ciclos_de_vida.md`, `agregados.md`, `fronteiras_transacionais.md` | `dominio/` (`estagio=DOMINIO`) | idem, só promovidos | `schema_elemento_modelo.json` |
| `modelo_canonico_dominio.md` | `dominio/` | síntese por `CTX-NNN` (seção 4.6) | — |
| `modelo_logico_relacional.md` | `logico/` | só `CTX-NNN` `MADURA_PARA_MODELO_LOGICO` | — |
| `areas_pendentes.md` | `logico/` | `CTX-NNN` `IMATURA`/`PARCIALMENTE_MADURA` e por quê | — |
| `registro_decisoes.md` | `decisoes/` | 1 bloco `json` por `DEC-NNN` | `schema_decisao.json` |

Contratos adicionais:

- cada elemento em `logico/modelo_logico_relacional.md` registra `bounded_context_id` e `derived_from[]` com IDs canônicos que justificam a derivação;
- cada entrada de `logico/areas_pendentes.md` registra `CTX-NNN`, `maturidade`, `blocking_ids[]`, `blocking_reason` e `required_resolution`.


Regra de slug (dossiês e demais arquivos por fonte): transliteração literal do nome original
(minúsculas, espaço/pontuação → `_`, sem acentos) + extensão + `.md`. Mecânica, não por
julgamento — evita o mesmo erro que gerou a colisão `CEPRAEA 2026*.xlsx`. Um arquivo por fonte
nos dossiês (diff pequeno, exigido pelo AGENT_POLICY para risco não-verde); um arquivo único por
tipo nos demais diretórios (cada um só é legível como conjunto coerente).

## 7. Definição formal de ação — usada para todas as 28 entradas de fonte

Toda ação de dossiê (`AC-NNN`) segue este template único. Não repito a especificação inteira 28
vezes — a tabela da seção 10 só varia arquivo, ordem, tipo/autoridade/proveniência hipotéticos e
particularidade.

**Critério de aceitação como dado:** a entrada correspondente em `fontes/inventario_fontes.md` e o
dossiê em `fontes/dossies/<slug>.md` (front matter) validam contra `schema_fonte.json` (seção 5.1),
checado por `schemas/validar.mjs`. Todo fragmento novo em `evidencias/registro_evidencias.md`
valida contra `schema_evidencia.json` (seção 4.5); todo termo novo/atualizado em
`conhecimento/glossario.md` valida contra `schema_termo.json` (seção 5.5); toda regra
nova/atualizada em `conhecimento/registro_regras.md` valida contra `schema_regra.json` (seção
5.6); todo elemento novo/atualizado nos seis arquivos da seção 4.1
valida contra `schema_elemento_modelo.json` (seção 4.5) — mesma ferramenta, mesma exigência.

**Critério de aceitação em BDD:**

```gherkin
Funcionalidade: Registro de dossiê por fonte

  Cenário: Dossiê aceito
    Dado um arquivo real listado em .drive/CEPRAEA BEACH PRO/
    Quando o dossiê docs/modelagem/fontes/dossies/<slug>.md é escrito
    Então o dossiê valida contra schema_fonte.json
    E nenhum valor classificado como sensível aparece de forma literal no dossiê
    E todo item de conceitos_encontrados/regras_encontradas existe em
      conhecimento/glossario.md ou conhecimento/registro_regras.md, cada um com fonte em
      EVD-NNNN (não AC-NNN bruto)
    E todo candidato a Bounded Context/identidade/agregado/invariante/ciclo de vida/fronteira
      transacional encontrado na fonte está registrado como elemento em candidatos/*.md
      (schema_elemento_modelo.json, seção 4.5), com fonte em EVD-NNNN apontando para este AC-NNN
    E estado_processamento é CONCLUIDO ou BLOQUEADO com justificativa em conflitos_ou_duvidas

  Cenário: id_drive ausente não bloqueia sozinho
    Dado um arquivo cujo id_drive não pôde ser determinado, mas hash_sha256, caminho_local e
      nome_arquivo_original identificam a fonte sem ambiguidade
    Quando o dossiê é escrito
    Então id_drive permanece null
    E estado_processamento pode chegar a CONCLUIDO normalmente — id_drive é locator, não
      identidade (seção 4/5.1)

  Cenário: Dossiê bloqueado por identidade genuinamente ambígua
    Dado um arquivo cujo nome colide com outro (ex.: CEPRAEA 2026*.xlsx) e cujo id_drive também
      não pôde ser determinado
    Quando o dossiê é escrito
    Então estado_processamento é BLOQUEADO até hash_sha256/caminho_local ou id_drive
      desambiguarem qual arquivo é qual
    E o dossiê NÃO avança para CONCLUIDO nesta rodada

  Cenário: Fonte tecnicamente completa não é promovida sem base
    Dado uma fonte que descreve a tentativa de modelagem anterior (D-02)
    Quando tipo_fonte, autoridade_fonte, proveniencia_fonte e estado_fonte são atribuídos
    Então autoridade_fonte é AUXILIAR e estado_fonte é SUBSTITUIDA, independente de a fonte
      conter SQL, schema ou DDL aparentemente prontos
```

**Checklist de evidência mínima (preencher o campo `evidencia` de toda ação, sem exceção):**

- [ ] Comando ou método executado registrado literalmente (não descrito de memória depois do fato).
- [ ] Resultado obtido registrado literalmente — trecho, contagem de linhas/abas ou hash —, nunca
      um resumo vago como "ok" ou "processado".
- [ ] Arquivo de saída (dossiê ou linha de registro) existe no caminho previsto na seção 6.
- [ ] `evidencia.repository_evidence.action_ref` preenchido antes do commit e igual a `id_acao`; o SHA real será resolvido depois por `verificar_repositorio.mjs`, evitando autorreferência.
- [ ] Limitações não verificadas listadas explicitamente em `evidencia.limitacoes`, se houver, em
      vez de omitidas silenciosamente.

Quando a ação registra uma decisão material em `decisoes/registro_decisoes.md`, a mesma checklist se
aplica ao objeto de decisão, mais: `fonte` não-vazio e `aprovador = "Davi Sermenho"` antes de
`estado=RESOLVIDA` — imposto por `schema_decisao.json` (seção 5.2), não apenas recomendado.

**Exemplo correto** (trecho de dossiê, campo de dado sensível):

```markdown
## Dados sensíveis
- Coluna "Senha" (aba Atletas, 18 linhas): valor em texto plano, mesmo valor repetido em todas
  as linhas. Classificação: CREDENCIAL. Valor não reproduzido aqui — ver DEC-005 (resultado de
  AD-02).
```

**Exemplo incorreto** (o que este processo proíbe):

```markdown
## Dados sensíveis
- Coluna "Senha": todas as atletas usam "cepraea2026".
```

O incorreto reproduz o valor literal da credencial dentro de um arquivo que vai para o Git —
exatamente o que a melhoria (b) e o campo `tratamento_dado_sensivel` existem para impedir.

**DONE de uma ação de dossiê:** `estado_processamento` em `CONCLUIDO` — o que exige
`evidencia.comando_ou_metodo`, `evidencia.resultado` e `evidencia.repository_evidence.action_ref` preenchidos,
schema válido, nenhum dado sensível transcrito — **ou** `BLOQUEADO` com uma entrada
correspondente em `decisoes/registro_decisoes.md` (com seu próprio `evidencia`/`fonte` preenchidos). Nunca
fica em `EM_EXECUCAO` entre commits — esse estado só existe durante a execução de um único
`AC-NNN`, nunca persiste de uma sessão para a próxima.

## 8. Casos adversariais

definidos agora;
ainda **não executados** — nenhuma ação de dossiê começou

Não registro um "resultado" de teste adversarial porque nada foi executado ainda — isso seria
inventar evidência, o que o guia de estilo e o próprio checklist proíbem explicitamente. O que
existe agora é o procedimento e o resultado esperado; o resultado real é registrado como decisão
material formal, com seu próprio `evidencia.repository_evidence.action_ref`, não como comentário solto no dossiê.

| ID | Ataque | Como será feito | Resultado esperado (correto) | Falha reconhecível | Registrado em |
|---|---|---|---|---|---|
| AD-01 | Fonte tecnicamente completa e persuasiva (`BancoCEPRAEA.docx`: 23 tabelas, DDL válido, texto técnico confiante) tentando ser promovida a fonte oficial/vigente | Processar o dossiê normalmente pelo template da seção 7, dentro de AC-002, e observar `tipo_fonte`/`autoridade_fonte`/`proveniencia_fonte`/`estado_fonte` atribuídos | `autoridade_fonte = AUXILIAR` e `estado_fonte = SUBSTITUIDA` (regra d), nunca `OFICIAL`/`PRIMARIA` nem `VIGENTE`; nenhum termo/elemento derivado dele passa de `OBSERVADO`/`INFERIDO` para `VALIDADO` sem confirmação independente e aprovação humana (seção 4.5) | Se `autoridade_fonte` sair `OFICIAL`/`PRIMARIA`, ou `estado_fonte` sair `VIGENTE`, ou algum termo/elemento virar `estado_epistemologico=VALIDADO`/`estado_tecnico` além de `NAO_MODELADO` só com essa fonte, o teste falhou — corrigir antes de continuar o lote | `DEC-004` em `decisoes/registro_decisoes.md`, `fonte` apontando para `AC-002` |
| AD-02 | Dado sensível real (coluna "Senha" de `CEPRAEA 2026(1).xlsx`) tentando vazar para o dossiê versionado | Processar o dossiê normalmente dentro de AC-008 e depois `grep` o valor literal conhecido da senha sobre `docs/modelagem/**` | `grep` não encontra o valor literal; `tratamento_dado_sensivel` está preenchido | Se o `grep` encontrar o valor, o teste falhou — remover do arquivo, corrigir o processo antes de commitar | `DEC-005` em `decisoes/registro_decisoes.md`, `fonte` apontando para `AC-008` |
| AD-03 | Cabeçalho de coluna de planilha (ex.: `AC-001`, `CEPRAEA AGOSTO 2026.xlsx`) tentando virar termo canônico só por existir | Processar AC-001 e conferir se cada `TERMO-NNN` novo em `conhecimento/glossario.md` tem `evidencia.semantic_evidence` preenchido com justificativa real, não só "existe uma coluna com esse nome" | Todo termo tem `semantic_evidence` explicando por que aquele dado corresponde a um conceito do domínio; nenhum termo nasce só por nome de coluna (antiobjetivo de `modelagem_dominio_dados.md` §37) | Termo em `conhecimento/glossario.md` sem `semantic_evidence`, ou com justificativa genérica que se aplicaria a qualquer coluna, o teste falhou | `DEC-007` em `decisoes/registro_decisoes.md`, `fonte` apontando para `AC-001` |
| AD-04 | Nomes de atleta com grafia variada nas planilhas de elenco (ex.: `AC-008`–`AC-010`) tentando virar a mesma identidade ou identidades diferentes só pela semelhança/diferença textual | Processar as fontes de elenco e conferir se `identidades_definitivas.md` (`schema_elemento_modelo.json`, `tipo=IDENTIDADE`) registra critérios de reconciliação explícitos para cada caso de grafia variada, em vez de decidir por semelhança de string | Casos genuinamente ambíguos ficam `estado_epistemologico=AMBIGUO`, registrados com a incerteza explícita — nunca mesclados nem separados por decisão silenciosa (`modelagem_dominio_dados.md` §11.1/§21) | Duas grafias da mesma pessoa tratadas como identidades diferentes sem registro de incerteza, ou vice-versa, o teste falhou | `DEC-008` em `decisoes/registro_decisoes.md`, `fonte` apontando para `AC-008`–`AC-010` |
| AD-05 | Dois termos com grafia diferente mas possível sobreposição semântica (ex.: "convocação" vs. termo equivalente encontrado em outra fonte) tentando virar dois conceitos definitivamente distintos sem análise | Ao encontrar termos candidatos com sobreposição de significado, conferir se `conhecimento/glossario.md` registra `sinonimos`/`termos_relacionados` antes de criar dois `TERMO-NNN` separados | Termos com sobreposição semântica ficam cross-referenciados ou `AMBIGUO` até reconciliação — nunca dois conceitos "definitivamente distintos" sem essa análise (antiobjetivo simétrico ao AD-04: `modelagem_dominio_dados.md` §37) | Dois `TERMO-NNN` cobrindo o mesmo conceito, sem `termos_relacionados` entre eles, o teste falhou | `DEC-009` em `decisoes/registro_decisoes.md` |
| AD-06 | **O mais importante.** 100% das entradas atingem estado terminal (`CONCLUIDO`, `BLOQUEADO` ou `NAO_APLICAVEL`) enquanto ainda restam termos/elementos `AMBIGUO`/`CONFLITANTE` não resolvidos, tentando ser lido como "pronto para modelo lógico" | Em `AC-029`, antes de escrever `logico/modelo_logico_relacional.md`: contar termos/elementos `AMBIGUO`/`CONFLITANTE` pendentes por Bounded Context e cruzar com a maturidade (seção 4.4) | Nenhum Bounded Context com pendência `AMBIGUO`/`CONFLITANTE` é classificado `MADURA_PARA_MODELO_LOGICO`; "100% das fontes processadas" não é tratado como sinônimo de "pronto para modelo lógico" | `logico/modelo_logico_relacional.md` contém entidade/relação derivada de um Bounded Context com `AMBIGUO`/`CONFLITANTE` pendente — mesmo com 100% das entradas em estado terminal, o teste falhou | `DEC-010` em `decisoes/registro_decisoes.md`, `fonte` apontando para `AC-029` |

## 9. Catálogo de edge cases

| Caso | Risco | Mitigação |
|---|---|---|
| Nomes de arquivo colidem (`CEPRAEA 2026*.xlsx`) | Confundir identidade de fontes | `hash_sha256`+`caminho_local` obrigatórios; `id_drive` quando obtível (melhoria a) |
| PDF ilegível com as ferramentas disponíveis | Fonte sem análise de conteúdo | `BLOQUEADO` com causa-raiz única; nunca simular conteúdo |
| Dado sensível (credencial, saúde) | Vazamento via Git | Melhoria b — nunca transcrever valor literal |
| Fonte tecnicamente completa mas não aprovada | Promover `autoridade_fonte`/`estado_fonte` indevidamente | Melhoria d, testada em AD-01 |
| Duas fontes autoritativas conflitantes | Escolha silenciosa | Melhoria c — `BLOQUEADO` imediato |
| Arquivo referenciado por outro documento mas ausente no disco | Dossiê baseado em suposição | `estado_processamento=BLOQUEADO`; nunca reconstruir conteúdo de memória (ver D-01) |
| Aba/planilha vazia ou só cabeçalho | Conceito inventado a partir do nome da coluna | Registrar ausência de fato observado; não criar termo sem exemplo real |
| Arquivo grande demais para leitura integral (`CEPRAEA.pdf`, 32,8 MB) | Leitura parcial tratada como cobertura total | Registrar explicitamente como amostra parcial |
| Extração falha silenciosamente (script quebra no meio) | Conteúdo truncado tratado como completo | Conferir exit code e tamanho da saída antes de aceitar como válida |
| Agente de execução escreve dentro de `.drive/**` | Perda de fonte original (ver D-01) | Melhoria e — scratch só fora de `.drive/` |

## 10. Ordem de execução

Todas as 28 entradas, começando por `CEPRAEA AGOSTO 2026.xlsx`
(sua instrução explícita)

Uma ação = um dossiê = um commit. "Ação" para toda linha de fonte é sempre "aplicar o
procedimento da seção 7"; a coluna Particularidade só registra o que muda por arquivo.

### 10.0 Sequência de IDs (ordem única, estritamente sequencial)

```text
AC-000 → AC-001 (+ AD-03 → DEC-007) → AC-002 (+ AD-01 → DEC-004) → AC-003 → AC-004 → AC-005
  → AC-006 → AC-007 → AC-008 → AC-009 → AC-010 (+ AD-02 → DEC-005; AD-04 → DEC-008) → AC-011
  → AC-012 → AC-013 → AC-014 → AC-015 → AC-016 → AC-017 → AC-018 → AC-019 → AC-020 → AC-021
  → AC-022 → AC-023 → AC-024 → AC-025 → AC-026 → AC-027 → AC-028 (+ AD-05 → DEC-009)
  → AC-029 (+ AD-06 → DEC-010)
```

Regras de sequenciamento, sem exceção:

- Estritamente sequencial por ID — nunca em paralelo. Só existe um agente escritor nesta branch
  (AGENT_POLICY.md), então `AC-(N+1)` não começa antes de `AC-N` atingir `CONCLUIDO`, `BLOQUEADO`
  ou `NAO_APLICAVEL`.
- Os seis testes adversariais não são passos à parte na sequência — cada um roda dentro do
  `AC-NNN` indicado acima (AD-02 permanece em `AC-008`, onde a coluna "Senha" de fato está — só a
  posição no diagrama que mudou, para ficar ao lado de AD-04, que usa a mesma família de fontes de
  elenco AC-008–AC-010) e só é considerado concluído quando sua entrada `DEC-00N` correspondente
  (seção 8) existir em `decisoes/registro_decisoes.md` com evidência real.
- Seis paradas obrigatórias na tabela abaixo (coluna Checkpoint = "Sim"): **AC-000, AC-002,
  AC-008, AC-018, AC-019, AC-029**. Nessas, não avanço para o próximo ID sem sua resposta.
  `AC-007` e `AC-021` deixaram de ser checkpoint — D-03 e a decisão sobre a cópia do Wellness já
  estão resolvidos (seção 0/14 removida).
- Se qualquer `AC-NNN` fora dessas oito encontrar algo que se enquadre nas condições de parada da
  seção 9 do checklist original (ex.: nova colisão de nome, novo dado sensível, nova fonte
  conflitante), essa linha vira checkpoint mesmo sem estar marcada como tal — a tabela abaixo é o
  mínimo, não o teto.
- O diagrama acima é a espinha dorsal de `AC-NNN` — não enumera onde `SEM-NNN` entra, porque isso
  depende da evidência real, não é previsível de antemão. Qualquer `SEM-NNN` que se tornar
  possível entre dois `AC-NNN` roda ali (seção 4.9), sem esperar `AC-029`.

Coluna de classificação: `tipo_fonte·autoridade_fonte·proveniencia_fonte`, todos hipóteses a
confirmar no dossiê (seção 5.1). `estado_fonte` nasce `INDETERMINADA` salvo quando uma decisão anterior explicitamente registrada já determine outro estado; `VIGENTE` só é atribuído após evidência suficiente — é o caso das seis fontes da tentativa anterior (D-02), que
nascem `SUBSTITUIDA`.

### 10.1 Critério de DONE do `AC-000` (bootstrap)

`AC-000` só está `CONCLUIDO` quando os itens abaixo forem verdadeiros:

1. `BASE_REF` registrado.
2. `BASE_SHA` registrado e existente.
3. `MAIN_SHA_BEFORE` registrado.
4. A branch `feat/cepraea-domain-modeling` existe no repositório `cepraea-beach-pro` e passou pelas guardas da seção 4.7 (worktree irmã removida por `DEC-008`).
5. A branch `feat/cepraea-domain-modeling` nasceu exatamente de `BASE_SHA`, não implicitamente de outra branch.
6. `CEPRAEA_SOURCE_ROOT` foi resolvido por caminho real, existe e as 27 fontes presentes são legíveis.
7. `READ_SCOPE` e `WRITE_SCOPE` estão registrados no `README.md`.
8. Toda a estrutura de diretórios da seção 4.7 existe.
9. Todos os arquivos-base estão inicializados sem conteúdo de domínio inventado.
10. Todos os schemas formais existem.
11. `validar.mjs` suporta todas as keywords de JSON Schema utilizadas e falha em keyword desconhecida.
12. `verificar_referencias.mjs` existe.
13. `verificar_repositorio.mjs` existe.
14. `schemas/fixtures/manifest.json` existe.
15. 100% das fixtures declaradas no manifest produzem o resultado e `expected_reason` esperados.
16. `INV-001` PRE-SEED valida pela rota excepcional (`REF:` + aprovação humana + `repository_evidence.action_ref=AC-000`).
17. `CTX-001`–`CTX-008` estão `estagio=CANDIDATO`, `estado_epistemologico=INFERIDO`, `maturidade=IMATURA`.
18. `DEC-006` está registrado com aprovação humana e `repository_evidence.action_ref=AC-000`.
19. `dominio/modelo_canonico_dominio.md` existe sem conteúdo inventado.
20. `logico/modelo_logico_relacional.md` existe vazio.
21. Nenhuma escrita ocorreu em `CEPRAEA_SOURCE_ROOT`.
22. O commit `AC-000 ...` existe e `verificar_repositorio.mjs` resolve `action_ref=AC-000` para exatamente um commit real da branch da fase.

| ID | Ordem | Arquivo | Tipo·Autoridade·Proveniência (hipótese) | Particularidade | Checkpoint |
|---|---|---|---|---|---|
| AC-000 | 0 | *(nenhum — bootstrap)* | — | Cria a branch dedicada e toda a hierarquia da seção 4.7 (worktree irmã removida por `DEC-008`) — critério completo de DONE na seção 10.1 (não é só "criar uns arquivos") | **Sim, antes do AC-001** |
| AC-001 | 1 | `CEPRAEA AGOSTO 2026.xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Início pedido por você; planilha mensal vigente (a mais recente por nome). Roda AD-03 aqui | Não |
| AC-002 | 2 | `BancoCEPRAEA.docx` | TÉCNICA·AUXILIAR·ORIGINAL | `estado_fonte=SUBSTITUIDA` (fixo por D-02). Roda AD-01 aqui | Sim — reporto resultado de AD-01 |
| AC-003 | 3 | `CEPRAEA-DB.docx` | TÉCNICA·AUXILIAR·ORIGINAL | `estado_fonte=SUBSTITUIDA` (D-02). Contém o inventário de 65 fontes de `BEACH HANDBALL` — só referenciar, não reprocessar (fora de escopo) | Não |
| AC-004 | 4 | `CEPRAEA DATABASE.xlsx` | OPERACIONAL·INDETERMINADA·INDETERMINADA | Testar a hipótese "é a fonte do schema de 13 tabelas do Glossário v0.2?" — registrar confirmação ou refutação, não presumir | Não |
| AC-005 | 5 | `DESC-CEPRAEA.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | `estado_fonte=SUBSTITUIDA` (D-02). Predecessor do REGISTRO MESTRE | Não |
| AC-006 | 6 | `Glossário de Dados — CEPRAEA v0.1.xlsx` | TÉCNICA·AUXILIAR·ORIGINAL | `estado_fonte=SUBSTITUIDA` (D-02). Já marcado SUPERSEDED pelo próprio REGISTRO MESTRE — herdar essa classificação, não reabrir | Não |
| AC-007 | 7 | `REGISTRO MESTRE DE ARTEFATOS E FUNCIONAMENTO — SISTEMA CEPRAEA.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | `estado_fonte=SUBSTITUIDA` (D-02, é parte da governança da tentativa anterior). Fonte de D-03 (já resolvido, seção 0) — reaproveitar os trechos já extraídos, não reanalisar | Não |
| AC-008 | 8 | `CEPRAEA 2026(1).xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Contém a coluna "Senha" em texto plano — roda AD-02 aqui | Sim — reporto resultado de AD-02 |
| AC-009 | 9 | `CEPRAEA 2026.xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Confirmar: artefato distinto de (1) e (2), não uma versão | Não |
| AC-010 | 10 | `CEPRAEA 2026(2).xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Idem. Roda AD-04 aqui (fecha a família de fontes de elenco AC-008–AC-010) | Não |
| AC-011 | 11 | `CEPRAEA_Preparacao_Competitiva_Ago_Set_2026.pdf` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | Canário de PDF — menor PDF da pasta; confirma se a limitação de ferramenta (sem poppler-utils) se aplica | Reporto resultado do canário |
| AC-012 | 12 | `CEPRAEA JULHO 2026.pdf` | OPERACIONAL·PRIMÁRIA·DERIVADA | Tentativa individual; se canário falhou, tentar mesmo assim e registrar | Não |
| AC-013 | 13 | `CEPRAEA_Preparacao_Competitiva_2026_CORRIGIDO.pdf` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | Idem; causa-raiz do bloqueio referencia AC-011, não repete a explicação | Não |
| AC-014 | 14 | `CEPRAEA_Preparacao_Competitiva_2026_FINAL_ACESSIVEL.pdf` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | Idem | Não |
| AC-015 | 15 | `CEPRAEA.pdf` (32,8 MB) | INDETERMINADO·INDETERMINADA·INDETERMINADA | Idem; se ilegível, registrar tamanho como fator agravante, não repetir análise de conteúdo | Não |
| AC-016 | 16 | `CEPRAEA ABRIL 2026.xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Comparar template com AC-001 (mesma família de planilha mensal) | Não |
| AC-017 | 17 | `Implementação — Pesquisa de Treinos CEPRAEA 2026.xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | — | Não |
| AC-018 | 18 | `# Autoavaliação – CEPRAEA.xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Conteúdo provável de autoavaliação/bem-estar — aplicar melhoria b preventivamente | Sim — checar sensibilidade antes de `CONCLUIDO` |
| AC-019 | 19 | `CEPRAEA — Wellness — Configuração e Respostas.xlsx` | OPERACIONAL·PRIMÁRIA·ORIGINAL | Dado provável de bem-estar/saúde | Sim — idem |
| AC-020 | 20 | `CEPRAEA — Wellness — Apps Script Mobile.txt` | TÉCNICA·AUXILIAR·DERIVADA | Restaurado (D-01); reconfirmar integridade antes de processar | Não |
| AC-021 | 21 | `Cópia de CEPRAEA — Wellness — Apps Script Mobile.txt` | — | **Resolvido — Davi decidiu não restaurar.** O original (`AC-020`) já supre a fonte. `estado_processamento=NAO_APLICAVEL` diretamente, registrado como decisão em `decisoes/registro_decisoes.md` | Não |
| AC-022 | 22 | `Preparação competitiva CEPRAEA 2026 — Treinos e cenários até a Fase Final.docx` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | Testar hipótese de pareamento com AC-011 (mesmo tema, timestamps próximos) | Não |
| AC-023 | 23 | `Preparação competitiva CEPRAEA 2026 — calendário e cenários — versão acessível.docx` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | Testar pareamento com AC-014 | Não |
| AC-024 | 24 | `Preparação competitiva CEPRAEA 2026 — versão corrigida.docx` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | Testar pareamento com AC-013 | Não |
| AC-025 | 25 | `CEPRAEA BEACH PRO.docx` | INDETERMINADO·INDETERMINADA·INDETERMINADA | Nome sugestivo, sinal de dado provavelmente baixo — confirmar em vez de presumir | Não |
| AC-026 | 26 | `CEPRAEA-pdf.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | — | Não |
| AC-027 | 27 | `Roteiro completo — Relatório curto e visual às atletas — CEPRAEA 2026.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | — | Não |
| AC-028 | 28 | `Roteiro relatório fase CEPRAEA.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | Roda AD-05 aqui (último ponto antes da síntese para checar termos com sobreposição semântica) | Não |
| AC-029 | 29 | *(nenhum — síntese, produz commit(s) `SYN-NNN`, seção 4.9)* | — | **Gate é a maturidade semântica, não a conclusão dos 28 dossiês** — as 28 entradas em estado terminal (`CONCLUIDO`, `BLOQUEADO` ou `NAO_APLICAVEL`) só habilitam esta ação a rodar. Ordem obrigatória, sem pular etapa (seção 4.7): (1) **reconciliar** — resolve o que ainda está pendente em `conhecimento/conflitos_semanticos.md`, registrando `SEM-NNN` por reconciliação material; (2) **promover** — só `candidatos/*.md` com `estado_epistemologico=VALIDADO` são promovidos por ação `SEM-NNN`: o candidato passa a `estagio=PROMOVIDO` com `promoted_to`, a representação canônica de mesmo ID nasce em `dominio/*.md` com `estagio=DOMINIO`, `promoted_from` e `promoted_by`; nenhuma promoção automática só por existir em `candidatos/`; (3) **consolidar** — escreve `dominio/modelo_canonico_dominio.md`, síntese por `CTX-NNN`; (4) **classificar** — roda AD-06 (conta `AMBIGUO`/`CONFLITANTE` pendente por contexto) e atribui `maturidade` a cada `CTX-NNN` (seção 4.4), com justificativa registrada mesmo quando o resultado é `IMATURA`; (5) **derivar** — só `MADURA_PARA_MODELO_LOGICO` vira entrada em `logico/modelo_logico_relacional.md`; todo o resto vira linha em `logico/areas_pendentes.md`, com o que falta para amadurecer. Vazio/parcial em `logico/modelo_logico_relacional.md` é `DONE` válido, nunca pendência | **Sim — homologação final da fase, inclui reportar `areas_pendentes.md` por completo** |

DONE de cada linha AC-001..AC-028: ver seção 7 (critério único). DONE de AC-000: os 12 itens da
seção 10.1. DONE de AC-029: **o gate é a maturidade semântica da seção 4.4 avaliada e registrada para
todo `CTX-NNN`, não a conclusão dos 28 dossiês.** As 28 entradas em estado terminal (`CONCLUIDO`, `BLOQUEADO` ou `NAO_APLICAVEL`) habilitam `AC-029` a
rodar, mas `logico/modelo_logico_relacional.md` só ganha conteúdo para o que passar no gate — sair vazio
ou parcial é `DONE` válido, não pendência. Critério completo: seção 11.

## 11. Critério de pronto desta fase

A fase só é `DONE` quando os cinco gates abaixo forem verdadeiros simultaneamente (`A && B && C && D && E`).

### GATE A — Cobertura operacional

- As 28 entradas possuem estado terminal: `CONCLUIDO`, `BLOQUEADO` ou `NAO_APLICAVEL`; nenhuma permanece `NAO_INICIADO`/`EM_EXECUCAO`.
- Estado terminal não implica maturidade semântica.
- Fontes `BLOQUEADO`/`NAO_APLICAVEL` são incorporadas ao cálculo de maturidade do(s) `CTX-NNN` afetado(s).

### GATE B — Integridade semântica

- Existe `dominio/modelo_canonico_dominio.md`, síntese por `CTX-NNN`.
- Nenhum termo, regra ou elemento com `estado_tecnico` além de `NAO_MODELADO` deixa de estar `VALIDADO`.
- Todo item `VALIDADO` possui `source_evidence`, `semantic_evidence` não vazio, `approval_evidence.aprovador="Davi Sermenho"`, data de aprovação e `repository_evidence.action_ref`.
- `INV-001`/`DEC-006` preservam a origem humana já validada; `CTX-001`–`CTX-008` permanecem candidatos `INFERIDO` até validação real.
- Nenhum elemento canônico material depende exclusivamente de fonte `SUBSTITUIDA`/`OBSOLETA` sem confirmação independente.

### GATE C — Rastreabilidade

- `validar.mjs` valida 100% dos registros contra o subconjunto de schema declarado.
- `verificar_referencias.mjs` resolve 100% das referências: `SRC→EVD→TERMO/REGRA→CTX/IDN/INV/LFC/AGG/TRX→dominio→logico`; zero órfãos.
- Para entrada `DOMINIO`, vale exatamente uma rota: promoção normal `SEM-NNN` com candidato `PROMOVIDO`, ou `PRE-SEED` formal.
- Todo elemento lógico possui `bounded_context_id` e `derived_from[]`; todo item de `areas_pendentes.md` possui `blocking_ids[]`.

### GATE D — Maturidade

- Cada `CTX-NNN` possui maturidade explicitamente atribuída e justificada.
- Qualquer ambiguidade/conflito estrutural impede `MADURA_PARA_MODELO_LOGICO`.
- `logico/modelo_logico_relacional.md` contém somente elementos de contextos `MADURA_PARA_MODELO_LOGICO`.
- Contextos não maduros aparecem em `logico/areas_pendentes.md` com `blocking_ids`, motivo e resolução necessária.
- AD-01..AD-06 foram executados com resultado real; AD-06 prova que cobertura documental não libera o modelo lógico.

### GATE E — Repositório e branch dedicada

- `verificar_repositorio.mjs` resolve todo `action_ref` para exatamente um commit real (`AC-NNN`, `SEM-NNN`, `SYN-NNN`).
- O SHA real é obtido externamente pelo Git; nenhum artefato contém SHA autorreferencial do commit que o contém.
- `git rev-parse main` ao final é igual a `MAIN_SHA_BEFORE`.
- Todos os commits da fase estão em `feat/cepraea-domain-modeling` depois de `BASE_SHA`.
- Nenhuma escrita ocorreu fora de `WRITE_SCOPE_EXECUTOR`/`WRITE_SCOPE_REVIEWER` (`DEC-008`); nenhum dado sensível foi reproduzido literalmente.
- Todas as fixtures declaradas no manifest continuam passando como regressão final.

Explicitamente fora deste critério: migrations executadas, RLS testada e testes SQL.

## 12. Classificação de risco e papéis de arquivo (AGENT_POLICY.md)

Esta seção, aprovada, serve como a proposta formal exigida pelo `AGENT_POLICY.md`
(schema de `.ai/task-proposal.example.json`). Os escopos de caminho abaixo foram revisados por
`DEC-008` (`decisoes/registro_decisoes.md`): a worktree irmã da seção 4.7 original foi removida;
isolamento agora é por branch dedicada + `WRITE_SCOPE` explícito.

- **Risco: amarelo** em toda a fase (múltiplos arquivos-alvo + semântica canônica), com
  **carve-out vermelho por privacidade** em AC-008, AC-018, AC-019 — exigem seu checkpoint
  antes de `CONCLUIDO`. Não é vermelho crítico.
- AJV é melhoria futura opcional; o plano atual é executável sem dependência nova porque `validar.mjs` cobre exatamente o subconjunto de JSON Schema utilizado e falha em keyword desconhecida.

| Caminho | Papel |
|---|---|
| `docs/modelagem/**` (a criar/completar, seção 4.7, branch `feat/cepraea-domain-modeling`) | alvo (`WRITE_SCOPE_EXECUTOR`) |
| ~~`.agent-flow/executions/**`~~ | removido — DEC-GOV-001 (2026-08-14) |
| ~~`.agent-flow/reviews/**`~~ | removido — DEC-GOV-001 (2026-08-14) |
| `docs/standards/guia_estilo_documentação.md`, `AGENT_POLICY.md`, `.ai/task-proposal.example.json` | referência |
| `.drive/BEACH HANDBALL/Fluxo de Modelagem.gdoc.docx`, `.drive/modelagem_dados_agente.md`, `.drive/modelagem_dominio_dados.md` | referência (canônicos, seção 4/4.1) |
| `.drive/CEPRAEA BEACH PRO/*` (27 fontes presentes) | somente leitura |
| Escrita fora de `WRITE_SCOPE_EXECUTOR`, incluindo `main`/`master` e `$CEPRAEA_SOURCE_ROOT` | proibida |
| Leitura fora de `READ_SCOPE` | proibida |
| Valor literal de qualquer segredo/PII encontrado | proibido (regra de conteúdo) |

Execução: branch dedicada `feat/cepraea-domain-modeling` (seção 4.7), um agente escritor nela —
nunca `main`. Um commit por `AC-NNN` (aquisição); `SEM-NNN`/`SYN-NNN` para reconciliação e síntese
(seção 4.9). Criação de branch/ref é operação Git de promoção — reservada a Davi
(`AGENT_POLICY.md` §Autoridade), inclusive por restrição de permissão de filesystem observada
durante `AC-000` (`.git/refs/heads` somente leitura para o `EXECUTOR`). Se surgir um 29º arquivo
na pasta ou necessidade de tocar RLS/auth, paro e levanto proposta nova.

## 13. Verificação

1. `schemas/validar.mjs` roda sobre todos os registros e retorna 0 erros.
2. `schemas/validar.mjs schemas/fixtures/manifest.json` executa todas as fixtures declaradas; `failed=0`.
3. `schemas/verificar_referencias.mjs` percorre 100% das referências e retorna `orfaos=0`.
4. `schemas/verificar_repositorio.mjs` resolve cada `action_ref` para exatamente um commit e retorna `duplicados=0`, `ausentes=0`.
5. Todo `EVD.id_fonte` referencia `SRC` existente e todo `EVD.id_acao` referencia ação de aquisição coerente.
6. Todo `TERMO.fonte`, `REGRA.fonte` e `elemento.fonte` aponta para `EVD-NNNN` existente ou `REF:` explicitamente permitido.
7. Todo `DOMINIO` segue ROTA A (candidato `PROMOVIDO` + `SEM-NNN`) ou ROTA B (`PRE-SEED` + `REF:` + aprovação).
8. Todo `bounded_context_id` resolve para `CTX-NNN` existente.
9. `dominio/modelo_canonico_dominio.md` referencia somente IDs existentes em `dominio/`.
10. Nenhum elemento de `logico/modelo_logico_relacional.md` pertence a contexto não `MADURA_PARA_MODELO_LOGICO`; cada elemento lógico possui `derived_from[]`.
11. Todo `CTX` não maduro aparece em `logico/areas_pendentes.md` com `blocking_ids[]`, `blocking_reason` e `required_resolution`.
12. AD-02: `grep` dirigido pelo valor literal conhecido da credencial sobre `docs/modelagem/**` retorna 0 ocorrências.
13. Amostra manual de três cadeias completas permanece como sanity check humano, mas a garantia primária é a validação exaustiva do item 3.
14. `git diff` é revisado a cada commit; `AC-NNN`, `SEM-NNN` e `SYN-NNN` são usados apenas para suas finalidades.
15. `git rev-parse main` ao final é exatamente `MAIN_SHA_BEFORE`; `git log "$BASE_SHA"..feat/cepraea-domain-modeling` contém apenas commits da fase.
16. `markdownlint --config .markdownlint.jsonc docs/modelagem/**/*.md` é executado quando disponível; indisponibilidade é registrada.
17. O critério de pronto da seção 11 é verificado gate por gate ao final do `AC-029`.
