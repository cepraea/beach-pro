# Registro de evidências

Um bloco `json` por `EVD-NNNN`, validado contra `schemas/schema_evidencia.json`. É o elo entre
"fonte" e "conceito/regra" na cadeia de rastreabilidade (seção 4.3/4.5 do plano):
`Fonte → Fragmento/Evidência → Conceito → Regra → Elemento do Modelo`.

Cada fragmento aponta para `id_fonte` + localização literal e específica (aba+coluna+linha,
página+parágrafo, célula, seção — nunca "o arquivo inteiro"). Quando `dado_sensivel_encontrado`
for `true`, `trecho_literal` descreve o tipo/formato do dado, nunca o valor real (melhoria b).

## SRC-001 / AC-001 — `CEPRAEA AGOSTO 2026.xlsx`

```json
{
  "id_evidencia": "EVD-0001",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_STATUS', linhas 1-7, colunas A-C",
  "trecho_literal": "status | ativo_para_entrada | observacao — SIM: Disponibilidade ou compromisso declarado. — NÃO: Indisponibilidade declarada. — FALTA JUSTIFICADA: Estado factual pós-sessão; não usar como disponibilidade futura. — TALVEZ: Disponibilidade incerta declarada. — NAO: Forma canônica sem acento para indisponibilidade declarada.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0002",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_FUNCOES', linhas 1-6, colunas A-C",
  "trecho_literal": "funcao | ativo | observacao — GOLEIRA, DEFESA, ATAQUE: 'Equivale a X nas abas atuais.' — CORINGA: 'Função híbrida, se validada pela fonte humana.' — INDEFINIDA: 'Usar quando não houver fonte validada.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0003",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_META', linha 12 (parametro=availability_semantics_decision)",
  "trecho_literal": "availability_semantics_decision | APPROVED_BY_HUMAN_STEWARD | Disponibilidade e presença factual são estados distintos.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0004",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_META', linha 4 (parametro=manual_input_policy)",
  "trecho_literal": "manual_input_policy | preservar | Não sobrescrever SIM/NAO/NÃO/TALVEZ/vazio; estados factuais exigem autorização humana.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0005",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_META', linha 7 (parametro=availability_semantics)",
  "trecho_literal": "availability_semantics | declaracao_nao_presenca | SIM/NAO/TALVEZ indicam disponibilidade ou compromisso, não comparecimento factual.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0006",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_META', linha 13 (parametro=canonical_presence_source)",
  "trecho_literal": "canonical_presence_source | CEPRAEA DATABASE!DB_PRESENCA_FATUAL | Registro somente pós-sessão e com autorização humana.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0007",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_META', linha 9 (parametro=next_training_rule)",
  "trecho_literal": "next_training_rule | data_hora_futura_e_status_planejado | Treino do mesmo dia já encerrado não permanece como próximo.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0008",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_META', linha 14 (parametro=canonical_availability_indicators)",
  "trecho_literal": "canonical_availability_indicators | CEPRAEA DATABASE!DB_INDICADORES_DISPONIBILIDADE | Indicadores derivados da disponibilidade declarada.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0009",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'Página16' (oculta), célula A1, bloco YAML 'availability_values'",
  "trecho_literal": "availability_values: allowed: [SIM, NAO, TALVEZ]; forbidden: [sim, não, N, OK, confirmado, free_text]",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0010",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'Página16' (oculta), célula A1, cabeçalho do documento e bloco 'governance'",
  "trecho_literal": "contract_id: CEPRAEA_UI_CONTRACT_v1_2; ssot.spreadsheet: CEPRAEA ABRIL 2026; ssot.hidden_sheet: Pagina16 — este contrato declara sua própria fonte de verdade como um arquivo diferente (CEPRAEA ABRIL 2026), embora uma cópia apareça dentro de SRC-001. governance.human_approval_required_for inclui 'status_semantics_change'.",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0011",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'Página16' (oculta), célula A1, bloco YAML 'risk_system'",
  "trecho_literal": "risk_system.allowed_values: ['🟢 OPERACIONAL', '🟡 ATENÇÃO', '🟠 DEFESA CURTA', '🔴 SEM GOLEIRA', '🔴 CRÍTICO']; must_use: [icon, text]; forbidden: [color_only]",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0012",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'Página16' (oculta), célula A1, bloco YAML 'competitiveness_index' e 'player_criticality'",
  "trecho_literal": "competitiveness_index.inputs: [disponibilidade, funcoes, criticidade]; output: percentage; ranges: excelente>=95, competitivo>=82, atencao>=65, critico<65; manual_score_forbidden: true. player_criticality.allowed_values: [ALTA, MEDIA, BAIXA]",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0013",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'DISPONIBILIDADE BR e RJ' (oculta), linha 1 (cabeçalho de etapas) e coluna B (nomes de atletas, linhas 2-19)",
  "trecho_literal": "Estrutura: coluna A = número sequencial; coluna B = nome completo da atleta (18 linhas); colunas C-O = uma etapa competitiva por coluna (ex.: 'Copa do Brasil', 'RJ - 1ª Etapa'...), valor = resposta SIM/NAO/TALVEZ; linha final = contagem de atletas disponíveis por etapa.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "Coluna B contém nomes completos reais de 18 atletas. Conforme docs/standards/guia_estilo_documentação.md (exemplo de PII, 'nomes reais de atletas, CPFs'), os nomes não são reproduzidos aqui — apenas a estrutura da coluna e a contagem de linhas."
}
```

