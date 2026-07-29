# Relatório de revisão editorial e Engenharia da Qualidade do VSCODE.md

## 1. Identificação

| Elemento | Definição |
| --- | --- |
| Documento avaliado | `.inicio/VSCODE.md` |
| Extensão avaliada | 4.059 linhas |
| Tipo de avaliação | Revisão editorial, controle de configuração e garantia da qualidade |
| Produto | CEPRAEA Beach Pro |
| Resultado desta avaliação | Plano de saneamento com ações e critérios de aceitação individuais |
| Situação do documento avaliado | Não apto, no estado atual, como especificação normativa única |

## 2. Objetivo deste relatório

Este relatório identifica as ações necessárias para transformar o `VSCODE.md` em uma
especificação de qualidade:

- única e inequívoca;
- verificável;
- rastreável;
- reproduzível;
- controlada por versão;
- coerente com os arquivos executáveis do repositório;
- capaz de distinguir requisitos obrigatórios, recomendações, exemplos, estado atual e
  histórico.

O relatório não redefine silenciosamente decisões técnicas. Quando o `VSCODE.md` apresenta
alternativas incompatíveis, a ação indicada é decidir, registrar e validar uma única alternativa
vigente.

## 3. Conclusão executiva

O `VSCODE.md` contém conhecimento suficiente para servir de base ao ambiente de desenvolvimento,
mas ainda não constitui uma especificação normativa confiável.

O principal problema não é falta de conteúdo. É a ausência de controle editorial e de configuração.
O arquivo reúne, no mesmo nível de autoridade:

- conceitos e justificativas;
- requisitos;
- recomendações;
- exemplos de arquivos;
- versões anteriores do texto;
- dados observados da máquina;
- instruções operacionais;
- registros de execução;
- estados concluídos e pendentes;
- conteúdo aparentemente copiado de uma conversa.

Como consequência, dois leitores podem aplicar configurações diferentes e ainda alegar conformidade
com o mesmo documento.

A transformação em especificação de qualidade exige quatro movimentos:

1. estabelecer uma fonte canônica para cada elemento configurável;
2. reestruturar o documento por função normativa;
3. resolver todas as decisões concorrentes;
4. implantar controles automáticos e evidências de conformidade.

## 4. Critério adotado para uma especificação de qualidade

O documento será considerado uma especificação de qualidade quando apresentar simultaneamente as
seguintes propriedades:

| Propriedade | Resultado esperado |
| --- | --- |
| Unicidade | Cada elemento possui uma única configuração vigente |
| Clareza | O caráter obrigatório ou informativo de cada conteúdo é explícito |
| Consistência | Não existem requisitos mutuamente incompatíveis |
| Rastreabilidade | Cada requisito possui identificador e método de verificação |
| Verificabilidade | Todo requisito obrigatório pode ser comprovado objetivamente |
| Reprodutibilidade | Uma instalação limpa produz o ambiente especificado |
| Atualidade | O texto corresponde aos arquivos reais e às decisões vigentes |
| Manutenibilidade | Alterações seguem processo de revisão e controle de versão |
| Segurança | Segredos e dados pessoais não são incorporados ao documento |
| Auditabilidade | Existem evidências datadas de validação e aprovação |

## 5. Diagnóstico editorial

### 5.1 Problemas críticos

#### D-01 — Não existe uma hierarquia de autoridade

O documento não informa quais partes são normativas e quais são apenas explicativas. Exemplos
iniciais, especificações posteriores e arquivos reais aparecem como se tivessem a mesma autoridade.

**Impacto:** implementação divergente, revisão subjetiva e impossibilidade de determinar
conformidade.

#### D-02 — Existem blocos concorrentes para os mesmos elementos

Foram encontradas versões diferentes para:

- `cepraea-beach-pro.code-workspace`;
- `.vscode/settings.json`;
- `.vscode/extensions.json`;
- `.vscode/tasks.json`;
- `.vscode/launch.json`;
- `.env.example`;
- `package.json`;
- scripts npm;
- `tsconfig.json`;
- estrutura TypeScript;
- configuração de Docker;
- dependências e versões.

**Impacto:** não há uma configuração única aplicável.

#### D-03 — A estrutura e a numeração estão corrompidas

Há seções repetidas, reinício indevido da numeração e duplicação de assuntos. Exemplos observados:

- duas seções de classificação consolidada;
- duas seções numeradas como 7;
- reinício em “1. Escopo” após a seção 14;
- repetição de boas práticas, configurações, riscos e critérios;
- títulos usados dentro de blocos ou transcrições sem integração à hierarquia principal.

**Impacto:** referências internas não são estáveis e o leitor não consegue identificar a versão
vigente de uma regra.

#### D-04 — Há conteúdo estranho ao documento

O trecho iniciado por “Você tem toda a razão” aparenta ser uma resposta de conversa incorporada ao
arquivo. Ele contém uma nova cópia parcial da especificação e formatação degradada.

**Impacto:** perda de integridade editorial e criação de regras concorrentes.

#### D-05 — Estado declarado é contraditório

