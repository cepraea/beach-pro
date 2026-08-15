# Taxonomias

Adaptação, para o CEPRAEA-BEACH-PRO, das taxonomias do "Guia 2" de
`.drive/BEACH HANDBALL/Fluxo de Modelagem.gdoc.docx` e de `modelagem_dominio_dados.md` §16–18.
Os enums normativos que efetivamente validam cada registro estão em `schemas/*.json`; este
documento explica seu significado e a correção que cada um recebeu em relação às fontes de
referência — quando este texto e um schema divergirem em detalhe, o schema prevalece.

## Taxonomia das fontes

`modelagem_dominio_dados.md` §16 já separa autoridade, proveniência e ciclo de vida — mistura que
existia na classificação original do Guia 1 (`classe: AUTORITATIVA / OPERACIONAL PRIMÁRIA /
DERIVADA / SUPORTE / HISTÓRICA / INDETERMINADA`, um único campo combinando as três dimensões).
`schema_fonte.json` adota a versão separada, com uma correção adicional própria desta fase
(melhoria a/seção 5.1): `HISTORICA` sai de `tipo_fonte` (gênero) porque temporalidade já pertence
inteiramente a `estado_fonte`.

### `tipo_fonte` (gênero)

`NORMATIVA`, `OPERACIONAL`, `CIENTIFICA`, `ADMINISTRATIVA`, `TECNICA`, `INDETERMINADO`.

### `autoridade_fonte`

`OFICIAL`, `PRIMARIA`, `AUXILIAR`, `INDETERMINADA`. Toda fonte da tentativa de modelagem anterior
(D-02) nasce `AUXILIAR`, nunca `OFICIAL`/`PRIMARIA`, independente de completude técnica (melhoria
d, testada em `AD-01`).

### `proveniencia_fonte`

`ORIGINAL`, `DERIVADA`, `INDETERMINADA`.

### `estado_fonte` (ciclo de vida)

`VIGENTE`, `SUBSTITUIDA`, `OBSOLETA`, `INDETERMINADA`. Substitui o enum de cinco valores do Guia 1
(`VIGENTE`/`COMPLEMENTAR`/`SUBSTITUIDA`/`HISTÓRICA`/`EM VERIFICAÇÃO`): `COMPLEMENTAR` virou
`autoridade_fonte=AUXILIAR`; `EM VERIFICAÇÃO` já é coberto por `estado_processamento`, que é
workflow, não propriedade estável da fonte.

## Estado epistemológico

Comum a termos, regras e aos seis objetos do Modelo Canônico (`modelagem_dados_agente.md`, etapa
5; `modelagem_dominio_dados.md` §17):

| Estado | Significado |
| --- | --- |
| `OBSERVADO` | Existe suporte direto e literal na fonte. |
| `INFERIDO` | Conclusão derivada de evidência, mas não declarada diretamente. |
| `AMBIGUO` | Mais de uma interpretação permanece plausível, ou falta informação suficiente. |
| `CONFLITANTE` | Fontes relevantes apresentam afirmações incompatíveis. |
| `VALIDADO` | Confirmado por autoridade humana adequada — nunca a própria IA. |
| `REJEITADO` | A hipótese foi avaliada e considerada incorreta. |

Isso substitui, para esta fase, a escada específica `EXTRAÍDA / VERIFICADA / VALIDADA / REJEITADA`
do Guia 1 §4 — um único vocabulário epistemológico cobre termos, regras e os seis objetos do
Modelo Canônico, em vez de vocabulários paralelos por tipo de registro.

## Estado técnico

`modelagem_dominio_dados.md` §18, dimensão independente do estado epistemológico:

`NAO_MODELADO`, `MODELADO`, `IMPLEMENTADO`, `TESTADO`, `ATIVO`, `SUBSTITUIDO`.

`VALIDADO ≠ IMPLEMENTADO`: um termo só pode avançar de `estado_tecnico=NAO_MODELADO` depois de
`estado_epistemologico=VALIDADO`, nunca antes. Nesta fase, só `NAO_MODELADO`/`MODELADO` são
alcançáveis — `IMPLEMENTADO`/`TESTADO`/`ATIVO` pertencem ao modelo físico, fora de escopo (seção 3
do plano).

## Classificação de termos (`classificacao`, `schema_termo.json`)

União das três taxonomias-fonte (Guia 1 §5, Guia 2 §3.2, `modelagem_dominio_dados.md` §8), nenhuma
delas se declarou substituta da outra:

`ENTIDADE`, `ATRIBUTO`, `VALOR_OBJETO`, `PAPEL`, `ASSOCIACAO`, `EVENTO`, `ESTADO`, `REGRA`,
`FATO_HISTORICO`, `PROJECAO`, `INDICADOR`, `CATALOGO`, `SNAPSHOT`.

Distinções materiais que este vocabulário protege (Guia 2 §5.8, "falsos cognatos"):
disponibilidade ≠ presença; convocação ≠ participação; relação nominal ≠ escalação efetiva;
programação ≠ resultado realizado; regra oficial ≠ política interna; validação da IA ≠ aprovação
humana; SQL sintaticamente válido ≠ modelo semanticamente correto.

## Tipo de regra (`tipo`, `schema_regra.json`)

União de Guia 1 §4 e `modelagem_dominio_dados.md` §20 (atomização de regras):

`DEFINICAO`, `OBRIGACAO`, `PROIBICAO`, `PERMISSAO`, `CONDICAO`, `EXCECAO`, `CLASSIFICACAO`,
`CALCULO`, `REGRA_TEMPORAL`, `CARDINALIDADE`, `UNICIDADE`, `AUTORIZACAO`,
`TRANSICAO_DE_ESTADO`.

## Namespaces de identificador

Ver seção 4.8 do plano — tabela completa de prefixos (`SRC`, `AC`, `EVD`, `TERMO`, `REGRA`, `IDN`,
`CTX`, `INV`, `LFC`, `AGG`, `TRX`, `DEC`) e o schema que cada um valida. Não duplicado aqui para
evitar divergência entre duas cópias da mesma tabela.
