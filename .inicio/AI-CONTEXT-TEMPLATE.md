# Modelo de contexto operacional para agentes de IA

## 1. Instruções de uso

Substitua os valores entre `<PREENCHER: ...>` antes de usar este modelo. Remova seções que não se aplicam e não mantenha permissões contraditórias.

O modelo organiza instruções; controles técnicos do ambiente continuam sendo necessários.

## 2. Modelo

````markdown
# Diretrizes do projeto: <PREENCHER: nome>

## 1. Identificação

- **Finalidade:** <PREENCHER: resultado esperado destas diretrizes>
- **Responsável:** <PREENCHER: função ou equipe>
- **Versão:** <PREENCHER: versão>
- **Vigência:** <PREENCHER: data ISO 8601>

## 2. Contexto confirmado

<contexto>
- Produto: <PREENCHER>
- Linguagens e versões: <PREENCHER>
- Frameworks e versões: <PREENCHER>
- Fonte canônica de requisitos: <PREENCHER>
- Comandos de validação existentes: <PREENCHER>
</contexto>

## 3. Escopo

### 3.1 Escrita permitida

- `<PREENCHER: caminho relativo>`

### 3.2 Somente leitura

- `<PREENCHER: caminho relativo>`

### 3.3 Fora do escopo

- `<PREENCHER: caminho relativo ou sistema externo>`

## 4. Matriz de permissões

| Categoria | Ação | Alvo | Condição |
| --- | --- | --- | --- |
| **ALWAYS** | Ler arquivos relacionados antes de editar. | Escopo da tarefa. | Sem alterar estado. |
| **ALWAYS** | Executar validações não destrutivas. | Arquivos modificados. | Antes da conclusão. |
| **ASK** | Instalar ou atualizar dependências. | Manifestos e lockfiles. | Exige autorização. |
| **ASK** | Alterar esquema ou dados persistentes. | Banco local ou remoto. | Exige autorização e plano de recuperação. |
| **NEVER** | Expor ou registrar credenciais. | Código, logs e documentação. | Sem exceção neste contexto. |
| **NEVER** | Alterar produção. | Serviços e dados de produção. | Fora do escopo. |

## 5. Padrões técnicos

<regras>
- <PREENCHER: regra observável e seu escopo>
- <PREENCHER: regra observável e seu escopo>
</regras>

## 6. Estado atual

- <PREENCHER: fato confirmado>
- <PREENCHER: fato confirmado>

## 7. Estado desejado

- <PREENCHER: resultado observável>
- <PREENCHER: resultado observável>

## 8. Critérios de aceitação

<criterios_aceitacao>

### AC-001 — <PREENCHER: nome>

- **Condição:** <PREENCHER>
- **Verificação:** `<PREENCHER: comando não destrutivo>`
- **Resultado esperado:** <PREENCHER: saída e código de retorno>

</criterios_aceitacao>

## 9. Fluxo de execução

1. Confirmar o escopo e o estado atual.
2. Ler os arquivos relacionados.
3. Implementar somente o estado desejado.
4. Executar as verificações aplicáveis.
5. Registrar resultados, limitações e arquivos alterados.

## 10. Condições de parada

O agente deve interromper a execução e solicitar orientação quando:

- uma ação necessária estiver classificada como `ASK`;
- houver conflito entre fontes autorizadas;
- a validação exigir credenciais indisponíveis;
- a única solução identificada violar uma regra `NEVER`;
- o estado real divergir materialmente do estado documentado.
````

## 3. Verificação do modelo preenchido

Antes de ativar as diretrizes:

1. remova todos os marcadores `<PREENCHER>`;
2. confirme que os caminhos existem;
3. execute os comandos de validação manualmente;
4. revise a matriz com o responsável;
5. passe o arquivo pelo validador estrutural.