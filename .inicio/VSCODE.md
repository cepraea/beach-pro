# Especificação do ambiente de desenvolvimento do CEPRAEA Beach Pro

## 1. Controle do documento

| Campo | Valor |
| --- | --- |
| Identificador | ESP-CEPRAEA-VSCODE-001 |
| Versão | 1.0.0 |
| Estado | Em qualificação |
| Proprietário | Desenvolvedor responsável pelo CEPRAEA Beach Pro |
| Aprovador | Proprietário do produto e do repositório |
| Data de vigência documental | 2026-07-28 |
| Última revisão | 2026-07-28 |
| Próxima revisão | Após alteração da baseline ou, no máximo, em 2027-01-28 |
| Relatório de origem | `RELATORIO-VSCODE.md` |
| Histórico anterior | `.inicio/historico/VSCODE-legacy-2026-07-28.md` |

O estado “Em qualificação” significa que a linha de base documental e as verificações automatizadas
estão definidas, mas ainda existem verificações manuais pendentes. O documento somente poderá mudar
para “Aprovado” após o atendimento dos critérios globais da seção 17.

## 2. Objetivo

Esta especificação define e controla um ambiente de desenvolvimento padronizado, seguro,
reproduzível e verificável para o CEPRAEA Beach Pro.

O ambiente DEVE:

- reduzir variações entre instalações;
- prevenir defeitos antes da execução;
- manter coerência entre editor, ferramentas, testes e build;
- proteger credenciais e informações pessoais;
- produzir evidências objetivas de conformidade;
- permitir reconstrução a partir do repositório e do lockfile.

## 3. Escopo

Esta especificação abrange:

- Visual Studio Code e Workspace;
- sistema operacional e WSL usados na qualificação principal;
- Node.js, npm e dependências;
- Vite, React e TypeScript;
- lint, formatação, testes e build;
- depuração no Chrome;
- variáveis de ambiente públicas do cliente;
- configuração básica da PWA;
- acesso local e móvel;
- Docker como alternativa opcional suportada;
- Git e proteção de informações;
- validação e registro de evidências.

Esta especificação não define:

- regras esportivas;
- critérios de avaliação de atletas;
- experiência visual detalhada;
- módulos completos de negócio;
- política jurídica de tratamento de dados;
- estratégia de produção e hospedagem;
- funcionamento offline de fluxos de negócio ainda não implementados.

## 4. Linguagem normativa

| Termo | Significado |
| --- | --- |
| DEVE ou NÃO DEVE | Requisito obrigatório e bloqueante |
| RECOMENDA-SE | Prática preferencial, não bloqueante |
| PODE | Alternativa permitida nos limites declarados |
| EXEMPLO | Conteúdo ilustrativo, sem força normativa |
| ESTADO ATUAL | Observação datada, sem criar requisito |
| HISTÓRICO | Conteúdo substituído e sem vigência |

Somente itens identificados por `REQ-VSC-###` criam obrigações. Recomendações, exemplos, estado atual
e histórico não podem ser usados isoladamente para reprovar a conformidade.

## 5. Hierarquia de autoridade

### REQ-VSC-001 — Fonte canônica única

Cada elemento configurável DEVE possuir exatamente uma fonte canônica conforme a tabela abaixo.

| Elemento | Fonte canônica |
| --- | --- |
| Scripts e faixas de dependências | `package.json` |
| Resolução exata das dependências | `package-lock.json` |
| Node.js | `.nvmrc` e `package.json#engines.node` |
| npm | `package.json#engines.npm` e `package.json#packageManager` |
| Workspace | `cepraea-beach-pro.code-workspace` |
| Editor | `.vscode/settings.json` |
| Extensões | `.vscode/extensions.json` |
| Tarefas | `.vscode/tasks.json` |
| Depuração | `.vscode/launch.json` |
| TypeScript | `tsconfig.json`, `tsconfig.app.json` e `tsconfig.node.json` |
| Vite e PWA | `vite.config.ts` |
| Variáveis públicas | `.env.example` |
| Formatação | `.editorconfig`, `.prettierrc` e `.prettierignore` |
| Lint | `eslint.config.js` e `.markdownlint.jsonc` |
| Docker opcional | `Dockerfile`, `docker-compose.yml` e `.dockerignore` |
| Requisitos | Este documento |
| Evidência de qualificação | `.inicio/evidencias/VALIDACAO-VSCODE.md` |

