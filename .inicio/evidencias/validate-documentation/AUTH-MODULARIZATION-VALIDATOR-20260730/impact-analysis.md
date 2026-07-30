# Análise de impacto — autorização da modularização do validador

## 1. Identificação

| Campo | Valor |
| --- | --- |
| Autorização | `AUTH-MODULARIZATION-VALIDATOR-20260730-001` |
| Plano | `.inicio/PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md` |
| Commit do plano | `6fbfdad55240b5b9f6d377f8b436e314d7feeb8a` |
| Autoridade declarada | Davi Sermenho — `AUTORIDADE_APROVADORA` |
| Gate Git | `GIT-WORKFLOW-READY = PASS` |
| Próximo gate | `GOVERNANCE-MODULARIZATION` |

## 2. Resultado executivo

A autorização remove a ambiguidade decisória de `BEH-01…BEH-07` e permite
iniciar a Fase 0 do plano. Ela não antecipa gates posteriores e não autoriza
tratar a modularização como prontidão para produção.

## 3. Impacto por decisão

| Decisão | Impacto observável | Risco principal | Controle obrigatório |
| --- | --- | --- | --- |
| `BEH-01` | A raiz deixa de depender exclusivamente de `parents[3]` e passa a ser descoberta por marcadores canônicos | selecionar workspace incorreto ou mudar a inicialização do pacote | RED–GREEN para raiz, arquivo, subdiretório, marcadores parciais, ausência e symlink suportado |
| `BEH-02` | Itens não mapping em `documents` deixam de ser descartados e passam a bloquear com índice exato | acervos antes aceitos por falso positivo passam a falhar | validar o registro bruto antes do estreitamento e preservar os demais diagnósticos verificáveis |
| `BEH-03` | Chaves YAML complexas deixam de encerrar com `TypeError` e passam a produzir erro controlado | captura excessiva esconder defeitos não relacionados | converter somente a falha prevista e preservar contexto da chave e do arquivo |
| `BEH-04` | UTF-8 inválido deixa de ser substituído silenciosamente e passa a falhar | arquivos historicamente tolerados podem ser revelados como inválidos | teste com bytes inválidos e mensagem determinística identificando o arquivo |
| `BEH-05` | Falhas de leitura deixam de escapar do pipeline e passam ao `Reporter` | normalização excessiva perder a causa operacional | preservar tipo, caminho e causa útil sem traceback inesperado |
| `BEH-06` | Testes podem fornecer `argv` diretamente; `argv=None` mantém a CLI real | divergência entre chamada programática e entrada por módulo | caracterização das duas entradas e equivalência de códigos e resultados |
| `BEH-07` | A fachada pública final passa a exportar somente `main` | quebra de consumidores externos não visíveis por busca local | inventário de consumidores, reexports transitórios e teste dedicado antes da remoção |

## 4. Impactos transversais

- Cada decisão comportamental exige teste RED pelo motivo correto e GREEN após
  a menor correção possível.
- Mudanças autorizadas devem permanecer separadas das extrações estruturais.
- Diferenças de saída devem ser justificadas contra a baseline; diferenças não
  autorizadas continuam bloqueantes.
- `npm run validate`, testes Python, Pyright fixado e gates afetados continuam
  obrigatórios conforme o plano.
- Funções complexas devem explicar o porquê de decisões de integridade,
  segurança, fail-fast e compatibilidade histórica.

## 5. Limitações preservadas

Continuam abertas:

1. identidade dos gates globais versus evidências de aprovação;
2. comprovação dos bytes reais de fontes locais em G2;
3. obrigatoriedade de G2 para aprovação;
4. quantidade fixa de dez registros de ingestão.

A autorização também não amplia o perfil Markdown e não declara o validador
apto a operar como gate bloqueante de produção.

## 6. Estado resultante

```text
GIT-WORKFLOW-READY:             PASS
BEH-01…BEH-07:                  APPROVED
EXECUÇÃO DO PLANO:              UNLOCKED FOR PHASE 0
GOVERNANCE-MODULARIZATION:      PENDING
PRONTIDÃO BLOQUEANTE PRODUÇÃO:  NOT AUTHORIZED
```
