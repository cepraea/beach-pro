# DEC-TRAD-001 — Português brasileiro como idioma operacional canônico

## Status

`APROVADA_PARA_IMPLEMENTACAO_CONTROLADA`

## Contexto

Os documentos do framework utilizam fontes japonesas e inglesas, enquanto `agent-list.md` já declara português brasileiro como fonte única. Manter pares ativos em vários idiomas cria autoridades concorrentes.

## Decisão

O idioma operacional canônico será `pt-BR`. Arquivos canônicos promovidos não usarão sufixo de idioma. As fontes históricas permanecerão recuperáveis por Git, URL imutável e SHA-256, fora do conjunto normativo ativo.

## Natureza da mudança

`BREAKING`. A promoção exige corte atômico, validação integral, PR própria e aprovação humana vinculada aos hashes do pacote.

## Limites

Esta decisão não autoriza correção, portabilidade ou atualização tecnológica durante a tradução.
