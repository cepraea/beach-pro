# Validação da Fase 7

## Escopo entregue

- `workflow.py`: referências e identificadores do workflow;
- `approvals.py`: cadeia entre aprovação, alvo e resultados de gate;
- `provenance.py`: contratos de pacotes, fontes e alegações;
- `ingestion.py`: manifesto, eventos, snapshots e linhagem;
- `instances.py`: validação das famílias e delegação das relações.

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

`npm run validate` foi executado após cada um dos cinco change sets de código.
G-ARCH, G0, G1, G2 para o contexto `0.1`, G-FM para o contexto `0.1.2` e a
validação global permaneceram semanticamente idênticos à baseline.

## Resultado

```text
DOMAIN-INSTANCES-EXTRACTION = PASS
```

As quatro limitações residuais do plano permanecem abertas. Este resultado não
declara o validador pronto para atuar como gate bloqueante de produção.