O documento afirma que todos os critérios foram atendidos em 2026-07-26, mas também registra como
pendentes a configuração do WSL, a confirmação do VS Code, a criação dos arquivos do Workspace, a
instalação, a validação, o build, a depuração e o teste móvel.

**Impacto:** o status não pode ser usado como evidência de prontidão.

### 5.2 Problemas técnicos e de configuração

#### D-06 — TypeScript possui duas arquiteturas documentadas

Uma parte apresenta um `tsconfig.json` único com `compilerOptions`. Outra define:

- `tsconfig.json` como orquestrador;
- `tsconfig.app.json` para a aplicação;
- `tsconfig.node.json` para o Vite.

O repositório atual utiliza a segunda arquitetura.

**Impacto:** aplicação incorreta das opções do compilador e divergência em `typecheck` e `build`.

#### D-07 — O comando de teste não é único

O documento alterna entre:

```json
"test": "vitest run"
```

e:

```json
"test": "vitest run --passWithNoTests"
```

O `package.json` atual utiliza `--passWithNoTests`.

**Impacto:** critérios diferentes para aprovar um projeto sem testes.

#### D-08 — A configuração de depuração não é única

O tipo do depurador alterna entre `chrome` e `pwa-chrome`. Também existem versões com Chrome, Edge,
anexação remota e tarefas de pré-execução, enquanto o arquivo real contém uma configuração mínima.

**Impacto:** instruções podem não funcionar na versão instalada do VS Code.

#### D-09 — Variáveis de ambiente são divergentes

Uma versão define variáveis do Supabase:

```env
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

Outra define:

```env
VITE_API_URL=
VITE_PUBLIC_APP_URL=
```

O `.env.example` atual utiliza as variáveis do Supabase.

**Impacto:** inicialização inconsistente e contratos de configuração indefinidos.

#### D-10 — Docker é simultaneamente implementado, opcional e pendente de decisão

O documento contém `Dockerfile`, `docker-compose.yml`, versões e comandos completos. Em outra seção,
determina que Docker não pertence ao ambiente mínimo e só deve ser adotado após decisão arquitetural.
Os arquivos de Docker existem no repositório.

**Impacto:** não é possível saber se Docker é requisito, alternativa suportada ou material histórico.

#### D-11 — Versões aparecem como vigentes e provisórias

Node.js 24.14.1 e npm 11.11.0 são apresentados em arquivos e comandos obrigatórios, mas também são
classificados como provisórios até validação da stack. O `package.json` atual não contém `engines`
nem `packageManager`, e não foi observado `.nvmrc`.

**Impacto:** o ambiente não é reproduzível quanto ao runtime e ao gerenciador de pacotes.

#### D-12 — A lista de extensões diverge do repositório

O documento inclui Playwright em algumas listas. Os arquivos atuais recomendam Markdownlint e não
incluem Playwright.

**Impacto:** o onboarding e as verificações esperadas não correspondem ao Workspace real.

#### D-13 — Scripts documentados divergem do `package.json`

O texto contém `preview`, `test:watch` e escopos diferentes para formatação. O `package.json` atual
não possui todos esses scripts e restringe os arquivos processados por Prettier.

**Impacto:** tarefas do VS Code ou procedimentos documentados podem chamar comandos inexistentes ou
produzir validações incompletas.

#### D-14 — O escopo de lint de Markdown exclui o documento avaliado

O script atual `lint:md` valida `docs/**/*.md` e `src/features/**/*.md`, mas não
`.inicio/VSCODE.md`. A própria configuração do Markdownlint informa que `.inicio/` está fora da
governança principal.

**Impacto:** erros editoriais podem reaparecer sem impedir a integração.

### 5.3 Problemas de Engenharia da Qualidade

#### D-15 — Requisitos não possuem identificadores

As obrigações aparecem como frases, listas, exemplos ou instruções, sem IDs estáveis.

**Impacto:** não existe matriz confiável entre requisito, implementação, teste e evidência.

#### D-16 — Critérios de aceitação são incompletos ou não mensuráveis

Alguns critérios usam expressões como “adequado”, “simples”, “estável” ou “sem consumo excessivo”
sem limite, comando, resultado esperado ou responsável pela verificação.

**Impacto:** aprovações dependem da interpretação do avaliador.

#### D-17 — Recomendação e obrigação usam a mesma linguagem

Expressões como “deve”, “ideal”, “pode”, “recomendado” e “preferencialmente” não possuem definições
normativas.

**Impacto:** não é possível saber o que bloqueia a aprovação.

#### D-18 — Não há processo formal de mudança

O documento não estabelece como substituir uma decisão, registrar a justificativa, atualizar os
arquivos afetados e preservar o histórico.

**Impacto:** novas alterações podem introduzir novamente múltiplas configurações vigentes.

#### D-19 — Evidências misturam fatos históricos e estado corrente

Inventário de hardware, espaço em disco e status de ações são incorporados ao corpo da especificação.

**Impacto:** fatos temporários envelhecem e fazem o contrato técnico parecer desatualizado.

#### D-20 — Não há aprovação formal da linha de base

Não foram definidos proprietário, revisor, versão aprovada, data de vigência ou próxima revisão.

**Impacto:** não existe baseline documental auditável.

## 6. Modelo editorial recomendado

### 6.1 Tipos obrigatórios de conteúdo

O documento revisado deve usar os seguintes tipos, de forma explícita:

| Tipo | Marcador | Função | Pode reprovar conformidade? |
| --- | --- | --- | --- |
| Requisito obrigatório | `REQ-VSC-###` | Define condição necessária | Sim |
| Recomendação | `REC-VSC-###` | Orienta uma prática preferencial | Não |
| Exemplo | `EX-VSC-###` | Ilustra uma aplicação possível | Não |
| Estado atual | `EST-VSC-###` | Registra situação observada e datada | Não por si só |
| Histórico | `HIS-VSC-###` | Preserva decisão substituída | Não |
| Risco | `RIS-VSC-###` | Registra ameaça e controle | Conforme tratamento |
| Critério de aceitação | `CA-VSC-###` | Define prova objetiva de atendimento | Sim |

