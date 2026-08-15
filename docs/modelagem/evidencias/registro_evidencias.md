# Registro de evidências

Um bloco `json` por `EVD-NNNN`, validado contra `schemas/schema_evidencia.json`. É o elo entre
"fonte" e "conceito/regra" na cadeia de rastreabilidade (seção 4.3/4.5 do plano):
`Fonte → Fragmento/Evidência → Conceito → Regra → Elemento do Modelo`.

Cada fragmento aponta para `id_fonte` + localização literal e específica (aba+coluna+linha,
página+parágrafo, célula, seção — nunca "o arquivo inteiro"). Quando `dado_sensivel_encontrado`
for `true`, `trecho_literal` descreve o tipo/formato do dado, nunca o valor real (melhoria b).

Nenhum fragmento registrado ainda.
