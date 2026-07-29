# Guia de documentação Markdown para agentes de IA

## 1. Finalidade

Este documento define convenções para escrever instruções técnicas em Markdown
de forma legível, verificável e segura para pessoas e agentes de IA.

As convenções organizam o conteúdo, mas não alteram a prioridade real das
instruções nem garantem obediência por um modelo. A prioridade depende do
ambiente que fornece as instruções ao agente.

## 2. Escopo

Use este guia para:

- instruções de repositório;
- especificações de tarefas;
- critérios de aceitação;
- procedimentos operacionais;
- dicionários de erros;
- exemplos técnicos destinados a agentes.

Este guia não substitui:

- controles de acesso;
- revisão humana;
- testes automatizados;
- políticas de segurança;
- documentação oficial das ferramentas utilizadas.

## 3. Convenções normativas

Os termos abaixo indicam a força de cada orientação:

- **DEVE**: requisito obrigatório para conformidade;
- **NÃO DEVE**: comportamento proibido;
- **DEVERIA**: recomendação que pode ter exceções justificadas;
- **PODE**: alternativa permitida.

### 3.1 Títulos

Cada documento DEVE conter um único título de nível 1 (`#`). Esse título
define o assunto do arquivo.

As seções principais usam `##`; suas subseções usam `###`. Um título NÃO
DEVE saltar níveis.

Exemplo:

```markdown
# Título do documento

## 1. Seção

### 1.1 Subseção
```

Numere títulos somente quando a ordem ou a referência cruzada trouxer valor.
Não reinicie a numeração dentro do mesmo documento.

### 3.2 Listas

Use listas com `-` para itens independentes, como regras, restrições e
requisitos sem ordem de execução.

Use listas numeradas apenas quando:

1. a ordem de execução for obrigatória;
2. uma etapa depender da anterior;
3. o número identificar um critério referenciado em outro ponto.

Itens de lista não podem estar vazios.

### 3.3 Tabelas

Use tabelas quando linhas e colunas tornarem relações repetidas mais fáceis de
comparar. São usos adequados:

- matrizes de permissões e responsabilidades;
- comparação entre estado atual e estado desejado;
- mapeamento entre identificadores, condições e resultados;
- relação entre erros, diagnósticos e ações;
- comparação de opções que compartilham os mesmos atributos.

Cada tabela **DEVE**:

- possuir cabeçalho;
- usar uma coluna por atributo comparável;
- manter células curtas e denotativas;
- indicar unidade ou contexto quando um valor puder ser ambíguo;
- evitar colunas vazias.

Não use tabela para representar uma sequência de execução. Use lista numerada
quando a ordem for obrigatória. Se as células exigirem parágrafos extensos,
prefira subseções ou listas.

Uma tabela organiza relações, mas não concede prioridade técnica às regras. A
prioridade continua dependendo da origem da instrução e do ambiente do agente.

### 3.4 Ênfase

Use negrito para termos normativos, identificadores e entidades que precisam
ser localizadas rapidamente.

Não dependa apenas de negrito, caixa alta, emojis ou blockquotes para indicar
prioridade. Expresse a regra e sua consequência de forma explícita.

### 3.5 Blocos de código

Todo bloco de código DEVE:

- ter uma cerca de abertura e outra de fechamento com o mesmo caractere;
- informar a linguagem quando ela for conhecida;
- conter apenas código, dados ou texto exemplar;
- ser validado antes da publicação quando for apresentado como executável.

Para exibir Markdown que contém cercas triplas, use quatro crases na cerca externa:

````markdown
```bash
printf '%sn' "exemplo"
```
````

### 3.6 Tags de delimitação

Tags semânticas como `<instructions>`, `<context>`, `<examples>` e `<input>`
**DEVERIAM** ser usadas quando ajudarem a distinguir tipos de conteúdo em
instruções ou documentos complexos.

Essa recomendação é geral e não está limitada a um fornecedor. A ausência de
evidência específica para um modelo, produto ou agente NÃO DEVE ser
interpretada como evidência de que as tags sejam ineficazes ou prejudiciais
nesse ambiente.

Para **Claude**, o uso de **tags XML** possui recomendação oficial da
Anthropic para:

- separar instruções, contexto, exemplos e entradas variáveis;
- envolver um exemplo em `<example>`;
- agrupar múltiplos exemplos em `<examples>`;
- estruturar documentos com `<document>`, `<document_content>` e `<source>`.

Para outros modelos e agentes, as tags **PODEM** ser adotadas pela mesma finalidade
sem presumir equivalência de desempenho. A estrutura **DEVERIA** ser validada com
os modelos, versões, prompts de sistema e interfaces realmente utilizados.

Ao utilizá-las:

- abra e feche cada tag;
- use nomes consistentes e descritivos;
- aninhe tags somente quando existir uma hierarquia natural;
- escape ou sanitize conteúdo externo que possa fechar ou criar tags;
- não use tags como substitutas obrigatórias da hierarquia Markdown;
- não atribua às tags efeitos que a ferramenta não documenta;
- mantenha o conteúdo da tag coerente com o título da seção.

Exemplo:

```xml
<instructions>
Resuma cada documento usando somente o conteúdo fornecido.
</instructions>

<documents>
  <document index="1">
    <source>relatorio-a.md</source>
    <document_content>
      Conteúdo do documento.
    </document_content>
  </document>
</documents>

<input>
Quais riscos foram identificados?
</input>
```

Tags são delimitadores semânticos, não fronteiras de confiança.

> Elas **NÃO DEVEM** ser tratadas isoladamente como proteção contra prompt
> injection, escalonamento de privilégios ou execução indevida. Conteúdo
> externo continua não confiável e **DEVERIA** ser combinado com:

- papéis de mensagem fornecidos pela API;
- validação e sanitização de entrada;
- menor privilégio para ferramentas;
- validação da saída;
- controles de acesso e isolamento do ambiente;
- testes adversariais representativos.

### 3.7 Blockquotes

Use `>` para destacar avisos, notas ou restrições visuais.

> **Aviso:** o blockquote melhora a apresentação, mas não concede prioridade
> técnica à instrução.

### 3.8 Linguagem

O texto DEVE ser denotativo e operacional:

- prefira ações observáveis;
- defina termos técnicos que admitam interpretações diferentes;
- substitua qualificadores vagos por limites mensuráveis;
- evite metáforas como descrição de comportamento interno de modelos;
- não declare percentuais, garantias ou superioridade sem evidência identificada.

Exemplo inadequado:

```text
A página deve carregar rapidamente.
```

Exemplo verificável:

```text
No ambiente de referência, 95% das respostas de GET /health devem ser
concluídas em até 200 ms durante um teste com 100 conexões simultâneas.
```

## 4. Modelo de conteúdo

### 4.1 Identificação

Um documento operacional DEVERIA registrar:

- título;
- finalidade;
- escopo incluído;
- escopo excluído;
- responsável;
- versão ou data de vigência;
- fontes autorizadas.

### 4.2 Estado atual

Descreva somente fatos observados ou confirmados. Inclua arquivos, interfaces,
versões e restrições relevantes para a tarefa.

Não apresente uma suposição como estado confirmado. Identifique explicitamente
dados ainda não verificados.

### 4.3 Estado desejado

Descreva resultados observáveis, sem prescrever uma implementação quando
diferentes soluções forem aceitáveis.

Cada resultado DEVERIA informar:

- objeto afetado;
- comportamento esperado;
- limite de escopo;
- condição de sucesso.

### 4.4 Matriz de permissões

Classifique ações pela consequência, não apenas pela frequência:

| Categoria | Consequência |
| --- | --- |
| **ALWAYS** | Executar dentro do escopo já autorizado. |
| **ASK** | Solicitar autorização ou confirmar o contexto. |
| **NEVER** | Não executar no contexto do documento. |

Exemplos:

- **ALWAYS:** ler arquivos relacionados e executar testes não destrutivos;
- **ASK:** instalar dependências, alterar esquema ou redefinir banco local;
- **NEVER:** expor credenciais ou contornar controles de segurança.

Uma regra DEVE indicar o alvo e a condição aplicável. Evite regras globais
quando a permissão vale somente para um diretório ou ambiente.

### 4.5 Critérios de aceitação

Cada critério DEVE permitir resultado `passou` ou `falhou`.

Um critério completo informa:

- condição avaliada;
- método de verificação;
- resultado esperado;
- ambiente ou dados necessários.

