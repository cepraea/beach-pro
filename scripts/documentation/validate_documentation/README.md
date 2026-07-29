# Validador de documentação

Guia operacional de
[`scripts.documentation.validate_documentation`](./).
O script valida o registro documental, arquivos gerenciados, contratos JSON
Schema, evidências, workflow, links, hashes e gates do CEPRAEA BEACH PRO.

O roteiro de correção incremental está em
[`.inicio/Plano-validator.md`](../../../.inicio/Plano-validator.md). O mapa
destinado a agentes está em
[`MAPA-VALIDADOR-DOC.md`](MAPA-VALIDADOR-DOC.md).

## Requisitos

- Python 3.10 ou superior;
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation);
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/validate/).

Enquanto não houver um arquivo de dependências Python controlado:

```bash
python3 -m pip install PyYAML jsonschema
```

Não é necessário Pydantic.

## Uso

Execute os comandos a partir da raiz do repositório.

### Validação global

```bash
python3 -m scripts.documentation.validate_documentation
```

### Gate específico

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G0
```

Gates aceitos atualmente:

- `G-ARCH`: conformidade arquitetural e tratamento estrito de legado;
- `G0`: identidade do lote documental de ingestão;
- `G1`: integridade e preservação do lote histórico;
- `G2`: proveniência;
- `G-FM`: Front Matter governado e feature specs.

### Resultado YAML

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G1 \
  --format yaml \
  --result-id GATE-RESULT-G1-AUDITORIA-20260729
```

A saída YAML segue
[`resultado-gate.schema.json`](../../../docs/contracts/schemas/resultado-gate.schema.json).
Sem `--result-id`, a identidade termina em `RUNTIME` e serve apenas para
diagnóstico; ela não deve ser persistida como evidência.

### Escopo documental

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G-FM \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1.1 \
  --format yaml
```

`--registry PATH` permite apontar para outro registro em testes ou auditorias
controladas. `--strict-legacy` transforma desvios legados conhecidos em erros.

`G-ARCH`, `G0` e `G1` são globais e rejeitam `--document-id` e `--version`.
`G2` e `G-FM` aceitam escopo documental. `--version` exige `--document-id`; se
um ID possuir várias versões, a versão é obrigatória.

## Estado e limites operacionais

O plano incremental está implementado. A validação global e os gates G-ARCH,
G0 e G1 passam no estado atual do repositório. G-FM passa para o canônico de
contexto `0.1.1`.

G2 exige um pacote ligado à versão e ao hash exatos. O pacote existente cobre
o contexto `0.1`; portanto:

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G2 \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1
```

passa, enquanto solicitar `0.1.1` falha com ausência de pacote. Isso é uma
lacuna de evidência da versão, não uma razão para relaxar o validador.

## Arquitetura para manutenção

A implementação única está em `validate_documentation/__init__.py`, mas deve
ser editada por unidades:

1. imports, constantes e tipos;
2. `Reporter`;
3. CLI e resolução documental;
4. caminhos, nomes, links e hashes;
5. registro e unicidade;
6. schemas e instâncias;
7. aprovações e evidências;
8. workflow e ingestão;
9. gates G-ARCH, G0, G1 e G2;
10. Front Matter e G-FM;
11. `main()` como orquestrador.

Ao corrigir uma unidade:

- crie primeiro um teste vermelho;
- aplique o menor patch possível;
- execute o teste verde;
- execute toda a suíte;
- não adicione imports fora da ação central de tipagem;
- não altere documentos ou schemas para esconder uma falha do script.

## Regra de qualidade

O código **DEVE** ser autoexplicativo, mas cada função complexa deve conter
*docstrings* ou *comentários inline* voltados para outros desenvolvedores ou
agentes de IA. Comentar o "porquê" de decisões técnicas para mitigar erros em
futuras manutenções.

Comentários devem explicar invariantes, segurança e decisões de governança, não
repetir literalmente a operação da linha seguinte.

## Testes

Os testes ficam em
[`scripts/documentation/tests/`](../tests/) e usam `unittest`. A suíte atual é
dividida por responsabilidade:

| Módulo | Escopo principal |
| --- | --- |
| `test_instances.py` | Contratos e instâncias |
| `test_approvals.py` | Aprovações e evidências |
| `test_workflow_and_ingestion.py` | Workflow e ingestão |
| `test_scoped_gates.py` | Gates com escopo documental |
| `test_registry_invariants.py` | Registro, unicidade e hashes |
| `test_main_pipeline.py` | Ordem e interrupção do pipeline |
| `test_reporter.py` | Coleta e emissão de achados |
| `test_cli_and_resolution.py` | CLI, versões e links |
| `test_front_matter.py` | Front Matter e G-FM |

`test_package_entrypoints.py` protege a execução por `-m`, a raiz do workspace,
a existência de uma única implementação, a localização do mapa, os consumidores
operacionais, as versões e os hashes controlados e a documentação dos testes
neste README.

### Suíte completa

```bash
python3 -m unittest discover scripts/documentation/tests
```

### Testes da migração para pacote

```bash
python3 -m unittest \
  scripts.documentation.tests.test_package_entrypoints
```

O teste localizado deve ficar verde antes da suíte completa. Uma falha de
import, sintaxe ou fixture não é um teste vermelho válido; o vermelho deve
demonstrar especificamente a regra que será implementada.

### Teste atual de Front Matter

```bash
python3 -m unittest \
  scripts.documentation.tests.test_front_matter
```

### CLI, resolução de versões e links

```bash
python3 -m unittest \
  scripts.documentation.tests.test_cli_and_resolution
```

### Unidades adicionais

```bash
python3 -m unittest \
  scripts.documentation.tests.test_instances \
  scripts.documentation.tests.test_approvals \
  scripts.documentation.tests.test_workflow_and_ingestion \
  scripts.documentation.tests.test_scoped_gates \
  scripts.documentation.tests.test_registry_invariants \
  scripts.documentation.tests.test_main_pipeline \
  scripts.documentation.tests.test_reporter
```

### Sintaxe

```bash
python3 -m compileall -q scripts/documentation/validate_documentation
```

## Verificação estática

O repositório usa `pyrightconfig.json` com Pylance/Pyright em modo `strict`:

```bash
npx --yes pyright
```

- [Pylance: type checking mode](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md)
- [Pyright: configuração](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
- [Python: type hints](https://docs.python.org/3/library/typing.html)

A verificação deve permanecer com zero diagnósticos e sem supressões genéricas.

## Segurança

- YAML deve ser carregado por `safe_load` ou loader derivado de `SafeLoader`.
- Caminhos locais devem ser resolvidos e confirmados dentro de
  `WORKSPACE_ROOT`.
- Links locais não podem escapar do workspace.
- Hashes são calculados sobre bytes, sem normalização implícita.
- O schema valida a forma; referências cruzadas validam a relação entre
  artefatos.

Referências:

- [PyYAML `safe_load`](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/validate/)

## Códigos de saída

| Código | Significado |
| --- | --- |
| `0` | Nenhum erro bloqueante foi registrado |
| `1` | Uma ou mais validações falharam |
| `2` | Uso inválido da CLI, emitido pelo `argparse` |
