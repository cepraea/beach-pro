# Validação da identidade canônica

## Resultado

```text
CANONICAL-IMPORT-IDENTITY = PASS
```

A Fase 3 alterou somente identidade de importação, taxonomia dos testes,
configuração Pyright e documentação operacional. Nenhuma função ou classe do
validador foi movida ou reescrita.

## Portas executadas

| Verificação | Resultado |
| --- | --- |
| `compileall` | PASS |
| suíte unitária | 92/92 |
| integração do repositório | 1/1 |
| Pyright `1.1.411` strict | 0 diagnósticos |
| `npm run validate` | PASS |
| patches preservados | 49 |
| imports curtos | 0 |
| alterações de `sys.path` | 0 |

O npm reproduziu 621 pacotes e voltou a informar dez vulnerabilidades altas já
presentes no lockfile. Nenhuma dependência foi alterada por estar fora do
escopo da fase.

## Preservação da implementação

Os hashes permanecem iguais à baseline:

```text
cea98c3679955949c528d1153222343c5d0d6f306d74ce5ab23ac23350270f20  __init__.py
ea37b8a2dd6e649e52824b127ea384245018bdcf0c88bdf6f3f0559be365d6f2  __main__.py
```

Isso comprova que a fase não antecipou a extração modular.

## Comparação documental

G-ARCH, G0, G1, G2 para o contexto histórico `0.1`, G-FM para o canônico
`0.1.2` e a validação global retornaram código `0`. Após remover somente
`evaluated_at` e `gate_result_id`, todas as saídas são semanticamente idênticas
à baseline.

As limitações residuais registradas na seção 3.3 do plano permanecem abertas.
Este gate não declara o validador pronto para operar como bloqueio de produção.
