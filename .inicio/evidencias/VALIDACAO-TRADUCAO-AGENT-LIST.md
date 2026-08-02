# Validação da tradução da lista de agentes

## 1. Escopo e proveniência

| Campo | Valor |
| --- | --- |
| Origem | `.inicio/archs/agent-list-ja.md` |
| Estado da origem | Blob não versionado, removido do worktree após fixação |
| SHA-256 da origem | `6f6014c9ad32e3ec5cea03c3f79d9eddc0cae225dec3e527d36a76ca921d860e` |
| Destino canônico | `.inicio/archs/agent-list.md` |
| Idioma do destino | Português brasileiro (`pt-BR`) |
| Norma aplicada | `.inicio/tradutor.md`, `REG-TRAD-001` |
| Perfil aplicado | `.inicio/archs/perfil-traducao-agent-list.md` |
| Natureza da alteração | Tradução sem alteração normativa |

A origem não possuía entrada no índice do Git. Por isso, a proveniência foi
fixada pelo hash do conteúdo antes da migração. Não há alegação de histórico
Git anterior para esse arquivo.

## 2. Resultado dos gates

| Gate | Resultado | Evidência |
| --- | :---: | --- |
| Fonte de origem fixada | PASS | SHA-256 reproduzido pelo comparador |
| Fonte canônica única | PASS | Somente `.inicio/archs/agent-list.md` existe no worktree |
| Estrutura | PASS | Contagens da origem e do destino idênticas |
| Contratos de agentes | PASS | Tuplas `name`, `model` e fases idênticas |
| Matriz de ownership | PASS | 31 tuplas relacionais idênticas |
| Grafo Mermaid | PASS | Nós, arestas, direções e estilos idênticos |
| Multiplicidade de tokens protegidos | PASS | Comparação com limites lexicais sem divergência |
| Japonês residual no destino | PASS | Zero caracteres japoneses |
| Modalidade e condições | PASS | Revisão direta registrada na seção 5 |
| Conteúdo novo sem origem | PASS | Zero unidades sem correspondência |
| Inconsistências corrigidas silenciosamente | PASS | `traceability-matrix` foi preservado |
| Referências normativas antigas | PASS | Zero links ativos para `agent-list-ja.md` |

## 3. Equivalência estrutural

| Elemento | Origem | Destino | Resultado |
| --- | ---: | ---: | :---: |
| Seções H2 numeradas | 5 | 5 | PASS |
| Subseções H3 de ownership | 12 | 12 | PASS |
| Linhas de agentes | 12 | 12 | PASS |
| Valores formais de `file_type` | 31 | 31 | PASS |
| Pseudolinhas de código e teste | 2 | 2 | PASS |
| Nós Mermaid | 13 | 13 | PASS |
| Arestas Mermaid | 23 | 23 | PASS |
| Linhas de fases | 8 | 8 | PASS |
| Passos do procedimento | 6 | 6 | PASS |

Os separadores horizontais foram normalizados de `---` para `***`. A função
Markdown foi preservada e o ajuste atende ao estilo `MD035` do repositório.

## 4. Rastreabilidade dos contratos

### 4.1 Agentes

| ID | Agente | Modelo | Fases protegidas | Resultado |
| --- | --- | --- | --- | :---: |
| AG-01 | `lead` | `opus` | todas | PASS |
| AG-02 | `srs-writer` | `opus` | `planning` | PASS |
| AG-03 | `architect` | `opus` | `design` | PASS |
| AG-04 | `security-reviewer` | `opus` | `design`, `implementation` | PASS |
| AG-05 | `implementer` | `opus` | `implementation` | PASS |
| AG-06 | `test-engineer` | `sonnet` | `testing` | PASS |
| AG-07 | `review-agent` | `opus` | todas, nos gates | PASS |
| AG-08 | `progress-monitor` | `sonnet` | a partir de `design` | PASS |
| AG-09 | `change-manager` | `sonnet` | a partir de `planning`, após aprovação | PASS |
| AG-10 | `risk-manager` | `sonnet` | a partir de `planning` | PASS |
| AG-11 | `license-checker` | `haiku` | `implementation`, `delivery` | PASS |
| AG-12 | `kotodama-kun` | `haiku` | todas, ao gerar um `Out` | PASS |

### 4.2 Ownership

