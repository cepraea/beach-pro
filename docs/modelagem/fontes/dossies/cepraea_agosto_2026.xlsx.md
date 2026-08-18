# `SRC-001` — `CEPRAEA AGOSTO 2026.xlsx`

## Identificação

- Nome do arquivo: `CEPRAEA AGOSTO 2026.xlsx`
- ID do Drive: não recuperável neste ambiente (`id_drive=null`, permitido — seção 5.1 do plano).
- ID interno: `SRC-001` / `AC-001`
- Tipo de arquivo: `xlsx` (Office Open XML — 45 abas, 41 ocultas, 4 visíveis)
- Idioma: pt-BR
- Escopo temporal: temporada 2026, com dados históricos desde junho de 2024
- Classe hipotética (seção 10 do plano): `OPERACIONAL·PRIMARIA·ORIGINAL` — confirmada abaixo
- Hash: `cb179a19a9f7e313e08e9577954035d0a5ad8be37ea68ae325cef03df413ef41` (SHA-256, verificado via `node:crypto` e `sha256sum`, ambos concordantes)
- Caminho local: `.drive/CEPRAEA BEACH PRO/CEPRAEA AGOSTO 2026.xlsx`

## Seleção de conteúdo

Planilha com 45 abas: 4 visíveis (`AGENDA CEPRAEA`, `🏖️ DIA DO JOGO`, `ANÁLISE JOGOS`,
`AGOSTO - 2026`) e 41 ocultas. Todas as 45 abas foram abertas e lidas integralmente ou até
completude estrutural confirmada — ver "Terceira nota de correção" abaixo. Abas processadas com
profundidade: `R_STATUS`, `R_FUNCOES`, `R_MONTHS`, `R_DATES`, `R_META`, `Página16` (contrato de
UI), `DISPONIBILIDADE BR e RJ`, `AGOSTO - 2026`, `JULHO - 2026`, `MAIO - 2026`, `ABRIL - 2026`,
`MARÇO - 2026`, `FEVEREIRO - JANEIRO 2026`, `NOVEMBRO 2025`, `OUTUBRO 2025`, `SETEMBRO 2025`,
`JULHO E AGOSTO 2025`, `JUNHO E JULHO 2025`, `MAIO 2025`, `MARÇO E ABRIL 2025`,
`JANEIRO E FEVEREIRO 2025`, `NOVEMBRO E DEZEMBRO 2024`, `OUTUBRO 2024`,
`AGOSTO E SETEMBRO 2024`, `JULHO 2024`, `JUNHO 2024`, `📑_CHANGELOG`, `PAINEL DATABASE`,
`PRÓXIMO TREINO`, `🏖️ DIA DO JOGO`, `ANÁLISE JOGOS`, `ANÁLISE DOS JOGOS` (oculta, distinta da
anterior — ver "Terceira nota de correção"), `AGENDA CEPRAEA` (1000 linhas de capacidade,
varredura completa confirma 44 linhas com conteúdo, nenhuma além da linha 45 — ver "Quarta nota de
correção"; visão de temporada por competição, com bloco de cálculo próprio "Formula engine",
estruturalmente distinta das matrizes semanais de treino), `📅 FEEDBACK
INDIVIDUAL`/`_AGENDA_FEEDBACK`/`_CONFIG_FEEDBACK`/`_LOG_FEEDBACK` (módulo de feedback,
caracterizado como suspenso), `_WX_DIA_DO_JOGO` (dados meteorológicos, baixo valor de domínio),
`_IMPORT_DATABASE`/`_FRONTEND_CHANGELOG` (ponte técnica com `CEPRAEA DATABASE.xlsx`, relevante
para `AC-004`), `_IMPORT_ANALISE_JOGOS` (staging de análise de jogos).

