# Plano revisado: Front Matter YAML com perfis por tipo documental

## Identificação

| Campo                      | Valor                                                        |
| -------------------------- | ------------------------------------------------------------ |
| Natureza                   | Proposta de implementação com cobertura ampliada             |
| Origem                     | Revisão de escopo de `PLANO-FRONT-MATTER-CORRIGIDO.md`       |
| Revisão                    | 2026-07-27 — cobertura, perfis e consumidores múltiplos      |
| Autoridade                 | Depende de decisões explícitas de Davi Sermenho              |
| Fonte de verdade           | `docs/registry/registro-documentos.yaml`                     |
| Estado                     | Não autorizado para execução automática                      |
| Front Matter neste arquivo | Não utilizado; o sistema ainda não existe                    |

## 1. Objetivo congelado

Implementar Front Matter YAML nos documentos Markdown relevantes do projeto,
usando perfis de schema distintos por tipo documental, com validação automática
e suporte a consumidores múltiplos.

O sistema deve:

1. reconhecer e interpretar Front Matter YAML em documentos Markdown;
2. aplicar o perfil de schema correto conforme o tipo documental;
3. validar os campos locais contra o schema do perfil correspondente;
4. comparar campos de documentos governados com `registro-documentos.yaml`;
5. preservar o registro mestre como fonte de verdade global;
6. ser processável por qualquer agente, sem dependência de fornecedor;
7. permitir migração sequencial e verificável;
8. preservar o corpo Markdown durante a migração;
9. atualizar versão e hash dos documentos governados conforme as regras
   documentais existentes.

Este plano não reforma a governança documental e não cria subsistemas
adicionais para resolver problemas que ainda não foram demonstrados por um
piloto.

## 2. Estado atual verificado

Em 2026-07-27, a inspeção do repositório confirmou:

- nenhum arquivo de `docs/**/*.md` começa com Front Matter válido;
- nenhum arquivo de `.inicio/**/*.md` possui Front Matter;
- não existem arquivos Markdown em `src/features/` neste momento;
- `validate_documentation.py` não aceita `G-FM`;
- não existe nenhum schema de Front Matter;
- `registro-documentos.yaml` já contém identidade, tipo, versão, estado,
  caminho, hash, autoridade e relacionamentos para documentos governados;
- `workflow-documentacao.yaml` mantém `NOVOS_CONTRATOS` em `out_of_scope`;
- `workflow.schema.json` exige `blocking: true` para gates registrados;
- `INV-LEAN-003` exige nova revisão e novo hash quando conteúdo aprovado é
  alterado;
- documentos `CANONICA_VIGENTE` não podem ser migrados por presunção;
- `.claude/` não contém arquivos Markdown; hooks e configurações são Python e
  JSON.

Fontes verificadas:

- [registro mestre](../docs/registry/registro-documentos.yaml);
- [workflow processável](../docs/registry/workflow-documentacao.yaml);
- [schema do workflow](../docs/contracts/schemas/workflow.schema.json);
- [schema documental](../docs/contracts/schemas/documento.schema.json);
- [validador documental](../scripts/documentation/validate_documentation.py).

## 3. Tipos documentais, perfis de schema e consumidores

### 3.1 Tipos documentais cobertos

| Perfil           | Padrão de caminho           | Exemplos                                    |
| ---------------- | --------------------------- | ------------------------------------------- |
| `governed`       | `docs/**/*.md`              | protocolos, decisões, relatórios, workflows |
| `agent-context`  | `.inicio/**/*.md`           | templates de contexto, guias de agente      |
| `feature-spec`   | `src/features/**/*.md`      | especificações de feature (futuro)          |

Arquivos `.ts`, `.tsx` e demais arquivos-fonte TypeScript não recebem Front
Matter em nenhuma circunstância.

Arquivos explicitamente excluídos de todos os perfis:

- `CLAUDE.md` (instrução de projeto, não artefato documental);
- `README.md` da raiz;
- `docs/README.md`;
- `node_modules/**`.

### 3.2 Modelo de consumidores

