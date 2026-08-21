# Scripts — verificação do ambiente de agentes

## `verify-agent-environment.sh`

Referência arquitetural canônica:

`docs/arquiteturas/multi-agentes/main/Human-Governed Dual-Agent SDLC Architecture.md`

O script verifica pré-condições observáveis do perfil BASE:

- processo não-root;
- Docker socket ausente;
- repositório `/workspaces/cepraea-beach-pro`;
- SOURCE_ROOT existente e read-only;
- managed settings/guard do Claude;
- configuração project/system do Codex;
- `.ai/control/control-plane.json`;
- ausência de credenciais privilegiadas conhecidas.

Execução:

```bash
bash .devcontainer/scripts/verify-agent-environment.sh
```

O script é verificador de pré-condições; não substitui filesystem/sandbox enforcement.

**Importante:** `test/scripts/bootstrap/README.md` atualmente declara o bootstrap arquitetural como `DESIGN / CANDIDATE / NOT VERIFIED`. O resultado deste script BASE e o bootstrap são mecanismos distintos. A promoção de qualquer bootstrap para gate global depende de decisão humana `ACTIVE`.