**Nota de correção (achado do REVIEWER — revisão adversarial):** a primeira versão deste dossiê
excluiu `AGENDA TÉCNICA V2`, `AGENDA TÉCNICA MODELO` e `3ª ETAPA CARIOCA 2026` sem abri-las,
presumindo pelo nome que não conteriam conceito novo, e ainda assim marcou `estado_processamento`
como `CONCLUIDO` — exatamente o antipadrão que a modelagem por evidência existe para impedir
(fonte ≠ inferência sobre a fonte, `modelagem_dados_agente.md`). As três abas foram reabertas e
lidas: continham conceitos genuinamente novos (`TERMO-012` adversário, `TERMO-013` status de
confirmação de jogo, `REGRA-006`, estrutura de fase/grupo de torneio) — ver `EVD-0029` a
`EVD-0034`. Essas três abas agora fazem parte das abas processadas com profundidade, não das
excluídas.

**Segunda nota de correção (achado do REVIEWER — revisão adversarial, segunda rodada):** a
correção acima ainda deixou `AGENDA TÉCNICA V2` (lida até a linha 42 de 52) e `3ª ETAPA CARIOCA
2026` (lida até a linha 45 de 90) parcialmente lidas, com `estado_processamento` já marcado
`CONCLUIDO` — o mesmo risco de inferência não sustentada, um nível abaixo (presumir que o
*restante* de uma aba já parcialmente lida não contém novidade, em vez de presumir isso pelo
*nome* da aba). Diferente das abas mensais históricas (que são um padrão recorrente já confirmado
por amostragem), essas duas abas têm blocos internos heterogêneos — não há garantia de que um
bloco não lido se pareça com os já lidos. Ambas as abas foram lidas por completo. Achados novos:
`REGRA-007` (disponibilidade de etapa sem participação do CEPRAEA é preservada só como histórico);
uma instância real de convocação já concluída (`TERMO-006`, reforçado); e uma discrepância de
identificador de atleta (`Nº` não sequencial em RELAÇÃO NOMINAL CEPRAEA vs. numeração sequencial
1-19 nas matrizes mensais, `TERMO-001.limitacoes`) — ver `EVD-0035` a `EVD-0038`.

**Terceira nota de correção (achado do REVIEWER — revisão adversarial, terceira rodada):**
`estado_processamento` continuava `CONCLUIDO` com dois problemas adicionais do mesmo antipadrão:
(1) as ~15 abas mensais históricas restantes (`JUNHO - 2026` até `JUNHO 2024`) haviam sido
amostradas via `MAIO - 2026`/`JULHO - 2026`, e o padrão recorrente foi extrapolado sem verificação
— a própria amostragem já continha uma divergência de vocabulário (`Ok`/`Out` vs. `SIM`/`NAO`/
`TALVEZ`) que deveria ter motivado leitura integral, não amostragem; (2) a aba oculta `ANÁLISE DOS
JOGOS` nunca foi aberta, presumivelmente por colisão de nome com a aba visível já lida `ANÁLISE
JOGOS`. Todas as 17 abas mensais históricas e `ANÁLISE DOS JOGOS` foram lidas por completo.
Achados novos: uma terceira variante histórica de vocabulário de resposta (`Tentarei`,
`TERMO-002.limitacoes`); confirmação de que `Ok`/`Out`/`Talvez` é o vocabulário predominante por
~2 anos, não uma amostra isolada; divergência estrutural de elenco entre abas antigas e a relação
atual (`TERMO-001.limitacoes`); uma regra de cálculo nova (`REGRA-008`, `jogo_real =
status_participacao JOGOU`) e um ativo técnico novo (`DB_PARTICIPACAO_JOGO`); e uma divergência
material entre os totais de temporada de `ANÁLISE DOS JOGOS` (23 jogos) e `ANÁLISE JOGOS` (19
jogos), ambos internamente consistentes mas mutuamente divergentes — registrada como `AMBIGUO`,
não resolvida por suposição (`TERMO-008.limitacoes`, `REGRA-008.duvidas`) — ver `EVD-0039` a
`EVD-0044`.

