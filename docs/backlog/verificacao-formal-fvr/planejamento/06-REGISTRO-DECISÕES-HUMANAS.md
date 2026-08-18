# REGISTRO DAS DECISÕES HUMANAS

## 3.1 Decisões confirmadas

HDEC-001 — Autoridade humana final
Status: CONFIRMADA.
Decisão: o humano permanece autoridade final sobre domínio, decisões materiais, Git privilegiado, release, deploy e homologação.

HDEC-002 — Manutenção do Executor
Status: CONFIRMADA.
Decisão: Claude Code permanece como EXECUTOR.

HDEC-003 — Manutenção do Reviewer
Status: CONFIRMADA.
Decisão: Codex permanece como REVIEWER independente. A nova camada formal não elimina o Reviewer.

HDEC-004 — Separação de funções
Status: CONFIRMADA.
Decisão: produção, verificação, revisão e homologação permanecem funções distintas; nenhum agente aprova o próprio trabalho.

HDEC-005 — Objetivo da nova arquitetura
Status: CONFIRMADA.
Decisão: a implantação deve diminuir riscos, manter o humano informado e preservar rastreabilidade do trabalho.

HDEC-006 — Verificação determinística antes do review
Status: CONFIRMADA PELO DIRECIONAMENTO DA NOVA ARQUITETURA.
Decisão: uma camada formal/determinística deve avaliar propriedades verificáveis antes do Reviewer.

HDEC-007 — Preservação de fail-closed
Status: CONFIRMADA PELO FLUXO VIGENTE E PELO OBJETIVO DE RISCO.
Decisão: ausência ou insuficiência de evidência não autoriza PASS; deve resultar em BLOCKED, FAIL ou decisão humana conforme a causa.

HDEC-008 — Plano em tasks atômicas
Status: CONFIRMADA.
Decisão: a implantação deve ser decomposta em tasks atômicas, com escopo limitado, critérios observáveis e handoff rastreável.

HDEC-009 — Runbook de implantação
Status: CONFIRMADA.
Decisão: a execução da mudança deve seguir um runbook explícito, com pré-condições, gates, evidências, estados de saída e rollback.

HDEC-010 — Registro no Google Drive
Status: CONFIRMADA.
Decisão: este Google Doc é o registro humano central para acompanhamento da implantação e das decisões materiais.

## 3.2 Decisões ainda pendentes de autoridade humana

PEND-001 — Nome e criação da branch dedicada de implantação.
Recomendação: feat/formal-verification-control-plane.
Não executar sem decisão humana.

PEND-002 — Estratégia de branch protection para main.
Fato de baseline: protected=false na API consultada.
Decisão necessária: habilitar ou manter sem proteção técnica externa.

