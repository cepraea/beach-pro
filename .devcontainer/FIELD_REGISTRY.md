# FIELD_REGISTRY — `.devcontainer/devcontainer.json`

**Objeto analisado:** configuração `CEPRAEA Agent` fornecida na conversa.  
**Data da revisão:** 2026-08-14.  
**Fonte:** `.devcontainer/devcontainer.json`
**Path:**
**Papel da revisão:** Arquitetura de Metadados + validação semântica contra fontes primárias/especializadas.  
**Escopo:** todos os campos JSON efetivamente presentes, chaves de configuração aninhadas e os parâmetros estruturados embutidos nas strings de `mounts`/`runArgs`.

> **Regra de leitura:** “válido no schema” não significa “necessário”, “seguro” ou “suficiente”. 

*Este registro separa contrato de metadados, efeito operacional e garantia de segurança.*

## 1. Sumário executivo

- Foram registrados **45 metacampos/controles lógicos**: 
- 23 campos/chaves estruturais Dev Container, 8 variáveis de ambiente (cada uma ocorre em `containerEnv` e `remoteEnv`), 7 settings VS Code/extensões, 4 parâmetros de mount e 3 argumentos Docker em `runArgs`.
- O desenho é coerente com um **workspace RW + control-plane RO + agente não-root + hardening Docker**.
- Há um **conflito semântico P0**: os três mounts de `gitconfig-agent` são neutralizados pelas próprias variáveis Git. `GIT_CONFIG_NOSYSTEM=1` ignora `/etc/gitconfig`; `GIT_CONFIG_GLOBAL=/dev/null` substitui tanto `~/.gitconfig` quanto o global XDG. Portanto, hoje esses três mounts não exercem a policy esperada sobre o Git.
- `updateRemoteUserUID:false` é válido, porém requer uma decisão explícita de plataforma/ownership. Em Linux nativo, bind mounts preservam UID/GID do host e um UID fixo do usuário `agent` pode causar `Permission denied` ou `dubious ownership`.
- O alias `runbooks -> /workspaces/cepraea-beach-pro/docs` **obscurece** qualquer `docs/` original nesse target durante a vida do mount. Deve ser tratado como decisão arquitetural, não como alias “gratuito”.
- `--add-host=host.docker.internal:host-gateway` é válido, mas abre uma rota nominal para serviços do host. Só deve existir se houver consumidor real.
- A duplicação integral das 8 variáveis em `containerEnv` e `remoteEnv` é válida, mas cria duas fontes de verdade. Preferência atual: `containerEnv` para requisito global; `remoteEnv` apenas para override/escopo remoto deliberado.
- Tokens vazios, auth settings desativados e prompts bloqueados são **defesa em profundidade**, não prova de “GitHub impossível”. Ausência real de acesso exige também controlar credential stores, SSH, sockets, rede e outros clientes.

## 2. Classificação de conformidade do arquivo atual

| Área | Estado | Decisão arquitetural |
|---|---|---|
| Schema Dev Container | **PASS** | Os campos apresentados pertencem à família de propriedades suportadas; subcampos específicos estão no local correto. |
| Build | **PASS com ressalva** | `context:".."` é apropriado se o Dockerfile precisa da raiz; exige `.dockerignore` rigoroso. |
| Usuário não-root | **PASS condicional** | `remoteUser=containerUser=agent` é coerente; `agent` precisa existir e possuir HOME/permissões adequados. |
| UID/GID | **REVISAR** | `updateRemoteUserUID:false` só deve permanecer com estratégia explícita de ownership. |
| Hardening Docker | **PASS** | `no-new-privileges` + `cap-drop=ALL` são boas camadas; testar compatibilidade funcional. |
| Host networking | **REVISAR** | `host-gateway` só se serviço no host for requisito. |
| Mounts RO | **PASS com conflitos** | Estratégia é boa; três mounts gitconfig são hoje inefetivos e `docs` é obscurecido. |
| Git policy | **FAIL semântico** | Escolher “nenhuma config global/system” OU “config controlada montada”; o arquivo tenta os dois ao mesmo tempo. |
| GitHub/SSH/Docker credentials | **PASS como hardening** | Valores/settings reduzem herança e automação, mas não são boundary completo. |
| Port forwarding | **PASS** | 5173 + `Vite` + `notify` são válidos; `notify` é explícito e atualmente coincide com o default. |
| VS Code customizations | **PASS** | Estrutura correta. IDs de Claude Code e OpenAI Codex estão atualmente válidos. |
| Lifecycle | **PASS** | `postStartCommand` é curto, idempotente e valida writability. |

## 3. Taxonomia de identidade dos campos

| Classe | Exemplos | Autoridade semântica |
|---|---|---|
| Campo core da Dev Container Spec | `build`, `workspaceFolder`, `mounts`, `remoteUser` | Dev Containers Specification |
| Campo tool-specific | `customizations.vscode.*` | Dev Containers supporting tools + VS Code |
| Setting de extensão/IDE | `git.autofetch`, `github.gitAuthentication`, `claudeCode.initialPermissionMode` | VS Code / extensão proprietária |
| Variável de processo | `GIT_*`, `GH_*`, `SSH_AUTH_SOCK`, `DOCKER_HOST` | Ferramenta consumidora (Git/GH/OpenSSH/Docker) |
| Parâmetro embutido de mount | `source`, `target`, `type`, `readonly` | Docker `--mount` |
| Flag embutida de runtime | `--security-opt`, `--cap-drop`, `--add-host` | Docker `run` + kernel Linux |

## 4. Registro canônico de campos

### FR-001 — `name`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `name` |
| **Tradução** | nome |
| **Identidade** | Metadado descritivo de nível raiz do Dev Container. |
| **Tipo de campo** | `string` |
| **Papel** | Identificação humana do ambiente. |
| **Função** | Define o nome apresentado pela ferramenta ao usuário. |
| **Objetivo** | Distinguir o ambiente de outros containers/configurações sem participar da execução. |
| **Preenchimento** | Texto curto, estável e reconhecível; no arquivo: `"CEPRAEA Agent"`. |
| **Obrigatoriedade** | Opcional pelo schema. |
| **Relação com outros campos** | Independente dos campos de build/runtime; pode ser exibido por ferramentas que implementam a especificação. |
| **O que o campo configura** | Somente a identidade visual/descritiva da configuração. |
| **Qual problema o campo resolve** | Evita nomes genéricos e confusão operacional entre ambientes. |
| **Qual a necessidade real do campo** | Alta quando existem múltiplos ambientes; baixa para execução técnica. |
| **O que o campo garante** | Uma identificação humana consistente. |
| **O que o campo **não** garante** | Não garante nome do container Docker, hostname, imagem, segurança nem unicidade global. |
| **Contexto válido** | Nome de produto, papel ou ambiente (`CEPRAEA Agent`, `Backend Dev`). |
| **Contexto inválido** | Usar como identificador de segurança, chave de automação ou pressupor que altere o runtime. |
| **Escopo permitido** | Nível raiz da configuração Dev Container. |
| **Escopo proibido** | Não deve carregar segredo, token, lógica de política ou dados voláteis. |
| **Exemplo de uso correto** | `"name": "CEPRAEA Agent"` |
| **Exemplo de uso incorreto** | `"name": "prod-token-abc123"` |
| **Riscos e edge cases** | Nomes ambíguos, excessivamente longos ou contendo dados sensíveis. |
| **Prevenção de riscos / solução de edge cases** | Usar rótulo estável, sem segredos e alinhado ao propósito. |
| **Borderlines** | Duas configurações podem ter o mesmo `name`; não é chave primária. |
| **Melhores técnicas atuais** | Tratá-lo como metadado de apresentação, não como controle. |
| **Boas práticas** | Nomear por finalidade/escopo e manter estável para reduzir confusão. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1] |

### FR-002 — `build`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `build` |
| **Tradução** | construção |
| **Identidade** | Objeto raiz que descreve a construção de uma imagem a partir de Dockerfile. |
| **Tipo de campo** | `object` |
| **Papel** | Agrupador de metadados de build. |
| **Função** | Seleciona o modo Dockerfile e reúne `dockerfile`, `context` e outras opções de construção suportadas. |
| **Objetivo** | Produzir a imagem usada pelo Dev Container com parâmetros reprodutíveis. |
| **Preenchimento** | Objeto; no arquivo contém `dockerfile` e `context`. |
| **Obrigatoriedade** | Obrigatório quando a configuração é do tipo Dockerfile e não usa `image`/Compose como alternativa. |
| **Relação com outros campos** | Pai de `build.dockerfile` e `build.context`; afeta o que pode ser copiado no Dockerfile. |
| **O que o campo configura** | A etapa de construção da imagem, não a inicialização do container. |
| **Qual problema o campo resolve** | Evita depender de imagem pré-pronta quando há dependências e usuário próprios. |
| **Qual a necessidade real do campo** | Real quando o ambiente precisa de Dockerfile customizado. |
| **O que o campo garante** | Que a ferramenta possui instruções suficientes para acionar um build conforme o schema, desde que os arquivos existam. |
| **O que o campo **não** garante** | Não garante build bem-sucedido, hermeticidade, cache correto, ausência de segredos ou segurança da imagem. |
| **Contexto válido** | Projeto com `.devcontainer/Dockerfile` e dependências próprias. |
| **Contexto inválido** | Misturar mentalmente `build` com `runArgs`; passar opções de runtime como se fossem de build. |
| **Escopo permitido** | Nível raiz, mutuamente condicionado ao modo escolhido. |
| **Escopo proibido** | Não deve conter chaves arbitrárias fora do schema. |
| **Exemplo de uso correto** | `"build": {"dockerfile":"Dockerfile","context":".."}` |
| **Exemplo de uso incorreto** | `"build": "Dockerfile"` |
| **Riscos e edge cases** | Contexto grande, Dockerfile ausente, caminhos relativos mal interpretados. |
| **Prevenção de riscos / solução de edge cases** | Validar no schema e manter contexto mínimo com `.dockerignore`. |
| **Borderlines** | Uma ferramenta pode suportar extensões adicionais do schema, mas portabilidade exige o conjunto oficial. |
| **Melhores técnicas atuais** | Separar build-time de runtime; fixar dependências e minimizar contexto. |
| **Boas práticas** | Manter Dockerfile determinístico, `.dockerignore` rigoroso e contexto menor possível. |
| **Situação no arquivo analisado** | Conforme, com atenção ao contexto `..`. |
| **Fontes** | [S1], [S8] |

### FR-003 — `build.dockerfile`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `build.dockerfile` |
| **Tradução** | arquivo Dockerfile |
| **Identidade** | Subcampo de `build` que aponta para o Dockerfile. |
| **Tipo de campo** | `string` |
| **Papel** | Localização da receita de imagem. |
| **Função** | Informa qual Dockerfile será usado; o caminho é relativo à pasta que contém `devcontainer.json`. |
| **Objetivo** | Selecionar explicitamente a receita correta. |
| **Preenchimento** | Caminho relativo; no arquivo: `"Dockerfile"`, esperado na mesma pasta do `devcontainer.json`. |
| **Obrigatoriedade** | Obrigatório dentro de `build` no modo Dockerfile definido pelo schema. |
| **Relação com outros campos** | Depende de `build`; trabalha com `build.context`. |
| **O que o campo configura** | O arquivo de instruções de construção. |
| **Qual problema o campo resolve** | Evita ambiguidade sobre qual Dockerfile executar. |
| **Qual a necessidade real do campo** | Essencial nesse modo de build. |
| **O que o campo garante** | Seleção determinística do arquivo, se existente e acessível. |
| **O que o campo **não** garante** | Não garante que o Dockerfile seja válido, seguro ou que o contexto contenha os arquivos usados por `COPY`. |
| **Contexto válido** | `.devcontainer/devcontainer.json` ao lado de `.devcontainer/Dockerfile`. |
| **Contexto inválido** | Apontar para arquivo fora do alcance esperado sem validar path/context ou assumir que é relativo ao workspace root. |
| **Escopo permitido** | Somente dentro de `build`. |
| **Escopo proibido** | Não deve ser usado para comandos shell ou imagem pronta. |
| **Exemplo de uso correto** | `"dockerfile": "Dockerfile"` |
| **Exemplo de uso incorreto** | `"dockerfile": ["Dockerfile"]` |
| **Riscos e edge cases** | Renomeações, case sensitivity, caminho relativo incorreto. |
| **Prevenção de riscos / solução de edge cases** | CI deve validar build a partir do mesmo diretório e plataforma. |
| **Borderlines** | Dockerfile pode ter outro nome; a semântica é path, não convenção de nome. |
| **Melhores técnicas atuais** | Preferir caminho simples e explícito; evitar duplicidade de Dockerfiles indistinguíveis. |
| **Boas práticas** | Documentar a relação entre Dockerfile, contexto e `.dockerignore`. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1] |

### FR-004 — `build.context`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `build.context` |
| **Tradução** | contexto de construção |
| **Identidade** | Subcampo de `build` que define o build context do Docker. |
| **Tipo de campo** | `string` |
| **Papel** | Delimitação do conjunto de arquivos visível ao build. |
| **Função** | Define o diretório enviado como contexto ao Docker; caminho relativo à pasta do `devcontainer.json`. |
| **Objetivo** | Permitir `COPY`/`ADD` dos arquivos necessários à construção. |
| **Preenchimento** | No arquivo: `".."`; se o JSON está em `.devcontainer/`, isso normalmente aponta para a raiz do repositório. |
| **Obrigatoriedade** | Opcional no schema; a necessidade depende do Dockerfile. |
| **Relação com outros campos** | Afeta `COPY`/`ADD`, performance, cache e exposição de arquivos ao daemon/build. |
| **O que o campo configura** | Fronteira de arquivos disponíveis durante o build. |
| **Qual problema o campo resolve** | Resolve builds que precisam acessar arquivos fora da pasta `.devcontainer`. |
| **Qual a necessidade real do campo** | Real quando Dockerfile copia lockfiles, scripts ou fontes do repositório. |
| **O que o campo garante** | Disponibilidade, ao build, dos arquivos dentro do contexto e não excluídos. |
| **O que o campo **não** garante** | Não garante que segredos não sejam enviados, nem que `.dockerignore` esteja correto. |
| **Contexto válido** | Contexto raiz quando o Dockerfile precisa de arquivos do projeto. |
| **Contexto inválido** | Usar `..` por conveniência sem necessidade, expondo uma árvore ampla. |
| **Escopo permitido** | Diretório acessível à ferramenta de build. |
| **Escopo proibido** | Não deve apontar para contexto excessivamente amplo ou incluir credenciais/artefatos desnecessários. |
| **Exemplo de uso correto** | `"context": ".."` com `.dockerignore` restritivo. |
| **Exemplo de uso incorreto** | `"context": "/"` para um projeto comum. |
| **Riscos e edge cases** | Build lento, cache invalidado, envio acidental de `.env`, chaves, artefatos grandes. |
| **Prevenção de riscos / solução de edge cases** | Reduzir contexto; manter `.dockerignore`; evitar segredos no contexto. |
| **Borderlines** | Às vezes contexto maior é necessário para monorepo; documentar a razão. |
| **Melhores técnicas atuais** | Princípio do menor contexto e build hermético/reprodutível. |
| **Boas práticas** | Tratar contexto como fronteira de dados, não só conveniência. |
| **Situação no arquivo analisado** | Válido, porém requer auditoria do `.dockerignore`. |
| **Fontes** | [S1], [S8] |

