# DEC-ARQ-001 — Dev Container como sandbox operacional primário (Via B)

**Data da decisão original:** 2026-08-06 (histórica)
**Data desta restauração:** 2026-08-14
**Status da decisão:** PROPOSTA (rebaixado de "RATIFICADO" em 2026-08-14 —
ver nota de evidência abaixo)
**Estado do enforcement referenciado:** IMPLANTADO / VALIDADO PARCIALMENTE
NO RUNTIME (conforme `CONTAINER-RUNBOOK-v0.3.md` v0.4) — `ISO-05`
(`Privileged=false` comprovado por `docker inspect` centralizado) segue
`PENDENTE` no Runbook (§`ISO-05`, linha 681); os demais sinais são
compatíveis com container não privilegiado, mas não substituem essa
comprovação específica.
**Aprovador original:** Davi Sermenho
**Aprovador desta restauração:** Davi Sermenho (2026-08-14)
**Tipo:** governança arquitetural — reconstituição de decisão histórica

## Nota de evidência (2026-08-14)

Rebaixado de `RATIFICADO` para `PROPOSTA` após revisão independente: não
existe, neste checkout, artefato verificável da aprovação/ratificação por
Davi Sermenho nem da tarefa `RECONCILIA-ARQ-DUAL-AGENT-001` — o conteúdo
normativo abaixo depende de conversa e de `Leitura-e-análise-de-PDF
(5)(1).json`, ambos externos a este repositório. O conteúdo normativo é
mantido como está (não é uma reversão de decisão), mas o status reflete
que a ratificação ainda não tem lastro auditável dentro deste checkout.
Promoção de volta a `RATIFICADO` exige um artefato de aprovação
referenciável e verificável no repositório.

## Proveniência histórica

O objeto Git desta clonagem não contém os arquivos originais desta decisão:

```bash
git log --all --oneline -- .ai/decisions        # vazio
git show --stat 7734846 -- .ai/                  # só task-proposal.example.json
git show --stat 8839402 -- .ai/                  # só verification-plan.schema.json
git fsck --full --unreachable --dangling         # 67 objetos soltos (trees+blobs)
```

`git fsck` sozinho só lista hashes de objetos soltos; não pesquisa o
conteúdo deles. Correção de método (revisão de 2026-08-14): os 67 objetos
retornados por esse `git fsck` foram inspecionados individualmente —
`git cat-file -p <hash> | grep "DEC-ARQ-001"` para cada um dos 67 — com
resultado de 0 ocorrências. É essa varredura de conteúdo, não a mera
listagem de hashes, que sustenta a conclusão de que o banco de objetos
deste checkout não contém os artefatos originais de `DEC-ARQ-001`.

Davi Sermenho informou nesta conversa (2026-08-14) que os valores abaixo
constam de uma fonte histórica externa a este checkout,
`Leitura-e-análise-de-PDF (5)(1).json`, registrando a materialização
original de `DEC-ARQ-001` em 2026-08-06. Esse arquivo não está presente
neste ambiente/checkout; os valores são registrados aqui com base na
autoridade humana de Davi sobre a decisão, não confirmados por inspeção
direta de bytes por este agente:

```text
JSON_SHA256:
7e7114e2914f9c11ffaba473f79f3e7df4309540242d76b3a88e9561005d93d5

MARKDOWN_SHA256:
50832d4533cb88e6cc954a954aa4c0cce5d55aac89e85d36df453c4b8f6ff652
```

Esses hashes são evidência histórica dos artefatos originais. Eles **não**
são hashes deste arquivo reconstituído e não implicam que esta restauração
seja byte-a-byte idêntica ao original — o conteúdo normativo abaixo é uma
reconstituição do sentido da decisão, não uma cópia bit-a-bit comprovada.

## Estado histórico na criação — 2026-08-06

```text
DECISAO=APPROVED
IMPLEMENTACAO=PENDING
LIBERACAO_OPERACIONAL=BLOCKED_UNTIL_ACCEPTANCE
```

## Estado operacional posterior — Runbook v0.4 (2026-08-14)

```text
DEC-ARQ-001
APPROVED / IMPLANTADO / VALIDADO NO RUNTIME
```

Os dois blocos acima são snapshots de momentos diferentes, não uma
contradição: o primeiro é o estado na criação da decisão; o segundo é o
estado corrente registrado pelo Runbook após a implementação e os testes
E2E subsequentes.

## Decisão (conteúdo normativo reconstituído)

> Não enfraquecer o Dev Container para satisfazer o sandbox interno do
> Claude. O Dev Container é o sandbox operacional primário.

Rejeitadas explicitamente como correção automática para o sandbox interno
(Bubblewrap) não funcionar:

```text
privileged=true
CAP_SYS_ADMIN / SYS_ADMIN
seccomp=unconfined
Docker socket
```

Mantidos como controles primários: Dev Container non-root, `privileged=false`
(comprovação centralizada via `docker inspect` ainda `PENDENTE` — `ISO-05`,
`CONTAINER-RUNBOOK-v0.3.md` §`ISO-05`), sem Docker socket; mounts/proteções
do plano de controle; ausência de credenciais Git/GitHub privilegiadas do
agente; Git e promoção permanecem humanos, fora do container de agentes.

## Referências

- `.drive/multi-agentes/CONTAINER-RUNBOOK-v0.3.md`, §7 `DEC-ARQ-001`,
  §21 `VAL-004`.
- `Leitura-e-análise-de-PDF (5)(1).json` (fonte histórica citada por Davi
  Sermenho, 2026-08-14; arquivo não presente neste ambiente).
- Log de implementação citado no Runbook (ausente neste ambiente):
  `/home/davis/implementacao-dec-arq-001-20260806T044003Z.log`.
