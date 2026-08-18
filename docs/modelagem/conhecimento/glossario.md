# Glossário

Só significado dos termos — responde "o que este termo quer dizer?" (seção 4.6 do plano). Um
bloco `json` por `TERMO-NNN`, validado contra `schemas/schema_termo.json`. O modelo conceitual
(existência, identidade, relações, regras, comportamento) fica em `dominio/modelo_canonico_dominio.md`,
não aqui.

## `AC-001` — `CEPRAEA AGOSTO 2026.xlsx`

`AD-03` roda nesta ação (seção 8 do plano): todo termo abaixo tem `semantic_evidence` explicando
por que o dado corresponde a um conceito do domínio, nunca apenas "existe uma coluna com esse
nome" — resultado registrado em `DEC-007`.

```json
{
  "id_termo": "TERMO-001",
  "termo_preferencial": "atleta",
  "nome_canonico": "Atleta",
  "classificacao": "ENTIDADE",
  "definicao": "Pessoa vinculada operacionalmente ao CEPRAEA-BEACH-PRO com papel ATLETA, sujeito recorrente de eventos e indicadores do domínio (disponibilidade, convocação, participação em jogos, criticidade).",
  "contexto_valido": "Toda a operação esportiva registrada nesta fonte.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": ["Usuário autenticado (identidade técnica de acesso, não observada nesta fonte)"],
  "sinonimos": [],
  "termos_relacionados": ["TERMO-004", "TERMO-011"],
  "fonte": ["EVD-0013", "EVD-0019", "EVD-0022", "EVD-0025", "EVD-0041"],
  "valores_permitidos": null,
  "temporalidade": null,
  "natureza_e_privacidade": "Nome completo é dado pessoal — nunca transcrito literalmente nos artefatos desta fase (ver EVD-0013).",
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [
    "A coluna 'Nº' em RELAÇÃO NOMINAL CEPRAEA (3ª ETAPA CARIOCA 2026, EVD-0038) usa valores não sequenciais (ex.: 3, 4, 6, 85), diferentes da numeração sequencial 1-19 usada como coluna 'A' nas matrizes mensais de disponibilidade — pode ser um identificador técnico estável (ex.: número de camisa/matrícula) distinto da posição de linha, mas isso não está confirmado nesta fonte. Registrado como observação para uma futura identidade definitiva (candidatos/identidades.md), não resolvido aqui.",
    "Nomes usados nas matrizes mensais podem ser apelidos/formas curtas, enquanto RELAÇÃO NOMINAL CEPRAEA usa nomes legais mais completos — possível caso de alias a reconciliar, não confirmado nesta fonte (nomes não comparados literalmente aqui, por tratamento de dado sensível).",
    "A leitura integral das abas mensais históricas (JUNHO 2024 a NOVEMBRO E DEZEMBRO 2024, EVD-0041) mostra nomes que não constam da relação de 19 atletas de AGOSTO - 2026, e vice-versa — consistente com entrada/saída de elenco ao longo de dois anos, não modelada como ciclo de vida nesta fase."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura estrutural de múltiplas abas via extração de xl/worksheets/*.xml",
      "resultado": "19 linhas de atleta presentes de forma consistente em quatro abas independentes (DISPONIBILIDADE BR e RJ, PAINEL DATABASE, ANÁLISE JOGOS, AGENDA CEPRAEA), sempre como sujeito de disponibilidade, resultado de jogo ou classificação de risco — não apenas nome de coluna isolado"
    },
    "semantic_evidence": "O conceito aparece como sujeito ativo de múltiplos eventos e indicadores distintos e independentes (declarar disponibilidade, participar de jogo, receber classificação de criticidade), correspondência recorrente que uma coluna isolada não teria."
  }
}
```

