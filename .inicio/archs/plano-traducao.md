# Plano de correção da norma de tradução

>O [tradutor.md](/home/davis/projetos/cepraea-beach-pro/.inicio/tradutor.md) exige correções normativas, estruturais e de versionamento. Os cinco comentários inline representam pendências válidas e bloqueantes.

## Ações necessárias e critérios de aceitação

| ID | Prioridade | Ação | Critério de aceitação |
| --- | :---: | --- | --- |
| COR-01 | Bloqueante | Separar a norma genérica do perfil específico de `agent-list.md` | A norma contém regras reutilizáveis; hash, 12 agentes, 31 `file_type` e demais números ficam em um perfil ou evidência de execução |
| COR-02 | Bloqueante | Definir a autoridade normativa do documento | `tradutor.md` está versionado e referenciado por uma autoridade do repositório; a declaração interna “NORMA OBRIGATÓRIA” não é a única fonte de autoridade |
| COR-03 | Bloqueante | Criar o dicionário fechado dos campos da `REG-TRAD-001` | Todo campo possui ID, nome canônico, tipo, cardinalidade, obrigatoriedade, valores permitidos, origem, consumidor e invariantes |
| COR-04 | Bloqueante | Definir formalmente o que é um segmento | A norma determina como segmentos começam e terminam por meio de AST Markdown, sem depender de interpretação livre |
| COR-05 | Bloqueante | Criar uma tabela determinística de classificação | Cada tipo de nó ou contexto possui exatamente uma classe, uma regra de decisão e um código de justificativa |
| COR-06 | Bloqueante | Fechar o vocabulário de classes e campos | Somente enums cadastrados podem ser usados; classe ou campo desconhecido produz `BLOCKED` |
| COR-07 | Bloqueante | Corrigir semanticamente as regras `REG-TRAD-001.1–001.5` | As cinco regras usam os mesmos campos, enums, estados e códigos definidos no dicionário |
| COR-08 | Bloqueante | Garantir a imutabilidade da origem | Placeholders são inseridos apenas em uma cópia de trabalho; o blob original fixado por hash nunca é modificado |
| COR-09 | Bloqueante | Definir uma máquina de estados da tradução | Estados, transições, pré-condições, ações e gates estão explicitamente enumerados |
| COR-10 | Bloqueante | Separar estados de códigos de erro | Condições como placeholder ausente tornam-se erros `E_*`, não valores genéricos de `status` |
| COR-11 | Bloqueante | Definir formalmente posição e ordem | Posição significa endereço lógico na AST, não offset absoluto após a tradução |
| COR-12 | Bloqueante | Especificar placeholder e checksum | Formato, unicidade, geração, encoding, bytes usados no hash, detecção de colisão e restauração são determinísticos |
| COR-13 | Bloqueante | Especificar o schema do manifesto | Manifesto possui schema fechado e validação automática; campo adicional ou ausente bloqueia a operação |
| COR-14 | Bloqueante | Tornar verificável a equivalência proposicional | Método de extração, assinatura semântica, cobertura, revisor e tratamento de divergência estão definidos |
| COR-15 | Alta | Integrar “Classificação total”, “Precedência” e `REG-TRAD-001` | Não há regras duplicadas ou conflitantes; as subseções usam uma única taxonomia |
| COR-16 | Alta | Corrigir o tratamento de `AMBIGUOUS` | `AMBIGUOUS` é resultado terminal de ausência de classificação segura, e não apenas o último item de uma precedência |
| COR-17 | Alta | Definir regras para segmentos mistos | Links, código inline, tabelas e Mermaid possuem regras explícitas para separar conteúdo protegido de texto traduzível |
| COR-18 | Alta | Substituir o diagrama HTML inválido | A estratégia é representada com Mermaid ou bloco `text`, sem tags HTML malformadas |
| COR-19 | Alta | Corrigir as fences de código | O pseudocódigo de `TRADUZIR(S)` usa `text`; somente exemplos reais de Markdown usam `markdown` |
| COR-20 | Alta | Corrigir sumário e hierarquia | Sumário automático corresponde exatamente aos headings, preserva a formatação nativa do gerador e possui exceção de lint estritamente localizada |
| COR-21 | Alta | Criar validação automatizada da norma | Schema, classes, placeholders, manifesto, estados e projeções contratuais possuem testes positivos e negativos |
| COR-22 | Alta | Resolver os comentários inline | Cada comentário é substituído pela definição solicitada e removido somente depois de seu critério ser atendido |
| COR-23 | Alta | Validar a fonte canônica única | Existe apenas um `agent-list.md` ativo; a versão japonesa fica fora do worktree e sua origem é comprovada por Git ou hash |
| COR-24 | Obrigatória | Executar validações e versionar | Markdownlint sem erros, testes da norma aprovados, `npm run validate` apresentado e entrega por branch/PR |

## Contratos individuais das ações

As listas de verificação abaixo têm funções distintas:

- **execução:** confirma que a mudança foi produzida;
- **validação:** confirma que o comportamento está correto;
- **evidência e encerramento:** confirma que o resultado é auditável e pode ser aceito.

### COR-01 — Separar norma genérica e perfil de `agent-list.md`

**Escopo positivo:** mover hashes, contagens, nomes e invariantes exclusivos de
`agent-list.md` para um perfil ou evidência de execução, mantendo na norma apenas
regras reutilizáveis. **Escopo negativo:** alterar os contratos traduzidos ou
eliminar a rastreabilidade da execução já realizada.

**Contexto válido:** conteúdo aplicável somente a um artefato está misturado ao
núcleo geral. **Contexto inválido:** mover regras universais apenas porque foram
exemplificadas com `agent-list.md`.

**Critérios de aceitação individuais:**

- o núcleo não depende de quantidades ou hashes de um documento específico;
- o perfil preserva 100% das restrições específicas removidas do núcleo;
- norma, perfil e evidência possuem referências unidirecionais e sem ciclo.

**Funcionando corretamente:** uma nova tradução pode aplicar a norma sem herdar
12 agentes, 31 `file_type` ou 23 arestas, enquanto o perfil de `agent-list.md`
continua verificável.

**Riscos e edge cases:** perda de requisito durante a extração; duplicação entre
perfil e evidência; referência circular. **Correções e soluções:** criar uma
matriz origem-destino para cada trecho, definir uma única autoridade por dado e
validar links nos dois sentidos.

**Verificação e evidências:** busca automatizada por hash e constantes específicas
no núcleo, matriz de migração com cobertura de 100% e relatório de links.

