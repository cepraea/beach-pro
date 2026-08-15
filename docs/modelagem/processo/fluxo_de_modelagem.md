# Fluxo de modelagem

Adaptação, para o CEPRAEA-BEACH-PRO, do checklist "Guia 1" de
`.drive/BEACH HANDBALL/Fluxo de Modelagem.gdoc.docx` (seções 1–6, 9, 11–13, conforme decisão
fixada na seção 4 de `PLANO_CEPRAEA_Modelo_Canonico_FINAL.md`). Este documento é orientação de
processo; os campos e enums que efetivamente validam cada registro estão em `schemas/*.json`, não
aqui — quando este texto e um schema divergirem em detalhe, o schema prevalece.

## 1. Como usar este fluxo

### Estados permitidos

Todo dossiê de fonte usa `estado_processamento` (`schema_fonte.json`):
`NAO_INICIADO`, `EM_EXECUCAO`, `BLOQUEADO`, `CONCLUIDO`, `NAO_APLICAVEL`.

Todo termo, regra e elemento do modelo usa `estado_epistemologico`:
`OBSERVADO`, `INFERIDO`, `AMBIGUO`, `CONFLITANTE`, `VALIDADO`, `REJEITADO`.

### Regra de progressão

- Processar uma fonte por vez, na ordem estritamente sequencial da seção 10 do plano — nunca em
  paralelo.
- Não misturar, num mesmo dossiê, fonte normativa, fonte operacional, material de apoio e decisão
  local.
- `EM_EXECUCAO` só existe durante o processamento de uma única ação; nunca atravessa o limite de
  um turno.
- Para dúvida não bloqueante, registrar hipótese explícita e marcar o elemento como `AMBIGUO`
  em vez de decidir silenciosamente.

### Critério geral de conclusão de uma ação

- A regra ou elemento extraído corresponde à fonte, não a uma suposição sobre ela.
- O conceito possui `definicao` e `contexto_valido` preenchidos quando aplicável.
- Identidade, temporalidade e histórico necessários estão preservados.
- A evidência (`evidencia.source_evidence`) permite reproduzir o resultado.
- Nenhuma migration, schema físico ou policy é produzido nesta fase (fora de escopo — seção 3 do
  plano).

## 2. Priorização do corpus

Ao contrário do Guia 1 original — que prioriza por classe de autoridade da fonte —, a ordem desta
fase é fixada explicitamente pela seção 10 do plano: as 28 entradas de
`.drive/CEPRAEA BEACH PRO/` na sequência `AC-001`…`AC-028`, começando por
`CEPRAEA AGOSTO 2026.xlsx` por instrução direta de Davi. A classificação de autoridade
(`tipo_fonte`/`autoridade_fonte`/`proveniencia_fonte`/`estado_fonte`) ainda é feita por fonte, mas
não determina a ordem de processamento nesta fase — só como cada fonte é tratada quando
processada.

## 3. Checklist por fonte

Ver seção 7 do plano ("Definição formal de ação") para o template completo — identificação
(`id_fonte`, `hash_sha256`, `caminho_local`), seleção de conteúdo, resultado da análise
(`conceitos_encontrados`, `regras_encontradas`, `conflitos_ou_duvidas`) e critério de saída. Cada
dossiê em `fontes/dossies/<slug>.md` segue esse template e valida contra `schema_fonte.json`.

## 4. Extração seletiva de regras

Cada regra relevante vira um registro `REGRA-NNN` em `conhecimento/registro_regras.md`
(`schema_regra.json`): `fonte` (sempre `EVD-NNNN`, nunca a fonte inteira), `tipo`, `sujeito`,
`acao`, `objeto`, `condicoes`, `excecoes`, cardinalidades, vigência, `estado_epistemologico`.

Validações permanentes (herdadas do Guia 1 §4, aplicáveis sem exceção):

- Uma regra não nasce só porque um substantivo apareceu no texto.
- Obrigação condicional não vira automaticamente `NOT NULL` — decisão física está fora de escopo
  aqui de qualquer forma.
