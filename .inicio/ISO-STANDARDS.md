# Relação entre normas de sistemas, software, requisitos e documentação

## 1. Finalidade

Este resumo situa quatro normas usadas no conteúdo original. Ele não reproduz o texto normativo e não substitui a consulta às publicações oficiais.

Situação consultada em 2026-07-23:

| Norma | Função resumida | Edição publicada consultada |
| --- | --- | --- |
| ISO/IEC/IEEE 15288 | Processos do ciclo de vida de sistemas. | 2023 |
| ISO/IEC/IEEE 12207 | Processos do ciclo de vida de software. | 2017 |
| ISO/IEC/IEEE 29148 | Engenharia de requisitos. | 2018 |
| ISO/IEC/IEEE 15289 | Conteúdo de itens de informação do ciclo de vida. | 2019 |

Antes de usar essas edições como base contratual ou de conformidade, confirme o status atual nas fontes oficiais.

## 2. Relação conceitual

```text
15288
processos do ciclo de vida do sistema
        │
        ├── 29148
        │   especializa processos e informações de requisitos
        │
        └── 15289
            organiza itens de informação do ciclo de vida

12207
processos do ciclo de vida do software
        │
        ├── 29148
        │   especializa requisitos de software
        │
        └── 15289
            organiza itens de informação do ciclo de vida
```

### 2.1 ISO/IEC/IEEE 15288

Define um conjunto comum de processos e terminologia para o ciclo de vida de sistemas. Os processos podem ser selecionados e adaptados ao sistema de interesse e aos elementos do sistema.

A norma não prescreve uma metodologia específica e remete à 15289 para o conteúdo dos itens de informação.

### 2.2 ISO/IEC/IEEE 12207

Define processos do ciclo de vida de software. É aplicável quando o objeto de interesse é um produto ou elemento de software e pode ser combinada com a 15288 em sistemas intensivos em software.

### 2.3 ISO/IEC/IEEE 29148

Especializa a engenharia de requisitos. Conforme o resumo oficial, ela:

- especifica processos que produzem requisitos de sistemas e software;
- orienta a aplicação de processos relacionados a requisitos da 15288 e da 12207;
- especifica itens de informação e conteúdos exigidos para requisitos;
- orienta a apresentação desses itens.

Um requisito controlável deve possuir identidade, origem, texto vigente, atributos relevantes, método de verificação e relações de rastreabilidade.

### 2.4 ISO/IEC/IEEE 15289

Trata do conteúdo de itens de informação produzidos por processos de ciclo de vida. Um item de informação é uma unidade semântica; ele não precisa corresponder a um único arquivo.

Exemplos de representações possíveis:

- documento Markdown;
- registro em ferramenta ALM;
- estrutura JSON ou YAML;
- planilha controlada;
- seção identificada de uma especificação.

## 3. Distinções necessárias

### 3.1 Sistema e software

Software pode ser um elemento de um sistema que também contém pessoas, hardware, serviços, procedimentos e interfaces.

### 3.2 Processo e documento

Processo é trabalho executado. Documento ou registro preserva informação produzida ou utilizada pelo processo.

### 3.3 Necessidade, requisito e solução

```text
necessidade
    ↓ análise
requisito verificável
    ↓ projeto
arquitetura e solução
    ↓ implementação
produto e evidência
```

Misturar essas camadas pode transformar uma preferência de solução em requisito sem justificativa.

### 3.4 Verificação e validação

- **Verificação:** o resultado corresponde à especificação?
- **Validação:** o resultado satisfaz a necessidade no contexto de uso?

## 4. Aplicação documental para agentes

Um agente não deveria receber apenas uma solicitação isolada quando a tarefa depende de controle de ciclo de vida. O contexto pode referenciar:

```yaml
work_context:
  system_processes:
    source: ISO/IEC/IEEE 15288
  software_processes:
    source: ISO/IEC/IEEE 12207
  requirements:
    source: ISO/IEC/IEEE 29148
    items:
      - SYSTEM_REQUIREMENTS.md
      - SOFTWARE_REQUIREMENTS.md
  lifecycle_information:
    source: ISO/IEC/IEEE 15289
    items:
      - ARCHITECTURE.md
      - TEST_STRATEGY.md
      - DECISION_LOG.md
```

As referências indicam a origem conceitual. A organização ainda precisa definir quais itens são obrigatórios, quem os aprova e quais versões normativas foram adotadas.

## 5. Fontes oficiais

- [ISO/IEC/IEEE 15288:2023](https://www.iso.org/standard/81702.html)
- [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html)
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)
- [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html)

