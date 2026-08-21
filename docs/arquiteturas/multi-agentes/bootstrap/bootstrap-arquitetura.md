# ARQUITETURA DO FLUXO DE TRABALHO DOS AGENTES - CEPRAEA BEACH PRO

# Arquitetura determinística de bootstrap

O bootstrap deve ser tratado como um componente do plano de controle, não como uma instrução dada ao agente. Sua função é construir e provar que uma sessão está apta a executar determinadas operações.

O princípio central é:

> Nenhuma ferramenta protegida é liberada porque o agente afirmou ter lido ou executado o bootstrap. A liberação ocorre somente quando um verificador externo valida um manifesto ligado à sessão atual.

Isso transforma o bootstrap de um procedimento textual probabilístico em um protocolo executável, auditável e fail-closed.

## 1. Objetivos

A arquitetura deve garantir que:

1. cada sessão comece em estado bloqueado;
2. o bootstrap seja executado por código confiável, fora do controle do modelo;
3. todas as entradas relevantes sejam identificadas por hash;
4. os checks sejam determinísticos e tenham resultados estruturados;
5. um manifesto válido seja necessário para liberar ferramentas;
6. reinicializações e mudanças relevantes invalidem automaticamente o manifesto;
7. falhas nunca causem fallback silencioso para um ambiente menos protegido;
8. relatórios humanos sejam derivados dos mesmos resultados usados pelo verificador;
9. Git continue sendo a state machine do trabalho, sem criar uma state machine paralela de tarefas;
10. o bootstrap seja idempotente e seguro para repetição.

## 2. Distinção entre bootstrap, preflight e runbook

Esses mecanismos têm responsabilidades diferentes.

### Bootstrap de sessão

Executado uma vez por sessão válida, e novamente quando houver invalidação.

Verifica:

- identidade e versão do ambiente;
- montagem do workspace;
- ferramentas obrigatórias;
- configuração dos agentes;
- políticas e controles;
- permissões de filesystem;
- rede;
- sandbox;
- hooks;
- integridade dos verificadores;
- identidade do repositório;
- branch e estado inicial;
- ausência de condições inseguras.

O bootstrap não analisa detalhadamente cada tarefa.

### Preflight de operação

Executado antes de cada ação protegida ou grupo atômico de ações.

Verifica:

- se o manifesto ainda é válido;
- se pertence à sessão atual;
- se a operação está autorizada para o papel;
- se a tarefa e sua etapa estão identificadas;
- se os runbooks aplicáveis foram determinados;
- se houve mudança desde o bootstrap;
- se o comando solicitado é compatível com as permissões.

O preflight deve ser rápido e não reinstalar o ambiente.

### Runbook

Define como executar ou revisar uma classe de operação, como:

- alteração de código;
- banco de dados;
- documentação;
- dependências.

O bootstrap prova que o ambiente é confiável. O preflight prova que a ação atual está autorizada. O runbook define o procedimento especializado.

## 3. Ciclo de estados

Uma máquina de estados mínima pode ser:

```text
UNINITIALIZED
      |
      v
BOOTSTRAPPING
      |
      +---------- falha ----------> BLOCKED
      |
      v
BOOTSTRAPPED
      |
      v
VERIFIED
      |
      +---------- invalidação ----> STALE
      |                               |
      v                               v
READY                         BOOTSTRAPPING
      |
      +---------- violação -------> BLOCKED
```

Significados:

- `UNINITIALIZED`: nenhuma evidência válida existe.
- `BOOTSTRAPPING`: checks em execução; ferramentas protegidas continuam bloqueadas.
- `BOOTSTRAPPED`: os checks terminaram, mas o manifesto ainda não foi validado.
- `VERIFIED`: schema, hashes, identidade da sessão e resultados foram verificados.
- `READY`: capacidades explicitamente autorizadas podem ser utilizadas.
- `STALE`: alguma entrada mudou; o manifesto não pode mais liberar operações.
- `BLOCKED`: ocorreu falha obrigatória ou violação de integridade.

O agente não pode mudar diretamente esses estados. Eles pertencem ao controlador externo.

## 4. Identidade da sessão

O manifesto precisa estar vinculado a uma sessão concreta. Um timestamp isolado é insuficiente.

A identidade pode combinar:

- ID aleatório gerado pelo launcher;
- boot ID do sistema ou container;
- ID do container;
- processo-pai ou sessão do Codex/Claude;
- caminho canônico do workspace;
- identidade do repositório;
- hash do commit inicial;
- hash das configurações do agente;
- nonce mantido pelo controlador.

Exemplo conceitual:

```json
{
  "session": {
    "session_id": "uuid",
    "boot_id": "...",
    "container_id": "...",
    "workspace": "/workspaces/cepraea-beach-pro",
    "repository_id": "...",
    "started_at": "2026-08-19T12:00:00Z"
  }
}
```

Copiar um manifesto de outra sessão não deve produzir autorização.

## 5. Entradas normativas

O bootstrap deve enumerar explicitamente suas entradas. Não pode depender de “todos os arquivos que parecerem relevantes”.

Entradas possíveis:

- configuração root-owned do ambiente;
- `AGENT_POLICY.md`;
- `AGENTS.md`;
- `CLAUDE.md`;
- `.codex/config.toml`;
- configurações gerenciadas do Claude;
- índice dos runbooks;
- schema do manifesto;
- verificador do bootstrap;
- hooks obrigatórios;
- configuração do Dev Container;
- versões mínimas das ferramentas;
- decisão humana que promoveu o bootstrap;
- perfil operacional: `BASE` ou `HARDENED`.

Cada entrada deve registrar:

- caminho ou identificador;
- tipo;
- autoridade;
- hash criptográfico;
- versão esperada;
- obrigatoriedade;
- resultado da leitura.

Isso permite distinguir “arquivo mencionado” de “arquivo realmente lido e verificado”.

## 6. Checks determinísticos

Cada check precisa possuir:

- identificador estável;
- versão;
- entradas declaradas;
- algoritmo conhecido;
- resultado enumerado;
- evidência estruturada;
- severidade;
- comportamento em falha.

Resultados recomendados:

```text
PASS
FAIL
NOT_APPLICABLE
UNAVAILABLE
ERROR
```

`UNAVAILABLE` não pode ser convertido automaticamente em `PASS`.

Exemplo:

```json
{
  "id": "ENV-PYTHON-001",
  "version": 1,
  "required": true,
  "result": "FAIL",
  "expected": "python >= 3.11",
  "observed": "executable not found",
  "evidence": {
    "probe": "command-resolution",
    "exit_code": 1
  }
}
```

Os checks não devem depender da interpretação do modelo. O agente pode explicar o resultado, mas não defini-lo.

## 7. Classes de checks

### Integridade

- schema válido;
- verificadores com hashes esperados;
- hooks presentes e íntegros;
- políticas presentes;
- configurações sem alterações não autorizadas.

### Ambiente

- sistema operacional;
- arquitetura;
- container;
- runtimes obrigatórios;
- versões de Node, Python, Git e CLIs;
- locale, timezone e relógio;
- variáveis obrigatórias e proibidas.

Segredos não devem ser copiados para o manifesto. Registra-se apenas presença, origem autorizada ou hash não reversível quando indispensável.

### Filesystem

- workspace correto;
- corpus controlado read-only;
- projeto read-only para o Reviewer;
- diretórios temporários graváveis;
- `.git` conforme o papel e a arquitetura;
- ausência de symlinks ou junctions perigosos;
- mounts compatíveis com o perfil.

### Rede

- rede desabilitada para review normal;
- destinos permitidos quando uma operação exigir rede;
- ausência de fallback irrestrito;
- coerência entre política declarada e capability real.

### Sandbox

- inicialização bem-sucedida;
- capability tests reais;
- bloqueio de escrita fora dos destinos autorizados;
- bloqueio de rede quando exigido;
- fail-closed.