### FR-005 — `workspaceMount`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `workspaceMount` |
| **Tradução** | montagem do workspace |
| **Identidade** | Campo raiz que substitui a montagem padrão do código. |
| **Tipo de campo** | `string` no formato aceito por `docker run --mount` |
| **Papel** | Definição da origem/destino do workspace. |
| **Função** | Instrui a ferramenta a montar `${localWorkspaceFolder}` no caminho alvo como bind mount. |
| **Objetivo** | Controlar exatamente como o repositório host entra no container. |
| **Preenchimento** | String `source=...,target=...,type=bind`; no arquivo é RW por ausência de `readonly`. |
| **Obrigatoriedade** | Opcional; a ferramenta normalmente cria uma montagem padrão. |
| **Relação com outros campos** | Deve ser coerente com `workspaceFolder`; sobreposições de `mounts` podem tornar subárvores RO. |
| **O que o campo configura** | A montagem principal do projeto. |
| **Qual problema o campo resolve** | Permite caminho de workspace estável e composição com overlays read-only. |
| **Qual a necessidade real do campo** | Alta quando a arquitetura depende de path fixo e overlays. |
| **O que o campo garante** | Que o workspace é solicitado no alvo indicado com a semântica de mount correspondente. |
| **O que o campo **não** garante** | Não garante permissões POSIX compatíveis, ownership, isolamento de subpaths nem que todas as ferramentas suportem a mesma estratégia em fluxos especiais. |
| **Contexto válido** | Bind mount de projeto local para um caminho previsível. |
| **Contexto inválido** | Usar target diferente de `workspaceFolder`; depender de bind host em fluxo que trabalha com volume remoto sem verificar suporte. |
| **Escopo permitido** | Nível raiz; sintaxe delegada ao Docker. |
| **Escopo proibido** | Não usar para segredos do host ou caminhos que não devam ser visíveis ao container. |
| **Exemplo de uso correto** | `source=${localWorkspaceFolder},target=/workspaces/cepraea-beach-pro,type=bind` |
| **Exemplo de uso incorreto** | `source=${localWorkspaceFolder},target=/x,type=bind` junto com `workspaceFolder=/y`. |
| **Riscos e edge cases** | UID/GID em Linux, path com vírgulas/espaços, comportamento em Docker Desktop, sobreposição de mounts. |
| **Prevenção de riscos / solução de edge cases** | Alinhar target com `workspaceFolder`; validar em Linux nativo e Desktop; documentar overlays. |
| **Borderlines** | `${localWorkspaceFolder}` depende do fluxo da ferramenta; há cenários de clone-em-volume com limitações. |
| **Melhores técnicas atuais** | Usar mount explícito só quando há necessidade real; preferir semântica portável. |
| **Boas práticas** | Manter a raiz RW apenas se o agente precisa editar código e proteger control-plane com mounts filhos RO. |
| **Situação no arquivo analisado** | Conforme e arquiteturalmente intencional. |
| **Fontes** | [S1], [S5], [S8] |

### FR-006 — `workspaceFolder`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `workspaceFolder` |
| **Tradução** | pasta de trabalho |
| **Identidade** | Campo raiz que define a pasta aberta como workspace dentro do container. |
| **Tipo de campo** | `string` |
| **Papel** | Contexto de trabalho da IDE/agente. |
| **Função** | Aponta para o diretório que a ferramenta deve abrir após a criação/inicialização. |
| **Objetivo** | Fazer terminais, extensões e operações de workspace iniciarem no projeto correto. |
| **Preenchimento** | Caminho absoluto interno; no arquivo `/workspaces/cepraea-beach-pro`. |
| **Obrigatoriedade** | Opcional, mas necessário quando se customiza a montagem e o default não coincide. |
| **Relação com outros campos** | Deve apontar para o `target` de `workspaceMount` ou para uma pasta existente dentro dele. |
| **O que o campo configura** | O diretório de trabalho da experiência remota. |
| **Qual problema o campo resolve** | Evita abrir raiz errada ou pasta inexistente. |
| **Qual a necessidade real do campo** | Alta quando `workspaceMount` é customizado. |
| **O que o campo garante** | Que ferramentas compatíveis tentem abrir esse caminho. |
| **O que o campo **não** garante** | Não cria o diretório, não monta arquivos e não corrige permissões. |
| **Contexto válido** | Path existente e montado no container. |
| **Contexto inválido** | Path inexistente, não montado ou divergente do target principal. |
| **Escopo permitido** | Caminho interno do container. |
| **Escopo proibido** | Não usar host path (`C:\...`, `/Users/...`) como se fosse path interno. |
| **Exemplo de uso correto** | `"workspaceFolder": "/workspaces/cepraea-beach-pro"` |
| **Exemplo de uso incorreto** | `"workspaceFolder": "${localWorkspaceFolder}"` esperando path interno. |
| **Riscos e edge cases** | Mudança de target sem atualizar este campo; symlinks inesperados. |
| **Prevenção de riscos / solução de edge cases** | Testar existência após start e manter um único path canônico. |
| **Borderlines** | Pode apontar para subdiretório legítimo do mount em monorepos. |
| **Melhores técnicas atuais** | Coerência estrutural com montagem principal. |
| **Boas práticas** | Não duplicar aliases desnecessários do workspace. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1], [S5] |

### FR-007 — `remoteUser`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `remoteUser` |
| **Tradução** | usuário remoto |
| **Identidade** | Campo raiz que define o usuário para processos iniciados pela ferramenta remota. |
| **Tipo de campo** | `string` |
| **Papel** | Identidade efetiva de IDE, terminais e lifecycle scripts. |
| **Função** | Faz processos remotos e comandos da ferramenta rodarem como `agent` em vez do usuário padrão da imagem. |
| **Objetivo** | Aplicar princípio do menor privilégio à sessão de desenvolvimento/agente. |
| **Preenchimento** | Nome de usuário existente na imagem; no arquivo `agent`. |
| **Obrigatoriedade** | Opcional; default é o usuário do container/imagem. |
| **Relação com outros campos** | Interage com `containerUser`, `updateRemoteUserUID`, ownership dos bind mounts e lifecycle commands. |
| **O que o campo configura** | Usuário de processos iniciados pelo ambiente remoto. |
| **Qual problema o campo resolve** | Evita executar IDE/agente como root quando não necessário. |
| **Qual a necessidade real do campo** | Alta para sandbox e ownership previsível. |
| **O que o campo garante** | Que os processos abrangidos pela especificação usam o usuário indicado, se ele existir. |
| **O que o campo **não** garante** | Não cria o usuário, não limita capabilities por si só, não impede outros processos do container de terem outro usuário. |
| **Contexto válido** | Usuário não-root criado no Dockerfile com home e permissões corretas. |
| **Contexto inválido** | Nome inexistente ou home não gravável para ferramentas que persistem estado. |
| **Escopo permitido** | Processos remotos/lifecycle definidos pela ferramenta. |
| **Escopo proibido** | Não pressupor que substitui controles Docker de usuário/capabilities. |
| **Exemplo de uso correto** | `"remoteUser": "agent"` |
| **Exemplo de uso incorreto** | `"remoteUser": "nobody"` sem home/permissões quando extensões precisam gravar estado. |
| **Riscos e edge cases** | UID host divergente, HOME incorreto, permissões em volumes. |
| **Prevenção de riscos / solução de edge cases** | Criar usuário na imagem; validar `id`, `$HOME`, ownership e bind mounts. |
| **Borderlines** | Em alguns ambientes somente `remoteUser` é desejado para não alterar o usuário de serviços do container. |
| **Melhores técnicas atuais** | Não-root + UID/GID compatível + permissões mínimas. |
| **Boas práticas** | Manter alinhado ao propósito; não usar root como correção de permissões. |
| **Situação no arquivo analisado** | Conforme; depende de `agent` existir no Dockerfile. |
| **Fontes** | [S1], [S4] |

### FR-008 — `containerUser`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerUser` |
| **Tradução** | usuário do container |
| **Identidade** | Campo raiz que define o usuário com o qual o container é iniciado. |
| **Tipo de campo** | `string` |
| **Papel** | Identidade padrão de runtime do container. |
| **Função** | Solicita que o container inteiro tenha `agent` como usuário padrão de execução. |
| **Objetivo** | Evitar runtime root e alinhar processos gerais ao agente. |
| **Preenchimento** | Nome/UID válido já presente na imagem; no arquivo `agent`. |
| **Obrigatoriedade** | Opcional; default deriva da imagem. |
| **Relação com outros campos** | Mais amplo que `remoteUser`; ambos estão iguais no arquivo, reduzindo divergência. |
| **O que o campo configura** | Usuário padrão do container, equivalente conceitual à seleção de usuário no runtime. |
| **Qual problema o campo resolve** | Reduz exposição de processos iniciados fora do canal da IDE. |
| **Qual a necessidade real do campo** | Alta para hardening se serviços não precisam de root. |
| **O que o campo garante** | Que o container é solicitado com esse usuário. |
| **O que o campo **não** garante** | Não cria o usuário, não corrige ownership, não remove capabilities nem impede escalada se houver outra vulnerabilidade/configuração. |
| **Contexto válido** | Imagem preparada para rodar integralmente como não-root. |
| **Contexto inválido** | Container que exige init/daemon root e não foi adaptado. |
| **Escopo permitido** | Runtime do container. |
| **Escopo proibido** | Não usar para mascarar ausência de modelagem de permissões. |
| **Exemplo de uso correto** | `"containerUser": "agent"` |
| **Exemplo de uso incorreto** | `"containerUser": "agent"` quando `/home/agent` e app pertencem a root e são imutáveis. |
| **Riscos e edge cases** | Entrypoint pode esperar root; portas privilegiadas; volumes com UID divergente. |
| **Prevenção de riscos / solução de edge cases** | Testar entrypoint como `agent`; corrigir ownership no build, não em start privilegiado. |
| **Borderlines** | Pode ser omitido e manter somente `remoteUser` quando serviços precisam de outro usuário. |
| **Melhores técnicas atuais** | Executar com menor privilégio compatível com a aplicação. |
| **Boas práticas** | Se ambos forem usados, documentar por que `containerUser` é necessário além de `remoteUser`. |
| **Situação no arquivo analisado** | Conforme e consistente com `remoteUser`. |
| **Fontes** | [S1], [S4] |

### FR-009 — `updateRemoteUserUID`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `updateRemoteUserUID` |
| **Tradução** | atualizar UID/GID do usuário remoto |
| **Identidade** | Campo raiz Linux-específico que controla ajuste de UID/GID para combinar com o host. |
| **Tipo de campo** | `boolean` |
| **Papel** | Compatibilidade de ownership em bind mounts. |
| **Função** | Quando habilitado em cenários suportados, permite à ferramenta ajustar UID/GID do usuário do container ao usuário local; `false` desativa essa adaptação. |
| **Objetivo** | Evitar conflitos de permissão em arquivos montados do host. |
| **Preenchimento** | Booleano; no arquivo `false`. |
| **Obrigatoriedade** | Opcional; comportamento padrão depende do cenário/ferramenta e é tipicamente habilitado para pasta local em Linux. |
| **Relação com outros campos** | Interage diretamente com `remoteUser`/`containerUser` e `workspaceMount` bind. |
| **O que o campo configura** | Política de remapeamento do usuário remoto em Linux. |
| **Qual problema o campo resolve** | Resolve mismatch de UID/GID entre host e container. |
| **Qual a necessidade real do campo** | Crítica em Linux nativo com bind mounts; menos relevante em alguns Docker Desktop setups. |
| **O que o campo garante** | Com `false`, garante apenas que a ferramenta não faça esse ajuste automático. |
| **O que o campo **não** garante** | Não garante permissões funcionais; não garante ownership seguro; não é controle de segurança isolado. |
| **Contexto válido** | UID do usuário `agent` é deliberadamente pré-alinhado ao host ou ambiente controlado com permissões adequadas. |
| **Contexto inválido** | Host multiusuário/CI com UID variável e workspace não gravável pelo UID fixo. |
| **Escopo permitido** | Ajuste de identidade em runtimes compatíveis. |
| **Escopo proibido** | Não usar `false` apenas por “imutabilidade” sem validar ownership. |
| **Exemplo de uso correto** | `false` quando a imagem usa UID conhecido e o host/volume é compatível. |
| **Exemplo de uso incorreto** | `false` em Linux arbitrário presumindo que bind mount será gravável. |
| **Riscos e edge cases** | `Permission denied`, Git dubious ownership, arquivos criados com dono inesperado. |
| **Prevenção de riscos / solução de edge cases** | Teste `id agent` e `stat`; preferir UID update quando portabilidade host é necessária ou parametrizar UID na imagem. |
| **Borderlines** | Há casos de segurança em que UID fixo é requisito; então as permissões do host devem ser preparadas explicitamente. |
| **Melhores técnicas atuais** | Decidir por threat model e plataforma, não por convenção. |
| **Boas práticas** | Documentar a razão de `false` e validar em Linux nativo. |
| **Situação no arquivo analisado** | Válido, porém é um ponto de risco operacional no arquivo atual. |
| **Fontes** | [S1], [S4], [S8] |

### FR-010 — `runArgs`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `runArgs` |
| **Tradução** | argumentos de execução |
| **Identidade** | Campo raiz com argumentos adicionais passados ao iniciar o container. |
| **Tipo de campo** | `array<string>` |
| **Papel** | Escape hatch de runtime Docker. |
| **Função** | Acrescenta opções de `docker run` necessárias e não representadas por campos de maior nível. |
| **Objetivo** | Aplicar hardening e integração específica do runtime. |
| **Preenchimento** | Lista de argumentos independentes; no arquivo contém `security-opt`, `cap-drop` e `add-host`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Semântica de cada item é delegada ao Docker; pode conflitar com campos de maior nível ou reduzir portabilidade. |
| **O que o campo configura** | Flags de criação/inicialização do container. |
| **Qual problema o campo resolve** | Permite controles não modelados diretamente pelo schema Dev Container. |
| **Qual a necessidade real do campo** | Real para hardening, mas deve ser mínimo. |
| **O que o campo garante** | Que a ferramenta tentará passar os argumentos ao runtime compatível. |
| **O que o campo **não** garante** | Não garante suporte em outros runtimes, nem valida coerência entre flags. |
| **Contexto válido** | Docker local onde essas flags são suportadas. |
| **Contexto inválido** | Ambientes remotos/alternativos que ignoram ou rejeitam flags Docker-específicas. |
| **Escopo permitido** | Runtime Docker da configuração. |
| **Escopo proibido** | Não usar como depósito de todas as opções quando existe campo Dev Container dedicado. |
| **Exemplo de uso correto** | `["--security-opt=no-new-privileges:true","--cap-drop=ALL"]` |
| **Exemplo de uso incorreto** | Colocar `--mount` duplicando `workspaceMount` sem necessidade e causando colisão. |
| **Riscos e edge cases** | Incompatibilidade multiplataforma, flags mutuamente conflitantes, falsa sensação de segurança. |
| **Prevenção de riscos / solução de edge cases** | Preferir propriedades da spec; usar `runArgs` só para gaps e testar o runtime alvo. |
| **Borderlines** | Algumas flags são Linux-only e podem ser no-op/erro fora desse contexto. |
| **Melhores técnicas atuais** | Menor conjunto de flags, explicitamente justificado. |
| **Boas práticas** | Revisar periodicamente se a spec passou a oferecer campo nativo. |
| **Situação no arquivo analisado** | Válido; dois hardenings são bons, `--add-host` exige justificativa. |
| **Fontes** | [S1], [S6] |

