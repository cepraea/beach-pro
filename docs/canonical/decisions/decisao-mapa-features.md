---
document_id: DOC-CEPRAEA-DEC-MAPA-FEATURES
title: "Mapa de features do MVP sintético"
document_type: decisao
version: "0.1.1"
workflow_status: CANONICA_VIGENTE
responsible: Davi Sermenho
permitted_uses:
  - decisao_vigente
  - criacao_feature_specs
prohibited_uses:
  - aprovacao_por_inferencia
  - dados_reais
  - criacao_sem_derivacao_dec019
---

# Mapa de features do MVP sintético

## 1. Autoridade e escopo

A DEC-019 (`DOC-CEPRAEA-DEC-019-MVP-SINTETICO`) autoriza unidades MVP e requisitos
funcionais. Ela não autoriza automaticamente a taxonomia de features nem a relação
explícita feature → unidade → RF → milestone. Esta decisão preenche essa lacuna.

A derivação parte exclusivamente de `proposta-mvp-sintetico-cepraea.md` (seção 5)
e da DEC-019 (seções 9 e 11). Nenhuma inferência ou interpretação adicional é
introduzida. Qualquer feature spec com `mvp_status: INCLUIDO` deve referenciar
este documento em `authorized_by`.

## 2. Tabela de unidades MVP por milestone

Fonte: proposta-mvp-sintetico-cepraea.md, seção 5.

| Unidade | Título | Milestone |
| --- | --- | --- |
| MVP-01 | Fundação, identidade e acesso | M1 |
| MVP-02 | Ciclo de vida do elenco | M2 |
| MVP-03 | Compromissos de treino | M2 |
| MVP-04 | Solicitações e respostas | M2 |
| MVP-05 | Declaração, lista prevista e presença real | M3 |
| MVP-06 | Caixa individual da atleta | M4 |
| MVP-07 | Estado operacional de Davi | M4 |
| MVP-08 | Cobertura por função ampla | M3 |
| MVP-09 | Histórico e auditoria | M1 (parcial) + M4 |
| MVP-10 | Privacidade aplicada ao fluxo | M4 |

## 3. Mapa de features autorizado

Estratégia aprovada: expansão temática. FT-PRESENCAS absorve MVP-06 e MVP-07;
FT-TREINADORES absorve MVP-09 e MVP-10.

| `feature_id` | `mvp_status` | `milestones` | `authorized_units` | `authorized_requirements` |
| --- | --- | --- | --- | --- |
| `FT-ATLETAS` | `INCLUIDO` | `[M2]` | `[MVP-02]` | `[RF-003, RF-004, RF-043, RF-045]` |
| `FT-TREINADORES` | `INCLUIDO` | `[M1, M4]` | `[MVP-01, MVP-09, MVP-10]` | `[RF-004, RF-007, RF-026, RF-033, RF-034, RF-036, RF-037, RF-038, RF-039, RF-040, RF-041, RF-042, RF-043, RF-044, RF-045, RF-046, RF-047, RF-048]` |
| `FT-TREINOS` | `INCLUIDO` | `[M2]` | `[MVP-03, MVP-04]` | `[RF-005, RF-006, RF-007, RF-008, RF-009, RF-010, RF-011, RF-027, RF-028, RF-029]` |
| `FT-PRESENCAS` | `INCLUIDO` | `[M3, M4]` | `[MVP-05, MVP-06, MVP-07]` | `[RF-001, RF-002, RF-012, RF-013, RF-014, RF-018, RF-019, RF-020, RF-021, RF-022, RF-023, RF-024, RF-025]` |
| `FT-AVALIACOES` | `INCLUIDO` | `[M3]` | `[MVP-08]` | `[RF-030, RF-031, RF-032]` |
| `FT-JOGOS` | `ADIADO` | `[]` | — | — |

## 4. Derivação por feature

### FT-ATLETAS — MVP-02, M2

MVP-02 (Ciclo de vida do elenco): RF-003 e RF-043 são primários; RF-004 e
RF-045 são controles explícitos definidos na proposta.