**Checklist de execução:**

- [x] Classificar cada trecho como regra geral, perfil ou evidência.
- [x] Mover o conteúdo sem alterar sua obrigação semântica.
- [x] Atualizar referências entre os artefatos.

**Saída esperada:** núcleo normativo genérico e perfil/evidência específico de
`agent-list.md` claramente identificados.

**Checklist de validação:**

- [x] Confirmar ausência de constantes específicas no núcleo.
- [x] Confirmar presença de todas as constantes no perfil ou evidência.

**Checklist de evidência e encerramento:**

- [x] Anexar matriz origem-destino e resultado da busca automatizada.
- [x] Registrar `PASS` somente com cobertura de 100%.

### COR-02 — Definir a autoridade normativa

**Escopo positivo:** registrar `tradutor.md` no mecanismo de governança e fazer
documentos de autoridade apontarem para ele. **Escopo negativo:** declarar
autoridade apenas no próprio documento ou alterar a hierarquia global sem
aprovação.

**Contexto válido:** documento aprovado, versionado e referenciado por uma fonte
superior. **Contexto inválido:** arquivo não rastreado, cópia local ou referência
apenas informativa.

**Critérios de aceitação individuais:** o arquivo está rastreado; existe uma
referência normativa externa; status e procedimento de mudança estão definidos;
não há outra norma concorrente.

**Funcionando corretamente:** um consumidor consegue descobrir a norma a partir
da governança do repositório e determinar qual versão prevalece.

**Riscos e edge cases:** autodeclaração circular, duas normas ativas ou registro
apontando para caminho antigo. **Correções e soluções:** autoridade externa,
busca de concorrentes e validação de links canônicos.

**Verificação e evidências:** `git ls-files`, busca de referências normativas,
checagem de links e registro da decisão de autoridade.

**Checklist de execução:**

- [x] Selecionar a autoridade documental aplicável.
- [x] Registrar `tradutor.md` e sua política de revisão.
- [x] Remover ou rebaixar declarações concorrentes.

**Saída esperada:** norma rastreada e alcançável a partir da governança.

**Checklist de validação:**

- [x] Confirmar exatamente uma norma ativa.
- [x] Confirmar que todas as referências resolvem para o caminho canônico.

**Checklist de evidência e encerramento:**

- [x] Registrar saída de `git ls-files` e busca de concorrentes.
- [x] Anexar aprovação da autoridade normativa.

### COR-03 — Criar o dicionário fechado de campos

**Escopo positivo:** definir cada campo da `REG-TRAD-001`, seu ID, tipo,
cardinalidade, obrigatoriedade, domínio, origem, consumidor e invariantes.
**Escopo negativo:** adicionar campos ad hoc durante uma execução ou misturar
campos do manifesto com estados e erros.

**Contexto válido:** schema fechado e versionado. **Contexto inválido:** exemplos
livres tratados como definição ou campos inferidos pelo agente.

**Critérios de aceitação individuais:** todos os campos usados pela norma estão
no dicionário; IDs são únicos; tipos e valores são verificáveis; campo desconhecido
gera `E_UNKNOWN_FIELD` e `BLOCKED`.

**Funcionando corretamente:** toda entrada pode ser validada sem interpretação
livre e nenhum agente consegue inventar um campo silenciosamente.

**Riscos e edge cases:** sinônimos para o mesmo campo, campo condicional sem
gatilho e evolução incompatível. **Correções e soluções:** nomes canônicos,
condições formais, versão de schema e política de migração.

**Verificação e evidências:** validação do schema, teste com campo desconhecido,
teste de IDs duplicados e relatório de cobertura dos campos citados na norma.

**Checklist de execução:**

- [x] Inventariar todos os campos existentes.
- [x] Completar as propriedades obrigatórias de cada campo.
- [x] Definir versionamento e regra de extensão.

**Saída esperada:** tabela normativa e schema fechado do manifesto.

**Checklist de validação:**

- [ ] Validar exemplo válido e exemplos inválidos.
- [ ] Confirmar cobertura de 100% dos campos referenciados.

**Checklist de evidência e encerramento:**

- [x] Publicar relatório do auditor estrutural do dicionário.
- [x] Registrar casos negativos `E_UNKNOWN_FIELD` e ID duplicado.

### COR-04 — Definir formalmente um segmento

**Escopo positivo:** especificar segmentação por AST Markdown, spans de bytes e
endereços lógicos. **Escopo negativo:** segmentar por intuição, tradução prévia
ou regex isolada que ignore a estrutura.

**Contexto válido:** origem imutável e parser com versão conhecida. **Contexto
inválido:** Markdown inválido não diagnosticado ou origem alterada após o parse.

**Critérios de aceitação individuais:** todos os bytes relevantes pertencem a
um segmento; spans não se sobrepõem; cada segmento possui `segment_id` e
`source_ast_path`; parse impossível produz `E_PARSE_FAILED`.

**Funcionando corretamente:** duas execuções sobre o mesmo blob produzem os
mesmos segmentos, IDs e endereços lógicos.

**Riscos e edge cases:** Unicode multibyte, CRLF, HTML embutido, tabelas, código
aninhado e Markdown malformado. **Correções e soluções:** offsets em bytes do
blob, encoding fixo, fixtures para cada nó e bloqueio em parse ambíguo.

**Verificação e evidências:** teste de determinismo repetido, mapa de cobertura
dos bytes e fixtures com Unicode, CRLF, HTML, tabelas e Mermaid.

**Checklist de execução:**

- [x] Selecionar e fixar parser e versão.
- [x] Definir algoritmo de IDs, spans e AST paths.
- [ ] Criar fixtures de nós simples e mistos.

**Saída esperada:** especificação de segmentação determinística.

**Checklist de validação:**

- [ ] Comparar duas execuções sobre o mesmo hash.
- [ ] Confirmar zero lacunas e zero sobreposições indevidas.

**Checklist de evidência e encerramento:**

- [ ] Arquivar mapas de segmentos das fixtures.
- [ ] Registrar testes de parse inválido e Unicode.

### COR-05 — Criar a tabela determinística de classificação

**Escopo positivo:** mapear tipo de nó, contexto e parte do conteúdo para uma
classe e um `classification_rule_id`. **Escopo negativo:** classificar por
preferência linguística ou inferência não registrada.

**Contexto válido:** segmento produzido pela COR-04. **Contexto inválido:** span
sem AST path ou regra fora da tabela fechada.

