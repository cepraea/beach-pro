# Perfil de tradução da lista de agentes

> **Tipo:** perfil de execução da norma de tradução.
> **Norma aplicável:** [`REG-TRAD-001`](../tradutor.md#reg-trad-001--preservação-por-congelamento-de-contratos).
> **Escopo:** tradução de `agent-list-ja.md` para `agent-list.md` em português brasileiro.
> **Autoridade:** este perfil restringe a execução, mas não pode alterar ou substituir a norma.

## 1. Proveniência e fonte canônica

| Campo | Valor |
| --- | --- |
| Origem histórica | `.inicio/archs/agent-list-ja.md` |
| Estado da origem | Blob não versionado, fixado antes da remoção do worktree |
| SHA-256 da origem | `6f6014c9ad32e3ec5cea03c3f79d9eddc0cae225dec3e527d36a76ca921d860e` |
| Destino | `.inicio/archs/agent-list.md` |
| Idioma | `pt-BR` |
| Política canônica | Exatamente um `agent-list.md` ativo; nenhuma cópia japonesa ativa |

O hash comprova a identidade do blob usado como origem. Ele não comprova, por
si só, equivalência semântica. A origem deve permanecer recuperável por Git ou
por evidência imutável fora do worktree.

## 2. Inventário estrutural obrigatório

| Elemento | Quantidade |
| --- | ---: |
| Seções H2 numeradas | 5 |
| Subseções H3 de ownership | 12 |
| Agentes | 12 |
| Valores formais de `file_type` | 31 |
| Pseudolinhas de código/teste | 2 |
| Nós Mermaid | 13 |
| Arestas Mermaid | 23 |
| Fases | 8 |
| Passos para adicionar agente | 6 |

Essas quantidades são invariantes deste perfil, não da norma geral.

## 3. Identificadores protegidos

- Agentes: `lead`, `srs-writer`, `architect`, `security-reviewer`,
  `implementer`, `test-engineer`, `review-agent`, `progress-monitor`,
  `change-manager`, `risk-manager`, `license-checker`, `kotodama-kun`.
- Modelos: `opus`, `sonnet`, `haiku`.
- Fases: `setup`, `planning`, `dependency-selection`, `design`,
  `implementation`, `testing`, `delivery`, `operation`.
- Valores de `file_type`: `pipeline-state`, `executive-dashboard`,
  `final-report`, `decision`, `handoff`, `user-manual`, `runbook`,
  `incident-report`, `stakeholder-register`, `user-order`, `interview-record`,
  `spec-foundation`, `spec-architecture`, `observability-design`,
  `hw-requirement-spec`, `ai-requirement-spec`,
  `framework-requirement-spec`, `disaster-recovery-plan`, `threat-model`,
  `security-architecture`, `security-scan-report`, `test-plan`, `defect`,
  `traceability`, `performance-report`, `review`, `progress`, `wbs`,
  `change-request`, `risk`, `license-report`.
- Caminhos: `src/`, `tests/`, `project-management/`, `project-records/...`,
  `docs/...`, `.claude/agents/*.md`.
- Siglas e gates: `R1-R6`, `PASS`, `SCA`, `SLA`, `WBS`, `OSS`, `OpenAPI`.
- Conceitos: `file_type`, `owner`, `Common Block`, `In`, `Out`, `Work`.
- Referências: `§1`, `§2`, `§3`, `§4`, `§7`, `§7.1`, `§11`, `Ch1-2`,
  `Ch3-6`.

O controle deve preservar valor, quantidade, ordem, owner, fase, origem e
destino de aresta, diretório e demais relações; presença isolada não é suficiente.

## 4. Glossário controlado

| Japonês | Português brasileiro | Restrição semântica |
| --- | --- | --- |
| 本文書の位置づけ | Posicionamento deste documento | Preservar autoridade documental |
| 導出元 | Derivado de | Preservar derivação normativa |
| 関連文書 | Documentos relacionados | Não converter em dependência obrigatória |
| 役割 | Função | Responsabilidade do agente |
| 主要フェーズ | Fase principal | Preservar nomes técnicos de fase |
| 全フェーズ | Todas as fases | Quantificador universal |
| 以降 | A partir de | Inclusivo desde a fase indicada |
| 条件付き | Condicional | Não converter em obrigatório |
| 仕様承認後 | Após a aprovação da especificação | Preservar precondição temporal |
| 単 | Único | Cardinalidade exatamente um |
| 連 | Múltiplo | Cardinalidade múltipla permitida |
| ルート | Raiz | Diretório raiz do projeto |
| 用語チェック済 | Terminologia verificada | Verificação concluída antes do fluxo seguinte |
| 用語指摘 | Apontamentos terminológicos | Resultado da verificação, não aprovação |
| 変更要求 | Solicitação de mudança | Não confundir com requisito |
| 品質ゲート | Gate de qualidade | Condição de transição |
| 仕様書承認 | Aprovação da especificação | Aprovação, não mera revisão |
| ユーザー受入 | Aceite do usuário | Aceite formal |
| クリア | Aprovada | Gate superado |
| 達成 | Atingido | Nível acordado alcançado |
| 新規エージェント追加手順 | Procedimento para adicionar um novo agente | Preservar ordem procedural |

## 5. Rastreabilidade exigida

| Prefixo | Unidade | Quantidade esperada |
| --- | --- | ---: |
| `META-*` | Posicionamento e referências | Conforme inventário da origem |
| `AG-*` | Linhas da lista de agentes | 12 |
| `OWN-*` | Relações formais de ownership | 31 |
| `NOTE-*` | Notas normativas | Conforme inventário da origem |
| `FLOW-*` | Arestas Mermaid | 23 |
| `PHASE-*` | Linhas de ativação | 8 |
| `PROC-*` | Passos de inclusão de agente | 6 |

Critério global: cobertura bidirecional de 100%, sem IDs ausentes, duplicados
ou adicionados sem fonte.

## 6. Projeções contratuais

```text
agent|model|phases
file_type|owner|directory|cardinality|phases
edge|source|label|target
phase|agents|quality_gate
procedure_step|position|references
```

A tradução somente é aceita quando a comparação normalizada dessas projeções
produzir diferença vazia.

## 7. Inconsistência conhecida

O original usa `traceability-matrix` em uma nota, enquanto a tabela registra
`traceability`. A tradução deve preservar essa divergência e registrá-la para
uma mudança normativa separada; corrigi-la silenciosamente é proibido.

## 8. Gates do perfil

- inventário estrutural integralmente preservado;
- divergências contratuais iguais a zero;
- cobertura semântica bidirecional de 100%;
- japonês residual no destino igual a zero, salvo exceção justificada;
- links normativos para o nome antigo iguais a zero;
- fontes ativas concorrentes iguais a zero;
- Markdown, links e Mermaid válidos;
- revisão bilíngue aprovada;
- validação do repositório apresentada.