### 6.2 Vocabulário normativo

- **DEVE** ou **NÃO DEVE:** requisito obrigatório.
- **RECOMENDA-SE:** orientação não bloqueante.
- **PODE:** alternativa permitida dentro de limites declarados.
- **EXEMPLO:** conteúdo ilustrativo que não cria requisito.
- **ESTADO ATUAL:** observação datada, sujeita a mudança.
- **HISTÓRICO:** conteúdo sem vigência normativa.

Palavras normativas devem ser usadas apenas nos tipos correspondentes. Um exemplo não pode conter
uma obrigação que não esteja registrada como requisito.

### 6.3 Estrutura-alvo do VSCODE.md

1. Controle do documento.
2. Objetivo.
3. Escopo e escopo negativo.
4. Termos e linguagem normativa.
5. Hierarquia de autoridade e fontes canônicas.
6. Linha de base técnica vigente.
7. Requisitos do ambiente.
8. Requisitos do Workspace.
9. Requisitos de qualidade, segurança e testes.
10. Procedimento de implantação.
11. Critérios de aceitação e matriz de rastreabilidade.
12. Recomendações.
13. Exemplos.
14. Estado atual.
15. Riscos, desvios e pendências.
16. Histórico de alterações.

O conteúdo conceitual extenso, justificativas, inventários e tutoriais podem ser mantidos em anexos
ou documentos separados, desde que não concorram com a especificação normativa.

### 6.4 Fontes canônicas recomendadas

| Elemento | Fonte canônica | Tratamento no VSCODE.md |
| --- | --- | --- |
| Dependências e scripts | `package.json` e `package-lock.json` | Declarar requisitos e referenciar os arquivos |
| Versão do Node.js | `.nvmrc` e `package.json#engines` | Informar a política e verificar igualdade |
| Versão do npm | `package.json#packageManager` | Informar a política e verificar igualdade |
| TypeScript | `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` | Descrever responsabilidades, sem cópias concorrentes |
| Vite e PWA | `vite.config.ts` | Registrar requisitos funcionais e referenciar a implementação |
| Workspace | `cepraea-beach-pro.code-workspace` | Referenciar como ponto de entrada oficial |
| Editor | `.vscode/settings.json` | Definir somente regras específicas do projeto |
| Extensões | `.vscode/extensions.json` | Manter uma lista única |
| Tarefas | `.vscode/tasks.json` | Exigir correspondência com scripts npm |
| Depuração | `.vscode/launch.json` | Exigir configuração validada no VS Code suportado |
| Variáveis | `.env.example` | Definir nomes públicos e sua finalidade |
| Segredos | `.env.local` fora do Git | Declarar proibição e método de verificação |
| Docker | `Dockerfile` e `docker-compose.yml`, se aprovados | Classificar como obrigatório, opcional suportado ou removido |
| Formatação | `.editorconfig`, `.prettierrc` e `.prettierignore` | Declarar responsabilidades sem duplicação |
| Lint | `eslint.config.js` e `.markdownlint.jsonc` | Referenciar regras e escopo |
| Evidências | relatório de validação separado | Manter apenas o resumo datado no documento |

## 7. Plano de ações editoriais

### A-01 — Declarar o proprietário e o controle do documento

**Prioridade:** P0 — bloqueante.

**Ação:** adicionar bloco de controle com proprietário, aprovador, versão, data de vigência, estado,
data da última revisão e periodicidade de revisão.

**Critérios de aceitação individuais:**

- CA-A01-01: existe um único proprietário nominal ou papel organizacional.
- CA-A01-02: existe um único estado entre `Rascunho`, `Em revisão`, `Aprovado` e `Obsoleto`.
- CA-A01-03: a versão e a data de vigência estão preenchidas.
- CA-A01-04: toda alteração posterior modifica a versão ou registra justificativa para não fazê-lo.

### A-02 — Definir a hierarquia de autoridade

**Prioridade:** P0 — bloqueante.