**Critérios de aceitação individuais:** toda regra tem ID único, predicado,
classe e prioridade; todo segmento recebe exatamente uma classe; ausência ou
empate não resolvido produz `AMBIGUOUS` e `BLOCKED`.

**Funcionando corretamente:** a mesma entrada sempre recebe a mesma classe e
regra justificadora.

**Riscos e edge cases:** regras sobrepostas, contexto misto e fallback permissivo.
**Correções e soluções:** predicados mutuamente exclusivos, precedência explícita,
divisão de spans e fallback fechado.

**Verificação e evidências:** testes de decisão para cada regra, casos de empate,
relatório de cobertura e snapshot das classificações.

**Checklist de execução:**

- [x] Enumerar contextos e partes classificáveis.
- [x] Definir IDs, predicados, prioridades e classes.
- [x] Cadastrar fallback `AMBIGUOUS`.

**Saída esperada:** tabela fechada de regras de classificação.

**Checklist de validação:**

- [ ] Testar pelo menos um caso positivo e negativo por regra.
- [ ] Confirmar exatamente uma decisão por segmento.

**Checklist de evidência e encerramento:**

- [x] Publicar matriz normativa regra-entrada-resultado.
- [ ] Registrar cobertura de regras e casos ambíguos.

### COR-06 — Fechar o vocabulário de classes e campos

**Escopo positivo:** consolidar enums canônicos e proibir extensões implícitas.
**Escopo negativo:** permitir aliases, grafias alternativas ou valores livres.

**Contexto válido:** evolução feita por revisão normativa e nova versão.
**Contexto inválido:** agente cria uma classe para concluir uma execução.

**Critérios de aceitação individuais:** enums estão em uma única definição;
aliases inexistem ou são explicitamente migrados; valores desconhecidos geram
`E_UNKNOWN_CLASS`, `E_UNKNOWN_FIELD` ou `E_UNKNOWN_CLASSIFICATION_RULE`.

**Funcionando corretamente:** somente valores cadastrados atravessam o gate de
schema.

**Riscos e edge cases:** diferença de caixa, hífen versus underscore e versão
antiga. **Correções e soluções:** comparação exata, sem normalização silenciosa,
e tabela de migração versionada.

**Verificação e evidências:** testes com caixa, grafia, alias e versão inválidos.

**Checklist de execução:**

- [x] Publicar enums canônicos.
- [x] Proibir sinônimos e aliases não normativos.
- [x] Definir procedimento de mudança de versão.

**Saída esperada:** vocabulário fechado e versionado.

**Checklist de validação:**

- [x] Auditar todos os valores canônicos declarados.
- [x] Registrar rejeição obrigatória de valores desconhecidos e aliases.

**Checklist de evidência e encerramento:**

- [x] Anexar resultados dos casos negativos normativos.
- [x] Registrar a versão dos enums usada.

### COR-07 — Corrigir `REG-TRAD-001.1–001.5`

**Escopo positivo:** reescrever as cinco regras com campos, classes, estados e
erros canônicos. **Escopo negativo:** mudar o objetivo de congelar contratos ou
introduzir exceções não modeladas.

**Contexto válido:** COR-03 a COR-06 aprovadas. **Contexto inválido:** reescrita
antes do fechamento da taxonomia.

**Critérios de aceitação individuais:** condições e efeitos são testáveis; nomes
existem no dicionário; a origem não é modificada; cada falha possui código; não
há contradição entre as cinco regras.

**Funcionando corretamente:** uma implementação consegue executar as regras sem
inventar decisões intermediárias.

**Riscos e edge cases:** condição circular, estado impossível e dupla restauração.
**Correções e soluções:** tabela de decisão, pré/pós-condições e testes de
transição negativa.

**Verificação e evidências:** revisão semântica das regras, tabela de rastreio
regra-campo-estado-erro e testes de cenários.

**Checklist de execução:**

- [ ] Reescrever cada regra em formato se-então inequívoco.
- [ ] Referenciar apenas IDs e enums normativos.
- [ ] Eliminar termos não definidos.

**Saída esperada:** cinco regras coerentes e implementáveis.

**Checklist de validação:**

- [ ] Executar cenários de sucesso e falha por regra.
- [ ] Confirmar ausência de ciclos e estados inalcançáveis.

**Checklist de evidência e encerramento:**

- [ ] Anexar matriz de rastreabilidade das cinco regras.
- [ ] Registrar aprovação semântica individual.

### COR-08 — Garantir a imutabilidade da origem

**Escopo positivo:** fixar hash, restringir a origem a leitura e criar cópia de
trabalho para placeholders. **Escopo negativo:** substituir texto no arquivo ou
blob original.

**Contexto válido:** origem disponível por Git ou snapshot imutável. **Contexto
inválido:** origem sem hash ou sobrescrita durante a execução.

**Critérios de aceitação individuais:** hash anterior e posterior é idêntico;
placeholders existem somente na cópia; alteração da origem gera
`E_SOURCE_NOT_FIXED` ou bloqueio equivalente.

**Funcionando corretamente:** a origem pode ser reaberta e reproduz exatamente
o baseline usado na tradução.

**Riscos e edge cases:** arquivo não rastreado, symlink, alteração concorrente e
normalização automática de linha. **Correções e soluções:** snapshot por bytes,
resolução segura de caminho, lock/checksum e proibição de formatador na origem.

**Verificação e evidências:** hashes antes/depois, identificação do blob e diff
vazio da origem.

**Checklist de execução:**

- [ ] Resolver caminho e fixar SHA-256 da origem.
- [ ] Criar cópia de trabalho identificada.
- [ ] Bloquear escrita na origem durante a execução.

**Saída esperada:** baseline imutável e cópia de trabalho rastreável.

**Checklist de validação:**

- [ ] Recalcular e comparar o hash da origem.
- [ ] Confirmar placeholders ausentes no baseline.

**Checklist de evidência e encerramento:**

- [ ] Registrar hashes, caminho e método de snapshot.
- [ ] Anexar diff vazio ou identificação do blob Git.

### COR-09 — Definir a máquina de estados

**Escopo positivo:** especificar estados, transições, entradas, saídas e gates.
**Escopo negativo:** usar estados como mensagens de erro ou permitir saltos.

**Contexto válido:** uma execução identificada por `translation_run_id`.
**Contexto inválido:** ações fora de uma execução ou retomada sem estado persistido.

**Critérios de aceitação individuais:** estado inicial e terminais são únicos;
transições permitidas são fechadas; pré/pós-condições existem; erro conduz a
`BLOCKED`; nenhuma transição obrigatória pode ser pulada.

