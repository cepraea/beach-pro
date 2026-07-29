---
document_id: DOC-VAL-REL-AUDITORIA-REQUISITOS-MVP
title: "Auditoria prática dos requisitos para definição do MVP"
document_type: relatorio
version: "0.1.1"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - revisao_do_catalogo
  - preparacao_da_decisao_de_mvp
prohibited_uses:
  - aprovacao_automatica_de_requisitos
  - autorizacao_de_implementacao
  - definicao_automatica_de_d0
---

# Auditoria prática dos requisitos para definição do MVP

## 1. Identificação

| Campo | Valor |
|---|---|
| ID | `DOC-VAL-REL-AUDITORIA-REQUISITOS-MVP` |
| Produto | CEPRAEA BEACH PRO |
| Versão | `0.1.1` |
| Estado | `RASCUNHO` |
| Data | 2026-07-25 |
| Revisão | Correção de domínio: especialista substitui coringa como classificação; coringa é papel tático |
| Responsável pela validade do domínio | Davi Sermenho |
| Catálogo auditado | `DOC-CEPRAEA-REQ-DERIVADOS-V01`, RF-001 a RF-053 |
| Contexto vigente | `DOC-CEPRAEA-CANDIDATA-CONTEXTO`, versão 0.1 |
| Contexto de revisão consultado | `DOC-CEPRAEA-CONTEXTO-TRABALHO-V02`, não vigente |

## 2. Objetivo e limite

O objetivo desta auditoria é descobrir quais requisitos podem seguir para
especificação e implementação sintética, quais devem ser consolidados, quais
exigem esclarecimento documental e quais dependem de decisão de Davi antes da
definição do MVP.

Este relatório:

- não aprova o MVP;
- não aprova individualmente os requisitos;
- não cria a `DEC-019`;
- não define D0;
- não autoriza implementação;
- não autoriza dados reais, piloto ou produção;
- não altera silenciosamente o catálogo RF v0.1.

## 3. Critérios de classificação

- `PRONTO_PARA_IMPLEMENTAR`: intenção funcional suficientemente clara para ser
  decomposta em critérios de aceitação e tarefas técnicas sem nova decisão de
  negócio.
- `CONSOLIDAR`: repete, especializa ou funciona como critério de aceitação de
  outro RF; deve ser preservado na rastreabilidade, mas não tratado como entrega
  independente.
- `ESCLARECER_SEM_DECISAO`: precisa de redação ou limite verificável, derivável
  das decisões já aprovadas sem nova escolha de Davi.
- `DEPENDE_DE_DAVI`: contém alternativa de produto ou regra do domínio que não
  deve ser escolhida tecnicamente pelo agente.
- `GATE_NAO_FUNCIONAL`: não é funcionalidade do MVP; é condição de liberação
  para dados reais ou produção.

`PRONTO_PARA_IMPLEMENTAR` não significa autorização para iniciar código. Indica
apenas que o item não contém uma decisão de produto ainda oculta.

## 4. Resultado executivo

| Classificação | Quantidade | Efeito |
|---|---:|---|
| `PRONTO_PARA_IMPLEMENTAR` | 33 | Pode entrar na decomposição do MVP |
| `CONSOLIDAR` | 11 | Não deve virar entrega ou pergunta separada |
| `ESCLARECER_SEM_DECISAO` | 4 | A equipe técnica pode especificar com base nas decisões existentes |
| `DEPENDE_DE_DAVI` | 4 | Concentra-se em três pontos decisórios reais |
| `GATE_NAO_FUNCIONAL` | 1 | Deve sair da lista funcional e permanecer como gate |
| **Total** | **53** | Catálogo integralmente classificado |

Não foi identificado nenhum RF-001 a RF-053 já aprovado como fase posterior.
Os únicos requisitos formalmente posteriores continuam sendo `RF-P01` a
`RF-P04`. A auditoria, entretanto, identifica a possibilidade de retirar o modo
offline do primeiro recorte implementável; isso depende de Davi porque altera o
escopo anteriormente aprovado.

## 5. Classificação requisito por requisito

