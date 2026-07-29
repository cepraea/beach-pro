# Plano de reconstrução do mapa e correção incremental do validador

## 1. Identificação

| Campo | Valor |
| --- | --- |
| Artefato atual | `scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md` |
| Implementação atual | `scripts/documentation/validate_documentation/__init__.py` |
| README operacional | `scripts/documentation/validate_documentation/README.md` |
| Natureza | Plano de correção incremental orientado a agentes de IA |
| Estratégia | Patches locais por função, sem reescrita integral |
| Framework de testes | `unittest` da biblioteca padrão |
| Verificação estática | Pylance/Pyright em modo `strict` |
| Estado | Execução concluída em 2026-07-29 |

## Estado da execução

Sucessão estrutural concluída pelo
[`Plano-migracao-validator.md`](Plano-migracao-validator.md): o mapa foi movido
para junto do pacote, a implementação passou a residir em `__init__.py` e o
encaminhador temporário foi removido. A restrição de movimentação deste plano
aplicava-se à correção incremental já concluída.

Execução concluída:

- Ações 1–3: mapa reconstruído, `pyrightconfig.json` em `strict`, imports e
  fronteira dinâmica corrigidos;
- Ações 4–8: Reporter, CLI tipada, identidade persistível, resolução exata de
  versão, segurança de links e invariantes tipados implementados;
- Ações 9–11: instâncias de documentos, workflow, gates e evidências separadas;
  referências de aprovações, workflow e ingestão cobertas isoladamente;
- Ações 12–14: G-ARCH explícito; escopos globais protegidos; G2 indexado por
  `(document_id, version)`; G-FM rejeita versão ausente, ambígua ou inexistente;
- Ação 15: `main()` reduzido a orquestração fail-fast entre etapas, com emissão
  única;
- Ação 16: README, mapa, testes, compilação, lint e strict-mode consolidados;
- verificação final: 72 testes verdes, compilação verde, Pyright strict com
  zero diagnósticos e Markdownlint verde nos três documentos desta execução.

Estado documental observado ao concluir:

- `registry.canonical_documents` contém os cinco registros
  `CANONICA_VIGENTE`;
- os documentos-alvo mantêm as relações com as aprovações corretivas;
- as aprovações corretivas e seus quatro resultados de gate existem e os hashes
  dos dois canônicos citados na não conformidade original coincidem com o
  registro;
- validação global, G-ARCH, G0, G1 e G-FM localizado passam;
- G2 passa para a versão `0.1`, coberta pelo pacote de proveniência existente;
  a versão canônica `0.1.1` falha explicitamente por ainda não possuir pacote
  de proveniência próprio.

## 2. Objetivo

Transformar `MAPA-VALIDADOR-DOC.md` em um guia que permita a um agente:

1. localizar a menor unidade responsável por um defeito;
2. entender o contrato e as invariantes dessa unidade;
3. criar primeiro um teste vermelho que reproduza a falha;
4. aplicar um patch local, sem reescrever o script inteiro;
5. executar o teste verde correspondente;
6. confirmar ausência de regressão na suíte existente;
7. preservar imports, contratos, schemas e comportamento fora do escopo.

O mapa final não será uma cópia do código. Após a sucessão estrutural, a fonte
executável passou a ser
`scripts/documentation/validate_documentation/__init__.py`, executada pelo
módulo `scripts.documentation.validate_documentation`.

## 3. Restrições globais

### 3.1 Regra de qualidade obrigatória

> **Regras de Qualidade:** O código **DEVE** ser autoexplicativo, mas cada
> função complexa deve conter *docstrings* ou *comentários inline* voltados para
> outros desenvolvedores ou agentes de IA. Comentar o "porquê" de decisões
> técnicas para mitigar erros em futuras manutenções.

Aplicação:

- comentar invariantes, decisões de segurança e razões de governança;
- não comentar operações óbvias linha a linha;
- manter docstrings sincronizadas com assinatura, retorno e efeitos colaterais;
- atualizar ou remover comentários que deixarem de corresponder ao código;
- não usar comentários para silenciar diagnósticos ou justificar código morto.

### 3.2 Limite de alteração

