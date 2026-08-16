ESTADO PRETENDIDO COM A ARQUITETURA FINAL

2.1 Arquitetura final pretendida

Autoridade Humana
↓
Task Proposal
↓
Task Contract formal
↓
Verification Plan
↓
Aprovação humana vinculada por hashes
↓
Claude Code — Executor
↓
Artefato candidato
↓
Verifier determinístico
↓
PASS | FAIL | BLOCKED
↓
Codex — Reviewer independente
↓
PASS | FAIL | HUMAN_DECISION_REQUIRED
↓
Homologação humana
↓
Git / promoção

2.2 Separação de funções

Executor ≠ Verifier ≠ Reviewer ≠ Autoridade Humana.

Executor
Produz e corrige o artefato candidato.

Verifier
Calcula propriedades formalizadas a partir de observações reproduzíveis.

Reviewer
Realiza assurance independente sobre semântica residual, regressões, completude, adequação de testes, suficiência de evidência, overclaims e possíveis lacunas do contrato.

Humano
Define significado, autoriza contrato e escopo, resolve decisões materiais, homologa e executa transições Git privilegiadas.

2.3 Regra matemática de decisão formal

Cada propriedade Pi assume exatamente um dos estados:
TRUE, FALSE ou UNKNOWN.

FAIL se existir pelo menos uma propriedade FALSE.
BLOCKED se não existir FALSE e existir pelo menos uma propriedade UNKNOWN.
PASS somente se todas as propriedades forem TRUE.

Ausência de evidência nunca é convertida em PASS.

2.4 Regra de precedência

FormalResult != PASS implica que o Reviewer não pode emitir PASS sobre a tarefa.
FormalResult == PASS não obriga Reviewer PASS.

Uma decisão humana que considere o contrato incorreto deve gerar revisão do contrato, nova aprovação e nova verificação. Não deve existir bypass narrativo que converta uma propriedade formal falsa em verdadeira.

2.5 Contrato formal da tarefa

Cada Task Contract deve possuir, no mínimo:
• contract_id e versão;
• task_id e vínculo com a proposta;
• baseline Git;
• read-set;
• write-set;
• forbidden-set;
• invariantes;
• critérios de aceite;
• propriedades formais;
• propriedades residuais de review;
• procedimentos de observação;
• bindings de evidência;
• política fail-closed;
• hashes de integridade.

2.6 Álgebra mínima de propriedades

A primeira versão deve ser pequena e auditável. Operadores recomendados:
exists
equals
not_equals
subset
disjoint
count_eq
count_le
unique
regex_match
sha256_equals
git_ref_equals
changed_paths_subset
exit_code_equals
json_schema_valid
no_orphan_references

Não introduzir linguagem arbitrária de script dentro do contrato quando um operador fechado puder representar a regra.

2.7 Verification Package

O verifier deve produzir resultado estruturado com:
• contract_id;
• hashes do contrato, plano e runner;
• baseline observado;
• resultado global;
• resultado de cada assertion;
• observações;
• contraexemplos para propriedades falsas quando disponíveis;
• causas de UNKNOWN/BLOCKED;
• integridade do package.

2.8 Objetivo de segurança

A correção da entrega deve depender progressivamente menos da confiança no texto produzido por LLMs e mais de:
• propriedades formalizadas;
• execução determinística;
• isolamento;
• evidência reproduzível;
• revisão independente;
• homologação humana.