Exemplo:

```yaml
id: AC-001
condition: GET /health retorna o estado da aplicação
verification:
  method: teste_de_integracao
  command: npm run test:integration -- health
expected:
  exit_code: 0
  http_status: 200
  body:
    status: healthy
```

### 4.6 Procedimentos de erro

Cada entrada de erro DEVERIA conter:

- identificador observável;
- causas possíveis, sem declarar como confirmada uma causa ainda não diagnosticada;
- diagnóstico não destrutivo;
- resolução ordenada;
- condição de parada;
- classificação `ALWAYS`, `ASK` ou `NEVER` para ações sensíveis.

O modelo completo está em [ERRORS-TEMPLATE.md](ERRORS-TEMPLATE.md).

## 5. Fronteiras de ação

Toda instrução destinada a um agente com acesso de escrita DEVERIA declarar:

- caminhos permitidos;
- caminhos somente para leitura;
- arquivos proibidos;
- comandos permitidos;
- ações que exigem confirmação;
- validações obrigatórias antes da conclusão.

Operações destrutivas, irreversíveis ou com impacto externo NÃO DEVEM ser
apresentadas como autocorreção automática.

São exemplos de ações `ASK`:

- redefinir banco de dados;
- excluir arquivos ou registros;
- executar migrações destrutivas;
- alterar credenciais ou variáveis de produção;
- publicar artefatos;
- instalar dependências.

## 6. Exemplos e automação

### 6.1 Exemplo integrado

O arquivo abaixo é um exemplo não normativo da aplicação conjunta de:

- limitação de escopo a testes unitários;
- tags XML para delimitar exemplos e dados;
- comandos escritos no modo imperativo.

````markdown
# Diretrizes de testes unitários

Este arquivo define o escopo exclusivo para a criação e manutenção de testes
unitários automatizados no projeto.

## Regras de execução

- **Escreva** testes isolados para cada nova função ou componente criado.
- **Use** Jest com Testing Library.
- **Garanta** cobertura mínima de 85% de linhas e branches.
- **Evite** dependências externas reais usando mocks para requisições de API.

## Padrão de estrutura do código

Siga a estrutura demonstrada abaixo para manter a consistência das asserções.

<example>

```typescript
import { calcularDesconto } from "./utils";

describe("calcularDesconto", () => {
  it("aplica 10% de desconto corretamente", () => {
    const resultado = calcularDesconto(100, 10);

    expect(resultado).toBe(90);
  });

  it("retorna o valor original quando o desconto é zero", () => {
    const resultado = calcularDesconto(100, 0);

    expect(resultado).toBe(100);
  });
});
```

</example>

## Restrições de contexto

<context>

- Ambiente: Node.js 20 ou versão posterior compatível
- Modo: strict
- Mocks: obrigatórios para `/api/v1/*`

</context>

- **Gere** o relatório de cobertura após executar a suíte.
- **Ordene** os testes começando pelos caminhos principais e seguindo pelos
  fluxos de exceção.
````

O exemplo demonstra organização e intenção. Os comandos, percentuais, versões
e ferramentas ainda precisam corresponder ao projeto em que ele for adotado.

### 6.2 Responsabilidade dos artefatos

Os artefatos deste conjunto têm responsabilidades separadas:

- [AI-CONTEXT-TEMPLATE.md](AI-CONTEXT-TEMPLATE.md): modelo de instruções de
  projeto;
- [ERRORS-TEMPLATE.md](ERRORS-TEMPLATE.md): modelo seguro de diagnóstico e
  resolução;
- [DOCUMENT-LINTER.md](DOCUMENT-LINTER.md): uso dos validadores;
- [ISO-STANDARDS.md](ISO-STANDARDS.md): relação resumida entre normas;
- [MD-FORMAT-LEGACY.md](MD-FORMAT-LEGACY.md): conteúdo original preservado
  para consulta histórica.

## 7. Avaliação de evidências

Recomendações destinadas a modelos ou agentes DEVERIAM registrar:

- comportamento alegado;
- modelo, versão e interface avaliados;
- tarefa e conjunto de dados;
- comparação ou baseline;
- métrica e resultado;
- fonte e data de consulta;
- limitações conhecidas.

