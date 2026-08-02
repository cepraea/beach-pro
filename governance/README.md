# Enforcement local da governança adaptativa

Runtime autoritativo de `ACT-F00-007`, executado com o Node.js fixado pelo repositório.

## Comandos

```bash
npm run governance:test
npm run governance:validate -- checker-report.schema.json caminho/relatorio.json
npm run governance:route -- caminho/acao.json
npm run governance:canonicalize -- caminho/artefato.json
npm run governance:hash -- caminho/artefato.json
npm run governance:install-hooks
```

## Invariantes

- saídas inválidas retornam código diferente de zero;
- `APROVADO` é rejeitado em `CHECKER_REPORT`;
- gatilhos críticos elevam a ação para `VIA_CRITICA`;
- uma via declarada não é rebaixada silenciosamente;
- objetos JSON semanticamente equivalentes geram o mesmo `content_hash`;
- alteração semântica gera hash diferente;
- arrays preservam ordem;
- metadados voláteis definidos no perfil não participam do `content_hash`.

O hash prova identidade do conteúdo canônico. Não prova verdade, suficiência da fonte ou aprovação humana.
