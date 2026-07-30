# Mapa de intervenção do validador documental

## 1. Finalidade

Este mapa ensina agentes de IA a extrair e corrigir o pacote
`scripts.documentation.validate_documentation` por unidades pequenas. A
implementação ainda está temporariamente concentrada em `__init__.py`; cada
unidade abaixo identifica o módulo proprietário que deve ser criado ou editado.
O mapa não é uma cópia da implementação e não substitui o código executável.

Plano de execução e critérios completos:
[`PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md`](../../../.inicio/PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md).

Os planos `Plano-validator.md` e `Plano-migracao-validator.md` permanecem
registros históricos e não governam novas extrações.

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
- Em extração estrutural, mover somente a responsabilidade indicada para o
  módulo proprietário previsto neste mapa e preservar o comportamento.
- Em mudança comportamental autorizada, criar o teste vermelho antes do patch
  funcional.
- Não reescrever o script inteiro.
- Não introduzir Pydantic.
- Não alterar schemas, registro ou documentos para esconder defeitos do código.
- Não usar supressões genéricas de tipo.
- Adicionar somente os imports exigidos pelo módulo em extração, respeitando a
  direção de dependências.
- Não acrescentar funcionalidade relevante ao `__init__.py` monolítico.
- Manter reexports transitórios apenas enquanto forem necessários para
  compatibilidade e removê-los no change set previsto pelo plano.

### 2.3 Subciclos e dependências

Cada change set deve declarar um único subciclo:

- **A — extração estrutural:** mover sem mudar regra, migrar testes e patches,
  comparar a saída com a baseline e manter tudo verde;
- **B — mudança comportamental:** citar `BEH-01…BEH-07`, demonstrar RED pelo
  motivo correto, aplicar a menor correção e demonstrar GREEN.

Não misturar os subciclos no mesmo commit. A ordem permitida de dependências é:

```text
json_types / models
        ↓
config / filesystem / reporter
        ↓
contracts / registry / workflow / approvals / provenance / ingestion
        ↓
instances / front_matter / links
        ↓
gates
        ↓
pipeline
        ↓
cli
        ↓
__init__ / __main__
```

Módulos consumidores consultam símbolos patcháveis pelo módulo proprietário,
por exemplo `links.validate_links()` e `config.WORKSPACE_ROOT`. Evitar importar
diretamente esses símbolos para o namespace consumidor.

### 2.4 Tipagem

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

### 2.5 Testes

Usar `unittest`, já adotado no repositório.

```bash
python3 -m unittest discover scripts/documentation/tests
```

- Vermelho válido: falha pela regra que será corrigida.
- Verde válido: o mesmo cenário passa depois do patch.
- Falha por sintaxe, import ou fixture incorreta não é teste vermelho válido.
- Depois do teste localizado, executar a suíte completa.

### 2.6 Fail-fast

O `Reporter` coleta todos os achados de uma etapa.
`pipeline.run_validation(args, reporter)` interrompe o pipeline antes da etapa
seguinte quando a etapa atual registra erro. `cli.main()` valida argumentos,
chama o pipeline e controla a emissão única.

```text
validar argumentos
→ carregar registro
→ resolver escopo documental
→ contratos
→ instâncias
→ registro/arquivos
→ canonicalidade
→ gate solicitado
→ links
→ emitir uma vez
```

Falha em uma etapa impede as etapas à direita.

## 3. Como usar uma unidade

1. Confirme no plano a fase, o gate de entrada e o subciclo autorizado.
2. Localize as funções da unidade no `__init__.py` ou no módulo já extraído.
3. Leia somente a unidade, seus helpers diretos e testes relacionados.
4. Crie ou edite apenas o módulo proprietário indicado na tabela abaixo.
5. No subciclo A, mova sem reescrever lógica e preserve o reexport transitório.
6. No subciclo B, execute o RED previsto e confirme a razão da falha.
7. Aplique o menor patch possível e migre os patches para o namespace de
   consulta.
8. Execute o teste localizado e depois as suítes aplicáveis.
9. Execute compilação, Pyright fixado, gates afetados e `npm run validate`.
10. Atualize docstring ou comentário quando a decisão técnica mudar.

Comandos finais de cada unidade:

```bash
python3 -m compileall -q scripts/documentation/validate_documentation
python3 -m unittest discover scripts/documentation/tests
npx --yes pyright@1.1.411 --project pyrightconfig.json
npm run validate
```

## 4. Unidades de intervenção

