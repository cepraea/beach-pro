---
document_id: DOC-VAL-REL-G2-PROVENIENCIA-INICIAL
title: "Relatório inicial de G2 — Proveniência"
document_type: relatorio
version: "0.1.0"
workflow_status: RASCUNHO
permitted_uses:
  - orientacao_de_remediacao
  - auditoria
prohibited_uses:
  - declaracao_de_pass
  - promocao
  - canonizacao
---

# Relatório inicial de G2 — Proveniência

## Identificação

- **Gate:** `G2 — Proveniência`
- **Documento:** `DOC-CEPRAEA-CANDIDATA-CONTEXTO`
- **Versão:** `0.1`
- **Pacote:** `PROV-CEPRAEA-CONTEXTO-001`
- **Resultado:** `fail`
- **Efeito:** transição para `BASE_CONTROLADA` bloqueada

## Implementação realizada

O conteúdo legado foi mantido sem edição. A seção de fontes e a matriz de
claims foram extraídas para um pacote processável com 20 fontes e 30 claims,
todos vinculados à versão e ao hash preservados do documento.

O avaliador valida contratos, IDs, versão, hash, integridade referencial,
estado das fontes, localização, verificação, referência imutável, ambiguidade
textual e cobertura dos claims críticos.

## Resultado inicial

- fontes catalogadas: 20;
- claims catalogados: 30;
- claims críticos: 30;
- claims cobertos por fonte verificada ou incerteza explícita: 1;
- cobertura crítica: 3,33%;
- cobertura exigida: 100%;
- claims com referência ambígua: 4;
- fontes ativas e verificadas: 0.

O único claim coberto é o que já declara inferência controlada com justificativa.
Os demais não podem ser considerados comprovados enquanto suas fontes
permanecerem sem captura verificável.

## Bloqueios de proveniência

As fontes foram classificadas inicialmente como `unverified`. Um ID textual ou
um identificador do Google Drive não comprova, isoladamente, o conteúdo, a
versão, o emissor ou a preservação do artefato.

Há referências não processáveis como intervalos de IDs, “documentos oficiais”,
“decisões de Davi” e “metadados de”. Elas precisam ser substituídas no pacote
de proveniência por relações explícitas, sem editar silenciosamente o documento
protegido por G1.

## Divergência de integridade observada

A execução também detectou que
`DOC-VAL-REL-CONTEXTO-V01` diverge do hash registrado depois da ingestão. A
diferença observada está em um link de sumário Markdown, mas continua sendo uma
alteração física pós-G1. O manifesto não foi atualizado para absorvê-la.

## Próximas ações

1. Capturar e preservar as fontes acessíveis.
2. Registrar hash, referência imutável, autoridade, data e responsável.
3. Resolver fontes genéricas ou não localizadas.
4. Normalizar as quatro referências ambíguas no pacote processável.
5. Reexecutar G2 até atingir 100% de cobertura crítica.
6. Tratar separadamente a divergência pós-G1.

G2 aprovado não promove o documento isoladamente. `G3 — Semântica e escopo`
também deverá passar antes de `CONSOLIDACAO_REGISTRADA`.