| Camada     | Consumidores                                          | Uso principal                                          |
| ---------- | ----------------------------------------------------- | ------------------------------------------------------ |
| Normativo  | Scripts Python de governança, validação, proveniência | Validação de schema, sincronização com registro, gates |
| Descoberta | Claude Code, Codex, agentes e subagentes              | Triagem, seleção de contexto, verificação documental   |
| Humano     | Davi Sermenho e colaboradores                         | Leitura, edição, revisão                               |
| Pipeline   | TypeScript/Vite                                       | Não consome Front Matter nesta fase                    |

O schema deve ser JSON Schema padrão, sem dependência de fornecedor ou
plataforma de agente específica. Qualquer consumidor capaz de parsear YAML e
validar JSON Schema pode processar o Front Matter.

### 3.3 Relação entre perfis e o registro mestre

`registro-documentos.yaml` é a fonte de verdade global. A relação com cada
perfil é:

| Perfil          | Relação com o registro                                                   |
| --------------- | ------------------------------------------------------------------------ |
| `governed`      | Sincronização obrigatória; campos duplicados devem ser idênticos         |
| `agent-context` | Sem sincronização obrigatória; registro não cobre estes documentos       |
| `feature-spec`  | Sem sincronização obrigatória; pode referenciar features do produto      |

O Front Matter não substitui o registro. Ele é metadata local que permite
descoberta e validação sem consultar o registro a cada leitura.

## 4. Escopo imutável deste plano

### Incluído

- documentos `docs/**/*.md` registrados no registro mestre;
- documentos `.inicio/**/*.md` (contexto de agentes);
- documentos `src/features/**/*.md` quando criados;
- três schemas de Front Matter, um por perfil;
- parser YAML seguro, aplicável a todos os perfis;
- sincronização com o registro para o perfil `governed`;
- testes unitários para cada perfil;
- relatório de cobertura por perfil;
- piloto em um documento não canônico do perfil `governed`;
- piloto em um documento do perfil `agent-context`;
- migração sequencial dos documentos não canônicos;
- decisão separada para documentos `CANONICA_VIGENTE`;
- atualização de versões e hashes dos documentos `governed` afetados;
- documentação operacional mínima após validação do piloto.

### Fora do escopo

- `CLAUDE.md`;
- `README.md` da raiz e `docs/README.md`;
- arquivos `.ts`, `.tsx` e demais arquivos-fonte TypeScript;
- schema específico para feature specs de subprodutos ainda não definidos;
- `feature-scope.yaml`;
- schema de escopo de features;
- manifesto de migração registrado;
- schema de manifesto;
- matriz entre requisitos, features e marcos;
- novos glossários, protocolos ou documentos de governança;
- alteração das regras de caminho do G-ARCH;
- redesign do workflow LEAN;
- versões predeterminadas como `0.3.0` ou `0.4.0`;
- automação nova de aprovações ou evidências;
- ativação obrigatória de `G-FM` no workflow;
- alterações em documentos canônicos sem decisão humana;
- integração do Front Matter no pipeline TypeScript/Vite.

Um item fora do escopo somente pode entrar por decisão humana registrada e por
um plano separado.

## 5. Classificação das propostas do plano anterior

### Necessárias para o objetivo

| Item                                      | Motivo                                                         |
| ----------------------------------------- | -------------------------------------------------------------- |
| Três schemas de Front Matter (um/perfil)  | Perfis distintos têm campos e regras diferentes                |
| Parser YAML seguro para todos os perfis   | Evita aceitar conteúdo inválido ou ambíguo                     |
| Sincronização com o registro (`governed`) | Impede divergência entre metadata local e registro mestre      |
| Validação por perfil                      | Aplica o schema correto conforme o tipo documental             |
| Testes por perfil                         | Demonstra comportamento verificável para cada caso             |
| Relatório de cobertura por perfil         | Identifica documentos migrados e pendentes em cada categoria   |
| Pilotos: um por perfil inicial            | Produz evidência antes da migração completa                    |
| Migração sequencial                       | Limita impacto e facilita reversão                             |
| Atualização de versão e hash (`governed`) | Mantém a identidade exata dos bytes nos documentos governados  |
| Decisão sobre canônicos                   | É exigida pela governança atual                                |

