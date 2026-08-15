# **Missão do agente e processo de descoberta do domínio a partir do acervo CEPRAEA**

- [**Missão do agente e processo de descoberta do domínio a partir do acervo CEPRAEA**](#missão-do-agente-e-processo-de-descoberta-do-domínio-a-partir-do-acervo-cepraea)
  - [**Missão do agente**](#missão-do-agente)
  - [**Princípio fundamental de descoberta**](#princípio-fundamental-de-descoberta)
- [**Objetos obrigatórios de descoberta, validação e formalização**](#objetos-obrigatórios-de-descoberta-validação-e-formalização)
  - [**1. Bounded Contexts**](#1-bounded-contexts)
    - [**Objetivo**](#objetivo)
    - [**Regra de descoberta**](#regra-de-descoberta)
    - [**Formalização esperada**](#formalização-esperada)
  - [**2. Identidades definitivas**](#2-identidades-definitivas)
    - [**Objetivo**](#objetivo-1)
    - [**Reconciliação entre fontes**](#reconciliação-entre-fontes)
    - [**Identidade humana, autenticação e papel**](#identidade-humana-autenticação-e-papel)
    - [**Formalização esperada**](#formalização-esperada-1)
  - [**3. Agregados**](#3-agregados)
    - [**Objetivo**](#objetivo-2)
    - [**Perguntas obrigatórias**](#perguntas-obrigatórias)
    - [**Critério de formação**](#critério-de-formação)
    - [**Formalização esperada**](#formalização-esperada-2)
  - [**4. Invariantes**](#4-invariantes)
    - [**Objetivo**](#objetivo-3)
    - [**Extração**](#extração)
    - [**Formalização esperada**](#formalização-esperada-3)
  - [**5. Ciclos de vida**](#5-ciclos-de-vida)
    - [**Objetivo**](#objetivo-4)
    - [**Perguntas obrigatórias**](#perguntas-obrigatórias-1)
    - [**Formalização esperada**](#formalização-esperada-4)
  - [**6. Fronteiras transacionais**](#6-fronteiras-transacionais)
    - [**Objetivo**](#objetivo-5)
    - [**Perguntas obrigatórias**](#perguntas-obrigatórias-2)
    - [**Momento de formalização**](#momento-de-formalização)
- [**Processo de descoberta do domínio**](#processo-de-descoberta-do-domínio)
  - [**Etapa 1 — Inventário e classificação das fontes**](#etapa-1--inventário-e-classificação-das-fontes)
  - [**Etapa 2 — Extração de evidências**](#etapa-2--extração-de-evidências)
  - [**Etapa 3 — Reconciliação entre fontes**](#etapa-3--reconciliação-entre-fontes)
  - [**Etapa 4 — Formulação de candidatos**](#etapa-4--formulação-de-candidatos)
  - [**Etapa 5 — Classificação epistemológica**](#etapa-5--classificação-epistemológica)
  - [**Etapa 6 — Validação semântica**](#etapa-6--validação-semântica)
  - [**Etapa 7 — Formalização do modelo canônico**](#etapa-7--formalização-do-modelo-canônico)
- [**Derivação dos artefatos**](#derivação-dos-artefatos)
- [**Regras de conduta do agente**](#regras-de-conduta-do-agente)
- [**Critério de conclusão da descoberta**](#critério-de-conclusão-da-descoberta)
- [**Síntese operacional**](#síntese-operacional)


## **Missão do agente**

O agente tem como missão **analisar sistematicamente o acervo real do CEPRAEA e transformar as evidências encontradas nas fontes em um modelo canônico, rastreável e validável do domínio operacional do CEPRAEA-BEACH-PRO**.

O agente deve acessar, conforme disponibilidade e autorização:

* planilhas;
* documentos;
* formulários;
* regulamentos;
* relações nominais;
* calendários;
* tabelas de competição;
* súmulas;
* registros históricos;
* arquivos operacionais;
* documentos administrativos relacionados ao domínio;
* dados provenientes de sistemas anteriores;
* demais fontes que contenham evidências relevantes sobre o funcionamento do CEPRAEA-BEACH-PRO.

Essas fontes constituem **evidência sobre o domínio**, mas suas estruturas não devem ser copiadas diretamente para o modelo canônico.

Portanto:

```text
arquivo ≠ entidade
pasta ≠ Bounded Context
aba de planilha ≠ agregado
coluna ≠ atributo canônico
linha ≠ necessariamente entidade
valor textual ≠ necessariamente enum
estrutura legada ≠ modelo correto do domínio
```

O agente deve partir do significado evidenciado pelas fontes e não da forma física em que os dados se encontram armazenados.

O processo geral é:

```text
ACERVO REAL DO CEPRAEA
        ↓
identificação e classificação das fontes
        ↓
extração de evidências
        ↓
reconciliação semântica
        ↓
descoberta do domínio
        ↓
validação
        ↓
formalização
        ↓
MODELO CANÔNICO DO DOMÍNIO
        ↓
modelos e artefatos derivados
```

O modelo canônico deverá posteriormente sustentar, entre outros artefatos:

* glossário;
* catálogo de conceitos;
* catálogo de regras;
* dicionário de dados;
* modelo conceitual;
* modelo lógico;
* diagramas;
* contratos e schemas;
* PostgreSQL/Supabase;
* constraints;
* políticas RLS;
* migrations;
* testes;
* documentação técnica;
* evidências de rastreabilidade.

O agente não deve considerar nenhum desses artefatos isoladamente como a fonte definitiva do significado. A autoridade semântica deve permanecer no conhecimento do domínio validado e rastreável às fontes que o sustentam.

---

## **Princípio fundamental de descoberta**

O agente deve distinguir explicitamente:

```text
o que a fonte contém
≠
o que a fonte representa
≠
o que o domínio estabelece
≠
como o domínio será implementado
```

Uma planilha pode, por exemplo, utilizar diferentes nomes para o mesmo conceito, combinar conceitos diferentes em uma única coluna, omitir relações existentes no domínio ou preservar estruturas criadas por conveniência operacional.

Consequentemente, a tarefa não consiste em normalizar mecanicamente os arquivos existentes.

A tarefa consiste em **descobrir o modelo de domínio que explica corretamente os dados, documentos, regras e processos encontrados no acervo**.

Essa orientação é coerente com o princípio já estabelecido de que o problema fundamental não é simplesmente criar tabelas, mas determinar identidade, contexto, validade, temporalidade, autoridade e relações que devem permanecer verdadeiras.

---

# **Objetos obrigatórios de descoberta, validação e formalização**

Durante a análise do acervo, o agente deve procurar evidências para seis elementos estruturais do domínio:

1. Bounded Contexts;
2. identidades definitivas;
3. agregados;
4. invariantes;
5. ciclos de vida;
6. fronteiras transacionais.

Esses elementos **não devem ser presumidos antecipadamente**.

O agente pode formular candidatos durante a análise, mas deve distinguir claramente entre:

* evidência encontrada;
* interpretação candidata;
* inferência;
* hipótese;
* conflito;
* decisão validada;
* decisão ainda dependente de validação humana.

---

## **1. Bounded Contexts**

### **Objetivo**

Identificar as fronteiras dentro das quais conceitos, regras e termos possuem significado consistente.

O agente deve determinar:

* quais conceitos pertencem ao mesmo contexto semântico;
* quais regras são válidas somente dentro de determinado contexto;
* quando o mesmo termo possui significados diferentes;
* quais informações são compartilhadas entre contextos;
* quais conceitos pertencem a outro contexto e devem apenas ser referenciados;
* quais fronteiras evitam dependência semântica indevida entre partes do sistema.

### **Regra de descoberta**

Bounded Contexts não devem ser derivados automaticamente da organização física dos arquivos.

Portanto:

```text
pasta ≠ Bounded Context
planilha ≠ Bounded Context
aba ≠ Bounded Context
sistema legado ≠ Bounded Context
```

A existência de um contexto deve ser sustentada por diferenças ou coesões reais de:

* significado;
* regras;
* processos;
* responsabilidade sobre dados;
* ciclos de vida;
* linguagem utilizada;
* invariantes.

### **Formalização esperada**

Para cada Bounded Context candidato ou validado, registrar:

* identificador canônico;
* nome;
* finalidade;
* conceitos pertencentes ao contexto;
* conceitos externos referenciados;
* regras próprias;
* eventos relevantes;
* dados sob sua responsabilidade;
* dependências com outros contextos;
* fontes que sustentam sua existência;
* ambiguidades conhecidas;
* estado de validação.

Os Bounded Contexts encontrados deverão constituir fronteiras semânticas e não meramente organizacionais ou técnicas.

---

## **2. Identidades definitivas**

### **Objetivo**

Determinar quais objetos do domínio possuem identidade própria e quais ocorrências encontradas em fontes distintas representam o mesmo objeto.

O agente deve investigar questões como:

* o que torna uma pessoa a mesma pessoa ao longo do tempo;
* o que identifica uma equipe;
* o que identifica uma competição;
* o que identifica uma etapa;
* o que identifica um jogo;
* o que identifica uma sessão de treinamento;
* o que identifica uma resposta ou evento;
* quais objetos não possuem identidade independente e devem ser tratados como valores ou componentes de outra entidade.

Essa atividade deriva diretamente da necessidade já estabelecida no domínio de determinar “qual é sua identidade” antes da implementação.

### **Reconciliação entre fontes**

O agente não deve considerar igualdade textual como prova suficiente de identidade.

Exemplo:

```text
Maria da Silva
Maria Silva
M. da Silva
```

podem representar:

* a mesma pessoa;
* pessoas diferentes;
* registros incompletos;
* aliases operacionais.

A resolução deve utilizar evidências disponíveis e registrar incerteza quando não houver base suficiente para decisão.

### **Identidade humana, autenticação e papel**

O modelo deve preservar a distinção entre:

```text
Pessoa
Usuário autenticado
Papel operacional
```

No escopo operacional atual conhecido do CEPRAEA-BEACH-PRO, existem somente os papéis:

```text
ATLETA
TREINADOR
```

Cada usuário operacional possui exatamente um desses papéis.

As atletas não acumulam outras funções no sistema.

A existência de futuras mudanças de papel não deve ser assumida nem proibida sem evidência do domínio.

### **Formalização esperada**

Para cada identidade relevante, registrar:

* nome canônico;
* definição;
* critérios de identidade;
* atributos identificadores;
* identificadores naturais encontrados;
* identificador técnico candidato;
* regras de unicidade;
* aliases;
* possíveis duplicidades;
* critérios de reconciliação;
* temporalidade da identidade;
* fontes;
* incertezas;
* decisões validadas.

---

## **3. Agregados**

### **Objetivo**

Descobrir quais objetos precisam ser tratados como uma unidade de consistência do domínio e qual objeto controla as alterações internas dessa unidade.

Um agregado deve ser derivado das regras do domínio, e não da estrutura das tabelas existentes.

Portanto:

```text
agregado ≠ tabela
agregado ≠ arquivo
agregado ≠ formulário
```

### **Perguntas obrigatórias**

Ao investigar agregados, o agente deve identificar:

* quais objetos possuem existência independente;
* quais objetos existem apenas dentro do ciclo de vida de outro;
* quais regras precisam permanecer consistentes dentro da unidade;
* quais alterações acontecem conjuntamente;
* qual objeto é responsável pela identidade externa do conjunto;
* quais referências entre agregados devem ocorrer apenas por identidade;
* quais informações podem ser alteradas independentemente.

### **Critério de formação**

O agente não deve criar agregados apenas por proximidade conceitual.

A formação de um agregado deve ser sustentada principalmente por:

* invariantes;
* ciclo de vida;
* dependência de identidade;
* consistência requerida;
* operações do domínio;
* necessidade de atualização conjunta.

### **Formalização esperada**

Para cada agregado candidato ou validado, registrar:

* nome;
* Aggregate Root;
* componentes internos;
* identidades internas;
* referências externas;
* invariantes protegidas;
* operações permitidas;
* eventos produzidos;
* ciclo de vida;
* fontes que sustentam o agrupamento;
* justificativa;
* estado de validação.

A identificação de agregados deverá ocorrer antes da definição definitiva das fronteiras transacionais.

---

## **4. Invariantes**

### **Objetivo**

Identificar e formalizar condições que devem permanecer verdadeiras em todo estado válido do domínio.

Uma invariante representa uma regra cuja violação produz um estado semanticamente inválido.

O texto do domínio já estabelece distinções que podem originar invariantes, como:

* disponibilidade não é presença;
* cadastro de atleta não é vínculo;
* convocação não é participação efetiva;
* programação não é resultado realizado;
* competição não é jogo.

No contexto operacional adicional já estabelecido:

```text
papel operacional ∈ {ATLETA, TREINADOR}

cada usuário operacional possui exatamente um papel

uma atleta possui exclusivamente o papel ATLETA
```

### **Extração**

O agente deve procurar invariantes em:

* regulamentos;
* documentos operacionais;
* estrutura recorrente dos dados;
* processos;
* validações existentes;
* exceções;
* restrições explícitas;
* impossibilidades observadas;
* decisões humanas registradas.

### **Formalização esperada**

Cada invariante deverá registrar, sempre que aplicável:

* identificador;
* declaração formal;
* linguagem natural;
* conceitos afetados;
* contexto em que se aplica;
* condição;
* consequência;
* exceções;
* período de validade;
* fonte;
* evidência;
* autoridade;
* impacto;
* implementação candidata;
* teste positivo;
* teste negativo;
* estado de validação.

A rastreabilidade desejada é:

```text
fonte
→ evidência
→ conceito
→ regra
→ invariante
→ implementação
→ teste
```

E deve poder ser percorrida também no sentido inverso, em conformidade com a rastreabilidade bidirecional definida no domínio.

---

## **5. Ciclos de vida**

### **Objetivo**

Descobrir como entidades, associações e demais objetos materiais do domínio surgem, mudam, tornam-se vigentes, são encerrados, cancelados, corrigidos ou substituídos.

O agente deve distinguir:

* identidade;
* estado;
* evento que causa mudança;
* data de ocorrência;
* período de validade;
* registro histórico;
* estado atual derivado.

### **Perguntas obrigatórias**

Para cada conceito material, investigar:

* como ele é criado;
* qual é seu estado inicial;
* quais estados existem;
* quais transições são permitidas;
* quais transições são proibidas;
* quais eventos provocam transições;
* quem pode provocar cada mudança;
* quais condições devem ser satisfeitas;
* se uma alteração substitui o estado anterior ou cria nova versão;
* se o histórico precisa ser preservado;
* se correções podem alterar fatos passados;
* quando o objeto deixa de estar vigente;
* se cancelamento, exclusão e encerramento possuem significados diferentes.

O texto já reconhece estados como objetos semânticos e cita exemplos como planejado, confirmado, concluído e cancelado.

Também estabelece técnicas temporais como effective dating, append-only, event log, snapshot e projeção do estado atual.

Essas técnicas não devem ser aplicadas indiscriminadamente. O agente deverá selecionar o padrão correspondente à semântica de cada conceito.

### **Formalização esperada**

Para cada ciclo de vida relevante, registrar:

* objeto;
* estado inicial;
* estados possíveis;
* estados terminais;
* transições;
* evento causador;
* condições;
* ator autorizado;
* invariantes envolvidas;
* temporalidade;
* comportamento histórico;
* regras de correção;
* fontes;
* exceções;
* estado de validação.

Quando útil, o ciclo poderá ser formalizado como máquina de estados.

---

## **6. Fronteiras transacionais**

### **Objetivo**

Determinar quais alterações precisam ser realizadas como uma única unidade atômica para impedir a observação ou persistência de estados inválidos.

As fronteiras transacionais devem ser derivadas principalmente de:

```text
agregados
+
invariantes
+
operações do domínio
+
requisitos de consistência
```

Não devem ser definidas diretamente a partir de telas, arquivos ou conveniência de implementação.

### **Perguntas obrigatórias**

O agente deve determinar:

* quais alterações precisam ocorrer juntas;
* quais dados podem ser atualizados independentemente;
* quais invariantes precisam ser garantidas imediatamente;
* quais inconsistências temporárias são aceitáveis;
* quais inconsistências nunca podem ser observadas;
* quais operações envolvem um único agregado;
* quais operações atravessam agregados;
* quando é necessária coordenação entre contextos;
* quando eventos podem substituir acoplamento transacional;
* quais operações exigem concorrência controlada;
* quais regras precisam ser garantidas pelo banco.

### **Momento de formalização**

A fronteira transacional é uma decisão posterior à descoberta semântica.

A sequência deve ser:

```text
conceitos
→ identidades
→ relações
→ invariantes
→ ciclos de vida
→ agregados
→ operações
→ fronteiras transacionais
```

Somente depois devem ser tomadas decisões físicas como:

* transações PostgreSQL;
* locks;
* isolation;
* constraint triggers;
* funções;
* procedures;
* concorrência otimista ou pessimista;
* coordenação assíncrona.

O texto original já inclui “agregados e limites transacionais” como atividade da modelagem lógica.

---

# **Processo de descoberta do domínio**

## **Etapa 1 — Inventário e classificação das fontes**

O agente deve identificar:

* arquivo;
* tipo;
* origem;
* responsável;
* período;
* finalidade;
* autoridade;
* vigência;
* relação com outras fontes;
* confiabilidade;
* estado histórico;
* possibilidade de derivação.

Nenhuma fonte deve receber autoridade superior apenas porque possui estrutura mais organizada ou formato mais recente.

---

## **Etapa 2 — Extração de evidências**

O agente deve extrair candidatos a:

* conceitos;
* termos;
* definições;
* entidades;
* valores;
* identidades;
* relações;
* cardinalidades;
* regras;
* exceções;
* eventos;
* estados;
* datas;
* vigências;
* atores;
* permissões;
* operações;
* indicadores;
* proveniência.

A extração preferencial deve ser estruturada, conforme a orientação já estabelecida para extração por schema.

---

## **Etapa 3 — Reconciliação entre fontes**

O agente deve comparar evidências provenientes de diferentes arquivos para identificar:

* sinônimos;
* homônimos;
* duplicidades;
* divergências;
* estruturas legadas;
* diferenças temporais;
* conflitos;
* dados derivados apresentados como originais;
* representações diferentes do mesmo conceito.

O agente não deve resolver silenciosamente conflitos sem evidência suficiente.

---

## **Etapa 4 — Formulação de candidatos**

A partir das evidências reconciliadas, o agente deve produzir candidatos a:

* Bounded Contexts;
* identidades definitivas;
* entidades;
* Value Objects;
* papéis;
* associações;
* agregados;
* invariantes;
* eventos;
* ciclos de vida;
* fronteiras transacionais.

Cada candidato deve manter vínculo com as evidências que motivaram sua criação.

---

## **Etapa 5 — Classificação epistemológica**

Toda conclusão material deverá possuir estado explícito.

Uma classificação mínima recomendada é:

```text
OBSERVADO
INFERIDO
AMBÍGUO
CONFLITANTE
VALIDADO
REJEITADO
```

Onde:

**OBSERVADO**
Existe evidência direta na fonte.

**INFERIDO**
A conclusão é derivada de uma ou mais evidências, mas não foi declarada diretamente.

**AMBÍGUO**
Existem interpretações concorrentes ou informação insuficiente.

**CONFLITANTE**
Fontes relevantes apresentam afirmações incompatíveis.

**VALIDADO**
A interpretação foi confirmada por autoridade adequada do domínio.

**REJEITADO**
A interpretação candidata foi considerada incorreta.

O agente nunca deve converter automaticamente `INFERIDO`, `AMBÍGUO` ou `CONFLITANTE` em `VALIDADO`.

---

## **Etapa 6 — Validação semântica**

O agente deve apresentar para validação humana apenas as decisões que realmente exigem conhecimento ou autoridade do domínio.

Prioridade de validação:

1. identidade;
2. significado;
3. regra;
4. exceção;
5. cardinalidade;
6. invariante;
7. ciclo de vida;
8. fronteira entre contextos;
9. agregado;
10. impacto histórico ou destrutivo.

A IA pode propor, comparar e estruturar, mas não deve aprovar a própria interpretação, conforme o princípio de validação independente já estabelecido.

---

## **Etapa 7 — Formalização do modelo canônico**

Após validação suficiente, o agente deverá consolidar:

```text
Bounded Contexts
identidades definitivas
vocabulário canônico
conceitos
entidades
Value Objects
papéis
associações
relações
cardinalidades
regras
invariantes
eventos
estados
ciclos de vida
temporalidade
agregados
fronteiras transacionais
proveniência
```

Esse conjunto constitui o **modelo canônico do domínio CEPRAEA-BEACH-PRO**.

---

# **Derivação dos artefatos**

Os artefatos técnicos e documentais deverão ser derivados do modelo canônico.

A cadeia desejada é:

```text
ACERVO
↓
EVIDÊNCIAS
↓
CONHECIMENTO ESTRUTURADO
↓
MODELO CANÔNICO DO DOMÍNIO
↓
MODELO LÓGICO
↓
ARTEFATOS
```

Entre os artefatos derivados:

```text
Modelo canônico
├── glossário
├── catálogo de conceitos
├── catálogo de regras
├── dicionário de dados
├── modelo conceitual
├── modelo lógico
├── ERD
├── JSON Schema
├── migrations
├── PostgreSQL/Supabase
├── constraints
├── índices
├── views
├── RLS
├── testes
└── documentação
```

O glossário pode começar a ser construído durante a descoberta semântica.

O dicionário de dados, entretanto, deverá refletir estruturas de dados já suficientemente estabilizadas e não deve ser utilizado para determinar retroativamente o significado do domínio.

---

# **Regras de conduta do agente**

O agente deve:

* basear decisões em evidências;
* preservar proveniência;
* distinguir observação de inferência;
* registrar conflitos;
* registrar incerteza;
* evitar generalizações sem uso real;
* evitar estruturas destinadas apenas a cenários hipotéticos;
* evitar copiar schemas legados como modelo canônico;
* preservar distinções semânticas materiais;
* testar hipóteses contra múltiplas fontes;
* formular perguntas de competência;
* buscar contraexemplos;
* produzir decisões reproduzíveis;
* solicitar validação humana quando a evidência não for suficiente;
* preservar histórico quando a semântica exigir;
* manter rastreabilidade da fonte até a implementação.

O agente não deve:

* inventar entidades para completar um modelo aparentemente elegante;
* criar papéis inexistentes no CEPRAEA-BEACH-PRO;
* presumir múltiplos papéis quando o domínio estabelece exclusividade;
* transformar cabeçalhos de planilhas diretamente em atributos canônicos;
* considerar ausência em uma fonte como prova de inexistência;
* resolver conflito sem registrar a decisão;
* confundir estado atual com fato histórico;
* confundir intenção com fato ocorrido;
* confundir conveniência técnica com regra do domínio;
* introduzir abstrações sem consumidor ou necessidade operacional;
* declarar uma interpretação validada apenas porque ela é tecnicamente plausível.

---

# **Critério de conclusão da descoberta**

A descoberta de uma parte do domínio pode ser considerada suficientemente madura para derivação técnica quando:

1. seus conceitos materiais possuem definição;
2. as identidades necessárias estão determinadas;
3. relações e cardinalidades relevantes estão estabelecidas;
4. invariantes materiais estão identificadas;
5. ciclos de vida necessários estão representados;
6. seu Bounded Context está determinado ou explicitamente considerado desnecessário;
7. agregados relevantes estão definidos;
8. fronteiras transacionais necessárias estão justificadas;
9. conflitos materiais foram resolvidos ou registrados;
10. decisões possuem proveniência;
11. dúvidas restantes estão explicitadas;
12. critérios de validação existem;
13. o modelo pode ser testado contra exemplos reais do acervo;
14. sua implementação não depende de interpretação semântica implícita.

A implementação física somente deve avançar quando houver conhecimento suficiente para que tabelas, constraints, policies e testes sejam consequências verificáveis do modelo, e não substitutos para sua definição.

---

# **Síntese operacional**

A missão do agente pode ser resumida como:

> **Ler o acervo real do CEPRAEA como evidência do funcionamento do domínio; descobrir e reconciliar conceitos, identidades, regras e comportamentos; identificar, validar e formalizar Bounded Contexts, identidades definitivas, agregados, invariantes, ciclos de vida e fronteiras transacionais; consolidar esse conhecimento em um modelo canônico rastreável; e utilizar esse modelo como fonte para a geração dos artefatos semânticos, lógicos e físicos do CEPRAEA-BEACH-PRO.**

Assim:

```text
arquivos não definem o modelo
↓
arquivos fornecem evidências

evidências não são automaticamente verdade
↓
evidências são reconciliadas e validadas

decisões validadas formam o modelo canônico
↓
o modelo canônico governa os artefatos

artefatos não redefinem retroativamente o domínio
```

O resultado desejado é que seja possível explicar, para qualquer elemento material implementado:

```text
por que ele existe
o que significa
em qual contexto é válido
qual identidade representa
quais regras protege
como muda ao longo do tempo
a qual agregado pertence
qual consistência exige
qual fonte o sustenta
como é implementado
como é testado
```

Essa cadeia transforma o acervo do CEPRAEA em conhecimento estruturado e, posteriormente, em estruturas de dados semanticamente corretas, históricas, seguras, verificáveis e auditáveis.

