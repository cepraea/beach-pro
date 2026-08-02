# Auditoria de consumidores da fachada pública

A pesquisa local cobriu código, testes, documentação operacional e evidências
versionadas. Não foi encontrado consumidor interno aprovado dos aliases
transitórios removidos de `validate_documentation.__init__`.

Os consumidores de tipos e funções nos testes foram migrados para os módulos
proprietários. O uso operacional permanece:

```text
python3 -m scripts.documentation.validate_documentation
```

As referências a `scripts/documentation/validate_documentation.py` presentes
em evidências e relatórios históricos foram preservadas, pois descrevem o
avaliador existente no momento daquelas execuções.

## Limite da conclusão

Uma busca com `rg` no repositório comprova apenas a situação interna
versionada. Ela não comprova a inexistência de consumidores externos. A
contração é autorizada pela decisão formal `BEH-07`; eventual integração
externa não registrada deverá importar módulos proprietários ou passar por uma
nova decisão de contrato.
