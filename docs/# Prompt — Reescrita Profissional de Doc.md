### 1. Texto reescrito

Classificação do conteúdo: **Guia de procedimento / How-to**, com elementos de **referência técnica**.
Público predominante inferido pelo conteúdo: pessoas responsáveis por preparar prompts para revisão e reescrita de documentação técnica de software.

# Preenchimento dos Campos do Prompt

## 1. Objetivo

Este guia descreve como preencher os campos de contexto utilizados pelo prompt de reescrita profissional de documentação de software.

O preenchimento desses campos fornece à IA informações sobre:

* o sistema ou projeto documentado;
* a finalidade da documentação;
* o público-alvo;
* o nível técnico esperado;
* a terminologia oficial;
* o formato de publicação;
* o conteúdo original que deverá ser analisado e reescrito.

O objetivo é fornecer contexto suficiente para que a reescrita preserve o significado técnico do texto original e utilize estrutura, terminologia e nível de detalhamento compatíveis com sua finalidade.

Não é necessário melhorar previamente o texto original antes de fornecê-lo. Ambiguidades, inconsistências e lacunas existentes devem permanecer disponíveis para análise.

---

## 2. Referência rápida

| Campo                            | Informação a fornecer                                                                                                                                                 | Exemplo                                                                                                 |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Sistema/projeto**              | Nome do software, módulo, serviço ou projeto ao qual o texto pertence. Pode incluir uma descrição curta quando o nome não for suficiente para estabelecer o contexto. | `Portal de Gestão de Contratos — módulo de aprovação`                                                   |
| **Tipo de documentação**         | Natureza e finalidade do documento. Essa informação orienta sua estrutura, linguagem e nível de detalhamento.                                                         | `Requisitos funcionais`, `Documentação de API`, `Runbook`, `Arquitetura`, `Tutorial`, `ADR`             |
| **Público-alvo**                 | Pessoas ou funções que utilizarão ou consultarão o documento. Deve ser especificado com a maior precisão possível.                                                    | `Desenvolvedores backend`, `Equipe de suporte N2`, `Usuários administrativos`, `Arquitetos de software` |
| **Nível técnico esperado**       | Nível de conhecimento técnico que pode ser presumido do leitor.                                                                                                       | `Iniciante`, `Intermediário`, `Avançado` ou `Misto`                                                     |
| **Terminologia obrigatória**     | Termos oficiais do projeto que DEVEM ser preservados conforme definidos, evitando substituições inadequadas por sinônimos.                                            | `Tenant = Organização; Cliente = empresa contratante; Usuário = pessoa que acessa o sistema`            |
| **Formato desejado**             | Sintaxe, plataforma ou local em que a documentação será publicada. Essa informação influencia títulos, tabelas, listas e blocos de código.                            | `Markdown para GitHub`, `Confluence`, `GitLab Wiki`, `Markdown`, `texto simples`                        |
| **Texto que deve ser reescrito** | Conteúdo original que será submetido à análise e à reescrita.                                                                                                         | Texto integral a ser revisado.                                                                          |

---

## 3. Sistema/projeto

### Objetivo do campo

Informe o sistema, aplicação, módulo, serviço ou projeto ao qual o conteúdo pertence.

A identificação deve fornecer contexto suficiente para interpretar corretamente conceitos, responsabilidades e terminologia presentes no texto.

### Evite

> Sistema financeiro

### Prefira

> Sistema Financeiro Corporativo — módulo de Contas a Pagar

ou:

> API de Pagamentos — microsserviço responsável pela criação, autorização e cancelamento de transações.

Não é necessário descrever toda a arquitetura do sistema. O campo deve apenas estabelecer o contexto necessário para interpretar o documento.

---

## 4. Tipo de documentação

### Objetivo do campo

Informe a finalidade principal da documentação.

Esse campo influencia diretamente:

* a estrutura do documento;
* a linguagem utilizada;
* o grau de detalhamento;
* a forma de apresentação de requisitos;
* a organização de procedimentos;
* a presença de informações de referência.

Por exemplo, se o campo for preenchido como:

> **Tipo de documentação:** Requisitos funcionais

a reescrita deverá privilegiar declarações claras e verificáveis, como:

> O sistema **DEVE** permitir que um administrador inative um usuário.

Se o campo for preenchido como:

> **Tipo de documentação:** Tutorial

