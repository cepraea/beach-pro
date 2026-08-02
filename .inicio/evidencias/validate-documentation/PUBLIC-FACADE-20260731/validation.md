# Validação da Fase 11

```text
python3 -m unittest discover -s scripts/documentation/tests -t . -q
Ran 108 tests
OK

python3 -m unittest discover \
  -s scripts/documentation/integration_tests -t . -q
Ran 1 test
OK

npx pyright@1.1.411 --project pyrightconfig.json
0 errors, 0 warnings, 0 informations

npm run validate
PASS
```

Os seis cenários documentais permaneceram idênticos à baseline após remover
somente `gate_result_id` e `evaluated_at`; todos retornaram código zero.

Resultado:

```text
PUBLIC-FACADE = PASS
BEH-07-CONTRACT = PASS
```

As quatro limitações residuais continuam abertas; este resultado não declara
prontidão para uso bloqueante em produção.
