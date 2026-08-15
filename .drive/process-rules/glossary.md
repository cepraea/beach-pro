# Glossário

> **Posicionamento deste Documento:** Definição dos termos utilizados no framework full-auto-dev. Não inclui termos gerais de dicionário. Registra os significados específicos do framework, motivos de seleção e alternativas não adotadas.
> **Documentos Relacionados:** [Regras de Processo](full-auto-dev-process-rules-ja.md), [Regras de Gestão de Documentos](full-auto-dev-document-rules-ja.md), [Lista de Agentes](agent-list-ja.md), [Taxonomia de Falhas](defect-taxonomy-ja.md)

***

## 1. Termos Selecionados Intencionalmente

Termos escolhidos intencionalmente entre múltiplos sinônimos. As alternativas não adotadas e os motivos estão registrados.

| Termo | Inglês | Definição | Alternativa Não Adotada | Motivo |
| --- | --- | --- | --- | --- |
| Requisito | requirement | Condição que o sistema deve satisfazer. Formalizado com a sintaxe EARS | Condição Necessária | O requisito é a raiz (o que se busca). A condição necessária é derivada (condição a satisfazer). Padronizado como Requirements = Requisito |
| Entrevista | interview | Extração de requisitos através de perguntas estruturadas ao usuário | Hearing | Hearing é um termo do inglês japonês (Wasei-eigo). Em inglês, significa audiência judicial ou audição |
| status | status | Valor indicando a posição atual no fluxo de trabalho (workflow) | state | A distinção entre state (modo de existência) e status (posição de progresso) é desnecessária na prática. Padronizado como status |
| error | error | Erro humano de percepção, julgamento ou operação. Causa do fault (IEEE 1044). Detalhes em [defect-taxonomy](defect-taxonomy.md) | Equívoco | Padronizado no termo em inglês. A palavra "equívoco" é cotidiana e tem baixa precisão técnica |
| fault | fault | Estado incorreto latente no código/design/especificação como resultado de um error. Não se manifesta até ser descoberto (IEEE 1044, IEC 61508) | Falha latente, Defeito | Padronizado no termo em inglês. Termos transliterados não foram adotados |
| failure | failure | Evento onde um fault se manifesta em tempo de execução e não atende mais aos requisitos (IEEE 1044, IEC 61508) | Pane, Avaria, Falha | "Avaria" é mais voltado a HW; "falha" é ambíguo. Padronizado no termo em inglês |
| defect | defect | Registro formal de um failure (ou fault) descoberto durante testes/operação (file_type). Cadeia causal: error -> fault -> failure -> defect | Obstáculo, bug, Problema | "Obstáculo" funde-se com failure/incident e foi abolido. Padronizado no termo em inglês |
| incident | incident | Evento não planejado que afeta o serviço em ambiente de produção (ITIL, ISO 20000). file_type: incident-report | Interrupção, Incidente | Padronizado no termo em inglês. Termos transliterados não foram adotados |
| hazard | hazard | Fonte de perigo onde um failure pode causar danos à vida, propriedade ou meio ambiente (IEC 61508). Usado quando o processo condicional "Segurança Funcional" está ativo | Perigo | Padronizado no termo em inglês |
| fault origin | fault origin | Fase em que o fault foi introduzido. Dividido em 3: requirements fault / design fault / implementation fault (IEEE 1044). Usado em root cause analysis de defect | — | Eixo de classificação para identificar a origem do fault na cadeia causal |
| HARA | HARA | Hazard Analysis and Risk Assessment (ISO 26262). Método para identificar hazard em nível de sistema e derivar safety goals. Obrigatório quando a Segurança Funcional está ativa | — | Análise top-down. Detalhes em [defect-taxonomy §7](defect-taxonomy.md) |
| FMEA | FMEA | Failure Mode and Effects Analysis (IEC 60812). Método de análise exaustiva de modos de fault e seus impactos em nível de componente | — | Análise bottom-up. Executado após a fixação do Ch3 |
| FTA | FTA | Fault Tree Analysis (IEC 61025). Método que busca causas de trás para frente usando portas AND/OR a partir de um top event específico | — | Análise top-down. Usada para análise de causas de hazard de alto risco ou incident graves |
| interview-record | Registro de Entrevista | Registro estruturado da entrevista com o usuário (file_type) | hearing-record | Vinculado à escolha de interview acima |
| disaster-recovery-plan | Plano de Recuperação de Desastres | Definição de procedimentos de recuperação baseados em RPO/RTO (file_type) | dr-plan | Segue a regra de proibição de abreviações no namespace |

## 2. Conceitos Específicos do Framework

Conceitos não encontrados em dicionários e definidos neste framework.

