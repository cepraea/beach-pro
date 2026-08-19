# Fields registry — CEPRAEA BEACH PRO

<!-- EXCEÇÃO-DOC-FR-001: a seção 4 é um catálogo estrutural e excede o limite editorial para manter o inventário completo em um único artefato verificável. Escopo: seção 4. Responsável: FR-001. Encerramento: após a implementação do catálogo canônico completo e de sua validação determinística. -->

## 1. Finalidade e autoridade

Este arquivo cataloga os campos observados nos seis JSON Schemas executáveis de `docs/modelagem/schemas/`.
Os schemas continuam sendo os contratos executáveis; este registry não cria campos nem altera seus significados.

**Estado da implementação:** `FR-001_IN_PROGRESS`.

Nesta etapa inicial, o inventário registra `Field ID` e `Requirement` derivados dos schemas. `Type`, `Constraints`, `Definition` e `Purpose` ainda precisam ser consolidados antes de `FR-001` poder ser declarado `READY_FOR_REVIEW`.

## 2. Regras de sincronização

- A identidade canônica usa `<schema>::<json-path>`.
- `required`, `optional` e `conditional` derivam somente dos schemas vigentes.
- Campo ausente dos schemas não pode aparecer como `ACTIVE`.
- Definição semântica não sustentada permanece `PENDING_DEFINITION`.
- A ausência global de `additionalProperties: false` não é reinterpretada como bloqueio de propriedades desconhecidas.

## 3. Estados

Os estados previstos pelo plano são `ACTIVE`, `PROPOSED`, `DEPRECATED`, `REMOVED`, `REJECTED` e `PENDING_DEFINITION`.

O inventário abaixo ainda não constitui a tabela canônica final de `FR-001`.

## 4. Inventário estrutural inicial

A extração dos `properties` observados resultou em **132 fields**:

| Schema | Fields |
| --- | ---: |
| `schema_fonte.json` | 25 |
| `schema_evidencia.json` | 8 |
| `schema_termo.json` | 30 |
| `schema_regra.json` | 30 |
| `schema_decisao.json` | 14 |
| `schema_elemento_modelo.json` | 25 |
| **Total** | **132** |

### 4.1 `schema_fonte.json`

- `schema_fonte.json::id_fonte` — `required`
- `schema_fonte.json::id_acao` — `required`
- `schema_fonte.json::nome_arquivo_original` — `required`
- `schema_fonte.json::caminho_local` — `required`
- `schema_fonte.json::hash_sha256` — `required`
- `schema_fonte.json::id_drive` — `optional`
- `schema_fonte.json::tipo_arquivo` — `required`
- `schema_fonte.json::idioma` — `optional`
- `schema_fonte.json::tipo_fonte` — `required`
- `schema_fonte.json::autoridade_fonte` — `required`
- `schema_fonte.json::proveniencia_fonte` — `required`
- `schema_fonte.json::estado_fonte` — `required`
- `schema_fonte.json::estado_processamento` — `required`
- `schema_fonte.json::dado_sensivel_encontrado` — `required`
- `schema_fonte.json::tratamento_dado_sensivel` — `conditional`
- `schema_fonte.json::conceitos_encontrados` — `optional`
- `schema_fonte.json::regras_encontradas` — `optional`
- `schema_fonte.json::conflitos_ou_duvidas` — `optional`
- `schema_fonte.json::evidencia` — `required`
- `schema_fonte.json::evidencia.comando_ou_metodo` — `required`
- `schema_fonte.json::evidencia.resultado` — `required`
- `schema_fonte.json::evidencia.repository_evidence` — `conditional`
- `schema_fonte.json::evidencia.repository_evidence.action_ref` — `conditional`
- `schema_fonte.json::evidencia.limitacoes` — `optional`
- `schema_fonte.json::proxima_acao` — `optional`

### 4.2 `schema_evidencia.json`

