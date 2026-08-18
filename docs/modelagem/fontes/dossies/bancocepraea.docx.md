# `SRC-002` — `BancoCEPRAEA.docx`

## Identificação

- Nome do arquivo: `BancoCEPRAEA.docx`
- ID do Drive: não recuperável neste ambiente (`id_drive=null`, permitido — seção 5.1 do plano).
- ID interno: `SRC-002` / `AC-002`
- Tipo de arquivo: `docx` (Office Open XML)
- Idioma: pt-BR
- Escopo temporal: documento técnico de modelagem, sem data explícita no corpo extraído; referencia
  a alteração normativa IHF vigente desde 2026-04-01.
- Classe hipotética (seção 10 do plano): `TÉCNICA·AUXILIAR·ORIGINAL`, com `estado_fonte=SUBSTITUIDA`
  **fixado por `DEC-002` (D-02)** — não é uma classificação derivada do conteúdo desta ação, é
  aplicação de uma decisão humana já resolvida em `AC-000`.
- Hash: `108900171b22e659c49892d69078cf64cd8631cf3efd20924e7ee56e5916fb73` (SHA-256, verificado via
  `sha256sum` e `node:crypto`, ambos concordantes)
- Caminho local: `.drive/CEPRAEA BEACH PRO/BancoCEPRAEA.docx`

## Seleção de conteúdo

Documento de 17 seções numeradas, íntegro: finalidade, evidências/correções sobre as planilhas já
processadas em `AC-001`, regras normativas (IHF Beach Handball), 10 princípios/invariantes
declarados (`DOM-001` a `DOM-010`), arquitetura de schemas (`public`/`private`/`audit`/`auth`),
catálogo de tipos PostgreSQL, catálogo de 23 tabelas físicas com dicionário completo de colunas e
`CREATE TABLE` por tabela, relações/cardinalidades, 10 views derivadas, políticas RLS completas
(`0005_rls.sql`), 7 RPCs transacionais (`0006_rpcs.sql`), 8 arquivos de migration (`0001` a
`0008_seed_synthetic.sql`, incluindo triggers de integridade e append-only), estratégia de
implementação por marco (M0-M4 + gate de dados reais), contrato de extensibilidade futura
(competição/partida deferidos) e uma matriz explícita de substituição das abas `DB_*` já
catalogadas em `AC-001`.

Extração via `perl -MIO::Uncompress::Unzip` (membro `word/document.xml`) + parser Node próprio
(reconstrução de parágrafos e tabelas a partir de `<w:p>`/`<w:tbl>`/`<w:tr>`/`<w:tc>`/`<w:t>`,
decodificação de entidades XML). Mesmo método já usado informalmente em `AC-000` para resolver
`D-03` sobre este mesmo arquivo, agora aplicado de forma completa e formal para `AC-002`. Todas as
17 seções foram lidas integralmente, incluindo os 8 arquivos de migration SQL brutos (seção 13) —
verificado que não são pura repetição do dicionário da seção 9: a seção 13.4 (triggers de
integridade) contém regras de validação cruzada (ex.: `training_sessions` exige
`commitment_type=TREINO`; `athlete_roster_memberships` exige que atleta e temporada pertençam à
mesma equipe) que não aparecem em nenhuma outra seção.

Nenhuma tabela/seção foi excluída por inferência de nome — lição já registrada em `DEC-007`
(`AD-03`, `AC-001`) aplicada preventivamente aqui.

## Resultado da análise

