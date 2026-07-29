# Desvios controlados da especificação VSCODE

## Controle

| Campo | Valor |
| --- | --- |
| Baseline | ESP-CEPRAEA-VSCODE-001 v1.0.0 |
| Data | 2026-07-28 |
| Estado | Proposto para aprovação do proprietário |

## DV-VSC-001 — Não conformidades no acervo Markdown preexistente

| Campo | Registro |
| --- | --- |
| Requisito relacionado | REQ-VSC-020 |
| Descrição | `npm run lint:md` encontra 1.414 ocorrências em 15 documentos preexistentes |
| Escopo | `docs/**/*.md` e `src/features/**/*.md` |
| Justificativa | O saneamento integral do acervo excede o escopo da especificação do Workspace e pode alterar documentos com integridade controlada |
| Tratamento atual | `lint:md:vscode` é bloqueante; `lint:md` permanece como auditoria ampla não bloqueante |
| Risco | Permanência de inconsistências editoriais no acervo documental |
| Mitigação | Não modificar automaticamente o acervo; abrir trabalho próprio com revisão da governança documental |
| Responsável | Mantenedor da documentação |
| Prazo de revisão | 2026-10-28 |
| Condição de encerramento | `npm run lint:md` termina com zero ocorrências ou a governança documental aprova uma baseline própria |
| Estado | Aguardando aprovação |

## DV-VSC-002 — Vulnerabilidades em dependências de desenvolvimento

| Campo | Registro |
| --- | --- |
| Requisito relacionado | REQ-VSC-022 |
| Descrição | `npm audit` informa 10 vulnerabilidades altas em cadeias de ferramentas de desenvolvimento |
| Produção | `npm audit --omit=dev` informa zero vulnerabilidades |
| Causa principal | `brace-expansion` transitivo por ESLint e Workbox |
| Justificativa | A correção indicada pelo npm exige `--force` e atualização incompatível do ESLint |
| Risco | Processamento malicioso ou excessivo por ferramentas locais de desenvolvimento |
| Mitigação | Não processar entradas não confiáveis; acompanhar releases; manter auditoria de produção bloqueante |
| Responsável | Desenvolvedor responsável |
| Prazo de revisão | 2026-08-28 |
| Condição de encerramento | Atualização compatível elimina os alertas e todas as portas de qualidade continuam aprovadas |
| Estado | Aguardando aprovação |

## Regra de aprovação

O proprietário DEVE registrar aprovação, rejeição ou novo tratamento para cada desvio. Um desvio
vencido não pode ser usado para aprovar a baseline.