O erro de `bubblewrap` observado anteriormente deveria resultar em um check estruturado. No perfil em que o nested sandbox seja obrigatório, isso deve bloquear a sessão. Não deve provocar uma execução externa automática.

### Git

- repositório correto;
- branch;
- commit inicial;
- worktree;
- alterações existentes;
- operações permitidas para o papel;
- hooks relevantes.

O bootstrap não deve limpar, restaurar ou modificar Git.

### Identidade e papel

- agente identificado;
- papel: `EXECUTOR` ou `REVIEWER`;
- conjunto de capacidades derivado do papel;
- política aplicável;
- proibição de autopromoção de autoridade.

## 8. Manifesto canônico

O manifesto é o artefato técnico central. Ele deve ser:

- JSON canônico;
- validado por JSON Schema;
- escrito atomicamente;
- imutável depois de finalizado;
- associado à sessão;
- protegido contra substituição;
- pequeno o suficiente para validação rápida;
- completo o suficiente para reproduzir a decisão.

Estrutura conceitual:

```json
{
  "schema_version": "1.0.0",
  "bootstrap_version": "1.0.0",
  "manifest_id": "uuid",
  "session": {},
  "role": "REVIEWER",
  "profile": "BASE",
  "inputs": [],
  "checks": [],
  "capabilities": {
    "granted": [],
    "denied": []
  },
  "summary": {
    "required_passed": 18,
    "required_failed": 0,
    "optional_unavailable": 1
  },
  "final_state": "READY",
  "started_at": "...",
  "completed_at": "...",
  "expires_at": "...",
  "integrity": {
    "algorithm": "sha256",
    "payload_digest": "..."
  }
}
```

O campo `capabilities.granted` deve ser calculado pelo controlador, nunca preenchido por texto produzido pelo agente.

## 9. Localização e persistência

O manifesto de sessão não deve ser versionado automaticamente no Git.

Locais adequados incluem:

- diretório runtime root-owned;
- volume efêmero controlado;
- `/run/...` dentro do container;
- diretório temporário com ownership e permissões verificadas.

Não é recomendável colocá-lo no working tree porque:

- criaria ruído;
- poderia ser alterado pelo Executor;
- contaminaria `git status`;
- confundiria estado operacional efêmero com estado versionado do produto.

Evidências materiais de falha podem ser exportadas conscientemente para um local autorizado, mas isso é diferente do manifesto runtime.

## 10. Relatórios

O manifesto é a fonte estruturada. Relatórios são projeções derivadas.

Devem existir três níveis:

### Resumo imediato

Saída curta:

```text
Bootstrap: BLOCKED
2 checks obrigatórios falharam:
- SANDBOX-INIT-001
- ENV-PYTHON-001
Manifest: /run/cepraea/bootstrap/...
```

### Relatório técnico de falha

Gerado automaticamente quando houver falha, com:

- checks;
- resultados;
- evidências;
- impacto nas capacidades;
- indicação do responsável pela correção;
- nenhuma alegação além da evidência.

### Relatório persistente

Somente quando:

- exigido por uma tarefa;
- necessário para auditoria;
- houver incidente material;
- houver decisão humana para promoção de perfil;
- constituir evidência de acceptance test.

Relatórios recorrentes não devem criar uma state machine paralela ao Git.

## 11. Liberação de ferramentas

O ponto mais importante é colocar o bootstrap no caminho técnico das ferramentas.

Fluxo:

```text
Solicitação do agente
        |
        v
Tool gateway / hook externo
        |
        v
Manifesto existe?
   não --> BLOQUEAR
        |
       sim
        |
        v
Schema e integridade válidos?
   não --> BLOQUEAR
        |
       sim
        |
        v
Sessão e entradas ainda coincidem?
   não --> INVALIDAR E BLOQUEAR
        |
       sim
        |
        v
Capacidade cobre a operação?
   não --> BLOQUEAR
        |
       sim
        |
        v
Preflight específico
        |
        v
Executar operação
```

O agente não deve conseguir:

- escolher seu próprio manifesto;
- alterar o estado para `READY`;
- dispensar um check;
- transformar `FAIL` em warning;
- executar diretamente uma ferramenta protegida contornando o gateway.

## 12. Granularidade das capacidades

Não deve existir uma permissão genérica “bootstrap aprovado”.

Capacidades devem ser específicas, por exemplo:

```text
workspace.read
workspace.write.executor_scope
git.inspect
git.mutate.denied
network.github.catalog.read
tmp.write
review.run_checks
skills.list
skills.install
```

Assim, um bootstrap pode liberar leitura do catálogo de skills sem liberar instalação. A instalação pode exigir:

- runtime disponível;
- rede autorizada;
- destino gravável;
- origem permitida;
- integridade do pacote;
- autorização humana específica.

## 13. Invalidação

O manifesto deve ser invalidado quando ocorrer qualquer mudança relevante:

- reinício do computador;
- reinício ou recriação do container;
- nova sessão do agente;
- mudança de papel;
- mudança no workspace;
- mudança de branch quando material;
- mudança nas políticas;
- mudança em hooks ou verificadores;
- atualização do Codex, Claude ou runtime relevante;
- mudança no perfil de segurança;
- mount alterado;
- expiração;
- perda do processo controlador;
- alteração na configuração de rede;
- falha de capability test.

A invalidação deve ocorrer por comparação objetiva, não porque o agente “percebeu” a mudança.

## 14. Idempotência

Executar o bootstrap duas vezes sobre o mesmo estado deve produzir:

- os mesmos resultados materiais;
- as mesmas capacidades;
- diferenças apenas em campos não semânticos, como IDs e timestamps;
- nenhuma alteração destrutiva;
- nenhuma duplicação de configuração;
- nenhuma instalação implícita.

É útil separar:

```text
bootstrap --check
bootstrap --provision
bootstrap --verify
```

- `--check`: identifica o estado sem modificá-lo.
- `--provision`: realiza mudanças explicitamente autorizadas.
- `--verify`: confirma o estado final e gera o manifesto.

O bootstrap de verificação não deve instalar Python silenciosamente só porque Python está ausente. Provisionamento é uma operação diferente, com autoridade e risco próprios.

## 15. Falhas e fail-closed

Regras fundamentais:

- falha do bootstrap bloqueia;
- falha do verificador bloqueia;
- manifesto ausente bloqueia;
- manifesto inválido bloqueia;
- estado desconhecido bloqueia;
- mismatch de sessão bloqueia;
- check obrigatório indisponível bloqueia;
- timeout bloqueia;
- fallback para execução menos protegida é proibido quando o controle é obrigatório.

O resultado deve indicar se a correção pertence:

- ao Executor;
- ao Reviewer;
- ao ambiente;
- ao humano;
- ao administrador da infraestrutura.

Bloquear não significa automaticamente `HUMAN_DECISION_REQUIRED`. Esse verdict só cabe quando há realmente uma decisão material humana, não quando existe uma falha técnica corrigível e já contratada.

## 16. Relação com o modelo Executor–Reviewer

O bootstrap deve gerar manifestos distintos por papel.

### Executor

Pode receber capacidades limitadas de escrita no escopo autorizado, mas não:

- commit;
- push;
- alteração de políticas;
- alteração de fontes controladas;
- autopromoção de permissões.

### Reviewer

Deve permanecer:

- read-only no projeto;
- com escrita apenas em armazenamento efêmero autorizado;
- sem mutação de Git;
- sem correção dos próprios findings;
- sem escalation automática.

O Reviewer deve poder verificar o manifesto do Executor quando isso fizer parte da evidência, mas não deve poder aprová-lo ou reescrevê-lo.

## 17. Promoção ao caminho crítico

A política atual determina corretamente que documentação candidata não pode bloquear operações. Para tornar o bootstrap obrigatório, é necessário um processo explícito de promoção:

1. arquitetura aprovada;
2. schema definido;
3. implementação do bootstrap;
4. verificador independente;
5. capability tests no ambiente real;
6. testes negativos;
7. integração com o gateway de ferramentas;
8. procedimento de recuperação;
9. decisão humana explícita de promoção;
10. somente então ativação fail-closed.

Antes da promoção, o bootstrap pode operar em modo de observação:

```text
OBSERVE → WARN → ENFORCE
```

Mas o modo deve estar explícito no manifesto. Um sistema em `OBSERVE` não pode alegar enforcement.

## 18. Testes de aceitação

O bootstrap precisa ser refutável. Testes mínimos:

- manifesto ausente bloqueia;
- manifesto de outra sessão bloqueia;
- manifesto adulterado bloqueia;
- política alterada invalida;
- hook removido invalida;
- sandbox indisponível bloqueia no perfil obrigatório;
- ferramenta ausente produz `FAIL`;
- runtime incompatível produz `FAIL`;
- reinício invalida;
- container recriado invalida;
- Reviewer não consegue escrever no workspace;
- Executor não consegue modificar Git;
- rede proibida permanece inacessível;
- relatório concorda exatamente com o manifesto;
- repetição não altera o ambiente;
- falha parcial não deixa manifesto `READY`;
- interrupção durante escrita não produz manifesto válido;
- agente não consegue fabricar autorização apenas por texto.

## 19. Observabilidade sem excesso de logs

Métricas úteis:

- duração do bootstrap;
- checks aprovados e reprovados;
- causas de invalidação;
- versões do bootstrap;
- frequência de falhas;
- diferença entre perfis;
- tentativas bloqueadas pelo gateway.

Não devem ser registrados:

- prompts completos por padrão;
- conteúdo de segredos;
- logs de interação usados como state machine;
- relatórios duplicados sem finalidade operacional.

## 20. Aplicação ao incidente observado

Na situação discutida, o comportamento robusto seria:

1. reinício invalida o manifesto anterior;
2. nova sessão começa bloqueada;
3. o launcher executa o bootstrap;
4. o bootstrap verifica o sandbox;
5. a falha do `bubblewrap` é registrada;
6. o perfil determina se essa falha bloqueia;
7. o runtime Python é verificado;
8. a ausência de Python é registrada;
9. `skills.list` permanece bloqueado se Python for requisito;
10. nenhuma execução externa é iniciada automaticamente;
11. o sistema apresenta o manifesto e a correção necessária;
12. após provisionamento autorizado, o bootstrap é reexecutado;
13. somente um novo manifesto `READY` libera a capacidade.

Nesse desenho, não importa se o modelo “lembrou” do bootstrap. Ele simplesmente não recebe acesso à operação antes da prova verificável.

## 21. Decisões de autoridade humana

hardening somente entra no caminho crítico depois de verificação executável e promoção humana explícita.
Até essa promoção, ela deve ser descrita como proposta, não como controle existente.

A decisão central é separar o bootstrap em duas camadas:

1. **Bootstrap do ambiente**, executado na criação/reinicialização do container.
2. **Validação da sessão**, executada ao iniciar cada agente e consultada antes das ferramentas.

O controlador deve ser externo ao modelo, e o manifesto deve ser uma consequência técnica da validação — não um documento produzido pelo agente.

## Decisões por necessidades

| Necessidade | Decisão | Impacto no bootstrap |
|---|---|---|
| Onde executar o controlador | Supervisor root-owned dentro do Dev Container, iniciado pelo entrypoint. O launcher cria a identidade da sessão. | O bootstrap acontece mesmo que o agente não “lembre” dele. Reiniciar o container remove a autorização anterior. |
| Proprietário dos arquivos runtime | `root` ou usuário técnico exclusivo; agentes apenas leem o resultado necessário. | Impede que Executor ou Reviewer fabriquem um manifesto `READY`. |
| Checks em `BASE` e `HARDENED` | `BASE` verifica controles obrigatórios e compatibilidade. `HARDENED` acrescenta capability tests reais de isolamento. | `BASE` permanece rápido e utilizável; `HARDENED` só é liberado quando o host suporta os controles adicionais. |
| Ferramentas no gateway | Todas as ferramentas passam por uma checagem leve; shell, escrita, rede, Git e integrações recebem preflight detalhado. | Não existe caminho alternativo desprotegido. Leituras comuns continuam rápidas por cache do manifesto. |
| Expiração da sessão | Vincular ao processo e ao boot do container, com limite máximo adicional. | Encerrar o agente ou recriar o container invalida a autorização automaticamente. |
| Eventos de invalidação | Usar identidade e hashes objetivos, não interpretação do agente. | Mudanças materiais fazem a sessão voltar a `STALE` ou `BLOCKED`. |
| Capacidades por papel | Privilégio mínimo e capacidades explícitas para Executor, Reviewer e humano. | O mesmo bootstrap produz autorizações diferentes conforme o papel autenticado. |
| Schema e verificador | Fonte versionada no repositório protegido; cópia promovida e imutável instalada na imagem. | Há auditabilidade no Git e integridade operacional fora do alcance dos agentes. |
| Retenção de relatórios | Manifestos de sucesso efêmeros; falhas materiais retidas por prazo definido fora do working tree. | Evita poluir o Git e preserva evidência útil para diagnóstico. |
| Provisionamento | Processo separado do bootstrap, preferencialmente durante o build da imagem. | Bootstrap verifica; não instala dependências silenciosamente nem muda o ambiente. |
| Recuperação | Fail-closed, diagnóstico estruturado e recuperação humana controlada. | Falha nunca resulta em fallback unsandboxed ou redução automática de segurança. |
| Promoção para `ENFORCE` | Acceptance tests, testes negativos, rollback comprovado e decisão humana registrada. | O bootstrap só passa a bloquear trabalho quando estiver operacionalmente comprovado. |

## 1. Local de execução do controlador

### Decisão

Usar dois componentes:

```text
Dev Container entrypoint
        |
        +-- cria identidade do ambiente
        +-- inicia controlador root-owned
        +-- executa bootstrap do container
        |
        v
Launcher do agente
        |
        +-- solicita uma sessão ao controlador
        +-- recebe somente session_id
        |
        v
Tool gateway
        |
        +-- consulta o controlador
        +-- libera ou bloqueia a operação
```

O controlador deve ser um processo pequeno, determinístico e sem dependência do modelo. Ele pode ser um daemon local ou um wrapper obrigatório em torno das ferramentas.

O agente não deve:

- iniciar o controlador;
- escolher o perfil;
- editar seus arquivos;
- declarar que o bootstrap terminou;
- selecionar um manifesto antigo;
- contornar o gateway.

### Impacto

Isso elimina o problema observado: mesmo que o modelo ignore o bootstrap, as ferramentas continuam bloqueadas.

Também preserva o uso humano do container. O controlador deve distinguir processos de agentes de operações humanas no VS Code e terminal.

## 2. Propriedade dos arquivos runtime

### Decisão

Usar um diretório efêmero como:

```text
/run/cepraea-bootstrap/
├── controller.sock
├── environment.json
├── sessions/
│   └── <session-id>.json
└── reports/
```

Propriedade sugerida:

```text
root:cepraea-control
```

Permissões conceituais:

- controlador: leitura e escrita;
- gateway: leitura ou consulta pelo socket;
- agentes: sem escrita;
- humano administrador: acesso controlado;
- aplicação CEPRAEA: nenhum acesso necessário.

Para integridade adicional, o manifesto pode conter um MAC ou assinatura gerada com chave inacessível aos agentes. Em ambiente local, ownership root e consulta por socket já oferecem uma base forte; assinatura ajuda quando o manifesto precisa ser exportado.

### Impacto

Um arquivo JSON gravável pelo agente não é evidência confiável. A propriedade externa transforma o manifesto em atestado do controlador.

## 3. Checks obrigatórios

### Perfil `BASE`

O perfil `BASE` deve exigir:

- identidade do container e da sessão;
- identidade do repositório e workspace;
- papel autenticado do agente;
- hashes das políticas e configurações promovidas;
- integridade do controlador, gateway e hooks;
- versões mínimas das ferramentas necessárias;
- mounts esperados;
- permissões efetivas do workspace;
- corpus controlado read-only;
- política de Git conforme o papel;
- diretório temporário disponível;
- ausência de segredos de produção;
- saúde do gateway;
- schema e verificador compatíveis;
- relógio suficientemente confiável;
- estado inicial do Git registrado, sem modificá-lo.

Para o Reviewer, deve ser testado que o projeto é realmente read-only. Para o Executor, devem ser testados os limites de escrita e o bloqueio de operações Git reservadas ao humano.

### Perfil `HARDENED`

Além do `BASE`:

- nested sandbox inicializa corretamente;
- tentativa controlada de escrita proibida falha;
- tentativa controlada de rede proibida falha;
- escape por symlink não funciona;
- `.git` não pode ser alterado pelo processo do agente;
- subprocessos herdam as restrições;
- fallback unsandboxed é impossível;
- seccomp, namespaces ou controles equivalentes estão ativos;
- capability tests correspondem ao host e kernel reais.

### Impacto

O perfil não pode ser apenas uma configuração declarada. Deve representar capacidades demonstradas.

Uma falha como a do `bubblewrap` teria os seguintes efeitos:

- em `BASE`, pode ser `NOT_APPLICABLE` se o nested sandbox não for requisito do perfil;
- em `HARDENED`, é `FAIL` obrigatório e bloqueia a sessão;
- nunca autoriza execução externa automática.

## 4. Ferramentas que passam pelo gateway

### Decisão

Todas as ferramentas devem consultar o gateway, mas com níveis diferentes.

#### Checagem básica para todas

- sessão existe;
- manifesto é válido;
- sessão não expirou;
- hashes críticos continuam compatíveis;
- papel possui a capacidade solicitada.

#### Preflight detalhado para operações sensíveis

- comandos de shell;
- escrita e edição;
- Git;
- rede;
- instalação de dependências ou skills;
- ferramentas externas;
- MCPs e conectores;
- banco de dados;
- deploy;
- manipulação de credenciais;
- alteração de políticas ou infraestrutura.

### Impacto

Passar tudo pelo gateway fecha rotas alternativas. O custo pode ser reduzido mantendo em memória o estado validado e repetindo apenas verificações baratas por chamada.

Uma listagem de skills poderia exigir:

```text
skills.catalog.read
network.github.read
runtime.python.execute
```

A instalação exigiria adicionalmente:

```text
skills.install
codex_skills_directory.write
artifact.integrity.verify
human_authorization
```

Assim, conseguir listar não implica poder instalar.

## 5. Expiração da sessão

### Decisão

A sessão deve expirar no primeiro destes eventos:

- processo do agente termina;
- launcher encerra a sessão;
- container é reiniciado ou recriado;
- boot ID muda;
- controlador reinicia sem recuperação segura;
- limite máximo de duração é alcançado;
- período de inatividade, se operacionalmente necessário;
- evento de invalidação material ocorre.

Um default razoável:

- validade ligada à vida do processo;
- máximo de 12 horas;
- renovação somente pelo controlador;
- renovação exige revalidação das entradas críticas.

O limite deve ser configurável e promovido como parte da política, não escolhido pelo agente.

### Impacto

TTL muito curto causa bootstraps repetitivos. TTL muito longo mantém autorizações antigas. Vincular a sessão ao processo e aos eventos materiais é mais importante que o relógio.

## 6. Eventos de invalidação imediata

### Decisão

Invalidar quando ocorrer:

- reinício da máquina;
- reinício ou recriação do container;
- reinício inesperado do controlador;
- nova sessão do agente;
- mudança de papel;
- mudança de workspace ou repositório;
- mudança das políticas promovidas;
- mudança do schema ou verificador;
- alteração de hooks ou gateway;
- atualização do Codex, Claude ou runtime relevante;
- alteração de mounts;
- alteração do perfil `BASE`/`HARDENED`;
- perda de um controle obrigatório;
- mudança relevante na configuração de rede;
- alteração de permissões;
- adulteração do manifesto;
- divergência entre imagem e versão promovida.

Mudanças comuns do working tree não devem necessariamente exigir bootstrap completo.
Elas pertencem ao preflight da tarefa. Alterar código da aplicação não é o mesmo que alterar o plano de controle.

### Impacto

Separar invalidação ambiental de mudança normal do projeto evita executar um bootstrap pesado após cada edição.

## 7. Capacidades por papel

### Executor

Decisão:

- ler o workspace;
- escrever apenas nos alvos autorizados;
- executar validadores e testes;
- escrever em temporários e caches permitidos;
- usar rede somente quando a tarefa autorizar;
- inspecionar Git;
- não executar commit, push, merge, reset ou alterações de refs;
- não alterar políticas, hooks ou controlador;
- não promover seu próprio manifesto.

### Reviewer

Decisão:

- ler o workspace;
- ler diff, status e evidências;
- executar checks independentes;
- escrever apenas em `/tmp` e caches técnicos autorizados;
- não editar o projeto;
- não alterar Git;
- rede desabilitada por padrão;
- rede temporária apenas para uma operação explicitamente autorizada;
- não corrigir findings.

### Humano

Decisão:

- autoridade para Git, promoção e provisionamento;
- acesso separado das identidades de processo dos agentes;
- operações críticas registradas;
- capacidade de recuperação e break-glass;
- nenhuma dependência do runtime da aplicação.

### Impacto

O manifesto não deve dizer apenas `READY`. Deve declarar capacidades concretas:

```json
{
  "granted": [
    "workspace.read",
    "git.inspect",
    "tmp.write",
    "review.checks.execute"
  ],
  "denied": [
    "workspace.write",
    "git.mutate",
    "network.access",
    "bootstrap.promote"
  ]
}
```

## 8. Localização do schema e do verificador

### Decisão

Manter duas representações deliberadas:

```text
Repositório:
.ai/control/bootstrap/
├── bootstrap-manifest.schema.json
├── bootstrap-policy.json
├── verify-bootstrap.mjs
└── acceptance/
```

```text
Imagem promovida:
/opt/cepraea/bootstrap/
├── bootstrap-manifest.schema.json
├── bootstrap-policy.json
├── verify-bootstrap
└── promoted-digests.json
```

O repositório fornece:

- revisão;
- histórico;
- autoria;
- proposta de mudança;
- testes.

A cópia instalada na imagem fornece:

- imutabilidade operacional;
- independência do working tree;
- proteção contra alteração pelo agente.

A imagem deve registrar qual commit ou digest foi promovido.

### Impacto

Executar o verificador diretamente de um working tree gravável permitiria que o mesmo ator alterasse a regra e depois “passasse” na regra modificada.

## 9. Retenção de manifestos e relatórios

### Decisão

- manifesto atual de sessão: retido apenas durante a sessão;
- manifestos de sucesso: descartados ao finalizar ou preservados por até 7 dias fora do Git, se úteis para métricas;
- relatórios de falha operacional: 30 dias;
- incidentes de segurança: conforme política específica, possivelmente prazo maior;
- evidência usada para promover `HARDENED`: persistida e versionada conscientemente;
- nenhum prompt, segredo ou conteúdo de arquivos sensíveis;
- rotação e limite de tamanho obrigatórios.

Relatórios persistentes devem conter IDs e hashes, não cópias indiscriminadas dos arquivos inspecionados.

### Impacto

Isso mantém auditabilidade sem criar `executions/**`, `STATE.md` ou uma segunda state machine dentro do projeto.

## 10. Procedimento de provisionamento

### Decisão

Separar rigorosamente:

```text
PROVISIONAR → VERIFICAR → ATESTAR
```

#### Provisionar

- instalar runtimes;
- configurar usuários e grupos;
- instalar controlador;
- configurar hooks;
- criar diretórios;
- aplicar permissões;
- construir a imagem.