- Não mover o script para outro módulo.
- Não dividir o script em múltiplos arquivos Python nesta execução.
- Não introduzir Pydantic.
- Não criar factories, frameworks ou abstrações sem necessidade demonstrada.
- Não reescrever `main()` antes de corrigir e testar as funções chamadas por ele.
- Não alterar schemas ou documentos governados para fazer o validador passar.
- Não usar `# type: ignore`, `# pyright: ignore` ou casts como correção padrão.
- Não adicionar imports durante as ações funcionais.

### 3.3 Regra única de imports

A única ação autorizada sobre imports do script é:

```python
from typing import Any
```

e a remoção de:

```python
import sys
```

Depois dessa ação, todos os cartões devem declarar `NÃO ADICIONAR IMPORTS`.
`Any` é usado somente na fronteira dinâmica de YAML/JSON; depois da validação
estrutural, os valores devem ser estreitados para tipos concretos.

### 3.4 Estratégia de falha

O comportamento desejado é **fail-fast entre etapas e coleta completa dentro da
etapa**:

1. uma etapa pode registrar todos os seus achados relacionados;
2. `main()` não inicia a próxima etapa se a etapa anterior registrou erro;
3. erros que impedem leitura, como registro ausente ou YAML raiz inválido,
   encerram imediatamente;
4. `Reporter.emit()` é o único ponto de emissão do resultado final.

Essa definição elimina a contradição atual entre "acumular erros" e "parar na
primeira falha".

## 4. Conteúdo do mapa atual: decisão de preservação

### 4.1 Conteúdo que deve permanecer

| Conteúdo | Tratamento |
| --- | --- |
| Reporter centralizado | Manter e atualizar para o payload real |
| Contratos de entrada, saída e mutação | Manter por unidade |
| Pylance/Pyright strict-mode | Manter com referências oficiais |
| Null safety | Manter, distinguindo fronteira dinâmica de dados já estreitados |
| Remoção de imports não usados | Manter |
| Regra de qualidade e comentários de "porquê" | Manter integralmente |
| Segurança contra path traversal | Manter e aplicar também a links |
| Teste antes da correção | Manter como ciclo vermelho/verde |
| Fail-fast | Manter com a semântica por etapas da seção 3.4 |
| Dependências PyYAML e jsonschema | Manter com links e uso real |

### 4.2 Conteúdo que deve ser transformado

| Conteúdo atual | Transformação |
| --- | --- |
| Mapa com apenas quatro componentes | Substituir pelo inventário completo de unidades |
| Trechos extensos de código | Reduzir a assinaturas e pequenos exemplos locais |
| "Código completo consolidado" | Remover; apontar para o script real |
| `validate_links` como "Ghost Code" | Documentar a implementação e o defeito real |
| pytest como suíte existente | Substituir por `unittest`, já adotado no repositório |
| Testes fictícios | Converter em testes planejados, com caminho e expectativa |
| Pylance sem enforcement | Adicionar ação específica de configuração e verificação |
| Fail-fast absoluto | Substituir por fail-fast entre etapas |
| `isinstance()` genericamente desencorajado | Permitir na fronteira YAML/JSON; evitar após narrowing |
| Dependências por `requirements.txt` inexistente | Documentar instalação direta até existir decisão de empacotamento |

### 4.3 Conteúdo que deve ser removido

- prompts de persona para agentes;
- feedback editorial sobre o próprio documento;
- perguntas como "Deseja criar um teste?";
- blocos Python sintaticamente inválidos;
- manifesto de testes duplicado;
- afirmação de que o mapa é a fonte de verdade do código;
- recomendações genéricas não vinculadas a uma função;
- instruções que exijam arquivos ou dependências inexistentes.

## 5. Modelo obrigatório de cartão de intervenção

Cada unidade do novo mapa deve usar este formato:

```markdown
### Unidade N — Nome

**Localização:** da função `x` até antes da função `y`.

**Responsabilidade:** uma frase.

**Contrato:**
- entrada;
- saída;
- mutação;
- erros.

**Diagnósticos relevantes:** regras Pylance/Pyright.

**Alterações permitidas:** lista fechada.

**Alterações proibidas:**
- não adicionar imports;
- não editar unidades adjacentes;
- não alterar schemas/documentos para satisfazer o teste.

**Porquê preservado:** decisão técnica que merece docstring/comentário.

**Teste vermelho:** nome, arranjo e falha esperada.

**Teste verde:** nome, arranjo e sucesso esperado.

**Critérios de aceitação:** lista verificável.

**Comandos:** teste localizado, suíte e verificação estática.
```

