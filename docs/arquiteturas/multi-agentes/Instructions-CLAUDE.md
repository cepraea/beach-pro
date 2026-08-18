# ARQUITETURA CLAUDE.md

Este documento trata das especificações e requisitos do [`CLAUDE.md`](/CLAUDE.md)

**Arquivos longos podem reduzir a aderência às instruções**.
> Então, **o tamanho oficial do `CLAUDE.md` do CEPRAEA Beach pro é de ~100 linhas**, deixando detalhes especializados em `.claude/rules/` e `skills`.

`CLAUDE.md` deve ter instruções persistentes, para gerar acúmulo de aprendizados automaticamente.

`CLAUDE.md` é carregado e seu conteúdo permanece relevante ao longo da sessão; quanto maior ele fica, mais contexto consome.

**Conhecimento entre sessões:**
- `CLAUDE.md`: instruções para dar contexto persistente ao Claude.
- Memória automática: Claude escreve notas sozinho com base nas as correções e preferências

Tamanho alvo do conteúdo:
* **~50–100 linhas:** excelente para a maioria dos projetos.
* **100–150 linhas:** ainda muito saudável.
* **150–200 linhas:** aceitável, mas vale revisar se tudo realmente precisa estar sempre presente.
* **>200 linhas:** sinal para decompor.

`CLAUDE.md` deve responder:

> *O que Claude **deve saber em toda sessão**:*

- comandos de build/testeconvenções essenciais,
- decisões arquiteturais importantes
- estrutura do projeto e regras do tipo “sempre faça X” ou “nunca faça Y”.

Recomendação para conteúdo maior:

```text
CLAUDE.md              # regras globais essenciais (100 linhas)

.claude/
├── rules/
│   ├── frontend.md    # regras específicas
│   ├── backend.md
│   └── tests.md
└── skills/
    ├── deploy/
    │   └── SKILL.md
    └── code-review/
        └── SKILL.md
```

**Distinção importante:**

> Mover texto para um arquivos importados com `@arquivo.md` **não economiza contexto**.

Os imports também são carregados junto com o `CLAUDE.md`, então para reduzir o contexto permanente, prefira **rules com escopo por caminho** ou **skills carregadas sob demanda**.

> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Como Claude se lembra do seu projeto

> Dê a Claude instruções persistentes com arquivos CLAUDE.md e deixe Claude acumular aprendizados automaticamente com memória automática.

Cada sessão do Claude Code começa com uma janela de contexto limpa. Dois mecanismos carregam conhecimento entre sessões:

* **Arquivos CLAUDE.md**: instruções que você escreve para dar a Claude contexto persistente
* **Memória automática**: notas que Claude escreve para si mesma com base em suas correções e preferências

> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Como Claude se lembra do seu projeto

> Dê a Claude instruções persistentes com arquivos CLAUDE.md e deixe Claude acumular aprendizados automaticamente com memória automática.

Cada sessão do Claude Code começa com uma janela de contexto limpa. Dois mecanismos carregam conhecimento entre sessões:

* **Arquivos CLAUDE.md**: instruções que você escreve para dar a Claude contexto persistente
* **Memória automática**: notas que Claude escreve para si mesma com base em suas correções e preferências

Esta página cobre como:

* [Escrever e organizar arquivos CLAUDE.md](#claude-md-files)
* [Escopear regras para tipos de arquivo específicos](#organize-rules-with-claude/rules/) com `.claude/rules/`
* [Configurar memória automática](#auto-memory) para que Claude tome notas automaticamente
* [Solucionar problemas](#troubleshoot-memory-issues) quando as instruções não estão sendo seguidas

<h2 id="claude-md-vs-auto-memory">
  CLAUDE.md vs memória automática
</h2>

Claude Code tem dois sistemas de memória complementares. Ambos são carregados no início de cada conversa. Claude os trata como contexto, não como configuração imposta. Para bloquear uma ação independentemente do que Claude decidir, use um [hook PreToolUse](/docs/pt/hooks-guide) em vez disso. Quanto mais específicas e concisas forem suas instruções, mais consistentemente Claude as seguirá.

|                  | Arquivos CLAUDE.md                                                 | Memória automática                                                              |
| :--------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **Quem escreve** | Você                                                               | Claude                                                                          |
| **O que contém** | Instruções e regras                                                | Aprendizados e padrões                                                          |
| **Escopo**       | Projeto, usuário ou organização                                    | Por repositório, compartilhado entre worktrees                                  |
| **Carregado em** | Cada sessão                                                        | Cada sessão (primeiras 200 linhas ou 25KB)                                      |
| **Usar para**    | Padrões de codificação, fluxos de trabalho, arquitetura do projeto | Comandos de compilação, insights de depuração, preferências que Claude descobre |

Use arquivos CLAUDE.md quando quiser guiar o comportamento de Claude. A memória automática permite que Claude aprenda com suas correções sem esforço manual.

Subagents também podem manter sua própria memória automática. Veja [configuração de subagent](/docs/pt/sub-agents#enable-persistent-memory) para detalhes.

<h2 id="claude-md-files">
  Arquivos CLAUDE.md
</h2>

Arquivos CLAUDE.md são arquivos markdown que dão a Claude instruções persistentes para um projeto, seu fluxo de trabalho pessoal ou toda a sua organização. Você escreve esses arquivos em texto simples; Claude os lê no início de cada sessão.

<h3 id="when-to-add-to-claude-md">
  Quando adicionar a CLAUDE.md
</h3>

Trate CLAUDE.md como o lugar onde você escreve o que teria que re-explicar. Adicione a ele quando:

* Claude comete o mesmo erro uma segunda vez
* Uma revisão de código encontra algo que Claude deveria saber sobre esta base de código
* Você digita a mesma correção ou esclarecimento no chat que digitou na sessão anterior
* Um novo colega de equipe precisaria do mesmo contexto para ser produtivo

Mantenha-o com fatos que Claude deve manter em cada sessão: comandos de compilação, convenções, layout do projeto, regras "sempre faça X". Se uma entrada é um procedimento de múltiplas etapas ou só importa para uma parte da base de código, mova-a para uma [skill](/docs/pt/skills) ou uma [regra com escopo de caminho](#organize-rules-with-claude/rules/) em vez disso. A [visão geral da extensão](/docs/pt/features-overview#build-your-setup-over-time) cobre quando usar cada mecanismo.

<h3 id="choose-where-to-put-claude-md-files">
  Escolha onde colocar arquivos CLAUDE.md
</h3>

Arquivos CLAUDE.md podem estar em vários locais, cada um com um escopo diferente. A tabela abaixo lista-os em ordem de carregamento, do escopo mais amplo para o mais específico, então uma instrução de projeto aparece em contexto após uma instrução de usuário.

| Escopo                    | Localização                                                                                                                                                           | Propósito                                                             | Exemplos de caso de uso                                                               | Compartilhado com                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Política gerenciada**   | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux e WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Instruções em toda a organização gerenciadas por TI/DevOps            | Padrões de codificação da empresa, políticas de segurança, requisitos de conformidade | Todos os usuários da organização         |
| **Instruções do usuário** | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferências pessoais para todos os projetos                          | Preferências de estilo de código, atalhos de ferramentas pessoais                     | Apenas você (todos os projetos)          |
| **Instruções do projeto** | `./CLAUDE.md` ou `./.claude/CLAUDE.md`                                                                                                                                | Instruções compartilhadas pela equipe para o projeto                  | Arquitetura do projeto, padrões de codificação, fluxos de trabalho comuns             | Membros da equipe via controle de versão |
| **Instruções locais**     | `./CLAUDE.local.md`                                                                                                                                                   | Preferências pessoais específicas do projeto; adicione a `.gitignore` | Suas URLs de sandbox, dados de teste preferidos                                       | Apenas você (projeto atual)              |

Arquivos CLAUDE.md e CLAUDE.local.md no diretório acima do diretório de trabalho são carregados completamente no lançamento. Arquivos em subdiretórios são carregados sob demanda quando Claude lê arquivos nesses diretórios. Veja [Como arquivos CLAUDE.md são carregados](#how-claude-md-files-load) para a ordem de resolução completa.

Para projetos grandes, você pode dividir instruções em arquivos específicos de tópicos usando [regras de projeto](#organize-rules-with-claude/rules/). As regras permitem que você escope instruções para tipos de arquivo específicos ou subdiretórios.

<h3 id="set-up-a-project-claude-md">
  Configure um CLAUDE.md de projeto
</h3>

Um CLAUDE.md de projeto pode ser armazenado em `./CLAUDE.md` ou `./.claude/CLAUDE.md`. Crie este arquivo e adicione instruções que se apliquem a qualquer pessoa trabalhando no projeto: comandos de compilação e teste, padrões de codificação, decisões arquitetônicas, convenções de nomenclatura e fluxos de trabalho comuns. Essas instruções são compartilhadas com sua equipe através do controle de versão, então foque em padrões de nível de projeto em vez de preferências pessoais.

<Tip>
  Execute `/init` para gerar um CLAUDE.md inicial automaticamente. Claude analisa sua base de código e cria um arquivo com comandos de compilação, instruções de teste e convenções de projeto que descobre. Se um CLAUDE.md já existe, `/init` sugere melhorias em vez de sobrescrever. Refine a partir daí com instruções que Claude não descobriria por conta própria.

  Defina `CLAUDE_CODE_NEW_INIT=1` para ativar um fluxo interativo de múltiplas fases. `/init` pergunta quais artefatos configurar: arquivos CLAUDE.md, skills e hooks. Em seguida, explora sua base de código com um subagent, preenche lacunas por meio de perguntas de acompanhamento e apresenta uma proposta revisável antes de escrever qualquer arquivo.
</Tip>

<h3 id="write-effective-instructions">
  Escreva instruções eficazes
</h3>

Arquivos CLAUDE.md são carregados na janela de contexto no início de cada sessão, consumindo tokens junto com sua conversa. A [visualização da janela de contexto](/docs/pt/context-window) mostra onde CLAUDE.md é carregado em relação ao resto do contexto de inicialização. Como são contexto em vez de configuração imposta, como você escreve as instruções afeta o quão confiável Claude as segue. Instruções específicas, concisas e bem estruturadas funcionam melhor.

**Tamanho**: alvo de menos de 200 linhas por arquivo CLAUDE.md. Arquivos mais longos consomem mais contexto e reduzem a aderência. Se suas instruções estão crescendo muito, use [regras com escopo de caminho](#path-specific-rules) para que as instruções sejam carregadas apenas quando Claude trabalha com arquivos correspondentes. Você também pode dividir conteúdo em [importações](#import-additional-files) para organização, embora arquivos importados ainda sejam carregados e entrem na janela de contexto no lançamento.

**Estrutura**: use cabeçalhos markdown e bullets para agrupar instruções relacionadas. Claude escaneia a estrutura da mesma forma que os leitores fazem: seções organizadas são mais fáceis de seguir do que parágrafos densos.

**Especificidade**: escreva instruções que sejam concretas o suficiente para verificar. Por exemplo:

* "Use indentação de 2 espaços" em vez de "Formate o código adequadamente"
* "Execute `npm test` antes de fazer commit" em vez de "Teste suas alterações"
* "Manipuladores de API vivem em `src/api/handlers/`" em vez de "Mantenha os arquivos organizados"

**Consistência**: se duas regras se contradizem, Claude pode escolher uma arbitrariamente. Revise seus arquivos CLAUDE.md, arquivos CLAUDE.md aninhados em subdiretórios e [`.claude/rules/`](#organize-rules-with-claude/rules/) periodicamente para remover instruções desatualizadas ou conflitantes. Em monorepos, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) para pular arquivos CLAUDE.md de outras equipes que não são relevantes para seu trabalho.

<h3 id="import-additional-files">
  Importe arquivos adicionais
</h3>

Arquivos CLAUDE.md podem importar arquivos adicionais usando a sintaxe `@path/to/import`. Arquivos importados são expandidos e carregados em contexto no lançamento junto com o CLAUDE.md que os referencia.

Caminhos relativos e absolutos são permitidos. Caminhos relativos são resolvidos em relação ao arquivo contendo a importação, não ao diretório de trabalho. Arquivos importados podem importar recursivamente outros arquivos, com uma profundidade máxima de quatro saltos.

A análise de importação ignora spans de código Markdown e blocos de código cercados. Para mencionar um caminho em seu CLAUDE.md sem importá-lo, envolva-o em backticks: escrever `` `@README` `` mantém o texto literal, enquanto `@README` fora de backticks importa o arquivo.

Para trazer um README, package.json e um guia de fluxo de trabalho, referencie-os com a sintaxe `@` em qualquer lugar do seu CLAUDE.md:

```text theme={null}
Veja @README para visão geral do projeto e @package.json para comandos npm disponíveis para este projeto.

# Instruções Adicionais
- fluxo de trabalho git @docs/git-instructions.md
```

Para preferências pessoais por projeto que não devem ser verificadas no controle de versão, crie um `CLAUDE.local.md` na raiz do projeto. Ele é carregado junto com `CLAUDE.md` e é tratado da mesma forma. Adicione `CLAUDE.local.md` ao seu `.gitignore` para que não seja confirmado; executar `/init` e escolher a opção pessoal faz isso para você.

Se você trabalha em múltiplos git worktrees do mesmo repositório, um `CLAUDE.local.md` ignorado pelo git só existe no worktree onde você o criou. Para compartilhar instruções pessoais entre worktrees, importe um arquivo do seu diretório home em vez disso:

```text theme={null}
# Preferências Individuais
- @~/.claude/my-project-instructions.md
```

<Warning>
  A primeira vez que Claude Code encontra importações externas em um projeto, mostra um diálogo de aprovação listando os arquivos. Se você recusar, as importações permanecem desabilitadas e o diálogo não aparece novamente.
</Warning>

Para uma abordagem mais estruturada para organizar instruções, veja [`.claude/rules/`](#organize-rules-with-claude/rules/).

<h3 id="agents-md">
  AGENTS.md
</h3>

Claude Code lê `CLAUDE.md`, não `AGENTS.md`. Se seu repositório já usa `AGENTS.md` para outros agentes de codificação, crie um `CLAUDE.md` que o importe para que ambas as ferramentas leiam as mesmas instruções sem duplicá-las. Você também pode adicionar instruções específicas do Claude Code abaixo da importação. Claude carrega o arquivo importado no início da sessão, depois anexa o resto:

```markdown CLAUDE.md theme={null}
@AGENTS.md

## Claude Code

Use plan mode para alterações em `src/billing/`.
```

Um symlink também funciona se você não precisar adicionar conteúdo específico do Claude Code:

```bash theme={null}
ln -s AGENTS.md CLAUDE.md
```

No Windows, criar um symlink requer privilégios de Administrador ou Modo de Desenvolvedor, então use a importação `@AGENTS.md` em vez disso.

Executar [`/init`](/docs/pt/commands) em um repositório que já tem um `AGENTS.md` o lê e incorpora as partes relevantes no `CLAUDE.md` gerado. Ele também lê outras configurações de ferramentas como `.cursorrules`, `.devin/rules/` e `.windsurfrules`.

<h3 id="how-claude-md-files-load">
  Como arquivos CLAUDE.md são carregados
</h3>

Claude Code lê arquivos CLAUDE.md caminhando para cima na árvore de diretórios a partir do seu diretório de trabalho atual, verificando cada diretório ao longo do caminho para arquivos `CLAUDE.md` e `CLAUDE.local.md`. Isso significa que se você executar Claude Code em `foo/bar/`, ele carrega instruções de `foo/bar/CLAUDE.md`, `foo/CLAUDE.md` e qualquer arquivo `CLAUDE.local.md` ao lado deles.

Todos os arquivos descobertos são concatenados em contexto em vez de se sobreporem. Dentro da árvore de diretórios, o conteúdo é ordenado da raiz do sistema de arquivos até seu diretório de trabalho. Para o exemplo `foo/bar/`, `foo/CLAUDE.md` aparece em contexto antes de `foo/bar/CLAUDE.md`, então as instruções mais próximas de onde você lançou Claude são lidas por último. Dentro de cada diretório, `CLAUDE.local.md` é anexado após `CLAUDE.md`, então suas notas pessoais são a última coisa que Claude lê naquele nível.

Claude também descobre arquivos `CLAUDE.md` e `CLAUDE.local.md` em subdiretórios sob seu diretório de trabalho atual. Em vez de carregá-los no lançamento, eles são incluídos quando Claude lê arquivos nesses subdiretórios.

Se você trabalha em um grande monorepo onde arquivos CLAUDE.md de outras equipes são capturados, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) para pular. Para o layout completo de arquivos CLAUDE.md de raiz e por diretório e regras, veja [Monorepos e repositórios grandes](/docs/pt/large-codebases).

Comentários HTML em nível de bloco (`<!-- notas do mantenedor -->`) em arquivos CLAUDE.md são removidos antes do conteúdo ser injetado no contexto de Claude. Use-os para deixar notas para mantenedores humanos sem gastar tokens de contexto neles. Comentários dentro de blocos de código são preservados. Quando você abre um arquivo CLAUDE.md diretamente com a ferramenta Read, os comentários permanecem visíveis.

<h4 id="load-from-additional-directories">
  Carregue de diretórios adicionais
</h4>

A flag `--add-dir` dá a Claude acesso a diretórios adicionais fora do seu diretório de trabalho principal. Por padrão, arquivos CLAUDE.md desses diretórios não são carregados.

Para também carregar arquivos de memória de diretórios adicionais, defina a variável de ambiente `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

Isso carrega `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` e `CLAUDE.local.md` do diretório adicional. `CLAUDE.local.md` é ignorado se você excluir `local` de [`--setting-sources`](/docs/pt/cli-reference).

<h3 id="organize-rules-with-claude/rules/">
  Organize regras com `.claude/rules/`
</h3>

Para projetos maiores, você pode organizar instruções em múltiplos arquivos usando o diretório `.claude/rules/`. Isso mantém as instruções modulares e mais fáceis para as equipes manterem. As regras também podem ser [escopadas para caminhos de arquivo específicos](#path-specific-rules), então elas só são carregadas em contexto quando Claude trabalha com arquivos correspondentes, reduzindo ruído e economizando espaço de contexto.

<Note>
  As regras são carregadas em contexto a cada sessão ou quando arquivos correspondentes são abertos. Para instruções específicas de tarefa que não precisam estar em contexto o tempo todo, use [skills](/docs/pt/skills) em vez disso, que só são carregadas quando você as invoca ou quando Claude determina que são relevantes para seu prompt.
</Note>

<h4 id="set-up-rules">
  Configure regras
</h4>

Coloque arquivos markdown no diretório `.claude/rules/` do seu projeto. Cada arquivo deve cobrir um tópico, com um nome de arquivo descritivo como `testing.md` ou `api-design.md`. Todos os arquivos `.md` são descobertos recursivamente, então você pode organizar regras em subdiretórios como `frontend/` ou `backend/`:

```text theme={null}
seu-projeto/
├── .claude/
│   ├── CLAUDE.md           # Instruções principais do projeto
│   └── rules/
│       ├── code-style.md   # Diretrizes de estilo de código
│       ├── testing.md      # Convenções de teste
│       └── security.md     # Requisitos de segurança
```

Regras sem [frontmatter `paths`](#path-specific-rules) são carregadas no lançamento com a mesma prioridade que `.claude/CLAUDE.md`.

<h4 id="path-specific-rules">
  Regras específicas de caminho
</h4>

As regras podem ser escopadas para arquivos específicos usando frontmatter YAML com o campo `paths`. Essas regras condicionais só se aplicam quando Claude está trabalhando com arquivos correspondentes aos padrões especificados.

```markdown theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Regras de Desenvolvimento de API

- Todos os endpoints de API devem incluir validação de entrada
- Use o formato de resposta de erro padrão
- Inclua comentários de documentação OpenAPI
```

Regras sem um campo `paths` são carregadas incondicionalmente e se aplicam a todos os arquivos. Regras com escopo de caminho são acionadas quando Claude lê arquivos correspondentes ao padrão, não em cada uso de ferramenta. A partir da v2.1.198, a correspondência também funciona quando Claude alcança um arquivo através de um caminho vinculado simbolicamente para o diretório do projeto, por exemplo em um checkout vinculado simbolicamente.

Use padrões glob no campo `paths` para corresponder arquivos por extensão, diretório ou qualquer combinação:

| Padrão                 | Corresponde                                        |
| ---------------------- | -------------------------------------------------- |
| `**/*.ts`              | Todos os arquivos TypeScript em qualquer diretório |
| `src/**/*`             | Todos os arquivos sob o diretório `src/`           |
| `*.md`                 | Arquivos Markdown na raiz do projeto               |
| `src/components/*.tsx` | Componentes React em um diretório específico       |

Você pode especificar múltiplos padrões e usar expansão de chaves para corresponder múltiplas extensões em um padrão:

```markdown theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

Sintaxe glob trata `[` como o início de uma expressão de colchete como `[abc]`. Um padrão com um `[` que não pode ser lido como uma expressão de colchete, como `photos [2024/**`, é inválido: ele não corresponde a nada, e os outros padrões da regra continuam funcionando. Para corresponder um `[` literal em um nome de arquivo, escape-o como `photos \[2024/**`. Antes da v2.1.207, um padrão inválido fazia a ferramenta Read falhar para cada arquivo em que a regra era avaliada, em vez de não corresponder a nada.

<h4 id="share-rules-across-projects-with-symlinks">
  Compartilhe regras entre projetos com symlinks
</h4>

O diretório `.claude/rules/` suporta symlinks, então você pode manter um conjunto compartilhado de regras e vinculá-las em múltiplos projetos. Symlinks são resolvidos e carregados normalmente, e symlinks circulares são detectados e tratados graciosamente.

Este exemplo vincula tanto um diretório compartilhado quanto um arquivo individual:

```bash theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

<h4 id="user-level-rules">
  Regras de nível de usuário
</h4>

Regras pessoais em `~/.claude/rules/` se aplicam a cada projeto na sua máquina. Use-as para preferências que não são específicas do projeto:

```text theme={null}
~/.claude/rules/
├── preferences.md    # Suas preferências pessoais de codificação
└── workflows.md      # Seus fluxos de trabalho preferidos
```

Regras de nível de usuário são carregadas antes das regras de projeto, dando às regras de projeto prioridade mais alta.

<h3 id="manage-claude-md-for-large-teams">
  Gerencie CLAUDE.md para grandes equipes
</h3>

Para organizações implantando Claude Code em equipes, você pode centralizar instruções e controlar quais arquivos CLAUDE.md são carregados.

<h4 id="deploy-organization-wide-claude-md">
  Implante CLAUDE.md em toda a organização
</h4>

As organizações podem implantar um CLAUDE.md gerenciado centralmente que se aplica a todos os usuários em uma máquina. Este arquivo não pode ser excluído por configurações individuais.

<Steps>
  <Step title="Crie o arquivo no local da política gerenciada">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux e WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Implante com seu sistema de gerenciamento de configuração">
    Use MDM, Group Policy, Ansible ou ferramentas similares para distribuir o arquivo entre máquinas de desenvolvedores. Veja [configurações gerenciadas](/docs/pt/permissions#managed-settings) para outras opções de configuração em toda a organização.
  </Step>
</Steps>

A chave `claudeMd` permite que você coloque conteúdo CLAUDE.md gerenciado diretamente dentro de `managed-settings.json` em vez de implantar um arquivo separado.

**Escopo**: cada sessão de Claude Code na máquina, em cada repositório. Para orientação específica do repositório, confirme um CLAUDE.md de projeto em vez disso.

**Precedência**: igual a um arquivo CLAUDE.md gerenciado. Carrega antes de CLAUDE.md de usuário e projeto.

**Onde é honrado**: apenas configurações gerenciadas e de política. Definir `claudeMd` em configurações de usuário, projeto ou local não tem efeito.

O exemplo abaixo adiciona instruções comportamentais diretamente em um arquivo de configurações gerenciadas:

```json theme={null}
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
```

Um CLAUDE.md gerenciado e [configurações gerenciadas](/docs/pt/settings#settings-files) servem a propósitos diferentes. Use configurações para imposição técnica e CLAUDE.md para orientação comportamental:

| Preocupação                                                       | Configure em                                                       |
| :---------------------------------------------------------------- | :----------------------------------------------------------------- |
| Bloqueie ferramentas, comandos ou caminhos de arquivo específicos | Configurações gerenciadas: `permissions.deny`                      |
| Imponha isolamento de sandbox                                     | Configurações gerenciadas: `sandbox.enabled`                       |
| Variáveis de ambiente e roteamento de provedor de API             | Configurações gerenciadas: `env`                                   |
| Método de autenticação e bloqueio de organização                  | Configurações gerenciadas: `forceLoginMethod`, `forceLoginOrgUUID` |
| Diretrizes de estilo de código e qualidade                        | CLAUDE.md gerenciado                                               |
| Lembretes de manipulação de dados e conformidade                  | CLAUDE.md gerenciado                                               |
| Instruções comportamentais para Claude                            | CLAUDE.md gerenciado                                               |

Regras de configurações são impostas pelo cliente independentemente do que Claude decide fazer. Instruções de CLAUDE.md moldam o comportamento de Claude, mas não são uma camada de imposição rígida.

<h4 id="exclude-specific-claude-md-files">
  Exclua arquivos CLAUDE.md específicos
</h4>

Em grandes monorepos, arquivos CLAUDE.md ancestrais podem conter instruções que não são relevantes para seu trabalho. A configuração `claudeMdExcludes` permite que você pule arquivos específicos por caminho ou padrão glob.

Este exemplo exclui um CLAUDE.md de nível superior e um diretório de regras de uma pasta pai. Adicione-o a `.claude/settings.local.json` para que a exclusão permaneça local à sua máquina:

```json theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Padrões são correspondidos contra caminhos de arquivo absolutos usando sintaxe glob. Você pode configurar `claudeMdExcludes` em qualquer [camada de configurações](/docs/pt/settings#settings-files): usuário, projeto, local ou política gerenciada. Arrays são mesclados entre camadas.

Arquivos CLAUDE.md de política gerenciada não podem ser excluídos. Isso garante que as instruções em toda a organização sempre se apliquem independentemente das configurações individuais.

<h2 id="auto-memory">
  Memória automática
</h2>

A memória automática permite que Claude acumule conhecimento entre sessões sem você escrever nada. Claude salva notas para si mesma enquanto trabalha: comandos de compilação, insights de depuração, notas de arquitetura, preferências de estilo de código e hábitos de fluxo de trabalho. Claude não salva algo a cada sessão. Ela decide o que vale a pena lembrar com base em se a informação seria útil em uma conversa futura.

<h3 id="enable-or-disable-auto-memory">
  Ative ou desative a memória automática
</h3>

A memória automática está ativada por padrão. Para alterná-la, abra `/memory` em uma sessão e use o toggle de memória automática, ou defina `autoMemoryEnabled` nas configurações do seu projeto:

```json theme={null}
{
  "autoMemoryEnabled": false
}
```

Para desabilitar a memória automática via variável de ambiente, defina `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

<h3 id="storage-location">
  Local de armazenamento
</h3>

Cada projeto obtém seu próprio diretório de memória em `~/.claude/projects/<project>/memory/`. O caminho `<project>` é derivado do repositório git, então todos os worktrees e subdiretórios dentro do mesmo repositório compartilham um diretório de memória automática. Fora de um repositório git, a raiz do projeto é usada em vez disso.

Para armazenar memória automática em um local diferente, defina `autoMemoryDirectory` em seu `settings.json`. Ele é lido de qualquer [escopo de configurações](/docs/pt/settings#settings-precedence): usuário, projeto, local, política, ou `--settings`.

```json theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

O valor deve ser um caminho absoluto ou começar com `~/`. Quando definido no `.claude/settings.json` ou `.claude/settings.local.json` de um projeto, o valor é respeitado apenas após você aceitar o diálogo de confiança do workspace para essa pasta, o mesmo gate que governa hooks.

O diretório contém um ponto de entrada `MEMORY.md` e arquivos de tópico opcionais:

```text theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Índice conciso, carregado em cada sessão
├── debugging.md       # Notas detalhadas sobre padrões de depuração
├── api-conventions.md # Decisões de design de API
└── ...                # Qualquer outro arquivo de tópico que Claude cria
```

`MEMORY.md` atua como um índice do diretório de memória. Claude lê e escreve arquivos neste diretório ao longo de sua sessão, usando `MEMORY.md` para acompanhar o que está armazenado onde.

A memória automática é local da máquina. Todos os worktrees e subdiretórios dentro do mesmo repositório git compartilham um diretório de memória automática. Os arquivos não são compartilhados entre máquinas ou ambientes em nuvem.

<h3 id="how-it-works">
  Como funciona
</h3>

As primeiras 200 linhas de `MEMORY.md`, ou os primeiros 25KB, o que vier primeiro, são carregados no início de cada conversa. Conteúdo além desse limite não é carregado no início da sessão. Claude mantém `MEMORY.md` conciso movendo notas detalhadas para arquivos de tópico separados.

Este limite se aplica apenas a `MEMORY.md`. Arquivos CLAUDE.md são carregados completamente independentemente do comprimento, embora arquivos mais curtos produzam melhor aderência.

Arquivos de tópico como `debugging.md` ou `patterns.md` não são carregados na inicialização. Claude os lê sob demanda usando suas ferramentas de arquivo padrão quando precisa da informação.

Claude lê e escreve arquivos de memória durante sua sessão. Quando você vê "Writing memory" ou "Recalled memory" na interface do Claude Code, Claude está ativamente atualizando ou lendo de `~/.claude/projects/<project>/memory/`.

<h3 id="audit-and-edit-your-memory">
  Audite e edite sua memória
</h3>

Arquivos de memória automática são markdown simples que você pode editar ou deletar a qualquer momento. Execute [`/memory`](#view-and-edit-with-%2Fmemory) para navegar e abrir arquivos de memória de dentro de uma sessão.

<h2 id="view-and-edit-with-/memory">
  Visualize e edite com `/memory`
</h2>

O comando `/memory` lista todos os arquivos CLAUDE.md, CLAUDE.local.md e rules carregados em sua sessão atual, permite que você alterne a memória automática ativada ou desativada, e fornece um link para abrir a pasta de memória automática. Selecione qualquer arquivo para abri-lo no seu editor.

Quando você pede a Claude para lembrar algo, como "sempre use pnpm, não npm" ou "lembre-se de que os testes de API requerem uma instância local de Redis," Claude salva em memória automática. Para adicionar instruções a CLAUDE.md em vez disso, peça a Claude diretamente, como "adicione isto a CLAUDE.md," ou edite o arquivo você mesmo via `/memory`.

<h2 id="troubleshoot-memory-issues">
  Solucione problemas de memória
</h2>

Estes são os problemas mais comuns com CLAUDE.md e memória automática, junto com passos para depurá-los.

<h3 id="claude-isn’t-following-my-claude-md">
  Claude não está seguindo meu CLAUDE.md
</h3>

O conteúdo de CLAUDE.md é entregue como uma mensagem de usuário após o prompt do sistema, não como parte do próprio prompt do sistema. Claude o lê e tenta segui-lo, mas não há garantia de conformidade estrita, especialmente para instruções vagas ou conflitantes.

Para depurar:

* Execute `/memory` para verificar se seus arquivos CLAUDE.md e CLAUDE.local.md estão sendo carregados. Se um arquivo não estiver listado, Claude não pode vê-lo.
* Verifique se o CLAUDE.md relevante está em um local que é carregado para sua sessão (veja [Escolha onde colocar arquivos CLAUDE.md](#choose-where-to-put-claude-md-files)).
* Torne as instruções mais específicas. "Use indentação de 2 espaços" funciona melhor do que "formate o código adequadamente."
* Procure por instruções conflitantes entre arquivos CLAUDE.md. Se dois arquivos dão orientação diferente para o mesmo comportamento, Claude pode escolher um arbitrariamente.

Se a instrução é algo que deve ser executado em um ponto específico, como antes de cada commit ou após cada edição de arquivo, escreva-a como um [hook](/docs/pt/hooks-guide) em vez disso. Hooks são executados como comandos shell em eventos de ciclo de vida fixos e se aplicam independentemente do que Claude decidir fazer.

Para instruções que você quer no nível do prompt do sistema, use [`--append-system-prompt`](/docs/pt/cli-reference#system-prompt-flags). Isso deve ser passado a cada invocação, então é mais adequado para scripts e automação do que para uso interativo.

<Tip>
  Use o hook [`InstructionsLoaded`](/docs/pt/hooks#instructionsloaded) para registrar exatamente quais arquivos de instrução são carregados, quando são carregados e por quê. Isso é útil para depurar regras específicas de caminho ou arquivos carregados preguiçosamente em subdiretórios.
</Tip>

<h3 id="i-don’t-know-what-auto-memory-saved">
  Não sei o que a memória automática salvou
</h3>

Execute `/memory` e selecione a pasta de memória automática para navegar o que Claude salvou. Tudo é markdown simples que você pode ler, editar ou deletar.

<h3 id="my-claude-md-is-too-large">
  Meu CLAUDE.md é muito grande
</h3>

Arquivos com mais de 200 linhas consomem mais contexto e podem reduzir a aderência. Use [regras com escopo de caminho](#path-specific-rules) para carregar instruções apenas quando Claude trabalha com arquivos correspondentes, ou reduza conteúdo que não é necessário em cada sessão. Dividir em [importações `@path`](#import-additional-files) ajuda na organização, mas não reduz contexto, já que arquivos importados são carregados no lançamento.

O checkup [`/doctor`](/docs/pt/commands#all-commands) propõe cortes para um CLAUDE.md verificado: ele corta conteúdo que Claude pode derivar da base de código, como layouts de diretório, listas de dependências e visões gerais de arquitetura, e mantém armadilhas, justificativa e convenções que diferem dos padrões de ferramentas. A verificação de corte requer Claude Code v2.1.206 ou posterior.

<h3 id="instructions-seem-lost-after-/compact">
  Instruções parecem perdidas após `/compact`
</h3>

CLAUDE.md de raiz de projeto sobrevive à compactação: após `/compact`, Claude relê do disco e reinjecta no contexto. Arquivos CLAUDE.md aninhados em subdiretórios não são reinjetados automaticamente; eles recarregam na próxima vez que Claude lê um arquivo naquele subdiretório.

Se uma instrução desapareceu após compactação, ela foi dada apenas em conversa ou vive em um CLAUDE.md aninhado que ainda não recarregou. Adicione instruções apenas de conversa a CLAUDE.md para torná-las persistir.

***

<h2 id="claude-md-vs-auto-memory">
  CLAUDE.md vs memória automática
</h2>

Claude Code tem dois sistemas de memória complementares. Ambos são carregados no início de cada conversa. Claude os trata como contexto, não como configuração imposta. Para bloquear uma ação independentemente do que Claude decidir, use um [hook PreToolUse](/docs/pt/hooks-guide) em vez disso. Quanto mais específicas e concisas forem suas instruções, mais consistentemente Claude as seguirá.

|                  | Arquivos CLAUDE.md                                                 | Memória automática                                                              |
| :--------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **Quem escreve** | Você                                                               | Claude                                                                          |
| **O que contém** | Instruções e regras                                                | Aprendizados e padrões                                                          |
| **Escopo**       | Projeto, usuário ou organização                                    | Por repositório, compartilhado entre worktrees                                  |
| **Carregado em** | Cada sessão                                                        | Cada sessão (primeiras 200 linhas ou 25KB)                                      |
| **Usar para**    | Padrões de codificação, fluxos de trabalho, arquitetura do projeto | Comandos de compilação, insights de depuração, preferências que Claude descobre |

Use arquivos CLAUDE.md quando quiser guiar o comportamento de Claude. A memória automática permite que Claude aprenda com suas correções sem esforço manual.

Subagents também podem manter sua própria memória automática. Veja [configuração de subagent](/docs/pt/sub-agents#enable-persistent-memory) para detalhes.

<h2 id="claude-md-files">
  Arquivos CLAUDE.md
</h2>

Arquivos CLAUDE.md são arquivos markdown que dão a Claude instruções persistentes para um projeto, seu fluxo de trabalho pessoal ou toda a sua organização. Você escreve esses arquivos em texto simples; Claude os lê no início de cada sessão.

<h3 id="when-to-add-to-claude-md">
  Quando adicionar a CLAUDE.md
</h3>

Trate CLAUDE.md como o lugar onde você escreve o que teria que re-explicar. Adicione a ele quando:

* Claude comete o mesmo erro uma segunda vez
* Uma revisão de código encontra algo que Claude deveria saber sobre esta base de código
* Você digita a mesma correção ou esclarecimento no chat que digitou na sessão anterior
* Um novo colega de equipe precisaria do mesmo contexto para ser produtivo

Mantenha-o com fatos que Claude deve manter em cada sessão: comandos de compilação, convenções, layout do projeto, regras "sempre faça X". Se uma entrada é um procedimento de múltiplas etapas ou só importa para uma parte da base de código, mova-a para uma [skill](/docs/pt/skills) ou uma [regra com escopo de caminho](#organize-rules-with-claude/rules/) em vez disso. A [visão geral da extensão](/docs/pt/features-overview#build-your-setup-over-time) cobre quando usar cada mecanismo.

<h3 id="choose-where-to-put-claude-md-files">
  Escolha onde colocar arquivos CLAUDE.md
</h3>

Arquivos CLAUDE.md podem estar em vários locais, cada um com um escopo diferente. A tabela abaixo lista-os em ordem de carregamento, do escopo mais amplo para o mais específico, então uma instrução de projeto aparece em contexto após uma instrução de usuário.

| Escopo                    | Localização                                                                                                                                                           | Propósito                                                             | Exemplos de caso de uso                                                               | Compartilhado com                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Política gerenciada**   | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux e WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Instruções em toda a organização gerenciadas por TI/DevOps            | Padrões de codificação da empresa, políticas de segurança, requisitos de conformidade | Todos os usuários da organização         |
| **Instruções do usuário** | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferências pessoais para todos os projetos                          | Preferências de estilo de código, atalhos de ferramentas pessoais                     | Apenas você (todos os projetos)          |
| **Instruções do projeto** | `./CLAUDE.md` ou `./.claude/CLAUDE.md`                                                                                                                                | Instruções compartilhadas pela equipe para o projeto                  | Arquitetura do projeto, padrões de codificação, fluxos de trabalho comuns             | Membros da equipe via controle de versão |
| **Instruções locais**     | `./CLAUDE.local.md`                                                                                                                                                   | Preferências pessoais específicas do projeto; adicione a `.gitignore` | Suas URLs de sandbox, dados de teste preferidos                                       | Apenas você (projeto atual)              |

Arquivos CLAUDE.md e CLAUDE.local.md no diretório acima do diretório de trabalho são carregados completamente no lançamento. Arquivos em subdiretórios são carregados sob demanda quando Claude lê arquivos nesses diretórios. Veja [Como arquivos CLAUDE.md são carregados](#how-claude-md-files-load) para a ordem de resolução completa.

Para projetos grandes, você pode dividir instruções em arquivos específicos de tópicos usando [regras de projeto](#organize-rules-with-claude/rules/). As regras permitem que você escope instruções para tipos de arquivo específicos ou subdiretórios.

<h3 id="set-up-a-project-claude-md">
  Configure um CLAUDE.md de projeto
</h3>

Um CLAUDE.md de projeto pode ser armazenado em `./CLAUDE.md` ou `./.claude/CLAUDE.md`. Crie este arquivo e adicione instruções que se apliquem a qualquer pessoa trabalhando no projeto: comandos de compilação e teste, padrões de codificação, decisões arquitetônicas, convenções de nomenclatura e fluxos de trabalho comuns. Essas instruções são compartilhadas com sua equipe através do controle de versão, então foque em padrões de nível de projeto em vez de preferências pessoais.

<Tip>
  Execute `/init` para gerar um CLAUDE.md inicial automaticamente. Claude analisa sua base de código e cria um arquivo com comandos de compilação, instruções de teste e convenções de projeto que descobre. Se um CLAUDE.md já existe, `/init` sugere melhorias em vez de sobrescrever. Refine a partir daí com instruções que Claude não descobriria por conta própria.

  Defina `CLAUDE_CODE_NEW_INIT=1` para ativar um fluxo interativo de múltiplas fases. `/init` pergunta quais artefatos configurar: arquivos CLAUDE.md, skills e hooks. Em seguida, explora sua base de código com um subagent, preenche lacunas por meio de perguntas de acompanhamento e apresenta uma proposta revisável antes de escrever qualquer arquivo.
</Tip>

***
<!-- INÍCIO DA DELIMITAÇÃO DA CONSIDERAÇÃO OBRIGATÓRIA DE INSTRUÇÕES EFICAZES -->
<h1 id=instrucoes-eficazes>
  Escreva instruções eficazes
</h1>

Arquivos CLAUDE.md são carregados na janela de contexto no início de cada sessão, consumindo tokens junto com sua conversa. A visualização da janela de contexto mostra onde CLAUDE.md é carregado em relação ao resto do contexto de inicialização. Como são contexto em vez de configuração imposta, como você escreve as instruções afeta o quão confiável Claude as segue. Instruções específicas, concisas e bem estruturadas funcionam melhor.

**Tamanho**: alvo de menos de 200 linhas por arquivo CLAUDE.md. Arquivos mais longos consomem mais contexto e reduzem a aderência. Se suas instruções estão crescendo muito, use [regras com escopo de caminho](#path-specific-rules) para que as instruções sejam carregadas apenas quando Claude trabalha com arquivos correspondentes. Você também pode dividir conteúdo em [importações](#import-additional-files) para organização, embora arquivos importados ainda sejam carregados e entrem na janela de contexto no lançamento.

**Estrutura**: use cabeçalhos markdown e bullets para agrupar instruções relacionadas. Claude escaneia a estrutura da mesma forma que os leitores fazem: seções organizadas são mais fáceis de seguir do que parágrafos densos.

**Especificidade**: escreva instruções que sejam concretas o suficiente para verificar. Por exemplo:

* "Use indentação de 2 espaços" em vez de "Formate o código adequadamente"
* "Execute `npm test` antes de fazer commit" em vez de "Teste suas alterações"
* "Manipuladores de API vivem em `src/api/handlers/`" em vez de "Mantenha os arquivos organizados"

**Consistência**: se duas regras se contradizem, Claude pode escolher uma arbitrariamente. Revise seus arquivos CLAUDE.md, arquivos CLAUDE.md aninhados em subdiretórios e [`.claude/rules/`](#organize-rules-with-claude/rules/) periodicamente para remover instruções desatualizadas ou conflitantes. Em monorepos, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) para pular arquivos CLAUDE.md de outras equipes que não são relevantes para seu trabalho.

<h3 id="import-additional-files">
  Importe arquivos adicionais
</h3>

Arquivos CLAUDE.md podem importar arquivos adicionais usando a sintaxe `@path/to/import`. Arquivos importados são expandidos e carregados em contexto no lançamento junto com o CLAUDE.md que os referencia.

Caminhos relativos e absolutos são permitidos. Caminhos relativos são resolvidos em relação ao arquivo contendo a importação, não ao diretório de trabalho. Arquivos importados podem importar recursivamente outros arquivos, com uma profundidade máxima de quatro saltos.

A análise de importação ignora spans de código Markdown e blocos de código cercados. Para mencionar um caminho em seu CLAUDE.md sem importá-lo, envolva-o em backticks: escrever `` `@README` `` mantém o texto literal, enquanto `@README` fora de backticks importa o arquivo.

Para trazer um README, package.json e um guia de fluxo de trabalho, referencie-os com a sintaxe `@` em qualquer lugar do seu CLAUDE.md:

```text theme={null}
Veja @README para visão geral do projeto e @package.json para comandos npm disponíveis para este projeto.

# Instruções Adicionais
- fluxo de trabalho git @docs/git-instructions.md
```

Para preferências pessoais por projeto que não devem ser verificadas no controle de versão, crie um `CLAUDE.local.md` na raiz do projeto. Ele é carregado junto com `CLAUDE.md` e é tratado da mesma forma. Adicione `CLAUDE.local.md` ao seu `.gitignore` para que não seja confirmado; executar `/init` e escolher a opção pessoal faz isso para você.

Se você trabalha em múltiplos git worktrees do mesmo repositório, um `CLAUDE.local.md` ignorado pelo git só existe no worktree onde você o criou. Para compartilhar instruções pessoais entre worktrees, importe um arquivo do seu diretório home em vez disso:

```text theme={null}
# Preferências Individuais
- @~/.claude/my-project-instructions.md
```

<Warning>
  A primeira vez que Claude Code encontra importações externas em um projeto, mostra um diálogo de aprovação listando os arquivos. Se você recusar, as importações permanecem desabilitadas e o diálogo não aparece novamente.
</Warning>

Para uma abordagem mais estruturada para organizar instruções, veja [`.claude/rules/`](#organize-rules-with-claude/rules/).

<h3 id="agents-md">
  AGENTS.md
</h3>

Claude Code lê `CLAUDE.md`, não `AGENTS.md`. Se seu repositório já usa `AGENTS.md` para outros agentes de codificação, crie um `CLAUDE.md` que o importe para que ambas as ferramentas leiam as mesmas instruções sem duplicá-las. Você também pode adicionar instruções específicas do Claude Code abaixo da importação. Claude carrega o arquivo importado no início da sessão, depois anexa o resto:

```markdown CLAUDE.md theme={null}
@AGENTS.md

## Claude Code

Use plan mode para alterações em `src/billing/`.
```

Um symlink também funciona se você não precisar adicionar conteúdo específico do Claude Code:

```bash theme={null}
ln -s AGENTS.md CLAUDE.md
```

No Windows, criar um symlink requer privilégios de Administrador ou Modo de Desenvolvedor, então use a importação `@AGENTS.md` em vez disso.

Executar [`/init`](/docs/pt/commands) em um repositório que já tem um `AGENTS.md` o lê e incorpora as partes relevantes no `CLAUDE.md` gerado. Ele também lê outras configurações de ferramentas como `.cursorrules`, `.devin/rules/` e `.windsurfrules`.

<h3 id="how-claude-md-files-load">
  Como arquivos CLAUDE.md são carregados
</h3>

Claude Code lê arquivos CLAUDE.md caminhando para cima na árvore de diretórios a partir do seu diretório de trabalho atual, verificando cada diretório ao longo do caminho para arquivos `CLAUDE.md` e `CLAUDE.local.md`. Isso significa que se você executar Claude Code em `foo/bar/`, ele carrega instruções de `foo/bar/CLAUDE.md`, `foo/CLAUDE.md` e qualquer arquivo `CLAUDE.local.md` ao lado deles.

Todos os arquivos descobertos são concatenados em contexto em vez de se sobreporem. Dentro da árvore de diretórios, o conteúdo é ordenado da raiz do sistema de arquivos até seu diretório de trabalho. Para o exemplo `foo/bar/`, `foo/CLAUDE.md` aparece em contexto antes de `foo/bar/CLAUDE.md`, então as instruções mais próximas de onde você lançou Claude são lidas por último. Dentro de cada diretório, `CLAUDE.local.md` é anexado após `CLAUDE.md`, então suas notas pessoais são a última coisa que Claude lê naquele nível.

Claude também descobre arquivos `CLAUDE.md` e `CLAUDE.local.md` em subdiretórios sob seu diretório de trabalho atual. Em vez de carregá-los no lançamento, eles são incluídos quando Claude lê arquivos nesses subdiretórios.

Se você trabalha em um grande monorepo onde arquivos CLAUDE.md de outras equipes são capturados, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) para pular. Para o layout completo de arquivos CLAUDE.md de raiz e por diretório e regras, veja [Monorepos e repositórios grandes](/docs/pt/large-codebases).

Comentários HTML em nível de bloco (`<!-- notas do mantenedor -->`) em arquivos CLAUDE.md são removidos antes do conteúdo ser injetado no contexto de Claude. Use-os para deixar notas para mantenedores humanos sem gastar tokens de contexto neles. Comentários dentro de blocos de código são preservados. Quando você abre um arquivo CLAUDE.md diretamente com a ferramenta Read, os comentários permanecem visíveis.

<h4 id="load-from-additional-directories">
  Carregue de diretórios adicionais
</h4>

A flag `--add-dir` dá a Claude acesso a diretórios adicionais fora do seu diretório de trabalho principal. Por padrão, arquivos CLAUDE.md desses diretórios não são carregados.

Para também carregar arquivos de memória de diretórios adicionais, defina a variável de ambiente `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

Isso carrega `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` e `CLAUDE.local.md` do diretório adicional. `CLAUDE.local.md` é ignorado se você excluir `local` de [`--setting-sources`](/docs/pt/cli-reference).

<h3 id="organize-rules-with-claude/rules/">
  Organize regras com `.claude/rules/`
</h3>

Para projetos maiores, você pode organizar instruções em múltiplos arquivos usando o diretório `.claude/rules/`. Isso mantém as instruções modulares e mais fáceis para as equipes manterem. As regras também podem ser [escopadas para caminhos de arquivo específicos](#path-specific-rules), então elas só são carregadas em contexto quando Claude trabalha com arquivos correspondentes, reduzindo ruído e economizando espaço de contexto.

<Note>
  As regras são carregadas em contexto a cada sessão ou quando arquivos correspondentes são abertos. Para instruções específicas de tarefa que não precisam estar em contexto o tempo todo, use [skills](/docs/pt/skills) em vez disso, que só são carregadas quando você as invoca ou quando Claude determina que são relevantes para seu prompt.
</Note>

<h4 id="set-up-rules">
  Configure regras
</h4>

Coloque arquivos markdown no diretório `.claude/rules/` do seu projeto. Cada arquivo deve cobrir um tópico, com um nome de arquivo descritivo como `testing.md` ou `api-design.md`. Todos os arquivos `.md` são descobertos recursivamente, então você pode organizar regras em subdiretórios como `frontend/` ou `backend/`:

```text theme={null}
seu-projeto/
├── .claude/
│   ├── CLAUDE.md           # Instruções principais do projeto
│   └── rules/
│       ├── code-style.md   # Diretrizes de estilo de código
│       ├── testing.md      # Convenções de teste
│       └── security.md     # Requisitos de segurança
```

Regras sem [frontmatter `paths`](#path-specific-rules) são carregadas no lançamento com a mesma prioridade que `.claude/CLAUDE.md`.

<h4 id="path-specific-rules">
  Regras específicas de caminho
</h4>

As regras podem ser escopadas para arquivos específicos usando frontmatter YAML com o campo `paths`. Essas regras condicionais só se aplicam quando Claude está trabalhando com arquivos correspondentes aos padrões especificados.

```markdown theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Regras de Desenvolvimento de API

- Todos os endpoints de API devem incluir validação de entrada
- Use o formato de resposta de erro padrão
- Inclua comentários de documentação OpenAPI
```

- Regras sem um campo `paths` são carregadas incondicionalmente e se aplicam a todos os arquivos.
- Regras com escopo de caminho são acionadas quando Claude lê arquivos correspondentes ao padrão, não em cada uso de ferramenta.
- A partir da v2.1.198, a correspondência também funciona quando Claude alcança um arquivo através de um caminho vinculado simbolicamente para o diretório do projeto, por exemplo em um checkout vinculado simbolicamente.

Use padrões glob no campo `paths` para corresponder arquivos por extensão, diretório ou qualquer combinação:

| Padrão                 | Corresponde                                        |
| ---------------------- | -------------------------------------------------- |
| `**/*.ts`              | Todos os arquivos TypeScript em qualquer diretório |
| `src/**/*`             | Todos os arquivos sob o diretório `src/`           |
| `*.md`                 | Arquivos Markdown na raiz do projeto               |
| `src/components/*.tsx` | Componentes React em um diretório específico       |

Você pode especificar múltiplos padrões e usar expansão de chaves para corresponder múltiplas extensões em um padrão:

```markdown theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

Sintaxe glob trata `[` como o início de uma expressão de colchete como `[abc]`. Um padrão com um `[` que não pode ser lido como uma expressão de colchete, como `photos [2024/**`, é inválido: ele não corresponde a nada, e os outros padrões da regra continuam funcionando. Para corresponder um `[` literal em um nome de arquivo, escape-o como `photos \[2024/**`. Antes da v2.1.207, um padrão inválido fazia a ferramenta Read falhar para cada arquivo em que a regra era avaliada, em vez de não corresponder a nada.

<h4 id="share-rules-across-projects-with-symlinks">
  Compartilhe regras entre projetos com symlinks
</h4>

O diretório `.claude/rules/` suporta symlinks, então você pode manter um conjunto compartilhado de regras e vinculá-las em múltiplos projetos. Symlinks são resolvidos e carregados normalmente, e symlinks circulares são detectados e tratados graciosamente.

Este exemplo vincula tanto um diretório compartilhado quanto um arquivo individual:

```bash theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

<h4 id="user-level-rules">
  Regras de nível de usuário
</h4>

Regras pessoais em `~/.claude/rules/` se aplicam a cada projeto na sua máquina. Use-as para preferências que não são específicas do projeto:

```text theme={null}
~/.claude/rules/
├── preferences.md    # Suas preferências pessoais de codificação
└── workflows.md      # Seus fluxos de trabalho preferidos
```

Regras de nível de usuário são carregadas antes das regras de projeto, dando às regras de projeto prioridade mais alta.

<!-- FIM DA DELIMITAÇÃO DA CONSIDERAÇÃO OBRIGATÓRIA DE INSTRUÇÕES EFICAZES -->

<h3 id="manage-claude-md-for-large-teams">
  Gerencie CLAUDE.md para grandes equipes
</h3>

Para organizações implantando Claude Code em equipes, você pode centralizar instruções e controlar quais arquivos CLAUDE.md são carregados.

<h4 id="deploy-organization-wide-claude-md">
  Implante CLAUDE.md em toda a organização
</h4>

As organizações podem implantar um CLAUDE.md gerenciado centralmente que se aplica a todos os usuários em uma máquina. Este arquivo não pode ser excluído por configurações individuais.

<Steps>
  <Step title="Crie o arquivo no local da política gerenciada">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux e WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Implante com seu sistema de gerenciamento de configuração">
    Use MDM, Group Policy, Ansible ou ferramentas similares para distribuir o arquivo entre máquinas de desenvolvedores. Veja [configurações gerenciadas](/docs/pt/permissions#managed-settings) para outras opções de configuração em toda a organização.
  </Step>
</Steps>

A chave `claudeMd` permite que você coloque conteúdo CLAUDE.md gerenciado diretamente dentro de `managed-settings.json` em vez de implantar um arquivo separado.

**Escopo**: cada sessão de Claude Code na máquina, em cada repositório. Para orientação específica do repositório, confirme um CLAUDE.md de projeto em vez disso.

**Precedência**: igual a um arquivo CLAUDE.md gerenciado. Carrega antes de CLAUDE.md de usuário e projeto.

**Onde é honrado**: apenas configurações gerenciadas e de política. Definir `claudeMd` em configurações de usuário, projeto ou local não tem efeito.

O exemplo abaixo adiciona instruções comportamentais diretamente em um arquivo de configurações gerenciadas:

```json theme={null}
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
```

Um CLAUDE.md gerenciado e [configurações gerenciadas](/docs/pt/settings#settings-files) servem a propósitos diferentes. Use configurações para imposição técnica e CLAUDE.md para orientação comportamental:

| Preocupação                                                       | Configure em                                                       |
| :---------------------------------------------------------------- | :----------------------------------------------------------------- |
| Bloqueie ferramentas, comandos ou caminhos de arquivo específicos | Configurações gerenciadas: `permissions.deny`                      |
| Imponha isolamento de sandbox                                     | Configurações gerenciadas: `sandbox.enabled`                       |
| Variáveis de ambiente e roteamento de provedor de API             | Configurações gerenciadas: `env`                                   |
| Método de autenticação e bloqueio de organização                  | Configurações gerenciadas: `forceLoginMethod`, `forceLoginOrgUUID` |
| Diretrizes de estilo de código e qualidade                        | CLAUDE.md gerenciado                                               |
| Lembretes de manipulação de dados e conformidade                  | CLAUDE.md gerenciado                                               |
| Instruções comportamentais para Claude                            | CLAUDE.md gerenciado                                               |

Regras de configurações são impostas pelo cliente independentemente do que Claude decide fazer. Instruções de CLAUDE.md moldam o comportamento de Claude, mas não são uma camada de imposição rígida.

<h4 id="exclude-specific-claude-md-files">
  Exclua arquivos CLAUDE.md específicos
</h4>

Em grandes monorepos, arquivos CLAUDE.md ancestrais podem conter instruções que não são relevantes para seu trabalho. A configuração `claudeMdExcludes` permite que você pule arquivos específicos por caminho ou padrão glob.

Este exemplo exclui um CLAUDE.md de nível superior e um diretório de regras de uma pasta pai. Adicione-o a `.claude/settings.local.json` para que a exclusão permaneça local à sua máquina:

```json theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Padrões são correspondidos contra caminhos de arquivo absolutos usando sintaxe glob. Você pode configurar `claudeMdExcludes` em qualquer [camada de configurações](/docs/pt/settings#settings-files): usuário, projeto, local ou política gerenciada. Arrays são mesclados entre camadas.

Arquivos CLAUDE.md de política gerenciada não podem ser excluídos. Isso garante que as instruções em toda a organização sempre se apliquem independentemente das configurações individuais.

<h2 id="auto-memory">
  Memória automática
</h2>

A memória automática permite que Claude acumule conhecimento entre sessões sem você escrever nada. Claude salva notas para si mesma enquanto trabalha: comandos de compilação, insights de depuração, notas de arquitetura, preferências de estilo de código e hábitos de fluxo de trabalho. Claude não salva algo a cada sessão. Ela decide o que vale a pena lembrar com base em se a informação seria útil em uma conversa futura.

<h3 id="enable-or-disable-auto-memory">
  Ative ou desative a memória automática
</h3>

A memória automática está ativada por padrão. Para alterná-la, abra `/memory` em uma sessão e use o toggle de memória automática, ou defina `autoMemoryEnabled` nas configurações do seu projeto:

```json theme={null}
{
  "autoMemoryEnabled": false
}
```

Para desabilitar a memória automática via variável de ambiente, defina `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

<h3 id="storage-location">
  Local de armazenamento
</h3>

Cada projeto obtém seu próprio diretório de memória em `~/.claude/projects/<project>/memory/`. O caminho `<project>` é derivado do repositório git, então todos os worktrees e subdiretórios dentro do mesmo repositório compartilham um diretório de memória automática. Fora de um repositório git, a raiz do projeto é usada em vez disso.

Para armazenar memória automática em um local diferente, defina `autoMemoryDirectory` em seu `settings.json`. Ele é lido de qualquer [escopo de configurações](/docs/pt/settings#settings-precedence): usuário, projeto, local, política, ou `--settings`.

```json theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

O valor deve ser um caminho absoluto ou começar com `~/`. Quando definido no `.claude/settings.json` ou `.claude/settings.local.json` de um projeto, o valor é respeitado apenas após você aceitar o diálogo de confiança do workspace para essa pasta, o mesmo gate que governa hooks.

O diretório contém um ponto de entrada `MEMORY.md` e arquivos de tópico opcionais:

```text theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Índice conciso, carregado em cada sessão
├── debugging.md       # Notas detalhadas sobre padrões de depuração
├── api-conventions.md # Decisões de design de API
└── ...                # Qualquer outro arquivo de tópico que Claude cria
```

`MEMORY.md` atua como um índice do diretório de memória. Claude lê e escreve arquivos neste diretório ao longo de sua sessão, usando `MEMORY.md` para acompanhar o que está armazenado onde.

A memória automática é local da máquina. Todos os worktrees e subdiretórios dentro do mesmo repositório git compartilham um diretório de memória automática. Os arquivos não são compartilhados entre máquinas ou ambientes em nuvem.

<h3 id="how-it-works">
  Como funciona
</h3>

As primeiras 200 linhas de `MEMORY.md`, ou os primeiros 25KB, o que vier primeiro, são carregados no início de cada conversa. Conteúdo além desse limite não é carregado no início da sessão. Claude mantém `MEMORY.md` conciso movendo notas detalhadas para arquivos de tópico separados.

Este limite se aplica apenas a `MEMORY.md`. Arquivos CLAUDE.md são carregados completamente independentemente do comprimento, embora arquivos mais curtos produzam melhor aderência.

Arquivos de tópico como `debugging.md` ou `patterns.md` não são carregados na inicialização. Claude os lê sob demanda usando suas ferramentas de arquivo padrão quando precisa da informação.

Claude lê e escreve arquivos de memória durante sua sessão. Quando você vê "Writing memory" ou "Recalled memory" na interface do Claude Code, Claude está ativamente atualizando ou lendo de `~/.claude/projects/<project>/memory/`.

<h3 id="audit-and-edit-your-memory">
  Audite e edite sua memória
</h3>

Arquivos de memória automática são markdown simples que você pode editar ou deletar a qualquer momento. Execute [`/memory`](#view-and-edit-with-%2Fmemory) para navegar e abrir arquivos de memória de dentro de uma sessão.

<h2 id="view-and-edit-with-/memory">
  Visualize e edite com `/memory`
</h2>

O comando `/memory` lista todos os arquivos CLAUDE.md, CLAUDE.local.md e rules carregados em sua sessão atual, permite que você alterne a memória automática ativada ou desativada, e fornece um link para abrir a pasta de memória automática. Selecione qualquer arquivo para abri-lo no seu editor.

Quando você pede a Claude para lembrar algo, como "sempre use pnpm, não npm" ou "lembre-se de que os testes de API requerem uma instância local de Redis," Claude salva em memória automática. Para adicionar instruções a CLAUDE.md em vez disso, peça a Claude diretamente, como "adicione isto a CLAUDE.md," ou edite o arquivo você mesmo via `/memory`.

<h2 id="troubleshoot-memory-issues">
  Solucione problemas de memória
</h2>

Estes são os problemas mais comuns com CLAUDE.md e memória automática, junto com passos para depurá-los.

<h3 id="claude-isn’t-following-my-claude-md">
  Claude não está seguindo meu CLAUDE.md
</h3>

O conteúdo de CLAUDE.md é entregue como uma mensagem de usuário após o prompt do sistema, não como parte do próprio prompt do sistema. Claude o lê e tenta segui-lo, mas não há garantia de conformidade estrita, especialmente para instruções vagas ou conflitantes.

Para depurar:

* Execute `/memory` para verificar se seus arquivos CLAUDE.md e CLAUDE.local.md estão sendo carregados. Se um arquivo não estiver listado, Claude não pode vê-lo.
* Verifique se o CLAUDE.md relevante está em um local que é carregado para sua sessão (veja [Escolha onde colocar arquivos CLAUDE.md](#choose-where-to-put-claude-md-files)).
* Torne as instruções mais específicas. "Use indentação de 2 espaços" funciona melhor do que "formate o código adequadamente."
* Procure por instruções conflitantes entre arquivos CLAUDE.md. Se dois arquivos dão orientação diferente para o mesmo comportamento, Claude pode escolher um arbitrariamente.

Se a instrução é algo que deve ser executado em um ponto específico, como antes de cada commit ou após cada edição de arquivo, escreva-a como um [hook](/docs/pt/hooks-guide) em vez disso. Hooks são executados como comandos shell em eventos de ciclo de vida fixos e se aplicam independentemente do que Claude decidir fazer.

Para instruções que você quer no nível do prompt do sistema, use [`--append-system-prompt`](/docs/pt/cli-reference#system-prompt-flags). Isso deve ser passado a cada invocação, então é mais adequado para scripts e automação do que para uso interativo.

<Tip>
  Use o hook [`InstructionsLoaded`](/docs/pt/hooks#instructionsloaded) para registrar exatamente quais arquivos de instrução são carregados, quando são carregados e por quê. Isso é útil para depurar regras específicas de caminho ou arquivos carregados preguiçosamente em subdiretórios.
</Tip>

<h3 id="i-don’t-know-what-auto-memory-saved">
  Não sei o que a memória automática salvou
</h3>

Execute `/memory` e selecione a pasta de memória automática para navegar o que Claude salvou. Tudo é markdown simples que você pode ler, editar ou deletar.

<h3 id="my-claude-md-is-too-large">
  Meu CLAUDE.md é muito grande
</h3>

Arquivos com mais de 200 linhas consomem mais contexto e podem reduzir a aderência. Use [regras com escopo de caminho](#path-specific-rules) para carregar instruções apenas quando Claude trabalha com arquivos correspondentes, ou reduza conteúdo que não é necessário em cada sessão. Dividir em [importações `@path`](#import-additional-files) ajuda na organização, mas não reduz contexto, já que arquivos importados são carregados no lançamento.

O checkup [`/doctor`](/docs/pt/commands#all-commands) propõe cortes para um CLAUDE.md verificado: ele corta conteúdo que Claude pode derivar da base de código, como layouts de diretório, listas de dependências e visões gerais de arquitetura, e mantém armadilhas, justificativa e convenções que diferem dos padrões de ferramentas. A verificação de corte requer Claude Code v2.1.206 ou posterior.

<h3 id="instructions-seem-lost-after-/compact">
  Instruções parecem perdidas após `/compact`
</h3>

CLAUDE.md de raiz de projeto sobrevive à compactação: após `/compact`, Claude relê do disco e reinjecta no contexto. Arquivos CLAUDE.md aninhados em subdiretórios não são reinjetados automaticamente; eles recarregam na próxima vez que Claude lê um arquivo naquele subdiretório.

Se uma instrução desapareceu após compactação, ela foi dada apenas em conversa ou vive em um CLAUDE.md aninhado que ainda não recarregou. Adicione instruções apenas de conversa a CLAUDE.md para torná-las persistir.

> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Como Claude se lembra do seu projeto

> Dê a Claude instruções persistentes com arquivos CLAUDE.md e deixe Claude acumular aprendizados automaticamente com memória automática.

Cada sessão do Claude Code começa com uma janela de contexto limpa. Dois mecanismos carregam conhecimento entre sessões:

* **Arquivos CLAUDE.md**: instruções que você escreve para dar a Claude contexto persistente
* **Memória automática**: notas que Claude escreve para si mesma com base em suas correções e preferências

Esta página cobre como:

* [Escrever e organizar arquivos CLAUDE.md](#claude-md-files)
* [Escopear regras para tipos de arquivo específicos](#organize-rules-with-claude/rules/) com `.claude/rules/`
* [Configurar memória automática](#auto-memory) para que Claude tome notas automaticamente
* [Solucionar problemas](#troubleshoot-memory-issues) quando as instruções não estão sendo seguidas

<h2 id="claude-md-vs-auto-memory">
  CLAUDE.md vs memória automática
</h2>

Claude Code tem dois sistemas de memória complementares. Ambos são carregados no início de cada conversa. Claude os trata como contexto, não como configuração imposta. Para bloquear uma ação independentemente do que Claude decidir, use um [hook PreToolUse](/docs/pt/hooks-guide) em vez disso. Quanto mais específicas e concisas forem suas instruções, mais consistentemente Claude as seguirá.

|                  | Arquivos CLAUDE.md                                                 | Memória automática                                                              |
| :--------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **Quem escreve** | Você                                                               | Claude                                                                          |
| **O que contém** | Instruções e regras                                                | Aprendizados e padrões                                                          |
| **Escopo**       | Projeto, usuário ou organização                                    | Por repositório, compartilhado entre worktrees                                  |
| **Carregado em** | Cada sessão                                                        | Cada sessão (primeiras 200 linhas ou 25KB)                                      |
| **Usar para**    | Padrões de codificação, fluxos de trabalho, arquitetura do projeto | Comandos de compilação, insights de depuração, preferências que Claude descobre |

Use arquivos CLAUDE.md quando quiser guiar o comportamento de Claude. A memória automática permite que Claude aprenda com suas correções sem esforço manual.

Subagents também podem manter sua própria memória automática. Veja [configuração de subagent](/docs/pt/sub-agents#enable-persistent-memory) para detalhes.

<h2 id="claude-md-files">
  Arquivos CLAUDE.md
</h2>

Arquivos CLAUDE.md são arquivos markdown que dão a Claude instruções persistentes para um projeto, seu fluxo de trabalho pessoal ou toda a sua organização. Você escreve esses arquivos em texto simples; Claude os lê no início de cada sessão.

<h3 id="when-to-add-to-claude-md">
  Quando adicionar a CLAUDE.md
</h3>

Trate CLAUDE.md como o lugar onde você escreve o que teria que re-explicar. Adicione a ele quando:

* Claude comete o mesmo erro uma segunda vez
* Uma revisão de código encontra algo que Claude deveria saber sobre esta base de código
* Você digita a mesma correção ou esclarecimento no chat que digitou na sessão anterior
* Um novo colega de equipe precisaria do mesmo contexto para ser produtivo

Mantenha-o com fatos que Claude deve manter em cada sessão: comandos de compilação, convenções, layout do projeto, regras "sempre faça X". Se uma entrada é um procedimento de múltiplas etapas ou só importa para uma parte da base de código, mova-a para uma [skill](/docs/pt/skills) ou uma [regra com escopo de caminho](#organize-rules-with-claude/rules/) em vez disso. A [visão geral da extensão](/docs/pt/features-overview#build-your-setup-over-time) cobre quando usar cada mecanismo.

<h3 id="choose-where-to-put-claude-md-files">
  Escolha onde colocar arquivos CLAUDE.md
</h3>

Arquivos CLAUDE.md podem estar em vários locais, cada um com um escopo diferente. A tabela abaixo lista-os em ordem de carregamento, do escopo mais amplo para o mais específico, então uma instrução de projeto aparece em contexto após uma instrução de usuário.

| Escopo                    | Localização                                                                                                                                                           | Propósito                                                             | Exemplos de caso de uso                                                               | Compartilhado com                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Política gerenciada**   | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux e WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Instruções em toda a organização gerenciadas por TI/DevOps            | Padrões de codificação da empresa, políticas de segurança, requisitos de conformidade | Todos os usuários da organização         |
| **Instruções do usuário** | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferências pessoais para todos os projetos                          | Preferências de estilo de código, atalhos de ferramentas pessoais                     | Apenas você (todos os projetos)          |
| **Instruções do projeto** | `./CLAUDE.md` ou `./.claude/CLAUDE.md`                                                                                                                                | Instruções compartilhadas pela equipe para o projeto                  | Arquitetura do projeto, padrões de codificação, fluxos de trabalho comuns             | Membros da equipe via controle de versão |
| **Instruções locais**     | `./CLAUDE.local.md`                                                                                                                                                   | Preferências pessoais específicas do projeto; adicione a `.gitignore` | Suas URLs de sandbox, dados de teste preferidos                                       | Apenas você (projeto atual)              |

Arquivos CLAUDE.md e CLAUDE.local.md no diretório acima do diretório de trabalho são carregados completamente no lançamento. Arquivos em subdiretórios são carregados sob demanda quando Claude lê arquivos nesses diretórios. Veja [Como arquivos CLAUDE.md são carregados](#how-claude-md-files-load) para a ordem de resolução completa.

Para projetos grandes, você pode dividir instruções em arquivos específicos de tópicos usando [regras de projeto](#organize-rules-with-claude/rules/). As regras permitem que você escope instruções para tipos de arquivo específicos ou subdiretórios.

<h3 id="set-up-a-project-claude-md">
  Configure um CLAUDE.md de projeto
</h3>

Um CLAUDE.md de projeto pode ser armazenado em `./CLAUDE.md` ou `./.claude/CLAUDE.md`. Crie este arquivo e adicione instruções que se apliquem a qualquer pessoa trabalhando no projeto: comandos de compilação e teste, padrões de codificação, decisões arquitetônicas, convenções de nomenclatura e fluxos de trabalho comuns. Essas instruções são compartilhadas com sua equipe através do controle de versão, então foque em padrões de nível de projeto em vez de preferências pessoais.

<Tip>
  Execute `/init` para gerar um CLAUDE.md inicial automaticamente. Claude analisa sua base de código e cria um arquivo com comandos de compilação, instruções de teste e convenções de projeto que descobre. Se um CLAUDE.md já existe, `/init` sugere melhorias em vez de sobrescrever. Refine a partir daí com instruções que Claude não descobriria por conta própria.

  Defina `CLAUDE_CODE_NEW_INIT=1` para ativar um fluxo interativo de múltiplas fases. `/init` pergunta quais artefatos configurar: arquivos CLAUDE.md, skills e hooks. Em seguida, explora sua base de código com um subagent, preenche lacunas por meio de perguntas de acompanhamento e apresenta uma proposta revisável antes de escrever qualquer arquivo.
</Tip>

<h3 id="write-effective-instructions">
  Escreva instruções eficazes
</h3>

Arquivos CLAUDE.md são carregados na janela de contexto no início de cada sessão, consumindo tokens junto com sua conversa. A [visualização da janela de contexto](/docs/pt/context-window) mostra onde CLAUDE.md é carregado em relação ao resto do contexto de inicialização. Como são contexto em vez de configuração imposta, como você escreve as instruções afeta o quão confiável Claude as segue. Instruções específicas, concisas e bem estruturadas funcionam melhor.

**Tamanho**: alvo de menos de 200 linhas por arquivo CLAUDE.md. Arquivos mais longos consomem mais contexto e reduzem a aderência. Se suas instruções estão crescendo muito, use [regras com escopo de caminho](#path-specific-rules) para que as instruções sejam carregadas apenas quando Claude trabalha com arquivos correspondentes. Você também pode dividir conteúdo em [importações](#import-additional-files) para organização, embora arquivos importados ainda sejam carregados e entrem na janela de contexto no lançamento.

**Estrutura**: use cabeçalhos markdown e bullets para agrupar instruções relacionadas. Claude escaneia a estrutura da mesma forma que os leitores fazem: seções organizadas são mais fáceis de seguir do que parágrafos densos.

**Especificidade**: escreva instruções que sejam concretas o suficiente para verificar. Por exemplo:

* "Use indentação de 2 espaços" em vez de "Formate o código adequadamente"
* "Execute `npm test` antes de fazer commit" em vez de "Teste suas alterações"
* "Manipuladores de API vivem em `src/api/handlers/`" em vez de "Mantenha os arquivos organizados"

**Consistência**: se duas regras se contradizem, Claude pode escolher uma arbitrariamente. Revise seus arquivos CLAUDE.md, arquivos CLAUDE.md aninhados em subdiretórios e [`.claude/rules/`](#organize-rules-with-claude/rules/) periodicamente para remover instruções desatualizadas ou conflitantes. Em monorepos, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) para pular arquivos CLAUDE.md de outras equipes que não são relevantes para seu trabalho.

<h3 id="import-additional-files">
  Importe arquivos adicionais
</h3>

Arquivos CLAUDE.md podem importar arquivos adicionais usando a sintaxe `@path/to/import`. Arquivos importados são expandidos e carregados em contexto no lançamento junto com o CLAUDE.md que os referencia.

Caminhos relativos e absolutos são permitidos. Caminhos relativos são resolvidos em relação ao arquivo contendo a importação, não ao diretório de trabalho. Arquivos importados podem importar recursivamente outros arquivos, com uma profundidade máxima de quatro saltos.

A análise de importação ignora spans de código Markdown e blocos de código cercados. Para mencionar um caminho em seu CLAUDE.md sem importá-lo, envolva-o em backticks: escrever `` `@README` `` mantém o texto literal, enquanto `@README` fora de backticks importa o arquivo.

Para trazer um README, package.json e um guia de fluxo de trabalho, referencie-os com a sintaxe `@` em qualquer lugar do seu CLAUDE.md:

```text theme={null}
Veja @README para visão geral do projeto e @package.json para comandos npm disponíveis para este projeto.

# Instruções Adicionais
- fluxo de trabalho git @docs/git-instructions.md
```

Para preferências pessoais por projeto que não devem ser verificadas no controle de versão, crie um `CLAUDE.local.md` na raiz do projeto. Ele é carregado junto com `CLAUDE.md` e é tratado da mesma forma. Adicione `CLAUDE.local.md` ao seu `.gitignore` para que não seja confirmado; executar `/init` e escolher a opção pessoal faz isso para você.

Se você trabalha em múltiplos git worktrees do mesmo repositório, um `CLAUDE.local.md` ignorado pelo git só existe no worktree onde você o criou. Para compartilhar instruções pessoais entre worktrees, importe um arquivo do seu diretório home em vez disso:

```text theme={null}
# Preferências Individuais
- @~/.claude/my-project-instructions.md
```

<Warning>
  A primeira vez que Claude Code encontra importações externas em um projeto, mostra um diálogo de aprovação listando os arquivos. Se você recusar, as importações permanecem desabilitadas e o diálogo não aparece novamente.
</Warning>

Para uma abordagem mais estruturada para organizar instruções, veja [`.claude/rules/`](#organize-rules-with-claude/rules/).

<h3 id="agents-md">
  AGENTS.md
</h3>

Claude Code lê `CLAUDE.md`, não `AGENTS.md`. Se seu repositório já usa `AGENTS.md` para outros agentes de codificação, crie um `CLAUDE.md` que o importe para que ambas as ferramentas leiam as mesmas instruções sem duplicá-las. Você também pode adicionar instruções específicas do Claude Code abaixo da importação. Claude carrega o arquivo importado no início da sessão, depois anexa o resto:

```markdown CLAUDE.md theme={null}
@AGENTS.md

## Claude Code

Use plan mode para alterações em `src/billing/`.
```

Um symlink também funciona se você não precisar adicionar conteúdo específico do Claude Code:

```bash theme={null}
ln -s AGENTS.md CLAUDE.md
```

No Windows, criar um symlink requer privilégios de Administrador ou Modo de Desenvolvedor, então use a importação `@AGENTS.md` em vez disso.

Executar [`/init`](/docs/pt/commands) em um repositório que já tem um `AGENTS.md` o lê e incorpora as partes relevantes no `CLAUDE.md` gerado. Ele também lê outras configurações de ferramentas como `.cursorrules`, `.devin/rules/` e `.windsurfrules`.

<h3 id="how-claude-md-files-load">
  Como arquivos CLAUDE.md são carregados
</h3>

Claude Code lê arquivos CLAUDE.md caminhando para cima na árvore de diretórios a partir do seu diretório de trabalho atual, verificando cada diretório ao longo do caminho para arquivos `CLAUDE.md` e `CLAUDE.local.md`. Isso significa que se você executar Claude Code em `foo/bar/`, ele carrega instruções de `foo/bar/CLAUDE.md`, `foo/CLAUDE.md` e qualquer arquivo `CLAUDE.local.md` ao lado deles.

Todos os arquivos descobertos são concatenados em contexto em vez de se sobreporem. Dentro da árvore de diretórios, o conteúdo é ordenado da raiz do sistema de arquivos até seu diretório de trabalho. Para o exemplo `foo/bar/`, `foo/CLAUDE.md` aparece em contexto antes de `foo/bar/CLAUDE.md`, então as instruções mais próximas de onde você lançou Claude são lidas por último. Dentro de cada diretório, `CLAUDE.local.md` é anexado após `CLAUDE.md`, então suas notas pessoais são a última coisa que Claude lê naquele nível.

Claude também descobre arquivos `CLAUDE.md` e `CLAUDE.local.md` em subdiretórios sob seu diretório de trabalho atual. Em vez de carregá-los no lançamento, eles são incluídos quando Claude lê arquivos nesses subdiretórios.

Se você trabalha em um grande monorepo onde arquivos CLAUDE.md de outras equipes são capturados, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) para pular. Para o layout completo de arquivos CLAUDE.md de raiz e por diretório e regras, veja [Monorepos e repositórios grandes](/docs/pt/large-codebases).

Comentários HTML em nível de bloco (`<!-- notas do mantenedor -->`) em arquivos CLAUDE.md são removidos antes do conteúdo ser injetado no contexto de Claude. Use-os para deixar notas para mantenedores humanos sem gastar tokens de contexto neles. Comentários dentro de blocos de código são preservados. Quando você abre um arquivo CLAUDE.md diretamente com a ferramenta Read, os comentários permanecem visíveis.

<h4 id="load-from-additional-directories">
  Carregue de diretórios adicionais
</h4>

A flag `--add-dir` dá a Claude acesso a diretórios adicionais fora do seu diretório de trabalho principal. Por padrão, arquivos CLAUDE.md desses diretórios não são carregados.

Para também carregar arquivos de memória de diretórios adicionais, defina a variável de ambiente `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

Isso carrega `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` e `CLAUDE.local.md` do diretório adicional. `CLAUDE.local.md` é ignorado se você excluir `local` de [`--setting-sources`](/docs/pt/cli-reference).

<h3 id="organize-rules-with-claude/rules/">
  Organize regras com `.claude/rules/`
</h3>

Para projetos maiores, você pode organizar instruções em múltiplos arquivos usando o diretório `.claude/rules/`. Isso mantém as instruções modulares e mais fáceis para as equipes manterem. As regras também podem ser [escopadas para caminhos de arquivo específicos](#path-specific-rules), então elas só são carregadas em contexto quando Claude trabalha com arquivos correspondentes, reduzindo ruído e economizando espaço de contexto.

<Note>
  As regras são carregadas em contexto a cada sessão ou quando arquivos correspondentes são abertos. Para instruções específicas de tarefa que não precisam estar em contexto o tempo todo, use [skills](/docs/pt/skills) em vez disso, que só são carregadas quando você as invoca ou quando Claude determina que são relevantes para seu prompt.
</Note>

<h4 id="set-up-rules">
  Configure regras
</h4>

Coloque arquivos markdown no diretório `.claude/rules/` do seu projeto. Cada arquivo deve cobrir um tópico, com um nome de arquivo descritivo como `testing.md` ou `api-design.md`. Todos os arquivos `.md` são descobertos recursivamente, então você pode organizar regras em subdiretórios como `frontend/` ou `backend/`:

```text theme={null}
seu-projeto/
├── .claude/
│   ├── CLAUDE.md           # Instruções principais do projeto
│   └── rules/
│       ├── code-style.md   # Diretrizes de estilo de código
│       ├── testing.md      # Convenções de teste
│       └── security.md     # Requisitos de segurança
```

Regras sem [frontmatter `paths`](#path-specific-rules) são carregadas no lançamento com a mesma prioridade que `.claude/CLAUDE.md`.

<h4 id="path-specific-rules">
  Regras específicas de caminho
</h4>

As regras podem ser escopadas para arquivos específicos usando frontmatter YAML com o campo `paths`. Essas regras condicionais só se aplicam quando Claude está trabalhando com arquivos correspondentes aos padrões especificados.

```markdown theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Regras de Desenvolvimento de API

- Todos os endpoints de API devem incluir validação de entrada
- Use o formato de resposta de erro padrão
- Inclua comentários de documentação OpenAPI
```

Regras sem um campo `paths` são carregadas incondicionalmente e se aplicam a todos os arquivos. Regras com escopo de caminho são acionadas quando Claude lê arquivos correspondentes ao padrão, não em cada uso de ferramenta. A partir da v2.1.198, a correspondência também funciona quando Claude alcança um arquivo através de um caminho vinculado simbolicamente para o diretório do projeto, por exemplo em um checkout vinculado simbolicamente.

Use padrões glob no campo `paths` para corresponder arquivos por extensão, diretório ou qualquer combinação:

| Padrão                 | Corresponde                                        |
| ---------------------- | -------------------------------------------------- |
| `**/*.ts`              | Todos os arquivos TypeScript em qualquer diretório |
| `src/**/*`             | Todos os arquivos sob o diretório `src/`           |
| `*.md`                 | Arquivos Markdown na raiz do projeto               |
| `src/components/*.tsx` | Componentes React em um diretório específico       |

Você pode especificar múltiplos padrões e usar expansão de chaves para corresponder múltiplas extensões em um padrão:

```markdown theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

Sintaxe glob trata `[` como o início de uma expressão de colchete como `[abc]`. Um padrão com um `[` que não pode ser lido como uma expressão de colchete, como `photos [2024/**`, é inválido: ele não corresponde a nada, e os outros padrões da regra continuam funcionando. Para corresponder um `[` literal em um nome de arquivo, escape-o como `photos \[2024/**`. Antes da v2.1.207, um padrão inválido fazia a ferramenta Read falhar para cada arquivo em que a regra era avaliada, em vez de não corresponder a nada.

<h4 id="share-rules-across-projects-with-symlinks">
  Compartilhe regras entre projetos com symlinks
</h4>

O diretório `.claude/rules/` suporta symlinks, então você pode manter um conjunto compartilhado de regras e vinculá-las em múltiplos projetos. Symlinks são resolvidos e carregados normalmente, e symlinks circulares são detectados e tratados graciosamente.

Este exemplo vincula tanto um diretório compartilhado quanto um arquivo individual:

```bash theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

<h4 id="user-level-rules">
  Regras de nível de usuário
</h4>

Regras pessoais em `~/.claude/rules/` se aplicam a cada projeto na sua máquina. Use-as para preferências que não são específicas do projeto:

```text theme={null}
~/.claude/rules/
├── preferences.md    # Suas preferências pessoais de codificação
└── workflows.md      # Seus fluxos de trabalho preferidos
```

Regras de nível de usuário são carregadas antes das regras de projeto, dando às regras de projeto prioridade mais alta.

<h3 id="manage-claude-md-for-large-teams">
  Gerencie CLAUDE.md para grandes equipes
</h3>

Para organizações implantando Claude Code em equipes, você pode centralizar instruções e controlar quais arquivos CLAUDE.md são carregados.

<h4 id="deploy-organization-wide-claude-md">
  Implante CLAUDE.md em toda a organização
</h4>

As organizações podem implantar um CLAUDE.md gerenciado centralmente que se aplica a todos os usuários em uma máquina. Este arquivo não pode ser excluído por configurações individuais.

<Steps>
  <Step title="Crie o arquivo no local da política gerenciada">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux e WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Implante com seu sistema de gerenciamento de configuração">
    Use MDM, Group Policy, Ansible ou ferramentas similares para distribuir o arquivo entre máquinas de desenvolvedores. Veja [configurações gerenciadas](/docs/pt/permissions#managed-settings) para outras opções de configuração em toda a organização.
  </Step>
</Steps>

A chave `claudeMd` permite que você coloque conteúdo CLAUDE.md gerenciado diretamente dentro de `managed-settings.json` em vez de implantar um arquivo separado.

**Escopo**: cada sessão de Claude Code na máquina, em cada repositório. Para orientação específica do repositório, confirme um CLAUDE.md de projeto em vez disso.

**Precedência**: igual a um arquivo CLAUDE.md gerenciado. Carrega antes de CLAUDE.md de usuário e projeto.

**Onde é honrado**: apenas configurações gerenciadas e de política. Definir `claudeMd` em configurações de usuário, projeto ou local não tem efeito.

O exemplo abaixo adiciona instruções comportamentais diretamente em um arquivo de configurações gerenciadas:

```json theme={null}
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
```

Um CLAUDE.md gerenciado e [configurações gerenciadas](/docs/pt/settings#settings-files) servem a propósitos diferentes. Use configurações para imposição técnica e CLAUDE.md para orientação comportamental:

| Preocupação                                                       | Configure em                                                       |
| :---------------------------------------------------------------- | :----------------------------------------------------------------- |
| Bloqueie ferramentas, comandos ou caminhos de arquivo específicos | Configurações gerenciadas: `permissions.deny`                      |
| Imponha isolamento de sandbox                                     | Configurações gerenciadas: `sandbox.enabled`                       |
| Variáveis de ambiente e roteamento de provedor de API             | Configurações gerenciadas: `env`                                   |
| Método de autenticação e bloqueio de organização                  | Configurações gerenciadas: `forceLoginMethod`, `forceLoginOrgUUID` |
| Diretrizes de estilo de código e qualidade                        | CLAUDE.md gerenciado                                               |
| Lembretes de manipulação de dados e conformidade                  | CLAUDE.md gerenciado                                               |
| Instruções comportamentais para Claude                            | CLAUDE.md gerenciado                                               |

Regras de configurações são impostas pelo cliente independentemente do que Claude decide fazer. Instruções de CLAUDE.md moldam o comportamento de Claude, mas não são uma camada de imposição rígida.

<h4 id="exclude-specific-claude-md-files">
  Exclua arquivos CLAUDE.md específicos
</h4>

Em grandes monorepos, arquivos CLAUDE.md ancestrais podem conter instruções que não são relevantes para seu trabalho. A configuração `claudeMdExcludes` permite que você pule arquivos específicos por caminho ou padrão glob.

Este exemplo exclui um CLAUDE.md de nível superior e um diretório de regras de uma pasta pai. Adicione-o a `.claude/settings.local.json` para que a exclusão permaneça local à sua máquina:

```json theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Padrões são correspondidos contra caminhos de arquivo absolutos usando sintaxe glob. Você pode configurar `claudeMdExcludes` em qualquer [camada de configurações](/docs/pt/settings#settings-files): usuário, projeto, local ou política gerenciada. Arrays são mesclados entre camadas.

Arquivos CLAUDE.md de política gerenciada não podem ser excluídos. Isso garante que as instruções em toda a organização sempre se apliquem independentemente das configurações individuais.

<h2 id="auto-memory">
  Memória automática
</h2>

A memória automática permite que Claude acumule conhecimento entre sessões sem você escrever nada. Claude salva notas para si mesma enquanto trabalha: comandos de compilação, insights de depuração, notas de arquitetura, preferências de estilo de código e hábitos de fluxo de trabalho. Claude não salva algo a cada sessão. Ela decide o que vale a pena lembrar com base em se a informação seria útil em uma conversa futura.

<h3 id="enable-or-disable-auto-memory">
  Ative ou desative a memória automática
</h3>

A memória automática está ativada por padrão. Para alterná-la, abra `/memory` em uma sessão e use o toggle de memória automática, ou defina `autoMemoryEnabled` nas configurações do seu projeto:

```json theme={null}
{
  "autoMemoryEnabled": false
}
```

Para desabilitar a memória automática via variável de ambiente, defina `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

<h3 id="storage-location">
  Local de armazenamento
</h3>

Cada projeto obtém seu próprio diretório de memória em `~/.claude/projects/<project>/memory/`. O caminho `<project>` é derivado do repositório git, então todos os worktrees e subdiretórios dentro do mesmo repositório compartilham um diretório de memória automática. Fora de um repositório git, a raiz do projeto é usada em vez disso.

Para armazenar memória automática em um local diferente, defina `autoMemoryDirectory` em seu `settings.json`. Ele é lido de qualquer [escopo de configurações](/docs/pt/settings#settings-precedence): usuário, projeto, local, política, ou `--settings`.

```json theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

O valor deve ser um caminho absoluto ou começar com `~/`. Quando definido no `.claude/settings.json` ou `.claude/settings.local.json` de um projeto, o valor é respeitado apenas após você aceitar o diálogo de confiança do workspace para essa pasta, o mesmo gate que governa hooks.

O diretório contém um ponto de entrada `MEMORY.md` e arquivos de tópico opcionais:

```text theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Índice conciso, carregado em cada sessão
├── debugging.md       # Notas detalhadas sobre padrões de depuração
├── api-conventions.md # Decisões de design de API
└── ...                # Qualquer outro arquivo de tópico que Claude cria
```

`MEMORY.md` atua como um índice do diretório de memória. Claude lê e escreve arquivos neste diretório ao longo de sua sessão, usando `MEMORY.md` para acompanhar o que está armazenado onde.

A memória automática é local da máquina. Todos os worktrees e subdiretórios dentro do mesmo repositório git compartilham um diretório de memória automática. Os arquivos não são compartilhados entre máquinas ou ambientes em nuvem.

<h3 id="how-it-works">
  Como funciona
</h3>

As primeiras 200 linhas de `MEMORY.md`, ou os primeiros 25KB, o que vier primeiro, são carregados no início de cada conversa. Conteúdo além desse limite não é carregado no início da sessão. Claude mantém `MEMORY.md` conciso movendo notas detalhadas para arquivos de tópico separados.

Este limite se aplica apenas a `MEMORY.md`. Arquivos CLAUDE.md são carregados completamente independentemente do comprimento, embora arquivos mais curtos produzam melhor aderência.

Arquivos de tópico como `debugging.md` ou `patterns.md` não são carregados na inicialização. Claude os lê sob demanda usando suas ferramentas de arquivo padrão quando precisa da informação.

Claude lê e escreve arquivos de memória durante sua sessão. Quando você vê "Writing memory" ou "Recalled memory" na interface do Claude Code, Claude está ativamente atualizando ou lendo de `~/.claude/projects/<project>/memory/`.

<h3 id="audit-and-edit-your-memory">
  Audite e edite sua memória
</h3>

Arquivos de memória automática são markdown simples que você pode editar ou deletar a qualquer momento. Execute [`/memory`](#view-and-edit-with-%2Fmemory) para navegar e abrir arquivos de memória de dentro de uma sessão.

<h2 id="view-and-edit-with-/memory">
  Visualize e edite com `/memory`
</h2>

O comando `/memory` lista todos os arquivos CLAUDE.md, CLAUDE.local.md e rules carregados em sua sessão atual, permite que você alterne a memória automática ativada ou desativada, e fornece um link para abrir a pasta de memória automática. Selecione qualquer arquivo para abri-lo no seu editor.

Quando você pede a Claude para lembrar algo, como "sempre use pnpm, não npm" ou "lembre-se de que os testes de API requerem uma instância local de Redis," Claude salva em memória automática. Para adicionar instruções a CLAUDE.md em vez disso, peça a Claude diretamente, como "adicione isto a CLAUDE.md," ou edite o arquivo você mesmo via `/memory`.

<h2 id="troubleshoot-memory-issues">
  Solucione problemas de memória
</h2>

Estes são os problemas mais comuns com CLAUDE.md e memória automática, junto com passos para depurá-los.

<h3 id="claude-isn’t-following-my-claude-md">
  Claude não está seguindo meu CLAUDE.md
</h3>

O conteúdo de CLAUDE.md é entregue como uma mensagem de usuário após o prompt do sistema, não como parte do próprio prompt do sistema. Claude o lê e tenta segui-lo, mas não há garantia de conformidade estrita, especialmente para instruções vagas ou conflitantes.

Para depurar:

* Execute `/memory` para verificar se seus arquivos CLAUDE.md e CLAUDE.local.md estão sendo carregados. Se um arquivo não estiver listado, Claude não pode vê-lo.
* Verifique se o CLAUDE.md relevante está em um local que é carregado para sua sessão (veja [Escolha onde colocar arquivos CLAUDE.md](#choose-where-to-put-claude-md-files)).
* Torne as instruções mais específicas. "Use indentação de 2 espaços" funciona melhor do que "formate o código adequadamente."
* Procure por instruções conflitantes entre arquivos CLAUDE.md. Se dois arquivos dão orientação diferente para o mesmo comportamento, Claude pode escolher um arbitrariamente.

Se a instrução é algo que deve ser executado em um ponto específico, como antes de cada commit ou após cada edição de arquivo, escreva-a como um [hook](/docs/pt/hooks-guide) em vez disso. Hooks são executados como comandos shell em eventos de ciclo de vida fixos e se aplicam independentemente do que Claude decidir fazer.

Para instruções que você quer no nível do prompt do sistema, use [`--append-system-prompt`](/docs/pt/cli-reference#system-prompt-flags). Isso deve ser passado a cada invocação, então é mais adequado para scripts e automação do que para uso interativo.

<Tip>
  Use o hook [`InstructionsLoaded`](/docs/pt/hooks#instructionsloaded) para registrar exatamente quais arquivos de instrução são carregados, quando são carregados e por quê. Isso é útil para depurar regras específicas de caminho ou arquivos carregados preguiçosamente em subdiretórios.
</Tip>

<h3 id="i-don’t-know-what-auto-memory-saved">
  Não sei o que a memória automática salvou
</h3>

Execute `/memory` e selecione a pasta de memória automática para navegar o que Claude salvou. Tudo é markdown simples que você pode ler, editar ou deletar.

<h3 id="my-claude-md-is-too-large">
  Meu CLAUDE.md é muito grande
</h3>

Arquivos com mais de 200 linhas consomem mais contexto e podem reduzir a aderência. Use [regras com escopo de caminho](#path-specific-rules) para carregar instruções apenas quando Claude trabalha com arquivos correspondentes, ou reduza conteúdo que não é necessário em cada sessão. Dividir em [importações `@path`](#import-additional-files) ajuda na organização, mas não reduz contexto, já que arquivos importados são carregados no lançamento.

O checkup [`/doctor`](/docs/pt/commands#all-commands) propõe cortes para um CLAUDE.md verificado: ele corta conteúdo que Claude pode derivar da base de código, como layouts de diretório, listas de dependências e visões gerais de arquitetura, e mantém armadilhas, justificativa e convenções que diferem dos padrões de ferramentas. A verificação de corte requer Claude Code v2.1.206 ou posterior.

<h3 id="instructions-seem-lost-after-/compact">
  Instruções parecem perdidas após `/compact`
</h3>

CLAUDE.md de raiz de projeto sobrevive à compactação: após `/compact`, Claude relê do disco e reinjecta no contexto. Arquivos CLAUDE.md aninhados em subdiretórios não são reinjetados automaticamente; eles recarregam na próxima vez que Claude lê um arquivo naquele subdiretório.

Se uma instrução desapareceu após compactação, ela foi dada apenas em conversa ou vive em um CLAUDE.md aninhado que ainda não recarregou. Adicione instruções apenas de conversa a CLAUDE.md para torná-las persistir.

Importe arquivos adicionais
Arquivos CLAUDE.md podem importar arquivos adicionais usando a sintaxe @path/to/import. Arquivos importados são expandidos e carregados em contexto no lançamento junto com o CLAUDE.md que os referencia.
Caminhos relativos e absolutos são permitidos. Caminhos relativos são resolvidos em relação ao arquivo contendo a importação, não ao diretório de trabalho. Arquivos importados podem importar recursivamente outros arquivos, com uma profundidade máxima de quatro saltos.
A análise de importação ignora spans de código Markdown e blocos de código cercados. Para mencionar um caminho em seu CLAUDE.md sem importá-lo, envolva-o em backticks: escrever `@README` mantém o texto literal, enquanto @README fora de backticks importa o arquivo.
Para trazer um README, package.json e um guia de fluxo de trabalho, referencie-os com a sintaxe @ em qualquer lugar do seu CLAUDE.md:
Veja @README para visão geral do projeto e @package.json para comandos npm disponíveis para este projeto.

# Instruções Adicionais
- fluxo de trabalho git @docs/git-instructions.md
Para preferências pessoais por projeto que não devem ser verificadas no controle de versão, crie um CLAUDE.local.md na raiz do projeto. Ele é carregado junto com CLAUDE.md e é tratado da mesma forma. Adicione CLAUDE.local.md ao seu .gitignore para que não seja confirmado; executar /init e escolher a opção pessoal faz isso para você.
Se você trabalha em múltiplos git worktrees do mesmo repositório, um CLAUDE.local.md ignorado pelo git só existe no worktree onde você o criou. Para compartilhar instruções pessoais entre worktrees, importe um arquivo do seu diretório home em vez disso:
# Preferências Individuais
- @~/.claude/my-project-instructions.md
A primeira vez que Claude Code encontra importações externas em um projeto, mostra um diálogo de aprovação listando os arquivos. Se você recusar, as importações permanecem desabilitadas e o diálogo não aparece novamente.
Para uma abordagem mais estruturada para organizar instruções, veja .claude/rules/.
​
AGENTS.md
Claude Code lê CLAUDE.md, não AGENTS.md. Se seu repositório já usa AGENTS.md para outros agentes de codificação, crie um CLAUDE.md que o importe para que ambas as ferramentas leiam as mesmas instruções sem duplicá-las. Você também pode adicionar instruções específicas do Claude Code abaixo da importação. Claude carrega o arquivo importado no início da sessão, depois anexa o resto:
CLAUDE.md
@AGENTS.md

## Claude Code

Use plan mode para alterações em `src/billing/`.
Um symlink também funciona se você não precisar adicionar conteúdo específico do Claude Code:
ln -s AGENTS.md CLAUDE.md
No Windows, criar um symlink requer privilégios de Administrador ou Modo de Desenvolvedor, então use a importação @AGENTS.md em vez disso.
Executar /init em um repositório que já tem um AGENTS.md o lê e incorpora as partes relevantes no CLAUDE.md gerado. Ele também lê outras configurações de ferramentas como .cursorrules, .devin/rules/ e .windsurfrules.
​
Como arquivos CLAUDE.md são carregados
Claude Code lê arquivos CLAUDE.md caminhando para cima na árvore de diretórios a partir do seu diretório de trabalho atual, verificando cada diretório ao longo do caminho para arquivos CLAUDE.md e CLAUDE.local.md. Isso significa que se você executar Claude Code em foo/bar/, ele carrega instruções de foo/bar/CLAUDE.md, foo/CLAUDE.md e qualquer arquivo CLAUDE.local.md ao lado deles.
Todos os arquivos descobertos são concatenados em contexto em vez de se sobreporem. Dentro da árvore de diretórios, o conteúdo é ordenado da raiz do sistema de arquivos até seu diretório de trabalho. Para o exemplo foo/bar/, foo/CLAUDE.md aparece em contexto antes de foo/bar/CLAUDE.md, então as instruções mais próximas de onde você lançou Claude são lidas por último. Dentro de cada diretório, CLAUDE.local.md é anexado após CLAUDE.md, então suas notas pessoais são a última coisa que Claude lê naquele nível.
Claude também descobre arquivos CLAUDE.md e CLAUDE.local.md em subdiretórios sob seu diretório de trabalho atual. Em vez de carregá-los no lançamento, eles são incluídos quando Claude lê arquivos nesses subdiretórios.
Se você trabalha em um grande monorepo onde arquivos CLAUDE.md de outras equipes são capturados, use claudeMdExcludes para pular. Para o layout completo de arquivos CLAUDE.md de raiz e por diretório e regras, veja Monorepos e repositórios grandes.
Comentários HTML em nível de bloco (<!-- notas do mantenedor -->) em arquivos CLAUDE.md são removidos antes do conteúdo ser injetado no contexto de Claude. Use-os para deixar notas para mantenedores humanos sem gastar tokens de contexto neles. Comentários dentro de blocos de código são preservados. Quando você abre um arquivo CLAUDE.md diretamente com a ferramenta Read, os comentários permanecem visíveis.
​
Carregue de diretórios adicionais
A flag --add-dir dá a Claude acesso a diretórios adicionais fora do seu diretório de trabalho principal. Por padrão, arquivos CLAUDE.md desses diretórios não são carregados.
Para também carregar arquivos de memória de diretórios adicionais, defina a variável de ambiente CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD:
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
Isso carrega CLAUDE.md, .claude/CLAUDE.md, .claude/rules/*.md e CLAUDE.local.md do diretório adicional. CLAUDE.local.md é ignorado se você excluir local de --setting-sources.
​
Organize regras com .claude/rules/
Para projetos maiores, você pode organizar instruções em múltiplos arquivos usando o diretório .claude/rules/. Isso mantém as instruções modulares e mais fáceis para as equipes manterem. As regras também podem ser escopadas para caminhos de arquivo específicos, então elas só são carregadas em contexto quando Claude trabalha com arquivos correspondentes, reduzindo ruído e economizando espaço de contexto.
As regras são carregadas em contexto a cada sessão ou quando arquivos correspondentes são abertos. Para instruções específicas de tarefa que não precisam estar em contexto o tempo todo, use skills em vez disso, que só são carregadas quando você as invoca ou quando Claude determina que são relevantes para seu prompt.
​
Configure regras
Coloque arquivos markdown no diretório .claude/rules/ do seu projeto. Cada arquivo deve cobrir um tópico, com um nome de arquivo descritivo como testing.md ou api-design.md. Todos os arquivos .md são descobertos recursivamente, então você pode organizar regras em subdiretórios como frontend/ ou backend/:
seu-projeto/
├── .claude/
│   ├── CLAUDE.md           # Instruções principais do projeto
│   └── rules/
│       ├── code-style.md   # Diretrizes de estilo de código
│       ├── testing.md      # Convenções de teste
│       └── security.md     # Requisitos de segurança
Regras sem frontmatter paths são carregadas no lançamento com a mesma prioridade que .claude/CLAUDE.md.
​
Regras específicas de caminho
As regras podem ser escopadas para arquivos específicos usando frontmatter YAML com o campo paths. Essas regras condicionais só se aplicam quando Claude está trabalhando com arquivos correspondentes aos padrões especificados.
---
paths:
  - "src/api/**/*.ts"
---

# Regras de Desenvolvimento de API

- Todos os endpoints de API devem incluir validação de entrada
- Use o formato de resposta de erro padrão
- Inclua comentários de documentação OpenAPI
Regras sem um campo paths são carregadas incondicionalmente e se aplicam a todos os arquivos. Regras com escopo de caminho são acionadas quando Claude lê arquivos correspondentes ao padrão, não em cada uso de ferramenta. A partir da v2.1.198, a correspondência também funciona quando Claude alcança um arquivo através de um caminho vinculado simbolicamente para o diretório do projeto, por exemplo em um checkout vinculado simbolicamente.
Use padrões glob no campo paths para corresponder arquivos por extensão, diretório ou qualquer combinação:
Padrão	Corresponde
**/*.ts	Todos os arquivos TypeScript em qualquer diretório
src/**/*	Todos os arquivos sob o diretório src/
*.md	Arquivos Markdown na raiz do projeto
src/components/*.tsx	Componentes React em um diretório específico
Você pode especificar múltiplos padrões e usar expansão de chaves para corresponder múltiplas extensões em um padrão:
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
Sintaxe glob trata [ como o início de uma expressão de colchete como [abc]. Um padrão com um [ que não pode ser lido como uma expressão de colchete, como photos [2024/**, é inválido: ele não corresponde a nada, e os outros padrões da regra continuam funcionando. Para corresponder um [ literal em um nome de arquivo, escape-o como photos \[2024/**. Antes da v2.1.207, um padrão inválido fazia a ferramenta Read falhar para cada arquivo em que a regra era avaliada, em vez de não corresponder a nada.
​
Compartilhe regras entre projetos com symlinks
O diretório .claude/rules/ suporta symlinks, então você pode manter um conjunto compartilhado de regras e vinculá-las em múltiplos projetos. Symlinks são resolvidos e carregados normalmente, e symlinks circulares são detectados e tratados graciosamente.
Este exemplo vincula tanto um diretório compartilhado quanto um arquivo individual:
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
​
Regras de nível de usuário
Regras pessoais em ~/.claude/rules/ se aplicam a cada projeto na sua máquina. Use-as para preferências que não são específicas do projeto:
~/.claude/rules/
├── preferences.md    # Suas preferências pessoais de codificação
└── workflows.md      # Seus fluxos de trabalho preferidos
Regras de nível de usuário são carregadas antes das regras de projeto, dando às regras de projeto prioridade mais alta.
​
Gerencie CLAUDE.md para grandes equipes
Para organizações implantando Claude Code em equipes, você pode centralizar instruções e controlar quais arquivos CLAUDE.md são carregados.
​
Implante CLAUDE.md em toda a organização
As organizações podem implantar um CLAUDE.md gerenciado centralmente que se aplica a todos os usuários em uma máquina. Este arquivo não pode ser excluído por configurações individuais.
1
Crie o arquivo no local da política gerenciada

macOS: /Library/Application Support/ClaudeCode/CLAUDE.md
Linux e WSL: /etc/claude-code/CLAUDE.md
Windows: C:\Program Files\ClaudeCode\CLAUDE.md
2
Implante com seu sistema de gerenciamento de configuração

Use MDM, Group Policy, Ansible ou ferramentas similares para distribuir o arquivo entre máquinas de desenvolvedores. Veja configurações gerenciadas para outras opções de configuração em toda a organização.
A chave claudeMd permite que você coloque conteúdo CLAUDE.md gerenciado diretamente dentro de managed-settings.json em vez de implantar um arquivo separado.
Escopo: cada sessão de Claude Code na máquina, em cada repositório. Para orientação específica do repositório, confirme um CLAUDE.md de projeto em vez disso.
Precedência: igual a um arquivo CLAUDE.md gerenciado. Carrega antes de CLAUDE.md de usuário e projeto.
Onde é honrado: apenas configurações gerenciadas e de política. Definir claudeMd em configurações de usuário, projeto ou local não tem efeito.
O exemplo abaixo adiciona instruções comportamentais diretamente em um arquivo de configurações gerenciadas:
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
Um CLAUDE.md gerenciado e configurações gerenciadas servem a propósitos diferentes. Use configurações para imposição técnica e CLAUDE.md para orientação comportamental:
Preocupação	Configure em
Bloqueie ferramentas, comandos ou caminhos de arquivo específicos	Configurações gerenciadas: permissions.deny
Imponha isolamento de sandbox	Configurações gerenciadas: sandbox.enabled
Variáveis de ambiente e roteamento de provedor de API	Configurações gerenciadas: env
Método de autenticação e bloqueio de organização	Configurações gerenciadas: forceLoginMethod, forceLoginOrgUUID
Diretrizes de estilo de código e qualidade	CLAUDE.md gerenciado
Lembretes de manipulação de dados e conformidade	CLAUDE.md gerenciado
Instruções comportamentais para Claude	CLAUDE.md gerenciado
Regras de configurações são impostas pelo cliente independentemente do que Claude decide fazer. Instruções de CLAUDE.md moldam o comportamento de Claude, mas não são uma camada de imposição rígida.
​
Exclua arquivos CLAUDE.md específicos
Em grandes monorepos, arquivos CLAUDE.md ancestrais podem conter instruções que não são relevantes para seu trabalho. A configuração claudeMdExcludes permite que você pule arquivos específicos por caminho ou padrão glob.
Este exemplo exclui um CLAUDE.md de nível superior e um diretório de regras de uma pasta pai. Adicione-o a .claude/settings.local.json para que a exclusão permaneça local à sua máquina:
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
Padrões são correspondidos contra caminhos de arquivo absolutos usando sintaxe glob. Você pode configurar claudeMdExcludes em qualquer camada de configurações: usuário, projeto, local ou política gerenciada. Arrays são mesclados entre camadas.
Arquivos CLAUDE.md de política gerenciada não podem ser excluídos. Isso garante que as instruções em toda a organização sempre se apliquem independentemente das configurações individuais.
​
Memória automática
A memória automática permite que Claude acumule conhecimento entre sessões sem você escrever nada. Claude salva notas para si mesma enquanto trabalha: comandos de compilação, insights de depuração, notas de arquitetura, preferências de estilo de código e hábitos de fluxo de trabalho. Claude não salva algo a cada sessão. Ela decide o que vale a pena lembrar com base em se a informação seria útil em uma conversa futura.
​
Ative ou desative a memória automática
A memória automática está ativada por padrão. Para alterná-la, abra /memory em uma sessão e use o toggle de memória automática, ou defina autoMemoryEnabled nas configurações do seu projeto:
{
  "autoMemoryEnabled": false
}
Para desabilitar a memória automática via variável de ambiente, defina CLAUDE_CODE_DISABLE_AUTO_MEMORY=1.
​
Local de armazenamento
Cada projeto obtém seu próprio diretório de memória em ~/.claude/projects/<project>/memory/. O caminho <project> é derivado do repositório git, então todos os worktrees e subdiretórios dentro do mesmo repositório compartilham um diretório de memória automática. Fora de um repositório git, a raiz do projeto é usada em vez disso.
Para armazenar memória automática em um local diferente, defina autoMemoryDirectory em seu settings.json. Ele é lido de qualquer escopo de configurações: usuário, projeto, local, política, ou --settings.
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
O valor deve ser um caminho absoluto ou começar com ~/. Quando definido no .claude/settings.json ou .claude/settings.local.json de um projeto, o valor é respeitado apenas após você aceitar o diálogo de confiança do workspace para essa pasta, o mesmo gate que governa hooks.
O diretório contém um ponto de entrada MEMORY.md e arquivos de tópico opcionais:
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Índice conciso, carregado em cada sessão
├── debugging.md       # Notas detalhadas sobre padrões de depuração
├── api-conventions.md # Decisões de design de API
└── ...                # Qualquer outro arquivo de tópico que Claude cria
MEMORY.md atua como um índice do diretório de memória. Claude lê e escreve arquivos neste diretório ao longo de sua sessão, usando MEMORY.md para acompanhar o que está armazenado onde.
A memória automática é local da máquina. Todos os worktrees e subdiretórios dentro do mesmo repositório git compartilham um diretório de memória automática. Os arquivos não são compartilhados entre máquinas ou ambientes em nuvem.
​
Como funciona
As primeiras 200 linhas de MEMORY.md, ou os primeiros 25KB, o que vier primeiro, são carregados no início de cada conversa. Conteúdo além desse limite não é carregado no início da sessão. Claude mantém MEMORY.md conciso movendo notas detalhadas para arquivos de tópico separados.
Este limite se aplica apenas a MEMORY.md. Arquivos CLAUDE.md são carregados completamente independentemente do comprimento, embora arquivos mais curtos produzam melhor aderência.
Arquivos de tópico como debugging.md ou patterns.md não são carregados na inicialização. Claude os lê sob demanda usando suas ferramentas de arquivo padrão quando precisa da informação.
Claude lê e escreve arquivos de memória durante sua sessão. Quando você vê “Writing memory” ou “Recalled memory” na interface do Claude Code, Claude está ativamente atualizando ou lendo de ~/.claude/projects/<project>/memory/.
​
Audite e edite sua memória
Arquivos de memória automática são markdown simples que você pode editar ou deletar a qualquer momento. Execute /memory para navegar e abrir arquivos de memória de dentro de uma sessão.
​
Visualize e edite com /memory
O comando /memory lista todos os arquivos CLAUDE.md, CLAUDE.local.md e rules carregados em sua sessão atual, permite que você alterne a memória automática ativada ou desativada, e fornece um link para abrir a pasta de memória automática. Selecione qualquer arquivo para abri-lo no seu editor.
Quando você pede a Claude para lembrar algo, como “sempre use pnpm, não npm” ou “lembre-se de que os testes de API requerem uma instância local de Redis,” Claude salva em memória automática. Para adicionar instruções a CLAUDE.md em vez disso, peça a Claude diretamente, como “adicione isto a CLAUDE.md,” ou edite o arquivo você mesmo via /memory.
​
Solucione problemas de memória
Estes são os problemas mais comuns com CLAUDE.md e memória automática, junto com passos para depurá-los.
​
Claude não está seguindo meu CLAUDE.md
O conteúdo de CLAUDE.md é entregue como uma mensagem de usuário após o prompt do sistema, não como parte do próprio prompt do sistema. Claude o lê e tenta segui-lo, mas não há garantia de conformidade estrita, especialmente para instruções vagas ou conflitantes.
Para depurar:
Execute /memory para verificar se seus arquivos CLAUDE.md e CLAUDE.local.md estão sendo carregados. Se um arquivo não estiver listado, Claude não pode vê-lo.
Verifique se o CLAUDE.md relevante está em um local que é carregado para sua sessão (veja Escolha onde colocar arquivos CLAUDE.md).
Torne as instruções mais específicas. “Use indentação de 2 espaços” funciona melhor do que “formate o código adequadamente.”
Procure por instruções conflitantes entre arquivos CLAUDE.md. Se dois arquivos dão orientação diferente para o mesmo comportamento, Claude pode escolher um arbitrariamente.
Se a instrução é algo que deve ser executado em um ponto específico, como antes de cada commit ou após cada edição de arquivo, escreva-a como um hook em vez disso. Hooks são executados como comandos shell em eventos de ciclo de vida fixos e se aplicam independentemente do que Claude decidir fazer.
Para instruções que você quer no nível do prompt do sistema, use --append-system-prompt. Isso deve ser passado a cada invocação, então é mais adequado para scripts e automação do que para uso interativo.
Use o hook InstructionsLoaded para registrar exatamente quais arquivos de instrução são carregados, quando são carregados e por quê. Isso é útil para depurar regras específicas de caminho ou arquivos carregados preguiçosamente em subdiretórios.
​
Não sei o que a memória automática salvou
Execute /memory e selecione a pasta de memória automática para navegar o que Claude salvou. Tudo é markdown simples que você pode ler, editar ou deletar.
​
Meu CLAUDE.md é muito grande
Arquivos com mais de 200 linhas consomem mais contexto e podem reduzir a aderência. Use regras com escopo de caminho para carregar instruções apenas quando Claude trabalha com arquivos correspondentes, ou reduza conteúdo que não é necessário em cada sessão. Dividir em importações @path ajuda na organização, mas não reduz contexto, já que arquivos importados são carregados no lançamento.
O checkup /doctor propõe cortes para um CLAUDE.md verificado: ele corta conteúdo que Claude pode derivar da base de código, como layouts de diretório, listas de dependências e visões gerais de arquitetura, e mantém armadilhas, justificativa e convenções que diferem dos padrões de ferramentas. A verificação de corte requer Claude Code v2.1.206 ou posterior.
​
Instruções parecem perdidas após /compact
CLAUDE.md de raiz de projeto sobrevive à compactação: após /compact, Claude relê do disco e reinjecta no contexto. Arquivos CLAUDE.md aninhados em subdiretórios não são reinjetados automaticamente; eles recarregam na próxima vez que Claude lê um arquivo naquele subdiretório.
Se uma instrução desapareceu após compactação, ela foi dada apenas em conversa ou vive em um CLAUDE.md aninhado que ainda não recarregou. Adicione instruções apenas de conversa a CLAUDE.md para torná-las persistir. Veja O que sobrevive à compactação para o detalhamento completo.

Precedência de configurações
Configurações se aplicam em ordem de precedência. De mais alta para mais baixa:
Configurações gerenciadas (gerenciadas pelo servidor, políticas de nível MDM/SO, ou configurações gerenciadas)
Políticas implantadas por TI através de entrega de servidor, perfis de configuração MDM, políticas de registro, ou arquivos de configurações gerenciadas
Não podem ser substituídas por qualquer outro nível, incluindo argumentos de linha de comando
Dentro do nível gerenciado, apenas uma fonte é usada e as outras são ignoradas em vez de mescladas. Precedência, mais alta primeiro:
Saída policyHelper: quando configurada, esta é a única fonte gerenciada usada
Remota (configurações gerenciadas pelo servidor do claude.ai ou gateway de aplicativos Claude-entregues)
Políticas de nível MDM/SO
Baseada em arquivo (managed-settings.d/*.json e managed-settings.json, mescladas juntas)
Registro HKCU (apenas Windows)
Algumas chaves são exceções, honradas quando qualquer fonte gerenciada controlada por administrador as define em vez de apenas a fonte vencedora. A fonte de registro HKCU gravável pelo usuário é excluída. As chaves de exceção são:
as chaves de bloqueio de sandbox sandbox.network.allowManagedDomainsOnly e sandbox.filesystem.allowManagedReadPathsOnly, com suas listas de permissões associadas
allowAllClaudeAiMcps
os caminhos binários de sandbox sandbox.bwrapPath e sandbox.socatPath
forceRemoteSettingsRefresh
Hosts de incorporação como Claude Desktop podem fornecer política via opção SDK managedSettings. Por padrão isto é ignorado quando qualquer fonte gerenciada controlada por administrador está presente: configurações gerenciadas pelo servidor, uma política MDM ou SO, ou um arquivo de configurações gerenciadas. O fallback de registro HKCU gravável pelo usuário não conta como uma fonte gerenciada controlada por administrador. Administradores podem optar por definir parentSettingsBehavior como "merge". Os valores do incorporador são filtrados para que possam apertar a política gerenciada mas não afrouxá-la.
Argumentos de linha de comando
Substituições temporárias para uma sessão específica. JSON passado via --settings <file-or-json> se mescla com configurações baseadas em arquivo usando as mesmas regras que as outras camadas: uma chave definida aqui substitui a mesma chave em configurações local, projeto, ou usuário, e omitir uma chave deixa o valor da camada inferior no lugar
Configurações de projeto local (.claude/settings.local.json)
Configurações pessoais específicas do projeto
Configurações de projeto compartilhadas (.claude/settings.json)
Configurações de projeto compartilhadas pela equipe no controle de origem
Configurações de usuário (~/.claude/settings.json)
Configurações globais pessoais
Esta hierarquia garante que políticas organizacionais sejam sempre aplicadas enquanto ainda permite que equipes e indivíduos personalizem sua experiência. A mesma precedência se aplica se você executar Claude Code a partir da CLI, da extensão VS Code, ou de um IDE JetBrains.
Por exemplo, se suas configurações de usuário definem permissions.defaultMode como acceptEdits e as configurações compartilhadas de um projeto definem como default, o valor do projeto se aplica. O exemplo abaixo cobre como configurações com valor de array como regras de permissão se combinam em vez disso.
Configurações de array se mesclam entre escopos. Quando a mesma configuração com valor de array (como sandbox.filesystem.allowWrite ou permissions.allow) aparece em múltiplos escopos, os arrays são concatenados e desduplicados, não substituídos. Isto significa que escopos de prioridade mais baixa podem adicionar entradas sem substituir aquelas definidas por escopos de prioridade mais alta, e vice-versa. Por exemplo, se configurações gerenciadas definem allowWrite como ["/opt/company-tools"] e um usuário adiciona ["~/.kube"], ambos os caminhos são incluídos na configuração final.
Duas configurações de array não se mesclam desta forma:
fallbackModel é uma cadeia ordenada onde a posição carrega significado: o arquivo de precedência mais alta que a define fornece o valor inteiro.
availableModels: quando a fonte gerenciada de precedência mais alta a define, essa lista se aplica como está e entradas de usuário, projeto e local não podem estendê-la. Entre escopos não gerenciados os arrays se mesclam como usual. Veja Comportamento de mesclagem.
​
Verificar configurações ativas
Execute /status dentro do Claude Code para ver quais fontes de configuração estão ativas. Dentro do menu, a aba Status inclui uma linha Setting sources que lista cada camada que Claude Code carregou para a sessão atual, como User settings ou Project local settings. Quando configurações gerenciadas estão em efeito, a entrada mostra o canal de entrega entre parênteses, por exemplo Enterprise managed settings (remote), (plist), (HKLM), (HKCU), ou (file). O canal remote cobre configurações gerenciadas pelo servidor do claude.ai e políticas gateway de aplicativos Claude-entregues. Uma camada aparece na lista apenas quando essa fonte é carregada com pelo menos uma chave, então uma lista vazia significa que nenhuma fonte de configuração foi encontrada.
A linha Setting sources confirma quais fontes estão sendo lidas. Ela não mostra qual camada forneceu cada chave individual. A aba Config no mesmo diálogo é um editor para um conjunto fixo de toggles como tema e saída verbose, não uma visualização do conteúdo do seu settings.json.
Se um arquivo de configuração contém erros, como JSON inválido ou um valor que falha na validação, /status lista os arquivos afetados. Execute claude doctor para ver os detalhes de cada erro.
​
Pontos-chave sobre o sistema de configuração
Arquivos de memória (CLAUDE.md): Contêm instruções e contexto que Claude carrega na inicialização
Arquivos de configuração (JSON): Configurar permissões, variáveis de ambiente, e comportamento de ferramenta
Skills: Prompts personalizados que podem ser invocados com /skill-name ou carregados pelo Claude automaticamente
MCP servers: Estender Claude Code com ferramentas e integrações adicionais
Precedência: Configurações de nível mais alto (Managed) substituem as de nível mais baixo (User/Project)
Herança: Configurações são mescladas entre escopos; valores escalares de escopos de prioridade mais alta substituem, e arrays se concatenam, com duas exceções descritas na Nota de mesclagem de array
​
Prompt do sistema
O prompt do sistema interno do Claude Code não é publicado. Para adicionar instruções personalizadas, use arquivos CLAUDE.md ou a flag --append-system-prompt.
​
Excluindo arquivos sensíveis
Para impedir que Claude Code acesse arquivos contendo informações sensíveis como chaves de API, segredos, e arquivos de ambiente, use a configuração permissions.deny no seu arquivo .claude/settings.json:
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
Isto substitui a configuração descontinuada ignorePatterns. Arquivos correspondentes a estes padrões são excluídos da descoberta de arquivo e resultados de busca, e operações de leitura nestes arquivos são negadas.
​
Configuração de subagent
O Claude Code suporta subagents de IA personalizados que podem ser configurados em níveis de usuário e projeto. Estes subagents são armazenados como arquivos Markdown com frontmatter YAML:
Subagents de usuário: ~/.claude/agents/, disponíveis em todos os seus projetos
Subagents de projeto: .claude/agents/, específicos ao seu projeto e compartilháveis com sua equipe
Arquivos de subagent definem assistentes de IA especializados com prompts personalizados e permissões de ferramenta. Saiba mais sobre criação e uso de subagents na documentação de subagents.
​
Configuração de plugin
Claude Code suporta um sistema de plugin que permite estender funcionalidade com skills, agents, hooks, e MCP servers. Plugins são distribuídos através de marketplaces e podem ser configurados em níveis de usuário e repositório.
​
Configurações de plugin
Configurações relacionadas a plugin em settings.json:
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  }
}
​
enabledPlugins
Controla quais plugins estão habilitados. Formato: "plugin-name@marketplace-name": true/false. Um plugin sem entrada em nenhum escopo volta ao seu valor defaultEnabled.
Escopos:
Configurações de usuário (~/.claude/settings.json): Preferências pessoais de plugin
Configurações de projeto (.claude/settings.json): Plugins específicos do projeto compartilhados com equipe
Configurações locais (.claude/settings.local.json): Substituições por máquina, gitignored quando Claude Code as cria
Configurações gerenciadas (managed-settings.json): Substituições de política em toda a organização que bloqueiam instalação em todos os escopos e ocultam o plugin do marketplace
As configurações de projeto têm precedência sobre as configurações de usuário, portanto, definir um plugin como false em ~/.claude/settings.json não desabilita um plugin que o .claude/settings.json do projeto habilita. Para optar por não usar um plugin habilitado pelo projeto em sua máquina, defina-o como false em .claude/settings.local.json em vez disso.
Plugins forçadamente habilitados por configurações gerenciadas não podem ser desabilitados desta forma, pois as configurações gerenciadas substituem as configurações locais.
Habilitar um plugin de uma fonte externa como um repositório GitHub ou pacote npm em um .claude/settings.json de projeto não o instala para outras pessoas. A partir de Claude Code v2.1.195, cada caminho que carrega plugins pede a cada usuário para instalar e confiar no plugin antes de executá-lo.
Exemplo:
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
​
pluginConfigs
Armazena os valores de opção não sensíveis que o prompt userConfig de um plugin coleta, indexados por ID de plugin. Claude Code escreve esta chave em configurações de usuário quando você preenche o diálogo de configuração do plugin, portanto você não precisa editá-la manualmente. Opções sensíveis são armazenadas no Keychain do macOS em vez disso, ou em ~/.claude/.credentials.json em plataformas sem um keychain suportado.
Este exemplo armazena uma opção para um plugin instalado do marketplace acme-tools:
{
  "pluginConfigs": {
    "deployer@acme-tools": {
      "options": {
        "api_endpoint": "https://api.example.com"
      }
    }
  }
}
pluginConfigs é lido de configurações de usuário, a flag --settings, e configurações gerenciadas apenas. Entradas em um .claude/settings.json de projeto ou .claude/settings.local.json são ignoradas, porque estes valores são substituídos em hook de plugin, MCP, e configurações LSP, e um repositório clonado não deve ser capaz de fornecê-los. Antes de v2.1.207, configurações de projeto e local também eram lidas.
​
extraKnownMarketplaces
Define marketplaces adicionais que devem ser disponibilizados para o repositório. Tipicamente usado em configurações em nível de repositório para garantir que membros da equipe tenham acesso a fontes de plugin necessárias.
Quando um repositório inclui extraKnownMarketplaces:
Membros da equipe são solicitados a instalar o marketplace quando confiam na pasta
Membros da equipe são então solicitados a instalar plugins daquele marketplace
Usuários podem pular marketplaces ou plugins indesejados (armazenados em configurações de usuário)
Instalação respeita limites de confiança e requer consentimento explícito
Exemplo:
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
Tipos de fonte de marketplace:
github: Repositório GitHub (usa repo)
git: Qualquer URL git (usa url)
directory: Caminho do sistema de arquivos local (usa path, apenas para desenvolvimento)
hostPattern: Padrão regex para corresponder hosts de marketplace (usa hostPattern)
settings: marketplace inline declarado diretamente em settings.json sem um repositório hospedado separado (usa name e plugins)
O tipo de fonte git funciona com qualquer serviço de hospedagem git, incluindo GitLab auto-hospedado e Bitbucket. Claude Code clona o repositório com a mesma autenticação que git clone usaria naquela máquina: assistentes de credencial configurados ou chaves SSH. Um token de provedor como GITHUB_TOKEN tem efeito apenas através de um assistente de credencial que o lê. Veja Repositórios privados para detalhes de configuração.
Para fontes github e git, defina "skipLfs": true dentro do objeto source (junto com repo ou url) para pular downloads de Git LFS quando Claude Code clona ou atualiza o repositório de marketplace. Arquivos de ponteiro LFS permanecem como ponteiros em vez de baixar seu conteúdo. Use isto quando o repositório contém objetos LFS grandes não relacionados ao conteúdo de plugin. Requer Claude Code v2.1.153 ou posterior.
Cada entrada de marketplace também aceita um Boolean autoUpdate opcional. Defina "autoUpdate": true junto com source para fazer Claude Code atualizar aquele marketplace e atualizar seus plugins instalados em segundo plano após a inicialização. Quando omitido, marketplaces oficiais da Anthropic padrão para true e todos os outros marketplaces padrão para false. Veja Configurar auto-atualizações.
Use source: 'settings' para declarar um pequeno conjunto de plugins inline sem configurar um repositório de marketplace hospedado. Plugins listados aqui devem referenciar fontes externas como GitHub ou npm. Você ainda precisa habilitar cada plugin separadamente em enabledPlugins.
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
​
strictKnownMarketplaces
Apenas configurações gerenciadas: Controla quais marketplaces de plugin os usuários podem adicionar e instalar plugins. Esta configuração pode ser configurada apenas em configurações gerenciadas e fornece aos administradores controle rigoroso sobre fontes de marketplace.
Localizações de arquivo de configurações gerenciadas:
macOS: /Library/Application Support/ClaudeCode/managed-settings.json
Linux e WSL: /etc/claude-code/managed-settings.json
Windows: C:\Program Files\ClaudeCode\managed-settings.json
Características principais:
Apenas disponível em configurações gerenciadas (managed-settings.json)
Não pode ser substituída por configurações de usuário ou projeto (precedência mais alta)
Aplicada antes de operações de rede e sistema de arquivos, portanto fontes bloqueadas nunca executam
Usa correspondência exata para especificações de fonte (incluindo ref, path para fontes git), exceto hostPattern e pathPattern, que usam correspondência regex
Comportamento de lista de permissões:
undefined (padrão): sem restrições, portanto usuários podem adicionar qualquer marketplace
Array vazio []: bloqueio completo, portanto usuários não podem adicionar novos marketplaces
Lista de fontes: usuários podem apenas adicionar marketplaces que correspondem exatamente
Todos os tipos de fonte suportados:
A lista de permissões suporta múltiplos tipos de fonte de marketplace. A maioria das fontes usa correspondência exata, enquanto hostPattern e pathPattern usam correspondência regex contra o host do marketplace e caminho do sistema de arquivos respectivamente.
Repositórios GitHub:
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
Campos: repo (obrigatório), ref (opcional: branch ou tag), path (opcional: subdiretório)
Repositórios Git:
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
Campos: url (obrigatório), ref (opcional: branch ou tag), path (opcional: subdiretório)
Marketplaces baseados em URL:
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
Campos: url (obrigatório), headers (opcional: cabeçalhos HTTP para acesso autenticado)
Marketplaces baseados em URL apenas baixam o arquivo marketplace.json. Eles não baixam arquivos de plugin do servidor. Plugins em marketplaces baseados em URL devem usar fontes externas (URLs GitHub, npm, ou git) em vez de caminhos relativos. Para plugins com caminhos relativos, use um marketplace baseado em Git em vez disso. Veja Troubleshooting para detalhes.
Pacotes NPM:
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
Campos: package (obrigatório, suporta pacotes com escopo)
Caminhos de arquivo:
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
Campos: path (obrigatório: caminho absoluto para arquivo marketplace.json)
Caminhos de diretório:
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
Campos: path (obrigatório: caminho absoluto para diretório contendo .claude-plugin/marketplace.json)
Correspondência de padrão de host:
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
Campos: hostPattern (obrigatório: padrão regex para corresponder contra o host do marketplace)
Use correspondência de padrão de host quando você deseja permitir todos os marketplaces de um host específico sem enumerar cada repositório individualmente. Isto é útil para organizações com GitHub Enterprise interno ou servidores GitLab onde desenvolvedores criam seus próprios marketplaces.
Extração de host por tipo de fonte:
github: sempre corresponde contra github.com
git: extrai nome de host da URL (suporta formatos HTTPS e SSH)
url: extrai nome de host da URL
npm, file, directory: não suportado para correspondência de padrão de host
Correspondência de padrão de caminho:
{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }
{ "source": "pathPattern", "pathPattern": ".*" }
Campos: pathPattern (obrigatório: padrão regex correspondido contra o campo path de fontes file e directory)
Use correspondência de padrão de caminho para permitir marketplaces baseados em sistema de arquivos junto com restrições hostPattern para fontes de rede. Defina ".*" para permitir todos os caminhos locais, ou um padrão mais estreito para restringir a diretórios específicos.
Exemplos de configuração:
Exemplo: permitir apenas marketplaces específicos:
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
Exemplo: desabilitar todas as adições de marketplace:
{
  "strictKnownMarketplaces": []
}
Exemplo: permitir todos os marketplaces de um servidor git interno:
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
Requisitos de correspondência exata:
Fontes de marketplace devem corresponder exatamente para que a adição de um usuário seja permitida. Para fontes baseadas em git (github e git), isto inclui todos os campos opcionais:
O repo ou url deve corresponder exatamente
O campo ref deve corresponder exatamente (ou ambos serem indefinidos)
O campo path deve corresponder exatamente (ou ambos serem indefinidos)
Exemplos de fontes que não correspondem:
// Estas são DIFERENTES fontes:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Estas também são DIFERENTES:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
Comparação com extraKnownMarketplaces:
Aspecto	strictKnownMarketplaces	extraKnownMarketplaces
Propósito	Aplicação de política organizacional	Conveniência da equipe
Arquivo de configuração	Apenas managed-settings.json	Qualquer arquivo de configuração
Comportamento	Bloqueia adições não permitidas	Auto-instala marketplaces faltantes
Quando aplicado	Antes de operações de rede/sistema de arquivos	Após prompt de confiança do usuário
Pode ser substituído	Não (precedência mais alta)	Sim (por configurações de precedência mais alta)
Formato de fonte	Objeto de fonte direto	Marketplace nomeado com fonte aninhada
Caso de uso	Conformidade, restrições de segurança	Onboarding, padronização
Diferença de formato:
strictKnownMarketplaces usa objetos de fonte diretos:
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
extraKnownMarketplaces requer marketplaces nomeados:
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
Usando ambos juntos:
strictKnownMarketplaces é um portão de política: controla o que os usuários podem adicionar mas não registra nenhum marketplace. Para restringir e pré-registrar um marketplace para todos os usuários, defina ambos em managed-settings.json:
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
Com apenas strictKnownMarketplaces definido, usuários ainda podem adicionar o marketplace permitido manualmente via /plugin marketplace add, mas não está disponível automaticamente.
Notas importantes:
Restrições são verificadas antes de qualquer solicitação de rede ou operação de sistema de arquivos
Quando bloqueado, usuários veem mensagens de erro claras indicando que a fonte é bloqueada por política gerenciada
A restrição é aplicada em adição de marketplace e em instalação, atualização, atualização e auto-atualização de plugin. Um marketplace adicionado antes da política ser definida não pode ser usado para instalar ou atualizar plugins uma vez que sua fonte não corresponde mais à lista de permissões
Configurações gerenciadas têm a precedência mais alta e não podem ser substituídas
Veja Restrições de marketplace gerenciado para documentação voltada para o usuário.
​
strictPluginOnlyCustomization
Apenas configurações gerenciadas: bloqueia skills, agents, hooks, e MCP servers de fontes de usuário e projeto, para que possam vir apenas de plugins ou configurações gerenciadas. Combine com strictKnownMarketplaces para controlar a cadeia de suprimento de personalização completa: a lista de permissões de marketplace controla quais plugins os usuários podem instalar, e esta configuração bloqueia tudo que não vem de um plugin ou de configurações gerenciadas.
O valor é true para bloquear todas as quatro superfícies, ou um array nomeando as superfícies a bloquear:
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}
Para cada superfície bloqueada, Claude Code pula fontes de nível de usuário e projeto e carrega apenas fontes fornecidas por plugin e gerenciadas:
Superfície	Bloqueado quando bloqueado	Ainda carrega
skills	~/.claude/skills/, .claude/skills/	Skills de plugin, skills agrupadas, skills no diretório de política gerenciada
agents	~/.claude/agents/, .claude/agents/	Agents de plugin, agents integrados, agents no diretório de política gerenciada
hooks	Hooks em settings.json de usuário, projeto e local	Hooks de plugin, hooks em configurações gerenciadas
mcp	Servidores em ~/.claude.json e .mcp.json	MCP servers de plugin, servidores managed-mcp.json
Nomes de superfície que uma versão de Claude Code não reconhece são ignorados em vez de falhar no arquivo de configurações, portanto você pode adicionar novos nomes de superfície antes que todos os clientes tenham atualizado.
​
Gerenciando plugins
Use o comando /plugin para gerenciar plugins interativamente:
Procurar plugins disponíveis de marketplaces
Instalar/desinstalar plugins
Habilitar/desabilitar plugins
Ver detalhes de plugin (skills, agents, hooks fornecidos)
Adicionar/remover marketplaces
Saiba mais sobre o sistema de plugin na documentação de plugins.
​
Variáveis de ambiente
Variáveis de ambiente permitem controlar o comportamento do Claude Code sem editar arquivos de configuração. Qualquer variável também pode ser configurada em settings.json sob a chave env para aplicá-la a cada sessão ou implantá-la para sua equipe.
Veja a referência de variáveis de ambiente para a lista completa.
​
Ferramentas disponíveis para Claude
O Claude Code tem acesso a um conjunto de ferramentas para leitura, edição, busca, execução de comandos, e orquestração de subagents. Nomes de ferramenta são as strings exatas que você usa em regras de permissão e correspondedores de hook.