**Funcionando corretamente:** dado estado e evento, existe no máximo uma próxima
transição válida.

**Riscos e edge cases:** retomada após falha, repetição idempotente e estado
inalcançável. **Correções e soluções:** persistir estado, definir idempotência,
rollback e análise automática de alcançabilidade.

**Verificação e evidências:** diagrama, tabela de transição e testes de todos os
pares estado-evento.

**Checklist de execução:**

- [ ] Enumerar estados e eventos.
- [ ] Definir transições e gates.
- [ ] Definir retomada, repetição e bloqueio.

**Saída esperada:** máquina de estados normativa.

**Checklist de validação:**

- [ ] Detectar estados inalcançáveis e transições ambíguas.
- [ ] Testar fluxo feliz, bloqueio e retomada.

**Checklist de evidência e encerramento:**

- [ ] Anexar grafo e matriz de transições coberta.
- [ ] Registrar resultados dos testes de idempotência.

### COR-10 — Separar estados e códigos de erro

**Escopo positivo:** definir catálogo `E_*`, condição de disparo e efeito.
**Escopo negativo:** representar erro como estado normal ou usar texto livre.

**Contexto válido:** violação detectada por regra ou gate. **Contexto inválido:**
erro inferido sem evidência associada.

**Critérios de aceitação individuais:** cada violação possui código único;
códigos não aparecem no enum de estados; todo erro registra localização e leva
a `BLOCKED` quando especificado.

**Funcionando corretamente:** consumidores distinguem posição do workflow de
causa da falha.

**Riscos e edge cases:** múltiplos erros, causa encadeada e erro desconhecido.
**Correções e soluções:** lista ordenada, `caused_by`, código genérico controlado
somente para falha interna e prioridade de reporte.

**Verificação e evidências:** testes de cada código, múltiplos erros e validação
de que nenhum código consta nos estados.

**Checklist de execução:**

- [ ] Definir códigos, gatilhos e severidade.
- [ ] Associar erros às regras e gates.
- [ ] Definir serialização e ordenação.

**Saída esperada:** catálogo fechado de erros separado do workflow.

**Checklist de validação:**

- [ ] Disparar cada erro com fixture mínima.
- [ ] Confirmar estado final correto para erros simultâneos.

**Checklist de evidência e encerramento:**

- [ ] Publicar matriz erro-fixture-regra.
- [ ] Arquivar saídas estruturadas dos testes.

### COR-11 — Definir posição e ordem

**Escopo positivo:** usar AST path e ordem lógica entre segmentos irmãos.
**Escopo negativo:** exigir offsets idênticos no destino traduzido.

**Contexto válido:** comparação entre projeções estruturais da mesma origem.
**Contexto inválido:** documentos estruturalmente diferentes autorizados por
outra mudança normativa.

**Critérios de aceitação individuais:** formato de AST path é normativo; ordem
significativa está declarada; deslocamento textual permitido não gera falso
positivo; movimentação lógica gera `E_LOGICAL_POSITION_CHANGED`.

**Funcionando corretamente:** texto pode crescer ou encolher sem alterar a
identidade lógica do segmento.

**Riscos e edge cases:** tabelas reformatadas, nós iguais e listas renumeradas.
**Correções e soluções:** IDs estáveis, chave composta por ancestral/tipo/índice
e normalização estrutural antes da comparação.

**Verificação e evidências:** fixtures com expansão textual, movimentação real,
linhas formatadas e elementos duplicados.

**Checklist de execução:**

- [ ] Definir gramática do AST path.
- [ ] Definir quando a ordem é significativa.
- [ ] Integrar a comparação ao manifesto.

**Saída esperada:** regra inequívoca de posição e ordem lógica.

**Checklist de validação:**

- [ ] Aceitar mudança apenas de comprimento textual.
- [ ] Rejeitar troca de linha, owner, fase ou aresta lógica.

**Checklist de evidência e encerramento:**

- [ ] Anexar pares antes/depois e resultados esperados.
- [ ] Registrar teste de elementos estruturalmente idênticos.

### COR-12 — Especificar placeholder e checksum

**Escopo positivo:** definir formato, geração, unicidade, bytes, encoding,
checksum, colisão e restauração. **Escopo negativo:** hashes de texto normalizado
ou placeholders escolhidos manualmente.

**Contexto válido:** segmento `PROTECTED_EXACT` registrado. **Contexto inválido:**
conteúdo traduzível ou origem sem bytes fixados.

**Critérios de aceitação individuais:** placeholder não colide com a origem;
SHA-256 usa bytes originais; restauração é byte a byte; ausência, duplicidade ou
colisão dispara erro específico.

**Funcionando corretamente:** congelar e restaurar produz exatamente os mesmos
bytes protegidos e a mesma multiplicidade.

**Riscos e edge cases:** placeholder já presente, Unicode, duas ocorrências
iguais e restauração fora de ordem. **Correções e soluções:** namespace por run,
ID por ocorrência, hash dos bytes e verificação de sequência.

**Verificação e evidências:** teste round-trip, colisão intencional, Unicode e
ocorrências repetidas.

**Checklist de execução:**

- [ ] Definir gramática e algoritmo do placeholder.
- [ ] Definir encoding e cálculo de checksum.
- [ ] Implementar detecção de colisão e multiplicidade.

**Saída esperada:** protocolo determinístico de congelamento/restauração.

**Checklist de validação:**

- [ ] Executar round-trip byte a byte.
- [ ] Rejeitar placeholder ausente, duplicado e colidente.

**Checklist de evidência e encerramento:**

- [ ] Registrar hashes antes/depois e fixtures.
- [ ] Anexar relatório de multiplicidade e ordem.

### COR-13 — Especificar o schema do manifesto

**Escopo positivo:** materializar o dicionário em schema validável e versionado.
**Escopo negativo:** aceitar propriedades adicionais ou coerção silenciosa.

**Contexto válido:** manifesto de uma execução e versão de schema conhecida.
**Contexto inválido:** documento parcial tratado como manifesto aprovado.

**Critérios de aceitação individuais:** campos obrigatórios e condicionais são
validados; propriedades extras são rejeitadas; relações e unicidade têm checks;
versão incompatível bloqueia.

**Funcionando corretamente:** qualquer consumidor obtém o mesmo resultado de
validação para o mesmo manifesto.

**Riscos e edge cases:** referências quebradas, grandes manifestos e migração de
versão. **Correções e soluções:** validação referencial em segunda etapa, limites
documentados e migrador explícito.