**Quarta nota de correção (achado do REVIEWER — revisão adversarial, quarta rodada):** a aba
`AGENDA CEPRAEA` permanecia amostrada nas primeiras ~30 linhas sob a presunção de que
compartilhava a estrutura recorrente das matrizes semanais de treino — a mesma classe de
inferência não verificada já corrigida nas rodadas anteriores, agora aplicada a um corte de linha
em vez de a uma aba inteira. A aba foi varrida por completo (1000 linhas de capacidade, ferramenta
própria, sem corte) e revelou-se estruturalmente distinta: uma visão de temporada por
competição/etapa, não uma matriz semanal, com um bloco de cálculo próprio rotulado "Formula
engine". A suposição de equivalência estrutural estava errada. Achados novos: prazos de inscrição
e de relação nominal por etapa (`TERMO-007`); um novo conceito, `TERMO-014` (ação técnica
recomendada); valores reais do índice de competitividade que confirmam operacionalmente as faixas
já documentadas em `TERMO-010`; e uma coluna de status por etapa no bloco "Formula engine" com
vocabulário mais estreito (3 valores) do que o enum de 5 valores de `TERMO-009`, cuja relação não
está resolvida — ver `EVD-0045` a `EVD-0048`.

Extração via `perl -MIO::Uncompress::Unzip` (membros `xl/sharedStrings.xml` e
`xl/worksheets/sheet*.xml`) + script Node de leitura própria (fora do escopo de escrita desta
fase — descartável, não commitado). Método idêntico ao já usado em `AC-000` para `.docx`, adaptado
à estrutura de planilha (tabela de strings compartilhadas + células por referência).

## Resultado da análise

- Conceitos encontrados: `TERMO-001` (atleta), `TERMO-002` (disponibilidade declarada),
  `TERMO-003` (presença factual), `TERMO-004` (função esportiva), `TERMO-005` (próximo treino),
  `TERMO-006` (convocação), `TERMO-007` (etapa competitiva), `TERMO-008` (jogo/resultado),
  `TERMO-009` (status de risco funcional), `TERMO-010` (índice de competitividade), `TERMO-011`
  (criticidade da atleta), `TERMO-012` (adversário), `TERMO-013` (status de confirmação de jogo),
  `TERMO-014` (ação técnica recomendada).
- Regras encontradas: `REGRA-001` a `REGRA-008` (ver `conhecimento/registro_regras.md`).
- Candidato de invariante: `INV-002` (disponibilidade declarada não implica presença factual),
  registrado em `candidatos/invariantes.md`, `bounded_context_id=CTX-004`.
- Fatos operacionais: 19 atletas ativas (coerente com `DEC-006`); elenco com 3 goleiras, 7
  defesas, 12 ataques (`PAINEL DATABASE`); temporada com 19 jogos, 12 vitórias, 7 derrotas
  segundo `ANÁLISE JOGOS` (visível) — a aba oculta homônima `ANÁLISE DOS JOGOS` registra 23
  jogos, 14 vitórias, 9 derrotas para a mesma temporada; divergência não resolvida, ver conflito
  9 abaixo.
- Relações e cardinalidades: uma resposta de disponibilidade por atleta por evento (treino ou
  etapa); um valor de função esportiva por atleta (sujeito a correção humana registrada).
- Regras temporais: disponibilidade futura vs. presença só pós-sessão (`REGRA-001`); próximo
  treino recalculado dinamicamente (`REGRA-005`).
- Valores permitidos: enum de disponibilidade (`SIM`/`NAO`/`TALVEZ`, `REGRA-003`); enum de função
  (`R_FUNCOES`); enum de status de risco (5 valores, `TERMO-009`).
