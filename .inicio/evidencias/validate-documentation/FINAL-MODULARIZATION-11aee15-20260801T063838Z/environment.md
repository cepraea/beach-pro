# Ambiente da validação final

```text
base: 11aee153be06f6ca76085b11e4b4ab112121ebd8
branch: agent/modularizacao-validator-fase-12
Python: 3.12.3
PyYAML: 6.0.1
jsonschema: 4.10.3
Node.js: 24.14.1
npm: 11.11.0
Pyright: 1.1.411
```

O `npm ci` foi tentado no worktree em `/tmp`, mas esse filesystem impediu a
execução do binário do esbuild com `EPERM`. Para a validação foi reutilizado o
`node_modules` materializado por `npm ci` na Fase 11, depois de confirmar que os
dois `package-lock.json` possuem o mesmo SHA-256
`be55ea580e419a121108e64e60eb88b17c2a313912f05392a441bca285c25396`.
O diretório reutilizado não integra a entrega. `npm run validate` foi executado
integralmente e aprovado fora da restrição de subprocessos do sandbox.
