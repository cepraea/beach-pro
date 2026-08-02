# Validação de COR-01 e COR-02

## 1. Escopo

Esta evidência registra o início da execução ordenada do plano de correção da
norma de tradução. COR-01 está concluída. COR-02 permanece parcialmente aberta
até que os arquivos sejam versionados e a aprovação documental seja anexada.

## 2. COR-01 — Separação entre norma, perfil e evidência

### Matriz origem-destino

| Conteúdo específico | Origem anterior | Autoridade atual | Resultado |
| --- | --- | --- | :---: |
| SHA-256 da origem japonesa | `.inicio/tradutor.md` | Evidência e perfil | PASS |
| Caminhos de `agent-list` | `.inicio/tradutor.md` | Perfil | PASS |
| Inventário 5/12/31/2/13/23/8/6 | `.inicio/tradutor.md` | Perfil | PASS |
| Nomes de agentes, modelos e fases | `.inicio/tradutor.md` | Perfil | PASS |
| 31 valores de `file_type` | `.inicio/tradutor.md` | Perfil | PASS |
| Glossário japonês → pt-BR | `.inicio/tradutor.md` | Perfil | PASS |
| Prefixos e quantidades de rastreabilidade | `.inicio/tradutor.md` | Perfil | PASS |
| Inconsistência `traceability-matrix` | `.inicio/tradutor.md` | Perfil | PASS |
| Gates específicos da lista | `.inicio/tradutor.md` | Perfil | PASS |

### Relação de autoridade

```text
tradutor.md (norma genérica)
  ↑
perfil-traducao-agent-list.md (restrições da execução)
  ↑
VALIDACAO-TRADUCAO-AGENT-LIST.md (resultados observados)
```

O núcleo não referencia o perfil nem a evidência. O perfil referencia somente a
norma. A evidência identifica norma e perfil. Não existe ciclo de autoridade.

### Resultado de COR-01

- constantes específicas encontradas no núcleo após a extração: `0`;
- restrições específicas com destino identificado: `9/9`;
- cobertura da matriz origem-destino: `100%`;
- ciclos de referência normativa: `0`;
- resultado: `PASS`.

## 3. COR-02 — Autoridade normativa

### Autoridade selecionada

O arquivo raiz `AGENTS.md` referencia `.inicio/tradutor.md` como autoridade
operacional obrigatória para traduções técnicas ou normativas. Ele também define
a precedência entre norma, perfil e evidência e a política fail-closed.

### Busca de concorrentes

| Verificação | Resultado |
| --- | :---: |
| Outra norma ativa de tradução encontrada | Não |
| Referência externa obrigatória criada | Sim |
| Política de revisão explícita | Sim |
| Links canônicos resolvidos | Sim |
| `tradutor.md` rastreado no índice Git | Sim, após autorização |
| Aprovação documental anexada | Sim, em 2026-08-02 |

### Resultado de COR-02

Em 2026-08-02, a autoridade documental declarou: “AUTORIZADO a ser a norma
operacional obrigatória.” Após essa autorização, os arquivos da norma e de sua
cadeia de evidências foram adicionados explicitamente ao índice Git, sem incluir
mudanças não relacionadas. Resultado de COR-02: `PASS`.
