# Histórico não normativo — Ambiente de Desenvolvimento do CEPRAEA Beach Pro

## Engenharia de Qualidade e Objetivos do Documento

Sob a ótica da Engenharia da Qualidade, o `VSCODE.md` atua como uma **especificação normativa e um plano de controle** do ambiente de desenvolvimento. Ele define o estado esperado, os controles preventivos, os métodos de verificação e os rigorosos critérios de aceitação.

Seu objetivo primordial é especificar e controlar um ambiente de desenvolvimento padronizado, seguro, reproduzível e verificável para o CEPRAEA Beach Pro. A finalidade é reduzir variações, prevenir defeitos estruturais e garantir que a escrita de código, os testes, o *build* e a depuração gerem resultados consistentes.

Embora o Visual Studio Code atue como o hub central, o propósito sistêmico deste documento é assegurar a qualidade do processo de desenvolvimento por meio de:

* **Padronização:** Uniformização de ferramentas, versões de software e arquivos de configuração
* **Prevenção:** Mitigação proativa de erros utilizando TypeScript, ESLint e Prettier
* **Automação:** Execução orquestrada de lintagem, testes, verificação de tipos e *build*
* **Segurança:** Proteção de credenciais, chaves de API e informações sensíveis/pessoais
* **Rastreabilidade:** Gestão de mudanças via Git, documentação clara e registro de evidências
* **Reproducibilidade:** Capacidade de recriar o ambiente idêntico em diferentes computadores
* **Validação:** Homologação do comportamento no navegador, em dispositivos móveis e em contexto de PWA
* **Objetividade:** Definição de critérios métricos para considerar o ambiente configurado e pronto

### Critérios de Aceite (Instalação Limpa)

Para que o ambiente de desenvolvimento seja considerado válido sob este plano de controle, uma instalação limpa (*clean install*) deve obrigatoriamente ser capaz de:

* Abrir o *Workspace* oficial do projeto sem conflitos ou alertas de ausência
* Instalar a árvore exata de dependências e extensões previstas
* Inicializar o sistema localmente sob as configurações predeterminadas
* Aplicar formatação e análise estática de código (*lint*) de forma automática
* Executar as suítes de testes, a validação de tipagem e o empacotamento (*build*) sem erros de ambiente
* Conectar e depurar o código perfeitamente sincronizado com o navegador
* Garantir que segredos e dados pessoais permaneçam fora do sistema de controle de versão
* Produzir resultados sistêmicos idênticos independentemente de quantas vezes o ambiente seja reinstalado

Este documento, tem o objetivo de configurar o Vs Code para desenvolver o CEPRAEA Beach Pro. Esse documento deve conter, todas as instruções, orientações, definições, configurações, decisões e tudo que for necessário, para garantir a configuração e a criação do ambiente de desenvolvimento, corretamente.

O Workspace não deve ser tratado apenas como uma configuração do VS Code. Para um desenvolvimento solo, ele pode funcionar como o centro operacional do projeto, concentrando código, documentação, padrões, comandos, testes e configurações.

Considerando a Engenharia da Qualidade, o objetivo do VSCODE.md é:
Especificar e controlar um ambiente de desenvolvimento padronizado, seguro, reproduzível e verificável para o CEPRAEA Beach Pro, reduzindo variações, prevenindo defeitos e garantindo que código, testes, build e depuração produzam resultados consistentes.

O VS Code é apenas o ponto central desse ambiente. O objetivo real do documento é assegurar a qualidade do processo de desenvolvimento por meio de:
padronização das ferramentas, versões e configurações;
prevenção de erros com TypeScript, ESLint e Prettier;
automação de lint, testes, verificação de tipos e build;
proteção de credenciais e informações pessoais;
rastreabilidade por Git, documentação e registro de evidências;
reprodução do ambiente em outro computador;
validação no navegador, no celular e em condições próprias de uma PWA;
definição de critérios objetivos para considerar o ambiente pronto.
O resultado esperado é que uma instalação limpa consiga:
abrir o Workspace oficial;
instalar exatamente as dependências previstas;
executar o sistema na configuração determinada;
formatar e analisar o código automaticamente;
executar testes, verificação de tipos e build sem erros;
depurar corretamente no navegador;
manter segredos e dados pessoais fora do repositório;
produzir os mesmos resultados independentemente da reinstalação do ambiente.
Em termos de qualidade, o documento deveria funcionar como uma especificação normativa e um plano de controle do ambiente de desenvolvimento. Ele define o estado esperado, os controles preventivos, os métodos de verificação e os critérios de aceitação.

## Identificação resumida

| Elemento | Definição |
| ---- | ---- |
| Taxonomia | Engenharia de Software → Aplicações Web → PWA → Gestão Esportiva → Handebol de Areia → CEPRAEA Beach Pro → Ambiente de Desenvolvimento → VS Code Workspace |
| Domínio | Ambiente de Desenvolvimento do CEPRAEA Beach Pro |
| Subdomínios centrais | VS Code, Workspace, estrutura do projeto, extensões, padrões, Git, execução, depuração, automação, variáveis, testes, PWA, implantação e documentação |
| Tema principal | Configuração e organização do ambiente de desenvolvimento solo do CEPRAEA Beach Pro |
| Contexto de negócio | Gestão de atletas e treinadores da equipe de handebol de areia do CEPRAEA |
| Contexto técnico | Desenvolvimento de uma aplicação web progressiva, responsiva, instalável e potencialmente offline |
| Contexto operacional | Uso prioritário em dispositivos móveis durante treinos, jogos e atividades da equipe |
| Responsável inicial | Davi Sermenho (Desenvolvedor solo) |
| Artefato central | `cepraea-beach-pro.code-workspace` |
| Resultado esperado | Ambiente consistente, automatizado, documentado, seguro e reproduzível |

## 1. Ambiente de Desenvolvimento

Domínio responsável pela preparação, organização, configuração e padronização das ferramentas utilizadas no desenvolvimento do CEPRAEA Beach Pro, incluindo VS Code, Workspace, Git, extensões, execução local, depuração, testes e publicação.

### 1.1. CEPRAEA Beach Pro

É uma aplicação web progressiva voltada à gestão e ao acompanhamento dos atletas e treinadores da equipe de handebol de areia do CEPRAEA, permitindo o gerenciamento de treinos, presença, avaliações, desempenho, jogos e informações da equipe.

## 2. Classificação consolidada

### 2.1. Taxonomia

```txt
A taxonomia organiza o conhecimento do projeto do nível mais amplo ao mais específico:
Engenharia de Software
└── Desenvolvimento de Aplicações Web
    └── Progressive Web Application — PWA
        └── Sistemas de Gestão Esportiva
            └── Gestão de Equipes de Handebol de Areia
                └── CEPRAEA Beach Pro
                    └── Ambiente de Desenvolvimento
                        └── VS Code Workspace
```

### 2.2. Em formato de classificação

- Nível
- Classificação
- Área de conhecimento
- Engenharia de Software
- Disciplina
- Desenvolvimento de Software
- Especialização
- Desenvolvimento de Aplicações Web
- Tipo de aplicação
- Progressive Web Application — PWA
- Domínio de negócio
- Gestão Esportiva
- Segmento
- Handebol de Areia
- Produto
- CEPRAEA Beach Pro
- Domínio técnico
- Ambiente de Desenvolvimento
- Unidade específica
- Workspace do VS Code

### 2.3. Domínio consolidado

Ambiente de Desenvolvimento do CEPRAEA Beach Pro
    É o domínio responsável por definir, configurar, organizar e manter todas as ferramentas, padrões e procedimentos necessários para o desenvolvimento solo do PWA.
Ele funciona como o centro operacional técnico do projeto, conectando:

- código-fonte;
- documentação;
- controle de versão;
- execução local;
- depuração; testes;
- banco de dados;
- configuração do PWA build;
- implantação.

## 3. Classificação consolidada

### 3.1. Taxonomia

A taxonomia organiza o conhecimento do projeto do nível mais amplo ao mais específico:

```text
Engenharia de Software
└── Desenvolvimento de Aplicações Web
    └── Progressive Web Application — PWA
        └── Sistemas de Gestão Esportiva
            └── Gestão de Equipes de Handebol de Areia
                └── CEPRAEA Beach Pro
                    └── Ambiente de Desenvolvimento
                        └── VS Code Workspace
```

Em formato de classificação:

| Nível                | Classificação                     |
| -------------------- | --------------------------------- |
| Área de conhecimento | Engenharia de Software            |
| Disciplina           | Desenvolvimento de Software       |
| Especialização       | Desenvolvimento de Aplicações Web |
| Tipo de aplicação    | Progressive Web Application — PWA |
| Domínio de negócio   | Gestão Esportiva                  |
| Segmento             | Handebol de Areia                 |
| Produto              | CEPRAEA Beach Pro                 |
| Domínio técnico      | Ambiente de Desenvolvimento       |
| Unidade específica   | Workspace do VS Code              |

***

## 4. Domínio consolidado

**Ambiente de Desenvolvimento do CEPRAEA Beach Pro**
É o domínio responsável por definir, configurar, organizar e manter todas as ferramentas, padrões e procedimentos necessários para o desenvolvimento solo do PWA.

Ele funciona como o centro operacional técnico do projeto, conectando:

- código-fonte;
- documentação;
- controle de versão;
- execução local;
- depuração;
- testes;
- banco de dados;
- configuração do PWA;
- build;
- implantação.

***

## 5. Subdomínios

### 5.1 Configuração do VS Code

Abrange a instalação, personalização e utilização do editor.

Inclui:

- configurações globais e específicas do projeto;
- interface e preferências do editor;
- terminal integrado;
- atalhos;
- perfis;
- sincronização de configurações.

### 5.2 Gerenciamento do Workspace

Responsável pela criação e manutenção do arquivo:

```text
cepraea-beach-pro.code-workspace
```

Inclui:

- definição das pastas do projeto;
- configurações exclusivas do workspace;
- suporte a múltiplas raízes;
- recomendações de extensões;
- associação de tarefas e depuradores.

### 5.3 Estrutura e Organização do Projeto

Define como os arquivos e diretórios serão distribuídos.

Inclui:

- organização por funcionalidades;
- componentes compartilhados;
- páginas e rotas;
- serviços;
- tipos;
- utilitários;
- testes;
- documentação;
- arquivos públicos.

### 5.4 Ferramentas e Extensões

Define as ferramentas utilizadas para apoiar o desenvolvimento.

Exemplos:

- ESLint;
- Prettier;
- GitLens;
- Error Lens;
- extensões para TypeScript;
- extensões para testes;
- extensões para banco de dados;
- ferramentas de inspeção do PWA.

### 5.5 Padronização do Código

Estabelece os padrões técnicos do projeto.

Inclui:

- formatação;
- linting;
- convenções de nomenclatura;
- organização de imports;
- estrutura dos componentes;
- tratamento de erros;
- comentários e documentação;
- regras para TypeScript.

### 5.6 Controle de Versão

Abrange a integração do projeto com Git.

Inclui:

- inicialização do repositório;
- configuração do `.gitignore`;
- branches;
- commits;
- tags;
- versionamento;
- repositório remoto;
- estratégias de backup e recuperação.

### 5.7 Execução Local

Define como iniciar e utilizar o sistema no computador de desenvolvimento.

Inclui:

- instalação de dependências;
- servidor local;
- scripts do projeto;
- portas utilizadas;
- acesso pelo navegador;
- acesso por dispositivos móveis na rede local.

### 5.8 Depuração

Responsável pela investigação e correção de falhas.

Inclui:

- breakpoints;
- configuração do `launch.json`;
- inspeção de variáveis;
- depuração no navegador;
- logs;
- análise de erros;
- diagnóstico do service worker.

### 5.9 Automação de Tarefas

Define comandos repetitivos executados pelo VS Code ou pelo gerenciador de pacotes.

Inclui:

- desenvolvimento;
- build;
- lint;
- testes;
- verificação de tipos;
- geração de arquivos;
- preparação para implantação.

### 5.10 Variáveis de Ambiente e Configurações

Gerencia informações que mudam entre os ambientes.

Inclui:

- `.env`;
- `.env.local`;
- `.env.example`;
- URLs de APIs;
- chaves públicas;
- configurações de banco de dados;
- separação entre desenvolvimento e produção.

Dados secretos não devem ser armazenados no Workspace nem enviados ao Git.

### 5.11 Qualidade e Testes

Abrange os mecanismos utilizados para verificar o funcionamento do sistema.

Inclui:

- testes unitários;
- testes de componentes;
- testes de integração;
- testes de ponta a ponta;
- validação de formulários;
- cobertura de testes;
- análise estática;
- acessibilidade.

### 5.12 Configuração do PWA

Concentra os recursos que diferenciam a solução de uma aplicação web convencional.

Inclui:

- manifesto da aplicação;
- service worker;
- instalação no dispositivo;
- cache;
- atualização da aplicação;
- funcionamento offline;
- ícones;
- telas de abertura;
- notificações, caso sejam necessárias.

### 5.13 Build e Implantação

Define como gerar e disponibilizar a aplicação.

Inclui:

- build de produção;
- variáveis de produção;
- validação antes da publicação;
- hospedagem;
- domínio;
- HTTPS;
- monitoramento;
- estratégia de atualização.

### 5.14 Documentação Técnica

Registra as decisões e os procedimentos do projeto.

Inclui:

- `README.md`;
- guia de instalação;
- arquitetura;
- decisões técnicas;
- comandos úteis;
- resolução de problemas;
- histórico de mudanças.

***

## 6. Tema principal

### **Configuração e organização do ambiente de desenvolvimento solo para o PWA CEPRAEA Beach Pro no Visual Studio Code**

Esse tema concentra a preparação de um ambiente:

- padronizado;
- produtivo;
- documentado;
- seguro;
- reproduzível;
- adequado à evolução do produto.

O foco não é somente configurar o editor. O objetivo é criar uma base técnica que permita desenvolver, testar, depurar, versionar e publicar o CEPRAEA Beach Pro de maneira organizada.

***

## 7. Contexto

### 7.1. Contexto organizacional

O sistema será utilizado no âmbito do **CEPRAEA**, atendendo a equipe de handebol de areia.

A aplicação deve apoiar as atividades esportivas e administrativas relacionadas a:

- atletas;
- treinadores;
- treinos;
- presença;
- avaliações;
- jogos;
- desempenho;
- estatísticas;
- comunicação e acompanhamento da equipe.

### 7.2. Contexto de desenvolvimento

O desenvolvimento será realizado inicialmente por uma única pessoa.