- Conflitos ou dúvidas:
  1. Rótulo de cabeçalho inconsistente entre meses para a mesma matriz de resposta: `JULHO -
     2026` usa "CONFIRMAÇÃO DE PRESENÇA" (`EVD-0015`), `AGOSTO - 2026` usa "DECLARAÇÃO DE
     DISPONIBILIDADE / COMPROMISSO" (`EVD-0014`). Não bloqueante — `R_META` (datado de
     2026-08-09, mais recente) já estabelece a semântica correta como disponibilidade, não
     presença; a divergência de rótulo é resíduo textual de reconciliação incompleta entre abas
     mensais, não um conflito normativo ativo. Registrado como `AMBIGUO` associado a `TERMO-002`,
     não resolvido por exclusão silenciosa do rótulo antigo.
  2. Vocabulário de resposta: três gerações históricas confirmadas por leitura integral —
     `Ok`/`Out`/`Talvez` predominante por ~2 anos (JUNHO 2024 a ABRIL 2026), a variante `Tentarei`
     no mesmo período (`EVD-0039`), e `SIM`/`NAO`/`TALVEZ` só a partir de `JUNHO - 2026`
     (`EVD-0040`) — evolução terminológica, não conflito ativo, mas as duas formas históricas não
     são cobertas pelo enum do contrato de UI atual (`EVD-0009`).
  3. Enum de `criticidade` divergente entre o contrato de UI (3 valores: ALTA/MEDIA/BAIXA,
     `EVD-0012`) e a coluna operacional real em `AGENDA CEPRAEA` (5 valores observados, incluindo
     "Muito alta" e "A validar", `EVD-0025`) — registrado como `AMBIGUO` em `TERMO-011`, não
     resolvido por suposição de qual enum está desatualizado.
  4. Relação entre "Competição" e "Etapa" não está formalmente definida nesta fonte — registrado
     como `AMBIGUO` em `TERMO-007`.
  5. Possível divergência entre `R_STATUS` (aceita `NÃO` acentuado como forma válida) e o contrato
     de UI (proíbe `não` acentuado como valor de resposta) — não fica claro se a proibição do
     contrato é sobre a forma minúscula/informal ou também sobre a forma maiúscula acentuada;
     registrado em `REGRA-003.duvidas`.
  6. `GARANTIDO`/`CONDICIONAL` (nível de jogo) vs. `PENDENTE`/`PREVISTO` (nível de
     atividade/evento) em `3ª ETAPA CARIOCA 2026`: não fica claro se é um único enum de estado
     compartilhado entre granularidades ou dois vocabulários distintos — registrado em
     `TERMO-013.limitacoes`.
  7. Identificador de atleta possivelmente duplo: coluna `Nº` em RELAÇÃO NOMINAL CEPRAEA usa
     valores não sequenciais, diferente da numeração sequencial 1-19 usada nas matrizes mensais de
     disponibilidade — pode ser um identificador técnico estável distinto da posição de linha;
     não confirmado nesta fonte. Registrado em `TERMO-001.limitacoes`, relevante para uma futura
     identidade definitiva (`candidatos/identidades.md`).
  8. Possível alias: nomes usados nas matrizes mensais podem ser formas curtas de nomes legais
     mais completos usados em RELAÇÃO NOMINAL CEPRAEA — não comparado literalmente (tratamento de
     dado sensível); registrado em `TERMO-001.limitacoes`.
  9. Dois resumos gerais de temporada divergentes: aba oculta `ANÁLISE DOS JOGOS` registra 23
     jogos/14 vitórias/9 derrotas; aba visível `ANÁLISE JOGOS` registra 19 jogos/12 vitórias/7
     derrotas — ambos internamente consistentes com sua própria quebra por
     competição/adversário, mas mutuamente divergentes para a mesma temporada. Não fica claro
     qual é autoritativo, nem se a diferença reflete um corte de data distinto ou um critério de
     contagem distinto. Registrado como `AMBIGUO` em `TERMO-008.limitacoes` e
     `REGRA-008.duvidas`, não resolvido por suposição — ver `EVD-0044`.
  10. Divergência estrutural de elenco entre abas mensais históricas de 2024 e a relação atual de
      19 atletas (`AGOSTO - 2026`) — nomes presentes em abas antigas ausentes da relação atual e
      vice-versa, consistente com entrada/saída de elenco ao longo de ~2 anos, não modelada como
      ciclo de vida nesta fase. Registrado em `TERMO-001.limitacoes` — ver `EVD-0041`.
  11. Terceira variante histórica de vocabulário de resposta (`Tentarei`), presente em abas de
      2024, não coberta pelo enum do contrato de UI atual nem pela observação de `R_STATUS`.
      Registrado em `TERMO-002.limitacoes` — ver `EVD-0039`.
  12. Coluna de status por etapa no bloco "Formula engine" de `AGENDA CEPRAEA` usa apenas 3
      valores (`OPERACIONAL`/`ATENÇÃO`/`NÃO PARTICIPA`) — não fica claro se é o mesmo enum de 5
      valores de `TERMO-009` em forma reduzida ou um indicador distinto. Registrado em
      `TERMO-009.limitacoes`, não resolvido por suposição — ver `EVD-0048`.
  13. `TERMO-014` (ação técnica recomendada, `AGENDA CEPRAEA`) não distingue se é calculada pela
      mesma camada "Formula engine" que gera os demais indicadores da aba ou preenchida
      manualmente — a fonte só rotula "Formula engine" explicitamente nas colunas adjacentes,
      não na coluna desta recomendação. Registrado em `TERMO-014.limitacoes`.
