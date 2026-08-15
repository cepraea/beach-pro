# Guia de Portabilidade: Procedimentos de Adaptação para Outras Plataformas de IA

## Objetivo

Embora este framework (claude-code-full-auto-dev) seja construído sobre o Claude Code, o valor essencial do framework reside nas regras de processo (process-rules/) e na estrutura de prompts (S0-S6). O front matter específico da CLI e a estrutura de diretórios são apenas a "casca", consistindo em diferenças que a IA de destino é capaz de converter por conta própria.

**O público-alvo presumido deste guia é a IA.** Não há necessidade de um humano fazer a conversão manualmente, um por um. Basta fazer com que este guia seja lido na plataforma de IA de destino e instruir a conversão automática. Uma IA que não consegue fazer isso não tem a capacidade de usar este framework.

## Classificação de Arquivos

### Sem necessidade de alteração (Portáteis)

Os itens a seguir independem da plataforma de IA. Use-os como estão:

| Caminho | Conteúdo |
|---|---|
| `docs/` | Especificações e Documentos de Design (Artefatos já gerados) |
| `src/` | Código-fonte |
| `tests/` | Código de teste |
| `infra/` | Código IaC |
| `project-management/` | Progresso / WBS |
| `project-records/` | Registros de revisão, decisões e riscos |
| `process-rules/glossary-ja.md` | Glossário |
| `process-rules/defect-taxonomy-ja.md` | Classificação de Defeitos |
| `process-rules/review-standards.md` | Critérios de Revisão (R1-R6) |
| `process-rules/spec-template-*.md` | Template de Especificação |
| `process-rules/prompt-structure-ja.md` | Convenção de Estrutura de Prompts (S0-S6) |
| `user-order.md` | Requisitos do Usuário (Formato de 3 perguntas) |
| `.mcp.json` | Configurações MCP (Padrão aberto) |

### Resolução por substituição em massa (Nome do fornecedor, nome do modelo, caminhos)

| Arquivo | Alvo da Substituição |
|---|---|
| `process-rules/full-auto-dev-process-rules-ja.md` | "Claude Code", "Agent Teams", Nomes de modelos (Opus/Sonnet/Haiku) |
| `process-rules/full-auto-dev-document-rules-ja.md` | Caminhos de `.claude/agents/`, `.claude/commands/` |
| `process-rules/agent-list.md` | Nomes de modelos na tabela de alocação de modelos |

### Necessidade de conversão de formato

| Tipo | Caminho Atual | Detalhes da Conversão |
|---|---|---|
| Arquivo de instruções do projeto | `CLAUDE.md` | Renomear e mover para o arquivo de instruções da plataforma de destino |
| Definição de Agentes (12 arquivos) | `.claude/agents/*.md` | Converter o front matter (YAML) para o formato de destino. O corpo (S0-S6) é reaproveitado |
| Comandos Personalizados (3 arquivos) | `.claude/commands/*.md` | Converter para o método de execução da plataforma de destino |
| Arquivos de configuração | `.claude/settings*.json` | Criar novos no formato de configuração da plataforma de destino |

## Especificações de Conversão por Plataforma

### Claude Code → OpenAI Codex 

| Item | Claude Code | Codex |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `AGENTS.md` |
| Definição de Agentes | `.claude/agents/*.md` | Integrado em `AGENTS.md` (Agente único) |
| Comandos Personalizados | `.claude/commands/*.md` | Colocado como arquivo de prompt em `prompt/` |
| Configurações | `.claude/settings.json` | Variáveis de ambiente + Argumentos de CLI |
| Especificação de Modelo | `model: opus` | `--model o3` |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Não suportado (Alterado para execução sequencial) |

### Claude Code → Gemini CLI

| Item | Claude Code | Gemini CLI |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `GEMINI.md` |
| Definição de Agentes | `.claude/agents/*.md` | Integrado em `GEMINI.md` |
| Comandos Personalizados | `.claude/commands/*.md` | Colocado como arquivo de prompt em `prompt/` |
| Configurações | `.claude/settings.json` | `.gemini/settings.json` |
| Especificação de Modelo | `model: opus` | `gemini-2.5-pro` |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Não suportado (Alterado para execução sequencial) |

### Claude Code → Cursor

| Item | Claude Code | Cursor |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `.cursor/rules/project.mdc` |
| Definição de Agentes | `.claude/agents/*.md` | Dividido como arquivos de regras em `.cursor/rules/` |
| Comandos Personalizados | `.claude/commands/*.md` | Colocado em Notepads |
| Configurações | `.claude/settings.json` | Tela de configurações da IDE |
| Especificação de Modelo | `model: opus` | Selecionado nas configurações da IDE |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Background Agent (Único) |

### Claude Code → Windsurf

| Item | Claude Code | Windsurf |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `.windsurfrules` |
| Definição de Agentes | `.claude/agents/*.md` | Integrado em `.windsurfrules` |
| Comandos Personalizados | `.claude/commands/*.md` | Integrado no arquivo de regras |
| Configurações | `.claude/settings.json` | Configurações da IDE |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Cascade (Múltiplas etapas internas) |

### Claude Code → Cline

| Item | Claude Code | Cline |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `.clinerules` |
| Definição de Agentes | `.claude/agents/*.md` | `.cline/` + JSON de definição de modo personalizado |
| Comandos Personalizados | `.claude/commands/*.md` | Integrado ao modo personalizado |
| Configurações | `.claude/settings.json` | Configurações da extensão do VSCode |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Não suportado (Substituído por alternância de modo) |

### Claude Code → Roo Code

| Item | Claude Code | Roo Code |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `.roo/rules/project.md` |
| Definição de Agentes | `.claude/agents/*.md` | Regras por modo colocadas em `.roo/rules/` |
| Comandos Personalizados | `.claude/commands/*.md` | Integrado na definição do modo personalizado |
| Configurações | `.claude/settings.json` | Configurações da extensão do VSCode |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Alternância de modo (Pseudo-múltiplos) |

### Claude Code → Aider

| Item | Claude Code | Aider |
|---|---|---|
| Instruções do Projeto | `CLAUDE.md` | `CONVENTIONS.md` |
| Definição de Agentes | `.claude/agents/*.md` | Integrado como descrição de funções em `CONVENTIONS.md` |
| Comandos Personalizados | `.claude/commands/*.md` | Script Shell + Arquivo de prompt |
| Configurações | `.claude/settings.json` | `.aider.conf.yml` |
| Especificação de Modelo | `model: opus` | `model: gpt-4.1` etc. |
| Múltiplos Agentes | Agent Teams (Execução em paralelo) | Não suportado (Alternância manual) |

## Valores Recomendados de Mapeamento de Modelos

Mapeamento recomendado ao substituir as especificações de modelos nas definições de agentes:

| Rank da Função | Claude | OpenAI | Google | Caso de Uso |
|---|---|---|---|---|
| Alto (Decisão/Design) | opus | o3 | gemini-2.5-pro | lead, architect, review-agent, security-reviewer, srs-writer, implementer |
| Médio (Tarefas de Rotina) | sonnet | gpt-4.1 / gpt-4.1-mini | gemini-2.5-flash | test-engineer, progress-monitor, change-manager, risk-manager |
| Baixo (Regras Simples) | haiku | gpt-4.1-mini | gemini-2.5-flash | license-checker, kotodama-kun |

> Os valores recomendados devem ser ajustados através de validações PoC. O equilíbrio entre capacidade, custo e velocidade de cada modelo varia de acordo com a plataforma.

## Procedimento de Portabilidade (Exemplo de instruções para a IA)

Instrua a IA de destino da seguinte maneira: