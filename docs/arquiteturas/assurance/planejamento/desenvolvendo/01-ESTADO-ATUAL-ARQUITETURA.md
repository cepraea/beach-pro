# ESTADO ATUAL DA ARQUITETURA

## 1.1 Arquitetura operacional vigente

O fluxo atual é um Human-Governed Dual-Agent SDLC:

Humano → Claude Code EXECUTOR → validações determinísticas → working tree/git diff → Codex REVIEWER → Humano → Git.

A política comum estabelece:
- o humano é a autoridade final sobre domínio, decisões materiais, Git, release e deploy;
- Claude Code é o EXECUTOR;
- Codex é o REVIEWER independente;
- produção, revisão e aprovação são funções distintas;
- nenhum agente pode aprovar ou promover o próprio trabalho;
- operações Git que alteram refs, index, histórico ou remoto pertencem ao humano;
- restrições não podem ser contornadas; incapacidade legítima gera BLOCKED ou HUMAN_DECISION_REQUIRED.

## 1.2 Executor

O Executor:
- recebe a tarefa autorizada;
- lê o contexto necessário;
- identifica validadores aplicáveis;
- produz somente a mudança autorizada;
- executa validações determinísticas;
- corrige erros mecânicos;
- inspeciona git diff, git diff --check e git status;
- entrega READY_FOR_REVIEW ou BLOCKED.

O Executor não possui autoridade para declarar a entrega homologada.

## 1.3 Reviewer

O Reviewer:
- opera de forma independente;
- inspeciona diff, status, arquivos-alvo, critérios e evidências;
- procura regressões;
- tenta refutar conclusões materiais;
- verifica rastreabilidade e suficiência de evidência;
- reexecuta checks proporcionalmente ao risco;
- não corrige findings nem altera os artefatos sob revisão;
- emite PASS, FAIL ou HUMAN_DECISION_REQUIRED.

O Reviewer continua obrigatório na arquitetura vigente.

## 1.4 Validação determinística existente

Já existem validadores determinísticos e uma estrutura FVR. O verification-plan suporta operações como file.exists, file.sha256, git.diff, git.diff_names e process.run em sandbox, além de assertions identificadas por AC-NNN e INV-NNN.

Entretanto, o task-proposal ainda representa critérios de aceite principalmente por strings humanas: condição, método e esperado. Portanto, existe um gap entre a tarefa textual e as assertions formais.

## 1.5 Estado do FVR

O pacote FVR existente se declara implementation candidate. A conformidade não é concedida apenas porque o runner executa.

O certificado disponível registra NOT_ISSUED / HARNESS_INVALID. Logo, não existe evidência suficiente, no baseline atual, para tratar o runner FVR como verificador conformante de produção do fluxo.

## 1.6 Gap principal

Estado atual:
Task Proposal textual → Executor → validadores → Reviewer.

Gap:
não existe ainda uma camada normativa completa que faça a transformação:
requisito humano → propriedade formal tipada → observação determinística → assertion → PASS/FAIL/BLOCKED.

## 1.7 Riscos atuais relevantes para a implantação

ID | Risco
:---: | ---
R-001  |  Critérios de aceite textuais permitem interpretação diferente entre Executor e Reviewer.
R-002  |  Um validador pode ser determinístico e ainda implementar uma regra formal incorreta.
R-003  |  O FVR ainda não possui conformidade comprovada no ambiente atual.
R-004  |  Ausência de ligação completa por hash entre proposta, contrato, plano e resultado pode permitir drift.
R-005  |  Reviewer ainda precisa recalcular fatos que poderiam ser decididos mecanicamente.
R-006  |  Uma propriedade formal incompleta pode produzir PASS técnico sem representar toda a intenção humana.
R-007  |  A branch main aparece sem branch protection no baseline observado.
R-008  |  Alterar simultaneamente policy, schemas, runner, container e runbooks ampliaria excessivamente o blast radius.