### FR-011 — `mounts`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `mounts` |
| **Tradução** | montagens adicionais |
| **Identidade** | Campo raiz para mounts extras além do workspace principal. |
| **Tipo de campo** | `array<object\|string>` |
| **Papel** | Composição de filesystem e persistência. |
| **Função** | Adiciona bind mounts e named volumes; strings seguem semântica de `--mount`. |
| **Objetivo** | Criar overlays read-only do control-plane e volumes persistentes para estado/cache do agente. |
| **Preenchimento** | No arquivo: 19 strings de mount. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Sobrepõe/interage com `workspaceMount`; ordem/targets determinam visibilidade; named volumes persistem além do container. |
| **O que o campo configura** | Fontes adicionais visíveis no filesystem do container. |
| **Qual problema o campo resolve** | Permite proteger subárvores e persistir homes/caches sem colocar tudo no workspace. |
| **Qual a necessidade real do campo** | Alta para a arquitetura atual. |
| **O que o campo garante** | Que mounts solicitados serão aplicados se sources/volumes forem válidos. |
| **O que o campo **não** garante** | Não garante isolamento completo; mount RO não impede leitura/exfiltração; named volume não é criptografia. |
| **Contexto válido** | Subpaths controlados RO, caches/estado em named volumes. |
| **Contexto inválido** | Montar socket Docker, secrets desnecessários, host root ou paths sensíveis. |
| **Escopo permitido** | Filesystem do container conforme cada target. |
| **Escopo proibido** | Evitar mounts privilegiados e colisões não documentadas. |
| **Exemplo de uso correto** | Mounts do arquivo atual, com `readonly` para control-plane e volumes para `.claude/.codex/.npm`. |
| **Exemplo de uso incorreto** | `source=/,target=/host,type=bind` em sandbox de agente. |
| **Riscos e edge cases** | Mount over obscure conteúdo existente; persistência de credenciais; source ausente; path collision. |
| **Prevenção de riscos / solução de edge cases** | Inventariar target/source, classificar RW/RO, minimizar host exposure, limpar volumes quando necessário. |
| **Borderlines** | String form é apropriada quando se precisa de opções Docker adicionais como `readonly`; objeto do schema tem conjunto mais restrito. |
| **Melhores técnicas atuais** | Tratar cada mount como permissão de dados explícita. |
| **Boas práticas** | Boa estratégia geral; há conflito semântico nos mounts de gitconfig e colisão deliberada/duvidosa em `docs`. |
| **Situação no arquivo analisado** | Válido com ressalvas: revisar gitconfig e o target `docs`. |
| **Fontes** | [S1], [S7], [S8] |

### FR-012 — `containerEnv`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv` |
| **Tradução** | variáveis de ambiente do container |
| **Identidade** | Mapa raiz de variáveis aplicadas ao container. |
| **Tipo de campo** | `object<string,string>` |
| **Papel** | Configuração ambiental ampla. |
| **Função** | Define variáveis disponíveis no container inteiro em cenários Dockerfile/image suportados. |
| **Objetivo** | Estabelecer comportamento comum de Git/GH/Docker/SSH para todos os processos. |
| **Preenchimento** | Mapa nome→string; no arquivo 8 variáveis. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Mais amplo que `remoteEnv`; valores aqui normalmente já alcançam processos remotos, salvo overrides/contextos específicos. |
| **O que o campo configura** | Ambiente do container. |
| **Qual problema o campo resolve** | Centraliza defaults de ferramentas e reduz dependência do host. |
| **Qual a necessidade real do campo** | Alta quando variáveis devem valer para qualquer processo. |
| **O que o campo garante** | Que os processos do container recebem os valores conforme runtime. |
| **O que o campo **não** garante** | Não garante política de segurança; variáveis podem ser sobrescritas em subprocessos e não substituem isolamento estrutural. |
| **Contexto válido** | Configurações não-secretas e estáveis, necessárias globalmente. |
| **Contexto inválido** | Segredos hardcoded ou valores cujo escopo deveria ser só IDE/lifecycle. |
| **Escopo permitido** | Todos os processos do container abrangidos pelo runtime. |
| **Escopo proibido** | Não usar para armazenar credenciais em plaintext no repositório. |
| **Exemplo de uso correto** | `"GIT_TERMINAL_PROMPT":"0"` para todos os processos. |
| **Exemplo de uso incorreto** | `"GITHUB_TOKEN":"token-real"` versionado no JSON. |
| **Riscos e edge cases** | Duplicação com `remoteEnv`, drift, exposição em processos/diagnósticos. |
| **Prevenção de riscos / solução de edge cases** | Preferir `containerEnv` quando o requisito é global; usar secrets manager para segredo. |
| **Borderlines** | Nem todas as ferramentas de Dev Container tratam Docker Compose da mesma forma; em Compose, env amplo pertence ao Compose. |
| **Melhores técnicas atuais** | Escopo mínimo e valor não sensível. |
| **Boas práticas** | Evitar duplicar automaticamente em `remoteEnv`; duplicar somente com razão documentada. |
| **Situação no arquivo analisado** | Válido; a duplicação integral com `remoteEnv` é redundante/arriscada a drift. |
| **Fontes** | [S1], [S3] |

### FR-013 — `remoteEnv`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `remoteEnv` |
| **Tradução** | variáveis de ambiente remotas |
| **Identidade** | Mapa raiz de variáveis para processos iniciados pela ferramenta remota. |
| **Tipo de campo** | `object<string,string\|null>` |
| **Papel** | Configuração ambiental de IDE/lifecycle/terminal remoto. |
| **Função** | Define/override variáveis para lifecycle scripts, servidor da ferramenta e subprocessos remotos. |
| **Objetivo** | Aplicar configuração apenas ao plano remoto sem alterar todo o container. |
| **Preenchimento** | Mapa nome→valor; no arquivo repete as mesmas 8 variáveis de `containerEnv`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Pode referenciar valores do ambiente do container; é mais estreito que `containerEnv`. |
| **O que o campo configura** | Ambiente de processos remotos. |
| **Qual problema o campo resolve** | Permite diferenças deliberadas entre runtime geral e sessão do desenvolvedor/agente. |
| **Qual a necessidade real do campo** | Real quando o escopo precisa ser remoto; baixa quando apenas duplica `containerEnv`. |
| **O que o campo garante** | Que processos abrangidos pela ferramenta recebem os overrides. |
| **O que o campo **não** garante** | Não garante que processos externos ao servidor remoto recebam os valores; não é política infalível. |
| **Contexto válido** | Override de PATH/variável específica da IDE ou lifecycle. |
| **Contexto inválido** | Duplicar sem razão todas as variáveis globais, criando duas fontes de verdade. |
| **Escopo permitido** | Servidor remoto, lifecycle commands, terminais/processos iniciados pela ferramenta. |
| **Escopo proibido** | Não pressupor alcance sobre daemons/entrypoint já iniciados fora desse escopo. |
| **Exemplo de uso correto** | `"remoteEnv":{"MY_TOOL_MODE":"agent"}` quando só sessão remota precisa disso. |
| **Exemplo de uso incorreto** | Copiar mecanicamente todo `containerEnv` sem governança. |
| **Riscos e edge cases** | Drift entre mapas, confusão sobre precedência, comportamento diferente em ferramentas. |
| **Prevenção de riscos / solução de edge cases** | Escolher uma fonte canônica; usar `remoteEnv` apenas para override/escopo remoto. |
| **Borderlines** | Duplicação pode ser intencional para tornar política explícita, mas deve ter teste de igualdade ou comentário fora do JSON. |
| **Melhores técnicas atuais** | Single source of truth e escopo mínimo. |
| **Boas práticas** | Se duplicar por defesa, automatizar validação para impedir divergência. |
| **Situação no arquivo analisado** | Válido, mas atualmente redundante com `containerEnv`. |
| **Fontes** | [S1], [S3] |

### FR-014 — `forwardPorts`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `forwardPorts` |
| **Tradução** | portas encaminhadas |
| **Identidade** | Lista de portas que a ferramenta deve encaminhar do container. |
| **Tipo de campo** | `array<integer\|string>` |
| **Papel** | Conectividade da experiência de desenvolvimento. |
| **Função** | Solicita port forwarding para serviços internos; aqui, porta 5173. |
| **Objetivo** | Tornar o servidor Vite acessível ao usuário sem exigir publicação Docker manual. |
| **Preenchimento** | Inteiro 0–65535 ou forma host:port prevista no schema; atual `[5173]`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Pode ser enriquecido por `portsAttributes["5173"]`; exige que um processo realmente escute na porta. |
| **O que o campo configura** | Encaminhamento feito pela ferramenta de Dev Container. |
| **Qual problema o campo resolve** | Resolve acesso ao dev server dentro do container. |
| **Qual a necessidade real do campo** | Alta para UX se Vite roda em 5173. |
| **O que o campo garante** | Solicitação de encaminhamento em ferramenta compatível. |
| **O que o campo **não** garante** | Não abre automaticamente a aplicação, não inicia o serviço, não garante bind em `0.0.0.0` nem segurança do serviço. |
| **Contexto válido** | Porta de dev server necessária durante desenvolvimento. |
| **Contexto inválido** | Encaminhar bancos/admin interfaces sem necessidade ou assumir equivalência a `docker -p`. |
| **Escopo permitido** | Portas de desenvolvimento explicitamente necessárias. |
| **Escopo proibido** | Evitar portas sensíveis ou não usadas. |
| **Exemplo de uso correto** | `"forwardPorts":[5173]` |
| **Exemplo de uso incorreto** | `"forwardPorts":["vite"]` |
| **Riscos e edge cases** | Porta em uso no host, serviço bindado só em interface incompatível, exposição inesperada pela ferramenta. |
| **Prevenção de riscos / solução de edge cases** | Usar portas mínimas e definir atributos; autenticar serviços sensíveis. |
| **Borderlines** | O mecanismo exato de exposição ao host depende da ferramenta. |
| **Melhores técnicas atuais** | Forwarding explícito em vez de publicar toda faixa de portas. |
| **Boas práticas** | Associar rótulo e comportamento de auto-forward apenas onde agrega UX. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1] |

### FR-015 — `portsAttributes`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `portsAttributes` |
| **Tradução** | atributos de portas |
| **Identidade** | Mapa de metadados e comportamento para portas/intervalos. |
| **Tipo de campo** | `object` com chaves seletoras |
| **Papel** | Política de UX de portas encaminhadas. |
| **Função** | Configura atributos por porta, faixa ou regex, como rótulo e ação de auto-forward. |
| **Objetivo** | Dar significado e comportamento previsível à porta 5173. |
| **Preenchimento** | Objeto; atual possui a chave dinâmica `"5173"`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Complementa `forwardPorts`, embora também possa descrever portas detectadas automaticamente. |
| **O que o campo configura** | Metadados de forwarding, não rede Docker. |
| **Qual problema o campo resolve** | Evita notificações/rótulos genéricos. |
| **Qual a necessidade real do campo** | Útil para UX; não necessária para conectividade básica. |
| **O que o campo garante** | Comportamento de apresentação/auto-forward conforme ferramenta. |
| **O que o campo **não** garante** | Não garante abertura da porta nem segurança do serviço. |
| **Contexto válido** | Portas conhecidas do projeto. |
| **Contexto inválido** | Usar como ACL/firewall. |
| **Escopo permitido** | Configuração de UX da ferramenta. |
| **Escopo proibido** | Não colocar segredos ou assumir controle de socket/listener. |
| **Exemplo de uso correto** | `"portsAttributes":{"5173":{"label":"Vite","onAutoForward":"notify"}}` |
| **Exemplo de uso incorreto** | Usar `portsAttributes` esperando bloquear tráfego. |
| **Riscos e edge cases** | Chaves regex/range mal especificadas; divergência com porta real. |
| **Prevenção de riscos / solução de edge cases** | Manter seletores simples e sincronizados com scripts da aplicação. |
| **Borderlines** | Uma porta pode ser auto-detectada mesmo sem constar em `forwardPorts`, dependendo da ferramenta. |
| **Melhores técnicas atuais** | Usar para UX e explicitude, não para segurança. |
| **Boas práticas** | Documentar só portas relevantes. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1] |

### FR-016 — `portsAttributes["5173"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `portsAttributes["5173"]` |
| **Tradução** | regra da porta 5173 |
| **Identidade** | Chave dinâmica de instância dentro de `portsAttributes`; não é nome de campo fixo do schema. |
| **Tipo de campo** | `object` |
| **Papel** | Seletor de política para uma porta específica. |
| **Função** | Aplica atributos exclusivamente à porta 5173. |
| **Objetivo** | Associar metadados ao servidor Vite. |
| **Preenchimento** | Chave string que representa porta/faixa/regex válida; aqui `"5173"`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Filho de `portsAttributes`; deve corresponder à porta usada/encaminhada. |
| **O que o campo configura** | A regra de UX da porta selecionada. |
| **Qual problema o campo resolve** | Evita aplicar atributos globalmente a outras portas. |
| **Qual a necessidade real do campo** | Útil quando há múltiplos serviços. |
| **O que o campo garante** | Escopo seletivo dos atributos. |
| **O que o campo **não** garante** | Não reserva a porta e não valida que Vite realmente use 5173. |
| **Contexto válido** | Porta fixa e conhecida. |
| **Contexto inválido** | Chave desatualizada após mudar config do Vite. |
| **Escopo permitido** | Somente no mapa `portsAttributes`. |
| **Escopo proibido** | Não tratar como propriedade universal chamada literalmente “5173”. |
| **Exemplo de uso correto** | `"5173": {...}` |
| **Exemplo de uso incorreto** | `"Vite": {...}` esperando que nome seja convertido em porta. |
| **Riscos e edge cases** | Drift entre app e Dev Container. |
| **Prevenção de riscos / solução de edge cases** | Centralizar a porta em documentação/teste ou atualizar em conjunto. |
| **Borderlines** | Ranges/regex são válidos quando várias portas compartilham política. |
| **Melhores técnicas atuais** | Seletor mais específico possível. |
| **Boas práticas** | Evitar regras amplas se só uma porta é necessária. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1] |