**Critério de aceitação CA-VSC-001:** `npm run quality:workspace` termina com código zero e nenhuma
seção deste documento apresenta uma segunda configuração vigente para o mesmo elemento.

### REQ-VSC-002 — Tratamento de divergências

Uma divergência entre esta especificação e uma fonte canônica DEVE reprovar a validação. A correção
DEVE ocorrer no mesmo conjunto de alterações e registrar impacto no histórico.

**Critério de aceitação CA-VSC-002:** toda alteração de baseline modifica as fontes afetadas, esta
especificação, a matriz de rastreabilidade e a evidência aplicável.

## 6. Linha de base técnica vigente

### 6.1 Stack aprovada

| Elemento | Configuração vigente | Classificação |
| --- | --- | --- |
| Interface | React 19 | Obrigatória |
| Build e desenvolvimento | Vite 6 | Obrigatória |
| Linguagem | TypeScript 5.7 em modo estrito | Obrigatória |
| Testes | Vitest 3 | Obrigatória |
| Lint de código | ESLint 9 | Obrigatória |
| Lint documental | Markdownlint CLI 2 | Obrigatória |
| Formatação | Prettier 3 e EditorConfig | Obrigatória |
| PWA | `vite-plugin-pwa` | Obrigatória |
| Cliente de dados | Supabase JS 2 | Obrigatória |
| Teste de componentes | Testing Library | Disponível, uso conforme necessidade |
| Docker | Dockerfile e Compose | Alternativa opcional suportada |

As versões exatas resolvidas são as registradas no `package-lock.json`. Faixas de compatibilidade são
as declaradas no `package.json`.

### REQ-VSC-003 — Runtime

O projeto DEVE usar Node.js 24.14.1 e npm 11.11.0.

**Critério de aceitação CA-VSC-003:** `.nvmrc`, `engines` e `packageManager` são coerentes; os
comandos `node --version` e `npm --version` retornam as versões especificadas.

### REQ-VSC-004 — Instalação reproduzível

Uma instalação regular DEVE usar `npm ci` e o `package-lock.json` versionado. `npm install` PODE ser
usado somente para adicionar, remover ou atualizar dependências.

**Critério de aceitação CA-VSC-004:** `npm ci` termina com código zero e não modifica o lockfile.

### REQ-VSC-005 — Arquitetura TypeScript

O TypeScript DEVE usar:

- `tsconfig.json` como orquestrador de referências;
- `tsconfig.app.json` para `src/` e JSX;
- `tsconfig.node.json` para `vite.config.ts`.

Todos os projetos TypeScript DEVEM operar em modo estrito.

**Critério de aceitação CA-VSC-005:** `npm run typecheck` e `npm run build` terminam com código zero.

## 7. Ambiente de execução principal

### REQ-VSC-006 — Ambiente qualificado

O fluxo principal de qualificação DEVE usar:

- Windows 11 como hospedeiro;
- Visual Studio Code instalado no Windows;
- extensão WSL do VS Code;
- Ubuntu 24.04 no WSL 2;
- projeto armazenado no sistema de arquivos Linux;
- Chrome no Windows como navegador principal de depuração.

O caminho do projeto DEVE estar sob `/home/<usuario-linux>/` e NÃO DEVE estar sob `/mnt/c/`.

**Critério de aceitação CA-VSC-006:** o VS Code indica conexão com WSL Ubuntu, e `pwd` confirma que o
projeto está no sistema de arquivos Linux.

### REQ-VSC-007 — Capacidade mínima

A máquina usada na qualificação DEVE possuir:

- pelo menos 30 GB livres no volume que armazena o WSL;
- pelo menos 8 GB de RAM física;
- pelo menos 4 processadores lógicos disponíveis ao WSL.

**Critério de aceitação CA-VSC-007:** evidência datada registra os resultados de armazenamento,
memória e processadores.

### REC-VSC-001 — Recursos do WSL

Para uma máquina com 8 GB de RAM, RECOMENDA-SE limitar o WSL a 4 GB de memória, 4 processadores e
4 GB de swap. Essa configuração é local e não integra o repositório.

