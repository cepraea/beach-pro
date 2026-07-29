---
document_id: DOC-GOV-WF-DOCUMENTACAO
title: "Workflow documental LEAN do CEPRAEA BEACH PRO"
document_type: workflow
version: "0.2.0"
workflow_status: RASCUNHO
permitted_uses:
  - execucao_controlada
  - orientacao
prohibited_uses:
  - autocanonizacao
---

# Workflow documental LEAN do CEPRAEA BEACH PRO

## 1. Decisão operacional

| Campo | Valor |
| --- | --- |
| ID | `DOC-GOV-WF-DOCUMENTACAO` |
| Workflow | `WF-DOC-CEPRAEA` |
| Versão | `0.2.0` |
| Perfil ativo | `LEAN` |
| Definição processável | `docs/registry/workflow-documentacao.yaml` |
| Autoridade aprovadora | Davi Sermenho |

O perfil rigoroso anterior foi congelado em 25 de julho de 2026. Seus contratos,
gates e evidências permanecem disponíveis como suporte, mas não são requisitos
do caminho ativo. Não serão implementados `G3` a `G8` nem um `G-CANON`
separado nesta fase. Também não serão criados novos contratos ou matrizes.

## 2. Objetivo

Manter um único documento-base oficial e vigente para o contexto documental do
CEPRAEA BEACH PRO, com o mínimo de controle necessário para evitar ambiguidade,
perda de integridade e promoção sem aprovação humana.

Esse estado documental não autoriza implementação, dados reais, piloto ou
produção.

## 3. Máquina de estados

```text
RASCUNHO
→ EM_REVISAO
→ CANONICA_VIGENTE
→ SUPERADA
```

Uma revisão devolvida retorna a `RASCUNHO`. Uma versão vigente também pode ser
`REVOGADA` por Davi.

## 4. Verificações obrigatórias

Somente três verificações bloqueiam a aprovação:

1. `G-ARCH`: caminho, nome e registro são consistentes;
2. `G0`: documento, versão, responsável, finalidade e escopo estão identificados;
3. `G1`: o hash registrado corresponde exatamente ao arquivo revisado.

`G2` permanece implementado e pode ser consultado quando a proveniência
detalhada for útil. Ele não é requisito do perfil LEAN. Os demais gates do
perfil rigoroso estão adiados e não são executados.

## 5. Aprovação LEAN

Davi promove uma versão de `EM_REVISAO` para `CANONICA_VIGENTE` mediante uma
declaração que identifique:

- `document_id`;
- versão;
- hash;
- finalidade;
- escopo;
- usos proibidos;
- decisão inequívoca;
- data.

Não existe promoção automática. A solicitação para executar tarefas não deve
ser interpretada como aprovação do conteúdo quando documento, versão e hash não
forem explicitamente confirmados.

## 6. Documento-base

O documento-base vigente é:

```text
DOC-CEPRAEA-CANDIDATA-CONTEXTO
docs/canonical/context/contexto-cepraea-beach-pro.md
versão 0.1
```

Ele foi aprovado explicitamente por Davi Sermenho para o hash
`71bd2695280f0cdd5c41b83c7e433d5a84a803b527a7e09d7dfd7eecaaeab847`
e publicado sem alteração de bytes. A aprovação não autoriza implementação,
dados reais, piloto ou produção.

## 7. Controles existentes como suporte

O registro mestre, os schemas, o pacote de integridade, o pacote de
proveniência e os resultados históricos de gates continuam preservados. Seu uso
é excepcional:

- investigar divergência;
- recuperar uma versão;
- esclarecer a origem de informação material;
- apoiar uma revisão futura.

O agente de IA não deve percorrê-los rotineiramente quando houver um
documento-base vigente que cubra o assunto.

## 8. Done LEAN

```text
Documento-base escolhido
+ G-ARCH, G0 e G1 pass
+ versão e hash congelados
+ aprovação explícita de Davi
+ cópia publicada com o mesmo hash
+ registro aponta CANONICA_VIGENTE
+ somente um documento-base vigente no escopo
= DONE_LEAN
```

## 9. Congelamento da infraestrutura

Depois da consolidação deste perfil:

- não expandir a máquina sem nova decisão explícita;
- não criar contratos, matrizes ou gates adicionais;
- não implementar os gates adiados;
- alterar a infraestrutura apenas para corrigir defeito que impeça o fluxo
  LEAN;
- concentrar o esforço seguinte em requisitos essenciais, arquitetura e
  desenvolvimento da PWA.