- Exceção não é tratada como regra geral.
- Fato histórico não é confundido com regra vigente.

## 5. Glossário e elementos do modelo

Cada conceito necessário vira um registro `TERMO-NNN` em `conhecimento/glossario.md`
(`schema_termo.json`) — só significado. Estruturas maiores (Bounded Context, identidade,
agregado, invariante, ciclo de vida, fronteira transacional) viram elementos em `candidatos/*.md`
(`schema_elemento_modelo.json`, `estagio=CANDIDATO`) — ver seção 4.1 do plano para os seis objetos
obrigatórios.

Validações conceituais permanentes (Guia 1 §5, todas já confirmadas como distinções reais do
domínio em `modelagem_dados_agente.md`):

- Disponibilidade declarada é diferente de presença factual.
- Cadastro de atleta é diferente de vínculo com a equipe.
- Usuário autenticado é diferente da entidade atleta.
- Convocação é diferente de participação efetiva.
- Programação é diferente de resultado realizado.

## 6. Modelo lógico relacional

Só é produzido em `AC-029`, e só para Bounded Contexts em `MADURA_PARA_MODELO_LOGICO` (seção 4.4
do plano). Nenhuma tabela, chave ou constraint é decidida antes disso — a ordem é sempre
conceitos → identidades → relações → invariantes → ciclos de vida → agregados → operações →
fronteiras transacionais → (fora de escopo) mecanismo PostgreSQL.

## 9. Aprovação proporcional ao risco

A classificação de risco desta fase inteira já está fixada pela seção 12 do plano: **amarelo**,
com **carve-out vermelho por privacidade** em `AC-008`, `AC-018`, `AC-019` (dado sensível
provável). Isso substitui a escada genérica baixo/médio/alto do Guia 1 §9 para esta fase
específica — toda ação exige os mesmos validadores determinísticos (seção "Validação e handoff"),
e as três ações marcadas exigem checkpoint humano antes de `CONCLUIDO`.

## 11. Condições de parada

Interromper e marcar `BLOQUEADO` quando (Guia 1 §11, seção 9 do plano):

- A autoridade ou vigência da fonte não pode ser determinada e isso altera a interpretação.
- Duas fontes autoritativas entram em conflito sem precedência definida (melhoria c).
- O arquivo está ilegível (PDF sem ferramenta disponível) e a informação não pode ser verificada.
- A alteração poderia apagar ou reescrever fato histórico.
- Identidade de arquivo genuinamente ambígua (colisão de nome sem `hash_sha256`/`id_drive`
  suficientes).

Não bloquear quando a dúvida não afetar integridade, segurança ou compatibilidade — registrar
como `AMBIGUO` com hipótese explícita e prosseguir.

## 12. Proibições operacionais

Herdadas de `modelagem_dados_agente.md` ("Regras de conduta do agente") e do Guia 1 §12, sem
exceção nesta fase:

- Não converter cabeçalho de coluna em termo canônico só por existir (`AD-03`).
- Não inferir presença a partir de disponibilidade, nem participação a partir de convocação.
- Não tratar fonte tecnicamente completa como autoritativa só por completude (`AD-01`, melhoria
  d).
- Não transcrever valor literal de dado sensível (melhoria b).
- Não promover `INFERIDO`/`AMBIGUO`/`CONFLITANTE` a `VALIDADO` sem aprovação humana registrada.
- Não escrever fora de `WRITE_SCOPE_EXECUTOR`; não escrever em `CEPRAEA_SOURCE_ROOT`.
- Não gerar SQL, migration, policy ou schema físico nesta fase.

## 13. Definição de pronto do fluxo

Ver seção 11 do plano — os cinco gates (`A` a `E`) verificados simultaneamente. Cobertura
documental completa (100% das entradas em estado terminal) não implica, isoladamente, prontidão
semântica (`AD-06`, `INV-PROC-007`).
