# Fluxo completo de desenvolvimento — CEPRAEA BEACH PRO

<!-- Atualizar este documento quando o domínio, as fases ou o ciclo agêntico forem alterados.
Utilize blocos mermaid para os fluxos
-->

## Domínio consolidado

```text
Domain-Driven Design (DDD)
   +
Human-Governed Agentic SDLC
   +
Deterministic Software Assurance
```
CEPRAEA BEACH PRO é uma Progressive Web App (PWA) de gestão esportiva voltada para atletas e treinadores de handebol de areia do CEPRAEA, desenvolvida por Davi Sermenho como projeto solo.

Escopo funcional: gestão de atletas, treinadores, treinos, jogos, presenças e avaliações.

Stack: React + TypeScript + Vite, com backend Supabase (PostgreSQL + Auth + RLS) hospedado na região São Paulo, deploy via Cloudflare Pages, autenticação de email via Brevo — tudo dentro de orçamento zero.

Característica distintiva: o projeto opera sob uma camada formal de governança de agentes de IA (AGENT_POLICY.md), que define papéis, classificação de risco, checkpoints obrigatórios e restrições de execução — o que o coloca além de um simples projeto assistido por IA e o aproxima de um modelo de desenvolvimento humano-IA com controle explícito de autoridade.

**Domínio consolidado:** _Human-Governed Agentic Software Development with Domain-Driven Deterministic Runtime_

## Subdomínios

| Nº | Subdomínio | Descrição |
| :---: | :--- | :--- |
| 1 | Gestão esportiva de alto rendimento | Operação do CEPRAEA Adulto Feminino — atletas, vínculos, convocações, treinos, jogos, resultados, scouting, Wellness |
| 2 | Domain-Driven Design (DDD) | Bounded Contexts, agregados, identidades, invariantes, ciclos de vida, fronteiras transacionais |
| 3 | Engenharia agêntica governada | Executor + Reviewer independentes, `AGENT_POLICY`, classificação de risco, checkpoints |
| 4 | Assurance determinístico | Tipos, constraints, RLS, testes automatizados, evidências verificáveis — sem dependência de LLM em runtime |
| 5 | Rastreabilidade e governança documental | Cadeia `SRC → EVD → TERMO/REGRA → candidatos → domínio → lógico`, schemas formais, namespaces de ID |
| 6 | Segurança e privacidade de dados | Dados sensíveis (senhas, Wellness), RLS, autenticação, proteção de contexto |

## Tema central

A realidade operacional do CEPRAEA deve ser representada no software de forma única, semanticamente inequívoca, historicamente preservada e verificável — e essa representação é construída por um processo agêntico cujo resultado é determinístico e independente de IA em runtime.

## Escopo permitido

No produto (runtime):

- Gestão de atletas, treinadores, vínculos, agenda, treinos, jogos, disponibilidade, presença, convocações, resultados, scouting, comunicação, feedbacks e Wellness
- Regras de negócio implementadas por tipos, validações, constraints, RLS e testes
- Estado operacional único e rastreável da equipe
- Offline-first com sincronização

No processo de engenharia:

- Agentes executando dentro de `WRITE_SCOPE` definido
- Proposta formal antes de escrita de risco amarelo/vermelho
- Fixtures sintéticas aprovadas por Davi
- Commits e evidências rastreáveis por Git
- Reviewer emitindo `PASS | FAIL | HUMAN_DECISION_REQUIRED`

## Escopo proibido

No produto (runtime):

- LLMs tomando decisões de negócio
- Inferência não sustentada por evidência como regra operacional
- Dois schemas físicos ou modelos canônicos coexistentes

No processo de engenharia:

- Encerre o fluxo de execução estritamente com a geração da working tree alterada — operações de commit, push, merge, rebase, deploy e manipulação de secrets pertencem exclusivamente a Davi
- Restrinja toda escrita obrigatoriamente ao `WRITE_SCOPE` definido
- Percorra a cadeia de promoção completa — promoção direta `fonte → modelo lógico` sem etapas intermediárias é proibida
- Marque elementos como `VALIDADO` somente após aprovação de Davi Sermenho
- Preserve decisões canônicas existentes — ajustes retroativos para justificar código já escrito são proibidos
- Restrinja escritas exclusivamente a branches de trabalho — `main`/`master` recebe somente integrações realizadas por Davi
- Represente dados sensíveis obrigatoriamente por descrição de tipo e formato, nunca por valor literal
- Mantenha exclusivamente um agente escritor por branch

## Taxonomia

```text
DOMÍNIO
├── PRODUTO (runtime)
│   ├── Entidades: Atleta, Treinador, Vínculo, Treino, Jogo, Convocação, Presença, Wellness
│   ├── Bounded Contexts: CTX-001..CTX-008 (candidatos)
│   ├── Invariantes: INV-001.. (ex.: papel único por usuário)
│   └── Modelo Canônico → Modelo Lógico → Schema Físico (fases separadas)
│
└── PROCESSO DE ENGENHARIA
    ├── Atores: Davi (autoridade), Executor (Claude Code), Reviewer (Codex)
    ├── Artefatos: dossiê (SRC), evidência (EVD), termo (TERMO), regra (REGRA),
    │             candidato, elemento de domínio, modelo lógico
    ├── Ações: AC-NNN (aquisição), SEM-NNN (reconciliação), SYN-NNN (síntese)
    ├── Estados epistemológicos: OBSERVADO → INFERIDO → AMBÍGUO/CONFLITANTE → VALIDADO/REJEITADO
    ├── Estados de maturidade: IMATURA → PARCIALMENTE_MADURA → MADURA_PARA_MODELO_LOGICO
    └── Risco: Verde → Amarelo → Vermelho → Vermelho Crítico
```

## Contexto válido e contexto inválido

| Situação | Classificação | Justificativa |
| :--- | :---: | :--- |
| Agente propõe implementação de invariante de domínio com evidência rastreável | Válido | Domínio governa código, processo correto |
| Reviewer emite `FAIL` com justificativa técnica | Válido | Assurance independente dentro do fluxo |
| Davi aprova promoção de candidato para domínio | Válido | Única fonte de `VALIDADO` |
| Elemento nasce `INFERIDO` em `candidatos/` | Válido | Estado epistemológico honesto, sem salto |
| Bounded Context permanece `IMATURA` ao final da fase | Válido | Resultado válido, registrado como tal |
| Credencial encontrada em fonte é tratada como dado sensível sem transcrição | Válido | Proteção de contexto, melhoria b do processo |
| Agente escreve diretamente em `dominio/` sem candidato prévio | Inválido | Viola cadeia de promoção e INV-PROC-003 |
| LLM interpreta regra de negócio em runtime | Inválido | Viola separação produto/processo; runtime deve ser determinístico |
| Elemento marcado `VALIDADO` com `aprovador=PENDENTE` | Inválido | Schema rejeita; `VALIDADO` exige aprovação humana real |
| Agente ajusta decisão canônica para justificar código já escrito | Inválido | Inversão explicitamente proibida pelo `AGENT_POLICY` |
| Reviewer aprova sem evidência — apenas por concordância | Inválido | Assurance sem base não é assurance |
| Bounded Context `MADURA_PARA_MODELO_LOGICO` com conflito estrutural pendente | Inválido | Viola INV-PROC-008 |
| Agente cria branch, faz push ou merge | Inválido | Operações reservadas exclusivamente a Davi |
| Modelo lógico derivado de candidato não validado | Inválido | Viola INV-PROC-002 e regra de promoção |

## Visão geral

