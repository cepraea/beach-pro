# Documento de Padrões de Perspectivas de Revisão (R1 a R6)

> **Posicionamento deste documento:** É a única fonte de verdade (**Single Source of Truth**) das perspectivas de revisão <br>consultadas pelo **review-agent**. O arquivo process-rules §9.2 é um resumo deste documento; consulte este documento<br> para obter os detalhes de forma abrangente.
> **Documentos relacionados:** [Regras de Processo](full-auto-dev-process-rules-ja.md) §9 Framework de Gestão da Qualidade, [Regras de Gestão de Documentos](full-auto-dev-document-rules-ja.md)

***

## R1: Perspectivas de Revisão da Qualidade dos Requisitos 

>**Alvo: Ch1-2 das Especificações**

### R1a: Qualidade da Estrutura dos Requisitos

- **Todos os requisitos funcionais** possuem um **ID** (**FR-xxx**) atribuído?
- **Não restaram expressões impossíveis de testar** (como "*adequadamente*", "*suficientemente*", "*rapidamente*", etc.)?
- **Não existem requisitos contraditórios** (*ex.: múltiplos resultados definidos para a mesma operação*)?
- Os casos de uso definem **cenários principais e cenários alternativos** (*fluxos de erro*)?
- **Os requisitos não funcionais** possuem critérios numéricos mensuráveis (*ex.: "*em até 200ms", "99,9% ou mais"*)?
- Os **nomes de entidades e operações** são usados de forma consistente (*sem múltiplos nomes para o mesmo conceito*)?
- As **abreviações e termos técnicos** estão definidos (*existência de um glossário*)?

### R1b: Qualidade da Expressão dos Requisitos 
> **Perspectiva de Engenharia de Requisitos**

#### Eliminação de Ambiguidade

- **Não restaram expressões ambíguas** como *"o mais rápido possível"*, *"adequadamente"*, *"conforme necessário"*<br> ou "sempre que possível"?
- Em caso de **refinamento gradual** (*expressão provisória → concretização*), há uma nota explícita indicando isso<br> (ex.: "A ser quantificado na fase **design**")?
- **O sujeito** (quem/o que) e **a ação** (o que faz) de cada requisito **estão claros**?



#### Eliminação de *Formas Negativas* e *Voz Passiva

- Para **requisitos na forma negativa** (*"não deve fazer..."*), há a definição de uma **ação alternativa sobre o <br>que deve ser feito** em vez disso?
- **A responsabilidade não está ambígua devido ao uso da voz passiva** (*"os dados são salvos"*)?
- É possível **reescrever na voz ativa** (*"o sistema salva os dados no banco de dados*")?
- Não há uso de dupla negação (ex.: "quando não for inválido")?

**Abrangência de Fluxos de Exceção e Subnormais:**
- As seguintes perspectivas foram consideradas para cada requisito funcional:
  - Timeout (sem resposta de serviço externo)
  - Interrupção (usuário cancela a operação no meio)
  - Operação simultânea (múltiplos usuários alteram o mesmo recurso simultaneamente)
  - Falta de privilégios (autenticação expirada, sem permissão)
  - Inconsistência de dados (referência inexistente, tipo inválido)
  - Esgotamento de recursos (disco cheio, falta de memória)
- Além do fluxo normal (caminho feliz), os fluxos subnormais (casos normais, mas especiais) e os fluxos de exceção estão explicitados?

#### Eliminação de Duplicação e Conflitos nas Especificações 

**DRY para Specs:**
- O mesmo requisito não está descrito em múltiplos locais dispersos? (Se estiver disperso, torna-se ambíguo qual é o correto, causando **defect**).
- Não escreva a mesma coisa duas vezes. Se necessário, faça referência direta à única fonte principal.
- Não há contradições implícitas entre os requisitos de seções diferentes (ex.: a pré-condição do **FR-001** entra em conflito com a ação do **FR-015**)?
- As dependências entre requisitos estão explícitas (ex.: "O **FR-005** tem como premissa a conclusão do **FR-001**")?

**Verificação de Integridade:**
- Os requisitos estão organizados sob a perspectiva **MECE** (mutuamente excludentes, coletivamente exaustivos)?
- Não há omissões de requisitos sob a perspectiva de cada stakeholder (administrador / usuário comum / sistema externo)?
- As condições de contorno (valor mínimo, valor máximo, vazio, *null*) estão explícitas?

***

## R2: Perspectivas de Revisão dos Princípios de Design de Software 
> **Alvo**: Ch3-4 das Especificações e Código

### Princípios SOLID

#### SRP - Princípio da Responsabilidade Única
- Uma classe/módulo não possui múltiplos motivos para mudar?
- Atenção a classes com nomes do tipo "faz isso e aquilo" ou que possuam vários métodos não relacionados.
- Exemplo de apontamento: `UserService` lidando simultaneamente com autenticação, gestão de perfil e envio de e-mails.

