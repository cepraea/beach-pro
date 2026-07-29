# Modelo de dicionário de erros e procedimentos

## 1. Finalidade

Este modelo registra diagnósticos reproduzíveis sem autorizar operações destrutivas por padrão.

## 2. Regras de execução

> **Segurança:** diagnósticos de leitura podem ser executados automaticamente dentro do escopo autorizado. Alterações persistentes, exclusões, redefinições e ações externas são `ASK`.

Para cada erro:

1. confirme o identificador observado;
2. execute somente o diagnóstico documentado;
3. escolha uma resolução compatível com a matriz de permissões;
4. valide o resultado;
5. pare se a causa observada não corresponder às causas documentadas.

## 3. Modelo de entrada

````markdown
## ERR-001 — <PREENCHER: identificador observável>

### Sintoma

```text
<PREENCHER: mensagem ou padrão de erro>
```

### Causas possíveis

- <PREENCHER: causa que ainda precisa ser confirmada>
- <PREENCHER: causa alternativa>

### Diagnóstico — ALWAYS

1. Execute `<PREENCHER: comando somente leitura>`.
2. Compare a saída com `<PREENCHER: condição observável>`.

### Resolução

#### Alternativa segura — ALWAYS

1. <PREENCHER: ação reversível dentro do escopo>
2. Execute `<PREENCHER: validação>`.

#### Alternativa sensível — ASK

Solicite autorização antes de:

- <PREENCHER: alteração persistente ou destrutiva>;
- <PREENCHER: ação com impacto externo>.

### Resultado esperado

- **Comando:** `<PREENCHER: validação final>`
- **Código de saída:** `0`
- **Evidência:** <PREENCHER: saída observável>

### Condição de parada

Interrompa se <PREENCHER: condição que invalida o procedimento>.
````

## 4. Exemplo

### ERR-REDIS-001 — Conexão recusada no Redis local

#### Sintoma

```text
Error: connect ECONNREFUSED 127.0.0.1:6379
```

#### Causas possíveis

- o serviço local não está em execução;
- a aplicação está usando host ou porta diferentes do ambiente local;
- o serviço está iniciando, mas ainda não está saudável.

#### Diagnóstico — ALWAYS

1. Execute `docker compose ps redis`.
2. Execute `docker compose logs --tail=50 redis`.
3. Leia a configuração local sem exibir valores secretos.

#### Resolução — ALWAYS

Se o projeto documentar `redis` como serviço local autorizado, execute:

```bash
docker compose up -d redis
docker compose ps redis
```

Aguarde a condição de saúde declarada pelo serviço. Não use uma espera fixa como substituta da verificação.

#### Resolução alternativa — ASK

Solicite autorização antes de editar arquivos de ambiente ou recriar volumes.

#### Resultado esperado

- o serviço aparece como saudável;
- o teste de conexão do projeto retorna código `0`;
- nenhuma credencial é impressa no terminal.

#### Condição de parada

Interrompa se o ambiente for compartilhado, remoto ou de produção.

## 5. Operações não autorizadas como autocorreção

Não apresente os comandos abaixo como ações automáticas:

```text
prisma migrate reset --force
docker compose down --volumes
DROP DATABASE
git clean -fd
```

Quando necessários, eles devem estar classificados como `ASK`, ter alvo confirmado e possuir plano de recuperação.
