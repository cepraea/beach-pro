# CEPRAEA BEACH PRO — Implantação da Arquitetura Formal de Verificação e Assurance

Documento de governança operacional para reduzir risco, manter a autoridade humana informada e preservar rastreabilidade durante a implantação da nova arquitetura.

**Escopo deste documento**
Este documento governa a implantação da camada formal de contrato e verificação no SDLC. Não altera o runtime do PWA, não substitui o Executor, não substitui o Reviewer e não concede autoridade de aprovação a agentes.

# GUIA 0 — IDENTIFICAÇÃO, BASELINE E ESCOPO

**Repositório**
`cepraea/beach-pro`

**Branch padrão**
`main`

**Branch de trabalho atualmente existente**
`feat/cepraea-domain-modeling`

Branch destinada à implantação da nova arquitetura
*PENDENTE DE DECISÃO HUMANA*. Nenhuma branch nova foi criada por este documento. A política atual reserva criação, alteração e promoção de refs Git ao humano.

**Recomendação não aprovada**
Criar uma branch dedicada, separada da modelagem de domínio, por exemplo `feat/formal-verification-control-plane`. Essa recomendação só se torna decisão após aprovação explícita do humano.

Fontes de autoridade e evidência consultadas no repositório
- ` AGENT_POLICY.md`
- ` CLAUDE.md`
- ` AGENTS.md`
- ` runbooks/README.md`
- ` runbooks/shared/RB-SHARED-003-failure-states.md`
- ` runbooks/reviewer/RB-REV-001-code-review.md`
- ` runbooks/reviewer/RB-REV-004-evidence- review.md`
- ` .ai/control/task-proposal.schema.json`
- ` .ai/control/verification- plan.schema.json`
- ` .ai/task- proposal.example.json`
- ` .ai/task- approval.example.json`
- ` .drive/FVR-1.0/IMPLEMENTATION_GUIDE.md`
- ` .drive/FVR-1.0/CONFORMANCE_CERTIFICATE_NOT_ISSUED.json`
- ` .devcontainer/Dockerfile`
- ` .devcontainer/devcontainer.json`
- ` docs/arquiteturas/multi-agentes/Human-Governed Dual-Agent SDLC Architecture.md`

**Observação de risco do baseline GitHub**
>No baseline consultado, a API do GitHub informou `protected=false para main`. Isso significa que a regra de controle humano existe na política do projeto, mas não está atualmente respaldada por branch protection do GitHub. Qualquer alteração dessa configuração exige decisão humana e deve ser tratada como mudança de controle.


