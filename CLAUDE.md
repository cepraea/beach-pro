# Regras do agente

## Forma de trabalho

- Leia os arquivos relevantes antes de editar.
- Faça alterações mínimas e focadas.
- Preserve a arquitetura e os padrões existentes.
- Não invente resultados de testes, comandos ou validações.
- Informe claramente qualquer verificação que não tenha sido executada.

## Segurança

- Nunca exponha, copie ou registre segredos.
- Não altere `.env`, credenciais, chaves privadas ou diretórios de produção.
- Não execute push, deploy, publicação, migração de banco ou instalação de dependências sem aprovação explícita.
- Não use comandos destrutivos ou irreversíveis.

## Qualidade

- Use os scripts de lint, typecheck e testes já definidos no projeto.
- Corrija a causa raiz, evitando desabilitar verificações.
- Não reduza cobertura nem remova testes para fazer a suíte passar.
- Mantenha compatibilidade, salvo instrução contrária.

## Tradução controlada

- Toda tradução normativa deve seguir `docs/governance/policies/tradutor.md`, `docs/governance/policies/politica-traducao-controlada.md` e `docs/registry/registro-traducao.yaml`.
- Tradução, correção, portabilidade e atualização factual são operações separadas.
- Ambiguidade, divergência contratual, fonte sem SHA-256, revisão bilíngue ausente ou aprovação humana ausente resultam em `BLOCKED`.
- Nenhuma versão traduzida pode ser promovida ou substituir a origem fora do corte atômico aprovado.
