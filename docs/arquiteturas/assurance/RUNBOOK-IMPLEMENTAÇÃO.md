# RUNBOOK DE IMPLEMENTAÇÃO

## 5.1 Objetivo

Executar a implantação da arquitetura formal com blast radius controlado, fail-closed, evidência reproduzível e autoridade humana em todos os pontos materiais.

## 5.2 Aplicabilidade

Aplicar às TASK-ARCH-001 até TASK-ARCH-046.

## 5.3 Autoridade e papéis

Humano
Autoriza tasks, branch, mudanças de control plane, Git privilegiado, promoção do verifier e rollout obrigatório.

Claude Code — Executor
Implementa somente a task atômica autorizada e não executa transições Git privilegiadas.

Verifier
Avalia somente propriedades formalizadas. Não interpreta intenção humana.

Codex — Reviewer
Opera read-only sobre artefatos sob revisão, tenta refutar a entrega e não corrige findings.

## 5.4 Pré-condições obrigatórias antes de cada task

1. Existe uma task ID autorizada.
2. A branch autorizada não é main.
3. git status foi inspecionado.
4. baseline da task foi capturado.
5. arquivos alvo, referência, read-only e proibidos estão identificados.
6. risco foi classificado.
7. runbooks aplicáveis foram carregados.
8. mudanças de control plane possuem autorização humana explícita.
9. nenhuma decisão pendente necessária à task está sendo inferida por agente.

Falha em qualquer pré-condição material → BLOCKED.

## 5.5 Procedimento padrão por task

PASSO 1 — Baseline
Capturar HEAD, main, status, diff inicial e hashes relevantes.

PASSO 2 — Scope lock
Resolver write-set, read-set e forbidden-set.

PASSO 3 — Implementação mínima
Alterar somente o necessário à task atual.

PASSO 4 — Autoinspeção do Executor
Executar validadores aplicáveis, git diff --check, git diff e git status.

PASSO 5 — Verificação formal
Quando a task já estiver coberta pelo novo mecanismo, executar o verifier sobre o contrato aprovado.

PASSO 6 — Decisão formal
Formal FAIL → corrigir somente dentro do escopo e verificar novamente.
Formal BLOCKED → parar e escalar ao humano.
Formal PASS → preparar handoff.

PASSO 7 — Handoff
Entregar arquivos alterados, validações, verification package, limitações e pontos de review.

PASSO 8 — Review independente
Codex verifica integridade do package, diff, regressões, evidências e residual semântico.

PASSO 9 — Tratamento do verdict
Reviewer FAIL → retorna ao Executor com findings.
Reviewer HUMAN_DECISION_REQUIRED → humano decide.
Reviewer PASS → elegível para homologação humana.

PASSO 10 — Git
Somente o humano executa add/commit/push/merge/rebase ou demais transições privilegiadas.

## 5.6 Gates de implantação

GATE G0 — GOVERNANCE_READY
Todas as decisões indispensáveis à próxima fase estão explícitas.

GATE G1 — CONTRACT_MODEL_READY
Schemas e operadores possuem fixtures positivas e negativas; coverage Proposal → Contract → Plan não possui órfãos.

GATE G2 — VERIFIER_READY
Evaluator ternário, hashes, observations e package funcionam deterministicamente.

GATE G3 — CONFORMANCE_READY
Harness CONFORMANT e vetores mandatórios PASS.

GATE G4 — DUAL_AGENT_INTEGRATED
Claude exige formal gate; Codex reconhece e respeita precedência formal; runbooks coerentes.

GATE G5 — PILOT_PASS
Piloto real e failure injection completos sem bypass.

GATE G6 — HUMAN_HOMOLOGATED
Humano autoriza MANDATORY.

Nenhum gate pode ser inferido como aprovado por ausência de finding.

## 5.7 Evidências mínimas por task

- task ID;
- baseline SHA;
- lista de arquivos alterados;
- diff;
- comandos/checks executados;
- exit codes;
- resultados de schemas/testes;
- hashes quando aplicáveis;
- verification package quando aplicável;
- verdict do Reviewer;
- decisão humana quando material;
- commit resultante somente após ação humana.

## 5.8 Estados de saída

Executor
READY_FOR_REVIEW ou BLOCKED.

Verifier
PASS, FAIL ou BLOCKED.

Reviewer
PASS, FAIL ou HUMAN_DECISION_REQUIRED.

Implantação
PILOT, READY ou MANDATORY, exclusivamente por decisão humana após gates.

## 5.9 Regras de fail-closed

- UNKNOWN nunca equivale a TRUE.
- Ausência de evidência nunca equivale a PASS.
- Formal FAIL não pode ser convertido em Reviewer PASS.
- Formal PASS não substitui review independente.
- Reviewer PASS não substitui homologação humana.
- Mudança de contrato após approval invalida approval.
- Mudança de runner após hash pinado invalida o run.
- Tentativa de alterar verifier para fazer uma task passar é violação de control plane.
- Contradição entre normas gera HUMAN_DECISION_REQUIRED/BLOCKED, não inferência.

## 5.10 Rollback

Se uma task introduzir regressão no control plane:
1. parar a sequência;
2. preservar evidência do estado falho;
3. não avançar para task seguinte;
4. humano executa rollback Git ou restauração autorizada;
5. recapturar baseline;
6. corrigir a task em nova execução;
7. repetir verifier e review.

Não realizar rollback silencioso por agente.

## 5.11 Regra de atualização deste Google Doc

Após cada decisão material ou gate:
- atualizar o ID correspondente;
- registrar estado atual;
- registrar evidência/commit relacionado;
- manter pendências abertas visíveis;
- não apagar histórico decisório; usar supersessão explícita.

## 5.12 Critério final de conclusão

A implantação só está concluída quando:
- schemas normativos estão válidos;
- Proposal → Contract → Plan possui cobertura integral de IDs materiais;
- verifier possui conformidade comprovada;
- fixtures positivas e negativas passam como esperado;
- fail-closed foi demonstrado por failure injection;
- Executor está integrado ao gate;
- Reviewer está integrado ao gate;
- arquitetura e runbooks estão consistentes;
- piloto foi concluído;
- humano homologou estado MANDATORY;
- rastreabilidade final aponta para decisões, evidências e commits.

Fórmula operacional:
ArchitectureReady =
ContractModelReady
AND VerifierConformant
AND FailClosedProven
AND ExecutorIntegrated
AND ReviewerIntegrated
AND PilotPass
AND HumanHomologated.
