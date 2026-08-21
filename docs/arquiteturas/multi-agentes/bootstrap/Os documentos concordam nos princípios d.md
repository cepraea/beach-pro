Os documentos concordam nos princípios de verificação, mas discordam materialmente sobre quem executa o bootstrap, onde reside a confiança e como uma sessão recebe autorização. O `README.md` descreve um verificador local acionado pelo agente; a arquitetura exige um plano de controle externo, root-owned e tecnicamente intermediário às ferramentas.

## Pontos de concordância

| Tema | `README.md` do script | Arquitetura | Avaliação |
|---|---|---|---|
| Determinismo | Exige checks, oráculos, evidências e resultado reproduzível | Exige checks determinísticos e evidência estruturada | Concordância |
| Fail-closed | Ausência de evidência e checks obrigatórios incompletos resultam em `FAIL` | Falha, estado desconhecido, timeout ou manifesto inválido bloqueiam | Concordância de princípio |
| Não mutação | O script não pode modificar repositório ou Git | Bootstrap verifica e atesta; não provisiona nem altera Git | Concordância |
| Identidade do repositório | Verifica raiz Git, remote, branch e HEAD | Verifica workspace, repositório, branch e commit inicial | Concordância |
| Separação de papéis | Valida Executor, Reviewer e autoridade humana | Define manifestos e capacidades distintos por papel | Concordância |
| Configuração efetiva | Declara que configuração textual não prova enforcement | Exige capability tests reais e proíbe confiança em declaração | Concordância |
| Bootstrap antes da tarefa | O bootstrap antecede F0 e não depende de uma Task Proposal concreta | Bootstrap verifica a sessão; preflight trata a tarefa e operação | Concordância parcial |
| Runbooks | Valida a capacidade do catálogo, sem selecionar runbook da tarefa | Distingue bootstrap, preflight e runbook | Concordância |
| Fingerprints e hashes | Define superfície protegida e fingerprint determinístico | Exige hashes das entradas críticas e versões promovidas | Concordância conceitual |
| Testes negativos | Exige known-good, known-bad, mutants e detecção de bypass | Exige testes de adulteração, bypass, expiração e isolamento | Concordância |
| Dados sensíveis | Proíbe leitura e persistência indiscriminada de segredos | Proíbe segredos e conteúdo sensível em manifestos e relatórios | Concordância |
| Provisionamento separado | O script não instala nem reconstrói o ambiente | Estabelece `PROVISIONAR → VERIFICAR → ATESTAR` | Concordância |
| Promoção humana | O script produz apenas fingerprint candidato | Agentes não promovem; ativação depende de decisão humana | Concordância |
| Estado atual não comprovado | Declara `CANDIDATE / NOT VERIFIED` | Declara implementação inexistente e enforcement `NONE` | Compatíveis se o script for tratado apenas como candidato |

## Discordâncias materiais

### 1. Autoridade para executar e autorizar

O [README](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:1744) define:

```text
AGENTS.md / CLAUDE.md
→ agente lê especificação
→ agente executa Bootstrap.py
→ PASS
→ AGENT_READY
```

A [arquitetura](/workspaces/cepraea-beach-pro/docs/arquiteturas/multi-agentes/bootstrap/bootstrap-arquitetura.md:5) determina:

```text
entrypoint do container
→ controlador root-owned
→ launcher autentica papel
→ controlador cria sessão
→ gateway consulta manifesto
→ ferramenta é liberada
```

Essa é a divergência mais importante. Pela arquitetura, o agente não pode ser responsável por iniciar o mecanismo que lhe concede autoridade.

### 2. Raiz de confiança

O README trata [Bootstrap.py](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/Bootstrap.py) no working tree como o verificador executável.

A arquitetura determina duas representações:

```text
working tree
→ fonte auditável e candidata

/opt/cepraea/bootstrap/
→ versão promovida, imutável e operacional
```

A arquitetura afirma expressamente que executar o verificador do working tree gravável permite que o mesmo ator altere o oráculo e passe na regra alterada.

### 3. `PASS` local versus autorização técnica