```text
REALIDADE DO CEPRAEA
        ↓
AUTORIDADE HUMANA (Davi Sermenho)
        ↓
DESCOBERTA E MODELAGEM DO DOMÍNIO
        ↓
REQUISITOS E INVARIANTES HOMOLOGADOS
        ↓
CICLO AGÊNTICO GOVERNADO
        ↓
IMPLEMENTAÇÃO VERIFICÁVEL
        ↓
ASSURANCE INDEPENDENTE
        ↓
INTEGRAÇÃO E RELEASE (Davi)
        ↓
CEPRAEA BEACH PRO EM RUNTIME
```

## Fase 0 — Fundação e governança

**Quem:** Davi

### Grupo A — Repositório e controle de versão

| ID | Ação atômica | Verificação de conclusão |
| :--- | :--- | :--- |
| F0-A01 | Criar repositório `cepraea-beach-pro` no GitHub (privado) | Repositório existe e está acessível |
| F0-A02 | Inicializar Git local (`git init`) | `.git/` presente |
| F0-A03 | Conectar remote origin ao repositório GitHub | `git remote -v` retorna origin correto |
| F0-A04 | Proteger branch `main` — somente Davi integra | Branch protection rule ativa no GitHub |
| F0-A05 | Criar `.gitignore` | Arquivo presente; `node_modules/`, `.env` e `dist/` excluídos |

### Grupo B — Decisões arquiteturais (DEC-015 / DEC-019)

| ID | Ação atômica | Verificação de conclusão |
| :--- | :--- | :--- |
| F0-B01 | Registrar DEC-015: stack React + TypeScript + Vite | Decisão registrada com aprovador e data |
| F0-B02 | Registrar DEC-019: Supabase (região São Paulo), Cloudflare Pages, Brevo SMTP, orçamento zero | Decisão registrada com aprovador e data |

### Grupo C — Governança de agentes

| ID | Ação atômica | Verificação de conclusão |
| :--- | :--- | :--- |
| F0-C01 | Criar `AGENT_POLICY.md` com classificação de risco (Verde / Amarelo / Vermelho / Vermelho Crítico) | Arquivo presente, seções de risco definidas |
| F0-C02 | Definir papéis de arquivo no `AGENT_POLICY.md` (alvo, referência, somente leitura, proibido) | Papéis descritos e exemplificados |
| F0-C03 | Definir escopos de escrita (`WRITE_SCOPE`) no `AGENT_POLICY.md` | `WRITE_SCOPE_EXECUTOR` e `WRITE_SCOPE_REVIEWER` declarados |
| F0-C04 | Definir checkpoints obrigatórios por nível de risco | Regras de checkpoint presentes e não ambíguas |
| F0-C05 | Criar `CLAUDE.md` referenciando `AGENT_POLICY.md` | Arquivo presente, instrução de leitura obrigatória |

### Grupo D — Ambiente de desenvolvimento

| ID | Ação atômica | Verificação de conclusão |
| :--- | :--- | :--- |
| F0-D01 | Criar `cepraea-beach-pro.code-workspace` | Arquivo presente, workspace abre sem erro |
| F0-D02 | Criar `.vscode/extensions.json` com extensões recomendadas | Arquivo presente |
| F0-D03 | Criar `.vscode/tasks.json` e `.vscode/launch.json` | Arquivos presentes |
| F0-D04 | Criar `.editorconfig` | Arquivo presente |
| F0-D05 | Criar `.prettierrc` | Arquivo presente |
| F0-D06 | Criar `.env.example` (sem valores reais) | Arquivo presente, nenhuma credencial real |

### Grupo E — Configuração do projeto Node/TypeScript

| ID | Ação atômica | Verificação de conclusão |
| :--- | :--- | :--- |
| F0-E01 | Criar `package.json` com scripts `dev`, `build`, `lint`, `format`, `typecheck`, `test`, `validate` | Scripts presentes e executáveis |
| F0-E02 | Criar `tsconfig.json` com `strict: true` | Arquivo presente, `tsc --noEmit` passa |
| F0-E03 | Criar `vite.config.ts` com plugin React e PWA | Arquivo presente, `vite build` executa sem erro |
| F0-E04 | Criar `eslint.config.js` (flat config) | Arquivo presente, `eslint .` executa sem erro |
| F0-E05 | Executar `npm install` | `node_modules/` presente, `package-lock.json` gerado |

