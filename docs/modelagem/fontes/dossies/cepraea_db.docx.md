# `SRC-003` — `CEPRAEA-DB.docx`

## Identificação

- Nome do arquivo: `CEPRAEA-DB.docx`
- ID do Drive: não recuperável neste ambiente (`id_drive=null`, permitido — seção 5.1 do plano).
- ID interno: `SRC-003` / `AC-003`
- Tipo de arquivo: `docx` (Office Open XML; ~3,2 MB no disco, mas ~3 MB são fontes embutidas —
  `word/fonts/GoogleSans-*.ttf` —, não conteúdo textual; `word/document.xml` extraído tem 1,98 MB)
- Idioma: pt-BR
- Escopo temporal: sem data explícita no corpo extraído; referencia um inventário do Google Drive
  datado de 2026-06-14.
- Classe hipotética (seção 10 do plano): `TÉCNICA·AUXILIAR·ORIGINAL`, com `estado_fonte=SUBSTITUIDA`
  **fixado por `DEC-002` (D-02)** — mesma aplicação direta de decisão já resolvida, não derivada do
  conteúdo desta ação.
- Hash: `a3143854ef77f8a8f9a88fabefe3944bae7ee7c89894aba86f2d34d84050317a` (SHA-256, verificado via
  `sha256sum` e `node:crypto`, ambos concordantes)
- Caminho local: `.drive/CEPRAEA BEACH PRO/CEPRAEA-DB.docx`

## Seleção de conteúdo

Documento de 4059 linhas de texto extraído, íntegro. Extração via `perl -MIO::Uncompress::Unzip`
(membro `word/document.xml`) + mesmo parser Node de `AC-002`. Diferente de `BancoCEPRAEA.docx`
(`AC-002`), **este documento não contém nenhuma tabela física, `CREATE TABLE` ou schema SQL** —
confirmado por busca textual (`create table`/`CREATE TABLE`: zero ocorrências) e por leitura
estrutural completa. É um **framework de governança e método** ("PLANO MESTRE PARA CRIAÇÃO DO
BANCO DE DADOS DO PWA") para a tentativa de modelagem anterior — não um schema físico como o nome
sugeriria.

Estrutura: um bloco normativo de controle (`C0`–`C15`: autoridade, fronteiras, ações controladas,
estados/transições, evidências, portões de validação, testes do comportamento da IA, condições de
parada) seguido de ações controladas executadas (`ACT-F00-001` a `ACT-F00-009`, `ACT-F01-001`,
`ACT-F02-001`/`002`, `ACT-F03-001`, `ACT-F04-001` e subitens `.1`–`.8`). Não foi reprocessado
item a item — conforme a particularidade desta linha na seção 10 do plano, o inventário embutido de
65 fontes de `BEACH HANDBALL` (seção "C17.2 Resultado reconciliado"/"C17.3 Inventário atual
integral" do documento-fonte — o inventário histórico de 43 itens está em C15.3, distinto do
inventário reconciliado de 65 itens; ID de pasta do Drive `1Z0OsR3dHmLMED0KYc_EE2lD1nEYykzWY`) foi
**apenas referenciado, não reprocessado** — está fora do escopo desta fase (`docs/modelagem/README.md`, `READ_SCOPE` cobre `.drive/CEPRAEA BEACH PRO/**`,
não `.drive/BEACH HANDBALL/**`).

## Resultado da análise

- **Achado principal — por que a tentativa anterior foi declarada falha (contexto para `DEC-002`):**
  este documento nunca chega a produzir schema físico, `CREATE TABLE` ou modelo lógico. Toda a
  extensão lida (as 9 ações `ACT-F00-NNN` da "Fase 0") é dedicada a construir infraestrutura de
  governança da própria governança — portões (`GATE-F00-GOV-01`), padrão "Maker/Checker",
  canonicalização JSON, migração append-only de registros históricos, piloto de extração
  heterogênea com vetores de teste negativos. A última linha do documento extraído é uma
  "Diretriz de Execução Imediata" para *começar* a Fase 4 (extração em lote), ainda dentro da
  Fase 0. Nenhuma tabela, coluna ou `CREATE TABLE` aparece em nenhum ponto do texto. Isto é
  evidência direta e concreta de que a tentativa anterior investiu extensamente em controle formal
  do processo sem alcançar o produto (banco de dados) que o próprio documento nomeia como
  objetivo — precedente relevante para a mesma classe de risco identificada nesta sessão sobre a
  governança atual do repositório.
- Conceitos/fatos de domínio: `C1.5 Contexto fixado` declara "um treinador e 19 atletas adultas",
  "handebol de areia", "adulto feminino", "backend previsto Supabase/PostgreSQL" — todos já
  estabelecidos por `DEC-006`/`INV-001`/README.md; esta fonte **corrobora**, não introduz.
- Princípios de escopo negativo (`C2.2`) coincidem com invariantes/decisões já registradas nesta
  modelagem, sem gerar candidato novo: "inserir dados pessoais reais em seeds ou ambientes de
  teste" proibido (já coberto por `README.md`/`DEC-019`, dados sintéticos); "apagar fatos
  históricos para representar correções" proibido (já coberto por `INV-005`, registrada em
  `AC-002`); "substituir decisão técnica do treinador" fora de escopo (coerente com `INV-001`,
  papel operacional único).