**Verificação e evidências:** suíte de exemplos válidos/inválidos, benchmark de
tamanho esperado e teste de versão.

**Checklist de execução:**

- [ ] Escolher formato e versão do schema.
- [ ] Codificar tipos, enums e condicionais.
- [ ] Implementar validações relacionais complementares.

**Saída esperada:** schema e conjunto de fixtures do manifesto.

**Checklist de validação:**

- [ ] Aprovar manifestos válidos mínimos e completos.
- [ ] Rejeitar ausência, excesso, tipo e referência inválidos.

**Checklist de evidência e encerramento:**

- [ ] Publicar relatório completo da suíte de schema.
- [ ] Registrar versão e hash do schema usado.

### COR-14 — Verificar equivalência proposicional

**Escopo positivo:** definir extração e comparação de sujeito, predicado, objeto,
modalidade, polaridade, quantificador, condição, tempo e referências. **Escopo
negativo:** usar tradução reversa como única prova ou aceitar similaridade geral.

**Contexto válido:** prosa traduzível com origem e destino rastreados. **Contexto
inválido:** contrato protegido ou proposição sem unidade de origem.

**Critérios de aceitação individuais:** toda proposição de origem possui destino;
nenhuma proposição nova fica sem origem; assinaturas preservam todos os campos;
divergência bloqueia e exige revisão bilíngue.

**Funcionando corretamente:** mudanças de estilo são aceitas, mas obrigação,
negação, quantidade, condição ou temporalidade alteradas são rejeitadas.

**Riscos e edge cases:** uma frase com várias proposições, sujeito elíptico,
negação indireta e ambiguidade cultural. **Correções e soluções:** decomposição
atômica, herança explícita de sujeito, glossário e revisão humana independente.

**Verificação e evidências:** matriz proposição a proposição, cobertura de 100%,
fixtures com alteração de modalidade e parecer bilíngue.

**Checklist de execução:**

- [ ] Definir unidade proposicional e assinatura.
- [ ] Mapear origem-destino e relações muitos-para-muitos.
- [ ] Definir workflow de divergência e revisão.

**Saída esperada:** método e matriz de equivalência proposicional.

**Checklist de validação:**

- [ ] Detectar perda, adição e mudança de modalidade.
- [ ] Confirmar cobertura bidirecional de 100%.

**Checklist de evidência e encerramento:**

- [ ] Anexar matriz e parecer do revisor bilíngue.
- [ ] Registrar todas as divergências e resoluções.

### COR-15 — Integrar taxonomia, precedência e regra principal

**Escopo positivo:** consolidar definições duplicadas em uma única cadeia
normativa. **Escopo negativo:** remover detalhes sem destino ou manter duas
definições autoritativas.

**Contexto válido:** COR-03 a COR-14 estabilizadas. **Contexto inválido:** fusão
antes de fechar campos e estados.

**Critérios de aceitação individuais:** cada conceito tem uma definição; seções
referenciam a definição canônica; não há contradições ou ciclos; exemplos não
criam regras novas.

**Funcionando corretamente:** alterar uma definição exige editar um único ponto.

**Riscos e edge cases:** perda durante deduplicação e referência órfã.
**Correções e soluções:** matriz de duplicidades, escolha de autoridade e busca
automática de termos antigos.

**Verificação e evidências:** relatório de duplicidades antes/depois, link check e
revisão de cobertura semântica.

**Checklist de execução:**

- [ ] Inventariar definições repetidas e conflitantes.
- [ ] Eleger definição canônica e substituir duplicatas por referências.
- [ ] Atualizar sumário e links internos.

**Saída esperada:** norma coesa com taxonomia única.

**Checklist de validação:**

- [ ] Confirmar uma definição por conceito.
- [ ] Confirmar ausência de referências órfãs e termos obsoletos.

**Checklist de evidência e encerramento:**

- [ ] Anexar matriz de consolidação.
- [ ] Registrar revisão sem perda de requisitos.

### COR-16 — Corrigir `AMBIGUOUS`

**Escopo positivo:** definir `AMBIGUOUS` como resultado terminal de classificação
insegura. **Escopo negativo:** usá-lo como fallback permissivo ou classe que pode
ser traduzida.

**Contexto válido:** nenhuma regra decide ou há conflito não resolvido. **Contexto
inválido:** regra específica válida já determinou a classe.

**Critérios de aceitação individuais:** `AMBIGUOUS` sempre gera código de erro e
`BLOCKED`; não entra na tradução; resolução exige regra normativa ou decisão
registrada, nunca override silencioso.

**Funcionando corretamente:** conteúdo incerto não atravessa o gate de
classificação.

**Riscos e edge cases:** excesso de falsos bloqueios e override manual.
**Correções e soluções:** fixtures para ampliar regras de modo controlado e
procedimento formal de escalonamento.

**Verificação e evidências:** teste sem regra, teste de conflito e auditoria de
que nenhum `AMBIGUOUS` aparece em execução aprovada.

**Checklist de execução:**

- [ ] Remover `AMBIGUOUS` da precedência comum.
- [ ] Definir gatilhos, erro e escalonamento.
- [ ] Proibir tradução e override direto.

**Saída esperada:** política fail-closed inequívoca.

**Checklist de validação:**

- [ ] Bloquear caso sem regra e caso conflitante.
- [ ] Confirmar zero ambiguidades em manifesto aprovado.

**Checklist de evidência e encerramento:**

- [ ] Anexar logs dos testes de bloqueio.
- [ ] Registrar decisões que originaram novas regras.

### COR-17 — Definir segmentos mistos

**Escopo positivo:** decompor links, código, tabelas, HTML e Mermaid em spans com
classes distintas. **Escopo negativo:** proteger ou traduzir o nó misto inteiro
sem análise de suas partes.

**Contexto válido:** parser reconhece a estrutura e os limites internos.
**Contexto inválido:** sintaxe quebrada ou extensão desconhecida.

**Critérios de aceitação individuais:** spans cobrem o nó sem sobreposição;
destinos/IDs permanecem exatos; rótulos humanos autorizados são traduzíveis;
estrutura desconhecida bloqueia.

**Funcionando corretamente:** `[texto](destino)` traduz somente `texto`, e Mermaid
traduz rótulos sem mudar IDs, arestas ou estilos.

**Riscos e edge cases:** escapes, links de referência, pipes em tabelas, HTML
aninhado e `<br/>` em Mermaid. **Correções e soluções:** regras por subtipo de nó
e fixtures específicas para cada sintaxe.

**Verificação e evidências:** snapshots de AST e round-trip de cada fixture mista.

