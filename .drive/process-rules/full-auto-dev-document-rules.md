# Regras de Gerenciamento de Documentos full-auto-dev v0.0.0

## Version 0.0.0 | Date: 2026-03-15

> \*\*Status:\*\* Pre-release (antes da PoC). Será promovida para v1.0.0 após a conclusão da PoC.

\---

## 1\. Visão Geral



Este documento define as regras de nomenclatura, estrutura, versionamento e propriedade de todos os arquivos sob o framework full-auto-dev.

Todos os agentes **DEVEM** (MUST) seguir estas regras ao criar ou atualizar arquivos gerenciados.

Independentemente do formato de especificação (ANMS / ANPS / ANGS) utilizado pelo processo, o formato de gerenciamento de documentos definido aqui (Common Block, Form Block, etc.) aplica-se a todos os documentos gerenciados.

**Documentos relacionados:** [Regras do Processo](full-auto-dev-process-rules-ja.md) — Regras de processo, como definição de fases, definição de agentes e controle de qualidade.



### 1.1 Versionamento deste documento

A versão deste próprio documento é gerenciada no formato **MAJOR.MINOR.PATCH**.

|Nível|Alvo da Alteração|Escopo de Impacto|Reutilização de Arquivos Existentes|
|-|-|-|:-:|
|**MAJOR**|Alteração estrutural do Common Block / Footer|Todos os arquivos gerenciados|Migração necessária para todos os arquivos|
|**MINOR**|Alteração/adição de Form Block|Apenas arquivos do tipo correspondente|Confirmação necessária apenas para o tipo correspondente|
|**PATCH**|Detail Block Guidance / Correção de texto|Sem impacto|Pode ser usado como está|

A `doc:schema\_version` dos arquivos gerenciados registrará o **MAJOR.MINOR** deste documento (PATCH é omitido).

**Status de Lançamento:**

|Versão|Condição|Significado|
|-|-|-|
|0.x.x|Antes da PoC|Fase de design. Pode ser alterado livremente, incluindo o Common Block|
|1.0.0|PoC concluída e verificada|Versão oficial. Alterações MAJOR requerem um guia de migração|

### 

### 1.2 Regras de revisão das convenções do framework



Regras de revisão aplicáveis a todos os arquivos sob `process-rules/` (incluindo este documento).

**Arquivos alvo:**

|Arquivo|Conteúdo|
|-|-|
|full-auto-dev-process-rules-ja.md|Regras do processo|
|full-auto-dev-document-rules-ja.md|Regras de gerenciamento de documentos (este documento)|
|review-standards-ja.md|Convenções de pontos de revisão|
|prompt-structure-ja.md|Convenções de estrutura de prompt|
|agent-list.md|Lista de agentes (Português do Brasil, única fonte de verdade)|
|glossary-ja.md|Glossário|
|defect-taxonomy-ja.md|Taxonomia de termos de defeitos (cadeia causal, fault origin, termos de segurança funcional)|
|spec-template-ja.md|Modelo de especificações|



**Classificação da Revisão:**



|Classificação|Conteúdo da Alteração|Aprovação|Análise de Impacto|
|-|-|:-:|-|
|**Breaking**|Alteração estrutural (adição/remoção/renomeação de seções, campos, namespaces)|Aprovação do usuário obrigatória|Listar todos os arquivos afetados|
|**Non-breaking**|Correção/esclarecimento de conteúdo (manutenção da estrutura existente)|Apenas notificação ao usuário|Desnecessária|
|**Additive**|Nova adição (novo file\_type, novo agente, novo termo)|Apenas notificação ao usuário|Sem impacto nos existentes|



**Procedimento de Revisão:**



1. Identificar o conteúdo da alteração.
2. Determinar a classificação (Breaking / Non-breaking / Additive).
3. No caso de Breaking:

   * Listar os arquivos afetados (convenções, prompts de agente, artefatos do projeto).
   * Relatar o conteúdo da alteração e o impacto ao usuário, solicitando aprovação.
   * Após a aprovação, alterar as convenções.
   * Atualizar os arquivos afetados.
4. No caso de Non-breaking / Additive:

   * Alterar as convenções.
   * Relatar o conteúdo da alteração ao usuário.



**Gerenciamento de histórico:** O histórico de revisão das convenções do framework é gerenciado via Git.
Como os arquivos de convenção não estão sujeitos ao Common Block, o uso de Footer / change\_log não é necessário.

\---

## 2\. Estrutura de Diretórios

**Repositório do Framework:**

```text
{framework-root}/
  README.md                    # Visão geral do repositório
  process-rules/               # Regras de operação (definição do framework)
    full-auto-dev-process-rules-ja.md
    full-auto-dev-process-rules-en.md
    full-auto-dev-document-rules-ja.md   # ← Este documento
    full-auto-dev-document-rules-en.md
    agent-list.md                        # Lista de agentes (pt-BR, única fonte de verdade)
    prompt-structure-ja.md               # Convenções de estrutura de prompt
    prompt-structure-en.md
    glossary-ja.md                       # Glossário
    glossary-en.md
    review-standards-ja.md               # Convenções de pontos de revisão (R1\~R6)
    review-standards-en.md
    spec-template-ja.md                  # Modelo de especificações
    spec-template-en.md
  essays/                      # Artigos/Pesquisa (JP/EN)
  .claude/commands/            # Definição de comandos personalizados