#### Verificar

- não alterar o ambiente;
- executar probes;
- comparar versões e hashes;
- testar capabilities.

#### Atestar

- gerar manifesto;
- validar schema;
- calcular integridade;
- liberar capacidades.

Provisionamento deve ocorrer preferencialmente no build da imagem, usando versões pinadas e lockfiles. Instalações em runtime devem ser exceções explícitas.

### Impacto

A ausência de Python resulta em diagnóstico claro. O bootstrap não deve instalar Python por conta própria, pois isso tornaria a verificação mutável, dependente de rede e menos reproduzível.

## 11. Recuperação

### Decisão

A recuperação deve ser orientada pelo tipo de falha:

```text
Falha de sessão
→ encerrar e criar nova sessão

Falha de configuração
→ corrigir fonte versionada, reconstruir e verificar

Falha de imagem
→ reconstruir ou fazer rollback para imagem promovida

Falha de capability
→ voltar ao perfil BASE, somente se isso for previamente autorizado

Falha de integridade
→ bloquear, preservar evidência e exigir intervenção humana
```

Break-glass deve:

- pertencer somente ao humano;
- ter duração curta;
- registrar motivo;
- não produzir manifesto normal `READY`;
- usar um estado distinto, como `EMERGENCY_OVERRIDE`;
- nunca ser acionado pelo agente;
- exigir nova inicialização depois do uso.

### Impacto

Não deve existir “tentar novamente fora do sandbox” como recuperação automática.
Isso converte falha de segurança em redução silenciosa de proteção.

## 12. Promoção para `ENFORCE`

### Decisão

Adotar estágios formais:

```text
DESIGN
  ↓
OBSERVE
  ↓
WARN
  ↓
ENFORCE_BASE
  ↓
ENFORCE_HARDENED
```

### Critérios mínimos

Antes de `ENFORCE_BASE`:

- schema validado;
- controlador e gateway instalados;
- integração com todas as ferramentas protegidas;
- testes positivos;
- testes negativos;
- teste de reinicialização;
- teste de manifesto adulterado;
- teste de sessão expirada;
- teste de bypass;
- rollback documentado e ensaiado;
- comportamento humano não prejudicado;
- pelo menos duas inicializações limpas e reproduzíveis;
- decisão humana registrando versão e digests promovidos.

Antes de `ENFORCE_HARDENED`:

- acceptance tests no host e container reais;
- nested sandbox comprovadamente compatível;
- testes de filesystem e rede;
- subprocessos confinados;
- nenhum fallback unsandboxed;
- estabilidade observada durante período definido;
- recuperação e rollback testados;
- nova decisão humana de promoção.

### Impacto

Uma documentação aprovada não basta. `ENFORCE` significa que uma tentativa real de bypass falha tecnicamente.

## Fluxo operacional recomendado

### Criação do container

```text
1. Entrypoint inicia.
2. Controlador verifica sua própria integridade.
3. Provisionamento previamente incorporado à imagem é confirmado.
4. Checks ambientais são executados.
5. Manifesto do ambiente é criado atomicamente.
6. Estado fica ENVIRONMENT_READY ou BLOCKED.
```

### Início do agente

```text
1. Launcher autentica o papel.
2. Controlador cria session_id e nonce.
3. Políticas e configurações do papel são verificadas.
4. Capability tests aplicáveis são executados.
5. Manifesto da sessão é criado.
6. Gateway recebe as capacidades concedidas.
7. Agente inicia somente depois do estado READY.
```

### Chamada de ferramenta

```text
1. Gateway recebe session_id, ferramenta e argumentos.
2. Valida sessão e integridade.
3. Verifica invalidações.
4. Mapeia a chamada para uma capacidade.
5. Executa preflight específico.
6. Libera ou bloqueia.
7. Registra somente evidência operacional mínima.
```

### Reinicialização

```text
1. Boot/container ID muda.
2. Manifestos anteriores deixam de corresponder.
3. Gateway bloqueia chamadas antigas.
4. Novo bootstrap é obrigatório.
5. Nenhuma lembrança do modelo é relevante.
```

## Defaults recomendados

Como ponto de partida:

```yaml
controller:
  location: container
  owner: root
  agent_writable: false

runtime:
  location: /run/cepraea-bootstrap
  persistence: ephemeral

session:
  bind_to_process: true
  bind_to_container_boot: true
  max_duration: 12h
  renew_with_revalidation: true

gateway:
  all_tools: basic_check
  shell_write_git_network_mcp: detailed_preflight
  fail_closed: true

reports:
  success_retention: ephemeral
  failure_retention: 30d
  secrets: forbidden
  working_tree_storage: forbidden

provisioning:
  preferred_stage: image_build
  runtime_installation: explicit_only

promotion:
  initial_mode: observe
  base_enforcement: human_approved
  hardened_enforcement: capability_tested_and_human_approved
```

O efeito esperado é um bootstrap rápido no uso normal, rigoroso nos eventos materiais e independente da memória ou obediência do agente.
O modelo passa a explicar decisões do controlador, mas deixa de ser responsável por garantir que o bootstrap aconteceu.

Entendido. O objetivo é definir o estado necessário da arquitetura, independentemente das limitações do ambiente atual. Considerando as recomendações como decisões humanas já adotadas, os registros devem ter status `ACCEPTED`, mas sua aplicação operacional continuará em `OBSERVE` até que os critérios formais de promoção para `ENFORCE` sejam satisfeitos.

Abaixo está o conjunto completo de registros formais e as ações necessárias para torná-los efetivos.

# Conjunto de decisões

## DEC-BOOT-001 — Controlador externo ao agente

**Status:** `ACCEPTED`
**Título:** Execução do controlador de bootstrap no Dev Container
**Decisão:** O bootstrap será controlado por um supervisor root-owned executado dentro do Dev Container e iniciado obrigatoriamente pelo entrypoint. O launcher criará a identidade de cada sessão de agente.

### Contexto

Instruções textuais não garantem que o agente execute o bootstrap. O controle precisa existir fora do modelo e anteceder o acesso às ferramentas.

### Regras normativas

- O controlador não pode ser iniciado, encerrado ou reconfigurado pelo agente.
- O entrypoint não pode iniciar agentes antes de verificar a saúde do controlador.
- Toda sessão deve receber identidade própria.
- Reiniciar ou recriar o container invalida todas as sessões anteriores.
- A ausência do controlador resulta em estado `BLOCKED`.
- Não pode existir fallback direto para ferramentas protegidas.

### Consequências

- O bootstrap independe da memória ou interpretação do agente.
- Falha no controlador impede o início de sessões.
- O entrypoint passa a ser parte do plano de controle.

### Ações necessárias

1. Implementar um serviço `bootstrap-controller`.
2. Instalá-lo na imagem do Dev Container.
3. Iniciá-lo pelo entrypoint antes dos agentes.
4. Criar health check determinístico.
5. Criar socket local protegido para consultas.
6. Fazer o launcher solicitar uma sessão ao controlador.
7. Bloquear o launcher quando o controlador estiver ausente ou inválido.
8. Implementar teste que prove que o agente não inicia sem controlador.
9. Implementar teste de reinicialização do container.
10. Documentar rollback do controlador.

### Critério de conformidade

Um agente não consegue iniciar uma sessão operacional nem acessar ferramentas protegidas quando o controlador está ausente, inválido ou indisponível.

---

## DEC-BOOT-002 — Propriedade protegida dos artefatos runtime

**Status:** `ACCEPTED`
**Título:** Propriedade e proteção dos arquivos runtime do bootstrap
**Decisão:** Todos os manifestos, estados e canais de comunicação runtime serão propriedade de `root` ou de usuário técnico exclusivo. Executor e Reviewer não terão permissão de escrita.

### Contexto

Um manifesto gravável pelo agente não pode provar que o próprio agente foi validado.

### Regras normativas