- **Resultado do teste adversarial `AD-01` (seção 8 do plano) — o propósito central desta ação:**
  este documento é tecnicamente completo e persuasivo — 23 tabelas físicas, `CREATE TABLE`/RLS/RPC
  prontos, texto técnico confiante ("A modelagem proposta é a base correta para o MVP..."). Apesar
  disso, `autoridade_fonte=AUXILIAR` e `estado_fonte=SUBSTITUIDA` são aplicados sem exceção, por
  `DEC-002` (D-02: fluxo de modelagem anterior declarado falho por Davi) — nunca `OFICIAL`/
  `PRIMARIA` nem `VIGENTE`. Nenhum termo ou elemento derivado desta fonte nesta ação recebe
  `estado_epistemologico=VALIDADO` — todos nascem `OBSERVADO`. Resultado formal registrado em
  `DEC-004` (`decisoes/registro_decisoes.md`), rascunho pendente da sua confirmação (mesmo
  mecanismo de `DEC-007`).
- Conceitos técnicos observados (mapeiam para conceitos de domínio já estabelecidos em `AC-001`,
  não geram `TERMO-NNN` novo por si só — ver "Conflitos ou dúvidas"): `athlete`/
  `athlete_roster_membership` (mapeia `TERMO-001`), `commitment`/`training_sessions` (mapeia
  `TERMO-005`), `operational_requests`/`operational_responses` (mapeia `TERMO-002`),
  `attendance_records` (mapeia `TERMO-003`), `operational_lists` (relacionado a `TERMO-005`).
- Candidatos de invariante novos, não cobertos por `INV-001`/`INV-002`: `INV-003` (identidade não é
  nome — junções usam UUID/código legado), `INV-004` (justificativa de ausência é privada, nunca
  compartilhada), `INV-005` (fatos históricos são preservados, nunca reescritos por mudança de
  regra ou por correção), `INV-006` (lista prevista não implica presença factual — generalização de
  `INV-002` para o objeto lista, não para a resposta de disponibilidade), `INV-007` (convocação de
  etapa ≠ escalação de partida ≠ participação real, três estados distintos de uma mesma cadeia).
  Todos registrados `candidatos/invariantes.md`, `estado_epistemologico=OBSERVADO`.
- Regra normativa nova: `REGRA-009` — número de camisa (`shirt_number`) válido entre 1 e 99,
  vigente por alteração IHF desde 2026-04-01 (antes dessa data o intervalo era outro, não
  detalhado nesta fonte).
- Fatos operacionais (técnicos, não de elenco): arquitetura de 4 schemas PostgreSQL
  (`public`/`private`/`audit`/`auth`); 23 tabelas físicas; RLS distingue papel `COACH` (exige
  MFA/AAL2) de `ATHLETE` (autoatendimento restrito ao próprio registro); 5 tabelas append-only
  (`athlete_roster_events`, `operational_responses`, `response_corrections`,
  `attendance_records`, `audit_events`) protegidas por trigger `prevent_update_delete`.
- Relações e cardinalidades: documentadas exaustivamente na seção 8 do documento-fonte (19 relações
  tabela-a-tabela, regra geral de exclusão `RESTRICT`) — não repetidas aqui, ver `EVD-0051`.
- Valores permitidos novos observados: `broad_player_function` (`GOLEIRA`/`DEFESA`/`ATAQUE`/
  `INDEFINIDA` — 4 valores, sem `CORINGA`/`ESPECIALISTA`, que a própria fonte declara papel tático
  futuro e fora do cadastro atual).