| RF | Classificação | Fundamentação e ação |
|---|---|---|
| RF-001 | `ESCLARECER_SEM_DECISAO` | É resultado/épico. Definir o conjunto inicial de perguntas operacionais e as visões que compõem o “estado único”, usando `OBJ-001` e o escopo já aprovado. |
| RF-002 | `CONSOLIDAR` | Critério negativo de RF-001 e RF-022. Preservar como critério de aceitação do fluxo central, não como entrega independente. |
| RF-003 | `PRONTO_PARA_IMPLEMENTAR` | Gestão do ciclo de elenco é necessária e sustentada pelo caso real de retorno de atleta. Acrescentar rastreabilidade direta a `EVID-001`, `CLAIM-006` e `CON-001`. |
| RF-004 | `CONSOLIDAR` | Regra ampla de visibilidade já operacionalizada por RF-007, RF-045 e RF-046. Manter como política transversal de acesso. |
| RF-005 | `PRONTO_PARA_IMPLEMENTAR` | Modelo de solicitação possui campos e autoridade definidos. |
| RF-006 | `PRONTO_PARA_IMPLEMENTAR` | Estados mínimos estão aprovados e semanticamente distintos. |
| RF-007 | `PRONTO_PARA_IMPLEMENTAR` | Regra de autoria e isolamento de resposta é objetiva e testável. |
| RF-008 | `PRONTO_PARA_IMPLEMENTAR` | Justificativa opcional, minimização e proibições estão definidas. |
| RF-009 | `CONSOLIDAR` | Detalha categorias de RF-008 e histórico de RF-010. Tratar como configuração e critérios desses requisitos. |
| RF-010 | `PRONTO_PARA_IMPLEMENTAR` | Autoria, vigência e preservação de versões estão definidos. |
| RF-011 | `PRONTO_PARA_IMPLEMENTAR` | Correção administrativa separada da declaração original está definida. |
| RF-012 | `PRONTO_PARA_IMPLEMENTAR` | Invariante central do domínio; deve orientar o modelo de dados e os testes. |
| RF-013 | `PRONTO_PARA_IMPLEMENTAR` | Define vínculos entre declaração, confirmação e fatos posteriores. |
| RF-014 | `CONSOLIDAR` | É aplicação de RF-012 e RF-013 ao treino. Preservar como cenário de aceitação obrigatório. |
| RF-015 | `PRONTO_PARA_IMPLEMENTAR` | Criação de convocação e autoridade exclusiva de Davi estão claras. |
| RF-016 | `PRONTO_PARA_IMPLEMENTAR` | Respostas, prazo, substituição, cancelamento e histórico estão definidos. |
| RF-017 | `PRONTO_PARA_IMPLEMENTAR` | Consulta da convocação vigente e visibilidade mínima estão definidas. |
| RF-018 | `PRONTO_PARA_IMPLEMENTAR` | Lista prevista de treino e separação de presença real estão definidas. |
| RF-019 | `CONSOLIDAR` | Regra comum de projeção de RF-017 e RF-018. Aplicar como política e critérios de segurança das duas listas. |
| RF-020 | `PRONTO_PARA_IMPLEMENTAR` | Vigência, substituição e histórico de listas são testáveis. |
| RF-021 | `PRONTO_PARA_IMPLEMENTAR` | “Não publicado” e “inexistente” são estados distintos já aprovados. |
| RF-022 | `ESCLARECER_SEM_DECISAO` | É objetivo/corte transversal. Enumerar os tipos obrigatórios cobertos no MVP conforme `DEC-012`, sem inventar novos canais ou assuntos. |
| RF-023 | `PRONTO_PARA_IMPLEMENTAR` | Conteúdo da caixa individual está definido. |
| RF-024 | `ESCLARECER_SEM_DECISAO` | Separar disponibilização, visualização e ciência explícita. Ciência não deve ser inferida da visualização e só deve ser exigida nos tipos que a requerem. |
| RF-025 | `PRONTO_PARA_IMPLEMENTAR` | Painel deriva estados já definidos; “completas” significa cobrir as categorias enumeradas no RF. |
| RF-026 | `PRONTO_PARA_IMPLEMENTAR` | Canal interno e limite do e-mail estão decididos pela arquitetura vigente. |
| RF-027 | `PRONTO_PARA_IMPLEMENTAR` | Compromissos, estado temporal, prazo, responsável e próxima ação estão definidos. Tipos adicionais podem ser configuração reversível. |
| RF-028 | `CONSOLIDAR` | É critério temporal obrigatório de RF-027. |
| RF-029 | `ESCLARECER_SEM_DECISAO` | Definir “crítica” como pendência de fluxo obrigatório com prazo ou ação exigida; não criar escala subjetiva nova. |
| RF-030 | `DEPENDE_DE_DAVI` | Falta definir se o primeiro recorte usa apenas funções amplas ou também posições e sistemas táticos específicos. O agente não deve inventar o modelo esportivo. |
| RF-031 | `PRONTO_PARA_IMPLEMENTAR` | Indicadores são opcionais, descritivos e limitados por proibições objetivas. |
| RF-032 | `CONSOLIDAR` | É invariante de qualidade dos indicadores de RF-031 e da rastreabilidade de RF-033. |
| RF-033 | `PRONTO_PARA_IMPLEMENTAR` | Proveniência e reconstrução do histórico estão suficientemente definidas. |
| RF-034 | `CONSOLIDAR` | Especializa RF-020 e RF-033 para listas; manter como cenário de auditoria. |
| RF-035 | `PRONTO_PARA_IMPLEMENTAR` | É requisito da migração/importação controlada, não sincronização permanente. Pode ser implementado como ferramenta administrativa. |
| RF-036 | `PRONTO_PARA_IMPLEMENTAR` | Eventos mínimos de auditoria de segurança estão enumerados. |
| RF-037 | `PRONTO_PARA_IMPLEMENTAR` | Conta individual e proibições de acesso estão decididas. |
| RF-038 | `PRONTO_PARA_IMPLEMENTAR` | Existem somente os contextos operacionais Davi e atleta. |
| RF-039 | `PRONTO_PARA_IMPLEMENTAR` | MFA privilegiada está decidida; em ambiente sintético pode ser testada sem usuários reais. |
| RF-040 | `PRONTO_PARA_IMPLEMENTAR` | Administração de conta e limites sobre credenciais estão claros. |
| RF-041 | `PRONTO_PARA_IMPLEMENTAR` | Cadastro fechado por convite/administração está decidido. |
| RF-042 | `PRONTO_PARA_IMPLEMENTAR` | Recuperação individual e limite de Davi estão definidos. |
| RF-043 | `DEPENDE_DE_DAVI` | É necessário aprovar os estados do vínculo esportivo e quando cada estado suspende a conta. Saída temporária, afastamento e desligamento definitivo não devem ser tratados automaticamente como equivalentes. |
| RF-044 | `CONSOLIDAR` | Proibição de impersonação é critério de RF-037, RF-040 e RF-045. |
| RF-045 | `PRONTO_PARA_IMPLEMENTAR` | RLS e testes negativos estão explicitamente decididos. |
| RF-046 | `PRONTO_PARA_IMPLEMENTAR` | Restrição de justificativas possui sujeitos e destinos proibidos definidos. |
| RF-047 | `CONSOLIDAR` | Repete a proibição de inferência de RF-031 e a proteção de RF-046. Manter como teste negativo transversal. |
| RF-048 | `PRONTO_PARA_IMPLEMENTAR` | Independência de IA externa e proibição de dados reais estão definidas. |
| RF-049 | `PRONTO_PARA_IMPLEMENTAR` | Área e canal de direitos são implementáveis; conteúdo jurídico final continua condicionado ao gate de dados reais. |
| RF-050 | `GATE_NAO_FUNCIONAL` | Não descreve comportamento de usuário isolado. Reclassificar como gate de privacidade anterior a dados reais/produção, preservando todos os controles. |
| RF-051 | `DEPENDE_DE_DAVI` | A leitura offline foi aprovada para a primeira fase, mas o snapshot foi definido como opcional e adiciona custo relevante. Davi deve confirmar inclusão ou adiamento no MVP. |
| RF-052 | `CONSOLIDAR` | É critério de segurança de RF-051. Se RF-051 for adiado, permanece como regra futura; se incluído, é obrigatório. |
| RF-053 | `DEPENDE_DE_DAVI` | Depende da mesma decisão de recorte offline de RF-051. Se incluído, criptografia, vínculo ao dispositivo e eliminação são obrigatórios; não há versão simplificada com dados pessoais. |

