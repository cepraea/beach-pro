# Histórico curado da interação com Claude Code

> [!IMPORTANT]
> Este documento organiza e resume um registro bruto de conversa. Ele não é uma
> fonte normativa nem representa necessariamente o estado atual do projeto.
> Decisões vigentes devem ser confirmadas nos documentos governados do
> repositório.

## Identificação

| Campo                | Valor                              |
| -------------------- | ---------------------------------- |
| Tipo de artefato     | Histórico de conversa              |
| Estado editorial     | Curado                             |
| Arquivo-fonte        | `.inicio/HISTORICO-CLAUDE-CODE.md` |
| Participantes        | Davi Sermenho e Claude Code        |
| Caráter autoritativo | Não autoritativo                   |
| Confidencialidade    | Uso interno                        |
| Data da curadoria    | 2026-07-27                         |

## Sobre esta versão

Esta versão foi criada para resolver dois problemas do registro original:

1. ausência de separação entre usuário, assistente, raciocínio e ferramentas;
2. perda da estrutura de títulos, listas, tabelas e blocos de código durante a
   exportação.

O [histórico bruto](./HISTORICO-CLAUDE-CODE.md) foi preservado sem alterações.
Versões intermediárias extensas, raciocínio operacional e listagens completas de
ferramentas permanecem disponíveis nele para auditoria.

### Convenções editoriais

| Elemento             | Tratamento nesta versão                                |
| -------------------- | ------------------------------------------------------ |
| Solicitação original | Apresentada em bloco “Usuário”                         |
| Resposta final       | Sintetizada em bloco “Assistente”                      |
| Raciocínio interno   | Convertido em justificativa objetiva, quando relevante |
| Ferramenta           | Identificada pelo objetivo e pela evidência produzida  |
| Saída extensa        | Resumida e vinculada ao intervalo do histórico bruto   |
| Plano repetido       | Substituído pela versão ou pelas alterações relevantes |
| Afirmação histórica  | Marcada como não autoritativa                          |

## Índice das sessões

1. Conceituação de Front Matter YAML
2. Identificação do sistema de memória
3. Análise do repositório e primeiro plano
4. Avaliação crítica do plano
5. Primeira revisão estruturada
6. Segunda avaliação e ampliação das correções
7. Consolidação do plano
8. Aplicação dos blocos finais de correção

---

## Sessão 01 — Conceituação de Front Matter YAML

**Referência bruta:** linhas 7–78.

### Turno 01.1

#### Usuário

> Identifique o domínio de conhecimento que trata do uso de metadados no topo
> dos documentos.

#### Assistente

O domínio principal foi identificado como **metadados de documentos**, com
**Front Matter** como o termo técnico para o bloco estruturado inserido no
início de documentos.

Áreas relacionadas:

- Ciência da Informação;
- Biblioteconomia;
- Arquitetura da Informação;
- gestão documental;
- linguagens de marcação;
- padrões de metadados.

#### Resultado

Front Matter foi caracterizado como uma representação estruturada, normalmente
em YAML, TOML ou JSON, destinada a classificação e consumo por ferramentas.

### Turno 01.2

#### Usuário

> Considerando Front Matter YAML para indexação e recuperação, identifique
> subdomínios, taxonomia, tema principal e contexto.

#### Assistente

O tema principal foi definido como:

> Estruturação declarativa de metadados em documentos para indexação,
> classificação e recuperação de informação.

Os subdomínios identificados foram:

| Subdomínio               | Finalidade                                   |
| ------------------------ | -------------------------------------------- |
| Serialização de dados    | Representar metadados em YAML, TOML ou JSON  |
| Metadados documentais    | Descrever título, autoria, data, tipo e tags |
| Indexação e recuperação  | Alimentar busca, filtragem e navegação       |
| Sistemas de documentação | Integrar SSGs, wikis e bases de conhecimento |
| Schemas e validação      | Definir campos, tipos e obrigatoriedade      |
| Ontologias e relações    | Relacionar documentos, temas e hierarquias   |

Taxonomia reconstruída:

```text
Gestão da Informação
└── Metadados de documentos
    ├── Padrões de representação
    │   ├── YAML Front Matter
    │   ├── TOML Front Matter
    │   └── JSON Front Matter
    ├── Campos descritivos
    │   ├── Identificação
    │   ├── Classificação
    │   ├── Temporalidade
    │   └── Relacionamentos
    ├── Validação de schema
    └── Consumo
        ├── Build-time
        ├── Query-time
        └── Runtime
```

### Turno 01.3

#### Usuário

