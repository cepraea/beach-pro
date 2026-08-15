# RB-REV-005 — Revisão de dependência

## Objetivo

Definir o procedimento especializado de revisão independente para inclusão, remoção,
atualização de dependências e alterações deliberadas de lockfile no CEPRAEA BEACH PRO.

## Aplicabilidade

Use este runbook quando o Reviewer receber um `git diff` resultante de:

- inclusão de nova dependência;
- remoção de dependência existente;
- atualização de versão de dependência;
- alteração deliberada de lockfile.

Este runbook corresponde à classe de operação `dependency_change`.

## Entradas

- `git diff` completo da alteração;
- `package.json` e lockfile afetados;
- critérios de aceite da tarefa;
- evidências produzidas pelo Executor;
- justificativa da alteração de dependência;
- versão anterior e versão proposta, quando aplicável.

## Fontes de autoridade

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md);
- [`AGENTS.md`](../../AGENTS.md);
- `package.json`;
- lockfile canônico do projeto;
- critérios de aceite da tarefa;
- documentação ou configuração do runtime existente, quando necessária para verificar compatibilidade.

## Pré-condições

Antes da revisão:

1. confirme a tarefa e seus critérios de aceite;
2. confirme que a classe da operação é `dependency_change`;
3. confirme que o `git diff` está disponível;
4. identifique os manifests e lockfiles alterados;
5. identifique a dependência afetada e a operação realizada;
6. confirme que o Reviewer opera com o projeto em modo read-only.

## Escopo operacional

Restrinja a revisão exclusivamente à inspeção e à verificação independente da alteração de
dependência e de seus efeitos materiais relacionados.

Use exclusivamente operações de leitura sobre o working tree.

Direcione qualquer escrita técnica necessária para verificações independentes a `/tmp` ou a
caches explicitamente autorizados.

Preserve o working tree sem modificações durante toda a revisão.

## Procedimento

1. Confirme a dependência adicionada, removida ou atualizada.

2. Compare o objetivo da tarefa com a alteração observada em `package.json`.

3. Confirme a versão anterior e a versão resultante, quando aplicável.

4. Inspecione o lockfile completo relacionado à alteração.

5. Verifique se a mudança no lockfile é compatível com a alteração declarada no manifest.

6. Identifique alterações transitivas materialmente relevantes introduzidas pelo lockfile.

7. Verifique se a dependência foi classificada corretamente como dependência de produção ou de
   desenvolvimento.

8. Verifique a compatibilidade declarada com:
   - versão do Node utilizada pelo projeto;
   - runtime existente;
   - dependências diretamente relacionadas;
   - ferramentas de build e typecheck aplicáveis.

9. Verifique se arquivos de configuração adicionais foram alterados e se essas alterações são
   necessárias à dependência autorizada.

10. Confronte a justificativa da alteração com o estado observável do repositório.

11. Verifique os impactos materiais registrados pelo Executor, quando aplicáveis:
    - compatibilidade;
    - licença;
    - runtime;
    - build;
    - tamanho de bundle, quando houver evidência produzida para essa propriedade.

12. Reexecute verificações independentes proporcionais ao risco e compatíveis com o ambiente
    read-only.

13. Compare os resultados independentes com as evidências fornecidas pelo Executor.

14. Verifique alterações fora do escopo autorizado.

15. Emita o verdict correspondente.

## Pontos de decisão

