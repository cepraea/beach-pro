# Revisão do gate de governança da modularização

## Resultado

```text
GOVERNANCE-MODULARIZATION = PASS
```

O resultado torna-se operacional quando a PR #3 for incorporada à `main`.
Nenhuma extração de código integra esta entrega.

## Critérios verificados

- O plano ativo está identificado pelo caminho canônico.
- A baseline usa o `HEAD` real e invalidação sensível aos caminhos do código,
  testes e configuração Pyright.
- O mapa não proíbe movimentações autorizadas e limita cada change set a um
  módulo proprietário.
- O mapa separa extração estrutural de mudança comportamental.
- A direção permitida de dependências está registrada no plano e no mapa.
- O fail-fast resolve o escopo documental antes de validar contratos.
- O README distingue migração concluída, monólito transitório e modularização
  incremental.
- O README distingue suíte unitária de integração dependente dos TARs.
- Os comandos Pyright usam a versão fixa `1.1.411`.
- O exemplo de G-FM usa o canônico `0.1.2`.
- A cobertura histórica de G2 em `0.1` e a lacuna de `0.1.2` permanecem
  explícitas.
- `Plano-validator.md` e `Plano-migracao-validator.md` foram preservados como
  registros históricos.
- As decisões `BEH-01…BEH-07` e o aprovador permanecem vinculados à evidência
  de autorização.
- A regra de qualidade exige código autoexplicativo e comentários sobre o
  porquê de decisões técnicas complexas.

## Invariantes de escopo

O worktree foi criado a partir de
`main@fcbc84dc19ca42c57ece96132def71c1a7420b19`. O diff entre o commit histórico
dos inventários e esse ponto não contém mudanças no pacote, nos testes Python
ou em `pyrightconfig.json`; portanto, os inventários existentes continuam
válidos para preparar a baseline.

As modificações não relacionadas existentes no worktree original não foram
movidas, restauradas, adicionadas ao staging ou incluídas na PR.

## Bloqueio seguinte

Os três TARs ignorados pelo Git não existem neste worktree limpo. A suíte
Python confirmou 91 testes aprovados e uma falha no teste de entrada que
executa G-ARCH. Esse resultado é a precondição já documentada para a Fase 1,
não uma falha do gate de governança.

A Fase 1 somente pode começar depois do merge da PR #3. Nenhuma extração
modular pode começar antes de:

```text
TAR-MATERIALIZATION = PASS
```