| Unidade | Módulo proprietário |
| --- | --- |
| 1 | `json_types.py`, `models.py`, `config.py`, `filesystem.py` |
| 2 | `reporter.py` |
| 3 | `cli.py` |
| 4 e 6 | `registry.py` |
| 5 | `filesystem.py`, `links.py` |
| 7 | `contracts.py`, `instances.py` |
| 8 | `approvals.py`, `provenance.py` |
| 9 | `workflow.py`, `ingestion.py` |
| 10 | `gates/g_arch.py`, `gates/g0.py`, `gates/g1.py` |
| 11 | `gates/g2.py` |
| 12 | `front_matter.py`, `gates/g_fm.py` |
| 13 | `pipeline.py`, `gates/dispatcher.py`, `cli.py` |
| 14 | `tests/`, `integration_tests/`, README e este mapa |

Esta tabela define propriedade, mas não autoriza criar todos os módulos de uma
vez. Cada módulo nasce somente na fase e no change set correspondente do plano.

### Unidade 1 — Imports, tipos e constantes

**Origem atual:** início do `__init__.py` até `class Reporter`.

**Destinos:** `json_types.py`, `models.py`, `config.py` e `filesystem.py`,
extraídos separadamente na ordem do plano.

**Responsabilidade:** disponibilizar somente dependências e constantes comuns.

**Editar:** mover tipos, modelo, configuração e helpers de filesystem sem
reformular suas regras; cada módulo recebe apenas os próprios imports.

**Não editar:** Reporter, funções ou gates.

**Porquê:** YAML e JSON são dinâmicos na entrada, mas o restante do script não
deve propagar tipos desconhecidos.

**Aceitação:** nenhum import não utilizado; nenhum ciclo entre módulos; cada
consumidor consulta configuração mutável por `config.WORKSPACE_ROOT`.

### Unidade 2 — Reporter

**Origem atual:** `class Reporter` no `__init__.py`.

**Destino:** `reporter.py`.

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

**Origem atual:** `parse_args()` e helper de validação de argumentos.

**Destino:** `cli.py`.

**Contrato:** aceitar somente combinações coerentes de gate, documento, versão e
formato.

**Editar:** validação de `--document-id`, `--version` e identidade do resultado.

**Não editar:** implementação dos gates.

**Porquê:** uma combinação inválida deve falhar antes de produzir evidência
enganosa.

**Aceitação:** `--version` sem documento falha; ID ambíguo exige versão; `--help`
documenta todos os gates.

### Unidade 4 — Resolução documental

**Origem atual:** após `validate_top_level()` e antes de `validate_record()`.

**Destino:** `registry.py`, incluindo `resolve_document_version`.

**Contrato:**

- entrada: registros, `document_id`, `version`;
- saída: registro exato ou `None` com erro no Reporter;
- chave operacional: `(document_id, version)`.

**Não editar:** conteúdo do registro.

**Porquê:** `document_id` é permanente e pode possuir versões simultâneas.

**Aceitação:** nunca selecionar a primeira versão por ID; ausência e ambiguidade
falham; Reporter recebe metadados do par exato.

### Unidade 5 — Caminhos, nomes, links e hash

**Origem atual:** `workspace_path()` até `validate_links()`.

**Destinos:** `workspace_path()` e `sha256()` em `filesystem.py`;
`validate_links()` e seus helpers em `links.py`.

**Contrato:** nenhum caminho local pode escapar de `WORKSPACE_ROOT`.

**Editar:** validação de links locais, narrowing e tipos.

**Não editar:** regexes e convenções sem teste específico.

**Porquê:** `Path.resolve()` normaliza o caminho, mas não concede autorização
para acessar fora da raiz.

**Aceitação:** link interno válido passa; quebrado falha; absoluto externo e
`..` externo falham; URL e âncora não são arquivos locais.

### Unidade 6 — Registro e unicidade

**Origem atual:** `validate_top_level()`, `validate_record()`,
`validate_uniqueness()`, `managed_files()` e `validate_canonical_registry()`.

**Destino:** `registry.py`.

**Contrato:** cada versão registrada aponta para arquivo e hash exatos.

**Editar:** tipos, narrowing e invariantes existentes.

**Não editar:** schemas ou dados controlados.

**Porquê:** `self_hash_exempt` existe apenas para romper a autorreferência do
registro mestre.

**Aceitação:** par ID/versão e caminho são únicos; hash divergir falha; canônico
ativo usa o próprio caminho canônico; terminal pode preservar caminho histórico.

### Unidade 7 — Schemas e instâncias

**Origem atual:** `load_json()` até antes de
`validate_approval_cross_references()`.

**Destinos:** validação de schemas em `contracts.py` e validação de instâncias
em `instances.py`.

**Contrato:** validar forma antes de relações entre artefatos.

**Editar:** mover os helpers para seu módulo proprietário e manter cada função
de alto nível como orquestração.

**Não editar:** schemas ou regras documentais.

**Porquê:** schema válido não prova que um ID referenciado existe.

