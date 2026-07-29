---
document_id: DOC-CEPRAEA-PROPOSTA-MVP-SINTETICO
title: "Proposta de recorte do MVP sintético do CEPRAEA BEACH PRO"
document_type: decisao
version: "0.1.3"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - revisao
  - preparacao_da_dec_019
prohibited_uses:
  - autorizacao_por_inferencia
  - dados_reais
  - piloto
  - producao
---

# Proposta de recorte do MVP sintético — CEPRAEA BEACH PRO

## 1. Identificação

| Campo | Valor |
| --- | --- |
| ID | `DOC-CEPRAEA-PROPOSTA-MVP-SINTETICO` |
| Versão | `0.1.3` |
| Estado | `RASCUNHO` |
| Data | 2026-07-25 |
| Revisão | Regularização da correção de domínio registrada após a versão 0.1.2 |
| Autoridade para aprovação | Davi Sermenho |
| Origem | `DOC-VAL-REL-AUDITORIA-REQUISITOS-MVP` |
| Contexto vigente | `DOC-CEPRAEA-CANDIDATA-CONTEXTO`, versão 0.1 |
| Catálogo de origem | `DOC-CEPRAEA-REQ-DERIVADOS-V01`, RF-001 a RF-053 |

## 2. Decisão proposta em uma frase

Construir primeiro, exclusivamente com dados sintéticos, um fluxo vertical de
treino que permita a Davi manter o elenco, criar um compromisso e uma
solicitação de disponibilidade, receber respostas, acompanhar pendências e
cobertura ampla, publicar a lista prevista de confirmadas e registrar a presença
real posteriormente, com identidade individual, isolamento, histórico e
auditoria.

O recorte comprova o núcleo semântico e operacional da PWA antes de implementar
convocações de competição, migração de dados reais, atendimento jurídico de
titulares ou snapshot offline.

## 3. O que este MVP é

Este documento propõe um `MVP_SINTETICO`, destinado à validação V1. Ele é:

- uma primeira entrega implementável e testável;
- um fluxo vertical completo, não uma coleção de telas desconectadas;
- executado em ambiente separado, somente com pessoas e dados fictícios;
- suficiente para testar o modelo de domínio, a visibilidade e a rastreabilidade;
- anterior a dados reais, piloto, homologação operacional e produção.

O termo MVP neste documento não significa produto liberado ao CEPRAEA real.

## 4. Fluxo vertical incluído

```text
Davi mantém o elenco sintético
        ↓
Davi cria um treino com prazo e vigência
        ↓
Davi solicita disponibilidade
        ↓
Atletas sintéticas respondem sim, não, incerta ou deixam sem resposta
        ↓
Davi acompanha respostas e pendências
        ↓
Sistema apresenta cobertura por função ampla
        ↓
Davi publica ou não publica a lista prevista de confirmadas
        ↓
Após o treino, Davi registra presença real separadamente
        ↓
Histórico permite reconstruir solicitação, resposta, lista e fato posterior
```

Esse é o menor fluxo que valida conjuntamente os problemas centrais do legado:
divergência de elenco, mistura de disponibilidade com presença, fragmentação de
comunicação, informação vencida e ausência de rastreabilidade.

## 5. Unidades implementáveis do MVP

Os 44 identificadores incluídos são organizados em dez unidades. Identificadores
consolidados permanecem como critérios e não geram trabalho duplicado.

### MVP-01 — Fundação, identidade e acesso

- Contas sintéticas individuais para Davi e atletas.
- Somente os contextos Davi e atleta.
- Cadastro público desabilitado.
- Convite, recuperação, MFA privilegiada, suspensão e revogação testáveis.
- RLS e testes negativos de isolamento.
- Nenhuma impersonação, acesso anônimo ou credencial administrativa no cliente.
- RFs: RF-026, RF-036 a RF-045 e RF-048.

### MVP-02 — Ciclo de vida do elenco