```json
{
  "id_termo": "TERMO-002",
  "termo_preferencial": "disponibilidade declarada",
  "nome_canonico": "Disponibilidade declarada",
  "classificacao": "EVENTO",
  "definicao": "Resposta declarada por uma atleta indicando disponibilidade ou compromisso para um treino ou etapa competitiva — SIM, NAO ou TALVEZ (R_STATUS, EVD-0001).",
  "contexto_valido": "Treinos semanais e etapas competitivas da temporada.",
  "contexto_invalido": "Nunca representa comparecimento factual (ver TERMO-003).",
  "inclusoes": ["Resposta SIM/NAO/TALVEZ a um treino ou etapa"],
  "exclusoes": ["Presença factual pós-sessão (TERMO-003)", "Convocação do treinador (TERMO-006)"],
  "sinonimos": ["compromisso declarado"],
  "termos_relacionados": ["TERMO-003", "TERMO-006"],
  "fonte": ["EVD-0001", "EVD-0003", "EVD-0005", "EVD-0009", "EVD-0014", "EVD-0039", "EVD-0040"],
  "valores_permitidos": "SIM | NAO | TALVEZ (formas alternativas como 'sim' minúsculo, 'não' acentuado como valor de resposta, 'N', 'OK', 'confirmado' ou texto livre são explicitamente proibidas — EVD-0009). Este enum é o vigente a partir de JUNHO - 2026; abas históricas usam vocabulários anteriores (ver limitações).",
  "temporalidade": "Uma resposta por atleta por evento (treino/etapa); respostas manuais não devem ser sobrescritas sem autorização humana (EVD-0004).",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [
    "O rótulo textual do cabeçalho para este conceito varia entre abas — ver TERMO-003 e a nota de conflito no dossiê de SRC-001.",
    "Leitura integral (não amostral) das 17 abas mensais históricas confirma três gerações de vocabulário de resposta: 'Ok'/'Out'/'Talvez' predominante por ~2 anos (JUNHO 2024 a ABRIL 2026), uma variante adicional 'Tentarei' no mesmo período (EVD-0039), e 'SIM'/'NAO'/'TALVEZ' apenas a partir de JUNHO - 2026 (EVD-0040). O enum atual do contrato de UI (EVD-0009) não cobre as duas formas históricas."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_STATUS, R_META e do contrato de UI (Página16)",
      "resultado": "três fontes internas independentes (tabela de status, metadados de reconciliação, contrato de interface) definem e reforçam o mesmo enum e a mesma semântica declarativa"
    },
    "semantic_evidence": "Não é um nome de coluna isolado: R_META registra explicitamente 'availability_semantics: declaracao_nao_presenca' com a observação 'SIM/NAO/TALVEZ indicam disponibilidade ou compromisso, não comparecimento factual' (EVD-0005) — uma definição semântica explícita, não uma inferência do agente a partir do cabeçalho."
  }
}
```

```json
{
  "id_termo": "TERMO-003",
  "termo_preferencial": "presença factual",
  "nome_canonico": "Presença factual",
  "classificacao": "FATO_HISTORICO",
  "definicao": "Registro factual de comparecimento de uma atleta a uma sessão, distinto e não derivável automaticamente da disponibilidade declarada.",
  "contexto_valido": "Pós-sessão, mediante autorização humana (EVD-0006).",
  "contexto_invalido": "Nunca inferida a partir de SIM/NAO/TALVEZ.",
  "inclusoes": [],
  "exclusoes": ["Disponibilidade declarada (TERMO-002)"],
  "sinonimos": ["comparecimento factual"],
  "termos_relacionados": ["TERMO-002"],
  "fonte": ["EVD-0006", "EVD-0003", "EVD-0015"],
  "valores_permitidos": null,
  "temporalidade": "Só existe após a sessão ocorrer; não é projetável a partir de disponibilidade futura.",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": ["CEPRAEA DATABASE!DB_PRESENCA_FATUAL (fonte canônica citada, não observada diretamente nesta fonte — ver AC-004)"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["Esta fonte (SRC-001) não contém registros de presença factual em si — só a regra que a distingue de disponibilidade e a referência à sua fonte canônica em outro arquivo."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_META (parametros availability_semantics_decision e canonical_presence_source)",
      "resultado": "duas linhas de metadados definem explicitamente presença como estado distinto, com fonte canônica própria e exigência de autorização humana"
    },
    "semantic_evidence": "R_META registra 'availability_semantics_decision: APPROVED_BY_HUMAN_STEWARD — Disponibilidade e presença factual são estados distintos' (EVD-0003) — uma decisão semântica explícita da fonte, coerente com a distinção já estabelecida em modelagem_dados_agente.md/modelagem_dominio_dados.md, agora com evidência operacional direta e independente."
  }
}
```

