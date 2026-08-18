# Registro de regras

Um bloco `json` por `REGRA-NNN`, validado contra `schemas/schema_regra.json`. Cada regra rastreável
até fragmentos de evidência específicos (`EVD-NNNN`), nunca até uma fonte inteira.

## `AC-001` — `CEPRAEA AGOSTO 2026.xlsx`

```json
{
  "id_regra": "REGRA-001",
  "fonte": ["EVD-0003", "EVD-0005", "EVD-0006"],
  "texto_original": "Disponibilidade e presença factual são estados distintos.",
  "tipo": "DEFINICAO",
  "sujeito": "disponibilidade declarada",
  "acao": "não implica",
  "objeto": "presença factual",
  "condicoes": [],
  "excecoes": [],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-002", "TERMO-003"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_META, parâmetros availability_semantics_decision/availability_semantics/canonical_presence_source",
      "resultado": "três parâmetros de metadados, todos apontando na mesma direção, um deles explicitamente marcado APPROVED_BY_HUMAN_STEWARD"
    }
  }
}
```

```json
{
  "id_regra": "REGRA-002",
  "fonte": ["EVD-0001"],
  "texto_original": "FALTA JUSTIFICADA: Estado factual pós-sessão; não usar como disponibilidade futura.",
  "tipo": "PROIBICAO",
  "sujeito": "estado FALTA JUSTIFICADA",
  "acao": "não deve ser usado como",
  "objeto": "disponibilidade futura",
  "condicoes": [],
  "excecoes": [],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-002", "TERMO-003"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_STATUS, linha 5",
      "resultado": "observação textual explícita associada ao valor FALTA JUSTIFICADA na tabela de referência"
    }
  }
}
```

```json
{
  "id_regra": "REGRA-003",
  "fonte": ["EVD-0009"],
  "texto_original": "availability_values: allowed: [SIM, NAO, TALVEZ]; forbidden: [sim, não, N, OK, confirmado, free_text]",
  "tipo": "CLASSIFICACAO",
  "sujeito": "resposta de disponibilidade",
  "acao": "deve usar exclusivamente",
  "objeto": "SIM, NAO ou TALVEZ",
  "condicoes": [],
  "excecoes": [],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": "Valores como 'sim' minúsculo, 'não' acentuado como resposta, 'N', 'OK', 'confirmado' ou texto livre são explicitamente proibidos pelo contrato de UI.",
  "conceitos_afetados": ["TERMO-002"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": ["R_STATUS (EVD-0001) também lista 'NÃO' (com acento) como forma aceita, tratando 'NAO' como 'forma canônica sem acento' — o contrato de UI (EVD-0009) proíbe 'não' acentuado como valor de resposta. Não fica claro se a proibição do contrato se refere apenas a entrada minúscula/informal ou também à forma maiúscula acentuada usada em R_STATUS; registrado como dúvida, não resolvido por suposição."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura do contrato de UI (Página16), bloco availability_values",
      "resultado": "lista explícita de valores permitidos e proibidos"
    }
  }
}
```

```json
{
  "id_regra": "REGRA-004",
  "fonte": ["EVD-0004"],
  "texto_original": "Não sobrescrever SIM/NAO/NÃO/TALVEZ/vazio; estados factuais exigem autorização humana.",
  "tipo": "PROIBICAO",
  "sujeito": "processo automatizado de reconciliação",
  "acao": "não deve sobrescrever",
  "objeto": "respostas manuais de disponibilidade (SIM/NAO/NÃO/TALVEZ/vazio)",
  "condicoes": ["ausência de autorização humana explícita"],
  "excecoes": [],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-002"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_META, parâmetro manual_input_policy",
      "resultado": "política explícita 'preservar', com observação nomeando os valores protegidos"
    }
  }
}
```

```json
{
  "id_regra": "REGRA-005",
  "fonte": ["EVD-0007"],
  "texto_original": "next_training_rule: data_hora_futura_e_status_planejado — Treino do mesmo dia já encerrado não permanece como próximo.",
  "tipo": "CALCULO",
  "sujeito": "próximo treino",
  "acao": "é calculado a partir de",
  "objeto": "data/hora futura e status planejado",
  "condicoes": [],
  "excecoes": ["treino do mesmo dia já encerrado deixa de ser o próximo treino"],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-005"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de R_META, parâmetro next_training_rule, e da aba PRÓXIMO TREINO",
      "resultado": "regra de cálculo e painel resultante concordam sobre o mesmo próximo treino (13/08/2026)"
    }
  }
}
```

### Complemento — abas reabertas após achado do REVIEWER

```json
{
  "id_regra": "REGRA-006",
  "fonte": ["EVD-0033"],
  "texto_original": "Resultados e participação real serão atualizados apenas após fonte validada.",
  "tipo": "CONDICAO",
  "sujeito": "resultado e participação real de um jogo",
  "acao": "só deve ser registrado/atualizado após",
  "objeto": "confirmação por fonte validada",
  "condicoes": [],
  "excecoes": [],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-008", "TERMO-013"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura da aba '3ª ETAPA CARIOCA 2026', linha 34",
      "resultado": "observação textual explícita associada ao cronograma da etapa, reforçando operacionalmente a distinção programação≠resultado realizado já documentada nas fontes de referência"
    }
  }
}
```