## 8. Workspace e Visual Studio Code

### REQ-VSC-008 — Ponto de entrada oficial

O projeto DEVE ser aberto por `cepraea-beach-pro.code-workspace`. Esse arquivo DEVE conter somente a
definição das pastas do Workspace; configurações e extensões NÃO DEVEM ser duplicadas nele.

**Critério de aceitação CA-VSC-008:** o Workspace abre a raiz correta e
`npm run quality:workspace` aprova sua estrutura.

### REQ-VSC-009 — Configurações compartilhadas

`.vscode/settings.json` DEVE controlar:

- formatação ao salvar para código;
- correções explícitas do ESLint;
- indentação de dois espaços e final de linha LF;
- TypeScript instalado no projeto;
- exclusão de `node_modules`, `dist` e `coverage`;
- comportamento específico de Markdown.

Markdown NÃO DEVE ser formatado automaticamente pelo Prettier; sua conformidade DEVE ser controlada
pelo Markdownlint.

**Critério de aceitação CA-VSC-009:** o arquivo é JSON válido, o TypeScript do Workspace é utilizado
e o comportamento ao salvar corresponde aos valores canônicos.

### REQ-VSC-010 — Extensões oficiais

`.vscode/extensions.json` DEVE ser a lista única de extensões recomendadas:

- ESLint;
- Prettier;
- Markdownlint;
- GitLens;
- Error Lens;
- EditorConfig.

Extensões de preferência visual NÃO DEVEM ser recomendadas pelo projeto.

**Critério de aceitação CA-VSC-010:** uma instalação limpa do VS Code apresenta exatamente as
recomendações canônicas e `npm run quality:workspace` confirma a presença do Markdownlint.

### REQ-VSC-011 — Tarefas oficiais

`.vscode/tasks.json` DEVE disponibilizar:

- `CEPRAEA: iniciar desenvolvimento`;
- `CEPRAEA: validar projeto`;
- `CEPRAEA: executar testes`;
- `CEPRAEA: verificar tipos`;
- `CEPRAEA: build de produção`.

Toda tarefa npm DEVE referenciar um script existente no `package.json`.

**Critério de aceitação CA-VSC-011:** `npm run quality:workspace` termina com código zero e cada
tarefa é iniciada pelo VS Code sem erro de resolução.

### REQ-VSC-012 — Depuração principal

`.vscode/launch.json` DEVE possuir uma única configuração principal:

- nome `CEPRAEA: depurar no Chrome`;
- tipo `pwa-chrome`;
- URL `http://localhost:5173`;
- `webRoot` igual a `${workspaceFolder}/src`;
- tarefa prévia `CEPRAEA: iniciar desenvolvimento`;
- source maps habilitados.

**Critério de aceitação CA-VSC-012:** o Chrome abre pela ação F5 e um breakpoint em um arquivo
TypeScript é atingido.

## 9. Execução, portas e scripts

### REQ-VSC-013 — Porta de desenvolvimento

O servidor Vite DEVE usar a porta 5173 e aceitar conexões de rede por `host: true`.

**Critério de aceitação CA-VSC-013:** `npm run dev` expõe `http://localhost:5173` e
`npm run quality:workspace` confirma a configuração.

### REQ-VSC-014 — Catálogo de scripts

O `package.json` DEVE oferecer:

| Script | Finalidade |
| --- | --- |
| `assets:pwa` | Geração determinística dos ícones da PWA |
| `dev` | Servidor de desenvolvimento |
| `build` | TypeScript e build de produção |
| `preview` | Visualização do build na porta 4173 |
| `lint` | Lint do código |
| `lint:md` | Auditoria ampla do acervo Markdown governado |
| `lint:md:vscode` | Lint bloqueante desta especificação e de seu relatório |
| `quality:workspace` | Consistência cruzada do ambiente |
| `format` | Formatação do código |
| `format:check` | Verificação de formatação do código |
| `typecheck` | Verificação de tipos |
| `test` | Testes sem tolerância à ausência de arquivos |
| `test:watch` | Testes em modo observação |
| `validate` | Todas as portas obrigatórias e build |

**Critério de aceitação CA-VSC-014:** os scripts existem e o script `validate` termina com código
zero.

### REQ-VSC-015 — Política de testes