- Nenhum candidato de invariante, termo ou regra novo registrado nesta ação — todo conteúdo
  relevante de domínio já está coberto por elementos existentes (`INV-001`, `INV-005`, `DEC-006`).
  Registrar duplicata aqui violaria o mesmo princípio que motivou `INV-005`/o antiobjetivo de
  `modelagem_dominio_dados.md` §37 (não criar entidade/elemento sem necessidade operacional).
- Fatos operacionais: nenhum novo.
- Relações e cardinalidades: não aplicável — fonte não contém schema físico.
- Conflitos ou dúvidas:
  1. O inventário de 65 fontes de `BEACH HANDBALL` embutido nesta fonte é material científico/
     técnico de referência (ex.: `EVD-0064` abaixo) potencialmente relevante para uma fase futura
     de fundamentação normativa/científica — não avaliado nesta ação por estar fora do
     `READ_SCOPE` atual. Registrado como candidato de escopo futuro, não como pendência bloqueante
     desta ação.
- Artefatos técnicos afetados: nenhum (fora de escopo desta fase — seção 3 do plano).
- Testes afetados: nenhum (fora de escopo desta fase).
- Estado final do arquivo: `CONCLUIDO`.
- Próxima ação: `AC-004` (`CEPRAEA DATABASE.xlsx`) — teste real da hipótese `DB_EXPORT_FRONTEND`/
  `DB_PRESENCA_FATUAL` levantada em `AC-001`, ainda pendente.

## Dados sensíveis

Nenhum dado pessoal real encontrado. Checagem de padrões sensíveis (`senha`/`password`/`cpf`)
sobre o texto extraído: zero ocorrências. Classificação: não aplicável
(`dado_sensivel_encontrado=false`).

## Critério de saída

- [x] Identidade e classe de autoridade registradas (classificação fixada por `DEC-002`, verificada
      contra o conteúdo real).
- [x] Escopo usado registrado — documento lido integralmente; inventário de 65 fontes de `BEACH
      HANDBALL` explicitamente referenciado e não reprocessado, conforme particularidade da seção
      10 do plano.
- [x] Trechos relevantes localizados (6 fragmentos em `evidencias/registro_evidencias.md`,
      `EVD-0063` a `EVD-0068`).
- [x] Interpretação separada do texto original.
- [x] Conflitos e precedências resolvidos ou explicitamente registrados (1 item acima, não
      bloqueante).
- [x] Nenhum conceito/regra/candidato duplicado — verificado que todo o conteúdo relevante já
      está coberto por `INV-001`, `INV-005`, `DEC-006`.
- [x] Nenhuma conclusão excede o que a fonte sustenta.
- [x] Nenhum dado sensível transcrito literalmente (nenhum foi encontrado).

```json
{
  "id_fonte": "SRC-003",
  "id_acao": "AC-003",
  "nome_arquivo_original": "CEPRAEA-DB.docx",
  "caminho_local": ".drive/CEPRAEA BEACH PRO/CEPRAEA-DB.docx",
  "hash_sha256": "a3143854ef77f8a8f9a88fabefe3944bae7ee7c89894aba86f2d34d84050317a",
  "id_drive": null,
  "tipo_arquivo": "docx",
  "idioma": "pt-BR",
  "tipo_fonte": "TECNICA",
  "autoridade_fonte": "AUXILIAR",
  "proveniencia_fonte": "ORIGINAL",
  "estado_fonte": "SUBSTITUIDA",
  "estado_processamento": "CONCLUIDO",
  "dado_sensivel_encontrado": false,
  "conceitos_encontrados": [],
  "regras_encontradas": [],
  "conflitos_ou_duvidas": [
    "Inventário de 65 fontes de BEACH HANDBALL embutido nesta fonte (científico/técnico de referência) não avaliado nesta ação — fora do READ_SCOPE atual (.drive/CEPRAEA BEACH PRO/** apenas). Candidato de escopo futuro, não pendência bloqueante."
  ],
  "evidencia": {
    "comando_ou_metodo": "perl -MIO::Uncompress::Unzip=unzip (extração de word/document.xml) + parser Node próprio + sha256sum/node:crypto para hash; busca textual por 'create table'/'CREATE TABLE' e por padrões sensíveis ('senha','password','cpf')",
    "resultado": "documento de 4059 linhas de texto reconstruído lido por completo; zero ocorrências de CREATE TABLE/schema físico; zero ocorrências de padrão sensível; confirmado framework de governança/método (blocos C0-C15 + ações ACT-F00-001 a ACT-F04-001.8) sem chegar a produto de banco de dados",
    "repository_evidence": {
      "action_ref": "AC-003"
    },
    "limitacoes": [
      "Leitura completa do texto reconstruído, mas sem verificação byte-a-byte contra o XML bruto além do já feito por amostragem no parser (mesmo método validado em AC-002)."
    ]
  },
  "proxima_acao": "AC-004 (CEPRAEA DATABASE.xlsx) continua sendo o teste real das hipóteses DB_EXPORT_FRONTEND/DB_PRESENCA_FATUAL/DB_INDICADORES_DISPONIBILIDADE/DB_PARTICIPACAO_JOGO levantadas em AC-001."
}
```
