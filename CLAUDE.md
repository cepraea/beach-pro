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
