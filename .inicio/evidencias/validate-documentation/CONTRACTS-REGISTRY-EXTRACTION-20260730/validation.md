# Validação da Fase 6

## Extrações estruturais

- as cinco funções de contratos foram movidas para `contracts.py`;
- as nove funções de registro e suas constantes foram movidas para
  `registry.py`;
- os corpos das funções foram comparados por AST com `origin/main`;
- o pacote conserva reexports transitórios;
- consumidores internos e patches consultam os módulos proprietários.

## Gate de qualidade

```text
python3 -m unittest discover -s scripts/documentation/tests -t . -v
Ran 99 tests
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

Os resultados normalizados de G-ARCH, G0, G1, G2 para o contexto `0.1` e
G-FM para o contexto `0.1.2` são idênticos à baseline. A validação global
permanece em `errors=0 warnings=0`.

## Resultado

```text
CONTRACTS-EXTRACTION = PASS
REGISTRY-EXTRACTION = PASS
BEH-02 = PASS
```