O projeto DEVE possuir pelo menos um teste. O comando de testes NÃO DEVE usar
`--passWithNoTests`.

**Critério de aceitação CA-VSC-015:** `npm run test` executa pelo menos um teste e reprova quando um
teste real falha.

## 10. Variáveis de ambiente e segurança

### REQ-VSC-016 — Contrato público de ambiente

`.env.example` DEVE declarar, nesta ordem:

| Variável | Obrigatória | Sensibilidade | Finalidade |
| --- | --- | --- | --- |
| `VITE_APP_NAME` | Sim | Pública | Nome do produto |
| `VITE_SUPABASE_URL` | Sim para integração | Pública | URL do projeto Supabase |
| `VITE_SUPABASE_ANON_KEY` | Sim para integração | Pública | Chave pública anon |
| `VITE_ENABLE_OFFLINE` | Sim | Pública | Ativação explícita de recursos offline |

`VITE_SUPABASE_ANON_KEY` é pública, mas sua autorização efetiva DEVE depender de políticas adequadas
no Supabase.

**Critério de aceitação CA-VSC-016:** `.env.example` corresponde ao contrato e
`npm run quality:workspace` termina com código zero.

### REQ-VSC-017 — Proteção de segredos

Arquivos com valores locais, tokens ou credenciais NÃO DEVEM ser versionados. Chaves privadas,
incluindo `service_role`, NÃO DEVEM usar prefixo `VITE_` nem aparecer no cliente.

**Critério de aceitação CA-VSC-017:** `git status` não lista `.env.local`, e a revisão de segurança
não encontra segredo ou dado pessoal nos arquivos versionáveis.

### REQ-VSC-018 — Dados pessoais no manual

Nome de usuário, e-mail, IP completo, número de série, Product ID e identificadores exclusivos de
máquina NÃO DEVEM integrar a especificação ou evidências publicáveis.

**Critério de aceitação CA-VSC-018:** a revisão documental encontra somente placeholders ou dados
sanitizados.

## 11. Qualidade e validação

### REQ-VSC-019 — Portas de qualidade

`npm run validate` DEVE executar, nesta ordem:

1. ESLint;
2. Markdownlint da especificação do ambiente;
3. consistência do Workspace;
4. verificação de tipos;
5. testes;
6. build de produção.

Qualquer falha DEVE retornar código diferente de zero.

**Critério de aceitação CA-VSC-019:** a saída do comando comprova todas as etapas e termina com
código zero.

### REQ-VSC-020 — Governança Markdown

O lint bloqueante desta baseline DEVE incluir:

- `.inicio/VSCODE.md`;
- `.inicio/evidencias/*.md`;
- `RELATORIO-VSCODE.md`.

O comando `npm run lint:md` DEVE permanecer disponível como auditoria ampla de `docs/**/*.md` e
`src/features/**/*.md`. Não conformidades preexistentes nesse acervo DEVEM ser registradas, mas não
podem impedir isoladamente a qualificação do Workspace até o saneamento documental específico.

**Critério de aceitação CA-VSC-020:** `npm run lint:md:vscode` termina com zero ocorrências, e o
resultado do lint amplo está registrado na evidência sem ser apresentado como aprovado.

### REQ-VSC-021 — Consistência cruzada

O script `scripts/quality/validate-workspace.mjs` DEVE verificar:

- validade dos arquivos JSON;
- raiz do Workspace;
- ausência de configurações duplicadas no Workspace;
- correspondência entre tarefas e scripts;
- correspondência entre tarefas prévias e depuração;
- porta e host do Vite;
- versões de Node.js e npm;
- proibição de `--passWithNoTests`;
- contrato de `.env.example`;
- existência e dimensões dos ícones da PWA.

**Critério de aceitação CA-VSC-021:** uma divergência controlada reprova o script e sua correção
restaura o código zero.

### REQ-VSC-022 — Vulnerabilidades de produção

Dependências de produção NÃO DEVEM possuir vulnerabilidades conhecidas classificadas como altas ou
críticas no momento da qualificação.

**Critério de aceitação CA-VSC-022:** `npm audit --omit=dev` retorna código zero.

### REQ-VSC-023 — Evidência

Cada qualificação DEVE registrar:

