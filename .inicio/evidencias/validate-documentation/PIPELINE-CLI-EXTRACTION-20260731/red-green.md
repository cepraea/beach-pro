# Evidência RED–GREEN de BEH-06

Os testes `test_parse_args_accepts_explicit_argv` e
`test_main_accepts_explicit_argv_and_emits_once` foram executados antes da
correção comportamental.

## RED

```text
TypeError: parse_args() takes 0 positional arguments but 1 was given
TypeError: main() takes 0 positional arguments but 1 was given
Ran 2 tests
FAILED (errors=2)
```

A falha demonstrou exatamente a ausência do contrato `argv`, sem erro de
import, sintaxe ou fixture.

## GREEN

```text
Ran 6 tests
OK
```

`parse_args(argv)` encaminha `Sequence[str] | None` ao `argparse`; `main(argv)`
encaminha o mesmo valor ao parser. `None` continua representando a entrada real
do processo, comprovada também pelo teste do entrypoint `python -m`.