### Grupo F — Estrutura de código fonte

| ID | Ação atômica | Verificação de conclusão |
| :--- | :--- | :--- |
| F0-F01 | Criar estrutura `src/` feature-based: `atletas/`, `treinadores/`, `treinos/`, `jogos/`, `presencas/`, `avaliacoes/`, `shared/` | Diretórios presentes |
| F0-F02 | Criar `src/main.tsx` e `src/App.tsx` como ponto de entrada | App renderiza sem erro (`npm run dev`) |

### Critério de conclusão da Fase 0

A Fase 0 está concluída quando todos os grupos A–F estiverem verificados e o repositório estiver no estado:

```text
git status        → working tree clean
npm run validate  → typecheck + lint + build passam sem erro
main protegida    → exclusivamente Davi integra nela
AGENT_POLICY.md   → presente e aplicável
```

> **Saída:** repositório com governança técnica operacional.

---

## Fase 1 — Descoberta e modelagem do domínio

**Branch:** `feat/cepraea-domain-modeling`\
**Quem:** Executor (Claude Code) + Davi como aprovador\
**Plano:** `PLANO-CEPRAEA-MODELO-CANONICO-002`

### Cadeia obrigatória de promoção

```text
.drive/CEPRAEA BEACH PRO/  →  fontes/  →  evidencias/  →  conhecimento/  →  candidatos/  →  dominio/  →  logico/
       (28 fontes)             SRC-NNN     EVD-NNNN        TERMO/REGRA       CTX/INV/AGG     VALIDADO    MADURA
```

Nenhuma etapa pode ser pulada.

### Sequência de ações

1. `AC-000` — **Bootstrap:** estrutura `docs/modelagem/`, schemas formais, pré-seed de INV-001 e CTX-001..008, registro de DEC-001..003
2. `AC-001` a `AC-028` — **Aquisição:** um dossiê `SRC-NNN` por fonte, com fragmentos `EVD-NNNN`, termos, regras e candidatos
3. `SEM-NNN` — **Reconciliação:** resolução de `AMBÍGUO/CONFLITANTE`, promoção `candidatos/ → dominio/`, aprovação de Davi
4. `AC-029` — **Síntese:** avaliação de maturidade por Bounded Context, escrita de `modelo_canonico_dominio.md`
5. `SYN-NNN` — **Síntese lógica:** modelo lógico relacional apenas para CTX em `MADURA_PARA_MODELO_LOGICO`

### Gate de maturidade por Bounded Context

```text
IMATURA  →  PARCIALMENTE_MADURA  →  MADURA_PARA_MODELO_LOGICO
                                              ↓
                                     entra no modelo lógico
```

Bounded Context com conflito estrutural pendente nunca atinge `MADURA_PARA_MODELO_LOGICO`.

Cobertura documental (100% das fontes processadas) não implica maturidade semântica.

### Estados epistemológicos dos elementos

```text
OBSERVADO → INFERIDO → AMBÍGUO ──→ CONFLITANTE
                              ↘
                          VALIDADO (exige aprovação de Davi)
                              ↓
                          REJEITADO
```

> **Saída:** `dominio/modelo_canonico_dominio.md` + modelo lógico das áreas maduras.

---

## Fase 2 — Schema físico e infraestrutura de dados

**Fora do escopo da Fase 1 — fase separada**\
**Quem:** Executor + Reviewer + Davi

- Derivação do schema físico PostgreSQL/Supabase a partir do modelo lógico validado
- Migrations de domínio
- Políticas RLS
- Autenticação (Supabase Auth + Brevo SMTP)
- Migrations escritas somente após modelo lógico aprovado como base

---

## Fase 3 — Implementação das funcionalidades (M0–M4)

