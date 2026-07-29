---
document_id: DOC-REG-ENTRADA-DOCUMENTACAO
title: "Documentação do CEPRAEA BEACH PRO"
document_type: inventario
version: "0.2.2"
workflow_status: RASCUNHO
permitted_uses:
  - entrada_documental
  - localizacao
prohibited_uses:
  - substituicao_do_registro
  - canonizacao
---

# Documentação do CEPRAEA BEACH PRO

## Estado atual

A implementação rigorosa foi congelada e substituída pelo perfil documental
`LEAN` em 25 de julho de 2026.

```yaml
canonical_documents:
  - DOC-CEPRAEA-CANDIDATA-CONTEXTO
  - DOC-CEPRAEA-DEC-019-MVP-SINTETICO
active_profile: LEAN
g_arch: pass
g0_identity: pass
g1_integrity: pass
g2_provenance: support_pass
g3_to_g8: deferred
g_canon_separate: deferred
legacy_ingestion: completed
legacy_documents_in_rascunho: 10
migration_status: completed
workflow_implementation: lean_active
documento_base_status: CANONICA_VIGENTE
working_document: DOC-CEPRAEA-CONTEXTO-TRABALHO-V02
working_version: "0.2"
approved_decisions: [DEC-019]
d0: "2026-07-26T00:24:32-03:00"
implementation_authorization: SINTETICA_M0_M4
implementation_start: [M0, M1]
implementation_status: AUTORIZADA_NAO_INICIADA
```

O perfil LEAN exige somente `G-ARCH`, `G0`, `G1` e aprovação explícita de Davi
para o documento, versão e hash. G2 está implementado e disponível como suporte;
G3 a G8 e um G-CANON separado estão adiados. Não serão criados novos contratos
ou matrizes nesta fase.

`DOC-CEPRAEA-CANDIDATA-CONTEXTO`, versão `0.1`, é o único documento-base no
estado `CANONICA_VIGENTE`. Sua aprovação é exclusivamente documental e não
autoriza implementação, dados reais, piloto ou produção.

`DOC-CEPRAEA-CONTEXTO-TRABALHO-V02`, versão `0.2`, é a cópia de trabalho não
vigente usada para acumular correções encontradas durante a revisão dos
requisitos. Agentes de IA somente devem usá-la quando a tarefa tratar
explicitamente da revisão da futura versão `0.2`.

`DOC-CEPRAEA-DEC-019-MVP-SINTETICO`, versão `0.1.1`, é a decisão vigente que
aprova o recorte do MVP e autoriza exclusivamente a implementação sintética de
M0 a M4, começando por M0/M1. D0 é `2026-07-26T00:24:32-03:00`. A autorização
não abrange dados reais, migração real, V2, piloto, produção ou M5/M6
operacionais.

## Fontes de controle

Consulte nesta ordem:

1. [registro mestre](registry/registro-documentos.yaml) para identidade,
   caminhos, hashes e estado operacional;
2. [política de arquitetura](governance/policies/politica-arquitetura-documental.md)
   para diretórios, nomes físicos e migração;
3. [workflow documental LEAN](governance/workflows/workflow-documentacao.md) e sua
   [definição processável](registry/workflow-documentacao.yaml) para estados,
   transições, contratos e gates;
4. [schemas contratuais](contracts/schemas/) apenas quando uma verificação
   estrutural ou investigação exigir;
5. [plano rigoroso congelado](governance/workflows/workflow-operacionalizacao-documental.md)
   como referência histórica e opção futura;
6. [relatório inicial de auditoria](validation/reports/relatorio-auditoria-acervo.md)
   para a condição encontrada no acervo legado;
7. [relatório de ingestão](validation/reports/relatorio-ingestao-legado.md)
   para os resultados de G0, G1 e a inicialização formal dos dez legados.

## Uso transitório do acervo legado

- A versão candidata pode ser usada como contexto promovido pelo processo
  legado, respeitando suas proibições expressas.
- A base controlada e as fontes especializadas preservam rastreabilidade e
  contexto histórico.
- Os requisitos funcionais são derivados e não constituem especificação
  aprovada.
- O inventário é uma síntese e não substitui as fontes.
- O fluxo narrativo explica a formação do acervo, mas ainda não é a máquina de
  estados executável.

## Regras para agentes de IA

- quando existir um documento em `canonical_documents`, usá-lo primeiro nos
  assuntos cobertos por seu escopo;
- verificar o registro mestre antes de selecionar uma fonte;
- não preencher `workflow_status` a partir de texto legado;
- não declarar um documento canônico enquanto a lista
  `canonical_documents` estiver vazia;
- não mover ou renomear arquivos sem migração controlada;
- não interpretar a presença em um diretório como autoridade suficiente;
- não converter requisitos derivados em autorização de implementação;
- sinalizar divergências de hash, caminho, vigência ou precedência;
- preservar a autoridade humana de Davi Sermenho.
- não percorrer contratos, gates e evidências históricas sem necessidade
  material;
- não interpretar o perfil LEAN como autorização de implementação, dados
  reais, piloto ou produção; autorização de implementação exige decisão
  canônica específica;
- aplicar a DEC-019 somente ao perfil sintético e aos marcos M0 a M4;
- tratar `coringa` como papel tático do jogo, nunca como posição ou
  classificação cadastral;
- usar somente `goleira`, `defesa`, `ataque`, `especialista` e `indefinida`
  como classificações amplas cobertas pelo MVP.

## Validação

Execute a partir da raiz do workspace:

```bash
python3 -m scripts.documentation.validate_documentation
```

O modo abaixo transforma desvios legados de nome e diretório em falhas:

```bash
python3 -m scripts.documentation.validate_documentation --strict-legacy
```

Após a migração controlada, o modo estrito também deve concluir sem falhas.

Os gates bloqueantes possuem saída YAML processável:

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G-ARCH \
  --format yaml

python3 -m scripts.documentation.validate_documentation \
  --gate G0 \
  --format yaml

python3 -m scripts.documentation.validate_documentation \
  --gate G1 \
  --format yaml
```

Código `1` com `status: fail` impede a transição documental. Para a ingestão
legada, `G-ARCH`, `G0` e `G1` devem passar conjuntamente antes do evento
`INGESTAO_REGISTRADA`.