Isso exige que o ambiente reduza o trabalho manual e preserve o conhecimento do projeto. As decisões, comandos e configurações precisam estar documentados para evitar dependência da memória do desenvolvedor.

O Workspace deve favorecer:

- rapidez na inicialização do projeto;
- automação de tarefas recorrentes;
- prevenção de erros;
- consistência do código;
- facilidade de manutenção;
- recuperação do ambiente em outro computador.

### 7.3. Contexto tecnológico

O CEPRAEA Beach Pro será uma **Progressive Web Application** acessível por navegador e instalável em dispositivos compatíveis.

O ambiente deverá contemplar:

- desenvolvimento web responsivo;
- uso em celulares;
- comportamento instalável;
- funcionamento em conexões instáveis;
- possibilidade de recursos offline;
- sincronização segura de dados;
- compatibilidade com diferentes navegadores.

### 7.4. Contexto dos usuários

Existem inicialmente dois grupos principais:

| Grupo       | Necessidades gerais                                              |
| ----------- | ---------------------------------------------------------------- |
| Atletas     | Consultar treinos, presença, jogos, avaliações e desempenho      |
| Treinadores | Gerenciar equipe, treinos, escalações, avaliações e estatísticas |

Os treinadores podem ter permissões administrativas superiores às dos atletas.

### 7.5. Contexto operacional

A aplicação deverá ser adequada ao ambiente esportivo, no qual o acesso pode ocorrer:

- durante treinos;
- em quadras ou praias;
- antes e depois dos jogos;
- por dispositivos móveis;
- sob conexão limitada ou instável;
- com necessidade de interação rápida.

Consequentemente, o produto deve priorizar simplicidade, responsividade, legibilidade e baixo número de etapas para registrar ou consultar informações.

***

### Declaração consolidada

> O domínio **Ambiente de Desenvolvimento do CEPRAEA Beach Pro** pertence à área de Engenharia de Software e trata da configuração, organização, padronização e manutenção do Workspace do Visual Studio Code e das ferramentas associadas ao desenvolvimento solo de uma Progressive Web Application para atletas e treinadores da equipe de handebol de areia do CEPRAEA.

## 7. Escopo

O escopo deste domínio compreende a preparação, configuração, organização e manutenção do ambiente utilizado no desenvolvimento solo do CEPRAEA Beach Pro.

Fazem parte do escopo:

- instalação e configuração do Visual Studio Code;
- criação do arquivo `cepraea-beach-pro.code-workspace`;
- definição da estrutura de pastas do projeto;
- instalação e recomendação de extensões;
- configuração de formatação e análise estática;
- configuração do TypeScript;
- integração com Git;
- definição de scripts de desenvolvimento;
- configuração de execução local;
- configuração de depuração;
- gerenciamento de variáveis de ambiente;
- definição de testes;
- configuração do PWA;
- configuração de build;
- preparação para implantação;
- documentação dos procedimentos técnicos;
- padronização das convenções de código;
- configuração de verificações automáticas;
- mecanismos de backup e recuperação do projeto.

O domínio também deve garantir que o ambiente seja:

- reproduzível em outro computador;
- suficientemente simples para manutenção individual;
- documentado;
- seguro;
- consistente;
- preparado para a evolução futura do produto.

***

## 2. Escopo negativo

O escopo negativo define aquilo que não é responsabilidade direta do domínio de ambiente de desenvolvimento.

Não fazem parte deste domínio:

- definição das regras esportivas do handebol de areia;
- decisão sobre escalações da equipe;
- planejamento de treinos;
- avaliação técnica dos atletas;
- gestão administrativa do CEPRAEA;
- definição jurídica sobre uso de dados pessoais;
- produção de conteúdo esportivo;
- aquisição de equipamentos físicos;
- gestão financeira da organização;
- manutenção dos dispositivos pessoais dos atletas;
- suporte geral de informática aos usuários;
- desenvolvimento completo das funcionalidades de negócio;
- definição visual detalhada da interface;
- execução de campanhas de comunicação;
- operação diária da equipe esportiva.

Embora alguns desses temas influenciem o desenvolvimento, eles pertencem a outros domínios.

Por exemplo, o ambiente de desenvolvimento pode fornecer ferramentas para construir o módulo de avaliação de atletas, mas não define os critérios esportivos dessa avaliação.

***

## 3. Boas práticas

### 3.1 Manter o ambiente reproduzível

As configurações essenciais devem estar versionadas no repositório.

Exemplos:

```text
.vscode/
.editorconfig
eslint.config.js
.prettierrc
tsconfig.json
tsconfig.app.json
tsconfig.node.json
.env.example
package.json
README.md
```

Um novo ambiente deve poder ser preparado por meio de procedimentos documentados, sem depender da memória do desenvolvedor.

### 3.2 Versionar configurações úteis

Devem ser versionadas as configurações que contribuem para a consistência do projeto.

Exemplos:

- formatação;
- extensões recomendadas;
- tarefas;
- depuração;
- convenções do editor;
- regras de lint;
- scripts de testes.

Não devem ser versionados dados pessoais, tokens ou configurações exclusivas da máquina.

### 3.3 Automatizar verificações repetitivas

A automação reduz falhas e evita que tarefas importantes sejam esquecidas.

Exemplos:

```bash
npm run dev
npm run build
npm run lint
npm run test
npm run typecheck
npm run format
```

Antes de publicar uma versão, o ideal é executar uma verificação consolidada:

```bash
npm run validate
```

Esse comando pode executar lint, verificação de tipos, testes e build.

### 3.4 Usar TypeScript com regras rigorosas

O TypeScript deve ser configurado para identificar problemas antes da execução.

Configurações recomendadas:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### 3.5 Separar configuração de código

Informações que variam entre ambientes não devem ficar fixas no código-fonte.

Exemplo inadequado:

```ts
const apiUrl = "https://api.producao.com";
```

Exemplo adequado:

```ts
const apiUrl = import.meta.env.VITE_API_URL;
```

### 3.6 Documentar decisões técnicas

Decisões importantes devem ser registradas.

Exemplos:

- escolha do framework;
- escolha do banco de dados;
- estratégia de autenticação;
- política de funcionamento offline;
- estrutura de pastas;
- abordagem de testes;
- estratégia de implantação.

### 3.7 Fazer commits pequenos e objetivos

Cada commit deve representar uma alteração compreensível.

Exemplos:

```text
feat: adiciona cadastro de atletas
fix: corrige validação da data de nascimento
test: adiciona testes do formulário de presença
docs: documenta configuração do workspace
```

### 3.8 Priorizar simplicidade

Como o desenvolvimento é solo, a arquitetura deve evitar complexidade desnecessária.

Uma solução simples, compreensível e testável tende a ser mais sustentável do que uma arquitetura sofisticada com grande custo de manutenção.

***

## 4. Técnicas utilizadas por desenvolvedores solo

### 4.1 Desenvolvimento orientado a funcionalidades

O projeto pode ser organizado por funcionalidades, em vez de apenas por tipos técnicos.

Exemplo:

```text
src/
├── features/
│   ├── atletas/
│   ├── treinadores/
│   ├── treinos/
│   ├── jogos/
│   ├── presencas/
│   └── avaliacoes/
```

Cada funcionalidade pode conter:

```text
atletas/
├── components/
├── pages/
├── services/
├── schemas/
├── types/
└── tests/
```

Essa técnica facilita a localização e manutenção do código.

### 4.2 Desenvolvimento incremental

As funcionalidades devem ser construídas em partes pequenas.

Exemplo de sequência:

1. cadastro básico de atletas;
2. listagem de atletas;
3. edição;
4. controle de permissões;
5. validação;
6. testes;
7. funcionamento offline.

### 4.3 Prototipação rápida

Antes de desenvolver uma funcionalidade completa, pode ser criado um protótipo funcional simples.

Exemplo:

- primeiro criar uma tela estática de presença;
- depois adicionar estado local;
- em seguida integrar com o banco;
- por último adicionar sincronização offline.

### 4.4 Uso de checklists

Checklists reduzem o risco de esquecimento.

Exemplo de checklist para concluir uma funcionalidade:

- requisitos atendidos;
- interface responsiva;
- validação implementada;
- tratamento de erros;
- controle de acesso;
- testes criados;
- lint aprovado;
- documentação atualizada.

### 4.5 Timeboxing

O desenvolvedor define períodos limitados para uma atividade.

Exemplo:

- até duas horas para investigar um erro;
- até um dia para criar um protótipo;
- uma sessão específica para testes;
- uma sessão semanal para manutenção.

Isso reduz o risco de passar muito tempo em detalhes pouco relevantes.

### 4.6 Diário técnico

Manter um registro de desenvolvimento ajuda a recuperar contexto.

Exemplo:

```text
2026-07-25

- Criada estrutura inicial do projeto.
- Definido uso de TypeScript.
- Configurado ESLint e Prettier.
- Próximo passo: autenticação de atletas e treinadores.
```

### 4.7 Uso de branches curtas

O desenvolvimento solo pode utilizar branches temporárias para mudanças relevantes.

Exemplos:

```text
main
feature/cadastro-atletas
feature/controle-presenca
fix/login-offline
```

Branches não devem permanecer abertas por longos períodos.

### 4.8 Automação local antes de automação complexa

Primeiro devem ser automatizadas as tarefas locais essenciais.

Depois podem ser adicionados recursos como integração contínua, testes automáticos remotos e implantação automática.

***

## 5. Configurações necessárias

### 5.1 Configuração do Workspace

Exemplo:

```json
{
  "folders": [
    {
      "name": "CEPRAEA Beach Pro",
      "path": "."
    }
  ],
  "settings": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit"
    },
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "files.exclude": {
      "**/node_modules": true,
      "**/dist": true
    },
    "files.eol": "\n",
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "typescript.tsdk": "node_modules/typescript/lib",
    "eslint.validate": ["javascript", "javascriptreact", "typescript", "typescriptreact"]
  },
  "extensions": {
    "recommendations": [
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "eamodio.gitlens",
      "usernamehw.errorlens",
      "editorconfig.editorconfig"
    ]
  }
}
```

### 5.2 Extensões recomendadas

Arquivo `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "eamodio.gitlens",
    "usernamehw.errorlens",
    "editorconfig.editorconfig"
  ]
}
```

As extensões devem ser recomendadas, mas não obrigatoriamente impostas.

### 5.3 Configuração de formatação

Exemplo de `.prettierrc`:

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100
}
```

### 5.4 EditorConfig

Exemplo de `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
```

### 5.5 Configuração de tarefas

Exemplo de `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Iniciar desenvolvimento",
      "type": "npm",
      "script": "dev",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Validar projeto",
      "type": "npm",
      "script": "validate",
      "problemMatcher": []
    },
    {
      "label": "Executar testes",
      "type": "npm",
      "script": "test",
      "problemMatcher": []
    },
    {
      "label": "Verificar tipos",
      "type": "npm",
      "script": "typecheck",
      "problemMatcher": []
    }
  ]
}
```

### 5.6 Configuração de depuração

Exemplo de `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Depurar CEPRAEA Beach Pro",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
```

### 5.7 Variáveis de ambiente

Exemplo de `.env.example`:

```env
VITE_APP_NAME=CEPRAEA Beach Pro
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
VITE_ENABLE_OFFLINE=false
```

O arquivo `.env.example` pode ser versionado.

O arquivo `.env.local` deve permanecer fora do repositório.

> A `VITE_SUPABASE_ANON_KEY` é uma chave pública segura para expor no cliente. A `service_role key` do Supabase jamais deve aparecer em variáveis `VITE_*`, pois fica embutida no bundle e é acessível por qualquer usuário.

### 5.8 Gitignore

Exemplo:

```gitignore
node_modules/
dist/
coverage/
.env
.env.local
*.log
.DS_Store
```

### 5.9 Scripts do projeto

Exemplo:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run --passWithNoTests",
    "validate": "npm run lint && npm run typecheck && npm run test && npm run build"
  }
}
```

> A flag `--passWithNoTests` faz o Vitest retornar exit 0 quando não há arquivos de teste, evitando que o script `validate` falhe durante a fase inicial do projeto. Quando testes forem adicionados, qualquer falha real continuará retornando exit 1 normalmente.

### 5.10 Configuração básica do PWA

Devem ser configurados:

- nome da aplicação;
- nome abreviado;
- ícones;
- cor do tema;
- URL inicial;
- modo de exibição;
- service worker;
- estratégia de cache;
- política de atualização;
- página de indisponibilidade;
- comportamento offline.

#### 5.10.1 vite.config.ts

Exemplo implementado usando `vite-plugin-pwa` com `@vitejs/plugin-react`:

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: Boolean(process.env.CHOKIDAR_USEPOLLING),
    },
  },
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'CEPRAEA Beach Pro',
        short_name: 'Beach Pro',
        description: 'Gestão de atletas e treinadores de handebol de areia do CEPRAEA',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: 'icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
    }),
  ],
});
```

`registerType: 'autoUpdate'` faz o service worker atualizar automaticamente quando uma nova versão do build estiver disponível, eliminando o risco de versões antigas ficarem presas em cache.

`server.host: true` vincula o servidor à interface `0.0.0.0`, necessário para acesso de fora do container Docker ou de dispositivos na rede local. `watch.usePolling` é ativado condicionalmente pela variável `CHOKIDAR_USEPOLLING`, definida apenas no `docker-compose.yml`, sem afetar o `npm run dev` direto no host.

### 5.11 Estrutura do TypeScript

O projeto usa três arquivos tsconfig com responsabilidades distintas, seguindo o padrão recomendado pelo Vite para projetos TypeScript:

| Arquivo | Compila | Target |
| --- | --- | --- |
| `tsconfig.json` | Orquestrador — apenas referências, sem `compilerOptions` | — |
| `tsconfig.app.json` | `src/` — código da aplicação React | ES2020 |
| `tsconfig.node.json` | `vite.config.ts` — ferramentas de build | ES2022 |

`tsconfig.app.json` (código da aplicação):

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
```

### 5.12 Dependências e versões

Gerenciador de pacotes: `npm`

**Dependências de produção:**

| Pacote | Versão |
| --- | --- |
| `react` + `react-dom` | `^19.0.0` |
| `@supabase/supabase-js` | `^2.49.0` |

**Dependências de desenvolvimento:**