### Dependentes de decisão humana

| Decisão                                        | Efeito                                            |
| ---------------------------------------------- | ------------------------------------------------- |
| Autorizar os contratos de Front Matter         | Desbloqueia a criação dos três schemas            |
| Escolher o documento piloto `governed`         | Desbloqueia a primeira alteração de conteúdo      |
| Escolher o documento piloto `agent-context`    | Desbloqueia o segundo piloto                      |
| Definir o tratamento dos canônicos             | Determina inclusão, nova versão ou exclusão       |
| Tornar `G-FM` obrigatório no workflow          | Exige avaliação posterior à migração              |

### Backlog; não bloqueia este plano

| Item                                | Justificativa para adiamento                              |
| ----------------------------------- | --------------------------------------------------------- |
| Perfil `feature-spec` em produção   | Depende da criação dos primeiros arquivos em `src/`       |
| `feature-scope.yaml`                | Introduz nova fonte processável                           |
| Modos globais `audit` e `enforce`   | Só devem ser considerados após o piloto                   |
| Filtro `--document-id`              | É conveniência, não pré-requisito do parser               |
| Integração TypeScript/Vite          | Não necessária nesta fase                                 |
| Matriz e glossário                  | Expandem taxonomia e governança                           |
| Novos fluxos de aprovação           | Já existe governança para versões aprovadas               |

### Rejeitados deste plano

- criação automática de contratos adicionais além dos três schemas;
- remoção genérica de `NOVOS_CONTRATOS` e `NOVAS_MATRIZES`;
- versões documentais fixadas antes de examinar cada artefato;
- aprovação automática de artefatos apenas porque foram editados;
- criação de evidências inexistentes por antecipação;
- obrigação de registrar um manifesto que muda a cada documento;
- transformação de melhorias opcionais em bloqueios;
- novas rodadas amplas de `SEARCH/REPLACE`.

## 6. Modelos mínimos de Front Matter por perfil

### Perfil `governed` — documentos em `docs/`

Campos sincronizados com o registro mestre:

```yaml
---
document_id: DOC-GOV-PROT-QUALIDADE
title: 'Protocolo de qualidade para documentação de contexto'
document_type: protocolo
version: 'VERSAO_DEFINIDA_PELA_REVISAO'
responsible: Davi Sermenho
permitted_uses: []
prohibited_uses: []
---
```

Regras de sincronização com `registro-documentos.yaml`:

| Campo             | Regra                                                        |
| ----------------- | ------------------------------------------------------------ |
| `document_id`     | Igualdade exata com o registro                               |
| `title`           | Igualdade exata com o registro                               |
| `document_type`   | Igualdade exata com o registro                               |
| `version`         | Igualdade exata com o registro                               |
| `responsible`     | Igual ao registro quando existir; omitido quando não existir |
| `permitted_uses`  | Subconjunto dos usos permitidos no registro                  |
| `prohibited_uses` | Deve conter todas as proibições do registro                  |

Campos exclusivos do registro — não entram no Front Matter:

- `workflow_status`, `registration_status`, `content_hash`;
- `current_path`, `target_path`, `canonical_path`;
- conformidade de nome ou diretório;
- estado de migração, relacionamentos globais, evidências, aprovações.

### Perfil `agent-context` — documentos em `.inicio/`

Campos focados em descoberta e triagem por agentes:

```yaml
---
title: 'Template de contexto para agentes de IA'
document_type: agent-context
scope: 'governança documental'
consumers: [claude-code, codex]
version: '1.0.0'
status: active
---
```

Não há sincronização obrigatória com o registro. O campo `document_id` é
opcional e, quando presente, é informativo, não vinculativo. A validação verifica
apenas o schema do perfil.

### Perfil `feature-spec` — documentos em `src/features/`