**Checklist de execução:**

- [ ] Enumerar estruturas mistas suportadas.
- [ ] Definir decomposição e classe de cada parte.
- [ ] Bloquear extensões não suportadas.

**Saída esperada:** tabela completa de decomposição de segmentos mistos.

**Checklist de validação:**

- [ ] Testar links, tabelas, código, HTML e Mermaid.
- [ ] Confirmar identidade byte a byte das partes protegidas.

**Checklist de evidência e encerramento:**

- [ ] Arquivar AST e saídas normalizadas das fixtures.
- [ ] Registrar cobertura de todos os subtipos suportados.

### COR-18 — Substituir o diagrama HTML inválido

**Escopo positivo:** representar o fluxo com Mermaid ou bloco `text` válido.
**Escopo negativo:** alterar a sequência origem → cópia/tradução → destino ou
introduzir dependência visual não suportada.

**Contexto válido:** renderizadores Markdown do repositório. **Contexto inválido:**
HTML dependente de navegador ou tags obsoletas.

**Critérios de aceitação individuais:** zero tags malformadas; fluxo semântico
idêntico; renderização legível em GitHub e editor; parser aceita o bloco.

**Funcionando corretamente:** a figura comunica uma única fonte canônica e a
preservação da origem sem depender de HTML.

**Riscos e edge cases:** Mermaid indisponível e texto ilegível em modo bruto.
**Correções e soluções:** preferir diagrama simples e acrescentar descrição
textual normativa independente da renderização.

**Verificação e evidências:** Markdownlint, parser Mermaid quando aplicável e
captura/renderização revisada.

**Checklist de execução:**

- [ ] Remover o bloco HTML e tags de apresentação.
- [ ] Inserir representação Markdown suportada.
- [ ] Preservar a explicação textual do fluxo.

**Saída esperada:** diagrama válido e semanticamente equivalente.

**Checklist de validação:**

- [ ] Validar sintaxe e leitura em texto bruto.
- [ ] Confirmar os mesmos nós, direção e condição de fonte única.

**Checklist de evidência e encerramento:**

- [ ] Anexar saída do parser ou renderização.
- [ ] Registrar zero HTML malformado na busca.

### COR-19 — Corrigir fences de código

**Escopo positivo:** atribuir linguagem correspondente ao conteúdo de cada fence.
**Escopo negativo:** modificar o conteúdo normativo do pseudocódigo.

**Contexto válido:** blocos cercados reconhecidos pelo Markdown. **Contexto
inválido:** conteúdo misto sem linguagem predominante.

**Critérios de aceitação individuais:** pseudocódigo usa `text`; exemplos reais
usam sua linguagem; toda fence possui identificador permitido e fechamento.

**Funcionando corretamente:** renderizador e agentes não interpretam pseudocódigo
como Markdown executável.

**Riscos e edge cases:** fence dentro de exemplo e linguagem não permitida.
**Correções e soluções:** escapar exemplos aninhados e usar lista de linguagens da
configuração Markdownlint.

**Verificação e evidências:** Markdownlint e inventário de fences com linguagem.

**Checklist de execução:**

- [ ] Inventariar todas as fences.
- [ ] Corrigir `markdown` para `text` no pseudocódigo.
- [ ] Validar fechamentos e exemplos aninhados.

**Saída esperada:** blocos cercados corretamente tipados.

**Checklist de validação:**

- [ ] Executar MD040, MD046 e MD048.
- [ ] Revisar visualmente blocos aninhados.

**Checklist de evidência e encerramento:**

- [ ] Anexar saída do Markdownlint.
- [ ] Registrar inventário final de fences.

### COR-20 — Corrigir sumário e hierarquia

**Escopo positivo:** identificar e fixar o gerador automático; sincronizar itens,
anchors e níveis com os headings; preservar exatamente a indentação nativa
produzida pelo gerador; delimitar uma exceção `MD007` somente ao bloco gerado.
**Escopo negativo:** reindentar manualmente o sumário para obedecer à regra geral
de listas; editar manualmente o conteúdo gerado; desabilitar `MD007` para o
arquivo inteiro ou para o repositório; renomear conceitos normativos somente
para ajustar anchors.

**Contexto válido:** headings finais estabilizados e sumário mantido por gerador
automático identificado. **Contexto inválido:** lista mantida manualmente ou
geração executada antes da consolidação estrutural.

**Critérios de aceitação individuais:** cada heading elegível aparece uma vez no
sumário; anchors resolvem; níveis refletem a hierarquia; a indentação é idêntica
à saída nativa do gerador, ainda que difira da regra geral de listas; a exceção
`MD007` começa imediatamente antes e termina imediatamente depois do bloco
gerado; não existe ocorrência de `MD007` fora desse bloco; duas gerações
consecutivas, sem mudança de headings, produzem zero diff na segunda execução.

**Funcionando corretamente:** o comando documentado regenera o sumário sem
intervenção manual; todo item navega para a seção correta; nenhuma seção elegível
fica órfã; a segunda regeneração é idempotente; a regra geral de indentação
continua ativa fora do sumário.

**Riscos e edge cases:** acentos, crases, headings duplicados e anchors gerados
com sufixo; o gerador pode substituir os delimitadores da exceção; versões
distintas podem produzir anchors ou espaçamento diferentes; uma correção
automática de lint pode reformatar o sumário. **Correções e soluções:** fixar
ferramenta, versão, configuração e comando; colocar os delimitadores de lint fora
da faixa substituída pelo gerador; usar o algoritmo de anchor do consumidor;
proibir correção manual ou automática da indentação dentro do bloco; testar
links internos e idempotência.

**Verificação e evidências:** registrar ferramenta, versão, configuração e
comando; salvar o diff da primeira geração; executar novamente e salvar o diff
vazio da segunda; executar Markdownlint com relatório que demonstre a exceção
local e ausência de `MD007` fora dela; executar link checker de anchors.

**Checklist de execução:**

- [ ] Identificar e fixar ferramenta, versão, configuração e comando do gerador.
- [ ] Gerar inventário final de headings elegíveis.
- [ ] Regenerar o sumário preservando a indentação nativa do gerador.
- [ ] Posicionar a exceção `MD007` somente ao redor do bloco gerado.
- [ ] Resolver anchors duplicados ou especiais.

**Saída esperada:** sumário automático completo, navegável, reproduzível e
idempotente, com formatação nativa preservada e exceção de lint localizada.

**Checklist de validação:**