```json
{
  "id_termo": "TERMO-004",
  "termo_preferencial": "função esportiva",
  "nome_canonico": "Função esportiva (posição)",
  "classificacao": "PAPEL",
  "definicao": "Posição tática exercida por uma atleta em quadra — GOLEIRA, DEFESA, ATAQUE, CORINGA ou INDEFINIDA (R_FUNCOES, EVD-0002).",
  "contexto_valido": "Escalação e planejamento tático.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": ["papel_operacional (ATLETA/TREINADOR, INV-001) — dimensão distinta: acesso ao sistema, não posição tática"],
  "sinonimos": ["posição"],
  "termos_relacionados": ["TERMO-001"],
  "fonte": ["EVD-0002", "EVD-0019", "EVD-0025"],
  "valores_permitidos": "GOLEIRA | DEFESA | ATAQUE | CORINGA | INDEFINIDA (R_FUNCOES); AGENDA CEPRAEA observa também subposições de ataque/defesa (ex.: Central, Lateral esquerda/direita, Pivô, Defensora solta/base/cobertura) que R_FUNCOES não lista — ver dúvida registrada no dossiê.",
  "temporalidade": "Sujeita a correção humana registrada (ex.: EVD-0018, correção de função aplicada em 2026-06-22).",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_FUNCOES, PAINEL DATABASE, coluna R de AGENDA CEPRAEA e do changelog operacional",
      "resultado": "o mesmo conjunto de valores aparece de forma consistente em três abas distintas com propósitos diferentes (catálogo de referência, painel agregado, coluna operacional), e uma correção humana real deste campo está registrada no changelog"
    },
    "semantic_evidence": "R_FUNCOES é explicitamente um catálogo de reconciliação ('Equivale a Goleira nas abas atuais'), não uma coluna isolada — e o changelog (EVD-0018) mostra o próprio treinador corrigindo o valor de uma atleta, confirmando que o campo carrega significado operacional decisório, não apenas rótulo textual."
  }
}
```

```json
{
  "id_termo": "TERMO-005",
  "termo_preferencial": "próximo treino",
  "nome_canonico": "Próximo treino",
  "classificacao": "PROJECAO",
  "definicao": "Projeção calculada automaticamente do próximo treino agendado, a partir de data/hora futura e status planejado.",
  "contexto_valido": "Sempre um único treino, recalculado conforme o tempo avança.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": [],
  "sinonimos": [],
  "termos_relacionados": ["TERMO-002"],
  "fonte": ["EVD-0007", "EVD-0020"],
  "valores_permitidos": null,
  "temporalidade": "Recalculada continuamente; 'treino do mesmo dia já encerrado não permanece como próximo' (EVD-0007).",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_META (next_training_rule) e da aba PRÓXIMO TREINO",
      "resultado": "regra de cálculo explícita em R_META e painel dedicado com data/horário/status e composição por disponibilidade declarada, coerentes entre si (ambos apontam 13/08/2026)"
    },
    "semantic_evidence": "A aba dedicada e a regra de cálculo em R_META concordam sobre o mesmo valor calculado (13/08/2026), evidenciando um conceito derivado real, não um rótulo estático de coluna."
  }
}
```

```json
{
  "id_termo": "TERMO-006",
  "termo_preferencial": "convocação",
  "nome_canonico": "Convocação",
  "classificacao": "EVENTO",
  "definicao": "Ato do treinador chamando atletas específicas para uma etapa ou jogo, distinto da disponibilidade declarada por elas.",
  "contexto_valido": "Etapas competitivas, a partir das atletas disponíveis.",
  "contexto_invalido": "Disponibilidade declarada não constitui convocação.",
  "inclusoes": [],
  "exclusoes": ["Disponibilidade declarada (TERMO-002)"],
  "sinonimos": ["chamada"],
  "termos_relacionados": ["TERMO-002"],
  "fonte": ["EVD-0021", "EVD-0038"],
  "valores_permitidos": "Observado em instância real: status 'Convocada' (RELAÇÃO NOMINAL CEPRAEA, EVD-0038).",
  "temporalidade": "Ocorre após disponibilidade ser declarada, por ação humana do treinador.",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["Duas evidências desta fonte mostram estágios diferentes do mesmo conceito: DIA DO JOGO mostra a estrutura vazia ('Aguardando convocação do treinador', etapa futura sem convocação ainda feita); RELAÇÃO NOMINAL CEPRAEA (3ª ETAPA CARIOCA 2026) mostra uma instância real já concluída (status 'Convocada' para uma lista de atletas, etapa já ocorrida). O ciclo de vida completo entre os dois estados não está formalizado nesta fonte."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura da aba 'DIA DO JOGO' (seção CONVOCADAS) e da aba '3ª ETAPA CARIOCA 2026' (seção RELAÇÃO NOMINAL CEPRAEA)",
      "resultado": "duas fontes complementares: uma mostra a estrutura de convocação vazia/pendente, a outra mostra uma instância real já concluída com status 'Convocada' atribuído a uma lista de atletas"
    },
    "semantic_evidence": "A seção é fisicamente distinta da matriz de disponibilidade e tem autoridade atribuída explicitamente ao treinador, coerente com a distinção convocação≠participação já estabelecida em modelagem_dados_agente.md. A instância real em RELAÇÃO NOMINAL CEPRAEA confirma que 'convocação' é um evento que de fato ocorre operacionalmente, não apenas uma estrutura de interface vazia."
  }
}
```

