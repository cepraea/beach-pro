# Bootstrap e Validação do Workspace — CEPRAEA BEACH PRO

## 1.1 Objetivo

Este documento define o procedimento técnico para criação e validação inicial do workspace do **CEPRAEA BEACH PRO** utilizando:

* Windows;
* WSL2;
* distribuição Linux;
* Git;
* Visual Studio Code com integração WSL;
* Claude Code;
* Codex IDE.

Além do procedimento, o documento registra as evidências de execução disponíveis para cada etapa.

O bootstrap tem como objetivo alcançar o seguinte estado:

```text
WSL2
  ↓
Diretório no filesystem Linux
  ↓
Git root
  ↓
VS Code conectado ao WSL
  ↓
Instruções do workspace
  ↓
Claude Code
  ↓
Codex IDE
  ↓
WORKSPACE_READY
```

## 1.2 Tipo de documentação

**Classificação:** Runbook técnico, procedimento de bootstrap e registro de validação.

### 1.3 Público-alvo

> **Público-alvo não especificado.**

Pelo nível técnico do procedimento, o conteúdo pressupõe familiaridade com Windows, WSL, shell Linux, Git, VS Code e ferramentas de desenvolvimento assistido por IA.

## 1.4 Convenções de validação

Cada etapa é tratada como um **gate**.

Os estados utilizados são:

* `PASS`: critério validado por evidência de execução;
* `FAIL`: critério de validação não atendido;
* `PENDING`: procedimento definido, mas sem evidência suficiente registrada neste documento.

Um resultado esperado **não constitui evidência de execução**.

---

## GATE-0 — Validar WSL2

## Objetivo

Confirmar que existe uma distribuição Linux configurada para utilizar WSL2 antes da criação do workspace.

## Procedimento

Os comandos devem ser executados no **PowerShell do Windows**, e não no shell da distribuição Linux.

Execute:

```powershell
wsl --status
wsl --list --verbose
```

Os comandos são utilizados para consultar a configuração do WSL e identificar as distribuições instaladas e suas respectivas versões.

## Critério de validação

```text
PASS:
- existe uma distribuição Linux;
- a distribuição utilizada apresenta VERSION = 2.

FAIL:
- não existe distribuição Linux adequada;
- a distribuição utilizada apresenta VERSION = 1.
```

## Evidência de execução

### Comando

```powershell
wsl --status
```

### Resultado capturado

```powershell
PS C:\Users\davis> wsl --status
Distribuição Padrão: Ubuntu
Versão Padrão: 2
```

### Avaliação

```text
PASS
```

---

### Comando

```powershell
wsl --list --verbose
```

### Resultado capturado

```powershell
PS C:\Users\davis> wsl --list --verbose
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Running         2
```

### Avaliação

```text
PASS
```

## Resultado do gate

```text
GATE-0 = PASS
```

A distribuição padrão identificada é:

```text
Ubuntu
```

e está configurada com:

```text
WSL VERSION = 2
```

## Observação sobre Codex

O texto original informa que a documentação consultada do Codex requer WSL2 para esse ambiente e registra que WSL1 deixou de ser suportado a partir da versão indicada do Codex.

> **Recomendação:** validar novamente essa exigência na documentação oficial do Codex sempre que este runbook for executado, pois requisitos de versão e sandbox podem mudar.

Se a distribuição utilizada estiver em WSL1, o procedimento deste documento **NÃO DEVE** avançar para a validação do Codex até que o requisito seja corrigido.

---

# GATE-0.1 — Entrar na distribuição Linux

## Objetivo

Iniciar explicitamente a distribuição que será utilizada pelo workspace.

## Procedimento

Utilize o nome retornado por:

```powershell
wsl --list --verbose
```

Sintaxe:

```powershell
wsl --distribution <NOME_DA_DISTRO>
```

Para a evidência registrada anteriormente:

```powershell
wsl --distribution Ubuntu
```

Depois de entrar na distribuição, execute:

```bash
echo "$WSL_DISTRO_NAME"
pwd
```

## Resultado esperado

A variável:

```bash
$WSL_DISTRO_NAME
```

