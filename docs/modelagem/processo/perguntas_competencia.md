# Perguntas de competência

Extraído da seção 4.3 de `PLANO_CEPRAEA_Modelo_Canonico_FINAL.md` — união das perguntas do
checklist original ("Guia 1"/"Guia 2") com as acrescentadas por `modelagem_dominio_dados.md` §22,
sem duplicar. Orientam o modelo e impedem a criação de entidades sem finalidade
(`modelagem_dados_agente.md`, "Síntese operacional").

## Do checklist original

- Qual era o vínculo de uma atleta em determinada data?
- Qual foi a última resposta de disponibilidade?
- Quais versões anteriores existiram?
- Quem registrou a presença?
- Qual documento sustenta um resultado?
- Qual regulamento estava vigente?
- Uma atleta pode consultar dados de outra atleta?

## Acrescentadas por `modelagem_dominio_dados.md` §22

Específicas da descoberta:

- De quais fontes surge este conceito?
- Há mais de uma definição?
- O termo possui significados diferentes?
- Esta estrutura possui identidade?
- O histórico é necessário?
- Há uma invariante associada?
- O objeto pertence a qual contexto?
- A alteração precisa ocorrer atomicamente?
- O dado é factual ou derivado?

## Uso

Cada elemento candidato (Bounded Context, identidade, agregado, invariante, ciclo de vida,
fronteira transacional — seção 4.1 do plano) deveria conseguir responder as perguntas acima
relevantes ao seu tipo antes de ser considerado para promoção `candidatos/ → dominio/`. Uma
pergunta sem resposta disponível não bloqueia sozinha o registro do candidato, mas deve constar em
`ambiguidades` (`schema_elemento_modelo.json`) até ser respondida ou explicitamente descartada
como não aplicável.