### FR-017 — `portsAttributes["5173"].label`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `portsAttributes["5173"].label` |
| **Tradução** | rótulo |
| **Identidade** | Subcampo de apresentação da regra de porta. |
| **Tipo de campo** | `string` |
| **Papel** | Nome humano do serviço. |
| **Função** | Exibe um rótulo como `Vite` na UI de portas. |
| **Objetivo** | Facilitar reconhecimento do serviço. |
| **Preenchimento** | Texto curto; atual `"Vite"`. |
| **Obrigatoriedade** | Opcional; há default genérico. |
| **Relação com outros campos** | Pertence à regra `5173`. |
| **O que o campo configura** | Somente apresentação da porta. |
| **Qual problema o campo resolve** | Evita identificar serviço apenas por número. |
| **Qual a necessidade real do campo** | UX. |
| **O que o campo garante** | Rótulo legível. |
| **O que o campo **não** garante** | Não muda a porta, protocolo, processo ou segurança. |
| **Contexto válido** | Nome do serviço real. |
| **Contexto inválido** | Rótulo enganoso/desatualizado. |
| **Escopo permitido** | UI da ferramenta. |
| **Escopo proibido** | Não usar como identificador técnico. |
| **Exemplo de uso correto** | `"label":"Vite"` |
| **Exemplo de uso incorreto** | `"label":"Production DB"` para uma porta Vite. |
| **Riscos e edge cases** | Drift semântico. |
| **Prevenção de riscos / solução de edge cases** | Atualizar junto com serviço/porta. |
| **Borderlines** | Pode haver múltiplos Vite servers; use rótulo mais específico se necessário. |
| **Melhores técnicas atuais** | Rótulos curtos e inequívocos. |
| **Boas práticas** | Nomear por serviço, não por pessoa/máquina. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1] |

### FR-018 — `portsAttributes["5173"].onAutoForward`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `portsAttributes["5173"].onAutoForward` |
| **Tradução** | ação ao encaminhar automaticamente |
| **Identidade** | Subcampo enum que controla reação da UI ao detectar/encaminhar porta. |
| **Tipo de campo** | `string enum` |
| **Papel** | Comportamento de notificação/abertura. |
| **Função** | Seleciona entre comportamentos suportados; atual `notify`. |
| **Objetivo** | Informar sem abrir navegador automaticamente. |
| **Preenchimento** | Um valor permitido pelo schema (`notify`, `openBrowser`, `openBrowserOnce`, `openPreview`, `silent`, `ignore`, conforme versão da spec). |
| **Obrigatoriedade** | Opcional; `notify` é o default no schema atual. |
| **Relação com outros campos** | Pertence à regra de porta; complementa `label`. |
| **O que o campo configura** | Reação da ferramenta ao auto-forward. |
| **Qual problema o campo resolve** | Evita popups/aberturas automáticas indesejadas ou ausência de feedback. |
| **Qual a necessidade real do campo** | UX. |
| **O que o campo garante** | Que a ferramenta usa a ação suportada quando auto-forward ocorre. |
| **O que o campo **não** garante** | Não garante que a porta será detectada/encaminhada nem que notificação será entregue fora da UI. |
| **Contexto válido** | Dev server onde notificação basta. |
| **Contexto inválido** | Usar `ignore` esperando firewall; é somente comportamento de auto-forward/UI. |
| **Escopo permitido** | Ferramenta compatível. |
| **Escopo proibido** | Não tratar enum como política de rede. |
| **Exemplo de uso correto** | `"onAutoForward":"notify"` |
| **Exemplo de uso incorreto** | `"onAutoForward":"deny"` (valor não previsto pelo schema). |
| **Riscos e edge cases** | Mudanças de enum entre versões, preferência do usuário/managed settings. |
| **Prevenção de riscos / solução de edge cases** | Validar contra schema atual. |
| **Borderlines** | `notify` explícito é redundante, mas documenta intenção. |
| **Melhores técnicas atuais** | Escolher a ação menos intrusiva compatível com workflow. |
| **Boas práticas** | Deixar explícito quando a política de UX é importante. |
| **Situação no arquivo analisado** | Conforme; valor válido e igual ao default atual. |
| **Fontes** | [S1] |

### FR-019 — `customizations`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations` |
| **Tradução** | customizações |
| **Identidade** | Objeto raiz para propriedades específicas de ferramentas consumidoras da spec. |
| **Tipo de campo** | `object` |
| **Papel** | Namespace de extensões por ferramenta. |
| **Função** | Agrupa configuração que não pertence ao core portável; cada ferramenta usa sua chave própria. |
| **Objetivo** | Permitir customizar VS Code sem poluir o schema core. |
| **Preenchimento** | Objeto; no arquivo contém `vscode`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Filho raiz; suas subchaves podem ser ignoradas por ferramentas que não as implementam. |
| **O que o campo configura** | Configuração tool-specific. |
| **Qual problema o campo resolve** | Resolve extensibilidade sem tornar todo detalhe de IDE parte da spec central. |
| **Qual a necessidade real do campo** | Alta para experiências específicas, baixa para runtime. |
| **O que o campo garante** | Isolamento semântico das opções VS Code. |
| **O que o campo **não** garante** | Não garante que outra IDE aplique esses valores. |
| **Contexto válido** | Configuração destinada ao VS Code. |
| **Contexto inválido** | Colocar flags Docker ou controles de segurança core aqui. |
| **Escopo permitido** | Somente namespaces de ferramentas compatíveis. |
| **Escopo proibido** | Não pressupor portabilidade entre IDEs. |
| **Exemplo de uso correto** | `"customizations":{"vscode":{...}}` |
| **Exemplo de uso incorreto** | `"customizations":{"docker":{"capDrop":"ALL"}}` sem extensão/spec correspondente. |
| **Riscos e edge cases** | Vendor lock-in, opções ignoradas silenciosamente. |
| **Prevenção de riscos / solução de edge cases** | Separar controles de segurança/runtime do UX da IDE. |
| **Borderlines** | Algumas ferramentas podem compartilhar conceitos, mas cada namespace tem contrato próprio. |
| **Melhores técnicas atuais** | Core para runtime; customizations para tooling. |
| **Boas práticas** | Documentar quais controles são apenas de IDE. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S1], [S2] |

### FR-020 — `customizations.vscode`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode` |
| **Tradução** | customizações do VS Code |
| **Identidade** | Namespace específico do VS Code em `customizations`. |
| **Tipo de campo** | `object` |
| **Papel** | Configuração da experiência VS Code dentro do container. |
| **Função** | Agrupa `settings`, `extensions` e outras propriedades reconhecidas pelo suporte VS Code. |
| **Objetivo** | Provisionar IDE coerente para o projeto/agente. |
| **Preenchimento** | Objeto; atual contém `settings` e `extensions`. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Só tem efeito em ferramentas que implementam esse namespace. |
| **O que o campo configura** | VS Code remoto, não Docker. |
| **Qual problema o campo resolve** | Automatiza setup de editor/extensões. |
| **Qual a necessidade real do campo** | Real para onboarding/consistência. |
| **O que o campo garante** | Configuração preferencial da experiência VS Code. |
| **O que o campo **não** garante** | Não garante enforcement contra User/Policy settings de maior precedência nem aplicação em outras IDEs. |
| **Contexto válido** | Equipe usa VS Code Dev Containers/Codespaces compatível. |
| **Contexto inválido** | Considerar isso uma barreira de segurança universal. |
| **Escopo permitido** | VS Code. |
| **Escopo proibido** | Não colocar segredos ou regras que precisam valer fora do VS Code. |
| **Exemplo de uso correto** | `"vscode":{"settings":{},"extensions":[]}` |
| **Exemplo de uso incorreto** | Usar `vscode` para controlar capabilities Linux. |
| **Riscos e edge cases** | Extensões indisponíveis/offline, settings deprecated. |
| **Prevenção de riscos / solução de edge cases** | Pin/validar IDs e revisar settings em upgrades do VS Code/extensões. |
| **Borderlines** | Algumas settings são machine/resource scoped e sua precedência depende do VS Code. |
| **Melhores técnicas atuais** | Automatizar defaults, não políticas de segurança. |
| **Boas práticas** | Distinguir preferências de IDE de controles do container. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S2] |

### FR-021 — `customizations.vscode.settings`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings` |
| **Tradução** | configurações do VS Code |
| **Identidade** | Mapa de settings aplicados como defaults/configuração do ambiente remoto. |
| **Tipo de campo** | `object` |
| **Papel** | Preferências e integrações da IDE. |
| **Função** | Define settings do VS Code para o contexto do container, incluindo terminal e integrações Git/Claude. |
| **Objetivo** | Tornar o comportamento da IDE previsível e reduzir autenticação automática. |
| **Preenchimento** | Objeto chave→valor conforme contratos dos respectivos settings. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Cada chave tem contrato próprio; pode ser sobrescrita conforme escopo/precedência do VS Code. |
| **O que o campo configura** | Comportamento do VS Code/extensões, não do Git/Docker diretamente. |
| **Qual problema o campo resolve** | Resolve setup manual e inconsistência de UX. |
| **Qual a necessidade real do campo** | Alta para experiência; limitada para segurança. |
| **O que o campo garante** | Defaults/valores aplicados pela IDE quando suportados. |
| **O que o campo **não** garante** | Não garante enforcement absoluto, especialmente contra CLI fora da integração da IDE. |
| **Contexto válido** | Preferências de terminal, Git extension, GitHub extension, Claude extension. |
| **Contexto inválido** | Guardar secrets ou confiar em settings como sandbox primário. |
| **Escopo permitido** | VS Code remoto. |
| **Escopo proibido** | Não extrapolar efeitos para outros clientes/processos. |
| **Exemplo de uso correto** | Configurar `git.autofetch:false` para evitar fetch automático pela extensão. |
| **Exemplo de uso incorreto** | Achar que `github.gitAuthentication:false` impede qualquer autenticação GitHub no container. |
| **Riscos e edge cases** | Settings renomeados/deprecated; precedência; extensão não instalada. |
| **Prevenção de riscos / solução de edge cases** | Validar IDs/settings na versão alvo e manter controles estruturais separados. |
| **Borderlines** | Managed settings podem ter precedência em ambientes corporativos. |
| **Melhores técnicas atuais** | Settings como camada UX/defesa em profundidade, nunca única barreira. |
| **Boas práticas** | Revisar periodicamente junto às versões das extensões. |
| **Situação no arquivo analisado** | Conforme; semântica de segurança deve ser entendida como defense-in-depth. |
| **Fontes** | [S2], [S13], [S14], [S15] |

### FR-022 — `customizations.vscode.extensions`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.extensions` |
| **Tradução** | extensões do VS Code |
| **Identidade** | Lista de identificadores de extensões a instalar no ambiente remoto. |
| **Tipo de campo** | `array<string>` |
| **Papel** | Provisionamento de tooling. |
| **Função** | Solicita instalação das extensões `anthropic.claude-code` e `openai.chatgpt`. |
| **Objetivo** | Disponibilizar agentes/assistentes de código no container sem setup manual. |
| **Preenchimento** | IDs `publisher.extension`; atuais são identificadores válidos no Marketplace. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Extensões podem ler workspace/usar rede conforme suas permissões e configurações; interagem com `settings`. |
| **O que o campo configura** | Tooling da IDE remota. |
| **Qual problema o campo resolve** | Resolve consistência de ferramentas entre desenvolvedores/containers. |
| **Qual a necessidade real do campo** | Alta para o propósito “Agent”. |
| **O que o campo garante** | Solicitação de instalação em VS Code compatível com acesso ao marketplace/cache. |
| **O que o campo **não** garante** | Não garante instalação offline, versão específica, login, disponibilidade do serviço ou isolamento. |
| **Contexto válido** | Ambiente em que essas extensões são aprovadas. |
| **Contexto inválido** | Incluir extensões não auditadas ou assumir que ID fixa versão. |
| **Escopo permitido** | VS Code remoto. |
| **Escopo proibido** | Evitar extensões desnecessárias em ambiente sensível. |
| **Exemplo de uso correto** | `["anthropic.claude-code","openai.chatgpt"]` |
| **Exemplo de uso incorreto** | `["claude","chatgpt"]` como nomes informais. |
| **Riscos e edge cases** | Supply chain, updates automáticos, mudança de comportamento, indisponibilidade de marketplace. |
| **Prevenção de riscos / solução de edge cases** | Governar allowlist, revisar publishers e políticas de atualização; usar controles estruturais do container. |
| **Borderlines** | O schema lista IDs, não versões; políticas corporativas podem controlar instalação/versão. |
| **Melhores técnicas atuais** | Menor conjunto de extensões; publishers oficiais; revisão contínua. |
| **Boas práticas** | Não dar a extensão mais privilégio de filesystem/rede do que o necessário. |
| **Situação no arquivo analisado** | Conforme; ambos os IDs são atualmente válidos/oficiais. |
| **Fontes** | [S2], [S16], [S17], [S18] |

### FR-023 — `postStartCommand`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `postStartCommand` |
| **Tradução** | comando pós-inicialização |
| **Identidade** | Lifecycle hook executado após o container iniciar, após `postCreateCommand` e antes de `postAttachCommand`. |
| **Tipo de campo** | `string \| array \| object` |
| **Papel** | Inicialização idempotente e health check. |
| **Função** | Executa `install -d -m 0700 /home/agent/.claude/plans && test -w ...` a cada start. |
| **Objetivo** | Garantir que o diretório de planos exista, tenha permissão restrita e seja gravável. |
| **Preenchimento** | String shell atual; deve ser idempotente porque roda em cada start. |
| **Obrigatoriedade** | Opcional. |
| **Relação com outros campos** | Executa no contexto do usuário remoto conforme lifecycle; depende dos mounts/ownership de `/home/agent/.claude`. |
| **O que o campo configura** | Estado pós-start do filesystem do agente. |
| **Qual problema o campo resolve** | Corrige/valida diretório persistente que pode vir de named volume. |
| **Qual a necessidade real do campo** | Real para Claude quando precisa gravar planos. |
| **O que o campo garante** | Falha o lifecycle se o diretório não puder ser criado/testado; `0700` restringe o diretório criado/ajustado pelo `install`. |
| **O que o campo **não** garante** | Não garante segurança de todo `/home/agent/.claude`, nem ausência de dados sensíveis, nem que `install` exista em toda imagem. |
| **Contexto válido** | Imagem Linux com utilitário `install`, home gravável pelo `agent`. |
| **Contexto inválido** | Comando destrutivo, não idempotente ou dependente de rede em todo start. |
| **Escopo permitido** | Lifecycle do Dev Container. |
| **Escopo proibido** | Não usar para migrações irreversíveis ou segredo inline. |
| **Exemplo de uso correto** | Comando atual é um padrão razoável de ensure+assert. |
| **Exemplo de uso incorreto** | `postStartCommand: "sudo chmod -R 777 /home/agent"`. |
| **Riscos e edge cases** | Utilitário ausente, volume com ownership incompatível, shell differences, falha bloqueando attach. |
| **Prevenção de riscos / solução de edge cases** | Manter curto/idempotente; testar pré-condições; corrigir ownership no build/volume quando possível. |
| **Borderlines** | Se o volume persistente foi criado com UID antigo, pode exigir migração controlada de ownership fora desse hook. |
| **Melhores técnicas atuais** | Lifecycle hooks como checks determinísticos, não como scripts de bootstrap ilimitados. |
| **Boas práticas** | Falhar cedo em invariantes essenciais e manter permissões mínimas. |
| **Situação no arquivo analisado** | Conforme e útil. |
| **Fontes** | [S1], [S4] |