uma estrutura procedural poderá ser utilizada:

1. Acesse **Configurações**.
2. Selecione **Usuários**.
3. Selecione o usuário.
4. Clique em **Inativar**.

### Tipos de documentação frequentemente utilizados

* requisitos funcionais;
* requisitos não funcionais;
* regras de negócio;
* especificação técnica;
* arquitetura de software;
* ADR;
* documentação de API;
* tutorial;
* guia de uso;
* procedimento operacional;
* runbook;
* troubleshooting;
* documentação de implantação;
* documentação de desenvolvimento;
* documentação de segurança;
* referência técnica.

Quando o documento possuir mais de uma finalidade, informe explicitamente a combinação.

Exemplo:

```text
Especificação técnica e requisitos de integração
```

Evite combinar tipos de documentação sem necessidade quando eles possuírem objetivos distintos.

---

## 5. Público-alvo

### Objetivo do campo

Informe quem deverá compreender, consultar ou executar ações com base na documentação.

A descrição deve ser específica sempre que o público puder ser determinado.

### Evite

> Equipe

### Prefira

> Desenvolvedores backend responsáveis pela integração com a API.

ou:

> Analistas de suporte N1 e N2 responsáveis pelo diagnóstico inicial de falhas.

ou:

> Usuários administrativos sem conhecimento de programação.

O público-alvo influencia o vocabulário e o nível de abstração utilizado.

Por exemplo, para desenvolvedores:

> O endpoint retorna HTTP 409 quando já existe um registro para o identificador informado.

Para usuários finais, a mesma condição poderá ser apresentada como:

> Se já existir um cadastro com o mesmo identificador, o sistema não permitirá criar um novo registro.

A formulação pode ser adaptada ao público, desde que o comportamento técnico original seja preservado.

---

## 6. Nível técnico esperado

### Objetivo do campo

Informe quanto conhecimento técnico pode ser presumido do leitor.

### Iniciante

Conceitos técnicos importantes devem ser explicados quando necessários à compreensão.

Exemplo:

> PostgreSQL é o banco de dados utilizado pela aplicação.

### Intermediário

Conhecimentos comuns da área podem ser presumidos.

Exemplo:

> Execute as migrations antes de iniciar a aplicação.

### Avançado

Terminologia especializada pode ser utilizada sem explicações introdutórias de conceitos básicos.

Exemplo:

> A operação utiliza isolamento `READ COMMITTED` e locking pessimista durante a atualização.

### Misto

Utilize quando o documento for destinado a leitores com níveis técnicos diferentes.

Nesse caso, o conteúdo deve permanecer compreensível sem simplificar excessivamente os conceitos técnicos.

---

## 7. Terminologia obrigatória

### Objetivo do campo

Registre os termos oficiais do domínio ou do projeto que devem permanecer consistentes durante a reescrita.

Esse campo funciona como um glossário mínimo para impedir substituições que possam alterar o significado técnico.

Exemplo:

```text
Tenant = Organização cliente do sistema
Conta = unidade financeira pertencente a uma Organização
Usuário = pessoa física autenticada
Administrador = usuário com perfil ADMIN
Pedido = entidade Order no domínio
```

Essa definição evita, por exemplo, que o termo:

> Organização

seja substituído automaticamente por:

> Empresa

ou:

> Cliente

quando esses conceitos possuírem significados distintos no domínio.

### Nomes que não devem ser traduzidos

Também é possível especificar termos que devem permanecer exatamente como definidos.

```text
Manter os seguintes nomes exatamente como estão:

- Payment Gateway
- Checkout Session
- Customer ID
- Tenant
```

### Regra terminológica explícita

Quando necessário, registre também proibições de substituição.

```text
Utilizar sempre "Organização".

NÃO substituir por "empresa", "cliente" ou "tenant".
```

Não agrupe termos como equivalentes sem que essa equivalência esteja definida no domínio do projeto.

---

## 8. Formato desejado

### Objetivo do campo

Informe a sintaxe, plataforma ou ambiente em que a documentação será publicada ou armazenada.

Essa informação orienta elementos como:

* hierarquia de títulos;
* listas;
* tabelas;
* blocos de código;
* links;
* restrições de formatação.

### Markdown para GitHub

Exemplo:

> Markdown para documentação no GitHub.

A documentação poderá utilizar estruturas como:

```markdown
## Configuração

### Pré-requisitos
```

### Confluence

Exemplo:

> Documento para publicação no Confluence. Priorizar títulos, tabelas, listas e seções curtas.

### Docs as Code

Para documentação armazenada com o código-fonte:

> Markdown para Docs as Code, armazenado em `/docs`.

### Restrições adicionais

Também podem ser declaradas regras específicas de formatação.

Exemplos:

> Markdown para GitHub. Não utilizar HTML.

ou:

> Confluence. Utilizar tabelas apenas quando melhorarem a consulta.

---

## 9. Texto que deve ser reescrito

### Objetivo do campo

Forneça o conteúdo original integral que deverá ser analisado e reescrito.

Não é necessário corrigir previamente:

* gramática;
* ortografia;
* organização;
* terminologia;
* estrutura;
* ambiguidades.

Manter essas características no texto original permite identificar problemas que poderiam ser ocultados por uma revisão prévia.

### Exemplo de texto original

```text
O usuário entra na tela e quando clicar em salvar ele vai
enviar os dados para API e se tiver tudo certo salva no
banco, mas se CPF já existir não pode cadastrar.
```

Esse texto contém informações que a reescrita deve identificar separadamente, como:

* uma ação do usuário;
* envio de dados para uma API;
* persistência no banco de dados;
* condição de sucesso;
* proibição de cadastro quando já existir o mesmo CPF.

Não é necessário transformar essas informações previamente em requisitos.

---

## 10. Exemplo de preenchimento completo

```text
Sistema/projeto:

Portal de Clientes — módulo de cadastro de pessoas

Tipo de documentação:

Requisitos funcionais e regras de negócio

Público-alvo:

Desenvolvedores backend, frontend e equipe de QA

Nível técnico esperado:

Intermediário

Terminologia obrigatória:

- Cliente = pessoa cadastrada no sistema
- CPF deve ser denominado sempre "CPF"
- Não utilizar "documento" como sinônimo de CPF

Formato desejado:

Markdown para GitLab

Texto que deve ser reescrito:

O usuário entra na tela e quando clicar em salvar ele vai
enviar os dados para API e se tiver tudo certo salva no
banco, mas se CPF já existir não pode cadastrar.
```

Com esse contexto, a regra:

> CPF duplicado não pode ser cadastrado.

pode ser identificada explicitamente como uma regra de negócio e, quando a finalidade da documentação exigir, representada de forma verificável.

A reescrita não deve limitar-se à correção gramatical do parágrafo quando o texto original contiver requisitos, regras de negócio, comportamentos ou restrições relevantes.

---

## 11. Critério para considerar o preenchimento suficiente

O contexto fornecido é suficiente quando permite determinar, sem suposições relevantes:

1. qual sistema ou componente está sendo documentado;
2. qual é a finalidade do documento;
3. quem utilizará o conteúdo;
4. qual nível técnico pode ser presumido;
5. quais termos precisam permanecer invariáveis;
6. qual formato deve ser utilizado;
7. qual conteúdo original deverá ser preservado semanticamente.

Quando uma dessas informações não estiver disponível, o campo correspondente pode permanecer sem preenchimento. A ausência não deve ser compensada por informações inventadas.

### 2. Pontos que precisam de esclarecimento

Há dois esclarecimentos relevantes.

1. O campo **Tipo de documentação** foi informado como `REGISTRO DE EXECUÇAÕ E LOGS`, mas o conteúdo fornecido não registra execuções, eventos, comandos executados, timestamps, resultados, evidências ou logs. Ele documenta como preencher um prompt. É necessário decidir se:

   * o tipo informado está incorreto; ou
   * foi fornecido o texto-fonte errado.

2. O **público-alvo** permanece como `[INSIRA AQUI]`. Pelo conteúdo, é possível inferir que o documento se destina a quem prepara prompts para documentação de software, mas essa inferência não deve ser convertida em definição oficial sem validação.

> **Informação necessária:** definir o público-alvo oficial do documento.

### 3. Problemas encontrados no texto original

O principal problema é a incompatibilidade entre o metadado `Tipo de documentação: REGISTRO DE EXECUÇAÕ E LOGS` e a natureza efetiva do conteúdo. Para classificação documental, o texto está muito mais próximo de um **guia de procedimento acompanhado de referência de campos**.