- [ ] Confirmar cobertura 1:1 entre sumário e headings.
- [ ] Regenerar duas vezes e confirmar zero diff na segunda execução.
- [ ] Confirmar que a saída preserva a indentação nativa do gerador.
- [ ] Executar Markdownlint e confirmar zero `MD007` fora do bloco exceptuado.
- [ ] Confirmar que `MD007` permanece ativo para todas as demais listas.

**Checklist de evidência e encerramento:**

- [ ] Anexar identidade do gerador, comando e diffs das duas gerações.
- [ ] Anexar relatório de anchors e lint com o intervalo exceptuado.
- [ ] Registrar zero links internos quebrados.

### COR-21 — Criar validação automatizada

**Escopo positivo:** validar schema, classificação, placeholders, estados,
contratos e projeções. **Escopo negativo:** tentar provar equivalência linguística
somente por testes automáticos ou adicionar dependência sem governança.

**Contexto válido:** regras normativas estabilizadas e fixtures aprovadas.
**Contexto inválido:** testes codificando comportamento ainda indefinido.

**Critérios de aceitação individuais:** há testes positivos, negativos e edge
cases; falha retorna código não zero e erro estruturado; execução é reproduzível;
CI ou `npm run validate` chama o validador autorizado.

**Funcionando corretamente:** toda violação modelada é detectada, e exemplos
válidos passam sem falsos positivos conhecidos.

**Riscos e edge cases:** testes tautológicos, snapshot atualizado cegamente e
dependência indisponível. **Correções e soluções:** fixtures independentes,
mutation cases, revisão de snapshots e dependências fixadas.

**Verificação e evidências:** relatório de testes, cobertura de regras e execução
com mutações intencionais.

**Checklist de execução:**

- [ ] Definir interface e códigos de saída do validador.
- [ ] Criar fixtures válidas, inválidas e limítrofes.
- [ ] Integrar à porta de qualidade autorizada.

**Saída esperada:** validador reproduzível e suíte de testes.

**Checklist de validação:**

- [ ] Confirmar que cada erro mínimo possui teste.
- [ ] Executar mutações de contrato e verificar rejeição.

**Checklist de evidência e encerramento:**

- [ ] Anexar relatório, cobertura e versões das ferramentas.
- [ ] Registrar comando reproduzível e código de saída.

### COR-22 — Resolver comentários inline

**Escopo positivo:** converter cada comentário editorial em definição, teste ou
decisão rastreável. **Escopo negativo:** apagar comentário sem cumprir sua
solicitação ou manter comentários resolvidos como regra paralela.

**Contexto válido:** correções correspondentes implementadas. **Contexto inválido:**
comentário ainda representa requisito pendente.

**Critérios de aceitação individuais:** os cinco comentários possuem ação e
evidência; busca retorna zero comentários editoriais pendentes; nenhuma informação
solicitada foi perdida.

**Funcionando corretamente:** o documento pode ser consumido sem instruções de
edição escondidas em HTML.

**Riscos e edge cases:** comentário técnico legítimo confundido com editorial.
**Correções e soluções:** inventário por localização e remoção apenas dos cinco
IDs/editoriais identificados.

**Verificação e evidências:** matriz comentário-ação-evidência e busca por padrões
HTML/TODO/FIXME.

**Checklist de execução:**

- [ ] Atribuir ID aos cinco comentários.
- [ ] Confirmar critério atendido para cada um.
- [ ] Remover somente os comentários resolvidos.

**Saída esperada:** norma sem pendências editoriais inline.

**Checklist de validação:**

- [ ] Confirmar zero comentários editoriais pendentes.
- [ ] Confirmar que comentários técnicos necessários foram preservados.

**Checklist de evidência e encerramento:**

- [ ] Anexar matriz de resolução dos cinco comentários.
- [ ] Registrar saída da busca final.

### COR-23 — Validar a fonte canônica única

**Escopo positivo:** manter somente `agent-list.md` ativo e preservar a origem por
Git ou hash em evidência. **Escopo negativo:** manter cópia japonesa ativa ou
apagar a proveniência.

**Contexto válido:** migração para pt-BR autorizada. **Contexto inválido:** projeto
que exige publicações multilíngues simultâneas sem hierarquia normativa.

**Critérios de aceitação individuais:** exatamente um arquivo ativo é canônico;
zero links normativos apontam para o nome antigo; origem é recuperável; catálogo
aponta para o canônico.

**Funcionando corretamente:** qualquer consumidor encontra a mesma lista e não
precisa decidir entre versões concorrentes.

**Riscos e edge cases:** cópia com nome alternativo, link histórico confundido
com normativo e arquivo não rastreado. **Correções e soluções:** busca por padrões,
classificação de referências históricas e verificação do índice Git.

**Verificação e evidências:** contagem de candidatos, `git ls-files`, link checker,
hash/commit da origem e catálogo atualizado.

**Checklist de execução:**

- [ ] Inventariar todos os candidatos a lista de agentes.
- [ ] Remover cópias ativas e atualizar referências normativas.
- [ ] Registrar proveniência fora do núcleo genérico.

**Saída esperada:** uma única lista canônica pt-BR rastreada.

**Checklist de validação:**

- [ ] Confirmar contagem canônica igual a um.
- [ ] Confirmar zero links normativos para nomes antigos.

**Checklist de evidência e encerramento:**

- [ ] Anexar inventário, hash/commit e saída de `git ls-files`.
- [ ] Registrar verificação do catálogo documental.

### COR-24 — Validar, versionar e entregar

**Escopo positivo:** executar todas as portas, revisar o diff, versionar somente o
escopo e abrir PR. **Escopo negativo:** mascarar falhas, incluir alterações alheias
ou declarar conclusão sem evidência.

**Contexto válido:** COR-01 a COR-23 aprovadas e branch não `main`. **Contexto
inválido:** gates pendentes, autenticação ausente ou worktree sem escopo isolado.

**Critérios de aceitação individuais:** Markdownlint direcionado passa; testes da
norma passam; `npm run validate` é apresentado; diff está limpo no escopo; commit,
push e PR contêm somente arquivos autorizados.

**Funcionando corretamente:** outro colaborador reproduz validações e revisa a
mudança integralmente pelo PR.

**Riscos e edge cases:** falha preexistente, worktree misto, remote/auth inválidos
e artefato gerado não versionado. **Correções e soluções:** registrar baseline,
stage explícito, separar falhas preexistentes e bloquear publicação sem auth.

**Verificação e evidências:** logs completos, `git diff --check`, lista de arquivos
staged, commit SHA e URL do PR.

