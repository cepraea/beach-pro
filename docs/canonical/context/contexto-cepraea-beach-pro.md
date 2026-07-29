---
document_id: DOC-CEPRAEA-CANDIDATA-CONTEXTO
title: "Versão candidata de contexto do CEPRAEA"
document_type: contexto
version: "0.1.1"
workflow_status: CANONICA_VIGENTE
responsible: Davi Sermenho
permitted_uses:
  - contexto_para_ia
  - derivacao_controlada
prohibited_uses:
  - canonizacao_por_inferencia
  - autorizacao_de_implementacao
  - dados_reais
  - piloto
  - producao
---
# DECISAO-CEPRAEA — VERSÃO CANDIDATA 0.1

- [DECISAO-CEPRAEA — VERSÃO CANDIDATA 0.1](#decisao-cepraea--versão-candidata-01)
  - [Descoberta, contexto e diagnóstico para orientar a documentação da futura PWA do CEPRAEA](#descoberta-contexto-e-diagnóstico-para-orientar-a-documentação-da-futura-pwa-do-cepraea)
  - [Como interpretar os estados](#como-interpretar-os-estados)
  - [Pergunta central e resposta canônica provisória](#pergunta-central-e-resposta-canônica-provisória)
  - [1. Identidade e contexto](#1-identidade-e-contexto)
    - [1.1 Objeto real — CEPRAEA](#11-objeto-real--cepraea)
    - [1.2 Produto futuro](#12-produto-futuro)
    - [1.3 Papel do DECISAO-CEPRAEA](#13-papel-do-decisao-cepraea)
  - [2. Realidade esportiva](#2-realidade-esportiva)
  - [3. Atores, autoridades e pessoas afetadas](#3-atores-autoridades-e-pessoas-afetadas)
    - [3.1 Davi Sermenho — usuário principal e autoridade interna](#31-davi-sermenho--usuário-principal-e-autoridade-interna)
    - [3.2 Atletas — usuárias secundárias, pessoas afetadas e fornecedoras de dados](#32-atletas--usuárias-secundárias-pessoas-afetadas-e-fornecedoras-de-dados)
    - [3.3 Papéis inexistentes no CEPRAEA real](#33-papéis-inexistentes-no-cepraea-real)
    - [3.4 Atores externos e papéis técnicos](#34-atores-externos-e-papéis-técnicos)
  - [4. Funcionamento atual com planilhas — AS-IS](#4-funcionamento-atual-com-planilhas--as-is)
    - [4.1 Componentes centrais](#41-componentes-centrais)
    - [4.2 Fluxo operacional atual](#42-fluxo-operacional-atual)
    - [4.3 Autoridade por assunto](#43-autoridade-por-assunto)
    - [4.4 Estado da implementação](#44-estado-da-implementação)
  - [5. Problema real, causas, consequências e evidências](#5-problema-real-causas-consequências-e-evidências)
    - [5.1 Declaração do problema](#51-declaração-do-problema)
    - [5.2 Causas confirmadas ou observadas](#52-causas-confirmadas-ou-observadas)
    - [5.3 Consequências](#53-consequências)
    - [5.4 Evidências principais](#54-evidências-principais)
  - [6. Capacidades atuais e tratamentos aprovados](#6-capacidades-atuais-e-tratamentos-aprovados)
  - [7. Objetivos, indicadores e resultados aprovados da futura PWA](#7-objetivos-indicadores-e-resultados-aprovados-da-futura-pwa)
    - [`OBJ-001` — Reduzir a incerteza operacional de Davi](#obj-001--reduzir-a-incerteza-operacional-de-davi)
    - [`OBJ-002` — Preservar as declarações das atletas](#obj-002--preservar-as-declarações-das-atletas)
    - [`OBJ-003` — Separar estados e fatos esportivos](#obj-003--separar-estados-e-fatos-esportivos)
    - [`OBJ-004` — Transformar o calendário em ação vigente](#obj-004--transformar-o-calendário-em-ação-vigente)
    - [`OBJ-005` — Apoiar a decisão esportiva sem automatizá-la](#obj-005--apoiar-a-decisão-esportiva-sem-automatizá-la)
    - [`OBJ-006` — Comunicar com visibilidade adequada](#obj-006--comunicar-com-visibilidade-adequada)
    - [`OBJ-007` — Preservar memória e rastreabilidade](#obj-007--preservar-memória-e-rastreabilidade)
  - [8. Escopo, limites e responsabilidades preservadas](#8-escopo-limites-e-responsabilidades-preservadas)
    - [8.1 Escopo aprovado da primeira fase](#81-escopo-aprovado-da-primeira-fase)
    - [8.2 Fora de escopo ou não autorizado](#82-fora-de-escopo-ou-não-autorizado)
    - [8.3 Responsabilidades humanas preservadas](#83-responsabilidades-humanas-preservadas)
  - [9. Domínio e vocabulário controlado](#9-domínio-e-vocabulário-controlado)
    - [9.1 Domínio e subdomínios](#91-domínio-e-subdomínios)
    - [9.2 Entidades e conceitos principais](#92-entidades-e-conceitos-principais)
    - [9.3 Regras conceituais obrigatórias](#93-regras-conceituais-obrigatórias)
    - [9.4 Elementos de implementação que não definem o domínio](#94-elementos-de-implementação-que-não-definem-o-domínio)
  - [10. Restrições do produto](#10-restrições-do-produto)
    - [10.1 Restrições confirmadas](#101-restrições-confirmadas)
    - [10.2 Restrições desconhecidas ou pendentes](#102-restrições-desconhecidas-ou-pendentes)
  - [11. Pendências, contradições e decisões](#11-pendências-contradições-e-decisões)
    - [11.1 Decisões de produto](#111-decisões-de-produto)
      - [`DEC-002`](#dec-002)
      - [`DEC-003`](#dec-003)
      - [`DEC-003-A`](#dec-003-a)
      - [`DEC-003-B`](#dec-003-b)
      - [`DEC-003-C`](#dec-003-c)
      - [`DEC-003-D`](#dec-003-d)
      - [`DEC-003-E`](#dec-003-e)
      - [`DEC-004`](#dec-004)
      - [`DEC-005`](#dec-005)
      - [`DEC-006`](#dec-006)
      - [`DEC-007`](#dec-007)
      - [`DEC-008`](#dec-008)
      - [`DEC-009`](#dec-009)
      - [`DEC-010`](#dec-010)
      - [`DEC-011`](#dec-011)
      - [`DEC-012`](#dec-012)
      - [`DEC-013`](#dec-013)
      - [`DEC-014`](#dec-014)
      - [`DEC-015`](#dec-015)
      - [`DEC-016`](#dec-016)
      - [`DEC-016-A`](#dec-016-a)
      - [`DEC-017`](#dec-017)
      - [`DEC-018`](#dec-018)
    - [11.2 Correções da operação atual que não podem ser confundidas com requisitos](#112-correções-da-operação-atual-que-não-podem-ser-confundidas-com-requisitos)
    - [11.3 Desconhecidos e pendências de evidência](#113-desconhecidos-e-pendências-de-evidência)
    - [11.4 Contradições controladas](#114-contradições-controladas)
  - [12. Registro mínimo de fontes](#12-registro-mínimo-de-fontes)
  - [13. MATRIZ](#13-matriz)
    - [`CLAIM-001`](#claim-001)
    - [`CLAIM-002`](#claim-002)
    - [`CLAIM-003`](#claim-003)
    - [`CLAIM-004`](#claim-004)
    - [`CLAIM-005`](#claim-005)
    - [`CLAIM-006`](#claim-006)
    - [`CLAIM-007`](#claim-007)
    - [`CLAIM-008`](#claim-008)
    - [`CLAIM-009`](#claim-009)
    - [`CLAIM-010`](#claim-010)
    - [`CLAIM-011`](#claim-011)
    - [`CLAIM-012`](#claim-012)
    - [`CLAIM-013`](#claim-013)
    - [`CLAIM-014`](#claim-014)
    - [`CLAIM-015`](#claim-015)
    - [`CLAIM-016`](#claim-016)
    - [`CLAIM-017`](#claim-017)
    - [`CLAIM-018`](#claim-018)
    - [`CLAIM-019`](#claim-019)
    - [`CLAIM-020`](#claim-020)
    - [`CLAIM-021`](#claim-021)
    - [`CLAIM-022`](#claim-022)
    - [`CLAIM-023`](#claim-023)
    - [`CLAIM-024`](#claim-024)
    - [`CLAIM-025`](#claim-025)
    - [`CLAIM-026`](#claim-026)
    - [`CLAIM-027`](#claim-027)
    - [`CLAIM-028`](#claim-028)
    - [`CLAIM-029`](#claim-029)
    - [`CLAIM-030`](#claim-030)
  - [14. Estado de conclusão desta base](#14-estado-de-conclusão-desta-base)
  - [15. Matriz de rastreabilidade](#15-matriz-de-rastreabilidade)

<!-- markdownlint-disable MD033 -->

<!-- markdownlint-disable-next-line MD013 -->

<!-- markdownlint-disable-next-line MD013 -->
## Descoberta, contexto e diagnóstico para orientar a documentação da futura PWA do CEPRAEA

<document_context>

- STATUS: `VERSAO_CANDIDATA` — PROMOVIDA EM 2026-07-24 A PARTIR DA BASE
  CONTROLADA DE CONTEÚDO v0.1 — NÃO É ESPECIFICAÇÃO FUNCIONAL NEM DOCUMENTAÇÃO
  FINAL DA PWA.
- Data de referência da validação: 2026-07-24.
- Data de promoção: 2026-07-24. Autoridade: Davi Sermenho.
- Finalidade: fonte canônica de descoberta, contexto e diagnóstico para orientar
  a documentação e o desenvolvimento da futura PWA CEPRAEA BEACH PRO. Substituiu
  a base controlada de conteúdo v0.1 após resolução de todas as ações requeridas
  (AR-001 a AR-015) e validação formal (VALIDACAO-CEPRAEA-v0.1.md).
- Governança confirmada: CONTEUDO `````DECISAO-CEPRAEA.md````` define o conteúdo obrigatório.
  VALIDACAO-CEPRAEA-v0.1.md registra a validação e a aprovação da promoção.
- Documento-base preservado: `DESCRICAO-CEPRAEA — BASE CONTROLADA DE CONTEÚDO
  v0.1.md` mantido como registro histórico.

## Como interpretar os estados

- `CONFIRMADO_HUMANO` — informação declarada ou aprovada por Davi Sermenho.
- `CONFIRMADO_FONTE` — informação sustentada por fonte identificada e compatível
  com o assunto.
- `ESTADO_TEMPORAL` — informação válida somente para o momento ou evento
  registrado.
- `PROBLEMA_OBSERVADO` — divergência, falha ou risco encontrado diretamente nas
  fontes.
- `INFERENCIA_CONTROLADA` — conclusão derivada das evidências, ainda separada de
  decisão.
- `NECESSIDADE_CANDIDATA` — necessidade plausível para o produto futuro, ainda
  não aprovada como requisito.
- `DECISAO_PENDENTE` — escolha que depende de Davi.
- `CONTRADITORIO` — fontes apresentam versões incompatíveis e não podem ser
  combinadas.
- `DESCONHECIDO` — informação não encontrada ou não confirmada.
- `FORA_DE_ESCOPO` — elemento explicitamente excluído do conteúdo ou produto.

## Pergunta central e resposta canônica provisória

- Pergunta: qual problema deve ser resolvido, para quem, em qual contexto e com
  qual resultado?
- Resposta canônica provisória: o problema a resolver é a incerteza operacional
  de Davi Sermenho ao coordenar o CEPRAEA, causada por informações fragmentadas,
  divergentes, temporalmente desatualizadas ou semanticamente ambíguas sobre
  elenco, disponibilidade, presença, cobertura tática, calendário, convocações,
  participação, resultados e comunicação. O problema afeta diretamente Davi,
  único treinador e responsável técnico e operacional, e secundariamente as
  atletas, que fornecem dados e recebem decisões e orientações. O contexto é uma
  equipe competitiva adulta feminina de handebol de praia cuja operação atual
  depende de planilhas, entradas humanas, documentos oficiais e comunicação
  externa. O resultado pretendido é um estado operacional único, atual,
  verificável e pronto para decisão, que reduza a reconciliação manual de Davi,
  preserve as declarações das atletas, mantenha as decisões esportivas sob
  autoridade humana e entregue a cada pessoa somente a informação necessária.
- Estado da resposta: `CONFIRMADO_HUMANO` quanto à composição e autoridade;
  `CONFIRMADO_FONTE` quanto ao problema operacional; `VERSAO_CANDIDATA`
  quanto ao uso como declaração promovida de contexto. A promoção documental
  foi concluída em 2026-07-24, mas não equivale a canonização pelo novo
  workflow documental.

</document_context>

## 1. Identidade e contexto

### 1.1 Objeto real — CEPRAEA

- `CONFIRMADO_HUMANO`: o CEPRAEA é uma equipe esportiva competitiva adulta
  feminina de handebol de praia, composta pelas atletas e conduzida
  exclusivamente pelo treinador Davi Sermenho.
- `CONFIRMADO_HUMANO`: não existem comissão técnica, coordenação, equipe
  administrativa ou equipe operacional interna.
- `CONFIRMADO_FONTE`: a equipe realiza treinos, participa de competições e
  mantém registros operacionais, técnico-táticos e históricos.
- `CONFIRMADO_FONTE`: CEPRAEA é o nome fantasia cadastrado da pessoa jurídica
  Centro de Prática de Esportes de Areia, CNPJ 19.993.964/0001-06, registrada
  como Associação Privada e com situação ativa no Mapa das OSC/IPEA.
- REGRA DE DESAMBIGUAÇÃO: CEPRAEA BEACH PRO identifica o produto; CEPRAEA
  identifica a organização e sua identidade esportiva pública; Centro de Prática
  de Esportes de Areia identifica a razão social. Esses nomes não são
  intercambiáveis.

### 1.2 Produto futuro

- Nome canônico: CEPRAEA BEACH PRO.
- Código: PWA-CEPRAEA-BEACH-PRO.
- Versão conceitual: 0.1.
- Identidade conceitual do produto: APROVADA por Davi Sermenho. A versão 0.1
  identifica a concepção atual do produto e não implica aprovação do escopo, dos
  requisitos ou da arquitetura.
- Responsável pelo problema, decisões esportivas e aprovação do contexto: Davi
  Sermenho.
- Organização de referência: CEPRAEA. Razão social verificada: Centro de Prática
  de Esportes de Areia. CNPJ: 19.993.964/0001-06. Natureza jurídica: Associação
  Privada. Nome fantasia cadastrado: CEPRAEA. A natureza jurídica foi verificada
  em fonte pública e não inferida.
- Estágio: descoberta e definição de contexto. Ainda não existe especificação
  aprovada da PWA.

### 1.3 Papel do DECISAO-CEPRAEA

- O DECISAO-CEPRAEA deve ser a fonte canônica de descoberta, contexto e
  diagnóstico. Ele deve explicar o CEPRAEA real, a operação atual, os problemas,
  as capacidades úteis, as necessidades candidatas, os limites, as restrições e
  os conceitos do domínio.
- O DECISAO-CEPRAEA não deve ser tratado como especificação da planilha existente,
  backlog, arquitetura técnica, documentação final da PWA ou autorização
  automática de requisitos.

## 2. Realidade esportiva

- `CONFIRMADO_HUMANO`: a unidade humana do CEPRAEA é formada por um treinador e
  pelas atletas.
- `CONFIRMADO_HUMANO`: Davi é o único responsável técnico e operacional interno.
- `ESTADO_TEMPORAL_CONFIRMADO_HUMANO`: a escala inicial informada para o CEPRAEA
  BEACH PRO é de 19 atletas e 1 treinador, totalizando 20 usuários operacionais.
  O número descreve o estado inicial e não autoriza limite técnico fixo ou
  codificado.
- `CONFIRMADO_FONTE`: a operação esportiva envolve elenco, treinos, calendário,
  competições, convocações, escalações, participação real, resultados,
  planejamento, comunicação e histórico.
- `CONFIRMADO_FONTE`: funções amplas usadas nas fontes incluem goleira, defesa,
  ataque, coringa e indefinida; posições específicas dependem de validação
  esportiva.
- `CONFIRMADO_FONTE`: a viabilidade de treino ou competição depende não apenas
  da quantidade de atletas, mas também da cobertura de funções, posições e
  sistemas táticos.
- `CONFIRMADO_FONTE`: documentos oficiais externos sustentam calendário,
  inscrição, relação nominal, jogos e resultados. Decisões esportivas internas
  permanecem sob autoridade de Davi.
- `ESTADO_TEMPORAL`: a composição do elenco muda. A base estruturada e a
  interface operacional não estão sincronizadas.
- `CONFIRMADO_HUMANO`: Gilvania Balbino é atleta histórica do CEPRAEA e está
  retornando.
- `PROBLEMA_OBSERVADO`: Gilvania aparece na interface operacional, mas não no
  cadastro estruturado de atletas. A decisão humana está resolvida; a
  atualização da representação digital permanece pendente.

## 3. Atores, autoridades e pessoas afetadas

### 3.1 Davi Sermenho — usuário principal e autoridade interna

- `CONFIRMADO_HUMANO`: Davi é treinador e único responsável técnico e
  operacional do CEPRAEA.
- Responsabilidades atuais confirmadas pelas fontes: planejamento de treinos;
  manutenção do elenco; análise de disponibilidade e cobertura; convocação;
  decisão tática; controle de prazos; comunicação; validação de participação e
  resultados; manutenção dos registros.
- `PAPEL_APROVADO_NA_PWA`: Davi é o usuário principal. Pode visualizar,
  registrar, corrigir e validar os dados operacionais necessários; manter o
  elenco; planejar treinos e competições; analisar disponibilidade e cobertura;
  emitir convocações e orientações; registrar decisões, participação e
  resultados; e acessar indicadores internos.
- Consequência do problema: Davi precisa conferir abas, reconciliar fontes,
  identificar dados vencidos, distinguir fatos de previsões e corrigir
  ambiguidades antes de decidir.

### 3.2 Atletas — usuárias secundárias, pessoas afetadas e fornecedoras de dados

- As atletas declaram disponibilidade, recebem informações de treinos e
  competições, recebem convocações e orientações, podem ter presença e
  participação registradas e são afetadas pela qualidade das decisões e
  comunicações.
- `NECESSIDADE_CONFIRMADA_HUMANO`: toda interação operacional destinada às
  atletas deve ocorrer dentro do CEPRAEA BEACH PRO. A atleta não deverá precisar
  acessar WhatsApp, e-mail, planilha, formulário ou outro site ou aplicativo
  para ler comunicações, responder solicitações, confirmar ciência, declarar
  disponibilidade ou consultar informação autorizada.
- `PAPEL_APROVADO_NA_PWA`, ADITADO PELAS `DEC-013` E `DEC-014`: cada atleta é
  usuária secundária. Pode visualizar as informações que lhe dizem respeito;
  declarar, confirmar, recusar ou indicar incerteza nas solicitações aplicáveis;
  justificar opcionalmente o próprio status; atualizar a resposta dentro das
  regras e prazos; receber informações de treinos, competições, convocações e
  orientações; consultar a resposta vigente, o próprio histórico e os próprios
  registros autorizados; solicitar correção posterior sem apagar a declaração
  original; consultar a lista vigente de convocação para jogo, etapa ou
  competição; e consultar a lista de atletas confirmadas para determinado
  treino, limitada à composição operacional autorizada.
- A resposta e a justificativa de uma atleta são dados humanos autorizados.
  Devem preservar autoria, data, vigência e histórico; não podem ser criadas,
  completadas, reclassificadas ou sobrescritas por inteligência artificial. Davi
  não poderá editar uma declaração como se tivesse sido produzida pela atleta;
  correções administrativas, invalidações e observações deverão existir em
  registro separado e auditável.
- `LIMITE_APROVADO` E ADITADO PELA `DEC-014`: a atleta não pode alterar decisões
  de Davi, respostas de outras atletas, registros oficiais, avaliações sensíveis
  ou informações internas sem autorização explícita. Justificativas, motivos
  pessoais, histórico completo, pendências individuais, dados de contato,
  avaliações, criticidade interna, lacunas táticas restritas e dados sensíveis
  ficam limitados à própria atleta e a Davi. Como exceção controlada, atletas
  autorizadas podem visualizar projeções operacionais mínimas de composição da
  equipe vinculadas a compromisso específico, como lista vigente de convocação e
  lista de confirmadas para treino.

### 3.3 Papéis inexistentes no CEPRAEA real

- `FORA_DO_MODELO_HUMANO_ATUAL`: comissão técnica, coordenação, equipe
  administrativa e equipe operacional interna.
- Regra terminológica: expressões como decisão da comissão ou link informado
  pela coordenação devem ser substituídas por decisão de Davi ou informação
  fornecida por Davi, quando isso corresponder à fonte humana.

### 3.4 Atores externos e papéis técnicos

- `CONFIRMADO_FONTE`: entidades organizadoras de competições e documentos
  oficiais atuam como fontes externas, não como integrantes do CEPRAEA.
- `ADMINISTRADOR_DA_PWA`: Davi. Administra os acessos do produto, podendo
  suspender, reativar e gerenciar contas, sem visualizar senhas ou segredos dos
  usuários.

- `MANTENEDOR_TECNICO_NA_PRIMEIRA_FASE`: Davi. Não será criado perfil técnico
  separado na PWA. Eventual mantenedor externo futuro dependerá de nova
  decisão e não será usuário esportivo.
- `OPERADOR_DE_SUPORTE_NA_PRIMEIRA_FASE`: inexistente. Não será criada conta ou
  função de suporte na PWA.
- `PUBLICO_OBSERVADOR`: não possui acesso aos dados operacionais. Conteúdo e
  publicação pública permanecem fora do produto conforme a `DEC-006`.

- `INTEGRACOES_APROVADAS`: sistemas externos são fontes, destinos ou serviços
  auxiliares; não se tornam integrantes do CEPRAEA nem autoridades esportivas.
  Todo intercâmbio deve preservar finalidade, proveniência, autoria, validação,
  privilégio mínimo e os limites das `DEC-008` e `DEC-009`.
- Regra: papéis técnicos não podem ser confundidos com integrantes reais da
  equipe, não possuem autoridade esportiva e não podem alterar decisões de Davi
  ou dados sem permissão compatível.

<as_is>

## 4. Funcionamento atual com planilhas — AS-IS

### 4.1 Componentes centrais

- CEPRAEA JUNHO 2026 — interface operacional para agenda, respostas,
  comunicação, planejamento e consultas.
- CEPRAEA DATABASE — base estruturada para atletas, funções, posições, treinos,
  competições, convocações, participação, resultados e mudanças.
- `CEPRAEA_CONTRACT`.gdoc — regras de operação, autoridade, preservação,
  decisões e histórico do sistema de planilhas.
- Documentos oficiais — fontes por evento para relação nominal, calendário,
  jogos e resultados.
- Respostas e decisões humanas — fontes primárias para disponibilidade declarada
  e decisões esportivas.

### 4.2 Fluxo operacional atual

- Fluxo sintetizado: a atleta declara informação; a interface registra ou
  apresenta; o database procura estruturar; fórmulas e painéis derivam
  consultas; Davi interpreta cobertura, prazos e pendências; Davi decide; a
  decisão é comunicada; fatos realizados devem ser validados e incorporados ao
  histórico.
- `PROBLEMA_CONFIRMADO_HUMANO`: WhatsApp, e-mail, planilhas e formulários
  fragmentam a comunicação e a ação. Mensagens podem não ser lidas, assuntos são
  misturados e respostas necessárias deixam de ser enviadas. O produto futuro
  deve substituir esses canais no fluxo operacional das atletas por comunicação,
  confirmação e resposta estruturadas dentro da PWA.
- `PROBLEMA_CONFIRMADO_HUMANO`: as opções atuais sim, não e talvez não fornecem
  contexto suficiente para distinguir disponibilidade afirmada,
  indisponibilidade, incerteza real, ausência de resposta, alteração posterior e
  fato ocorrido. Tratar talvez como não pode ser uma postura conservadora de
  planejamento, mas não autoriza apagar a diferença semântica no registro.
- A operação é temporal. Um valor pode representar solicitação, declaração,
  justificativa, confirmação, decisão, realização ou resultado. Esses estados
  não são equivalentes.

### 4.3 Autoridade por assunto

- Elenco e retorno de atleta — decisão humana de Davi; database deve representar
  a decisão.
- Disponibilidade futura — declaração da própria atleta, preservada sem
  inferência.
- Presença real em treino — registro factual posterior ao evento; não pode ser
  deduzida apenas da disponibilidade.
- Convocação e escalação — decisão de Davi.
- Participação em jogo — fato validado por partida.
- Calendário e resultado oficial — documento autorizado e validação humana.
- Indicadores — valores derivados de fatos previamente validados, nunca fontes
  primárias.

### 4.4 Estado da implementação

- `PROBLEMA_OBSERVADO`: interface e database apresentam divergência de elenco.
- `PROBLEMA_OBSERVADO`: existem fórmulas com erro de referência e painéis que
  podem apresentar estado vencido.
- `PROBLEMA_OBSERVADO`: planejamento técnico possui campos incompletos e o
  módulo de feedback não está plenamente operacional.
- `PROBLEMA_OBSERVADO`: logs possuem identificadores duplicados ou pendências
  sem fechamento.
- `PROBLEMA_OBSERVADO`: comentários históricos permanecem não resolvidos e
  contêm justificativas pessoais.
- `PROBLEMA_OBSERVADO`: contrato, interface e database permitem edição por
  qualquer pessoa com o link, reduzindo a garantia de integridade.

## 5. Problema real, causas, consequências e evidências

### 5.1 Declaração do problema

- `PROB-001` — Incerteza operacional: não existe, hoje, uma representação única,
  atual, semanticamente consistente e verificável do estado operacional do
  CEPRAEA.
- `PROB-002` — Falha de comunicação e resposta: os canais externos usados com as
  atletas não asseguram leitura, separação de assuntos, confirmação de ciência
  ou conclusão das respostas necessárias.
- `PROB-003` — Insuficiência de contexto para decisão: respostas reduzidas a
  sim, não ou talvez, sem estado temporal, justificativa opcional, histórico ou
  vínculo claro com a solicitação, não fornecem base suficiente para distinguir
  incerteza, indisponibilidade, ausência de resposta e fato posterior.
- Pessoas afetadas: Davi principalmente; atletas secundariamente.
- Frequência: `INFERENCIA_CONTROLADA` — o problema pode ocorrer sempre que elenco,
  disponibilidade, calendário, convocação, participação ou resultado mudarem sem
  reconciliação.
- Gravidade: `DESCONHECIDO` — sem escala aprovada; pendente de definição antes
  da promoção para versão candidata. Impactos observados alcançam decisão
  esportiva, comunicação, histórico, privacidade e integridade.

### 5.2 Causas confirmadas ou observadas

- `CAUSA-001` — Dados distribuídos entre interface, database, documentos
  oficiais, comentários e comunicação externa.
- `CAUSA-002` — Sincronização incompleta entre representações do mesmo objeto.
- `CAUSA-003` — Conceitos diferentes usando estruturas ou estados semelhantes,
  especialmente disponibilidade e presença.
- `CAUSA-004` — Painéis e automações sem controle temporal suficiente.
- `CAUSA-005` — Vocabulário obsoleto que cria atores inexistentes.
- `CAUSA-006` — Módulos incompletos, fórmulas quebradas e logs inconsistentes.
- `CAUSA-007` — Permissões amplas de edição e ausência de política explícita de
  retenção de comentários.
- `CAUSA-008` — Dependência de Davi para toda validação, sem outra pessoa
  interna para reconciliar a operação.
- `CAUSA-009` — Uso de WhatsApp, e-mail, planilhas e formulários como canais
  separados, sem uma caixa operacional única por atleta, assunto, prazo e estado
  de resposta.
- `CAUSA-010` — Modelo atual de resposta excessivamente reduzido, sem categorias
  controladas de justificativa, distinção entre resposta incerta e ausência de
  resposta, vigência, fechamento e comparação com o fato posteriormente
  validado.

### 5.3 Consequências

- `CONSEQ-001` — respostas diferentes conforme a aba consultada.
- `CONSEQ-002` — necessidade de conferência e reconstrução manual por Davi.
- `CONSEQ-003` — risco de convocação, comunicação ou planejamento baseados em
  informação vencida.
- `CONSEQ-004` — histórico individual incorreto se convocação for tratada como
  participação.
- `CONSEQ-005` — análise tática incorreta se respostas ausentes ou estados
  ambíguos forem tratados como disponibilidade.
- `CONSEQ-006` — exposição de justificativas pessoais e risco de alteração não
  autorizada das fontes.
- `CONSEQ-007` — comunicações não lidas, respostas atrasadas ou ausentes,
  mistura de assuntos e necessidade de cobrança manual por Davi.
- `CONSEQ-008` — risco de interpretar indevidamente uma resposta incerta como
  recusa, uma ausência de resposta como indisponibilidade ou uma justificativa
  como prova automática de comprometimento, disciplina, confiabilidade ou
  problema pessoal.

### 5.4 Evidências principais

- `EVID-001` — retorno de atleta confirmado por Davi, presente na interface e
  ausente do database.
- `EVID-002` — painel operacional de evento permaneceu ativo depois da
  respectiva realização.
- `EVID-003` — erros de referência na interface de consulta.
- `EVID-004` — disponibilidade e presença aparecem semanticamente misturadas.
- `EVID-005` — referências a comissão e coordenação contradizem a composição
  humana confirmada.
- `EVID-006` — comentários históricos não resolvidos e permissões de edição por
  link nas fontes centrais.
- `EVID-007` — duplicidades e pendências em registros de mudança.
- `EVID-008` — confirmação humana de Davi de que atletas não leem comunicações
  ou não respondem adequadamente quando o fluxo depende de WhatsApp, e-mail,
  planilhas e formulários externos.
- `EVID-009` — confirmação humana de Davi de que a planilha atual coleta apenas
  sim, não ou talvez e não registra contexto suficiente para avaliar
  corretamente a situação operacional que sustenta uma decisão.

## 6. Capacidades atuais e tratamentos aprovados

- Regra: estas capacidades descrevem o que as planilhas procuram realizar hoje.
  A `DEC-004` aprova o tratamento da finalidade de cada capacidade, mas não
  determina automaticamente sua inclusão na primeira fase nem aprova sua
  implementação atual como requisito.
- `CAP-01` — Representar o elenco atual. TRATAMENTO APROVADO: PRESERVAR A
  FINALIDADE e CORRIGIR A SINCRONIZAÇÃO. FASE: PRIMEIRA FASE.
- `CAP-02` — Coletar e preservar disponibilidade declarada. TRATAMENTO APROVADO
  E ADITADO PELA `DEC-013`: preservar e corrigir a semântica; distinguir
  disponível, indisponível, incerta e não respondida; permitir justificativa
  opcional e minimizada; registrar prazo, vigência, autoria e histórico; e
  comparar posteriormente a declaração com a presença real sem transformar uma
  na outra. FASE: PRIMEIRA FASE.
- `CAP-03` — Avaliar viabilidade por função, posição e sistema. TRATAMENTO
  APROVADO: PRESERVAR COMO APOIO, mantendo a decisão humana. FASE: PRIMEIRA
  FASE.
- `CAP-04` — Controlar calendário, compromissos e prazos. TRATAMENTO APROVADO:
  PRESERVAR e EXPANDIR O CONTROLE TEMPORAL. FASE: PRIMEIRA FASE.
- `CAP-05` — Apoiar convocações. TRATAMENTO APROVADO E ADITADO PELAS `DEC-013` E
  `DEC-014`: preservar a decisão exclusivamente com Davi; permitir à atleta
  aceitar, recusar ou permanecer pendente até o prazo, com justificativa
  opcional; distinguir resposta, convocação, escalação e participação; registrar
  substituição, cancelamento e histórico; e publicar às atletas autorizadas a
  lista vigente de convocação, limitada à composição esportiva necessária e sem
  justificativas, motivos pessoais ou histórico individual. FASE: PRIMEIRA FASE.
- `CAP-06` — Organizar o dia do jogo. TRATAMENTO APROVADO: PRESERVAR A
  NECESSIDADE e SUBSTITUIR O MECANISMO ATUAL. FASE: POSTERIOR.
- `CAP-07` — Distinguir convocação, confirmação da atleta, escalação, presença e
  participação. TRATAMENTO APROVADO E ADITADO PELA `DEC-013`: preservar
  obrigatoriamente cada camada como registro próprio; a resposta anterior não
  comprova o fato posterior, e o fato deverá ser validado por Davi ou fonte
  autorizada. FASE: PRIMEIRA FASE.
- `CAP-08` — Preservar resultados e histórico. TRATAMENTO APROVADO: PRESERVAR e
  EXIGIR FONTE E VALIDAÇÃO. FASE: POSTERIOR.
- `CAP-09` — Apoiar planejamento técnico. TRATAMENTO APROVADO: PRESERVAR A
  FINALIDADE e SUBSTITUIR A IMPLEMENTAÇÃO INCOMPLETA. FASE: POSTERIOR.
- `CAP-10` — Comunicar informações, coletar respostas e apresentar composição
  operacional às atletas. TRATAMENTO APROVADO E ADITADO PELAS `DEC-012`,
  `DEC-013` E `DEC-014`: preservar a finalidade e transformar a PWA no canal
  operacional interno canônico; separar assuntos e visibilidade; manter caixa
  individual; registrar disponibilização, visualização, ciência, resposta,
  justificativa opcional, prazo, pendência, substituição, fechamento e
  histórico; publicar listas vigentes de convocação e de confirmadas para treino
  com dados mínimos; impedir dependência de outro aplicativo; impedir exposição
  de justificativas; e impedir rótulos automáticos sobre a atleta. FASE:
  PRIMEIRA FASE.
- `CAP-11` — Organizar feedback individual. TRATAMENTO APROVADO: PRESERVAR COMO
  MÓDULO FUTURO DO CEPRAEA BEACH PRO; o módulo atual não é requisito aprovado.
  FASE: POSTERIOR, sujeita às regras de autenticação e perfis da `DEC-008` e às
  regras de privacidade, retenção, dados sensíveis e visibilidade aprovadas na
  `DEC-009`.
- `CAP-12` — Garantir rastreabilidade e auditoria. TRATAMENTO APROVADO:
  PRESERVAR e EXPANDIR. FASE: PRIMEIRA FASE.
- A classificação de tratamento foi aprovada por Davi na `DEC-004`. A `DEC-005`
  define as capacidades da primeira fase e as capacidades adiadas. A `DEC-006`
  define o feedback individual como módulo interno de fase posterior e separa
  scout, vídeo, finanças e publicação pública do produto.

</as_is>

<product_definition>

## 7. Objetivos, indicadores e resultados aprovados da futura PWA

Regra aprovada pela `DEC-011` e complementada pela `DEC-018`: os sete objetivos
orientam a primeira fase e as fases posteriores. A linha de base será coletada
por quatro semanas ou três ciclos operacionais completos, com registro manual
simples. As metas iniciais aprovadas incluem redução de pelo menos 50% das
fontes externas consultadas, 30% do tempo aproximado de preparação, 50% das
cobranças externas, pelo menos 80% das respostas esperadas concluídas dentro da
PWA no prazo e pelo menos 90% das atletas do piloto concluindo o fluxo principal
sem ajuda individual. Metas de segurança, privacidade, isolamento,
rastreabilidade e integridade exigem atendimento integral; metas de eficiência
serão avaliadas com contexto e não autorizam remoção de controles.

- Prioridade relativa: os sete objetivos têm prioridade equivalente para a
  primeira fase, conforme a `DEC-005`. Nenhum objetivo pode ser removido sem
  nova decisão humana de Davi. A sequência de implementação será determinada
  pelo planejamento técnico com base em dependências, não por hierarquia de valor.

### `OBJ-001` — Reduzir a incerteza operacional de Davi

- Resultado pretendido: Davi consulta um estado único e identifica situação,
  pendências, decisão e próxima ação sem reconciliar manualmente fontes
  divergentes.
- INDICADORES APROVADOS: perguntas operacionais críticas que exigem consulta
  externa; divergências internas; registros sem estado ou próxima ação; e, após
  linha de base, tempo necessário para preparar uma decisão operacional.
- CONDIÇÃO DE SUCESSO: nenhuma pergunta crítica incluída no escopo exige
  reconciliação manual entre representações internas da PWA.
- Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoa beneficiada: Davi.

### `OBJ-002` — Preservar as declarações das atletas

- Resultado pretendido: toda resposta, justificativa e alteração permanece fiel
  ao que a atleta informou, ao tipo de solicitação e ao período de vigência.
- INDICADORES APROVADOS E ADITADOS PELA `DEC-013`: respostas ou justificativas
  sem autoria; alterações sem histórico; respostas inferidas ou reclassificadas
  pelo sistema; sobrescritas não autorizadas; divergências entre o declarado e o
  apresentado; perda da resposta anterior; justificativa atribuída à pessoa
  errada; e correção administrativa apresentada como declaração da atleta.
- CONDIÇÃO DE SUCESSO ADITADA PELA `DEC-013`: nenhuma resposta ou justificativa
  é criada, inferida, reclassificada ou sobrescrita sem ação autorizada, autoria
  e trilha de alteração; a resposta vigente e todas as versões anteriores podem
  ser reconstruídas.
- Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoas beneficiadas: atletas e
  Davi.

### `OBJ-003` — Separar estados e fatos esportivos

- Resultado pretendido: solicitação, declaração anterior, justificativa,
  confirmação de decisão, disponibilidade, presença, convocação, escalação,
  participação e resultado possuem significados e registros distintos.
- INDICADORES APROVADOS E ADITADOS PELA `DEC-013`: equivalências indevidas entre
  conceitos; tratamento de incerta ou não respondida como indisponível sem
  identificação; resposta anterior usada como presença ou participação;
  consultas que utilizem o fato errado; registros sem estado temporal;
  indicadores derivados de fatos não validados.
- CONDIÇÃO DE SUCESSO ADITADA PELA `DEC-013`: todos os fluxos e consultas da
  primeira fase utilizam a camada correta, distinguem incerta, não e não
  respondida e impedem que declaração, justificativa, confirmação e fato
  posterior sejam apresentados como equivalentes.
- Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoas beneficiadas: Davi e
  atletas.

### `OBJ-004` — Transformar o calendário em ação vigente

- Resultado pretendido: cada compromisso aplicável apresenta estado temporal,
  pendências e próxima ação; eventos passados não permanecem como vigentes.
- INDICADORES APROVADOS: compromissos vencidos exibidos como atuais; pendências
  sem responsável; ações sem prazo; compromissos sem estado temporal;
  comunicações baseadas em evento vencido.
- CONDIÇÃO DE SUCESSO: nenhum compromisso passado aparece como vigente e toda
  pendência crítica possui responsável e estado.
- Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoa beneficiada: Davi; atletas
  recebem comunicação vigente.

### `OBJ-005` — Apoiar a decisão esportiva sem automatizá-la

- Resultado pretendido: Davi recebe dados atuais sobre elenco, respostas,
  justificativas minimizadas, disponibilidade, confirmações, fatos posteriores e
  cobertura, mas mantém integralmente a interpretação humana, a convocação, o
  planejamento e a decisão tática.
- INDICADORES APROVADOS E ADITADOS PELA `DEC-013`: decisões produzidas
  automaticamente; decisões sem confirmação explícita de Davi; recomendações
  apresentadas como decisões; análises baseadas em dados vencidos ou não
  validados; justificativas convertidas em rótulos de comprometimento,
  disciplina ou confiabilidade; e contagens apresentadas como julgamento
  pessoal.
- CONDIÇÃO DE SUCESSO ADITADA PELA `DEC-013`: zero decisão esportiva final e
  zero classificação pessoal de comprometimento, disciplina, confiabilidade ou
  problema individual sem avaliação e ação explícitas de Davi.
- Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoa beneficiada: Davi.

### `OBJ-006` — Comunicar com visibilidade adequada

- Resultado pretendido: toda comunicação operacional e toda resposta obrigatória
  das atletas são gerenciadas dentro da PWA, em assunto identificável, com
  estado, prazo e ação esperada; cada atleta recebe informação atual e
  necessária para agir e pode consultar a composição operacional autorizada do
  compromisso; detalhes individuais, justificativas e informações internas
  permanecem restritos.
- INDICADORES APROVADOS E ADITADOS PELAS `DEC-012` E `DEC-014`: comunicações ou
  listas vencidas, divergentes, substituídas ou canceladas exibidas como
  vigentes; exposição de justificativa, motivo pessoal, histórico, contato,
  pendência individual ou dado sensível de outra atleta; lista sem compromisso,
  público, origem ou vigência; conteúdo publicado antes da autorização de Davi;
  itens não visualizados, não confirmados, não respondidos ou vencidos;
  respostas vinculadas ao assunto errado; cobranças manuais; dependência de
  canal externo; e ações obrigatórias exigidas fora da PWA.
- CONDIÇÃO DE SUCESSO ADITADA PELAS `DEC-012` E `DEC-014`: toda comunicação e
  lista deriva de estado autorizado, possui compromisso, público, assunto e
  vigência definidos; Davi identifica pendências completas; cada atleta
  identifica o que deve fazer e quem compõe o grupo autorizado; a lista de
  treino é apresentada como previsão baseada em confirmações e não como presença
  real; listas substituídas, canceladas ou encerradas deixam de aparecer como
  vigentes; justificativas e motivos não são expostos; o histórico reconstrói
  publicação, alteração e resposta; e nenhuma ação obrigatória exige outro
  aplicativo.

Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoas beneficiadas: atletas e
Davi.

### `OBJ-007` — Preservar memória e rastreabilidade

- Resultado pretendido: solicitações, respostas, justificativas, fatos, decisões
  e alterações podem ser reconstruídos por fonte, autoria, vigência, estado e
  vínculo com o compromisso correspondente.
- INDICADORES APROVADOS E ADITADOS PELA `DEC-013`: registros críticos sem fonte;
  respostas ou justificativas sem autoria; alterações sem versão anterior;
  importações sem origem ou validação; fatos sem estado; ausência de vínculo
  entre solicitação, resposta e fato posterior; e falhas que alterem dados
  silenciosamente.
- CONDIÇÃO DE SUCESSO ADITADA PELA `DEC-013`: todo registro crítico da primeira
  fase possui proveniência verificável e histórico suficiente para reconstruir
  solicitação, resposta vigente, justificativa opcional, alterações, fechamento,
  fato posterior e validação.
- Fase definida pela `DEC-005`: PRIMEIRA FASE. Pessoas beneficiadas: Davi e
  futuros revisores autorizados.
- Nota sobre terminologia de resultados: saída é o artefato produzido pelo
  sistema (ex: estado operacional exibido, lista de convocação publicada);
  resultado é a mudança observável causada pelo uso da saída (ex: Davi decide
  sem reconciliar fontes manualmente); impacto é o efeito de médio ou longo
  prazo sobre a operação e as pessoas (ex: atletas respondem com mais contexto
  em ciclos sucessivos). Os critérios `CRIT-FASE1-*` avaliam saídas funcionais;
  os `OBJ-*` definem resultados esperados; os indicadores `IND-001` a `IND-010`
  aproximam impactos mensuráveis.

## 8. Escopo, limites e responsabilidades preservadas

### 8.1 Escopo aprovado da primeira fase

- Capacidades incluídas na primeira fase: `CAP-01` — elenco atual; `CAP-02` —
  disponibilidade declarada; `CAP-03` — avaliação de viabilidade como apoio;
  `CAP-04` — calendário, compromissos e prazos; `CAP-05` — apoio às convocações;
  `CAP-07` — distinção entre convocação, escalação e participação; `CAP-10` —
  comunicação com separação de visibilidade; `CAP-12` — rastreabilidade e
  auditoria.
- REGRA DE ESCOPO: o registro de presença real integra obrigatoriamente a
  primeira fase e deve permanecer semanticamente separado da disponibilidade
  declarada.
- Capacidades adiadas para fase posterior: `CAP-06` — organização do dia do
  jogo; `CAP-08` — resultados e histórico; `CAP-09` — planejamento técnico.
- Capacidade interna destinada a fase posterior: `CAP-11` — feedback individual,
  sujeita às regras de autenticação e perfis aprovadas na `DEC-008` e às regras
  de privacidade, retenção, dados sensíveis e visibilidade aprovadas na
  `DEC-009`.
- Processos incluídos na primeira fase: atualização do elenco; criação de
  solicitações por Davi; declaração e atualização de disponibilidade;
  confirmação ou recusa de convocação; justificativa opcional e minimizada;
  separação entre incerta, não e não respondida; registro posterior de presença
  e participação; planejamento de compromissos e prazos; análise de viabilidade;
  decisão humana de Davi; comunicação interna; caixa individual; publicação
  controlada da lista vigente de convocação; publicação da lista de confirmadas
  para treino como composição prevista; separação de assuntos e visibilidade;
  ciência quando exigida; resposta estruturada; fechamento e correção auditável;
  acompanhamento de pendências; validação de fatos; estado operacional;
  indicadores descritivos; fonte e auditoria.
- Usuários operacionais aprovados para o produto, conforme a `DEC-017`: somente
  Davi como treinador, administrador e mantenedor; e atletas como usuárias
  secundárias, com ações e limites de visibilidade definidos pelas decisões
  anteriores. Ex-atletas não terão perfil operacional; fornecedores, entidades
  esportivas, público e patrocinadores não terão conta na PWA.
- Ambiente atual incluído na descoberta: Google Sheets, Google Drive, documentos
  oficiais, entradas humanas e comunicação externa.

`AMBIENTE_APROVADO_DA_PWA`: PWA responsiva e instalável. Aplicativo nativo não é
necessário na primeira fase.

`DISPOSITIVOS_APROVADOS`: smartphones de Davi e das atletas como dispositivos
principais; computador ou notebook de Davi para administração.

- `AMBIENTES_DE_USO`: treinos, competições, deslocamentos e administração
  remota.
- `INTEGRACOES_NA_PRIMEIRA_FASE`: não haverá sincronização automática contínua
  ou bidirecional com planilhas, mensagens, documentos oficiais ou outros
  sistemas. As fontes atuais poderão ser usadas em migração inicial controlada,
  importação manual validada e referências autorizadas.
- `CANAL_OPERACIONAL_INTERNO_APROVADO_PELA_DEC`-012: após a entrada da PWA em
  operação, WhatsApp, e-mail, planilhas, formulários e outros sites ou
  aplicativos não serão componentes do fluxo obrigatório das atletas. Cadastro,
  leitura, confirmação, resposta, disponibilidade, consulta e demais ações
  incluídas deverão ser concluídos dentro da PWA. Documentos oficiais externos
  poderão continuar sendo tratados por Davi como fontes, sem obrigar a atleta a
  sair do produto.
- `CRIT-FASE1-001` — Davi consegue consultar um estado operacional único e
  atual.
- `CRIT-FASE1-002` — cada atleta consegue atualizar somente a própria
  disponibilidade.
- `CRIT-FASE1-003` — disponibilidade, presença, convocação, escalação e
  participação permanecem semanticamente distintas.
- `CRIT-FASE1-004` — decisões esportivas dependem da confirmação de Davi.
- `CRIT-FASE1-005` — toda informação temporal relevante indica vigência e
  estado.
- `CRIT-FASE1-006` — dados críticos possuem fonte, validação e histórico.
- `CRIT-FASE1-007` — a visibilidade respeita os limites aprovados na `DEC-003`.
- `CRIT-FASE1-008` — o fluxo central não exige reconciliação manual entre várias
  planilhas.
- `CRIT-FASE1-009` — cada solicitação utiliza estados adequados ao seu tipo e
  distingue incerta, não e não respondida.
- `CRIT-FASE1-010` — a atleta pode justificar opcionalmente a própria resposta
  sem ser obrigada a informar dado sensível.
- `CRIT-FASE1-011` — resposta anterior, confirmação, presença e participação
  permanecem separadas e vinculadas ao mesmo compromisso.
- `CRIT-FASE1-012` — o sistema apresenta fatos e indicadores descritivos, mas
  não produz automaticamente rótulos de comprometimento, disciplina,
  confiabilidade ou problema pessoal.
- `CRIT-FASE1-013` — cada atleta autorizada consegue consultar a lista vigente
  de convocação vinculada ao jogo, etapa ou competição correspondente.
- `CRIT-FASE1-014` — cada atleta autorizada consegue consultar a lista de
  confirmadas para determinado treino, identificada como composição prevista e
  não como presença real.
- `CRIT-FASE1-015` — listas substituídas, canceladas ou encerradas não aparecem
  como vigentes e mantêm vínculo auditável com a versão anterior.
- `CRIT-FASE1-016` — listas compartilhadas exibem somente nome, função ou
  posição autorizada, estado mínimo necessário, compromisso e vigência, sem
  justificativas, motivos pessoais, histórico completo, contato, pendências
  individuais ou dados sensíveis.

### 8.2 Fora de escopo ou não autorizado

- `FORA_DE_ESCOPO`: substituir Davi em decisão técnica, tática, convocatória ou
  disciplinar.
- `FORA_DE_ESCOPO`: inferir disponibilidade, presença, participação ou resultado
  sem evidência.
- `FORA_DE_ESCOPO`: sobrescrever resposta humana sem autorização e histórico.
- `FORA_DE_ESCOPO_DO_CONTEXTO_GERAL`: avaliações psicológicas individuais e
  conteúdo sensível sem finalidade aprovada.
- `FORA_DO_PRODUTO`: coleta e processamento de scout pertencem a sistema
  separado. A PWA poderá consumir somente dados agregados ou validados por
  integração futura específica, com contrato de dados, proveniência, finalidade,
  controle de acesso e tratamento de falhas; nenhuma integração de scout integra
  a primeira fase.
- `FORA_DO_PRODUTO`: edição e processamento de vídeo pertencem a sistema
  separado. A PWA poderá manter referências ou links autorizados, sem editar ou
  processar vídeos.
- `FORA_DO_PRODUTO`: gestão financeira, pagamentos, cobranças e contabilidade
  pertencem a sistema separado.
- `FORA_DO_PRODUTO`: publicação de conteúdo público, conteúdo promocional,
  gestão de torcedores e publicação automática pertencem a canais ou sistemas
  separados.
- `DENTRO_DO_PRODUTO_EM_FASE_POSTERIOR`: feedback individual pertence ao CEPRAEA
  BEACH PRO como módulo futuro, sujeito às regras de autenticação e perfis de
  acesso da `DEC-008` e às regras de privacidade, retenção, dados sensíveis e
  visibilidade da `DEC-009`.
- REGRA DE FRONTEIRA: o CEPRAEA BEACH PRO não substitui ferramentas
  especializadas de scout, vídeo, finanças ou publicação pública.

`FORA_DA_PRIMEIRA_FASE`: aplicativo nativo e escrita offline.

### 8.3 Responsabilidades humanas preservadas

- Davi preserva: validação do elenco; definição de função e posição;
  planejamento; convocação; escalação; decisão tática; comunicação; confirmação
  de fatos sem fonte oficial suficiente; aprovação do conteúdo.
- Atletas preservam: declaração, confirmação, recusa, indicação de incerteza,
  justificativa opcional e atualização das próprias informações autorizadas. A
  ausência de justificativa ou a escolha por não informar não autoriza o sistema
  a completar o motivo.
- Fontes oficiais preservam: comprovação de calendário, inscrição, relação
  nominal, partida e resultado quando aplicável.

## 9. Domínio e vocabulário controlado

### 9.1 Domínio e subdomínios

- Domínio: gestão operacional, técnico-tática e histórica de uma equipe adulta
  feminina de handebol de praia.
- Subdomínios: elenco; solicitações e respostas operacionais; justificativas;
  disponibilidade e presença; treinos; cobertura tática; calendário;
  competições; convocações e confirmações; operação do jogo; participação;
  resultados; comunicação; feedback; proveniência e auditoria.
- Tema central: estado operacional atual e verificável do CEPRAEA.

### 9.2 Entidades e conceitos principais

- CEPRAEA — equipe esportiva real formada por Davi e atletas.
- Treinador — Davi Sermenho, autoridade interna para planejamento, convocação,
  definição tática, validação e comunicação.
- Atleta — pessoa integrante ou candidata ao elenco, com identidade, estado,
  função e posições autorizadas.
- Elenco — conjunto de atletas reconhecidas como ativas em determinado estado
  temporal.
- Status da atleta — condição de vínculo com o elenco; não representa
  disponibilidade para um compromisso.
- Função — classificação esportiva ampla, como goleira, defesa, ataque, coringa
  ou indefinida.
- Posição — papel esportivo autorizado ou efetivamente desempenhado, que pode
  variar conforme o contexto.
- Compromisso — treino, competição, reunião, feedback ou outra atividade
  operacional.
- Solicitação operacional — pedido criado por Davi que define assunto, pessoa
  destinatária, tipo de resposta, opções válidas, prazo, vigência e ação
  esperada.
- Resposta operacional — declaração da atleta vinculada a uma solicitação.
  Possui estado, autoria, data, vigência e histórico; seus estados dependem do
  tipo de solicitação.
- Resposta de disponibilidade — declaração anterior da atleta sobre
  possibilidade de comparecer, distinguindo disponível, indisponível, incerta e
  não respondida.
- Justificativa operacional — contexto opcional fornecido pela própria atleta,
  por categoria controlada e, quando necessário, observação curta não sensível.
  Não comprova presença, participação, disciplina, comprometimento ou
  legitimidade do motivo.
- Confirmação de convocação — resposta da atleta a uma convocação de Davi,
  distinguindo aceita, recusada, pendente, prazo vencido, cancelada ou
  substituída.
- Correção administrativa — registro separado, feito por Davi, que corrige,
  invalida ou contextualiza um dado sem assumir a autoria da atleta nem apagar o
  original.
- Presença real — evidência posterior de comparecimento ao treino.
- Treino — sessão planejada e posteriormente classificada por realização.
- Competição — evento esportivo organizado por entidade externa.
- Etapa — ocorrência específica dentro de circuito ou competição.
- Jogo — partida individual pertencente a competição ou etapa.
- Convocação — decisão de Davi que seleciona atletas para competição ou etapa.
- Escalação — subconjunto autorizado ou escolhido para uma partida específica.
- Participação real — relação factual entre atleta e partida realizada.
- Resultado — desfecho validado de partida efetivamente realizada.
- Cobertura tática — comparação entre posições necessárias e atletas
  disponíveis.
- Estado operacional — representação atual e verificável de elenco, respostas,
  cobertura, compromissos, decisões e fatos validados.
- Próxima ação — ação humana necessária para manter a operação regular.
- Fonte autorizada — origem aceita para sustentar determinado dado.
- Validação — confronto de uma afirmação com fonte e autoridade compatíveis.
- Rastreabilidade — capacidade de reconstruir origem, alteração, responsável e
  estado.

### 9.3 Regras conceituais obrigatórias

- `REGRA-DO-001` — CEPRAEA não é sinônimo de planilha, database, interface ou
  PWA.
- `REGRA-DO-002` — disponibilidade não comprova presença.
- `REGRA-DO-003` — convocação não comprova escalação nem participação.
- `REGRA-DO-004` — participação pertence a uma partida específica.
- `REGRA-DO-005` — jogo previsto não comprova realização.
- `REGRA-DO-006` — resultado informado não é resultado validado.
- `REGRA-DO-007` — indicadores são derivados de fatos validados e não constituem
  fonte primária.
- `REGRA-DO-008` — resposta de atleta deve ser preservada sem inferência.
- `REGRA-DO-009` — decisão esportiva final pertence a Davi.
- `REGRA-DO-010` — criticidade representa risco funcional, não julgamento
  pessoal.
- `REGRA-DO-011` — toda informação temporal precisa indicar vigência ou estado.
- `REGRA-DO-012` — termos comissão e coordenação não representam atores internos
  atuais.
- `REGRA-DO-013` — sim, não, incerta e não respondida são estados distintos; uma
  regra conservadora de planejamento não pode apagar essa diferença no registro.
- `REGRA-DO-014` — declaração anterior, confirmação de convocação, presença real
  e participação real são camadas distintas.
- `REGRA-DO-015` — justificativa é opcional; a atleta pode selecionar assunto
  privado ou prefere não informar.
  EXCECAO: a atleta pode alterar ou retirar a justificativa dentro do prazo
  definido — autoridade: a própria atleta — efeito: a versão anterior é
  preservada no histórico auditável — registro: nova entrada com autoria, data
  e marcador de alteração.
- `REGRA-DO-016` — categorias iniciais permitidas de justificativa são trabalho
  ou estudo; compromisso familiar ou pessoal; transporte ou logística; conflito
  de horário; imprevisto; indisponibilidade previamente informada; assunto
  privado; outro motivo não sensível; e prefere não informar.
  EXCECAO: a lista de categorias pode ser expandida por nova decisão explícita
  de Davi — autoridade: Davi — efeito: novas categorias ficam disponíveis para
  seleção — registro: nova decisão DEC-* documentada antes da implementação.
- `REGRA-DO-017` — campos de justificativa não podem solicitar diagnóstico,
  lesão, condição médica, psicológica, biométrica ou detalhe equivalente.
- `REGRA-DO-018` — indicadores podem descrever respostas no prazo, pendências,
  alterações, ausências e divergência entre declaração e fato, mas não podem
  produzir julgamento automático sobre comprometimento, disciplina,
  confiabilidade ou problema pessoal.
  EXCECAO: Davi pode interpretar humanamente os indicadores e registrar sua
  avaliação em campo separado com autoria e data — autoridade: Davi —
  efeito: avaliação registrada como decisão humana explícita, não como saída
  automática do sistema — registro: campo de observação auditável distinto dos
  indicadores calculados.
- `REGRA-DO-019` — após o fechamento, correção ou contestação deve preservar a
  resposta original e criar nova entrada auditável.
  EXCECAO: erro administrativo comprovado por Davi permite invalidação da
  entrada errônea com marcador visível — autoridade: Davi — efeito: a entrada
  original permanece no histórico marcada como inválida; a correção cria novo
  registro vinculado — registro: motivo da invalidação, autoria, data e
  referência à entrada original.
- `REGRA-DO-020` — lista de convocação é uma projeção operacional de decisão
  vigente de Davi; não revela justificativas, recusas, pendências pessoais ou
  histórico completo.
- `REGRA-DO-021` — lista de confirmadas para treino é uma projeção de
  declarações vigentes e não comprova presença real.
- `REGRA-DO-022` — projeção operacional compartilhável deve estar vinculada a
  compromisso, público e vigência e conter somente dados mínimos autorizados.
  EXCECAO: Davi pode decidir não publicar a projeção para um compromisso
  específico — autoridade: Davi — efeito: a lista não é exibida às atletas para
  aquele compromisso — registro: ausência de publicação não requer justificativa,
  mas o estado de não publicado deve ser distinguível de lista inexistente.

### 9.4 Elementos de implementação que não definem o domínio

Abas, células, fórmulas, intervalos, importações, frontend, database,
identificadores técnicos e tecnologia de armazenamento implementam a operação,
mas não definem a realidade esportiva.

## 10. Restrições do produto

### 10.1 Restrições confirmadas

- Autoridade: decisões esportivas permanecem humanas e pertencem a Davi.
- Integridade: respostas humanas não podem ser inferidas ou sobrescritas.
- Privacidade: o produto lidará com dados pessoais e operacionais de atletas;
  minimização e separação de visibilidade são obrigatórias. O isolamento
  individual não impede o compartilhamento de composição operacional mínima
  quando necessário e autorizado para um compromisso específico.
- Rastreabilidade: fatos críticos precisam de fonte, validação e histórico.
- Temporalidade: compromissos, respostas, decisões e resultados mudam de estado
  e não podem permanecer indefinidamente vigentes.
- Regras esportivas: limites de convocação, participação e documentação dependem
  da competição e da fonte oficial; não devem ser universalizados sem validação.
- Operação atual: depende de conectividade e serviços do Google. Essa condição
  descreve o AS-IS, não decide a arquitetura da PWA.
- Segurança atual: permissões de edição por link constituem risco que deve ser
  corrigido; edição por link não é autorizada pela `DEC-008`.

- Identidade e acesso: cada pessoa deve utilizar conta individual com identidade
  verificada. Contas compartilhadas e acesso anônimo aos dados operacionais não
  são permitidos.
- Autenticação multifator: obrigatória para Davi e para acessos técnicos
  privilegiados.
- Perfis mínimos: a primeira fase terá somente Davi e atleta. Não haverá conta
  separada de mantenedor, suporte, representante, custodiante ou observador.
- Recuperação de acesso: realizada pela própria pessoa por meio de identidade
  verificada. Davi pode administrar o estado das contas, mas não visualizar senhas
  ou segredos.
- Auditoria de segurança: login, recuperação, alterações de permissão e acessos
  privilegiados devem ser registrados.
- Desativação: a saída de uma atleta causa a desativação da conta, preservando o
  histórico autorizado.

- Impersonação: nenhum perfil pode assumir silenciosamente a identidade de outro
  usuário.
- Justificativas: são dados pessoais restritos à própria atleta e a Davi; serão
  opcionais, minimizadas, preservadas por autoria e histórico e nunca serão
  exibidas nas listas de convocação, nas listas de confirmadas para treino ou a
  outras atletas.
- Interpretação: ausência de justificativa, escolha por não informar, resposta
  incerta, não resposta ou categoria informada não poderá gerar automaticamente
  rótulo de comprometimento, disciplina, confiabilidade ou problema individual.
- Composição operacional compartilhável: atletas autorizadas poderão consultar a
  lista vigente de convocação e a lista de confirmadas para treino. A projeção
  compartilhada será separada da declaração individual completa e limitada a
  nome, função ou posição autorizada, estado mínimo necessário, compromisso e
  vigência.
- Lista de treino: representa previsão baseada nas confirmações vigentes; não
  comprova presença real. Atletas que responderam não, incerta ou não
  responderam não terão esses estados expostos coletivamente, salvo decisão
  futura específica.

### 10.2 Restrições desconhecidas ou pendentes

Privacidade e legislação — `DEC-014` APROVADA como modelo mínimo de governança:
o Centro de Prática de Esportes de Areia é controlador candidato, sujeito a
confirmação documental; Davi é responsável operacional, sem se tornar
automaticamente controlador pessoal ou encarregado; a PWA deverá possuir canal
Privacidade e meus dados, inventário das operações, hipóteses legais por
finalidade, aviso de privacidade, processo de direitos, retenção e eliminação,
avaliação de fornecedores e transferências, segurança, resposta a incidentes e
triagem de RIPD. Dados reais permanecerão bloqueados até atendimento verificável
do portão de produção.

- `ORÇAMENTO_CONFIRMADO_HUMANO`: custo incremental obrigatório de
  desenvolvimento e operação igual a R$ 0. Não poderão ser contratados novos
  serviços pagos, consumo por API, créditos avulsos ou assinaturas específicas
  para a PWA. Serviços gratuitos ou benefícios já disponíveis somente poderão
  ser usados enquanto não gerarem cobrança e atenderem aos requisitos aprovados.
  Condição de revalidação do orçamento: sempre que surgir necessidade de
  contratação de novo serviço pago ou antes de iniciar cada fase posterior ao
  núcleo inicial.
- `PLANEJAMENTO_APROVADO_PELA_DEC`-016: a implementação da primeira fase terá
  horizonte-base de 24 semanas contado a partir de D0, data de início formal
  registrada somente após preparação do repositório, documentação inicial,
  fornecedores e capacidade do primeiro ciclo. O horizonte é previsão
  controlada, não promessa irrevogável; entrada em produção depende dos portões
  e pode ultrapassar a semana 24 sem redução de segurança, privacidade, testes
  ou documentação.
- `CAPACIDADE_CONFIRMADA_HUMANO` E REGULADA PELA `DEC-016`: Davi Sermenho
  desenvolverá e manterá a PWA individualmente. A capacidade-base de
  planejamento é 8 horas semanais em média móvel de quatro semanas, com faixa
  normal de 6 a 10 horas e limite excepcional de 12 horas. Média inferior a 6
  horas por duas semanas consecutivas exige replanejamento; pausas não geram
  compensação obrigatória. Após produção, no mínimo 2 horas semanais em média
  mensal serão reservadas para operação e manutenção. Claude Code e Codex
  permanecem assistentes sob revisão de Davi e não contam como equipe ou
  continuidade humana.
  Condição de revalidação da capacidade: em cada revisão de marco M0-M6 ou
  quando a média móvel de quatro semanas indicar redução sustentada superior a
  30% da capacidade-base aprovada.
- `CONTINUIDADE_ADITADA_PELA_DEC`-016-A: a continuidade será proporcional ao
  projeto solo. Permanecem obrigatórios backup, restauração testada, código e
  migrações versionados, documentação técnica, proteção das credenciais e
  códigos de recuperação de Davi, plano simples de contingência e retorno manual
  controlado. Não serão exigidos custodiante institucional, conta emergencial,
  acesso técnico de terceiros previamente configurado, recuperação institucional
  programada, teste de continuidade sem Davi ou pacote corporativo de
  continuidade. Quando Davi ou a PWA estiverem indisponíveis, a equipe poderá
  usar temporariamente o WhatsApp para a atividade imediata, sem transformar
  esse canal em fluxo normal ou integração da aplicação. Não haverá suporte 24
  horas nem SLA; incidentes críticos suspendem a operação afetada até validação.
- Hardware e navegadores suportados: smartphones de Davi e das atletas;
  computador ou notebook de Davi; Chrome no Android; Safari no iPhone/iPad;
  Chrome e Edge em computadores. Não há necessidade de hardware dedicado.
- Conectividade mínima: conexão com a internet é obrigatória para registrar,
  alterar, confirmar e sincronizar dados.

Funcionamento offline aprovado e detalhado pela `DEC-015`: somente leitura de
snapshot local opcional, criptografado e vinculado a dispositivo pessoal
confiável, sempre com aviso de possível desatualização, horário da última
sincronização, validade limitada e eliminação no logout, revogação ou expiração.
O snapshot não conterá segredos, dados administrativos, avaliações ou
justificativas de outras atletas. Se a proteção criptográfica não puder ser
comprovada por testes, os dados pessoais offline permanecerão desabilitados.

Escrita offline: não permitida na primeira fase.

Regra de atualidade: dados locais desatualizados nunca devem ser apresentados
como atuais.

- Regra de sincronização: a sincronização deve preservar autoria, ordem temporal
  e estado; dados locais desatualizados não podem sobrescrever dados já
  validados.
- `ARQUITETURA_APROVADA_PELA_DEC`-015: frontend React, TypeScript e Vite como
  PWA estática hospedada no plano gratuito do Cloudflare Pages; PostgreSQL,
  Supabase Auth, Data API, Row Level Security e funções SQL controladas no plano
  gratuito do Supabase, com produção na região de São Paulo e projeto separado
  de homologação contendo somente dados sintéticos; Brevo SMTP gratuito somente
  para convite, confirmação, recuperação e alertas de segurança; repositório
  privado e automações controladas no GitHub, sem gasto automático. Cadastro
  público ficará desabilitado; contas serão criadas por convite ou
  administração; MFA TOTP será obrigatória para Davi e acessos privilegiados.
  Gratuidade, cotas e termos deverão ser revalidados antes da produção e
  periodicamente; perda de compatibilidade bloqueará o componente ou reabrirá a
  decisão, nunca gerará cobrança automática.
- Integrações externas — `DEC-010` APROVADA E ADITADA PELA `DEC-012`: a primeira
  fase não depende de sincronização automática com Google Sheets, Google Drive,
  mensageria, documentos oficiais, scout, vídeo ou outros sistemas. A PWA é o
  canal obrigatório das atletas; WhatsApp, e-mail, planilhas, formulários e
  outros aplicativos ficam excluídos do fluxo operacional obrigatório delas.
  Dependências técnicas específicas de fornecedores, APIs, webhooks e formatos
  permanecem decisões de implementação posteriores e não podem reduzir as regras
  aprovadas. A aplicação não utilizará APIs da OpenAI ou da Anthropic.

</product_definition>

<governance>

## 11. Pendências, contradições e decisões

### 11.1 Decisões de produto

#### `DEC-002`

- **Status:** RESOLVIDA
- **Descrição e Detalhes:** Nome canônico: CEPRAEA BEACH PRO; código:
  PWA-CEPRAEA-BEACH-PRO; versão conceitual: 0.1; responsável: Davi Sermenho;
  organização de referência: CEPRAEA; estágio: descoberta e definição de
  contexto.

#### `DEC-003`

- **Status:** APROVADA
- **Descrição e Detalhes:** Davi é o usuário principal da PWA e as atletas são
  usuárias secundárias.

#### `DEC-003-A`

- **Status:** APROVADA
- **Descrição e Detalhes:** Davi pode visualizar, registrar, corrigir e validar
  os dados operacionais necessários; manter o elenco; planejar treinos e
  competições; analisar disponibilidade e cobertura; emitir convocações e
  orientações; registrar decisões, participação e resultados; e acessar
  indicadores internos.

#### `DEC-003-B`

- **Status:** APROVADO E ADITADO PELA `DEC-013`
- **Descrição e Detalhes:** Cada atleta pode visualizar as informações que lhe
  dizem respeito; responder somente às próprias solicitações; declarar,
  confirmar, recusar ou indicar incerteza conforme o tipo de atividade;
  justificar opcionalmente o próprio status; alterar a resposta dentro das
  regras e prazos; consultar a resposta vigente, o próprio histórico e os
  próprios registros autorizados; e solicitar correção posterior sem apagar a
  declaração original.

#### `DEC-003-C`

- **Status:** APROVADO
- **Descrição e Detalhes:** A atleta não pode alterar decisões de Davi,
  respostas de outras atletas, registros oficiais, avaliações sensíveis ou
  informações internas sem autorização explícita.

#### `DEC-003-D`

- **Status:** APROVADO E ADITADO PELA `DEC-014`
- **Descrição e Detalhes:** Criticidade interna, lacunas táticas restritas,
  avaliações, justificativas, motivos pessoais, histórico completo, pendências
  individuais, contatos e dados sensíveis ficam limitados à própria atleta e a
  Davi. Atletas autorizadas podem visualizar somente projeções operacionais
  mínimas vinculadas a compromisso específico: lista vigente de convocação e
  lista de confirmadas para treino.

#### `DEC-003-E`

- **Status:** RESOLVIDA PELAS `DEC-008` E `DEC-017`
- **Descrição e Detalhes:** Davi é o único administrador e mantenedor da
  primeira fase. Não serão criados perfis separados de mantenedor, suporte,
  representante, custodiante ou observador. Autenticação, recuperação e
  auditoria seguem as regras aplicáveis da `DEC-008`.

#### `DEC-004`

- **Status:** APROVADA
- **Descrição e Detalhes:** `CAP-01`, `CAP-02`, `CAP-03`, `CAP-04`, `CAP-05`,
  `CAP-06`, `CAP-07`, `CAP-08`, `CAP-09`, `CAP-10` e `CAP-12` têm finalidade
  preservada com os tratamentos registrados na seção 6. `CAP-11` fica adiada até
  a `DEC-006`.

#### `DEC-005`

- **Status:** APROVADA E ADITADA PELAS `DEC-012`, `DEC-013` E `DEC-014`
- **Descrição e Detalhes:** A primeira fase inclui `CAP-01`, `CAP-02`, `CAP-03`,
  `CAP-04`, `CAP-05`, `CAP-07`, `CAP-10` e `CAP-12`, presença e participação
  reais separadas das declarações. O núcleo inclui comunicação interna, caixa
  individual, solicitações, justificativa opcional, estados semânticos
  distintos, prazo, fechamento, histórico, correção auditável, indicadores
  descritivos, lista vigente de convocação e lista de confirmadas para treino
  como composição prevista. Canais externos serão substituídos. `CAP-06`,
  `CAP-08`, `CAP-09` e `CAP-11` permanecem posteriores. Os critérios
  `CRIT-FASE1-001` a `CRIT-FASE1-016` e as condições aditadas dos `OBJ-002`,
  `OBJ-003`, `OBJ-005`, `OBJ-006` e `OBJ-007` definem a conclusão funcional do
  núcleo inicial.

#### `DEC-006`

- **Status:** APROVADA
- **Descrição e Detalhes:** Scout, vídeo, finanças e publicação de conteúdo
  público pertencem a sistemas ou canais separados. O CEPRAEA BEACH PRO poderá
  consumir dados validados de scout ou manter referências autorizadas de vídeo
  somente mediante integração futura aprovada. Feedback individual pertence ao
  produto como módulo de fase posterior, condicionado às decisões de
  autenticação, acesso e privacidade. Publicação automática não é autorizada.

#### `DEC-007`

- **Status:** APROVADA
- **Descrição e Detalhes:** O produto será uma PWA responsiva e instalável,
  usada principalmente nos smartphones de Davi e das atletas e administrada
  também por computador ou notebook de Davi. São suportados Chrome no Android,
  Safari no iPhone/iPad e Chrome e Edge em computadores. O uso ocorrerá em
  treinos, competições, deslocamentos e administração remota. A internet é
  obrigatória para registrar, alterar, confirmar e sincronizar dados. Offline, a
  primeira fase permite apenas a leitura do último estado sincronizado, sempre
  com aviso de possível desatualização e horário da última sincronização;
  escrita offline não é permitida. Dados desatualizados nunca podem aparecer
  como atuais nem sobrescrever dados validados. Não há hardware dedicado e
  aplicativo nativo fica fora da primeira fase.

#### `DEC-008`

- **Status:** APROVADA, ADITADA PELAS `DEC-013` E `DEC-017` E IMPLEMENTADA
  TECNICAMENTE PELA `DEC-015`
- **Descrição e Detalhes:** Cada pessoa usará conta individual com identidade
  verificada; contas compartilhadas, edição por link e acesso anônimo não são
  permitidos. Davi administrará acessos sem visualizar credenciais. Cada atleta
  terá conta limitada aos próprios dados e informações autorizadas. A primeira
  fase terá somente contas de Davi e das atletas; não haverá perfil separado de
  mantenedor, suporte, representante, custodiante ou observador. Recuperação,
  MFA de Davi, desativação e proibição de impersonação permanecem obrigatórias.
  Cada resposta, justificativa, alteração, fechamento, correção administrativa e
  contestação registrará autoria, data e histórico. A autenticação inicial
  utilizará Supabase Auth com e-mail e senha, cadastro público desabilitado,
  criação por convite ou administração, recuperação individual e revogação de
  sessões. Brevo SMTP será usado somente para mensagens de identidade, sujeito
  aos portões da `DEC-014` e `DEC-015`.

#### `DEC-009`

- **Status:** APROVADA E ADITADA PELAS `DEC-013` E `DEC-014`
- **Descrição e Detalhes:** Davi acessa os dados necessários; cada atleta acessa
  os próprios dados, respostas, justificativas, histórico e registros
  autorizados. Justificativas permanecem restritas à atleta e a Davi, opcionais,
  minimizadas e vedadas a ranking, exposição coletiva ou avaliação automática.
  Como exceção de finalidade esportiva, atletas autorizadas podem ver a
  composição operacional mínima de compromisso específico: lista vigente de
  convocação e lista de confirmadas para treino, com nome, função ou posição
  autorizada, estado mínimo, compromisso e vigência. Não serão exibidos
  justificativa, motivo, resposta negativa ou incerta, ausência de resposta,
  histórico completo, contato, pendência individual, avaliação ou dado sensível.
  A lista de treino é previsão e não presença real. Retenções aprovadas
  permanecem. Dados reais não entram em ferramentas de IA; nenhuma regra
  automática pode inferir motivo, comprometimento, disciplina, confiabilidade,
  saúde, condição psicológica ou desempenho. A governança e o portão de produção
  seguem a `DEC-014`.

#### `DEC-010`

- **Status:** APROVADA E ADITADA PELAS `DEC-012` E `DEC-013`
- **Descrição e Detalhes:** A PWA será a fonte operacional canônica após
  migração validada e não manterá sincronização contínua ou bidirecional com
  planilhas. Google Sheets, Google Drive, e-mail, WhatsApp, formulários e
  documentos antigos serão apenas fontes de migração, conferência, preservação
  histórica ou referência de Davi. Toda solicitação, comunicação, confirmação,
  resposta, justificativa, disponibilidade e consulta obrigatória das atletas
  ocorrerá dentro da PWA. Importações exigirão prévia, origem, data, validação,
  detecção de duplicidade, resultado e possibilidade de rejeição. Respostas
  históricas que contenham somente sim, não ou talvez serão preservadas como
  foram registradas; o processo de migração não poderá inventar justificativas,
  reinterpretar talvez como não nem criar fatos posteriores inexistentes.
  Documentos oficiais só produzirão fatos após validação; OCR, extração ou IA
  não são fonte de verdade. A aplicação não lerá conversas pessoais nem usará
  APIs da OpenAI ou Anthropic. Integrações futuras exigirão decisão específica,
  minimização, proveniência, segurança, prevenção de sobrescrita, auditoria e
  tratamento de falhas.

#### `DEC-011`

- **Status:** APROVADA INTEGRALMENTE E ADITADA PELAS `DEC-012`, `DEC-013` E
  `DEC-014`
- **Descrição e Detalhes:** Os objetivos `OBJ-001` a `OBJ-007` permanecem
  aprovados. O `OBJ-002` preserva resposta e versões; o `OBJ-003` separa
  declaração e fato; o `OBJ-005` proíbe julgamento automático; o `OBJ-006`
  inclui comunicação interna, lista vigente de convocação e lista de confirmadas
  para treino com visibilidade mínima e sem justificativas; e o `OBJ-007` exige
  reconstrução completa. A Fase 1 corresponde aos critérios `CRIT-FASE1-001` a
  `CRIT-FASE1-016`. Fases posteriores dependem de estabilidade, segurança,
  privacidade, rastreabilidade e custo zero. Metas numéricas aguardam linha de
  base; incidentes bloqueiam conclusão até tratamento. NOVAS PREMISSAS
  INCORPORADAS PELA `DEC-012`: escala inicial de 19 atletas mais Davi; canal
  operacional das atletas integralmente dentro da PWA; substituição de WhatsApp,
  e-mail, planilhas, formulários e outros aplicativos no fluxo obrigatório das
  atletas; custo incremental obrigatório R$ 0; desenvolvimento e manutenção solo
  por Davi; uso controlado de Claude Code e Codex por extensões do VS Code como
  assistentes de desenvolvimento; proibição de APIs da OpenAI e da Anthropic na
  aplicação; uso exclusivo de dados sintéticos ou anonimizados pelos agentes; e
  independência operacional da PWA em relação a esses agentes. Os aditamentos às
  `DEC-005`, `DEC-010` e `DEC-011` estão aprovados.

#### `DEC-012`

- **Status:** REESCRITA, APROVADA INTEGRALMENTE E COMPLEMENTADA PELAS `DEC-013`
  E `DEC-014`
- **Descrição e Detalhes:** O CEPRAEA BEACH PRO será o canal operacional
  canônico entre Davi e as atletas. Leitura, ciência, respostas,
  disponibilidade, compromissos, convocações, orientações, prazos e pendências
  ocorrerão na PWA. A caixa individual apresentará opções, justificativa
  opcional, resposta vigente, prazo, fechamento e histórico. O produto também
  apresentará, com visibilidade controlada, a lista vigente de convocação e a
  lista de confirmadas para treino. Custo zero, escala, desenvolvimento solo,
  serviços gratuitos, limites dos agentes e proibição das APIs da OpenAI e
  Anthropic permanecem. A decisão não seleciona arquitetura nem autoriza dados
  reais antes do portão da `DEC-014`.

#### `DEC-013`

- **Status:** APROVADA INTEGRALMENTE E COMPLEMENTADA PELA `DEC-014`
- **Descrição e Detalhes:** A primeira fase adotará modelo geral de
  solicitações, respostas, justificativas e fatos posteriores. Estados
  distintos, justificativa opcional, minimização, histórico, correção separada,
  distinção entre declaração e fato e proibição de julgamento automático
  permanecem. A declaração completa e a justificativa continuam restritas à
  atleta e a Davi; delas poderá ser derivada somente projeção operacional mínima
  autorizada para lista de convocação ou lista de confirmadas para treino. Davi
  controla publicação e vigência; lista de treino não comprova presença. A
  decisão adita as `DEC-003`, `DEC-005`, `DEC-008`, `DEC-009`, `DEC-010`,
  `DEC-011` e `DEC-012`.

#### `DEC-014`

- **Status:** APROVADA INTEGRALMENTE, COM AJUSTE DE VISIBILIDADE OPERACIONAL
- **Descrição e Detalhes:** Aprova o modelo mínimo de governança de privacidade.
  Centro de Prática de Esportes de Areia é controlador candidato, sujeito a
  confirmação documental; Davi é responsável operacional, sem se tornar
  automaticamente controlador pessoal ou encarregado. A PWA deverá oferecer a
  área Privacidade e meus dados, atendimento para titulares e ex-atletas,
  inventário das operações, hipótese legal por finalidade, aviso de privacidade,
  retenção e eliminação, avaliação de fornecedores e transferências
  internacionais, segurança, resposta a incidentes e triagem de RIPD. Dados
  reais ficam bloqueados até comprovação do portão de produção: controlador e
  representante confirmados, bases legais, canal de direitos, fornecedores,
  transferências, permissões, backup e restauração, eliminação e exportação,
  isolamento das ferramentas de IA e tratamento de riscos. Justificativas
  permanecem privadas. Atletas autorizadas podem consultar a lista vigente de
  convocação e a lista de confirmadas para treino, limitadas a nome, função ou
  posição autorizada, estado mínimo, compromisso e vigência. Não serão exibidos
  justificativas, motivos pessoais, histórico completo, contato, pendências
  individuais, avaliações ou dados sensíveis. Estados não, incerta e não
  respondida não serão expostos coletivamente. Lista de treino é previsão, não
  presença. A decisão adita as `DEC-003`, `DEC-005`, `DEC-009`, `DEC-011`,
  `DEC-012` e `DEC-013`; não confirma conformidade integral, não escolhe
  fornecedor ou arquitetura e não autoriza dados reais antes do portão.

#### `DEC-015`

- **Status:** APROVADA INTEGRALMENTE
- **Descrição e Detalhes:** A primeira fase utilizará React, TypeScript e Vite
  para a PWA estática; Cloudflare Pages gratuito para o frontend; Supabase
  gratuito para PostgreSQL, Auth, Data API, RLS e funções SQL controladas, com
  produção em São Paulo e homologação separada apenas com dados sintéticos;
  Brevo SMTP gratuito somente para identidade; e repositório privado com
  automações controladas no GitHub. Não haverá servidor próprio, cadastro
  público, chave administrativa no cliente, backend tradicional obrigatório,
  upload de arquivos ou push obrigatório na primeira fase. RLS e testes
  negativos deverão isolar atletas e impedir justificativas em listas
  compartilhadas. MFA TOTP será obrigatória para Davi e acessos privilegiados. A
  central interna de notificações será canônica. Offline será somente leitura
  por snapshot opcional criptografado; sem prova de segurança, dados pessoais
  offline ficarão desabilitados. Haverá backup lógico diário criptografado,
  cópia local e em Drive restrito, retenção de 7 diários, 4 semanais e 3
  mensais, teste de restauração e procedimento de saída dos fornecedores. Logs
  serão minimizados; cotas, pausa, gratuidade e termos serão monitorados;
  nenhuma cobrança ou upgrade automático será permitido. Dados reais dependem do
  portão jurídico da `DEC-014` e de evidências técnicas de separação de
  ambientes, recuperação, MFA, RLS, backup, restauração, segurança, cotas e
  portabilidade. A decisão não define prazo nem autoriza produção imediata.

#### `DEC-016`

- **Status:** APROVADA INTEGRALMENTE
- **Descrição e Detalhes:** A capacidade-base de Davi será 8 horas semanais em
  média móvel de quatro semanas, com faixa normal de 6 a 10 horas e limite
  excepcional de 12 horas; redução sustentada exige replanejamento, sem
  compensação por corte de qualidade. O horizonte-base da primeira fase será de
  24 semanas após D0, organizado nos marcos M0 preparação; M1 fundação e
  identidade; M2 elenco, compromissos e respostas; M3 convocação, listas e
  fatos; M4 comunicação, privacidade e auditoria; M5 backup, restauração e
  segurança; e M6 validação, piloto e corte. Conclusão exige funcionalidade,
  testes, autorização, documentação, segurança e rastreabilidade. Mudanças de
  escopo deverão substituir esforço, deslocar prazo ou permanecer para fase
  posterior. Após produção, serão reservadas no mínimo 2 horas semanais em média
  mensal para manutenção. Ocorrências serão classificadas de P0 a P3; P0
  suspende a operação afetada. A continuidade foi aditada pela `DEC-016-A`:
  permanecem backup, restauração testada, documentação, proteção das credenciais
  de Davi, contingência temporária por WhatsApp e retorno manual controlado;
  deixam de ser exigidos custodiante, conta emergencial, acesso técnico de
  terceiros, recuperação institucional programada e teste sem Davi. A decisão
  não fixa data de lançamento antes de D0, não cria SLA, não autoriza substituto
  a decidir esportivamente e não libera dados reais antes dos portões.

#### `DEC-016-A`

- **Status:** APROVADA INTEGRALMENTE
- **Descrição e Detalhes:** Adita a `DEC-016` e simplifica a continuidade para a
  escala real do projeto. Retira custodiante obrigatório, conta emergencial,
  perfil de suporte ou mantenedor externo, botão do pânico, acesso técnico de
  terceiros previamente configurado, recuperação institucional programada, MFA
  emergencial, teste de continuidade sem Davi e pacote corporativo de
  continuidade. Mantém código e migrações versionados, backup e restauração
  documentados e testados, exportação, documentação técnica, proteção das
  credenciais e códigos de recuperação por Davi, contingência temporária por
  WhatsApp e retorno manual controlado à PWA. A primeira fase continua limitada
  aos perfis Davi e atleta. A emenda não altera capacidade, horizonte, marcos,
  manutenção, piloto, qualidade, segurança, privacidade ou os demais portões.

#### `DEC-017`

- **Status:** APROVADA INTEGRALMENTE
- **Descrição e Detalhes:** A primeira fase terá somente dois perfis
  operacionais: Davi e atleta, com RLS baseada nesses dois contextos. Davi
  permanece treinador, autoridade esportiva, administrador e mantenedor; cada
  atleta acessa somente os próprios dados e as listas mínimas autorizadas.
  Ex-atletas não terão perfil operacional e exercerão direitos sobre os próprios
  dados por canal externo apropriado. Cloudflare, Supabase, Brevo, GitHub e
  Google Drive são fornecedores de infraestrutura, não usuários. Federações,
  confederações, ligas, organizadores e documentos oficiais são fontes ou
  destinos externos tratados por Davi, sem conta ou integração automática.
  Público, familiares, imprensa, patrocinadores, apoiadores e parceiros ficam
  fora da PWA operacional. A decisão não cria RBAC adicional, perfis técnicos,
  painel institucional, conta de emergência, conta de observador nem novos
  módulos. A simplificação da continuidade foi formalizada pela `DEC-016-A`.

#### `DEC-018`

- **Status:** APROVADA INTEGRALMENTE
- **Descrição e Detalhes:** Aprova linha de base proporcional coletada durante
  quatro semanas de operação real ou três ciclos completos, com registro manual
  simples e sem sistema obrigatório de BI ou telemetria. Aprova os indicadores
  `IND-001` a `IND-010`: fontes externas consultadas, tempo de preparação,
  divergências operacionais, pendências após o prazo, cobranças manuais,
  registros sem rastreabilidade, erros de visibilidade, erros semânticos,
  conclusão do fluxo pela atleta e falhas críticas. Aprova metas iniciais de
  redução de fontes, tempo e cobranças, conclusão das respostas dentro da PWA,
  autonomia das atletas, rastreabilidade integral, isolamento por RLS e zero
  falha crítica aberta. A validação seguirá V0 documental, V1 sintética, V2
  piloto controlado com cinco a oito atletas por dois ciclos e V3 com o elenco
  completo em ciclo de baixo risco. A promoção para DECISAO-CEPRAEA — VERSÃO
  CANDIDATA 0.1 dependerá de revisão e autorização expressa separada de Davi; a
  aprovação desta decisão não inicia D0, não autoriza dados reais, piloto ou
  produção e não cria novo módulo funcional.

### 11.2 Correções da operação atual que não podem ser confundidas com requisitos

- `CORR-001` — Sincronizar o retorno confirmado de Gilvania no cadastro
  estruturado e nas representações aplicáveis.
- `CORR-002` — Separar disponibilidade declarada de presença real.
- `CORR-003` — Unificar estados e vocabulário.
- `CORR-004` — Remover atores inexistentes do conteúdo e das mensagens.
- `CORR-005` — Corrigir fórmulas quebradas e painéis vencidos.
- `CORR-006` — Resolver identificadores duplicados e pendências de logs.
- `CORR-007` — Revisar permissões de edição e política de comentários.

### 11.3 Desconhecidos e pendências de evidência

- `DES-001` — RESOLVIDO. CEPRAEA é o nome fantasia cadastrado de Centro de
  Prática de Esportes de Areia, CNPJ 19.993.964/0001-06, natureza jurídica
  Associação Privada.
- `DES-002` — RESOLVIDO PELAS `DEC-012`, `DEC-016` E `DEC-016-A`. Orçamento
  incremental permanece R$ 0; desenvolvimento e manutenção pertencem a Davi em
  atuação solo; capacidade-base de 8 horas semanais, horizonte de 24 semanas
  após D0, marcos M0 a M6, reserva de manutenção, replanejamento e classificação
  de ocorrências estão aprovados. A continuidade foi simplificada para backup e
  restauração documentados e testados, proteção das credenciais por Davi,
  contingência temporária por WhatsApp e retorno manual controlado, sem
  custodiante, conta emergencial, acesso técnico de terceiros previamente
  configurado, recuperação institucional programada ou teste sem Davi.
- `DES-003` — RESOLVIDO EM NÍVEL DECISÓRIO PELA `DEC-014`. O modelo de
  governança, papéis candidatos, canal de direitos, inventário, bases legais por
  operação, fornecedores, transferências, aviso, retenção, incidentes, RIPD,
  visibilidade e portão de produção estão aprovados. Permanecem como obrigações
  de implementação e evidência antes de dados reais: confirmar controlador e
  representante, documentar encarregado ou dispensa, concluir inventário e bases
  legais, avaliar fornecedores, testar segurança, backup, restauração,
  exportação, eliminação e fechar o portão de produção.
- `DES-004` — RESOLVIDO EM NÍVEL DECISÓRIO PELA `DEC-015`. A arquitetura inicial
  seleciona Cloudflare Pages, Supabase/PostgreSQL/Auth/RLS na região de São
  Paulo, Brevo SMTP de identidade, GitHub privado, ambientes separados, central
  interna de notificações, snapshot offline somente leitura condicionado à
  criptografia, backup diário criptografado, restauração testada,
  observabilidade mínima, monitoramento de cotas e saída dos fornecedores.
  Permanecem obrigações de implementação e evidência antes de dados reais,
  incluindo testes de autorização, recuperação, MFA, backup, restauração,
  segurança, cotas, portabilidade e fechamento conjunto dos portões das
  `DEC-014` e `DEC-015`.
- `DES-005` — RESOLVIDO EM NÍVEL DECISÓRIO PELA `DEC-018`. A linha de base, os
  indicadores `IND-001` a `IND-010`, as metas iniciais, os níveis V0 a V3, o
  piloto controlado, os critérios funcionais, de usabilidade, segurança e
  privacidade e os critérios de promoção documental estão aprovados. Permanecem
  como atividades futuras a coleta da linha de base, a execução dos testes e
  pilotos, a produção das evidências e a autorização expressa de promoção.
- `DES-006` — RESOLVIDO PELA `DEC-017`. Os únicos perfis operacionais da
  primeira fase são Davi e atleta. Ex-atletas mantêm direitos sobre os próprios
  dados sem conta operacional; fornecedores são infraestrutura; entidades
  esportivas externas são fontes ou destinos tratados por Davi; e público,
  familiares, imprensa, patrocinadores, apoiadores e parceiros ficam fora da
  PWA.
- `DES-007` — `DESCONHECIDO` — condições físicas dos ambientes de uso
  (luminosidade, ruído, temperatura e restrições de mobilidade) em treinos,
  competições e deslocamentos não foram documentadas. O levantamento permanece
  pendente e não foi tratado pela promoção documental como fato conhecido.
- `DES-008` — `DESCONHECIDO` — padrão de uso temporal (horários habituais,
  frequência de sessões por semana, duração típica de uso por sessão, picos de
  utilização e janelas operacionais críticas) não documentado. O levantamento
  permanece pendente e não foi tratado pela promoção como fato conhecido.
- `DES-009` — `DESCONHECIDO` — condições humanas dos usuários (experiência
  prévia com ferramentas similares, necessidade de treinamento, carga cognitiva
  em contexto de uso, acessibilidade e pressão de tempo durante operação) não
  documentadas. O levantamento permanece pendente e não foi tratado pela
  promoção como fato conhecido.

### 11.4 Contradições controladas

- `CON-001` — elenco na interface versus elenco no database. Decisão humana
  sobre o retorno existe; sincronização permanece pendente.
- `CON-002` — disponibilidade versus presença real.
- `CON-003` — RESOLVIDA PELA `DEC-013`. Solicitações usam um modelo geral com
  estados específicos por tipo; incerta, não e não respondida permanecem
  distintas, e declaração anterior não é convertida em fato posterior.
- `CON-004` — Davi e atletas versus comissão, coordenação e papéis obsoletos.
- `CON-005` — fonte estruturada pretendida versus entradas manuais e documentos
  com autoridades específicas.
- `CON-006` — painel atualizado tecnicamente versus conteúdo esportivo vencido.
- `CON-007` — RESOLVIDA PELA `DEC-015`. A arquitetura inicial, os fornecedores,
  os ambientes e os controles técnicos foram selecionados sem alterar a
  autoridade esportiva, os papéis humanos ou os limites de acesso aprovados.
- `CON-008` — RESOLVIDA PELA `DEC-012`. A `DEC-010` foi aditada: materiais e
  canais externos não compõem o fluxo obrigatório das atletas; toda comunicação,
  confirmação e resposta operacional obrigatória ocorre dentro da PWA.
- `CON-009` — TRATADA PELA `DEC-015`, COM RISCO RESIDUAL ACEITO. A arquitetura
  utiliza somente camadas gratuitas, sem cobrança ou upgrade automático, com
  monitoramento de cotas, backup próprio, portabilidade e substituição. Mudança
  de termos, perda de gratuidade, pausa ou insuficiência de limites bloqueará o
  componente ou reabrirá a decisão; a operação gratuita não possui SLA nem
  garantia de continuidade.
- `CON-010` — RESOLVIDA PELA `DEC-013`. Justificativa fornece contexto
  operacional, mas não comprova comprometimento, disciplina, confiabilidade,
  legitimidade do motivo ou problema pessoal; qualquer interpretação permanece
  humana e sob autoridade de Davi.

## 12. Registro mínimo de fontes

- `SRC-001` — confirmação humana de Davi: composição do CEPRAEA, autoridade
  exclusiva interna, retorno de Gilvania e aprovação das decisões `DEC-002` a
  `DEC-018`, incluindo a `DEC-016-A`. Inclui escala 19 mais 1; fluxo integral na
  PWA; custo R$ 0; desenvolvimento solo; limites dos agentes e ausência de APIs
  da OpenAI e Anthropic; modelo de respostas e justificativas; distinção entre
  estados e fatos; proibição de julgamento automático; governança e portão de
  dados reais; visibilidade operacional mínima; arquitetura gratuita com
  Cloudflare Pages, Supabase/PostgreSQL/Auth/RLS em São Paulo, Brevo SMTP,
  GitHub privado, ambientes separados, backup próprio, restauração,
  monitoramento de cotas e portabilidade; planejamento de 8 horas semanais,
  horizonte de 24 semanas após D0 e marcos M0 a M6; continuidade proporcional
  sem custodiante ou conta emergencial; somente dois perfis operacionais, Davi e
  atleta; e linha de base proporcional, indicadores `IND-001` a `IND-010`, metas
  iniciais, validação V0 a V3, piloto controlado e critérios de promoção
  documental sem autorização automática de dados reais, piloto ou produção.
- `SRC-002` — DECISAO-CEPRAEA atual. Arquivo
  1JjFf_AstkZwp3K2RcnZGD0GTjLVqA_jAwlSdtKlrnpg. Uso: rascunho e evidência de
  entendimento; não é fonte soberana.
- `SRC-003` — `CEPRAEA_CONTRACT`.gdoc. Arquivo
  1EXWEC1ULPvUgtYCFKqrSJ4j4UBZi_bsHGgulie01T-s. Uso: governança da operação de
  planilhas, sujeito a vocabulário obsoleto e decisões posteriores.
- `SRC-004` — CEPRAEA JUNHO 2026. Arquivo
  14d3vIfkvhkTvjjTxkM7CxA9Oo1etHAgC2KUzGzzEn88. Uso: interface, entrada humana e
  evidência do AS-IS.
- `SRC-005` — CEPRAEA DATABASE. Arquivo
  10Dv1oBIKdodWEWsK8qUeLPyazzdg4hdRkVi4gjvVSno. Uso: dados estruturados por
  assunto, sujeito a divergências com decisão humana mais recente.
- `SRC-006` — documentos oficiais específicos. Uso: relação nominal, calendário,
  competição, partida e resultado conforme o evento.
- `SRC-007` — MODELAGEM_ATTENDANCE_CEPRAEA_v0.1. Arquivo
  1pRR6xrw_XUEWi65I01w27Bex7b0LFZCq8hK5AxFR83U. Uso: proposta, não decisão
  aprovada.
- `SRC-008` — Engenharia Documentação. Arquivo
  1Hyl3peGP6ZDS4Wm6T8t7EKJChleGB_kePiSjcLJRkxI. Uso: referência metodológica em
  estado de rascunho.
- `SRC-009` — PROTOCOLO OPERACIONAL DE RISCOS DE IA. Arquivo
  12cSXeFFZnm8-RN1W8ttrfzmRoSNCmyxz_UXKkAwGBsE. Uso: controles e gates da
  elaboração.
- `SRC-010` — conteúdos psicológicos e avaliações individuais. Uso: restrito;
  excluídos do contexto geral.
- `SRC-011` — comprovante fornecido por Davi Sermenho. Arquivo
  1LmrmK2NUCOfOd3UZRBhGhTa-rOfTj51C. Uso limitado: confirmar a convergência
  entre o destinatário CEPRAEA e o CNPJ 19.993.964/0001-06. Dados pessoais e
  financeiros são excluídos.
- `SRC-012` — comprovante fornecido por Davi Sermenho. Arquivo
  1YAMDBILE0ibG0eBR4qDrBXAlHDKG0rIF. Uso limitado: confirmar a razão social
  Centro de Prática de Esportes de Areia e o CNPJ 19.993.964/0001-06. Dados
  pessoais e financeiros são excluídos.
- `SRC-013` — Mapa das OSC/IPEA, registro 891031. Uso: confirmar razão social,
  CNPJ, nome fantasia CEPRAEA, natureza jurídica Associação Privada, situação
  ativa e área de atuação esportiva.
- `SRC-014` — Confederação Brasileira de Handebol, cadastro de clube 1021. Uso:
  confirmar a identidade esportiva institucional Centro de Prática de Esportes
  de Areia e registros oficiais de CEPRAEA em competições de handebol de praia.
- `SRC-015` — Instagram público @cepraeabeachhand. Uso: identidade pública e
  marca esportiva; não valida CNPJ, natureza jurídica nem requisitos do produto.
- `SRC-016` — página pública CEPRAEA no Facebook. Uso: identidade pública e
  marca esportiva; não valida CNPJ, natureza jurídica nem requisitos do produto.
- `SRC-017` — documentação oficial do Cloudflare Pages. Uso: hospedagem
  estática, plano gratuito, limites e cabeçalhos; condições devem ser
  revalidadas antes da produção.
- `SRC-018` — documentação oficial do Supabase. Uso: planos e cotas, regiões,
  PostgreSQL, Auth, RLS, MFA, backups, tamanho do banco e pausa de projetos;
  condições devem ser revalidadas antes da produção.
- `SRC-019` — documentação oficial do Brevo. Uso: SMTP e condições do plano
  gratuito; condições devem ser revalidadas antes da produção.
- `SRC-020` — documentação oficial do GitHub. Uso: repositório privado, GitHub
  Actions e controle de gastos; condições devem ser revalidadas antes da
  produção.

## 13. MATRIZ

### `CLAIM-001`

- **Descrição:** CEPRAEA é equipe adulta feminina de handebol de praia.
- **Estado:** `CONFIRMADO_HUMANO` e `CONFIRMADO_FONTE`
- **Fontes / Evidências:** `SRC-001`, `SRC-002`, `SRC-004` e documentos oficiais

### `CLAIM-002`

- **Descrição:** a equipe possui apenas Davi e atletas.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`

### `CLAIM-003`

- **Descrição:** Davi é único responsável técnico e operacional interno.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`

### `CLAIM-004`

- **Descrição:** a operação atual depende de interface, database, entradas
  humanas e documentos.
- **Estado:** `CONFIRMADO_FONTE`
- **Fontes / Evidências:** `SRC-003`, `SRC-004`, `SRC-005` e `SRC-006`

### `CLAIM-005`

- **Descrição:** o problema central é incerteza operacional.
- **Estado:** `INFERENCIA_CONTROLADA` sustentada por problemas observados
- **Fontes / Evidências:** `SRC-002` a `SRC-005`

### `CLAIM-006`

- **Descrição:** retorno de Gilvania está confirmado e o database não representa
  a decisão.
- **Estado:** `CONFIRMADO_HUMANO` mais `PROBLEMA_OBSERVADO`
- **Fontes / Evidências:** `SRC-001`, `SRC-004` e `SRC-005`

### `CLAIM-007`

- **Descrição:** disponibilidade e presença são conceitos distintos.
- **Estado:** `CONFIRMADO_FONTE`
- **Fontes / Evidências:** `SRC-002`, `SRC-003` e `SRC-005`

### `CLAIM-008`

- **Descrição:** convocação, escalação e participação são distintas.
- **Estado:** `CONFIRMADO_FONTE`
- **Fontes / Evidências:** `SRC-002`, `SRC-003`, `SRC-005` e documentos oficiais

### `CLAIM-009`

- **Descrição:** decisões esportivas permanecem com Davi.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`

### `CLAIM-010`

- **Descrição:** propostas técnicas existentes não são requisitos aprovados.
- **Estado:** `CONFIRMADO_POR_AUDITORIA`
- **Fontes / Evidências:** `SRC-007` e `SRC-008`

### `CLAIM-011`

- **Descrição:** permissões de edição por link afetam integridade das fontes
  centrais.
- **Estado:** `PROBLEMA_OBSERVADO`
- **Fontes / Evidências:** metadados de `SRC-003`, `SRC-004` e `SRC-005`

### `CLAIM-012`

- **Descrição:** identidade, escopo da primeira fase, restrições, objetivos,
  indicadores, metas iniciais, condições de sucesso, custo zero, canal interno,
  modelo de respostas, governança de privacidade, arquitetura inicial,
  capacidade, marcos, continuidade proporcional, partes interessadas essenciais,
  protocolo de validação V0 a V3, piloto controlado e critérios de promoção
  documental estão aprovados. Permanecem pendentes a execução da linha de base,
  dos testes, do piloto e das evidências dos portões jurídico, técnico e humano,
  além da autorização expressa de promoção e das autorizações separadas para
  dados reais, piloto e produção.
- **Estado:** `CONFIRMADO_HUMANO` e `CONFIRMADO_POR_AUDITORIA`
- **Fontes / Evidências:** decisões de Davi Sermenho, `SRC-007` e `SRC-008`

### `CLAIM-013`

- **Descrição:** CEPRAEA é o nome fantasia de Centro de Prática de Esportes de
  Areia, CNPJ 19.993.964/0001-06, natureza jurídica Associação Privada e
  situação ativa.
- **Estado:** `CONFIRMADO_FONTE`
- **Fontes / Evidências:** `SRC-011`, `SRC-012` e `SRC-013`

### `CLAIM-014`

- **Descrição:** a CBHb identifica Centro de Prática de Esportes de Areia como
  clube e registra CEPRAEA em competições oficiais de handebol de praia.
- **Estado:** `CONFIRMADO_FONTE`
- **Fontes / Evidências:** `SRC-014`

### `CLAIM-015`

- **Descrição:** os perfis públicos usam as denominações CEPRAEA Beach Hand e
  Cepraea Beach Handball.
- **Estado:** `IDENTIDADE_PUBLICA`; não é prova cadastral nem definição do
  produto
- **Fontes / Evidências:** `SRC-015` e `SRC-016`

### `CLAIM-016`

- **Descrição:** Davi é o usuário principal; atletas respondem somente por si,
  justificam opcionalmente, consultam o próprio histórico e pedem correção sem
  apagar o original. Atletas autorizadas também podem consultar a lista vigente
  de convocação e a lista de confirmadas para treino, sem acesso a
  justificativas ou detalhes individuais restritos.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-003`, `DEC-013` e `DEC-014`

### `CLAIM-017`

- **Descrição:** as doze capacidades atuais possuem tratamento aprovado: onze
  têm a finalidade preservada com correção, substituição, expansão, apoio ou
  controle humano conforme o caso; o feedback individual pertence ao produto
  como módulo de fase posterior.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-004` e `DEC-006`

### `CLAIM-018`

- **Descrição:** a primeira fase possui escopo funcional e dezesseis critérios
  de conclusão: oito capacidades numeradas, fatos separados das declarações,
  respostas estruturadas, justificativa opcional, histórico, proibição de
  rótulos automáticos, lista vigente de convocação, lista de confirmadas para
  treino, ciclo de vigência e exposição mínima.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-005`, `DEC-013` e `DEC-014`

### `CLAIM-019`

- **Descrição:** scout, vídeo, finanças e publicação pública pertencem a
  sistemas separados; feedback individual pertence ao CEPRAEA BEACH PRO como
  módulo de fase posterior condicionado a acesso e privacidade.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-006`

### `CLAIM-020`

- **Descrição:** o ambiente operacional futuro será uma PWA responsiva e
  instalável, compatível com os dispositivos e navegadores aprovados; escrita
  exige conexão, enquanto o modo offline da primeira fase é somente leitura com
  indicação de desatualização e última sincronização.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-007`

### `CLAIM-021`

- **Descrição:** o produto exige contas individuais e identidade verificada;
  Davi administra acessos sem acessar credenciais; perfis técnicos são mínimos e
  auditados; recuperação, desativação, MFA e proibição de impersonação são
  obrigatórias; respostas, justificativas e correções preservam autoria e trilha
  separada.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-008` e `DEC-013`

### `CLAIM-022`

- **Descrição:** a privacidade exige minimização, retenção, autoria e separação
  entre dados individuais restritos e composição operacional compartilhável.
  Justificativas permanecem restritas à atleta e a Davi; listas de convocação e
  treino exibem somente dados mínimos autorizados; dados reais não entram em
  ferramentas de IA; nenhum sistema infere motivo, comprometimento, disciplina,
  confiabilidade ou decisão esportiva final.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-009`, `DEC-013` e `DEC-014`

### `CLAIM-023`

- **Descrição:** não há sincronização contínua com planilhas ou mensagens;
  migrações são controladas; toda solicitação, resposta e justificativa
  obrigatória ocorre dentro da PWA; respostas históricas são preservadas sem
  justificativa inventada ou reinterpretação; documentos externos mantêm
  autoridade própria; futuras integrações exigem decisão, proveniência,
  segurança e tratamento de falhas.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-010`, `DEC-012` e `DEC-013`

### `CLAIM-024`

- **Descrição:** o produto deverá atender inicialmente 19 atletas e 1 treinador,
  centralizar todo o fluxo operacional das atletas dentro da PWA, substituir
  WhatsApp, e-mail, planilhas, formulários e outros aplicativos nesse fluxo,
  operar com custo incremental obrigatório R$ 0 e ser desenvolvido e mantido por
  Davi com uso controlado de Claude Code e Codex no VS Code, sem uso das APIs da
  OpenAI ou da Anthropic na aplicação. A PWA deverá funcionar sem esses agentes,
  que não poderão receber dados reais, credenciais ou segredos.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-012`

### `CLAIM-025`

- **Descrição:** a `DEC-012` reescrita foi aprovada integralmente e aditou as
  `DEC-005`, `DEC-010` e `DEC-011`, tornando obrigatórios o canal operacional
  interno, a experiência integral das atletas na PWA, a caixa individual, os
  estados de comunicação, o custo zero, o desenvolvimento solo e os limites dos
  agentes de codificação.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-012`

### `CLAIM-026`

- **Descrição:** a `DEC-013` aprovou um modelo geral de solicitações, respostas,
  justificativas e fatos posteriores; incerta, não e não respondida são
  distintas; justificativa é opcional e minimizada; declarações e fatos não se
  confundem; o histórico é preservado; e o sistema não produz rótulos
  automáticos. A `DEC-014` complementa o modelo com projeções operacionais
  mínimas para listas autorizadas.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `DEC-013` e `DEC-014`

### `CLAIM-027`

- **Descrição:** a `DEC-014` aprovou governança mínima de privacidade, portão
  verificável para dados reais, canal de direitos, inventário, bases legais por
  operação, avaliação de fornecedores, transferências, segurança, incidentes e
  RIPD. Também autorizou atletas a ver listas vigentes de convocação e de
  confirmadas para treino com dados mínimos, sem justificativas ou motivos
  pessoais; confirmação de treino continua distinta de presença real.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-014`

### `CLAIM-028`

- **Descrição:** a `DEC-015` aprovou a arquitetura inicial gratuita: PWA
  React/TypeScript/Vite no Cloudflare Pages; Supabase/PostgreSQL/Auth/Data
  API/RLS em São Paulo, com homologação sintética separada; Brevo SMTP somente
  para identidade; GitHub privado; MFA privilegiada; central interna de
  notificações; offline somente leitura condicionado à criptografia; backups
  próprios criptografados, restauração testada, cotas monitoradas e
  portabilidade. Dados reais permanecem bloqueados até os portões das `DEC-014`
  e `DEC-015`.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001`, `SRC-017`, `SRC-018`, `SRC-019`, `SRC-020`
  e `DEC-015`

### `CLAIM-029`

- **Descrição:** a `DEC-016`, aditada pela `DEC-016-A`, aprovou capacidade-base
  de 8 horas semanais, horizonte-base de 24 semanas após D0, marcos M0 a M6,
  controle de mudanças, definição de concluído, piloto e corte, reserva mínima
  de manutenção e classificação P0 a P3. A continuidade proporcional exige
  backup e restauração documentados e testados, proteção das credenciais por
  Davi, contingência temporária por WhatsApp e retorno manual controlado, sem
  custodiante, conta emergencial, acesso técnico de terceiros previamente
  configurado, recuperação institucional programada ou teste sem Davi. O
  cronograma não autoriza redução de segurança, privacidade, testes ou
  documentação e não constitui garantia de lançamento.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-016`

### `CLAIM-030`

- **Descrição:** a `DEC-017` aprovou somente Davi e atleta como perfis
  operacionais da primeira fase, com RLS baseada nesses contextos. Ex-atletas
  exercem direitos sobre os próprios dados sem conta operacional; fornecedores
  são infraestrutura; entidades esportivas externas são fontes ou destinos
  tratados por Davi; e público, familiares, imprensa, patrocinadores, apoiadores
  e parceiros não acessam a PWA. A decisão não cria RBAC adicional, contas
  técnicas, emergência, observador ou módulos externos.
- **Estado:** `CONFIRMADO_HUMANO`
- **Fontes / Evidências:** `SRC-001` e `DEC-017`

## 14. Estado de conclusão desta base

- Conteúdo já estabelecido: identidade conceitual e cadastral; problemas
  operacionais; escala 19 mais 1; autoridade de Davi; usuários, ações e
  visibilidade; contas, autenticação e auditoria; privacidade, retenção,
  justificativas e dados sensíveis; governança mínima, canal de direitos e
  portão de dados reais; capacidades, escopo e dezesseis critérios da primeira
  fase; canal interno, caixa individual, respostas, prazos, histórico e
  correções; distinção entre estados, declarações e fatos; listas vigentes de
  convocação e confirmadas para treino com exposição mínima; indicadores sem
  julgamento automático; migração; custo R$ 0; desenvolvimento solo; arquitetura
  React/TypeScript/Vite, Cloudflare Pages, Supabase/PostgreSQL/Auth/RLS em São
  Paulo, Brevo SMTP e GitHub privado; ambientes separados; notificações
  internas; offline somente leitura condicionado à criptografia; backup,
  restauração, observabilidade, cotas e portabilidade; capacidade-base de 8
  horas semanais; horizonte de 24 semanas após D0; marcos M0 a M6; manutenção
  reservada; classificação de ocorrências; continuidade proporcional por backup,
  proteção de credenciais, contingência temporária por WhatsApp e retorno manual
  controlado; dois perfis operacionais, Davi e atleta; linha de base
  proporcional; indicadores `IND-001` a `IND-010`; metas iniciais de eficiência,
  qualidade, segurança e integridade; validação V0 a V3; piloto controlado;
  critérios de aceitação funcional e critérios de promoção documental; agentes
  controlados; ausência de APIs da OpenAI e Anthropic; domínio, limites humanos,
  riscos e fontes.
- Conteúdo decisório pendente: nenhum dentro da sequência `DEC-002` a `DEC-018`.
  A revisão documental V0 foi concluída e aprovada. Permanecem futuras a coleta
  da linha de base, os testes V1, o piloto V2, o ensaio V3, a produção dos
  artefatos e evidências dos portões vigentes. A autorização humana separada
  promoveu a base a DECISAO-CEPRAEA — VERSÃO CANDIDATA 0.1 em 2026-07-24. Essa
  promoção documental não autorizou dados reais, piloto ou produção e não
  constitui canonização pelo novo workflow documental.
- Próxima ação controlada: iniciar V1 — testes sintéticos conforme `DEC-018`.
  A promoção para VERSÃO CANDIDATA 0.1 foi concluída em 2026-07-24 por Davi
  Sermenho. A conclusão da promoção não inicia D0, não autoriza dados reais,
  piloto ou produção.

```yaml
approval_record:
  item_id: DECISAO-CEPRAEA-v0.1
  item_name: Base Controlada de Conteúdo — promovida para Versão Candidata 0.1
  document_version: "0.1-candidata"
  status: approved
  approved_by: Davi Sermenho
  approval_date: "2026-07-24"
  promotion_date: "2026-07-24"
  scope_approved: >
    Revisão documental V0. Decisões DEC-002 a DEC-018,
    incluindo DEC-016-A, registradas como aprovadas, resolvidas
    ou aditadas de forma compatível. AR-001 a AR-015 resolvidas.
    Derivação independente concluída (RF-CEPRAEA-v0.1.md).
    Promoção para VERSÃO CANDIDATA 0.1 autorizada por Davi Sermenho.
  reservations:
    - Dados reais, piloto e produção bloqueados por portões separados.
    - Promoção documental não autoriza D0, piloto nem produção.
  next_action: >
    Iniciar V1 — testes sintéticos conforme DEC-018.
```

- REVISÃO DOCUMENTAL V0 — CONCLUÍDA E APROVADA COM AJUSTES EDITORIAIS NÃO
  MATERIAIS.
- `V0-01` — APROVADO: as decisões `DEC-002` a `DEC-018`, incluindo `DEC-016-A`,
  estão registradas como aprovadas, resolvidas ou aditadas de forma compatível.
- `V0-02` — APROVADO: nenhuma proposta rejeitada aparece como decisão vigente; a
  versão corporativa anterior da `DEC-017` não integra o conteúdo aprovado.
- `V0-03` — APROVADO: os itens `DES-001` a `DES-006` estão resolvidos em nível
  decisório ou classificados como obrigações futuras de implementação e
  evidência.
- `V0-04` — APROVADO: `CLAIM-012`, `CLAIM-029`, `CLAIM-030` e `SRC-001` refletem
  as decisões finais, incluindo continuidade proporcional, dois perfis
  operacionais e validação V0 a V3.
- `V0-05` — APROVADO: não foi identificada contradição material entre decisões.
  As contradições `CON-001` a `CON-010` descrevem o AS-IS, correções pendentes
  ou riscos residuais explicitamente controlados.
- `V0-06` — APROVADO: a próxima ação está indicada e o documento permanece
  identificado como base de descoberta, não como especificação funcional,
  implementação concluída ou autorização de produção.
- OBSERVAÇÕES V0: não existem comentários abertos no Google Doc; o cabeçalho e o
  estado da declaração central foram ajustados para distinguir aprovação do V0
  de promoção documental; dados reais, piloto, produção e D0 continuam
  bloqueados por autorizações e portões separados.
- RESULTADO V0: a base está documentalmente apta a ser submetida a uma decisão
  humana separada de promoção para DECISAO-CEPRAEA — VERSÃO CANDIDATA 0.1.
- `PROMOCAO_PARA_CANDIDATA_0.1` — CONCLUÍDA em 2026-07-24. Autoridade: Davi
  Sermenho. Todas as ações requeridas (AR-001 a AR-015) resolvidas. Validação
  formal registrada em `VALIDACAO-CEPRAEA-v0.1.md`. A promoção não inicia D0,
  não autoriza dados reais, piloto ou produção. Próxima etapa: V1 (testes
  sintéticos conforme DEC-018).
- `DERIVACAO_INDEPENDENTE_V0` — EXECUTADO. Data: 2026-07-24. Resultado: lista de
  53 requisitos funcionais (RF-001 a RF-053) para a primeira fase e 4 requisitos
  de fases posteriores (RF-P01 a RF-P04), organizados em 11 domínios com seção
  de origem rastreável ao documento-fonte. Nenhum fato inventado identificado —
  todos os itens possuem ao menos um identificador de origem (CRIT-FASE1-*,
  CAP-*, DEC-*, REGRA-DO-*, OBJ-*, PROB-* ou referência de seção). Artefato
  gerado: `RF-CEPRAEA-v0.1.md` em `/home/davis/DAVI2/docs/`. A lista não
  constitui especificação aprovada nem autoriza implementação; integrou as
  evidências consideradas na promoção para DECISAO-CEPRAEA — VERSÃO CANDIDATA
  0.1.

## 15. Matriz de rastreabilidade

<!-- markdownlint-disable MD013 -->

| Problema | Pessoas afetadas | Objetivos relacionados | Resultados (CRIT-FASE1) | Capacidades no escopo |
| --- | --- | --- | --- | --- |
| PROB-001 | Davi (primário) | OBJ-001, OBJ-003, OBJ-004, OBJ-005 | -001, -003, -004, -005, -008, -009, -012 | CAP-01, CAP-03, CAP-04, CAP-07, CAP-12 |
| PROB-002 | Davi e atletas | OBJ-006 | -007, -013, -014, -015, -016 | CAP-10 |
| PROB-003 | Davi e atletas | OBJ-002, OBJ-003, OBJ-005 | -002, -009, -010, -011, -012 | CAP-02, CAP-05, CAP-07 |

| Objetivo | Restrições vinculadas | Conceitos do domínio usados |
| --- | --- | --- |
| OBJ-001 | Autoridade humana; rastreabilidade | Estado operacional; próxima ação; validação |
| OBJ-002 | Integridade; privacidade | Resposta operacional; justificativa; correção administrativa |
| OBJ-003 | Integridade | Resposta de disponibilidade; presença real; convocação; participação |
| OBJ-004 | Temporalidade | Compromisso; calendário; estado operacional |
| OBJ-005 | Autoridade humana | Cobertura tática; função; posição |
| OBJ-006 | Privacidade; segregação de visibilidade | Solicitação operacional; lista de convocação; lista de treino |
| OBJ-007 | Rastreabilidade | Fonte autorizada; validação; rastreabilidade |

<!-- markdownlint-enable MD013 -->

</governance>

<!-- markdownlint-enable MD033 -->
