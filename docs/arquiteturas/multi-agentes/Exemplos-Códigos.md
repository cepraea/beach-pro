# Exemplos

Exemplos de código do mundo real que demonstram os quatro princípios. Cada exemplo mostra o que os LLMs geralmente fazem de errado e como corrigir isso.

---

## 1. Pense Antes de Codificar

### Exemplo 1: Suposições Ocultas

**Solicitação do Usuário:** "Adicione uma funcionalidade para exportar dados de usuários"

**❌ O que os LLMs fazem (Suposições incorretas)**

```python
def export_users(format='json'):
"""Exporta todos os usuários para um arquivo."""
users = User.query.all()

if format == 'json':
with open('users.json', 'w') as f:
json.dump([u.to_dict() for u in users], f)
elif format == 'csv':
with open('users.csv', 'w') as f:
writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
writer.writeheader()
writer.writerows([u.to_dict() for u in users])

return f"Exportados {len(users)} usuários"
```

**Problemas:**
- Supôs que deveria exportar TODOS os usuários (e quanto à paginação? privacidade?)
- Supôs o local do arquivo sem perguntar
- Supôs quais campos incluir
- Supôs os nomes dos campos do CSV sem verificar a estrutura real dos dados

**✅ O que deveria acontecer (Explicitar suposições)**

```
Antes de implementar, preciso esclarecer:

1. **Escopo**: Exportar todos os usuários ou um subconjunto filtrado? (implicações de privacidade)
2. **Formato**: Você mencionou "exportar" – quis dizer:
- Download do arquivo no navegador?
- Tarefa em segundo plano com notificação por e-mail?
- Endpoint de API retornando os dados?
3. **Campos**: Quais campos do usuário? (alguns podem ser sensíveis)
4. **Volume**: Quantos usuários normalmente? (afeta a abordagem)

Abordagem mais simples: Adicionar um endpoint de API que retorna JSON paginado.
Seriam necessárias mais informações para exportações baseadas em arquivos.

Qual é a sua preferência?
```

### Exemplo 2: Múltiplas Interpretações

**Solicitação do Usuário:** "Torne a busca mais rápida"

**❌ O que as LLMs fazem (decidem silenciosamente)**

```python
# Adiciona cache, índices de banco de dados e processamento assíncrono
# sem perguntar qual tipo de "rapidez" é importante
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
# ... 200 linhas de código de otimização
```

**✅ O que deveria acontecer**

```
"Tornar a busca mais rápida" pode significar:

1. **Tempo de resposta menor** (< 100ms em vez de 500ms)
- Adicionar índices ao banco de dados
- Fazer cache de consultas frequentes
- Esforço estimado: 2 horas

2. **Suportar mais buscas simultâneas** (vazão/throughput)
- Adicionar async/await
- Pool de conexões
- Esforço estimado: 4 horas

3. **Maior velocidade percebida** (UX)
- Exibir resultados parciais imediatamente
- Carregamento progressivo
- Esforço estimado: 3 horas

A busca atual leva ~500ms para consultas típicas.
Qual aspecto é mais importante para o seu caso de uso?
```

---

## 2. Simplicidade em Primeiro Lugar

### Exemplo 1: Abstração Excessiva

**Solicitação do Usuário:** "Adicione uma função para calcular desconto"

**❌ O que as LLMs fazem (Complexidade excessiva)**

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol, Union
from dataclasses import dataclass

class DiscountStrategy(ABC):
@abstractmethod
def calculate(self, amount: float) -> float:
pass

class PercentageDiscount(DiscountStrategy):
def __init__(self, percentage: float):
self.percentage = percentage

def calculate(self, amount: float) -> float:
return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
def __init__(self, fixed_amount: float):
self.fixed_amount = fixed_amount

def calculate(self, amount: float) -> float:
return min(self.fixed_amount, amount)

@dataclass
class DiscountConfig:
strategy: DiscountStrategy
min_purchase: float = 0.0
max_discount: float = float('inf')

class DiscountCalculator:
def __init__(self, config: DiscountConfig):
self.config = config

def apply_discount(self, amount: float) -> float:
if amount < self.config.min_purchase:
return 0
discount = self.config.strategy.calculate(amount)
return min(discount, self.config.max_discount)

# O uso requer mais de 30 linhas de configuração para um cálculo simples
```

**✅ O que deveria acontecer (Simples)**

```python
def calculate_discount(amount: float, percent: float) -> float:
"""Calcula o valor do desconto. percent deve estar entre 0 e 100."""
return amount * (percent / 100)

# Uso
discount = calculate_discount(100.0, 10.0)  # $10 de desconto
```

**Quando adicionar complexidade:** Apenas quando você realmente precisar de múltiplos tipos de desconto. Se esse requisito surgir mais tarde, faça a refatoração nesse momento.

### Exemplo 2: Funcionalidades Especulativas

**Solicitação do usuário:** "Salvar preferências do usuário no banco de dados"

**❌ O que os LLMs fazem (Funcionalidades desnecessárias)**

```python
class PreferenceManager:
def __init__(self, db, cache=None, validator=None):
self.db = db
self.cache = cache or InMemoryCache()
self.validator = validator or DefaultValidator()