```json
{
  "id_evidencia": "EVD-0014",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGOSTO - 2026' (visível), linha 2 (subtítulo)",
  "trecho_literal": "AGENDA DE TREINOS E DECLARAÇÃO DE DISPONIBILIDADE / COMPROMISSO",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0015",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'JULHO - 2026' (oculta), linha 2 (subtítulo)",
  "trecho_literal": "AGENDA DE TREINOS E CONFIRMAÇÃO DE PRESENÇA",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0016",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'MAIO - 2026' (oculta), linhas 4-9, colunas C-K (amostra)",
  "trecho_literal": "Mesma matriz de resposta por atleta/data usada em meses mais recentes, mas com valores 'Ok'/'Out' em vez de 'SIM'/'NAO'/'TALVEZ' — vocabulário anterior à consolidação registrada em R_STATUS/R_META.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0017",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '📑_CHANGELOG' (oculta), linha 4, coluna E (registro de 2026-08-09T16:18:09)",
  "trecho_literal": "Disponibilidade separada de presença; próximo treino agora 13/08; jogos e adversários alinhados; clima ligado à etapa de 23/08; feedback suspenso; registries atualizados.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0018",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '📑_CHANGELOG' (oculta), linha 3 (registro de 2026-06-22T01:37:00)",
  "trecho_literal": "Correção humana: atualizada função principal de uma atleta em AGENDA CEPRAEA para Goleira. Fórmulas do painel mensal usam essa fonte.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "A entrada original do changelog cita o nome completo da atleta corrigida; substituído aqui por 'uma atleta', conforme tratamento de nomes reais (ver EVD-0013)."
}
```