- Conflitos ou dúvidas:
  1. Vocabulário técnico desta fonte (`athlete`, `commitment`, `request`/`response`,
     `attendance`) não foi promovido a `TERMO-NNN` novo nesta ação — mapeia, com boa confiança,
     para conceitos já nomeados em `AC-001` (`TERMO-001`, `TERMO-005`, `TERMO-002`, `TERMO-003`),
     mas a fonte é técnica/`AUXILIAR` e a nomeação em português já estabelecida por `AC-001` tem
     precedência. Registrado como correspondência a confirmar em `AC-029` (reconciliação), não
     resolvido por fusão automática de nomenclatura aqui.
  2. `DOM-003` (convocação de etapa ≠ escalação/roster de partida ≠ participação real) antecipa
     estrutura de um módulo (`CTX-005`/`CTX-006`) que a própria fonte declara **fora do MVP atual**
     (seção 15, "Contrato de extensibilidade futura"). Registrado como candidato (`INV-007`) porque
     a distinção em si já aparece corroborada por `TERMO-006` (`AC-001`), não porque o módulo deva
     ser antecipado — nenhuma tabela nova foi sugerida para `candidatos/` além da invariante.
  3. `DOM-008` ("indicadores são projeções de fatos validados") e `DOM-010` ("nenhum dado real é
     autorizado no estágio sintético atual") não geraram candidato de invariante de domínio —
     são princípios de arquitetura/governança técnica já cobertos por decisão de projeto existente
     (`README.md` raiz, `DEC-019`), não fatos novos sobre atletas/treinos/jogos.
  4. `DOM-005` ("respostas, correções, presença e eventos de vínculo preservam histórico") foi
     absorvido em `INV-005` junto com `DOM-009`, por serem a mesma propriedade (preservação de
     fato histórico) vista de dois ângulos (design de tabela vs. regra de não-reescrita) — não
     registrados como dois candidatos separados para não duplicar o mesmo invariante.
  5. Nenhum dado real (nome de atleta, contato, credencial) foi encontrado nesta fonte — confirmado
     por leitura integral e por checagem específica de padrões sensíveis (`senha`/`password`/`cpf`)
     sobre o texto extraído, sem ocorrência além de uma regra de design ("não armazenar senha,
     token ou segredo", `EVD-0053`). Dado sintético de seed usa apenas placeholders genéricos e
     UUIDs fixos de exemplo.
- Artefatos técnicos afetados: nenhum (fora de escopo desta fase — seção 3 do plano). O esquema
  físico proposto por esta fonte **não é adotado** nesta fase — `DEC-002` já fecha que o modelo
  lógico desta fase nasce do Modelo Canônico, não deste documento.
- Testes afetados: nenhum (fora de escopo desta fase).
- Estado final do arquivo: `CONCLUIDO`.
- Próxima ação: `AC-003` (`CEPRAEA-DB.docx`) — mesma classificação fixada por `DEC-002`
  (`TÉCNICA·AUXILIAR·SUBSTITUIDA`), e o próprio inventário já nota que este arquivo contém o
  inventário de 65 fontes de `BEACH HANDBALL` a apenas referenciar, não reprocessar. `AC-004`
  (`CEPRAEA DATABASE.xlsx`) continua sendo o teste real da hipótese `DB_EXPORT_FRONTEND`/
  `DB_PRESENCA_FATUAL` levantada em `AC-001`.

## Dados sensíveis

Nenhum dado pessoal real encontrado. Documento é especificação técnica de schema com dados de seed
exclusivamente sintéticos (UUIDs de exemplo fixos, rótulos genéricos como "Temporada sintética
2026"). Classificação: não aplicável (`dado_sensivel_encontrado=false`).

## Critério de saída

- [x] Identidade e classe de autoridade registradas (classificação fixada por `DEC-002`, verificada
      contra o conteúdo real, não presumida).
- [x] Escopo usado registrado, sem escopo descartado remanescente — todas as 17 seções, incluindo
      os 8 arquivos de migration, foram lidas integralmente.
- [x] Trechos relevantes localizados (14 fragmentos em `evidencias/registro_evidencias.md`,
      `EVD-0049` a `EVD-0062`).
- [x] Interpretação separada do texto original (`trecho_literal` vs. prosa desta seção).
- [x] Conflitos e precedências resolvidos ou explicitamente registrados (5 itens acima, nenhum
      resolvido por suposição).
- [x] Conceitos, regras e candidatos encaminhados aos artefatos corretos (`registro_regras.md`,
      `candidatos/invariantes.md`), sem duplicar nomenclatura já estabelecida por `AC-001`.
- [x] Nenhuma conclusão excede o que a fonte sustenta — `AD-01` executado e registrado como decisão
      formal (`DEC-004`), pendente de confirmação.
- [x] Nenhum dado sensível transcrito literalmente (nenhum foi encontrado).

```json
{
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "nome_arquivo_original": "BancoCEPRAEA.docx",
  "caminho_local": ".drive/CEPRAEA BEACH PRO/BancoCEPRAEA.docx",
  "hash_sha256": "108900171b22e659c49892d69078cf64cd8631cf3efd20924e7ee56e5916fb73",
  "id_drive": null,
  "tipo_arquivo": "docx",
  "idioma": "pt-BR",
  "tipo_fonte": "TECNICA",
  "autoridade_fonte": "AUXILIAR",
  "proveniencia_fonte": "ORIGINAL",
  "estado_fonte": "SUBSTITUIDA",
  "estado_processamento": "CONCLUIDO",
  "dado_sensivel_encontrado": false,
  "conceitos_encontrados": [],
  "regras_encontradas": ["REGRA-009"],
  "conflitos_ou_duvidas": [
    "Vocabulário técnico (athlete, commitment, request/response, attendance) mapeia para TERMO-001/002/003/005 já estabelecidos por AC-001, sem TERMO-NNN novo criado nesta ação — correspondência a confirmar em AC-029, não fusão automática.",
    "DOM-003 (convocação de etapa ≠ escalação de partida ≠ participação real) antecipa estrutura de módulo declarado fora do MVP atual pela própria fonte (seção 15) — registrado só como candidato de invariante (INV-007), nenhuma tabela nova sugerida.",
    "DOM-008 e DOM-010 são princípios de arquitetura/governança técnica já cobertos por decisão de projeto existente, não geraram candidato de invariante de domínio.",
    "DOM-005 e DOM-009 foram absorvidos em um único candidato (INV-005) por serem a mesma propriedade vista de dois ângulos.",
    "Nenhum dado real encontrado nesta fonte, confirmado por leitura integral e checagem de padrões sensíveis."
  ],
  "evidencia": {
    "comando_ou_metodo": "perl -MIO::Uncompress::Unzip=unzip (extração de word/document.xml) + parser Node próprio (reconstrução de parágrafos e tabelas a partir de w:p/w:tbl/w:tr/w:tc/w:t) + sha256sum/node:crypto para hash",
    "resultado": "documento de 17 seções numeradas extraído por completo (4065 linhas de texto reconstruído, 57 tabelas Word identificadas incluindo as 23 tabelas físicas do schema proposto); todas as seções lidas integralmente, incluindo os 8 arquivos de migration SQL brutos (seção 13), verificados por amostragem como não puramente redundantes com a seção 9 (triggers de integridade cruzada só aparecem na seção 13.4); checagem de padrões sensíveis (grep case-insensitive por 'senha', 'password', 'cpf') sobre o texto extraído retornou uma única ocorrência, sendo uma regra de design, não um valor real",
    "repository_evidence": {
      "action_ref": "AC-002"
    },
    "limitacoes": [
      "A leitura da seção 13 (migrations brutas) foi verificada por amostragem de subseções representativas (13.4, 13.5, 13.7, 13.9), não por comparação linha a linha contra a seção 9/10/11/12 — risco residual de conteúdo novo não capturado nas subseções não amostradas (13.1, 13.2, 13.3, 13.6, 13.8), mitigado por essas serem, pelo título, cópias diretas de DDL/índices/RLS/audit já cobertos textualmente nas seções correspondentes."
    ]
  },
  "proxima_acao": "AC-003 (CEPRAEA-DB.docx) segue a mesma classificação fixada por DEC-002; o inventário já nota que contém o inventário de 65 fontes de BEACH HANDBALL, só a referenciar. AC-004 (CEPRAEA DATABASE.xlsx) continua sendo o teste real das hipóteses DB_EXPORT_FRONTEND/DB_PRESENCA_FATUAL levantadas em AC-001."
}
```