## 6. Consolidações recomendadas

As consolidações reduzem 53 linhas para unidades implementáveis sem perder
rastreabilidade:

| Unidade | RFs preservados |
|---|---|
| Estado operacional e independência das fontes | RF-001, RF-002 e RF-022 |
| Autorização e isolamento por atleta | RF-004, RF-007, RF-045 e RF-046 |
| Justificativa e histórico de resposta | RF-008, RF-009 e RF-010 |
| Declaração e fatos posteriores | RF-012, RF-013 e RF-014 |
| Listas com visibilidade mínima | RF-017, RF-018 e RF-019 |
| Compromisso vigente | RF-027 e RF-028 |
| Indicadores derivados de fatos | RF-031 e RF-032 |
| Histórico de listas | RF-020, RF-033 e RF-034 |
| Identidade sem impersonação | RF-037, RF-040, RF-044 e RF-045 |
| Proibição de julgamento e exposição | RF-031, RF-046 e RF-047 |
| Offline seguro | RF-051, RF-052 e RF-053 |

Consolidar não significa apagar identificadores. Os RFs continuam como fontes de
critérios e rastreabilidade, mas não devem gerar histórias, componentes ou
estimativas duplicadas.

## 7. Esclarecimentos que não precisam chegar a Davi

Os seguintes esclarecimentos são derivados de decisões já aprovadas e podem ser
resolvidos durante a especificação:

1. RF-001 — enumerar as perguntas operacionais do painel a partir dos fluxos do
   MVP.
2. RF-022 — enumerar solicitações, orientações, convocações, prazos e pendências
   como comunicação obrigatória.
3. RF-024 — visualização é evento técnico; ciência é ação explícita quando
   exigida pelo tipo de comunicação.
4. RF-029 — pendência crítica é a que possui prazo ou ação obrigatória dentro do
   fluxo aprovado.
5. RF-050 — mover para o checklist do gate de dados reais/produção.
6. Acrescentar a RF-003 a origem direta do caso de retorno de atleta, sem
   registrar motivo pessoal desnecessário.

Nomes internos, componentes, organização de pastas, tabelas técnicas e
sequenciamento de tarefas permanecem decisões técnicas reversíveis.

## 8. Pontos decisórios reais para Davi

Os quatro RFs classificados como `DEPENDE_DE_DAVI` formam apenas três escolhas:

### PD-001 — Profundidade da cobertura tática no MVP

- **Afeta:** RF-030.
- **Escolha:** cobertura apenas por funções amplas já documentadas ou também por
  posições e sistemas táticos específicos.
- **Recomendação LEAN:** começar com funções amplas e adiar posições/sistemas
  específicos até que o vocabulário esportivo seja validado.
- **Correção confirmada por Davi:** usar especialista, não coringa, na
  classificação ampla. Coringa é papel tático do jogo e não posição.

### PD-002 — Estados do vínculo da atleta e efeito sobre a conta

- **Afeta:** RF-003 e RF-043.
- **Escolha:** quais estados distinguem atleta ativa, temporariamente afastada,
  desligada e retornando; quais deles suspendem acesso.
- **Recomendação LEAN:** preservar uma única identidade e histórico; permitir
  reativação sem duplicidade; suspender a conta apenas quando o vínculo não
  autorizar acesso. O estado exato continua sendo decisão de domínio de Davi.

### PD-003 — Offline no primeiro recorte implementável

- **Afeta:** RF-051, RF-052 e RF-053.
- **Escolha:** implementar já o snapshot offline criptografado ou adiar todo o
  acesso offline a dados para uma entrega posterior.
- **Recomendação LEAN:** adiar o snapshot de dados e manter apenas o
  comportamento instalável/online da PWA no MVP. Se Davi mantiver offline no
  MVP, RF-052 e RF-053 tornam-se obrigatórios integralmente.

Esses pontos podem ser incorporados à futura decisão de recorte do MVP. Não é
necessário abrir decisões separadas antes de apresentar o recorte completo.

## 9. Consequência para a futura DEC-019

Depois de transformar as consolidações em unidades implementáveis e aplicar as
respostas de `PD-001` a `PD-003`, uma única `DEC-019` pode:

1. aprovar o recorte do MVP;
2. registrar inclusões e adiamentos;
3. aprovar os estados do vínculo esportivo;
4. definir o tratamento de cobertura tática;
5. definir o tratamento de offline;
6. autorizar somente M0/M1 com dados sintéticos;
7. definir D0;
8. reiterar que dados reais, piloto e produção continuam bloqueados.

Até essa decisão, os requisitos podem ser especificados e estimados, mas não há
autorização para iniciar implementação.

## 10. Done desta auditoria

A auditoria está concluída quando:

- RF-001 a RF-053 estiverem classificados;
- duplicidades não forem tratadas como entregas independentes;
- esclarecimentos técnicos não forem enviados a Davi;
- `PD-001` a `PD-003` forem apresentados junto ao recorte recomendado do MVP;
- RF-050 for tratado como gate, não como funcionalidade;
- o catálogo original permanecer preservado até a revisão controlada;
- nenhuma implementação tiver sido autorizada por inferência.