DEVE identificar a distribuição selecionada.

Neste estágio ainda não existe projeto.

Estado conceitual:

```text
Windows
└── WSL2
    └── Ubuntu
```

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar a saída real de `echo "$WSL_DISTRO_NAME"` e `pwd` para comprovar a execução desta etapa.

---

# GATE-1 — Criar o diretório do projeto

## Objetivo

Criar o diretório raiz inicial do CEPRAEA BEACH PRO dentro do filesystem Linux do WSL.

## Procedimento

No terminal WSL:

```bash
mkdir -p ~/projetos/NOME_DO_PROJETO
cd ~/projetos/NOME_DO_PROJETO
pwd
```

Para um nome de exemplo:

```bash
mkdir -p ~/projetos/novo-projeto
cd ~/projetos/novo-projeto
pwd
```

## Resultado esperado

```text
/home/<usuario>/projetos/novo-projeto
```

O diretório utilizado neste procedimento NÃO DEVE estar em:

```text
/mnt/c/...
C:\...
/workspaces/...
```

O procedimento prioriza o filesystem Linux do WSL para projetos manipulados predominantemente por ferramentas Linux.

## Critério de validação

```text
PASS:
PWD começa em /home/

FAIL:
PWD começa em /mnt/c/
ou
PWD está em /workspaces/
```

Estado esperado:

```text
WSL2
└── /home/<user>/projetos/novo-projeto/
```

Nenhuma aplicação é criada neste gate.

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar a saída real de `pwd`.

---

# GATE-2 — Inicializar e validar o repositório Git

## Objetivo

Verificar a instalação do Git, criar o repositório e confirmar explicitamente sua raiz e branch inicial.

## Pré-requisito

O `GATE-1` deve estar validado.

## Verificação do Git

Execute:

```bash
git --version
```

### Critério

Saída equivalente a:

```text
git version X.Y.Z
```

indica disponibilidade do Git.

Se ocorrer:

```text
command not found
```

o procedimento NÃO DEVE avançar para `git init` até que o Git esteja disponível.

## Inicialização

Execute:

```bash
git init -b main
```

Esse comando inicializa um repositório Git e define explicitamente:

```text
branch inicial = main
```

Neste estágio:

```text
main = branch inicial
main ≠ branch contendo commit
```

Nenhum commit é criado por esse comando.

## Verificação

Execute:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
```

Esses comandos verificam, respectivamente:

```text
git rev-parse --show-toplevel
→ raiz da working tree

git branch --show-current
→ branch atual

git status --short --branch
→ estado resumido do repositório
```

## Resultado esperado

Para o exemplo deste documento:

```text
/home/<user>/projetos/novo-projeto
main
## No commits yet on main
```

## Critério

```text
PASS:
- Git root = diretório pretendido;
- branch = main;
- repositório sem commits.

FAIL:
- Git root aponta para diretório pai ou inesperado;
- branch diferente de main;
- comando retorna "not a git repository".
```

Estado esperado:

```text
/home/<user>/projetos/novo-projeto/
└── .git/
```

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar as saídas reais de `git --version`, `git rev-parse --show-toplevel`, `git branch --show-current` e `git status --short --branch`.

---

# GATE-3 — Abrir o Git root no VS Code conectado ao WSL

## Objetivo

Garantir que o VS Code utilize exatamente o diretório Git criado anteriormente e que sua execução esteja conectada ao ambiente WSL.

## Pré-requisito

O `GATE-2` deve estar validado.

## Verificar a CLI do VS Code

Execute:

```bash
code --version
```

Se o comando estiver disponível, abra o diretório atual:

```bash
code .
```

O `.` representa o diretório corrente, que neste momento DEVE corresponder ao Git root.

## Verificação visual

Na nova janela do VS Code, a interface DEVE indicar conexão com a distribuição WSL utilizada, por exemplo:

```text
WSL: Ubuntu
```

## Verificação pelo terminal integrado

No VS Code:

```text
Terminal
→ New Terminal
```

Execute:

```bash
echo "$WSL_DISTRO_NAME"
pwd
git rev-parse --show-toplevel
git branch --show-current
```

## Resultado esperado

```text
Ubuntu
/home/<user>/projetos/novo-projeto
/home/<user>/projetos/novo-projeto
main
```

## Critério

```text
PASS:
- VS Code conectado ao WSL;
- PWD = Git root;
- Git root = diretório pretendido;
- branch = main.