- O diretório runtime deve ficar fora do working tree.
- O diretório deve ser efêmero e recriado no início do container.
- Agentes não podem criar, editar, substituir ou remover manifestos.
- O estado autorizado deve ser consultado pelo gateway.
- Arquivos temporários não finalizados não podem ser interpretados como válidos.
- Escrita de manifestos deve ser atômica.
- O controlador deve rejeitar arquivos com owner, modo ou integridade incorretos.

### Local recomendado

```text
/run/cepraea-bootstrap/
├── controller.sock
├── environment.json
├── sessions/
└── reports/
```

### Ações necessárias

1. Criar usuário ou grupo técnico do controlador.
2. Criar o diretório runtime no entrypoint.
3. Definir owner e modos de acesso.
4. Proibir escrita pelos processos dos agentes.
5. Implementar escrita em arquivo temporário seguida de rename atômico.
6. Incluir digest ou MAC de integridade.
7. Validar owner e permissões antes de aceitar um manifesto.
8. Testar tentativa de adulteração por Executor.
9. Testar tentativa de adulteração por Reviewer.
10. Garantir que o working tree permaneça sem artefatos runtime.

### Critério de conformidade

Nenhum processo de agente consegue produzir ou modificar um manifesto que o gateway aceite como válido.

---

## DEC-BOOT-003 — Perfis `BASE` e `HARDENED`

**Status:** `ACCEPTED`
**Título:** Separação entre controles obrigatórios e hardening dependente de capability
**Decisão:** O perfil `BASE` verificará os controles operacionais obrigatórios. O perfil `HARDENED` adicionará capability tests reais de isolamento e somente poderá ser ativado em ambientes aprovados.

### Perfil `BASE`

Checks obrigatórios:

- identidade do ambiente;
- identidade da sessão;
- papel do agente;
- workspace e repositório esperados;
- integridade de política, gateway e verificador;
- versões mínimas das ferramentas;
- mounts obrigatórios;
- permissões do workspace;
- proteção das fontes controladas;
- restrições de Git;
- temporários autorizados;
- ausência de segredos proibidos;
- saúde do controlador;
- validade do schema;
- estado inicial do Git.

### Perfil `HARDENED`

Checks adicionais:

- sandbox inicializa corretamente;
- escrita proibida é realmente bloqueada;
- rede proibida é realmente bloqueada;
- subprocessos herdam restrições;
- symlinks não permitem escape;
- `.git` permanece protegido;
- namespaces e controles de kernel estão ativos;
- fallback unsandboxed é impossível.

### Regras normativas

- `HARDENED` não pode ser ativado apenas porque existe configuração declarativa.
- Falha de capability obrigatória resulta em `BLOCKED`.
- `HARDENED` não pode cair silenciosamente para `BASE`.
- A mudança de perfil exige nova sessão.
- O perfil deve constar no manifesto.

### Ações necessárias

1. Definir catálogo versionado de checks.
2. Classificar cada check como `BASE`, `HARDENED` ou ambos.
3. Definir severidade e resultado esperado.
4. Implementar probes sem efeitos permanentes.
5. Implementar testes positivos e negativos.
6. Definir matriz de compatibilidade de host e kernel.
7. Registrar o perfil no manifesto.
8. Bloquear downgrade automático.
9. Criar processo humano de escolha e promoção de perfil.
10. Testar explicitamente a falha do sandbox.

### Critério de conformidade

Um manifesto `HARDENED` somente é emitido após todos os capability tests obrigatórios passarem no ambiente concreto.

---

## DEC-BOOT-004 — Gateway obrigatório para ferramentas

**Status:** `ACCEPTED`
**Título:** Mediação obrigatória de todas as ferramentas
**Decisão:** Todas as ferramentas utilizadas pelos agentes passarão pelo gateway. Operações sensíveis receberão preflight detalhado.

### Regras normativas

Todas as chamadas verificam:

- sessão existente;
- identidade da sessão;
- validade do manifesto;
- expiração;
- estado de invalidação;
- papel;
- capacidade exigida.

Recebem preflight detalhado:

- shell;
- escrita e edição;
- Git;
- rede;
- conectores e MCP;
- instalação de skills ou dependências;
- banco de dados;
- deploy;
- credenciais;
- alteração de políticas;
- alteração de infraestrutura.

### Ações necessárias

1. Inventariar todas as ferramentas acessíveis aos agentes.
2. Atribuir capacidade necessária a cada ferramenta.
3. Criar wrapper ou integração obrigatória com o gateway.
4. Remover caminhos diretos alternativos.
5. Implementar validação leve em todas as chamadas.
6. Implementar preflight por classe sensível.
7. Criar cache seguro para verificações imutáveis.
8. Invalidar o cache em mudanças materiais.
9. Testar chamadas diretas e tentativas de bypass.
10. Registrar bloqueios de forma estruturada.

### Critério de conformidade

Nenhuma ferramenta protegida pode ser chamada por um agente sem validação da sessão e da capacidade aplicável.

---

## DEC-BOOT-005 — Identidade e expiração de sessão

**Status:** `ACCEPTED`
**Título:** Vinculação da autorização ao processo e ao ambiente
**Decisão:** Cada sessão será vinculada ao processo do agente, ao boot do container e a um limite máximo de duração.

### Identidade mínima

- `session_id`;
- nonce;
- identidade do processo;
- identidade do launcher;
- boot ID;
- container ID;
- workspace;
- repositório;
- papel;
- instante de criação;
- instante máximo de expiração.

### Política recomendada

- termina com o processo do agente;
- termina com o launcher;
- expira ao reiniciar ou recriar o container;
- duração máxima de 12 horas;
- renovação somente pelo controlador;
- renovação exige revalidação;
- sessão não pode ser transferida para outro processo.

### Ações necessárias

1. Definir formato da identidade.
2. Gerar IDs com fonte criptograficamente segura.
3. Vincular sessão ao PID e ao launcher.
4. Observar término do processo.
5. Registrar boot ID e container ID.
6. Implementar TTL máximo.
7. Implementar renovação controlada.
8. Rejeitar replay de session ID.
9. Testar encerramento do agente.
10. Testar reinício do container.
11. Testar cópia de manifesto entre sessões.

### Critério de conformidade

Uma sessão encerrada, expirada ou pertencente a outro processo não autoriza nenhuma nova operação.

---

## DEC-BOOT-006 — Invalidação objetiva

**Status:** `ACCEPTED`
**Título:** Invalidação baseada em identidade, versão e hashes
**Decisão:** O estado da sessão será invalidado por eventos e comparações objetivas, nunca por interpretação do agente.

### Eventos de invalidação imediata

- reinício da máquina;
- reinício ou recriação do container;
- reinício não recuperável do controlador;
- encerramento do agente;
- mudança de papel;
- mudança de workspace;
- mudança de repositório;
- mudança de política promovida;
- mudança de gateway;
- mudança de hook;
- mudança de schema;
- mudança de verificador;
- atualização de runtime relevante;
- alteração de mounts;
- alteração de permissões;
- alteração de rede;
- perda de controle obrigatório;
- adulteração de manifesto;
- alteração do perfil operacional.

### Regras normativas

- Alteração comum no código da aplicação não exige necessariamente bootstrap completo.
- Mudanças da tarefa são tratadas por preflight.
- Mudanças do plano de controle invalidam a sessão.
- Estado invalidado deve ser `STALE` ou `BLOCKED`.
- `STALE` não pode executar ferramentas protegidas.

### Ações necessárias

1. Definir conjunto canônico de entradas críticas.
2. Calcular hashes canônicos.
3. Registrar versões promovidas.
4. Implementar monitoramento de eventos.
5. Revalidar hashes antes de operações sensíveis.
6. Definir diferença entre `STALE` e `BLOCKED`.
7. Invalidar caches do gateway.
8. Encerrar capacidades concedidas.
9. Criar testes para cada evento.
10. Garantir que invalidação seja registrada com causa objetiva.