No [README](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:1140), `PASS` do script pode resultar em `AGENT_READY`.

Na arquitetura:

- checks produzem observações;
- o controlador gera o manifesto;
- um verificador externo valida integridade e sessão;
- o gateway calcula e aplica capacidades;
- apenas então existe `READY`.

Portanto:

```text
Bootstrap.py verdict = PASS
```

não é suficiente para:

```text
session.final_state = READY
```

### 4. Entry points textuais

O README exige que `AGENTS.md` e `CLAUDE.md` mandem o agente ler e executar o bootstrap.

A arquitetura começa justamente refutando essa abordagem: instruções textuais não garantem execução. Os entrypoints dos agentes podem informar o contrato, mas não podem ser o enforcement.

Há também ambiguidade no termo `entrypoint`:

- no README, significa `AGENTS.md`/`CLAUDE.md`;
- na arquitetura, significa principalmente o entrypoint técnico do Dev Container.

### 5. Manifestos diferentes com o mesmo nome

O README usa `manifest.json` como inventário declarativo de artefatos do repositório.

A arquitetura usa “manifesto canônico” como atestado runtime da sessão, contendo:

- identidade da sessão;
- papel;
- perfil;
- checks;
- capacidades;
- validade;
- integridade;
- expiração.

Os artefatos têm funções distintas e não deveriam compartilhar terminologia sem qualificação. Sugestões conceituais:

```text
repository-asset-manifest
session-bootstrap-manifest
```

### 6. Baseline versus versão promovida

O README propõe:

```text
full
→ candidate_fingerprint
→ aprovação humana
→ baseline aprovado
→ revalidate
```

A arquitetura exige algo mais forte:

```text
fonte revisada no Git
→ build/provisionamento
→ instalação imutável em /opt
→ promoted-digests
→ controlador compara runtime
→ manifesto de sessão
```

Um arquivo de baseline acessível ao agente não substitui a cópia promovida e protegida na imagem.

### 7. Semântica de `revalidate`

No README, `revalidate` é um comando executado antes de uma TASK:

```bash
python3 test/scripts/bootstrap/Bootstrap.py revalidate
```

Na arquitetura:

- bootstrap acontece por sessão;
- renovação/revalidação pertence ao controlador;
- preflight acontece antes de operações protegidas;
- mudanças normais do código pertencem ao preflight, não necessariamente a um novo bootstrap.

Assim, o `revalidate` do README mistura três responsabilidades:

1. renovação da sessão;
2. detecção de drift do plano de controle;
3. preflight anterior à tarefa.

### 8. Modelo de resultados

O README permite externamente apenas:

```text
PASS
FAIL
```

A arquitetura recomenda resultados de check:

```text
PASS
FAIL
NOT_APPLICABLE
UNAVAILABLE
ERROR
```

e estados da sessão:

```text
UNINITIALIZED
BOOTSTRAPPING
BOOTSTRAPPED
VERIFIED
READY
STALE
BLOCKED
```

Não é necessariamente errado reduzir o exit code público a sucesso/falha, mas o schema do README perde informação necessária para diagnóstico, recuperação e controle de sessão.

Uma conciliação possível seria:

```text
check.result = PASS | FAIL | NOT_APPLICABLE | UNAVAILABLE | ERROR
session.state = READY | STALE | BLOCKED | ...
process exit = 0 | 1 | 2
```

### 9. Capacidades ausentes

O output do README contém checks, reason codes, fingerprint e verdict.

A arquitetura exige capacidades concretas:

```json
{
  "granted": ["workspace.read", "git.inspect"],
  "denied": ["workspace.write", "git.mutate"]
}
```

`READY` sem capacidades explícitas não é autorização suficiente segundo a arquitetura.

### 10. Ausência de identidade forte de sessão

O README observa repositório, branch e HEAD, mas não define vínculo obrigatório com:

- `session_id`;
- nonce;
- PID do agente;
- launcher;
- boot ID;
- container ID;
- expiração;
- prevenção de replay.

A arquitetura considera esses elementos indispensáveis. Sem eles, um resultado anterior pode ser reutilizado fora da sessão em que foi produzido.