- Uma identidade única por atleta.
- Inclusão, inativação, encerramento de vínculo e retorno sem duplicidade.
- Histórico preservado durante todas as transições.
- O motivo pessoal da saída ou retorno não integra o cadastro operacional.
- RFs: RF-003 e RF-043; RF-004 e RF-045 como controles.

### MVP-03 — Compromissos de treino

- Criação de treino com data, prazo, vigência, responsável e próxima ação.
- Eventos passados não aparecem como vigentes.
- Pendências obrigatórias possuem estado.
- RFs: RF-027 a RF-029.

### MVP-04 — Solicitações e respostas

- Solicitação de disponibilidade vinculada ao treino.
- Estados `sim`, `não`, `incerta` e `não respondida`.
- Justificativa opcional e minimizada.
- Alteração dentro do prazo com versão anterior preservada.
- Correção administrativa separada da declaração da atleta.
- RFs: RF-005 a RF-011.

### MVP-05 — Declaração, lista prevista e presença real

- Disponibilidade e presença são entidades distintas.
- Respostas são vinculadas ao mesmo compromisso sem virar fato posterior.
- Lista de confirmadas é uma previsão, não comprovação de presença.
- Davi pode publicar, substituir, encerrar ou não publicar a lista.
- Presença real é registrada somente depois do treino.
- RFs: RF-012 a RF-014 e RF-018 a RF-021.

### MVP-06 — Caixa individual da atleta

- Solicitações pendentes, prazo, resposta vigente, justificativa opcional,
  fechamento e histórico próprio.
- Registro separado de disponibilização, visualização e ciência explícita
  quando exigida.
- RFs: RF-022 a RF-024.

### MVP-07 — Estado operacional de Davi

- Visão única de elenco, próximos treinos, respostas, pendências, lista vigente
  e fatos ainda não registrados.
- Nenhuma pergunta do fluxo vertical exige reconciliar planilhas, mensagens ou
  outras representações internas.
- RFs: RF-001, RF-002 e RF-025.

### MVP-08 — Cobertura por função ampla

- Contagem descritiva baseada exclusivamente nas respostas vigentes.
- Funções iniciais: goleira, defesa, ataque, especialista e indefinida.
- Coringa é papel tático do jogo e não integra a classificação de posição ou
  função do cadastro.
- Nenhuma recomendação automática de convocação, escalação, disciplina,
  confiabilidade ou condição pessoal.
- RFs: RF-030 a RF-032.

### MVP-09 — Histórico e auditoria

- Reconstrução de solicitação, resposta, alterações, lista, fechamento e
  presença.
- Autoria, data, vigência e proveniência dos registros críticos.
- Eventos mínimos de segurança auditáveis.
- RFs: RF-033, RF-034 e RF-036.

### MVP-10 — Privacidade aplicada ao fluxo

- Cada atleta vê somente seus dados e as listas mínimas autorizadas.
- Justificativas ficam restritas à atleta e a Davi.
- Nenhuma inferência pessoal automática.
- Nenhum dado é enviado a ferramenta de IA externa.
- RFs: RF-004, RF-007 e RF-045 a RF-048.

## 6. Mapeamento integral dos RFs

### 6.1 Incluídos no MVP sintético

```text
RF-001 a RF-014
RF-018 a RF-034
RF-036 a RF-048
```

Total: 44 identificadores preservados em dez unidades implementáveis.

Entre eles, RF-002, RF-004, RF-009, RF-014, RF-019, RF-028, RF-032, RF-034,
RF-044 e RF-047 funcionam como critérios consolidados, não como entregas
independentes.

### 6.2 Adiados para incremento posterior

| RF | Tratamento | Motivo |
| --- | --- | --- |
| RF-015 | Adiar | Convocação de competição não é necessária para validar o ciclo de treino |
| RF-016 | Adiar | Confirmação de convocação depende do fluxo de competição |
| RF-017 | Adiar | Lista vigente de convocação depende do fluxo de competição |
| RF-035 | Adiar | Importação será necessária antes de dados reais, não para V1 sintética |
| RF-049 | Adiar | Área de direitos deve estar pronta antes de piloto/dados reais, não para o núcleo sintético |
| RF-051 | Adiar | Snapshot offline aumenta custo e risco sem validar o núcleo do produto |
| RF-052 | Adiar com RF-051 | Regra obrigatória quando o snapshot offline for implementado |
| RF-053 | Adiar com RF-051 | Segurança obrigatória do snapshot; não existe versão pessoal simplificada |