### Critério de conformidade

A alteração de qualquer entrada crítica impede imediatamente o uso do manifesto anterior.

---

## DEC-BOOT-007 — Capacidades explícitas por papel

**Status:** `ACCEPTED`
**Título:** Modelo de autorização por capacidade e privilégio mínimo
**Decisão:** Executor, Reviewer e humano receberão conjuntos diferentes e explícitos de capacidades.

### Executor

Capacidades possíveis:

```text
workspace.read
workspace.write.authorized_scope
git.inspect
checks.execute
tests.execute
tmp.write
cache.write.authorized
network.task_scoped
```

Capacidades negadas:

```text
git.mutate
policy.write
bootstrap.modify
bootstrap.promote
protected_sources.write
deploy.unapproved
```

### Reviewer

Capacidades possíveis:

```text
workspace.read
git.inspect
checks.execute
tests.execute
tmp.write
cache.write.authorized
```

Capacidades negadas:

```text
workspace.write
git.mutate
network.default
bootstrap.modify
bootstrap.promote
finding.self_fix
```

### Humano

Capacidades possíveis:

- Git completo;
- provisionamento;
- promoção;
- recuperação;
- override emergencial controlado;
- alteração do plano de controle.

### Regras normativas

- Capacidades são calculadas pelo controlador.
- O agente não pode solicitar autopromoção.
- A capacidade deve considerar papel, perfil, tarefa e operação.
- Rede e escrita devem ser escopadas.
- `READY` sem lista de capacidades não é autorização suficiente.

### Ações necessárias

1. Criar catálogo canônico de capacidades.
2. Criar matriz papel × capacidade.
3. Mapear ferramentas para capacidades.
4. Mapear classes de operação para capacidades adicionais.
5. Implementar escopo por caminho, destino e comando.
6. Implementar negações explícitas.
7. Registrar capacidades no manifesto.
8. Criar testes de separação Executor–Reviewer.
9. Criar testes de negação de Git.
10. Criar identidade técnica distinta para ações humanas.

### Critério de conformidade

Cada operação autorizada pode ser explicada por uma capacidade concreta concedida ao papel e à sessão.

---

## DEC-BOOT-008 — Schema versionado e verificador promovido

**Status:** `ACCEPTED`
**Título:** Separação entre fonte auditável e verificador operacional imutável
**Decisão:** Schema, política e código-fonte do verificador serão versionados no repositório protegido. A versão promovida será instalada de forma imutável na imagem.

### Estrutura recomendada no repositório

```text
.ai/control/bootstrap/
├── bootstrap-manifest.schema.json
├── bootstrap-policy.schema.json
├── bootstrap-policy.json
├── verify-bootstrap.mjs
├── capabilities.json
├── checks.json
└── acceptance/
```

### Estrutura promovida

```text
/opt/cepraea/bootstrap/
├── bootstrap-manifest.schema.json
├── bootstrap-policy.json
├── verify-bootstrap
├── capabilities.json
├── checks.json
└── promoted-digests.json
```

### Regras normativas

- O gateway usa apenas a versão promovida.
- O working tree não é fonte executável de confiança.
- Toda promoção registra commit, versão e digests.
- Alteração no repositório não altera automaticamente o runtime.
- Incompatibilidade de versões bloqueia a sessão.
- O mesmo ator não pode alterar e promover sozinho o controle.

### Ações necessárias

1. Definir schemas.
2. Definir versionamento semântico.
3. Implementar verificador determinístico.
4. Criar empacotamento imutável.
5. Registrar digests promovidos.
6. Integrar instalação ao build da imagem.
7. Definir processo de revisão e promoção.
8. Criar teste de adulteração do working tree.
9. Criar teste de divergência entre fonte e versão promovida.
10. Implementar rollback por versão.

### Critério de conformidade

Modificar o verificador no working tree não altera o comportamento do gateway até que uma nova versão seja revisada e promovida.

---

## DEC-BOOT-009 — Retenção controlada de manifestos e relatórios

**Status:** `ACCEPTED`
**Título:** Persistência mínima e proteção de evidências operacionais
**Decisão:** Manifestos de sucesso serão efêmeros. Falhas materiais serão retidas por prazo definido fora do working tree.

### Política inicial recomendada

- manifesto ativo: durante a sessão;
- sucesso: efêmero ou retenção técnica máxima de 7 dias;
- falha operacional: 30 dias;
- incidente de segurança: conforme política específica;
- evidência de promoção: persistida formalmente;
- prompts completos: não armazenar;
- segredos: nunca armazenar;
- conteúdo sensível: redigir ou referenciar por hash.

### Regras normativas

- Relatórios são derivados do manifesto.
- Relatórios não são uma state machine de tarefas.
- O Git não recebe relatórios automáticos de cada execução.
- Deve existir rotação.
- Deve existir limite de tamanho.
- Toda retenção precisa de finalidade definida.

### Ações necessárias

1. Definir classificação dos relatórios.
2. Implementar armazenamento fora do working tree.
3. Implementar rotação por idade e tamanho.
4. Implementar redaction.
5. Proibir segredos por schema.
6. Gerar resumo humano derivado do manifesto.
7. Criar relatório detalhado automático em falhas materiais.
8. Definir exportação humana de evidências de promoção.
9. Testar expiração e remoção.
10. Documentar acesso aos relatórios.

### Critério de conformidade

O working tree permanece limpo e nenhuma informação sensível é armazenada como consequência automática do bootstrap.

---

## DEC-BOOT-010 — Separação entre provisionamento e verificação

**Status:** `ACCEPTED`
**Título:** Bootstrap não realiza provisionamento implícito
**Decisão:** Dependências e controles serão provisionados preferencialmente no build da imagem. O bootstrap apenas verificará e atestará o estado.

### Fluxo obrigatório

```text
PROVISIONAR
     ↓
VERIFICAR
     ↓
ATESTAR
```

### Regras normativas

- Verificação não instala ferramentas.
- Falta de runtime resulta em `FAIL` ou `UNAVAILABLE`.
- Bootstrap não usa rede para “consertar” o ambiente.
- Provisionamento runtime exige ação explícita.
- Dependências devem ter versões pinadas.
- Builds devem ser reproduzíveis.
- O manifesto registra o observado, não o estado desejado.

### Ações necessárias

1. Inventariar dependências do bootstrap.
2. Piná-las na imagem.
3. Criar lockfiles ou digests.
4. Separar comandos de provisionamento e verificação.
5. Tornar probes read-only.
6. Definir fluxo de atualização de dependências.
7. Implementar rebuild da imagem.
8. Implementar testes de imagem incompleta.
9. Provar que o bootstrap não modifica o ambiente.
10. Criar rollback para imagem anterior.

### Critério de conformidade

Executar o bootstrap repetidamente não instala, atualiza nem remove qualquer componente do ambiente.

---

## DEC-BOOT-011 — Recuperação fail-closed

**Status:** `ACCEPTED`
**Título:** Diagnóstico estruturado e recuperação humana controlada
**Decisão:** Falhas bloqueiam operações protegidas. A recuperação depende de procedimento explícito e não pode reduzir silenciosamente o isolamento.

### Regras normativas

- Falha resulta em `BLOCKED`.
- O controlador gera diagnóstico estruturado.
- Não existe fallback unsandboxed automático.
- Não existe downgrade automático de `HARDENED` para `BASE`.
- Recuperação não altera Git.
- Override emergencial pertence somente ao humano.
- Override usa estado distinto de `READY`.
- Nova inicialização é obrigatória após override.

### Mecanismos de recuperação

- recriar sessão;
- reiniciar controlador;
- recriar container;
- reconstruir imagem;
- fazer rollback de versão promovida;
- corrigir configuração;
- usar override emergencial humano e auditado.

### Ações necessárias