## 6. Convenção de testes

### 6.1 Significado

- **Teste vermelho:** deve falhar antes da correção pela razão exata que a ação
  pretende resolver. Falha por import, fixture ou sintaxe não é um vermelho
  válido.
- **Teste verde:** é o mesmo comportamento após a correção, agora passando.
- Cada vermelho deve possuir uma mensagem ou asserção específica.
- Cada ação deve rodar também toda a suíte existente.

### 6.2 Localização planejada

| Arquivo | Cobertura |
| --- | --- |
| `scripts/documentation/tests/test_reporter.py` | payload e códigos de saída |
| `scripts/documentation/tests/test_target_resolution.py` | `(document_id, version)` |
| `scripts/documentation/tests/test_paths_and_links.py` | workspace e links |
| `scripts/documentation/tests/test_registry_validation.py` | registros e unicidade |
| `scripts/documentation/tests/test_instances.py` | schemas e instâncias |
| `scripts/documentation/tests/test_approvals.py` | hashes e evidências |
| `scripts/documentation/tests/test_workflow_ingestion.py` | workflow e ingestão |
| `scripts/documentation/tests/test_gates.py` | G-ARCH, G0 e G1 |
| `scripts/documentation/tests/test_provenance.py` | G2 |
| `scripts/documentation/tests/test_front_matter.py` | G-FM, já existente |
| `scripts/documentation/tests/test_main.py` | fail-fast e CLI end-to-end |

Todos os testes usam `unittest`. Não adicionar pytest.

## 7. Ações de implementação

### Ação 1 — Reestruturar o mapa como índice de intervenções

**Escopo atual:** somente
`scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md`.

**Ações:**

1. preservar as regras listadas em 4.1;
2. remover o conteúdo listado em 4.3;
3. criar índice das unidades reais do script;
4. adicionar o modelo de cartão da seção 5;
5. declarar que o mapa orienta patches e o script é a fonte executável;
6. adicionar links cruzados para o plano e para o README operacional.

**Teste vermelho:**

- `test_map_has_single_test_manifest`: falha enquanto houver duas seções
  "Manifesto de Testes Unitários";
- `test_map_does_not_claim_embedded_source_of_truth`: falha enquanto o mapa
  disser que o código copiado é a fonte de verdade.

**Teste verde:**

- cada seção normativa aparece uma única vez;
- não existe bloco de "código completo consolidado";
- todas as unidades do script aparecem no índice.

**Critérios de aceitação:**

- regra de qualidade preservada textualmente;
- nenhuma cópia integral do script;
- nenhuma sintaxe Python inválida;
- todos os cartões possuem limites de edição e testes vermelho/verde;
- mapa utilizável sem exigir leitura integral do script.

### Ação 2 — Ativar verificação Pylance/Pyright strict

**Escopo:** configuração do workspace e documentação; não alterar lógica.

**Ações:**

1. registrar `python.analysis.typeCheckingMode: strict` no workspace ou criar
   configuração Pyright equivalente mediante decisão do projeto;
2. limitar inicialmente a análise ao script e seus testes;
3. capturar o baseline de diagnósticos por categoria;
4. não reduzir severidade para obter verde artificial.

**Teste vermelho:**

- abrir/analisar o script em strict e confirmar diagnósticos como
  `reportMissingTypeArgument`, `reportUnknownVariableType` e
  `reportUnusedImport`.

**Teste verde:**

- a análise strict do script e dos testes termina sem erros;
- nenhuma regra relevante está desativada.

**Critérios de aceitação:**

- strict-mode efetivamente ativo;
- resultado reproduzível por outro agente;
- zero `type: ignore`;
- baseline anexado à evidência da ação.

### Ação 3 — Corrigir imports e definir a fronteira dinâmica

**Localização:** cabeçalho do script até antes de `WORKSPACE_ROOT`.

**Ações:**

1. remover `import sys`;
2. adicionar `from typing import Any`;
3. documentar no mapa que YAML/JSON entram como `Any`;
4. proibir qualquer import adicional nos cartões seguintes.

**Teste vermelho:**

- strict-mode acusa `reportUnusedImport` para `sys`;
- strict-mode acusa coleções sem argumentos de tipo nas funções posteriores.