FAIL:
- terminal utiliza caminho C:\;
- PWD diferente do Git root;
- janela não está conectada ao WSL.
```

Neste ponto, uma pasta aberta diretamente no VS Code é tratada como um **single-folder workspace**.

A criação de um arquivo `.code-workspace` não é requisito deste procedimento.

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar `code --version`, as saídas do terminal integrado e evidência de que a janela do VS Code está conectada ao WSL.

---

# GATE-4 — Criar a camada de instruções dos agentes

## Objetivo

Criar somente os arquivos utilizados para fornecer instruções de projeto ao Codex e ao Claude Code.

Este gate NÃO cria código de aplicação.

## Estrutura pretendida

```text
novo-projeto/
├── .git/
├── AGENTS.md
└── CLAUDE.md
```

## Criar `AGENTS.md`

Execute:

```bash
cat > AGENTS.md <<'EOF'
# Workspace Instructions

- The repository is currently in workspace bootstrap state.
- Do not create application code unless explicitly instructed.
- Do not install application dependencies unless explicitly instructed.
- Do not create Docker or Dev Container configuration unless explicitly instructed.
EOF
```

## Criar `CLAUDE.md`

Execute:

```bash
cat > CLAUDE.md <<'EOF'
@AGENTS.md
EOF
```

## Finalidade dos arquivos

Neste procedimento:

```text
AGENTS.md
→ instruções de projeto utilizadas pelo Codex

CLAUDE.md
→ instruções carregadas pelo Claude Code
```

O conteúdo:

```text
@AGENTS.md
```

é utilizado para importar as instruções comuns para o contexto do Claude Code.

Esses arquivos fazem parte da infraestrutura de agentes definida neste bootstrap.

Eles **NÃO são necessários para que o VS Code reconheça uma pasta como workspace**.

## Verificação

Execute:

```bash
cat CLAUDE.md
git status --short
```

## Resultado esperado

```text
@AGENTS.md
```

e:

```text
?? AGENTS.md
?? CLAUDE.md
```

Não é necessário criar commit neste gate.

Estado esperado:

```text
novo-projeto/
├── .git/
├── AGENTS.md
└── CLAUDE.md
    └── @AGENTS.md
```

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar as saídas reais de `cat CLAUDE.md` e `git status --short`.

---

# GATE-5 — Validar Claude Code no workspace

## Objetivo

Verificar se o Claude Code está operando dentro do workspace e carregando as instruções correspondentes ao projeto.

## Pré-requisitos

Devem estar disponíveis:

* VS Code compatível com a extensão;
* extensão Claude Code;
* autenticação compatível;
* `CLAUDE.md` criado no projeto.

## Instalação ou habilitação

No VS Code:

```text
Ctrl+Shift+X
```

Localize:

```text
Claude Code
```

e instale ou habilite a extensão.

## Abrir Claude Code

Utilize:

```text
Ctrl+Shift+P
→ Claude Code
→ Open in New Tab
```

Realize autenticação quando solicitada.

## Verificar contexto

No Claude Code, execute:

```text
/context
```

A verificação deve confirmar a presença de:

```text
CLAUDE.md
```

em `Memory files`.

A estrutura esperada é:

```text
CLAUDE.md
    ↓
@AGENTS.md
```

## Critério

```text
PASS:
CLAUDE.md aparece em /context → Memory files.

FAIL:
CLAUDE.md não aparece no contexto esperado.
```

Nenhum desenvolvimento de aplicação deve ser solicitado durante este gate.

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar a evidência da saída de `/context` que demonstre o carregamento do arquivo.

---

# GATE-6 — Validar Codex no workspace

## Objetivo

Verificar se o Codex IDE reconhece as instruções de projeto existentes em `AGENTS.md`.

## Pré-requisitos

* VS Code conectado ao WSL;
* extensão Codex instalada ou habilitada;
* autenticação concluída;
* `AGENTS.md` existente no Git root.

## Abrir Codex

Se necessário:

```text
Ctrl+Shift+P
→ Codex: Open Codex Sidebar
```

## Teste de inspeção

No Codex IDE, solicite apenas leitura:

```text
List the active project instruction files and summarize the
current repository instructions.

