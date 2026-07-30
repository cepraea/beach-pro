# Baseline executável do validador documental

## Resultado

```text
BASELINE-CODE = PASS
BASELINE-INTEGRATION = PASS
BASELINE-VALIDATE-DOCUMENTATION = PASS
BASELINE-NPM-VALIDATE = PASS
```

A baseline representa os bytes de
`main@88c3bc530fd0cc2496d9b2812b31d47ef7306d5e`. Nenhum código, teste, schema,
registro ou documento governado foi alterado durante sua execução.

## Ambiente e materialização

| Componente | Versão ou resultado |
| --- | --- |
| Python | `3.12.3` |
| PyYAML | `6.0.1` |
| jsonschema | `4.10.3` |
| Node.js | `24.14.1` |
| npm | `11.11.0` |
| Pyright | `1.1.411` |
| TARs | 3/3 hashes exatos |

O npm reproduziu 621 pacotes a partir do lockfile e reportou dez
vulnerabilidades altas já existentes. Nenhuma dependência foi atualizada,
porque essa remediação não pertence ao escopo da modularização.

## Inventários regenerados

| Inventário | Resultado |
| --- | --- |
| Funções de topo | 45 |
| Classes de topo | 3 |
| Métodos de `Reporter` | 4 |
| Métodos de teste | 92 |
| `patch.object` | 49 |
| Grupos de patch | 13 |

O diff desde o commit histórico `defaa043` contém mudanças apenas no mapa e no
README do pacote. Os inventários foram regenerados mesmo assim e confirmaram as
contagens anteriores.

Não há consumidor de produção que importe símbolos internos do pacote. O
arquivo `api-publica.tsv` registra `main` como futura fachada aprovada e os
demais nomes sem sublinhado como superfície incidental atual, ainda necessária
para compatibilidade dos testes durante as extrações.

## Portas de código e projeto

| Verificação | Resultado |
| --- | --- |
| `compileall` | código `0` |
| `unittest` | 92/92 |
| Pyright strict | 0 erros, 0 avisos, 0 informações |
| `npm run validate` | código `0` |
| Vitest | 1/1 |
| Build PWA | PASS |

O teste de entrada integrado passou com os TARs materializados. A separação em
`integration_tests/` pertence à Fase 3 e ainda não foi antecipada.

## Gates documentais

| Execução | Escopo | Status | Código |
| --- | --- | --- | --- |
| G-ARCH | global | pass | 0 |
| G0 | global | pass | 0 |
| G1 | global | pass | 0 |
| G2 | contexto `0.1` | pass | 0 |
| G-FM | contexto `0.1.2` | pass | 0 |
| Validação global | repositório | pass | 0 |

As saídas normalizadas removem somente `evaluated_at` e `gate_result_id`.
Identidade do documento, versão, hash, status, evidências, falhas e próximas
ações permanecem inalterados.

G2 conserva a versão histórica `0.1`, única coberta pelo pacote materializado.
Essa execução não declara resolvida a lacuna de proveniência do canônico
`0.1.2`, nem as outras limitações residuais registradas no plano.

## Reprodutibilidade

`hashes.sha256` ancora o pacote, testes, configuração Pyright, workflow,
registro, schemas, TARs, README, mapa e plano nos bytes existentes antes da
criação desta evidência. A futura atualização do campo de estado no plano não
reescreve essa fotografia: seu hash deve ser verificado contra o arquivo no
commit-base.

Os TARs são ignorados pelo Git. Outro clone ou worktree precisa rematerializar
ou reverificar esses bytes antes de usar a baseline em uma extração.