```json
{
  "id_termo": "TERMO-007",
  "termo_preferencial": "etapa competitiva",
  "nome_canonico": "Etapa competitiva",
  "classificacao": "ENTIDADE",
  "definicao": "Evento competitivo individual da temporada (ex.: uma etapa de circuito estadual ou brasileiro), unidade sobre a qual disponibilidade é declarada e resultado é registrado.",
  "contexto_valido": "Temporada 2026.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": [],
  "sinonimos": ["etapa"],
  "termos_relacionados": ["TERMO-002", "TERMO-008"],
  "fonte": ["EVD-0013", "EVD-0022", "EVD-0025", "EVD-0046"],
  "valores_permitidos": null,
  "temporalidade": "Datada; algumas etapas podem ser marcadas como sem participação do CEPRAEA (ex.: 'CEPRAEA NÃO PARTICIPARÁ'). AGENDA CEPRAEA registra três datas distintas por etapa: data do evento, prazo de inscrição ('Inscrição até') e prazo de relação nominal ('Relação nominal até', EVD-0046).",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "AMBIGUO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [
    "Relação entre 'Etapa' e 'Competição' não está totalmente resolvida nesta fonte: ANÁLISE JOGOS agrupa etapas sob rótulos como 'Circuito Estadual de Handebol de Praia 2026 - 1ª Etapa', sugerindo que etapa é subunidade de uma competição/circuito maior — mas DISPONIBILIDADE BR e RJ e AGENDA CEPRAEA usam 'Etapa' e nomes de competição (ex.: 'Copa do Brasil') lado a lado como colunas do mesmo nível, sem hierarquia explícita marcada."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "comparação de cabeçalhos entre DISPONIBILIDADE BR e RJ, AGENDA CEPRAEA e ANÁLISE JOGOS",
      "resultado": "13 colunas de etapa/competição nomeadas de forma consistente entre as três abas, mas sem campo explícito de hierarquia entre 'competição' e 'etapa'"
    },
    "semantic_evidence": "O termo aparece de forma consistente como unidade de disponibilidade e de resultado em três abas operacionais independentes — evidência real de um conceito de domínio, mas cuja relação com 'competição' fica registrada como AMBIGUO em vez de presumida (antiobjetivo de modelagem_dominio_dados.md §37)."
  }
}
```