**Aceitação:** erros informam arquivo e caminho JSON; documentos, workflow,
gates e evidências são validados separadamente; referências cruzadas continuam
executadas.

### Unidade 8 — Aprovações e evidências

**Origem atual:** `validate_approval_cross_references()`.

**Destino:** `approvals.py`. Validação de pacotes de proveniência pertence a
`provenance.py`; a implementação do gate pertence a `gates/g2.py`.

**Contrato:** aprovação ativa vincula alvo e gates exatos por ID, versão e hash.

**Editar:** alvo inexistente, IDs duplicados, conjunto obrigatório de gates,
campos nulos, relação inversa e supersessão.

**Não editar:** schemas para aceitar dados inválidos.

**Porquê:** evidência histórica deve ser preservada, mas não pode satisfazer uma
promoção atual quando foi superada.

**Aceitação:** hash divergente, gate inexistente/não passante/nulo/duplicado e
supersessão sem sucessora falham; cadeia exata passa.

### Unidade 9 — Workflow e ingestão

**Origem atual:** `validate_workflow_references()` até antes de `validate_g0()`.

**Destinos:** `workflow.py` e `ingestion.py`.

**Contrato:** todas as referências processáveis existem e snapshots históricos
permanecem verificáveis.

**Editar:** tipos, índices e duplicidades.

**Não editar:** política do workflow.

**Porquê:** revisão corrente não reescreve evidência histórica; a mesma versão
também não pode mudar de hash.

**Aceitação:** referência desconhecida e ID duplicado falham; versão nova não
invalida snapshot; mesma versão divergente falha.

### Unidade 10 — G-ARCH, G0 e G1

**Origem atual:** `validate_g0()`, `validate_g1()` e despacho relacionado.

**Destinos:** `gates/g_arch.py`, `gates/g0.py` e `gates/g1.py`. O despacho
pertence exclusivamente a `gates/dispatcher.py`.

**Contrato:** cada gate declara explicitamente se é global ou documental.

**Editar:** escopo, tipos e função explícita de G-ARCH quando necessária.

**Não editar:** emitir metadados documentais para gate global.

**Porquê:** execução global não pode ser apresentada como evidência localizada.

**Aceitação:** gate global emite metadados nulos; documental usa o alvo exato;
semântica corresponde ao workflow.

### Unidade 11 — G2

**Origem atual:** `validate_g2()` e helpers diretos.

**Destino:** `gates/g2.py`, consumindo `provenance.py`.

**Contrato:** proveniência referencia bytes exatos de uma versão.

**Editar:** índice por `(document_id, version)`, narrowing e tipos.

**Não editar:** conteúdo dos pacotes.

**Porquê:** índice apenas por ID sobrescreve versões simultâneas.

**Aceitação:** pacote resolve versão exata; hash divergente e caminho preservado
externo falham; claims críticos mantêm cobertura.

### Unidade 12 — Front Matter e G-FM

**Origem atual:** `_DuplicateKeyLoader` até `validate_front_matter()`.

**Destinos:** parsing e validação em `front_matter.py`; implementação do gate
em `gates/g_fm.py`.

**Contrato:** parser seguro, schema correto e sincronização com o registro exato.

**Editar:** tipos, seleção inexistente/ambígua e docstrings.

**Não editar:** corpo Markdown nem schemas sem decisão própria.

**Porquê:** arquivos arquivados são snapshots históricos e ficam fora do perfil
ativo; feature specs têm contrato independente do registro.

**Aceitação:** alvo vazio falha; versão exata passa; chaves duplicadas, YAML
inválido e divergências continuam falhando; corpo permanece intacto.

### Unidade 13 — Main

**Origem atual:** `main()` e o despacho no `__init__.py`.

**Destinos:** `pipeline.py`, `gates/dispatcher.py` e `cli.py`.

**Pré-condição:** Unidades 1–12 verdes.

**Responsabilidade:** `pipeline.run_validation(args, reporter) -> None`
orquestra e não importa CLI nem emite resultados. `cli.main(argv)` valida os
argumentos, chama o pipeline e emite exatamente uma vez.

**Editar:** ordem, fail-fast entre etapas e chamadas de helpers corrigidos.

**Não editar:** reimplementar regra de negócio dentro de `main()`.

**Porquê:** corrigir o orquestrador cedo demais espalha soluções temporárias e
obriga reescrita posterior.

**Aceitação:** escopo é resolvido antes dos contratos; cada etapa executa uma
vez; erro impede etapas posteriores; Reporter emite uma vez; alvo exato é
reutilizado.

### Unidade 14 — Testes e documentação

**Localização:** `scripts/documentation/tests/`,
`scripts/documentation/integration_tests/`, este mapa e README operacional.

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