**Teste verde:**

- nenhum import não utilizado;
- `Any` está disponível para assinaturas dinâmicas;
- importação do módulo continua funcionando.

**Critérios de aceitação:**

- somente a troca autorizada de imports;
- `python3 -m compileall -q scripts/documentation/validate_documentation`
  passa;
- nenhuma dependência nova.

### Ação 4 — Tipar e documentar `Reporter`

**Localização:** `class Reporter`.

**Ações:**

1. tipar explicitamente o payload heterogêneo de `emit()`;
2. preservar todos os campos exigidos por `resultado-gate.schema.json`;
3. manter `print()` apenas em `emit()`;
4. explicar por que erros são ordenados antes da emissão;
5. permitir que um resultado persistível receba identidade não ambígua na ação
   de CLI, sem gerar IDs duplicados silenciosamente.

**Teste vermelho:**

- `test_yaml_result_matches_gate_result_schema` falha se faltar qualquer campo;
- `test_reporter_is_only_output_boundary` falha se outra unidade imprimir erro;
- `test_runtime_id_is_not_persistable_twice` demonstra colisão do ID constante.

**Teste verde:**

- payload YAML valida contra o schema;
- saída textual contém erros, avisos e resumo;
- saída de sucesso retorna `0`; falha retorna `1`;
- resultado persistível possui ID explícito ou determinístico e único.

**Critérios de aceitação:**

- assinatura integralmente tipada;
- nenhum campo do schema perdido;
- comentários explicam determinismo e fronteira de saída;
- testes não dependem do relógio real sem controle.

### Ação 5 — Tipar CLI e validar combinações de argumentos

**Localização:** `parse_args()` e helper de validação dos argumentos.

**Ações:**

1. documentar todos os gates atuais;
2. rejeitar `--version` sem `--document-id`;
3. exigir `--version` quando o ID tiver múltiplas versões;
4. rejeitar escopo em gate que for formalmente global;
5. adicionar opção de ID de resultado somente se necessária para persistência;
6. não adicionar biblioteca de CLI.

**Teste vermelho:**

- `test_version_without_document_id_is_rejected`;
- `test_ambiguous_document_id_requires_version`;
- `test_unknown_gate_scope_is_rejected`.

**Teste verde:**

- combinações válidas são aceitas;
- mensagens de erro identificam o argumento problemático;
- `--help` lista G-ARCH, G0, G1, G2 e G-FM.

**Critérios de aceitação:**

- nenhum `AttributeError` de `Namespace`;
- contrato CLI documentado no README;
- erros de uso retornam código não zero;
- nenhuma alteração em gates nesta ação.

### Ação 6 — Criar resolução exata de `(document_id, version)`

**Localização:** após `validate_top_level()` e antes de `validate_record()`.

**Ações:**

1. criar helper local `resolve_document_version`;
2. selecionar pelo par exato quando a versão for informada;
3. falhar quando o ID ou a versão não existir;
4. falhar por ambiguidade quando houver várias versões e nenhuma versão;
5. preencher `Reporter.document_id`, `version` e `content_hash` somente a partir
   do registro resolvido;
6. reutilizar o helper em `main()` e G2.

**Teste vermelho:**

- `test_resolver_does_not_return_first_version`;
- `test_resolver_rejects_unknown_version`;
- `test_resolver_rejects_ambiguous_id`.

**Teste verde:**

- CONTEXTO `0.1.1` resolve para `27a64560...`;
- DEC-019 `0.1.2` resolve para `447e1ee7...`;
- versão inexistente produz erro e não metadados da versão antiga.

**Critérios de aceitação:**

- nenhuma chamada a `next()` seleciona somente por `document_id`;
- metadados YAML correspondem ao par solicitado;
- helper possui docstring explicando identidades permanentes com versões
  simultâneas;
- nenhuma alteração de registro ou documento.

### Ação 7 — Endurecer caminhos, nomes e links

**Localização:** `workspace_path()` até `validate_links()`.

**Ações:**

1. preservar `sha256()` e `valid_name()` como funções pequenas;
2. fazer todo destino local de link passar pela fronteira do workspace;
3. rejeitar caminhos absolutos externos e `..` que escapem;
4. definir tratamento de links externos, âncoras e referências com linha;
5. documentar por que `Path.resolve()` sozinho não constitui autorização.

