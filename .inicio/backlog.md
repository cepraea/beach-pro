# Backlog técnico M0/M1

Auditoria do workspace e produção do backlog técnico mínimo de M0/M1; depois inicializar a aplicação React + TypeScript + Vite e o ambiente exclusivamente sintético

A base M0/M1 foi criada em cepraea-beach-pro.

Principais entregas:

- Auditoria do workspace (`docs/auditoria-workspace-m0.md`)
- Backlog técnico M0/M1 (`docs/backlog-m0-m1.md`)
- React + TypeScript + Vite
- PWA instalável e estritamente online, sem cache de dados
- repositório Git local isolado
- dependências com versões exatas e lockfile
- CI, lint, typecheck, testes e build
- guarda que bloqueia perfil diferente de `SYNTHETIC`
- rejeição de chaves Supabase privilegiadas no frontend
- Supabase inicializado com cadastro público fechado e MFA TOTP habilitada
- primeira migração de identidade e RLS (`supabase/migrations/20260726081207_m1_identity_foundation.sql`)
- esqueleto de auditoria append-only
- interface marcada visivelmente como ambiente sintético

Validação:

```text
Fronteira sintética: OK
Lint: pass
TypeScript: pass
Testes: 6/6
Build: pass
npm audit: 0 vulnerabilidades
```

A revisão React também foi aplicada: componentes separados, exports nomeados, HTML semântico e propriedades tipadas.

Estado real:

- M0 local: iniciado e funcional.
- M1 estrutural: schema e políticas versionados.
- M1 executável: ainda não concluído.
- Dados reais: bloqueados.
- GitHub, Cloudflare e Supabase remoto: não conectados.
- Commit inicial: não realizado porque não há identidade Git configurada.

O bloqueio atual é a ausência de Docker/Podman. O Supabase local precisa de runtime compatível com Docker, conforme a [documentação oficial](https://supabase.com/docs/guides/local-development). A alternativa é criar/conectar um projeto Supabase remoto exclusivamente sintético.

Depois de resolver isso, as próximas ações são:

1. aplicar a migração em banco sintético;
2. criar Davi e atletas fictícias;
3. testar convite, MFA e sessões;
4. executar testes negativos de RLS;
5. concluir o gate de M1.