#### OCP - Princípio `Aberto-Fechado`
- A estrutura não exige alterações no código existente (especialmente a adição de ramificações if/switch) ao adicionar novas funcionalidades?
- Foram estabelecidos pontos de extensão utilizando o padrão `Strategy`, padrão `Template Method`, etc.?

#### LSP - Princípio da Substituição de Liskov

- As subclasses não estão fortalecendo as pré-condições ou enfraquecendo as pós-condições da classe pai?
- Os métodos sobrescritos (*overridden*) não estão alterando o contrato do pai (tipos de exceção, significado do valor de retorno)?

#### ISP - Princípio da Segregação de Interfaces

- As classes concretas não estão implementando interfaces com métodos que elas não utilizam?
- Uma interface grande não pode ser dividida por finalidade de uso?

#### DIP - Princípio da Inversão de Dependência

- Módulos de alto nível (lógica de negócios) não dependem diretamente de classes concretas de módulos de baixo nível (DB, APIs externas)?
- A direção da dependência passa por interfaces/classes abstratas?

#### Outros Princípios de Design

**DRY (Don't Repeat Yourself)**
- A mesma lógica não está duplicada em múltiplos lugares?
- Não há números mágicos ou strings mágicas espalhados (foram convertidos em constantes)?
- A mesma validação não está implementada de forma redundante em múltiplas camadas?

**KISS (Keep It Simple, Stupid)**
- A solução não se tornou desnecessariamente complexa em relação ao problema?
- A profundidade de aninhamento (*nesting*) de funções não é de 4 ou mais níveis?
- As ramificações condicionais complexas não podem ser achatadas (*flattened*) com retornos antecipados (*early returns*)?

**YAGNI (You Aren't Gonna Need It)**
- Funcionalidades que não existem nos requisitos atuais não foram implementadas antecipadamente?
- Não há generalização/abstração excessiva (ex.: classes abstratas para as quais existe apenas um caso concreto no momento)?
- Não há parâmetros, *flags* ou valores de configuração não utilizados?

**SoC (Separação de Interesses)**
- Lógicas de interface de usuário (UI) e lógicas de negócios não estão misturadas?
- Lógicas de acesso a dados não vazaram para a camada de lógica de negócios?
- Validação, transformação e persistência não estão misturadas na mesma função?

**SLAP (Princípio do Nível Único de Abstração)**
- "Intenções de alto nível (o que fazer)" e "detalhes de implementação de baixo nível (como fazer)" não estão misturados em uma mesma função?
- Exemplo de apontamento: Processamento HTTP e montagem de strings SQL existindo na mesma função.

**LOD (Lei de Demeter / Princípio do Menor Conhecimento)**
- Chamadas em cadeia como `a.b.c.doSomething()` não estão sendo usadas em excesso (dependência excessiva da estrutura)?
- O objeto não está dependendo de detalhes além de seus "amigos diretos"?

**CQS (Segregação de Comando e Consulta)**
- Não existem métodos que alteram o estado (com efeitos colaterais) e retornam um valor ao mesmo tempo?
- Exemplo de apontamento: `getNextId()` alterando um contador interno enquanto retorna o valor.

**POLA (Princípio da Menor Surpresa)**
- O comportamento real condiz com o comportamento esperado a partir do nome da função/método?
- Não há efeitos colaterais ocultos (alterações de estado além da saída de logs) em locais invisíveis para quem faz a chamada?
- Não existem *flags* booleanas invertidas (dupla negação, como `isNotInvalid`)?

**PIE (Princípio da Intenção Expressa)**
- Os nomes de variáveis/funções expressam não apenas "o que está fazendo", mas também "por que está fazendo"?
- Os comentários explicam "por que está sendo feito assim" em vez de "o que está sendo feito" (o que já é óbvio pelo código)?
- Não há locais onde a intenção poderia ser esclarecida nomeando resultados intermediários através de variáveis temporárias?

**CA (Clean Architecture / Arquitetura em Camadas)**
- A direção das dependências aponta para a camada de domínio (interior)? (Apenas dependências de fora para dentro são permitidas).
- As entidades de domínio não estão contaminadas por detalhes do framework/DB (como *annotations*)?
- A estrutura garante que alterações na camada de infraestrutura (DB, APIs externas) não se propaguem para a lógica de negócios?

- **Correção da divisão em camadas**:
  * A classificação em **Entity** / **UseCase** / **Adapter** / **Framework** é adequada?
  * Conceitos que deveriam pertencer ao domínio não foram classificados erroneamente na camada **Framework**?
   * Inversamente, coisas que poderiam ficar no **Framework** não foram elevadas para **Entity**
  * Avalie com base no critério: "Para o propósito deste projeto, isso é a essência ou um meio?".
- **Adequação da camada Adapter**:
  * A camada **Adapter** não está fina demais, vazando dependências externas para o domínio?  
  * Ou espessa demais, misturando a lógica de negócios dentro da camada **Adapter**?

**Naming (Nomenclatura)**
- Os nomes das variáveis representam com precisão seus papéis (sem nomes genéricos como `data`, `info`, `tmp`, `obj`, etc.)?
- Os nomes das funções estão no formato Verbo + Objeto (sem verbos ambíguos como `process`, `handle`, `manage`, etc.)?
- Os nomes de variáveis/funções booleanas começam com `is`, `has`, `can` ou `should`?
- Os nomes de variáveis de coleções estão no plural?
- As abreviações estão sendo usadas de forma consistente (sem misturar `Usr` e `User`)?

**Engenharia de Prompt (Quando a Integração AI/LLM estiver ativa)**
- Os templates de prompt do produto estão localizados no diretório `src/` (sem se misturarem com a camada meta no diretório `.claude/`)?
- Os schemas de entrada e saída (tipo da entrada esperada e tipo da saída esperada) estão explicitados em cada prompt?
- Não há expressões ambíguas nas instruções do prompt (aplicar aos prompts a mesma perspectiva de eliminação de ambiguidade do **R1b**)?
- Existem testes de prompt (pares de entrada → saída esperada) no diretório `tests/`?
- Foi definida uma política de controle de versão dos prompts (como resposta a mudanças de comportamento quando o modelo for alterado)?
- Foram projetadas medidas contra alucinações (lógica de validação de saída, métodos de *grounding*)?

***

## R3: Perspectivas de Revisão da Qualidade de Codificação (Alvo: Código)

### Tratamento de Erros
- Erros foram capturados em todos os I/Os externos (rede, DB, arquivos)?
- Não existem erros sendo engolidos silenciosamente (blocos *catch* vazios, ignorados com `_`)?
- As mensagens de erro incluem as informações de contexto necessárias para a depuração (*debugging*)?
- As mensagens de erro retornadas ao usuário não expõem detalhes da implementação interna (*stack traces*, erros de DB)?

### Programação Defensiva
- Todas as entradas externas (argumentos de API, variáveis de ambiente, arquivos de configuração) estão sendo validadas?
- Casos envolvendo *Null*, *Undefined* ou *arrays* vazios foram considerados?
- Asserções de tipo (`as Type`) não estão sendo usadas sem a verificação de segurança apropriada?

***

## R4: Perspectivas de Revisão de Concorrência e Transição de Estado

### Deadlock

**Nível de Design:**
- Em fluxos que utilizam múltiplos recursos simultaneamente (DB, cache, arquivos, etc.), a ordem de aquisição está definida de forma comum para todos os caminhos?
- A "restrição da ordem de aquisição de recursos" está descrita nos documentos de design?
- Foram analisados os níveis de isolamento de transações do DB e os padrões de acesso capazes de gerar *deadlocks*?

**Nível de Código:**
- O aninhamento de bloqueios (*locks*) (padrão onde se adquire `lock B` dentro de `lock A`) não está sendo acessado por meio de múltiplas ordens de aquisição?
- Não há chamadas a APIs externas ou processos demorados ocorrendo dentro de transações de DB (retenção prolongada de *locks*)?
- Ao usar `SELECT ... FOR UPDATE`, a ordem de aquisição é consistente?

### Condição de Corrida (Race Condition)
**Nível de Design:**

>**Os fluxos** onde podem ocorrer acessos simultâneos a estados compartilhados foram <br>identificados e **tiveram medidas de mitigação projetadas**?
>
>O padrão **Check-Then-Act** "verificar a existência antes de usar": foi projetado para ser<br> implementável atomicamente ?

**Nível de Código**

Focado em `JavaScript`/`TypeScript`

> Não ocorrem conflitos em padrões que leem e gravam estados compartilhados<br> através de múltiplos `await`?

  ```javascript
  // Exemplo perigoso
  const count = await getCount();   // Outro processo pode alterar count aqui
  await setCount(count + 1);        // Atualização baseada em um count obsoleto
```

* Não há pontos onde a execução paralela de manipuladores de eventos (*event handlers*) causa inconsistências em filas ou contadores?
* Processos executados em paralelo via `Promise.all` não atualizam o mesmo recurso de forma conflitante?
* Bloqueios otimistas ou pessimistas estão sendo aplicados em locais onde o *Read-Modify-Write* de DB não é atômico?

**Nível de Código (Focado em linguagens multithreading):**

* Foram aplicados *locks* apropriados, operações atômicas ou modificadores voláteis (*volatile modifiers*) no acesso a variáveis compartilhadas?
* Coleções que não são *thread-safe* (como `HashMap`, etc.) não estão sendo usadas em ambientes *multithreading*?

### Glitch (Estado Incorreto Momentâneo Durante Transições de Estado)

**Nível de Design:**

* O diagrama de transição de estados do Ch3 das especificações está definido de forma implementável (os estados intermediários durante a transição estão explícitos)?
* Quando a atualização simultânea de múltiplos campos for necessária, sua atomicidade está garantida no design?

**Nível de Código:**

* O diagrama de transição de estados definido no Ch3 das especificações é consistente com o código implementado (não existem transições de estado inválidas)?
* Processos que atualizam múltiplos campos simultaneamente não estão ocorrendo fora de uma transação?
```javascript
// Exemplo perigoso (estado intermediário entre order.status e order.completedAt é observável)
order.status = 'completed';     // Neste momento o status é 'completed', mas completedAt é null
order.completedAt = new Date();
```


* Na sincronização de estado entre *frontend* e *backend*, não existe um período em que atualizações parciais sejam observáveis?
* O momento da notificação de eventos (se é "antes" ou "depois" da alteração de estado) está claro?

***

## R5: Perspectivas de Revisão de Desempenho

### Algoritmos e Estruturas de Dados

**Nível de Design:**

* Para atender aos requisitos de desempenho (NFR do Ch2 das especificações), a complexidade de tempo dos algoritmos importantes foi analisada?
* Não foram selecionados algoritmos de O(n²) ou pior para processamentos lidando com grandes volumes de dados?

**Nível de Código:**

* Cálculos invariantes não estão sendo executados repetidamente dentro de laços (omissão em mover a expressão invariante para fora do laço)?
* Nos locais onde se utiliza busca linear, não há nada que possa ser substituído por acesso em O(1) usando *Map* ou *Set*?
* Não houve omissão na aplicação de buscas binárias em *arrays* já ordenados?

### Banco de Dados e I/O

**Nível de Design:**

* O design de índices (*indexes*) para consultas acessadas com frequência foi levado em consideração?
* A obtenção de grandes volumes de dados, que necessitam de paginação ou cursores, foi projetada?

**Nível de Código:**

* O problema de N+1 *queries* não está ocorrendo (consultas dentro de laços devido ao carregamento preguiçoso /*lazy loading* de ORM)?

```javascript
// Exemplo perigoso
const users = await User.findAll();
for (const user of users) {
  const orders = await user.getOrders(); // Emite query N vezes
}
```


* Onde se utiliza `SELECT *`, não estão sendo obtidas colunas desnecessárias?
* Em locais onde operações em lote (*bulk*) são possíveis, não estão ocorrendo INSERTs/UPDATEs avulsos dentro de laços?
* I/Os de rede ou processamentos demorados não estão ocorrendo dentro de transações?

### Memória e Recursos

**Nível de Código:**

* Nos locais em que se carrega uma grande quantidade de dados na memória de uma só vez, não há itens que possam ser alterados para processamento via *streaming*?
* Não houve omissão na remoção de *EventListeners* e *timers* (causa de vazamento de memória /*memory leak*)?
* Não estão sendo gerados objetos inalcançáveis pelo *Garbage Collector* (GC) devido a referências circulares?
* Foram configurados tempo de expiração e tamanho máximo para os caches?

### Rede e Frontend

**Nível de Código:**

* Chamadas de API que não precisam ser sequenciais não estão sendo serializadas via `await` (possível paralelizar com `Promise.all`)?
* As respostas da API não incluem campos desnecessários (*overfetching*)?
* Não estão ocorrendo re-renderizações desnecessárias no *frontend* (como configurações incorretas em *arrays* de dependências do `useEffect` do React, etc.)?
* Onde é aplicável o carregamento preguiçoso (*lazy loading*) ou a divisão de código (*code splitting*), não estão ocorrendo importações estáticas?

***

## R6: Perspectivas de Revisão da Qualidade dos Testes 

> **Alvo**: Código de Teste

* Os nomes dos testes expressam sua intenção no formato "Pré-condição → Ação → Resultado Esperado" ou "should + comportamento esperado"?
* Os testes são independentes (sem dependência na ordem de execução ou estado compartilhado entre testes)?
* Estão abrangidos não apenas os fluxos normais, mas também valores de contorno, fluxos de exceção e casos limite (*edge cases*)?
* Os *mocks* e *stubs* não estão sendo usados em excesso a ponto de os testes não conseguirem validar o comportamento real?
* Não estão incluídos testes instáveis (*flaky tests* - dependentes de *timing* ou aleatoriedade)?
* Não há omissões na cobertura de requisitos, validando contra a rastreabilidade das especificações (traces: **FR-xxx**)?