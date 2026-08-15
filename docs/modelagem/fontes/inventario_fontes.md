# Inventário de fontes

Tabela mestra das 28 entradas de `.drive/CEPRAEA BEACH PRO/` (27 arquivos reais + 1 registro de
bloqueio para a fonte ausente, seção 2 do plano). A ordem de processamento é a da seção 10 do
plano — sempre sequencial, nunca em paralelo. `estado_processamento` aqui espelha o campo de mesmo
nome no dossiê correspondente (`fontes/dossies/<slug>.md`, `schema_fonte.json`); esta tabela é a
visão consolidada, o dossiê é o registro de fato.

A coluna "Hipótese" é `tipo_fonte·autoridade_fonte·proveniencia_fonte`, sempre a confirmar ou
refutar no dossiê — nunca presumida como definitiva antes do processamento real (seção 10 do
plano). `AC-021` não tem hipótese: a fonte já é conhecida como ausente do disco (D-01).

| `id_fonte` | `id_acao` | Arquivo | Hipótese | `estado_processamento` | Checkpoint |
| --- | --- | --- | --- | --- | --- |
| SRC-001 | AC-001 | `CEPRAEA AGOSTO 2026.xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Não |
| SRC-002 | AC-002 | `BancoCEPRAEA.docx` | TECNICA·AUXILIAR·ORIGINAL | NAO_INICIADO | Sim |
| SRC-003 | AC-003 | `CEPRAEA-DB.docx` | TECNICA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |
| SRC-004 | AC-004 | `CEPRAEA DATABASE.xlsx` | OPERACIONAL·INDETERMINADA·INDETERMINADA | NAO_INICIADO | Não |
| SRC-005 | AC-005 | `DESC-CEPRAEA.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |
| SRC-006 | AC-006 | `Glossário de Dados — CEPRAEA v0.1.xlsx` | TECNICA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |
| SRC-007 | AC-007 | `REGISTRO MESTRE DE ARTEFATOS E FUNCIONAMENTO — SISTEMA CEPRAEA.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |
| SRC-008 | AC-008 | `CEPRAEA 2026(1).xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Sim |
| SRC-009 | AC-009 | `CEPRAEA 2026.xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Não |
| SRC-010 | AC-010 | `CEPRAEA 2026(2).xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Não |
| SRC-011 | AC-011 | `CEPRAEA_Preparacao_Competitiva_Ago_Set_2026.pdf` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | NAO_INICIADO | Não (canário de PDF) |
| SRC-012 | AC-012 | `CEPRAEA JULHO 2026.pdf` | OPERACIONAL·PRIMARIA·DERIVADA | NAO_INICIADO | Não |
| SRC-013 | AC-013 | `CEPRAEA_Preparacao_Competitiva_2026_CORRIGIDO.pdf` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | NAO_INICIADO | Não |
| SRC-014 | AC-014 | `CEPRAEA_Preparacao_Competitiva_2026_FINAL_ACESSIVEL.pdf` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | NAO_INICIADO | Não |
| SRC-015 | AC-015 | `CEPRAEA.pdf` | INDETERMINADO·INDETERMINADA·INDETERMINADA | NAO_INICIADO | Não |
| SRC-016 | AC-016 | `CEPRAEA ABRIL 2026.xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Não |
| SRC-017 | AC-017 | `Implementação — Pesquisa de Treinos CEPRAEA 2026.xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Não |
| SRC-018 | AC-018 | `# Autoavaliação – CEPRAEA.xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Sim |
| SRC-019 | AC-019 | `CEPRAEA — Wellness — Configuração e Respostas.xlsx` | OPERACIONAL·PRIMARIA·ORIGINAL | NAO_INICIADO | Sim |
| SRC-020 | AC-020 | `CEPRAEA — Wellness — Apps Script Mobile.txt` | TECNICA·AUXILIAR·DERIVADA | NAO_INICIADO | Não |
| SRC-021 | AC-021 | `Cópia de CEPRAEA — Wellness — Apps Script Mobile.txt` | (arquivo ausente — D-01) | NAO_INICIADO | Não |
| SRC-022 | AC-022 | `Preparação competitiva CEPRAEA 2026 — Treinos e cenários até a Fase Final.docx` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | NAO_INICIADO | Não |
| SRC-023 | AC-023 | `Preparação competitiva CEPRAEA 2026 — calendário e cenários — versão acessível.docx` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | NAO_INICIADO | Não |
| SRC-024 | AC-024 | `Preparação competitiva CEPRAEA 2026 — versão corrigida.docx` | ADMINISTRATIVA·AUXILIAR·INDETERMINADA | NAO_INICIADO | Não |
| SRC-025 | AC-025 | `CEPRAEA BEACH PRO.docx` | INDETERMINADO·INDETERMINADA·INDETERMINADA | NAO_INICIADO | Não |
| SRC-026 | AC-026 | `CEPRAEA-pdf.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |
| SRC-027 | AC-027 | `Roteiro completo — Relatório curto e visual às atletas — CEPRAEA 2026.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |
| SRC-028 | AC-028 | `Roteiro relatório fase CEPRAEA.docx` | ADMINISTRATIVA·AUXILIAR·ORIGINAL | NAO_INICIADO | Não |

Checkpoints adicionais fora desta tabela: `AC-000` (bootstrap — arquivos escritos pelo `EXECUTOR`
e conferidos pelos validadores determinísticos disponíveis (`validar.mjs`,
`verificar_referencias.mjs`) nesta revisão; isso não é o mesmo que `estado_epistemologico=VALIDADO`
(`schema_elemento_modelo.json`), que exige confirmação humana — revisão independente do `REVIEWER`
e commit humano ainda pendentes. `estado_processamento` só é `CONCLUIDO` de fato depois que Davi
commitar com subject `AC-000 ...` e `verificar_repositorio.mjs` resolver esse `action_ref`; ver
`decisoes/registro_decisoes.md`) e `AC-029` (síntese final) — não têm linha aqui por não
corresponderem a uma fonte física (seção
10 do plano). Qualquer linha acima pode virar checkpoint de fato, mesmo sem estar marcada como tal,
se encontrar uma condição de parada da seção 9 do plano (nova colisão de nome, novo dado sensível,
nova fonte conflitante).