**Ação:** declarar quais arquivos são fontes canônicas e como resolver divergências entre o texto e
os arquivos executáveis.

**Critérios de aceitação individuais:**

- CA-A02-01: cada elemento configurável possui exatamente uma fonte canônica.
- CA-A02-02: o documento determina que divergência entre fontes canônicas é falha de conformidade.
- CA-A02-03: não existe elemento cuja precedência dependa da interpretação do leitor.

### A-03 — Adotar linguagem normativa

**Prioridade:** P0 — bloqueante.

**Ação:** introduzir e aplicar os termos `DEVE`, `NÃO DEVE`, `RECOMENDA-SE`, `PODE`, `EXEMPLO`,
`ESTADO ATUAL` e `HISTÓRICO`.

**Critérios de aceitação individuais:**

- CA-A03-01: todos os termos estão definidos antes do primeiro requisito.
- CA-A03-02: todo uso de `DEVE` ou `NÃO DEVE` está associado a um ID de requisito.
- CA-A03-03: recomendações e exemplos não são usados como critérios bloqueantes.
- CA-A03-04: uma busca por expressões ambíguas não encontra obrigações sem classificação.

### A-04 — Identificar todos os requisitos

**Prioridade:** P0 — bloqueante.

**Ação:** converter obrigações dispersas em requisitos atômicos `REQ-VSC-###`.

**Critérios de aceitação individuais:**

- CA-A04-01: cada requisito contém uma única obrigação principal.
- CA-A04-02: cada requisito possui ID único e permanente.
- CA-A04-03: cada requisito informa fonte canônica, método de verificação e critério de aceitação.
- CA-A04-04: não existem obrigações normativas fora do catálogo de requisitos.

### A-05 — Remover conteúdo duplicado e estranho

**Prioridade:** P0 — bloqueante.

**Ação:** excluir as cópias redundantes e o trecho de conversa, preservando apenas conteúdo único que
tenha finalidade definida.

**Critérios de aceitação individuais:**

- CA-A05-01: o trecho “Você tem toda a razão” e sua transcrição não aparecem no documento normativo.
- CA-A05-02: cada assunto possui uma única seção normativa.
- CA-A05-03: nenhum bloco integral de configuração aparece em versões concorrentes.
- CA-A05-04: conteúdo removido que precise ser preservado está no histórico do Git ou em anexo
  explicitamente não normativo.

### A-06 — Reconstruir a hierarquia e a numeração

**Prioridade:** P0 — bloqueante.

**Ação:** reorganizar o conteúdo conforme a estrutura-alvo e gerar uma sequência única de títulos.

**Critérios de aceitação individuais:**

- CA-A06-01: existe um único título H1.
- CA-A06-02: não há salto indevido de nível de heading.
- CA-A06-03: cada número de seção é único e crescente.
- CA-A06-04: referências internas apontam para seções existentes e inequívocas.
- CA-A06-05: o Markdownlint não acusa erros de headings duplicados ou hierarquia.

### A-07 — Separar especificação, procedimento, estado e histórico

**Prioridade:** P0 — bloqueante.

**Ação:** mover cada conteúdo para sua categoria editorial correta.

**Critérios de aceitação individuais:**

- CA-A07-01: requisitos vigentes ficam apenas nas seções normativas.
- CA-A07-02: procedimentos não redefinem valores já fixados em requisitos.
- CA-A07-03: todo estado atual possui data da observação.
- CA-A07-04: decisões substituídas aparecem somente no histórico.
- CA-A07-05: exemplos são identificados e não podem ser confundidos com arquivos vigentes.

### A-08 — Reduzir cópias literais de arquivos canônicos

**Prioridade:** P1 — alta.

**Ação:** substituir cópias completas por requisitos, referências e pequenos exemplos quando a fonte
canônica já existir no repositório.

**Critérios de aceitação individuais:**

- CA-A08-01: cada arquivo real tem no máximo uma representação integral no documento.
- CA-A08-02: se houver representação integral, existe teste automático de igualdade.
- CA-A08-03: exemplos parciais contêm aviso explícito de que não substituem o arquivo canônico.
- CA-A08-04: mudanças no arquivo canônico não exigem busca manual por múltiplas cópias.

### A-09 — Retirar inventário mutável do corpo normativo

**Prioridade:** P1 — alta.

**Ação:** mover hardware, espaço em disco, versões instaladas e ações locais para relatório de estado
ou anexo datado.

**Critérios de aceitação individuais:**

- CA-A09-01: o corpo normativo contém requisitos mínimos, não medições temporárias.
- CA-A09-02: medições preservadas indicam data, origem e responsável.
- CA-A09-03: nenhuma medição histórica é apresentada como estado corrente sem revalidação.

### A-10 — Criar histórico controlado de alterações

**Prioridade:** P1 — alta.

**Ação:** manter somente um resumo de mudanças aprovadas, com versão, data, descrição, responsável e
referência à decisão.

**Critérios de aceitação individuais:**