```json
{
  "id_termo": "TERMO-008",
  "termo_preferencial": "jogo",
  "nome_canonico": "Jogo (resultado)",
  "classificacao": "FATO_HISTORICO",
  "definicao": "Partida realizada dentro de uma etapa competitiva, com resultado factual (vitória/derrota, sets, adversário) distinto da programação da etapa.",
  "contexto_valido": "Etapas já realizadas.",
  "contexto_invalido": "Etapa programada e ainda não realizada não é um jogo (ver STATUS 'ETAPA PREVISTA — TABELA PENDENTE', EVD-0021).",
  "inclusoes": [],
  "exclusoes": ["Etapa competitiva programada e não realizada"],
  "sinonimos": ["partida"],
  "termos_relacionados": ["TERMO-007"],
  "fonte": ["EVD-0022", "EVD-0042", "EVD-0044"],
  "valores_permitidos": null,
  "temporalidade": "Fato histórico, registrado após a realização.",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": ["CEPRAEA DATABASE!DB_PARTICIPACAO_JOGO (fonte citada para o cálculo de participação real em jogo, REGRA-008 — não observada diretamente nesta fonte, ver AC-004)"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["A aba oculta 'ANÁLISE DOS JOGOS' (distinta da aba visível 'ANÁLISE JOGOS', omitida por colisão de nome na primeira leitura) registra um resumo geral da mesma temporada com totais diferentes (23 jogos, 14 vitórias, 9 derrotas) do resumo já usado como fonte deste termo (19 jogos, 12 vitórias, 7 derrotas) — ambos internamente consistentes com sua própria quebra por competição/adversário, mas divergentes entre si. Não fica claro qual resumo é autoritativo; não resolvido por suposição — ver EVD-0044 e REGRA-008.duvidas."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de ANÁLISE JOGOS, resumo geral e por competição; leitura complementar de ANÁLISE DOS JOGOS (oculta) na rodada de completude",
      "resultado": "totais agregados (19 jogos, 12 vitórias, 7 derrotas, sets pró/contra) e detalhamento por competição com contagens próprias (J/V/D/%), consistentes entre si; aba oculta homônima com resumo geral divergente (23/14/9), também internamente consistente"
    },
    "semantic_evidence": "A aba distingue explicitamente programação ('ETAPA PREVISTA — TABELA PENDENTE' em DIA DO JOGO) de resultado factual já ocorrido (ANÁLISE JOGOS) — a mesma distinção programação≠resultado realizado já documentada nas fontes de referência, agora com evidência operacional própria."
  }
}
```

```json
{
  "id_termo": "TERMO-009",
  "termo_preferencial": "status de risco funcional",
  "nome_canonico": "Status de risco funcional",
  "classificacao": "INDICADOR",
  "definicao": "Indicador derivado, calculado a partir de disponibilidade por função, que resume o risco operacional do elenco em um valor textual com ícone.",
  "contexto_valido": "Painel de comando (AGENDA CEPRAEA / contrato de UI).",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": ["Cálculo manual — 'manual_risk_typing' é proibido pelo contrato de UI"],
  "sinonimos": ["risco funcional"],
  "termos_relacionados": ["TERMO-004", "TERMO-010"],
  "fonte": ["EVD-0011", "EVD-0048"],
  "valores_permitidos": "🟢 OPERACIONAL | 🟡 ATENÇÃO | 🟠 DEFESA CURTA | 🔴 SEM GOLEIRA | 🔴 CRÍTICO (sempre com ícone + texto; cor isolada é proibida)",
  "temporalidade": null,
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [
    "Esta fonte não mostra a fórmula de cálculo em si, só o contrato que define o enum e proíbe digitação manual.",
    "O bloco 'Formula engine' de AGENDA CEPRAEA usa uma coluna de status por etapa com apenas três valores observados (OPERACIONAL, ATENÇÃO, NÃO PARTICIPA, EVD-0048) — não fica claro se é o mesmo enum de 5 valores deste termo em forma reduzida, ou um indicador coarser distinto. Não resolvido por suposição."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura do contrato de UI (Página16), bloco risk_system",
      "resultado": "enum de 5 valores com regra explícita de apresentação (ícone+texto, nunca só cor) e proibição de digitação manual"
    },
    "semantic_evidence": "O contrato classifica explicitamente 'manual_risk_typing' como prática proibida ('guardrails.forbidden'), o que só faz sentido se o valor for um indicador calculado, não um rótulo livre — confirma se tratar de um conceito derivado do domínio, não um nome de coluna."
  }
}
```