**Teste vermelho:**

- `test_markdown_link_cannot_escape_workspace`;
- `test_absolute_external_path_is_rejected`;
- `test_broken_internal_link_fails`.

**Teste verde:**

- link interno existente passa;
- âncora local é ignorada corretamente;
- URL HTTP/HTTPS não é tratada como arquivo;
- referência `arquivo.md:12` resolve o arquivo correto.

**Critérios de aceitação:**

- nenhuma chamada a `exists()` para destino local não validado;
- symlinks não permitem escapar do workspace;
- erros identificam o documento de origem;
- nenhuma mudança em regras de nome nesta ação.

### Ação 8 — Completar tipagem e invariantes de registro

**Localização:** `validate_top_level()`, `validate_record()`,
`validate_uniqueness()`, `managed_files()` e `validate_canonical_registry()`.

**Ações:**

1. substituir `list[dict]` e `dict` nus por tipos parametrizados;
2. estreitar cada valor dinâmico uma vez;
3. preservar auto-hash, terminalidade e caminhos canônicos;
4. manter unicidade por `(document_id, version)`;
5. manter unicidade de `current_path`, inclusive case-insensitive;
6. explicar o porquê da exceção `self_hash_exempt`.

**Teste vermelho:**

- `test_duplicate_document_version_fails`;
- `test_duplicate_path_casefold_fails`;
- `test_self_hash_exemption_outside_registry_fails`;
- `test_canonical_path_must_equal_current_path`.

**Teste verde:**

- duas versões distintas do mesmo ID são aceitas;
- registros válidos têm hash conferido;
- documento terminal preserva `canonical_path` histórico;
- registro autorreferente permanece a única exceção de hash.

**Critérios de aceitação:**

- zero coleção sem tipo nesta unidade;
- zero acesso inseguro a valor opcional;
- invariantes existentes preservadas;
- suíte de registro verde.

### Ação 9 — Decompor `validate_instances()` sem criar módulos

**Localização:** `validate_contract_schemas()` até antes de
`validate_approval_cross_references()`.

**Ações:**

1. extrair helpers no mesmo arquivo para:
   - documentos;
   - workflow;
   - resultados de gates;
   - evidências YAML;
2. manter `validate_instances()` apenas como orquestrador;
3. evitar releitura desnecessária dos mesmos schemas;
4. preservar `FormatChecker`;
5. documentar por que validação de schema não substitui referências cruzadas.

**Teste vermelho:**

- `test_invalid_document_instance_fails`;
- `test_invalid_workflow_instance_fails`;
- `test_invalid_gate_result_instance_fails`;
- `test_schema_valid_but_unknown_reference_still_fails`.

**Teste verde:**

- instâncias válidas passam por seus schemas;
- erro contém caminho do arquivo e caminho JSON da falha;
- validação cruzada continua executada depois do schema válido.

**Critérios de aceitação:**

- nenhuma função extraída excede responsabilidade única;
- nenhum arquivo Python novo;
- nenhum import novo;
- `validate_instances()` fica legível como sequência de etapas.

### Ação 10 — Completar referências cruzadas de aprovações

**Localização:** `validate_approval_cross_references()`.

**Ações:**

1. exigir alvo registrado para `(document_id, version)`;
2. comparar `approval.content_hash` com o alvo exato;
3. detectar `gate_result_id` duplicado antes de indexar;
4. exigir `status: pass`;
5. exigir `document_id`, `version` e `content_hash` não nulos em evidência
   documental;
6. validar igualdade exata entre gate e aprovação;
7. validar o conjunto obrigatório de gates, sem duplicatas;
8. validar relação aprovação → documento e documento → aprovação;
9. resolver `superseded_by` para um artefato existente antes de ignorar a
   aprovação anterior;
10. documentar por que aprovação histórica é preservada, mas não satisfaz a
    promoção atual.

**Teste vermelho:**

- `test_approval_unknown_target_fails`;
- `test_approval_hash_mismatch_fails`;
- `test_missing_evidence_id_fails`;
- `test_duplicate_gate_result_id_fails`;
- `test_null_scoped_gate_metadata_fails`;
- `test_non_passing_gate_fails`;
- `test_wrong_gate_set_fails`;
- `test_unresolved_superseded_by_fails`.