| Pacote | Versão |
| --- | --- |
| `vite` | `^6.2.0` |
| `@vitejs/plugin-react` | `^4.3.4` |
| `vite-plugin-pwa` | `^0.21.1` |
| `typescript` | `~5.7.2` |
| `vitest` | `^3.0.8` |
| `@testing-library/react` | `^16.2.0` |
| `eslint` | `^9.22.0` |
| `typescript-eslint` | `^8.26.1` |
| `prettier` | `^3.5.3` |

### 5.13 Contêinerização com Docker

O Docker permite executar o servidor de desenvolvimento em um container isolado, sem exigir que Node.js esteja instalado na máquina.

**Quando usar:**

- máquina sem Node.js instalado;
- garantia de ambiente idêntico entre diferentes computadores;
- acesso ao servidor via dispositivos móveis na rede local.

**Pré-requisito:** Docker Desktop instalado e daemon em execução (`docker ps` deve retornar sem erro).

**Versões utilizadas:** Docker 29.1.3, Docker Compose v2.40.3.

#### Dockerfile

```dockerfile
FROM node:24-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
EXPOSE 5173
CMD ["npm", "run", "dev"]
```

`npm ci` instala dependências a partir do `package-lock.json`, garantindo reprodutibilidade.

#### docker-compose.yml

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true
    env_file:
      - path: .env.local
        required: false
```

Pontos importantes:

- volume `.:/app` → código-fonte montado para hot reload;
- volume anônimo `/app/node_modules` → preserva as dependências do container e impede que o `node_modules` do host sobrescreva;
- `CHOKIDAR_USEPOLLING=true` → necessário no WSL2, onde o inotify não propaga eventos de arquivo dentro do container;
- `env_file.required: false` → não falha se `.env.local` ainda não existir.

#### .dockerignore

```text
node_modules/
dist/
coverage/
.env
.env.local
.git/
.vscode/
*.log
.DS_Store
```

Impede que `node_modules` do host entre no contexto de build, reduzindo tempo e tamanho da imagem.

#### Comandos

```bash
# Primeira execução (constrói a imagem e inicia)
docker compose up --build

# Execuções subsequentes
docker compose up

# Encerrar
docker compose down
```

O servidor fica disponível em `http://localhost:5173`. O hot reload funciona normalmente: alterações nos arquivos `.tsx` e `.ts` são detectadas pelo polling e refletidas no navegador sem reiniciar o container.

> O `npm run dev` direto no host continua funcionando sem alteração. O polling é ativado apenas quando a variável `CHOKIDAR_USEPOLLING` está presente no ambiente, o que ocorre somente dentro do container.

***

## 6. O que fazer / O que não fazer

| O que fazer | O que não fazer |
| :--- | :--- |
| criar o Workspace no início do projeto; | armazenar senhas ou tokens no repositório; |
| manter configurações essenciais no Git; | versionar arquivos `.env` com dados reais; |
| usar TypeScript em modo rigoroso; | depender exclusivamente de extensões do editor; |
| configurar formatação automática; | instalar muitas extensões sem necessidade; |
| configurar lint; | misturar regra de negócio com componentes visuais; |
| definir scripts padronizados; | manter toda a aplicação em poucos arquivos grandes; |
| criar um `.env.example`; | ignorar mensagens do TypeScript; |
| separar segredos de configurações públicas; | desativar regras de lint sem justificativa; |
| documentar como instalar e executar o projeto; | publicar sem executar testes; |
| testar a aplicação em celular; | confiar apenas em testes manuais; |
| verificar o comportamento em conexão lenta; | desenvolver apenas para telas de computador; |
| testar instalação como PWA; | assumir que sempre haverá internet; |
| validar o funcionamento offline; | armazenar dados sensíveis sem proteção; |
| criar testes para regras importantes; | criar arquitetura complexa prematuramente; |
| revisar dependências periodicamente; | adicionar bibliotecas para resolver problemas simples; |
| manter commits pequenos; | manter código sem documentação mínima; |
| criar backups; | fazer alterações grandes em um único commit; |
| utilizar autenticação e autorização; | trabalhar diretamente na versão de produção; |
| validar dados no cliente e no servidor; | permitir acesso administrativo apenas com verificações visuais; |
| monitorar erros de produção; | utilizar o cache do PWA sem estratégia de atualização; |
| manter o projeto simples. | tratar o service worker como um detalhe secundário. |

***

## 8. Exemplos de uso real

### 8.1 Início de uma sessão de desenvolvimento

O desenvolvedor abre:

```text
cepraea-beach-pro.code-workspace
```

O VS Code carrega:

- configurações do projeto;
- extensões recomendadas;
- atalhos;
- tarefas;
- depuradores;
- estrutura correta de pastas.

Depois, o desenvolvedor executa a tarefa:

```text
Iniciar desenvolvimento
```

O servidor local é iniciado de forma padronizada.

### 8.2 Criação do módulo de presença

O desenvolvedor cria:

```text
src/features/presencas/
├── components/
├── pages/
├── services/
├── schemas/
├── types/
└── tests/
```

Ao salvar um arquivo:

- o Prettier formata o código;
- o ESLint sinaliza problemas;
- o TypeScript identifica inconsistências;
- o Error Lens apresenta erros diretamente no editor.

### 8.3 Depuração de erro no cadastro

Um atleta não consegue concluir o cadastro.

O desenvolvedor:

1. abre o modo de depuração;
2. reproduz o erro;
3. adiciona um breakpoint;
4. inspeciona os dados enviados;
5. identifica uma data em formato inválido;
6. corrige o schema;
7. cria um teste para evitar regressão.

### 8.4 Trabalho em ambiente sem internet

Durante um treino na praia, a conexão fica indisponível.

A aplicação:

- carrega a interface armazenada em cache;
- permite consultar dados previamente sincronizados;
- registra presença localmente;
- marca a operação como pendente;
- sincroniza os dados quando a conexão retorna.

Esse comportamento depende diretamente da configuração correta do PWA.

### 8.5 Publicação de uma nova versão

Antes da publicação, o desenvolvedor executa:

```bash
npm run validate
```

O processo verifica:

- lint;
- tipos;
- testes;
- build.

A publicação só continua quando todas as etapas forem aprovadas.

***

## 9. Impacto das configurações no resultado final

### 9.1 Formatação automática

Impacto positivo:

- código visualmente consistente;
- revisão mais fácil;
- menos discussões sobre estilo;
- commits mais limpos.

Sem configuração:

- formatação irregular;
- alterações desnecessárias;
- maior dificuldade de leitura.

### 9.2 ESLint

Impacto positivo:

- identificação antecipada de erros;
- redução de código inseguro;
- prevenção de padrões inadequados.

Sem configuração:

- problemas aparecem apenas durante a execução;
- inconsistências se acumulam.

### 9.3 TypeScript rigoroso

Impacto positivo:

- contratos mais claros;
- menos erros de valores indefinidos;
- refatoração mais segura;
- maior previsibilidade.

Sem configuração rigorosa:

- erros podem ficar escondidos;
- tipos perdem valor;
- manutenção se torna mais arriscada.

### 9.4 Testes automáticos

Impacto positivo:

- prevenção de regressões;
- maior confiança nas mudanças;
- facilidade de evolução.

Sem testes:

- cada alteração pode quebrar funcionalidades antigas;
- validação depende exclusivamente do desenvolvedor.

### 9.5 Configuração do PWA

Impacto positivo:

- instalação em dispositivos móveis;
- melhor desempenho;
- uso em condições de conectividade limitada;
- experiência próxima de um aplicativo.

Configuração incorreta pode causar:

- versões antigas presas em cache;
- dados desatualizados;
- falhas de instalação;
- comportamento inconsistente.

### 9.6 Variáveis de ambiente

Impacto positivo:

- separação entre desenvolvimento e produção;
- maior segurança;
- implantação mais simples.

Configuração inadequada pode expor:

- credenciais;
- URLs privadas;
- chaves de serviços;
- informações internas.

### 9.7 Workspace padronizado

Impacto positivo:

- inicialização rápida;
- menor carga mental;
- contexto centralizado;
- facilidade de retomada do trabalho.

Sem padronização:

- comandos ficam dispersos;
- configurações se perdem;
- erros de ambiente são mais frequentes.

***

## 10. Possíveis melhorias

### 10.1 Integração contínua

Adicionar um fluxo automático que execute:

- lint;
- testes;
- typecheck;
- build;
- auditoria de dependências.

### 10.2 Implantação automática

Publicar automaticamente versões aprovadas após integração com a branch principal.

### 10.3 Ambiente de homologação

Criar um ambiente separado para testes antes da produção.

Exemplo:

```text
Desenvolvimento
Homologação
Produção
```

### 10.4 Testes de ponta a ponta

Automatizar fluxos como:

- login;
- cadastro de atleta;
- registro de presença;
- criação de treino;
- consulta de avaliação.

### 10.5 Auditoria de acessibilidade

Adicionar verificações para:

- contraste;
- navegação por teclado;
- leitores de tela;
- tamanho de elementos interativos;
- mensagens de erro.

### 10.6 Monitoramento de erros

Registrar erros reais da aplicação para identificar falhas que não apareceram durante o desenvolvimento.

### 10.7 Verificação de desempenho

Avaliar:

- tamanho do bundle;
- velocidade de carregamento;
- uso de cache;
- consumo de dados;
- desempenho em celulares mais simples.

### 10.8 Padronização de componentes

Criar uma biblioteca interna de componentes reutilizáveis.

Exemplos:

- botão;
- campo de formulário;
- cartão de atleta;
- seletor de treino;
- modal;
- indicador de conexão;
- mensagem de erro.

### 10.9 Estratégia de sincronização

Definir claramente:

- quais dados podem funcionar offline;
- como os dados pendentes são armazenados;
- quando ocorre a sincronização;
- como conflitos são resolvidos;
- como o usuário é informado.

### 10.10 Documentação arquitetural

Criar registros formais para decisões relevantes, conhecidos como Architecture Decision Records.

***

## 11. Riscos

### 11.1 Dependência de uma única pessoa

Como o projeto é desenvolvido individualmente, conhecimento e decisões podem ficar concentrados.

Mitigação:

- documentação;
- commits claros;
- código simples;
- automação;
- backups.

### 11.2 Sobrecarga do desenvolvedor

O desenvolvedor solo acumula funções de:

- análise;
- arquitetura;
- programação;
- testes;
- implantação;
- suporte;
- documentação.

Mitigação:

- priorização;
- entregas incrementais;
- automação;
- redução de escopo;
- uso de checklists.

### 11.3 Complexidade excessiva

O projeto pode adotar tecnologias acima da necessidade real.

Mitigação:

- justificar cada dependência;
- começar simples;
- evitar abstrações prematuras;
- revisar a arquitetura periodicamente.

### 11.4 Vazamento de dados

Dados de atletas podem incluir informações pessoais.

Riscos:

- exposição acidental;
- acesso indevido;
- armazenamento inseguro;
- logs contendo dados sensíveis.

Mitigação:

- controle de acesso;
- criptografia;
- políticas de retenção;
- minimização de dados;
- revisão de logs.

### 11.5 Falhas de sincronização offline

Operações feitas sem internet podem entrar em conflito.

Exemplo:

- treinador altera uma presença;
- outro dispositivo altera o mesmo registro;
- ambos sincronizam depois.

Mitigação:

- identificação de versão;
- registro de data e hora;
- regras de resolução;
- confirmação do usuário em conflitos relevantes.

### 11.6 Cache desatualizado

O service worker pode manter arquivos antigos.

Mitigação:

- versionamento do cache;
- estratégia de atualização;
- aviso de nova versão;
- limpeza de caches antigos.

### 11.7 Dependência de bibliotecas

Bibliotecas podem ser abandonadas, apresentar vulnerabilidades ou introduzir alterações incompatíveis.

Mitigação:

- manter poucas dependências;
- revisar atualizações;
- fixar versões quando necessário;
- executar auditorias.

### 11.8 Falta de testes em dispositivos reais

A aplicação pode funcionar no computador e falhar em celulares.

Mitigação:

- testar em diferentes tamanhos de tela;
- testar navegadores móveis;
- testar conexão lenta;
- testar instalação;
- testar modo offline.

### 11.9 Perda do repositório ou do ambiente local

Mitigação:

- repositório remoto;
- backups periódicos;
- documentação de recuperação;
- variáveis protegidas fora do repositório.

***

## 12. Limites

### 12.1 Limites do VS Code

O VS Code organiza e apoia o desenvolvimento, mas não garante sozinho:

- qualidade do código;
- segurança;
- bom desempenho;
- funcionamento offline;
- cobertura de testes;
- conformidade legal.

Esses resultados dependem das práticas adotadas.

### 12.2 Limites do PWA

Uma PWA pode apresentar diferenças entre navegadores e sistemas operacionais.

Alguns recursos podem ter suporte limitado, principalmente:

- notificações;
- execução em segundo plano;
- integração com hardware;
- sincronização periódica;
- armazenamento local.

### 12.3 Limites do funcionamento offline

Nem todas as funcionalidades precisam ou podem funcionar sem internet.

Operações que dependem de dados atualizados, autenticação remota ou processamento externo podem exigir conexão.

### 12.4 Limites de segurança no cliente

Nenhuma informação secreta deve ser considerada protegida dentro do código do navegador.

Variáveis incluídas no build do front-end podem ser inspecionadas pelos usuários.

Chaves privadas e operações sensíveis devem permanecer no servidor.

### 12.5 Limites do desenvolvimento solo

A capacidade de entrega será limitada por:

- tempo disponível;
- conhecimento técnico;
- quantidade de funcionalidades;
- manutenção;
- suporte;
- testes;
- operação.

O escopo deve ser ajustado à capacidade real de uma única pessoa.

### 12.6 Limites da automação

Automação reduz erros, mas não substitui:

- revisão crítica;
- testes manuais;
- validação com usuários;
- análise de segurança;
- decisões de produto.

***

## 13. Critérios de conclusão do domínio

O ambiente de desenvolvimento pode ser considerado inicialmente estabelecido quando:

- o Workspace estiver criado;
- o repositório Git estiver configurado;
- a estrutura inicial estiver definida;
- o projeto puder ser executado localmente;
- o lint estiver funcionando;
- a formatação automática estiver ativa;
- o TypeScript estiver configurado;
- as variáveis de ambiente estiverem documentadas;
- os testes puderem ser executados;
- a depuração estiver disponível;
- o build de produção for concluído;
- a configuração básica do PWA estiver implementada;
- o processo estiver documentado no README.

**Estado:** Todos os critérios foram atendidos em 2026-07-26.

***

## 14. Declaração final

