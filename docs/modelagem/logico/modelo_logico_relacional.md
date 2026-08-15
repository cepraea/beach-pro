# Modelo lógico relacional

Só recebe entidades/tabelas/relações de Bounded Contexts em `estagio=DOMINIO` com
`maturidade=MADURA_PARA_MODELO_LOGICO` (seção 4.4 do plano). Nenhuma migration, schema físico ou
policy é gerada aqui — isso é fora de escopo desta fase (seção 3 do plano).

Cada elemento registra `bounded_context_id` e `derived_from[]` com os IDs canônicos que justificam
a derivação (seção 6, "Contratos adicionais").

Vazio no momento — nenhum Bounded Context atingiu `MADURA_PARA_MODELO_LOGICO` ainda. Isso é o
estado esperado de `AC-000` até `AC-028`: só `AC-029` classifica maturidade e, se aplicável,
preenche este arquivo. Vazio ao final da fase também é um resultado `DONE` válido, não uma
pendência (seção 10, linha `AC-029`).