**Teste verde:**

- aprovação válida com quatro gates exatos passa;
- aprovação superada com sucessora válida é preservada e não bloqueia;
- hash, documento e versão coincidem em toda a cadeia.

**Critérios de aceitação:**

- nenhuma evidência inexistente é aceita;
- nenhum campo nulo satisfaz aprovação documental;
- duplicatas não são sobrescritas silenciosamente;
- mensagens indicam aprovação e evidência envolvidas;
- função totalmente tipada e documentada.

### Ação 11 — Separar workflow e ingestão

**Localização:** `validate_workflow_references()` até antes de `validate_g0()`.

**Ações:**

1. tipar índices de estados, papéis, gates, contratos e transições;
2. validar referências sem assumir listas/dicionários antes do narrowing;
3. manter ingestão histórica separada de revisão corrente;
4. detectar IDs duplicados;
5. documentar por que o manifesto histórico não é reescrito por revisão nova.

**Teste vermelho:**

- `test_workflow_unknown_gate_reference_fails`;
- `test_duplicate_workflow_identifier_fails`;
- `test_ingestion_unknown_gate_result_fails`;
- `test_ingestion_snapshot_changed_same_version_fails`.

**Teste verde:**

- workflow válido resolve todas as referências;
- revisão posterior não invalida snapshot histórico;
- mesma versão com hash divergente continua bloqueada.

**Critérios de aceitação:**

- fronteiras históricas explicitadas em docstring;
- IDs duplicados reportados deterministicamente;
- nenhum `Any` vaza para operações sem narrowing.

### Ação 12 — Formalizar o escopo de G-ARCH, G0 e G1

**Localização:** `validate_g0()`, `validate_g1()` e despacho em `main()`.

**Ações:**

1. documentar G-ARCH como verificação arquitetural global ou implementar
   função explícita se houver requisito documental localizado;
2. decidir e registrar se G0/G1 são globais ou documentais;
3. impedir saída documental enganosa para gate global;
4. se forem documentais, receber o registro resolvido;
5. preservar a validação histórica de ingestão em função com nome próprio;
6. não usar a simples execução global de `validate_record()` como evidência
   implícita de um gate documental.

**Teste vermelho:**

- `test_global_gate_cannot_emit_scoped_metadata`;
- `test_scoped_gate_validates_requested_version`;
- `test_garch_has_explicit_dispatch`.

**Teste verde:**

- gate global emite campos documentais nulos;
- gate documental emite o alvo exato;
- comando e semântica correspondem ao workflow processável.

**Critérios de aceitação:**

- escopo de cada gate escrito no mapa e README;
- ausência de evidência com semântica ambígua;
- G0/G1 históricos continuam cobertos;
- nenhum gate é renomeado sem decisão documental.

### Ação 13 — Corrigir G2 para múltiplas versões

**Localização:** `validate_g2()`.

**Ações:**

1. substituir índice por `document_id` pelo par `(document_id, version)`;
2. reutilizar o resolvedor da Ação 6;
3. preservar verificações de fontes, claims e artefatos em TAR;
4. manter a proteção de caminhos dos arquivos preservados;
5. explicar por que proveniência deve apontar para bytes exatos.

**Teste vermelho:**

- `test_g2_does_not_overwrite_versions_by_document_id`;
- `test_g2_package_hash_mismatch_fails`;
- `test_g2_archive_escape_fails`.

**Teste verde:**

- pacote resolve a versão exata;
- fonte ativa e verificada passa;
- claim crítico coberto passa;
- incerteza explícita continua sendo tratada conforme política.

**Critérios de aceitação:**

- nenhuma versão sobrescreve outra;
- hash de pacote e registro coincidem;
- proteção contra path traversal preservada;
- função e helpers tipados.

### Ação 14 — Corrigir tipagem e seleção de G-FM

**Localização:** `_DuplicateKeyLoader` até `validate_front_matter()`.

**Ações:**

1. parametrizar todos os `dict` e retornos;
2. manter loader derivado de `SafeLoader`;
3. preservar detecção de chaves duplicadas;
4. fazer escopo inexistente falhar;
5. exigir versão quando houver versões simultâneas;
6. preservar os testes existentes de schema e sincronização;
7. documentar por que arquivos arquivados são excluídos do perfil ativo.

