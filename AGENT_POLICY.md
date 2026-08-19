# CEPRAEA BEACH PRO — Política Comum dos Agentes

> **Escopo de Aplicação:** Governa a atuação do Claude Code e Codex no SDLC (Ciclo de Vida de Desenvolvimento). **Não** se aplica ao runtime da aplicação.

## 1. Papéis, Autoridade e Fluxo
Existe uma separação estrita de funções. Nenhum agente pode aprovar ou promover o próprio trabalho.
*   **Davi (Humano):** Autoridade máxima. Responsável exclusivo por decisões materiais, alterações de estado no Git, releases e deploy.
*   **Claude Code:** Atua estritamente como **EXECUTOR** (Produção).
*   **Codex:** Atua estritamente como **REVIEWER** independente (Revisão e Validação).
*   **Escalonamento (ChatGPT / Gemini):** Uso restrito a divergências materiais, decisões arquiteturais ou necessidade de terceira opinião. Eles **não** possuem autoridade de aprovação.
*   **Fluxo Obrigatório:** `Davi → Claude → Codex → Claude → Codex → Davi → Git`

## 2. Escopo da Tarefa e Anti-Bypass
*   **Foco Exclusivo:** Execute *somente* a tarefa autorizada. Não avance automaticamente para outras tarefas (AC, SEM, SYN).
*   **Sem Iniciativas Paralelas:** Não crie agentes, workflows, documentos ou infraestruturas que não tenham sido explicitamente solicitados.
*   **Proibição de Bypass:** A falta de permissão não autoriza a quebra de regras. Não altere políticas, sandboxes ou controles para contornar restrições. Se não puder avançar, interrompa e responda com `BLOCKED` ou `HUMAN_DECISION_REQUIRED`.

## 3. Matriz de Classificação de Risco
Antes de qualquer alteração, o risco deve ser classificado:

| Risco | Nível | Descrição (Gatilhos) |
| :---: | :--- | :--- |
| 🟢 | **Verde** | Mudança local, reversível; sem impacto em auth, dados ou plano de controle. |
| 🟡 | **Amarelo** | Múltiplos alvos/módulos, semântica canônica ou expansão relevante de código. |
| 🔴 | **Vermelho** | Dependências, migrations, RLS, MFA, auth, auditoria ou privacidade. |
| 🚨 | **Crítico** | `.devcontainer`, `CI`, `hooks`, `managed settings`, `secrets`, `deploy` ou infra. |

## 4. Regras Estritas de Git e Estado
O Git é a *state machine* exclusiva do projeto e o mecanismo oficial de handoff. Não crie logs de interação, state machines ou relatórios paralelos ao Git para persistir evidências materiais.

*   **PERMITIDO aos Agentes (Inspeção - Read Only):** `status`, `diff`, `log`, `show`, `rev-parse`, `ls-files`.
*   **PROIBIDO aos Agentes (Mutações - Exclusivo Humano):** Qualquer comando que altere index, refs, histórico ou remoto (`add`, `commit`, `push`, `pull`, `merge`, `rebase`, `checkout`, `branch`, `worktree`, `stash`, `clean`, etc.).

## 5. Zonas de Controle (Read-Only)
**NUNCA** modifique os arquivos/diretórios abaixo, a menos que a tarefa solicite explicitamente essa alteração:
*   `AGENT_POLICY.md`, `CLAUDE.md`, `AGENTS.md`
*   `.devcontainer/**`, `.claude/**`, `.codex/**`, `.github/workflows/**`, `runbooks/**`, `scripts/ci/**`
*   Segredos, tokens e credenciais.

## 6. Tratamento de Dados e Modelagem
*   **Fontes:** Fontes controladas são *somente leitura*. O diretório `.drive/**` **não é** autoritativo (pode conter rascunhos humanos).
*   **Pipeline de Modelagem:** Siga estritamente a ordem: `fonte → evidência → conhecimento → modelo canônico → modelo lógico`.
*   **Integridade:** Não invente conhecimento (alucinação) para cobrir lacunas. Não altere a fonte para forçar uma conclusão.
*   **Referência Base:** Ao modelar dados, consulte `[PLANO_CEPRAEA_Modelo_Canonico_FINAL.md](./docs/modelagem/PLANO_CEPRAEA_Modelo_Canonico_FINAL.md)`.

## 7. Validação e Documentação
*   **Executor:** Deve rodar todos os validadores determinísticos aplicáveis *antes* de realizar o handoff.
*   **Reviewer:** Reexecuta apenas os checks necessários para auditoria independente, baseando-se no nível de risco (Matriz).
*   **Documentação:** Toda criação ou alteração de arquivos Markdown deve seguir estritamente o `docs/standards/guia_estilo_documentação.md`.