### 11. Local e propriedade do resultado

No README, o script imprime JSON e deixa localização/schema do baseline em aberto.

A arquitetura exige:

```text
/run/cepraea-bootstrap/
```

com:

- ownership root ou usuário técnico;
- escrita atômica;
- agentes sem escrita;
- consulta pelo gateway;
- proteção contra substituição;
- retenção controlada.

Essa lacuna impede que o resultado do script seja evidência confiável de autorização.

### 12. Perfis operacionais

A arquitetura separa:

```text
BASE
HARDENED
```

e define efeitos diferentes para falhas como a indisponibilidade do nested sandbox.

O README não modela perfis. Consequentemente, não consegue decidir de forma contratual quando uma capability é:

- obrigatória;
- não aplicável;
- opcional;
- bloqueante.

### 13. Estágios de promoção

A arquitetura exige:

```text
DESIGN
→ OBSERVE
→ WARN
→ ENFORCE_BASE
→ ENFORCE_HARDENED
```

O README salta do script candidato para:

```text
PASS
→ AGENT_READY
→ F0
```

Embora declare `CANDIDATE / NOT VERIFIED`, seu fluxo operacional não representa `OBSERVE` nem impede alegação prematura de enforcement.

### 14. Gateway e bypass

O README tenta verificar enforcement por probes do próprio script.

A arquitetura exige que todas as ferramentas sejam mediadas pelo gateway e que não exista rota direta alternativa.

Probes são evidência necessária, mas não substituem mediação contínua:

```text
probe passou uma vez
≠ toda chamada futura está protegida
```

### 15. Self-tests em cada bootstrap

O README coloca `Verifier Self-Tests` no fluxo do `full`, incluindo cópia e mutação de fixtures.

A arquitetura trata acceptance tests e testes negativos principalmente como requisitos de implementação e promoção. No runtime normal, o controlador deve executar checks proporcionais e rápidos.

Executar toda a suíte de mutants em cada bootstrap de sessão pode ser:

- caro;
- redundante;
- inadequado à operação normal.

A divisão mais coerente seria:

```text
build/promotion
→ suíte completa de self-tests e mutants

session bootstrap
→ integridade da versão promovida + capability checks do ambiente
```

### 16. Escopo excessivo do inventário

O README propõe inventário físico amplo do checkout e confronto com um `manifest.json`.

A arquitetura exige entradas críticas explicitamente enumeradas e rejeita “todos os arquivos que parecerem relevantes”. Alterações comuns no working tree não devem invalidar necessariamente a sessão.

O inventário amplo pode continuar como ferramenta diagnóstica, mas não deve automaticamente participar do gate de confiança sem uma política explícita.

### 17. Reviewer-first incompatível com a promoção operacional

O fluxo do README prevê que o Reviewer execute o `Bootstrap.py` do working tree alterado e, após `PASS`, o humano disponibilize um baseline ao Executor.

Na arquitetura:

1. Reviewer revisa a fonte candidata;
2. acceptance tests são executados;
3. humano aprova;
4. artefatos são construídos e instalados na imagem;
5. digests são promovidos;
6. nova sessão usa a versão imutável.

O Reviewer pode validar a proposta, mas não transformar diretamente o working tree em raiz de confiança operacional.

## Diferenças complementares, não necessariamente contradições

Alguns conteúdos do README são especializações úteis que podem sobreviver:

- normalização do remote Git;
- classificação do working tree;
- inventário canônico de entradas explicitamente selecionadas;
- validação do catálogo de runbooks;
- validação estrutural das configurações Claude/Codex;
- catálogo de reason codes;
- modelo `CheckResult`;
- arquitetura Python modular;
- uso preferencial da standard library;
- fixtures known-good/known-bad;
- fingerprint determinístico;
- invariância de não mutação.

Esses elementos podem ser incorporados como biblioteca de checks do controlador. O problema é conceder ao script local autoridade para emitir `AGENT_READY`.

## Findings

### CRITICAL — Raiz de confiança controlada pelo agente

