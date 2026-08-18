# Invariantes — candidatos

Hipóteses de invariante (`schemas/schema_elemento_modelo.json`, `tipo=INVARIANTE`,
`estagio=CANDIDATO`) ainda não promovidas ao Modelo Canônico. `INV-001` não aparece aqui — nasceu
diretamente em `dominio/invariantes.md` pela rota PRE-SEED (seção 4.2 do plano), por já ter sido
validado diretamente por Davi Sermenho em `AC-000`.

## INV-002 — Disponibilidade declarada não implica presença factual (candidata)

```json
{
  "id_elemento": "INV-002",
  "tipo": "INVARIANTE",
  "nome": "Disponibilidade declarada não implica presença factual",
  "estagio": "CANDIDATO",
  "bounded_context_id": "CTX-004",
  "detalhes": {
    "linguagem_natural": "Uma resposta de disponibilidade declarada (SIM/NAO/TALVEZ) por uma atleta nunca constitui, por si só, prova de presença factual; presença é um estado distinto, registrado apenas após a sessão e mediante autorização humana.",
    "conceitos_afetados": ["TERMO-002", "TERMO-003"]
  },
  "maturidade": null,
  "fonte": ["EVD-0003", "EVD-0005", "EVD-0006", "EVD-0010", "EVD-0017", "EVD-0049"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "A fonte (R_META, EVD-0003) rotula esta distinção 'APPROVED_BY_HUMAN_STEWARD' — uma alegação de aprovação humana feita pela própria fonte operacional, anterior e externa a este processo de modelagem. Isso é evidência forte de que a distinção já foi validada operacionalmente, mas não substitui a aprovação direta de Davi Sermenho exigida por este processo para promoção a VALIDADO (schema_elemento_modelo.json) — permanece OBSERVADO até essa confirmação explícita.",
    "Corroborada por SRC-002 (BancoCEPRAEA.docx, DOM-001, EVD-0049) em AC-002 — fonte TÉCNICA/AUXILIAR (DEC-002), então a corroboração reforça a hipótese mas não substitui a validação humana direta ainda pendente."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura cruzada de R_META, contrato de UI (Página16) e 📑_CHANGELOG",
      "resultado": "três artefatos internos independentes desta mesma fonte (metadados de reconciliação, contrato de interface, log de mudanças) declaram e reforçam a mesma distinção, incluindo um evento de changelog datado em que a separação foi explicitamente implementada"
    }
  }
}
```

## INV-003 — Identidade não é nome (candidata)

```json
{
  "id_elemento": "INV-003",
  "tipo": "INVARIANTE",
  "nome": "Identidade não é nome — junção usa identificador estável",
  "estagio": "CANDIDATO",
  "bounded_context_id": "CTX-001",
  "detalhes": {
    "linguagem_natural": "O nome de uma atleta nunca é usado como chave de junção ou identidade técnica; identidade é resolvida por um identificador estável (técnico ou código legado controlado), porque nomes podem repetir, variar de grafia ou mudar.",
    "conceitos_afetados": ["TERMO-001"]
  },
  "maturidade": null,
  "fonte": ["EVD-0049", "EVD-0052"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "Fonte é TÉCNICA/AUXILIAR (DEC-002) — reforça, mas não valida por si só, a ambiguidade de identificador de atleta já registrada como limitação de TERMO-001 em AC-001 (coluna 'Nº' não sequencial vs. numeração 1-19)."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de SRC-002 (BancoCEPRAEA.docx), seção 4 (DOM-004) e seções 9.5/9.6 (athletes.legacy_athlete_id)",
      "resultado": "princípio declarado explicitamente (DOM-004) e materializado em coluna dedicada (legacy_athlete_id) desenhada para reconciliar identidade legada sem depender do nome"
    }
  }
}
```

## INV-004 — Justificativa de ausência é privada (candidata)

```json
{
  "id_elemento": "INV-004",
  "tipo": "INVARIANTE",
  "nome": "Justificativa de ausência é privada e nunca integra artefato compartilhado",
  "estagio": "CANDIDATO",
  "bounded_context_id": "CTX-004",
  "detalhes": {
    "linguagem_natural": "O motivo/justificativa que uma atleta associa a uma resposta de disponibilidade é informação privada; nunca deve aparecer em listas publicadas, comunicações ou qualquer artefato visível a outras atletas.",
    "conceitos_afetados": ["TERMO-002"]
  },
  "maturidade": null,
  "fonte": ["EVD-0049", "EVD-0054"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "Fonte é TÉCNICA/AUXILIAR (DEC-002) — não há, até esta ação, confirmação em fonte OPERACIONAL/PRIMÁRIA de que a privacidade de justificativa já é uma prática real do CEPRAEA hoje, ou apenas uma recomendação de design para o novo sistema."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de SRC-002 (BancoCEPRAEA.docx), seção 4 (DOM-006) e seções 9.15/9.16 (justification_categories, private.response_justifications)",
      "resultado": "princípio declarado explicitamente (DOM-006) e materializado em desenho físico: justificativa fica em schema private, sem grants diretos ao cliente, separada fisicamente da resposta pública"
    }
  }
}
```