| Condição | Ação |
| --- | --- |
| Dependência ou versão difere da tarefa autorizada | `FAIL` com finding |
| Lockfile contém alteração material sem correspondência com a mudança declarada | Investigue a causa; use `FAIL` quando a divergência impedir aceitação |
| Dependência de produção foi registrada como desenvolvimento, ou o inverso | `FAIL` quando a classificação produzir comportamento incorreto |
| Dependência exige mudança de runtime não autorizada | `HUMAN_DECISION_REQUIRED` quando a mudança exigir decisão material |
| Compatibilidade requerida não pode ser demonstrada | Finding proporcional ao impacto |
| Build, typecheck ou teste aplicável apresenta regressão causada pela dependência | `FAIL` |
| Licença materialmente incompatível foi demonstrada | `FAIL` |
| A compatibilidade de licença depende de interpretação ou decisão ainda não estabelecida | `HUMAN_DECISION_REQUIRED` |
| Alterações transitivas relevantes estão sem explicação ou evidência suficiente | Finding proporcional ao impacto |
| Arquivo fora do escopo foi alterado sem necessidade demonstrável | `FAIL` quando a expansão for material |
| Evidência material é insuficiente | Aplique também `RB-REV-004-evidence-review.md` quando previsto pelo `runbook_binding` |

## Validações independentes

Execute somente as verificações compatíveis com o ambiente read-only e proporcionais ao risco.

Quando aplicável:

- inspecione o diff de `package.json`;
- inspecione o diff completo do lockfile;
- confirme a consistência entre manifest e lockfile;
- execute o build sem modificar o projeto;
- execute o typecheck sem emissão de artefatos persistentes;
- execute testes selecionados para as áreas afetadas;
- verifique a resolução da dependência utilizando comandos somente de inspeção;
- confronte versões e alterações transitivas com o lockfile.

Direcione caches e saídas temporárias exclusivamente para locais autorizados quando a
ferramenta exigir escrita.

Uma limitação do runtime que impeça uma verificação DEVE ser reportada como limitação de
evidência, sem converter ausência de verificação em sucesso.

## Evidências

Registre no review somente evidências materiais para o verdict.

Inclua, quando aplicável:

- dependência revisada;
- operação realizada: inclusão, remoção ou atualização;
- versão anterior e versão resultante;
- diff de `package.json` inspecionado;
- diff do lockfile inspecionado;
- alterações transitivas materialmente relevantes identificadas;
- verificações independentes executadas;
- exit codes e resultados relevantes;
- incompatibilidades encontradas;
- findings classificados.

Use [`RB-REV-004-evidence-review.md`](./RB-REV-004-evidence-review.md) adicionalmente quando a
suficiência da evidência for material para a aceitação da tarefa e estiver declarada no
`runbook_binding`.

## Handoff

Emita um handoff factual contendo:

- dependência revisada;
- operação realizada;
- versão anterior e versão resultante, quando aplicável;
- manifests e lockfiles inspecionados;
- verificações independentes executadas;
- resultados observados;
- impactos materiais confirmados;
- limitações de verificação;
- findings classificados, quando existirem;
- questões que dependam de decisão humana.

## Estados de saída

`PASS` — a alteração de dependência corresponde à tarefa autorizada, manifest e lockfile são
consistentes, as verificações aplicáveis não identificam regressão bloqueante e as alegações
materiais possuem evidência suficiente.

`FAIL` — a alteração apresenta erro técnico, incompatibilidade demonstrada, regressão,
inconsistência material entre manifest e lockfile, expansão material de escopo ou evidência
insuficiente que impeça aceitação.

`HUMAN_DECISION_REQUIRED` — a conclusão depende de decisão material que pertence à autoridade
humana, incluindo mudança de runtime, aceitação de trade-off ou questão sem precedente
suficiente para decisão técnica independente.

Finalize exclusivamente com um destes verdicts:

- `PASS`;
- `FAIL`;
- `HUMAN_DECISION_REQUIRED`.

## Referências

- [`AGENT_POLICY.md`](../../AGENT_POLICY.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`RB-EXEC-004-dependency-change.md`](../executor/RB-EXEC-004-dependency-change.md)
- [`RB-REV-004-evidence-review.md`](./RB-REV-004-evidence-review.md)
- [`RB-SHARED-002-evidence.md`](../shared/RB-SHARED-002-evidence.md)
- [`RB-SHARED-003-failure-states.md`](../shared/RB-SHARED-003-failure-states.md)