Do not modify files.
Do not install anything.
Do not create application code.
Do not create container configuration.
```

## Resultado esperado

O Codex deve identificar as instruções provenientes de:

```text
AGENTS.md
```

## Critério

```text
PASS:
AGENTS.md reconhecido como fonte de instruções do projeto.

FAIL:
AGENTS.md não reconhecido ou instruções incompatíveis com seu conteúdo.
```

A CLI standalone do Codex não é requisito deste bootstrap.

## Status documental

```text
PENDING
```

> **Informação necessária:** registrar a resposta efetiva do Codex que demonstre o reconhecimento das instruções de `AGENTS.md`.

---

# GATE-7 — Validação consolidada

## Objetivo

Obter uma visão final do ambiente, diretório, Git root, branch e estado do repositório.

## Procedimento

Execute no terminal integrado do VS Code:

```bash
printf '%s\n' \
  "=== WSL ==="
echo "$WSL_DISTRO_NAME"

printf '%s\n' \
  "=== PWD ==="
pwd

printf '%s\n' \
  "=== GIT ROOT ==="
git rev-parse --show-toplevel

printf '%s\n' \
  "=== BRANCH ==="
git branch --show-current

printf '%s\n' \
  "=== GIT STATUS ==="
git status --short --branch
```

## Resultado esperado

```text
=== WSL ===
Ubuntu

=== PWD ===
/home/<user>/projetos/novo-projeto

=== GIT ROOT ===
/home/<user>/projetos/novo-projeto

=== BRANCH ===
main

=== GIT STATUS ===
## No commits yet on main
?? AGENTS.md
?? CLAUDE.md
```

## Critérios adicionais

Também devem ser comprovados:

```text
VS Code:
WSL: <distro>                       PASS

Claude:
/context
CLAUDE.md carregado                 PASS

Codex:
AGENTS.md reconhecido               PASS
```

Somente depois de todas essas evidências estarem registradas poderá ser declarado:

```text
WORKSPACE_BOOTSTRAP = PASS
```

ou:

```text
WORKSPACE_READY
```

## Estado documental atual

Com base exclusivamente nas evidências presentes no texto fornecido:

```text
GATE-0    PASS
GATE-0.1  PENDING
GATE-1    PENDING
GATE-2    PENDING
GATE-3    PENDING
GATE-4    PENDING
GATE-5    PENDING
GATE-6    PENDING
GATE-7    PENDING
```

Portanto:

```text
WORKSPACE_BOOTSTRAP = PENDING
```

Não há evidência suficiente no documento original para registrar `WORKSPACE_READY = PASS`.

---

# Estado arquitetural pretendido

Quando todos os gates forem validados, a estrutura será:

```text
Windows
│
└── WSL2
    │
    └── /home/<user>/projetos/novo-projeto/
        │
        ├── .git/
        │   └── HEAD → main
        │
        ├── AGENTS.md
        │   └── instruções comuns
        │
        └── CLAUDE.md
            └── @AGENTS.md

VS Code
│
├── Remote = WSL
├── Workspace root = Git root
├── Claude Code
│   └── CLAUDE.md → AGENTS.md
└── Codex
    └── AGENTS.md
```

---

# Fora do escopo deste bootstrap

Ao final deste procedimento ainda NÃO devem ser criados, salvo instrução explícita posterior:

```text
package.json
src/
app/
node_modules/
Dockerfile
docker-compose.yml
compose.yaml
.devcontainer/
devcontainer.json
/workspaces/<projeto>
```

O bootstrap também não decide:

* stack da aplicação;
* framework;
* linguagem de implementação;
* banco de dados;
* arquitetura da aplicação;
* estratégia de containers;
* adoção de Dev Container.

Essas decisões devem ocorrer em etapas posteriores.

---

# Condição de encerramento

O fluxo deste documento termina quando todos os seguintes gates estiverem comprovados:

```text
WORKSPACE_READY
      │
      ├── WSL2          PASS
      ├── DIRECTORY     PASS
      ├── GIT           PASS
      ├── VS CODE       PASS
      ├── CLAUDE        PASS
      └── CODEX         PASS
             │
             ▼
      STOP DO BOOTSTRAP
