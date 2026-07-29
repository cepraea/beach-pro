# Mapa de intervenção do validador documental

## 1. Finalidade

Este mapa ensina agentes de IA a corrigir
`scripts/documentation/validate_documentation/__init__.py` por unidades
pequenas. Ele não é uma cópia da implementação e não substitui o código
executável.

Plano de execução e critérios completos:
[`Plano-validator.md`](../../../.inicio/Plano-validator.md).

README operacional:
[`README.md`](README.md).

## 2. Regras globais

### 2.1 Qualidade

**Regras de Qualidade**:

   1. O código **DEVE** ser autoexplicativo, mas cada função
complexa deve conter *docstrings* ou *comentários inline* voltados para outros
desenvolvedores ou agentes de IA.

   2. Comentar o "porquê" de decisões técnicas para
mitigar erros em futuras manutenções.

Comentários devem explicar:

- invariantes documentais;
- decisões de segurança;
- diferenças entre snapshot histórico e revisão corrente;
- razão para uma etapa ser global ou localizada;
- motivo de uma exceção, como `self_hash_exempt`.

Comentários não devem repetir operações óbvias.

### 2.2 Limites

- Editar somente a unidade indicada.
- Criar o teste vermelho antes do patch funcional.
- Não mover funções para outros módulos.
- Não reescrever o script inteiro.
- Não introduzir Pydantic.
- Não alterar schemas, registro ou documentos para esconder defeitos do código.
- Não usar supressões genéricas de tipo.
- Não adicionar imports fora da Unidade 1.

### 2.3 Tipagem

O padrão é Pylance/Pyright `strict`.

- Assinaturas devem ter parâmetros e retorno completos.
- Não usar `dict`, `list[dict]` ou `tuple` sem argumentos de tipo.
- Dados de `yaml.safe_load()` e `json.loads()` entram pela fronteira dinâmica.
- Usar `Any` somente nessa fronteira e estreitar para tipos concretos antes das
  operações.
- `isinstance()` é necessário na fronteira de dados externos; depois do
  estreitamento, não repetir a mesma verificação.
- Todo `.get()` que possa retornar `None` deve ser estreitado antes do uso.

Diagnósticos prioritários:

- [`reportArgumentType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportArgumentType.md)
- [`reportReturnType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportReturnType.md)
- [`reportMissingTypeArgument`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingTypeArgument.md)
- [`reportOptionalMemberAccess`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalMemberAccess.md)
- [`reportUnknownArgumentType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownArgumentType.md)
- [`reportUnknownMemberType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownMemberType.md)
- [`reportUnknownParameterType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownParameterType.md)
- [`reportUnknownVariableType`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownVariableType.md)
- [`reportUnnecessaryIsInstance`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryIsInstance.md)
- [`reportUnusedImport`](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedImport.md)

### 2.4 Testes

Usar `unittest`, já adotado no repositório.

```bash
python3 -m unittest discover scripts/documentation/tests
```

- Vermelho válido: falha pela regra que será corrigida.
- Verde válido: o mesmo cenário passa depois do patch.
- Falha por sintaxe, import ou fixture incorreta não é teste vermelho válido.
- Depois do teste localizado, executar a suíte completa.

### 2.5 Fail-fast

O `Reporter` coleta todos os achados de uma etapa. O `main()` interrompe o
pipeline antes da etapa seguinte quando a etapa atual registra erro.

```text
carregar
→ contratos/instâncias
→ registro/arquivos
→ canonicalidade
→ gate solicitado
→ links
→ emitir uma vez
```

Falha em uma etapa impede as etapas à direita.

## 3. Como usar uma unidade

1. Localize as funções da unidade.
2. Leia apenas a unidade, seus helpers diretos e testes relacionados.
3. Confirme as invariantes e alterações proibidas.
4. Crie o teste vermelho descrito no plano.
5. Execute somente o teste e confirme a razão da falha.
6. Aplique o menor patch possível.
7. Execute o teste verde.
8. Execute a suíte completa, compilação e strict-mode.
9. Atualize docstring/comentário quando a decisão técnica mudar.

Comandos finais de cada unidade:

```bash
python3 -m compileall -q scripts/documentation/validate_documentation
python3 -m unittest discover scripts/documentation/tests
npx --yes pyright
```

## 4. Unidades de intervenção

### Unidade 1 — Imports, tipos e constantes

**Localização:** início do arquivo até `class Reporter`.

**Responsabilidade:** disponibilizar somente dependências e constantes comuns.

**Editar:**

- remover `import sys`;
- adicionar `from typing import Any`;
- tipar constantes compostas quando o strict-mode exigir.

**Não editar:** Reporter, funções ou gates.

**Porquê:** YAML e JSON são dinâmicos na entrada, mas o restante do script não
deve propagar tipos desconhecidos.

**Aceitação:** nenhum import não utilizado e nenhum import novo nas unidades
seguintes.

### Unidade 2 — Reporter

**Localização:** `class Reporter`.

**Contrato:**

- entrada: mensagens e metadados já validados;
- saída: texto ou instância de `resultado-gate.schema.json`;
- mutação: acumula erros e avisos;
- efeito externo: único ponto autorizado a imprimir o resultado final.

**Editar:** tipos do payload, ID persistível, determinismo e docstring.

**Não editar:** regras documentais.

**Porquê:** uma única fronteira de saída mantém CI e agentes consumidores
compatíveis.

**Aceitação:** schema do resultado passa; sucesso retorna `0`; falha retorna
`1`; IDs persistidos não colidem.

### Unidade 3 — CLI

**Localização:** `parse_args()` e helper de validação de argumentos.

**Contrato:** aceitar somente combinações coerentes de gate, documento, versão e
formato.

**Editar:** validação de `--document-id`, `--version` e identidade do resultado.

**Não editar:** implementação dos gates.

**Porquê:** uma combinação inválida deve falhar antes de produzir evidência
enganosa.

**Aceitação:** `--version` sem documento falha; ID ambíguo exige versão; `--help`
documenta todos os gates.

### Unidade 4 — Resolução documental

**Localização:** após `validate_top_level()` e antes de `validate_record()`.

**Criar:** helper `resolve_document_version`.

**Contrato:**

- entrada: registros, `document_id`, `version`;
- saída: registro exato ou `None` com erro no Reporter;
- chave operacional: `(document_id, version)`.

**Não editar:** conteúdo do registro.

**Porquê:** `document_id` é permanente e pode possuir versões simultâneas.

**Aceitação:** nunca selecionar a primeira versão por ID; ausência e ambiguidade
falham; Reporter recebe metadados do par exato.

### Unidade 5 — Caminhos, nomes, links e hash

**Localização:** `workspace_path()` até `validate_links()`.

**Contrato:** nenhum caminho local pode escapar de `WORKSPACE_ROOT`.

**Editar:** validação de links locais, narrowing e tipos.

**Não editar:** regexes e convenções sem teste específico.

**Porquê:** `Path.resolve()` normaliza o caminho, mas não concede autorização
para acessar fora da raiz.

**Aceitação:** link interno válido passa; quebrado falha; absoluto externo e
`..` externo falham; URL e âncora não são arquivos locais.

### Unidade 6 — Registro e unicidade

**Localização:** `validate_top_level()`, `validate_record()`,
`validate_uniqueness()`, `managed_files()` e `validate_canonical_registry()`.

**Contrato:** cada versão registrada aponta para arquivo e hash exatos.

**Editar:** tipos, narrowing e invariantes existentes.

**Não editar:** schemas ou dados controlados.

**Porquê:** `self_hash_exempt` existe apenas para romper a autorreferência do
registro mestre.

**Aceitação:** par ID/versão e caminho são únicos; hash divergir falha; canônico
ativo usa o próprio caminho canônico; terminal pode preservar caminho histórico.

### Unidade 7 — Schemas e instâncias

**Localização:** `load_json()` até antes de
`validate_approval_cross_references()`.

**Contrato:** validar forma antes de relações entre artefatos.

**Editar:** extrair helpers no mesmo arquivo e reduzir `validate_instances()` a
orquestração.

**Não editar:** schemas e imports.

**Porquê:** schema válido não prova que um ID referenciado existe.

**Aceitação:** erros informam arquivo e caminho JSON; documentos, workflow,
gates e evidências são validados separadamente; referências cruzadas continuam
executadas.

### Unidade 8 — Aprovações e evidências

**Localização:** `validate_approval_cross_references()`.

**Contrato:** aprovação ativa vincula alvo e gates exatos por ID, versão e hash.

**Editar:** alvo inexistente, IDs duplicados, conjunto obrigatório de gates,
campos nulos, relação inversa e supersessão.

**Não editar:** schemas para aceitar dados inválidos.

**Porquê:** evidência histórica deve ser preservada, mas não pode satisfazer uma
promoção atual quando foi superada.

**Aceitação:** hash divergente, gate inexistente/não passante/nulo/duplicado e
supersessão sem sucessora falham; cadeia exata passa.

### Unidade 9 — Workflow e ingestão

**Localização:** `validate_workflow_references()` até antes de `validate_g0()`.

**Contrato:** todas as referências processáveis existem e snapshots históricos
permanecem verificáveis.

**Editar:** tipos, índices e duplicidades.

**Não editar:** política do workflow.

**Porquê:** revisão corrente não reescreve evidência histórica; a mesma versão
também não pode mudar de hash.

**Aceitação:** referência desconhecida e ID duplicado falham; versão nova não
invalida snapshot; mesma versão divergente falha.

### Unidade 10 — G-ARCH, G0 e G1

**Localização:** `validate_g0()`, `validate_g1()` e despacho relacionado.

**Contrato:** cada gate declara explicitamente se é global ou documental.

**Editar:** escopo, tipos e função explícita de G-ARCH quando necessária.

**Não editar:** emitir metadados documentais para gate global.

**Porquê:** execução global não pode ser apresentada como evidência localizada.

**Aceitação:** gate global emite metadados nulos; documental usa o alvo exato;
semântica corresponde ao workflow.

### Unidade 11 — G2

**Localização:** `validate_g2()` e helpers diretos.

**Contrato:** proveniência referencia bytes exatos de uma versão.

**Editar:** índice por `(document_id, version)`, narrowing e tipos.

**Não editar:** conteúdo dos pacotes.

**Porquê:** índice apenas por ID sobrescreve versões simultâneas.

**Aceitação:** pacote resolve versão exata; hash divergente e caminho preservado
externo falham; claims críticos mantêm cobertura.

### Unidade 12 — Front Matter e G-FM

**Localização:** `_DuplicateKeyLoader` até `validate_front_matter()`.

**Contrato:** parser seguro, schema correto e sincronização com o registro exato.

**Editar:** tipos, seleção inexistente/ambígua e docstrings.

**Não editar:** corpo Markdown nem schemas sem decisão própria.

**Porquê:** arquivos arquivados são snapshots históricos e ficam fora do perfil
ativo; feature specs têm contrato independente do registro.

**Aceitação:** alvo vazio falha; versão exata passa; chaves duplicadas, YAML
inválido e divergências continuam falhando; corpo permanece intacto.

### Unidade 13 — Main

**Localização:** `main()`.

**Pré-condição:** Unidades 1–12 verdes.

**Responsabilidade:** somente orquestrar.

**Editar:** ordem, fail-fast entre etapas e chamadas de helpers corrigidos.

**Não editar:** reimplementar regra de negócio dentro de `main()`.

**Porquê:** corrigir o orquestrador cedo demais espalha soluções temporárias e
obriga reescrita posterior.

**Aceitação:** cada etapa executa uma vez; erro impede etapas posteriores;
Reporter emite uma vez; alvo exato é reutilizado.

### Unidade 14 — Testes e documentação

**Localização:** `scripts/documentation/tests/`, este mapa e README operacional.

**Editar:** testes `unittest`, comandos e limitações documentadas.

**Não editar:** testes para aceitar comportamento sabidamente incorreto.

**Porquê:** o mapa orienta a correção; os testes demonstram que ela permanece
válida.

**Aceitação:** vermelho/verde por unidade, suíte completa verde, strict-mode sem
supressões e README coerente com `--help`.

## 5. Referências das bibliotecas

- [Python `typing`](https://docs.python.org/3/library/typing.html)
- [Python `argparse`](https://docs.python.org/3/library/argparse.html)
- [Python `unittest`](https://docs.python.org/3/library/unittest.html)
- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [PyYAML e `safe_load`](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/validate/)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Pylance strict-mode](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md)
- [Pyright configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)

## 6. Definição de pronto

- mapa sem cópia integral do script;
- cada unidade tem responsabilidade, limites, porquê e aceitação;
- regra de qualidade preservada;
- testes vermelhos e verdes descritos no plano;
- script e testes passam no strict-mode;
- nenhuma dependência, import ou módulo desnecessário;
- README e CLI coerentes;
- nenhum defeito conhecido ocultado por supressão.