def save(self, user_id: int, prefs: dict,
merge: bool = True,
validate: bool = True,
notify: bool = False) -> bool:
"""Salva preferências com mesclagem, validação e notificações opcionais."""

if validate:
errors = self.validator.validate(prefs)
if errors:
raise ValidationError(errors)

existing = self.get(user_id) if merge else {}

if merge:
existing.update(prefs)
prefs = existing

self.db.execute(
"UPDATE users SET preferences = ? WHERE id = ?",
(json.dumps(prefs), user_id)
)

if self.cache:
self.cache.set(f"prefs:{user_id}", prefs)

if notify:
self.notify_preference_change(user_id, prefs)

return True

def notify_preference_change(self, user_id: int, prefs: dict):
# Mais 30 linhas para uma funcionalidade que ninguém pediu
pass
```

**✅ O que deveria acontecer (Apenas o que foi pedido)**

```python
def save_preferences(db, user_id: int, preferences: dict):
"""Salva as preferências do usuário no banco de dados."""
db.execute(
"UPDATE users SET preferences = ? WHERE id = ?",
(json.dumps(preferences), user_id)
)
```

**Adicione mais tarde, se necessário:** Cache (quando o desempenho importa), validação (quando surgem dados inválidos), mesclagem (quando o requisito surgir).

---

## 3. Alterações Cirúrgicas

### Exemplo 1: Refatoração Pontual (*Drive-by Refactoring*)

**Solicitação do Usuário:** "Corrija o bug em que e-mails vazios travam o validador"

**❌ O que as LLMs fazem (Excesso de alterações)**

```diff
def validate_user(user_data):
-     # Verifica o formato do e-mail
-     if not user_data.get('email'):
+     """Valida os dados do usuário."""
+     email = user_data.get('email', '').strip()
+
+     # Valida o e-mail
+     if not email:
raise ValueError("E-mail obrigatório")
-
-     # Validação básica de e-mail
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
raise ValueError("Invalid email")

-     # Check username
-     if not user_data.get('username'):
+     # Validate username
+     username = user_data.get('username', '').strip()
+     if not username:
raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")
+     if not username.isalnum():
+         raise ValueError("Username must be alphanumeric")

return True
```

**Problemas:**
- Validação de e-mail "melhorada" além da correção do bug
- Adição de validação de nome de usuário não solicitada
- Alteração de comentários
- Adição de docstring

**✅ O que deveria acontecer (Alteração cirúrgica)**

```diff
def validate_user(user_data):
# Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
raise ValueError("Email required")

# Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
raise ValueError("Invalid email")

# Check username
if not user_data.get('username'):
raise ValueError("Username required")

return True
```

**Alterado apenas:** As linhas específicas que corrigem o tratamento de e-mail vazio. ### Exemplo 2: Desvio de Estilo (Style Drift)

**Solicitação do Usuário:** "Adicione registro de logs à função de upload"

**❌ O que as LLMs fazem (Reformatação completa)**

```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
+     logger.info(f"Uploading {file_path} to {destination}")
+
try:
-         with open(file_path, 'rb') as f:
-             data = f.read()
-
-         response = requests.post(destination, files={'file': data})
-
-         if response.status_code == 200:
-             return True
-         else:
-             return False
+         with open(file_path, "rb") as f:
+             data = f.read()
+         response = requests.post(destination, files={"file": data})
+         success = response.status_code == 200
+
+         if success:
+             logger.info(f"Upload successful: {file_path}")
+         else:
+             logger.error(f"Upload failed: {file_path}, status={response.status_code}")
+
+         return success
except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f"Upload error for {file_path}: {e}")
return False
```

**Problemas:**
- Alterou o estilo de aspas (de '' para "")
- Adicionou *type hints* (dicas de tipo) não solicitados
- Adicionou *docstring*
- Reformatou espaços em branco
- Alterou a lógica de retorno booleano

**✅ O que deveria acontecer (Manter o estilo existente)**

```diff
+ import logging
+
+ logger = logging.getLogger(__name__)
+
def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
try:
with open(file_path, 'rb') as f:
data = f.read()

response = requests.post(destination, files={'file': data})