Campos focados em identidade e rastreabilidade da feature:

```yaml
---
title: 'Especificação da feature de autenticação'
document_type: feature-spec
feature_id: auth
version: '0.1.0'
status: draft
---
```

Perfil ativado somente quando os primeiros arquivos `src/features/**/*.md`
forem criados. O schema é criado junto com o primeiro piloto deste perfil.

## 7. Decisão mínima de autorização

O workflow atual mantém `NOVOS_CONTRATOS` fora do escopo. Portanto, nenhuma
implementação governada começa antes de Davi decidir explicitamente:

> Autorizar ou não a criação de até três contratos de schema de Front Matter
> (`front-matter-governed.schema.json`, `front-matter-agent-context.schema.json`,
> `front-matter-feature-spec.schema.json`), limitados aos perfis documentais
> definidos neste plano, sem autorizar matrizes, manifestos, schemas auxiliares,
> novos tipos documentais ou ativação obrigatória de `G-FM`.

O schema `feature-spec` pode ser diferido para quando o primeiro arquivo
`src/features/**/*.md` existir, se Davi optar por aprovar apenas os dois
primeiros schemas neste momento.

Se a decisão for negativa, este plano termina sem alterar `docs/`, `src/`,
`.inicio/` ou `scripts/`.

Se a decisão for positiva, ela deve seguir o processo documental já existente.
Este plano não predetermina: identificador da decisão, versão dos documentos
afetados, caminho da decisão, aprovação, hashes ou evidências. Esses dados
devem ser produzidos pelo workflow real, não inventados no plano.

## 8. Fases de implementação

### Fase 0 — Autorizar os contratos mínimos

1. Registrar a decisão humana sobre os schemas solicitados.
2. A decisão deve definir como reconciliar a autorização pontual com
   `NOVOS_CONTRATOS` no `out_of_scope` vigente:
   - exceção explícita e limitada aos schemas de Front Matter; ou
   - atualização mínima do workflow, sem remover genericamente a restrição.
3. Verificar a decisão e a eventual atualização mínima pelos gates já vigentes.
4. Confirmar que a autorização não alcança nenhum item do backlog.
5. Interromper se a decisão, o workflow ou os gates não permitirem prosseguir.

**Saída:** autorização verificável ou encerramento sem implementação.

### Fase 1 — Implementar schemas, parser e testes

1. Criar os schemas autorizados em `docs/contracts/schemas/`:
   - `front-matter-governed.schema.json`;
   - `front-matter-agent-context.schema.json`;
   - `front-matter-feature-spec.schema.json` (se autorizado nesta fase).
2. Registrar os contratos conforme o workflow e o schema documental existentes.
3. Implementar uma função de parsing e validação em
   `scripts/documentation/validate_documentation.py`.
4. A função deve:
   - detectar o perfil correto com base no caminho do arquivo;
   - aceitar somente Front Matter no início lógico do arquivo;
   - tolerar apenas BOM UTF-8 antes do delimitador;
   - detectar delimitador final ausente;
   - usar carregamento YAML seguro;
   - rejeitar YAML inválido;
   - rejeitar raiz que não seja objeto;
   - rejeitar chaves duplicadas;
   - validar contra o schema do perfil detectado;
   - para perfil `governed`: comparar os campos com o registro mestre;
   - preservar o corpo Markdown sem alteração.
5. Criar testes para cada perfil cobrindo:
   - documento válido;
   - Front Matter ausente;
   - YAML inválido;
   - delimitador final ausente;
   - chave duplicada;
   - campo desconhecido;
   - campo divergente do registro (apenas `governed`);
   - `responsible` presente e ausente (apenas `governed`);
   - permissão excessiva e proibição omitida (apenas `governed`);
   - presença de campo exclusivo do registro (apenas `governed`);
   - preservação byte a byte do corpo.
6. Não adicionar `G-FM` ao workflow.
7. Não modificar o G-ARCH.

**Saída:** parser e testes funcionando sem alterar nenhum documento Markdown.

### Fase 2 — Produzir baseline derivada