| Termo | Definição |
| --- | --- |
| STFB | Stable Top, Flexible Bottom (Topo Estável, Base Flexível). Estrutura de capítulos da especificação baseada no princípio de dependências estáveis. Os capítulos superiores são estáveis/abstratos e os inferiores são mutáveis/concretos |
| ANMS | AI-Native Minimal Spec. Formato de especificação em arquivo Markdown único. Para projetos que cabem em uma janela de contexto |
| ANPS | AI-Native Plural Spec. Formato com múltiplos arquivos Markdown + Common Block. Para projetos de médio porte |
| ANGS | AI-Native Graph Spec. Formato com GraphDB + Git. Para grandes projetos. O MD é apenas uma view (visão) |
| Common Block | Bloco de metadados comum a todos os file_types. Prova de identidade do arquivo (identificação, estado, workflow, contexto, origem) |
| Form Block | Bloco de campos estruturados específico de um file_type. Os agentes realizam parsing para tomar decisões e agir |
| Detail Block | Zona de explicações detalhadas. O núcleo do conhecimento de domínio. Lido por humanos e agentes para compreensão |
| Footer | Bloco de histórico de atualizações. Tipo append-only (só acréscimos). Usado para auditoria |
| In | Entrada do agente. Arquivos que existem no início do trabalho. Imutáveis (apenas leitura) |
| Out | Saída do agente. Entregável final ao concluir o trabalho. Corresponde às End Conditions. Torna-se o In do próximo agente |
| Work | Arquivos temporários de trabalho do agente. Excluídos após a conclusão do Out. Não são reutilizados |

## 3. Critérios de Permissão para Abreviações

Registros de decisões sobre o uso de abreviações em namespaces (nomes de file_type). Regra geral: abreviações proibidas (document-rules §7).

| Abreviação | Nome Oficial | Avaliação | Motivo |
| --- | --- | :---: | --- |
| WBS | Work Breakdown Structure | Permitido | Termo geral de PM. Ninguém escreve "Work Breakdown Structure" por extenso |
| SRS | Software Requirements Specification | Permitido apenas em nomes de agentes | `srs-writer` é um nome de agente (não se aplica à regra de namespace). Proibido em namespaces |
| DR | Disaster Recovery | Não Permitido | Renomeado para `disaster-recovery-plan`. Está dentro do limite de 3 palavras |
| CR | Change Request | Não Permitido | Renomeado para o campo `change_request_status` |
| HW | Hardware | Permitido | Usado no file_type `hw-requirement-spec`. `hardware-requirement-spec` tem 4 palavras e excede o limite |
| AI | Artificial Intelligence | Permitido | Termo geral. Usado em `ai-requirement-spec` |
| FW | Framework | Não Permitido | `framework-requirement-spec` possui 3 palavras e está no limite. Não necessita de abreviação |

## 4. Distinção de Pares Confusos

Distinção clara entre conceitos similares, porém diferentes.

| Par | Distinção |
| --- | --- |
| Requisito vs Solicitação de Mudança | Requisito = requirement (condições a serem atendidas). Solicitação de Mudança = change request (pedido iniciado pelo usuário pós-aprovação). Em inglês diferem como requirement vs request |
| Especificação vs Template | Especificação = Entregável específico do projeto (docs/spec/). Template = Modelo fornecido pelo framework (process-rules/spec-template.md) |
| Agente vs Subagente | Agente = As 12 definições de papéis cadastradas na agent-list. Subagente = Processo filho iniciado pelo Claude Code (pode incluir agentes) |
| lead vs organizer | lead = Agente orquestrador definido nas regras de processo. organizer = Agente de travessia de grafos proposto no paper ANGS. Atualmente, referem-se ao mesmo papel em contextos diferentes |
| document_status vs {type}_status | Mesma palavra status. document_status = Common Block (ciclo de vida do documento: draft/review/approved/archived). {type}_status = Form Block (posição no workflow específico do domínio) |
| fault vs defect | fault = Estado incorreto latente no código (não descoberto). defect = Ficha de problema formal documentada após descoberta (file_type). Um fault descoberto gera um defect |
| failure vs incident | failure = Evento técnico onde os requisitos não são atendidos (inclusive durante testes). incident = Evento operacional onde um failure afetou o serviço em produção. Failures em testes não são incidents |
| defect vs incident | defect = Registro de descoberta durante teste/desenvolvimento (file_type: defect, dono: test-engineer). incident = Registro de ocorrência em produção (file_type: incident-report, dono: lead). Fases diferentes |
| hazard vs risk | hazard = Fonte de perigo à vida e propriedades (IEC 61508). risk = Impacto sobre os objetivos do projeto (file_type: risk). Hazard é específico de Segurança Funcional; Risk aplica-se a todos os projetos |