Adiar não remove esses requisitos da primeira fase documental. Significa apenas
que eles não integram o primeiro recorte implementável.

### 6.3 Gate preservado fora do backlog funcional

`RF-050` passa a ser tratado como `GATE_DADOS_REAIS_PRIVACIDADE`. Todos os seus
controles permanecem obrigatórios antes de dados reais, piloto ou produção, mas
não geram uma funcionalidade isolada no MVP sintético.

### 6.4 Fases posteriores já existentes

`RF-P01` a `RF-P04` permanecem fora do MVP e conservam seu estado de fase
posterior. Scout, vídeo, finanças e publicação pública continuam fora do
produto ou da primeira fase conforme as decisões vigentes.

## 7. Resolução proposta dos três pontos decisórios

Estas respostas são propostas para aprovação conjunta, não decisões já tomadas.

### PD-001 — Cobertura tática

**Proposta:** incluir no MVP somente cobertura quantitativa por função ampla:
goleira, defesa, ataque, especialista e indefinida.

Posições específicas, combinações e sistemas táticos ficam adiados até que Davi
valide um vocabulário mais detalhado. A PWA não produz convocação ou escalação.
Coringa pode ser tratado futuramente como papel tático contextual, mas não como
posição nem como nome alternativo para especialista.

### PD-002 — Vínculo esportivo e conta

**Proposta:** utilizar três estados persistentes e uma transição:

| Estado/transição | Participa do elenco ativo | Acesso operacional | Histórico |
| --- | --- | --- | --- |
| `ATIVA` | Sim | Ativo | Preservado |
| `INATIVA_TEMPORARIA` | Não | Suspenso | Preservado |
| `VINCULO_ENCERRADO` | Não | Desativado | Preservado |
| `RETORNAR_AO_ELENCO` | Transição para `ATIVA` | Reativado por Davi | Mesma identidade |

O retorno nunca cria uma nova atleta. A decisão de Davi altera o vínculo e a
conta correspondente de forma auditável. Motivo médico, reprodutivo, familiar
ou pessoal não é necessário para executar a transição.

### PD-003 — Offline

**Proposta:** o MVP será uma PWA instalável que exige conexão para acessar dados.
Não haverá snapshot local de dados no primeiro recorte.

RF-051 a RF-053 permanecem adiados em conjunto. Quando implementados, aviso de
desatualização, criptografia, vínculo ao dispositivo e eliminação no encerramento
da sessão serão indivisíveis.

## 8. Dados e ambiente permitidos

Durante todo o MVP:

- usar somente dados sintéticos;
- utilizar nomes e contatos fictícios;
- não copiar a planilha real;
- não cadastrar Gilvania ou qualquer outra atleta real;
- representar o cenário de retorno com uma atleta sintética;
- não importar conversas, justificativas ou dados pessoais;
- não enviar dados operacionais a APIs de IA;
- não usar o ambiente como piloto informal;
- exibir marcação visível de ambiente sintético/não produtivo.

## 9. Sequência de implementação

A sequência respeita os marcos existentes e não cria um workflow novo.

### M0 — Preparação

- transformar as dez unidades em backlog técnico;
- escrever critérios de aceitação e testes;
- preparar ambientes e dados sintéticos;
- configurar repositório, qualidade e segredos;
- registrar D0 após aprovação da `DEC-019`.

### M1 — Fundação e identidade

- implementar MVP-01;
- criar o esqueleto de auditoria de MVP-09;
- comprovar RLS com Davi sintético e pelo menos duas atletas sintéticas;
- impedir cadastro público, acesso cruzado e privilégios no cliente.

