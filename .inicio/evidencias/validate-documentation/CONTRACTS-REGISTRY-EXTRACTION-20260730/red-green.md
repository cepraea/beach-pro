# Evidência RED–GREEN de BEH-02

## RED

Teste:
`RegistryInvariantTests.test_non_mapping_document_reports_index_and_preserves_valid_items`.

Entrada: dois mapeamentos válidos separados por um escalar em `documents[1]`.

Resultado antes da correção:

```text
AssertionError: 'documents[1] must be a mapping' not found in []
Ran 1 test
FAILED (failures=1)
```

O retorno já preservava os dois mapeamentos; a falha demonstrou especificamente
o descarte silencioso do escalar.

## GREEN

`validate_top_level()` passou a enumerar os itens, registrar
`documents[1] must be a mapping` e continuar a varredura.

```text
Ran 1 test
OK
```

A suíte de `test_registry_invariants` também passou com sete testes.