- data e executor;
- commit ou estado do repositório;
- versões de Node.js e npm;
- comandos executados;
- resultado por requisito;
- pendências e desvios;
- validações manuais.

**Critério de aceitação CA-VSC-023:** `.inicio/evidencias/VALIDACAO-VSCODE.md` contém todos os campos
e não declara como aprovado um teste não executado.

## 12. PWA

### REQ-VSC-024 — Manifesto e service worker

O build DEVE gerar manifesto e service worker por meio de `vite-plugin-pwa`. A política vigente de
atualização é `autoUpdate`.

**Critério de aceitação CA-VSC-024:** o build termina com código zero e `dist/` contém o manifesto e
os artefatos do service worker.

### REQ-VSC-025 — Identidade instalável

Os ícones declarados no manifesto DEVEM existir, ter os tamanhos declarados e ser adequados à
instalação.

**Critério de aceitação CA-VSC-025:** inspeção automatizada ou manual confirma os arquivos de
192 × 192 e 512 × 512 pixels.

### REQ-VSC-026 — Limite do offline

A geração do service worker não comprova funcionalidades de negócio offline. Fluxos offline somente
PODEM ser declarados atendidos após implementação e teste próprios.

**Critério de aceitação CA-VSC-026:** a evidência distingue cache da aplicação de operações de
negócio offline; capacidades não implementadas permanecem pendentes.

## 13. Docker

### REQ-VSC-027 — Classificação do Docker

Docker é uma alternativa opcional suportada e NÃO integra o critério mínimo de prontidão do ambiente.
O fluxo oficial principal continua sendo `npm ci` e `npm run dev` no Ubuntu.

Quando utilizado, Docker DEVE usar os arquivos canônicos e a mesma versão de Node.js da baseline.

**Critério de aceitação CA-VSC-027:** `docker compose config` termina com código zero quando Docker
estiver disponível. Indisponibilidade do daemon não reprova o fluxo principal.

### REC-VSC-002 — Uso do Docker

RECOMENDA-SE usar Docker somente quando o isolamento trouxer benefício concreto. Em máquinas com
8 GB de RAM, RECOMENDA-SE evitar sua execução simultânea com outras ferramentas pesadas.

## 14. Acesso e depuração

### REQ-VSC-028 — Acesso no computador

O navegador do Windows DEVE acessar `http://localhost:5173` enquanto o servidor estiver ativo no
WSL.

**Critério de aceitação CA-VSC-028:** a página exibe `CEPRAEA Beach Pro` e não apresenta erro fatal
no console.

### REQ-VSC-029 — Acesso móvel

Um celular autorizado na mesma rede privada DEVE acessar o endereço de rede apresentado pelo Vite.
A porta 5173 NÃO DEVE ser liberada para redes públicas.

**Critério de aceitação CA-VSC-029:** evidência manual registra dispositivo, rede privada, URL
sanitizada e carregamento da aplicação.

## 15. Estrutura do projeto

### REQ-VSC-030 — Organização por funcionalidade

Código de negócio DEVE ser organizado sob `src/features/`. Código compartilhado DEVE ficar sob
`src/shared/`. Subdiretórios DEVEM ser criados sob demanda; diretórios vazios não constituem
requisito arquitetural.

**Critério de aceitação CA-VSC-030:** inspeção da árvore confirma que código de negócio e código
compartilhado respeitam seus limites.

### REC-VSC-003 — Simplicidade

RECOMENDA-SE evitar dependências, diretórios e abstrações sem necessidade comprovada.

## 16. Matriz de rastreabilidade