**Teste vermelho:**

- `test_scoped_front_matter_unknown_version_fails`;
- `test_scoped_front_matter_ambiguous_version_fails`;
- manter vermelhos existentes para YAML inválido, chave duplicada e campos
  divergentes.

**Teste verde:**

- alvo exato válido passa;
- todos os 23 testes existentes continuam verdes;
- feature specs continuam validadas sem registro mestre.

**Critérios de aceitação:**

- nenhum escopo vazio retorna sucesso;
- loader seguro preservado;
- corpo Markdown não é alterado;
- zero diagnóstico strict na unidade.

### Ação 15 — Reduzir `main()` a orquestração por etapas

**Localização:** `main()`.

**Pré-condição:** Ações 3 a 14 verdes.

**Ações:**

1. validar argumentos;
2. carregar e estreitar registro;
3. resolver alvo quando solicitado;
4. executar, nesta ordem:
   - contratos e instâncias;
   - integridade do registro e arquivos;
   - canonicalidade;
   - gate solicitado;
   - links;
   - emissão;
5. parar entre etapas quando houver erros;
6. nunca duplicar dentro de `main()` lógica pertencente a helper;
7. explicar a decisão fail-fast por etapas.

**Teste vermelho:**

- `test_main_stops_before_files_when_contract_stage_fails`;
- `test_main_stops_before_gate_when_registry_stage_fails`;
- `test_main_stops_before_links_when_gate_fails`;
- `test_main_uses_exact_scoped_record`.

**Teste verde:**

- pipeline válido executa todas as etapas uma vez;
- cada falha impede somente etapas posteriores;
- `Reporter.emit()` é chamado uma vez;
- códigos de saída são determinísticos.

**Critérios de aceitação:**

- `main()` contém composição, não regras de negócio;
- ordem do mapa corresponde ao código;
- nenhum import novo;
- nenhuma regressão na suíte.

### Ação 16 — Consolidar suíte e documentação operacional

**Escopo:** testes, mapa e README.

**Ações:**

1. executar todos os testes localizados;
2. executar a suíte completa;
3. executar strict-mode;
4. executar validação global em fixture limpa;
5. atualizar o mapa apenas com contratos estáveis;
6. atualizar o README com CLI e limitações restantes;
7. remover do README comandos para arquivos inexistentes.

**Teste vermelho:**

- busca encontra referência a pytest ou teste inexistente como estado atual;
- README omite G-FM, `--document-id` ou `--version`;
- mapa contém código completo duplicado.

**Teste verde:**

- documentação corresponde ao `--help`;
- todos os caminhos documentados existem;
- todos os testes estão listados corretamente;
- links oficiais abrem e sustentam a regra associada.

**Critérios de aceitação:**

- suíte completa verde;
- strict-mode verde;
- README útil para execução;
- mapa útil para correção localizada;
- nenhuma divergência conhecida escondida.

## 8. Ordem obrigatória de execução

```text
Ação 1  — mapa
Ação 2  — enforcement strict
Ação 3  — imports
Ação 4  — Reporter
Ações 5–6 — CLI e resolução
Ações 7–9 — infraestrutura de validação
Ação 10 — aprovações
Ação 11 — workflow/ingestão
Ações 12–14 — gates
Ação 15 — main
Ação 16 — consolidação
```

Não executar a Ação 15 antecipadamente. Isso evitará que o agente reescreva o
orquestrador para compensar contratos ainda defeituosos.

## 9. Comandos de verificação

### 9.1 Sintaxe

```bash
python3 -m compileall -q scripts/documentation/validate_documentation
```

### 9.2 Teste localizado

```bash
python3 -m unittest \
  scripts.documentation.tests.test_target_resolution
```

O módulo varia conforme a ação.

### 9.3 Suíte completa

```bash
python3 -m unittest discover scripts/documentation/tests
```

### 9.4 Validador

```bash
python3 -m scripts.documentation.validate_documentation
python3 -m scripts.documentation.validate_documentation --gate G-ARCH
python3 -m scripts.documentation.validate_documentation --gate G0
python3 -m scripts.documentation.validate_documentation --gate G1
python3 -m scripts.documentation.validate_documentation --gate G-FM
```

### 9.5 Escopo exato

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G-FM \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1.1 \
  --format yaml
