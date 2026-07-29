---
document_id: DOC-GOV-PROT-QUALIDADE
title: "Protocolo de qualidade para documentação de contexto"
document_type: protocolo
version: "0.1.1-ingestao"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - validacao_documental
prohibited_uses:
  - aprovacao_automatica
---

# Protocolo de qualidade para documentação de contexto de produto gerada por IA

Este protocolo converte os princípios de qualidade aplicáveis à documentação de
contexto de produto em critérios operacionais de aceitação e métodos de
validação. Seu objetivo é permitir que cada afirmação relevante seja avaliada
com base em evidências, que cada seção receba um dos estados de avaliação
definidos neste protocolo e que o documento completo seja submetido às
validações transversais e à regra final de aprovação.

- [Protocolo de qualidade para documentação de contexto de produto gerada por IA](#protocolo-de-qualidade-para-documentação-de-contexto-de-produto-gerada-por-ia)
  - [Finalidade](#finalidade)
  - [1. Fatores críticos de sucesso](#1-fatores-críticos-de-sucesso)
    - [1.1 Correção factual](#11-correção-factual)
    - [1.2 Completude semântica](#12-completude-semântica)
    - [1.3 Precisão terminológica](#13-precisão-terminológica)
    - [1.4 Ausência de ambiguidade](#14-ausência-de-ambiguidade)
    - [1.5 Rastreabilidade](#15-rastreabilidade)
    - [1.6 Separação entre fato, inferência e decisão](#16-separação-entre-fato-inferência-e-decisão)
    - [1.7 Verificabilidade](#17-verificabilidade)
    - [1.8 Consistência interna](#18-consistência-interna)
    - [1.9 Consistência externa](#19-consistência-externa)
    - [1.10 Acionabilidade](#110-acionabilidade)
    - [1.11 Delimitação de autoridade](#111-delimitação-de-autoridade)
    - [1.12 Temporalidade](#112-temporalidade)
    - [1.13 Viabilidade](#113-viabilidade)
    - [1.14 Granularidade adequada](#114-granularidade-adequada)
    - [1.15 Preservação de incertezas e lacunas](#115-preservação-de-incertezas-e-lacunas)
    - [1.16 Adequação ao público consumidor](#116-adequação-ao-público-consumidor)
  - [2. Critérios de aceitação e métodos de validação](#2-critérios-de-aceitação-e-métodos-de-validação)
    - [2.1 Identidade do produto](#21-identidade-do-produto)
      - [PA-ID-001 — Nome canônico único](#pa-id-001--nome-canônico-único)
      - [PA-ID-002 — Código ou identificador único](#pa-id-002--código-ou-identificador-único)
      - [PA-ID-003 — Versão conceitual](#pa-id-003--versão-conceitual)
      - [PA-ID-004 — Responsável identificado](#pa-id-004--responsável-identificado)
      - [PA-ID-005 — Organização identificada](#pa-id-005--organização-identificada)
      - [PA-ID-006 — Estágio do produto](#pa-id-006--estágio-do-produto)
      - [PA-ID-007 — Estado temporal](#pa-id-007--estado-temporal)
    - [2.2 Problema real](#22-problema-real)
      - [PA-PR-001 — Existência de uma situação atual observável](#pa-pr-001--existência-de-uma-situação-atual-observável)
      - [PA-PR-002 — Dificuldade específica](#pa-pr-002--dificuldade-específica)
      - [PA-PR-003 — Separação entre problema e solução](#pa-pr-003--separação-entre-problema-e-solução)
      - [PA-PR-004 — Causas identificadas](#pa-pr-004--causas-identificadas)
      - [PA-PR-005 — Consequências identificadas](#pa-pr-005--consequências-identificadas)
      - [PA-PR-006 — Frequência definida](#pa-pr-006--frequência-definida)
      - [PA-PR-007 — Gravidade definida](#pa-pr-007--gravidade-definida)
      - [PA-PR-008 — Evidência disponível](#pa-pr-008--evidência-disponível)
      - [PA-PR-009 — Formulação causal coerente](#pa-pr-009--formulação-causal-coerente)
    - [2.3 Pessoas afetadas e atores](#23-pessoas-afetadas-e-atores)
      - [PA-PE-001 — Usuário principal identificado](#pa-pe-001--usuário-principal-identificado)
      - [PA-PE-002 — Usuários secundários identificados](#pa-pe-002--usuários-secundários-identificados)
      - [PA-PE-003 — Separação entre usuário e parte interessada](#pa-pe-003--separação-entre-usuário-e-parte-interessada)
      - [PA-PE-004 — Papéis operacionais definidos](#pa-pe-004--papéis-operacionais-definidos)
      - [PA-PE-005 — Sistemas externos como atores](#pa-pe-005--sistemas-externos-como-atores)
      - [PA-PE-006 — Necessidades por ator](#pa-pe-006--necessidades-por-ator)
      - [PA-PE-007 — Ausência de atores fictícios](#pa-pe-007--ausência-de-atores-fictícios)
      - [PA-PE-008 — Autoridade identificada](#pa-pe-008--autoridade-identificada)
      - [PA-PE-009 — Separação entre pessoa e papel](#pa-pe-009--separação-entre-pessoa-e-papel)
    - [2.4 Ambiente operacional](#24-ambiente-operacional)
      - [PA-AM-001 — Ambiente físico identificado](#pa-am-001--ambiente-físico-identificado)
      - [PA-AM-002 — Ambiente tecnológico identificado](#pa-am-002--ambiente-tecnológico-identificado)
      - [PA-AM-003 — Condições de conectividade](#pa-am-003--condições-de-conectividade)
      - [PA-AM-004 — Condições temporais](#pa-am-004--condições-temporais)
      - [PA-AM-005 — Condições humanas](#pa-am-005--condições-humanas)
      - [PA-AM-006 — Restrições reais](#pa-am-006--restrições-reais)
      - [PA-AM-007 — Dados estáveis e temporais separados](#pa-am-007--dados-estáveis-e-temporais-separados)
      - [PA-AM-008 — Validação de compatibilidade](#pa-am-008--validação-de-compatibilidade)
    - [2.5 Objetivos](#25-objetivos)
      - [PA-OB-001 — Objetivo orientado a resultado](#pa-ob-001--objetivo-orientado-a-resultado)
      - [PA-OB-002 — Relação com o problema](#pa-ob-002--relação-com-o-problema)
      - [PA-OB-003 — Beneficiário identificado](#pa-ob-003--beneficiário-identificado)
      - [PA-OB-004 — Indicador definido](#pa-ob-004--indicador-definido)
      - [PA-OB-005 — Condição de sucesso](#pa-ob-005--condição-de-sucesso)
      - [PA-OB-006 — Prazo ou fase](#pa-ob-006--prazo-ou-fase)
      - [PA-OB-007 — Viabilidade](#pa-ob-007--viabilidade)
      - [PA-OB-008 — Independência de solução](#pa-ob-008--independência-de-solução)
      - [PA-OB-009 — Prioridade](#pa-ob-009--prioridade)
    - [2.6 Resultados esperados](#26-resultados-esperados)
      - [PA-RE-001 — Resultado observável](#pa-re-001--resultado-observável)
      - [PA-RE-002 — Distinção entre saída e resultado](#pa-re-002--distinção-entre-saída-e-resultado)
      - [PA-RE-003 — Relação com objetivo](#pa-re-003--relação-com-objetivo)
      - [PA-RE-004 — Critério de comparação](#pa-re-004--critério-de-comparação)
      - [PA-RE-005 — Condição de aceitação](#pa-re-005--condição-de-aceitação)
      - [PA-RE-006 — Dependências explicitadas](#pa-re-006--dependências-explicitadas)
      - [PA-RE-007 — Ausência de garantia indevida](#pa-re-007--ausência-de-garantia-indevida)
    - [2.7 Escopo e limites do produto](#27-escopo-e-limites-do-produto)
      - [PA-LI-001 — Escopo positivo definido](#pa-li-001--escopo-positivo-definido)
      - [PA-LI-002 — Fora de escopo explícito](#pa-li-002--fora-de-escopo-explícito)
      - [PA-LI-003 — Fronteira do sistema](#pa-li-003--fronteira-do-sistema)
      - [PA-LI-004 — Responsabilidade humana preservada](#pa-li-004--responsabilidade-humana-preservada)
      - [PA-LI-005 — Limites de automação](#pa-li-005--limites-de-automação)
      - [PA-LI-006 — Compatibilidade com objetivos](#pa-li-006--compatibilidade-com-objetivos)
      - [PA-LI-007 — Ausência de contradição](#pa-li-007--ausência-de-contradição)
      - [PA-LI-008 — Controle de expansão](#pa-li-008--controle-de-expansão)
    - [2.8 Conceitos do domínio](#28-conceitos-do-domínio)
      - [PA-DO-001 — Vocabulário canônico](#pa-do-001--vocabulário-canônico)
      - [PA-DO-002 — Entidades identificadas](#pa-do-002--entidades-identificadas)
      - [PA-DO-003 — Papéis diferenciados](#pa-do-003--papéis-diferenciados)
      - [PA-DO-004 — Eventos identificados](#pa-do-004--eventos-identificados)
      - [PA-DO-005 — Regras do domínio](#pa-do-005--regras-do-domínio)
      - [PA-DO-006 — Exceções](#pa-do-006--exceções)
      - [PA-DO-007 — Relações conceituais](#pa-do-007--relações-conceituais)
      - [PA-DO-008 — Ausência de circularidade](#pa-do-008--ausência-de-circularidade)
      - [PA-DO-009 — Consistência com dados e processos](#pa-do-009--consistência-com-dados-e-processos)
      - [PA-DO-010 — Separação entre conceito e implementação](#pa-do-010--separação-entre-conceito-e-implementação)
    - [2.9 Restrições do produto](#29-restrições-do-produto)
      - [PA-RS-001 — Restrição confirmada](#pa-rs-001--restrição-confirmada)
      - [PA-RS-002 — Impacto identificado](#pa-rs-002--impacto-identificado)
      - [PA-RS-003 — Temporalidade identificada](#pa-rs-003--temporalidade-identificada)
      - [PA-RS-004 — Separação entre restrição e preferência](#pa-rs-004--separação-entre-restrição-e-preferência)
      - [PA-RS-005 — Compatibilidade](#pa-rs-005--compatibilidade)
    - [2.10 Resposta da pergunta central](#210-resposta-da-pergunta-central)
      - [PA-PC-001 — Problema explícito](#pa-pc-001--problema-explícito)
      - [PA-PC-002 — Público afetado explícito](#pa-pc-002--público-afetado-explícito)
      - [PA-PC-003 — Contexto explícito](#pa-pc-003--contexto-explícito)
      - [PA-PC-004 — Resultado explícito](#pa-pc-004--resultado-explícito)
      - [PA-PC-005 — Coerência com as seções detalhadas](#pa-pc-005--coerência-com-as-seções-detalhadas)
      - [PA-PC-006 — Ausência de linguagem promocional](#pa-pc-006--ausência-de-linguagem-promocional)
      - [PA-PC-007 — Concisão sem perda semântica](#pa-pc-007--concisão-sem-perda-semântica)
      - [PA-PC-008 — Ausência de decisão técnica indevida](#pa-pc-008--ausência-de-decisão-técnica-indevida)
  - [3. Validação transversal do documento completo](#3-validação-transversal-do-documento-completo)
    - [3.1 Matriz de rastreabilidade](#31-matriz-de-rastreabilidade)
    - [3.2 Revisão de afirmações](#32-revisão-de-afirmações)
    - [3.3 Revisão de executabilidade](#33-revisão-de-executabilidade)
    - [3.4 Revisão de consistência](#34-revisão-de-consistência)
    - [3.5 Revisão de viabilidade](#35-revisão-de-viabilidade)
    - [3.6 Validação por autoridade](#36-validação-por-autoridade)
  - [4. Estados de avaliação](#4-estados-de-avaliação)
    - [Aprovado](#aprovado)
    - [Aprovado com ressalvas](#aprovado-com-ressalvas)
    - [Pendente de evidência](#pendente-de-evidência)
    - [Pendente de decisão](#pendente-de-decisão)
    - [Reprovado](#reprovado)
    - [Não aplicável](#não-aplicável)
  - [5. Registro mínimo da validação](#5-registro-mínimo-da-validação)
  - [6. Regra final de aprovação](#6-regra-final-de-aprovação)

## Finalidade

Este protocolo estabelece os fatores críticos de sucesso, os critérios de
aceitação e os métodos de validação aplicáveis à criação de documentos de
contexto de produto destinados a orientar pessoas e agentes de inteligência
artificial no desenvolvimento de software.

O objetivo é impedir a aprovação de documentos que:

- sejam visualmente bem organizados, mas semanticamente incorretos;
- contenham afirmações sem fonte ou autoridade;
- confundam problema, requisito, solução e implementação;
- apresentem informações vagas, contraditórias ou não verificáveis;
- não permitam derivar requisitos, arquitetura, decisões ou planos executáveis;
- induzam a IA a completar lacunas por inferência não autorizada.

A unidade de aprovação não é apenas o documento completo. Cada afirmação
relevante deve poder ser avaliada individualmente.

---

## 1. Fatores críticos de sucesso

### 1.1 Correção factual

O conteúdo deve representar corretamente a realidade do produto, da organização,
dos usuários e do ambiente operacional.

A correção factual exige que afirmações sobre pessoas, processos, ferramentas,
limitações, sistemas, regras e evidências possam ser confirmadas por fonte
confiável ou autoridade competente.

**Falha evitada:** Documentação coerente na aparência, porém fundamentada em
fatos inventados, antigos ou incorretos.

---

### 1.2 Completude semântica

O documento deve conter todas as informações necessárias para compreender:

- qual é o problema;
- quem é afetado;
- onde o problema ocorre;
- por que ele importa;
- o que o produto pretende modificar;
- quais resultados são esperados;
- quais limites não podem ser ultrapassados.

Completude não significa quantidade de texto. Significa ausência de lacunas que
obriguem o leitor ou o agente a inventar informação necessária para agir.

**Falha evitada:** Documentos extensos que ainda não permitem determinar o que
deve ser feito.

---

### 1.3 Precisão terminológica

Cada termo relevante deve possuir significado estável e compatível com o
domínio.

Termos semelhantes não podem ser usados como sinônimos quando representam
conceitos diferentes.

Exemplos de distinções necessárias:

- usuário e operador;
- administrador e mantenedor;
- objetivo e funcionalidade;
- problema e causa;
- causa e consequência;
- escopo e requisito;
- evidência e inferência;
- sistema externo e parte interessada.

**Falha evitada:** Interpretações diferentes produzidas por humanos ou agentes a
partir do mesmo texto.

---

### 1.4 Ausência de ambiguidade

Cada afirmação deve admitir uma interpretação operacional dominante.

Expressões como “rápido”, “adequado”, “fácil”, “seguro”, “completo”, “intuitivo”
e “quando necessário” não devem permanecer sem definição ou critério mensurável.

**Falha evitada:** Implementações distintas e incompatíveis baseadas na mesma
frase.

---

### 1.5 Rastreabilidade

Afirmações relevantes devem apontar para:

- fonte;
- autoridade;
- evidência;
- decisão;
- documento relacionado;
- requisito derivado, quando já existente.

A rastreabilidade deve permitir reconstruir de onde a informação veio e por que
ela foi considerada válida.

**Falha evitada:** Informação sem origem que não pode ser confirmada nem
corrigida.

---

### 1.6 Separação entre fato, inferência e decisão

O documento deve distinguir explicitamente:

- fato confirmado;
- informação declarada por uma fonte;
- inferência analítica;
- hipótese;
- decisão aprovada;
- recomendação;
- pendência;
- informação desconhecida.

**Falha evitada:** A IA transformar uma suposição plausível em regra oficial do
produto.

---

### 1.7 Verificabilidade

Cada afirmação crítica deve poder ser:

- confirmada;
- rejeitada;
- medida;
- observada;
- testada;
- aprovada por autoridade identificada.

Conteúdo que não possa ser verificado deve ser classificado como hipótese,
pendência ou interpretação.

**Falha evitada:** Aprovação baseada apenas em qualidade textual.

---

### 1.8 Consistência interna

Nenhuma seção pode contradizer outra.

Devem ser consistentes, entre si:

- problema;
- objetivos;
- resultados esperados;
- escopo;
- fora de escopo;
- atores;
- restrições;
- conceitos do domínio.

**Falha evitada:** Um objetivo exigir uma capacidade que o escopo proíbe ou que
as restrições tornam inviável.

---

### 1.9 Consistência externa

O documento deve permanecer compatível com:

- políticas organizacionais;
- decisões aprovadas;
- contratos;
- legislação;
- arquitetura existente;
- ambiente de engenharia;
- documentos canônicos;
- estado operacional vigente.

**Falha evitada:** Documento internamente coerente, mas incompatível com a
realidade institucional ou técnica.

---

### 1.10 Acionabilidade

O conteúdo deve permitir derivar ações posteriores.

A partir dele deve ser possível produzir:

- requisitos;
- critérios de aceitação;
- decisões;
- arquitetura;
- plano de implementação;
- riscos;
- testes;
- estado operacional.

**Falha evitada:** Documento puramente descritivo, incapaz de orientar trabalho
real.

---

### 1.11 Delimitação de autoridade

O documento deve identificar:

- quem forneceu a informação;
- quem pode aprová-la;
- quem pode alterá-la;
- qual fonte prevalece em caso de conflito;
- quais itens ainda dependem de decisão.

**Falha evitada:** A IA escolher arbitrariamente entre informações conflitantes.

---

### 1.12 Temporalidade

Informações sujeitas a mudança devem conter:

- data de referência;
- versão;
- período de validade;
- condição de revalidação.

Exemplos:

- equipe disponível;
- orçamento;
- ferramentas instaladas;
- prazo;
- estágio do produto;
- integrações ativas;
- restrições temporárias.

**Falha evitada:** Uso de informação antiga como verdade atual.

---

### 1.13 Viabilidade

Objetivos, resultados e escopo devem ser compatíveis com:

- orçamento;
- prazo;
- equipe;
- tecnologia;
- dados;
- permissões;
- infraestrutura;
- dependências externas.

**Falha evitada:** Documentação correta conceitualmente, mas impossível de
executar.

---

### 1.14 Granularidade adequada

Cada afirmação deve tratar de um objeto principal.

Itens muito amplos devem ser decompostos para permitir:

- aprovação individual;
- alteração controlada;
- rastreabilidade;
- verificação isolada.

**Falha evitada:** Um único item conter partes corretas e incorretas sem
possibilidade de avaliação separada.

---

### 1.15 Preservação de incertezas e lacunas

A IA não deve completar silenciosamente informações ausentes.

Toda lacuna relevante deve ser marcada como:

- desconhecida;
- não confirmada;
- pendente de decisão;
- pendente de evidência;
- não aplicável.

**Falha evitada:** Documentação aparentemente completa, mas construída com
invenções.

---

### 1.16 Adequação ao público consumidor

O conteúdo deve ser compreensível e utilizável por:

- responsáveis pelo produto;
- especialistas do domínio;
- desenvolvedores;
- arquitetos;
- testadores;
- operadores;
- agentes de IA.

A redação deve preservar precisão técnica sem depender de conhecimento implícito
exclusivo de uma pessoa.

**Falha evitada:** Documento inteligível para o autor, mas insuficiente para os
demais consumidores.

---

## 2. Critérios de aceitação e métodos de validação

### 2.1 Identidade do produto

**Critérios de aceitação:**

#### PA-ID-001 — Nome canônico único

Deve existir um único nome oficial.

#### PA-ID-002 — Código ou identificador único

O código deve ser estável, não ambíguo e não reutilizado.

#### PA-ID-003 — Versão conceitual

A versão deve indicar a evolução do conceito documental, independentemente da
versão do software, quando forem diferentes.

#### PA-ID-004 — Responsável identificado

Deve haver pessoa ou papel responsável pela validade do conteúdo.

#### PA-ID-005 — Organização identificada

A organização proprietária ou responsável deve ser explícita.

#### PA-ID-006 — Estágio do produto

O estágio deve usar vocabulário controlado, como:

- ideia;
- descoberta;
- concepção;
- protótipo;
- desenvolvimento;
- piloto;
- produção;
- manutenção;
- descontinuação.

#### PA-ID-007 — Estado temporal

Deve existir data de atualização e status documental.

**Método de validação:**

1. Comparar com registros oficiais.
2. Verificar duplicidade de nomes e códigos.
3. Confirmar responsável e organização.
4. Verificar se o estágio corresponde às evidências reais.
5. Conferir histórico de versões.
6. Validar que “produção” só seja usado quando houver implantação e aceitação
   comprovadas.

---

### 2.2 Problema real

**Finalidade:**Descrever a situação negativa, necessidade não atendida ou
oportunidade que justifica a criação do produto.

**Critérios de aceitação:**

#### PA-PR-001 — Existência de uma situação atual observável

O texto deve explicar o que ocorre atualmente, antes da introdução do produto.

Deve indicar:

- processo atual;
- comportamento atual;
- condição insatisfatória;
- local ou contexto em que ocorre.

Não pode começar diretamente com uma solução tecnológica.

#### PA-PR-002 — Dificuldade específica

A dificuldade deve ser descrita como uma condição concreta.

Deve responder:

- o que não pode ser feito;
- o que é feito com erro;
- o que exige esforço excessivo;
- o que demora;
- o que gera perda, risco ou retrabalho.

#### PA-PR-003 — Separação entre problema e solução

A formulação do problema não deve incorporar prematuramente:

- linguagem de programação;
- banco de dados;
- framework;
- interface;
- arquitetura;
- ferramenta específica;
- automação ainda não aprovada.

#### PA-PR-004 — Causas identificadas

As causas devem ser separadas do problema e classificadas como:

- confirmadas;
- prováveis;
- hipóteses;
- desconhecidas.

Causas não confirmadas não podem ser apresentadas como fatos.

#### PA-PR-005 — Consequências identificadas

O texto deve indicar impactos concretos, como:

- tempo perdido;
- erro;
- atraso;
- custo;
- risco;
- perda de informação;
- baixa qualidade;
- impossibilidade de decisão;
- exposição legal ou operacional.

#### PA-PR-006 — Frequência definida

A frequência deve ser expressa por:

- ocorrência;
- período;
- volume;
- evento disparador;
- condição recorrente.

Expressões como “frequentemente” devem ser acompanhadas de evidência ou
classificação explícita como estimativa.

#### PA-PR-007 — Gravidade definida

A gravidade deve considerar:

- impacto;
- alcance;
- urgência;
- reversibilidade;
- risco associado.

A classificação deve possuir escala ou justificativa.

#### PA-PR-008 — Evidência disponível

O problema deve possuir pelo menos uma fonte de sustentação:

- registro;
- documento;
- entrevista;
- medição;
- planilha;
- incidente;
- observação;
- histórico;
- declaração da autoridade.

Na ausência de evidência, o problema deve ser classificado como hipótese a
validar.

#### PA-PR-009 — Formulação causal coerente

A relação deve seguir:

```text
causa
→ situação problemática
→ consequência
```

A causa não pode ser repetida como consequência nem a solução ser descrita como
causa.

**Método de validação:**

1. Executar revisão por especialista do domínio.
2. Comparar o texto com entrevistas, documentos e registros disponíveis.
3. Aplicar teste de reformulação:

   - remover toda referência à solução;
   - verificar se o problema continua compreensível.

4. Construir um diagrama causal.
5. Procurar afirmações sem fonte.
6. Classificar cada afirmação como fato, inferência ou hipótese.
7. Solicitar ao responsável que confirme:

   - “Esta descrição corresponde ao problema real?”

8. Rejeitar o item quando a única evidência for a própria redação da IA.

**Evidências mínimas para aprovação:**

- uma descrição da situação atual;
- uma dificuldade observável;
- pelo menos uma consequência;
- uma fonte ou declaração autorizada;
- classificação das causas não confirmadas.

---

### 2.3 Pessoas afetadas e atores

**Finalidade:** Identificar quem sofre o problema, quem interage com o produto e
quem é afetado pelas consequências ou decisões relacionadas.

**Critérios de aceitação:**

#### PA-PE-001 — Usuário principal identificado

O usuário principal deve ser definido por:

- papel;
- objetivo;
- atividade;
- contexto de uso;
- relação com o problema.

Nome de pessoa não substitui definição de papel.

#### PA-PE-002 — Usuários secundários identificados

Devem ser incluídos os usuários que:

- consultam resultados;
- fornecem dados;
- recebem saídas;
- executam etapas auxiliares;
- são afetados indiretamente.

#### PA-PE-003 — Separação entre usuário e parte interessada

O documento deve distinguir:

- quem utiliza o produto;
- quem decide;
- quem financia;
- quem mantém;
- quem regula;
- quem recebe impacto;
- quem fornece serviço externo.

#### PA-PE-004 — Papéis operacionais definidos

Os papéis de administrador, operador e mantenedor devem ser explicitados ou
marcados como não aplicáveis.

Cada papel deve conter:

- responsabilidades;
- permissões;
- limites;
- interação com o produto.

#### PA-PE-005 — Sistemas externos como atores

Sistemas externos que enviam, recebem ou processam dados devem ser identificados
como atores não humanos.

#### PA-PE-006 — Necessidades por ator

Cada ator relevante deve possuir:

- necessidade;
- objetivo;
- responsabilidade;
- risco ou consequência associada.

#### PA-PE-007 — Ausência de atores fictícios

Nenhum ator deve ser incluído apenas porque é comum em sistemas semelhantes.

#### PA-PE-008 — Autoridade identificada

Deve ser possível determinar quem:

- aprova o produto;
- aprova requisitos;
- autoriza mudanças;
- aceita resultados.

#### PA-PE-009 — Separação entre pessoa e papel

Uma mesma pessoa deve ser representada por papéis distintos quando exercer
responsabilidades, permissões ou interesses diferentes no produto.

**Método de validação:**

1. Construir matriz de atores e responsabilidades.
2. Revisar com responsáveis reais.
3. Verificar organogramas, contratos ou processos existentes.
4. Simular jornadas de uso para cada ator.
5. Perguntar para cada papel:

   - qual ação executa;
   - qual informação consome;
   - qual decisão toma.

6. Remover papéis sem interação, responsabilidade ou impacto identificável.
7. Comparar permissões descritas com políticas reais.
8. Criar uma matriz RACI ou equivalente.
9. Verificar se todos os fluxos possuem ator responsável.
10. Identificar conflitos de responsabilidade entre papéis.

**Evidências mínimas para aprovação:**

- usuário principal;
- atores secundários relevantes;
- autoridade de aprovação;
- responsabilidades;
- sistemas externos aplicáveis;
- justificativa para papéis declarados como não aplicáveis;
- separação explícita entre pessoas e papéis.

---

### 2.4 Ambiente operacional

**Finalidade:** Definir onde, quando e sob quais condições o produto será
utilizado.

**Critérios de aceitação:**

#### PA-AM-001 — Ambiente físico identificado

Quando aplicável, devem ser descritos:

- local;
- condições físicas;
- mobilidade;
- iluminação;
- ruído;
- temperatura;
- acesso a energia;
- riscos ambientais.

#### PA-AM-002 — Ambiente tecnológico identificado

Deve incluir, conforme aplicável:

- sistema operacional;
- dispositivo;
- navegador;
- runtime;
- rede;
- armazenamento;
- serviços;
- integrações;
- versões mínimas.

#### PA-AM-003 — Condições de conectividade

Devem ser explicitadas:

- operação online;
- operação offline;
- largura de banda;
- instabilidade;
- latência;
- sincronização posterior.

#### PA-AM-004 — Condições temporais

Deve indicar:

- momento de uso;
- frequência;
- duração;
- picos de utilização;
- janelas operacionais;
- prazo crítico de resposta.

#### PA-AM-005 — Condições humanas

Devem ser consideradas:

- experiência do usuário;
- treinamento necessário;
- carga cognitiva;
- disponibilidade;
- acessibilidade;
- pressão de tempo.

#### PA-AM-006 — Restrições reais

O ambiente deve refletir a infraestrutura efetivamente disponível, e não a
infraestrutura desejada.

#### PA-AM-007 — Dados estáveis e temporais separados

Informações sujeitas a mudança devem conter data de verificação.

#### PA-AM-008 — Validação de compatibilidade

O ambiente descrito deve ser compatível com:

- requisitos;
- integrações;
- arquitetura;
- ferramentas;
- restrições.

**Método de validação:**

1. Inspecionar o ambiente real.
2. Executar comandos de identificação de versões.
3. Testar o produto ou protótipo no ambiente-alvo.
4. Confirmar disponibilidade de rede, hardware e permissões.
5. Realizar entrevista contextual com operadores.
6. Comparar o ambiente descrito com o contexto de engenharia.
7. Marcar como não confirmado tudo que não foi observado ou comprovado.
8. Revalidar dados temporais antes de decisões técnicas.

**Evidências mínimas para aprovação:**

- plataforma;
- condições de conectividade;
- contexto físico ou operacional relevante;
- limitações observadas;
- data da verificação;
- fonte das informações.

---

### 2.5 Objetivos

**Finalidade:** Definir mudanças de estado que o produto deve provocar.

**Critérios de aceitação:**

#### PA-OB-001 — Objetivo orientado a resultado

O objetivo deve expressar uma transformação, não apenas uma atividade.

Inadequado:

```text
Criar uma tela de exportação.
```

Adequado:

```text
Reduzir o tempo necessário para produzir um clipe compartilhável.
```

#### PA-OB-002 — Relação com o problema

Cada objetivo deve responder a pelo menos uma causa, consequência ou necessidade
identificada.

#### PA-OB-003 — Beneficiário identificado

Cada objetivo deve indicar quem recebe o benefício.

#### PA-OB-004 — Indicador definido

O objetivo deve possuir uma medida ou observação verificável.

Exemplos:

- tempo;
- taxa de erro;
- número de etapas;
- disponibilidade;
- volume;
- percentual de sucesso.

#### PA-OB-005 — Condição de sucesso

Deve existir um limiar que permita decidir se o objetivo foi alcançado.

#### PA-OB-006 — Prazo ou fase

Cada objetivo deve indicar:

- data;
- versão;
- release;
- marco;
- fase;
- condição temporal.

#### PA-OB-007 — Viabilidade

O objetivo deve ser compatível com restrições conhecidas.

#### PA-OB-008 — Independência de solução

O objetivo não deve impor tecnologia sem decisão aprovada.

#### PA-OB-009 — Prioridade

Objetivos devem ser classificados quando houver mais de um.

**Método de validação:**

1. Mapear objetivo para problema e beneficiário.
2. Aplicar teste SMART adaptado:

   - específico;
   - mensurável;
   - atingível;
   - relevante;
   - temporal.

3. Verificar se o indicador possui fonte de medição.
4. Simular avaliação futura:

   - “Com quais dados afirmaremos que foi atingido?”

5. Confirmar viabilidade com engenharia e responsável pelo produto.
6. Rejeitar objetivos que sejam apenas entregáveis técnicos.

**Evidências mínimas para aprovação:**

- resultado pretendido;
- beneficiário;
- indicador;
- condição de sucesso;
- prazo ou fase;
- vínculo com o problema.

---

### 2.6 Resultados esperados

**Finalidade:** Descrever os efeitos observáveis que devem existir após a
implementação e o uso do produto.

**Critérios de aceitação:**

#### PA-RE-001 — Resultado observável

O resultado deve poder ser percebido ou medido.

#### PA-RE-002 — Distinção entre saída e resultado

O documento deve diferenciar:

- saída: artefato produzido pelo sistema;
- resultado: mudança provocada pela utilização;
- impacto: consequência mais ampla ou de longo prazo.

#### PA-RE-003 — Relação com objetivo

Cada resultado esperado deve estar ligado a um objetivo.

#### PA-RE-004 — Critério de comparação

Quando aplicável, deve existir linha de base:

- situação anterior;
- valor atual;
- processo anterior;
- desempenho de referência.

#### PA-RE-005 — Condição de aceitação

Deve existir um critério que permita classificar o resultado como:

- atingido;
- parcialmente atingido;
- não atingido.

#### PA-RE-006 — Dependências explicitadas

Resultados dependentes de comportamento humano, serviço externo ou dado não
controlado devem declarar essa dependência.

#### PA-RE-007 — Ausência de garantia indevida

O documento não pode garantir impactos fora do controle do produto.

**Método de validação:**

1. Construir matriz objetivo–resultado–indicador.
2. Comparar com linha de base.
3. Verificar método de coleta do indicador.
4. Separar resultado direto de impacto indireto.
5. Testar causalidade:

   - “O produto consegue realmente produzir este resultado?”

6. Identificar variáveis externas.
7. Validar com usuários e autoridade do produto.

**Evidências mínimas para aprovação:**

- resultado observável;
- objetivo relacionado;
- indicador;
- linha de base ou referência;
- condição de aceitação;
- dependências externas.

---

### 2.7 Escopo e limites do produto

**Finalidade:** Delimitar o que o produto pode, deve e não deve fazer.

**Critérios de aceitação:**

#### PA-LI-001 — Escopo positivo definido

Devem ser descritas:

- capacidades incluídas;
- processos incluídos;
- usuários incluídos;
- ambientes incluídos;
- integrações incluídas.

Cada capacidade deve possuir nome, finalidade, usuário beneficiado, limite e
relação com um objetivo.

Cada processo deve indicar início, fim, ator, entrada e saída.

Os usuários incluídos devem ser identificados pelos papéis autorizados ou
beneficiados.

Os ambientes incluídos devem indicar as plataformas e condições suportadas.

Cada integração deve indicar sistema, direção do fluxo, dados envolvidos,
dependência e autoridade responsável.

#### PA-LI-002 — Fora de escopo explícito

Devem ser descritas:

- funcionalidades excluídas;
- automações não realizadas;
- ambientes não suportados;
- integrações excluídas;
- responsabilidades preservadas fora do produto.

Para as automações não realizadas, deve ser indicado o que continuará manual,
assistido, externo ou dependente de aprovação.

Exclusões críticas devem conter justificativa, fase, decisão relacionada e
condição de reavaliação.

#### PA-LI-003 — Fronteira do sistema

Deve ser possível distinguir:

- o que pertence ao produto;
- o que pertence ao usuário;
- o que pertence à organização;
- o que pertence a sistemas externos.

#### PA-LI-004 — Responsabilidade humana preservada

Decisões que permanecem humanas devem ser explicitadas.

#### PA-LI-005 — Limites de automação

Deve ser indicado:

- o que a IA pode executar;
- o que exige aprovação;
- o que não pode executar;
- o que deve apenas recomendar.

#### PA-LI-006 — Compatibilidade com objetivos

Tudo que for necessário para atingir um objetivo obrigatório deve estar incluído
ou ter dependência externa formalizada.

#### PA-LI-007 — Ausência de contradição

Um item não pode estar simultaneamente em escopo e fora de escopo.

#### PA-LI-008 — Controle de expansão

Itens futuros devem ser classificados como:

- possibilidade;
- backlog;
- hipótese;
- fase posterior.

Não devem aparecer como capacidade vigente.

**Método de validação:**

1. Construir diagrama de contexto.
2. Criar matriz “dentro/fora”.
3. Mapear objetivos para capacidades.
4. Identificar responsabilidades humanas.
5. Revisar interfaces externas.
6. Procurar funcionalidades implícitas no texto.
7. Simular pedidos limítrofes:

   - “O produto deve fazer isto?”

8. Confirmar com autoridade de produto.
9. Mapear os processos incluídos em fluxograma.
10. Confrontar os ambientes incluídos com o contexto operacional.
11. Testar a disponibilidade das integrações incluídas.
12. Registrar as decisões de exclusão.

**Evidências mínimas para aprovação:**

- lista de capacidades incluídas;
- lista de exclusões;
- fronteiras;
- responsabilidades humanas;
- integrações;
- ambientes suportados;
- justificativas para exclusões críticas.

---

### 2.8 Conceitos do domínio

**Finalidade:** Estabelecer uma linguagem comum e um modelo conceitual
suficiente para orientar requisitos, arquitetura, dados, regras e validações.

**Critérios de aceitação:**

#### PA-DO-001 — Vocabulário canônico

Cada termo relevante deve possuir:

- nome preferencial;
- definição;
- sinônimos permitidos;
- sinônimos proibidos ou ambíguos;
- fonte ou autoridade.

#### PA-DO-002 — Entidades identificadas

As entidades principais devem possuir:

- identidade;
- definição;
- atributos relevantes;
- relações;
- ciclo de vida, quando aplicável.

#### PA-DO-003 — Papéis diferenciados

Papéis devem ser definidos por responsabilidade, e não apenas por nome.

#### PA-DO-004 — Eventos identificados

Eventos relevantes devem indicar:

- o que ocorreu;
- quem ou o que participou;
- quando ocorre;
- quais efeitos produz.

#### PA-DO-005 — Regras do domínio

Regras devem ser expressas como condições verificáveis.

#### PA-DO-006 — Exceções

Cada regra sujeita a exceção deve indicar:

- condição excepcional;
- autoridade;
- efeito;
- registro necessário.

#### PA-DO-007 — Relações conceituais

Devem ser definidas relações como:

- pertence a;
- executa;
- produz;
- depende de;
- substitui;
- valida;
- ocorre antes de;
- deriva de.

#### PA-DO-008 — Ausência de circularidade

Uma definição não pode depender apenas de outro termo igualmente indefinido.

#### PA-DO-009 — Consistência com dados e processos

O modelo conceitual deve corresponder aos registros, documentos e processos
reais.

#### PA-DO-010 — Separação entre conceito e implementação

Entidades do domínio não devem ser confundidas com:

- tabelas;
- classes;
- telas;
- endpoints;
- nomes de arquivos.

**Método de validação:**

1. Revisar glossário com especialista do domínio.
2. Construir modelo conceitual ou mapa de entidades.
3. Verificar termos em documentos existentes.
4. Testar definições com exemplos e contraexemplos.
5. Validar regras com casos normais e excepcionais.
6. Identificar termos usados com mais de um significado.
7. Comparar o vocabulário com dados reais.
8. Verificar se requisitos utilizam apenas termos definidos.

**Evidências mínimas para aprovação:**

- glossário;
- entidades;
- papéis;
- eventos;
- regras;
- exceções;
- relações;
- aprovação de especialista do domínio.

---

### 2.9 Restrições do produto

**Finalidade:** Definir condições que limitam as soluções possíveis.

**Critérios de aceitação:** **Privacidade:** Deve indicar:

- tipos de dados;
- pessoas afetadas;
- finalidade;
- acesso;
- retenção;
- compartilhamento;
- anonimização;
- base normativa aplicável.

**Orçamento:** Deve indicar:

- limite;
- período;
- itens incluídos;
- itens excluídos;
- autoridade;
- data de validade.

**Conectividade:** Deve indicar:

- dependência de internet;
- operação offline;
- sincronização;
- falhas esperadas.

**Hardware:** Deve indicar:

- dispositivos;
- requisitos mínimos;
- recursos disponíveis;
- limitações.

**Legislação:** Deve indicar:

- norma aplicável;
- jurisdição;
- obrigação;
- responsável pela interpretação;
- data de verificação.

**Prazo:** Deve indicar:

- marco;
- data;
- dependências;
- tolerância;
- impacto do atraso.

**Capacidade da equipe:** Deve indicar:

- papéis;
- disponibilidade;
- competências;
- limitações;
- atividades externas.

**Dependências de terceiros:** Deve indicar:

- fornecedor;
- serviço;
- contrato;
- disponibilidade;
- risco;
- alternativa;
- condição de interrupção.

#### PA-RS-001 — Restrição confirmada

Cada restrição deve possuir fonte ou autoridade.

#### PA-RS-002 — Impacto identificado

Deve ser explicado quais decisões ou capacidades a restrição afeta.

#### PA-RS-003 — Temporalidade identificada

Restrições temporárias não podem ser tratadas como permanentes.

#### PA-RS-004 — Separação entre restrição e preferência

Preferências devem ser classificadas separadamente.

#### PA-RS-005 — Compatibilidade

As restrições não podem ser incompatíveis com objetivos obrigatórios sem
registro de conflito.

**Método de validação:**

1. Revisar contratos, políticas e legislação.
2. verificar ambiente técnico.
3. confirmar orçamento e prazo com autoridade.
4. revisar dependências externas.
5. executar análise de viabilidade.
6. mapear restrição para requisitos e arquitetura.
7. classificar cada restrição como:

   - obrigatória;
   - negociável;
   - temporária;
   - não confirmada.

8. registrar conflitos para decisão.

**Evidências mínimas para aprovação:**

- fonte;
- autoridade;
- impacto;
- validade;
- classificação;
- dependências;
- conflitos.

---

### 2.10 Resposta da pergunta central

**Pergunta:**

> Qual problema deve ser resolvido, para quem, em qual contexto e com qual
> resultado?

**Finalidade:** Produzir uma síntese executiva que conecte problema,
beneficiário, ambiente e resultado sem eliminar as nuances das seções
detalhadas.

**Critérios de aceitação:**

#### PA-PC-001 — Problema explícito

A resposta deve descrever a dificuldade atual, sem iniciar pela solução.

#### PA-PC-002 — Público afetado explícito

A resposta deve nomear o papel principal afetado.

#### PA-PC-003 — Contexto explícito

Deve indicar onde, quando ou sob quais condições o problema ocorre.

#### PA-PC-004 — Resultado explícito

Deve descrever a transformação esperada.

#### PA-PC-005 — Coerência com as seções detalhadas

A síntese não pode introduzir informações ausentes das seções de suporte.

#### PA-PC-006 — Ausência de linguagem promocional

Não deve utilizar formulações como:

- revolucionar;
- solução completa;
- experiência perfeita;
- eliminar todos os erros.

#### PA-PC-007 — Concisão sem perda semântica

A resposta deve ser suficientemente curta para funcionar como síntese, mas
completa o bastante para responder aos quatro componentes.

#### PA-PC-008 — Ausência de decisão técnica indevida

A resposta central não deve impor arquitetura ou tecnologia, salvo quando
constituírem restrição aprovada.

**Estrutura recomendada:**

```text
O produto deve resolver [problema], que afeta [pessoa ou papel],
no contexto de [ambiente ou processo], para produzir [resultado verificável].
```

**Método de validação:**

1. Separar a frase em quatro partes:

   - problema;
   - público;
   - contexto;
   - resultado.

2. Comparar cada parte com a seção detalhada correspondente.
3. Remover nomes de tecnologias e verificar se a síntese permanece válida.
4. Solicitar ao responsável que reformule com suas próprias palavras.
5. Rejeitar a síntese quando qualquer componente depender de inferência.

**Evidências mínimas para aprovação:**

- problema rastreável;
- pessoa rastreável;
- contexto rastreável;
- resultado rastreável;
- concordância com o conteúdo detalhado.

---

## 3. Validação transversal do documento completo

Além da aprovação individual de cada seção, o documento deve passar pelas
validações abaixo.

### 3.1 Matriz de rastreabilidade

Deve existir relação entre:

```text
problema
→ pessoas afetadas
→ objetivos
→ resultados esperados
→ escopo
→ restrições
→ conceitos do domínio
```

**Critério de aceitação:** Nenhum objetivo obrigatório pode existir sem problema
ou necessidade correspondente.

Nenhum resultado esperado pode existir sem objetivo.

Nenhuma capacidade incluída pode existir sem justificativa.

Nenhuma exclusão pode contradizer objetivo obrigatório.

**Método de validação:** Construir matriz com identificadores e procurar
relações ausentes ou contraditórias.

---

### 3.2 Revisão de afirmações

Cada afirmação crítica deve ser classificada como:

- fato;
- evidência;
- declaração de fonte;
- inferência;
- hipótese;
- decisão;
- recomendação;
- pendência.

**Critério de aceitação:** Nenhuma inferência ou hipótese pode aparecer como
fato confirmado.

**Método de validação:** Executar revisão sentença por sentença e exigir
marcação de proveniência.

---

### 3.3 Revisão de executabilidade

**Critério de aceitação:** O documento deve permitir derivar:

- requisitos funcionais;
- requisitos não funcionais;
- regras de negócio;
- restrições;
- atores;
- critérios de aceitação;
- riscos;
- arquitetura inicial.

**Método de validação:** Solicitar a um revisor independente ou agente sem
contexto anterior que produza uma primeira decomposição de requisitos apenas a
partir do documento.

Se o revisor precisar inventar informações críticas, o documento não está
completo.

---

### 3.4 Revisão de consistência

**Critério de aceitação:** Não pode haver contradição entre:

- problema e objetivo;
- objetivo e resultado;
- resultado e escopo;
- escopo e fora de escopo;
- ambiente e restrição;
- ator e responsabilidade;
- regra e exceção.

**Método de validação:** Executar análise cruzada de pares de seções e registrar
conflitos.

---

### 3.5 Revisão de viabilidade

**Critério de aceitação:** Os resultados esperados devem ser possíveis
considerando:

- orçamento;
- prazo;
- equipe;
- hardware;
- conectividade;
- integrações;
- legislação.

**Método de validação:** Realizar revisão conjunta entre produto, domínio e
engenharia.

---

### 3.6 Validação por autoridade

**Critério de aceitação:** O documento deve possuir aprovação explícita da
autoridade competente.

A aprovação deve indicar:

- versão;
- data;
- escopo aprovado;
- ressalvas;
- pendências;
- responsável.

**Método de validação:** Registrar decisão, aceite ou assinatura em meio
controlado.

---

## 4. Estados de avaliação

Cada seção deve receber um dos seguintes estados:

### Aprovado

Todos os critérios obrigatórios foram atendidos e existem evidências
suficientes.

### Aprovado com ressalvas

O conteúdo pode ser utilizado, mas existem limitações não bloqueantes
explicitadas.

### Pendente de evidência

A informação é plausível, porém não foi comprovada.

### Pendente de decisão

Existe conflito ou ausência de autoridade para definir o conteúdo.

### Reprovado

O conteúdo possui erro, contradição, ambiguidade crítica ou ausência de
informação essencial.

### Não aplicável

O item não pertence ao produto, e a justificativa foi registrada.

---

## 5. Registro mínimo da validação

```yaml
validation_record:
  item_id: PA-PR-001
  item_name: Situacao atual
  document_version: "1.0.0"
  status: approved
  validator: "papel ou pessoa"
  validation_date: "AAAA-MM-DD"
  method:
    - document_review
    - stakeholder_confirmation
  evidence:
    - source_id: SRC-001
    - decision_id: DEC-001
  findings: []
  limitations: []
  required_actions: []
```

---

## 6. Regra final de aprovação

O documento somente deve ser considerado apto a orientar agentes de IA quando:

1. a pergunta central estiver respondida;
2. todas as seções obrigatórias estiverem aprovadas ou justificadamente não
   aplicáveis;
3. as afirmações críticas possuírem fonte, autoridade ou classificação de
   incerteza;
4. não houver contradições bloqueantes;
5. os limites do produto estiverem explícitos;
6. os conceitos do domínio estiverem definidos;
7. objetivos e resultados forem verificáveis;
8. o ambiente operacional e as restrições forem reais;
9. um revisor independente conseguir derivar requisitos sem inventar fatos;
10. a versão aprovada estiver identificada, registrada e controlada.

O documento não deve ser aprovado apenas porque:

- está bem formatado;
- possui muitas seções;
- utiliza linguagem técnica;
- contém diagramas;
- foi gerado por um modelo avançado;
- parece coerente;
- não apresenta erros gramaticais.

A aprovação exige correspondência comprovável entre texto, realidade,
autoridade, restrições e possibilidade de execução.

*Esse protocolo pode ser convertido posteriormente em checklist, schema JSON ou
matriz de auditoria automatizada.*
