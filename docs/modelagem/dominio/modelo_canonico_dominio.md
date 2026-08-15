# Modelo Canônico do Domínio — CEPRAEA-BEACH-PRO

Este é o produto intelectual principal da fase (seção 4.6 e "Objetivo" de
`PLANO_CEPRAEA_Modelo_Canonico_FINAL.md) — não o inventário, não o glossário, não o modelo lógico:
esses são insumos e derivações dele.

## Estrutura

Uma seção por `CTX-NNN` (Bounded Context), cada uma reunindo — **por referência, não duplicando o
conteúdo** — os elementos de `dominio/bounded_contexts.md`, `dominio/identidades_definitivas.md`,
`dominio/agregados.md`, `dominio/invariantes.md`, `dominio/ciclos_de_vida.md`,
`dominio/fronteiras_transacionais.md` que declaram aquele `bounded_context_id`, mais os termos de
`conhecimento/glossario.md` e regras de `conhecimento/registro_regras.md` que o contexto usa, mais
a `maturidade` atual do contexto (seção 4.4).

## Estado atual

`AC-000` inicializa este arquivo sem conteúdo de domínio inventado (critério de DONE, seção 10.1,
item 19) — nenhuma síntese acontece antes de haver Modelo Canônico suficiente para sintetizar.

A consolidação real é produzida por `AC-029`, depois de:

1. reconciliar pendências semânticas (`conhecimento/conflitos_semanticos.md`);
2. promover candidatos `VALIDADO` para `dominio/*.md` (rota A ou rota B — seção 4.7);
3. classificar a maturidade de cada `CTX-NNN` (`AD-06`, seção 4.4).

Nenhuma seção por `CTX-NNN` existe ainda.
