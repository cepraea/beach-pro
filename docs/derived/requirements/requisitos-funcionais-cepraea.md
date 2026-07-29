---
document_id: DOC-CEPRAEA-REQ-DERIVADOS-V01
title: "Requisitos funcionais derivados do CEPRAEA"
document_type: requisito
version: "0.1.1"
workflow_status: RASCUNHO
responsible: Davi Sermenho
permitted_uses:
  - insumo_para_validacao
prohibited_uses:
  - especificacao_aprovada
  - autorizacao_de_implementacao
---

# Requisitos Funcionais — CEPRAEA BEACH PRO v0.1

- [Requisitos Funcionais — CEPRAEA BEACH PRO v0.1](#requisitos-funcionais--cepraea-beach-pro-v01)
  - [Nota de derivação](#nota-de-derivação)
  - [RF por domínio — Primeira Fase](#rf-por-domínio--primeira-fase)
    - [Domínio 1: Estado Operacional](#domínio-1-estado-operacional)
    - [Domínio 2: Elenco](#domínio-2-elenco)
    - [Domínio 3: Solicitações e Respostas Operacionais](#domínio-3-solicitações-e-respostas-operacionais)
    - [Domínio 4: Convocações e Listas](#domínio-4-convocações-e-listas)
    - [Domínio 5: Comunicação e Caixa Individual](#domínio-5-comunicação-e-caixa-individual)
    - [Domínio 6: Calendário e Compromissos](#domínio-6-calendário-e-compromissos)
    - [Domínio 7: Cobertura Tática e Indicadores](#domínio-7-cobertura-tática-e-indicadores)
    - [Domínio 8: Rastreabilidade e Auditoria](#domínio-8-rastreabilidade-e-auditoria)
    - [Domínio 9: Identidade e Acesso](#domínio-9-identidade-e-acesso)
    - [Domínio 10: Privacidade e Visibilidade](#domínio-10-privacidade-e-visibilidade)
    - [Domínio 11: Offline e Conectividade](#domínio-11-offline-e-conectividade)
  - [Requisitos de fases posteriores](#requisitos-de-fases-posteriores)
  - [Itens excluídos da derivação](#itens-excluídos-da-derivação)
  - [Verificação de cobertura](#verificação-de-cobertura)

<!-- markdownlint-disable MD013 -->

## Nota de derivação

- **Documento-fonte:** `DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO v0.1.md`
- **Data da derivação:** 2026-07-24
- **Procedimento:** `DERIVACAO_INDEPENDENTE_V0` (§ 14 do documento-fonte)
- **Restrição:** nenhum requisito foi incluído sem identificador de origem rastreável
  ao documento-fonte. Itens sem origem aprovada foram excluídos ou marcados como
  `NECESSIDADE_CANDIDATA`.
- **Escopo desta lista:** Primeira Fase (`DEC-005`) e fases posteriores identificadas.
  A lista não constitui especificação aprovada nem autoriza implementação; é insumo
  para a promoção para DECISAO-CEPRAEA — VERSÃO CANDIDATA 0.1.

***

## RF por domínio — Primeira Fase

### Domínio 1: Estado Operacional

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-001 | O sistema deve apresentar a Davi um estado operacional único, atual e verificável do CEPRAEA, de forma que Davi consiga identificar situação, pendências, decisões e próximas ações sem reconciliar manualmente fontes divergentes. | `CRIT-FASE1-001`, `OBJ-001`, `PROB-001`, `DEC-005` |
| RF-002 | O sistema não deve exigir que Davi consulte múltiplas fontes externas (planilhas, WhatsApp, e-mail, documentos) para responder a perguntas operacionais críticas incluídas no escopo da primeira fase. | `CRIT-FASE1-008`, `OBJ-001`, `DEC-010`, `DEC-012` |

---

### Domínio 2: Elenco

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-003 | O sistema deve manter o cadastro de atletas do elenco ativo, representando a decisão humana de Davi sobre composição, inclusão, desativação e retorno de atletas. | `CAP-01`, `DEC-004`, `DEC-005`, `§ 4.3` |
| RF-004 | Cada atleta deve acessar somente os próprios dados operacionais e as projeções de composição autorizadas; o sistema deve impedir o acesso a dados de outras atletas além das listas mínimas autorizadas. | `CRIT-FASE1-007`, `DEC-003-B`, `DEC-003-C`, `DEC-003-D`, `DEC-009` |

---

### Domínio 3: Solicitações e Respostas Operacionais

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-005 | O sistema deve suportar um modelo geral de solicitações criadas por Davi, contendo: assunto/tipo, pessoa(s) destinatária(s), opções de resposta válidas, prazo, vigência e ação esperada. | `DEC-013`, `DEC-012`, `§ 9.2` (Solicitação operacional) |
| RF-006 | Para cada tipo de solicitação, o sistema deve suportar estados semânticos distintos que distingam ao menos: disponível/sim, indisponível/não, incerta e não respondida; esses estados não podem ser tratados como equivalentes no registro. | `CRIT-FASE1-009`, `REGRA-DO-013`, `DEC-013`, `CAP-02` |
| RF-007 | Cada atleta pode responder somente às próprias solicitações; o sistema deve impedir que uma atleta altere a resposta de outra. | `CRIT-FASE1-002`, `DEC-003-B`, `DEC-003-C`, `DEC-013` |
| RF-008 | O sistema deve oferecer campo de justificativa opcional para respostas de atletas, com categorias controladas e a opção "prefere não informar"; o campo não pode solicitar diagnóstico, lesão, condição médica, psicológica, biométrica ou detalhe sensível equivalente. | `CRIT-FASE1-010`, `REGRA-DO-015`, `REGRA-DO-016`, `REGRA-DO-017`, `DEC-013` |
| RF-009 | As categorias iniciais de justificativa disponíveis para seleção são: trabalho ou estudo; compromisso familiar ou pessoal; transporte ou logística; conflito de horário; imprevisto; indisponibilidade previamente informada; assunto privado; outro motivo não sensível; prefere não informar. A atleta pode alterar ou retirar a justificativa dentro do prazo; a versão anterior deve ser preservada no histórico auditável com autoria, data e marcador de alteração. | `REGRA-DO-016`, `REGRA-DO-015`, `DEC-013` |
| RF-010 | O sistema deve preservar autoria, data, vigência e histórico de cada resposta operacional; ao alterar uma resposta dentro do prazo, a versão anterior não deve ser apagada. | `OBJ-002`, `REGRA-DO-008`, `DEC-013`, `CAP-02`, `§ 9.2` |
| RF-011 | Correções administrativas de Davi sobre respostas de atletas devem ser registradas em campo separado, com autoria, data e motivo, sem apagar a declaração original da atleta nem assumir a autoria dela. Erro administrativo comprovado por Davi permite invalidação da entrada errônea com marcador visível, preservando o original no histórico. | `REGRA-DO-019`, `DEC-013`, `§ 9.2` (Correção administrativa), `OBJ-002` |
| RF-012 | O sistema deve manter disponibilidade declarada, presença real, confirmação de convocação, escalação e participação real como registros semanticamente distintos; nenhum pode ser substituído por outro, derivado automaticamente de outro ou apresentado como equivalente. | `CRIT-FASE1-003`, `CRIT-FASE1-011`, `REGRA-DO-002`, `REGRA-DO-003`, `REGRA-DO-004`, `REGRA-DO-014`, `DEC-013`, `CAP-07` |
| RF-013 | Para cada compromisso, o sistema deve manter registros separados e vinculados de: resposta de disponibilidade, confirmação de convocação (quando aplicável), presença real e participação real; cada camada requer validação própria antes de ser registrada como fato. | `CRIT-FASE1-011`, `REGRA-DO-014`, `DEC-013`, `DEC-005`, `CAP-07` |
| RF-014 | Presença real em treino deve ser registrada como fato posterior ao evento e mantida semanticamente separada da disponibilidade declarada anteriormente; disponibilidade não comprova presença. | `REGRA-DO-002`, `§ 8.1`, `DEC-005`, `CRIT-FASE1-003`, `CAP-02` |

---

### Domínio 4: Convocações e Listas

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-015 | Davi pode criar convocações para competição ou etapa, selecionando atletas; a decisão de convocação pertence exclusivamente a Davi e não pode ser gerada automaticamente pelo sistema. | `CAP-05`, `DEC-004`, `DEC-005`, `CRIT-FASE1-004`, `REGRA-DO-009`, `DEC-013` |
| RF-016 | Cada atleta convocada pode aceitar, recusar ou permanecer pendente até o prazo; substituições, cancelamentos e o histórico de respostas de convocação devem ser registrados. | `CAP-05`, `DEC-013`, `DEC-014`, `§ 9.2` (Confirmação de convocação) |
| RF-017 | Atletas autorizadas devem poder consultar a lista vigente de convocação vinculada ao jogo, etapa ou competição correspondente, exibindo somente nome, função ou posição autorizada, estado mínimo, compromisso e vigência; justificativas, motivos pessoais, histórico individual e dados sensíveis não devem ser expostos. | `CRIT-FASE1-013`, `REGRA-DO-020`, `DEC-003-D`, `DEC-009`, `DEC-013`, `DEC-014`, `CAP-05` |
| RF-018 | Atletas autorizadas devem poder consultar a lista de confirmadas para determinado treino, identificada explicitamente como composição prevista baseada em declarações vigentes, não como presença real; atletas com estado não, incerta ou não respondida não devem ter esses estados expostos coletivamente na lista. | `CRIT-FASE1-014`, `REGRA-DO-021`, `DEC-003-D`, `DEC-009`, `DEC-013`, `DEC-014` |
| RF-019 | Listas compartilhadas (convocação e confirmadas para treino) devem exibir somente: nome, função ou posição autorizada, estado mínimo necessário, compromisso e vigência; justificativas, motivos pessoais, histórico completo, contatos, pendências individuais e dados sensíveis não podem ser expostos. | `CRIT-FASE1-016`, `REGRA-DO-020`, `REGRA-DO-022`, `DEC-003-D`, `DEC-009`, `DEC-014` |
| RF-020 | Listas substituídas, canceladas ou encerradas devem deixar de ser exibidas como vigentes; o sistema deve manter vínculo auditável com a versão anterior e preservar o histórico de publicação e alteração. | `CRIT-FASE1-015`, `OBJ-006`, `REGRA-DO-011`, `DEC-013`, `DEC-014` |
| RF-021 | Davi pode decidir não publicar a lista de convocação ou a lista de confirmadas para treino para um compromisso específico; o estado "não publicado" deve ser distinguível do estado "lista inexistente". | `REGRA-DO-022`, `DEC-013`, `DEC-014` |

---

### Domínio 5: Comunicação e Caixa Individual

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-022 | A PWA deve ser o canal operacional canônico entre Davi e as atletas; toda comunicação operacional obrigatória (solicitações, orientações, convocações, prazos, pendências) deve ocorrer dentro da PWA, sem dependência de WhatsApp, e-mail, planilhas, formulários ou outros aplicativos externos. | `CAP-10`, `DEC-005`, `DEC-010`, `DEC-012`, `PROB-002`, `CRIT-FASE1-008` |
| RF-023 | Cada atleta deve ter uma caixa individual apresentando: solicitações pendentes, prazo, opções de resposta válidas, resposta vigente, campo de justificativa opcional, estado de fechamento e histórico das próprias respostas. | `CAP-10`, `DEC-012`, `DEC-013` |
| RF-024 | O sistema deve registrar o estado de disponibilização, visualização e ciência de cada comunicação relevante, permitindo a Davi identificar pendências por atleta e assunto. | `CAP-10`, `OBJ-006`, `DEC-012`, `DEC-013` |
| RF-025 | O sistema deve apresentar a Davi um painel de pendências completas (itens não visualizados, não confirmados, não respondidos ou vencidos por atleta e assunto) sem exigir cobranças manuais externas. | `OBJ-006`, `CAP-10`, `DEC-012` |
| RF-026 | O sistema deve utilizar central interna de notificações como canal canônico; e-mail externo (Brevo SMTP) deve ser usado somente para ações de identidade (convite, confirmação de conta, recuperação de acesso e alertas de segurança). | `DEC-015`, `DEC-008` |

---

### Domínio 6: Calendário e Compromissos

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-027 | O sistema deve registrar compromissos (treinos, competições, reuniões e outros) com estado temporal, prazos associados, responsável e próxima ação; toda informação temporal deve indicar vigência e estado. | `CAP-04`, `CRIT-FASE1-005`, `OBJ-004`, `DEC-004`, `DEC-005`, `REGRA-DO-011` |
| RF-028 | Compromissos passados não devem ser exibidos como vigentes; o sistema deve distinguir o estado temporal de cada compromisso. | `CRIT-FASE1-005`, `OBJ-004`, `EVID-002` |
| RF-029 | Toda pendência crítica deve ter responsável e estado identificados; prazos sem responsável ou ações sem prazo devem ser sinalizados a Davi. | `OBJ-004`, `CRIT-FASE1-005` |

---

### Domínio 7: Cobertura Tática e Indicadores

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-030 | O sistema deve apresentar a Davi uma análise de cobertura de funções e posições baseada nas respostas vigentes de disponibilidade ou confirmação, sem substituir a decisão de convocação ou escalação; a decisão esportiva final permanece exclusivamente com Davi. | `CAP-03`, `OBJ-005`, `CRIT-FASE1-004`, `REGRA-DO-009`, `DEC-004`, `DEC-005` |
| RF-031 | O sistema pode exibir indicadores descritivos (respostas no prazo, pendências, alterações, ausências, divergência entre declaração e fato posterior), mas não deve gerar automaticamente rótulos ou inferências sobre comprometimento, disciplina, confiabilidade, saúde ou problema pessoal de atletas. | `CRIT-FASE1-012`, `REGRA-DO-018`, `OBJ-005`, `DEC-013`, `DEC-018` |
| RF-032 | Indicadores devem ser derivados exclusivamente de fatos previamente validados; indicadores não constituem fonte primária. | `REGRA-DO-007`, `DEC-018`, `OBJ-007` |

---

### Domínio 8: Rastreabilidade e Auditoria

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-033 | Registros críticos da primeira fase devem conter proveniência verificável, autoria, data e histórico suficiente para reconstruir: solicitação original, resposta vigente, justificativa opcional, alterações realizadas, fechamento, fato posterior e validação correspondente. | `CAP-12`, `OBJ-007`, `CRIT-FASE1-006`, `DEC-013`, `DEC-005` |
| RF-034 | O sistema deve registrar o histórico de publicação, alteração e resposta de listas de convocação e de confirmadas para treino, de forma que cada versão publicada possa ser identificada. | `OBJ-006`, `DEC-013`, `DEC-014`, `CAP-12` |
| RF-035 | Toda importação de dados de fontes externas deve registrar: origem, data, responsável pela importação, validação realizada e resultado; duplicidades devem ser detectadas e permitir rejeição antes da consolidação. | `DEC-010`, `DEC-013` |
| RF-036 | O sistema deve manter trilha de auditoria de eventos de segurança: login, recuperação de acesso, alterações de permissão e acessos privilegiados. | `DEC-008`, `§ 10.1` |

---

### Domínio 9: Identidade e Acesso

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-037 | Cada pessoa deve utilizar conta individual com identidade verificada; contas compartilhadas, edição por link e acesso anônimo a dados operacionais são proibidos. | `DEC-008`, `§ 10.1` |
| RF-038 | A primeira fase deve suportar somente dois perfis operacionais: Davi (treinador e administrador) e atleta; não serão criados perfis separados de mantenedor, suporte, observador, representante ou custodiante. | `DEC-017`, `DEC-008`, `DEC-003-E`, `DEC-016-A` |
| RF-039 | MFA TOTP é obrigatória para Davi e para acessos privilegiados. | `DEC-008`, `DEC-015`, `§ 10.1` |
| RF-040 | Davi deve poder administrar o estado das contas (suspender, reativar, revogar sessões), mas não pode visualizar senhas, segredos ou códigos de recuperação de outros usuários. | `DEC-008`, `DEC-017`, `§ 10.1` |
| RF-041 | O cadastro público de novas contas deve estar desabilitado; contas devem ser criadas por convite ou administração de Davi. | `DEC-008`, `DEC-015` |
| RF-042 | Recuperação de acesso deve ser realizada pela própria pessoa por meio de identidade verificada; Davi pode administrar o estado da conta, mas não recuperar credenciais alheias. | `DEC-008`, `§ 10.1` |
| RF-043 | A desativação de uma atleta do elenco deve desativar a conta correspondente; o histórico autorizado deve ser preservado após a desativação; ex-atletas exercem direitos sobre os próprios dados por canal externo. | `DEC-008`, `DEC-017`, `§ 10.1` |
| RF-044 | O sistema não deve permitir que nenhum perfil assuma silenciosamente a identidade de outro usuário. | `DEC-008`, `§ 10.1` |
| RF-045 | Row Level Security deve isolar os dados de cada atleta, garantindo que uma atleta acesse somente os próprios dados e as listas mínimas autorizadas; testes negativos de isolamento são obrigatórios. | `DEC-017`, `DEC-015`, `DEC-009` |

---

### Domínio 10: Privacidade e Visibilidade

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-046 | Justificativas de atletas devem ser restritas à própria atleta e a Davi; não devem ser exibidas em listas compartilhadas, rankings, relatórios ou a outras atletas. | `DEC-009`, `DEC-013`, `DEC-014`, `§ 10.1`, `REGRA-DO-017` |
| RF-047 | O sistema não deve inferir automaticamente motivo, comprometimento, disciplina, confiabilidade, saúde ou condição psicológica com base em qualquer dado de resposta, justificativa ou ausência de justificativa. | `DEC-009`, `DEC-013`, `REGRA-DO-018`, `§ 10.1` |
| RF-048 | Dados reais de atletas e dados operacionais não devem ser enviados a ferramentas de IA externas (incluindo APIs da OpenAI e da Anthropic); a PWA deve operar independentemente desses serviços. | `DEC-009`, `DEC-010`, `DEC-011`, `DEC-015`, `DEC-012` |
| RF-049 | A PWA deve oferecer área "Privacidade e meus dados" com canal para exercício de direitos de titulares e ex-atletas sobre os próprios dados. | `DEC-014`, `§ 10.2` |
| RF-050 | Dados reais de usuários devem permanecer bloqueados até que o portão de produção de privacidade seja verificado: confirmação de controlador e representante, bases legais, canal de direitos, avaliação de fornecedores, evidências técnicas de separação de ambientes, backup, restauração, eliminação e portabilidade. | `DEC-014`, `DEC-015`, `§ 10.2` |

---

### Domínio 11: Offline e Conectividade

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-051 | No modo offline, o sistema deve permitir somente leitura do último estado sincronizado, exibindo sempre aviso explícito de possível desatualização e horário da última sincronização; escrita offline não é permitida na primeira fase. | `DEC-015`, `DEC-007`, `CRIT-FASE1-005`, `§ 10.2` |
| RF-052 | Dados locais desatualizados nunca devem ser apresentados como atuais; dados locais não podem sobrescrever dados já validados no servidor. | `DEC-007`, `DEC-015`, `§ 10.2` |
| RF-053 | O snapshot local offline deve ser criptografado e vinculado a dispositivo pessoal confiável; se a proteção criptográfica não puder ser comprovada por testes, os dados pessoais offline devem ser desabilitados; o snapshot deve ser eliminado no logout, revogação ou expiração da sessão. | `DEC-015`, `§ 10.2` |

---

## Requisitos de fases posteriores

Listados para preservar rastreabilidade; fora do escopo da primeira fase conforme `DEC-005` e `DEC-006`.

| ID | Descrição | Origem |
| --- | --- | --- |
| RF-P01 | Organização do dia do jogo (necessidade preservada; mecanismo atual a substituir). | `CAP-06`, `DEC-004`, `DEC-005` |
| RF-P02 | Registro de resultados e histórico de competições com exigência de fonte autorizada e validação. | `CAP-08`, `DEC-004`, `DEC-005` |
| RF-P03 | Planejamento técnico (finalidade preservada; implementação atual a substituir). | `CAP-09`, `DEC-004`, `DEC-005` |
| RF-P04 | Módulo de feedback individual como módulo interno do CEPRAEA BEACH PRO, condicionado às regras de autenticação, perfis, privacidade, retenção e visibilidade. | `CAP-11`, `DEC-006`, `DEC-008`, `DEC-009` |

---

## Itens excluídos da derivação

Os itens abaixo foram explicitamente marcados como fora de escopo ou fora do produto no documento-fonte e não foram incluídos como requisitos.

| Item | Motivo da exclusão | Origem |
| --- | --- | --- |
| Scout e análise estatística | Pertence a sistema separado | `DEC-006`, `§ 8.2` |
| Edição e processamento de vídeo | Pertence a sistema separado | `DEC-006`, `§ 8.2` |
| Gestão financeira, pagamentos e contabilidade | Pertence a sistema separado | `DEC-006`, `§ 8.2` |
| Publicação de conteúdo público, conteúdo promocional e gestão de torcedores | Pertence a canal ou sistema separado | `DEC-006`, `§ 8.2` |
| Aplicativo nativo | Fora da primeira fase | `DEC-007`, `§ 8.1` |
| Perfis de público, familiares, imprensa, patrocinadores ou parceiros | Fora da PWA operacional | `DEC-017`, `§ 8.1` |
| Sincronização automática contínua ou bidirecional com planilhas ou mensagens | Não autorizada | `DEC-010`, `§ 8.1` |
| Decisões esportivas produzidas automaticamente | Proibido | `CRIT-FASE1-004`, `REGRA-DO-009`, `OBJ-005` |
| Inferência de disponibilidade, presença ou participação sem evidência | Proibido | `§ 8.2`, `REGRA-DO-002`, `REGRA-DO-003` |
| Avaliações psicológicas individuais e conteúdo sensível sem finalidade aprovada | Fora de escopo | `§ 8.2` |
| Conta ou função de suporte na PWA | Não autorizado na primeira fase | `DEC-017`, `DEC-003-E` |

---

## Verificação de cobertura

| Critério verificado | Resultado |
| --- | --- |
| Todos os 16 CRIT-FASE1 cobertos | CRIT-001→RF-001; CRIT-002→RF-007; CRIT-003→RF-012; CRIT-004→RF-015,RF-030; CRIT-005→RF-027,RF-028,RF-051; CRIT-006→RF-033; CRIT-007→RF-004; CRIT-008→RF-002; CRIT-009→RF-006; CRIT-010→RF-008; CRIT-011→RF-013; CRIT-012→RF-031; CRIT-013→RF-017; CRIT-014→RF-018; CRIT-015→RF-020; CRIT-016→RF-019 |
| CAP-06, -08, -09, -11 ausentes da primeira fase | Confirmado: presentes somente em RF-P01 a RF-P04 |
| Scout, vídeo, finanças e publicação pública ausentes | Confirmado: presentes somente na tabela de itens excluídos |
| Cada RF possui ao menos um identificador de origem | Confirmado |
| Nenhuma inferência não controlada adicionada | Confirmado: toda descrição rastreável a identificador existente no documento-fonte |

<!-- markdownlint-enable MD013 -->
