---
document_id: DOC-CEPRAEA-DIRETRIZ-CONTEXTO
title: "Conteúdo para documentação técnica da PWA"
document_type: politica
version: "0.1.1-ingestao"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - orientacao_de_consolidacao
prohibited_uses:
  - especificacao_tecnica
  - autorizacao_de_implementacao
---

# CONTEÚDO PARA DOCUMENTAÇÃO TÉCNICA DA PWA

O `DECISAO-CEPRAEA.md`não deve ser tratado como especificação da planilha nem como documentação técnica final da PWA. Ele deve ser o documento canônico de descoberta e contexto que permitirá à IA produzir, posteriormente, a documentação necessária para desenvolver a PWA do CEPRAEA.

## ÍNDICE

- [CONTEÚDO PARA DOCUMENTAÇÃO TÉCNICA DA PWA](#conteúdo-para-documentação-técnica-da-pwa)
  - [ÍNDICE](#índice)
  - [Finalidade correta do documento](#finalidade-correta-do-documento)
  - [Correção da interpretação anterior](#correção-da-interpretação-anterior)
  - [O que a IA precisa aprender com o documento](#o-que-a-ia-precisa-aprender-com-o-documento)
  - [Estrutura adequada ao novo objetivo](#estrutura-adequada-ao-novo-objetivo)
    - [1. Identidade do contexto](#1-identidade-do-contexto)
    - [2. Realidade esportiva](#2-realidade-esportiva)
    - [3. Atores e autoridades](#3-atores-e-autoridades)
    - [4. Funcionamento atual com planilhas — estado `AS-IS`](#4-funcionamento-atual-com-planilhas--estado-as-is)
    - [5. Problemas atuais](#5-problemas-atuais)
    - [6. Capacidades atuais que devem ser preservadas](#6-capacidades-atuais-que-devem-ser-preservadas)
    - [7. Necessidades do produto futuro — estado `TO-BE`](#7-necessidades-do-produto-futuro--estado-to-be)
    - [8. Escopo e limites](#8-escopo-e-limites)
    - [9. Domínio](#9-domínio)
    - [10. Restrições e condições](#10-restrições-e-condições)
    - [11. Pendências e desconhecidos](#11-pendências-e-desconhecidos)
  - [Regra fundamental para os objetivos atuais](#regra-fundamental-para-os-objetivos-atuais)
  - [Documentação que poderá ser derivada](#documentação-que-poderá-ser-derivada)

## Finalidade correta do documento

> O `DECISAO-CEPRAEA.md`deve descrever a realidade do CEPRAEA, seu funcionamento operacional atual por meio de planilhas, seus atores, dados, processos, problemas, regras, conceitos, restrições e necessidades. Esse conteúdo será a fonte contextual utilizada pela inteligência artificial para criar a documentação funcional e técnica da PWA do CEPRAEA.

Isso estabelece quatro objetos diferentes:

| Objeto           | Significado                                                                  |
| ---------------- | ---------------------------------------------------------------------------- |
| CEPRAEA          | Equipe esportiva real.                                                       |
| Planilhas atuais | Sistema operacional existente, que representa e apoia parcialmente a equipe. |
| `DECISAO-CEPRAEA.md`  | Fonte canônica de contexto, descoberta e diagnóstico.                        |
| PWA do CEPRAEA   | Produto futuro que será especificado e desenvolvido a partir desse contexto. |

## Correção da interpretação anterior

A lacuna de “identidade do produto” precisa ser reformulada. O documento deve identificar separadamente:

1. --Entidade descrita:-- CEPRAEA.
2. --Sistema atual:-- ecossistema de planilhas.
3. --Produto pretendido:-- PWA do CEPRAEA.
4. --Finalidade do documento:-- fornecer contexto validado para a IA produzir a documentação da PWA.

O texto atual mistura esses quatro níveis. Em alguns trechos, “CEPRAEA”, “planilha”, “sistema”, “banco” e “produto” aparecem como se representassem o mesmo objeto.

## O que a IA precisa aprender com o documento

Ao terminar a leitura, a IA deve conseguir responder sem inferência:

- o que é o CEPRAEA;
- quem compõe a equipe;
- quem possui autoridade sobre cada informação;
- como o CEPRAEA funciona atualmente;
- quais processos são executados;
- quais planilhas e fontes participam desses processos;
- quais dados são registrados;
- quais problemas existem no funcionamento atual;
- quais problemas são provocados pelas planilhas;
- quais capacidades atuais precisam ser preservadas;
- quais limitações devem ser eliminadas;
- quais decisões permanecem humanas;
- quais conceitos possuem significado específico;
- quais informações são confirmadas, temporárias, contraditórias ou desconhecidas;
- quais necessidades poderão originar requisitos da PWA;
- quais decisões ainda precisam ser tomadas antes de definir requisitos.

## Estrutura adequada ao novo objetivo

### 1. Identidade do contexto

- CEPRAEA;
- modalidade e categoria;
- treinador responsável;
- composição humana;
- temporada ou período de validade;
- finalidade do `DECISAO-CEPRAEA.md`;
- produto futuro ao qual o contexto se destina.

### 2. Realidade esportiva

- treinos;
- competições;
- elenco;
- disponibilidade;
- convocações;
- escalações;
- participação;
- resultados;
- planejamento técnico;
- comunicação com as atletas.

### 3. Atores e autoridades

Deve deixar explícito que:

- Davi é treinador, operador, administrador e mantenedor atual;
- as atletas são integrantes e autoridades sobre a própria disponibilidade;
- documentos oficiais possuem autoridade sobre calendário e resultados oficiais;
- a IA não possui autoridade esportiva;
- não existe comissão técnica, coordenação ou equipe administrativa adicional.

### 4. Funcionamento atual com planilhas — estado `AS-IS`

- arquivos canônicos;
- função de cada arquivo;
- abas e módulos relevantes;
- entradas;
- transformações;
- saídas;
- integrações;
- atualizações manuais;
- fórmulas e automações;
- dados compartilhados;
- dados restritos;
- dependências externas.

### 5. Problemas atuais

Cada problema deve possuir:

- ID;
- descrição;
- causa;
- pessoas afetadas;
- consequência;
- frequência;
- gravidade;
- evidência;
- fonte;
- data da verificação;
- estado de validação.

Exemplo de distinção necessária:

- --Problema estrutural:-- informações podem ficar divergentes entre interface e banco.
- --Evidência datada:-- determinada atleta aparece em uma planilha e não aparece na outra em uma data específica.

### 6. Capacidades atuais que devem ser preservadas

As funcionalidades das planilhas não devem ser automaticamente convertidas em requisitos da PWA. Primeiro, devem ser classificadas como capacidades atuais, por exemplo:

- controlar elenco;
- registrar disponibilidade;
- avaliar composição funcional;
- controlar calendário;
- apoiar convocação;
- registrar participação;
- preservar resultados;
- apoiar planejamento;
- comunicar informações;
- manter rastreabilidade.

Depois, cada capacidade deverá ser avaliada para decidir se será:

- preservada;
- corrigida;
- substituída;
- ampliada;
- excluída;
- mantida como responsabilidade humana.

### 7. Necessidades do produto futuro — estado `TO-BE`

Aqui devem aparecer resultados necessários, sem antecipar arquitetura técnica:

- eliminar divergência entre representações;
- manter um estado operacional confiável;
- reduzir reconciliação manual;
- preservar autoridade das fontes;
- separar conteúdos internos e conteúdos das atletas;
- garantir rastreabilidade;
- reduzir a sobrecarga de Davi;
- impedir inferências indevidas da IA;
- manter histórico verificável.

Essas necessidades poderão originar requisitos da PWA, mas não devem ser chamadas de requisitos aprovados antes da validação.

### 8. Escopo e limites

É necessário separar:

- escopo operacional do CEPRAEA;
- escopo do sistema atual;
- capacidades candidatas à PWA;
- funcionalidades definitivamente incluídas;
- funcionalidades definitivamente excluídas;
- ambientes suportados;
- ambientes não suportados;
- integrações previstas;
- decisões humanas que não poderão ser automatizadas.

### 9. Domínio

O glossário existente deve ser mantido, mas dividido em:

- conceitos esportivos;
- entidades;
- papéis;
- eventos;
- estados;
- regras;
- exceções;
- relações;
- conceitos técnicos das planilhas.

`Atleta`, `treino`, `convocação` e `participação` pertencem ao domínio esportivo. `DB_ATLETAS`, célula, aba e fórmula pertencem à implementação atual.

### 10. Restrições e condições

- privacidade;
- conectividade;
- Google Drive e Google Sheets;
- operação concentrada em Davi;
- capacidade de manutenção;
- dispositivos utilizados;
- legislação aplicável;
- orçamento;
- prazo;
- dependências de terceiros;
- indisponibilidade de fontes externas.

### 11. Pendências e desconhecidos

Informações não comprovadas devem utilizar estados explícitos:

- `CONFIRMADO`;
- `PENDENTE_DE_VALIDACAO`;
- `CONTRADITORIO`;
- `DESCONHECIDO`;
- `NAO_SE_APLICA`;
- `FORA_DE_ESCOPO`.

Isso evita que a IA complete lacunas com suposições.

## Regra fundamental para os objetivos atuais

> Os 12 objetivos existentes no documento são, predominantemente, objetivos das planilhas ou da operação atual. Eles não devem ser convertidos diretamente em requisitos da PWA.

O fluxo correto é:

| Conteúdo atual               | Transformação documental               |
| ---------------------------- | -------------------------------------- |
| Objetivo da planilha         | Capacidade operacional existente       |
| Problema da planilha         | Necessidade de mudança                 |
| Resultado esperado           | Resultado de negócio desejado          |
| Critério de aceitação atual  | Evidência para avaliar a necessidade   |
| Solução sugerida             | Hipótese, não requisito aprovado       |
| Decisão validada sobre a PWA | Requisito candidato                    |
| Requisito aprovado           | Entrada para projeto e desenvolvimento |

## Documentação que poderá ser derivada

Com o `DECISAO-CEPRAEA.md`organizado corretamente, a IA poderá produzir:

- contexto do produto;
- visão da PWA;
- mapa de atores e permissões;
- descrição do funcionamento atual;
- modelo operacional futuro;
- escopo e fora de escopo;
- modelo de domínio;
- glossário canônico;
- regras de negócio;
- catálogo de fontes e dados;
- requisitos funcionais;
- requisitos não funcionais;
- requisitos de privacidade e segurança;
- critérios de aceitação;
- arquitetura da informação;
- fluxos de usuário;
- backlog inicial;
- documentação técnica de desenvolvimento.

Conclusão:

> o `DECISAO-CEPRAEA.md`deve funcionar como a base factual e semântica da documentação da PWA. Seu conteúdo atual é rico, mas mistura realidade esportiva, funcionamento das planilhas, auditoria, problemas, soluções e estados momentâneos. O refinamento principal consiste em separar claramente `CEPRAEA`, `sistema atual`, `diagnóstico` e `produto futuro`, preservando a proveniência e impedindo que a IA transforme observações ou hipóteses em requisitos aprovados.