## INV-005 — Fato histórico é preservado, nunca reescrito (candidata)

```json
{
  "id_elemento": "INV-005",
  "tipo": "INVARIANTE",
  "nome": "Fato histórico é preservado — correção ou mudança de regra nunca reescreve o registro original",
  "estagio": "CANDIDATO",
  "bounded_context_id": null,
  "detalhes": {
    "linguagem_natural": "Respostas, correções, presença e eventos de vínculo, uma vez registrados, nunca são sobrescritos ou apagados — uma correção cria um novo registro que referencia o anterior. Da mesma forma, uma mudança na regra esportiva vigente não altera fatos já registrados sob a regra anterior.",
    "conceitos_afetados": []
  },
  "maturidade": null,
  "fonte": ["EVD-0049", "EVD-0056"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "Une DOM-005 e DOM-009 da fonte (mesma propriedade — preservação de fato histórico — vista pelo ângulo de desenho de tabela e pelo ângulo de regra de não-reescrita), para não registrar dois candidatos redundantes.",
    "Fonte é TÉCNICA/AUXILIAR (DEC-002); o princípio de preservação de histórico já aparece indiretamente no próprio processo desta modelagem (seção 5.5 de modelagem_dominio_dados.md, 'estado atual não substitui histórico'), então esta fonte corrobora um princípio metodológico já conhecido, não o introduz."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de SRC-002 (BancoCEPRAEA.docx), seção 4 (DOM-005, DOM-009) e seção 13.4 (triggers prevent_update_delete)",
      "resultado": "princípio declarado explicitamente e materializado em cinco triggers append-only sobre tabelas de fato/histórico (roster_events, responses, corrections, attendance, audit_events)"
    }
  }
}
```

## INV-006 — Lista prevista não implica presença factual (candidata)

```json
{
  "id_elemento": "INV-006",
  "tipo": "INVARIANTE",
  "nome": "Lista prevista não implica presença factual",
  "estagio": "CANDIDATO",
  "bounded_context_id": "CTX-004",
  "detalhes": {
    "linguagem_natural": "Uma atleta constar em uma lista prevista/publicada (projeção do que se espera para um treino) nunca constitui, por si só, prova de que ela de fato compareceu — mesma propriedade de INV-002, mas aplicada ao objeto lista em vez de à resposta individual de disponibilidade.",
    "conceitos_afetados": ["TERMO-005"]
  },
  "maturidade": null,
  "fonte": ["EVD-0049", "EVD-0057"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "Relacionada a INV-002 (mesma família de invariante — declaração/projeção ≠ fato), mas objeto distinto (lista vs. resposta individual); registrada separadamente por seção 4.2 do plano tratar cada afirmação da fonte em seus próprios termos, sem fundir sem evidência de que sejam literalmente a mesma regra.",
    "Fonte é TÉCNICA/AUXILIAR (DEC-002)."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de SRC-002 (BancoCEPRAEA.docx), seção 4 (DOM-002) e seção 10 (view v_availability_attendance_divergence)",
      "resultado": "princípio declarado explicitamente (DOM-002) e materializado em view que trata declaração/lista e presença como fatos distintos e comparáveis, nunca equivalentes"
    }
  }
}
```

## INV-007 — Convocação, escalação e participação são estados distintos (candidata)

```json
{
  "id_elemento": "INV-007",
  "tipo": "INVARIANTE",
  "nome": "Convocação de etapa ≠ escalação de partida ≠ participação real",
  "estagio": "CANDIDATO",
  "bounded_context_id": "CTX-006",
  "detalhes": {
    "linguagem_natural": "Uma atleta convocada para uma etapa/competição não está automaticamente escalada para uma partida específica dessa etapa, e estar escalada não equivale a ter participado de fato — são três estados sequenciais e distintos, nenhum implicando o próximo.",
    "conceitos_afetados": ["TERMO-006"]
  },
  "maturidade": null,
  "fonte": ["EVD-0049", "EVD-0059"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "Fonte é TÉCNICA/AUXILIAR (DEC-002) e o módulo correspondente (matches/match_rosters/match_participations) é declarado explicitamente fora do MVP atual pela própria fonte (seção 15) — este candidato registra a distinção semântica encontrada, não antecipa a criação de tabelas ou a maturidade do Bounded Context CTX-006.",
    "AC-001 já havia estabelecido TERMO-006 (convocação) com evidência operacional real (EVD de SRC-001); esta fonte acrescenta a distinção de três estados, mas com autoridade técnica/auxiliar, não operacional/primária."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura de SRC-002 (BancoCEPRAEA.docx), seção 4 (DOM-003), seção 2 ('DB_CONVOCACOES, DB_CONVOCACAO_ATLETAS e DB_PARTICIPACAO_JOGO comprovam que convocada para etapa não equivale a escalada ou jogou uma partida') e seção 15 (match_rosters/match_participations)",
      "resultado": "princípio declarado explicitamente (DOM-003) com correspondência direta às abas DB_CONVOCACOES/DB_PARTICIPACAO_JOGO já citadas em AC-001 como pendentes de teste em AC-004"
    }
  }
}
```