- CA-A10-01: cada entrada informa qual requisito ou configuração foi alterado.
- CA-A10-02: a configuração substituída não permanece vigente no corpo.
- CA-A10-03: o histórico não duplica versões completas dos arquivos.
- CA-A10-04: o Git continua sendo a evidência detalhada da alteração.

## 8. Plano de ações para consolidar a configuração técnica

### A-11 — Ratificar a stack oficial

**Prioridade:** P0 — bloqueante.

**Ação:** aprovar uma única stack, distinguindo dependências obrigatórias, opcionais e futuras. A
baseline observada no repositório é React 19, Vite 6, TypeScript 5.7, Vitest 3, ESLint 9, Prettier 3,
Vite PWA e Supabase JS.

**Critérios de aceitação individuais:**

- CA-A11-01: todas as tecnologias vigentes aparecem em uma única tabela de baseline.
- CA-A11-02: versões declaradas correspondem ao `package.json` e ao `package-lock.json`.
- CA-A11-03: tecnologias futuras estão classificadas como recomendação ou backlog.
- CA-A11-04: o texto não afirma simultaneamente que a stack está definida e aguarda escolha.

### A-12 — Fixar Node.js, npm e política de versões

**Prioridade:** P0 — bloqueante.

**Ação:** decidir a versão suportada do Node.js e do npm, criar a fonte canônica e definir a política
de atualização.

**Critérios de aceitação individuais:**

- CA-A12-01: `.nvmrc` existe e contém uma única versão válida.
- CA-A12-02: `package.json#engines.node` corresponde à política aprovada.
- CA-A12-03: `package.json#packageManager` fixa o npm aprovado.
- CA-A12-04: `npm ci` funciona com o `package-lock.json` versionado.
- CA-A12-05: o documento não classifica as mesmas versões como oficiais e provisórias.

### A-13 — Consolidar a arquitetura TypeScript

**Prioridade:** P0 — bloqueante.

**Ação:** ratificar a arquitetura de três arquivos já utilizada no repositório e eliminar o exemplo
concorrente de `tsconfig.json` monolítico, salvo decisão formal em sentido contrário.

**Critérios de aceitação individuais:**

- CA-A13-01: `tsconfig.json` possui somente a função de orquestração aprovada.
- CA-A13-02: `tsconfig.app.json` cobre o código da aplicação e JSX.
- CA-A13-03: `tsconfig.node.json` cobre as ferramentas de build.
- CA-A13-04: `npm run typecheck` e `npm run build` terminam com código zero.
- CA-A13-05: o documento descreve apenas essa arquitetura como vigente.

### A-14 — Consolidar scripts npm e tarefas do VS Code

**Prioridade:** P0 — bloqueante.

**Ação:** definir o catálogo oficial de scripts e garantir correspondência exata com
`.vscode/tasks.json`.

**Critérios de aceitação individuais:**

- CA-A14-01: toda tarefa npm referencia um script existente.
- CA-A14-02: nenhum script obrigatório documentado está ausente do `package.json`.
- CA-A14-03: `validate` executa todas as barreiras obrigatórias na ordem aprovada.
- CA-A14-04: cada tarefa é executada com sucesso pelo VS Code ou possui falha reproduzível e
  documentada.
- CA-A14-05: nomes de tarefas e scripts aparecem uma única vez como configuração vigente.

### A-15 — Decidir a política para ausência de testes

**Prioridade:** P0 — bloqueante.

**Ação:** decidir se `--passWithNoTests` é uma exceção temporária ou uma política permanente.

**Critérios de aceitação individuais:**

- CA-A15-01: há uma decisão explícita para aprovar ou reprovar um projeto sem testes.
- CA-A15-02: se temporária, a exceção possui responsável, prazo e condição objetiva de remoção.
- CA-A15-03: `package.json`, tarefas, CI e documento usam o mesmo comando.
- CA-A15-04: uma falha real de teste sempre retorna código diferente de zero.

### A-16 — Consolidar a configuração do Workspace e do editor

**Prioridade:** P0 — bloqueante.

**Ação:** eliminar sobreposição desnecessária entre `.code-workspace` e `.vscode/settings.json`,
definindo a responsabilidade de cada arquivo.

**Critérios de aceitação individuais:**

- CA-A16-01: uma chave não possui valores divergentes entre os dois arquivos.
- CA-A16-02: configurações compartilhadas e configurações específicas possuem local definido.
- CA-A16-03: o Workspace abre sem erro de sintaxe ou configuração desconhecida.
- CA-A16-04: salvar arquivos TypeScript produz o comportamento de formatação e lint especificado.
- CA-A16-05: Markdown segue a política declarada, inclusive quanto a `formatOnSave`.

### A-17 — Consolidar extensões recomendadas

**Prioridade:** P1 — alta.

**Ação:** manter a lista canônica somente em `.vscode/extensions.json` e definir se Playwright e
Markdownlint pertencem ao conjunto oficial.

**Critérios de aceitação individuais:**