1. Criar taxonomia de falhas.
2. Mapear falhas para ações de recuperação.
3. Definir estados `BLOCKED`, `STALE` e `EMERGENCY_OVERRIDE`.
4. Criar diagnóstico estruturado.
5. Criar runbook humano de recuperação.
6. Implementar rollback.
7. Implementar override com TTL curto.
8. Registrar motivo e identidade humana.
9. Proibir override por processos dos agentes.
10. Testar falha parcial e interrupção.
11. Testar ausência de fallback.

### Critério de conformidade

Toda falha obrigatória impede operações protegidas e nenhuma recuperação ocorre com redução automática de segurança.

---

## DEC-BOOT-012 — Promoção formal para `ENFORCE`

**Status:** `ACCEPTED`
**Título:** Ativação gradual e baseada em evidência
**Decisão:** O bootstrap será promovido gradualmente e somente entrará no caminho crítico após acceptance tests, testes negativos, rollback comprovado e decisão humana registrada.

### Estados de promoção

```text
DESIGN
   ↓
OBSERVE
   ↓
WARN
   ↓
ENFORCE_BASE
   ↓
ENFORCE_HARDENED
```

### Significados

- `DESIGN`: decisões e contratos em elaboração.
- `OBSERVE`: checks executam, mas não bloqueiam.
- `WARN`: falhas geram alerta explícito.
- `ENFORCE_BASE`: controles obrigatórios bloqueiam.
- `ENFORCE_HARDENED`: isolamento adicional comprovado bloqueia.

### Critérios para `ENFORCE_BASE`

- schema válido;
- controlador instalado;
- gateway obrigatório;
- ferramentas inventariadas;
- capabilities definidas;
- testes positivos aprovados;
- testes negativos aprovados;
- reinicialização testada;
- expiração testada;
- adulteração testada;
- bypass testado;
- rollback ensaiado;
- fluxo humano preservado;
- duas inicializações limpas e reproduzíveis;
- decisão humana com versão e digests.

### Critérios para `ENFORCE_HARDENED`

- todos os critérios de `BASE`;
- sandbox compatível com host e container reais;
- testes de filesystem;
- testes de rede;
- testes de subprocesso;
- teste de symlink escape;
- ausência de fallback;
- período de estabilidade observado;
- rollback de perfil testado;
- nova decisão humana registrada.

### Ações necessárias

1. Implementar estado de promoção.
2. Impedir que o agente altere o estado.
3. Criar suite de acceptance tests.
4. Criar suite de testes negativos.
5. Criar relatório de promoção.
6. Registrar versões e digests.
7. Implementar rollback.
8. Definir autoridade aprovadora.
9. Definir período de observação.
10. Implementar gate de promoção.
11. Testar que `OBSERVE` não é apresentado como enforcement.
12. Testar que `ENFORCE` realmente bloqueia.

### Critério de conformidade

Nenhum perfil recebe status `ENFORCE` apenas por documentação ou configuração nominal; a promoção exige evidência executável e autorização humana.

# Relações entre as decisões

```text
DEC-BOOT-001 Controlador
        |
        +--> DEC-BOOT-002 Runtime protegido
        |
        +--> DEC-BOOT-005 Sessões
        |
        +--> DEC-BOOT-006 Invalidação
        |
        +--> DEC-BOOT-004 Gateway
                    |
                    +--> DEC-BOOT-007 Capacidades

DEC-BOOT-008 Schema e verificador
        |
        +--> DEC-BOOT-003 Perfis e checks
        |
        +--> DEC-BOOT-009 Relatórios

DEC-BOOT-010 Provisionamento
        |
        +--> DEC-BOOT-011 Recuperação
        |
        +--> DEC-BOOT-012 Promoção
```

A promoção depende da implementação e validação de todas as decisões anteriores.

# Plano de implementação necessário

## Fase 1 — Contratos

Objetivo: transformar as decisões em contratos verificáveis.

Ações:

1. criar os 12 registros de decisão;
2. criar schema do manifesto;
3. criar schema da política;
4. criar catálogo de checks;
5. criar catálogo de capacidades;
6. criar matriz papel × capacidade;
7. criar taxonomia de falhas;
8. definir estados da sessão;
9. definir estados de promoção;
10. criar vetores de teste canônicos.

Saída:

```text
Decisões ACCEPTED
Implementação DESIGN
Enforcement inexistente
```

## Fase 2 — Controlador mínimo

Objetivo: produzir manifestos sem bloquear trabalho.

Ações:

1. implementar controlador;
2. implementar identidade do ambiente;
3. implementar identidade da sessão;
4. implementar diretório runtime protegido;
5. implementar escrita atômica;
6. implementar validação por schema;
7. implementar checks `BASE`;
8. gerar relatórios;
9. operar em `OBSERVE`.

Saída:

```text
Bootstrap observável
Sem bloqueio
Sem alegação de enforcement
```

## Fase 3 — Gateway

Objetivo: garantir mediação técnica.

Ações:

1. inventariar ferramentas;
2. mapear capacidades;
3. integrar wrappers;
4. bloquear caminhos alternativos;
5. implementar preflight;
6. implementar cache seguro;
7. implementar invalidação;
8. executar testes de bypass.

Saída:

```text
Gateway funcional
Modo WARN
Bloqueios ainda não promovidos
```

## Fase 4 — Enforcement `BASE`

Objetivo: tornar obrigatórios os controles compatíveis.

Ações:

1. executar acceptance tests;
2. executar testes negativos;
3. validar fluxo Executor;
4. validar fluxo Reviewer;
5. validar fluxo humano;
6. testar rollback;
7. produzir relatório de promoção;
8. registrar decisão humana;
9. promover digests;
10. ativar `ENFORCE_BASE`.

Saída:

```text
BASE fail-closed
HARDENED ainda não promovido
```

## Fase 5 — Hardening

Objetivo: provar isolamento adicional.

Ações:

1. implementar nested sandbox;
2. testar namespaces;
3. testar filesystem;
4. testar rede;
5. testar subprocessos;
6. testar symlinks;
7. testar `.git`;
8. verificar ausência de fallback;
9. observar estabilidade;
10. promover `ENFORCE_HARDENED`.

Saída:

```text
HARDENED fail-closed
Somente em hosts aprovados
```

# Matriz de responsabilidade

| Artefato ou ação | Executor | Reviewer | Humano/Administrador |
|---|---:|---:|---:|
| Propor implementação | Sim | Não | Sim |
| Implementar controlador | Sim, se autorizado | Não | Sim |
| Revisar controlador | Não aprova o próprio trabalho | Sim | Sim |
| Alterar decisões | Propor | Revisar | Aprovar |
| Promover versão | Não | Não | Sim |
| Gerar manifesto | Não | Não | Controlador |
| Alterar manifesto | Não | Não | Não manualmente |
| Executar acceptance tests | Sim | Reexecuta proporcionalmente | Pode executar |
| Ativar `ENFORCE` | Não | Não | Sim |
| Usar break-glass | Não | Não | Sim |
| Fazer rollback | Não automaticamente | Não | Sim |

# Evidências obrigatórias

Cada promoção deve preservar:

- versão do controlador;
- commit de origem;
- digests promovidos;
- schema utilizado;
- perfil;
- ambiente testado;
- resultados dos checks;
- resultados dos testes negativos;
- tentativas de bypass;
- resultado do rollback;
- limitações conhecidas;
- identidade e data da aprovação humana.

# Regra de transição

A adoção das decisões não significa que o bootstrap já esteja aplicado:

```text
Decisão ACCEPTED
≠
Implementação concluída
≠
Controle verificado
≠
ENFORCE promovido
```

O estado inicial formal deve ser:

```yaml
decisions: ACCEPTED
implementation: NOT_IMPLEMENTED
operational_mode: DESIGN
enforcement: NONE
```

Somente depois das fases de implementação, verificação e promoção humana o estado poderá tornar-se:

```yaml
decisions: ACCEPTED
implementation: VERIFIED
operational_mode: ENFORCE_BASE
enforcement: FAIL_CLOSED
```