### FR-024 — `containerEnv.GIT_CONFIG_GLOBAL` / `remoteEnv.GIT_CONFIG_GLOBAL`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.GIT_CONFIG_GLOBAL` / `remoteEnv.GIT_CONFIG_GLOBAL` |
| **Tradução** | caminho da configuração global do Git |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Define qual arquivo Git considera como configuração global; quando setado, substitui a busca normal por `~/.gitconfig` e `$XDG_CONFIG_HOME/git/config`. |
| **Objetivo** | Controlar ou suprimir toda configuração Git global herdada. |
| **Preenchimento** | Atual: `/dev/null`. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Fonte de configuração global do Git. |
| **Qual problema o campo resolve** | Evita herdar configuração global do usuário/volume. |
| **Qual a necessidade real do campo** | Alta se a política exige Git sem config global. |
| **O que o campo garante** | Com `/dev/null`, o Git ignora os arquivos globais normais. |
| **O que o campo **não** garante** | Não impede configuração de repositório (`.git/config`), `-c`, env específica, nem outras fontes permitidas; e torna inúteis os mounts de `/home/agent/.gitconfig` e XDG. |
| **Contexto válido** | Quando a intenção é explicitamente “nenhuma configuração global”. |
| **Contexto inválido** | Quando se monta `gitconfig-agent` como política global e se espera que ele seja lido. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `GIT_CONFIG_GLOBAL=/dev/null` + remover mounts globais redundantes. |
| **Exemplo de uso incorreto** | `GIT_CONFIG_GLOBAL=/dev/null` + esperar que `/home/agent/.gitconfig` governe o Git. |
| **Riscos e edge cases** | Conflito semântico atual; falsa sensação de policy enforcement via arquivo montado. |
| **Prevenção de riscos / solução de edge cases** | Escolher UM modelo: (A) no-global: `/dev/null` e remover 2 mounts globais; ou (B) controlled-global: apontar `GIT_CONFIG_GLOBAL=/home/agent/.gitconfig` e manter esse mount RO. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | CONFLITO: atualmente anula dois mounts de `gitconfig-agent`. |
| **Fontes** | [S9] |

### FR-025 — `containerEnv.GIT_TERMINAL_PROMPT` / `remoteEnv.GIT_TERMINAL_PROMPT`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.GIT_TERMINAL_PROMPT` / `remoteEnv.GIT_TERMINAL_PROMPT` |
| **Tradução** | prompt de terminal do Git |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Controla se Git pode pedir credenciais pelo terminal; `0` desabilita o prompt terminal. |
| **Objetivo** | Evitar bloqueio/entrada interativa de credenciais em automação/agente. |
| **Preenchimento** | Atual: `"0"`. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Interatividade de autenticação do Git. |
| **Qual problema o campo resolve** | Evita prompts inesperados e hangs de automação. |
| **Qual a necessidade real do campo** | Alta para agente não interativo. |
| **O que o campo garante** | Git não solicitará credenciais via terminal quando esse mecanismo é consultado. |
| **O que o campo **não** garante** | Não desativa helpers, askpass, SSH keys, tokens já disponíveis ou autenticação feita por outras ferramentas. |
| **Contexto válido** | Agente/CI onde credenciais interativas são proibidas. |
| **Contexto inválido** | Ambiente humano que depende de prompt interativo e não tem outro fluxo de auth. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `GIT_TERMINAL_PROMPT=0` combinado com askpass/auth integration desabilitados. |
| **Exemplo de uso incorreto** | Achar que isso sozinho torna `git push` impossível. |
| **Riscos e edge cases** | Operações podem falhar imediatamente ou ainda autenticar por helper/chave. |
| **Prevenção de riscos / solução de edge cases** | Combinar com ausência de credenciais, config de helpers controlada e `.git` RO se writes Git são proibidos. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | Conforme e coerente com sandbox; não é barreira única. |
| **Fontes** | [S9] |

### FR-026 — `containerEnv.GH_CONFIG_DIR` / `remoteEnv.GH_CONFIG_DIR`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.GH_CONFIG_DIR` / `remoteEnv.GH_CONFIG_DIR` |
| **Tradução** | diretório de configuração do GitHub CLI |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Redireciona onde `gh` procura/grava sua configuração. |
| **Objetivo** | Isolar o GitHub CLI da configuração persistente/host do usuário. |
| **Preenchimento** | Atual: `/home/agent/.config/gh-empty`. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Configuração e estado do `gh`. |
| **Qual problema o campo resolve** | Reduz chance de reutilizar credenciais/config previamente armazenadas no local padrão. |
| **Qual a necessidade real do campo** | Alta se `gh` estiver instalado e auth deve ser isolada. |
| **O que o campo garante** | `gh` usa o diretório selecionado como config dir conforme seu contrato. |
| **O que o campo **não** garante** | Não torna `gh` incapaz de autenticar via env, login interativo, browser/device flow ou outros mecanismos; o diretório precisa existir/permissões adequadas. |
| **Contexto válido** | Diretório vazio dedicado, não montado do host. |
| **Contexto inválido** | Apontar para diretório compartilhado/persistente com credenciais quando objetivo é isolamento. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `GH_CONFIG_DIR=/home/agent/.config/gh-empty` e garantir diretório limpo. |
| **Exemplo de uso incorreto** | Apontar para `/home/agent/.config/gh` persistente e afirmar “sem credenciais”. |
| **Riscos e edge cases** | Diretório pode deixar de estar vazio após `gh auth login`; permissões podem impedir uso. |
| **Prevenção de riscos / solução de edge cases** | Se objetivo é deny, combinar com política de rede/credenciais e opcionalmente `GH_PROMPT_DISABLED=1`; limpar/recriar diretório conforme lifecycle desejado. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | Válido; nome “gh-empty” não garante que permaneça vazio. |
| **Fontes** | [S10] |

### FR-027 — `containerEnv.SSH_AUTH_SOCK` / `remoteEnv.SSH_AUTH_SOCK`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.SSH_AUTH_SOCK` / `remoteEnv.SSH_AUTH_SOCK` |
| **Tradução** | socket do agente SSH |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Indica o socket Unix usado por clientes para falar com `ssh-agent`; vazio remove a referência convencional herdada. |
| **Objetivo** | Evitar encaminhamento/acesso acidental ao agente SSH do host. |
| **Preenchimento** | Atual: string vazia. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Descoberta do `ssh-agent` por SSH/processos. |
| **Qual problema o campo resolve** | Reduz chance de usar chaves carregadas em agent socket. |
| **Qual a necessidade real do campo** | Alta se o container não deve herdar autenticação SSH do host. |
| **O que o campo garante** | Não fornece um socket de agente via essa variável. |
| **O que o campo **não** garante** | Não desabilita SSH nem chaves privadas em arquivos, config `IdentityFile`, outros sockets explicitamente informados ou outros mecanismos. |
| **Contexto válido** | Sandbox sem agent forwarding. |
| **Contexto inválido** | Ambiente que deliberadamente precisa de signing/auth via ssh-agent. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `SSH_AUTH_SOCK=""` e nenhum socket SSH montado. |
| **Exemplo de uso incorreto** | Montar `/run/host-services/ssh-auth.sock` e só zerar a env, presumindo isolamento total. |
| **Riscos e edge cases** | Ferramenta pode definir outro socket; chaves em `~/.ssh` ainda funcionam. |
| **Prevenção de riscos / solução de edge cases** | Não montar socket/chaves; controlar `~/.ssh`; bloquear rede se a política exigir impossibilidade de SSH. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | Conforme como hardening; garantia é limitada. |
| **Fontes** | [S12] |

### FR-028 — `containerEnv.GITHUB_TOKEN` / `remoteEnv.GITHUB_TOKEN`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.GITHUB_TOKEN` / `remoteEnv.GITHUB_TOKEN` |
| **Tradução** | token GitHub |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Variável de token reconhecida pelo GitHub CLI e por várias ferramentas/ecossistema. |
| **Objetivo** | Neutralizar herança explícita desse nome de token no ambiente. |
| **Preenchimento** | Atual: string vazia. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Credencial potencial para GitHub em ferramentas que a respeitam. |
| **Qual problema o campo resolve** | Evita que um valor de mesmo nome seja passado inadvertidamente pela configuração Dev Container. |
| **Qual a necessidade real do campo** | Alta se o threat model inclui não herdar tokens. |
| **O que o campo garante** | O valor definido por estes mapas é vazio nos processos abrangidos, salvo override posterior. |
| **O que o campo **não** garante** | Não prova ausência de credenciais; `gh` prioriza/usa outras fontes, outros tokens, config armazenada, browser auth, credential helpers, SSH etc. |
| **Contexto válido** | Ambiente onde não se deve fornecer token GitHub por env. |
| **Contexto inválido** | Versionar token real no JSON. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `"GITHUB_TOKEN":""` como uma das camadas, com outras credenciais removidas. |
| **Exemplo de uso incorreto** | `"GITHUB_TOKEN":"ghp_..."` no repositório. |
| **Riscos e edge cases** | Falsa sensação de deny; subprocesso pode sobrescrever; outra variável pode autenticar. |
| **Prevenção de riscos / solução de edge cases** | Usar secret manager quando token é necessário; para deny, remover todas as fontes e aplicar controles de rede/FS. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | Conforme como neutralização, não como prova de ausência de auth. |
| **Fontes** | [S10] |

### FR-029 — `containerEnv.GH_TOKEN` / `remoteEnv.GH_TOKEN`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.GH_TOKEN` / `remoteEnv.GH_TOKEN` |
| **Tradução** | token primário do GitHub CLI |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Variável de autenticação de alta precedência usada pelo `gh` para GitHub.com conforme documentação. |
| **Objetivo** | Neutralizar fornecimento de token explícito ao GitHub CLI. |
| **Preenchimento** | Atual: string vazia. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Autenticação do `gh`. |
| **Qual problema o campo resolve** | Evita disponibilizar token por essa variável. |
| **Qual a necessidade real do campo** | Alta se `gh` não deve herdar token. |
| **O que o campo garante** | Nenhum token útil é fornecido por `GH_TOKEN` nesta configuração. |
| **O que o campo **não** garante** | Não impede `gh` de usar outras fontes/autenticar depois; valor vazio não é ACL. |
| **Contexto válido** | Sandbox sem auth GitHub por env. |
| **Contexto inválido** | Armazenar token real no JSON. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `GH_TOKEN=""` + config dir isolado + prompts/políticas apropriadas. |
| **Exemplo de uso incorreto** | Afirmar que `GH_TOKEN=""` torna login impossível. |
| **Riscos e edge cases** | Outras fontes de auth, login interativo, config persistida. |
| **Prevenção de riscos / solução de edge cases** | Tratar credenciais como capability explícita; bloquear suas fontes e rede conforme necessidade. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | Conforme como hardening, mas não enforcement completo. |
| **Fontes** | [S10] |

### FR-030 — `containerEnv.DOCKER_HOST` / `remoteEnv.DOCKER_HOST`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.DOCKER_HOST` / `remoteEnv.DOCKER_HOST` |
| **Tradução** | host/endpoint do Docker daemon |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Variável que seleciona endpoint do daemon Docker para clientes que a respeitam. |
| **Objetivo** | Evitar herdar um endpoint Docker remoto específico do ambiente externo. |
| **Preenchimento** | Atual: string vazia. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Descoberta/conexão de cliente Docker a daemon. |
| **Qual problema o campo resolve** | Reduz herança de um `DOCKER_HOST` configurado externamente. |
| **Qual a necessidade real do campo** | Média; principal controle deve ser não fornecer socket/endpoint. |
| **O que o campo garante** | Nenhum endpoint não-vazio é explicitamente fornecido por essa variável. |
| **O que o campo **não** garante** | Não garante que Docker CLI esteja inutilizável: clientes podem usar contexto/default socket se disponível; string vazia não substitui isolamento do socket. |
| **Contexto válido** | Container sem `/var/run/docker.sock` e sem endpoint acessível. |
| **Contexto inválido** | Montar docker.sock e achar que `DOCKER_HOST=""` elimina acesso ao daemon. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `DOCKER_HOST=""` e nenhum socket Docker montado. |
| **Exemplo de uso incorreto** | `DOCKER_HOST=""` com `/var/run/docker.sock:/var/run/docker.sock` RW. |
| **Riscos e edge cases** | Fallback para contexto/socket padrão; outras libs ignoram a variável. |
| **Prevenção de riscos / solução de edge cases** | Não montar Docker socket; revisar `DOCKER_CONTEXT`; bloquear endpoint por rede/permissões. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | Válido como neutralização de herança; não é boundary. |
| **Fontes** | [S11] |

### FR-031 — `containerEnv.GIT_CONFIG_NOSYSTEM` / `remoteEnv.GIT_CONFIG_NOSYSTEM`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `containerEnv.GIT_CONFIG_NOSYSTEM` / `remoteEnv.GIT_CONFIG_NOSYSTEM` |
| **Tradução** | desabilitar configuração Git de sistema |
| **Identidade** | Chave de variável de ambiente presente em `containerEnv` e `remoteEnv`. |
| **Tipo de campo** | `string` (valor de environment variable) |
| **Papel** | Controle de comportamento de ferramenta via ambiente. |
| **Função** | Quando verdadeiro/não vazio conforme Git, impede leitura do arquivo de configuração de sistema. |
| **Objetivo** | Evitar herdar `/etc/gitconfig` ou equivalente da imagem/host mount. |
| **Preenchimento** | Atual: `"1"`. |
| **Obrigatoriedade** | Não é obrigatória pela spec Dev Container; só deve existir se a política exigir seu efeito. |
| **Relação com outros campos** | Duplicada nos dois mapas. `containerEnv` já tem escopo amplo; `remoteEnv` deve ser mantido apenas se houver razão explícita para duplicação/override. |
| **O que o campo configura** | Camada system config do Git. |
| **Qual problema o campo resolve** | Torna o comportamento Git menos dependente da imagem base. |
| **Qual a necessidade real do campo** | Alta se system config não é confiável. |
| **O que o campo garante** | Git ignora a configuração de sistema. |
| **O que o campo **não** garante** | Não impede global/local/command-line config; e torna o mount atual em `/etc/gitconfig` inefetivo. |
| **Contexto válido** | Intenção explícita de ignorar system config. |
| **Contexto inválido** | Montar uma policy em `/etc/gitconfig` esperando enforcement. |
| **Escopo permitido** | Ambiente do container e/ou processos remotos, conforme necessidade real. |
| **Escopo proibido** | Não tratar variável de ambiente como barreira de segurança mais forte que mounts, permissões, credenciais e rede. |
| **Exemplo de uso correto** | `GIT_CONFIG_NOSYSTEM=1` e remover mount `/etc/gitconfig`. |
| **Exemplo de uso incorreto** | `GIT_CONFIG_NOSYSTEM=1` + confiar em `/etc/gitconfig` montado RO. |
| **Riscos e edge cases** | Conflito atual e perda de uma policy que se pensava ativa. |
| **Prevenção de riscos / solução de edge cases** | Escolher: ignorar system config OU usar `/etc/gitconfig` controlado; não fazer ambos. |
| **Borderlines** | Subprocessos podem sobrescrever env; ferramentas podem ter fontes adicionais de configuração/credenciais. |
| **Melhores técnicas atuais** | Preferir uma fonte canônica de configuração e controles estruturais para enforcement. |
| **Boas práticas** | Documentar por que a variável existe e testar o efeito negativo/positivo esperado. |
| **Situação no arquivo analisado** | CONFLITO: anula o mount de `gitconfig-agent` em `/etc/gitconfig`. |
| **Fontes** | [S9] |

