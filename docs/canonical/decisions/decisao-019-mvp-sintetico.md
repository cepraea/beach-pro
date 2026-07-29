---
document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
title: "DEC-019 — Recorte e autorização do MVP sintético"
document_type: decisao
version: "0.1.2"
workflow_status: CANONICA_VIGENTE
responsible: Davi Sermenho
permitted_uses:
  - decisao_vigente
  - implementacao_exclusivamente_sintetica_m0_m4
  - inicio_por_m0_m1
  - definicao_de_d0
prohibited_uses:
  - aprovacao_por_inferencia
  - dados_reais
  - migracao_real
  - v2
  - piloto
  - producao
  - m5_m6_operacionais
---
# DEC-019 — Recorte e autorização do MVP sintético

## 1. Identificação

| Campo | Valor |
|---|---|
| ID da decisão | `DEC-019` |
| Documento | `DOC-CEPRAEA-DEC-019-MVP-SINTETICO` |
| Produto | CEPRAEA BEACH PRO |
| Versão | `0.1.1` |
| Estado | `PROPOSTA_PARA_APROVACAO` |
| Data da proposta | 2026-07-26 |
| Autoridade aprovadora | Davi Sermenho |
| Efeito pretendido | Aprovar o recorte e autorizar sua implementação exclusivamente sintética |

O identificador correto é `DEC-019`, mantendo a sequência `DEC-002` a
`DEC-018`. A grafia `DEC-0019` não cria um identificador distinto.

## 2. Fontes da decisão

| Fonte | Versão | Hash |
|---|---|---|
| `DOC-CEPRAEA-CANDIDATA-CONTEXTO` | 0.1 | `71bd2695280f0cdd5c41b83c7e433d5a84a803b527a7e09d7dfd7eecaaeab847` |
| `DOC-CEPRAEA-REQ-DERIVADOS-V01` | 0.1 | `a1a29af5b1d6d4045e558a436ff824e750f90adee32423707c389d5b0fc0e478` |
| `DOC-VAL-REL-AUDITORIA-REQUISITOS-MVP` | 0.1.1 | `10f8e3dd6fb040fa6f3e973f86ecb20328be2ede0f0aa537b5db36dbce035313` |
| `DOC-CEPRAEA-PROPOSTA-MVP-SINTETICO` | 0.1.2 | `c0f7ffb89606cb6ec5ed8f71283c991e7d602446fec5710bf46fc687e946e420` |

A versão de trabalho 0.2 do contexto foi consultada para compreender a
reclassificação dos problemas do legado, mas não substitui a versão canônica
0.1 nesta decisão.

## 3. Problema decisório

O catálogo possui 53 RFs de primeira fase, mas eles não representam 53 entregas
independentes:

- 33 estão prontos para decomposição;
- 11 são critérios, invariantes ou especializações que devem ser consolidados;
- 4 exigem esclarecimento derivável das decisões existentes;
- 4 concentram-se em três escolhas reais de produto;
- 1 é gate de dados reais/produção, não funcionalidade.

Sem um recorte explícito, iniciar código poderia transformar todos os 53 RFs em
backlog simultâneo, duplicar trabalho, antecipar complexidade offline e misturar
validação sintética com preparação para operação real.

## 4. Decisão proposta

Mediante aprovação expressa de Davi Sermenho, fica decidido:

1. adotar o `MVP_SINTETICO` como primeiro recorte implementável do CEPRAEA BEACH
   PRO;
2. implementar um fluxo vertical completo de treino;
3. aprovar os 44 identificadores incluídos no nível de intenção e escopo para
   implementação sintética;
4. consolidar identificadores repetidos como critérios de aceitação, sem
   apagá-los da rastreabilidade;
5. adiar oito RFs sem removê-los da primeira fase documental;
6. tratar RF-050 como gate anterior a dados reais, piloto e produção;
7. autorizar o início formal da implementação sintética em M0/M1;
8. permitir o avanço subsequente de M2 a M4 sem nova decisão de produto, desde
   que o escopo permaneça inalterado e os dados sejam exclusivamente sintéticos;
9. manter M5/M6 operacionais, V2, dados reais, migração real, piloto e produção
   bloqueados;
10. definir D0 como a data e hora da aprovação expressa desta `DEC-019`, no fuso
    `America/Sao_Paulo`.

## 5. Fluxo aprovado do MVP