- `schema_evidencia.json::id_evidencia` — `required`
- `schema_evidencia.json::id_fonte` — `required`
- `schema_evidencia.json::id_acao` — `required`
- `schema_evidencia.json::localizacao` — `required`
- `schema_evidencia.json::trecho_literal` — `required`
- `schema_evidencia.json::tipo_evidencia` — `required`
- `schema_evidencia.json::dado_sensivel_encontrado` — `required`
- `schema_evidencia.json::tratamento_dado_sensivel` — `conditional`

### 4.3 `schema_termo.json`

- `schema_termo.json::id_termo` — `required`
- `schema_termo.json::termo_preferencial` — `required`
- `schema_termo.json::nome_canonico` — `required`
- `schema_termo.json::classificacao` — `required`
- `schema_termo.json::definicao` — `required`
- `schema_termo.json::contexto_valido` — `optional`
- `schema_termo.json::contexto_invalido` — `optional`
- `schema_termo.json::inclusoes` — `optional`
- `schema_termo.json::exclusoes` — `optional`
- `schema_termo.json::sinonimos` — `optional`
- `schema_termo.json::termos_relacionados` — `optional`
- `schema_termo.json::fonte` — `required`
- `schema_termo.json::valores_permitidos` — `optional`
- `schema_termo.json::temporalidade` — `optional`
- `schema_termo.json::natureza_e_privacidade` — `optional`
- `schema_termo.json::ativos_tecnicos` — `optional`
- `schema_termo.json::estado_epistemologico` — `required`
- `schema_termo.json::estado_tecnico` — `required`
- `schema_termo.json::limitacoes` — `optional`
- `schema_termo.json::evidencia` — `required`
- `schema_termo.json::evidencia.source_evidence` — `required`
- `schema_termo.json::evidencia.source_evidence.comando_ou_metodo` — `required`
- `schema_termo.json::evidencia.source_evidence.resultado` — `required`
- `schema_termo.json::evidencia.source_evidence.limitacoes` — `optional`
- `schema_termo.json::evidencia.semantic_evidence` — `conditional`
- `schema_termo.json::evidencia.approval_evidence` — `conditional`
- `schema_termo.json::evidencia.approval_evidence.aprovador` — `conditional`
- `schema_termo.json::evidencia.approval_evidence.data` — `conditional`
- `schema_termo.json::evidencia.repository_evidence` — `conditional`
- `schema_termo.json::evidencia.repository_evidence.action_ref` — `conditional`

### 4.4 `schema_regra.json`

- `schema_regra.json::id_regra` — `required`
- `schema_regra.json::fonte` — `required`
- `schema_regra.json::texto_original` — `optional`
- `schema_regra.json::tipo` — `required`
- `schema_regra.json::sujeito` — `required`
- `schema_regra.json::acao` — `required`
- `schema_regra.json::objeto` — `optional`
- `schema_regra.json::condicoes` — `optional`
- `schema_regra.json::excecoes` — `optional`
- `schema_regra.json::cardinalidade_minima` — `optional`
- `schema_regra.json::cardinalidade_maxima` — `optional`
- `schema_regra.json::vigencia` — `optional`
- `schema_regra.json::contexto_valido` — `optional`
- `schema_regra.json::contexto_invalido` — `optional`
- `schema_regra.json::conceitos_afetados` — `optional`
- `schema_regra.json::implementacao_candidata` — `optional`
- `schema_regra.json::estado_epistemologico` — `required`
- `schema_regra.json::estado_tecnico` — `required`
- `schema_regra.json::duvidas` — `optional`
- `schema_regra.json::evidencia` — `required`
- `schema_regra.json::evidencia.source_evidence` — `required`
- `schema_regra.json::evidencia.source_evidence.comando_ou_metodo` — `required`
- `schema_regra.json::evidencia.source_evidence.resultado` — `required`
- `schema_regra.json::evidencia.source_evidence.limitacoes` — `optional`
- `schema_regra.json::evidencia.semantic_evidence` — `conditional`
- `schema_regra.json::evidencia.approval_evidence` — `conditional`
- `schema_regra.json::evidencia.approval_evidence.aprovador` — `conditional`
- `schema_regra.json::evidencia.approval_evidence.data` — `conditional`
- `schema_regra.json::evidencia.repository_evidence` — `conditional`
- `schema_regra.json::evidencia.repository_evidence.action_ref` — `conditional`