1. Percorrer os registros cujo `current_path` corresponda a `docs/**/*.md`
   (perfil `governed`).
2. Percorrer todos os arquivos em `.inicio/**/*.md` (perfil `agent-context`).
3. Para cada arquivo, classificar:
   - sem Front Matter;
   - Front Matter válido;
   - Front Matter inválido;
   - divergente do registro (apenas `governed`);
   - `CANONICA_VIGENTE` (apenas `governed`).
4. Gerar relatório de execução por perfil, sem registrá-lo como novo documento
   governado.
5. Não criar manifesto persistente.
6. Confirmar que a baseline não altera arquivos nem gates vigentes.

**Saída:** lista reproduzível de cobertura por perfil, derivada do registro e do
sistema de arquivos.

### Fase 3 — Selecionar e executar pilotos

#### Piloto `governed`

1. Selecionar um único documento que:
   - esteja registrado;
   - esteja em `RASCUNHO`;
   - não seja `CANONICA_VIGENTE`;
   - não integre um pacote de integridade que impeça alteração;
   - possa ser restaurado de forma segura.
2. Registrar a escolha e o motivo.
3. Preservar uma cópia verificável do corpo original.
4. Definir a nova versão conforme a política vigente.
5. Adicionar o Front Matter mínimo do perfil `governed`.
6. Confirmar que o corpo posterior ao delimitador é idêntico ao corpo original.
7. Calcular o novo hash.
8. Atualizar versão e hash no registro na mesma alteração.
9. Validar: schema do perfil, sincronização com o registro, G-ARCH, gates
   aplicáveis, links locais.
10. Reverter o piloto se qualquer validação falhar.

#### Piloto `agent-context`

1. Selecionar um documento em `.inicio/` que seja representativo e reversível.
2. Adicionar o Front Matter mínimo do perfil `agent-context`.
3. Confirmar que o corpo posterior ao delimitador é idêntico ao corpo original.
4. Validar: schema do perfil, ausência de campos do perfil `governed`.
5. Reverter o piloto se qualquer validação falhar.

**Saída:** um documento migrado por perfil e evidência empírica do procedimento.

### Fase 4 — Avaliar os pilotos

Cada piloto somente é aprovado quando:

- o parser rejeita todos os casos inválidos previstos para o perfil;
- o documento válido passa;
- o corpo Markdown foi preservado;
- para `governed`: versão e hash estão sincronizados;
- nenhum gate vigente regrediu;
- o registro continua sendo a fonte de verdade;
- nenhuma expansão de escopo foi necessária.

Se o piloto revelar necessidade de manifesto, novo modo operacional, alteração
do G-ARCH ou outro contrato, a implementação para. A necessidade é registrada
como nova decisão; ela não entra automaticamente neste plano.

### Fase 5 — Migrar documentos não canônicos

Após aprovação explícita dos pilotos:

1. Derivar novamente a lista de documentos por perfil a partir do registro e
   do sistema de arquivos.
2. Excluir temporariamente documentos `CANONICA_VIGENTE` (apenas `governed`).
3. Migrar um documento por alteração independente.
4. Repetir o procedimento validado no piloto correspondente.
5. Executar testes e gates aplicáveis após cada documento.
6. Interromper na primeira regressão.
7. Regenerar o relatório de cobertura por perfil ao final.

Não usar lote e não declarar cobertura integral enquanto houver documentos
pendentes ou excluídos.

### Fase 6 — Decidir sobre documentos canônicos

Davi escolhe uma opção para cada documento `CANONICA_VIGENTE`:

1. criar nova versão e percorrer o workflow normal;
2. autorizar procedimento excepcional específico;
3. excluir o documento do escopo desta implantação.

A opção 2 não pode ser inferida por agente. A opção 3 deve alterar a declaração
de cobertura: o sistema não poderá afirmar que todos os documentos governados
possuem Front Matter.

### Fase 7 — Encerrar a implantação mínima