```text
Davi mantém o elenco sintético
        ↓
Davi cria um treino com prazo e vigência
        ↓
Davi solicita disponibilidade
        ↓
Atletas sintéticas respondem
        ↓
Davi acompanha respostas e pendências
        ↓
Sistema apresenta cobertura por função ampla
        ↓
Davi publica ou não publica a lista prevista
        ↓
Davi registra presença real após o treino
        ↓
Histórico reconstrói declaração, lista e fato posterior
```

Esse fluxo valida:

- ciclo de vida do elenco;
- disponibilidade sem confusão com presença;
- comunicação operacional interna;
- lista prevista sem exposição indevida;
- estado temporal;
- autoridade esportiva de Davi;
- identidade, isolamento, histórico e auditoria.

## 6. Escopo funcional aprovado

### 6.1 RFs incluídos

```text
RF-001 a RF-014
RF-018 a RF-034
RF-036 a RF-048
```

Total: 44 identificadores.

### 6.2 Consolidações obrigatórias

Os seguintes itens permanecem rastreáveis, mas funcionam como critérios ou
invariantes, não como entregas independentes:

| RF | Consolidado em |
|---|---|
| RF-002 | Estado operacional e fluxo interno de RF-001/RF-022 |
| RF-004 | Isolamento e visibilidade de RF-007/RF-045/RF-046 |
| RF-009 | Justificativa e histórico de RF-008/RF-010 |
| RF-014 | Declaração e fato posterior de RF-012/RF-013 |
| RF-019 | Visibilidade das listas RF-017/RF-018; no MVP aplica-se à RF-018 |
| RF-028 | Estado temporal de RF-027 |
| RF-032 | Qualidade dos indicadores de RF-031 |
| RF-034 | Histórico de listas de RF-020/RF-033 |
| RF-044 | Identidade e isolamento de RF-037/RF-040/RF-045 |
| RF-047 | Proibição de inferência e exposição de RF-031/RF-046 |

### 6.3 RFs adiados

| RF | Estado após a decisão | Condição de retomada |
|---|---|---|
| RF-015 | `ADIADO_POS_MVP` | Incremento de convocações de competição |
| RF-016 | `ADIADO_POS_MVP` | Incremento de convocações de competição |
| RF-017 | `ADIADO_POS_MVP` | Incremento de convocações de competição |
| RF-035 | `ADIADO_PRE_DADOS_REAIS` | Preparação de migração/importação validada |
| RF-049 | `ADIADO_PRE_PILOTO` | Antes de titulares ou ex-atletas usarem dados reais |
| RF-051 | `ADIADO_OFFLINE` | Nova decisão de recorte e prova de segurança |
| RF-052 | `ADIADO_OFFLINE` | Obrigatório conjuntamente com RF-051 |
| RF-053 | `ADIADO_OFFLINE` | Obrigatório conjuntamente com RF-051 |

### 6.4 Gate não funcional

RF-050 passa a ser tratado como `GATE_DADOS_REAIS_PRIVACIDADE`. Nenhuma de suas
condições é dispensada. O item deixa apenas de ser estimado como funcionalidade
isolada do MVP sintético.

### 6.5 Itens já posteriores ou excluídos

- `RF-P01` a `RF-P04` permanecem em fase posterior.
- Scout, vídeo, finanças e publicação pública permanecem fora do produto ou da
  primeira fase, conforme as decisões vigentes.

## 7. Decisões de domínio incorporadas

### 7.1 Cobertura tática do MVP

Fica aprovada somente a cobertura quantitativa pelas funções amplas:

- goleira;
- defesa;
- ataque;
- especialista;
- indefinida.

Posições específicas, combinações e sistemas táticos não integram o MVP.
Indicadores são descritivos e não geram convocação, escalação ou julgamento
automático.

Coringa é papel tático contextual do jogo. Não é posição nem nome alternativo
para especialista e não integra a classificação de posição ou função do MVP.

### 7.2 Vínculo esportivo e conta

Ficam aprovados três estados persistentes:

| Estado | Elenco ativo | Conta | Histórico |
|---|---|---|---|
| `ATIVA` | Incluída | Ativa | Preservado |
| `INATIVA_TEMPORARIA` | Não incluída | Suspensa | Preservado |
| `VINCULO_ENCERRADO` | Não incluída | Desativada | Preservado |

`RETORNAR_AO_ELENCO` é uma transição autorizada por Davi para `ATIVA`, não um
novo cadastro. O retorno:

- reutiliza a mesma identidade;
- reativa a conta quando aplicável;
- preserva o histórico anterior;
- registra autoria, data e transição;
- atualiza as representações internas dependentes do elenco;
- não exige registrar motivo médico, reprodutivo, familiar ou pessoal.