| Requisito | Fonte canônica principal | Verificação | Estado em 2026-07-28 |
| --- | --- | --- | --- |
| REQ-VSC-001 a 002 | Esta especificação | Revisão e `quality:workspace` | Implementado |
| REQ-VSC-003 | `.nvmrc`, `package.json` | Versões e `quality:workspace` | Implementado |
| REQ-VSC-004 | `package-lock.json` | `npm ci` limpo | Aprovado |
| REQ-VSC-005 | `tsconfig*.json` | `typecheck` e `build` | Aprovado |
| REQ-VSC-006 a 007 | Ambiente local | Inspeção manual | Pendente manual |
| REQ-VSC-008 a 011 | Workspace e `.vscode/` | `quality:workspace` e VS Code | Automatizado aprovado; VS Code pendente |
| REQ-VSC-012 | `.vscode/launch.json` | Breakpoint | Pendente manual |
| REQ-VSC-013 a 015 | Vite e `package.json` | Scripts e testes | Aprovado |
| REQ-VSC-016 a 018 | `.env.example`, `.gitignore` | Script e revisão | Aprovado |
| REQ-VSC-019 a 022 | Scripts de qualidade | `validate` e `npm audit` | Aprovado com DV-VSC-001 |
| REQ-VSC-023 | Evidência | Revisão documental | Implementado |
| REQ-VSC-024 | `vite.config.ts` | Build e inspeção de `dist/` | Aprovado |
| REQ-VSC-025 | `public/icons/` | Dimensões dos PNGs | Aprovado |
| REQ-VSC-026 | Implementação futura | Testes offline | Pendente por escopo |
| REQ-VSC-027 | Arquivos Docker | `docker compose config` | Não aplicável nesta execução |
| REQ-VSC-028 | Servidor e navegador | Teste automatizado | Aprovado |
| REQ-VSC-029 | Dispositivo móvel | Teste manual | Pendente manual |
| REQ-VSC-030 | `src/` | Inspeção da árvore | Implementado |

Os estados acima são observações datadas. A fonte autoritativa dos resultados da qualificação é o
relatório de evidência.

## 17. Critérios globais de aprovação

Esta especificação somente poderá assumir o estado “Aprovado” quando:

- CG-VSC-001: `npm ci` for executado em instalação limpa;
- CG-VSC-002: `npm run validate` terminar com código zero;
- CG-VSC-003: `npm audit --omit=dev` terminar com código zero;
- CG-VSC-004: o Workspace abrir conectado ao WSL;
- CG-VSC-005: a depuração atingir um breakpoint TypeScript;
- CG-VSC-006: o navegador do Windows acessar a aplicação;
- CG-VSC-007: o teste móvel for aprovado em rede privada;
- CG-VSC-008: os ícones da PWA existirem e forem validados;
- CG-VSC-009: nenhuma credencial ou informação pessoal estiver exposta;
- CG-VSC-010: a evidência registrar todos os resultados sem pendência bloqueante;
- CG-VSC-011: proprietário e aprovador registrarem a aprovação.

## 18. Gestão de mudanças e desvios

### REQ-VSC-031 — Mudança de baseline

Alterações de versões, portas, ferramentas, fontes canônicas ou requisitos DEVEM atualizar no mesmo
conjunto:

- implementação;
- especificação;
- matriz de rastreabilidade;
- testes de consistência;
- histórico;
- evidência, quando houver requalificação.

**Critério de aceitação CA-VSC-031:** a revisão da alteração não identifica referência vigente à
baseline substituída.

### REQ-VSC-032 — Desvios

Uma não conformidade temporariamente aceita DEVE registrar:

- ID;
- requisito afetado;
- justificativa;
- risco;
- responsável;
- prazo ou condição de encerramento.

Desvio vencido DEVE reprovar a aprovação.

**Critério de aceitação CA-VSC-032:** todas as pendências bloqueantes possuem resolução ou desvio
vigente formalmente aprovado.

## 19. Recomendações operacionais

### REC-VSC-004 — Commits

RECOMENDA-SE criar commits pequenos, objetivos e rastreáveis.

### REC-VSC-005 — Testes em dispositivos

RECOMENDA-SE repetir testes de PWA, responsividade e conectividade após mudanças que afetem cache,
rede, manifesto ou interface.

### REC-VSC-006 — Dependências

RECOMENDA-SE revisar vulnerabilidades e atualizações periodicamente, sem aplicar atualizações
incompatíveis de forma automática.

## 20. Histórico

| Versão | Data | Alteração | Estado |
| --- | --- | --- | --- |
| 1.0.0 | 2026-07-28 | Consolidação normativa resultante de `RELATORIO-VSCODE.md` | Vigente |
| Legado | Até 2026-07-28 | Manual acumulativo com versões concorrentes | Substituído |

O conteúdo legado foi preservado como snapshot editorial em
`.inicio/historico/VSCODE-legacy-2026-07-28.md`. Ele é exclusivamente histórico e NÃO possui
vigência normativa.
