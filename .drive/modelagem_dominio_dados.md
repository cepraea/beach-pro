# **Modelagem Completa do Domínio de Conhecimento — Descoberta e Modelagem do CEPRAEA-BEACH-PRO**

- [**Modelagem Completa do Domínio de Conhecimento — Descoberta e Modelagem do CEPRAEA-BEACH-PRO**](#modelagem-completa-do-domínio-de-conhecimento--descoberta-e-modelagem-do-cepraea-beach-pro)
  - [**1. Denominação do domínio**](#1-denominação-do-domínio)
    - [**1.1 Domínio científico e metodológico**](#11-domínio-científico-e-metodológico)
    - [**1.2 Domínio de aplicação**](#12-domínio-de-aplicação)
    - [**1.3 Domínio de implementação**](#13-domínio-de-implementação)
    - [**1.4 Domínios transversais**](#14-domínios-transversais)
  - [**2. Objeto real da tarefa**](#2-objeto-real-da-tarefa)
  - [**3. Problema fundamental**](#3-problema-fundamental)
  - [**4. Missão do agente**](#4-missão-do-agente)
  - [**5. Princípios fundamentais**](#5-princípios-fundamentais)
    - [**5.1 Fonte não é modelo**](#51-fonte-não-é-modelo)
    - [**5.2 Significado precede implementação**](#52-significado-precede-implementação)
    - [**5.3 Evidência precede inferência**](#53-evidência-precede-inferência)
    - [**5.4 Fato não é intenção**](#54-fato-não-é-intenção)
    - [**5.5 Estado atual não substitui histórico**](#55-estado-atual-não-substitui-histórico)
    - [**5.6 Não generalizar sem necessidade operacional**](#56-não-generalizar-sem-necessidade-operacional)
  - [**6. Escopo do domínio operacional**](#6-escopo-do-domínio-operacional)
  - [**7. Restrições operacionais atualmente validadas**](#7-restrições-operacionais-atualmente-validadas)
  - [**8. Objetos semânticos fundamentais**](#8-objetos-semânticos-fundamentais)
    - [**8.1 Entidade**](#81-entidade)
    - [**8.2 Value Object**](#82-value-object)
    - [**8.3 Papel**](#83-papel)
    - [**8.4 Associação**](#84-associação)
    - [**8.5 Evento**](#85-evento)
    - [**8.6 Estado**](#86-estado)
    - [**8.7 Regra**](#87-regra)
    - [**8.8 Fato histórico**](#88-fato-histórico)
    - [**8.9 Projeção**](#89-projeção)
  - [**9. Seis objetos obrigatórios de descoberta e formalização**](#9-seis-objetos-obrigatórios-de-descoberta-e-formalização)
  - [**10. Bounded Contexts**](#10-bounded-contexts)
    - [**10.1 Objetivo**](#101-objetivo)
    - [**10.2 Descoberta**](#102-descoberta)
    - [**10.3 Candidatos iniciais**](#103-candidatos-iniciais)
    - [**10.4 Formalização**](#104-formalização)
  - [**11. Identidades definitivas**](#11-identidades-definitivas)
    - [**11.1 Objetivo**](#111-objetivo)
    - [**11.2 Para cada identidade, descobrir**](#112-para-cada-identidade-descobrir)
    - [**11.3 Identidade humana**](#113-identidade-humana)
  - [**12. Agregados**](#12-agregados)
    - [**11.1 Objetivo**](#111-objetivo-1)
    - [**11.2 Um agregado não é automaticamente**](#112-um-agregado-não-é-automaticamente)
    - [**11.3 Critérios**](#113-critérios)
    - [**11.4 Formalização**](#114-formalização)
  - [**13. Invariantes**](#13-invariantes)
    - [**11.1 Definição**](#111-definição)
    - [**11.2 Invariantes atualmente conhecidas ou candidatas**](#112-invariantes-atualmente-conhecidas-ou-candidatas)
    - [**11.3 Registro formal de invariante**](#113-registro-formal-de-invariante)
  - [**14. Ciclos de vida**](#14-ciclos-de-vida)
    - [**14.1 Padrões temporais candidatos**](#141-padrões-temporais-candidatos)
  - [**15. Fronteiras transacionais**](#15-fronteiras-transacionais)
    - [**15.1 Objetivo**](#151-objetivo)
    - [**15.2 Perguntas**](#152-perguntas)
    - [**15.3 Ordem correta**](#153-ordem-correta)
  - [**16. Fontes de conhecimento**](#16-fontes-de-conhecimento)
    - [**16.1 Tipo**](#161-tipo)
    - [**16.2 Autoridade**](#162-autoridade)
    - [**16.3 Proveniência**](#163-proveniência)
    - [**16.4 Ciclo de vida**](#164-ciclo-de-vida)
  - [**17. Evidência e estado epistemológico**](#17-evidência-e-estado-epistemológico)
    - [**17.1 OBSERVADO**](#171-observado)
    - [**17.2 INFERIDO**](#172-inferido)
    - [**17.3 AMBÍGUO**](#173-ambíguo)
    - [**17.4 CONFLITANTE**](#174-conflitante)
    - [**17.5 VALIDADO**](#175-validado)
    - [**17.6 REJEITADO**](#176-rejeitado)
  - [**18. Estado técnico**](#18-estado-técnico)
  - [**19. Processo completo de descoberta**](#19-processo-completo-de-descoberta)
    - [**19.1 Etapa 1 — Inventário**](#191-etapa-1--inventário)
    - [**19.2 Etapa 2 — Leitura estrutural**](#192-etapa-2--leitura-estrutural)
    - [**19.3 Etapa 3 — Extração semântica**](#193-etapa-3--extração-semântica)
  - [**20. Atomização de regras**](#20-atomização-de-regras)
  - [**21. Reconciliação semântica**](#21-reconciliação-semântica)
  - [**22. Perguntas de competência**](#22-perguntas-de-competência)
  - [**23. Modelo canônico do domínio**](#23-modelo-canônico-do-domínio)
  - [**24. Metamodelo mínimo de rastreabilidade**](#24-metamodelo-mínimo-de-rastreabilidade)
  - [**25. Modelo conceitual**](#25-modelo-conceitual)
  - [**26. Modelo lógico**](#26-modelo-lógico)
  - [**27. Modelo físico**](#27-modelo-físico)
  - [**28. Artefatos derivados**](#28-artefatos-derivados)
  - [**29. Glossário**](#29-glossário)
  - [**30. Dicionário de dados**](#30-dicionário-de-dados)
  - [**31. Constraints**](#31-constraints)
  - [**32. Segurança e autorização**](#32-segurança-e-autorização)
  - [**33. Test-Driven Data Modeling**](#33-test-driven-data-modeling)
  - [**34. Validação adversarial**](#34-validação-adversarial)
  - [**35. Autoridade humana**](#35-autoridade-humana)
  - [**36. Escopo proibido**](#36-escopo-proibido)
  - [**37. Antiobjetivos**](#37-antiobjetivos)
  - [**38. Critérios para alta qualidade**](#38-critérios-para-alta-qualidade)
  - [**Semanticamente correta**](#semanticamente-correta)
  - [**Evidenciável**](#evidenciável)
  - [**Rastreável**](#rastreável)
  - [**Temporalmente correta**](#temporalmente-correta)
  - [**Proporcional**](#proporcional)
  - [**Normalizada adequadamente**](#normalizada-adequadamente)
  - [**Executável**](#executável)
  - [**Íntegra**](#íntegra)
  - [**Segura**](#segura)
  - [**Testável**](#testável)
  - [**Evolutiva**](#evolutiva)
  - [**Auditável**](#auditável)
  - [**Independente da confiança na IA**](#independente-da-confiança-na-ia)
  - [**Orientada à operação**](#orientada-à-operação)
  - [**39. Critérios de maturidade do modelo**](#39-critérios-de-maturidade-do-modelo)
  - [**40. Definição de pronto para implementação física**](#40-definição-de-pronto-para-implementação-física)
  - [**41. Cadeia profissional da tarefa**](#41-cadeia-profissional-da-tarefa)
  - [**42. Síntese final da modelagem**](#42-síntese-final-da-modelagem)

## **1. Denominação do domínio**

A denominação mais precisa para esta tarefa é:

> **Engenharia do Conhecimento e Modelagem Semântica Orientada por Evidências para Descoberta, Formalização e Implementação do Domínio Operacional do CEPRAEA-BEACH-PRO.**

Trata-se de um domínio composto por quatro dimensões:

### **1.1 Domínio científico e metodológico**

**Engenharia do Conhecimento e Representação do Conhecimento**
Responsável por transformar conhecimento existente em documentos, dados e práticas operacionais em conceitos, regras, relações e estruturas formais.

### **1.2 Domínio de aplicação**

**Gestão operacional do handebol de praia no CEPRAEA-BEACH-PRO**
É o domínio real que precisa ser descoberto e representado.

Inclui, conforme evidenciado pelas fontes:

- pessoas participantes;
- atletas;
- treinador;
- vínculos;
- treinamentos;
- disponibilidade;
- presença;
- convocações;
- competições;
- jogos;
- participação;
- resultados;
- documentos;
- regulamentos;
- demais conceitos identificados no acervo.

### **1.3 Domínio de implementação**

**Engenharia de Dados e Engenharia de Bancos de Dados**
Responsável por transformar o modelo validado em estruturas executáveis:

- modelos lógicos;
- schemas;
- PostgreSQL;
- Supabase;
- migrations;
- constraints;
- índices;
- views;
- RLS;
- testes.

### **1.4 Domínios transversais**

- governança de dados;
- qualidade;
- proveniência;
- segurança;
- temporalidade;
- auditoria;
- engenharia de requisitos;
- validação assistida por IA.

A governança não constitui o objetivo principal. Ela funciona como mecanismo transversal para preservar autoridade, proveniência, qualidade e controle das decisões, coerente com a distinção estabelecida no texto original.

***

## **2. Objeto real da tarefa**

O objeto desta tarefa não é simplesmente:

> criar um banco de dados para handebol de praia.

Também não é:

> converter planilhas do CEPRAEA para PostgreSQL.

O objeto real é:

> **descobrir, formalizar e manter um modelo canônico do domínio operacional do CEPRAEA-BEACH-PRO a partir das evidências existentes no acervo do CEPRAEA.**

O agente deve acessar e analisar:

- planilhas;
- documentos;
- formulários;
- regulamentos;
- súmulas;
- tabelas;
- relações nominais;
- calendários;
- registros históricos;
- arquivos operacionais;
- documentos administrativos pertinentes;
- sistemas ou exportações legadas;
- demais fontes autorizadas.

Essas fontes são utilizadas como **evidências sobre o domínio**.

O modelo não deve ser determinado diretamente pela estrutura física dessas fontes.

A transformação fundamental é:

```text
ACERVO REAL DO CEPRAEA
        ↓
FONTES E EVIDÊNCIAS
        ↓
CONHECIMENTO EXTRAÍDO
        ↓
RECONCILIAÇÃO SEMÂNTICA
        ↓
MODELO CANÔNICO DO DOMÍNIO
        ↓
MODELO LÓGICO
        ↓
IMPLEMENTAÇÃO
        ↓
ARTEFATOS EXECUTÁVEIS E DOCUMENTAIS
```

Essa cadeia desenvolve a transformação já prevista no texto original entre documentos, conceitos, modelo conceitual, modelo lógico, registros canônicos e PostgreSQL/Supabase.

***

## **3. Problema fundamental**

O problema central não é descobrir quais tabelas precisam ser criadas.

Antes disso, o agente precisa determinar:

- o que existe no domínio;
- o significado de cada informação;
- quais objetos possuem identidade;
- quando duas ocorrências representam a mesma coisa;
- quais termos são sinônimos;
- quais termos iguais possuem significados diferentes;
- em qual contexto determinado significado é válido;
- quais relações existem;
- quais cardinalidades são verdadeiras;
- quais regras precisam permanecer verdadeiras;
- quais exceções existem;
- quais informações são fatos;
- quais representam intenção;
- quais representam previsão;
- quais representam decisão;
- quais representam projeções;
- quais informações possuem vigência;
- como o histórico é preservado;
- quais fontes possuem autoridade;
- quais mudanças precisam ser atômicas;
- quem pode consultar ou alterar cada informação.

O próprio texto original coloca identidade, contexto, validade, temporalidade, autoridade e relações entre as questões fundamentais da modelagem.

***

## **4. Missão do agente**

O agente tem como missão:

> **analisar sistematicamente o acervo real do CEPRAEA, extrair e reconciliar evidências sobre o funcionamento do CEPRAEA-BEACH-PRO, descobrir sua estrutura semântica, formalizar o conhecimento validado em um modelo canônico e utilizar esse modelo como fundamento para a produção posterior dos artefatos de dados e implementação.**

O agente atua como:

- agente de descoberta do domínio;
- engenheiro do conhecimento;
- modelador semântico;
- auxiliar de modelagem de dados;
- auxiliar de engenharia de requisitos;
- auxiliar de qualidade;
- auxiliar de implementação;
- gerador de evidências para decisão humana.

O agente **não é autoridade final sobre o significado do domínio**.

Quando uma conclusão material não puder ser sustentada pelas fontes disponíveis, deverá:

1. registrar a evidência existente;
2. identificar a lacuna;
3. formular a interpretação candidata;
4. indicar o grau de incerteza;
5. solicitar decisão humana quando necessário.

A IA pode gerar, sugerir, comparar e testar, mas não deve transformar sua própria plausibilidade em evidência ou aprovação, conforme o princípio de validação independente definido no texto original.

***

## **5. Princípios fundamentais**

### **5.1 Fonte não é modelo**

```text
arquivo ≠ entidade
pasta ≠ Bounded Context
planilha ≠ agregado
aba ≠ entidade
coluna ≠ atributo canônico
linha ≠ necessariamente entidade
valor textual ≠ necessariamente enum
schema legado ≠ modelo canônico
```

Uma estrutura existente pode refletir:

- conveniência;
- limitação de ferramenta;
- processo manual;
- duplicação;
- histórico;
- erro;
- decisão antiga;
- necessidade já extinta.

O agente deve interpretar a estrutura, não reproduzi-la automaticamente.

***

### **5.2 Significado precede implementação**

A ordem correta é:

```text
significado
→ regra
→ modelo
→ implementação
```

e não:

```text
coluna encontrada
→ coluna PostgreSQL
→ tentativa posterior de explicar seu significado
```

***

### **5.3 Evidência precede inferência**

Toda afirmação relevante deve poder ser classificada como:

- observada;
- inferida;
- ambígua;
- conflitante;
- validada;
- rejeitada.

***

### **5.4 Fato não é intenção**

Devem permanecer semanticamente distintos, quando aplicável:

- disponibilidade;
- convocação;
- presença;
- participação;
- programação;
- realização;
- resultado oficial.

O texto original já estabelece explicitamente que disponibilidade não é presença, convocação não é participação e programação não é resultado realizado.

***

### **5.5 Estado atual não substitui histórico**

Quando o domínio exigir preservação temporal:

```text
novo estado ≠ destruição automática do estado anterior
```

O padrão correto poderá envolver:

- effective dating;
- append-only;
- eventos;
- snapshots;
- versões;
- projeções reconstruíveis.

***

### **5.6 Não generalizar sem necessidade operacional**

O agente não deve criar:

- entidades hipotéticas;
- papéis inexistentes;
- fluxos futuros não demonstrados;
- estruturas de múltiplos papéis sem necessidade;
- abstrações técnicas sem consumidor;
- enums baseados apenas em valores acidentais.

***

## **6. Escopo do domínio operacional**

Pertence ao escopo tudo aquilo que precisa ser compreendido para modelar corretamente os dados operacionais do CEPRAEA-BEACH-PRO.

Entre os conceitos já reconhecidos no material original encontram-se:

- atleta;
- equipe;
- vínculo;
- sessão de treinamento;
- disponibilidade;
- presença;
- competição;
- jogo;
- segmentos do jogo;
- resultados;
- eventos;
- documentação oficial.

Entretanto, essa lista não constitui um modelo fechado.

Novos conceitos podem ser adicionados somente quando encontrados ou exigidos pelas evidências do acervo.

***

## **7. Restrições operacionais atualmente validadas**

No estado atual conhecido do CEPRAEA-BEACH-PRO:

- existem **19 atletas**;
- existe **1 treinador**;
- existem somente dois papéis operacionais conhecidos:

  - `ATLETA`;
  - `TREINADOR`;
- cada pessoa participante do sistema exerce somente um papel operacional;
- atletas não possuem dupla função;
- uma atleta exerce exclusivamente o papel `ATLETA`;
- o treinador exerce o papel `TREINADOR`;
- usuário autenticado não implica papel `ATLETA`.

A modelagem não deverá introduzir, sem nova evidência:

- administrador como papel operacional;
- árbitro como papel de usuário;
- organizador como papel de usuário;
- múltiplos papéis simultâneos;
- tabelas N:N de papéis apenas para suportar cenários hipotéticos.

A possibilidade de alteração histórica de papel também não deve ser assumida nem proibida até que o domínio a estabeleça.

***

## **8. Objetos semânticos fundamentais**

O agente deverá classificar as estruturas encontradas, quando aplicável, em categorias semânticas.

### **8.1 Entidade**

Objeto cuja identidade precisa permanecer reconhecível ao longo do tempo.

Exemplos candidatos:

- Pessoa;
- Equipe;
- Competição;
- Jogo;
- Sessão de treinamento.

A classificação definitiva depende das evidências.

***

### **8.2 Value Object**

Objeto definido por seus valores e sem identidade independente relevante.

Exemplos possíveis:

- intervalo de datas;
- placar;
- período;
- endereço;
- posição temporal.

***

### **8.3 Papel**

Função contextual exercida por uma pessoa ou entidade.

No CEPRAEA-BEACH-PRO atualmente:

```text
PapelOperacional =
    ATLETA
    | TREINADOR
```

***

### **8.4 Associação**

Relação que possui significado ou atributos próprios.

Exemplos candidatos:

- vínculo de uma pessoa à equipe;
- inscrição;
- participação em competição;
- participação em jogo.

***

### **8.5 Evento**

Representa algo que ocorreu.

Exemplos:

- resposta de disponibilidade;
- registro de presença;
- alteração administrativa;
- evento de jogo;
- correção de resultado.

***

### **8.6 Estado**

Representa situação de um objeto em determinado momento de seu ciclo de vida.

Estados não devem ser criados apenas por conveniência técnica.

***

### **8.7 Regra**

Representa uma condição, obrigação, proibição, cálculo, autorização, cardinalidade ou restrição do domínio.

***

### **8.8 Fato histórico**

Algo realizado e que precisa permanecer preservado.

***

### **8.9 Projeção**

Representação reconstruível ou otimizada do estado atual.

A distinção entre fato histórico, projeção e indicador derivado já é reconhecida no texto original.

***

## **9. Seis objetos obrigatórios de descoberta e formalização**

O agente deverá tratar explicitamente os seguintes elementos como **objetos obrigatórios de investigação do domínio**:

1. Bounded Contexts;
2. identidades definitivas;
3. agregados;
4. invariantes;
5. ciclos de vida;
6. fronteiras transacionais.

Eles não devem ser estabelecidos por convenção antes da leitura das fontes.

***

## **10. Bounded Contexts**

### **10.1 Objetivo**

Identificar regiões semânticas nas quais:

- conceitos possuam significado consistente;
- regras sejam coerentes;
- ciclos de vida estejam relacionados;
- responsabilidades sobre dados sejam claras;
- uma linguagem própria possa ser definida.

***

### **10.2 Descoberta**

O agente deverá procurar:

- conjuntos de conceitos frequentemente utilizados juntos;
- regras que se aplicam apenas a determinadas atividades;
- termos que mudam de significado conforme o contexto;
- processos com ciclos de vida independentes;
- diferentes responsáveis ou autoridades;
- informações que pertencem claramente a outro contexto.

***

### **10.3 Candidatos iniciais**

Sem tratá-los como definitivamente validados, o acervo poderá revelar contextos como:

```text
Identidade e Participantes
Equipe e Vínculos
Treinamentos
Disponibilidade e Convocação
Competições
Jogos e Resultados
Fontes Normativas e Proveniência
Identidade Digital e Autorização
```

Esses nomes são **hipóteses de organização**.

O agente deverá confirmá-los, subdividi-los, agrupá-los ou rejeitá-los conforme as evidências.

***

### **10.4 Formalização**

Cada Bounded Context deverá registrar:

- ID;
- nome canônico;
- objetivo;
- linguagem;
- conceitos internos;
- conceitos externos;
- regras;
- invariantes;
- eventos;
- dados sob responsabilidade;
- integrações;
- fontes;
- ambiguidades;
- estado de validação.

***

## **11. Identidades definitivas**

### **11.1 Objetivo**

Determinar quais objetos possuem identidade própria e como diferentes representações existentes no acervo são reconciliadas.

Exemplo:

```text
Maria da Silva
Maria Silva
M. da Silva
```

não constitui evidência suficiente, isoladamente, para afirmar:

```text
mesma pessoa
```

nem:

```text
três pessoas distintas
```

***

### **11.2 Para cada identidade, descobrir**

- critérios de igualdade;
- atributos identificadores;
- identificadores naturais;
- identificadores externos;
- aliases;
- variações de nome;
- duplicidades;
- período de existência;
- regras de unicidade;
- possíveis merges;
- possíveis splits históricos.

***

### **11.3 Identidade humana**

Deve ser preservada a distinção entre:

```text
Pessoa
      ↓
identidade humana

Usuário autenticado
      ↓
identidade técnica de acesso

Papel operacional
      ↓
ATLETA | TREINADOR
```

Essas estruturas podem se relacionar 1:1 no cenário atual sem serem semanticamente equivalentes.

***

## **12. Agregados**

### **11.1 Objetivo**

Descobrir quais objetos precisam formar unidades de consistência.

Um agregado representa uma fronteira dentro da qual determinadas invariantes devem permanecer válidas.

***

### **11.2 Um agregado não é automaticamente**

- tabela;
- planilha;
- formulário;
- tela;
- arquivo;
- Bounded Context.

***

### **11.3 Critérios**

O agente deverá investigar:

- identidade externa do conjunto;
- dependência de existência;
- regras que precisam ser verificadas conjuntamente;
- alterações que ocorrem juntas;
- operações válidas;
- componentes internos;
- referências externas;
- eventos produzidos.

***

### **11.4 Formalização**

Para cada agregado:

- Aggregate Root;
- entidades internas;
- Value Objects;
- invariantes;
- operações;
- eventos;
- ciclo de vida;
- referências externas;
- justificativa;
- fontes;
- estado de validação.

Os agregados somente devem ser definidos após evidência suficiente sobre regras e comportamento.

***

## **13. Invariantes**

### **11.1 Definição**

Invariante é uma condição que deve permanecer verdadeira em todo estado válido relevante do domínio.

***

### **11.2 Invariantes atualmente conhecidas ou candidatas**

Já podem ser registradas, ao menos, as seguintes:

```text
PapelOperacional ∈ {ATLETA, TREINADOR}
```

```text
Cada participante operacional possui exatamente um papel.
```

```text
Uma atleta possui exclusivamente o papel ATLETA.
```

```text
Disponibilidade não cria presença.
```

```text
Convocação não equivale a participação efetiva.
```

```text
Programação de jogo não equivale a jogo realizado.
```

```text
Cadastro de pessoa/atleta não equivale automaticamente a vínculo esportivo.
```

As últimas distinções estão explicitamente presentes no documento-base.

***

### **11.3 Registro formal de invariante**

Cada invariante deverá conter:

- `invariant_id`;
- nome;
- declaração;
- contexto;
- conceitos envolvidos;
- condição;
- consequência;
- exceções;
- vigência;
- fontes;
- evidências;
- autoridade;
- criticidade;
- implementação candidata;
- teste positivo;
- teste negativo;
- estado de validação.

***

## **14. Ciclos de vida**

Cada conceito material deverá ser investigado quanto a seu comportamento temporal.

O agente deverá responder:

- como nasce;
- quem o cria;
- qual estado inicial;
- quais estados são possíveis;
- quais eventos causam transições;
- quais transições são proibidas;
- quando se torna vigente;
- quando deixa de ser vigente;
- se pode ser cancelado;
- se pode ser corrigido;
- se pode ser reaberto;
- se uma correção altera passado ou cria nova versão;
- qual histórico precisa permanecer preservado.

***

### **14.1 Padrões temporais candidatos**

O texto original já prevê:

- effective dating;
- append-only;
- event log;
- snapshot;
- projeção atual.

O padrão deverá ser escolhido por conceito, conforme sua semântica.

Não se deve implantar event sourcing em todo o sistema apenas porque alguns fatos são naturalmente eventuais.

***

## **15. Fronteiras transacionais**

### **15.1 Objetivo**

Determinar quais mudanças precisam ocorrer atomicamente para evitar estados inválidos.

A decisão deve ser derivada de:

```text
agregados
+
invariantes
+
operações
+
consistência requerida
```

***

### **15.2 Perguntas**

Para cada operação material:

- quais objetos mudam;
- quais alterações precisam ocorrer juntas;
- que estado intermediário seria inválido;
- quais invariantes precisam ser imediatamente preservadas;
- existe concorrência;
- mais de um agregado está envolvido;
- é necessária atomicidade;
- consistência eventual seria aceitável;
- um evento seria suficiente para coordenação.

***

### **15.3 Ordem correta**

```text
semântica
→ identidade
→ relação
→ invariante
→ ciclo de vida
→ agregado
→ operação
→ fronteira transacional
→ mecanismo PostgreSQL
```

Agregados e limites transacionais já aparecem entre as atividades de modelagem lógica no texto-base.

***

## **16. Fontes de conhecimento**

As fontes deverão ser classificadas em dimensões independentes.

### **16.1 Tipo**

```text
NORMATIVA
OPERACIONAL
CIENTÍFICA
ADMINISTRATIVA
HISTÓRICA
TÉCNICA
```

***

### **16.2 Autoridade**

```text
OFICIAL
PRIMÁRIA
AUXILIAR
INDETERMINADA
```

***

### **16.3 Proveniência**

```text
ORIGINAL
DERIVADA
```

***

### **16.4 Ciclo de vida**

```text
VIGENTE
SUBSTITUÍDA
OBSOLETA
INDETERMINADA
```

Essa separação corrige a mistura existente entre autoridade, proveniência e temporalidade na taxonomia original das fontes. O documento-base atualmente reúne categorias como autoritativa, operacional primária, derivada, suporte e histórica em uma única classificação.

***

## **17. Evidência e estado epistemológico**

Todo conhecimento extraído deve possuir um estado epistemológico.

Valores mínimos:

```text
OBSERVADO
INFERIDO
AMBÍGUO
CONFLITANTE
VALIDADO
REJEITADO
```

### **17.1 OBSERVADO**

Existe suporte direto na fonte.

### **17.2 INFERIDO**

Conclusão derivada de evidências, mas não declarada diretamente.

### **17.3 AMBÍGUO**

Mais de uma interpretação permanece plausível.

### **17.4 CONFLITANTE**

Fontes apresentam afirmações incompatíveis.

### **17.5 VALIDADO**

A interpretação foi confirmada pela autoridade adequada.

### **17.6 REJEITADO**

A hipótese foi avaliada e considerada incorreta.

Esse estado epistemológico deve ser separado do estado técnico de implementação.

***

## **18. Estado técnico**

O conhecimento validado pode possuir estado técnico independente:

```text
NÃO_MODELADO
MODELADO
IMPLEMENTADO
TESTADO
ATIVO
SUBSTITUÍDO
```

Portanto:

```text
VALIDADO ≠ IMPLEMENTADO
```

e:

```text
TESTADO ≠ SEMANTICAMENTE VALIDADO
```

***

## **19. Processo completo de descoberta**

### **19.1 Etapa 1 — Inventário**

Identificar todas as fontes disponíveis.

Registrar:

- título;
- arquivo;
- formato;
- origem;
- responsável;
- período;
- finalidade;
- tipo;
- autoridade;
- proveniência;
- vigência.

***

### **19.2 Etapa 2 — Leitura estrutural**

Identificar:

- planilhas;
- abas;
- colunas;
- documentos;
- seções;
- cabeçalhos;
- campos;
- valores;
- repetições;
- estruturas anômalas.

Essa etapa descreve a fonte, não o domínio.

***

### **19.3 Etapa 3 — Extração semântica**

Extrair candidatos a:

- conceitos;
- termos;
- sinônimos;
- definições;
- entidades;
- Value Objects;
- identidades;
- papéis;
- associações;
- relações;
- cardinalidades;
- regras;
- exceções;
- estados;
- eventos;
- datas;
- operações;
- permissões;
- indicadores.

A extração deve preferencialmente utilizar schemas estruturados, conforme a orientação do documento-base.

***

## **20. Atomização de regras**

Cada regra encontrada deve ser dividida em unidades independentes.

Separar:

- definição;
- obrigação;
- proibição;
- permissão;
- condição;
- exceção;
- cardinalidade;
- unicidade;
- regra temporal;
- cálculo;
- autorização;
- transição de estado.

O documento-base já define a atomização normativa como mecanismo para evitar que uma única entrada combine comportamentos diferentes.

***

## **21. Reconciliação semântica**

Depois da extração, o agente deverá detectar:

- sinônimos;
- aliases;
- homônimos;
- conceitos duplicados;
- valores equivalentes;
- conflitos;
- diferentes representações da mesma identidade;
- termos obsoletos;
- estruturas derivadas;
- divergências temporais.

Nenhuma unificação material deve ocorrer apenas por similaridade textual.

***

## **22. Perguntas de competência**

O agente deve formular perguntas que o modelo precisará responder.

Exemplos já apropriados:

- Qual era o vínculo de uma atleta em determinada data?
- Qual foi a última resposta de disponibilidade?
- Quais versões anteriores existiram?
- Quem registrou a presença?
- Qual documento sustenta determinado resultado?
- Qual regulamento estava vigente?
- Uma atleta pode consultar dados de outra atleta?

O documento-base já estabelece essas perguntas como mecanismo para impedir a criação de entidades sem finalidade.

Devem ser acrescentadas perguntas específicas da tarefa de descoberta, como:

- De quais fontes surge este conceito?
- Há mais de uma definição?
- O termo possui significados diferentes?
- Esta estrutura possui identidade?
- O histórico é necessário?
- Há uma invariante associada?
- O objeto pertence a qual contexto?
- A alteração precisa ocorrer atomicamente?
- O dado é factual ou derivado?

***

## **23. Modelo canônico do domínio**

O Modelo Canônico do Domínio constitui o principal produto intelectual desta tarefa.

Ele deve conter, conforme aplicável:

```text
Bounded Contexts
identidades
vocabulário canônico
entidades
Value Objects
papéis
associações
relações
cardinalidades
agregados
regras
invariantes
eventos
estados
ciclos de vida
temporalidade
operações
fronteiras transacionais
autoridade
proveniência
permissões
questões de competência
```

O modelo deve ser independente da tecnologia de persistência.

***

## **24. Metamodelo mínimo de rastreabilidade**

Cada elemento material do modelo deverá poder apontar para sua origem.

A cadeia mínima é:

```text
Fonte
  ↓
Fragmento / Evidência
  ↓
Conceito
  ↓
Regra
  ↓
Elemento do Modelo
  ↓
Implementação
  ↓
Teste
```

E deverá ser possível percorrê-la no sentido inverso:

```text
Teste
  ↓
Constraint / Policy / Implementação
  ↓
Elemento do Modelo
  ↓
Regra
  ↓
Conceito
  ↓
Evidência
  ↓
Fonte
```

Essa rastreabilidade bidirecional já é definida explicitamente no documento-base.

***

## **25. Modelo conceitual**

O modelo conceitual responde:

```text
O que existe?
O que significa?
Como se relaciona?
Que regras possui?
Como muda?
```

Não deverá conter decisões físicas prematuras como:

- tipo PostgreSQL;
- nome definitivo de coluna;
- índice;
- trigger;
- política RLS.

***

## **26. Modelo lógico**

Depois da estabilização conceitual, deverão ser definidos:

- relações;
- atributos;
- PKs;
- FKs;
- cardinalidades;
- domínios de valores;
- histórico;
- modelo temporal;
- decomposição N:N;
- projeções;
- normalização;
- agregados;
- limites transacionais.

***

## **27. Modelo físico**

Somente depois:

- tipos PostgreSQL;
- tabelas;
- constraints;
- índices;
- functions;
- triggers;
- views;
- migrations;
- grants;
- RLS;
- seeds;
- testes.

A separação entre modelo conceitual, lógico e físico é expressamente defendida no documento original para evitar que limitações tecnológicas determinem prematuramente a semântica.

***

## **28. Artefatos derivados**

O Modelo Canônico funciona como fonte para os artefatos.

```text
MODELO CANÔNICO
│
├── Glossário
├── Catálogo de conceitos
├── Catálogo de regras
├── Catálogo de invariantes
├── Dicionário de dados
├── Modelo conceitual
├── Modelo lógico
├── ERD
├── JSON Schema
├── Migrations
├── PostgreSQL/Supabase
├── Constraints
├── Índices
├── Views
├── RLS
├── Testes
└── Documentação
```

***

## **29. Glossário**

O glossário representa o significado do domínio.

Para cada conceito:

- termo preferencial;
- nome canônico;
- definição;
- sinônimos;
- contexto;
- inclusões;
- exclusões;
- diferenças para conceitos semelhantes;
- temporalidade;
- fonte;
- estado epistemológico.

O glossário pode começar a ser produzido durante a descoberta.

***

## **30. Dicionário de dados**

O dicionário de dados descreve a representação estruturada dos dados.

Deve ser derivado de estruturas já suficientemente estabilizadas.

Pode conter:

- tabela;
- coluna;
- tipo;
- nulabilidade;
- chave;
- domínio;
- constraint;
- definição semântica;
- conceito canônico associado;
- fonte da definição.

O dicionário não deve ser utilizado como substituto do glossário.

***

## **31. Constraints**

Regras essenciais devem ser garantidas no nível mais forte tecnicamente apropriado.

Candidatos:

- `NOT NULL`;
- `CHECK`;
- `UNIQUE`;
- `FOREIGN KEY`;
- exclusion constraints;
- índices únicos parciais;
- constraint triggers.

O documento-base já estabelece constraints como primeira linha de integridade.

***

## **32. Segurança e autorização**

Autenticação e entidade esportiva devem permanecer conceitualmente separadas.

A autorização deverá ser derivada de:

- papel operacional;
- propriedade;
- contexto;
- vínculo;
- estado;
- sensibilidade;
- operação.

No CEPRAEA-BEACH-PRO, o modelo atual de papéis deve permanecer restrito a:

```text
ATLETA
TREINADOR
```

até que nova necessidade real seja comprovada.

RLS deve ser tratada como regra executável e testável, não como convenção da interface.

***

## **33. Test-Driven Data Modeling**

Toda regra material deve possuir verificação associada.

Exemplo já estabelecido no domínio:

```text
Regra:
disponibilidade não cria presença.
```

Teste:

```text
registrar disponibilidade
→ disponibilidade é preservada

consultar presença
→ nenhuma presença foi criada
```

O documento-base utiliza exatamente esse princípio como exemplo de Test-Driven Data Modeling.

***

## **34. Validação adversarial**

Antes de validar uma hipótese importante, o agente deverá procurar:

- contraexemplos;
- registros incompatíveis;
- documentos divergentes;
- exceções;
- períodos históricos diferentes;
- significado alternativo;
- ausência de evidência suficiente.

O objetivo não é apenas confirmar a primeira interpretação plausível.

***

## **35. Autoridade humana**

A validação humana é obrigatória quando houver decisão material sem evidência conclusiva.

Exemplos:

- definição ambígua;
- identidade duvidosa;
- exceção operacional;
- conflito normativo;
- regra local;
- mudança semântica;
- eliminação de dados;
- mudança histórica;
- autorização mais permissiva.

***

## **36. Escopo proibido**

Não pertence à missão principal:

- prescrição de treinamento;
- periodização esportiva;
- preparação física;
- diagnóstico;
- conduta médica;
- estratégia tática;
- julgamento disciplinar;
- interpretação jurídica definitiva;
- design de interface;
- desenvolvimento completo do frontend;
- previsão de resultados;
- scouting automatizado;
- machine learning preditivo.

Esses temas somente entram quando for necessário **modelar dados que os representam**.

Essa separação segue o escopo proibido definido no documento-base para treinamento, saúde, arbitragem, aplicação completa e ciência de dados.

***

## **37. Antiobjetivos**

O agente não deverá:

- criar documentação redundante;
- replicar dados sem finalidade;
- produzir matrizes sem consumidor;
- criar abstrações para futuros hipotéticos;
- normalizar mecanicamente arquivos;
- transformar todo texto em enum;
- transformar toda planilha em tabela;
- transformar toda coluna em atributo;
- transformar toda diferença textual em conceito distinto;
- transformar toda semelhança textual em identidade compartilhada;
- ocultar conflitos;
- eliminar histórico sem decisão explícita;
- inventar regras para completar lacunas;
- afirmar que algo foi validado sem evidência.

***

## **38. Critérios para alta qualidade**

Uma modelagem desta tarefa será considerada de alto nível quando for:

## **Semanticamente correta**

Preserva os significados do domínio.

## **Evidenciável**

As conclusões materiais possuem suporte identificável.

## **Rastreável**

É possível percorrer fonte → implementação e implementação → fonte.

## **Temporalmente correta**

Vigência e histórico são preservados quando necessários.

## **Proporcional**

Não cria complexidade sem necessidade real.

## **Normalizada adequadamente**

Evita duplicação sem destruir significado.

## **Executável**

Pode gerar structures válidas de implementação.

## **Íntegra**

Invariantes essenciais são protegidas.

## **Segura**

Autorização é aplicada no nível adequado.

## **Testável**

Regras possuem evidência executável.

## **Evolutiva**

Mudanças futuras podem ser incorporadas sem reconstrução destrutiva indevida.

## **Auditável**

É possível explicar origem e transformação.

## **Independente da confiança na IA**

A correção não depende da declaração do agente.

## **Orientada à operação**

Cada elemento possui finalidade real.

Esses princípios ampliam os 14 critérios finais já apresentados no documento original.

***

## **39. Critérios de maturidade do modelo**

Uma área do domínio está suficientemente madura para implementação quando:

1. os conceitos materiais estão definidos;
2. identidades relevantes estão resolvidas;
3. aliases e sinônimos estão reconciliados;
4. relações possuem significado;
5. cardinalidades relevantes são conhecidas;
6. invariantes materiais foram identificadas;
7. ciclos de vida estão formalizados quando necessários;
8. o Bounded Context está estabelecido ou sua ausência está justificada;
9. agregados relevantes foram determinados;
10. fronteiras transacionais necessárias estão justificadas;
11. regras materiais possuem evidência;
12. conflitos estão resolvidos ou explicitamente pendentes;
13. decisões possuem estado epistemológico;
14. histórico está corretamente tratado;
15. questões de competência podem ser respondidas;
16. testes podem ser derivados.

***

## **40. Definição de pronto para implementação física**

Nenhuma estrutura deverá ser considerada pronta para implementação apenas porque:

- existe uma planilha correspondente;
- um schema SQL pode ser escrito;
- o agente conseguiu produzir JSON válido;
- a estrutura parece tecnicamente elegante.

A implementação física estará pronta quando for possível responder:

```text
O que representa?
Por que existe?
Qual é sua identidade?
Em qual contexto é válido?
Quais regras protege?
Quais relações possui?
Como muda ao longo do tempo?
Qual histórico deve preservar?
A qual agregado pertence?
Qual operação o modifica?
Qual consistência precisa garantir?
Qual fonte sustenta a decisão?
Como será testado?
```

***

## **41. Cadeia profissional da tarefa**

```text
ACERVO DO CEPRAEA
        ↓
EVIDÊNCIAS
        ↓
ENGENHARIA DO CONHECIMENTO
        ↓
MODELO SEMÂNTICO
        ↓
MODELO CANÔNICO
        ↓
MODELO LÓGICO
        ↓
ENGENHARIA DE BANCO DE DADOS
        ↓
IMPLEMENTAÇÃO
        ↓
TESTES
        ↓
OPERAÇÃO SEGURA
```

O especialista do domínio determina ou valida o significado.

O agente extrai, estrutura, compara e formaliza.

O modelador transforma o conhecimento em estruturas coerentes.

A implementação transforma essas estruturas em mecanismos executáveis.

Os testes demonstram que as regras foram preservadas.

***

## **42. Síntese final da modelagem**

O domínio desta tarefa pode ser formalmente descrito como:

> **Disciplina de descoberta orientada por evidências que transforma o acervo documental, normativo e operacional do CEPRAEA em um modelo canônico do domínio CEPRAEA-BEACH-PRO, por meio da identificação, reconciliação, validação e formalização de conceitos, identidades, relações, regras, estados, eventos, temporalidade, Bounded Contexts, agregados, invariantes, ciclos de vida e fronteiras transacionais, preservando autoridade, proveniência e histórico, para permitir a posterior geração controlada de glossários, dicionários de dados, modelos conceituais e lógicos, schemas, banco PostgreSQL/Supabase, constraints, políticas de acesso e testes.**

A relação fundamental é:

```text
ACERVO
    não é
MODELO

ACERVO
    fornece
EVIDÊNCIAS

EVIDÊNCIAS
    são
INTERPRETADAS + RECONCILIADAS + VALIDADAS

CONHECIMENTO VALIDADO
    constitui
MODELO CANÔNICO

MODELO CANÔNICO
    governa
ARTEFATOS

ARTEFATOS
    implementam
O DOMÍNIO
```

Consequentemente:

> **o objetivo do agente não é reproduzir os dados existentes, mas descobrir e formalizar o sistema de significados, identidades, regras e comportamentos que explica corretamente esses dados e permite transformá-los em estruturas canônicas, históricas, seguras, verificáveis e auditáveis.**

Leia [Modelagem Agente](/home/agent/.claude/plans/modelagem_pelo_agente.md)
