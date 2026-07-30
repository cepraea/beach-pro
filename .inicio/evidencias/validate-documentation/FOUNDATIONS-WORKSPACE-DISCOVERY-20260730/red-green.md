# Evidência RED–GREEN de BEH-01

## RED

Com os seis testes presentes e antes da implementação de
`config.find_workspace_root`, o comando:

```bash
python3 -m unittest \
  scripts.documentation.tests.test_workspace_discovery \
  -v
```

retornou código `1`, com seis erros `AttributeError`. A causa esperada foi a
ausência da função autorizada por BEH-01.

## GREEN

Depois da implementação mínima por quatro marcadores canônicos, o mesmo comando
retornou código `0`:

```text
Ran 6 tests
OK
```

Os casos cobertos são:

1. início na raiz;
2. início em arquivo;
3. início em subdiretório;
4. marcadores parciais;
5. ausência total;
6. início por symlink.

Os TARs não participam da descoberta. A falha informa, em ordem estável, os
quatro marcadores obrigatórios.