```json
{
  "id_evidencia": "EVD-0019",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'PAINEL DATABASE' (oculta), linhas 5-6 e 9-14",
  "trecho_literal": "ELENCO — Total de atletas: 19, Goleiras: 3, Defesas: 7, Ataques: 12. POSIÇÕES DE ATAQUE — Centrais: 5, Laterais esquerdas: 3, Laterais direitas: 2, Pivôs: 2. POSIÇÕES DE DEFESA — Defensoras soltas: 2, Defensora base: 1, Defensora cobertura: 1, Goleiras: 3.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0020",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'PRÓXIMO TREINO' (oculta), linhas 3-10",
  "trecho_literal": "Data: 13/08/2026 | Horário: 20:00-21:30 | Status: OK. COMPOSIÇÃO POR DISPONIBILIDADE DECLARADA — Goleiras: 1, Defesa: 3, Ataque: 6.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0021",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '🏖️ DIA DO JOGO' (visível), linhas 3-5 e 22-31",
  "trecho_literal": "STATUS: 🟡 ETAPA PREVISTA — TABELA PENDENTE. CONVOCADAS, por posição (GOLEIRAS / DEFESA / ATAQUE): 'Aguardando convocação do treinador' nas três seções.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0022",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'ANÁLISE JOGOS' (visível), linhas 4-14",
  "trecho_literal": "RESUMO GERAL — Jogos: 19, Vitórias: 12, Derrotas: 7, Aproveit.: 63%, Sets pró: 28, Sets contra: 17. POR COMPETIÇÃO — 4 competições listadas com colunas J/V/D/%/Status (ex.: 'Copa do Brasil' 5J-5V-0D-100%-OK).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0023",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_DATES' (oculta), linhas 1-4 (amostra de 26 linhas totais)",
  "trecho_literal": "data | dia_horario | origem | aba_alvo — cada linha mapeia uma data-serial a um horário/evento textual, à célula de origem na aba mensal e à aba mensal alvo.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0024",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'R_MONTHS' (oculta), linhas 1-4",
  "trecho_literal": "mes | ano | aba | status — junho: historico; julho: historico; agosto: ativo. Cada mês do calendário é mapeado a exatamente uma aba e a um status de ciclo de vida (historico/ativo).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0025",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA CEPRAEA' (visível), linha 4 (cabeçalho colunas R-AD) e linha 27 (totais)",
  "trecho_literal": "Colunas R/S/T = 'Função principal' / 'Criticidade' / 'Ação técnica' por atleta (criticidade observada: Alta, Muito alta, Média, Baixa, A validar). Colunas U-AD replicam os totais de disponibilidade sob o rótulo 'Formula engine', coerente com hidden_technical_layers.U_AG do contrato de UI (EVD-0010).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0026",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '📅 FEEDBACK INDIVIDUAL — PRÓXIMO CICLO' (oculta), linhas 3-6",
  "trecho_literal": "STATUS DO MÓDULO: SUSPENSO — aguardando definição do novo ciclo pelo treinador. REGRAS: 1 atleta por horário • 1 horário por atleta • Feedback individual não será registrado na planilha.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0027",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '_FRONTEND_CHANGELOG' (oculta), linha 2 (registro FLOG-0001)",
  "trecho_literal": "Criar ponte técnica database para frontend — Criada aba oculta _IMPORT_DATABASE com IMPORTRANGE para 'CEPRAEA DATABASE!DB_EXPORT_FRONTEND!A1:I15'.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0028",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '_IMPORT_ANALISE_JOGOS' (oculta), linhas 1-6",
  "trecho_literal": "tipo | item_id | campo_01...campo_10 — linhas tipo=COMPETICAO com item_id no padrão COMP-2026-NNN, incluindo uma competição com status COM_PENDENCIAS (0 jogos registrados).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

### Complemento — abas inicialmente descartadas por nome, reabertas após achado do REVIEWER (revisão adversarial)

```json
{
  "id_evidencia": "EVD-0029",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA TÉCNICA V2' (oculta), linhas 34-42 (BLOCO 2 - LEITURA TÉCNICA POR COMPETIÇÃO)",
  "trecho_literal": "Colunas: Competição/Local | Inscrição | Taxa | Relação nominal | Confirmadas | Talvez | Não | Situação | Risco de elenco | Foco técnico | ... Situação observada: 'Realizada / histórico' ou 'Próxima / acompanhamento'. Risco de elenco observado: Estável, Moderado ou Atenção — granularidade por competição, distinta do status de risco elenco-geral do contrato de UI.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0030",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA TÉCNICA V2' (oculta), linha 2 e linha 4 (rótulos de bloco)",
  "trecho_literal": "'Fonte: AGENDA CEPRAEA. As abas mensais continuam sendo o fluxo recorrente de presença. Esta aba organiza as competições já respondidas.' / 'BLOCO 1 - MATRIZ ORIGINAL MATERIALIZADA — Preenchimento preservado; competições passadas podem ser recolhidas sem perder histórico.'",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0031",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA TÉCNICA MODELO' (oculta), linhas 1-8 (modelo/template vazio)",
  "trecho_literal": "'Modelo não destrutivo para redesenhar a agenda... A aba AGENDA CEPRAEA permanece intacta.' MATRIZ DAS ATLETAS (linha 8, template sem dados reais): Função=Goleira/Defesa/Ataque; Criticidade=Baixa/Média/Alta/Muito alta; Ação técnica=Confirmar/Monitorar/Cobrir posição.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0032",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '3ª ETAPA CARIOCA 2026' (oculta), linhas 21-33 (JOGOS DO CEPRAEA / CENÁRIOS DE CLASSIFICAÇÃO)",
  "trecho_literal": "Status de jogo observado: GARANTIDO, CONDICIONAL. Estrutura de fase/grupo: 'Grupo FB', cenários '1º ou 2º → Semifinal', '3º → Disputa 5º/6º'. Nomes de equipes adversárias (não são PII — entidades organizacionais, não pessoas): NR Beach, Niterói Rugby.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0033",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '3ª ETAPA CARIOCA 2026' (oculta), linha 34",
  "trecho_literal": "Observação: Resultados e participação real serão atualizados apenas após fonte validada.",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0034",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '3ª ETAPA CARIOCA 2026' (oculta), linhas 36-45 (CRONOGRAMA GERAL DA COMPETIÇÃO)",
  "trecho_literal": "Coluna 'Naipe' com valores F/M identificando categoria feminino/masculino por confronto — inclui confrontos de outras equipes, não só CEPRAEA (ex.: 'Rio Handbeach x ADM Maricá').",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

### Complemento — leitura completa das duas abas parcialmente lidas (achado do REVIEWER, segunda rodada)

```json
{
  "id_evidencia": "EVD-0035",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA TÉCNICA V2' (oculta), linha 43 (etapa BR 4ª Etapa, CEPRAEA NÃO PARTICIPARÁ)",
  "trecho_literal": "Situação: 'CEPRAEA não participará' | Risco de elenco: 'Não aplicável' | Foco técnico: 'Sem preparação específica' | Observação para atletas: 'Disponibilidades preservadas apenas como histórico.'",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0036",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA TÉCNICA V2' (oculta), linhas 50-52 (BLOCO 3 - CICLO DE TREINO / ANALISE)",
  "trecho_literal": "Bloco inteiramente em template ('Selecionar competição', 'Exercícios-chave do treino', 'Recado técnico para o grupo') — nenhum dado real preenchido.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0037",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '3ª ETAPA CARIOCA 2026' (oculta), linhas 46-56 (CRONOGRAMA GERAL DA COMPETIÇÃO, continuação) e linha 69 (RODAPÉ DE CONTROLE)",
  "trecho_literal": "Confrontos adicionais entre equipes terceiras (ex.: 'IDEC x IDEC B'), estrutura de mata-mata com referências a vencedor/perdedor de jogos anteriores (ex.: 'Perdedor J14 x Perdedor J15'), intervalos programados. Rodapé: 'Aba oculta para uso da comissão técnica. Resultados, placares e participação real só devem ser atualizados após fonte validada.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0038",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba '3ª ETAPA CARIOCA 2026' (oculta), linhas 58-65 (RELAÇÃO NOMINAL CEPRAEA)",
  "trecho_literal": "Colunas: Nº | Atleta | Função | Status — Status observado em todas as linhas: 'Convocada'. Coluna 'Nº' não é sequencial (valores observados incluem números como 3, 4, 6, 7, 8, 12, 14, 16, 22, 25, 28, 85), diferente da numeração sequencial 1-19 usada como coluna 'A'/'#' nas matrizes mensais de disponibilidade (DISPONIBILIDADE BR e RJ, AGOSTO - 2026, AGENDA CEPRAEA).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "A tabela lista nomes completos (inclusive nomes legais mais completos que os usados nas abas mensais, ex.: sobrenomes adicionais) de atletas convocadas. Nenhum nome é reproduzido — apenas estrutura das colunas e o padrão do identificador 'Nº'."
}
```

### Complemento — leitura integral das abas remanescentes (achado do REVIEWER, terceira rodada)

As 17 abas mensais históricas antes amostradas por inferência (`JUNHO - 2026` a `JUNHO 2024`,
exceto `MAIO - 2026`/`JULHO - 2026`, já lidas) e a aba `ANÁLISE DOS JOGOS` (oculta, distinta da
aba visível `ANÁLISE JOGOS`, omitida por colisão de nome) foram lidas por completo nesta rodada.

```json
{
  "id_evidencia": "EVD-0039",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'JUNHO 2024' (oculta), coluna K, linhas 3-11 (matriz de disponibilidade); ocorrência adicional em 'NOVEMBRO 2024' (oculta), colunas E, H, L, P",
  "trecho_literal": "Valor de resposta 'Tentarei'/'tentarei' presente na matriz de disponibilidade — terceira variante de vocabulário histórico, distinta de SIM/NAO/TALVEZ (JUNHO-2026 em diante) e de Ok/Out/Talvez (ABRIL-2026 a JUNHO-2024). Não coberta pelo enum do contrato de UI (EVD-0009) nem pela observação de R_STATUS (EVD-0001).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0040",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "abas 'ABRIL - 2026' a 'JUNHO 2024' (17 abas ocultas), colunas de resposta de disponibilidade em cada matriz mensal",
  "trecho_literal": "Leitura integral (não amostral) confirma que o vocabulário 'Ok'/'Out'/'Talvez' (e a variante 'Tentarei', EVD-0039) é o padrão predominante por aproximadamente dois anos (JUNHO 2024 a ABRIL 2026), não uma amostra isolada como registrado na rodada anterior — o vocabulário 'SIM'/'NAO'/'TALVEZ' (R_STATUS, EVD-0001) é o mais recente, confirmado a partir de 'JUNHO - 2026' em diante.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0041",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "abas 'JUNHO 2024' a 'NOVEMBRO E DEZEMBRO 2024' (6 abas ocultas), coluna de nome da matriz de disponibilidade, comparada à relação de 19 atletas de 'AGOSTO - 2026'",
  "trecho_literal": "Nomes presentes nas matrizes de disponibilidade de 2024 incluem atletas que não constam da relação de 19 atletas de AGOSTO - 2026 (e vice-versa) — estrutura consistente com entrada/saída de elenco ao longo do tempo. Nomes não comparados literalmente aqui (dado sensível); apenas a divergência estrutural entre as relações é registrada.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "Comparação de listas de nomes entre abas realizada apenas estruturalmente (presença/ausência de correspondência), sem reproduzir nenhum nome literal nesta evidência ou em qualquer outro artefato do dossiê."
}
```

```json
{
  "id_evidencia": "EVD-0042",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'ANÁLISE DOS JOGOS' (oculta), seção 'PARTICIPAÇÃO DAS ATLETAS', colunas 'Fonte' e 'Obs.', linhas 22-39",
  "trecho_literal": "Fonte: 'DB_PARTICIPACAO_JOGO' | Obs.: 'jogo_real = status_participacao JOGOU' — regra de cálculo explícita definindo participação real em jogo a partir do valor 'JOGOU' no campo status_participacao. Status observado também inclui 'SEM JOGO' para atletas sem jogos registrados no período.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "As linhas desta seção associam estatísticas de jogo (J/V/D/%) a nomes de atletas individuais. Nenhum nome é reproduzido — apenas a fórmula de derivação e o nome do ativo técnico de origem."
}
```

```json
{
  "id_evidencia": "EVD-0043",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'ANÁLISE DOS JOGOS' (oculta), linha 3 (cabeçalho de aviso)",
  "trecho_literal": "NÃO PREENCHER MANUALMENTE • ALTERAÇÕES FACTUAIS DEVEM SER FEITAS NO DATABASE",
  "tipo_evidencia": "CELULA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0044",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'ANÁLISE DOS JOGOS' (oculta), linhas 6-7 (RESUMO GERAL), comparada à aba 'ANÁLISE JOGOS' (visível), linhas 5-6 (RESUMO GERAL)",
  "trecho_literal": "'ANÁLISE DOS JOGOS' (oculta): Jogos totais=23, Vitórias=14, Derrotas=9, Aproveitamento=61% — total internamente consistente com a soma da própria quebra por adversário na mesma aba. 'ANÁLISE JOGOS' (visível, já registrada como fonte de TERMO-008): Jogos=19, Vitórias=12, Derrotas=7, Aproveitamento=63% — também internamente consistente com sua própria quebra por competição. Os dois resumos gerais, para a mesma temporada, divergem entre si.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

### Complemento — leitura integral de `AGENDA CEPRAEA` (achado do REVIEWER, quarta rodada)

A aba `AGENDA CEPRAEA` (1000 linhas de capacidade) havia sido amostrada nas ~30 primeiras linhas
sob a presunção de que compartilhava a estrutura recorrente das matrizes semanais de treino — uma
inferência não verificada, do mesmo tipo já corrigido nas rodadas anteriores. A aba foi lida por
completo (ferramenta própria, sem corte de linha) e revelou-se estruturalmente distinta: uma visão
de temporada por competição, não uma matriz semanal, com uma camada de cálculo própria rotulada
"Formula engine".

```json
{
  "id_evidencia": "EVD-0045",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA CEPRAEA' (visível), varredura das 1000 linhas de capacidade via ferramenta de leitura própria",
  "trecho_literal": "Varredura completa (não amostral) confirma 44 linhas com conteúdo, todas entre as linhas 2 e 45; nenhuma linha entre 46 e 1000 contém dado. Última linha populada: 45.",
  "tipo_evidencia": "METADADO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0046",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA CEPRAEA' (visível), linhas 5-7 (cabeçalho por etapa/competição)",
  "trecho_literal": "Linhas 'Data da competição', 'Inscrição até' e 'Relação nominal até' — três datas distintas por etapa/competição da temporada, além da data do evento em si.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0047",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA CEPRAEA' (visível), colunas 'Função principal'/'Criticidade'/'Ação técnica', linhas 8-26",
  "trecho_literal": "Coluna 'Ação técnica' com valor textual por atleta, ao lado de 'Função principal' e 'Criticidade' (já observados em TERMO-004/TERMO-011). Valores distintos observados: 'Confirmar disponibilidade', 'Monitorar agenda da seleção', 'Garantir cobertura da posição', 'Validar função com comissão', 'Confirmar interesse'.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "A coluna associa uma recomendação a cada atleta individualmente. Nenhum nome é reproduzido — apenas os valores distintos de recomendação observados."
}
```

```json
{
  "id_evidencia": "EVD-0048",
  "id_fonte": "SRC-001",
  "id_acao": "AC-001",
  "localizacao": "aba 'AGENDA CEPRAEA' (visível), colunas U-AD (bloco 'Formula engine'), linhas 27-37",
  "trecho_literal": "Bloco rotulado 'Formula engine' com contagens (atletas disponíveis/confirmadas/talvez/não), um valor percentual por etapa (ex.: 90, 95, 83, 79, 88) com rótulo qualitativo correspondente ('Competitivo', 'Excelente', 'Atenção') e uma coluna de status por etapa com apenas três valores observados aqui: 'OPERACIONAL', 'ATENÇÃO', 'NÃO PARTICIPA' (esta última na etapa marcada 'CEPRAEA NÃO PARTICIPARÁ', REGRA-007). Os valores percentuais observados são consistentes com as faixas já documentadas em TERMO-010 (excelente >=95%, competitivo >=82%, atenção >=65%).",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": true,
  "tratamento_dado_sensivel": "A linha 31 ('Pendentes') deste mesmo bloco replica, nas colunas U-AD, os nomes de atletas pendentes já listados nas colunas F-O da mesma linha (fora do bloco 'Formula engine' propriamente dito, mas dentro do intervalo de linhas desta evidência). Nenhum nome é reproduzido nesta evidência — apenas a estrutura do bloco e os valores agregados/qualitativos."
}
```

## SRC-002 / AC-002 — `BancoCEPRAEA.docx`

```json
{
  "id_evidencia": "EVD-0049",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 4 'Princípios obrigatórios do domínio', tabela DOM-001 a DOM-010",
  "trecho_literal": "DOM-001 Disponibilidade ≠ presença real. DOM-002 Lista prevista ≠ presença real. DOM-003 Convocação de etapa ≠ escalação/roster de partida ≠ participação real. DOM-004 Nome não é chave; joins usam UUID ou código legado controlado. DOM-005 Respostas, correções, presença e eventos de vínculo preservam histórico. DOM-006 Justificativas são privadas e nunca integram listas compartilhadas. DOM-007 ESPECIALISTA = CORINGA; ambos são papel tático contextual, não função ampla nem posição permanente. DOM-008 Indicadores são projeções de fatos validados. DOM-009 Mudança de regra esportiva não reescreve fatos históricos. DOM-010 Nenhum dado real é autorizado no estágio sintético atual.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0050",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 7 'Catálogo de tabelas', tabela de 23 linhas (# / Nome da tabela / Descrição)",
  "trecho_literal": "23 tabelas físicas nos schemas public (21), private (1: response_justifications) e audit (1: audit_events), cobrindo equipe/temporada, identidade/acesso, elenco, agenda/treino, solicitação/resposta/correção, lista prevista, presença factual, comunicação e auditoria.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0051",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 8 'Relações entre as tabelas', tabela de 19 linhas (Origem/Destino/Cardinalidade/Finalidade/Exclusão)",
  "trecho_literal": "19 relações tabela-a-tabela documentadas; regra geral de exclusão é RESTRICT ('fatos históricos não devem desaparecer em cascata'), SET NULL restrito a relações opcionais de conta/autor.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0052",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seções 9.5 (public.athletes) e 9.6 (public.athlete_roster_memberships)",
  "trecho_literal": "athletes: 'Identidade esportiva estável da atleta. Não guarda função, posição ou status temporal do elenco; esses atributos pertencem ao vínculo de temporada.' Coluna legacy_athlete_id: 'Código estável da planilha, como ATH-0001... Conciliar legado sem depender do nome.' athlete_roster_memberships: 'Vínculo temporal da atleta com uma temporada. Guarda estado do elenco, função ampla corrigida e número de camisa.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0053",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 11 'Segurança, RLS e privacidade', prosa introdutória + função private.is_team_coach",
  "trecho_literal": "'O treinador opera apenas equipes em que possui vínculo COACH ativo e MFA AAL2. A atleta lê e altera apenas seus próprios fluxos... Service role nunca deve ser incluída no frontend.' Função is_team_coach exige coalesce(auth.jwt() ->> 'aal', 'aal1') = 'aal2'. Seção 9.3 (profiles), regra da tabela: 'Não armazenar senha, token ou segredo.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0054",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 9.16 (private.response_justifications) e 9.15 (public.justification_categories)",
  "trecho_literal": "response_justifications: 'Conteúdo privado opcional associado a uma resposta. Fica fora do schema exposto e só é acessado por RPCs autorizadas.' justification_categories possui coluna 'sensitive' (boolean); seed sintético marca categorias 'PERSONAL' e 'HEALTH_PRIVATE' como sensitive=true, com descrição 'Não solicitar diagnóstico.' para a segunda.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0055",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 13.4 'Integridade e triggers', funções validate_training_commitment/validate_roster_scope/validate_response_option",
  "trecho_literal": "training_sessions_validate_commitment: 'if v_type is distinct from TREINO then raise exception'. roster_validate_scope: 'if v_athlete_team is distinct from v_season_team then raise exception Atleta e temporada pertencem a equipes diferentes'. responses_validate_option: 'if v_expected is distinct from v_actual then raise exception Opção não pertence à definição da solicitação'.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0056",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 13.4 'Integridade e triggers', bloco '-- append-only'",
  "trecho_literal": "Triggers before update or delete executando private.prevent_update_delete() em cinco tabelas: athlete_roster_events, operational_responses, response_corrections, attendance_records, audit.audit_events. Função prevent_update_delete: 'raise exception Tabela append-only: operação % não permitida em %.%'.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0057",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 10 'Views e indicadores derivados', view v_availability_attendance_divergence",
  "trecho_literal": "View calcula divergence_code comparando effective_semantic_group (disponibilidade declarada) com attendance_status (presença factual): 'CONFIRMED_BUT_ABSENT' quando declarou AFFIRMATIVE mas attendance_status=AUSENTE; 'UNAVAILABLE_BUT_ATTENDED' quando declarou NEGATIVE mas compareceu; 'ATTENDANCE_NOT_RECORDED' quando não há registro de presença.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0058",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 15 'Contrato de extensibilidade futura', bloco 'Regra específica de especialista/coringa'",
  "trecho_literal": "'Código canônico do papel tático: ESPECIALISTA. Alias de domínio/legado: CORINGA. Nunca adicionar ESPECIALISTA ou CORINGA ao enum broad_player_function.' Tabela do topo do documento (seção 1) já classifica: 'Especialista/coringa: Mesmo papel tático contextual; fora do cadastro e fora do MVP atual.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0059",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 15 'Contrato de extensibilidade futura', tabela de 12 módulos futuros",
  "trecho_literal": "'As entidades abaixo são previstas, mas não devem ser criadas no MVP atual.' Inclui competitions, competition_stages, competition_rule_snapshots, matches, match_periods, match_rosters, match_participations, match_role_assignments, result_validations, source_documents/record_provenance, import_batches/import_batch_items, external_metric_snapshots.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0060",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 16 'Matriz de substituição das planilhas', tabela de 12 linhas",
  "trecho_literal": "Mapeia DB_ATLETAS → athletes+athlete_roster_memberships; DB_FUNCOES → enum broad_player_function; DB_TREINOS+DB_CALENDARIO → commitments+training_sessions+v_calendar; DB_PRESENCA → requests/recipients/responses ('Tratar como disponibilidade antecipada'); Presença observada → attendance_records ('Novo fato posterior ao treino'); DB_AVISOS → communications+communication_recipients; DB_CONVOCACOES → módulo futuro; DB_JOGOS → módulo futuro de matches; DB_INDICADORES/EXPORTS → views ('Não persistir métricas deriváveis'); DB_CHANGELOG → audit_events.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0061",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 13.9 '0008_seed_synthetic.sql'",
  "trecho_literal": "'-- Somente ambiente sintético. Não importar nomes ou contatos reais.' Todos os valores de exemplo usam UUIDs fixos de placeholder (ex.: '11111111-1111-4111-8111-111111111111') e rótulos genéricos ('Temporada sintética 2026'); nenhum nome de pessoa real.",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0062",
  "id_fonte": "SRC-002",
  "id_acao": "AC-002",
  "localizacao": "seção 3 'Regras normativas consideradas' + seção 9.6 (athlete_roster_memberships), coluna shirt_number e constraint roster_shirt_number_ck",
  "trecho_literal": "'As alterações IHF válidas desde 1º de abril de 2026 permitem números de uniforme de 1 a 99; por isso shirt_number é temporal e validado nesse intervalo.' Constraint: 'check (shirt_number is null or shirt_number between 1 and 99)'. Regra de coluna: 'Entre 1 e 99 conforme regra IHF vigente desde 01/04/2026; pode variar por temporada.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

## SRC-003 / AC-003 — `CEPRAEA-DB.docx`

```json
{
  "id_evidencia": "EVD-0063",
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "localizacao": "seção 'GATE-F00-GOV-01 — MATERIALIZAÇÃO DA GOVERNANÇA ADAPTATIVA', fim do documento extraído",
  "trecho_literal": "'Diretriz de Execução Imediata: Confirmada a integração deste escopo no CEPRAEA-DB, deve-se instanciar o ambiente físico de testes (ACT-F00-007) para prosseguir em linha com a Execução do Piloto Integrado (ACT-F00-009).' Este é o último trecho do documento — nenhuma seção posterior alcança schema físico, CREATE TABLE ou modelo de banco.",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0064",
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "localizacao": "seção 'C17.2 Resultado reconciliado' (números de reconciliação) e início de 'C17.3 Inventário atual integral' (cabeçalho da tabela dos 65 itens) — distinta de 'C15.3 Inventário integral', que documenta o inventário histórico de 43 itens; linhas 761-772 do texto extraído",
  "trecho_literal": "'Pasta: FONTES → BEACH HANDBALL, ID 1Z0OsR3dHmLMED0KYc_EE2lD1nEYykzWY. Itens atuais: 65. Formatos atuais: 60 PDFs, 3 XLSX e 2 Markdown... Reconciliação: 43 históricos − 8 ausentes + 30 novos = 65 atuais.'",
  "tipo_evidencia": "TABELA",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0065",
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "localizacao": "seção 'C1.5 Contexto fixado'",
  "trecho_literal": "'Público inicial: um treinador e 19 atletas adultas. Modalidade: handebol de areia. Categoria inicial: adulto feminino. Backend previsto: Supabase/PostgreSQL.'",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0066",
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "localizacao": "seção 'C2.2 Escopo negativo'",
  "trecho_literal": "'inserir dados pessoais reais em seeds ou ambientes de teste' e 'apagar fatos históricos para representar correções' listados entre os itens fora de escopo salvo mudança formal aprovada.",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0067",
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "localizacao": "seção 'C0. REGRA DE SUPREMACIA E FINALIDADE DO CONTROLE'",
  "trecho_literal": "'Exemplos de tabelas, campos, módulos, SQL ou arquitetura permanecem hipóteses até atravessarem os portões correspondentes. A ausência de informação não autoriza a invenção.'",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```

```json
{
  "id_evidencia": "EVD-0068",
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "localizacao": "seções 'ACT-F00-001' a 'ACT-F00-009' (Fase 0), busca textual sobre o documento inteiro",
  "trecho_literal": "Nove ações controladas (ACT-F00-001 a ACT-F00-009) dedicadas a governança/portões/teste do próprio processo (Maker/Checker, canonicalização JSON, migração append-only, piloto de extração). Busca por 'create table'/'CREATE TABLE' sobre as 4059 linhas extraídas: zero ocorrências.",
  "tipo_evidencia": "TEXTO",
  "dado_sensivel_encontrado": false
}
```
