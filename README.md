# CEPRAEA Beach Pro

Aplicação web progressiva (PWA) para gestão de atletas e treinadores da equipe de handebol de areia do CEPRAEA.

Permite gerenciar treinos, presenças, avaliações, desempenho, jogos e informações da equipe. Projetada para uso em dispositivos móveis, inclusive em condições de conexão instável.

## Pré-requisitos

- Node.js 24.14.1 (consulte `.nvmrc`)
- npm 11.11.0

## Instalação

```bash
git clone https://github.com/cepraea/beach-pro
cd cepraea-beach-pro
npm ci
cp .env.example .env.local
```

Preencha as variáveis em `.env.local` com os dados do projeto Supabase (veja a seção [Variáveis de ambiente](#variáveis-de-ambiente)).

## Scripts disponíveis

| Script | Descrição |
| --- | --- |
| `npm run assets:pwa` | Regenera os ícones oficiais da PWA |
| `npm run dev` | Inicia o servidor de desenvolvimento em `localhost:5173` |
| `npm run build` | Gera o build de produção em `dist/` |
| `npm run preview` | Visualiza o build em `localhost:4173` |
| `npm run lint` | Executa o ESLint |
| `npm run lint:md` | Audita o acervo Markdown governado |
| `npm run lint:md:vscode` | Valida a especificação do ambiente e seu relatório |
| `npm run quality:workspace` | Verifica consistência entre as configurações |
| `npm run format` | Formata o código com Prettier |
| `npm run typecheck` | Verifica os tipos TypeScript sem gerar arquivos |
| `npm run test` | Executa os testes com Vitest |
| `npm run validate` | Executa todas as portas de qualidade e o build |

Execute `npm run validate` antes de publicar qualquer versão.

## Estrutura de pastas

```text
src/
├── features/
│   ├── atletas/        # Cadastro e perfil de atletas
│   ├── treinadores/    # Cadastro e perfil de treinadores
│   ├── treinos/        # Planejamento e registro de treinos
│   ├── jogos/          # Registro e acompanhamento de jogos
│   ├── presencas/      # Controle de presença
│   └── avaliacoes/     # Avaliações de desempenho
└── shared/
    ├── components/     # Componentes reutilizáveis
    ├── hooks/          # Hooks React compartilhados
    └── lib/            # Utilitários e configurações (ex: cliente Supabase)
```

Cada feature segue a estrutura: `components/`, `pages/`, `services/`, `schemas/`, `types/`, `tests/`.

## Como executar no VS Code

1. Abra o arquivo `cepraea-beach-pro.code-workspace`.
2. Instale as extensões recomendadas quando solicitado.
3. Use a tarefa **CEPRAEA: iniciar desenvolvimento** (`Ctrl+Shift+P` → `Tasks: Run Task`).
4. Para depurar, pressione `F5`; o VS Code abre o Chrome e conecta o depurador.

## Variáveis de ambiente

Copie `.env.example` para `.env.local` e preencha:

| Variável | Descrição |
| --- | --- |
| `VITE_APP_NAME` | Nome exibido na aplicação |
| `VITE_SUPABASE_URL` | URL do projeto Supabase |
| `VITE_SUPABASE_ANON_KEY` | Chave pública (anon) do Supabase |
| `VITE_ENABLE_OFFLINE` | Habilita recursos offline (`true`/`false`) |

O arquivo `.env.local` não deve ser versionado. Nunca insira a service key ou outros segredos em variáveis `VITE_*`.
