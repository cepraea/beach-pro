# Equivalência estrutural da Fase 9

Cada gate e o dispatcher foram extraídos em change set próprio. Os corpos
executáveis foram comparados por AST antes do respectivo commit.

| Módulo | Função | Resultado |
| --- | --- | --- |
| `gates/g_arch.py` | `validate_garch` | idêntico |
| `gates/g0.py` | `validate_g0` | idêntico |
| `gates/g1.py` | `validate_g1` | idêntico |
| `gates/g2.py` | `validate_g2` | idêntico |
| `gates/g_fm.py` | `validate_front_matter` | idêntico |
| `gates/dispatcher.py` | `dispatch_gate` | idêntico |

Os reexports transitórios permanecem no pacote. O pipeline consulta
`dispatcher.dispatch_gate()` e o dispatcher consulta os módulos proprietários
dos gates. Quatro patches do pipeline foram migrados para o dispatcher; o patch
de G-ARCH foi migrado para `g_arch`.

Não houve alteração de schema, dado controlado, escopo, regra documental ou
política de gate. As quatro limitações residuais não foram corrigidas nem
ocultadas durante a extração.