1. Executar todos os testes do parser e da sincronização.
2. Executar o validador documental vigente.
3. Produzir o relatório final de cobertura por perfil.
4. Atualizar somente a documentação operacional necessária para explicar:
   - perfis disponíveis e campos aceitos por cada um;
   - fonte de verdade e regras de sincronização;
   - comando de validação;
   - limites de cobertura e exclusões;
   - tratamento dos canônicos.
5. Recalcular versões e hashes dos documentos `governed` efetivamente alterados.
6. Não ativar `G-FM` como gate obrigatório do workflow nesta fase.

**Saída:** Front Matter mínimo implementado e validado no escopo autorizado.

## 9. Ativação futura de G-FM

Transformar a validação em gate obrigatório é uma decisão posterior e separada.
Ela somente pode ser considerada quando:

- a cobertura autorizada estiver concluída em todos os perfis ativos;
- o relatório não apresentar divergências;
- o comportamento do piloto e da migração estiver comprovado;
- o impacto sobre transições e contratos tiver sido analisado;
- Davi autorizar a alteração do workflow.

A eventual ativação deve ter plano próprio. Ela não reabre nem bloqueia a
conclusão da implantação mínima.

## 10. Arquivos previstos

### Criar, se autorizado

- `docs/contracts/schemas/front-matter-governed.schema.json`;
- `docs/contracts/schemas/front-matter-agent-context.schema.json`;
- `docs/contracts/schemas/front-matter-feature-spec.schema.json` (quando
  existirem arquivos `src/features/**/*.md`);
- arquivo de testes do parser de Front Matter, no padrão adotado pelo projeto.

### Alterar, se autorizado

- `scripts/documentation/validate_documentation.py`;
- `docs/registry/registro-documentos.yaml`;
- documentos Markdown escolhidos para migração nos perfis `governed` e
  `agent-context`;
- documentação operacional estritamente necessária.

### Não alterar por este plano

- `docs/contracts/schemas/documento.schema.json`;
- `docs/contracts/schemas/workflow.schema.json`;
- regras de caminho do G-ARCH;
- `src/**/*.ts`, `src/**/*.tsx`;
- `CLAUDE.md`;
- `README.md` da raiz;
- workflow processável para tornar `G-FM` obrigatório.

## 11. Critérios de conclusão

O plano termina quando:

- a autorização mínima foi respeitada;
- existem somente os schemas autorizados, um por perfil;
- parser e testes passam para todos os perfis ativos;
- os pilotos de cada perfil foram aprovados;
- documentos não canônicos autorizados foram migrados sequencialmente;
- documentos canônicos receberam decisão explícita;
- o relatório final declara cobertura e exclusões com precisão por perfil;
- registro, versões e hashes dos documentos `governed` permanecem sincronizados;
- gates vigentes não apresentam regressão;
- nenhum item de backlog foi introduzido implicitamente.

## 12. Regra de parada

Uma revisão bloqueia a execução somente quando demonstrar:

- violação de schema vigente;
- contradição com política ou workflow vigente;
- perda de integridade;
- divergência entre Front Matter e registro (perfil `governed`);
- alteração não autorizada de documento aprovado;
- etapa tecnicamente inexequível.

Não bloqueiam:

- preferência de nomenclatura;
- arquitetura alternativa mais sofisticada;
- artefato auxiliar potencialmente útil;
- melhoria sem evidência de necessidade;
- desejo de ampliar cobertura;
- recomendação para trabalho futuro.

Quando os critérios de conclusão forem atendidos, o plano está encerrado.
Melhorias opcionais vão para backlog e não reabrem a aprovação.

## 13. Relação com os históricos

Este documento não substitui nem altera:

- [histórico do Claude Code](./HISTORICO-CLAUDE-CODE.md);
- [histórico do ChatGPT](./HISTORICO-CHATGPT.json);
- [histórico do plano expandido](./HISTORICO-PLANO.md).

Os três arquivos permanecem como evidência da orquestração humana e da expansão
recursiva de escopo. Este plano é uma revisão de escopo do plano mínimo anterior,
não uma edição retroativa do histórico.