- CA-A17-01: `.vscode/extensions.json` contém a única lista canônica.
- CA-A17-02: o `.code-workspace` referencia a mesma lista ou deixa de duplicá-la.
- CA-A17-03: cada extensão possui justificativa ligada a um requisito.
- CA-A17-04: nenhuma extensão de preferência pessoal integra a lista.
- CA-A17-05: o VS Code apresenta as recomendações esperadas em uma instalação limpa.

### A-18 — Validar e consolidar a depuração

**Prioridade:** P0 — bloqueante.

**Ação:** escolher uma configuração principal suportada pela versão atual do VS Code e classificar
outras configurações como opcionais.

**Critérios de aceitação individuais:**

- CA-A18-01: existe exatamente uma configuração principal de depuração.
- CA-A18-02: o tipo do depurador é reconhecido sem extensão obsoleta.
- CA-A18-03: a URL corresponde à porta do servidor Vite.
- CA-A18-04: `webRoot` aponta para o código-fonte correto.
- CA-A18-05: um breakpoint em TypeScript é atingido em teste manual registrado.

### A-19 — Consolidar o contrato de variáveis de ambiente

**Prioridade:** P0 — bloqueante.

**Ação:** definir o conjunto oficial de variáveis, finalidade, obrigatoriedade, ambiente e
sensibilidade.

**Critérios de aceitação individuais:**

- CA-A19-01: `.env.example` contém todas e somente as variáveis públicas necessárias ao cliente.
- CA-A19-02: cada variável possui descrição, tipo, obrigatoriedade e valor de exemplo seguro.
- CA-A19-03: código e documentação usam os mesmos nomes.
- CA-A19-04: `.env.local` e outros arquivos reais de segredo estão ignorados pelo Git.
- CA-A19-05: nenhuma chave `service_role` ou segredo é exposto por prefixo `VITE_`.

### A-20 — Classificar definitivamente o Docker

**Prioridade:** P0 — bloqueante.

**Ação:** escolher uma das classificações: requisito obrigatório, alternativa opcional suportada ou
configuração removida. Não manter as três interpretações.

**Critérios de aceitação individuais:**

- CA-A20-01: a classificação do Docker aparece uma única vez na baseline.
- CA-A20-02: se suportado, `docker compose config` termina com código zero.
- CA-A20-03: se suportado, o container inicia a aplicação e permite hot reload conforme especificado.
- CA-A20-04: se removido, arquivos, comandos e requisitos de Docker deixam a baseline vigente.
- CA-A20-05: a estratégia escolhida respeita os limites de memória definidos para a máquina.

### A-21 — Consolidar Vite e PWA

**Prioridade:** P1 — alta.

**Ação:** converter a implementação do `vite.config.ts` em requisitos verificáveis de porta, host,
manifesto, atualização, ícones e comportamento offline.

**Critérios de aceitação individuais:**

- CA-A21-01: porta e host são únicos e iguais nos scripts, tarefas, depuração e documentação.
- CA-A21-02: o build gera manifesto e service worker válidos.
- CA-A21-03: todos os ícones referenciados existem e possuem dimensões declaradas.
- CA-A21-04: a política `autoUpdate` ou sua substituta está formalmente aprovada.
- CA-A21-05: instalação e atualização da PWA possuem teste registrado.
- CA-A21-06: funcionalidades offline declaradas correspondem ao que está implementado; capacidades
  futuras são recomendações, não requisitos atendidos.

### A-22 — Consolidar a estrutura de diretórios

**Prioridade:** P1 — alta.

**Ação:** documentar somente a estrutura real e os diretórios obrigatórios, sem exigir árvores vazias
sem necessidade técnica.

**Critérios de aceitação individuais:**

- CA-A22-01: a árvore normativa corresponde ao resultado de uma inspeção do repositório.
- CA-A22-02: cada diretório obrigatório possui finalidade definida.
- CA-A22-03: diretórios opcionais são identificados como criados sob demanda.
- CA-A22-04: o documento não prescreve arquivos `.gitkeep` onde já existem arquivos reais.

## 9. Plano de ações para assegurar a Engenharia da Qualidade

### A-23 — Criar matriz de rastreabilidade

**Prioridade:** P0 — bloqueante.

**Ação:** relacionar requisito, risco, fonte canônica, método de teste, evidência e estado.

**Critérios de aceitação individuais:**

- CA-A23-01: 100% dos requisitos obrigatórios aparecem na matriz.
- CA-A23-02: cada requisito possui pelo menos um método de verificação.
- CA-A23-03: cada critério bloqueante referencia evidência ou resultado esperado.
- CA-A23-04: requisitos não implementados aparecem como `Pendente` ou `Desvio aceito`, nunca como
  concluídos.

### A-24 — Definir portas de qualidade

**Prioridade:** P0 — bloqueante.

**Ação:** formalizar os comandos que bloqueiam aprovação local e integração contínua.

**Critérios de aceitação individuais:**

- CA-A24-01: a baseline mínima inclui lint, lint de Markdown, typecheck, testes e build.
- CA-A24-02: qualquer falha obrigatória produz código de saída diferente de zero.
- CA-A24-03: `npm run validate` cobre todas as portas aprovadas ou chama um script agregador
  equivalente.
