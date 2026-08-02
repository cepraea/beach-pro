# Validação da materialização dos TARs

## Resultado

```text
TAR-MATERIALIZATION = PASS
```

O resultado vale para o worktree em que os bytes foram materializados. Como os
TARs são ignorados pelo Git, outro clone ou worktree deve verificar fontes
locais próprias antes de reutilizar o gate.

## Aquisição

Os três destinos estavam ausentes. As fontes já existiam em outro worktree
local e foram aceitas somente depois de seus SHA-256 coincidirem exatamente com
o manifesto do plano.

A cópia foi executada sem permissão para sobrescrever destinos existentes. Os
hashes foram recalculados depois da cópia e permaneceram idênticos. O arquivo
[`tar-acquisition.yaml`](tar-acquisition.yaml) registra os identificadores,
tamanhos, hashes e a política operacional utilizada.

## Manifesto verificado

| Artefato | SHA-256 | Estado |
| --- | --- | --- |
| `pacote-integridade-legado.tar` | `7b0d9effe3da654af63638f8850841332605f9c535a8a7181ac021b5be284cf6` | PASS |
| `pacote-fontes-contexto-cepraea.tar` | `3f49cde024244a630cf0e4e335348d26252cf7550ec586e0e78d4ff609ecfc21` | PASS |
| `pacote-divergencia-relatorio-validacao-v01.tar` | `6dcfdc0f295e40e77fdd82be3b4dce4b47f6c04d43ef9fe553b140b375da97ec` | PASS |

Os arquivos aparecem no estado Git somente como ignorados por `*.tar`. Nenhum
TAR foi adicionado ao staging ou será versionado.

## Verificações funcionais

```text
python3 -m unittest discover -s scripts/documentation/tests -v
92 testes executados
92 aprovados
0 falhas
0 erros
```

O teste de entrada que anteriormente falhava pela ausência dos pacotes passou
depois da materialização.

```text
python3 -m scripts.documentation.validate_documentation \
  --gate G-ARCH \
  --format yaml

status: pass
exit code: 0
```

Não houve alteração de código, schema ou regra documental para alcançar esses
resultados.

## Porta geral do projeto

Após `npm ci`, a porta obrigatória também foi executada:

```text
npm run validate
exit code: 0
```

ESLint, Markdownlint governado pelo script, validação do workspace, TypeScript,
Vitest e build da PWA passaram. O npm informou dez vulnerabilidades de
severidade alta na resolução existente do lockfile; nenhuma dependência foi
alterada porque a remediação desse inventário não pertence ao escopo da Fase 1.
