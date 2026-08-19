# CEPRAEA BEACH PRO

> Fundação do MVP autorizado pela DEC-019. Este repositório aceita exclusivamente dados sintéticos e não está autorizado para migração real, piloto ou produção.

## Stack

- React 19 + TypeScript + Vite;
- PWA estática e online;
- Supabase PostgreSQL/Auth/Data API/RLS;
- Cloudflare Pages como destino futuro;
- npm com dependências fixadas;
- Vitest, Testing Library e Oxlint;
- manifesto e service worker mínimos, sem cache offline de dados.

## Início local do frontend

```bash
npm ci
cp .env.example .env
npm run dev
```

Sem URL e chave do Supabase, a interface abre em modo seguro desconectado.

## Validação

```bash
npm run validate
```

O comando verifica a fronteira sintética, lint, tipos, testes e build.

## Supabase

A configuração está em `supabase/`. Para executar localmente é necessário um
runtime compatível com Docker.

```bash
npx supabase start
npx supabase db reset
```

Não conecte este repositório a um projeto com dados reais.
O frontend aceita somente uma chave publicável; chaves secretas ou de serviço são proibidas.

## Estado

- M0: fundação local iniciada; serviços externos ainda não conectados.
- M1: schema e políticas iniciais versionados; Auth/RLS ainda precisam ser
  executados e comprovados em Supabase sintético.