```json
{
  "id_termo": "TERMO-010",
  "termo_preferencial": "índice de competitividade",
  "nome_canonico": "Índice de competitividade",
  "classificacao": "INDICADOR",
  "definicao": "Indicador percentual derivado, calculado a partir de disponibilidade, funções e criticidade, com geração manual explicitamente proibida.",
  "contexto_valido": "Painel de comando competitivo.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": [],
  "sinonimos": [],
  "termos_relacionados": ["TERMO-009", "TERMO-011"],
  "fonte": ["EVD-0012", "EVD-0048"],
  "valores_permitidos": "Percentual; faixas nomeadas: excelente (>=95%), competitivo (>=82%), atenção (>=65%), crítico (<65%).",
  "temporalidade": null,
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["Fórmula de cálculo exata não está nesta fonte, só as entradas, a saída e as faixas."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura do contrato de UI (Página16), bloco competitiveness_index; leitura complementar do bloco 'Formula engine' em AGENDA CEPRAEA na rodada de completude",
      "resultado": "três entradas nomeadas (disponibilidade, funções, criticidade), uma saída percentual e quatro faixas nomeadas com limiares numéricos explícitos; valores percentuais reais observados em AGENDA CEPRAEA (ex.: 90, 95, 83, 79, 88) com rótulo qualitativo correspondente, todos consistentes com as faixas do contrato de UI"
    },
    "semantic_evidence": "'manual_score_forbidden: true' só faz sentido para um valor calculado a partir de outros dados do domínio, e as três entradas citadas (disponibilidade, funções, criticidade) são, elas mesmas, conceitos já observados de forma independente nesta fonte (TERMO-002, TERMO-004, TERMO-011). Os valores reais de AGENDA CEPRAEA (EVD-0048) confirmam operacionalmente as faixas do contrato, não apenas a definição declarada."
  }
}
```

```json
{
  "id_termo": "TERMO-014",
  "termo_preferencial": "ação técnica recomendada",
  "nome_canonico": "Ação técnica recomendada",
  "classificacao": "ATRIBUTO",
  "definicao": "Recomendação textual de próximo passo para a comissão técnica em relação a uma atleta, associada a sua função esportiva, criticidade e disponibilidade declaradas.",
  "contexto_valido": "Painel de comando (AGENDA CEPRAEA), por atleta.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": [],
  "sinonimos": ["ação técnica"],
  "termos_relacionados": ["TERMO-001", "TERMO-004", "TERMO-011"],
  "fonte": ["EVD-0047"],
  "valores_permitidos": "Cinco valores distintos observados nesta fonte: 'Confirmar disponibilidade', 'Monitorar agenda da seleção', 'Garantir cobertura da posição', 'Validar função com comissão', 'Confirmar interesse' — não fica claro se é um enum fechado ou texto derivado com repetição observada; não confirmado nesta fonte.",
  "temporalidade": null,
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["Não fica claro se este valor é gerado por regra automática (como os indicadores do bloco 'Formula engine', colunas U-AD) ou preenchido manualmente pela comissão técnica — a fonte rotula 'Formula engine' explicitamente só nas colunas U-AD, não nas colunas R-T onde esta coluna aparece."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura integral de AGENDA CEPRAEA, colunas 'Função principal'/'Criticidade'/'Ação técnica', linhas 8-26",
      "resultado": "coluna dedicada com valor textual por atleta, ao lado de 'Função principal' e 'Criticidade' já observados de forma independente em outros termos"
    },
    "semantic_evidence": "O valor varia sistematicamente por atleta e aparenta correlação com a combinação de função/criticidade (ex.: atletas com criticidade mais alta em posições de cobertura recebem recomendações de garantia de posição) — sugere conceito derivado, não rótulo de coluna isolado, mas a regra exata de derivação não está na fonte."
  }
}
```

```json
{
  "id_termo": "TERMO-011",
  "termo_preferencial": "criticidade da atleta",
  "nome_canonico": "Criticidade da atleta",
  "classificacao": "ATRIBUTO",
  "definicao": "Classificação da importância estratégica de uma atleta para o elenco, usada como entrada de indicadores de risco e competitividade.",
  "contexto_valido": "Planejamento de elenco e cálculo de indicadores.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": [],
  "sinonimos": [],
  "termos_relacionados": ["TERMO-001", "TERMO-010"],
  "fonte": ["EVD-0012", "EVD-0025"],
  "valores_permitidos": "ALTA | MEDIA | BAIXA (contrato de UI, EVD-0012) — a coluna observada em AGENDA CEPRAEA (EVD-0025) usa também 'Muito alta' e 'A validar', não previstos no enum do contrato.",
  "temporalidade": null,
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "AMBIGUO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["Divergência entre o enum declarado no contrato de UI (3 valores) e os valores observados na coluna operacional real (5 valores, incluindo 'Muito alta' e 'A validar') — registrada como ambiguidade, não resolvida por suposição."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "comparação entre o bloco player_criticality do contrato de UI e a coluna S de AGENDA CEPRAEA",
      "resultado": "contrato declara 3 valores permitidos; dados operacionais reais usam 5 valores distintos, dois deles fora do enum declarado"
    },
    "semantic_evidence": "'critical_players_absent.must_increase_risk: true' no mesmo contrato confirma que o campo alimenta o cálculo de risco — é um conceito real e consequente, não um rótulo de coluna; a divergência de enum é registrada como AMBIGUO em vez de silenciosamente resolvida pelo agente."
  }
}
```