- Artefatos técnicos afetados: nenhum (fora de escopo desta fase — seção 3 do plano).
- Testes afetados: nenhum (fora de escopo desta fase).
- Estado final do arquivo: `CONCLUIDO` — critério revisado quatro vezes após revisão adversarial:
  as três abas antes excluídas por inferência de nome, as duas abas que ainda estavam parcialmente
  lidas, as 17 abas mensais históricas antes amostradas por inferência de padrão recorrente, a aba
  `ANÁLISE DOS JOGOS` omitida por colisão de nome, e `AGENDA CEPRAEA` (amostrada por corte de linha
  sob a mesma inferência de padrão recorrente, hoje refutada) foram todas efetivamente lidas por
  completo, com evidência reproduzível do último dado presente em cada caso. Nenhuma das 45 abas
  permanece não inspecionada.
- Próxima ação: nenhuma decorrente diretamente — mas `AC-004` (`CEPRAEA DATABASE.xlsx`) deve
  testar a hipótese de ser a fonte materializada por trás de `CEPRAEA DATABASE!DB_EXPORT_FRONTEND`,
  `DB_PRESENCA_FATUAL`/`DB_INDICADORES_DISPONIBILIDADE` (`EVD-0006`, `EVD-0008`, `EVD-0027`) e
  `DB_PARTICIPACAO_JOGO` (`EVD-0042`) citados nesta fonte, e também deve testar se resolve a
  divergência de totais de jogos do conflito 9; `AC-016` (`CEPRAEA ABRIL 2026.xlsx`) deve testar se
  é a fonte real do contrato de UI `CEPRAEA_UI_CONTRACT_v1_2`, que se autodeclara originário de
  "CEPRAEA ABRIL 2026" mesmo aparecendo copiado nesta fonte (`EVD-0010`).

## Dados sensíveis

Nomes completos reais de atletas aparecem em `DISPONIBILIDADE BR e RJ`, `AGOSTO - 2026`, `ANÁLISE
JOGOS`, `ANÁLISE DOS JOGOS`, `AGENDA CEPRAEA`, `AGENDA TÉCNICA V2`, `RELAÇÃO NOMINAL CEPRAEA`
(dentro de `3ª ETAPA CARIOCA 2026`, em formato de nome legal mais completo que o usado nas abas
mensais), as 17 abas mensais históricas (`JUNHO - 2026` a `JUNHO 2024`) e uma entrada do
`📑_CHANGELOG`. Conforme `docs/standards/guia_estilo_documentação.md` (que cita explicitamente
"nomes reais de atletas, CPFs" como exemplo de dado que exige dados simulados em vez do valor
real), nenhum nome é reproduzido literalmente em nenhum artefato desta fase — só estrutura,
contagens e o padrão de dado (ver `EVD-0013`, `EVD-0018`, `EVD-0038`, `EVD-0041`, `EVD-0042`,
`EVD-0047`, `EVD-0048`). Classificação: `PII` (não é credencial, mas é dado pessoal identificável).

