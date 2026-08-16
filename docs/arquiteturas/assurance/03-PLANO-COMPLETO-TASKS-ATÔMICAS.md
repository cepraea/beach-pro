# PLANO COMPLETO EM TASKS ATÔMICAS

**Princípio**
Uma task atômica deve produzir um único resultado verificável, não misturar decisões humanas com implementação mecânica e não avançar automaticamente quando sua pós-condição falhar.

***

## FASE A — GOVERNANÇA E BASELINE

TASK-ARCH-001 — Homologar o escopo da mudança arquitetural
Owner: Humano.
Entrada: este documento e arquitetura vigente.
Ação: confirmar quais componentes de control plane podem ser alterados.
Saída: decisão humana explícita.
Gate: sem aprovação, nenhuma task de escrita do control plane inicia.

TASK-ARCH-002 — Definir a branch de implantação
Owner: Humano.
Ação: escolher nome, base e política de integração.
Saída: branch autorizada.
Gate: branch diferente de main para execução por agentes.

TASK-ARCH-003 — Capturar baseline imutável da execução
Owner: Executor, somente inspeção.
Ação: registrar HEAD da branch, HEAD de main, git status e hashes dos arquivos de controle relevantes.
Saída: baseline verificável.
Gate: working tree e refs coerentes com a tarefa aprovada.

TASK-ARCH-004 — Definir critérios de rollout
Owner: Humano + Reviewer.
Ação: fixar condições que diferenciam PILOT, READY e MANDATORY.
Saída: critérios binários de promoção.
Gate: critérios não podem depender de opinião narrativa indefinida.

TASK-ARCH-005 — Decidir branch protection
Owner: Humano.
Ação: avaliar risco de main sem proteção e decidir configuração.
Saída: decisão registrada; alteração de GitHub somente se autorizada.

***

## FASE B — MODELO FORMAL DO CONTRATO

TASK-ARCH-006 — Criar task-contract.schema.json
Owner: Executor.
Ação: definir estrutura normativa do Task Contract.
Saída: schema válido.
Gate: additionalProperties controlado, IDs e hashes tipados.

TASK-ARCH-007 — Criar assertion.schema.json
Owner: Executor.
Ação: definir a estrutura de uma propriedade verificável.
Saída: schema com domain, operator, operands, expected e observation binding.
Gate: nenhuma assertion aceita lógica textual arbitrária como autoridade.

TASK-ARCH-008 — Criar verification-result.schema.json
Owner: Executor.
Ação: definir PASS, FAIL e BLOCKED e a estrutura das evidências/violações.
Saída: schema validável.
Gate: resultado global derivável dos resultados individuais.

TASK-ARCH-009 — Criar task-approval.schema.json
Owner: Executor.
Ação: transformar o example de aprovação em schema normativo.
Saída: approval vinculada por digest à proposta, contrato, plano e baseline.
Gate: alteração de qualquer artefato vinculado invalida approval anterior.

TASK-ARCH-010 — Evoluir task-proposal
Owner: Executor.
Ação: adicionar IDs estáveis de critérios e classificação formal/reviewer.
Saída: schema de proposta atualizado ou nova versão.
Gate: compatibilidade decidida pela PEND-006.

TASK-ARCH-011 — Criar catálogo fechado de operadores v1
Owner: Executor + Reviewer.
Ação: especificar semântica exata dos operadores mínimos.
Saída: catálogo normativo testável.
Gate: cada operador deve ter truth table ou regra computável.

TASK-ARCH-012 — Criar fixtures de schemas
Owner: Executor.
Ação: produzir casos ACCEPT/REJECT para proposta, contrato, assertion, approval e resultado.
Saída: suíte de fixtures.
Gate: ao menos um caso negativo por invariante estrutural material.

TASK-ARCH-013 — Verificar cobertura Proposal → Contract → Plan
Owner: Reviewer.
Ação: tentar encontrar critérios que desapareçam na transformação.
Saída: finding ou PASS.
Gate: conjunto de IDs materiais preservado sem órfãos.

***

## FASE C — VERIFIER DETERMINÍSTICO

TASK-ARCH-014 — Definir modelo de observações
Owner: Executor.
Ação: mapear cada operador para observações reproduzíveis.
Saída: contrato de observation types.

TASK-ARCH-015 — Implementar avaliação ternária
Owner: Executor.
Ação: implementar TRUE/FALSE/UNKNOWN e agregação global.
Saída: evaluator determinístico.
Gate: FAIL tem precedência sobre UNKNOWN; UNKNOWN sem FALSE resulta BLOCKED.

TASK-ARCH-016 — Implementar changed_paths e conjuntos de arquivos
Owner: Executor.
Ação: suportar subset/disjoint sobre paths observados.
Saída: verificação de write-set e forbidden-set.

TASK-ARCH-017 — Implementar integridade por SHA-256
Owner: Executor.
Ação: verificar contrato, plano, runner e fontes read-only pinadas.
Saída: checks de digest.

TASK-ARCH-018 — Implementar checks de processo
Owner: Executor.
Ação: executar ferramentas permitidas em sandbox e capturar exit code/stdout/stderr como evidência.
Saída: observações processuais estruturadas.

TASK-ARCH-019 — Implementar validação de schema e referências
Owner: Executor.
Ação: integrar json_schema_valid e no_orphan_references.
Saída: assertions estruturais.

TASK-ARCH-020 — Implementar verification package
Owner: Executor.
Ação: publicar atomicamente resultado, observações, hashes e violações.
Saída: package imutável por run_id.

