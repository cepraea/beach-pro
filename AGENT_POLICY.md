# CEPRAEA BEACH PRO - Política comum dos agentes

## Autoridade

- Davi decide domínio, Git, GitHub e promoção.
- O agente nunca executa commit, push, merge, rebase, deploy ou secrets.
- Se a branch for main/master, pare antes de qualquer escrita.

## Antes de escrever: classificação proporcional

1. Classifique a tarefa como verde, amarelo, vermelho ou vermelho crítico.
2. Produza proposta formal antes da escrita se qualquer condição for verdadeira:
   - houver mais de um arquivo alvo;
   - o risco for amarelo, vermelho ou vermelho crítico;
   - Davi solicitar explicitamente a proposta.
3. A proposta formal pode ser omitida somente quando todas forem verdadeiras:
   - existe exatamente um arquivo alvo;
   - o risco é verde;
   - a mudança é local e reversível;
   - não envolve dependência, auth, RLS, MFA, dados, decisão canônica ou plano de controle.
4. Se uma tarefa verde passar a exigir segundo alvo ou adquirir natureza não verde, pare antes da
   expansão, produza a proposta formal e obtenha o checkpoint correspondente.
5. Em caso de dúvida sobre a classificação, trate como amarelo.

## Papéis de arquivo

Quando houver proposta formal, cada arquivo é referência, alvo, somente leitura ou proibido.
Não mude o papel nem expanda o conjunto de alvos sem explicar e, quando a classificação exigir,
obter checkpoint de Davi.

## Autoria de documentação

Antes de criar ou alterar arquivos Markdown, leia e siga
`docs/standards/DOCUMENTATION_STYLE_GUIDE.md`.

Esse arquivo é a fonte canônica das regras de autoria de documentação Markdown. O guia não altera
os limites de autoridade, os papéis de arquivo ou os requisitos de aprovação desta política.

## Risco

- Verde: mudança local e reversível, sem auth, dados ou plano de controle.
- Amarelo: múltiplos módulos, semântica canônica ou expansão.
- Vermelho: dependência, migration, RLS, MFA, auth, auditoria ou privacidade.
- Vermelho crítico: .devcontainer, CI, hooks, managed settings, secrets, deploy ou infraestrutura.
  Exige fluxo separado e aprovação específica.

## Execução

- Um agente escritor por branch.
- Somente fixtures sintéticas aprovadas.
- Amarelo/vermelho: execução incremental e diff por etapa.
- Não altere decisão canônica para justificar retroativamente o código.
- Rode critérios e apresente evidências, falhas e limitações.
- Advisor, npm audit e telemetria local são detectores, não garantias.

## Encerramento

Entregue resumo, arquivos, testes/resultados, riscos residuais e itens para Davi revisar.
Se houver proposta formal, não a marque como aprovada. Se a proposta não tiver sido exigida,
informe explicitamente: `proposta não exigida — risco verde, um alvo`.