O ambiente de desenvolvimento do CEPRAEA Beach Pro deve funcionar como uma base técnica simples, segura, automatizada e reproduzível para o desenvolvimento solo da aplicação.

***

## 1. Escopo: Domínio de Ambiente de Desenvolvimento

O escopo deste domínio compreende a preparação, configuração, organização e manutenção do ambiente utilizado no desenvolvimento solo do CEPRAEA Beach Pro.

O domínio também deve garantir que o ambiente seja:

- reproduzível em outro computador
- suficientemente simples para manutenção individual
- documentado
- seguro
- consistente
- preparado para a evolução futura do produto

> Seu principal papel é reduzir erros, preservar conhecimento, facilitar a manutenção e garantir que o PWA possa evoluir sem que o aumento de funcionalidades torne o projeto desorganizado ou inviável para um único desenvolvedor.

O **escopo** negativo define aquilo que não é responsabilidade direta do domínio de ambiente de desenvolvimento.

Embora alguns desses temas influenciem o desenvolvimento, eles pertencem a outros domínios.

Por exemplo, o ambiente de desenvolvimento pode fornecer ferramentas para construir o módulo de avaliação de atletas, mas não define os critérios esportivos dessa avaliação.

| Faz parte do Escopo (Ambiente de Desenvolvimento) | Não Faz parte do Escopo (Regras de Negócio e Gestão) |
| :--- | :--- |
| [Ferramental] Instalação e configuração do Visual Studio Code | [Esporte] Definição das regras esportivas do handebol de areia |
| [Configuração] Criação do arquivo cepraea-beach-pro.code-workspace | [Esporte] Decisão sobre escalações da equipe |
| [Arquitetura] Definição da estrutura de pastas do projeto | [Esporte] Planejamento de treinos |
| [Ferramental] Instalação e recomendação de extensões | [Esporte] Avaliação técnica dos atletas |
| [Qualidade] Configuração de formatação e análise estática | [Gestão] Gestão administrativa do CEPRAEA |
| [Compilação] Configuração do TypeScript | [Legal] Definição jurídica sobre uso de dados pessoais |
| [VCS] Integração com Git | [Marketing] Produção de conteúdo esportivo |
| [Automação] Definição de scripts de desenvolvimento | [Gestão] Aquisição de equipamentos físicos |
| [Execução] Configuração de execução local | [Finanças] Gestão financeira da organização |
| [Execução] Configuração de depuração | [Suporte] Manutenção dos dispositivos pessoais dos atletas |
| [Segurança] Gerenciamento de variáveis de ambiente | [Suporte] Suporte geral de informática aos usuários |
| [Qualidade] Definição de testes | [Negócio] Desenvolvimento completo das funcionalidades de negócio |
| [Build] Configuração do PWA | [Design] Definição visual detalhada da interface |
| [Build] Configuração de build | [Marketing] Execução de campanhas de comunicação |
| [Deploy] Preparação para implantação | [Esporte] Operação diária da equipe esportiva |
| [Documentação] Documentação dos procedimentos técnicos | [Esporte] Definição dos critérios esportivos de avaliação |
| [Qualidade] Padronização das convenções de código | [Negócio] Captação de patrocínios e parcerias comerciais |
| [Automação] Configuração de verificações automáticas | [Gestão] Logística de viagens e hospedagem da equipe |
| [Segurança] Mecanismos de backup e recuperação do projeto | [Suporte] Atendimento e suporte final aos usuários do aplicativo |

Você tem toda a razão. Eu cometi o erro de manter a regra da sua primeira mensagem (onde pediu uma matriz) na segunda resposta, o que acabou "espremendo" o conteúdo e destruindo os blocos de código.

Aqui está a reescrita **sem usar tabelas**, mantendo integralmente todos os seus exemplos e blocos de código, e aplicando estritamente as regras de governança do arquivo `.markdownlint.jsonc` (como o uso de `***` para separadores, blocos de código com crases triplas e linguagens permitidas explícitas).

```txt
### 3.1 Manter o ambiente reproduzível

As configurações essenciais devem estar versionadas no repositório.
Exemplos:

* `.vscode/`
* `.editorconfig`
* `.eslintrc`
* `.prettierrc`
* `tsconfig.json`
* `.env.example`
* `package.json`
* `README.md`

Um novo ambiente deve poder ser preparado por meio de procedimentos documentados, sem depender da memória do desenvolvedor.

***

### 3.2 Versionar configurações úteis

Devem ser versionadas as configurações que contribuem para a consistência do projeto.
Exemplos:

* formatação;
* extensões recomendadas;
* tarefas;
* depuração;
* convenções do editor;
* regras de lint;
* scripts de testes.

Não devem ser versionados dados pessoais, tokens ou configurações exclusivas da máquina.

***

### 3.3 Automatizar verificações repetitivas

A automação reduz falhas e evita que tarefas importantes sejam esquecidas.
Exemplos:

```bash
npm run dev
npm run build
npm run lint
npm run test
npm run typecheck
npm run format

```

Antes de publicar uma versão, o ideal é executar uma verificação consolidada:

```bash
npm run validate

```

Esse comando pode executar lint, verificação de tipos, testes e build.

---

### 3.4 Usar TypeScript com regras rigorosas

O TypeScript deve ser configurado para identificar problemas antes da execução.
Configurações recomendadas:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}

```

---

### 3.5 Separar configuração de código

Informações que variam entre ambientes não devem ficar fixas no código-fonte.

Exemplo inadequado:

```ts
const apiUrl = "[https://api.producao.com](https://api.producao.com)";

```

Exemplo adequado:

```ts
const apiUrl = import.meta.env.VITE_API_URL;

```

---

### 3.6 Documentar decisões técnicas

Decisões importantes devem ser registradas.
Exemplos:

* escolha do framework;
* escolha do banco de dados;
* estratégia de autenticação;
* política de funcionamento offline;
* estrutura de pastas;
* abordagem de testes;
* estratégia de implantação.

---

### 3.7 Fazer commits pequenos e objetivos

Cada commit deve representar uma alteração compreensível.
Exemplos:

```text
feat: adiciona cadastro de atletas
fix: corrige validação da data de nascimento
test: adiciona testes do formulário de presença
docs: documenta configuração do workspace

```

---

### 3.8 Priorizar simplicidade

Como o desenvolvimento é solo, a arquitetura deve evitar complexidade desnecessária.
Uma solução simples, compreensível e testável tende a ser mais sustentável do que uma arquitetura sofisticada com grande custo de manutenção.


1. Técnicas utilizadas por desenvolvedores solo
4.1 Desenvolvimento orientado a funcionalidades
O projeto pode ser organizado por funcionalidades, em vez de apenas por tipos técnicos.
Exemplo:
src/
├── features/
│   ├── atletas/
│   ├── treinadores/
│   ├── treinos/
│   ├── jogos/
│   ├── presencas/
│   └── avaliacoes/
Cada funcionalidade pode conter:
atletas/
├── components/
├── pages/
├── services/
├── schemas/
├── types/
└── tests/
Essa técnica facilita a localização e manutenção do código.

4.2 Desenvolvimento incremental
As funcionalidades devem ser construídas em partes pequenas.
Exemplo de sequência:
cadastro básico de atletas;
listagem de atletas;
edição;
controle de permissões;
validação;
testes;
funcionamento offline.
4.3 Prototipação rápida
Antes de desenvolver uma funcionalidade completa, pode ser criado um protótipo funcional simples.
Exemplo:
primeiro criar uma tela estática de presença;
depois adicionar estado local;
em seguida integrar com o banco;
por último adicionar sincronização offline.
4.4 Uso de checklists
Checklists reduzem o risco de esquecimento.
Exemplo de checklist para concluir uma funcionalidade:
requisitos atendidos;
interface responsiva;
validação implementada;
tratamento de erros;
controle de acesso;
testes criados;
lint aprovado;
documentação atualizada.
4.5 Timeboxing
O desenvolvedor define períodos limitados para uma atividade.
Exemplo:
até duas horas para investigar um erro;
até um dia para criar um protótipo;
uma sessão específica para testes;
uma sessão semanal para manutenção.
Isso reduz o risco de passar muito tempo em detalhes pouco relevantes.
4.6 Diário técnico
Manter um registro de desenvolvimento ajuda a recuperar contexto.
Exemplo:
2026-07-25

- Criada estrutura inicial do projeto.
- Definido uso de TypeScript.
- Configurado ESLint e Prettier.
- Próximo passo: autenticação de atletas e treinadores.
4.7 Uso de branches curtas
O desenvolvimento solo pode utilizar branches temporárias para mudanças relevantes.
Exemplos:
main
feature/cadastro-atletas
feature/controle-presenca
fix/login-offline
Branches não devem permanecer abertas por longos períodos.
4.8 Automação local antes de automação complexa
Primeiro devem ser automatizadas as tarefas locais essenciais.
Depois podem ser adicionados recursos como integração contínua, testes automáticos remotos e implantação automática.

5. Configurações necessárias
5.1 Configuração do Workspace
Exemplo:
{
  "folders": [
    {
      "name": "CEPRAEA Beach Pro",
      "path": "."
    }
  ],
  "settings": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit"
    },
    "files.exclude": {
      "**/node_modules": true,
      "**/dist": true
    },
    "typescript.tsdk": "node_modules/typescript/lib"
  }
}
5.2 Extensões recomendadas
Arquivo .vscode/extensions.json:
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "eamodio.gitlens",
    "usernamehw.errorlens",
    "editorconfig.editorconfig"
  ]
}
As extensões devem ser recomendadas, mas não obrigatoriamente impostas.
5.3 Configuração de formatação
Exemplo de .prettierrc:
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100
}
5.4 EditorConfig
Exemplo de .editorconfig:
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
5.5 Configuração de tarefas
Exemplo de .vscode/tasks.json:
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Iniciar desenvolvimento",
      "type": "npm",
      "script": "dev",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Validar projeto",
      "type": "npm",
      "script": "validate",
      "problemMatcher": []
    }
  ]
}
5.6 Configuração de depuração
Exemplo de .vscode/launch.json:
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "pwa-chrome",
      "request": "launch",
      "name": "Depurar CEPRAEA Beach Pro",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
5.7 Variáveis de ambiente
Exemplo de .env.example:
VITE_APP_NAME=CEPRAEA Beach Pro
VITE_API_URL=
VITE_PUBLIC_APP_URL=
VITE_ENABLE_OFFLINE=false
O arquivo .env.example pode ser versionado.
O arquivo .env.local deve permanecer fora do repositório.
5.8 Gitignore
Exemplo:
node_modules/
dist/
coverage/
.env
.env.local
*.log
.DS_Store
5.9 Scripts do projeto
Exemplo:
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "validate": "npm run lint && npm run typecheck && npm run test && npm run build"
  }
}
5.10 Configuração básica do PWA
Devem ser configurados:
nome da aplicação;
nome abreviado;
ícones;
cor do tema;
URL inicial;
modo de exibição;
service worker;
estratégia de cache;
política de atualização;
página de indisponibilidade;
comportamento offline.

6. O que fazer
criar o Workspace no início do projeto;
manter configurações essenciais no Git;
usar TypeScript em modo rigoroso;
configurar formatação automática;
configurar lint;
definir scripts padronizados;
criar um .env.example;
separar segredos de configurações públicas;
documentar como instalar e executar o projeto;
testar a aplicação em celular;
verificar o comportamento em conexão lenta;
testar instalação como PWA;
validar o funcionamento offline;
criar testes para regras importantes;
revisar dependências periodicamente;
manter commits pequenos;
criar backups;
utilizar autenticação e autorização;
validar dados no cliente e no servidor;
monitorar erros de produção;
manter o projeto simples.

7. O que não fazer
armazenar senhas ou tokens no repositório;
versionar arquivos .env com dados reais;
depender exclusivamente de extensões do editor;
instalar muitas extensões sem necessidade;
misturar regra de negócio com componentes visuais;
manter toda a aplicação em poucos arquivos grandes;
ignorar mensagens do TypeScript;
desativar regras de lint sem justificativa;
publicar sem executar testes;
confiar apenas em testes manuais;
desenvolver apenas para telas de computador;
assumir que sempre haverá internet;
armazenar dados sensíveis sem proteção;
criar arquitetura complexa prematuramente;
adicionar bibliotecas para resolver problemas simples;
manter código sem documentação mínima;
fazer alterações grandes em um único commit;
trabalhar diretamente na versão de produção;
permitir acesso administrativo apenas com verificações visuais;
utilizar o cache do PWA sem estratégia de atualização;
tratar o service worker como um detalhe secundário.

8. Exemplos de uso real
8.1 Início de uma sessão de desenvolvimento
O desenvolvedor abre:
cepraea-beach-pro.code-workspace
O VS Code carrega:
configurações do projeto;
extensões recomendadas;
atalhos;
tarefas;
depuradores;
estrutura correta de pastas.
Depois, o desenvolvedor executa a tarefa:
Iniciar desenvolvimento
O servidor local é iniciado de forma padronizada.
8.2 Criação do módulo de presença
O desenvolvedor cria:
src/features/presencas/
├── components/
├── pages/
├── services/
├── schemas/
├── types/
└── tests/
Ao salvar um arquivo:
o Prettier formata o código;
o ESLint sinaliza problemas;
o TypeScript identifica inconsistências;
o Error Lens apresenta erros diretamente no editor.
8.3 Depuração de erro no cadastro
Um atleta não consegue concluir o cadastro.
O desenvolvedor:
abre o modo de depuração;
reproduz o erro;
adiciona um breakpoint;
inspeciona os dados enviados;
identifica uma data em formato inválido;
corrige o schema;
cria um teste para evitar regressão.
8.4 Trabalho em ambiente sem internet
Durante um treino na praia, a conexão fica indisponível.
A aplicação:
carrega a interface armazenada em cache;
permite consultar dados previamente sincronizados;
registra presença localmente;
marca a operação como pendente;
sincroniza os dados quando a conexão retorna.
Esse comportamento depende diretamente da configuração correta do PWA.
8.5 Publicação de uma nova versão
Antes da publicação, o desenvolvedor executa:
npm run validate
O processo verifica:
lint;
tipos;
testes;
build.
A publicação só continua quando todas as etapas forem aprovadas.