PEND-003 — Local definitivo do runner/verifier.
Recomendação: scripts/ci/task-verifier/** ou outro caminho protegido equivalente.
Decisão humana necessária antes de alterar o control plane.

PEND-004 — Promoção do FVR candidate.
Decisão: somente considerar o FVR como autoridade operacional após conformance harness CONFORMANT e todos os vetores obrigatórios PASS.

PEND-005 — Momento em que o novo gate deixa de ser piloto e se torna obrigatório.
Recomendação: após fixtures negativas, piloto real, review independente e homologação humana.

PEND-006 — Política de compatibilidade/migração de task-proposal v1.0.
Opções: migração in-place para v2.0 ou coexistência temporária v1/v2.

PEND-007 — Assinatura/attestation humana.
Decisão necessária sobre uso real de assinatura criptográfica, trusted UI ou somente digest/handoff humano no MVP.

3.3 Regra de manutenção deste registro

Toda decisão pendente transformada em decisão final deve receber:
• ID estável;
• status;
• decisão literal;
• autor humano;
• artefatos afetados;
• motivo;
• efeito sobre tasks já executadas;
• necessidade ou não de reexecução.

As sete decisões pendentes existem porque afetam o próprio plano de controle da arquitetura. Portanto, não devem ser inferidas pelo Executor ou pelo Reviewer. Elas precisam ser resolvidas pela autoridade humana antes da fase que delas depende.

A leitura correta de cada uma é a seguinte.

### PEND-001 — Nome e criação da branch dedicada de implantação

Decisão pendente: definir em qual branch será implantada a nova arquitetura formal. O documento propositalmente não criou essa branch, porque criar, mover ou promover refs Git pertence à autoridade humana no modelo vigente.

Recomendação registrada:

`feat/formal-verification-control-plane`

A justificativa é separar duas mudanças conceitualmente diferentes. A branch existente `feat/cepraea-domain-modeling` trata de modelagem canônica do domínio; já essa nova implantação modifica o mecanismo que governa como tarefas são especificadas, verificadas e aceitas.

Misturar as duas coisas aumentaria o blast radius e dificultaria responder perguntas como: “esta alteração ocorreu por causa da modelagem do domínio ou por causa da mudança do sistema de assurance?”

A separação produz uma fronteira clara:

```text
feat/cepraea-domain-modeling
        ↓
modelagem do domínio

feat/formal-verification-control-plane
        ↓
contratos + verifier + schemas + policies + runbooks
```

Minha recomendação técnica coincide com a registrada: usar uma branch dedicada. O nome exato é secundário; a separação é o requisito material.

---

### PEND-002 — Estratégia de branch protection para `main`

Decisão pendente: decidir se a política humana atualmente descrita documentalmente também será reforçada tecnicamente pelo GitHub.

O fato observado durante a elaboração do documento foi:

```text
main
protected = false
```

Isso significa que há uma regra normativa dizendo que agentes não devem executar determinadas transições Git, mas o próprio GitHub não está necessariamente impedindo essas operações.

A decisão é entre duas arquiteturas:

```text
A. Governança predominantemente normativa

Policy:
agente NÃO DEVE alterar main

GitHub:
tecnicamente pode não impedir
```

ou:

```text
B. Governança + enforcement técnico

Policy:
agente NÃO DEVE alterar main

GitHub:
também impede determinadas alterações
```

A justificativa para recomendar proteção técnica é o princípio de defense in depth. Uma regra que pode ser fisicamente imposta não deveria depender exclusivamente de obediência comportamental de um agente.

Em termos simples:

```text
Regra textual ≠ barreira técnica
```

e:

```text
Policy + Enforcement > Policy isolada
```

Minha recomendação técnica é habilitar branch protection compatível com o fluxo humano, sem impedir as operações legítimas que você decidiu reservar a si mesmo.

Isso é particularmente coerente com o objetivo da arquitetura: reduzir a quantidade de segurança que depende da interpretação correta de uma LLM.

---

### PEND-003 — Local definitivo do runner/verifier

Decisão pendente: definir onde ficará o código que verifica as próprias tarefas.

A recomendação registrada é algo como:

```text
scripts/ci/task-verifier/**
```

ou outro diretório equivalente explicitamente protegido.

O problema é arquitetural, não apenas organizacional. O verifier não é um script comum. Ele pertence ao plano de controle.

Se uma tarefa puder modificar simultaneamente:

```text
artefato que será julgado
+
regra utilizada para julgá-lo
```

a independência da verificação desaparece.

Exemplo incorreto:

```text
TASK
  ↓
agente altera feature
  ↓
agente percebe que verifier rejeita feature
  ↓
agente altera verifier
  ↓
PASS
```

O resultado pode ser deterministicamente `PASS`, mas o mecanismo foi adulterado.

A arquitetura correta exige:

```text
Artefato candidato
        ↓
Verifier previamente fixado
        ↓
Resultado
```

Por isso a recomendação de um caminho dedicado vem acompanhada da ideia de proteção/read-only para tarefas normais.

Minha recomendação é adotar uma localização explícita do plano de controle e tratá-la como `forbidden-set` por padrão. Uma tarefa específica para modificar o verifier teria de receber autorização humana própria.

---

### PEND-004 — Promoção do FVR candidate

Decisão pendente: determinar quando o FVR deixa de ser apenas uma implementação candidata e pode ser considerado uma autoridade operacional do fluxo.

O próprio estado atual registrado não permite promovê-lo automaticamente. O certificado existente está como `NOT_ISSUED / HARNESS_INVALID`.

O critério proposto é forte:

```text
FVR_OPERACIONAL =
    HarnessConformant
    AND
    MandatoryVectorsPass
```

Ou seja, “o programa executou” não basta.

É necessário demonstrar que o próprio verificador implementa corretamente o protocolo que afirma implementar.

Essa distinção é fundamental:

```text
Runner executável
≠
Runner correto
≠
Runner conformante
```

A recomendação é não utilizar o FVR como autoridade de decisão antes de:

1. o conformance harness declarar `CONFORMANT`;
2. todos os vetores obrigatórios produzirem os resultados esperados;
3. o Reviewer independente tentar refutar essa conclusão;
4. a autoridade humana homologar a promoção.

A justificativa é evitar um bootstrap circular:

```text
“o verifier é confiável porque o próprio verifier disse que é confiável”
```

A conformidade precisa vir de evidência externa ao objeto que está sendo avaliado.

---

### PEND-005 — Quando o gate passa de piloto para obrigatório

Decisão pendente: determinar em que momento todas as tarefas passam obrigatoriamente pelo novo mecanismo formal.

O documento recomenda não tornar o gate obrigatório logo após a implementação.

A sequência proposta é:

```text
IMPLEMENTADO
    ↓
FIXTURES
    ↓
PILOTO REAL
    ↓
FAILURE INJECTION
    ↓
REVIEW INDEPENDENTE
    ↓
HOMOLOGAÇÃO HUMANA
    ↓
MANDATORY
```

A justificativa é evitar transformar um mecanismo ainda não validado em dependência crítica de todo o SDLC.

Se o gate for tornado obrigatório cedo demais, um erro no próprio verifier pode bloquear todas as tarefas legítimas ou, pior, aprovar tarefas incorretas.

O piloto deve testar dois lados:

```text
Positive assurance:
uma entrega correta consegue passar?

Negative assurance:
uma entrega incorreta é realmente rejeitada?
```

Por isso as fixtures negativas e o failure injection são especialmente importantes.

Minha recomendação é manter três estados explícitos:

```text
PILOT
READY
MANDATORY
```

e impedir transição automática entre eles. A promoção deve ser uma decisão humana.

---

### PEND-006 — Compatibilidade e migração do `task-proposal` v1.0

Decisão pendente: definir como introduzir a nova representação formal sem quebrar o formato existente das tarefas.

Hoje, simplificando, o modelo é:

```json
{
  "condicao": "...",
  "metodo": "...",
  "esperado": "passou"
}
```

Esse formato é compreensível por humanos, mas ainda depende de interpretação.

A arquitetura nova precisa chegar a algo estruturalmente mais próximo de:

```text
ID
Domain
Operator
Operands
Expected
Observation
```

Há duas estratégias registradas.

Opção A — migração direta:

```text
task-proposal v1
        ↓
task-proposal v2
```

A partir da mudança, apenas v2 seria aceito.

Vantagem: arquitetura simples e uma única fonte normativa.

Risco: aumenta o blast radius da migração e pode tornar artefatos existentes incompatíveis imediatamente.

Opção B — coexistência temporária:

```text
v1 ──┐
     ├── período de transição
v2 ──┘
```

Vantagem: rollout mais seguro e reversível.

Risco: durante algum tempo existem dois contratos de representação, aumentando a complexidade do sistema.

Para a implantação mínima, minha recomendação é coexistência curta e explicitamente limitada, seguida da remoção da v1.

Por exemplo:

```text
PILOT       → v1 + v2
READY       → v2 preferencial
MANDATORY   → somente v2
```

Assim a compatibilidade existe apenas durante a migração, e não se transforma em dívida permanente.

---

### PEND-007 — Assinatura ou attestation humana

Essa é provavelmente a decisão pendente mais fácil de over-engineer.

O problema que precisa ser resolvido é legítimo: o sistema deve conseguir provar exatamente qual conjunto de artefatos você aprovou.

Imagine:

```text
proposal = A
contract = B
plan = C
```

Você aprova.

Depois alguém modifica `B`.

Sem binding de integridade, ainda poderia existir uma aprovação humana aparentemente válida para um contrato diferente daquele que você efetivamente aprovou.

Por isso a arquitetura precisa de algo como:

```text
Approval(
    SHA256(proposal),
    SHA256(contract),
    SHA256(plan),
    baseline
)
```

A decisão pendente é como materializar essa aprovação.

As alternativas registradas são aproximadamente:

```text
1. assinatura criptográfica real;
2. trusted UI / attestation;
3. digest + handoff humano.
```

Uma assinatura criptográfica oferece assurance mais forte, mas introduz gerenciamento de chaves, revogação, armazenamento seguro e novos modos de falha.

Para o MVP atual, isso provavelmente seria desproporcional.

Minha recomendação é:

```text
Human Approval v1 =
    identidade humana
    + timestamp
    + hashes dos artefatos aprovados
    + baseline
    + decisão explícita
```

sem introduzir, inicialmente, PKI ou infraestrutura de assinatura criptográfica.

O princípio importante não é “ter uma assinatura sofisticada”. É garantir:

```text
Approved(A) ∧ A ≠ B
        ⇒
Approval(B) = FALSE
```

Isto é: qualquer alteração posterior em um artefato aprovado deve invalidar automaticamente a aprovação anterior.

---

Há também uma relação de dependência entre essas decisões. Elas não precisam necessariamente ser tomadas todas simultaneamente.

A ordem racional é:

```text
PEND-001
Branch de implantação
        ↓
PEND-002
Proteção da main
        ↓
PEND-003
Local do verifier
        ↓
PEND-006
Estratégia de schema/migração
        ↓
PEND-007
Binding da aprovação humana
        ↓
IMPLEMENTAÇÃO
        ↓
PEND-004
Verifier pode ser promovido?
        ↓
PEND-005
Gate pode se tornar obrigatório?
```

Os cinco primeiros são predominantemente decisões de projeto necessárias para construir corretamente o mecanismo. `PEND-004` e `PEND-005` são diferentes: são decisões de promoção baseadas em evidências que ainda precisam ser produzidas.

Portanto, eu não encerraria `PEND-004` nem `PEND-005` agora. Seria incorreto “decidir antecipadamente” que o verifier será conformante ou que o gate será obrigatório. Esses dois estados devem continuar pendentes até que seus predicados sejam demonstrados.

**Não substituir silenciosamente uma decisão antiga. Registrar supersessão explícita.**