## Critério de saída

- [x] Identidade e classe de autoridade registradas.
- [x] Escopo usado registrado, sem escopo descartado remanescente — todas as 45 abas foram lidas
      (seção "Seleção de conteúdo").
- [x] Trechos relevantes localizados (48 fragmentos em `evidencias/registro_evidencias.md`).
- [x] Interpretação separada do texto original (`trecho_literal` vs. `semantic_evidence`/prosa).
- [x] Conflitos e precedências resolvidos ou explicitamente bloqueados (13 itens registrados como
      `AMBIGUO`/dúvida, nenhum resolvido por suposição).
- [x] Conceitos, regras e fatos encaminhados aos artefatos corretos (glossário, regras,
      candidatos/invariantes.md).
- [x] Nenhuma conclusão excede o que a fonte sustenta.
- [x] Nenhum dado sensível transcrito literalmente.

```json
{
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "nome_arquivo_original": "CEPRAEA AGOSTO 2026.xlsx",
  "caminho_local": ".drive/CEPRAEA BEACH PRO/CEPRAEA AGOSTO 2026.xlsx",
  "hash_sha256": "cb179a19a9f7e313e08e9577954035d0a5ad8be37ea68ae325cef03df413ef41",
  "id_drive": null,
  "tipo_arquivo": "xlsx",
  "idioma": "pt-BR",
  "tipo_fonte": "OPERACIONAL",
  "autoridade_fonte": "PRIMARIA",
  "proveniencia_fonte": "ORIGINAL",
  "estado_fonte": "VIGENTE",
  "estado_processamento": "CONCLUIDO",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "Nomes completos reais de atletas (PII, não credencial) aparecem em múltiplas abas. Nenhum nome é reproduzido literalmente em dossiê, evidências, glossário ou regras — apenas estrutura, contagens e o padrão observado, conforme docs/standards/guia_estilo_documentação.md.",
  "conceitos_encontrados": [
    "TERMO-001", "TERMO-002", "TERMO-003", "TERMO-004", "TERMO-005",
    "TERMO-006", "TERMO-007", "TERMO-008", "TERMO-009", "TERMO-010", "TERMO-011",
    "TERMO-012", "TERMO-013", "TERMO-014"
  ],
  "regras_encontradas": ["REGRA-001", "REGRA-002", "REGRA-003", "REGRA-004", "REGRA-005", "REGRA-006", "REGRA-007", "REGRA-008"],
  "conflitos_ou_duvidas": [
    "Rótulo 'CONFIRMAÇÃO DE PRESENÇA' (JULHO - 2026) vs. 'DECLARAÇÃO DE DISPONIBILIDADE' (AGOSTO - 2026) para a mesma matriz de resposta — ver TERMO-002.",
    "Vocabulário de resposta: três gerações históricas confirmadas por leitura integral — 'Ok'/'Out'/'Talvez' predominante por ~2 anos (JUNHO 2024 a ABRIL 2026), variante 'Tentarei' no mesmo período, 'SIM'/'NAO'/'TALVEZ' só a partir de JUNHO - 2026 — evolução terminológica, não conflito ativo.",
    "Enum de criticidade: 3 valores no contrato de UI vs. 4 valores no modelo/template (AGENDA TÉCNICA MODELO) vs. 5 valores observados na coluna operacional real (AGENDA CEPRAEA) — ver TERMO-011.",
    "Relação entre 'Competição' e 'Etapa' não formalmente definida — ver TERMO-007.",
    "Forma aceita de 'NÃO' (com acento) em R_STATUS vs. proibição de 'não' acentuado no contrato de UI — ver REGRA-003.",
    "GARANTIDO/CONDICIONAL (nível de jogo) vs. PENDENTE/PREVISTO (nível de atividade/evento) em 3ª ETAPA CARIOCA 2026 — mesmo enum ou vocabulários distintos, não resolvido — ver TERMO-013.",
    "Identificador de atleta possivelmente duplo: 'Nº' não sequencial em RELAÇÃO NOMINAL CEPRAEA vs. numeração sequencial 1-19 nas matrizes mensais — ver TERMO-001.",
    "Possível alias entre nomes curtos (matrizes mensais) e nomes legais completos (RELAÇÃO NOMINAL CEPRAEA) — não comparado literalmente — ver TERMO-001.",
    "Dois resumos gerais de temporada divergentes: aba oculta ANÁLISE DOS JOGOS registra 23 jogos/14 vitórias/9 derrotas; aba visível ANÁLISE JOGOS registra 19 jogos/12 vitórias/7 derrotas — ambos internamente consistentes, mutuamente divergentes, não resolvido qual é autoritativo — ver TERMO-008, REGRA-008.",
    "Divergência estrutural de elenco entre abas mensais históricas (2024) e a relação atual de 19 atletas — consistente com entrada/saída de elenco ao longo do tempo, não modelada como ciclo de vida — ver TERMO-001.",
    "Terceira variante histórica de vocabulário de resposta ('Tentarei'), não coberta pelo enum do contrato de UI atual — ver TERMO-002.",
    "Coluna de status por etapa no bloco 'Formula engine' de AGENDA CEPRAEA usa apenas 3 valores (OPERACIONAL/ATENÇÃO/NÃO PARTICIPA) — não resolvido se é o mesmo enum de 5 valores de TERMO-009 em forma reduzida — ver TERMO-009.",
    "TERMO-014 (ação técnica recomendada) não distingue se é calculada pela camada 'Formula engine' ou preenchida manualmente — ver TERMO-014."
  ],
  "evidencia": {
    "comando_ou_metodo": "perl -MIO::Uncompress::Unzip=unzip (extração de xl/sharedStrings.xml e xl/worksheets/sheet1..45.xml) + parser Node próprio (resolução de shared strings, decodificação de células) + sha256sum/node:crypto para hash",
    "resultado": "45 abas identificadas via xl/workbook.xml (4 visíveis, 41 ocultas); todas as 45 abas foram abertas e inspecionadas ao longo de quatro rodadas de leitura, incluindo varredura completa e sem corte de linha em AGENDA CEPRAEA (1000 linhas de capacidade, 44 com conteúdo); 48 fragmentos de evidência extraídos (28 na primeira passada + 6 na segunda + 4 completando duas abas parcialmente lidas na terceira + 6 completando as 17 abas mensais históricas e ANÁLISE DOS JOGOS + 4 completando AGENDA CEPRAEA na quarta); hash SHA-256 verificado por dois métodos independentes concordantes",
    "repository_evidence": {
      "action_ref": "AC-001"
    },
    "limitacoes": []
  },
  "proxima_acao": "AC-004 deve testar se CEPRAEA DATABASE.xlsx é a fonte materializada citada como DB_EXPORT_FRONTEND/DB_PRESENCA_FATUAL/DB_INDICADORES_DISPONIBILIDADE/DB_PARTICIPACAO_JOGO (EVD-0006/0008/0027/0042), e se resolve a divergência de totais de jogos (23 vs. 19) entre ANÁLISE DOS JOGOS e ANÁLISE JOGOS. AC-016 deve testar se CEPRAEA ABRIL 2026.xlsx é a origem real do contrato de UI CEPRAEA_UI_CONTRACT_v1_2 (EVD-0010)."
}
```
