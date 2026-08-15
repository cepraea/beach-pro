# Backlog técnico mínimo — M0/M1

## Convenções

- Estados: `DONE`, `READY`, `BLOCKED`.
- Dados permitidos: somente `SYNTHETIC`.
- Fonte: DEC-019, MVP-01 e esqueleto de MVP-09.
- Um item bloqueado não autoriza contornar a restrição com dados ou ambiente
  reais.

## M0 — Preparação

| ID | Ação | Rastreabilidade | Aceite | Estado |
| --- | --- | --- | --- | --- |
| M0-01 | Auditar workspace e ferramentas | DEC-019 §11 | Relatório registra fatos, riscos e contenções | DONE |
| M0-02 | Isolar aplicação em repositório próprio | DEC-019 §9.1 | Git local existe somente dentro do projeto | DONE |
| M0-03 | Inicializar React, TypeScript e Vite | DEC-015; DEC-019 §11 | Aplicação compila e abre | DONE |
| M0-04 | Configurar PWA instalável e online | DEC-019 Done 13–14 | Manifesto e service worker de rede entram no build sem cache de dados | DONE |
| M0-05 | Fixar dependências e lockfile | DEC-019 §9.1 | Versões exatas e `package-lock.json` versionável | DONE |
| M0-06 | Configurar qualidade automatizada | DEC-019 §11 | Lint, tipos, testes e build executados por um comando | DONE |
| M0-07 | Criar barreira de dados sintéticos | DEC-019 §10 | Build falha para perfil real ou segredo privilegiado | DONE |
| M0-08 | Preparar CI sem segredos | DEC-019 §11 | Workflow usa `npm ci` e perfil sintético | DONE |
| M0-09 | Preparar Supabase versionado | DEC-015; MVP-01 | Configuração e primeira migração existem | DONE |
| M0-10 | Subir Supabase local e testar migração | MVP-01 | Reset local conclui e schema é consultável | BLOCKED |
| M0-11 | Criar projeto GitHub privado | DEC-015 | Remote privado configurado sem gasto automático | BLOCKED |
| M0-12 | Criar ambiente Cloudflare sintético | DEC-015 | Deploy marcado como sintético, sem dados reais | BLOCKED |

### Dependências dos bloqueios de M0

- `M0-10`: instalar Docker/Podman ou autorizar projeto Supabase remoto
  exclusivamente sintético.
- `M0-11`: conexão/autenticação GitHub e confirmação do repositório remoto.
- `M0-12`: conexão/autenticação Cloudflare; somente depois do build local
  validado.

## M1 — Fundação e identidade

| ID | Ação | RFs | Aceite | Estado |
| --- | --- | --- | --- | --- |
| M1-01 | Modelar perfis `DAVI` e `ATLETA` | RF-037, RF-038 | Enum e tabela versionados | DONE |
| M1-02 | Impor marcador sintético no banco | RF-048 | Banco rejeita `is_synthetic = false` | READY |
| M1-03 | Fechar cadastro público | RF-041 | Configuração local desabilita signup | DONE |
| M1-04 | Configurar Auth por convite/administração | RF-037, RF-040, RF-041 | Conta não nasce por cadastro público | BLOCKED |
| M1-05 | Configurar MFA TOTP privilegiada | RF-039 | Davi sintético autentica com segundo fator | BLOCKED |
| M1-06 | Implementar leitura do próprio perfil | RF-037, RF-045 | Atleta acessa somente o próprio perfil | READY |
| M1-07 | Implementar visão administrativa de Davi | RF-038, RF-045 | Davi sintético lê perfis autorizados | READY |
| M1-08 | Impedir acesso anônimo | RF-037, RF-041 | Requisições `anon` não leem tabelas | READY |
| M1-09 | Criar esqueleto append-only de auditoria | RF-033, RF-036 | Tabela e políticas de leitura versionadas | DONE |
| M1-10 | Criar personas sintéticas | DEC-019 Done 1 | Davi e ao menos cinco atletas fictícias | BLOCKED |
| M1-11 | Testar isolamento negativo | RF-045; DEC-019 Done 11 | Atleta A não acessa dados da atleta B | BLOCKED |
| M1-12 | Verificar ausência de chave privilegiada | RF-040, RF-048 | Scanner e teste de runtime passam | DONE |

### Gate de conclusão de M1

M1 somente poderá ser declarado concluído quando `M1-02` a `M1-12` estiverem
comprovados em banco executável, incluindo duas sessões sintéticas distintas,
MFA de Davi e testes negativos de RLS. A existência do SQL não equivale à prova
de execução.