### M2 — Elenco, compromissos e respostas

- implementar MVP-02, MVP-03 e MVP-04;
- validar retorno sem duplicidade;
- preservar resposta original e correção administrativa.

### M3 — Listas e fatos

- implementar MVP-05 e MVP-08;
- comprovar que lista prevista não vira presença;
- registrar presença somente como fato posterior.

### M4 — Comunicação, privacidade e auditoria

- implementar MVP-06, MVP-07, MVP-09 e MVP-10;
- completar caixa individual, painel, histórico e testes negativos.

### Fechamento V1 sintético

- executar o Done do MVP;
- registrar falhas e correções;
- não iniciar V2, dados reais ou piloto sem nova autorização específica.

M5 e M6 operacionais continuam fora desta autorização inicial porque backup de
dados reais, restauração operacional, piloto e corte dependem de portões
posteriores.

## 10. Done do MVP sintético

O MVP está concluído somente quando:

1. existem personas sintéticas de Davi e pelo menos cinco atletas;
2. Davi cria um treino e uma solicitação de disponibilidade;
3. atletas respondem nos quatro estados previstos, com e sem justificativa;
4. uma resposta é alterada e a versão anterior permanece recuperável;
5. uma correção administrativa não altera a autoria da atleta;
6. Davi visualiza respondidas, não respondidas, vencidas e próximas ações;
7. a cobertura usa somente funções amplas e fatos vigentes;
8. uma lista prevista é publicada, substituída, encerrada ou deixada como não
   publicada sem expor justificativas;
9. presença real é registrada depois do treino e não é inferida da
   disponibilidade;
10. o histórico reconstrói o fluxo completo por autoria, data e vigência;
11. uma atleta não acessa dados privados de outra em testes negativos;
12. retorno de atleta sintética reutiliza a mesma identidade e histórico;
13. a PWA é instalável e funciona online nos navegadores aprovados;
14. não existe snapshot offline de dados, sincronização contínua com planilhas
    ou dependência de WhatsApp/e-mail para o fluxo testado;
15. testes automatizados do domínio, RLS e fluxo vertical estão passando;
16. não existe falha crítica aberta;
17. todo o conjunto de dados permanece comprovadamente sintético;
18. nenhuma evidência é apresentada como autorização para dados reais, piloto
    ou produção.

## 11. Autorização proposta

A futura `DEC-019` pode, em um único ato:

1. aprovar este recorte;
2. aprovar as respostas propostas a `PD-001`, `PD-002` e `PD-003`;
3. autorizar a implementação integral do MVP exclusivamente sintético;
4. determinar que a execução comece por M0/M1;
5. permitir avanço de M2 a M4 sem nova decisão de produto, desde que não haja
   expansão de escopo ou uso de dados reais;
6. definir D0 como a data e hora da aprovação expressa da própria `DEC-019`,
   no fuso `America/Sao_Paulo`;
7. manter V2, dados reais, piloto, produção, migração real e M5/M6 operacionais
   bloqueados por decisões e gates próprios.

## 12. O que ainda exige resposta de Davi

Para aprovar a proposta, Davi precisa responder somente:

1. aprova cobertura apenas por função ampla no MVP?
2. aprova os estados `ATIVA`, `INATIVA_TEMPORARIA` e `VINCULO_ENCERRADO`, com
   retorno como transição para a mesma identidade?
3. aprova adiar integralmente RF-051 a RF-053 e operar o MVP somente online?
4. aprova o recorte integral e a autorização sintética descritos neste
   documento?

As quatro respostas podem ser dadas conjuntamente na `DEC-019`. Nenhuma outra
escolha técnica reversível precisa ser submetida a Davi antes de M0/M1.

## 13. Estado desta proposta

Esta proposta permanece `RASCUNHO`. Sua criação:

- não aprova o MVP;
- não constitui a `DEC-019`;
- não define D0;
- não autoriza código;
- não autoriza dados reais;
- não autoriza piloto ou produção.