### Complemento — abas reabertas após achado do REVIEWER

```json
{
  "id_termo": "TERMO-012",
  "termo_preferencial": "adversário",
  "nome_canonico": "Adversário",
  "classificacao": "ENTIDADE",
  "definicao": "Equipe opositora enfrentada em um jogo específico dentro de uma etapa competitiva — distinta da equipe CEPRAEA.",
  "contexto_valido": "Confrontos dentro de etapas competitivas.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": ["Equipe CEPRAEA"],
  "sinonimos": [],
  "termos_relacionados": ["TERMO-007", "TERMO-008"],
  "fonte": ["EVD-0032", "EVD-0034"],
  "valores_permitidos": null,
  "temporalidade": null,
  "natureza_e_privacidade": "Nomes de equipes adversárias são entidades organizacionais, não pessoas — não tratados como PII (diferente de EVD-0013).",
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura da aba '3ª ETAPA CARIOCA 2026', seções JOGOS DO CEPRAEA e CRONOGRAMA GERAL DA COMPETIÇÃO",
      "resultado": "múltiplos confrontos nomeados envolvendo CEPRAEA e outras equipes (ex.: NR Beach, Niterói Rugby), inclusive confrontos entre terceiros não envolvendo CEPRAEA, confirmando que 'confronto' é uma estrutura própria da etapa, não um atributo unário do CEPRAEA"
    },
    "semantic_evidence": "A mesma etapa registra confrontos entre equipes terceiras (ex.: 'Rio Handbeach x ADM Maricá') sem qualquer relação direta com CEPRAEA — prova de que 'adversário'/'confronto' é modelado como estrutura da competição como um todo, já esperado por modelagem_dados_agente.md ('Adversário é diferente da equipe CEPRAEA'), agora com evidência operacional direta nesta fonte."
  }
}
```

```json
{
  "id_termo": "TERMO-013",
  "termo_preferencial": "status de confirmação de jogo",
  "nome_canonico": "Status de confirmação de jogo",
  "classificacao": "ESTADO",
  "definicao": "Estado de confirmação de um jogo programado dentro de uma etapa, indicando se sua realização depende de resultados de outros jogos.",
  "contexto_valido": "Jogos programados dentro de uma etapa com fase de classificação.",
  "contexto_invalido": null,
  "inclusoes": [],
  "exclusoes": [],
  "sinonimos": [],
  "termos_relacionados": ["TERMO-007", "TERMO-008"],
  "fonte": ["EVD-0032"],
  "valores_permitidos": "GARANTIDO | CONDICIONAL (observados no nível de jogo); PENDENTE | PREVISTO (observados no nível de atividade/evento — pode ser o mesmo enum em granularidades diferentes ou dois enums distintos; não resolvido nesta fonte).",
  "temporalidade": "Jogos da fase de grupos nascem GARANTIDO; jogos de fases eliminatórias nascem CONDICIONAL até a classificação ser decidida.",
  "natureza_e_privacidade": null,
  "ativos_tecnicos": [],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "limitacoes": ["Não fica claro nesta fonte se GARANTIDO/CONDICIONAL (nível de jogo) e PENDENTE/PREVISTO (nível de atividade/evento) são o mesmo enum ou dois vocabulários de estado distintos — registrado como limitação, não resolvido por suposição."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura da aba '3ª ETAPA CARIOCA 2026', seções CRONOGRAMA OPERACIONAL CEPRAEA e JOGOS DO CEPRAEA",
      "resultado": "jogos da fase de grupos (J1, J5) aparecem sempre como GARANTIDO; jogos de mata-mata (J13-J17) aparecem sempre como CONDICIONAL, com observação explícita da condição ('Se classificar', 'Se disputar 5º/6º')"
    },
    "semantic_evidence": "A correlação sistemática entre fase do torneio e valor do status (nunca um jogo de grupo aparece CONDICIONAL, nunca um jogo eliminatório aparece GARANTIDO sem qualificação) evidencia uma regra de domínio real — não uma etiqueta arbitrária por jogo."
  }
}
```