- **Problema:** O README permite que o próprio agente execute do working tree o verificador que resulta em `AGENT_READY`.
- **Evidência:** Fluxo em [Resumo operacional](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:1744), contraposto ao controlador externo exigido pela [arquitetura](/workspaces/cepraea-beach-pro/docs/arquiteturas/multi-agentes/bootstrap/bootstrap-arquitetura.md:5).
- **Impacto:** O mecanismo não impede bypass nem prova autorização independente da obediência do modelo.
- **Correção Requerida:** Reespecificar `Bootstrap.py` como biblioteca/ferramenta candidata do controlador ou diagnóstico em `OBSERVE`, removendo sua autoridade direta para conceder `AGENT_READY`.

### CRITICAL — Ausência de gateway e manifesto protegido

- **Problema:** O contrato do README não exige mediação obrigatória de todas as ferramentas nem manifesto root-owned ligado à sessão.
- **Evidência:** O output mínimo do README contém somente checks, fingerprint e verdict; a arquitetura exige gateway, capacidades e armazenamento protegido em `/run/cepraea-bootstrap/`.
- **Impacto:** Mesmo após `PASS`, o agente pode continuar usando rotas que não consultam o resultado, e o resultado pode não estar protegido contra replay ou substituição.
- **Correção Requerida:** Incorporar controlador, manifesto de sessão protegido, identidade forte, capacidades e gateway ao contrato antes de qualquer promoção para enforcement.

### HIGH — `revalidate` conflita com sessão e preflight

- **Problema:** O README define `revalidate` antes de cada TASK, misturando bootstrap, renovação da sessão e preflight.
- **Evidência:** [Modo revalidate](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:1100) versus a distinção arquitetural entre [bootstrap, preflight e runbook](/workspaces/cepraea-beach-pro/docs/arquiteturas/multi-agentes/bootstrap/bootstrap-arquitetura.md:28).
- **Impacto:** Pode causar bootstraps desnecessários e, simultaneamente, deixar operações sensíveis sem preflight específico.
- **Correção Requerida:** Transferir a revalidação de sessão ao controlador e criar preflight separado no gateway por operação protegida.

### HIGH — Promoção prematura de `PASS` para enforcement

- **Problema:** O README conecta diretamente `PASS` a `AGENT_READY`, sem representar `DESIGN`, `OBSERVE`, `WARN` e promoção humana para `ENFORCE`.
- **Evidência:** [Gate AGENT_READY](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:1140) versus [promoção gradual](/workspaces/cepraea-beach-pro/docs/arquiteturas/multi-agentes/bootstrap/bootstrap-arquitetura.md:1886).
- **Impacto:** Um componente candidato pode ser apresentado como controle fail-closed implantado.
- **Correção Requerida:** Acrescentar estado de implementação e promoção ao contrato e proibir `AGENT_READY` operacional antes de `ENFORCE_BASE`.

### MEDIUM — Colisão semântica de manifestos e baseline

- **Problema:** O README não diferencia claramente o inventário `manifest.json`, o baseline aprovado e o manifesto runtime da sessão.
- **Evidência:** [Manifest Verification](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:651), [Baseline](/workspaces/cepraea-beach-pro/test/scripts/bootstrap/README.md:1079) e manifesto canônico da arquitetura.
- **Impacto:** Implementadores podem usar um artefato versionado ou gravável como se fosse atestado operacional protegido.
- **Correção Requerida:** Definir nomes, schemas, autoridades, localizações e ciclos de vida distintos para cada artefato.

### MEDIUM — Modelo de resultados insuficiente

- **Problema:** O README reduz todos os resultados externos a `PASS/FAIL`, enquanto a arquitetura necessita estados diagnósticos e estados de sessão distintos.
- **Evidência:** Princípio `PASS/FAIL` do README versus `PASS`, `FAIL`, `NOT_APPLICABLE`, `UNAVAILABLE`, `ERROR` e a máquina de estados arquitetural.
- **Impacto:** Perde-se a distinção necessária para perfil, recuperação, invalidação e diagnóstico, incentivando reason codes sobrecarregados.
- **Correção Requerida:** Separar resultado de check, estado da sessão, verdict do gate e exit code do processo.

FAIL
