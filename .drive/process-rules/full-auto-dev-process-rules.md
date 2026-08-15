# Regras de Processo do full-auto-dev

> **Escopo de Aplicação:** Estas regras de processo foram projetadas como um processo abrangente capaz de responder a qualquer desenvolvimento de software, desde projetos de pequena escala, como aplicativos de dados, até sistemas de missão crítica, como SO e sistemas de controle de foguetes. Em projetos de pequena escala, basta omitir os processos desnecessários na fase de setup. Como é difícil adicionar processos posteriormente, adota-se a diretriz de defini-los de forma abrangente desde o início e realizar o scale-down conforme o projeto.

> **Versão Alvo:** Claude Code (Versão mais recente em fevereiro de 2026 — Compatível com Opus 4.6 / Sonnet 4.6)
> **Pré-requisitos:** Assinatura Claude Pro/Team/Enterprise ou conta de API Anthropic
> **Posicionamento deste Documento:** Regras de processo do framework full-auto-dev. Estruturado com base nas funcionalidades oficiais do Claude Code, mas inclui recursos experimentais como Agent Teams. Certifique-se de consultar a documentação oficial (https://code.claude.com/docs/en/overview) para obter as especificações mais recentes.
> **Documento Relacionado:** [Regras de Gestão de Documentos](full-auto-dev-document-rules-ja.md) v0.0.0 — Regras de gestão de documentos como nomeação de arquivos, estrutura de blocos e versionamento. Programado para ser promovido a v1.0.0 após a conclusão do PoC.

---

## Sumário

**Parte 1: Visão Geral**

- [Capítulo 1 Visão Geral e Filosofia Fundamental](#第1章-概要と基本思想)
  - 1.1 Objetivo deste Manual
  - 1.2 Arquitetura Geral
  - 1.3 Principais Funcionalidades do Claude Code Assumidas
- [Capítulo 2 Visão Geral das Fases de Desenvolvimento](#第2章-開発フェーズの全体像)
  - 2.1 Definição dos Nomes das Fases
  - 2.2 Fluxo das Fases de Desenvolvimento
- [Capítulo 3 Framework de Gestão de Processos](#第3章-プロセス管理フレームワーク)
  - 3.1 Visão Geral das Categorias de Processos
  - 3.2 Processos Obrigatórios (Comuns a Todos os Projetos)
  - 3.3 Processos Recomendados (Médio Porte ou Superior)
  - 3.4 Crio de Decisão e Momento de Avaliação dos Processos Condicionais

**Parte 2: Detalhes das Fases**

- [Capítulo 4 Workflow de Desenvolvimento](#第4章-開発ワークフロー)
  - 4.1 Fase setup: Avaliação de Processos Condicionais (Obrigatório)
  - 4.2 Fase planning: Planejamento — Da Entrevista à Criação dos Ch1-2 das Especificações
  - 4.3 Fase dependency-selection: Seleção de Dependências Externas — Avaliação, Seleção e Aquisição (Condicional)
  - 4.4 Fase design: Design — Detalhamento dos Ch3-6 das Especificações, Segurança e WBS
  - 4.5 Fase implementation: Implementação — Desenvolvimento Paralelo e Testes
  - 4.6 Fase testing: Testes — Teste de Integração, Teste de Desempenho e Monitoramento de Qualidade
  - 4.7 Fase delivery: Entrega — Implantação, Relatório Final e Teste de Aceitação
  - 4.8 Fase operation: Operação e Manutenção — Gestão de Incidentes, Gestão de Patches e Operação de Monitoramento (Condicional)

**Parte 3: Configuração e Preparação**

- [Capítulo 5 Construção do Ambiente](#第5章-環境構築)
  - 5.1 Instalação do Claude Code
  - 5.2 Extensão do VS Code
  - 5.3 Ativação do Agent Teams
  - 5.4 Configuração do Servidor MCP
  - 5.5 Estrutura de Projeto Recomendada (Versão Completa)
- [Capítulo 6 Design do CLAUDE.md](#第6章-claudemd-の設計プロジェクトの頭脳)
  - 6.1 Template do CLAUDE.md
  - 6.2 Pontos-chave do Design do CLAUDE.md
- [Capítulo 7 Definição de Agentes](#第7章-エージェント定義) (→ [Lista de Agentes](agent-list.md), [Convenções de Estrutura de Prompts](prompt-structure-ja.md), [Glossário](glossary-ja.md))
- [Capítulo 8 Definição de Comandos Personalizados](#第8章-カスタムコマンド定義)
  - 8.1 Comando de Início do Desenvolvimento Totalmente Automático (full-auto-dev)
  - 8.2 Comando de Verificação de Progresso (check-progress)
  - 8.3 Comando de Retrospectiva (retrospective)

**Parte 4: Qualidade e Operação**

- [Capítulo 9 Framework de Gestão da Qualidade](#第9章-品質管理フレームワーク)
  - 9.1 Gates de Revisão em Estágios
  - 9.2 Perspectivas de Revisão (R1 a R6)
  - 9.3 Tabela de Critérios de Qualidade
- [Capítulo 10 Modo Headless e Integração CI/CD](#第10章-ヘッドレスモードとcicd連携)
  - 10.1 Básico do Modo Headless
  - 10.2 Integração com GitHub Actions
- [Capítulo 11 Implantação e Observabilidade](#第11章-デプロイメントと可観測性)
  - 11.1 Processo de Implantação
  - 11.2 Design de Observabilidade
  - 11.3 Checklist de Lançamento em Produção
  - 11.4 Monitoramento e Resposta a Incidentes na Fase de Operação

**Parte 5: Materiais de Referência**

- [Capítulo 12 Resolução de Problemas](#第12章-トラブルシューティング)
  - 12.1 Problemas Comuns e Soluções
  - 12.2 Diretrizes de Gestão de Custos
- [Capítulo 13 Boas Práticas e Precauções](#第13章-ベストプラクティスと注意事項)
  - 13.1 Boas Práticas
  - 13.2 Precauções e Restrições
- [Capítulo 14 Tutorial Prático](#第14章-実践チュートリアルほぼ全自動でwebアプリを開発する)
  - 14.1 a 14.6 Passos para Desenvolvimento de Web App de Gestão de Tarefas

**Apêndices**

- [Apêndice A: Diagrama de Comunicação entre Agentes](#付録a-エージェント間コミュニケーション図)
- [Apêndice B: Schema dos Dados de Gestão de Progresso](#付録b-進捗管理データのスキーマ)
- [Apêndice C: Referência Rápida](#付録c-クイックリファレンス)

---

# Parte 1: Visão Geral

## Capítulo 1 Visão Geral e Filosofia Fundamental

### 1.1 Objetivo deste Manual

Este manual é um guia prático para automatizar quase totalmente o processo de desenvolvimento de software utilizando o Claude Code. 
"Quase totalmente automático" refere-se a uma abordagem na qual o trabalho do ser humano (usuário) é limitado às três tarefas 
importantes a seguir, delegando todas as outras etapas ao Claude Code e ao seu grupo de subagentes.

**Tarefas sob responsabilidade do usuário (apenas 3):**

1. Apresentação da necessidade e do conceito do SW (o que deseja criar)
2. Decisões importantes necessárias ao desenvolvimento do SW (tomada de decisão nos pontos de ramificação)
3. Teste de aceitação final do SW (confirmação e aprovação do produto concluído)

**Tarefas sob responsabilidade do Claude Code (todas as outras):**

- Elaboração do plano de desenvolvimento (WBS/Gráfico de Gantt), gestão de pessoal (AI), gestão de recursos, gestão de progresso
- Criação de especificações (Ch1-2: Foundation/Requirements; formato selecionado entre ANMS/ANPS/ANGS), design de segurança, detalhamento das especificações (Ch3-6: Architecture/Specification/Test Strategy/Design Principles)
- Implementação do SW, testes unitários de módulos, testes de integração, testes de sistema, testes de desempenho
- Monitoramento da curva de execução de testes, monitoramento da curva de defeitos (defect curve)
- Adição de recursos/pessoal (AI) a gargalos/áreas frágeis
- Revisões em estágios de cada entregável (incluindo princípios de engenharia de SW, concorrência e desempenho)
- Gestão de mudanças, gestão de riscos, verificação de licenças, gestão de registros de auditoria
- Geração de documentação de API, varreduras de segurança SAST/SCA
- Build de contêineres, configuração IaC, implantação, testes de fumaça (smoke test)
- Verificação das configurações de observabilidade (logs, métricas, alertas)
- Todas as outras tarefas possíveis de serem executadas por AI

### 1.2 Arquitetura Geral

**Visão Geral do Desenvolvimento Totalmente Automático:**

```mermaid
flowchart TB
    subgraph Human["Usuário (Humano)"]
        H1["Apresentação do Conceito"]
        H2["Decisões Importantes"]
        H3["Teste de Aceitação"]
    end

    subgraph ClaudeCode["Camada de Orquestração do Claude Code"]
        Lead["Agente Líder<br/>Opus 4.6"]
        Plan["Subagente Plan"]
        Explore["Subagente Explore"]
    end

    subgraph AgentTeam["Camada de Execução Agent Teams"]
        SRS_Agent["srs-writer<br/>Criação de Especificações"]
        Arch_Agent["architect<br/>Design"]
        Sec_Agent["security-reviewer<br/>Segurança"]
        Impl_Agent["implementer<br/>Implementação"]
        Test_Agent["test-engineer<br/>Testes"]
        Review_Agent["review-agent<br/>Revisão"]
        PM_Agent["progress-monitor<br/>Gestão de Progresso"]
        Change_Agent["change-manager<br/>Gestão de Mudanças"]
        Risk_Agent["risk-manager<br/>Gestão de Riscos"]
        License_Agent["license-checker<br/>Licenças"]
        Koto_Agent["kotodama-kun<br/>Verificação de Termos"]
    end

    subgraph Tools["Integração com Ferramentas Externas MCP"]
        Git["Git/GitHub"]
        Jira["Jira/Gestão de Tarefas"]
        Docs["Google Docs"]
        Slack["Notificação Slack"]
    end

    H1 -->|"1 Entrada do Conceito"| Lead
    Lead -->|"2 Solicitação de Elaboração de Plano"| Plan
    Plan -->|"3 Solicitação de Aprovação do Plano"| H2
    H2 -->|"4 Instrução de Aprovação/Modificação"| Lead
    Lead -->|"5 Distribuição de Tarefas"| AgentTeam
    SRS_Agent -->|"6 Criação dos Ch1-2 das Especificações"| Arch_Agent
    Arch_Agent -->|"7 Detalhamento dos Ch3-6 / Comunicação do Design"| Impl_Agent
    Sec_Agent -->|"8 Requisitos de Segurança"| Impl_Agent
    Impl_Agent -->|"9 Submissão de Código"| Test_Agent
    Test_Agent -->|"10 Resultado dos Testes"| Review_Agent
    Review_Agent -->|"11 Relatório de Qualidade"| PM_Agent
    PM_Agent -->|"12 Relatório de Progresso"| Lead
    Lead -->|"13 Relatório de Conclusão"| H3
    AgentTeam -->|"14 Uso de Ferramentas"| Tools
    Explore -->|"15 Investigação da Base de Código"| Lead