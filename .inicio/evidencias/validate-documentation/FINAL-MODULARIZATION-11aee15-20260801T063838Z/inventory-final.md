# Inventário final por AST

| Inventário | Baseline | Resultado final | Explicação |
| --- | ---: | ---: | --- |
| Funções de topo | 45 | 47 | 45 migradas e 2 autorizadas |
| Classes de topo | 3 | 3 | Preservadas |
| Métodos de teste | 92 | 108 | 16 regressões e caracterizações |
| `patch.object` | 49 | 59 | 49 migrados e 10 posteriores |
| Grupos de patch | 13 | 15 | Alvos adicionais dos novos testes |

As duas funções novas autorizadas são `config.find_workspace_root` e
`pipeline.run_validation`. A matriz do plano foi verificada por nome e módulo:
as 45 funções históricas, as 2 funções novas e as 3 classes possuem exatamente
um módulo proprietário, sem ausências, duplicações ou proprietários incorretos.

Grupos atuais de patches:

```text
Path.read_text: 1
cli_module.parse_args: 5
config.DEFAULT_WORKFLOW: 1
config.INTEGRITY_MANIFEST: 1
config.WORKSPACE_ROOT: 7
contracts_module.validate_contract_schemas: 6
dispatcher_module.dispatch_gate: 4
g_arch_module.validate_garch: 1
instances_module.validate_instances: 5
links_module.validate_links: 3
pipeline_module.run_validation: 2
registry_module.load_registry: 7
registry_module.validate_canonical_registry: 3
registry_module.validate_registry_integrity: 5
reporter_module.Reporter.emit: 8
```
