#!/usr/bin/env python3
from pathlib import Path

repo_readme = Path("README.md")
section_file = Path(__file__).with_name("AGENT_BOOTSTRAP.md")

if not repo_readme.exists():
    raise SystemExit("FAIL: execute na raiz do repositório; README.md não encontrado")
if not section_file.exists():
    raise SystemExit(f"FAIL: arquivo de seção não encontrado: {section_file}")

text = repo_readme.read_text(encoding="utf-8")
bootstrap = section_file.read_text(encoding="utf-8").rstrip() + "\n\n"

anchor = "# PARTE V — ARQUITETURA DO PLANO E DO FLUXO\n\n## 29. Fases candidatas\n"
if anchor not in text:
    raise SystemExit("FAIL: anchor da PARTE V ausente ou README divergente")

text = text.replace(
    anchor,
    "# PARTE V — ARQUITETURA DO PLANO E DO FLUXO\n\n" + bootstrap +
    "## 29. Task Lifecycle — fases candidatas\n",
    1,
)

old_boot = '''## 43. Regra geral das TASKs deste plano

Cada TASK abaixo precisa, antes de execução, ser expandida para o contrato completo da arquitetura definida neste arquivo, receber sua própria suite e passar Pre-Review. A lista abaixo define dependências e resultado atômico; não substitui o Task Contract detalhado.

### TASK-BOOT-000 — Validar o ambiente local do laboratório

**Resultado:** provar qual repositório, root, branch, HEAD, filesystem, ferramentas e configurações o agente local realmente enxerga.

**DONE:** inventário executado localmente; nenhuma informação do conector usada como substituto; evidência reproduzível produzida; gate = PASS.

### TASK-BOOT-001 — Construir e verificar o manifest de path parity

**Dependência:** `TASK-BOOT-000`.

**Resultado:** manifests machine-readable dos paths relevantes do Beach Pro e do laboratório + comparação determinística.

**Testes obrigatórios:** `PATH-UT-001..009` e golden fixtures do próprio comparador.

**DONE:** path verifier sensível a todos os known-bad; `PATH-PARITY-001` produz resultado explícito; nenhuma divergência silenciosa.

### TASK-F0 — Especificar e implementar F0
'''

new_boot = '''## 43. Regra geral das TASKs deste plano

O Agent Bootstrap é pré-condição do Task Lifecycle e, portanto, não pode depender de uma TASK normal ainda não autorizada por `AGENT_READY`. Os itens `BOOT-*` abaixo são **work items de bootstrap**, não Task Proposals de produto.

Somente após `AGENT_READY = PASS`, cada `TASK-F*` deve ser expandida para o contrato completo da arquitetura definida neste arquivo, receber sua própria suíte e passar Pre-Review. A lista abaixo define dependências e resultado atômico; não substitui o Task Contract detalhado.

### BOOT-000 — Full Bootstrap Review do laboratório

**Ator inicial:** Reviewer independente, read-only.

**Resultado:** provar qual repositório, root, branch, HEAD, working tree, inventário físico, autoridades, control plane, validadores e configurações efetivas o ambiente local realmente apresenta.

**Regra:** o Reviewer começa por `git status`/`git diff`; nenhuma informação deste conector ou de um manifesto substitui o estado observado.

**DONE:** `FULL_BOOTSTRAP_PASS = PASS`, evidência reproduzível produzida e baseline candidato emitido para operação privilegiada humana.

### BOOT-001 — Verificar paridade estrutural e de autoridade

**Dependência:** `BOOT-000`.

**Resultado:** comparar os paths relevantes do Beach Pro e do laboratório e verificar `SameRelativePath + SameRole + SameMutationAuthority + SameConsumerClass` para os artefatos sujeitos a espelhamento.

**Testes obrigatórios:** `PATH-UT-001..009`, golden fixtures do comparador e testes específicos de authority parity.

**DONE:** comparador sensível aos known-bad; `PATH-PARITY-001` e o gate de authority parity produzem verdict explícito; nenhuma divergência silenciosa.

### TASK-F0 — Especificar e implementar F0
'''

if old_boot not in text:
    raise SystemExit("FAIL: backlog BOOT esperado não encontrado")
text = text.replace(old_boot, new_boot, 1)

old_sequence = '''# PARTE XV — PRIMEIRA SEQUÊNCIA DE EXECUÇÃO APÓS ESTE PLANO

1. Agente local executa `TASK-BOOT-000` em read-only e produz evidência do próprio ambiente.
2. Humano e Reviewer confrontam o inventário local; nenhum dado deste conector substitui o resultado.
3. Elaborar Task Contract completo de `TASK-BOOT-001`.
4. Implementar manifest/validator de path parity no `CEPRAEA/testes` usando os paths confirmados localmente.
5. Executar `PATH-UT-001..009` e testar o próprio comparador com known-good/known-bad.
6. Somente após o laboratório estar estruturalmente validado, revisar adversarialmente a especificação candidata F0-v0.1.
7. Elaborar Task Contract completo de `TASK-F0`.
8. Pre-Review.
9. Implementação.
10. Testes e evidências.
11. Post-Review.
12. Repetir fase por fase até `TASK-F17`.
13. Executar a bateria E2E e golden fixtures.
14. Avaliar `DONE_GENERAL` pelo gate determinístico.
'''

new_sequence = '''# PARTE XV — PRIMEIRA SEQUÊNCIA DE EXECUÇÃO APÓS ESTE PLANO

1. Humano/operador privilegiado introduz a alteração candidata de bootstrap no working tree, sem commit.
2. Codex Reviewer é o primeiro agente a consumir a alteração e inicia `BOOT-000` por `git status` e `git diff`.
3. Reviewer executa os gates `B00..B15`; qualquer propriedade obrigatória não comprovada produz `FAIL`.
4. Se `FULL_BOOTSTRAP_PASS = PASS`, o humano executa a operação Git privilegiada aplicável e estabelece o baseline aprovado.
5. Executar `BOOT-001` para path parity e authority parity entre `CEPRAEA/testes` e CEPRAEA BEACH PRO.
6. Executor realiza Bootstrap Revalidation contra o baseline aprovado.
7. Somente `AGENT_READY = PASS` permite iniciar o Task Lifecycle.
8. Revisar adversarialmente a especificação candidata F0-v0.1.
9. Elaborar Task Contract completo de `TASK-F0`.
10. Pre-Review.
11. Implementação.
12. Testes e evidências.
13. Post-Review.
14. Repetir fase por fase até `TASK-F17`.
15. Executar a bateria E2E e golden fixtures.
16. Avaliar `DONE_GENERAL` pelo gate determinístico.
'''

if old_sequence not in text:
    raise SystemExit("FAIL: sequência final esperada não encontrada")
text = text.replace(old_sequence, new_sequence, 1)

old_state = "Próximo estado permitido: execução local e auditável de `TASK-BOOT-000`."
new_state = "Próximo estado permitido: alteração candidata no working tree → Reviewer-first `BOOT-000` → `PASS | FAIL`."
if old_state not in text:
    raise SystemExit("FAIL: registro de estado esperado não encontrado")
text = text.replace(old_state, new_state, 1)

repo_readme.write_text(text, encoding="utf-8")
print("PASS: README.md atualizado no working tree")
print("OBRIGATÓRIO AGORA: não fazer commit; Codex Reviewer deve executar git status/git diff primeiro.")