Também foram identificadas redundâncias significativas. A tabela inicial explica os campos e, posteriormente, praticamente as mesmas informações são repetidas em seções individuais. A repetição não é tecnicamente incorreta, mas reduz a eficiência de consulta. Na versão reescrita, a tabela foi mantida como referência rápida e as seções seguintes passaram a concentrar regras, exemplos e critérios adicionais.

Há ainda uso de expressões subjetivas como “quanto mais específico, melhor” e “um dos campos mais importantes”. Elas não estabelecem critérios objetivos. Foram substituídas por orientações verificáveis sobre a quantidade de contexto necessária.

O texto original também afirma que determinada formulação “impede” a IA de substituir termos. Isso é excessivamente absoluto para uma instrução de prompt. A função real da terminologia obrigatória é estabelecer uma restrição explícita que a reescrita deve respeitar; não há garantia técnica demonstrada de impossibilidade de violação.

Por fim, o exemplo `CPF duplicado não pode ser cadastrado` evidencia uma regra de negócio, mas não fornece detalhes suficientes para transformá-la integralmente em um requisito de implementação, como escopo da unicidade, normalização do CPF, comportamento da API ou código HTTP. Esses detalhes não foram inventados na reescrita.

### 4. Recomendações opcionais

Para transformar este material em um componente estável da documentação do CEPRAEA BEACH PRO, seria útil separar três artefatos conceitualmente diferentes: o **prompt propriamente dito**, o **guia de preenchimento do prompt** e uma **referência dos campos aceitos**. Isso evita que instruções dirigidas ao modelo sejam confundidas com instruções dirigidas ao humano.

Também seria útil definir uma terminologia canônica para `Tipo de documentação`. Por exemplo, se “Registro de Execução” e “Log de Execução” forem artefatos distintos no projeto, eles não deveriam aparecer agregados em um único rótulo sem uma definição formal de sua relação.

Para um verdadeiro **Registro de execução e logs**, a estrutura necessária seria substancialmente diferente e deveria considerar, entre outros elementos, identidade da execução, data/hora, agente ou operador, tarefa, ambiente, comandos ou ações, resultado esperado, resultado observado, status, evidências, erros e correlação com commit/branch/task. Esses elementos são uma recomendação para um documento futuro; eles não aparecem no texto original e, portanto, não foram incorporados como fatos.

````markdown

# Prompt — Reescrita Profissional de Documentação de Software

Atue como **Technical Writer, Software Architect e especialista em documentação de software**.

Sua tarefa é **reescrever o texto fornecido**, tornando-o adequado para documentação técnica profissional de software, sem alterar fatos, requisitos, regras de negócio ou decisões técnicas existentes.

Use como referência boas práticas de documentação técnica e princípios associados a padrões como **ISO/IEC/IEEE 26514, ISO/IEC/IEEE 15289, ISO/IEC/IEEE 29148 e ISO/IEC/IEEE 12207**, além de práticas modernas como **Diátaxis, Docs as Code, C4 Model, ADRs, OpenAPI e linguagem normativa baseada em RFC 2119/BCP 14**, quando aplicáveis.

Não afirme que o documento está formalmente em conformidade com uma norma ISO/IEC/IEEE apenas por ter sido reescrito seguindo estas orientações.

## Objetivos

Reescreva o conteúdo para que ele seja:

- claro;
- objetivo;
- tecnicamente preciso;
- consistente;
- verificável quando aplicável;
- fácil de consultar;
- adequado ao público-alvo;
- livre de ambiguidades;
- estruturado de acordo com o propósito da documentação.

## 1. Preserve o significado técnico

Não altere:

- regras de negócio;
- nomes técnicos;
- parâmetros;
- endpoints;
- comandos;
- código;
- valores;
- limites;
- requisitos;
- decisões arquiteturais;
- comportamentos do sistema.

Não invente funcionalidades, requisitos, dependências, comportamentos ou informações ausentes.

Quando alguma informação importante estiver faltando, marque explicitamente:

> **Informação necessária:** [descrever informação faltante]

Quando houver ambiguidade relevante, marque:

> **Ambiguidade identificada:** [explicar]

Não tente preencher lacunas com suposições.

## 2. Identifique o tipo de documentação

Antes de reescrever, determine qual categoria melhor representa o conteúdo:

- Tutorial;
- Guia de procedimento / How-to;
- Referência técnica;
- Explicação conceitual;
- Requisitos;
- Arquitetura;
- ADR — Architecture Decision Record;
- Documentação de API;
- Desenvolvimento;
- Implantação;
- Operação;
- Runbook;
- Troubleshooting;
- Segurança;
- Regra de negócio;
- Manual do usuário;
- Outro.

Use os princípios do **Diátaxis** quando apropriado.

Não misture tutorial, referência, explicação e procedimento desnecessariamente.

## 3. Considere o público-alvo

Adapte vocabulário, profundidade e nível técnico de acordo com o leitor.

Possíveis públicos:

- usuário final;
- desenvolvedor;
- arquiteto;
- QA;
- DevOps/SRE;
- suporte;
- produto;
- segurança;
- auditoria;
- gestão;
- integração externa.

Se o público não puder ser determinado pelo texto, mantenha uma linguagem técnica neutra e sinalize:

> **Público-alvo não especificado.**

## 4. Melhore clareza e objetividade

Prefira frases:

- curtas;
- diretas;
- afirmativas;
- com sujeito e ação claramente identificáveis.

Evite:

- linguagem vaga;
- redundância;
- excesso de adjetivos;
- frases excessivamente longas;
- termos como “corretamente”, “adequadamente”, “rapidamente” ou “normalmente” sem definição objetiva;
- expressões subjetivas;
- construções que permitam múltiplas interpretações.

Exemplo:

Evite:

> O sistema deve responder rapidamente.

Prefira:

> O sistema deve responder em até 300 ms no percentil 95.

Entretanto, **não invente o valor de 300 ms** caso essa informação não esteja presente no texto original.

Nesse caso, escreva:

> O sistema deve atender ao limite de tempo de resposta definido para a operação.

E indique:

> **Informação necessária:** definir o limite máximo de tempo de resposta e a métrica utilizada.

## 5. Transforme requisitos em declarações verificáveis

Quando o texto contiver requisitos, verifique se eles são:

- claros;
- específicos;
- mensuráveis quando possível;
- testáveis;
- não ambíguos;
- rastreáveis;
- independentes quando possível.

Prefira estruturas como:

### REQ-[TIPO]-[ID]

**Descrição:**
[requisito]

**Justificativa:**
[motivo, se conhecido]

**Critério de aceitação:**
[forma de verificar o requisito]

**Prioridade:**
[se informada]

**Origem:**
[se informada]

**Relacionamentos:**
[se informados]

Não crie IDs, prioridades ou critérios como se fossem fatos caso não tenham sido fornecidos. Se necessário, use marcadores indicando que precisam ser definidos.

## 6. Use linguagem normativa corretamente

Quando houver obrigações formais, utilize termos consistentes:

- **DEVE** — requisito obrigatório;
- **NÃO DEVE** — proibição;
- **DEVERIA** — recomendação forte, permitindo exceções justificadas;
- **PODE** — comportamento opcional ou permitido.

Não transforme uma recomendação em obrigação ou uma possibilidade em requisito.

Preserve o nível de obrigatoriedade do texto original.

## 7. Mantenha terminologia consistente

Escolha uma única denominação para cada conceito.

Não alterne sem necessidade entre sinônimos como:

- usuário;
- cliente;
- consumidor;
- operador;
- account;
- customer;

se eles representam a mesma entidade.

Quando houver conceitos potencialmente diferentes, não os unifique sem evidência.

Se existirem inconsistências terminológicas, inclua ao final:

### Inconsistências terminológicas identificadas

- “[termo A]” e “[termo B]” parecem representar o mesmo conceito.
- Recomenda-se confirmar a terminologia oficial.

Quando relevante, proponha um pequeno glossário.

## 8. Estruture o documento hierarquicamente

Utilize:

- títulos;
- subtítulos;
- listas;
- tabelas quando realmente melhorarem a consulta;
- blocos de código;
- exemplos;
- observações;
- avisos.

Evite grandes blocos contínuos de texto.

A estrutura deve permitir que o leitor encontre rapidamente a informação necessária.

## 9. Procedimentos devem ser executáveis

Quando o texto descrever uma tarefa, estruture-a preferencialmente assim:

### Objetivo

Explique o resultado da operação.

### Pré-requisitos

Liste dependências, permissões e condições necessárias.

