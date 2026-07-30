# Validação das fundações e descoberta do workspace

## Resultado

```text
FOUNDATIONS = PASS
WORKSPACE-DISCOVERY = PASS
```

Os resultados foram produzidos na branch da Fase 4 e tornam-se efetivos após a
incorporação da PR #7 à `main`.

## Portas executadas

| Verificação | Resultado |
| --- | --- |
| `compileall` | PASS |
| suíte unitária | 98/98 |
| integração do repositório | 1/1 |
| Pyright `1.1.411` strict | 0 diagnósticos |
| `npm run validate` | PASS |
| comparação normalizada dos gates | PASS |
| referências legadas de patch de configuração | 0 |

A contagem unitária passou de 92 para 98 porque BEH-01 exigiu seis cenários
novos. Não houve remoção ou relaxamento de testes preexistentes.

## Extrações estruturais

As responsabilidades foram movidas em commits separados:

- fronteiras dinâmicas de JSON e YAML para `json_types.py`;
- `ValidatorArgs` para `models.py`;
- paths e configuração para `config.py`;
- `workspace_path` e `sha256` para `filesystem.py`.

Os consumidores consultam `config.WORKSPACE_ROOT` no módulo proprietário. Os
reexports no pacote são transitórios e não constituem o ponto de patch.

## Preservação comportamental

G-ARCH, G0, G1, G2 para o contexto histórico `0.1`, G-FM para o canônico
`0.1.2` e a validação global retornaram código `0`. Depois da remoção exclusiva
de `evaluated_at` e `gate_result_id`, os resultados permaneceram idênticos à
baseline.

As limitações residuais do plano não foram alteradas nesta fase.
