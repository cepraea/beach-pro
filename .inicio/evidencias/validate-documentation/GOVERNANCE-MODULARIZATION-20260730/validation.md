# Validação da Fase 0

Data UTC: `2026-07-30T13:25:54Z`.

## Ambiente

```text
Node.js v24.14.1
npm 11.11.0
Python 3.12.3
Pyright 1.1.411
```

`npm ci` instalou 621 pacotes a partir do lockfile. O npm informou dez
vulnerabilidades de severidade alta já presentes na resolução de dependências;
nenhuma atualização de dependência pertence ao escopo deste gate documental.

## Resultados verdes

| Verificação | Resultado |
| --- | --- |
| Markdownlint do plano, mapa e README | 0 ocorrências |
| `git diff --check` | PASS |
| `python3 -m compileall` | PASS |
| Pyright `1.1.411` em modo `strict` | 0 erros, 0 avisos, 0 informações |
| `npm run validate` | PASS |
| ESLint | PASS |
| Validação do workspace | PASS |
| TypeScript | PASS |
| Vitest | 1 teste aprovado |
| Build da PWA | PASS |

## Suíte Python e precondição da Fase 1

Comando executado:

```bash
python3 -m unittest discover \
  -s scripts/documentation/tests \
  -v
```

Resultado:

```text
92 testes descobertos
91 aprovados
1 falha
0 erros
```

A única falha foi
`EntrypointBehaviorTests.test_module_entrypoint_operates`: o subprocesso
executa G-ARCH e retorna `1` porque estes arquivos estão ausentes:

```text
docs/evidence/integrity/pacote-integridade-legado.tar
docs/evidence/provenance/pacote-fontes-contexto-cepraea.tar
docs/evidence/integrity/pacote-divergencia-relatorio-validacao-v01.tar
```

O plano reserva a aquisição e a verificação dos hashes desses bytes para a
Fase 1. Não foram criados TARs sintéticos, relaxados testes ou modificadas
regras para mascarar essa precondição.