```

### 9.6 Verificação estática

Usar Pylance/Pyright em `strict`. Se a CLI do Pyright for adotada pelo projeto:

```bash
npx --yes pyright
```

Não declarar essa etapa verde enquanto o executável não estiver instalado e a
configuração strict não estiver ativa.

## 10. Baseline observado em 2026-07-29

- `MAPA-VALIDADOR-DOC.md`: 654 linhas, com conteúdo duplicado e código obsoleto;
- `validate_documentation.py`: aproximadamente 1.680 linhas;
- suíte existente: 23 testes de Front Matter, todos verdes;
- não existem testes específicos para Reporter, resolução, aprovações, gates ou
  `main()`;
- o script importa `sys` sem uso e não importa `Any`;
- há numerosas anotações `dict` e `list[dict]` sem parâmetros completos;
- Pylance/Pyright strict não está configurado no workspace;
- o script já possui validação parcial de referências cruzadas de aprovações;
- a seleção do `Reporter` ainda usa o primeiro registro pelo `document_id`;
- o README solicitado já existia em formato preliminar e foi atualizado por
  esta entrega.

Arquivos de correção ou evidência não registrados observados no workspace são
um problema de estado documental separado. Não devem ser incorporados aos
testes unitários do script como exceção permanente.

## 11. Referências oficiais

### Pylance e Pyright

- [Pylance: `python.analysis.typeCheckingMode`](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md)
- [Pyright: configuração](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
- [Pylance: `reportArgumentType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportArgumentType.md)
- [Pylance: `reportReturnType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportReturnType.md)
- [Pylance: `reportMissingTypeArgument`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingTypeArgument.md)
- [Pylance: `reportOptionalMemberAccess`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalMemberAccess.md)
- [Pylance: `reportUnknownArgumentType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownArgumentType.md)
- [Pylance: `reportUnknownMemberType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownMemberType.md)
- [Pylance: `reportUnknownParameterType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownParameterType.md)
- [Pylance: `reportUnknownVariableType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownVariableType.md)
- [Pylance: `reportUnnecessaryIsInstance`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryIsInstance.md)
- [Pylance: `reportUnusedImport`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedImport.md)

Conteúdo aplicado: o modo `strict` acrescenta, entre outros, diagnósticos para
argumentos genéricos ausentes, tipos desconhecidos, imports não usados e
`isinstance()` desnecessário. O plano não desativa essas regras.

### Python

- [Python `typing`](https://docs.python.org/3/library/typing.html)
- [Python `argparse`](https://docs.python.org/3/library/argparse.html)
- [Python `unittest`](https://docs.python.org/3/library/unittest.html)
- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html)

Conteúdo aplicado:

- anotações são verificadas por ferramentas estáticas, não impostas pelo
  runtime;
- coleções devem indicar os tipos de seus elementos;
- `Any` deve ficar restrito à fronteira inevitavelmente dinâmica;
- `unittest` suporta descoberta sem dependência adicional;
- caminhos resolvidos precisam ser confrontados com a raiz autorizada.

### YAML e JSON Schema

- [PyYAML: documentação e `safe_load`](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [jsonschema: validação](https://python-jsonschema.readthedocs.io/en/stable/validate/)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)

Conteúdo aplicado:

- `safe_load` restringe a construção a tipos YAML padrão, mas ainda retorna
  estrutura dinâmica que precisa de narrowing;
- `Draft202012Validator.check_schema()` valida o próprio schema;
- `FormatChecker` deve ser fornecido explicitamente quando formatos precisam
  ser verificados;
- schema válido não comprova integridade referencial entre arquivos.

## 12. Definição de pronto

O trabalho termina somente quando:

- o mapa foi convertido em cartões de intervenção local;
- a regra de qualidade foi preservada;
- o script passa em Pylance/Pyright strict;
- cada ação possui vermelho reproduzível e verde correspondente;
- todos os testes existentes e novos passam;
- seleção de versão é exata;
- gates não emitem escopo enganoso;
- aprovações resolvem hashes e evidências reais;
- caminhos não escapam do workspace;
- `main()` apenas orquestra;
- README e `--help` são coerentes;
- nenhum import ou módulo desnecessário foi criado;
- nenhuma cópia integral do script permanece no mapa.