9. Impacto das configurações no resultado final
9.1 Formatação automática
Impacto positivo:
código visualmente consistente;
revisão mais fácil;
menos discussões sobre estilo;
commits mais limpos.
Sem configuração:
formatação irregular;
alterações desnecessárias;
maior dificuldade de leitura.
9.2 ESLint
Impacto positivo:
identificação antecipada de erros;
redução de código inseguro;
prevenção de padrões inadequados.
Sem configuração:
problemas aparecem apenas durante a execução;
inconsistências se acumulam.
9.3 TypeScript rigoroso
Impacto positivo:
contratos mais claros;
menos erros de valores indefinidos;
refatoração mais segura;
maior previsibilidade.
Sem configuração rigorosa:
erros podem ficar escondidos;
tipos perdem valor;
manutenção se torna mais arriscada.
9.4 Testes automáticos
Impacto positivo:
prevenção de regressões;
maior confiança nas mudanças;
facilidade de evolução.
Sem testes:
cada alteração pode quebrar funcionalidades antigas;
validação depende exclusivamente do desenvolvedor.
9.5 Configuração do PWA
Impacto positivo:
instalação em dispositivos móveis;
melhor desempenho;
uso em condições de conectividade limitada;
experiência próxima de um aplicativo.
Configuração incorreta pode causar:
versões antigas presas em cache;
dados desatualizados;
falhas de instalação;
comportamento inconsistente.
9.6 Variáveis de ambiente
Impacto positivo:
separação entre desenvolvimento e produção;
maior segurança;
implantação mais simples.
Configuração inadequada pode expor:
credenciais;
URLs privadas;
chaves de serviços;
informações internas.
9.7 Workspace padronizado
Impacto positivo:
inicialização rápida;
menor carga mental;
contexto centralizado;
facilidade de retomada do trabalho.
Sem padronização:
comandos ficam dispersos;
configurações se perdem;
erros de ambiente são mais frequentes.

10. Possíveis melhorias
10.1 Integração contínua
Adicionar um fluxo automático que execute:
lint;
testes;
typecheck;
build;
auditoria de dependências.
10.2 Implantação automática
Publicar automaticamente versões aprovadas após integração com a branch principal.
10.3 Ambiente de homologação
Criar um ambiente separado para testes antes da produção.
Exemplo:
Desenvolvimento
Homologação
Produção
10.4 Testes de ponta a ponta
Automatizar fluxos como:
login;
cadastro de atleta;
registro de presença;
criação de treino;
consulta de avaliação.
10.5 Auditoria de acessibilidade
Adicionar verificações para:
contraste;
navegação por teclado;
leitores de tela;
tamanho de elementos interativos;
mensagens de erro.
10.6 Monitoramento de erros
Registrar erros reais da aplicação para identificar falhas que não apareceram durante o desenvolvimento.
10.7 Verificação de desempenho
Avaliar:
tamanho do bundle;
velocidade de carregamento;
uso de cache;
consumo de dados;
desempenho em celulares mais simples.
10.8 Padronização de componentes
Criar uma biblioteca interna de componentes reutilizáveis.
Exemplos:
botão;
campo de formulário;
cartão de atleta;
seletor de treino;
modal;
indicador de conexão;
mensagem de erro.
10.9 Estratégia de sincronização
Definir claramente:
quais dados podem funcionar offline;
como os dados pendentes são armazenados;
quando ocorre a sincronização;
como conflitos são resolvidos;
como o usuário é informado.
10.10 Documentação arquitetural
Criar registros formais para decisões relevantes, conhecidos como Architecture Decision Records.

11. Riscos
11.1 Dependência de uma única pessoa
Como o projeto é desenvolvido individualmente, conhecimento e decisões podem ficar concentrados.
Mitigação:
documentação;
commits claros;
código simples;
automação;
backups.
11.2 Sobrecarga do desenvolvedor
O desenvolvedor solo acumula funções de:
análise;
arquitetura;
programação;
testes;
implantação;
suporte;
documentação.
Mitigação:
priorização;
entregas incrementais;
automação;
redução de escopo;
uso de checklists.
11.3 Complexidade excessiva
O projeto pode adotar tecnologias acima da necessidade real.
Mitigação:
justificar cada dependência;
começar simples;
evitar abstrações prematuras;
revisar a arquitetura periodicamente.
11.4 Vazamento de dados
Dados de atletas podem incluir informações pessoais.
Riscos:
exposição acidental;
acesso indevido;
armazenamento inseguro;
logs contendo dados sensíveis.
Mitigação:
controle de acesso;
criptografia;
políticas de retenção;
minimização de dados;
revisão de logs.
11.5 Falhas de sincronização offline
Operações feitas sem internet podem entrar em conflito.
Exemplo:
treinador altera uma presença;
outro dispositivo altera o mesmo registro;
ambos sincronizam depois.
Mitigação:
identificação de versão;
registro de data e hora;
regras de resolução;
confirmação do usuário em conflitos relevantes.
11.6 Cache desatualizado
O service worker pode manter arquivos antigos.
Mitigação:
versionamento do cache;
estratégia de atualização;
aviso de nova versão;
limpeza de caches antigos.
11.7 Dependência de bibliotecas
Bibliotecas podem ser abandonadas, apresentar vulnerabilidades ou introduzir alterações incompatíveis.
Mitigação:
manter poucas dependências;
revisar atualizações;
fixar versões quando necessário;
executar auditorias.
11.8 Falta de testes em dispositivos reais
A aplicação pode funcionar no computador e falhar em celulares.
Mitigação:
testar em diferentes tamanhos de tela;
testar navegadores móveis;
testar conexão lenta;
testar instalação;
testar modo offline.
11.9 Perda do repositório ou do ambiente local
Mitigação:
repositório remoto;
backups periódicos;
documentação de recuperação;
variáveis protegidas fora do repositório.

12. Limites
12.1 Limites do VS Code
O VS Code organiza e apoia o desenvolvimento, mas não garante sozinho:
qualidade do código;
segurança;
bom desempenho;
funcionamento offline;
cobertura de testes;
conformidade legal.
Esses resultados dependem das práticas adotadas.
12.2 Limites do PWA
Uma PWA pode apresentar diferenças entre navegadores e sistemas operacionais.
Alguns recursos podem ter suporte limitado, principalmente:
notificações;
execução em segundo plano;
integração com hardware;
sincronização periódica;
armazenamento local.
12.3 Limites do funcionamento offline
Nem todas as funcionalidades precisam ou podem funcionar sem internet.
Operações que dependem de dados atualizados, autenticação remota ou processamento externo podem exigir conexão.
12.4 Limites de segurança no cliente
Nenhuma informação secreta deve ser considerada protegida dentro do código do navegador.
Variáveis incluídas no build do front-end podem ser inspecionadas pelos usuários.
Chaves privadas e operações sensíveis devem permanecer no servidor.
12.5 Limites do desenvolvimento solo
A capacidade de entrega será limitada por:
tempo disponível;
conhecimento técnico;
quantidade de funcionalidades;
manutenção;
suporte;
testes;
operação.
O escopo deve ser ajustado à capacidade real de uma única pessoa.
12.6 Limites da automação
Automação reduz erros, mas não substitui:
revisão crítica;
testes manuais;
validação com usuários;
análise de segurança;
decisões de produto.

13. Critérios de conclusão do domínio
O ambiente de desenvolvimento pode ser considerado inicialmente estabelecido quando:
o Workspace estiver criado;
o repositório Git estiver configurado;
a estrutura inicial estiver definida;
o projeto puder ser executado localmente;
o lint estiver funcionando;
a formatação automática estiver ativa;
o TypeScript estiver configurado;
as variáveis de ambiente estiverem documentadas;
os testes puderem ser executados;
a depuração estiver disponível;
o build de produção for concluído;
a configuração básica do PWA estiver implementada;
o processo estiver documentado no README.

14. Declaração final
O ambiente de desenvolvimento do CEPRAEA Beach Pro deve funcionar como uma base técnica simples, segura, automatizada e reproduzível para o desenvolvimento solo da aplicação.
Seu principal papel é reduzir erros, preservar conhecimento, facilitar a manutenção e garantir que o PWA possa evoluir sem que o aumento de funcionalidades torne o projeto desorganizado ou inviável para um único desenvolvedor.
15. Especificação prática do Workspace

15.1 Premissas técnicas

Esta especificação adota, como linha de base inicial:

• Visual Studio Code como ambiente de desenvolvimento;
• Node.js em versão LTS;
• npm como gerenciador de pacotes;
• Vite como servidor de desenvolvimento e ferramenta de build;
• TypeScript para tipagem estática;
• ESLint para análise do código;
• Prettier para formatação;
• Vitest para testes automatizados;
• Chrome ou Microsoft Edge para depuração;
• porta local 5173 para o servidor Vite.

Caso uma dessas decisões seja alterada, os arquivos desta seção deverão ser revisados de forma coordenada.

15.2 Estrutura de arquivos

Os arquivos devem ser organizados desta forma:

cepraea-beach-pro/
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── src/
├── public/
├── tests/
├── cepraea-beach-pro.code-workspace
├── package.json
└── README.md

Os cinco arquivos desta especificação devem ser versionados no Git. Configurações pessoais, caminhos absolutos, senhas, tokens e dados exclusivos da máquina não devem ser incluídos neles.

15.3 Arquivo cepraea-beach-pro.code-workspace

Finalidade: funcionar como ponto de entrada oficial do projeto no VS Code, concentrando a pasta principal, configurações compartilhadas e recomendações de extensões.

Localização:

cepraea-beach-pro/cepraea-beach-pro.code-workspace

Conteúdo:

{
  "folders": [
    {
      "name": "CEPRAEA Beach Pro",
      "path": "."
    }
  ],
  "settings": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit",
      "source.organizeImports": "explicit"
    },
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.rulers": [100],
    "files.eol": "\n",
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "typescript.tsdk": "node_modules/typescript/lib",
    "typescript.enablePromptUseWorkspaceTsdk": true
  },
  "extensions": {
    "recommendations": [
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "editorconfig.editorconfig",
      "usernamehw.errorlens",
      "eamodio.gitlens",
      "ms-playwright.playwright"
    ]
  }
}

Regras de uso:

• abrir preferencialmente o arquivo .code-workspace, e não somente a pasta;
• manter caminhos relativos;
• não incluir caminhos do Windows, Linux ou macOS específicos da máquina;
• não duplicar excessivamente as configurações existentes em .vscode/settings.json;
• usar este arquivo como ponto de entrada, enquanto settings.json permanece como fonte detalhada das configurações do projeto.

15.4 Arquivo .vscode/settings.json

Finalidade: padronizar formatação, correções automáticas, TypeScript, pesquisa, arquivos observados e comportamento do editor para o projeto.

Localização:

cepraea-beach-pro/.vscode/settings.json

Conteúdo:

{
  "editor.formatOnSave": true,
  "editor.formatOnPaste": false,
  "editor.formatOnType": false,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.rulers": [100],
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,
  "files.encoding": "utf8",
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.trimTrailingWhitespace": true,
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/coverage": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/coverage": true,
    "**/*.lock": true
  },
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/coverage/**": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "typescript.preferences.importModuleSpecifier": "non-relative",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "javascript.updateImportsOnFileMove.enabled": "always",
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "npm.packageManager": "npm",
  "npm.enableRunFromFolder": true,
  "debug.javascript.autoAttachFilter": "smart",
  "terminal.integrated.cwd": "${workspaceFolder}",
  "workbench.startupEditor": "none",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "files.trimTrailingWhitespace": false
  }
}

Decisões importantes:

• formatOnSave garante formatação consistente ao salvar;
• fixAll.eslint aplica correções seguras oferecidas pelo ESLint;
• organizeImports remove e reorganiza imports quando houver suporte;
• files.watcherExclude reduz consumo de CPU e memória;
• typescript.tsdk força o uso da versão de TypeScript instalada no projeto;
• caminhos absolutos e preferências visuais pessoais não devem ser adicionados.

Observação: typescript.preferences.importModuleSpecifier está definido como non-relative. Essa configuração pressupõe que o projeto terá aliases configurados no tsconfig.json e no Vite. Enquanto os aliases não existirem, alterar temporariamente para shortest.

15.5 Arquivo .vscode/extensions.json

Finalidade: recomendar apenas extensões diretamente úteis ao projeto e evitar dependência excessiva do editor.

Localização:

cepraea-beach-pro/.vscode/extensions.json

Conteúdo:

{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "editorconfig.editorconfig",
    "usernamehw.errorlens",
    "eamodio.gitlens",
    "ms-playwright.playwright"
  ]
}

Responsabilidade de cada extensão:

• ESLint: apresenta violações das regras de qualidade e segurança;
• Prettier: formata o código de maneira uniforme;
• EditorConfig: preserva charset, indentação e finais de linha;
• Error Lens: exibe erros e avisos diretamente nas linhas afetadas;
• GitLens: facilita análise de histórico, autoria e alterações;
• Playwright: apoia testes de ponta a ponta e depuração de cenários reais.

Regras:

• não recomendar extensões sem uso comprovado;
• revisar a lista quando a stack for alterada;
• não incluir extensões de tema, ícones ou preferências pessoais;
• não tratar extensões como substitutas das dependências e scripts do projeto;
• adicionar extensões específicas de framework somente após a escolha formal do framework.

15.6 Arquivo .vscode/tasks.json

Finalidade: disponibilizar comandos padronizados para instalar, executar, testar, validar e gerar o build do projeto sem depender da memorização de comandos.

Localização:

cepraea-beach-pro/.vscode/tasks.json

Conteúdo:

{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "CEPRAEA: instalar dependências",
      "type": "npm",
      "script": "install",
      "problemMatcher": []
    },
    {
      "label": "CEPRAEA: iniciar desenvolvimento",
      "type": "npm",
      "script": "dev",
      "isBackground": true,
      "presentation": {
        "reveal": "always",
        "panel": "dedicated",
        "clear": true
      },
      "problemMatcher": {
        "owner": "vite",
        "pattern": {
          "regexp": "^$"
        },
        "background": {
          "activeOnStart": true,
          "beginsPattern": ".*",
          "endsPattern": "Local:.*http://localhost:5173"
        }
      }
    },
    {
      "label": "CEPRAEA: lint",
      "type": "npm",
      "script": "lint",
      "group": "test",
      "problemMatcher": ["$eslint-stylish"]
    },
    {
      "label": "CEPRAEA: verificar tipos",
      "type": "npm",
      "script": "typecheck",
      "group": "test",
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "CEPRAEA: executar testes",
      "type": "npm",
      "script": "test",
      "group": "test",
      "problemMatcher": []
    },
    {
      "label": "CEPRAEA: build de produção",
      "type": "npm",
      "script": "build",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "CEPRAEA: visualizar build",
      "type": "npm",
      "script": "preview",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "CEPRAEA: validar projeto",
      "dependsOrder": "sequence",
      "dependsOn": [
        "CEPRAEA: lint",
        "CEPRAEA: verificar tipos",
        "CEPRAEA: executar testes",
        "CEPRAEA: build de produção"
      ],
      "problemMatcher": []
    }
  ]
}

Scripts exigidos no package.json:

{
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 5173",
    "build": "tsc -b && vite build",
    "preview": "vite preview --host 0.0.0.0 --port 4173",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "validate": "npm run lint && npm run typecheck && npm run test && npm run build"
  }
}

Nota sobre instalação: uma tarefa npm do tipo install pode não ser reconhecida como script em todas as versões do VS Code. Caso isso ocorra, substituir somente essa tarefa por:

{
  "label": "CEPRAEA: instalar dependências",
  "type": "shell",
  "command": "npm install",
  "problemMatcher": []
}

A opção --host 0.0.0.0 permite testar a aplicação em um celular conectado à mesma rede local. O firewall do computador deve permitir a conexão apenas em redes confiáveis.

15.7 Arquivo .vscode/launch.json

Finalidade: iniciar a aplicação e conectar o depurador do VS Code ao navegador com source maps e breakpoints no código TypeScript.

Localização:

cepraea-beach-pro/.vscode/launch.json

Conteúdo:

{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "CEPRAEA: depurar no Chrome",
      "type": "pwa-chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src",
      "sourceMaps": true,
      "preLaunchTask": "CEPRAEA: iniciar desenvolvimento",
      "skipFiles": [
        "<node_internals>/**",
        "**/node_modules/**"
      ]
    },
    {
      "name": "CEPRAEA: depurar no Edge",
      "type": "pwa-msedge",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src",
      "sourceMaps": true,
      "preLaunchTask": "CEPRAEA: iniciar desenvolvimento",
      "skipFiles": [
        "<node_internals>/**",
        "**/node_modules/**"
      ]
    },
    {
      "name": "CEPRAEA: anexar ao Chrome",
      "type": "pwa-chrome",
      "request": "attach",
      "port": 9222,
      "webRoot": "${workspaceFolder}/src",
      "sourceMaps": true
    }
  ],
  "compounds": [
    {
      "name": "CEPRAEA: desenvolvimento completo",
      "configurations": [
        "CEPRAEA: depurar no Chrome"
      ],
      "stopAll": true
    }
  ]
}

Uso recomendado:

1. abrir cepraea-beach-pro.code-workspace;
2. instalar as extensões recomendadas;
3. executar CEPRAEA: instalar dependências;
4. abrir a área Executar e Depurar;
5. selecionar CEPRAEA: depurar no Chrome;
6. inserir breakpoints em arquivos dentro de src;
7. iniciar a depuração;
8. confirmar que o navegador abriu http://localhost:5173;
9. verificar se o breakpoint é atingido.

Para usar a configuração de anexação, iniciar o Chrome com depuração remota na porta 9222. Essa configuração é opcional e não deve ser usada como fluxo principal.

15.8 Compatibilidade entre os arquivos

As seguintes relações devem permanecer consistentes:

• a porta de tasks.json deve ser igual à URL de launch.json;
• o script dev deve existir no package.json;
• o diretório webRoot deve apontar para o local do código-fonte;
• as extensões usadas como formatador ou linter devem aparecer em extensions.json;
• o TypeScript local deve estar instalado em node_modules;
• o arquivo .code-workspace deve apontar para a raiz correta;
• os aliases usados pelo editor devem coincidir com tsconfig.json e vite.config.ts;
• os nomes das tarefas referenciadas em preLaunchTask devem ser idênticos.

15.9 Procedimento de implantação local da especificação

1. criar a pasta .vscode na raiz do projeto;
2. criar os cinco arquivos com os conteúdos desta seção;
3. confirmar que package.json contém os scripts exigidos;
4. executar npm install;
5. abrir cepraea-beach-pro.code-workspace;
6. aceitar a instalação das extensões recomendadas;
7. executar a tarefa CEPRAEA: validar projeto;
8. corrigir todos os erros apresentados;
9. iniciar a configuração CEPRAEA: depurar no Chrome;
10. testar a aplicação no computador;
11. testar pelo endereço IP local em um celular da mesma rede;
12. versionar os arquivos em um commit específico.

Exemplo de commit:

chore: configura workspace de desenvolvimento do CEPRAEA Beach Pro

15.10 Critérios de aceitação

A especificação estará corretamente implantada quando:

• o Workspace abrir sem referências a caminhos inexistentes;
• as extensões forem sugeridas pelo VS Code;
• o código for formatado ao salvar;
• problemas do ESLint aparecerem no editor;
• o TypeScript local for utilizado;
• npm run dev iniciar o sistema na porta 5173;
• a tarefa de validação executar lint, tipos, testes e build;
• a depuração abrir o navegador e respeitar breakpoints;
• o celular conseguir acessar o servidor pela rede local, quando autorizado;
• node_modules, dist e coverage não sobrecarregarem pesquisa e observação de arquivos;
• nenhuma credencial ou configuração pessoal estiver versionada.

15.11 Limites e ajustes futuros

Esta é uma especificação inicial. Ela deverá ser adaptada quando forem formalmente definidos:

• o framework de interface;
• a biblioteca de testes de componentes;
• a solução de banco de dados;
• o provedor de autenticação;
• a plataforma de hospedagem;
• a estratégia de PWA e service worker;
• o padrão de aliases;
• a integração contínua;
• os navegadores oficialmente suportados.

Toda mudança deve preservar simplicidade, portabilidade, segurança e facilidade de manutenção por um desenvolvedor solo.

16. Ambiente real da máquina de desenvolvimento

16.1 Inventário técnico sanitizado

O ambiente real utilizado para o desenvolvimento do CEPRAEA Beach Pro é composto por:

• Equipamento: Acer Nitro 5 AN515-57;
• arquitetura: x64;
• processador: Intel Core i7-11800H, com 8 núcleos e 16 processadores lógicos no Windows;
• memória física: 8 GB DDR4 3200 MHz;
• armazenamento: SSD NVMe de aproximadamente 512 GB;
• sistema operacional: Windows 11 Home Single Language, build 26200;
• idioma: Português do Brasil;
• fuso horário: UTC−03:00 — Brasília;
• firmware: UEFI;
• virtualização: ativa;
• WSL: versão 2.6.1.0;
• distribuição Linux: Ubuntu 24.04.3 LTS;
• kernel WSL: Linux 6.6.87.2;
• processadores disponibilizados ao WSL: 4 processadores lógicos;
• Git: 2.43.0;
• GitHub CLI: 2.67.0;
• Node.js: 24.14.1;
• npm: 11.11.0;
• Python: 3.12.3;
• uv: 0.11.28;
• FFmpeg: 6.1.1;
• Docker Desktop: presente no Windows, mas ainda não acessível na distribuição Ubuntu;
• SQLite CLI: não instalado;
• navegador para depuração: Chrome ou Microsoft Edge no Windows;
• rede local: disponível para testes em dispositivos móveis.

Informações pessoais e identificadores exclusivos da máquina, como e-mail, número de série, Product ID, nome de usuário, nome do computador e endereço IP, não devem ser registrados no repositório nem em versões públicas deste manual.

16.2 Avaliação de capacidade

O processador é suficiente para executar VS Code, Vite, TypeScript, ESLint, Vitest, Playwright, Git, navegador, build e serviços locais leves. CPU e GPU não são bloqueadores para o desenvolvimento do PWA.

A memória física de 8 GB é um limite importante. O desenvolvimento deve evitar a execução simultânea de Docker Desktop, vários navegadores, máquinas virtuais, ferramentas pesadas e múltiplos servidores. Testes de ponta a ponta devem ser executados sob demanda. A ampliação para 16 GB de RAM é a melhoria de hardware com maior impacto esperado.

16.3 Bloqueador de armazenamento

Estado verificado em 2026-07-25 (Configurações do Windows → Armazenamento):

• Capacidade: 475 GB
• Utilizado: 439 GB (92%)
• Livre: 36,2 GB

Distribuição do uso:
• Aplicativos instalados: 302 GB
• Sistema e reservado: 56,8 GB
• Outros: 52,3 GB
• Área de Trabalho: 12,3 GB
• Vídeos: 6,83 GB
• Documentos: 6,28 GB
• Arquivos temporários: 918 MB
• Imagens: 643 MB

O mínimo de 30 GB exigido foi atingido (36,2 GB disponíveis). A meta preferencial de 50 GB ainda não foi atingida.

Esse estado deixa de ser um bloqueador formal, mas o espaço disponível é apertado. Operações simultâneas pesadas (npm install, build, WSL swap, atualizações do Windows) podem pressionar o disco. As principais oportunidades de liberação estão em Aplicativos instalados (302 GB) e Área de Trabalho (12,3 GB).

Ação recomendada para maior conforto operacional:

• liberar preferencialmente 50 GB ou mais na unidade C:;
• manter preferencialmente 50 GB ou mais livres;
• revisar Downloads, Lixeira, arquivos temporários, caches, node_modules antigos, imagens e volumes Docker, instaladores, vídeos, distribuições WSL sem uso e arquivos duplicados;
• não excluir diretórios automaticamente sem confirmar sua finalidade.

Passo a passo para liberar espaço no Windows:

1. Abrir Configurações → Sistema → Armazenamento;
1. Clicar em "Arquivos temporários", marcar todos os itens listados e clicar em "Remover arquivos";
1. Clicar em "Aplicativos e recursos" e desinstalar programas que não são mais utilizados;
1. Abrir a pasta Área de Trabalho (identificada com 12,3 GB) e mover ou excluir arquivos grandes;
1. Esvaziar a Lixeira;
1. Limpar a pasta Downloads de instaladores e arquivos antigos;
1. Após as limpezas, confirmar o resultado no PowerShell:

```powershell
Get-Volume -DriveLetter C
```

Saída esperada: campo "SizeRemaining" com valor próximo ou acima de 50 GB.

Ordem de prioridade para liberação (baseada no estado verificado em 2026-07-25):

| Categoria | Tamanho | Ação recomendada |
| --- | --- | --- |
| Aplicativos instalados | 302 GB | Desinstalar os não utilizados |
| Área de Trabalho | 12,3 GB | Mover para pasta de documentos ou excluir |
| Vídeos | 6,83 GB | Mover para armazenamento externo |
| Documentos | 6,28 GB | Avaliar e compactar se necessário |
| Arquivos temporários | 918 MB | Remover via Storage Sense |

Comando de verificação no PowerShell:

Get-Volume -DriveLetter C

O fato de o Ubuntu indicar grande espaço disponível em seu disco virtual não reduz a pressão sobre o disco Windows, porque o arquivo do disco virtual do WSL está armazenado fisicamente no SSD da unidade C:.

16.4 Estratégia oficial de desenvolvimento

A estratégia oficial recomendada é:

• Windows 11 como sistema hospedeiro;
• Visual Studio Code instalado no Windows;
• extensão oficial WSL do VS Code;
• Ubuntu 24.04 como ambiente de terminal, Git, Node.js, npm, testes e build;
• Chrome ou Edge no Windows para depuração;
• projeto armazenado no sistema de arquivos Linux.

Local oficial recomendado:

/home/<usuario-linux>/projetos/cepraea-beach-pro

Não é recomendado armazenar o projeto em /mnt/c/Users/... para o fluxo principal, pois projetos Node.js nesse local podem apresentar pior desempenho de entrada e saída, observação de arquivos mais lenta, diferenças de permissões e maior risco de inconsistências de final de linha.

O projeto deve ser aberto a partir do Ubuntu com:

cd ~/projetos/cepraea-beach-pro
code cepraea-beach-pro.code-workspace

A barra inferior do VS Code deve indicar que a janela está conectada ao WSL Ubuntu.

16.5 Limites recomendados para o WSL

Com 8 GB de memória física, o WSL não deve utilizar praticamente toda a memória da máquina. Criar ou revisar o arquivo:

C:\Users\<usuario>\.wslconfig

Conteúdo inicial recomendado:

[wsl2]
memory=4GB
processors=4
swap=4GB
localhostForwarding=true

Depois de salvar, executar no PowerShell:

wsl --shutdown

Ao abrir novamente o Ubuntu, validar:

free -h
nproc

O resultado esperado é aproximadamente 4 GB de memória máxima, 4 processadores lógicos e swap disponível. Esses valores devem ser revistos após observação do consumo real.

16.6 Node.js e npm

O ambiente atualmente possui Node.js 24.14.1 e npm 11.11.0. Essas versões são o inventário observado, mas somente se tornam versões oficiais do projeto após confirmação de compatibilidade com a stack escolhida.

Ações obrigatórias:

• utilizar um gerenciador de versões do Node no Ubuntu;
• criar .nvmrc ou arquivo equivalente;
• declarar engines no package.json;
• declarar packageManager no package.json;
• versionar package-lock.json;
• utilizar npm ci quando o lockfile existir e não houver intenção de alterar dependências;
• utilizar npm install somente para adicionar, remover ou atualizar dependências.

Exemplo provisório:

.nvmrc
24.14.1

package.json
{
  "engines": {
    "node": "24.14.1",
    "npm": "11.11.0"
  },
  "packageManager": "npm@11.11.0"
}

Validar no Ubuntu:

node --version
npm --version
which node
which npm

Os caminhos devem apontar para instalações Linux, e não para executáveis montados do Windows.

16.7 Git e GitHub

Git e GitHub CLI já estão disponíveis no Ubuntu. O Git do Windows e o Git do WSL são ambientes separados; portanto, identidade e autenticação devem ser confirmadas dentro do Ubuntu.

Verificações:

git config --global user.name
git config --global user.email
git config --global init.defaultBranch
git config --global core.autocrlf
gh auth status

Configuração recomendada no Ubuntu:

```bash
git config --global init.defaultBranch main
git config --global core.autocrlf input
git config --global core.eol lf
git config --global pull.rebase false
git config --global fetch.prune true
```

Explicação de cada parâmetro:

| Parâmetro | Valor | Motivo |
| --- | --- | --- |
| init.defaultBranch | main | Cria repositórios com branch principal chamada "main" em vez do padrão antigo "master" |
| core.autocrlf | input | Aceita LF e CRLF ao adicionar arquivos ao stage, mas nunca converte LF para CRLF; garante que commits do Linux não introduzam CRLF |
| core.eol | lf | Define LF como final de linha ao fazer checkout; mantém consistência com o EditorConfig e o ambiente Linux |
| pull.rebase | false | Usa merge ao executar git pull em vez de rebase; preserva o histórico linear e evita conflitos silenciosos de reescrita |
| fetch.prune | true | Remove automaticamente referências locais de branches remotas que foram deletadas; mantém a lista de branches limpa |

Configuração de identidade (requer decisão do proprietário do repositório):

```bash
git config --global user.name "<nome-do-desenvolvedor>"
git config --global user.email "<email-vinculado-ao-github>"
```

O nome e o e-mail são vinculados a cada commit e devem corresponder à conta do GitHub. Não devem ser fixados neste manual.

Verificação completa:

```bash
git config --global --list
```

Confirmar que todas as chaves aparecem com os valores corretos.

Nome e e-mail devem ser definidos pelo proprietário do repositório e não devem ser fixados neste manual.

16.8 Docker, SQLite e GPU

Docker não deve ser obrigatório no ambiente inicial. Ele só deve ser introduzido quando existir necessidade concreta, como banco local isolado, backend local ou testes de integração. Caso seja adotado, habilitar a integração do Docker Desktop com a distribuição Ubuntu e validar:

docker version
docker compose version
docker run --rm hello-world

Não instalar uma segunda implementação independente do Docker no Ubuntu sem decisão arquitetural explícita.

O cliente sqlite3 não está instalado e não é um bloqueio enquanto SQLite não fizer parte da arquitetura. Não instalar ferramentas sem finalidade definida.

A ausência de nvidia-smi no Ubuntu não bloqueia o desenvolvimento web. A GPU dedicada não é necessária para Vite, TypeScript, testes, build ou PWA. Não instalar pacotes NVIDIA apenas para eliminar essa mensagem.

16.9 Ordem obrigatória de preparação

1. sanitizar qualquer inventário antes de adicioná-lo à documentação;
2. liberar pelo menos 30 GB na unidade C:;
3. configurar os limites do WSL;
4. reiniciar o WSL;
5. confirmar VS Code e extensão WSL;
6. criar o diretório ~/projetos no Ubuntu;
7. confirmar Git, GitHub CLI, Node.js e npm dentro do Ubuntu;
8. configurar identidade e autenticação do Git;
9. definir e fixar as versões oficiais do Node.js e npm;
10. criar o projeto no sistema de arquivos Linux;
11. abrir o arquivo .code-workspace em uma janela WSL;
12. executar npm ci ou npm install conforme o estado do projeto;
13. validar lint, tipos, testes e build;
14. validar depuração no navegador;
15. validar acesso por celular na mesma rede local;
16. somente depois avaliar a necessidade de Docker.

16.10 Critérios de prontidão da máquina

O computador será considerado preparado quando:

• houver pelo menos 30 GB livres na unidade C:;
• o WSL estiver limitado e iniciar sem consumo excessivo;
• o Ubuntu estiver funcional;
• o VS Code abrir conectado ao WSL;
• o projeto estiver dentro de /home/<usuario-linux>/projetos;
• Git e GitHub CLI estiverem configurados e autenticados;
• Node.js e npm forem carregados pelo Ubuntu;
• as versões estiverem fixadas no projeto;
• package-lock.json estiver versionado;
• npm ci funcionar em uma instalação limpa;
• o servidor Vite iniciar na porta configurada;
• o navegador do Windows acessar localhost;
• um celular autorizado acessar o servidor pela rede local;
• lint, verificação de tipos, testes e build forem concluídos;
• nenhuma informação pessoal ou credencial estiver versionada.

16.11 Decisão consolidada sobre a máquina

O equipamento possui capacidade de processamento suficiente para desenvolver o CEPRAEA Beach Pro. Os principais limites são o armazenamento quase esgotado e a memória física de 8 GB. O desenvolvimento deve ocorrer com VS Code no Windows conectado ao Ubuntu pelo WSL 2, mantendo o código no sistema de arquivos Linux e Docker fora do ambiente mínimo inicial.

Nenhuma instalação adicional relevante deve ser iniciada antes da liberação de espaço na unidade C:.

17. Execução das ações identificadas

17.1 Limite de execução

As ações documentais foram executadas diretamente neste manual. As ações que alteram o computador dependem de execução local pelo proprietário, pois o Google Drive e o assistente não possuem acesso remoto ao Windows, ao WSL, ao sistema de arquivos, ao VS Code ou às credenciais da máquina.

17.2 Estado das ações

CONCLUÍDO — inventário técnico sanitizado e incorporado ao manual.
CONCLUÍDO — estratégia oficial definida: Windows 11 como hospedeiro, VS Code no Windows e execução no Ubuntu pelo WSL 2.
CONCLUÍDO — local oficial recomendado para o projeto: ~/projetos/cepraea-beach-pro.
CONCLUÍDO — Node.js 24.14.1 e npm 11.11.0 registrados como versões instaladas, ainda pendentes de validação como versões oficiais da stack.
CONCLUÍDO — Docker removido do ambiente mínimo obrigatório.
CONCLUÍDO — critérios de prontidão e proteção de dados pessoais definidos.
CONCLUÍDO (mínimo) — 36,2 GB livres em C: verificado em 2026-07-25. Mínimo de 30 GB atingido. Meta preferencial de 50 GB ainda não atingida — recomendado liberar mais espaço, especialmente de Aplicativos instalados (302 GB) e Área de Trabalho (12,3 GB).
PENDENTE LOCAL — limitar recursos do WSL.
PENDENTE LOCAL — confirmar VS Code e extensão WSL.
PENDENTE LOCAL — configurar identidade e autenticação Git no Ubuntu.
PENDENTE LOCAL — criar a pasta oficial do projeto.
PENDENTE LOCAL — criar ou clonar o repositório.
PENDENTE LOCAL — criar os arquivos reais do Workspace.
PENDENTE LOCAL — executar instalação, validação, build, depuração e teste móvel.

17.3 Procedimento obrigatório no Windows

Antes de instalar dependências, executar no PowerShell:

Get-Volume -DriveLetter C
wsl --shutdown

Criar ou editar C:\Users\<usuario>\.wslconfig com:

[wsl2]
memory=4GB
processors=4
swap=4GB
localhostForwarding=true

Como criar ou editar o arquivo .wslconfig no Windows:

Opção A — usando o Bloco de Notas pelo PowerShell:

```powershell
notepad $env:USERPROFILE\.wslconfig
```

Opção B — usando o VS Code instalado no Windows (fora do WSL):

```powershell
code $env:USERPROFILE\.wslconfig
```

Se o arquivo não existir, o editor o criará automaticamente ao salvar. Colar o conteúdo abaixo e salvar o arquivo:

```ini
[wsl2]
memory=4GB
processors=4
swap=4GB
localhostForwarding=true
```

Explicação de cada parâmetro:

• memory=4GB — limita o uso de memória RAM do WSL a 4 GB, evitando que o Ubuntu consuma toda a memória física da máquina (8 GB);
• processors=4 — limita os processadores lógicos disponíveis ao WSL (a máquina tem 16, mas 4 são suficientes para desenvolvimento);
• swap=4GB — define o arquivo de swap do WSL em 4 GB para aliviar a pressão quando a RAM estiver próxima do limite;
• localhostForwarding=true — permite que o Windows acesse portas abertas no Ubuntu via localhost (necessário para o navegador acessar o servidor Vite).

Depois executar:

```powershell
wsl --shutdown
wsl --status
wsl --list --verbose
```

Verificação após reiniciar o Ubuntu:

```bash
free -h
nproc
```

O campo "total" de memória deve exibir aproximadamente 4 GB e o número de processadores deve ser 4.

Critério de aprovação: unidade C: com no mínimo 30 GB livres e Ubuntu executando em WSL 2.

17.4 Procedimento obrigatório no Ubuntu

Executar:

mkdir -p ~/projetos
cd ~/projetos
git --version
gh --version
node --version
npm --version
which git
which node
which npm
free -h
nproc
df -h

Configurar parâmetros globais do Git (podem ser executados pelo agente):

```bash
git config --global init.defaultBranch main
git config --global core.autocrlf input
git config --global core.eol lf
git config --global pull.rebase false
git config --global fetch.prune true
```

Configurar identidade (requer informação do proprietário — não executar sem confirmar os valores):

```bash
git config --global user.name "<nome-do-desenvolvedor>"
git config --global user.email "<email-do-git>"
```

Verificar a configuração completa:

```bash
git config --global --list
```

Verificar autenticação no GitHub CLI:

```bash
gh auth status
```

Saída esperada: "Logged in to github.com as <usuario>" com protocolo SSH.

Caso ainda não esteja autenticado:

```bash
gh auth login
```

O processo interativo solicitará: plataforma (GitHub.com), protocolo (SSH recomendado), geração de chave SSH (se necessário) e autenticação via navegador. Seguir as instruções exibidas no terminal.

17.5 Preparação do diretório do projeto

Para um projeto novo:

cd ~/projetos
mkdir cepraea-beach-pro
cd cepraea-beach-pro
git init

Para um repositório existente:

cd ~/projetos
gh repo clone <organizacao-ou-usuario>/<repositorio> cepraea-beach-pro
cd cepraea-beach-pro

O projeto não deve ser criado em /mnt/c.

17.6 Arquivos de controle de versão do ambiente

Após a validação definitiva da compatibilidade da stack, criar .nvmrc com a versão oficial do Node.js e registrar no package.json:

{
  "engines": {
    "node": "24.14.1",
    "npm": "11.11.0"
  },
  "packageManager": "npm@11.11.0"
}

Esses valores permanecem provisórios até a escolha formal do framework e a confirmação de compatibilidade de todas as dependências.

17.7 Abertura no VS Code e verificação da extensão WSL

Esta seção cobre dois momentos: (1) verificar que a extensão WSL está instalada no VS Code do Windows, e (2) abrir o projeto corretamente a partir do Ubuntu.

Parte 1 — Verificar a extensão WSL no VS Code (Windows):

1. Abrir o VS Code no Windows;
1. Abrir o painel de extensões com Ctrl+Shift+X;
1. Pesquisar por "WSL";
1. Localizar a extensão "WSL" publicada pela Microsoft (ID: ms-vscode-remote.remote-wsl);
1. Se não estiver instalada, clicar em "Install";
1. Aguardar a instalação e, se solicitado, reiniciar o VS Code.

Parte 2 — Abrir o projeto a partir do Ubuntu:

```bash
cd ~/projetos/cepraea-beach-pro
code cepraea-beach-pro.code-workspace
```

O VS Code abrirá uma janela conectada ao WSL Ubuntu. Confirmar o status de conexão:

• A barra inferior esquerda do VS Code deve exibir "><WSL: Ubuntu" em azul;
• Caso exiba somente o ícone "><" sem texto, clicar nele e selecionar "Reopen Folder in WSL".

Parte 3 — Instalar extensões recomendadas no ambiente WSL:

1. No VS Code conectado ao WSL, abrir o painel de extensões com Ctrl+Shift+X;
1. Clicar na aba "Recommended" (ou pesquisar "@recommended");
1. Instalar as extensões listadas no arquivo .vscode/extensions.json:
   - ESLint (dbaeumer.vscode-eslint)
   - Prettier (esbenp.prettier-vscode)
   - EditorConfig (editorconfig.editorconfig)
   - Error Lens (usernamehw.errorlens)
   - GitLens (eamodio.gitlens)
   - Playwright (ms-playwright.playwright)
1. Certificar-se de clicar em "Install in WSL:Ubuntu" e não somente "Install".

Parte 4 — Validar que o ambiente está funcional:

1. Abrir qualquer arquivo .ts dentro de src/;
1. Confirmar que o ESLint mostra o ícone de status na barra inferior sem erros de configuração;
1. Salvar o arquivo e verificar que o Prettier aplicou formatação automática;
1. Confirmar que a versão do TypeScript na barra de status corresponde à instalada no projeto (não à do VS Code).

Critério de aprovação: a barra inferior exibe "WSL: Ubuntu" e o ESLint, o Prettier e o TypeScript operam sem erros de configuração.

17.8 Validação do ambiente

Depois de criar o projeto e os arquivos definidos na seção 15, executar:

npm ci
npm run format:check
npm run lint
npm run typecheck
npm run test
npm run build
npm run dev

Se o projeto ainda não possuir package-lock.json, executar npm install uma única vez para criá-lo, versionar o lockfile e usar npm ci nas instalações seguintes.

17.9 Teste no computador e no celular

O servidor deve iniciar com host 0.0.0.0 e porta 5173. Confirmar no navegador do Windows:

```text
http://localhost:5173
```

Ao iniciar com `--host 0.0.0.0`, o Vite exibe dois endereços no terminal:

```text
  VITE v5.x.x  ready in Xms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.X.X:5173/
```

O endereço "Network" é o que deve ser usado no celular.

Passo a passo para testar no celular:

1. Conectar o celular à mesma rede Wi-Fi do computador de desenvolvimento;
1. No Ubuntu, descobrir o endereço IP da interface de rede:

```bash
ip addr show eth0 | grep "inet "
```

Saída esperada:

```text
    inet 172.X.X.X/20 brd ...
```

O endereço exibido pelo Vite no terminal ("Network:") corresponde a esse IP.

1. No navegador do celular, acessar o endereço exibido pelo Vite:

```text
http://192.168.X.X:5173
```

Substituir pelo endereço real exibido no terminal.

1. Confirmar que a aplicação carrega e responde normalmente.

Requisitos para o teste funcionar:

• o celular e o computador devem estar na mesma rede Wi-Fi;
• o firewall do Windows deve permitir conexões na porta 5173 em redes privadas;
• não autorizar essa abertura em redes públicas (cafeterias, aeroportos, etc.).

Verificação do firewall do Windows (PowerShell):

```powershell
Get-NetFirewallRule -DisplayName "*5173*" | Select-Object DisplayName,Enabled,Direction
```

Se não houver regra, o Windows pode exibir um alerta de firewall ao iniciar o Vite pela primeira vez. Autorizar somente para "Redes privadas".

17.10 Critério de conclusão da execução

A preparação será considerada concluída somente quando:

• houver pelo menos 30 GB livres em C:;
• o WSL estiver limitado e estável;
• o projeto estiver em ~/projetos/cepraea-beach-pro;
• Git e GitHub CLI estiverem configurados no Ubuntu;
• Node.js e npm forem carregados pelo Linux;
• o Workspace abrir conectado ao WSL;
• npm ci, lint, typecheck, testes e build forem aprovados;
• a depuração atingir breakpoints;
• o computador e o celular acessarem a aplicação;
• nenhuma credencial ou informação pessoal estiver versionada.

17.11 Registro de evidências

Após cada ação local, registrar neste manual a data, o comando executado, o resultado e o status. Não registrar senhas, tokens, números de série, Product ID, endereço IP completo ou outras informações pessoais.

2026-07-25
Ação: Verificação de espaço em C: via Configurações do Windows (Sistema → Armazenamento → Acer C: 475 GB).
Resultado: 439 GB usados, 36,2 GB livres (92% de utilização). Distribuição: Aplicativos 302 GB, Sistema 56,8 GB, Outros 52,3 GB, Área de Trabalho 12,3 GB, Vídeos 6,83 GB, Documentos 6,28 GB, Temporários 918 MB, Imagens 643 MB.
Status: CONCLUÍDO (mínimo). Meta preferencial de 50 GB pendente.

17.12 Matriz de responsabilidade das ações

Esta tabela consolida todas as ações necessárias para implantar o ambiente de desenvolvimento, indicando quem executa cada uma, o pré-requisito e onde encontrar as instruções detalhadas.

Legenda:
• A — Agente de IA (executa sem intervenção humana)
• B — Requer decisão ou informação do humano antes de o agente executar
• C — Exclusivamente humano (exige acesso ao Windows ou dispositivo físico)

Ações do grupo A — executadas pelo agente

| # | Ação | Pré-requisito | Seção |
| --- | ------ | -------------- | ------- |
| A1 | Configurar git global (defaultBranch, autocrlf, eol, pull.rebase, fetch.prune) | Ubuntu acessível | §17.4 |
| A2 | Criar diretório ~/projetos/cepraea-beach-pro | Ubuntu acessível | §17.5 |
| A3 | Executar git init | Diretório A2 criado | §17.5 |
| A4 | Criar cepraea-beach-pro.code-workspace | Diretório A2 criado | §15.3 |
| A5 | Criar .vscode/settings.json | Diretório A2 criado | §15.4 |
| A6 | Criar .vscode/extensions.json | Diretório A2 criado | §15.5 |
| A7 | Criar .vscode/tasks.json | Diretório A2 criado | §15.6 |
| A8 | Criar .vscode/launch.json | Diretório A2 criado | §15.7 |
| A9 | Criar .editorconfig | Diretório A2 criado | §17.13 |
| A10 | Criar .prettierrc | Diretório A2 criado | §17.13 |
| A11 | Criar .gitignore | Diretório A2 criado | §17.13 |
| A12 | Criar .env.example | Diretório A2 criado | §17.13 |
| A13 | Criar .nvmrc | Diretório A2 criado | §17.13 |
| A14 | Criar package.json com scripts e engines | Diretório A2 criado | §17.13 |
| A15 | Criar tsconfig.json | Diretório A2 criado | §17.13 |
| A16 | Criar README.md inicial | Diretório A2 criado | §17.13 |
| A17 | Criar estrutura src/features/ e subpastas | Diretório A2 criado | §17.14 |
| A18 | Criar commit inicial | A3–A17 concluídos | §17.15 |

Ações do grupo B — requerem decisão do humano antes de executar

| # | Ação | Informação necessária | Seção |
| --- | ------ | ----------------------- | ------- |
| B1 | git config --global user.name | Nome real do desenvolvedor | §17.4 |
| B2 | git config --global user.email | E-mail vinculado ao GitHub | §17.4 |
| B3 | npm install (primeira vez) | Confirmação de que o package.json foi revisado | §17.8 |

Ações do grupo C — exclusivamente humano

| # | Ação | Motivo | Seção |
| --- | ------ | -------- | ------- |
| C1 | Liberar espaço em C: | Requer interação com a interface do Windows | §16.3 |
| C2 | Criar ou editar `C:\Users\<usuario>\.wslconfig` | Arquivo fora do alcance do WSL | §17.3 |
| C3 | Executar wsl --shutdown | Comando PowerShell no Windows | §17.3 |
| C4 | Confirmar VS Code instalado no Windows | Verificação visual no Windows | §16.4 |
| C5 | Instalar e confirmar extensão WSL no VS Code | Interface gráfica do editor | §17.7 |
| C6 | Abrir .code-workspace e aceitar extensões recomendadas | Interface gráfica do editor | §17.7 |
| C7 | gh auth login (autenticar GitHub CLI) | Requer credenciais do usuário | §17.4 |
| C8 | Validar depuração com breakpoints no navegador | Requer navegador e interação manual | §15.7 |
| C9 | Testar aplicação no celular | Requer dispositivo físico na rede local | §17.9 |

17.13 Criação dos arquivos de configuração de base

Esta seção consolida a criação de todos os arquivos de configuração do projeto que não fazem parte do Workspace do VS Code (cobertos em §15). Todos os arquivos devem ser criados na raiz de ~/projetos/cepraea-beach-pro.

Pré-requisito: diretório do projeto criado conforme §17.5.

17.13.1 Arquivo .editorconfig

Finalidade: garantir que qualquer editor respeite as mesmas convenções de charset, indentação e finais de linha, independentemente das configurações pessoais do desenvolvedor.

Conteúdo:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
```

Verificação: abrir qualquer arquivo no VS Code, verificar na barra de status que o final de linha exibe "LF" e a indentação exibe "2 espaços".

17.13.2 Arquivo .prettierrc

Finalidade: definir o estilo de formatação automática aplicado pelo Prettier ao salvar.

Conteúdo:

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

Verificação: criar um arquivo temporário .ts com aspas duplas e espaçamento inconsistente, salvar e confirmar que o Prettier formata automaticamente.

17.13.3 Arquivo .gitignore

Finalidade: impedir que arquivos gerados, dependências, segredos e configurações pessoais sejam versionados.

Conteúdo:

```gitignore
# Dependências
node_modules/

# Build e cobertura
dist/
coverage/
.vite/

# Variáveis de ambiente
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*

# Sistema operacional
.DS_Store
Thumbs.db
desktop.ini

# Editor (configurações pessoais)
.vscode/settings.local.json

# Playwright
/test-results/
/playwright-report/
/playwright/.cache/
```

Observação: o arquivo .vscode/ com settings.json, extensions.json, tasks.json e launch.json deve ser versionado. Somente arquivos com configurações pessoais ou temporárias não devem ser versionados.

Verificação: executar git status após criar os arquivos e confirmar que node_modules não aparece como não rastreado.

17.13.4 Arquivo .env.example

Finalidade: documentar quais variáveis de ambiente o projeto precisa, sem revelar valores reais.

Conteúdo:

```env
VITE_APP_NAME=CEPRAEA Beach Pro
VITE_API_URL=
VITE_PUBLIC_APP_URL=
VITE_ENABLE_OFFLINE=false
```

O arquivo .env.example pode e deve ser versionado. O arquivo .env.local, com os valores reais, não deve ser versionado.

Verificação: confirmar que .env.example aparece em git status como não rastreado e que .env.local não aparece (pois está no .gitignore).

17.13.5 Arquivo .nvmrc

Finalidade: registrar a versão oficial do Node.js do projeto, permitindo que o NVM (Node Version Manager) selecione automaticamente a versão correta.

Conteúdo:

```text
24.14.1
```

Verificação: executar no Ubuntu:

```bash
cat .nvmrc
node --version
```

Os dois valores devem coincidir.

17.13.6 Arquivo package.json

Finalidade: declarar metadados do projeto, scripts padronizados, restrições de versão e o gerenciador de pacotes oficial.

Conteúdo inicial:

```json
{
  "name": "cepraea-beach-pro",
  "version": "0.0.1",
  "private": true,
  "description": "PWA para gestão de atletas e treinadores de handebol de areia do CEPRAEA",
  "engines": {
    "node": "24.14.1",
    "npm": "11.11.0"
  },
  "packageManager": "npm@11.11.0",
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 5173",
    "build": "tsc -b && vite build",
    "preview": "vite preview --host 0.0.0.0 --port 4173",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "validate": "npm run lint && npm run typecheck && npm run test && npm run build"
  }
}
```

Observação: as dependências (vite, typescript, eslint, vitest, prettier) serão adicionadas ao package.json com npm install após a escolha formal do framework e da stack completa. O conteúdo acima registra apenas os metadados e scripts iniciais.

Verificação: executar node -e "require('./package.json')" para confirmar que o JSON é válido.

17.13.7 Arquivo tsconfig.json

Finalidade: configurar o compilador TypeScript com regras rigorosas, adequadas ao projeto.

Conteúdo:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

Observação: quando o framework de interface for definido, pode ser necessário adicionar "jsx" ao compilerOptions. Por exemplo, para React: "jsx": "react-jsx". A opção moduleResolution: "bundler" requer TypeScript 5.0 ou superior e é compatível com Vite.

Verificação: executar npm run typecheck. O comando deve concluir sem erros (ou com erros apenas de dependências ausentes, que serão resolvidos após npm install).

17.13.8 Arquivo README.md

Finalidade: documentar o projeto de forma que qualquer pessoa possa instalar, executar e entender a aplicação.

Conteúdo:

````markdown
# CEPRAEA Beach Pro

Progressive Web Application para gestão de atletas e treinadores da equipe de handebol de areia do CEPRAEA.

## Pré-requisitos

- Node.js 24.14.1 (ver `.nvmrc`)
- npm 11.11.0
- Ubuntu 24.04 via WSL 2
- Visual Studio Code com extensão WSL

## Instalação

```bash
cd ~/projetos/cepraea-beach-pro
npm ci
```

## Desenvolvimento

```bash
npm run dev
```

Acesse `http://localhost:5173` no navegador do Windows.

Em uma rede local confiável, acesse pelo endereço de rede exibido pelo Vite no celular.

## Scripts disponíveis

| Script | Descrição |
| --- | --- |
| `npm run dev` | Inicia o servidor de desenvolvimento |
| `npm run build` | Gera o build de produção |
| `npm run preview` | Visualiza o build localmente |
| `npm run lint` | Executa o ESLint |
| `npm run typecheck` | Verifica os tipos TypeScript |
| `npm run test` | Executa os testes |
| `npm run validate` | Executa lint, tipos, testes e build em sequência |

## Estrutura do projeto

```text
cepraea-beach-pro/
├── .vscode/              Configurações do VS Code
├── src/
│   └── features/         Funcionalidades organizadas por domínio
│       ├── atletas/
│       ├── treinadores/
│       ├── treinos/
│       ├── presencas/
│       ├── avaliacoes/
│       └── jogos/
├── public/               Arquivos estáticos
└── tests/                Testes de ponta a ponta
```

## Documentação técnica

Consultar `vscode.md` para o manual completo do ambiente de desenvolvimento, incluindo configurações, decisões técnicas e procedimentos de execução.
````

Verificação: confirmar que o arquivo é renderizado corretamente abrindo-o no VS Code.

17.14 Criação da estrutura de pastas do projeto

Esta seção documenta a criação dos diretórios de código, recursos estáticos e testes, usando comandos executáveis no Ubuntu.

Pré-requisito: projeto criado conforme §17.5.

Explicação da estrutura:

• src/features/ — organiza o código por funcionalidade de negócio, não por tipo técnico;
• cada feature tem subpastas para components, pages, services, schemas, types e tests;
• public/ — arquivos servidos diretamente pelo Vite sem processamento (ícones, manifesto);
• tests/ — testes de ponta a ponta com Playwright.

Comandos:

```bash
cd ~/projetos/cepraea-beach-pro

# Criar subpastas de cada feature
mkdir -p src/features/atletas/{components,pages,services,schemas,types,tests}
mkdir -p src/features/treinadores/{components,pages,services,schemas,types,tests}
mkdir -p src/features/treinos/{components,pages,services,schemas,types,tests}
mkdir -p src/features/presencas/{components,pages,services,schemas,types,tests}
mkdir -p src/features/avaliacoes/{components,pages,services,schemas,types,tests}
mkdir -p src/features/jogos/{components,pages,services,schemas,types,tests}

# Criar diretórios raiz
mkdir -p public
mkdir -p tests
```

Verificação da estrutura criada:

```bash
find src public tests -type d | sort
```

Saída esperada:

```text
public
src/features/atletas
src/features/atletas/components
src/features/atletas/pages
src/features/atletas/services
src/features/atletas/schemas
src/features/atletas/types
src/features/atletas/tests
src/features/avaliacoes
src/features/avaliacoes/components
...
tests
```

Observação: Git não versiona diretórios vazios. Para que as pastas sejam incluídas no commit inicial, criar um arquivo .gitkeep em cada uma:

```bash
find src public tests -type d -exec touch {}/.gitkeep \;
```

17.15 Commit inicial

O commit inicial registra a configuração do ambiente de desenvolvimento antes de qualquer código de funcionalidade.

Pré-requisito: todas as ações A1–A17 concluídas.

Passo a passo:

1. Verificar o estado atual do repositório:

```bash
cd ~/projetos/cepraea-beach-pro
git status
```

1. Adicionar os arquivos de configuração ao stage:

```bash
git add \
  cepraea-beach-pro.code-workspace \
  .vscode/ \
  .editorconfig \
  .prettierrc \
  .gitignore \
  .env.example \
  .nvmrc \
  package.json \
  tsconfig.json \
  README.md \
  src/ \
  public/ \
  tests/
```

1. Conferir o que será commitado:

```bash
git status
git diff --staged --stat
```

Confirmar que:
• nenhum arquivo de .env.local, node_modules ou dist está incluído;
• todos os arquivos listados acima aparecem como "new file".

1. Criar o commit:

```bash
git commit -m "chore: configura workspace de desenvolvimento do CEPRAEA Beach Pro"
```

1. Verificar o resultado:

```bash
git log --oneline
git show --stat HEAD
```

Saída esperada do git log:

```text
abc1234 (HEAD -> main) chore: configura workspace de desenvolvimento do CEPRAEA Beach Pro
```

Saída esperada do git show --stat:

```text
chore: configura workspace de desenvolvimento do CEPRAEA Beach Pro

 .editorconfig                              | 10 +
 .env.example                               |  4 +
 .gitignore                                 | 20 +
 .nvmrc                                     |  1 +
 .prettierrc                               |  6 +
 .vscode/extensions.json                   |  9 +
 .vscode/launch.json                       | 35 +
 .vscode/settings.json                     | 55 +
 .vscode/tasks.json                        | 65 +
 README.md                                  | 50 +
 cepraea-beach-pro.code-workspace          | 25 +
 package.json                              | 25 +
 tsconfig.json                             | 20 +
 ...
```

Registrar a data e o hash do commit na seção §17.11.