### Complemento — leitura completa das duas abas parcialmente lidas (achado do REVIEWER, segunda rodada)

```json
{
  "id_regra": "REGRA-007",
  "fonte": ["EVD-0035"],
  "texto_original": "CEPRAEA não participará — Risco de elenco: Não aplicável — Foco técnico: Sem preparação específica — Disponibilidades preservadas apenas como histórico.",
  "tipo": "EXCECAO",
  "sujeito": "disponibilidade declarada para uma etapa em que o CEPRAEA não participará",
  "acao": "é preservada apenas como",
  "objeto": "histórico",
  "condicoes": ["etapa marcada como 'CEPRAEA NÃO PARTICIPARÁ'"],
  "excecoes": [],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": "Não deve alimentar risco de elenco, foco técnico ou planejamento ativo para essa etapa.",
  "conceitos_afetados": ["TERMO-002", "TERMO-007"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de AGENDA TÉCNICA V2, linha 43 (etapa BR 4ª Etapa)",
      "resultado": "linha inteira com tratamento excepcional explícito para a única etapa da temporada marcada como sem participação do CEPRAEA"
    }
  }
}
```

### Complemento — leitura integral das abas remanescentes (achado do REVIEWER, terceira rodada)

```json
{
  "id_regra": "REGRA-008",
  "fonte": ["EVD-0042"],
  "texto_original": "jogo_real = status_participacao JOGOU",
  "tipo": "CALCULO",
  "sujeito": "participação real em jogo (jogo_real)",
  "acao": "é calculada a partir de",
  "objeto": "status_participacao = JOGOU",
  "condicoes": [],
  "excecoes": ["Atletas sem jogos no período recebem status 'SEM JOGO', não computadas como jogo_real"],
  "cardinalidade_minima": null,
  "cardinalidade_maxima": null,
  "vigencia": null,
  "contexto_valido": null,
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-008"],
  "implementacao_candidata": null,
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": ["Não fica claro se 'status_participacao' admite outros valores além de JOGOU/SEM JOGO (ex.: lesionada, ausência justificada em jogo) — apenas esses dois foram observados nesta fonte.", "A aba onde esta regra aparece ('ANÁLISE DOS JOGOS', oculta) mostra um total de jogos da temporada (23) divergente do total registrado na aba visível 'ANÁLISE JOGOS' já usada como fonte de TERMO-008 (19) — ver EVD-0044. Não fica claro qual resumo é autoritativo; não resolvido por suposição."],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura da aba 'ANÁLISE DOS JOGOS' (oculta), seção PARTICIPAÇÃO DAS ATLETAS",
      "resultado": "coluna 'Obs.' explicita a fórmula de derivação para cada atleta, com fonte declarada DB_PARTICIPACAO_JOGO; coluna 'Fonte' repete o mesmo ativo técnico em todas as linhas da seção"
    }
  }
}
```

## `AC-002` — `BancoCEPRAEA.docx`

```json
{
  "id_regra": "REGRA-009",
  "fonte": ["EVD-0062"],
  "texto_original": "As alterações IHF válidas desde 1º de abril de 2026 permitem números de uniforme de 1 a 99; por isso shirt_number é temporal e validado nesse intervalo.",
  "tipo": "CARDINALIDADE",
  "sujeito": "número de camisa (shirt_number) do vínculo de elenco",
  "acao": "deve estar entre",
  "objeto": "1 e 99, inclusive",
  "condicoes": ["Vigente para vínculos de elenco a partir da alteração normativa IHF de 2026-04-01."],
  "excecoes": [],
  "cardinalidade_minima": "1",
  "cardinalidade_maxima": "99",
  "vigencia": "A partir de 2026-04-01 (alteração IHF Beach Handball). Intervalo anterior a essa data não detalhado nesta fonte.",
  "contexto_valido": "Número de camisa atribuído a uma atleta dentro de um vínculo de elenco por temporada.",
  "contexto_invalido": null,
  "conceitos_afetados": ["TERMO-001"],
  "implementacao_candidata": "CHECK (shirt_number is null or shirt_number between 1 and 99) — já observado como constraint física na fonte (roster_shirt_number_ck), não implementado neste repositório nesta fase.",
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "duvidas": [
    "Fonte é TÉCNICA/AUXILIAR (DEC-002) — o intervalo 1-99 é atribuído à IHF como fonte normativa externa, não é uma regra inventada por este documento, mas esta ação não verificou o texto oficial da IHF diretamente; permanece OBSERVADO até confirmação contra a fonte normativa primária (IHF — Rules of the Game, Beach Handball) ou aprovação humana direta.",
    "Não fica claro nesta fonte qual era o intervalo válido antes de 2026-04-01, nem se camisas já atribuídas fora do novo intervalo antes da mudança precisam de correção retroativa."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de SRC-002 (BancoCEPRAEA.docx), seção 3 ('Regras normativas consideradas') e seção 9.6 (athlete_roster_memberships, coluna shirt_number e constraint roster_shirt_number_ck)",
      "resultado": "regra declarada em prosa na seção 3 e materializada como constraint física idêntica na seção 9.6, ambas atribuindo a origem à alteração IHF vigente desde 2026-04-01"
    }
  }
}
```