Use três estados para classificar a evidência:

- **positiva:** sustenta a recomendação no contexto avaliado;
- **negativa:** sustenta restrição ou desaconselhamento no contexto avaliado;
- **ausente ou inconclusiva:** não permite concluir a favor nem contra.

Ausência de evidência NÃO DEVE ser convertida em evidência negativa. Uma
recomendação confirmada para um fornecedor pode aumentar a confiança nesse
ambiente, mas não restringe automaticamente sua aplicabilidade aos demais.

Fontes possuem finalidades diferentes:

- documentação oficial sustenta comportamento declarado pelo fornecedor;
- estudos revisados por pares sustentam resultados no desenho experimental;
- orientação técnica sustenta práticas de implementação e hipóteses;
- testes locais sustentam somente o ambiente e as versões avaliadas.

Afirmações de segurança exigem atenção adicional. Um delimitador que melhora a
interpretação não deve ser descrito como controle de acesso ou isolamento
garantido.

### 7.1 Base de referência

- [Anthropic: prompting best practices][anthropic-prompting]: recomenda XML
  para estruturar instruções, contexto, exemplos, entradas e documentos.
- [Anthropic: effective context engineering][anthropic-context]: recomenda XML
  ou títulos Markdown e ressalta que o formato exato pode variar.
- [Zverev et al., ICLR 2025][iclr-separation]: demonstra limitações na
  separação entre instruções e dados.
- [Wu et al., ICLR 2025][iclr-hierarchy]: investiga hierarquia de instruções e
  limitações de delimitadores sem suporte arquitetural.
- [AWS Prescriptive Guidance][aws-prompt-injection]: apresenta testes técnicos
  com Claude e recomenda defesa em camadas contra prompt injection.
- [Correa, Tech4Humans][medium-xml]: registra orientação da comunidade técnica;
  não substitui estudo controlado ou fonte revisada por pares.

## 8. Validação

Antes de publicar um documento:

1. execute o markdownlint;
2. execute o validador estrutural complementar;
3. corrija títulos, listas, cercas e espaços reportados;
4. execute os exemplos de código em ambiente isolado;
5. verifique links, referências e vigência das fontes;
6. revise ações `ASK` e `NEVER`;
7. confirme que critérios de aceitação são reproduzíveis;
8. valide regras específicas nos modelos e interfaces de destino.

**Comandos executados** a partir da raiz do workspace:

```bash
npx --yes markdownlint-cli2 md-format/docs/MD-FORMAT.md

python3 md-format/scripts/validate_ai_docs.py \
  md-format/docs/MD-FORMAT.md \
  md-format/docs/AI-CONTEXT-TEMPLATE.md \
  md-format/docs/ERRORS-TEMPLATE.md \
  md-format/docs/DOCUMENT-LINTER.md \
  md-format/docs/ISO-STANDARDS.md
```

> O resultado de um validador vale somente para as regras que ele implementa.
> `OK` no validador complementar não significa aprovação no markdownlint,
> correção factual, vigência das fontes ou segurança do documento.

## 9. Critérios de conformidade deste guia

Este arquivo está conforme quando:

- existe exatamente um título `#`;
- nenhum título salta níveis;
- não existem itens de lista vazios;
- todas as cercas estão fechadas;
- todos os blocos cercados informam uma linguagem;
- não há espaços ao final das linhas;
- exemplos executáveis passam por validação apropriada;
- operações sensíveis estão classificadas como `ASK` ou `NEVER`;
- referências possuem destino identificável;
- não existem marcadores de conversa ou chamadas para continuar uma resposta.

[anthropic-prompting]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
[anthropic-context]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[iclr-separation]: https://proceedings.iclr.cc/paper_files/paper/2025/hash/a77eadda332b6d4a9ae1e0e4024555f2-Abstract-Conference.html
[iclr-hierarchy]: https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea13534ee239bb3977795b8cc855bacc-Abstract-Conference.html
[aws-prompt-injection]: https://docs.aws.amazon.com/prescriptive-guidance/latest/llm-prompt-engineering-best-practices/introduction.html
[medium-xml]: https://medium.com/@TechforHumans/effective-prompt-engineering-mastering-xml-tags-for-clarity-precision-and-security-in-llms-992cae203fdc