### Procedimento

Use passos numerados.

Cada passo deve conter preferencialmente uma ação principal.

### Exemplo

Inclua somente quando houver dados suficientes.

### Resultado esperado

Explique como confirmar que a operação foi concluída.

### Possíveis erros

Documente, quando conhecidos:

- mensagem de erro;
- causa;
- diagnóstico;
- solução.

## 10. Código, comandos e configuração

Preserve código exatamente quando sua alteração não for necessária.

Use blocos de código apropriados.

Para comandos, procure informar:

1. o que será executado;
2. o comando;
3. o resultado esperado.

Exemplo:

Execute:

```bash
npm run dev
```

Resultado esperado:

```text
Server running at http://localhost:3000
```

Não invente saídas que não estejam presentes ou que não possam ser inferidas com segurança.

## 11. Arquitetura

Quando o texto documentar arquitetura, procure separar:

- contexto;
- componentes;
- responsabilidades;
- dependências;
- integrações;
- fluxo de dados;
- decisões;
- restrições;
- consequências.

Quando aplicável, organize informações seguindo conceitos do **C4 Model**:

- System Context;
- Container;
- Component;
- Deployment.

Não crie componentes inexistentes.

## 12. Decisões arquiteturais

Quando o conteúdo representar uma decisão arquitetural, considere reorganizá-lo como ADR:

### Título da decisão

**Status:**
[Proposto / Aceito / Substituído / Depreciado — somente se conhecido]

**Contexto:**
[problema que motivou a decisão]

**Opções consideradas:**
[alternativas conhecidas]

**Decisão:**
[decisão adotada]

**Justificativa:**
[motivos]

**Consequências:**
[impactos positivos, negativos e trade-offs]

Não invente opções alternativas ou justificativas que não estejam presentes.

## 13. APIs

Quando houver documentação de APIs, deixe explícitos, quando disponíveis:

- método HTTP;
- endpoint;
- finalidade;
- autenticação;
- parâmetros de path;
- query parameters;
- headers;
- request body;
- tipos;
- campos obrigatórios;
- respostas;
- códigos HTTP;
- erros;
- exemplos.

Se houver estrutura suficiente, utilize conceitos compatíveis com OpenAPI, mas não invente um contrato inexistente.

## 14. Erros e troubleshooting

Quando houver informação suficiente, organize problemas da seguinte forma:

### Problema

[descrição]

### Sintoma

[o que o usuário observa]

### Causa

[motivo conhecido]

### Diagnóstico

[como confirmar]

### Solução

[procedimento]

### Prevenção

[quando aplicável]

## 15. Diferencie fatos de recomendações

Não apresente sugestão como se fosse comportamento existente do sistema.

Use explicitamente:

> **Recomendação:** ...

para melhorias sugeridas que não fazem parte do conteúdo original.

## 16. Não esconda problemas do texto original

Depois da reescrita, faça uma pequena análise crítica.

Liste apenas problemas relevantes encontrados, como:

- requisito não verificável;
- informação ausente;
- contradição;
- ambiguidade;
- terminologia inconsistente;
- dependência não documentada;
- comportamento indefinido;
- erro sem tratamento especificado;
- regra de negócio incompleta;
- ausência de critério de aceitação.

## 17. Formato da resposta

Produza a resposta nesta ordem:

### 1. Texto reescrito

Apresente a versão final, pronta para utilização na documentação.

### 2. Pontos que precisam de esclarecimento

Liste apenas informações realmente necessárias para eliminar ambiguidades ou completar a documentação.

Caso não existam:

> Nenhum esclarecimento essencial identificado.

### 3. Problemas encontrados no texto original

Liste inconsistências, ambiguidades ou fragilidades relevantes.

Caso não existam:

> Nenhum problema relevante identificado.

### 4. Recomendações opcionais

Apresente melhorias adicionais que poderiam tornar a documentação mais completa, mas que não devem ser incorporadas como fatos sem validação.

## 18. Regra final

O objetivo não é tornar o texto mais sofisticado.

O objetivo é torná-lo **mais preciso, compreensível, verificável, consultável e útil para quem precisa desenvolver, testar, integrar, operar, manter ou utilizar o software**.

Sempre prefira precisão técnica à linguagem ornamental.

---

## Contexto opcional

Use as informações abaixo somente se forem preenchidas.

