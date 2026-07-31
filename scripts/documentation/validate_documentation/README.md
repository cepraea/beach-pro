# Validador de documentação

Guia operacional de
[`scripts.documentation.validate_documentation`](./).
O script valida o registro documental, arquivos gerenciados, contratos JSON
Schema, evidências, workflow, links, hashes e gates do CEPRAEA BEACH PRO.

O plano ativo de modularização está em
[`PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md`](../../../.inicio/PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md).
O mapa destinado a agentes está em
[`MAPA-VALIDADOR-DOC.md`](MAPA-VALIDADOR-DOC.md).
`Plano-validator.md` e `Plano-migracao-validator.md` são registros históricos,
preservados sem governar novas extrações.

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
  --version 0.1.2 \
  --format yaml
```

`--registry PATH` permite apontar para outro registro em testes ou auditorias
controladas. `--strict-legacy` transforma desvios legados conhecidos em erros.

`G-ARCH`, `G0` e `G1` são globais e rejeitam `--document-id` e `--version`.
`G2` e `G-FM` aceitam escopo documental. `--version` exige `--document-id`; se
um ID possuir várias versões, a versão é obrigatória.

## Estado e limites operacionais

A migração do script para pacote executável está implementada. A modularização
interna está autorizada, mas será incremental e governada pelo plano ativo. A
validação global e os gates G-ARCH, G0 e G1 passam no estado atual do
repositório. G-FM passa para o canônico de contexto `0.1.2`.

G2 exige um pacote ligado à versão e ao hash exatos. O pacote existente cobre
o contexto histórico `0.1`; portanto:

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G2 \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1
```

passa, enquanto solicitar o canônico `0.1.2` falha com ausência de pacote. Isso
é uma lacuna de evidência da versão, não uma razão para relaxar o validador.

## Arquitetura para manutenção

A implementação de domínio ainda está temporariamente concentrada em
`validate_documentation/__init__.py`. As fundações já extraídas são:

- `json_types.py`: fronteiras tipadas de JSON e YAML;
- `models.py`: `ValidatorArgs`;
- `config.py`: paths e descoberta do workspace pelos quatro marcadores
  canônicos;
- `filesystem.py`: resolução segura de paths e SHA-256 em streaming;
- `reporter.py`: coleta determinística e emissão única em texto ou YAML;
- `contracts.py`: carregamento e validação dos contratos JSON Schema;
- `registry.py`: envelope, identidade, paths, hashes e integridade do registro;
- `workflow.py`: referências internas do workflow controlado;
- `approvals.py`: identidade entre aprovações, alvos e gates;
- `provenance.py`: contratos de pacotes, fontes e alegações;
- `ingestion.py`: snapshots históricos e sua linhagem;
- `instances.py`: famílias de instâncias e delegação de relações.
- `front_matter.py`: parsing e validação estrutural do Front Matter;
- `links.py`: normalização e validação dos links locais.

O monólito remanescente é uma etapa transitória protegida pelos testes, não a
arquitetura final. Nenhuma funcionalidade relevante nova deve ser acrescentada
a ele.

As responsabilidades serão extraídas, uma por change set, na direção:

```text
json_types / models
        ↓
config / filesystem / reporter
        ↓
contratos e domínios
        ↓
gates
        ↓
pipeline
        ↓
cli
        ↓
__init__ / __main__
```

Uma extração estrutural move código sem alterar sua regra e mantém reexports
transitórios quando necessários. Uma mudança comportamental cita a decisão
`BEH` autorizadora, registra RED pelo motivo esperado e somente então aplica a
correção mínima. Os dois subciclos não são misturados no mesmo commit.

`pipeline.run_validation(args, reporter) -> None` será responsável pelo
fail-fast e não emitirá resultados. `cli.main(argv)` validará argumentos,
chamará o pipeline e controlará a emissão única. O `__init__.py` terminará como
fachada pública restrita a `main`.

O mapa operacional identifica, para cada unidade, o arquivo que deve ser criado
ou editado. Não se deve criar todos os módulos de uma vez nem alterar documentos
ou schemas para esconder uma falha do código.

## Regra de qualidade

O código **DEVE** ser autoexplicativo, mas cada função complexa deve conter
*docstrings* ou *comentários inline* voltados para outros desenvolvedores ou
agentes de IA. Comentar o "porquê" de decisões técnicas para mitigar erros em
futuras manutenções.

Comentários devem explicar invariantes, segurança e decisões de governança, não
repetir literalmente a operação da linha seguinte.

## Testes

Os testes usam `unittest` e estão separados por responsabilidade:

- testes unitários em `scripts/documentation/tests/`, independentes dos TARs;
- integração do repositório em
  `scripts/documentation/integration_tests/`, executada somente depois de
  `TAR-MATERIALIZATION = PASS`.

A suíte unitária é dividida por responsabilidade:

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
| `test_workspace_discovery.py` | Marcadores canônicos e descoberta da raiz |

`test_package_entrypoints.py` protege a execução de `--help` por `-m`, a
identidade canônica do pacote, a raiz do workspace, a existência de uma única
implementação, a localização do mapa, os consumidores operacionais, as versões
e os hashes controlados e a documentação dos testes neste README.

`integration_tests/test_repository_entrypoint.py` executa G-ARCH contra o
acervo real. A ausência dos TARs é falha de precondição e não causa `skip`.

A baseline anterior à Fase 4 possuía 92 testes unitários. BEH-01 acrescentou
seis cenários RED–GREEN. BEH-02 acrescentou um cenário que exige o índice do
item não mapeamento e preserva os registros válidos adjacentes. A Fase 8
acrescentou três regressões: BEH-03 rejeita chaves YAML complexas de forma
controlada, BEH-04 rejeita Front Matter fora de UTF-8 e BEH-05 converte falhas
de leitura de Markdown em erros do Reporter. A suíte totaliza 102 testes
unitários, além do teste de integração.

### Suíte unitária

```bash
python3 -m unittest discover \
  -s scripts/documentation/tests \
  -t . \
  -v
```

### Integração com os TARs materializados

```bash
python3 -m unittest discover \
  -s scripts/documentation/integration_tests \
  -t . \
  -v
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
npx --yes pyright@1.1.411 --project pyrightconfig.json
```

- [Pylance: type checking mode](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md)
- [Pyright: configuração](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
- [Python: type hints](https://docs.python.org/3/library/typing.html)

A verificação deve permanecer com zero diagnósticos e sem supressões genéricas.

Depois de qualquer change set de código ou configuração, executar também:

```bash
npm run validate
```

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
