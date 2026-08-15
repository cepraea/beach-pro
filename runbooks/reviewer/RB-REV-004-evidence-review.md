# RB-REV-004 — Revisão de evidências

## Objetivo

Definir o procedimento especializado de revisão independente quando a suficiência da evidência
é um aspecto material para a aceitação da operação.

## Aplicabilidade

Usar este runbook em combinação com o runbook especializado principal quando:

- os critérios de aceite exigirem evidência específica de propriedades materiais
- o Executor fizer alegações que precisam ser verificadas independentemente
- a operação envolver risco que justifique verificação adicional de evidências

## Entradas

- Evidências produzidas pelo Executor
- `git diff` da operação
- Critérios de aceite da tarefa

## Fontes de autoridade

- `AGENT_POLICY.md` — seção Persistent Evidence
- `AGENTS.md`
- Critérios de aceite da tarefa

## Pré-condições

- Evidências do Executor disponíveis
- Critérios de aceite identificados
- Reviewer operando com projeto read-only

## Escopo operacional

Somente leitura e verificação independente.

Escrita efêmera exclusivamente em `/tmp` ou caches técnicos explicitamente autorizados.

Não corrigir silenciosamente deficiências de evidência: registrar como finding.

## Procedimento

1. Identificar as alegações materiais feitas pelo Executor.
2. Para cada alegação, identificar a evidência correspondente produzida.
3. Comparar cada alegação com o estado observável no repositório.
4. Reproduzir verificações críticas quando proporcional ao risco (usar somente `/tmp` para escrita).
5. Classificar insuficiência de evidência conforme severidade.
6. Emitir o verdict com findings quando aplicável.

## Pontos de decisão

| Condição | Ação |
|---|---|
| Alegação sem evidência correspondente | Finding MEDIUM ou HIGH conforme impacto |
| Evidência contraditória com estado observável | Finding HIGH ou CRITICAL |
| Verificação crítica não reproduzível | Finding + comunicar limitação |
| Critérios de aceite ambíguos sobre o que constitui evidência | `HUMAN_DECISION_REQUIRED` |

## Critérios de suficiência mínima

Uma evidência é materialmente suficiente quando:

- existe e é verificável no estado atual do repositório
- é consistente com a alegação feita
- não contraditória com o estado observável

Uma evidência é insuficiente quando:

- está ausente para uma alegação material
- contradiz o estado observável
- não pode ser verificada independentemente e a alegação é de alto risco

## Evidências do próprio review

- Lista das alegações revisadas
- Verificações executadas independentemente
- Findings de insuficiência classificados

## Handoff

Emitir verdict com:

- lista das alegações verificadas
- findings de insuficiência (quando existirem)
- verificações independentes executadas
- questões para Davi quando aplicável

## Estados de saída

`PASS` — todas as alegações materiais possuem evidência suficiente e consistente.

`FAIL` — alegação material sem evidência, evidência contraditória ou insuficiência que impeça
aceitação.

`HUMAN_DECISION_REQUIRED` — critérios de suficiência de evidência exigem decisão de Davi.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
