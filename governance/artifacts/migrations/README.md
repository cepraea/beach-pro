# Migrações históricas de governança

Este diretório contém artefatos append-only produzidos por ações formais de migração.

Para `ACT-F00-008`, os registros originais permanecem intocados. Os arquivos em `act-f00-008/` inventariam as ocorrências do termo legado, classificam seu papel semântico e vinculam cada estado ativo legado a um registro de normalização determinístico.

## Formatos persistidos

- inventário completo: `legacy-approved-inventory.json.gz`;
- registros migrados: `migrated-records.jsonl.gz`;
- mapa, resumo, regressão e pendências: JSON aberto.

A compressão GZIP é determinística e não modifica o conteúdo lógico. O pipeline descompacta os arquivos para validação estrutural e comparação byte a byte com uma regeneração executada sobre o commit-base autorizado.

Esses artefatos não constituem aprovação humana, não autorizam `ACT-F00-009` e não liberam `GATE-F00-GOV-01`.
