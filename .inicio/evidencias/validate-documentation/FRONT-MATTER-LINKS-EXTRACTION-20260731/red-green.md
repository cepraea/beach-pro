# Evidência RED–GREEN da Fase 8

Cada correção comportamental foi executada depois das extrações estruturais,
em change set próprio e sob a decisão `BEH` correspondente.

## BEH-03 — chave YAML complexa

O teste `test_complex_mapping_key_reports_controlled_yaml_error` usa uma chave
YAML representada por sequência.

### RED BEH-03

```text
TypeError: unhashable type: 'list'
FAILED (errors=1)
```

A exceção escapava de `_DuplicateKeyLoader` sem chegar ao Reporter.

### GREEN BEH-03

```text
test_complex_mapping_key_reports_controlled_yaml_error ... ok
Ran 1 test
OK
```

O loader rejeita nós de chave não escalares com `ConstructorError` e converte
uma eventual chave não hashável no mesmo erro YAML controlado.

## BEH-04 — UTF-8 inválido

O teste `test_invalid_utf8_reports_file_and_stops_validation` grava bytes
inválidos no Front Matter.

### RED BEH-04

```text
FAIL: test_invalid_utf8_reports_file_and_stops_validation
AssertionError: erro esperado de UTF-8 não encontrado
```

O decoder substituía bytes inválidos por `U+FFFD`; a validação prosseguia e
produzia somente erros derivados do schema.

### GREEN BEH-04

```text
test_invalid_utf8_reports_file_and_stops_validation ... ok
Ran 1 test
OK
```

O decode agora é estrito. `UnicodeDecodeError` identifica o arquivo no Reporter
e encerra apenas a validação daquele documento.

## BEH-05 — falha de leitura

O teste `test_markdown_read_failure_is_reported` simula
`Path.read_text()` lançando `OSError("permission denied")`.

### RED BEH-05

```text
OSError: permission denied
FAILED (errors=1)
```

A exceção escapava de `validate_links()` com traceback.

### GREEN BEH-05

```text
test_markdown_read_failure_is_reported ... ok
Ran 1 test
OK
```

O Reporter recebe o caminho `docs/source.md`, a operação e a causa; o validador
continua a inspeção da coleção sem encerrar inesperadamente.
