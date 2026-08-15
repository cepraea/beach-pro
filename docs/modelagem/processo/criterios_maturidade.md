# Critérios de maturidade

Extraído da seção 4.4 de `PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`, que corrige a inversão do
Definition of Done: a dependência correta é **Modelo Canônico maduro → modelo lógico**, nunca o
inverso. Nenhum objeto é justificado retroativamente pelo que o modelo lógico "usa".

## Gate de maturidade por Bounded Context

Cada `CTX-NNN` recebe um campo `maturidade` quando `AC-029` classifica (seção 4.5 do plano,
`schema_elemento_modelo.json`):

| Maturidade | Critério |
| --- | --- |
| `IMATURA` | Conceitos ainda não definidos, ou identidades não resolvidas, ou existe termo/regra `AMBIGUO`/`CONFLITANTE` sem resolução dentro deste contexto, ou o próprio Bounded Context ainda não possui `estado_epistemologico=VALIDADO`. |
| `PARCIALMENTE_MADURA` | Conceitos definidos e identidades resolvidas; mas invariantes, ciclos de vida, agregados ou fronteiras transacionais deste contexto ainda incompletos, ou há pendência não crítica registrada. |
| `MADURA_PARA_MODELO_LOGICO` | Os 16 critérios abaixo satisfeitos para este contexto. |

**Regra de bloqueio:** qualquer `AMBIGUO` ou `CONFLITANTE` com impacto estrutural obriga o contexto
a permanecer `IMATURA` ou `PARCIALMENTE_MADURA` — nunca pode ser `MADURA_PARA_MODELO_LOGICO`.

**Regra de derivação:** `logico/modelo_logico_relacional.md` só recebe entidades de Bounded
Contexts em `MADURA_PARA_MODELO_LOGICO`. Um contexto `IMATURA`/`PARCIALMENTE_MADURA` ao final da
fase não é erro — é resultado válido, registrado em `dominio/modelo_canonico_dominio.md` e em
`logico/areas_pendentes.md`, sem entrada correspondente no modelo lógico.

## Os 16 critérios (`modelagem_dominio_dados.md` §39)

Uma área do domínio está suficientemente madura para implementação quando:

1. os conceitos materiais estão definidos;
2. identidades relevantes estão resolvidas;
3. aliases e sinônimos estão reconciliados;
4. relações possuem significado;
5. cardinalidades relevantes são conhecidas;
6. invariantes materiais foram identificadas;
7. ciclos de vida estão formalizados quando necessários;
8. o Bounded Context está estabelecido ou sua ausência está justificada;
9. agregados relevantes foram determinados;
10. fronteiras transacionais necessárias estão justificadas;
11. regras materiais possuem evidência;
12. conflitos estão resolvidos ou explicitamente pendentes;
13. decisões possuem estado epistemológico;
14. histórico está corretamente tratado;
15. questões de competência podem ser respondidas;
16. testes podem ser derivados.

Pendências remanescentes só são compatíveis com `MADURA_PARA_MODELO_LOGICO` quando classificadas
explicitamente como não bloqueantes e incapazes de alterar identidade, definição, relação,
cardinalidade, invariante, ciclo de vida, agregado, fronteira transacional ou estrutura lógica
derivada.

## Quando isso é avaliado

Não é um lote à parte: cada `AC-NNN` já pode atualizar candidatos que, na prática, afetam a
maturidade futura de um contexto. A classificação formal de `maturidade`, porém, só acontece em
`AC-029`, depois de `AD-06` (contagem de `AMBIGUO`/`CONFLITANTE` pendente por contexto) — nunca
antes, e nunca só porque as 28 fontes atingiram estado terminal (`INV-PROC-007`).