### FR-032 — `customizations.vscode.settings["terminal.integrated.defaultProfile.linux"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["terminal.integrated.defaultProfile.linux"]` |
| **Tradução** | perfil padrão do terminal Linux |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `string` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Seleciona o perfil de terminal integrado padrão no Linux. |
| **Objetivo** | Abrir terminais em Bash de forma previsível. |
| **Preenchimento** | Atual: `"bash"`; o perfil deve existir/ser reconhecido pelo VS Code. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | UX do terminal integrado. |
| **Qual problema o campo resolve** | Evita shell padrão inesperado. |
| **Qual a necessidade real do campo** | Média para scripts/uso consistente. |
| **O que o campo garante** | Terminais integrados usam o perfil selecionado quando aplicável. |
| **O que o campo **não** garante** | Não muda `/bin/sh`, shell de lifecycle commands nem garante Bash instalado. |
| **Contexto válido** | Imagem possui Bash e equipe quer esse shell interativo. |
| **Contexto inválido** | Imagem sem Bash ou fluxo que depende de outro shell. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `"bash"` em imagem que instala Bash. |
| **Exemplo de uso incorreto** | `"bash"` em imagem scratch/minimal sem Bash. |
| **Riscos e edge cases** | Falha/fallback de perfil; diferença entre interactive shell e scripts. |
| **Prevenção de riscos / solução de edge cases** | Garantir Bash no Dockerfile; não escrever scripts assumindo que este setting muda `/bin/sh`. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme se Bash existe. |
| **Fontes** | [S2] |

### FR-033 — `customizations.vscode.settings["git.autofetch"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["git.autofetch"]` |
| **Tradução** | busca automática do Git |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `boolean` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Controla fetch automático periódico pela extensão Git do VS Code. |
| **Objetivo** | Evitar acesso remoto Git automático e mudanças de refs remotas disparadas pela IDE. |
| **Preenchimento** | Atual: `false`. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | Automação de fetch da extensão Git. |
| **Qual problema o campo resolve** | Reduz tráfego/rede e autenticação automática. |
| **Qual a necessidade real do campo** | Alta para sandbox que quer Git passivo. |
| **O que o campo garante** | A extensão Git não executa seu autofetch automático quando setting é respeitado. |
| **O que o campo **não** garante** | Não impede `git fetch` manual, outras extensões ou processos externos. |
| **Contexto válido** | Agente deve ler estado local sem sincronizar automaticamente. |
| **Contexto inválido** | Equipe espera atualização automática de remotes. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `false` com `.git` RO e sem credenciais. |
| **Exemplo de uso incorreto** | `false` e afirmar “nenhum processo pode acessar Git remoto”. |
| **Riscos e edge cases** | Outras ferramentas podem fetch; extensões podem ter mecanismos próprios. |
| **Prevenção de riscos / solução de edge cases** | Combinar com `.git` RO, ausência de credenciais e rede se necessário. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme e coerente. |
| **Fontes** | [S13] |

### FR-034 — `customizations.vscode.settings["git.confirmSync"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["git.confirmSync"]` |
| **Tradução** | confirmar sincronização Git |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `boolean` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Exige confirmação da ação Sync da extensão Git em contextos suportados. |
| **Objetivo** | Evitar push/pull acidental por clique/ação da IDE. |
| **Preenchimento** | Atual: `true`. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | UX de sincronização Git da extensão. |
| **Qual problema o campo resolve** | Adiciona fricção antes de sync. |
| **Qual a necessidade real do campo** | Média como proteção humana; baixa para agente automatizado. |
| **O que o campo garante** | A extensão apresenta confirmação conforme implementação do setting. |
| **O que o campo **não** garante** | Não impede CLI, automação, extensões ou operações sem esse comando de Sync. |
| **Contexto válido** | Usuário humano interage com Source Control. |
| **Contexto inválido** | Tratar confirmação como ACL para agente. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `true` como safeguard de UI. |
| **Exemplo de uso incorreto** | `true` como único impedimento contra push. |
| **Riscos e edge cases** | Automação pode não passar pela ação Sync; prompts podem variar. |
| **Prevenção de riscos / solução de edge cases** | Manter barreiras estruturais independentes. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme; defesa de UX. |
| **Fontes** | [S13] |

### FR-035 — `customizations.vscode.settings["git.terminalAuthentication"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["git.terminalAuthentication"]` |
| **Tradução** | autenticação Git no terminal integrada pelo VS Code |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `boolean` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Controla integração de autenticação Git para processos de terminal conforme implementação da extensão. |
| **Objetivo** | Evitar que terminais ganhem automaticamente credenciais providas pelo VS Code. |
| **Preenchimento** | Atual: `false`. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | Integração auth entre VS Code e Git no terminal. |
| **Qual problema o campo resolve** | Reduz um canal de credential injection. |
| **Qual a necessidade real do campo** | Alta para ambiente sem auth automática. |
| **O que o campo garante** | Desabilita essa integração específica quando setting é respeitado. |
| **O que o campo **não** garante** | Não desabilita helpers, SSH, tokens env, credential stores ou Git fora desse mecanismo. |
| **Contexto válido** | Sandbox que quer terminal sem assistência de credenciais da IDE. |
| **Contexto inválido** | Fluxo normal que depende da integração para autenticar. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `false` junto com tokens vazios e `GIT_TERMINAL_PROMPT=0`. |
| **Exemplo de uso incorreto** | `false` e deixar credenciais em `~/.git-credentials`, alegando isolamento. |
| **Riscos e edge cases** | Outras fontes de credenciais continuam válidas. |
| **Prevenção de riscos / solução de edge cases** | Auditar credential helpers, SSH e env; manter `.git`/network controls. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme; camada adicional, não boundary. |
| **Fontes** | [S13] |

### FR-036 — `customizations.vscode.settings["git.useIntegratedAskPass"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["git.useIntegratedAskPass"]` |
| **Tradução** | usar AskPass integrado |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `boolean` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Controla o mecanismo AskPass integrado do VS Code para Git. |
| **Objetivo** | Evitar prompt/fornecimento de credenciais via helper gráfico/integrado. |
| **Preenchimento** | Atual: `false`. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | Mecanismo AskPass da extensão Git. |
| **Qual problema o campo resolve** | Reduz autenticação interativa indireta. |
| **Qual a necessidade real do campo** | Alta para agente não interativo. |
| **O que o campo garante** | A integração AskPass do VS Code não é usada quando setting é aplicado. |
| **O que o campo **não** garante** | Não impede `GIT_ASKPASS` externo, SSH_ASKPASS, helpers ou credenciais já disponíveis. |
| **Contexto válido** | Automação sem prompt. |
| **Contexto inválido** | Ambiente humano que depende do AskPass integrado. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `false` + `GIT_TERMINAL_PROMPT=0`. |
| **Exemplo de uso incorreto** | `false` enquanto se exporta outro `GIT_ASKPASS` funcional. |
| **Riscos e edge cases** | Fallbacks de autenticação. |
| **Prevenção de riscos / solução de edge cases** | Neutralizar também env/helpers se deny é requisito. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme e coerente. |
| **Fontes** | [S13] |

### FR-037 — `customizations.vscode.settings["github.gitAuthentication"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["github.gitAuthentication"]` |
| **Tradução** | autenticação Git do GitHub pelo VS Code |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `boolean` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Controla se a extensão GitHub fornece autenticação para comandos Git integrados. |
| **Objetivo** | Evitar que login GitHub do VS Code seja reutilizado automaticamente pelo Git. |
| **Preenchimento** | Atual: `false`. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | Integração de Git auth da extensão GitHub. |
| **Qual problema o campo resolve** | Separa identidade da IDE de Git CLI/extension operations. |
| **Qual a necessidade real do campo** | Alta se a IDE pode estar logada mas Git não deve receber credencial. |
| **O que o campo garante** | Desabilita esse provedor de autenticação específico. |
| **O que o campo **não** garante** | Não faz logout do GitHub, não bloqueia `gh`, tokens, SSH, helpers ou outras extensões. |
| **Contexto válido** | Ambiente onde GitHub extension pode existir sem fornecer Git credentials. |
| **Contexto inválido** | Assumir que isso impede toda comunicação GitHub. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `false` como defense-in-depth. |
| **Exemplo de uso incorreto** | `false` e montar credenciais GitHub persistentes. |
| **Riscos e edge cases** | Outros mecanismos de auth permanecem. |
| **Prevenção de riscos / solução de edge cases** | Combinar com env/config/FS/network controls. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme; não é boundary. |
| **Fontes** | [S14] |

### FR-038 — `customizations.vscode.settings["claudeCode.initialPermissionMode"]`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `customizations.vscode.settings["claudeCode.initialPermissionMode"]` |
| **Tradução** | modo inicial de permissão do Claude Code |
| **Identidade** | Chave de configuração do VS Code/extensão dentro de `customizations.vscode.settings`. |
| **Tipo de campo** | `string enum` |
| **Papel** | Comportamento da IDE/extensão. |
| **Função** | Define o modo inicial de permissão para sessões Claude Code iniciadas pela extensão VS Code. |
| **Objetivo** | Iniciar em modo Manual/default em vez de um modo mais permissivo. |
| **Preenchimento** | Atual: `"default"`; documentação atual associa `default` ao modo Manual. |
| **Obrigatoriedade** | Opcional; deve existir apenas se o comportamento explícito é desejado. |
| **Relação com outros campos** | Seu efeito é limitado ao VS Code/extensão e complementa, mas não substitui, controles Docker/Git/FS. |
| **O que o campo configura** | Política inicial de aprovação de ações do Claude Code na extensão. |
| **Qual problema o campo resolve** | Evita começar automaticamente em `acceptEdits`/Plan ou outro modo mais permissivo. |
| **Qual a necessidade real do campo** | Alta para governança do agente dentro da extensão. |
| **O que o campo garante** | Sessões iniciadas pela extensão começam no modo correspondente, sujeito à versão/políticas do produto. |
| **O que o campo **não** garante** | Não é sandbox do SO, não impede mudanças de modo autorizadas, CLI separado, bugs, nem substitui mounts RO/capabilities. |
| **Contexto válido** | Ambiente de agente onde mudanças precisam de aprovação conforme modo Manual. |
| **Contexto inválido** | Confiar nesse setting como única proteção de arquivos/segredos. |
| **Escopo permitido** | Escopo VS Code remoto/container conforme suporte do setting. |
| **Escopo proibido** | Não promover um setting de UX/integration a controle de segurança primário. |
| **Exemplo de uso correto** | `"default"` + control-plane RO e hardening Docker. |
| **Exemplo de uso incorreto** | `"default"` e todo filesystem/credenciais RW, alegando segurança suficiente. |
| **Riscos e edge cases** | Semântica pode evoluir; settings de usuário/managed policy podem afetar comportamento. |
| **Prevenção de riscos / solução de edge cases** | Manter hard boundaries no container; validar documentação da versão; usar policy administrada quando disponível. |
| **Borderlines** | Precedência de settings, políticas administradas, mudanças de versão e execução de CLI fora da IDE podem mudar o efeito. |
| **Melhores técnicas atuais** | Defesa em profundidade: IDE restritiva + ambiente/FS/rede restritivos. |
| **Boas práticas** | Validar o setting na versão alvo e testar o comportamento efetivo. |
| **Situação no arquivo analisado** | Conforme à documentação atual; `default` é um valor válido para Manual. |
| **Fontes** | [S15] |

### FR-039 — Parâmetro embutido `source` em mounts

| Dimensão | Registro |
|---|---|
| **Nome do campo** | Parâmetro embutido `source` em mounts |
| **Tradução** | origem |
| **Identidade** | Parâmetro embutido em cada string de `workspaceMount`/`mounts`; não é uma chave JSON autônoma no arquivo. |
| **Tipo de campo** | Token key/value da sintaxe Docker `--mount`. |
| **Papel** | Descrever uma dimensão da montagem. |
| **Função** | Seleciona o path host ou nome do volume que alimenta o mount. |
| **Objetivo** | Definir explicitamente a procedência dos dados. |
| **Preenchimento** | Path interpolado (`${localWorkspaceFolder}/...`) para bind ou nome (`cepraea-agent-*`) para volume. |
| **Obrigatoriedade** | Depende do tipo/sintaxe do mount; para a forma usada, `target` e `type`/`source` são essenciais conforme caso. |
| **Relação com outros campos** | Interpretado pelo Docker após o Dev Container encaminhar a string. |
| **O que o campo configura** | Origem dos dados montados. |
| **Qual problema o campo resolve** | Evita depender de origem implícita. |
| **Qual a necessidade real do campo** | Essencial na arquitetura atual. |
| **O que o campo garante** | Docker usa a origem solicitada se existir/for válida. |
| **O que o campo **não** garante** | Não valida sensibilidade dos dados nem ownership. |
| **Contexto válido** | Subpath necessário ou named volume dedicado. |
| **Contexto inválido** | Host root, home inteiro ou socket sensível sem justificativa. |
| **Escopo permitido** | Somente dentro das strings de mount onde a sintaxe Docker o aceita. |
| **Escopo proibido** | Não confundir com campo nativo de nível raiz do JSON. |
| **Exemplo de uso correto** | `source=${localWorkspaceFolder}/.git` |
| **Exemplo de uso incorreto** | `source=/` em sandbox comum. |
| **Riscos e edge cases** | Paths inexistentes, escaping, exposição excessiva. |
| **Prevenção de riscos / solução de edge cases** | Minimizar source e classificar sensibilidade. |
| **Borderlines** | A forma objeto de `mounts` no schema tem propriedades próprias e mais restritas; a forma string preserva opções Docker adicionais. |
| **Melhores técnicas atuais** | Preferir sintaxe consistente `source=...,target=...,type=...` e revisar cada target como uma permissão. |
| **Boas práticas** | Ordenar mentalmente por origem → destino → tipo → modo de acesso e evitar colisões. |
| **Situação no arquivo analisado** | Conforme nas strings atuais; revisar especialmente paths de control-plane. |
| **Fontes** | [S7], [S8] |

### FR-040 — Parâmetro embutido `target` em mounts

