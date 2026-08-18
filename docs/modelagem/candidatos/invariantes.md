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
  "fonte": ["EVD-0003", "EVD-0005", "EVD-0006", "EVD-0010", "EVD-0017"],
  "estado_epistemologico": "OBSERVADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [
    "A fonte (R_META, EVD-0003) rotula esta distinção 'APPROVED_BY_HUMAN_STEWARD' — uma alegação de aprovação humana feita pela própria fonte operacional, anterior e externa a este processo de modelagem. Isso é evidência forte de que a distinção já foi validada operacionalmente, mas não substitui a aprovação direta de Davi Sermenho exigida por este processo para promoção a VALIDADO (schema_elemento_modelo.json) — permanece OBSERVADO até essa confirmação explícita."
  ],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "leitura cruzada de R_META, contrato de UI (Página16) e 📑_CHANGELOG",
      "resultado": "três artefatos internos independentes desta mesma fonte (metadados de reconciliação, contrato de interface, log de mudanças) declaram e reforçam a mesma distinção, incluindo um evento de changelog datado em que a separação foi explicitamente implementada"
    }
  }
}
```