```

Somente após o `STOP DO BOOTSTRAP` devem ser iniciadas decisões relacionadas à aplicação e, separadamente, à utilização ou não de Dev Containers.

---

# Referências informadas no documento original

As referências abaixo foram preservadas a partir do material de origem e devem ser tratadas como referências técnicas do procedimento:

1. OpenAI — Custom instructions with `AGENTS.md`

   * https://developers.openai.com/codex/guides/agents-md

2. Microsoft — Comandos básicos para WSL

   * https://learn.microsoft.com/pt-br/windows/wsl/basic-commands

3. OpenAI — Codex no WSL

   * https://learn.chatgpt.com/codex/windows/wsl

4. GNU Coreutils

   * https://www.gnu.org/software/coreutils/manual/coreutils.html

5. Microsoft — Trabalhando entre sistemas de arquivos WSL/Windows

   * https://learn.microsoft.com/pt-br/windows/wsl/filesystems

6. Git — `git init`

   * https://git-scm.com/docs/git-init/pt_BR

7. Git — `git rev-parse`

   * https://git-scm.com/docs/git-rev-parse/pt_BR

8. Git — `git branch`

   * https://git-scm.com/docs/git-branch

9. Git — `git status`

   * https://git-scm.com/docs/git-status/pt_BR

10. Visual Studio Code — Command Line Interface

    * https://code.visualstudio.com/docs/configure/command-line

11. Visual Studio Code — Developing in WSL

    * https://code.visualstudio.com/docs/remote/wsl

12. Visual Studio Code — Workspaces

    * https://code.visualstudio.com/docs/editing/workspaces/workspaces

13. GNU Bash — Redirections

    * https://www.gnu.org/s/bash/manual/html_node/Redirections.html

14. Anthropic — Claude Code memory

    * https://code.claude.com/docs/en/memory

15. Anthropic — Claude Code no VS Code

    * https://code.claude.com/docs/en/ide-integrations

16. OpenAI — Codex IDE Extension

    * https://developers.openai.com/codex/ide

17. GNU Bash — Builtins

    * https://www.gnu.org/s/bash/manual/html_node/Bash-Builtins.html

> **Observação:** esta reescrita preserva as referências fornecidas no material original; ela não constitui, por si só, uma nova validação da disponibilidade, versão ou conteúdo atual de cada referência.

---

## 2. Pontos que precisam de esclarecimento

### Público-alvo

> **Informação necessária:** definir formalmente quem utilizará este runbook.

Uma definição adequada pode ser:

```text
Desenvolvedores, arquitetos e responsáveis por DevOps do
CEPRAEA BEACH PRO que executam o bootstrap, validação e
manutenção do ambiente de desenvolvimento.
```

### Nome definitivo do diretório

O documento utiliza:

```text
NOME_DO_PROJETO
```

e:

```text
novo-projeto
```

como placeholders.

> **Informação necessária:** definir se o diretório real será, por exemplo, `cepraea-beach-pro` ou outro nome.

### Evidências dos gates posteriores

Somente `GATE-0` contém logs reais suficientes para comprovação.

Faltam evidências efetivas para:

* entrada na distribuição;
* criação do diretório;
* instalação e configuração do Git;
* inicialização do repositório;
* VS Code conectado ao WSL;
* criação de `AGENTS.md`;
* criação de `CLAUDE.md`;
* carregamento de `CLAUDE.md` pelo Claude;
* reconhecimento de `AGENTS.md` pelo Codex;
* validação consolidada.

### Versionamento das ferramentas

> **Informação necessária:** decidir se o runbook deve registrar explicitamente as versões utilizadas de WSL, Git, VS Code, Claude Code e Codex.

Isso aumentaria a reprodutibilidade do registro.

---

## 3. Problemas encontrados no texto original

### Resultados esperados confundidos com evidências

O principal problema metodológico era apresentar diversos resultados esperados e, ao final, construir uma conclusão:

```text
WORKSPACE_READY
```

sem que todos os gates possuíssem evidência capturada.

Um procedimento pode definir:

```text
resultado esperado = X
```

mas isso não comprova que:

```text
resultado observado = X
```

A reescrita separa esses conceitos.

### Uso prematuro de `PASS`

O documento original utiliza `PASS` como critério e também como resultado conceitual.

Para registro de execução, recomenda-se utilizar:

```text
PASS
FAIL
PENDING
```

e conceder `PASS` somente quando houver evidência.

### Mistura entre runbook e registro de execução

O texto original contém simultaneamente:

* instruções;
* justificativas;
* documentação de referência;
* critérios de teste;
* logs;
* resultados esperados;
* resultados aparentemente executados.

Essa mistura dificulta identificar o que realmente ocorreu.

A reescrita mantém tudo no mesmo documento, mas separa:

```text
Objetivo
Procedimento
Resultado esperado
Evidência
Critério
Status
```

### Conclusões absolutas baseadas em documentação mutável

Expressões como:

```text
A documentação oficial atual diz...
```

podem envelhecer rapidamente.

Quando o requisito depende de comportamento de Codex, Claude, VS Code ou outra ferramenta com atualização frequente, a data e/ou versão da referência deveria ser registrada.

### Identificação incompleta da execução

O material não possui um cabeçalho operacional contendo, por exemplo:

```text
Data da execução
Executor
Host
Distribuição WSL
Versão do VS Code
Versão do Git
Versão do Codex
Versão do Claude Code
Commit/revisão do runbook
```

Sem isso, uma execução futura pode ser confundida com outra.

### Inconsistência entre projeto e exemplo

O sistema é denominado:

```text
CEPRAEA BEACH PRO
```

mas diversos exemplos utilizam:

```text
novo-projeto
```

Isso é válido como exemplo, mas deveria ficar explicitamente marcado como placeholder para evitar que seja interpretado como nome real.

---

## 4. Recomendações opcionais

### Adotar identificador para cada execução

Por exemplo:

```text
EXEC-WS-2026-08-21-001
```

Então o início de um registro poderia conter:

```text
Execução: EXEC-WS-2026-08-21-001
Projeto: CEPRAEA BEACH PRO
Procedimento: Bootstrap do workspace
Ambiente: Windows + WSL2
Status: IN_PROGRESS
```

Isso ajuda bastante quando houver várias máquinas ou reinstalações.

### Separar runbook de evidências no futuro

Para uma estrutura Docs as Code mais escalável:

```text
docs/
├── runbooks/
│   └── workspace-bootstrap.md
│
└── execution-records/
    └── workspace/
        └── EXEC-WS-2026-08-21-001.md
```

O primeiro documento explica **como executar**.

O segundo registra **o que realmente aconteceu**.

Isso evita alterar o procedimento sempre que uma nova execução for realizada.

### Registrar a versão do próprio procedimento

Exemplo:

```text
Documento: Workspace Bootstrap
Versão: 1.0
Revisão: 2026-08-21
```

Assim é possível determinar sob qual versão do procedimento cada evidência foi produzida.

### Utilizar uma tabela consolidada de gates

Ao final de cada registro:

| Gate   | Verificação     | Status  | Evidência        |
| ------ | --------------- | ------- | ---------------- |
| GATE-0 | WSL2            | PASS    | Logs registrados |
| GATE-1 | Diretório Linux | PENDING | —                |
| GATE-2 | Git             | PENDING | —                |
| GATE-3 | VS Code/WSL     | PENDING | —                |
| GATE-4 | Instruções      | PENDING | —                |
| GATE-5 | Claude          | PENDING | —                |
| GATE-6 | Codex           | PENDING | —                |
| GATE-7 | Validação final | PENDING | —                |

Essa tabela torna impossível confundir o **estado planejado** com o **estado efetivamente comprovado**.
