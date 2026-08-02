# AGENTS.md

## Projeto

CEPRAEA BEACH PRO, PWA React e TypeScript para gestão da equipe
de handebol de praia do CEPRAEA.

## Ambiente

- Node.js 24.14.1
- npm 11.11.0
- Instalação: `npm ci`

## Leitura inicial

1. `README.md`
2. `package.json`
3. documentação aplicável em `docs/`
4. arquivos da feature afetada em `src/features/`

Para qualquer tradução de documentação técnica ou normativa, ler também
`.inicio/tradutor.md` antes de iniciar a operação.

## Norma de tradução

- `.inicio/tradutor.md` é a autoridade operacional para traduções de linguagem
  natural de artefatos técnicos ou normativos neste repositório.
- Perfis de tradução podem restringir a norma, mas não podem relaxar seus gates.
- Evidências de execução não substituem a norma nem o perfil aplicável.
- Em caso de ambiguidade, divergência contratual ou gate sem evidência, a
  tradução deve permanecer `BLOCKED`.
- Mudanças na norma exigem análise de impacto, validação e aprovação explícita
  antes de serem tratadas como vigentes.

## Validação obrigatória

Execute `npm run validate` após qualquer alteração de código ou configuração.

## Regras de mudança

- Não editar diretamente a branch `main`.
- Trabalhar em branch específica e entregar por pull request.
- Não alterar arquivos fora do escopo solicitado.
- Não versionar `.env.local` nem segredos.
- Não declarar a tarefa concluída sem apresentar o resultado da validação.