- **RF-003**: cadastro de atletas (identidade, composição, inclusão, inativação, retorno)
- **RF-004**: controle de acesso aos dados da atleta (controle de MVP-02)
- **RF-043**: desativação e preservação de histórico (Domínio 9 — Identidade e Acesso)
- **RF-045**: Row Level Security (controle de MVP-02)

### FT-TREINADORES — MVP-01, MVP-09, MVP-10, M1 + M4

MVP-01 (Fundação, identidade e acesso): contas, MFA, cadastro desabilitado,
convite, recuperação, RLS, isolamento e proibições de impersonação.
MVP-09 (Histórico e auditoria): rastreabilidade e trilha de segurança.
MVP-10 (Privacidade aplicada): isolamento de dados, proibição de inferência
automática, independência de IA, dados pessoais restritos.

RFs atribuídos (MVP-01 = RF-026, RF-036–RF-045, RF-048; MVP-09 = RF-033,
RF-034, RF-036; MVP-10 = RF-004, RF-007, RF-045–RF-048), com deduplicação:
RF-004, RF-007, RF-026, RF-033, RF-034, RF-036–RF-048.

### FT-TREINOS — MVP-03, MVP-04, M2

MVP-03 (Compromissos de treino): criação de treino com data, prazo, vigência,
responsável, próxima ação e estado temporal.
MVP-04 (Solicitações e respostas): modelo geral de solicitações, estados
semânticos, isolamento de respostas, justificativa minimizada, correção
administrativa e preservação de histórico.

- MVP-03: RF-027, RF-028, RF-029
- MVP-04: RF-005, RF-006, RF-007, RF-008, RF-009, RF-010, RF-011

### FT-PRESENCAS — MVP-05, MVP-06, MVP-07, M3 + M4

MVP-05 (Declaração, lista prevista e presença real): disponibilidade e presença
como entidades distintas, lista de confirmadas como previsão, presença real
registrada somente pós-treino.
MVP-06 (Caixa individual da atleta): solicitações pendentes, prazo, resposta
vigente, justificativa, fechamento, histórico e registro de ciência.
MVP-07 (Estado operacional de Davi): visão única de elenco, próximos treinos,
respostas, pendências e fatos não registrados.

- MVP-05: RF-012, RF-013, RF-014, RF-018, RF-019, RF-020, RF-021
- MVP-06: RF-022, RF-023, RF-024
- MVP-07: RF-001, RF-002, RF-025

### FT-AVALIACOES — MVP-08, M3

MVP-08 (Cobertura por função ampla): contagem descritiva baseada nas respostas
vigentes. Sem recomendação de convocação, escalação, disciplina ou condição
pessoal. Funções: goleira, defesa, ataque, especialista e indefinida.

- RF-030, RF-031, RF-032

Escopo negativo: feedback individual (RF-P04) e avaliação psicológica sensível
ficam fora do MVP sintético.

### FT-JOGOS — ADIADO

RF-015 (convocações), RF-016 (confirmações) e RF-017 (lista vigente) dependem
do fluxo de competição e são adiados. Não há milestone nem unidade MVP
autorizada para esta feature nesta fase.

## 5. RFs transversais

Os seguintes RFs aparecem em mais de uma feature em razão de sua presença em
múltiplas unidades MVP:

| RF | Features | Unidades MVP |
| --- | --- | --- |
| RF-004 | FT-ATLETAS, FT-TREINADORES | MVP-02 (controle), MVP-10 |
| RF-007 | FT-TREINOS, FT-TREINADORES | MVP-04, MVP-10 |
| RF-043 | FT-ATLETAS, FT-TREINADORES | MVP-02 (primário), MVP-01 (range) |
| RF-045 | FT-ATLETAS, FT-TREINADORES | MVP-02 (controle), MVP-01, MVP-10 |

A presença em múltiplas features não duplica o trabalho de implementação;
expressa que o RF é um critério de verificação para cada feature que o lista.

## 6. Cobertura

Todos os 44 RFs incluídos no MVP sintético (RF-001–014, RF-018–034, RF-036–048)
aparecem em pelo menos uma feature INCLUIDO. Os RFs adiados (RF-015–017,
RF-035, RF-049, RF-051–053) e o gate de privacidade (RF-050) não são atribuídos
a nenhuma feature nesta fase, conforme a proposta-fonte.