| IDs | Owner | Quantidade | Relações preservadas | Resultado |
| --- | --- | ---: | --- | :---: |
| OWN-01–OWN-09 | `lead` | 9 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-10–OWN-12 | `srs-writer` | 3 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-13–OWN-18 | `architect` | 6 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-19–OWN-21 | `security-reviewer` | 3 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-22–OWN-25 | `test-engineer` | 4 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-26 | `review-agent` | 1 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-27–OWN-28 | `progress-monitor` | 2 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-29 | `change-manager` | 1 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-30 | `risk-manager` | 1 | `file_type`, diretório, cardinalidade e fase | PASS |
| OWN-31 | `license-checker` | 1 | `file_type`, diretório, cardinalidade e fase | PASS |

As pseudolinhas do `implementer` permanecem associadas a `src/` e `tests/`.
O `kotodama-kun` continua sem possuir `file_type`; casos menores são informados
ao `lead`, e casos graves usam `review` sob ownership do `review-agent`.

### 4.3 Fluxos, fases e procedimento

| Faixa | Cobertura | Resultado |
| --- | --- | :---: |
| FLOW-01–FLOW-23 | 23 de 23 arestas, com origem, destino e artefatos preservados | PASS |
| PHASE-01–PHASE-08 | 8 de 8 fases, agentes e gates preservados | PASS |
| PROC-01–PROC-06 | 6 de 6 passos, na mesma ordem e com as mesmas referências | PASS |

Os três rótulos humanos do Mermaid foram traduzidos de forma controlada. IDs,
topologia, direção, `file_type`, cores e atributos não foram traduzidos.

## 5. Rastreabilidade semântica

| ID | Proposição preservada | Elementos de risco verificados | Resultado |
| --- | --- | --- | :---: |
| META-01 | O documento é a lista única de agentes registrados | Autoridade e obrigação de atualização | PASS |
| META-02 | A lista deriva das seções normativas indicadas | Links e referências de seção | PASS |
| META-03 | Prompts e convenção estrutural continuam relacionados | Caminhos e escopo da relação | PASS |
| NOTE-01 | Cada `file_type` possui exatamente um `owner` | Quantificador “exatamente um” | PASS |
| NOTE-02 | Código e testes não são gerenciados pelo Common Block | Negação e exceção de escopo | PASS |
| NOTE-03 | `traceability-matrix` gerencia a rastreabilidade | Inconsistência original preservada | PASS |
| NOTE-04 | `kotodama-kun` não possui `file_type` | Negação e ownership emprestado | PASS |
| NOTE-05 | Cores representam a progressão das fases | Ordem e agrupamentos cromáticos | PASS |
| NOTE-06 | O mapa determina quais agentes iniciam em cada fase | Agentes, fases e gates | PASS |

A revisão direta preservou sujeito, predicado, objeto, modalidade, polaridade,
quantificador, condição, temporalidade e referências. Em particular:

- “a partir de” permaneceu inclusivo;
- “após a aprovação da especificação” permaneceu como precondição;
- “condicional” não foi convertido em obrigatório;
- “todas as fases” permaneceu universal;
- `SCA クリア` foi traduzido como “SCA aprovada”, preservando a superação do gate;
- `SLA 達成` foi traduzido como “SLA atingido”, preservando o alcance do nível acordado.

## 6. Comando de comparação

A comparação foi executada contra a cópia temporária imutável da origem, fora
do worktree:

```bash
node /tmp/validate-agent-list-translation.mjs \
  /tmp/cepraea-translation.5DCFN8/agent-list-ja.source.md \
  .inicio/archs/agent-list.md
```

Resultado normalizado:

```text
sourceSha256 = 6f6014c9ad32e3ec5cea03c3f79d9eddc0cae225dec3e527d36a76ca921d860e
h2 = 5/5
h3 = 12/12
agents = 12/12
formal_file_types = 31/31
mermaid_nodes = 13/13
mermaid_edges = 23/23
phases = 8/8
procedure_steps = 6/6
contract_differences = 0
status = PASS
```

## 7. Conclusão

A tradução atende à `REG-TRAD-001`: a estrutura, os identificadores protegidos,
as relações contratuais e as proposições normativas foram preservados. O único
arquivo ativo da lista de agentes é `.inicio/archs/agent-list.md`.
