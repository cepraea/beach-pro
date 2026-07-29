# Validação de documentos e fronteiras de escopo

## 1. Validador estrutural

O script `scripts/validate_ai_docs.py` verifica:

- quantidade de títulos de nível 1;
- saltos na hierarquia de títulos;
- cercas não fechadas;
- blocos sem identificador de linguagem;
- itens de lista vazios;
- espaços ao final das linhas;
- marcadores conversacionais;
- comandos destrutivos apresentados fora de contexto seguro.

Execute:

```bash
python3 scripts/validate_ai_docs.py MD-FORMAT.md AI-CONTEXT-TEMPLATE.md
```

O código de saída é `0` quando todos os arquivos passam e `1` quando existe ao menos um erro.

O arquivo `MD-FORMAT-LEGACY.md` é histórico e não faz parte da validação canônica.

## 2. Verificador de escopo Git

O script `scripts/check-ai-scope.sh` verifica alterações locais contra um ou mais prefixos permitidos e procura padrões proibidos nos arquivos modificados.

Exemplo:

```bash
scripts/check-ai-scope.sh src/modules/users/ src/shared/types/
```

Sem argumentos, o prefixo permitido é `src/modules/`.

O script:

- não modifica arquivos;
- considera alterações preparadas, não preparadas e arquivos não rastreados;
- trata nomes de arquivos com espaços;
- retorna código `1` para violações;
- retorna código `2` quando não está em um repositório Git.

## 3. Integração

Antes de configurar um hook ou pipeline:

1. execute os scripts diretamente;
2. confirme os prefixos permitidos;
3. registre exceções de forma explícita;
4. faça o hook chamar o script em sua localização estável;
5. mantenha operações destrutivas fora dos validadores.

Exemplo de hook:

```bash
#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate_ai_docs.py MD-FORMAT.md AI-CONTEXT-TEMPLATE.md
scripts/check-ai-scope.sh src/modules/
```

Copiar esse conteúdo para `.git/hooks/pre-commit` é uma alteração de configuração local e deve ser feita somente quando autorizada.