if response.status_code == 200:
+             logger.info(f'Upload bem-sucedido: {file_path}')
return True
else:
+             logger.error(f'Falha no upload: {file_path}, status
s={response.status_code}')
return False
except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
return False
```

**Correspondência:** Aspas simples, sem *type hints*, padrão booleano existente, estilo de espaçamento.

---

## 4. Execução Orientada a Objetivos

### Exemplo 1: Vago vs. Verificável

**Solicitação do Usuário:** "Corrija o sistema de autenticação"

**❌ O que as LLMs fazem (Abordagem vaga)**

```
Vou corrigir o sistema de autenticação:
1. Revisando o código
2. Identificando problemas
3. Fazendo melhorias
4. Testando as alterações

[Prossegue fazendo alterações sem critérios de sucesso claros]
```

**✅ O que deveria acontecer (Objetivos verificáveis)**

```
Para "corrigir a autenticação", preciso definir critérios de sucesso.
Qual problema específico estamos resolvendo?

Se o problema for "usuários permanecem logados após a alteração de senha":

Plano:
1. Escrever teste: Alterar senha → verificar se a sessão antiga foi invalidada
Verificação: Teste falha (reproduz o bug)

2. Implementar: Invalidar sessões ao alterar a senha
Verificação: Teste passa

3. Verificar casos de borda: Múltiplas sessões ativas, alterações simultâneas
Verificação: Testes adicionais passam

4. Verificar ausência de regressão: Testes de autenticação existentes continuam passando
Verificação: Suíte de testes completa aprovada (verde)

Cobertura de testes atual para autenticação: [mostra a cobertura]
Qual é o problema específico de autenticação que você está observando?
```

### Exemplo 2: Abordagem em várias etapas com verificação

**Solicitação do usuário:** "Adicionar limitação de taxa (rate limiting) à API"

**❌ O que os LLMs fazem (tudo de uma vez)**

```python
# Implementa limitação de taxa completa com Redis, múltiplas estratégias,
# sistema de configuração e monitoramento em um único commit de 300 linhas
# Sem etapas de verificação claras
```

**✅ O que deveria acontecer (incremental com verificação)**

```
Plano para limitação de taxa:

1. Adicionar limitação de taxa básica em memória (endpoint único)
Verificação:
- Teste: 100 requisições → as primeiras 10 têm sucesso, as demais recebem erro 429
- Manual: executar curl no endpoint 11 vezes, observar erro de limite de taxa

2. Extrair para middleware (aplicar a todos os endpoints)
Verificação:
- Teste: Limites de taxa aplicados a /users e /posts
- Testes de endpoints existentes continuam passando

3. Adicionar backend Redis (para múltiplos servidores)
Verificação:
- Teste: Limite de taxa persiste após reinicializações da aplicação
- Teste: Duas instâncias da aplicação compartilham o contador de limite de taxa

4. Adicionar configuração (limites por endpoint)
Verificação:
- Teste: /search permite 10/min, /users permite 100/min
- Arquivo de configuração analisado corretamente

Cada etapa é verificável e implantável de forma independente.
Começar pela etapa 1?
``` ```

### Exemplo 3: Verificação com Foco em Testes (Test-First)

**Solicitação do Usuário:** "A ordenação falha quando há pontuações duplicadas"

**❌ O que os LLMs fazem (Corrigem sem reproduzir)**

```python
# Altera imediatamente a lógica de ordenação sem confirmar o bug
def sort_scores(scores):
return sorted(scores, key=lambda x: (-x['score'], x['name']))
```

**✅ O que deveria acontecer (Reproduzir primeiro)**

```python
# 1. Primeiro, escreva um teste que reproduza o problema
def test_sort_with_duplicate_scores():
"""Testa a ordenação quando múltiplos itens têm a mesma pontuação."""
scores = [
{'name': 'Alice', 'score': 100},
{'name': 'Bob', 'score': 100},
{'name': 'Charlie', 'score': 90},
]

result = sort_scores(scores)

# O bug: a ordem é não determinística para duplicatas
# Execute este teste várias vezes; o resultado deve ser consistente
assert result[0]['score'] == 100
assert result[1]['score'] == 100
assert result[2]['score'] == 90

# Verificação: Execute o teste 10 vezes → falha devido à ordem inconsistente

# 2. Agora, corrija usando uma ordenação estável
def sort_scores(scores):
"""Ordena por pontuação (decrescente) e depois por nome (crescente) em caso de empate."""
return sorted(scores, key=lambda x: (-x['score'], x['name']))

# Verificação: O teste passa consistentemente
```

---

## Resumo de Antipadrões

| Princípio | Antipadrão | Correção |
|-----------|-------------|-----|
| Pense antes de codificar | Assume silenciosamente formato de arquivo, campos ou escopo | Liste suposições explicitamente, peça esclarecimentos |
| Simplicidade em primeiro lugar | Padrão Strategy para cálculo de desconto único | Uma única função até que a complexidade seja realmente necessária |
| Alterações cirúrgicas | Reformata aspas, adiciona *type hints* ao corrigir um bug | Altere apenas as linhas que corrigem o problema relatado |
| Foco no objetivo | "Vou revisar e melhorar o código" | "Escreva teste para o bug X → faça passar → verifique se não há regressões" | ## Ponto-chave

Os exemplos "excessivamente complexos" não estão necessariamente errados — eles seguem padrões de projeto e melhores práticas. O problema é o **momento**: eles adicionam complexidade antes de ela ser necessária, o que:

- Torna o código mais difícil de entender
- Introduz mais bugs
- Leva mais tempo para implementar
- Dificulta os testes

As versões "simples":
- São mais fáceis de entender
- São mais rápidas de implementar
- São mais fáceis de testar
- Podem ser refatoradas mais tarde, quando a complexidade for realmente necessária

**Bom código é aquele que resolve o problema de hoje de forma simples, e não o problema de amanhã de forma prematura.**