- CA-A24-04: os comandos são executáveis em instalação limpa com `npm ci`.
- CA-A24-05: a evidência registra comando, data, versão e resultado.

### A-25 — Incluir o VSCODE.md na governança de Markdown

**Prioridade:** P0 — bloqueante.

**Ação:** mover a especificação para o diretório documental governado ou ampliar explicitamente o
escopo de `lint:md`.

**Critérios de aceitação individuais:**

- CA-A25-01: o comando oficial de lint inclui o caminho definitivo do documento.
- CA-A25-02: o documento passa no Markdownlint sem exclusões locais não justificadas.
- CA-A25-03: todos os blocos de código possuem linguagem permitida.
- CA-A25-04: separadores, headings, listas e cercas seguem `.markdownlint.jsonc`.

### A-26 — Automatizar verificações de consistência cruzada

**Prioridade:** P1 — alta.

**Ação:** criar validações para valores repetidos entre arquivos, evitando divergências silenciosas.

**Critérios de aceitação individuais:**

- CA-A26-01: um teste confirma igualdade da porta entre Vite, scripts, tarefas e depuração.
- CA-A26-02: um teste confirma que tarefas npm referenciam scripts existentes.
- CA-A26-03: um teste confirma coerência entre `.nvmrc`, `engines` e `packageManager`.
- CA-A26-04: um teste confirma que variáveis usadas no código estão documentadas em `.env.example`.
- CA-A26-05: uma divergência intencional possui exceção explícita e justificada.

### A-27 — Implantar revisão de segurança documental

**Prioridade:** P0 — bloqueante.

**Ação:** verificar segredos, dados pessoais, caminhos pessoais e identificadores de máquina antes da
aprovação.

**Critérios de aceitação individuais:**

- CA-A27-01: uma busca automatizada não encontra tokens ou chaves privadas.
- CA-A27-02: nomes de usuário, e-mails, IPs completos, números de série e Product IDs não aparecem.
- CA-A27-03: exemplos usam placeholders inequívocos.
- CA-A27-04: o `.gitignore` cobre todos os arquivos locais de segredo especificados.
- CA-A27-05: a revisão de segurança possui evidência datada.

### A-28 — Definir gestão de desvios e exceções

**Prioridade:** P1 — alta.

**Ação:** criar processo para aceitar temporariamente uma não conformidade sem alterar silenciosamente
o requisito.

**Critérios de aceitação individuais:**

- CA-A28-01: todo desvio possui ID, requisito afetado, justificativa, risco e responsável.
- CA-A28-02: todo desvio possui prazo ou condição objetiva de encerramento.
- CA-A28-03: desvios vencidos reprovam a validação de prontidão.
- CA-A28-04: exceções não são incorporadas como regra permanente sem nova aprovação.

### A-29 — Definir gestão de mudanças

**Prioridade:** P1 — alta.

**Ação:** exigir análise de impacto antes de alterar versões, portas, ferramentas, arquivos canônicos
ou requisitos.

**Critérios de aceitação individuais:**

- CA-A29-01: toda mudança identifica arquivos, requisitos, testes e documentação afetados.
- CA-A29-02: a mudança é revisada antes de entrar em vigor.
- CA-A29-03: fontes canônicas e matriz de rastreabilidade são atualizadas no mesmo conjunto de
  alterações.
- CA-A29-04: a baseline anterior permanece recuperável pelo Git, mas não aparece como vigente.

### A-30 — Definir evidências de qualificação do ambiente

**Prioridade:** P1 — alta.

**Ação:** criar um relatório de validação separado para cada qualificação ou requalificação do
ambiente.

**Critérios de aceitação individuais:**

- CA-A30-01: a evidência contém data, executor, sistema, versões e commit validado.
- CA-A30-02: cada critério registra `Aprovado`, `Reprovado`, `Não executado` ou `Não aplicável`.
- CA-A30-03: itens `Não aplicável` possuem justificativa.
- CA-A30-04: o `VSCODE.md` apresenta apenas o estado resumido e aponta para a evidência.
- CA-A30-05: uma nova baseline técnica exige requalificação dos critérios impactados.

### A-31 — Validar reprodutibilidade em ambiente limpo

**Prioridade:** P0 — bloqueante para aprovação final.

**Ação:** executar o procedimento completo em um ambiente limpo ou controlado.

**Critérios de aceitação individuais:**

- CA-A31-01: o repositório é obtido sem dependências preexistentes.
- CA-A31-02: a versão oficial do Node.js é selecionada a partir da fonte canônica.
- CA-A31-03: `npm ci` termina com código zero sem alterar o lockfile.
- CA-A31-04: todas as portas de qualidade terminam com código zero.
- CA-A31-05: a aplicação inicia na porta oficial.
- CA-A31-06: depuração, acesso no navegador e, quando obrigatório, acesso móvel são comprovados.
- CA-A31-07: os passos executados correspondem integralmente ao procedimento documentado.

### A-32 — Realizar revisão editorial e aprovação independentes

