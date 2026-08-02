# Validação da Fase 8

## Escopo entregue

- `front_matter.py`: loader, parsing e validações estruturais;
- `links.py`: normalização e validação de links locais;
- BEH-03: erro controlado para chaves YAML complexas;
- BEH-04: rejeição de Front Matter fora de UTF-8;
- BEH-05: erro controlado para falhas de leitura de Markdown.

## Gate de qualidade

```text
python3 -m compileall -q \
  scripts/documentation/validate_documentation \
  scripts/documentation/tests
PASS

python3 -m unittest discover -s scripts/documentation/tests -t . -v
Ran 102 tests
OK

python3 -m unittest discover \
  -s scripts/documentation/integration_tests -t . -v
Ran 1 test
OK

npx --yes pyright@1.1.411 --project pyrightconfig.json
0 errors, 0 warnings, 0 informations

npm run validate
PASS
```

`npm run validate` foi executado após cada um dos cinco change sets de código.
G-ARCH, G0, G1, G2 para o contexto `0.1`, G-FM para o contexto `0.1.2` e a
validação global permaneceram semanticamente idênticos à baseline.

## Resultado

```text
FRONT-MATTER-EXTRACTION = PASS
LINKS-EXTRACTION = PASS
BEH-03 = PASS
BEH-04 = PASS
BEH-05 = PASS
```

As quatro limitações residuais do plano permanecem abertas. Este resultado não
declara o validador pronto para atuar como gate bloqueante de produção.
