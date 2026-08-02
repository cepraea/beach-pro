# Auditoria estrutural final

Resultados:

```text
alterações dinâmicas de sys.path: 0
imports curtos: 0
funções ou classes em __init__.py: 0
patch.object(validator, ...): 0
comandos Pyright sem @1.1.411 no plano: 0
ciclos no grafo de imports do pacote: 0
```

A busca por imports curtos foi ancorada no início da instrução para não tratar
o import canônico `from scripts.documentation import validate_documentation`
como ocorrência curta. Uma auditoria AST complementou a expressão regular.

A fachada declara `__all__ == ["main"]`, e o objeto exportado é exatamente
`cli.main`. `__main__.py` permanece restrito à entrada canônica da CLI.
