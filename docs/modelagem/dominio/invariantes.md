# Invariantes — domínio

Invariantes promovidas ao Modelo Canônico (`schemas/schema_elemento_modelo.json`,
`tipo=INVARIANTE`, `estagio=DOMINIO`) — sempre `estado_epistemologico=VALIDADO`, com
`promoted_from`/`promoted_by` preenchidos.

## INV-001 — Papel operacional único (PRE-SEED)

Fato de domínio pré-semeado (seção 4.2 do plano): Davi Sermenho confirmou esta regra diretamente,
como especialista do domínio, nesta sessão — ela não nasce `OBSERVADO` como hipótese, porque isso
fingiria que uma validação humana que já aconteceu não aconteceu. Nasce direto em `dominio/`, sem
passar por `candidatos/`, pela rota PRE-SEED (`promoted_by="PRE-SEED"`).

**Nota — não é imutável:** se `AC-004`/`AC-008`–`AC-010`/`AC-016`–`AC-019` revelarem um papel
operacional diferente ou divergência temporal, isso vira novo registro em
`decisoes/registro_decisoes.md` (conflito, melhoria c) para Davi decidir — não uma reversão
silenciosa do que já foi validado.

```json
{
  "id_elemento": "INV-001",
  "tipo": "INVARIANTE",
  "nome": "Papel operacional único por usuário",
  "estagio": "DOMINIO",
  "promoted_from": "REF:modelagem_dados_agente.md — Identidade humana, autenticação e papel",
  "promoted_by": "PRE-SEED",
  "bounded_context_id": null,
  "detalhes": {
    "declaracao_formal": "papel_operacional ∈ {ATLETA, TREINADOR} ∧ ∀ usuário: |papéis(usuário)| = 1",
    "linguagem_natural": "Cada usuário operacional do CEPRAEA-BEACH-PRO tem exatamente um papel — ATLETA ou TREINADOR; uma atleta nunca acumula outra função no sistema."
  },
  "maturidade": null,
  "fonte": [
    "REF:modelagem_dados_agente.md — Identidade humana, autenticação e papel",
    "REF:modelagem_dominio_dados.md §7/§13.2"
  ],
  "estado_epistemologico": "VALIDADO",
  "estado_tecnico": "NAO_MODELADO",
  "ambiguidades": [],
  "evidencia": {
    "source_evidence": {
      "comando_ou_metodo": "decisão humana direta + documentos REF listados em fonte",
      "resultado": "regra explicitamente confirmada por Davi Sermenho"
    },
    "semantic_evidence": "confirmado diretamente por Davi Sermenho, especialista do domínio, nesta conversa.",
    "approval_evidence": { "aprovador": "Davi Sermenho", "data": "2026-08-15" },
    "repository_evidence": { "action_ref": "AC-000" }
  }
}
```