### 7.3 Offline

O MVP será instalável, mas exigirá conexão para acessar dados e executar o fluxo.
Não haverá snapshot local de dados no primeiro recorte.

RF-051 a RF-053 permanecem juntos e só podem retornar mediante nova decisão. Se
retornarem, aviso de desatualização, impedimento de sobrescrita, criptografia,
vínculo ao dispositivo e eliminação local serão obrigatórios integralmente.

## 8. Unidades de entrega aprovadas

| Unidade | Conteúdo |
|---|---|
| MVP-01 | Fundação, identidade, acesso, RLS e segurança básica |
| MVP-02 | Ciclo de vida do elenco |
| MVP-03 | Compromissos de treino |
| MVP-04 | Solicitações, respostas e justificativas |
| MVP-05 | Lista prevista e presença real |
| MVP-06 | Caixa individual da atleta |
| MVP-07 | Estado operacional e pendências de Davi |
| MVP-08 | Cobertura por função ampla |
| MVP-09 | Histórico e auditoria |
| MVP-10 | Privacidade aplicada ao fluxo |

Os identificadores RF continuam sendo a rastreabilidade normativa. As unidades
MVP são a organização de implementação e não substituem os RFs.

## 9. Autorização de implementação

### 9.1 Autorizado

Após a aprovação desta decisão:

- iniciar M0 e M1;
- criar e editar código, testes, migrações e documentação técnica;
- configurar ambientes exclusivamente sintéticos;
- criar contas, nomes, contatos e eventos fictícios;
- usar Claude Code e Codex como assistentes de desenvolvimento conforme as
  decisões vigentes;
- decompor os RFs incluídos em critérios e tarefas;
- tomar decisões técnicas reversíveis sem nova consulta a Davi;
- avançar de M2 a M4 quando as condições técnicas do marco anterior estiverem
  atendidas.

### 9.2 Não autorizado

A aprovação não autoriza:

- cadastrar Davi, Gilvania ou qualquer atleta real;
- copiar ou importar a planilha real;
- usar e-mail, telefone, justificativa ou outro dado pessoal real;
- iniciar migração real;
- usar a aplicação como piloto informal;
- executar V2 ou V3;
- liberar acesso ao elenco;
- publicar em produção operacional;
- executar M5/M6 operacionais;
- integrar planilhas ou mensagens;
- implementar os RFs adiados;
- alterar o recorte sem controle de mudança.

## 10. Tratamento dos dados sintéticos

Todo ambiente autorizado pela decisão deve:

1. usar marcação visível `AMBIENTE_SINTETICO`;
2. usar somente identidades fictícias;
3. incluir pelo menos uma atleta sintética com saída e retorno para validar
   RF-003/RF-043;
4. excluir motivos pessoais reais do cenário;
5. impedir conexão com fontes reais;
6. impedir envio de dados do produto a APIs externas de IA;
7. permitir eliminação integral do conjunto sintético;
8. manter segredos e privilégios fora do cliente.

## 11. Marcos autorizados

### M0 — Preparação

- decompor as dez unidades em backlog técnico;
- escrever critérios de aceitação e testes;
- preparar ambientes e massa sintética;
- configurar repositório, qualidade, segredos e integração contínua;
- registrar D0 e a evidência da aprovação.

### M1 — Fundação e identidade

- implementar MVP-01;
- iniciar o esqueleto de MVP-09;
- criar Davi sintético e atletas sintéticas;
- comprovar isolamento, RLS, MFA privilegiada e cadastro fechado;
- impedir acesso cruzado, acesso anônimo e privilégio administrativo no cliente.

### M2 — Elenco, compromissos e respostas

- implementar MVP-02, MVP-03 e MVP-04;
- validar retorno sem duplicidade;
- preservar declaração e correção administrativa separadamente.

### M3 — Listas e fatos

- implementar MVP-05 e MVP-08;
- validar lista prevista, cobertura ampla e presença posterior.

### M4 — Comunicação, privacidade e auditoria

- implementar MVP-06, MVP-07, MVP-09 e MVP-10;
- completar painel, caixa, histórico e testes negativos;
- executar V1 sintética.

M5/M6 operacionais continuam bloqueados.

## 12. Done vinculante do MVP sintético

O MVP somente pode ser declarado concluído quando:

1. existem personas sintéticas de Davi e pelo menos cinco atletas;
2. Davi cria treino e solicitação de disponibilidade;
3. atletas respondem nos quatro estados, com e sem justificativa;
4. alteração de resposta preserva a versão anterior;
5. correção administrativa não altera a autoria da atleta;
6. Davi visualiza respondidas, não respondidas, vencidas e próximas ações;
7. cobertura utiliza somente funções amplas e respostas vigentes;
8. lista prevista pode ser publicada, substituída, encerrada ou não publicada
   sem expor justificativas;
9. presença é registrada depois do treino e nunca inferida da disponibilidade;
10. histórico reconstrói solicitação, resposta, lista e fato por autoria, data e
    vigência;
11. testes negativos comprovam que uma atleta não acessa dados privados de
    outra;
12. retorno de atleta sintética reutiliza a mesma identidade e histórico;
13. PWA é instalável e funciona online nos navegadores aprovados;
14. não existe snapshot offline, sincronização contínua com planilhas ou
    dependência externa no fluxo testado;
15. testes automatizados do domínio, RLS e fluxo vertical passam;
16. não existe falha crítica aberta;
17. todo dado permanece comprovadamente sintético;
18. nenhuma evidência é apresentada como autorização para dados reais, piloto
    ou produção.

## 13. Autonomia técnica

Não exigem nova decisão de Davi:

- nomes internos de módulos, componentes, funções ou tabelas;
- estrutura inicial de código;
- organização de pastas;
- bibliotecas auxiliares compatíveis com a arquitetura aprovada;
- ordem interna de tarefas dentro do marco;
- refatorações reversíveis;
- desenho visual que não altere semântica, visibilidade ou escopo;
- detalhes de testes que apenas comprovem regras já aprovadas.

Exigem nova decisão ou aditamento:

- incluir ou retirar unidade do MVP;
- antecipar qualquer RF adiado;
- criar novo perfil operacional;
- modificar estados do vínculo;
- incluir posições ou sistemas táticos específicos;
- incluir offline;
- usar dados reais;
- iniciar migração, piloto ou produção;
- alterar autoridade, privacidade ou fronteira do produto.

## 14. Efeito sobre decisões anteriores

A `DEC-019`:

- não revoga `DEC-002` a `DEC-018`;
- recorta a ordem de implementação da primeira fase;
- adia itens sem removê-los do produto;
- transforma a auditoria dos RFs em autorização executável;
- mantém a arquitetura aprovada;
- preserva os gates de segurança e privacidade;
- não transforma o MVP sintético em produto operacional.

Em conflito estrito sobre o recorte do primeiro MVP, esta decisão prevalece
sobre a expectativa anterior de implementar simultaneamente todos os RFs da
primeira fase. Nos demais assuntos, as decisões anteriores permanecem vigentes.

## 15. Riscos aceitos e não aceitos

### Riscos aceitos

- MVP não cobre convocações de competição;
- MVP não importa o legado;
- MVP não oferece canal real de direitos;
- MVP não funciona com dados offline;
- cobertura tática inicial é deliberadamente ampla;
- validação inicial não comprova uso por atletas reais.

### Riscos não aceitos

- vazamento entre atletas;
- perda ou sobrescrita silenciosa de declaração;
- presença inferida da disponibilidade;
- duplicação de identidade no retorno;
- exposição de justificativa;
- uso de dado real;
- decisão esportiva automática;
- privilégio administrativo no cliente;
- falha crítica aberta no Done.

## 16. Regra de D0

Se aprovada sem alteração, a data e hora do registro de aprovação da `DEC-019`
serão `D0`.

Se Davi indicar outra data expressamente, essa data substituirá a regra padrão.
Nenhuma atividade anterior à aprovação pode ser retroativamente classificada
como implementação autorizada por esta decisão.

## 17. Registro de aprovação pendente

Esta seção será preenchida somente após manifestação expressa de Davi:

```yaml
approval_record:
  decision_id: DEC-019
  document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO
  version: "0.1.1"
  content_hash: PREENCHER_COM_HASH_EXTERNO_DESTA_VERSAO
  decision: PENDENTE
  approved_by: Davi Sermenho
  approved_at: PENDENTE
  d0: PENDENTE
  reservations: []
```

A aprovação deve identificar decisão, documento, versão e hash. O hash não é
inserido antecipadamente no próprio arquivo para evitar autorreferência
impossível.

## 18. Estado e efeito atual

Enquanto esta versão permanecer `PROPOSTA_PARA_APROVACAO`:

- nenhuma resolução acima está aprovada;
- D0 não existe;
- implementação não está autorizada;
- a proposta anterior e a auditoria permanecem apenas insumos;
- dados reais, piloto e produção continuam bloqueados.