| Dimensão | Registro |
|---|---|
| **Nome do campo** | Parâmetro embutido `target` em mounts |
| **Tradução** | destino |
| **Identidade** | Parâmetro embutido em cada string de `workspaceMount`/`mounts`; não é uma chave JSON autônoma no arquivo. |
| **Tipo de campo** | Token key/value da sintaxe Docker `--mount`. |
| **Papel** | Descrever uma dimensão da montagem. |
| **Função** | Define onde o mount aparece dentro do container. |
| **Objetivo** | Criar path canônico e controlar sobreposições. |
| **Preenchimento** | Path absoluto interno. |
| **Obrigatoriedade** | Depende do tipo/sintaxe do mount; para a forma usada, `target` e `type`/`source` são essenciais conforme caso. |
| **Relação com outros campos** | Interpretado pelo Docker após o Dev Container encaminhar a string. |
| **O que o campo configura** | Visibilidade e sobreposição no filesystem do container. |
| **Qual problema o campo resolve** | Permite proteger subpaths específicos com mounts RO. |
| **Qual a necessidade real do campo** | Essencial. |
| **O que o campo garante** | Conteúdo montado aparece no target conforme runtime. |
| **O que o campo **não** garante** | Não garante que conteúdo original abaixo do target continue visível; mount over o obscurece. |
| **Contexto válido** | Target dedicado ou overlay intencional. |
| **Contexto inválido** | Target que encobre dados não relacionados sem documentação. |
| **Escopo permitido** | Somente dentro das strings de mount onde a sintaxe Docker o aceita. |
| **Escopo proibido** | Não confundir com campo nativo de nível raiz do JSON. |
| **Exemplo de uso correto** | `target=/workspaces/cepraea-beach-pro/.git` |
| **Exemplo de uso incorreto** | `target=/workspaces/cepraea-beach-pro/docs` apontando para `runbooks` sem intenção explícita. |
| **Riscos e edge cases** | Obscuring e colisões; aliases confusos. |
| **Prevenção de riscos / solução de edge cases** | Inventário de targets; evitar dois significados para mesmo path. |
| **Borderlines** | A forma objeto de `mounts` no schema tem propriedades próprias e mais restritas; a forma string preserva opções Docker adicionais. |
| **Melhores técnicas atuais** | Preferir sintaxe consistente `source=...,target=...,type=...` e revisar cada target como uma permissão. |
| **Boas práticas** | Ordenar mentalmente por origem → destino → tipo → modo de acesso e evitar colisões. |
| **Situação no arquivo analisado** | Há uma colisão semântica potencial: `runbooks` é montado sobre `/docs`, ocultando `docs` original. |
| **Fontes** | [S7], [S8] |

### FR-041 — Parâmetro embutido `type` em mounts

| Dimensão | Registro |
|---|---|
| **Nome do campo** | Parâmetro embutido `type` em mounts |
| **Tradução** | tipo |
| **Identidade** | Parâmetro embutido em cada string de `workspaceMount`/`mounts`; não é uma chave JSON autônoma no arquivo. |
| **Tipo de campo** | Token key/value da sintaxe Docker `--mount`. |
| **Papel** | Descrever uma dimensão da montagem. |
| **Função** | Seleciona o mecanismo de mount, como `bind` ou `volume`. |
| **Objetivo** | Distinguir dados ligados ao host de storage gerenciado/persistente. |
| **Preenchimento** | Atual usa `bind` para paths do workspace e `volume` para homes/caches do agente. |
| **Obrigatoriedade** | Depende do tipo/sintaxe do mount; para a forma usada, `target` e `type`/`source` são essenciais conforme caso. |
| **Relação com outros campos** | Interpretado pelo Docker após o Dev Container encaminhar a string. |
| **O que o campo configura** | Semântica de storage. |
| **Qual problema o campo resolve** | Resolve necessidade de overlays host vs persistência independente. |
| **Qual a necessidade real do campo** | Alta. |
| **O que o campo garante** | `bind` referencia host path; `volume` usa storage gerenciado Docker. |
| **O que o campo **não** garante** | Não define sozinho read/write, lifecycle, backup ou sensibilidade. |
| **Contexto válido** | Bind para arquivos fonte/policy; volume para estado/cache deliberadamente persistente. |
| **Contexto inválido** | Usar volume quando precisa refletir arquivo host em tempo real ou bind para cache portátil sem avaliar ownership. |
| **Escopo permitido** | Somente dentro das strings de mount onde a sintaxe Docker o aceita. |
| **Escopo proibido** | Não confundir com campo nativo de nível raiz do JSON. |
| **Exemplo de uso correto** | `type=bind` para `.git`; `type=volume` para `.npm`. |
| **Exemplo de uso incorreto** | `type=bind` com `source=cepraea-agent-npm` esperando named volume. |
| **Riscos e edge cases** | Portabilidade e persistência diferentes. |
| **Prevenção de riscos / solução de edge cases** | Escolher por lifecycle/ownership e documentar retenção. |
| **Borderlines** | A forma objeto de `mounts` no schema tem propriedades próprias e mais restritas; a forma string preserva opções Docker adicionais. |
| **Melhores técnicas atuais** | Preferir sintaxe consistente `source=...,target=...,type=...` e revisar cada target como uma permissão. |
| **Boas práticas** | Ordenar mentalmente por origem → destino → tipo → modo de acesso e evitar colisões. |
| **Situação no arquivo analisado** | Conforme. |
| **Fontes** | [S7], [S8] |

### FR-042 — Parâmetro embutido `readonly` em mounts

| Dimensão | Registro |
|---|---|
| **Nome do campo** | Parâmetro embutido `readonly` em mounts |
| **Tradução** | somente leitura |
| **Identidade** | Parâmetro embutido em cada string de `workspaceMount`/`mounts`; não é uma chave JSON autônoma no arquivo. |
| **Tipo de campo** | Token key/value da sintaxe Docker `--mount`. |
| **Papel** | Descrever uma dimensão da montagem. |
| **Função** | Marca o mount como não gravável pelo container. |
| **Objetivo** | Proteger o control-plane contra mutação via filesystem normal. |
| **Preenchimento** | Flag sem valor na sintaxe atual, presente nos binds sensíveis. |
| **Obrigatoriedade** | Depende do tipo/sintaxe do mount; para a forma usada, `target` e `type`/`source` são essenciais conforme caso. |
| **Relação com outros campos** | Interpretado pelo Docker após o Dev Container encaminhar a string. |
| **O que o campo configura** | Modo de acesso ao mount. |
| **Qual problema o campo resolve** | Evita alterações acidentais/maliciosas em arquivos protegidos pelo usuário do container. |
| **Qual a necessidade real do campo** | Alta para `.git`, policies, workflows etc. |
| **O que o campo garante** | Operações normais de escrita através daquele mount são negadas pelo VFS/runtime. |
| **O que o campo **não** garante** | Não impede leitura/exfiltração, não protege cópias existentes em outros paths, não torna o host inteiro imutável, nem bloqueia writes via outro mount para o mesmo inode/path se houver. |
| **Contexto válido** | Policies/configs que o agente só precisa ler. |
| **Contexto inválido** | Código que o agente precisa editar ou cache que precisa persistir alterações. |
| **Escopo permitido** | Somente dentro das strings de mount onde a sintaxe Docker o aceita. |
| **Escopo proibido** | Não confundir com campo nativo de nível raiz do JSON. |
| **Exemplo de uso correto** | `...,type=bind,readonly` em `AGENT_POLICY.md`. |
| **Exemplo de uso incorreto** | Marcar workspace inteiro RO quando o agente precisa editar código. |
| **Riscos e edge cases** | Aplicações podem tentar lock/temp files dentro do RO; Git pode tentar optional locks. |
| **Prevenção de riscos / solução de edge cases** | Usar RO no control-plane; para Git read-only considerar `GIT_OPTIONAL_LOCKS=0`; fornecer paths RW separados para estado. |
| **Borderlines** | A forma objeto de `mounts` no schema tem propriedades próprias e mais restritas; a forma string preserva opções Docker adicionais. |
| **Melhores técnicas atuais** | Preferir sintaxe consistente `source=...,target=...,type=...` e revisar cada target como uma permissão. |
| **Boas práticas** | Ordenar mentalmente por origem → destino → tipo → modo de acesso e evitar colisões. |
| **Situação no arquivo analisado** | Bem aplicado em vários subpaths; named volumes ficam RW por design. |
| **Fontes** | [S7], [S8] |

### FR-043 — `runArgs[]`: `--security-opt=no-new-privileges:true`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `runArgs[]`: `--security-opt=no-new-privileges:true` |
| **Tradução** | não permitir novos privilégios |
| **Identidade** | Argumento Docker embutido como item string de `runArgs`; não é campo JSON independente. |
| **Tipo de campo** | Flag de `docker run`. |
| **Papel** | Controle de runtime Linux/Docker. |
| **Função** | Ativa a opção Docker/Linux que impede processos de ganhar privilégios adicionais por mecanismos como setuid/setgid conforme kernel/runtime. |
| **Objetivo** | Reduzir caminhos de escalada dentro do container. |
| **Preenchimento** | String exata suportada pelo Docker. |
| **Obrigatoriedade** | Não obrigatório pela spec; manter apenas se o threat model/requisito exigir. |
| **Relação com outros campos** | Aplicado junto a `containerUser`, mounts e demais argumentos; semântica vem do Docker. |
| **O que o campo configura** | Bit/política `no_new_privs` do processo/container. |
| **Qual problema o campo resolve** | Mitiga elevação por executáveis privilegiados. |
| **Qual a necessidade real do campo** | Alta para sandbox de agente. |
| **O que o campo garante** | Processos não podem adquirir novos privilégios pelos mecanismos cobertos pela flag. |
| **O que o campo **não** garante** | Não elimina vulnerabilidades do kernel, capabilities já concedidas, acesso a dados/rede ou privilégios inerentes ao usuário/mounts. |
| **Contexto válido** | Agente não precisa de sudo/setuid funcional. |
| **Contexto inválido** | Workload que legitimamente depende de elevação dentro do container. |
| **Escopo permitido** | Runtime Docker compatível, principalmente Linux para flags de segurança. |
| **Escopo proibido** | Não pressupor portabilidade universal para runtimes não Docker. |
| **Exemplo de uso correto** | `--security-opt=no-new-privileges:true` |
| **Exemplo de uso incorreto** | Desabilitar a flag para “fazer sudo funcionar” sem reavaliar o threat model. |
| **Riscos e edge cases** | Pode quebrar sudo/su/setuid workflows. |
| **Prevenção de riscos / solução de edge cases** | Corrigir imagem para não precisar de elevação; conceder apenas o mínimo inevitável. |
| **Borderlines** | Ferramentas e plataformas podem rejeitar, adaptar ou ignorar opções específicas. |
| **Melhores técnicas atuais** | Usar deny-by-default e adicionar exceções mínimas apenas quando necessário. |
| **Boas práticas** | Testar funcionalidades essenciais sob as restrições e registrar a justificativa de cada exceção. |
| **Situação no arquivo analisado** | Conforme e recomendado para o objetivo. |
| **Fontes** | [S6] |

### FR-044 — `runArgs[]`: `--cap-drop=ALL`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `runArgs[]`: `--cap-drop=ALL` |
| **Tradução** | remover todas as capabilities Linux |
| **Identidade** | Argumento Docker embutido como item string de `runArgs`; não é campo JSON independente. |
| **Tipo de campo** | Flag de `docker run`. |
| **Papel** | Controle de runtime Linux/Docker. |
| **Função** | Solicita ao Docker remoção de todas as Linux capabilities do conjunto padrão do container. |
| **Objetivo** | Minimizar privilégios kernel concedidos ao agente. |
| **Preenchimento** | Atual `--cap-drop=ALL`. |
| **Obrigatoriedade** | Não obrigatório pela spec; manter apenas se o threat model/requisito exigir. |
| **Relação com outros campos** | Aplicado junto a `containerUser`, mounts e demais argumentos; semântica vem do Docker. |
| **O que o campo configura** | Capabilities Linux do container. |
| **Qual problema o campo resolve** | Reduz superfície para operações privilegiadas. |
| **Qual a necessidade real do campo** | Alta em sandbox que só edita/roda app user-space. |
| **O que o campo garante** | Remove as capabilities abrangidas pelo mecanismo Docker; o processo fica sem o conjunto padrão concedido. |
| **O que o campo **não** garante** | Não é isolamento de filesystem/rede, não impede syscalls não privilegiadas nem vulnerabilidades do kernel; não substitui seccomp/AppArmor/SELinux. |
| **Contexto válido** | Frontend/dev tooling que não precisa de capabilities. |
| **Contexto inválido** | Debugger/network tooling ou serviço que exige capability específica e não foi adaptado. |
| **Escopo permitido** | Runtime Docker compatível, principalmente Linux para flags de segurança. |
| **Escopo proibido** | Não pressupor portabilidade universal para runtimes não Docker. |
| **Exemplo de uso correto** | `--cap-drop=ALL` e adicionar uma capability específica somente se demonstradamente necessária. |
| **Exemplo de uso incorreto** | `--cap-drop=ALL` seguido de `--cap-add=ALL` por conveniência. |
| **Riscos e edge cases** | Pode quebrar ping raw, debug, chown/setuid específicos, low-level networking. |
| **Prevenção de riscos / solução de edge cases** | Teste funcional; se necessário, `--cap-add=<mínima>` documentada. |
| **Borderlines** | Ferramentas e plataformas podem rejeitar, adaptar ou ignorar opções específicas. |
| **Melhores técnicas atuais** | Usar deny-by-default e adicionar exceções mínimas apenas quando necessário. |
| **Boas práticas** | Testar funcionalidades essenciais sob as restrições e registrar a justificativa de cada exceção. |
| **Situação no arquivo analisado** | Conforme e forte. |
| **Fontes** | [S6] |

### FR-045 — `runArgs[]`: `--add-host=host.docker.internal:host-gateway`