> Implementar Front Matter é apenas inserir um bloco de metadados no início do
> arquivo? Ele substitui o sumário Markdown?

#### Assistente

Não. Um sistema funcional requer mais que o bloco YAML:

- parser;
- schema;
- validação;
- indexador ou consumidor;
- integração com o fluxo documental.

Front Matter e sumário possuem responsabilidades diferentes:

| Aspecto           | Front Matter              | Sumário             |
| ----------------- | ------------------------- | ------------------- |
| Público principal | Máquina                   | Leitor              |
| Escopo            | Documento no sistema      | Seções do documento |
| Finalidade        | Classificação e indexação | Navegação interna   |
| Formato           | YAML, TOML ou JSON        | Links Markdown      |

### Turno 01.4

#### Usuário

> Como identificar as informações que devem ser passadas aos agentes pelo Front
> Matter?

#### Assistente

O critério proposto foi identificar quais decisões o agente precisa tomar antes
de ler o corpo completo:

1. decidir se o documento é relevante;
2. reconhecer tipo, escopo e relacionamentos;
3. evitar inferências caras ou ambíguas;
4. consultar estado operacional que muda independentemente do conteúdo.

Regra editorial consolidada:

> Front Matter é um índice do documento, não uma repetição do seu conteúdo.

---

## Sessão 02 — Identificação do sistema de memória

**Referência bruta:** linhas 79–103.

### Turno 02.1

#### Usuário

> Onde está o sistema de memória deste projeto?

#### Assistente

Foi identificado um diretório de memória do Claude Code fora do repositório.
Como o caminho contém informações do ambiente local, ele não é reproduzido
integralmente nesta versão curada.

#### Ferramenta

**Objetivo:** listar os arquivos existentes no diretório de memória.

**Resultado resumido:**

```text
MEMORY.md
project_cepraea_context.md
```

### Turno 02.2

#### Usuário

> Esses arquivos estão no repositório ou fazem parte das configurações do
> Claude?

#### Assistente

Foi esclarecido que os arquivos pertenciam ao armazenamento local do Claude
Code, externo ao repositório.

### Turno 02.3

#### Usuário

> Então o projeto não possui um sistema Front Matter implementado?

#### Assistente

A resposta inicial concluiu que não havia implementação no projeto. Essa
conclusão foi posteriormente superada pela exploração mais completa do
repositório, que encontrou uma arquitetura documental, registros YAML, schemas e
uso parcial de Front Matter.

> [!WARNING]
> A resposta deste turno é histórica e não deve ser usada para determinar o
> estado atual do projeto.

---

## Sessão 03 — Análise do repositório e primeiro plano

**Referência bruta:** linhas 105–937.

### Turno 03.1

#### Usuário

> Analise o repositório para identificar as ações necessárias para adicionar um
> sistema Front Matter YAML.

#### Assistente

Foi iniciada uma exploração do repositório com foco em:

- dependências e scripts;
- estrutura de `src/`;
- documentação existente;
- schemas JSON;
- registros YAML;
- validadores Python;
- regras de governança;
- documentos que já utilizavam metadados.

#### Ferramentas

As ferramentas foram usadas para:

1. listar arquivos e diretórios;
2. ler configurações e documentos de governança;
3. localizar Front Matter existente;
4. comparar documentos Markdown com o registro mestre;
5. identificar validadores e contratos.

Principais evidências encontradas:

- existência de `docs/registry/registro-documentos.yaml`;
- existência de `docs/registry/workflow-documentacao.yaml`;
- presença de schemas em `docs/contracts/schemas/`;
- uso parcial e inconsistente de Front Matter;
- existência de scripts Python de validação documental;
- ausência inicial de specs documentais nas features de `src/`.

### Turno 03.2

#### Usuário

Durante a análise, o usuário definiu:

- escopo abrangendo documentação e feature specs;
- prioridade para scripts Python de governança e validação;
- consumo secundário por agentes de IA;
- processamento por máquina e validação contra schema;
- ausência de obrigatoriedade de consumo pelo pipeline Vite nesta fase.

#### Assistente

Foi produzido um primeiro plano para:

1. criar schemas de Front Matter;
2. criar documentação das features;
3. implementar o gate `G-FM`;
4. adicionar testes;
5. migrar documentos progressivamente;
6. produzir contexto para agentes;
7. integrar validação ao fluxo final.

### Evolução do plano

O plano apareceu em múltiplas versões completas no histórico bruto. Nesta versão
curada, elas são representadas pelas mudanças principais:

| Revisão  | Mudança principal                                     |
| -------- | ----------------------------------------------------- |
| Inicial  | Definição do schema e das fases de implantação        |
| Segunda  | Regras de sincronização com o registro mestre         |
| Terceira | Testes específicos para `validate_front_matter()`     |
| Quarta   | Separação entre documentos governados e feature specs |
| Quinta   | Tratamento de documentos canônicos e aprovações       |

### Resultado da sessão

Foi criado um plano executável, mas ainda com incompatibilidades em relação aos
schemas e invariantes vigentes. Essas incompatibilidades motivaram a sessão
seguinte.

---

## Sessão 04 — Avaliação crítica do plano

**Referência bruta:** linhas 942–1663.

### Turno 04.1

#### Usuário

O usuário solicitou uma análise linha a linha de uma avaliação crítica do plano,
incluindo:

- conteúdo semântico;
- ações sugeridas;
- evidências usadas;
- confronto das afirmações com o repositório.

#### Assistente

As afirmações da avaliação foram verificadas diretamente contra schemas,
registros, workflows, scripts e documentos.

### Resultado da verificação

|  Nº | Afirmação verificada                                          | Resultado               |
| --: | ------------------------------------------------------------- | ----------------------- |
|   1 | `blocking: false` viola o schema vigente                      | Confirmada              |
|   2 | Registrar um gate não o torna requisito de transição          | Confirmada              |
|   3 | Novos contratos conflitavam com o perfil LEAN                 | Confirmada              |
|   4 | Havia documentos sem `responsible` no registro                | Confirmada              |
|   5 | `milestone` escalar não representava múltiplos marcos         | Confirmada              |
|   6 | O mapeamento de features precisava preceder as specs          | Confirmada              |
|   7 | Alguns caminhos poderiam conflitar com o G-ARCH               | Parcialmente confirmada |
|   8 | `package.json` faltava nos arquivos críticos                  | Confirmada              |
|   9 | Não havia manifesto reproduzível das dependências Python      | Confirmada              |
|  10 | Faltavam testes para campos sincronizados                     | Confirmada              |
|  11 | O invariante de conteúdo invalidava uma presunção da migração | Confirmada              |
|  12 | Alterar o README exigia recalcular seu hash                   | Confirmada              |

### Decisões resultantes

- manter `G-FM` fora do workflow processável até sua ativação formal;
- atualizar explicitamente os gates exigidos pelas transições;
- tornar `responsible` condicional;
- usar `milestones` como lista;
- bloquear feature specs até validação do mapeamento;
- incluir dependências e testes no plano;
- não presumir que Front Matter em documento aprovado dispensa nova revisão;
- recalcular hashes após alterações governadas.

---

## Sessão 05 — Primeira revisão estruturada

**Referência bruta:** linhas 1644–2660.

### Turno 05.1

#### Usuário

> Execute as ações do plano, garantindo conformidade com a avaliação.

#### Assistente

Antes de executar mudanças no repositório, foi identificado que a extensão do
perfil LEAN exigia autorização formal. O plano foi então revisado para incorporar
as correções verificadas.

### Alterações incorporadas

1. criação de fase preliminar de autorização;
2. separação entre schema documental e schema de feature spec;
3. criação do `G-FM` inicialmente como auditoria;
4. testes para divergência de campos;
5. migração sequencial de documentos;
6. bloqueio explícito para documentos canônicos;
7. inclusão de contexto para agentes;
8. encerramento condicionado a hashes, gates e aprovações.

### Ferramentas

Foram utilizadas leituras e edições sucessivas do arquivo de plano. Erros de
numeração e tabelas apontados pelo linter foram corrigidos durante a revisão.

### Resultado

Uma nova versão completa do plano foi produzida. O conteúdo integral permanece
no histórico bruto; esta versão curada conserva apenas suas decisões.

---

## Sessão 06 — Segunda avaliação e ampliação das correções

**Referência bruta:** linhas 2668–3040.

### Turno 06.1

#### Usuário

O plano revisado foi submetido a nova avaliação.

#### Assistente

Foram identificadas novas incompatibilidades:

1. valor de migração rejeitado pelo schema do registro;
2. caminho proposto para `feature-scope.yaml` incompatível com G-ARCH;
3. ordem incorreta entre manifesto e criação de documentos;
4. divergência temporária do README;
5. contrato não incorporado ao workflow processável;
6. glossário em estado inicial colocado diretamente em caminho canônico;
7. aprovações tratadas de forma agregada, em vez de individual.

### Correções decididas

