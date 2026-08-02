# Evidência RED–GREEN de BEH-07

O teste `test_public_api_matches_beh_07` foi criado antes da contração da
fachada.

## RED

```text
AttributeError: module 'scripts.documentation.validate_documentation'
has no attribute '__all__'
```

A falha demonstrou a ausência do contrato explícito de API pública, sem erro de
sintaxe, import ou fixture.

## GREEN

```text
test_public_api_matches_beh_07 ... ok
Ran 1 test
OK
```

O pacote agora declara `__all__ == ["main"]`, e `main` é exatamente a função
proprietária de `cli.py`.