**Sistema/projeto:**
CEPRAEA BEACH PRO

**Tipo de documentação:**
REGISTRO DE EXECUÇAÕ E LOGS

**Público-alvo:**
[INSIRA AQUI]

**Nível técnico esperado:**
Avançado

**Terminologia obrigatória:**
[INSIRA AQUI]

**Formato desejado:**
Markdown

---

## Texto que deve ser reescrito

[# Preenchimento dos Campos

Para preencher os campos do prompt, use estas orientações:

| Campo | O que informar | Exemplo |
| --- | --- | --- |
| **Sistema/projeto** | Nome do software, módulo, serviço ou projeto ao qual o texto pertence. Pode incluir uma descrição curta se o nome não deixar claro o contexto. | `Portal de Gestão de Contratos — módulo de aprovação` |
| **Tipo de documentação** | Natureza do documento que está sendo escrito. Isso ajuda a IA a escolher estrutura, linguagem e nível de detalhamento adequados. | `Requisitos funcionais`, `Documentação de API`, `Runbook`, `Arquitetura`, `Tutorial`, `ADR` |
| **Público-alvo** | Quem deverá utilizar ou consultar o documento. Seja específico quando possível. | `Desenvolvedores backend`, `Equipe de suporte N2`, `Usuários administrativos`, `Arquitetos de software` |
| **Nível técnico esperado** | Quanto conhecimento técnico o leitor presumidamente possui. | `Iniciante`, `Intermediário`, `Avançado` ou `Misto` |
| **Terminologia obrigatória** | Termos oficiais do projeto que devem ser mantidos exatamente como definidos. É útil para evitar que a IA substitua conceitos por sinônimos inadequados. | `Tenant = Organização; Cliente = empresa contratante; Usuário = pessoa que acessa o sistema`            |
| **Formato desejado** | Onde ou em qual sintaxe a documentação será publicada. Isso influencia títulos, tabelas, blocos de código e formatação. | `Markdown para GitHub`, `Confluence`, `GitLab Wiki`, `Markdown`, `texto simples` |
| **Texto que deve ser reescrito** | Conteúdo original. Deve ser fornecido sem tentar “melhorá-lo” previamente, pois a IA precisa identificar ambiguidades, inconsistências e lacunas existentes. | Cole o texto integral que deseja revisar. |

### Sistema/projeto

Informe **sobre qual sistema o texto está falando**.
Quanto mais específico, melhor.
Por exemplo, em vez de:

> Sistema financeiro

prefira:

> Sistema Financeiro Corporativo — módulo de Contas a Pagar

ou:

> API de Pagamentos — microsserviço responsável pela criação, autorização e cancelamento de transações.

*Não é necessário descrever toda a arquitetura. O objetivo é fornecer contexto suficiente para a IA interpretar corretamente termos e responsabilidades.*

---

### Tipo de documentação

Este é um dos campos mais importantes porque muda bastante a maneira como o texto será reescrito.

Se informar:

> **Tipo de documentação:** Requisitos funcionais
Então a IA deverá privilegiar frases verificáveis, como:

> O sistema **DEVE** permitir que um administrador inative um usuário.

Se informar:

> **Tipo de documentação:** Tutorial

Então, a estrutura poderá ser:

> 1. Acesse **Configurações**.
> 2. Selecione **Usuários**.
> 3. Selecione o usuário.
> 4. Clique em **Inativar**.

Alguns valores que podem ser usados com frequência são:

- requisitos funcionais;
- requisitos não funcionais;
- regras de negócio;
- especificação técnica;
- arquitetura de software;
- ADR;
- documentação de API;
- tutorial;
- guia de uso;
- procedimento operacional;
- runbook;
- troubleshooting;
- documentação de implantação;
- documentação de desenvolvimento;
- documentação de segurança;
- referência técnica.

Se um texto tiver mais de uma finalidade, então escreva:

> `Especificação técnica e requisitos de integração`

---

### Público-alvo

Informe **quem deverá entender e utilizar aquela documentação**.

Evite, quando possível:

> Equipe

Prefira:

> Desenvolvedores backend responsáveis pela integração com a API.

ou:

> Analistas de suporte N1 e N2 responsáveis pelo diagnóstico inicial de falhas.

ou:

> Usuários administrativos sem conhecimento de programação.

Esse campo influencia diretamente o vocabulário.

Para desenvolvedores, por exemplo, isto pode ser suficiente:

> O endpoint retorna HTTP 409 quando já existe um registro para o identificador informado.

Para usuário final, provavelmente será melhor:

> Se já existir um cadastro com o mesmo identificador, o sistema não permitirá criar um novo registro.

---

### Nível técnico esperado

Esse campo diz à IA **quanto conhecimento pode ser presumido**.

**Iniciante** significa que conceitos técnicos importantes devem ser explicados. Exemplo:

> PostgreSQL é o banco de dados utilizado pela aplicação.

**Intermediário** permite assumir conhecimentos comuns da área:

> Execute as migrations antes de iniciar a aplicação.

**Avançado** permite utilizar terminologia especializada sem explicar conceitos básicos:

> A operação utiliza isolamento `READ COMMITTED` e locking pessimista durante a atualização.

**Misto** é útil para documentação destinada a públicos diferentes. Nesse caso, a IA deve tentar manter o conteúdo compreensível sem simplificar excessivamente os conceitos técnicos.

---

### Terminologia obrigatória

Use este campo para criar uma espécie de **mini glossário oficial**.

Por exemplo:

```text
Tenant = Organização cliente do sistema
Conta = unidade financeira pertencente a uma Organização
Usuário = pessoa física autenticada
Administrador = usuário com perfil ADMIN
Pedido = entidade Order no domínio
```

Isso impede um problema muito comum em documentação: a IA transformar inadvertidamente:

> Organização

em:

> Empresa

ou:

> Cliente

mesmo que, no seu domínio, essas três palavras tenham significados diferentes.

Você também pode especificar nomes que **não devem ser traduzidos**:

```text
Manter os seguintes nomes exatamente como estão:
- Payment Gateway
- Checkout Session
- Customer ID
- Tenant
```

Ou estabelecer uma regra:

```text
Utilizar sempre "Organização".
Nunca substituir por "empresa", "cliente" ou "tenant".
```

---

### Formato desejado

Informe **onde o conteúdo será utilizado**.

Por exemplo:

> Markdown para documentação no GitHub.

Isso permite utilizar:

```markdown
## Configuração

### Pré-requisitos
```

Para Confluence, você pode informar:

> Documento para publicação no Confluence. Priorizar títulos, tabelas, listas e seções curtas.

Para documentação dentro do próprio repositório:

> Markdown para Docs as Code, armazenado em `/docs`.

Também pode especificar restrições:

> Markdown para GitHub. Não utilizar HTML.

ou:

> Confluence. Utilizar tabelas apenas quando melhorarem a consulta.

---

### Texto que deve ser reescrito

Aqui você deve colocar **o conteúdo original**, mesmo que esteja mal escrito.

Por exemplo:

```text
O usuário entra na tela e quando clicar em salvar ele vai
enviar os dados para API e se tiver tudo certo salva no
banco, mas se CPF já existir não pode cadastrar.
```

Não é necessário primeiro corrigir português ou organizar o texto. Na verdade, preservar o texto original ajuda a IA a identificar problemas como:

- ambiguidade;
- regras escondidas dentro de parágrafos;
- requisitos não verificáveis;
- termos inconsistentes;
- informações faltantes.

Com o contexto preenchido, poderia ficar assim:

```text
Sistema/projeto:
Portal de Clientes — módulo de cadastro de pessoas

Tipo de documentação:
Requisitos funcionais e regras de negócio

Público-alvo:
Desenvolvedores backend, frontend e equipe de QA

Nível técnico esperado:
Intermediário

Terminologia obrigatória:
- Cliente = pessoa cadastrada no sistema
- CPF deve ser denominado sempre "CPF"
- Não utilizar "documento" como sinônimo de CPF

Formato desejado:
Markdown para GitLab

Texto que deve ser reescrito:
O usuário entra na tela e quando clicar em salvar ele vai
enviar os dados para API e se tiver tudo certo salva no
banco, mas se CPF já existir não pode cadastrar.
```

Com essas informações, a IA terá condições de perceber que **“CPF duplicado não pode ser cadastrado” é uma regra de negócio**,
que precisa ser escrita de maneira explícita e potencialmente transformada em um requisito verificável, em vez de simplesmente
fazer uma correção gramatical do parágrafo.
]

````

***