**Prioridade:** P0 — bloqueante para publicação.

**Ação:** submeter a versão consolidada a uma revisão que verifique forma, conteúdo e aplicabilidade.

**Critérios de aceitação individuais:**

- CA-A32-01: a revisão confirma ausência de configurações concorrentes.
- CA-A32-02: uma pessoa que não participou da consolidação identifica corretamente a configuração
  vigente de cada elemento.
- CA-A32-03: todos os achados P0 estão encerrados.
- CA-A32-04: achados P1 remanescentes possuem desvio formal aprovado.
- CA-A32-05: proprietário e aprovador registram a aprovação da baseline.

## 10. Decisões técnicas que precisam de resolução explícita

As decisões abaixo não devem permanecer implícitas durante a reescrita:

| ID | Elemento | Alternativas encontradas | Decisão necessária |
| --- | --- | --- | --- |
| DEC-01 | Node.js | 24.14.1 oficial ou provisório | Versão e política suportada |
| DEC-02 | npm | 11.11.0 oficial ou provisório | Versão e forma de fixação |
| DEC-03 | Testes vazios | `vitest run` ou `--passWithNoTests` | Regra de aprovação |
| DEC-04 | TypeScript | arquivo único ou três arquivos | Arquitetura oficial |
| DEC-05 | Depurador | `chrome` ou `pwa-chrome` | Tipo suportado e fluxo principal |
| DEC-06 | Navegador | Chrome, Edge ou ambos | Principal e opcionais |
| DEC-07 | Variáveis | Supabase ou API genérica | Contrato oficial |
| DEC-08 | Docker | obrigatório, opcional suportado ou removido | Classificação definitiva |
| DEC-09 | Extensões | Playwright e Markdownlint | Lista oficial |
| DEC-10 | Scripts | conjunto mínimo ou ampliado | Catálogo oficial |
| DEC-11 | Formatação Markdown | automática ou somente lint | Comportamento oficial |
| DEC-12 | Offline | requisito atual ou evolução futura | Escopo verificável |
| DEC-13 | Teste móvel | requisito bloqueante ou recomendação | Critério de prontidão |
| DEC-14 | Limite do WSL | requisito do projeto ou recomendação local | Escopo e aplicabilidade |

Uma decisão só estará encerrada quando atualizar simultaneamente:

- requisito correspondente;
- fonte canônica;
- procedimento;
- teste;
- matriz de rastreabilidade;
- histórico.

## 11. Ordem recomendada de execução

### Fase 1 — Saneamento bloqueante

Executar A-01 a A-07, removendo duplicações, reconstruindo a estrutura e estabelecendo autoridade
documental.

### Fase 2 — Baseline técnica

Resolver DEC-01 a DEC-14 e executar A-11 a A-22. Nesta fase, os arquivos reais do repositório devem
ser reconciliados com as decisões aprovadas.

### Fase 3 — Garantia da qualidade

Executar A-23 a A-31, implantando rastreabilidade, portas de qualidade, segurança, gestão de
mudanças e evidências.

### Fase 4 — Aprovação

Executar A-32 e publicar a primeira versão normativa aprovada.

## 12. Critérios globais de aceite do VSCODE.md revisado

O documento somente poderá ser classificado como especificação de qualidade quando todos os critérios
abaixo forem atendidos:

- CG-01: existe uma única configuração vigente para cada elemento.
- CG-02: 100% dos requisitos obrigatórios possuem ID, fonte canônica e critério verificável.
- CG-03: requisitos, recomendações, exemplos, estado e histórico estão visualmente e semanticamente
  separados.
- CG-04: não existem trechos duplicados, transcrições de conversa ou numeração concorrente.
- CG-05: o texto e os arquivos executáveis não apresentam divergências.
- CG-06: todas as decisões técnicas abertas estão resolvidas ou formalmente registradas como desvio.
- CG-07: o documento passa no Markdownlint e nas verificações de consistência.
- CG-08: `npm ci`, lint, typecheck, testes e build são aprovados em ambiente limpo.
- CG-09: a depuração principal é validada por breakpoint.
- CG-10: os requisitos de PWA e acesso móvel são comprovados ou reclassificados corretamente.
- CG-11: nenhuma credencial ou informação pessoal está presente.
- CG-12: existe matriz de rastreabilidade completa.
- CG-13: existe relatório de validação datado e associado a um commit.
- CG-14: todos os achados P0 estão encerrados.
- CG-15: a baseline possui proprietário, aprovador, versão e data de vigência.

## 13. Resultado da revisão

**Classificação atual:** não conforme como especificação normativa única.

**Potencial de aproveitamento:** alto. O conteúdo técnico pode ser consolidado; não é necessário
reescrever todo o conhecimento do zero.

**Condição para aprovação:** conclusão das ações P0, resolução das decisões técnicas concorrentes,
implantação da rastreabilidade e validação da baseline em ambiente limpo.

**Próximo artefato recomendado:** uma versão reestruturada do `VSCODE.md`, produzida a partir deste
plano, acompanhada de matriz de rastreabilidade e relatório de validação.
