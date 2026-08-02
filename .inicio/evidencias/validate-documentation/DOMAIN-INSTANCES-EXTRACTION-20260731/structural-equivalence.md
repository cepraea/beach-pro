# Equivalência estrutural da Fase 7

Cada responsabilidade foi extraída em change set próprio. Os corpos executáveis
foram comparados por AST antes do respectivo commit:

| Módulo | Funções | Resultado |
| --- | ---: | --- |
| `workflow.py` | 1 | idêntico |
| `approvals.py` | 1 | idêntico |
| `provenance.py` | 1 | idêntico |
| `ingestion.py` | 2 | idênticos |
| `instances.py` | 5 | idênticos |

Em `provenance.py` foi acrescentada somente uma docstring de função; ela foi
excluída da comparação do corpo executável.

Os reexports transitórios permanecem no pacote. Consumidores internos consultam
os módulos proprietários. Os cinco patches de `validate_instances` foram
migrados de `validator.validate_instances` para
`instances_module.validate_instances`.

Não houve alteração de schema, dado controlado, regra documental ou política de
gate.