### 4.5 `schema_decisao.json`

- `schema_decisao.json::id_decisao` — `required`
- `schema_decisao.json::data` — `required`
- `schema_decisao.json::decisao` — `required`
- `schema_decisao.json::alternativas` — `optional`
- `schema_decisao.json::escolha` — `required`
- `schema_decisao.json::justificativa` — `required`
- `schema_decisao.json::fonte` — `required`
- `schema_decisao.json::impacto` — `optional`
- `schema_decisao.json::riscos` — `optional`
- `schema_decisao.json::aprovador` — `required`
- `schema_decisao.json::estado` — `required`
- `schema_decisao.json::evidencia` — `conditional`
- `schema_decisao.json::evidencia.repository_evidence` — `conditional`
- `schema_decisao.json::evidencia.repository_evidence.action_ref` — `conditional`

### 4.6 `schema_elemento_modelo.json`

- `schema_elemento_modelo.json::id_elemento` — `required`
- `schema_elemento_modelo.json::tipo` — `required`
- `schema_elemento_modelo.json::nome` — `required`
- `schema_elemento_modelo.json::estagio` — `required`
- `schema_elemento_modelo.json::promoted_from` — `conditional`
- `schema_elemento_modelo.json::promoted_by` — `conditional`
- `schema_elemento_modelo.json::promoted_to` — `conditional`
- `schema_elemento_modelo.json::bounded_context_id` — `optional`
- `schema_elemento_modelo.json::detalhes` — `optional`
- `schema_elemento_modelo.json::maturidade` — `conditional`
- `schema_elemento_modelo.json::fonte` — `required`
- `schema_elemento_modelo.json::estado_epistemologico` — `required`
- `schema_elemento_modelo.json::estado_tecnico` — `required`
- `schema_elemento_modelo.json::ambiguidades` — `optional`
- `schema_elemento_modelo.json::evidencia` — `required`
- `schema_elemento_modelo.json::evidencia.source_evidence` — `required`
- `schema_elemento_modelo.json::evidencia.source_evidence.comando_ou_metodo` — `required`
- `schema_elemento_modelo.json::evidencia.source_evidence.resultado` — `required`
- `schema_elemento_modelo.json::evidencia.source_evidence.limitacoes` — `optional`
- `schema_elemento_modelo.json::evidencia.semantic_evidence` — `conditional`
- `schema_elemento_modelo.json::evidencia.approval_evidence` — `conditional`
- `schema_elemento_modelo.json::evidencia.approval_evidence.aprovador` — `conditional`
- `schema_elemento_modelo.json::evidencia.approval_evidence.data` — `conditional`
- `schema_elemento_modelo.json::evidencia.repository_evidence` — `conditional`
- `schema_elemento_modelo.json::evidencia.repository_evidence.action_ref` — `conditional`

## 5. Pendências de `FR-001`

Antes de declarar `FR-001` concluída, este inventário deve ser convertido na tabela canônica com as colunas `Field ID`, `Schema`, `Path`, `Type`, `Requirement`, `Constraints`, `Definition`, `Purpose`, `Status` e `Source`, usando apenas os seis schemas como fonte estrutural.

`Definition` e `Purpose` devem permanecer `PENDING_DEFINITION` até `FR-002` quando o significado não estiver sustentado.

## 6. Histórico de revisões

| Data | Tarefa | Alteração | Estado |
| --- | --- | --- | --- |
| 2026-08-19 | `FR-001` | Criação do arquivo e inventário inicial de 132 field IDs. | `IN_PROGRESS` |