- representar migração em manifesto próprio;
- posicionar artefatos conforme tipo e estado;
- registrar arquivos no manifesto na fase correta;
- sincronizar README, versões e hashes;
- incorporar contratos ao workflow quando formalmente ativados;
- promover documentos por transições válidas;
- emitir uma aprovação por documento e versão.

---

## Sessão 07 — Consolidação do plano

**Referência bruta:** linhas 3045–4100.

### Turno 07.1

#### Usuário

Foram solicitadas novas correções estruturadas no formato
`SEARCH/REPLACE`.

#### Assistente

O plano foi consolidado com:

- autorização formal antes da extensão do perfil LEAN;
- manifesto de migração;
- validação de caminho dependente de tipo e estado;
- implementação e testes do `G-FM` antes da baseline;
- atualização atômica de documentos, hashes e registros;
- correção dos caminhos dos documentos voltados a agentes;
- sincronização das aprovações finais;
- atualização das tabelas de arquivos críticos e riscos.

### Ferramentas

As substituições foram aplicadas sequencialmente. Quando uma correspondência
falhou, o trecho atual foi relido antes de realizar uma substituição localizada.

### Resultado

O plano passou a distinguir:

| Modo      | Comportamento                                       |
| --------- | --------------------------------------------------- |
| `audit`   | Registra ausência ou divergência durante a migração |
| `enforce` | Falha quando a cobertura obrigatória estiver ativa  |

---

## Sessão 08 — Aplicação dos blocos finais de correção

**Referência bruta:** linhas 4110–4904.

### Turno 08.1

#### Usuário

O usuário forneceu 16 blocos finais de substituição para corrigir o plano.

#### Assistente

Os blocos foram aplicados em sequência, com releitura localizada nos casos em
que o texto existente não correspondia exatamente ao trecho esperado.

### Resultado consolidado

1. `workflow_status` foi removido do Front Matter governado.
2. O estado documental permaneceu exclusivo do registro mestre.
3. A descrição e a trajetória do glossário foram corrigidas.
4. A extensão do perfil LEAN passou a exigir decisão documental específica.
5. O schema de Front Matter foi mantido sem estado mutável.
6. G-ARCH foi vinculado à política normativa e ao par tipo × estado.
7. `G-FM` ganhou seleção localizada por documento.
8. Foram definidos os modos `audit` e `enforce`.
9. A baseline passou a usar explicitamente o modo de auditoria.
10. A migração passou a validar cada documento e depois o conjunto global.
11. Documentos novos passaram a nascer registrados no manifesto.
12. O campo `reason` ficou restrito às exclusões.
13. Os pré-requisitos da fase final foram corrigidos.
14. Aprovações passaram a depender de transições e evidências formais.
15. A tabela de arquivos críticos foi atualizada.
16. Riscos, verificações e condicionamentos finais foram sincronizados.

### Estado ao final do registro

O histórico termina após a confirmação textual de que os 16 blocos haviam sido
aplicados ao arquivo de plano. O registro não demonstra, por si só, que todo o
plano tenha sido implementado no repositório.

---

## Decisões históricas consolidadas

As principais decisões produzidas pela conversa foram:

- Front Matter não substitui sumário;
- Front Matter precisa de schema, parser, consumidor e validação;
- o registro mestre continua responsável por estado e vigência;
- metadados imutáveis podem ser duplicados no documento quando houver regra de
  sincronização;
- migração deve começar em modo de auditoria;
- ativação obrigatória exige atualização formal do workflow;
- documentos aprovados não podem ser alterados sem observar revisão, hash e
  aprovação;
- feature specs exigem mapeamento de escopo autoritativo;
- agentes de IA são consumidores secundários dos metadados;
- documentos históricos não devem ser tratados como fontes normativas.

## Evidências e limitações

### Evidências preservadas no histórico bruto

- comandos executados;
- saídas completas de diretórios;
- conteúdo intermediário dos planos;
- mensagens de erro de edição;
- resultados de buscas;
- trechos integrais de schemas e registros;
- instruções `SEARCH/REPLACE`.

### Limitações desta versão curada

- não reproduz raciocínio interno integral;
- não reproduz saídas extensas de ferramentas;
- não conserva todas as versões intermediárias do plano;
- não certifica o estado atual dos arquivos citados;
- não substitui registros, schemas ou decisões governadas.

## Referências

- [Histórico bruto](./HISTORICO-CLAUDE-CODE.md)
- [Regras do agente](../CLAUDE.md)
- [Documentação do projeto](../docs/README.md)
- [Política de arquitetura documental](../docs/governance/policies/politica-arquitetura-documental.md)
- [Workflow documental](../docs/governance/workflows/workflow-documentacao.md)