| Dimensão | Registro |
|---|---|
| **Nome do campo** | `runArgs[]`: `--add-host=host.docker.internal:host-gateway` |
| **Tradução** | adicionar hostname do host via gateway |
| **Identidade** | Argumento Docker embutido como item string de `runArgs`; não é campo JSON independente. |
| **Tipo de campo** | Flag de `docker run`. |
| **Papel** | Controle de runtime Linux/Docker. |
| **Função** | Adiciona entrada no `/etc/hosts` do container fazendo `host.docker.internal` resolver para o endereço especial `host-gateway`. |
| **Objetivo** | Permitir que o container alcance serviços expostos no host por um nome estável. |
| **Preenchimento** | Atual string suportada pelo Docker. |
| **Obrigatoriedade** | Não obrigatório pela spec; manter apenas se o threat model/requisito exigir. |
| **Relação com outros campos** | Aplicado junto a `containerUser`, mounts e demais argumentos; semântica vem do Docker. |
| **O que o campo configura** | Resolução de nome para host gateway. |
| **Qual problema o campo resolve** | Resolve diferenças de acesso ao host em Linux/Docker local. |
| **Qual a necessidade real do campo** | Só é necessária se há serviço host que o container deve consumir. |
| **O que o campo garante** | O hostname é resolvido conforme mapeamento do Docker. |
| **O que o campo **não** garante** | Não garante que serviço esteja ouvindo, nem restringe quais portas do host podem ser tentadas; amplia conectividade potencial ao host. |
| **Contexto válido** | Dev server/backend local no host explicitamente necessário. |
| **Contexto inválido** | Sandbox que deveria estar isolado do host e não usa nenhum serviço host. |
| **Escopo permitido** | Runtime Docker compatível, principalmente Linux para flags de segurança. |
| **Escopo proibido** | Não pressupor portabilidade universal para runtimes não Docker. |
| **Exemplo de uso correto** | `--add-host=host.docker.internal:host-gateway` com serviço host necessário e firewall adequado. |
| **Exemplo de uso incorreto** | Manter por convenção sem nenhum consumidor, em ambiente de alta restrição. |
| **Riscos e edge cases** | Aumenta superfície de rede; serviços host não autenticados podem ficar alcançáveis. |
| **Prevenção de riscos / solução de edge cases** | Remover se não necessário; limitar serviços/firewall; autenticar endpoints. |
| **Borderlines** | Ferramentas e plataformas podem rejeitar, adaptar ou ignorar opções específicas. |
| **Melhores técnicas atuais** | Usar deny-by-default e adicionar exceções mínimas apenas quando necessário. |
| **Boas práticas** | Testar funcionalidades essenciais sob as restrições e registrar a justificativa de cada exceção. |
| **Situação no arquivo analisado** | Válido tecnicamente, mas é a maior abertura deliberada para o host neste `runArgs`. |
| **Fontes** | [S6] |

## 5. Inventário dos 19 mounts

O registro abaixo não cria “novos campos JSON”; ele materializa as instâncias do campo `mounts[]` para governança e auditoria.

| # | Source | Target | Tipo | Acesso | Avaliação |
|---:|---|---|---|---|---|
| 1 | `.git` | `/workspaces/cepraea-beach-pro/.git` | `bind` | **RO** | Bom para Git metadata somente leitura; operações Git que escrevem tendem a falhar. |
| 2 | `.devcontainer` | `/workspaces/cepraea-beach-pro/.devcontainer` | `bind` | **RO** | Protege a própria configuração/control-plane. |
| 3 | `.github/workflows` | `/workspaces/cepraea-beach-pro/.github/workflows` | `bind` | **RO** | Protege workflows CI contra alteração no container. |
| 4 | `.claude` | `/workspaces/cepraea-beach-pro/.claude` | `bind` | **RO** | Protege configuração Claude do repositório. |
| 5 | `.codex` | `/workspaces/cepraea-beach-pro/.codex` | `bind` | **RO** | Protege configuração Codex do repositório. |
| 6 | `.mcp.json` | `/workspaces/cepraea-beach-pro/.mcp.json` | `bind` | **RO** | Protege configuração MCP do repositório. |
| 7 | `CLAUDE.md` | `/workspaces/cepraea-beach-pro/CLAUDE.md` | `bind` | **RO** | Protege instruções Claude. |
| 8 | `AGENTS.md` | `/workspaces/cepraea-beach-pro/AGENTS.md` | `bind` | **RO** | Protege instruções do agente. |
| 9 | `cepraea-agent-claude` | `/home/agent/.claude` | `volume` | **RW** | Estado Claude persistente; pode reter sessão/config/credenciais. |
| 10 | `cepraea-agent-codex` | `/home/agent/.codex` | `volume` | **RW** | Estado Codex persistente; pode reter sessão/config/credenciais. |
| 11 | `cepraea-agent-npm` | `/home/agent/.npm` | `volume` | **RW** | Cache/estado npm persistente. |
| 12 | `.devcontainer/control-plane/gitconfig-agent` | `/etc/gitconfig` | `bind` | **RO** | INEFETIVO atualmente: `GIT_CONFIG_NOSYSTEM=1` manda Git ignorar system config. |
| 13 | `.devcontainer/control-plane/gitconfig-agent` | `/home/agent/.gitconfig` | `bind` | **RO** | INEFETIVO atualmente: `GIT_CONFIG_GLOBAL=/dev/null` substitui o global config. |
| 14 | `.devcontainer/control-plane/gitconfig-agent` | `/home/agent/.config/git/config` | `bind` | **RO** | INEFETIVO atualmente: `GIT_CONFIG_GLOBAL=/dev/null` substitui a busca global/XDG. |
| 15 | `scripts/ci` | `/workspaces/cepraea-beach-pro/scripts/ci` | `bind` | **RO** | Protege scripts de CI. |
| 16 | `AGENT_POLICY.md` | `/workspaces/cepraea-beach-pro/AGENT_POLICY.md` | `bind` | **RO** | Protege policy do agente. |
| 17 | `runbooks` | `/workspaces/cepraea-beach-pro/runbooks` | `bind` | **RO** | Expose runbooks canonicamente em RO. |
| 18 | `runbooks` | `/workspaces/cepraea-beach-pro/.drive` | `bind` | **RO** | Alias RO; aumenta superfície/ambiguidade de paths. |
| 19 | `runbooks` | `/workspaces/cepraea-beach-pro/docs` | `bind` | **RO** | Atenção: obscurece qualquer conteúdo original existente em `docs/` dentro do workspace. |

### 5.1 Regra arquitetural correta para os mounts

1. **Workspace editável:** manter somente as áreas que o agente realmente precisa alterar em RW.
2. **Control-plane imutável:** policies, workflows, instruções, configuração do agente e metadados Git podem ser sobrepostos por mounts RO quando devem ser somente leitura.
3. **Estado persistente separado:** named volumes para `.claude`, `.codex` e `.npm` são corretos quando a persistência é desejada; devem ser tratados como storage persistente, inclusive do ponto de vista de credenciais/dados de sessão.
4. **Não criar aliases sem contrato:** `runbooks -> .drive` e `runbooks -> docs` devem ter consumidor e semântica documentados. O target `docs` é especialmente sensível porque esconde o conteúdo original nesse caminho.
5. **Não montar policy que a própria ferramenta ignora:** os três mounts `gitconfig-agent` precisam ser reestruturados conforme a decisão Git abaixo.

## 6. Decisão P0 — modelo correto de configuração Git

O arquivo atual combina duas estratégias mutuamente contraditórias. Escolha uma delas:

### Modelo A — Git sem configuração global/system herdada

Use quando o objetivo é impedir que qualquer `gitconfig-agent` global/system seja aplicado e operar somente com defaults + config local do repositório permitida.

```json
"GIT_CONFIG_GLOBAL": "/dev/null",
"GIT_CONFIG_NOSYSTEM": "1"
```

Nesse modelo, **remova** os mounts para `/etc/gitconfig`, `/home/agent/.gitconfig` e `/home/agent/.config/git/config`, porque são deliberadamente ignorados.

### Modelo B — Git governado por `gitconfig-agent` controlado e RO

Use quando `gitconfig-agent` contém regras que de fato DEVEM governar o Git. A forma mais simples é manter uma única origem global controlada:

```json
"GIT_CONFIG_GLOBAL": "/home/agent/.gitconfig",
"GIT_CONFIG_NOSYSTEM": "1"
```

e manter somente o mount:

```text
source=${localWorkspaceFolder}/.devcontainer/control-plane/gitconfig-agent,target=/home/agent/.gitconfig,type=bind,readonly
```

Nesse modelo, remova os mounts redundantes para `/etc/gitconfig` e `/home/agent/.config/git/config`. Se a intenção for também impedir optional locks em `.git` RO, avalie adicionar `GIT_OPTIONAL_LOCKS=0` após teste do workflow Git de leitura.

## 7. Inventário de valores relevantes (não são campos novos)

| Caminho | Valor | Interpretação |
|---|---|---|
| `forwardPorts[0]` | `5173` | Porta padrão comum do Vite no projeto; forwarding da ferramenta, não publicação Docker. |
| `customizations.vscode.extensions[0]` | `anthropic.claude-code` | ID atual da extensão oficial Claude Code. |
| `customizations.vscode.extensions[1]` | `openai.chatgpt` | ID atual da extensão oficial OpenAI/Codex no Marketplace. |
| `runArgs[0]` | `--security-opt=no-new-privileges:true` | Hardening Linux/Docker. |
| `runArgs[1]` | `--cap-drop=ALL` | Hardening de capabilities. |
| `runArgs[2]` | `--add-host=host.docker.internal:host-gateway` | Conectividade deliberada com host gateway. |

## 8. Regras normativas de uso — SHOULD/MUST para este arquivo

- **MUST:** `workspaceFolder` deve permanecer coerente com o `target` de `workspaceMount`.
- **MUST:** `agent` deve existir na imagem e ter HOME/permissões compatíveis com os volumes persistentes e lifecycle scripts.
- **MUST:** escolher exatamente um modelo Git coerente (Modelo A ou B acima).
- **MUST:** tratar named volumes como persistentes; não assumir que rebuild apaga identidade, configuração ou credenciais neles.
- **MUST:** considerar `runbooks -> docs` uma substituição do conteúdo visível em `docs`, não um alias neutro.
- **MUST:** não versionar tokens reais em `containerEnv`, `remoteEnv` ou settings.
- **MUST:** não montar Docker socket, SSH agent socket ou credential stores se o agente não deve possuí-los.
- **SHOULD:** manter `no-new-privileges` e `cap-drop=ALL` enquanto os testes funcionais passarem.
- **SHOULD:** remover `--add-host=host.docker.internal:host-gateway` se nenhum fluxo concreto usa serviço no host.
- **SHOULD:** revisar `updateRemoteUserUID:false` em Linux nativo e documentar a estratégia de UID/GID.
- **SHOULD:** manter variáveis globais em `containerEnv` e reservar `remoteEnv` a overrides deliberados; se a duplicação for policy, validar igualdade automaticamente.
- **SHOULD:** usar `.dockerignore` rigoroso porque `build.context` alcança o diretório pai (`..`).
- **SHOULD:** manter ports mínimos e tratar `portsAttributes` como UX, nunca firewall.
- **SHOULD:** considerar settings Git/GitHub/Claude da IDE como defesa em profundidade, não como boundary de segurança.

## 9. Checklist de validação operacional

- [ ] `devcontainer.json` valida contra o schema da Dev Container Spec.
- [ ] `.devcontainer/Dockerfile` existe no path inferido por `build.dockerfile`.
- [ ] `.dockerignore` exclui segredos, caches e artefatos desnecessários do contexto `..`.
- [ ] `id agent` retorna o usuário esperado e `$HOME=/home/agent` é gravável.
- [ ] Em Linux host, `stat` do workspace é compatível com a decisão `updateRemoteUserUID`.
- [ ] `git status`, `git diff`, `git log` funcionam no modo read-only desejado.
- [ ] `git add`, `git commit` e operações que exigem escrita em `.git` falham quando essa é a policy.
- [ ] A policy `gitconfig-agent` é efetivamente lida **ou** seus mounts foram removidos conforme o modelo escolhido.
- [ ] Nenhum Docker socket está montado e nenhum endpoint Docker acessível é fornecido quando Docker-in-Docker/host access não é requisito.
- [ ] Nenhum SSH agent socket/chave privada é exposto quando SSH auth é proibida.
- [ ] `gh auth status` não encontra credencial quando o objetivo é ambiente não autenticado.
- [ ] `host.docker.internal` só existe se houver dependência real do host.
- [ ] Os targets `.git`, `.devcontainer`, `.github/workflows`, policies e instruções retornam erro em tentativa de escrita.
- [ ] `/home/agent/.claude`, `.codex` e `.npm` persistem de forma deliberada e têm política de limpeza/retenção.
- [ ] `/workspaces/cepraea-beach-pro/docs` contém `runbooks` por decisão explícita; nenhum `docs` original necessário foi ocultado.
- [ ] Vite escuta na porta 5173 e o forwarding funciona sem expor serviços adicionais.
- [ ] As extensões `anthropic.claude-code` e `openai.chatgpt` são permitidas pela política da organização e atualizadas/auditadas.
- [ ] `postStartCommand` passa após rebuild e após restart com volumes preexistentes.

## 10. Fontes primárias e especializadas

- **[S1] Dev Container Specification — base schema:** https://github.com/devcontainers/spec/blob/main/schemas/devContainer.base.schema.json
- **[S2] Dev Container Specification — supporting tools / VS Code customizations:** https://github.com/devcontainers/spec/blob/main/docs/specs/supporting-tools.md
- **[S3] VS Code — Environment variables in Dev Containers:** https://code.visualstudio.com/remote/advancedcontainers/environment-variables
- **[S4] VS Code — Add a non-root user to a container:** https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user
- **[S5] VS Code — Change the default source code mount:** https://code.visualstudio.com/remote/advancedcontainers/change-default-source-mount
- **[S6] Docker CLI — docker container run:** https://docs.docker.com/reference/cli/docker/container/run/
- **[S7] Docker Engine — Volumes:** https://docs.docker.com/engine/storage/volumes/
- **[S8] Docker Engine — Bind mounts:** https://docs.docker.com/engine/storage/bind-mounts/
- **[S9] Git — Environment variables and configuration behavior:** https://git-scm.com/docs/git
- **[S10] GitHub CLI — Environment variables:** https://cli.github.com/manual/gh_help_environment
- **[S11] Docker CLI — Environment variables / daemon endpoint:** https://docs.docker.com/reference/cli/docker/
- **[S12] OpenSSH — ssh-agent manual:** https://man.openbsd.org/ssh-agent.1
- **[S13] VS Code built-in Git extension manifest:** https://github.com/microsoft/vscode/blob/main/extensions/git/package.json
- **[S14] VS Code built-in GitHub extension manifest:** https://github.com/microsoft/vscode/blob/main/extensions/github/package.json
- **[S15] Claude Code — Permission modes:** https://code.claude.com/docs/en/permission-modes
- **[S16] Visual Studio Marketplace — Claude Code:** https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code
- **[S17] Visual Studio Marketplace — OpenAI Codex extension identifier openai.chatgpt:** https://marketplace.visualstudio.com/items?itemName=openai.chatgpt
- **[S18] OpenAI Codex — IDE extension documentation:** https://developers.openai.com/codex/ide

## 11. Conclusão arquitetural

A configuração tem uma arquitetura defensiva consistente: usuário `agent`, workspace editável, control-plane sobreposto como somente leitura, ausência deliberada de tokens e hardening de runtime. O problema principal não é de sintaxe; é de **coerência semântica entre metadados**. O caso Git demonstra por que um FIELD REGISTRY é necessário: campos individualmente válidos podem, em conjunto, cancelar uns aos outros.

A condição para considerar este `devcontainer.json` “governado” é: **resolver o modelo Git, validar UID/GID, justificar host-gateway, decidir conscientemente o overlay de `docs`, e tratar persistência/credenciais como capacidades explícitas**. Após essas decisões, o arquivo pode servir como uma boa baseline de Dev Container para agente com privilégio reduzido.
