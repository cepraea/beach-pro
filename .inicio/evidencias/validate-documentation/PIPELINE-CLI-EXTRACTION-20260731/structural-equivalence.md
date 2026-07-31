# Equivalência estrutural da Fase 10

O primeiro change set moveu a sequência documental para
`pipeline.run_validation(args, reporter) -> None`. A ordem permaneceu:
registro, escopo, contratos, instâncias, integridade, canonicalidade, gate e
links. Cada fronteira retorna antes da etapa seguinte quando há erros.

O segundo change set moveu parser, validação da CLI e `main` para `cli.py`.
`main` cria um Reporter, valida argumentos, chama o pipeline quando permitido e
executa uma única emissão. `__main__.py` consulta diretamente `.cli.main`.

Os reexports transitórios permanecem em `__init__.py`. Cinco patches de
`parse_args` foram migrados para `cli`; os patches de estágios continuam nos
módulos proprietários. Testes dedicados comprovam que o pipeline não importa
CLI, não emite resultados e resolve o escopo antes dos contratos.
