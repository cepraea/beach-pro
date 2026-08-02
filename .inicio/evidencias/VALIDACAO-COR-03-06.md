# Validação de COR-03 a COR-06

## 1. Escopo

Esta evidência audita as definições normativas criadas para o dicionário de
campos, segmentação, classificação e enums. Ela não substitui o schema executável
de COR-13 nem a suíte funcional de COR-21.

## 2. Ambiente fixado

| Item | Valor |
| --- | --- |
| Norma | `.inicio/tradutor.md` |
| Versão do contrato | `1.0.0` |
| Parser | `markdown-it` |
| Versão normativa | `14.3.0` |
| Versão instalada | `14.3.0` |
| Encoding | UTF-8 estrito, sem normalização Unicode |

## 3. Resultado do auditor estrutural

O auditor temporário `/tmp/audit-cor-03-06.mjs` foi executado sobre a norma.

| Verificação | Resultado |
| --- | :---: |
| IDs `F-001` a `F-025` completos | PASS |
| IDs de campo únicos | PASS |
| Nomes de campo únicos | PASS |
| 25 campos encontrados | PASS |
| IDs `CR-001` a `CR-012` + `CR-999` completos | PASS |
| IDs e prioridades de regra únicos | PASS |
| Classes usadas pertencem ao enum fechado | PASS |
| `CR-999` termina em `AMBIGUOUS` | PASS |
| Parser normativo disponível | PASS |
| Cobertura integral de bytes especificada | PASS |
| UTF-8 estrito especificado | PASS |
| Erros para campo, classe e regra desconhecidos | PASS |
| Alias e coerção silenciosa proibidos | PASS |

Resultado agregado: `PASS`, com 18 verificações aprovadas e zero falhas.

## 4. Casos negativos normativos

| Entrada | Resultado obrigatório |
| --- | --- |
| Campo `Segment_ID` | `E_UNKNOWN_FIELD` + `BLOCKED` |
| Classe `protected_exact` | `E_UNKNOWN_CLASS` + `BLOCKED` |
| Regra `CR_001` | `E_UNKNOWN_CLASSIFICATION_RULE` + `BLOCKED` |
| Alias `segmento_conteúdo` | `E_UNKNOWN_FIELD` + `BLOCKED` |
| Extensão Markdown desconhecida | `CR-999`, `AMBIGUOUS` + `BLOCKED` |
| Duas regras empatadas com classes distintas | `E_CLASSIFICATION_CONFLICT` + `BLOCKED` |

Os resultados acima são exigências normativas verificadas por inspeção do enum
e das regras. Sua execução automatizada ficará pendente até COR-13/COR-21.

## 5. Pendências deliberadas

- schema processável do manifesto: COR-13;
- fixtures físicas de Unicode, CRLF, HTML, tabelas e Mermaid: COR-04/COR-17;
- execução real do segmentador e mapa de cobertura: COR-21;
- testes positivos e negativos de cada regra: COR-21;
- substituição dos nomes legados nas regras `REG-TRAD-001.1–001.5`: COR-07.

Por isso, esta evidência autoriza marcar as definições e auditorias estruturais,
mas não os checklists dependentes de execução funcional futura.
