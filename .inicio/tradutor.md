# Norma de tradução de linguagem natural
<!-- markdownlint-disable MD007 -->
- [Norma de tradução de linguagem natural](#norma-de-tradução-de-linguagem-natural)
  - [Modelagem de Domínio](#modelagem-de-domínio)
  - [Estratégia de tradução](#estratégia-de-tradução)
  - [`REG-TRAD-001` — Preservação por congelamento de contratos](#reg-trad-001--preservação-por-congelamento-de-contratos)
    - [Versão e política de fechamento](#versão-e-política-de-fechamento)
    - [Dicionário fechado de campos](#dicionário-fechado-de-campos)
    - [Segmentação determinística](#segmentação-determinística)
    - [Enums canônicos](#enums-canônicos)
    - [Tabela fechada de classificação](#tabela-fechada-de-classificação)
    - [Exemplos de decisão](#exemplos-de-decisão)
  - [Classificação total](#classificação-total)
  - [Precedência](#precedência)
  - [Congelamento e restauração](#congelamento-e-restauração)
    - [Preservação relacional e proposicional](#preservação-relacional-e-proposicional)
    - [Condição de falha](#condição-de-falha)
  - [Identificadores que devem ser protegidos](#identificadores-que-devem-ser-protegidos)
  - [Glossário bilíngue controlado](#glossário-bilíngue-controlado)
  - [Matriz de rastreabilidade semântica](#matriz-de-rastreabilidade-semântica)
  - [Como evitar duas fontes concorrentes](#como-evitar-duas-fontes-concorrentes)
    - [Solução obrigatória](#solução-obrigatória)
  - [Verificações objetivas](#verificações-objetivas)
    - [1. Equivalência estrutural](#1-equivalência-estrutural)
    - [2. Equivalência dos contratos](#2-equivalência-dos-contratos)
    - [3. Ausência de japonês residual](#3-ausência-de-japonês-residual)
    - [4. Revisão linguística](#4-revisão-linguística)
    - [5. Não corrigir inconsistências durante a tradução](#5-não-corrigir-inconsistências-durante-a-tradução)
  - [Gates finais de aceitação](#gates-finais-de-aceitação)

<!-- markdownlint-enable MD007 -->

> **Status normativo:** NORMA OBRIGATÓRIA.
> **Contexto deste documento:** este documento governa toda tradução de linguagem natural de artefatos normativos do repositório. Seus termos `DEVE`, `NÃO DEVE`, `PODE` e `FALHA` têm sentido normativo. Uma tradução somente pode substituir sua origem quando cumprir todos os gates definidos nesta norma.

Perfis de execução PODEM restringir esta norma para um artefato, idioma ou
estrutura específicos, mas NÃO PODEM relaxar seus gates. Evidências registram
resultados de uma execução e NÃO constituem regras. A dependência permitida é
unidirecional: evidência → perfil → norma.

Em caso de conflito entre esta norma e uma orientação não normativa, esta
norma prevalece. Alterar uma regra, classe, precedência ou gate deste documento
é uma alteração normativa e exige revisão explícita de impacto.

## Modelagem de Domínio

| Campo | Definição normativa |
| --- | --- |
| Domínio de conhecimento | Tradução controlada de documentação técnica e normativa |
| Subdomínios | Linguagem natural, Markdown, contratos técnicos, rastreabilidade e validação |
| Tema principal | Preservação estrutural, contratual, relacional e proposicional |
| Escopo positivo | Tradução de conteúdo humano entre idiomas sem alterar o comportamento definido |
| Escopo negativo | Correção, adaptação de plataforma, refatoração, atualização tecnológica ou mudança normativa |
| Contexto válido | Artefato de origem fixado por hash e submetido ao processo completo desta norma |
| Contexto inválido | Origem mutável, tradução parcial, contrato sem classificação ou validação incompleta |
| Boa prática obrigatória | Falhar de modo fechado diante de qualquer ambiguidade ou divergência |

***

*Não existe uma prova matemática de equivalência para tradução de linguagem natural. O que se pode obter é uma garantia forte, objetiva e auditável por meio de invariantes estruturais, contratos protegidos, rastreabilidade proposição a proposição e revisão bilíngue.*

***

## Estratégia de tradução

Estratégia obrigatória do repositório:

> *Tornar a versão em português o **único arquivo canônico***

<center>
<b>documento-origem-{idioma}.md<br></b>
            │     <br>  
            |  <br><i>git mv</i>
<br>        |    <br>  +
<br>        |   <br>Tradução
<br>        |
<br>        ▼<br>  
<b>documento-canônico.md</b> ← <i>única fonte normativa no idioma-alvo</i></b></center><br><i><center>A proveniência da origem permanece recuperável por Git ou hash criptográfico, mas não como uma segunda cópia ativa.</center><br><center>Quando a origem ainda não estiver versionada, sua preservação auditável DEVE
ser feita por hash criptográfico e manifesto de equivalência antes da remoção
do worktree.<br><br><b>Nesse caso, é proibido afirmar que existe histórico Git prévio.
</i></center></b>

***

## `REG-TRAD-001` — Preservação por congelamento de contratos
<!-- Criar a tabela com o dicionário dos campos, desta seção com um id de identificação para cada campo -->

<!-- Falta explicar como funciona a classificação dos segmentos dos conteúdos. Quais são as regras, os métodos, os critérios e quais são so campos utilizados nessa classificação. Montar a tabela de classicação dos conteúdos com os campos especificados. Se um agente inventar um campo ou uma classificação é BLOCKED -->

### Versão e política de fechamento

O contrato de campos e enums desta norma usa `schema_version: 1.0.0`. Nomes de
campo, classes, regras, estados e erros são comparados byte a byte, com diferença
de caixa significativa. Alias, coerção, correção ortográfica ou normalização
silenciosa são proibidos.

Uma extensão exige revisão normativa, incremento de versão conforme SemVer,
análise de compatibilidade e, quando incompatível, procedimento explícito de
migração. Campo, classe ou regra desconhecidos resultam em `BLOCKED`.

### Dicionário fechado de campos

| ID | Campo canônico | Tipo/cardinalidade | Obrigatório | Origem | Consumidor | Domínio e invariantes |
| --- | --- | --- | :---: | --- | --- | --- |
| `F-001` | `schema_version` | string/1 | Sim | Norma | Parser, validador | SemVer; nesta versão, `1.0.0` |
| `F-002` | `translation_run_id` | string/1 | Sim | Orquestrador | Todos | `TRUN-` + ULID; imutável e único |
| `F-003` | `source_artifact` | path/1 | Sim | Solicitação | Parser | Caminho lógico resolvido dentro do escopo autorizado |
| `F-004` | `source_artifact_sha256` | SHA-256/1 | Sim | Fixação | Todos | 64 hex minúsculos calculados sobre bytes originais |
| `F-005` | `source_encoding` | enum/1 | Sim | Fixação | Parser | Exatamente `UTF-8`; BOM é preservado como bytes |
| `F-006` | `working_copy` | path/1 | Sim | Orquestrador | Tradutor | Diferente da origem; única área em que placeholders podem existir |
| `F-007` | `target_artifact` | path/1 | Sim | Perfil | Restaurador | Caminho canônico autorizado; diferente da origem durante a execução |
| `F-008` | `source_language` | BCP 47/1 | Sim | Perfil | Tradutor | Tag canônica declarada; não inferida silenciosamente |
| `F-009` | `target_language` | BCP 47/1 | Sim | Perfil | Tradutor | Tag canônica declarada e distinta da origem |
| `F-010` | `segment_id` | string/1 por segmento | Sim | Segmentador | Classificador | `SEG-` + seis dígitos; único e ordenado pelo byte inicial |
| `F-011` | `source_ast_path` | string/1 por segmento | Sim | Segmentador | Comparador | Gramática definida na seção de segmentação; único no run |
| `F-012` | `source_byte_start` | inteiro/1 | Sim | Segmentador | Restaurador | Inclusivo, `>= 0` e menor que `source_byte_end` |
| `F-013` | `source_byte_end` | inteiro/1 | Sim | Segmentador | Restaurador | Exclusivo, `<=` tamanho do blob e maior que o início |
| `F-014` | `source_value_base64` | base64/1 | Sim | Segmentador | Restaurador | Codifica exatamente o intervalo original, sem normalização |
| `F-015` | `source_value_sha256` | SHA-256/1 | Sim | Segmentador | Validador | Hash dos bytes decodificados de `source_value_base64` |
| `F-016` | `node_type` | enum/1 | Sim | Parser | Classificador | Um valor de `NODE_TYPE`; caixa significativa |
| `F-017` | `classification` | enum/1 | Sim | Classificador | Tradutor | Um valor de `CLASSIFICATION` |
| `F-018` | `classification_rule_id` | enum/1 | Sim | Classificador | Auditor | Uma regra `CR-*` cadastrada; `CR-999` apenas para ambiguidade |
| `F-019` | `placeholder_id` | string/0..1 | Condicional | Congelador | Restaurador | Obrigatório somente para `PROTECTED_EXACT`; único por ocorrência |
| `F-020` | `occurrence` | inteiro/1 | Sim | Segmentador | Validador | Começa em 1 para valores repetidos e não possui lacunas |
| `F-021` | `relation_ids` | lista/0..n | Condicional | Perfil | Comparador | IDs únicos e existentes; obrigatório quando houver relação contratual |
| `F-022` | `translation_value` | string/0..1 | Condicional | Tradutor | Comparador | Somente para `TRANSLATABLE_CONTROLLED`; nunca contém placeholder não restaurado |
| `F-023` | `proposition_ids` | lista/0..n | Condicional | Revisor | Validador | Obrigatório para prosa normativa; IDs únicos e existentes |
| `F-024` | `validation_status` | enum/1 | Sim | Validador | Gate | Um valor de `VALIDATION_STATUS`; não armazena código de erro |
| `F-025` | `error_codes` | lista/0..n | Sim | Validadores | Gate | Somente valores de `ERROR_CODE`, sem duplicatas e em ordem de detecção |

Regras condicionais fazem parte do schema: campo obrigatório sob sua condição
não pode ser omitido; fora da condição, sua presença é proibida. Propriedades
adicionais são proibidas. Sinônimos em português usados em versões anteriores,
como `segmento_conteúdo`, não constituem campos válidos.

### Segmentação determinística

O parser normativo é `markdown-it` `14.3.0`, preset `default`, com opções
`html: true`, `breaks: false`, `linkify: false` e `typographer: false`. A entrada
DEVE ser decodificada como UTF-8 estrito sem normalização Unicode e analisada a
partir dos bytes fixados por `source_artifact_sha256`.

O segmentador DEVE:

1. construir o token stream do parser fixado;
2. mapear linhas do token stream para intervalos dos bytes originais;
3. decompor conteúdo inline e misto em spans contíguos e não sobrepostos;
4. cobrir o intervalo completo `[0, tamanho_do_blob)`, incluindo whitespace,
   quebras de linha, BOM e delimitadores;
5. ordenar spans por `source_byte_start` e gerar `SEG-000001`, `SEG-000002` etc.;
6. atribuir um AST path antes da classificação;
7. bloquear com `E_PARSE_FAILED` ou `E_UNCOVERED_SOURCE_BYTES` quando não puder
   garantir a estrutura ou a cobertura integral.

A gramática do endereço lógico é:

```text
document/block[NNNN]/node_type/inline[NNNN]/span[NNNN]
```

Componentes inexistentes são omitidos, nunca preenchidos com índice fictício.
Índices usam quatro dígitos, começam em `0001` e representam a ordem entre
irmãos do mesmo pai. Offsets são medidos em bytes, não em caracteres Unicode.

Dois segmentos não podem se sobrepor. Segmentos adjacentes DEVEM satisfazer
`anterior.source_byte_end == próximo.source_byte_start`. O primeiro começa em 0
e o último termina no tamanho exato do blob. A repetição sobre o mesmo hash DEVE
produzir os mesmos segmentos, IDs, paths e hashes.

### Enums canônicos

| Enum | Valores permitidos |
| --- | --- |
| `CLASSIFICATION` | `PROTECTED_EXACT`, `TRANSLATABLE_CONTROLLED`, `MARKDOWN_SYNTAX`, `AMBIGUOUS` |
| `NODE_TYPE` | `bom`, `whitespace`, `heading`, `paragraph`, `text`, `emphasis`, `strong`, `blockquote`, `bullet_list`, `ordered_list`, `list_item`, `table`, `table_row`, `table_cell`, `link`, `image`, `code_inline`, `code_fence`, `html_inline`, `html_block`, `thematic_break`, `mermaid`, `front_matter`, `unknown` |
| `VALIDATION_STATUS` | `NOT_RUN`, `PASS`, `FAIL`, `BLOCKED` |
| `ERROR_CODE` | `E_SOURCE_NOT_FIXED`, `E_PARSE_FAILED`, `E_UNCOVERED_SOURCE_BYTES`, `E_UNCLASSIFIED_SEGMENT`, `E_UNKNOWN_FIELD`, `E_UNKNOWN_CLASS`, `E_UNKNOWN_CLASSIFICATION_RULE`, `E_CLASSIFICATION_CONFLICT`, `E_PLACEHOLDER_MISSING`, `E_PLACEHOLDER_DUPLICATED`, `E_PLACEHOLDER_COLLISION`, `E_PROTECTED_VALUE_CHANGED`, `E_LOGICAL_POSITION_CHANGED`, `E_CARDINALITY_CHANGED`, `E_ASSOCIATION_CHANGED`, `E_CONTRACT_RELATION_CHANGED`, `E_SEMANTIC_SIGNATURE_CHANGED`, `E_UNMATCHED_SOURCE_PROPOSITION`, `E_TARGET_ADDITION_WITHOUT_SOURCE` |

### Tabela fechada de classificação

As regras são avaliadas por prioridade numérica decrescente. Uma regra somente
vence quando seu predicado é verdadeiro e nenhuma outra regra da mesma prioridade
produz classe diferente. Empate conflitante resulta em `CR-999`,
`E_CLASSIFICATION_CONFLICT` e `BLOCKED`.

| Regra | Prioridade | Predicado determinístico | Parte classificada | Classe |
| --- | ---: | --- | --- | --- |
| `CR-001` | 1000 | Span coincide com valor protegido declarado pelo perfil | Span coincidente | `PROTECTED_EXACT` |
| `CR-002` | 950 | `node_type` é `front_matter` | Bloco completo | `PROTECTED_EXACT` |
| `CR-003` | 900 | `node_type` é `code_inline` ou `code_fence` e não há exceção no perfil | Conteúdo e delimitadores | `PROTECTED_EXACT` |
| `CR-004` | 850 | Parte é destino de `link` ou `image` | URL/destino | `PROTECTED_EXACT` |
| `CR-005` | 840 | Parte é título humano de link, texto do link ou alt de imagem | Span textual | `TRANSLATABLE_CONTROLLED` |
| `CR-006` | 800 | Parte é ID, seta, estilo, cor, atributo ou delimitador Mermaid | Span de sintaxe | `PROTECTED_EXACT` |
| `CR-007` | 790 | Parte é rótulo humano Mermaid cadastrado pelo perfil | Span textual | `TRANSLATABLE_CONTROLLED` |
| `CR-008` | 750 | Parte é tag, nome de atributo ou delimitador HTML | Span de sintaxe | `PROTECTED_EXACT` |
| `CR-009` | 740 | Parte é texto visível em HTML suportado | Span textual | `TRANSLATABLE_CONTROLLED` |
| `CR-010` | 700 | Span é delimiter Markdown, pipe de tabela, marcador ou whitespace | Span estrutural | `MARKDOWN_SYNTAX` |
| `CR-011` | 650 | Texto contém termo normativo coberto pelo glossário do perfil | Span textual mínimo do termo | `TRANSLATABLE_CONTROLLED` |
| `CR-012` | 600 | `node_type` textual não contém valor protegido nem termo normativo desconhecido | Span textual | `TRANSLATABLE_CONTROLLED` |
| `CR-999` | 0 | Nenhuma regra decide ou regras empatadas divergem | Span completo | `AMBIGUOUS` |

Regras `CR-005`, `CR-007` e `CR-009` só se aplicam após decomposição do nó misto.
Sintaxe quebrada, extensão desconhecida, termo normativo sem glossário ou span
que não possa ser decomposto de modo total resultam em `CR-999`. Nenhum override
manual é permitido durante a execução.

### Exemplos de decisão

| Entrada/contexto | Regra | Resultado esperado |
| --- | --- | --- |
| `` `file_type` `` em código inline | `CR-003` | `PROTECTED_EXACT` |
| `[texto humano](path/file.md)` — texto | `CR-005` | `TRANSLATABLE_CONTROLLED` |
| `[texto humano](path/file.md)` — destino | `CR-004` | `PROTECTED_EXACT` |
| Pipe delimitador de tabela | `CR-010` | `MARKDOWN_SYNTAX` |
| ID de nó Mermaid | `CR-006` | `PROTECTED_EXACT` |
| Rótulo Mermaid autorizado no perfil | `CR-007` | `TRANSLATABLE_CONTROLLED` |
| Extensão Markdown desconhecida | `CR-999` | `AMBIGUOUS` e `BLOCKED` |

Alterações nos enums ou regras exigem nova versão normativa. Valores com caixa
divergente, hífen no lugar de underscore, alias legado ou ID não cadastrado são
desconhecidos e DEVEM produzir o código `E_UNKNOWN_*` correspondente.

Antes de qualquer tradução:
<!-- Verifique as regras escritas abaixo e valide a semantica para que sejam cumpridas sem riscos semanticos-->

**`REG-TRAD-001.1`**
> <b>*Se*</b>, classificação do `segmento_conteúdo` for `contrato_protegido`, <b>*então*</b> o `segmento_conteúdo` <b>*deve ser*</b> extraído e registrado no `manifesto_ordenado`.

<br>

**`REG-TRAD-001.2`**
><b>*Se*</b>, `segmento_conteúdo` for registrado em `manifesto_ordenado`, *<b>então</b>* no `segmento_local_original` *<b>deve ser*</b>  substituído por
um `placeholder_unico`.

<br>

**`REG-TRAD-001.3`**
><b>*Se*</b>, `segmento_classificado`
é somente `linguagem_natural_traduzível`, *<b>então</b>* o tradutor *<b>pode fazer</b>* modificações.

<br>

**`REG-TRAD-001.4`**
><b>*Se*</b>, o status for `traducao_concluida`, *<b>então</b>* cada  `placeholder_unico` *<b>deve ser*</b> restaurado com o valor original, byte a byte.

<br>

**`REG-TRAD-001.5`**
> <b>*Se*</b>, o status for
`segmento_sem_classificação`, `placeholder_ausente`, `placeholder_duplicado`, `valor_alterado`, `posição_alterada`,
`cardinalidade_alterada`, `associação_alterada` ou `relação_contratual_alterada`, *<b>então</b>* a operação *<b>deve falhar e bloquear*</b> a publicação do documento canônico.

<!-- o bloco de código abaixo é markdown? -->
```markdown
TRADUZIR(S) =
  restaurar(
    traduzir_somente_linguagem_natural(
      congelar_contratos(S)
    )
  )
```

`S` é o artefato de origem fixado por hash e `T` é o resultado traduzido.

## Classificação total
<!-- Analise o impacto da expansão de "## `REG-TRAD-001` — Preservação por congelamento de contratos", nesta seção para solucionar possivéis gaps, incoerencias, duplicidades e incoerencias -->

Cada segmento da origem DEVE receber exatamente uma destas classes:

| Classe | Regra operacional |
| --- | --- |
| `PROTECTED_EXACT` | Copiar e restaurar byte a byte; tradução proibida |
| `TRANSLATABLE_CONTROLLED` | Traduzir somente pelo glossário ou por equivalência proposicional |
| `MARKDOWN_SYNTAX` | Preservar a estrutura e a função sintática |
| `AMBIGUOUS` | Interromper a operação; publicação proibida |

São `PROTECTED_EXACT`: nomes de agentes, modelos, fases, valores de
`file_type`, caminhos, nomes de arquivos, glob patterns, siglas, gates,
referências de seção e capítulo, IDs Mermaid, direção de arestas, estilos,
cores, atributos e destinos de links.

São `TRANSLATABLE_CONTROLLED`: títulos humanos, descrições, notas, rótulos
visíveis, cabeçalhos descritivos e instruções processuais. Termos normativos
recorrentes DEVEM usar uma entrada única do glossário bilíngue.

São `MARKDOWN_SYNTAX`: níveis de título, delimitadores de tabela, listas,
blocos de citação, fences, sintaxe de links e sintaxe Mermaid.

Texto entre crases e conteúdo de bloco de código são `PROTECTED_EXACT` por
padrão. Exceções, como rótulos humanos dentro de Mermaid, DEVEM ser cadastradas
explicitamente antes da tradução.

## Precedência

Quando um segmento corresponder a mais de uma classe, aplicar esta precedência:

```text
PROTECTED_EXACT
  > MARKDOWN_SYNTAX
  > TRANSLATABLE_CONTROLLED
  > AMBIGUOUS
```

Em links Markdown, o destino é `PROTECTED_EXACT` e o texto humano é
`TRANSLATABLE_CONTROLLED`. Em uma expressão mista como
`design（条件付き）`, `design` é protegido e somente a condição é traduzível.

## Congelamento e restauração

Cada ocorrência protegida DEVE receber um placeholder com ID único e checksum:

```text
⟦KEEP:0042:sha256-do-valor⟧
```

O manifesto DEVE registrar, no mínimo:

```yaml
- id: KEEP-0042
  value: identificador-protegido
  source_location: ITEM-001.identifier
  class: protected_identifier
  occurrence: 1
  relation:
    owner: consumidor-contratual
    states: [estado-inicial, estado-final]
```

Na restauração, valor, quantidade, posição lógica e ordem relativa DEVEM ser
iguais aos da origem. Presença textual isolada não prova preservação.

### Preservação relacional e proposicional

Os contratos DEVEM ser comparados por projeções normalizadas:

```text
agent(name, model, role, phases)
ownership(file_type, owner, directory, cardinality, phases)
flow(source, artifacts, target)
activation(phase, agents, gate)
procedure(position, action, references, conditions)
```

Para linguagem natural, cada proposição normativa DEVE preservar esta assinatura:

```text
sujeito | predicado | objeto | modalidade | polaridade |
quantificador | condição | escopo temporal | referências
```

Obrigação não pode virar recomendação; negação não pode desaparecer; “exatamente
um” não pode virar “principal”; “a partir de” não pode virar “durante”; e uma
condição não pode virar regra incondicional.

A tradução é admissível somente quando:

```text
estrutura(T) = estrutura(S)
contratos(T) = contratos(S)
relações(T) = relações(S)
assinaturas_semânticas(T) ≡ assinaturas_semânticas(S)
cobertura(S → T) = 100%
adições_sem_origem(T) = 0
```

### Condição de falha

Aplica-se a política `AMBIGUOUS ⇒ FAIL`. Qualquer segmento não classificado,
contrato divergente, proposição sem destino, conteúdo novo sem origem ou gate
sem evidência torna o resultado `REJEITADO`. O tradutor NÃO DEVE corrigir,
modernizar, adaptar ou completar silenciosamente a origem.

## Identificadores que devem ser protegidos

> A tradução deve operar com uma regra explícita de *“copiar, não traduzir”* para estas categorias:

- identificadores de schema, enums, estados, códigos de erro e namespaces;
- nomes de agentes, modelos, fases e valores de tipos contratuais;
- caminhos, nomes de arquivos, URLs, anchors e glob patterns;
- siglas, gates, referências de seção e capítulo;
- IDs, direção, estilos, cores e atributos de diagramas;
- destinos de links e conteúdo de código protegido;
- todo valor adicional declarado por um perfil de execução aprovado.

O controle deve comparar não apenas se os tokens continuam presentes, mas também:

- quantidade de ocorrências;
- ordem dentro de cada tabela;
- proprietário associado;
- fase associada;
- origem e destino de cada aresta;
- caminho associado ao `file_type`.

Por exemplo, preservar um tipo e seu owner separadamente não basta.

Deve-se preservar a relação:

```text
tipo
owner
diretório
cardinalidade
fase
```

## Glossário bilíngue controlado

Cada perfil DEVE fornecer um glossário fechado para termos normativos recorrentes.
Cada entrada DEVE conter termo de origem, tradução canônica, contexto e restrição
semântica. Termo normativo ausente ou tradução alternativa não aprovada resulta
em `AMBIGUOUS` e bloqueia a execução.

## Matriz de rastreabilidade semântica

Cada unidade da origem **deve receber um identificador estável**:

| Prefixo | Unidade |
| :---: | :---: |
| `META-*` | Posicionamento e referências iniciais |
| `ITEM-*` | Itens contratuais do artefato |
| `OWN-*` | Linhas da matriz de ownership |
| `NOTE-*` | Notas normativas |
| `FLOW-*` | Relações de fluxo ou grafo |
| `STATE-*` | Estados, fases ou ativações |
| `PROC-*` | Passos procedurais |

- **Exemplo**:

| ID | Fonte japonesa | Tradução pt-BR | Contratos preservados | Resultado |
| :---: | :---: | :---: | :---: | :---: |
| `ITEM-001` | Unidade de origem | Unidade traduzida | identificadores e relações aplicáveis | Conforme |
| `FLOW-001` | Origem → destino | Mesmo fluxo | direção, rótulo e artefatos | Conforme |
| `STATE-001` | Estado ou fase | Mesmo estado ou fase | participantes, condições e gates | Conforme |

>Critério global: cobertura de 100%, sem IDs ausentes, duplicados ou adicionados sem fonte.

***

## Como evitar duas fontes concorrentes

### Solução obrigatória

1. Fixar a origem por commit ou SHA-256 antes da migração.
2. Definir exatamente um caminho canônico de destino.
3. Traduzir somente a cópia de trabalho autorizada.
4. Atualizar referências normativas para o caminho canônico.
5. Atualizar o catálogo documental aplicável.
6. Não manter outra versão ativa para o mesmo escopo e idioma-alvo.
7. Preservar a origem por Git ou evidência imutável.

> Assim, o repositório possui uma única versão operacional por escopo e idioma-alvo, enquanto a origem continua auditável.

## Verificações objetivas

### 1. Equivalência estrutural

O perfil DEVE inventariar seções, subseções, tabelas, itens, relações, grafos,
estados e passos relevantes. O resultado DEVE preservar exatamente os valores e
ordens declarados nesse inventário, salvo transformação estrutural explicitamente
autorizada pelo próprio perfil.

### 2. Equivalência dos contratos

Gerar representações normalizadas antes e depois, como:

```text
agent|model|phases
file_type|owner|directory|cardinality|phases
edge|source|label|target
phase|agents|quality_gate
procedure_step|position|references
```

A tradução é aceita somente se a comparação dessas representações produzir diferença vazia.

### 3. Ausência de japonês residual

Pesquisar caracteres japoneses no documento final. Toda ocorrência deve ser:

- eliminada; ou
- explicitamente justificada, caso seja nome próprio ou citação necessária.

### 4. Revisão linguística

Verificar especialmente modalidade e temporalidade:

- obrigação não pode virar recomendação;
- “único” não pode virar “principal”;
- “a partir de” não pode virar “durante”;
- “após a aprovação” não pode perder a precondição;
- “condicional” não pode parecer obrigatório;
- “todas as fases” não pode ser reduzido a fases específicas.

### 5. Não corrigir inconsistências durante a tradução

Inconsistências da origem DEVEM ser preservadas e registradas no perfil ou na
evidência para uma mudança normativa separada. Corrigir silenciosamente qualquer
inconsistência impede classificar o trabalho como tradução sem mudança normativa.

## Gates finais de aceitação

A tradução somente pode ser considerada aprovada quando:

- cobertura da matriz semântica = 100%;
- divergências contratuais = 0;
- unidades da origem sem tradução = 0;
- conteúdo novo sem correspondência na origem = 0;
- alterações silenciosas de obrigação, condição ou cardinalidade = 0;
- links normativos para o nome antigo = 0;
- fontes ativas concorrentes = 0;
- erros estruturais de Markdown ou Mermaid = 0;
- revisão bilíngue aprovada;
- validação do repositório apresentada;
- diff limitado ao escopo autorizado.

> O hash do arquivo não serve para provar equivalência, pois necessariamente muda com a tradução. A garantia vem da combinação de baseline imutável, comparação estrutural automatizada, preservação relacional dos contratos e revisão semântica rastreável.