TASK-ARCH-021 — Proteger o verifier contra autoalteração
Owner: Humano + Executor.
Ação: colocar runner e schemas normativos em caminho protegido/read-only para o Executor em tarefas comuns.
Saída: enforcement técnico.
Gate: tarefa normal não pode editar o mecanismo que a julga.

***

## FASE D — CONFORMIDADE E AMBIENTE

TASK-ARCH-022 — Inventariar requisitos reais do FVR
Owner: Reviewer.
Ação: comparar SYSTEM_REQUIREMENTS, Dockerfile e harness.
Saída: matriz instalado/faltante/incompatível.

TASK-ARCH-023 — Completar dependências do ambiente
Owner: Executor, somente após autorização vermelho-crítico.
Ação: instalar/pinar somente dependências exigidas.
Saída: Dev Container reproduzível.

TASK-ARCH-024 — Executar conformance harness
Owner: Executor.
Ação: executar harness completo.
Saída: relatório de conformidade.

TASK-ARCH-025 — Revisar independentemente a conformidade
Owner: Reviewer.
Ação: reproduzir checks críticos e tentar refutar o resultado.
Saída: PASS/FAIL/HUMAN_DECISION_REQUIRED.

TASK-ARCH-026 — Homologar promoção do verifier
Owner: Humano.
Gate: somente se harness CONFORMANT e todos os vetores mandatórios PASS.
Saída: autorização para uso piloto.

***

## FASE E — INTEGRAÇÃO COM EXECUTOR

TASK-ARCH-027 — Atualizar AGENT_POLICY.md
Owner: Executor, com autorização explícita de control plane.
Ação: registrar Executor ≠ Verifier ≠ Reviewer ≠ Humano e precedência do FormalResult.
Saída: política comum atualizada.

TASK-ARCH-028 — Atualizar CLAUDE.md
Owner: Executor.
Ação: exigir Formal PASS antes de READY_FOR_REVIEW quando task usar o novo contrato.
Saída: protocolo de handoff atualizado.

TASK-ARCH-029 — Atualizar runbooks shared
Owner: Executor.
Ação: incorporar verification package, estados formais e evidências.
Saída: runbooks compartilhados consistentes.

TASK-ARCH-030 — Atualizar runbooks do Executor
Owner: Executor.
Ação: definir sequência contract → execute → verify → correct/block → handoff.
Saída: procedimentos por operation_class.

***

## FASE F — INTEGRAÇÃO COM REVIEWER

TASK-ARCH-031 — Atualizar AGENTS.md
Owner: Executor para a alteração; Codex revisa, não edita.
Ação: impedir PASS quando FormalResult != PASS.
Saída: política do Reviewer atualizada.

TASK-ARCH-032 — Atualizar runbooks do Reviewer
Owner: Executor.
Ação: incluir validação do verification package antes do assurance residual.
Saída: procedimentos reviewer atualizados.

TASK-ARCH-033 — Definir matriz de propriedades formais versus residuais
Owner: Reviewer + Humano.
Ação: classificar o que é decidido pelo verifier e o que permanece em review.
Saída: fronteira explícita.
Gate: nenhuma propriedade material pode ficar sem owner de verificação.

TASK-ARCH-034 — Testar tentativa de bypass
Owner: Reviewer.
Ação: usar fixture Formal FAIL e verificar que Reviewer PASS é rejeitado pelo fluxo.
Saída: evidência fail-closed.

***

## FASE G — DOCUMENTAÇÃO CANÔNICA

TASK-ARCH-035 — Atualizar arquitetura Human-Governed Dual-Agent SDLC
Owner: Executor.
Ação: adicionar Contract Plane e Formal Verification Plane sem remover Execution/Assurance Plane.
Saída: arquitetura final versionada.

TASK-ARCH-036 — Atualizar diagramas e precedência
Owner: Executor.
Ação: documentar estados, transições, autoridade e canais de handoff.
Saída: diagramas coerentes com policies e runbooks.

TASK-ARCH-037 — Revisar consistência documental
Owner: Reviewer.
Ação: comparar arquitetura, policies, schemas e runbooks.
Saída: nenhuma contradição material.

***

## FASE H — PILOTO E PROMOÇÃO

TASK-ARCH-038 — Selecionar tarefa piloto
Owner: Humano.
Critério: pequena, reversível, baixa ambiguidade e propriedades observáveis.

TASK-ARCH-039 — Escrever contrato do piloto
Owner: Executor; humano aprova.
Saída: proposal + contract + verification plan + approval bindings.

TASK-ARCH-040 — Executar piloto
Owner: Claude Code.
Saída: artefato candidato.

TASK-ARCH-041 — Verificar piloto
Owner: Verifier.
Saída: PASS/FAIL/BLOCKED + package.

TASK-ARCH-042 — Revisar piloto
Owner: Codex.
Saída: PASS/FAIL/HUMAN_DECISION_REQUIRED.

TASK-ARCH-043 — Executar failure injection
Owner: Reviewer/Executor conforme fixture.
Casos mínimos: path não autorizado; hash alterado; assertion FALSE; evidência ausente; UNKNOWN; tentativa de alterar verifier; contrato alterado após approval.

TASK-ARCH-044 — Homologar resultado do piloto
Owner: Humano.
Saída: decisão de corrigir, repetir ou promover.

TASK-ARCH-045 — Tornar gate obrigatório
Owner: Humano.
Pré-condição: somente após critérios de rollout atendidos.
Saída: estado MANDATORY.

TASK-ARCH-046 — Encerrar implantação
Owner: Humano + Reviewer.
Ação: confirmar rastreabilidade, decisões finais, artefatos e ausência de pendências bloqueantes.
Saída: arquitetura implantada e homologada.

***