**Quem:** Executor (Claude Code) operando sob `AGENT_POLICY`\
**Reviewer:** Codex

### Ciclo agêntico por funcionalidade

```text
┌─────────────────────────────────────────────────────┐
│                 AUTORIDADE HUMANA                   │
│         requisito homologado + invariantes          │
└──────────────────────┬──────────────────────────────┘
                       ↓
              CLASSIFICAÇÃO DE RISCO
         Verde | Amarelo | Vermelho | Vermelho Crítico
                       ↓
         ┌─────────────────────────────┐
         │  [Amarelo/Vermelho]         │
         │  PROPOSTA FORMAL            │
         │  - arquivos alvo            │
         │  - arquivos referência      │
         │  - arquivos somente leitura │
         │  - arquivos proibidos       │
         │  - evidências e riscos      │
         └──────────┬──────────────────┘
                    ↓ checkpoint Davi
              EXECUTOR — Claude Code
              (dentro de WRITE_SCOPE)
              implementação + validação Shift-Left
              (tipos, testes, lint, typecheck)
                    ↓
              ALTERAÇÃO PROPOSTA + EVIDÊNCIA
                    ↓
              REVIEWER — Codex
              (independente do Executor)
                    ↓
         ┌──────────────────────────────────┐
         │   PASS  │  FAIL  │ HUMAN_DECISION │
         └──────────────────────────────────┘
                    ↓ PASS
              DAVI — commit, push, merge
              Git / integração / release
```

### Regras invariantes do ciclo

- Mantenha exclusivamente um agente escritor por branch
- Encerre o fluxo de execução estritamente com a geração da working tree alterada e notifique o status `READY_FOR_REVIEW`
- Risco amarelo/vermelho: execução incremental com diff por etapa
- Preserve decisões canônicas — ajustes retroativos para justificar código já escrito são proibidos
- Utilize obrigatoriamente fixtures sintéticas aprovadas em ambiente de desenvolvimento
- Baseie verificações em evidências — não em confiança na IA

### Validação Shift-Left obrigatória antes de propor alteração

```text
typecheck → lint → format → test → build
```

Falha em qualquer etapa não é entregue ao Reviewer.

---

## Fase 4 — Assurance independente (Reviewer)

**Quem:** Codex\
**Independência:** Reviewer avalia o artefato produzido pelo Executor, sem acesso ao raciocínio interno

| Veredicto | Significado | Próximo passo |
| :--- | :--- | :--- |
| `PASS` | Implementação correta, invariantes respeitadas, evidência suficiente | Davi integra |
| `FAIL` | Violação de invariante, regressão, risco não coberto | Executor corrige, novo ciclo |
| `HUMAN_DECISION_REQUIRED` | Ambiguidade semântica ou decisão de domínio além do escopo do agente | Davi decide, registra, ciclo reinicia |

---

## Fase 5 — Integração e release

**Quem:** exclusivamente Davi

```text
PASS do Reviewer
       ↓
Davi revisa diff final
       ↓
commit + push + merge para main
       ↓
Cloudflare Pages (deploy automático)
       ↓
CEPRAEA BEACH PRO em runtime
```

Nenhum agente participa desta fase. O runtime resultante é determinístico e independente de IA — Claude Code e Codex pertencem ao processo de engenharia, não ao produto.

---

## Separação fundamental

```text
┌─────────────────────────────────────────────┐
│  PROCESSO DE ENGENHARIA                     │
│  Claude Code + Codex + Davi                 │
│  (agêntico, governado, rastreável)          │
├─────────────────────────────────────────────┤
│  PRODUTO EM RUNTIME                         │
│  PWA offline-first                          │
│  (determinístico, sem IA, domain-driven)    │
└─────────────────────────────────────────────┘
```

Essa separação não é uma convenção — é a propriedade arquitetural central do domínio. Qualquer decisão que confunda os dois planos é contexto inválido.
