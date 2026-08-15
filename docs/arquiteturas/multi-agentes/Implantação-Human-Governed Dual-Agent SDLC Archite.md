# Human-Governed Dual-Agent SDLC Architecture

Além dos arquivos de configuração, faltam **cinco coisas práticas** para considerar essa arquitetura realmente implantada: integrar os arquivos ao repositório existente, configurar os agentes nas extensões reais, validar o container em runtime, migrar o workflow antigo e executar um teste ponta a ponta.

Eu trataria a implantação como este conjunto:

1. **Materializar os 9 arquivos da arquitetura** no repositório e mesclá-los com o `Dockerfile`/`devcontainer.json` atuais, sem substituir a stack existente.
2. **Desativar o workflow antigo** baseado em `.agent-flow/STATE.md`, `executions/**` e `reviews/**` como mecanismo obrigatório. Preserve o histórico já produzido, mas não o use mais como state machine.
3. **Configurar Claude e Codex reais**:

   * Claude deve reconhecer `CLAUDE.md`, carregar `AGENT_POLICY.md`, usar o managed settings instalado pelo container e o `PreToolUse`.
   * Codex deve reconhecer `AGENTS.md` e operar com o profile de Reviewer: projeto RO, escrita efêmera apenas onde necessária.
4. **Executar os acceptance tests do container**, não apenas conferir arquivos.
5. **Executar uma ação real completa** — idealmente AC-000 — passando por Claude → validações → Codex → PASS/FAIL → commit humano.

A implantação deve seguir esta ordem:

```text
Arquitetura aprovada
        ↓
arquivos materializados
        ↓
Dev Container rebuild
        ↓
verificação BASE
        ↓
testes manuais Claude/Codex
        ↓
primeiro fluxo end-to-end
        ↓
arquitetura operacional
```

## 1. O que precisa ser testado de verdade

O script `verify-agent-environment.sh` cobre parte importante, mas não consegue provar tudo. Eu usaria um checklist formal de implantação:


- [x] **CT-01** Container roda como non-root. Resultado: PASS — coberto por `verify-agent-environment.sh` ("container session is non-root")
- [x] **CT-02**  Docker socket ausente. Resultado: PASS — coberto por `verify-agent-environment.sh` ("Docker socket is not mounted")
- [x] **CT-03**  Produ**CTion secrets ausentesResultado: PASS neste ambiente — coberto por `verify-agent-environment.sh`; caminho PASS confirmado (nenhuma das 4 variáveis definida) e caminho FAIL comprovado expondo as 4 variáveis com valores fictícios simultaneamente, gerando `FAIL` individual para cada uma
- [x] **CT-04**  .drive/CEPRAEA BEACH PRO realmente `RO`. Resultado: FAIL — coberto por `verify-agent-environment.sh` ("SOURCE_ROOT is not confirmed read-only via findmnt"); `findmnt` não reporta a opção `ro` isolada para SOURCE_ROOT neste ambiente
- [x] **CT-05**  Davi consegue editar workspace pelo VS Code. Resultado: não coberto pelo script — exige teste interativo humano
- [x] **CT-06**  Davi consegue `git add/commit` no VS Code. Resultado: não coberto pelo script — exige teste interativo humano
- [x] **CT-07**  Claude consegue editar arquivo autorizado. Resultado: PASS — comprovado ao vivo nesta sessão (edição bem-sucedida deste próprio arquivo, dentro do escopo autorizado)
- [x] **CT-08**  Claude não consegue editar `AGENT_POLICY.md`. Resultado: PASS (bloqueado) — comprovado ao vivo: tentativa real de `Edit` em `AGENT_POLICY.md` foi barrada pelo hook `pretool` com `Bloqueado: caminho do plano de controle`; arquivo confirmado inalterado após a tentativa
- [x] **CT-09**  Claude não consegue alterar .drive/**. Resultado: testado ao vivo — o hook `pretool` NÃO bloqueia `Write`/`Edit` dentro de `.drive/**` (inclusive SOURCE_ROOT); comprovado criando e removendo um arquivo de teste, e editando/revertendo uma linha de um arquivo real, ambos sem qualquer bloqueio. Davi esclareceu que isso é intencional: `.drive` contém arquivos de rascunho de uso humano, não é tratado como falha a corrigir
- [x] **CT-10**  Claude tenta git commit. Resultado: validado por leitura estática do script `pretool` (execução ao vivo não autorizada pelo usuário nesta sessão) — o script casa `git commit`/`add`/`push`/`merge`/etc. no comando Bash e chama `block()` → `exit 2`, o mesmo mecanismo que bloqueou CT-08 ao vivo
- [x] **CT-11**  Claude consegue `git status/diff/log`. Resultado: PASS — comprovado repetidamente ao longo desta sessão (`git status`, `git diff --check`, `git diff`, `git branch --show-current` executados sem bloqueio)
- [ ] **CT-12**  Codex consegue ler todo o diff. Resultado: não coberto pelo script — exige execução real do agente
- [ ] **CT-13** Codex não consegue alterar source/modelagem.Resultado: não coberto pelo script — o script só verifica presença de `.codex/config.toml`/`requirements.toml`, não o comportamento real
- [ ] **CT-14** Codex consegue escrever em `/tmp`. Resultado: não coberto pelo script — exige execução real do agente
- [ ] **CT-15** Codex consegue rodar check que usa `temp`. Resultado: não coberto pelo script — exige execução real do agente
- [ ] **CT-16** Codex não consegue escalar permissões. Resultado: não coberto pelo script — exige execução real do agente
- [ ] **CT-17** Claude produz → Codex revisa → humano commit. Resultado: não coberto pelo script — exige fluxo end-to-end real


*O mais importante é o **CT-17**. Sem ele, temos configuração; com ele, temos arquitetura implantada.*

## 2. Também falta decidir o destino do workflow antigo

*Hoje já existem artefatos como:*

```text
.agent-flow/
├── STATE.md
├── EXECUTOR.md
├── REVIEWER.md
├── executions/
└── reviews/
```

Eu não apagaria o histórico de `AC-000`. Ele documenta bloqueios reais que levaram à evolução arquitetural.

Faria:

```text
.agent-flow/
→ legado / histórico
→ não usado pelo fluxo novo
```

e registraria formalmente uma decisão semelhante a:

```text
DEC-009 — Substituição do workflow .agent-flow
          por Git como state machine operacional
```

Ela deveria dizer:

```text
STATE.md              → não mais autoridade operacional
EXECUTOR.md           → substituído por CLAUDE.md
REVIEWER.md           → substituído por AGENTS.md
executions/**         → não obrigatório
reviews/**            → não obrigatório
Git                   → state machine/handoff
```

Isso evita que daqui a algumas semanas um agente leia documentos antigos e conclua que ainda precisa atualizar `STATE.md`.

## 3. O plano de modelagem também precisa ser reconciliado

Esse é outro ponto importante.

O plano atual foi construído quando `.agent-flow` ainda era parte da infraestrutura operacional. Se ele ainda disser coisas como:

```text
escrever executions/AC-NNN.md
esperar STATE.md
produzir reviews/AC-NNN.md
alterar status READY_FOR_REVIEW
```

ele estará em conflito com a arquitetura nova.

Portanto há uma tarefa de migração:

```text
ARQUITETURA NOVA
        ↓
DECISÃO FORMAL
        ↓
PLANO atualizado
        ↓
CLAUDE.md / AGENTS.md
        ↓
execução
```

Não devemos deixar:

```text
`AGENT_POLICY` diz Git
+
PLANO diz STATE.md
```

porque voltaríamos a ter duas autoridades.

### Falta também uma política explícita de branch

Como Git virou a state machine, a disciplina de branch fica mais importante.

Para a modelagem atual:

```text
feat/cepraea-domain-modeling
```

e a regra deveria ser:

```text
Claude só trabalha em branch autorizada != main/master.

Codex revisa a mesma working tree.

Davi cria commit após PASS.

Davi decide quando mergear.
```

Não precisamos de branch por agente.

### Como devem ser os commits

Eu manteria o action ID no início:

```text
AC-000: bootstrap da modelagem canônica
AC-001: processa SRC-001
SEM-001: reconcilia identidade de atleta
SYN-001: consolida modelo canônico
```

Isso mantém:

```text
action_ref
   ↓
commit subject
   ↓
SHA real
```

sem inventar uma state machine paralela.

### O nested sandbox do Claude não deve bloquear a implantação

A arquitetura revisada já resolveu isso. Então a implantação deve ter dois marcos:

```text
BASE_READY
```

quando:

```text
permissions
hook
non-root
.drive RO
secrets ausentes
Codex reviewer isolation
```

estiverem funcionando.

Depois:

```text
HARDENED_READY
```

somente se o teste real provar que:

```text
bubblewrap
+
user namespaces
+
container
```

funcionam corretamente.

Não seguraria AC-000 esperando HARDENED.

### Por fim, falta um pequeno runbook humano

Não criaria um sistema de workflow, mas um arquivo curto pode economizar erros operacionais:

```text
`docs/operacao/agent-workflow.md`
```

Com algo como:

```text
1. Confirmar branch.
2. Pedir Claude para executar apenas ACTION.
3. Esperar `READY_FOR_REVIEW`.
4. Pedir Codex para revisar git diff.
5. Se FAIL → devolver findings ao Claude.
6. Se HUMAN_DECISION_REQUIRED → decidir/registrar DEC.
7. Se PASS → revisar diff e commit.
8. Iniciar próxima ACTION.
```

Isso não é state machine; é um **runbook de uma página** para você.

### Portanto, para declarar implantação concluída

Eu usaria esta Definition of Done:


- [ ] 9 arquivos da arquitetura presentes
- [ ] `AGENT_POLICY` canônica
- [ ] `CLAUDE.md` carregado pelo Claude
- [ ] `AGENTS.md` carregado pelo Codex
- [ ] managed settings instalados `root-owned`
- [ ] `claude-guard` ativo
- [ ] Codex `reviewer` profile ativo
- [ ] `.drive` confirmado RO
- [ ] `.git` continua funcional para Davi
- [ ] zero production secrets
- [ ] BASE acceptance tests `PASS`
- [ ] workflow antigo declarado legado
- [ ] decisão arquitetural registrada
- [ ] plano reconciliado com `Git-as-state-machine`
- [ ] `AC-000` executado `end-to-end`
- [ ] Codex `PASS/FAIL` comprovadamente funciona
- [ ] commit humano concluído


Quando esses itens estiverem verdes, eu consideraria a arquitetura **implantada**, não apenas documentada.