**Checklist de execução:**

- [ ] Executar validações direcionadas e integrais.
- [ ] Revisar e stagear caminhos explícitos.
- [ ] Commitar, enviar branch e abrir PR conforme a governança.

**Saída esperada:** alteração versionada em PR com evidências reproduzíveis.

**Checklist de validação:**

- [ ] Confirmar todas as portas aprovadas ou desvios preexistentes documentados.
- [ ] Confirmar que o PR não contém arquivos fora do escopo.

**Checklist de evidência e encerramento:**

- [ ] Anexar logs, SHA do commit e URL do PR.
- [ ] Marcar a tarefa concluída somente após todos os gates.

## Dicionário mínimo exigido

A tabela solicitada no primeiro comentário deve conter, no mínimo:

| ID | Campo | Tipo | Obrigatório | Regra principal |
| --- | --- | --- | :---: | --- |
| F-001 | `translation_run_id` | string | Sim | Identifica uma execução |
| F-002 | `source_artifact` | path | Sim | Caminho lógico da origem |
| F-003 | `source_artifact_sha256` | SHA-256 | Sim | Fixa o blob integral |
| F-004 | `segment_id` | string única | Sim | Identidade estável |
| F-005 | `source_ast_path` | string | Sim | Endereço lógico do segmento |
| F-006 | `source_byte_start` | inteiro | Sim | Início no blob original |
| F-007 | `source_byte_end` | inteiro | Sim | Fim no blob original |
| F-008 | `source_value` | bytes | Sim | Valor original exato |
| F-009 | `source_value_sha256` | SHA-256 | Sim | Integridade do segmento |
| F-010 | `classification` | enum | Sim | Uma das classes fechadas |
| F-011 | `classification_rule_id` | enum | Sim | Regra determinística aplicada |
| F-012 | `placeholder_id` | string única | Condicional | Obrigatório para conteúdo protegido |
| F-013 | `relation_ids` | lista | Condicional | Relações contratuais afetadas |
| F-014 | `translation_value` | string | Condicional | Somente para conteúdo traduzível |
| F-015 | `validation_status` | enum | Sim | Estado da validação |
| F-016 | `error_codes` | lista fechada | Não | Violações detectadas |

Regra de fechamento:

```text
campo desconhecido
ou classe desconhecida
ou regra de classificação desconhecida
⇒ BLOCKED
```

## Método determinístico de classificação

A classificação deve partir de uma AST Markdown:

1. Fixar o blob de origem por SHA-256.
2. Analisar o Markdown em nós estruturais.
3. Atribuir a cada nó um `source_ast_path`.
4. Dividir nós mistos em spans não sobrepostos.
5. Aplicar uma tabela fechada de regras, na ordem definida.
6. Registrar a regra responsável pela classificação.
7. Produzir `AMBIGUOUS` quando nenhuma regra for aplicável.
8. Bloquear se houver bytes da origem sem cobertura.

Tabela mínima:

| Contexto | Parte | Classificação |
| --- | --- | --- |
| Link Markdown | Destino | `PROTECTED_EXACT` |
| Link Markdown | Texto humano | `TRANSLATABLE_CONTROLLED` |
| Código inline | Conteúdo | `PROTECTED_EXACT` por padrão |
| Tabela contratual | Identificadores e enums | `PROTECTED_EXACT` |
| Tabela contratual | Descrição humana | `TRANSLATABLE_CONTROLLED` |
| Mermaid | IDs, setas, estilos e atributos | `PROTECTED_EXACT` |
| Mermaid | Rótulo humano cadastrado | `TRANSLATABLE_CONTROLLED` |
| Prosa | Termo do glossário | `TRANSLATABLE_CONTROLLED` |
| Conteúdo sem regra aplicável | Segmento completo | `AMBIGUOUS` → `BLOCKED` |

## Máquina de estados necessária

```text
SOURCE_FIXED
→ PARSED
→ CLASSIFIED
→ CONTRACTS_FROZEN
→ NATURAL_LANGUAGE_TRANSLATED
→ CONTRACTS_RESTORED
→ STRUCTURE_VALIDATED
→ CONTRACTS_VALIDATED
→ SEMANTICS_VALIDATED
→ APPROVED
```

Qualquer erro leva a:

```text
BLOCKED
```

`traducao_concluida`, atualmente usada na `REG-TRAD-001.4`, deve ser substituída por um estado intermediário como `NATURAL_LANGUAGE_TRANSLATED`.

## Códigos de erro mínimos

```text
E_SOURCE_NOT_FIXED
E_PARSE_FAILED
E_UNCOVERED_SOURCE_BYTES
E_UNCLASSIFIED_SEGMENT
E_UNKNOWN_FIELD
E_UNKNOWN_CLASS
E_UNKNOWN_CLASSIFICATION_RULE
E_PLACEHOLDER_MISSING
E_PLACEHOLDER_DUPLICATED
E_PLACEHOLDER_COLLISION
E_PROTECTED_VALUE_CHANGED
E_LOGICAL_POSITION_CHANGED
E_CARDINALITY_CHANGED
E_ASSOCIATION_CHANGED
E_CONTRACT_RELATION_CHANGED
E_SEMANTIC_SIGNATURE_CHANGED
E_UNMATCHED_SOURCE_PROPOSITION
E_TARGET_ADDITION_WITHOUT_SOURCE
```

## Correções editoriais objetivas

Também são necessárias:

- trocar a fence da linha 116 de `markdown` para `text`;
- remover o HTML malformado das linhas 65–76;
- regenerar o sumário preservando a indentação nativa do gerador automático;
- delimitar as ocorrências `MD007` do sumário com exceção estritamente local,
  sem desabilitar a regra para as demais listas;
- retirar o hash específico de `agent-list.md` do núcleo normativo e colocá-lo na evidência;
- remover os cinco comentários inline somente após sua resolução;
- registrar o arquivo no Git — atualmente ele continua como `??`, portanto ainda não é uma norma efetiva do repositório.

## Ordem recomendada

1. COR-01 e COR-02: autoridade e separação entre norma e perfil.
2. COR-03 a COR-06: modelo de dados e classificação fechada.
3. COR-07 a COR-14: semântica operacional.
4. COR-15 a COR-19: consolidação e correções estruturais.
5. COR-20 a COR-23: automação, comentários e fonte canônica.
6. COR-24: validação, commit e PR.

Até COR-03–COR-14 serem concluídas, a norma deve permanecer com status operacional `BLOCKED`, pois ainda admite decisões não determinísticas.
