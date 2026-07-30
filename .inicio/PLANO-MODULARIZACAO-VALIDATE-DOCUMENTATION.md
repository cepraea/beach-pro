# Plano determinístico de modularização do validador documental

## 1. Controle do documento

| Campo | Valor |
| --- | --- |
| Projeto | CEPRAEA BEACH PRO |
| Componente | `scripts.documentation.validate_documentation` |
| Repositório | `cepraea/beach-pro` |
| Branch de baseline inspecionada | `main` |
| Branch de ajuste do plano | `codex/ajustar-plano-modularizacao-validator` |
| Branch de autorização operacional | `agent/autorizar-modularizacao-validator` |
| Branch de execução da Fase 0 | `agent/modularizacao-validator-fase-0` |
| Branch de execução da Fase 1 | `agent/modularizacao-validator-fase-1` |
| Branch de execução da Fase 2 | `agent/modularizacao-validator-fase-2` |
| Branch de execução da Fase 3 | `agent/modularizacao-validator-fase-3` |
| Branch de execução da Fase 4 | `agent/modularizacao-validator-fase-4` |
| Branch de execução da Fase 5 | `agent/modularizacao-validator-fase-5` |
| Branch de execução da Fase 6 | `agent/modularizacao-validator-fase-6` |
| Commit-base validado | `defaa0439e5163b159dfd18359dd31cc65f469f4` |
| Commit de incorporação do plano | `6fbfdad55240b5b9f6d377f8b436e314d7feeb8a` |
| Commit de incorporação da autorização | `fcbc84dc19ca42c57ece96132def71c1a7420b19` |
| Commit de incorporação da governança | `2bbb23c2e9dbbbe5da77203eb00266f52ac99ccf` |
| Commit de incorporação da materialização | `88c3bc530fd0cc2496d9b2812b31d47ef7306d5e` |
| Commit de incorporação da baseline | `e8292e6368557f6dd5384a2c380c1301bfb5279d` |
| Data da validação | 2026-07-30 |
| Estado deste plano | Fase 5 incorporada; Fase 6 implementada na PR #9 com gates locais aprovados, efetivos após merge |
| Framework de testes | `unittest` |
| Verificador estático | Pyright/Pylance em modo `strict` |
| Política Git | Alterações somente em branch específica, com isolamento do worktree e entrega por pull request |

Este documento substitui, para a futura modularização, as recomendações
fragmentadas produzidas durante a migração do script para pacote. Ele não
reescreve os planos históricos. A autorização operacional é um registro
separado, vinculado ao conteúdo incorporado no commit `6fbfdad`.

Este arquivo, em
`.inicio/PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md`, é o plano ativo da
modularização.

## 2. Objetivo

Dividir a implementação de 2.181 linhas atualmente concentrada em
`validate_documentation/__init__.py` em módulos coesos, preservando:

- a execução por
  `python3 -m scripts.documentation.validate_documentation`;
- o comportamento observável do validador durante cada extração estrutural;
- a identidade canônica do pacote;
- o fail-fast do pipeline;
- a API pública deliberadamente aprovada;
- a previsibilidade de `unittest.mock.patch`;
- o modo Pyright/Pylance `strict`;
- a integridade dos gates e das evidências documentais.

## 3. Escopo

### 3.1 Incluído

- governança necessária para autorizar a divisão;
- criação ou seleção de branch específica antes da primeira alteração;
- isolamento das mudanças não relacionadas já existentes no worktree;
- entrega das mudanças da modularização por pull request;
- materialização e verificação dos três pacotes TAR;
- baseline reprodutível;
- regularização dos pacotes ancestrais;
- remoção das alterações dinâmicas de `sys.path` nos testes;
- migração para imports canônicos;
- extração incremental das 45 funções e 3 classes existentes;
- criação do módulo de pipeline;
- descoberta da raiz por marcadores fortes, em mudança comportamental separada;
- migração completa dos 49 patches;
- redução final do `__init__.py`;
- atualização do README e do mapa operacional;
- validação final.

### 3.2 Fora do escopo

- adoção de pytest;
- introdução de Pydantic;
- alteração de schemas para acomodar defeitos do código;
- criação automática de workflow do GitHub Actions;
- alteração das regras dos gates sem decisão contratual própria;
- inclusão dos TARs no Git;
- criação de tag, force-push ou qualquer operação Git destrutiva;
- inclusão de mudanças não relacionadas nos commits ou no pull request;
- implementação de `--workspace-root`;
- correções lógicas não explicitamente autorizadas.

### 3.3 Limitações residuais e prontidão de produção

Concluir este plano comprova a modularização e a preservação controlada do
comportamento. Isso **não** torna, por si só, o validador apto a operar como
gate bloqueante de produção.

Permanecem fora deste plano e exigem decisões contratuais e testes próprios:

1. compatibilizar a identidade dos gates globais com as evidências exigidas
   pelas aprovações;
2. fazer G2 comprovar os bytes reais de fontes locais, e não apenas comparar
   hashes declarados;
3. decidir se G2 é obrigatório para aprovação e como comprovar a cobertura de
   todos os documentos aplicáveis;
4. substituir a quantidade fixa de dez registros de ingestão por fonte
   contratual versionada.

Nenhum resultado deste plano pode ser usado para declarar resolvidas essas
quatro limitações.

## 4. Estado verificado do repositório

| Evidência | Estado no commit-base |
| --- | --- |
| Implementação | 2.181 linhas em `validate_documentation/__init__.py` |
| Funções de topo | 45 |
| Classes de topo | 3 |
| Métodos de `Reporter` | 4 |
| Métodos de teste | 92 |
| Ocorrências de `patch.object` | 49 |
| Grupos de alvos de patch | 13 |
| Pyright `strict` | 0 erros, 0 avisos |
| Compilação | Aprovada |
| Clone limpo: testes | 91 aprovados, 1 reprovado |
| Causa da reprovação | Três TARs registrados e ausentes |
| Pacotes ancestrais | `scripts/__init__.py` e `scripts/documentation/__init__.py` ausentes |
| Imports canônicos nos testes funcionais | Ausentes |
| Entrada operacional | `python3 -m scripts.documentation.validate_documentation` |
| `WORKSPACE_ROOT` | `Path(__file__).resolve().parents[3]` |
| Arquivo de dependências Python | Ausente |

O resultado 91/92 de um clone limpo não representa defeito demonstrado no
código Python. O teste de entrada executa G-ARCH, que depende dos TARs
deliberadamente ignorados pelo Git.

## 5. Invariantes obrigatórias

1. Uma extração estrutural não altera regra documental.
2. Uma mudança comportamental não fica oculta em uma extração estrutural.
3. Cada change set movimenta uma responsabilidade principal.
4. O teste vermelho somente é criado quando o comportamento esperado estiver
   autorizado.
5. Um teste vermelho deve falhar pela regra esperada, não por import, sintaxe ou
   fixture.
6. O patch atinge o namespace em que o objeto é consultado.
7. Módulos consumidores consultam objetos mutáveis pelo módulo proprietário:

   ```python
   config.WORKSPACE_ROOT
   links.validate_links(...)
   registry.load_registry(...)
   ```

8. Não usar, nos consumidores:

   ```python
   from .config import WORKSPACE_ROOT
   from .links import validate_links
   ```

   Essas formas copiam referências para o namespace consumidor e tornam patches
   mais frágeis.

9. `Any` permanece restrito às fronteiras dinâmicas de YAML, JSON e
   `jsonschema`.
10. Nenhuma supressão genérica de Pyright/Pylance é permitida.
11. Nenhum arquivo histórico é reescrito para fazer um gate passar.
12. Nenhum TAR com hash divergente é sobrescrito ou regenerado
    silenciosamente.
13. Nenhuma fase posterior começa sem o gate de saída da fase anterior.
14. Nenhuma alteração é feita diretamente na branch `main`.
15. Mudanças não relacionadas já existentes no worktree não são editadas,
    adicionadas ao staging ou incluídas no pull request.
16. `npm run validate` é executado depois de cada change set que altere código
    ou configuração e novamente no gate final.
17. Todas as funções permanecem autoexplicativas. Funções complexas contêm
    docstrings ou comentários inline que expliquem o **porquê** das decisões
    técnicas, especialmente limites de segurança, fail-fast, integridade e
    compatibilidade histórica.

## 6. Arquitetura-alvo

```text
scripts/
├── __init__.py
└── documentation/
    ├── __init__.py
    ├── integration_tests/
    │   ├── __init__.py
    │   └── test_repository_entrypoint.py
    ├── tests/
    │   └── ...
    └── validate_documentation/
        ├── __init__.py
        ├── __main__.py
        ├── README.md
        ├── MAPA-VALIDADOR-DOC.md
        ├── approvals.py
        ├── cli.py
        ├── config.py
        ├── contracts.py
        ├── filesystem.py
        ├── front_matter.py
        ├── ingestion.py
        ├── instances.py
        ├── json_types.py
        ├── links.py
        ├── models.py
        ├── pipeline.py
        ├── provenance.py
        ├── registry.py
        ├── reporter.py
        ├── workflow.py
        └── gates/
            ├── __init__.py
            ├── dispatcher.py
            ├── g_arch.py
            ├── g0.py
            ├── g1.py
            ├── g2.py
            └── g_fm.py
```

### 6.1 Direção permitida de dependências

```text
json_types / models
        ↓
config / filesystem / reporter
        ↓
contracts / registry / workflow / approvals / provenance / ingestion
        ↓
instances / front_matter / links
        ↓
gates
        ↓
pipeline
        ↓
cli
        ↓
__init__ / __main__
```

Regras:

- uma camada não importa camada situada abaixo dela no diagrama;
- `cli.py` não contém validação documental;
- `pipeline.py` apenas orquestra estágios;
- `gates/dispatcher.py` despacha, mas não implementa gates;
- `gates/*.py` não importam `cli.py` ou `pipeline.py`;
- `models.py` não importa módulos de domínio;
- `json_types.py` não conhece paths, gates ou Reporter;
- `__init__.py` é fachada, não módulo de implementação;
- `__main__.py` contém apenas a entrada da CLI;
- imports entre módulos irmãos são relativos e preferencialmente importam o
  módulo, não símbolos patcháveis.

## 7. Contrato dos dois subciclos

### 7.1 Subciclo A — extração estrutural

1. Confirmar os gates da fase anterior.
2. Selecionar uma responsabilidade.
3. Criar somente o módulo de destino dessa responsabilidade.
4. Mover o código sem reescrever sua lógica.
5. Preservar temporariamente o reexport no `__init__.py`.
6. Migrar testes unitários da responsabilidade para o módulo proprietário.
7. Atualizar patches somente quando o namespace de consulta mudar.
8. Executar o teste localizado.
9. Executar a suíte unitária.
10. Executar compilação e Pyright.
11. Executar os gates afetados.
12. Executar `npm run validate` quando o change set alterar código ou
    configuração.
13. Comparar as saídas normalizadas com a baseline.
14. Confirmar que funções complexas movidas preservam ou recebem documentação
    sobre o porquê das decisões técnicas, sem comentários redundantes.

Aceitação:

```text
API transitória preservada
+ testes verdes
+ Pyright verde
+ npm run validate verde quando aplicável
+ gates semanticamente idênticos
+ nenhuma mudança intencional de regra
+ decisões complexas documentadas para desenvolvedores e agentes de IA
```

### 7.2 Subciclo B — mudança comportamental

1. Identificar o contrato autorizador.
2. Registrar decisão quando o contrato for ambíguo.
3. Criar um teste que demonstre o comportamento esperado.
4. Executar o teste e confirmar RED pelo motivo correto.
5. Aplicar a menor correção possível.
6. Executar o teste e confirmar GREEN.
7. Executar testes do módulo.
8. Executar a suíte unitária.
9. Executar a integração aplicável.
10. Executar Pyright e gates afetados.
11. Executar `npm run validate`.
12. Comparar e justificar cada diferença autorizada.
13. Atualizar contrato, mapa ou README quando necessário.
14. Documentar o porquê da correção quando a regra não for evidente pelo
    código.

O registro do RED é evidência da execução; o teste não permanece vermelho na
linha principal.

## 8. Diretório de evidências da execução

Cada execução cria, sem commit automático:

```text
.inicio/evidencias/validate-documentation/
└── BASELINE-<SHORT_SHA>-<UTC>/
    ├── metadata.yaml
    ├── git-head.txt
    ├── git-status.txt
    ├── git-diff.patch
    ├── untracked-files.txt
    ├── environment.txt
    ├── dependencies.txt
    ├── hashes.sha256
    ├── tar-manifest.sha256
    ├── compile.txt
    ├── pyright.json
    ├── npm-validate.txt
    ├── tests-unit.txt
    ├── tests-integration.txt
    ├── api-publica.tsv
    ├── functions.tsv
    ├── patches.tsv
    ├── tar-acquisition.yaml
    └── gates/
        ├── raw/
        └── normalized/
```

`metadata.yaml` deve registrar:

- commit-base;
- estado limpo ou sujo;
- data e hora UTC;
- sistema operacional;
- Python;
- PyYAML;
- jsonschema;
- Pyright;
- quantidade descoberta de testes;
- resultado dos gates;
- identidade do executor;
- caminho deste plano;
- autorização ou ausência de autorização Git.
- branch de execução;
- decisão de isolamento de cada alteração preexistente;
- identificadores e estado de `BEH-01` a `BEH-07`;
- comando e resultado de `npm run validate`.

Se o diretório não for versionado, seu conteúdo deve ser preservado fora do
workspace antes de qualquer limpeza. Hash sem conteúdo não permite reconstrução.

## 9. Fase -1 — fluxo Git e isolamento do worktree

Esta fase é obrigatória antes de qualquer alteração do plano, código,
configuração, mapa ou README.

### 9.1 Entrada

- regras locais em `AGENTS.md`;
- branch atual;
- `git status --porcelain=v1`;
- diff rastreado e lista de arquivos não rastreados.

### 9.2 Ações

1. Executar:

   ```bash
   git branch --show-current
   git rev-parse HEAD
   git status --porcelain=v1
   git diff --binary HEAD
   git ls-files --others --exclude-standard
   ```

2. Parar se a branch atual for `main`.
3. Criar ou selecionar uma branch específica para a modularização.
4. Registrar cada modificação preexistente como:
   - pertencente à modularização;
   - não relacionada e intocável;
   - dependência que exige decisão antes de prosseguir.
5. Não mover, apagar, restaurar, adicionar ao staging ou incluir em commit
   qualquer alteração não relacionada.
6. Definir que a entrega final ocorrerá por pull request da branch específica.
7. Confirmar que nenhum segredo ou `.env.local` entrou no escopo.

### 9.3 Gate de saída da Fase -1

```text
GIT-WORKFLOW-READY = PASS
```

Aceitação:

- branch diferente de `main`;
- HEAD e estado inicial registrados;
- mudanças preexistentes classificadas;
- escopo do futuro pull request delimitado;
- nenhuma mudança não relacionada tocada.

Qualquer falha bloqueia a Fase 0.

Estado materializado em 2026-07-30:

```text
GIT-WORKFLOW-READY = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/AUTH-MODULARIZATION-VALIDATOR-20260730/metadata.yaml`.
Estado Git detalhado:
`.inicio/evidencias/validate-documentation/AUTH-MODULARIZATION-VALIDATOR-20260730/git-state.md`.
O worktree de execução foi criado limpo a partir de
`main@6fbfdad55240b5b9f6d377f8b436e314d7feeb8a`; as mudanças preexistentes do
worktree de origem foram classificadas como não relacionadas e intocáveis.

Após a incorporação da autorização, a Fase 0 foi iniciada em novo worktree,
na branch `agent/modularizacao-validator-fase-0`, a partir de
`main@fcbc84dc19ca42c57ece96132def71c1a7420b19`. O worktree original permanece
fora do escopo e não foi alterado.

## 10. Fase 0 — autorização e governança

### 10.1 Entrada

- este plano;
- `MAPA-VALIDADOR-DOC.md`;
- README do pacote;
- planos históricos em `.inicio`.

### 10.2 Ações

1. Aprovar este plano e seu escopo.
2. Registrar seu caminho como plano ativo da modularização.
3. Atualizar o mapa ativo para:
   - remover a proibição absoluta de mover funções;
   - permitir imports exigidos pelo módulo em extração;
   - impor os dois subciclos;
   - impor a direção de dependências deste plano.
4. Atualizar o README para distinguir:
   - manutenção anterior no monólito;
   - modularização atual autorizada;
   - suíte unitária;
   - integração dependente de TAR.
5. Preservar `.inicio/Plano-validator.md` e
   `.inicio/Plano-migracao-validator.md` como registros históricos.
6. Aprovar e registrar as sete decisões comportamentais abaixo antes de
   iniciar qualquer implementação:

   | Decisão | Comportamento esperado | RED obrigatório | GREEN obrigatório |
   | --- | --- | --- | --- |
   | `BEH-01` | Descobrir o workspace pelos quatro marcadores canônicos da Fase 4, com falha determinística quando ausentes | profundidade fixa ou marcadores incompletos selecionam raiz incorreta | raiz, subdiretório, arquivo, ausência e marcadores parciais obedecem ao contrato |
   | `BEH-02` | Rejeitar `documents[index]` que não seja mapping sem descartá-lo silenciosamente | item escalar não produz erro | erro contém o índice exato e os demais itens continuam verificáveis |
   | `BEH-03` | Converter chave YAML complexa ou não hashável em erro controlado | YAML encerra com `TypeError` | `Reporter` recebe erro determinístico e o processo não cai |
   | `BEH-04` | Rejeitar bytes que não sejam UTF-8 válido | bytes inválidos são substituídos e aceitos | erro de UTF-8 identifica o arquivo e interrompe sua validação |
   | `BEH-05` | Converter falhas de leitura em erros controlados | `OSError` escapa do pipeline | `Reporter` recebe erro determinístico sem traceback inesperado |
   | `BEH-06` | Permitir `parse_args(argv)` e `main(argv)` sem alterar o comportamento quando `argv` for `None` | teste precisa modificar `sys.argv` | argumentos explícitos e entrada real produzem resultados equivalentes |
   | `BEH-07` | Contrair a fachada pública para somente `main`, se não houver consumidor externo aprovado | remoção quebra consumidor documentado ou teste de compatibilidade | teste dedicado comprova a API deliberadamente aprovada |

7. Registrar cada decisão em `metadata.yaml`, incluindo aprovador, data,
   contrato autorizador e resultado esperado.
8. Registrar que branch e pull request são obrigatórios; commit e push somente
   integram a execução quando necessários para entregar o pull request.

Estado das decisões em 2026-07-30:

```text
BEH-01 = APPROVED
BEH-02 = APPROVED
BEH-03 = APPROVED
BEH-04 = APPROVED
BEH-05 = APPROVED
BEH-06 = APPROVED
BEH-07 = APPROVED
```

Autorização:
`.inicio/evidencias/validate-documentation/AUTH-MODULARIZATION-VALIDATOR-20260730/authorization.yaml`.
Análise de impacto:
`.inicio/evidencias/validate-documentation/AUTH-MODULARIZATION-VALIDATOR-20260730/impact-analysis.md`.

Esses registros desbloqueiam a execução da Fase 0. O gate
`GOVERNANCE-MODULARIZATION` permanece pendente até concluir as demais ações
desta fase; fases posteriores continuam condicionadas aos respectivos gates.

### 10.3 Gate de saída da Fase 0

```text
GOVERNANCE-MODULARIZATION = PASS
```

Estado materializado em 2026-07-30:

```text
GOVERNANCE-MODULARIZATION = PASS
```

O resultado está registrado em
`.inicio/evidencias/validate-documentation/GOVERNANCE-MODULARIZATION-20260730/`
e é efetivo quando a PR #3 for incorporada à `main`. Até o merge, a Fase 1
permanece bloqueada para impedir que código seja extraído a partir de
governança ainda não canônica.

Bloqueios:

- plano não aprovado;
- mapa ainda proíbe movimentação;
- README ainda descreve somente o monólito;
- tentativa de reescrever fatos históricos;
- qualquer decisão entre `BEH-01` e `BEH-07` ausente, ambígua ou sem aprovador.

## 11. Fase 1 — materialização dos TARs

### 11.1 Manifesto obrigatório

| Documento | Versão | Caminho | SHA-256 esperado |
| --- | --- | --- | --- |
| `DOC-EVID-PACOTE-INTEGRIDADE-LEGADO` | `0.1.0` | `docs/evidence/integrity/pacote-integridade-legado.tar` | `7b0d9effe3da654af63638f8850841332605f9c535a8a7181ac021b5be284cf6` |
| `DOC-EVID-PACOTE-FONTES-CONTEXTO` | `0.1.0` | `docs/evidence/provenance/pacote-fontes-contexto-cepraea.tar` | `3f49cde024244a630cf0e4e335348d26252cf7550ec586e0e78d4ff609ecfc21` |
| `DOC-EVID-PACOTE-DIVERGENCIA-RELATORIO-V01` | `0.1.0` | `docs/evidence/integrity/pacote-divergencia-relatorio-validacao-v01.tar` | `6dcfdc0f295e40e77fdd82be3b4dce4b47f6c04d43ef9fe553b140b375da97ec` |

### 11.2 Procedimento

1. Verificar primeiro os caminhos de destino no workspace. Um arquivo já
   existente é uma aquisição local válida somente quando seu SHA-256 coincide
   exatamente com o manifesto.
2. Se um destino estiver ausente, o operador fornece um arquivo local obtido de
   fonte autorizada e registra em `tar-acquisition.yaml`:
   - identificador da fonte;
   - caminho de origem, ou identificador redigido quando o caminho contiver
     informação sensível;
   - SHA-256 da origem antes da cópia;
   - responsável e instante UTC;
   - caminho de destino.
3. Não reconstruir TARs a partir de arquivos aparentemente equivalentes.
4. Calcular o hash da origem antes de copiar. Se divergir do manifesto, parar.
5. Se o destino já existir, calcular o hash antes de qualquer ação.
6. Se o hash do destino divergir, parar; não sobrescrever.
7. Se o destino estiver ausente, copiar sem substituir arquivo existente e
   recalcular o hash do destino.
8. Executar:

   ```bash
   sha256sum \
     docs/evidence/integrity/pacote-integridade-legado.tar \
     docs/evidence/provenance/pacote-fontes-contexto-cepraea.tar \
     docs/evidence/integrity/pacote-divergencia-relatorio-validacao-v01.tar
   ```

9. Comparar cada hash, byte por byte, com a tabela.
10. Salvar o resultado em `tar-manifest.sha256`.
11. Confirmar que `git status --porcelain=v1` não pretende versioná-los, pois
   `*.tar` está ignorado.
12. Preservar `tar-acquisition.yaml` junto às evidências da execução. O arquivo
    registra proveniência operacional, mas não autoriza versionar os TARs.

No workspace validado para este plano, os três destinos já existem e possuem os
hashes exatos do manifesto. Um clone que não possua esses bytes permanece
bloqueado até receber uma fonte local autorizada; o plano não presume que o Git
reconstrua arquivos ignorados.

### Gate de saída da Fase 1

```text
TAR-MATERIALIZATION = PASS
```

Estado materializado em 2026-07-30:

```text
TAR-MATERIALIZATION = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/TAR-MATERIALIZATION-20260730/`.
A execução ocorreu na branch `agent/modularizacao-validator-fase-1` e foi
entregue pela PR #4. Os três TARs permanecem ignorados pelo Git; por isso, o
resultado comprova o worktree registrado e não transfere os bytes para outro
clone. A Fase 2 exige o merge da evidência e nova verificação dos hashes no
worktree de baseline.

Se qualquer fonte estiver indisponível:

```text
TAR-MATERIALIZATION = BLOCKED
```

Nesse estado pode-se produzir diagnóstico de código, mas nenhuma extração
modular deve começar.

## 12. Fase 2 — baseline

### 12.1 Evidência Git somente leitura

```bash
git rev-parse HEAD
git status --porcelain=v1
git diff --binary HEAD
git ls-files --others --exclude-standard
```

Condições:

- `defaa0439e5163b159dfd18359dd31cc65f469f4` permanece como fonte histórica
  dos inventários registrados na seção 4;
- registrar o `HEAD` real no início da baseline, sem exigir que ele seja igual
  ao commit histórico;
- comparar, entre o commit histórico e o `HEAD`, somente os caminhos capazes
  de invalidar os inventários:

  ```bash
  git diff --name-status \
    defaa0439e5163b159dfd18359dd31cc65f469f4..HEAD -- \
    scripts/documentation/validate_documentation \
    scripts/documentation/tests \
    pyrightconfig.json
  ```

- se essa comparação apontar mudança, regenerar os inventários de funções,
  classes, testes e patches antes da primeira extração;
- commits exclusivamente documentais ou de governança não invalidam os
  inventários, mas seu `HEAD` continua obrigatório na evidência;
- no início da primeira extração de código, fixar no `metadata.yaml` o novo
  commit de baseline executável. As comparações seguintes usam essa identidade
  registrada, e não uma igualdade impossível com um commit anterior;
- se o worktree estiver limpo, HEAD e hashes permitem reconstrução;
- se estiver sujo, preservar `git diff --binary HEAD`;
- arquivos não rastreados precisam ter conteúdo preservado, não apenas hash;
- não criar commit de baseline sem autorização explícita.

### 12.2 Ambiente

```bash
python3 --version
python3 -m pip show PyYAML jsonschema
node --version
npm --version
npx --yes pyright@1.1.411 --version
```

Registrar as saídas completas. A inexistência de lock Python é uma limitação
explícita desta baseline.

Confirmar Node.js `24.14.1` e npm `11.11.0`, conforme `AGENTS.md`. Quando as
dependências Node não estiverem materializadas a partir do lockfile, executar
`npm ci` antes dos comandos de validação.

### 12.3 Compilação

```bash
python3 -m compileall -q \
  scripts/documentation/validate_documentation \
  scripts/documentation/tests
```

Esperado:

```text
exit code = 0
```

### 12.4 Suíte atual

```bash
python3 -m unittest discover \
  -s scripts/documentation/tests \
  -v
```

Esperado depois da materialização correta:

```text
92 testes executados
92 aprovados
0 falhas
0 erros
```

O número 92 é a contagem do commit-base. O executor deve também registrar a
contagem descoberta, não apenas comparar uma string fixa.

### 12.5 Pyright

```bash
npx --yes pyright@1.1.411 \
  --project pyrightconfig.json \
  --outputjson
```

Esperado:

```text
errorCount = 0
warningCount = 0
informationCount = 0
```

### 12.6 Validação obrigatória do projeto

```bash
npm run validate
```

Esperado:

```text
exit code = 0
```

Preservar a saída completa em `npm-validate.txt`. Essa validação complementa,
mas não substitui, os testes Python, o Pyright fixado e os gates documentais.

### 12.7 Gates

```bash
python3 -m scripts.documentation.validate_documentation \
  --gate G-ARCH --format yaml

python3 -m scripts.documentation.validate_documentation \
  --gate G0 --format yaml

python3 -m scripts.documentation.validate_documentation \
  --gate G1 --format yaml

python3 -m scripts.documentation.validate_documentation \
  --gate G2 \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1 \
  --format yaml

python3 -m scripts.documentation.validate_documentation \
  --gate G-FM \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1.2 \
  --format yaml
```

O comando G2 conserva a versão histórica `0.1` porque o pacote de proveniência
materializado corresponde a essa versão. A versão canônica `0.1.2` não possui
pacote G2 registrado; essa limitação não deve ser ocultada nem corrigida dentro
deste plano.

Executar também a validação global:

```bash
python3 -m scripts.documentation.validate_documentation
```

### 12.8 Normalização dos gates

Preservar a saída bruta. Na saída normalizada remover apenas:

- `evaluated_at`;
- `gate_result_id` quando tiver identidade de execução.

Comparar obrigatoriamente:

- código de saída;
- `gate_id`;
- `document_id`;
- `version`;
- `content_hash`;
- `status`;
- `evidence_ids`;
- `failures`;
- `next_actions`;
- warnings emitidos no formato textual.

Ordenar somente coleções cujo contrato não atribui significado à ordem.

### 12.9 Hashes

Gerar SHA-256 de:

- pacote do validador;
- testes;
- `pyrightconfig.json`;
- workflow;
- registro;
- schemas consumidos;
- três TARs;
- README e mapa;
- este plano.

### Gate de saída da Fase 2

```text
BASELINE-CODE = PASS
BASELINE-INTEGRATION = PASS
BASELINE-VALIDATE-DOCUMENTATION = PASS
BASELINE-NPM-VALIDATE = PASS
```

Estado materializado em 2026-07-30:

```text
BASELINE-CODE = PASS
BASELINE-INTEGRATION = PASS
BASELINE-VALIDATE-DOCUMENTATION = PASS
BASELINE-NPM-VALIDATE = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/BASELINE-88c3bc5-20260730T174342Z/`.
A execução foi ancorada em
`main@88c3bc530fd0cc2496d9b2812b31d47ef7306d5e` e entregue pela PR #5. O hash
deste plano em `hashes.sha256` corresponde aos bytes anteriores a esta
atualização de estado e deve ser verificado contra o commit-base.

Qualquer resultado diferente bloqueia a Fase 3.

## 13. Fase 3 — identidade canônica e taxonomia dos testes

Esta fase é atômica: não remover `sys.path` sem substituir simultaneamente os
imports curtos.

### 13.1 Pacotes ancestrais

Criar:

```text
scripts/__init__.py
scripts/documentation/__init__.py
```

Cada arquivo deve conter somente uma docstring curta.

### 13.2 Testes que devem abandonar o import curto

1. `test_approvals.py`;
2. `test_cli_and_resolution.py`;
3. `test_front_matter.py`;
4. `test_instances.py`;
5. `test_main_pipeline.py`;
6. `test_package_entrypoints.py`;
7. `test_registry_invariants.py`;
8. `test_reporter.py`;
9. `test_scoped_gates.py`;
10. `test_workflow_and_ingestion.py`.

Substituir:

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_documentation as validator
```

por:

```python
from scripts.documentation import validate_documentation as validator
```

Em `test_front_matter.py`, substituir os imports diretos pelo caminho canônico.
Remover `# noqa: E402`. Remover `sys` e `Path` somente quando ficarem realmente
sem uso. `test_package_entrypoints.py` ainda usa `sys.executable` e não deve
perder o import de `sys`.

### 13.3 Separar unidade e integração

Alterar `test_module_entrypoint_operates` para verificar:

```bash
python3 -m scripts.documentation.validate_documentation --help
```

Esse teste comprova a entrada por módulo sem depender do acervo.

Mover a execução real de G-ARCH para:

```text
scripts/documentation/integration_tests/test_repository_entrypoint.py
```

A integração não deve ser silenciosamente ignorada. Seu comando possui como
precondição `TAR-MATERIALIZATION = PASS`.

### 13.4 Comandos após a separação

Suíte unitária:

```bash
python3 -m unittest discover \
  -s scripts/documentation/tests \
  -t . \
  -v
```

Integração:

```bash
python3 -m unittest discover \
  -s scripts/documentation/integration_tests \
  -t . \
  -v
```

Esperado:

- 92 testes unitários;
- 1 teste de integração;
- todos aprovados quando os TARs estiverem materializados.

### Gate de saída da Fase 3

```text
CANONICAL-IMPORT-IDENTITY = PASS
```

Estado materializado em 2026-07-30:

```text
CANONICAL-IMPORT-IDENTITY = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/CANONICAL-IMPORT-IDENTITY-20260730/`.
O resultado foi produzido na branch
`agent/modularizacao-validator-fase-3` e incorporado pela PR #6. O merge
materializou o gate e desbloqueou a Fase 4.

Aceitação adicional:

```bash
rg 'sys\.path\.(insert|append)' scripts/documentation/tests
```

não retorna ocorrências.

## 14. Fase 4 — fundações

### 14.1 Subciclo 4A — tipos JSON

Criar `json_types.py` e mover:

- `JsonObject`;
- `_accept_dynamic_value`;
- `_accept_dynamic_mapping`;
- `as_json_object`;
- `_accept_dynamic_array`;
- `as_json_array`.

### 14.2 Subciclo 4A — modelo da CLI

Criar `models.py` e mover:

- `ValidatorArgs`.

### 14.3 Subciclo 4A — configuração

Criar `config.py` e mover os paths:

- `WORKSPACE_ROOT`;
- `DEFAULT_REGISTRY`;
- `DEFAULT_WORKFLOW`;
- `SCHEMA_ROOT`;
- todos os paths de schema;
- `INTEGRITY_MANIFEST`;
- paths de schema do Front Matter.

Inicialmente preservar:

```python
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
```

### 14.4 Subciclo 4A — filesystem

Criar `filesystem.py` e mover:

- `workspace_path`;
- `sha256`.

`filesystem.py` deve consultar `config.WORKSPACE_ROOT` em tempo de chamada.

### 14.5 Subciclo 4B — descoberta da raiz

Somente depois de 4A verde e de `BEH-01 = APPROVED`, criar:

```python
def find_workspace_root(start: Path | None = None) -> Path:
    ...
```

Contrato:

1. resolver `start` ou `Path(__file__)`;
2. se o resultado for arquivo, iniciar pelo pai;
3. percorrer o diretório atual e seus ancestrais;
4. aceitar somente candidato que contenha simultaneamente:
   - `docs/registry/registro-documentos.yaml`;
   - `docs/registry/workflow-documentacao.yaml`;
   - `docs/contracts/schemas/documento.schema.json`;
   - `scripts/documentation/validate_documentation`;
5. retornar o primeiro ancestral completo;
6. lançar `RuntimeError` determinístico se nenhum candidato for válido.

Testes RED–GREEN:

- raiz válida;
- início em arquivo;
- início em subdiretório;
- marcadores parciais;
- ausência total;
- symlink, se suportado pelo ambiente.

Não usar os TARs como marcadores de raiz.

### Gate de saída da Fase 4

```text
FOUNDATIONS = PASS
WORKSPACE-DISCOVERY = PASS
```

Estado materializado em 2026-07-30:

```text
FOUNDATIONS = PASS
WORKSPACE-DISCOVERY = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/FOUNDATIONS-WORKSPACE-DISCOVERY-20260730/`.
O resultado foi produzido na branch
`agent/modularizacao-validator-fase-4` e incorporado pela PR #7. O merge
materializou os gates e desbloqueou a Fase 5.

## 15. Fase 5 — Reporter

### Subciclo 5A

Criar `reporter.py` e mover integralmente `Reporter`, sem alterar:

- ordenação;
- YAML;
- texto;
- códigos de saída;
- evaluator;
- comportamento de warnings;
- geração de `evaluated_at`.

Migrar testes para:

```python
from scripts.documentation.validate_documentation import reporter
```

Não realizar alterações comportamentais em 5A.

### Gate de saída da Fase 5

```text
REPORTER-EXTRACTION = PASS
```

Estado materializado em 2026-07-30:

```text
REPORTER-EXTRACTION = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/REPORTER-EXTRACTION-20260730/`.
O resultado foi produzido na branch
`agent/modularizacao-validator-fase-5` e incorporado pela PR #8. O merge
materializou o gate e desbloqueou a Fase 6.

## 16. Fase 6 — contratos e registro

### 16.1 Subciclo 6A — contratos

Criar `contracts.py` e mover:

- `load_json`;
- `validate_schema_definition`;
- `schema_validation_errors`;
- `validate_contract_schemas`;
- `validate_yaml_instance`.

### 16.2 Subciclo 6A — registro

Criar `registry.py` e mover:

- regexes e invariantes de nomes e caminhos do registro;
- `valid_name`;
- `validate_top_level`;
- `resolve_document_version`;
- `validate_record`;
- `validate_uniqueness`;
- `managed_files`;
- `validate_canonical_registry`;
- `load_registry`;
- `validate_registry_integrity`.

### 16.3 Subciclo 6B — defeitos autorizados

Executar somente com `BEH-02 = APPROVED`. Cada correção deve ser independente:

- rejeitar item não mapeamento em `documents`, após confirmar o schema;
- reportar o índice do item inválido;
- impedir descarte silencioso.

Não executar 6B enquanto o contrato do registro não estiver confirmado ou
`BEH-02` não estiver aprovado.

### Gate de saída da Fase 6

```text
CONTRACTS-EXTRACTION = PASS
REGISTRY-EXTRACTION = PASS
```

Estado materializado em 2026-07-30:

```text
CONTRACTS-EXTRACTION = PASS
REGISTRY-EXTRACTION = PASS
BEH-02 = PASS
```

Evidência:
`.inicio/evidencias/validate-documentation/CONTRACTS-REGISTRY-EXTRACTION-20260730/`.
O resultado foi produzido na branch
`agent/modularizacao-validator-fase-6` e entregue pela PR #9. Os gates
tornam-se efetivos após o merge; até lá, a Fase 7 permanece bloqueada.

## 17. Fase 7 — workflow, evidências e instâncias

### 17.1 Workflow

Criar `workflow.py` e mover:

- `validate_workflow_references`.

### 17.2 Aprovações

Criar `approvals.py` e mover:

- `validate_approval_cross_references`.

### 17.3 Proveniência

Criar `provenance.py` e mover:

- `validate_provenance_packages`.

### 17.4 Ingestão

Criar `ingestion.py` e mover:

- `ingestion_records`;
- `validate_ingestion_consistency`.

### 17.5 Instâncias

Criar `instances.py` e mover:

- `validate_document_instances`;
- `validate_workflow_instance`;
- `validate_gate_result_instances`;
- `validate_evidence_instances`;
- `validate_instances`.

`instances.py` orquestra famílias, mas delega relações a `workflow`,
`approvals`, `provenance` e `ingestion`.

### Gate de saída da Fase 7

```text
DOMAIN-INSTANCES-EXTRACTION = PASS
```

## 18. Fase 8 — Front Matter e links

### 18.1 Front Matter estrutural

Criar `front_matter.py` e mover:

- `_DuplicateKeyLoader`;
- `parse_front_matter`;
- `validate_governed`;
- `validate_feature_spec`;
- constantes e schemas específicos de Front Matter.

### 18.2 Links estrutural

Criar `links.py` e mover:

- `normalize_link_target`;
- `validate_links`;
- regexes específicas de links.

### 18.3 Correções comportamentais independentes

Executar um RED–GREEN separado para cada decisão aprovada:

1. `BEH-03`: chave YAML complexa ou não hashável;
2. `BEH-04`: UTF-8 inválido;
3. `BEH-05`: falha de leitura.

Ampliar a cobertura da sintaxe Markdown permanece fora do escopo. Nenhum parser
ou perfil novo deve ser adotado até existir decisão normativa que defina as
sintaxes suportadas, o tratamento de HTML e links por referência e os critérios
de compatibilidade com o acervo atual.

### Gate de saída da Fase 8

```text
FRONT-MATTER-EXTRACTION = PASS
LINKS-EXTRACTION = PASS
```

## 19. Fase 9 — gates

### 19.1 Módulos

| Gate | Módulo |
| --- | --- |
| G-ARCH | `gates/g_arch.py` |
| G0 | `gates/g0.py` |
| G1 | `gates/g1.py` |
| G2 | `gates/g2.py` |
| G-FM | `gates/g_fm.py` |
| Despacho | `gates/dispatcher.py` |

Mover um gate por change set. Para cada um:

1. extrair sem mudar a lógica;
2. migrar o teste localizado;
3. manter reexport transitório;
4. executar unidade, suíte, integração, Pyright e gate;
5. comparar a saída normalizada;
6. somente depois considerar mudança comportamental.

`validate_front_matter`, por ser a execução de G-FM, vai para `gates/g_fm.py`;
os parsers permanecem em `front_matter.py`.

### Gate de saída da Fase 9

```text
GATES-EXTRACTION = PASS
```

## 20. Fase 10 — pipeline e CLI

### 20.1 Pipeline estrutural

Criar `pipeline.py` com:

```python
def run_validation(
    args: ValidatorArgs,
    reporter: Reporter,
) -> None:
    ...
```

Mover para essa função somente a orquestração documental atualmente presente em
`main`. O pipeline não analisa `argv`, não importa `cli.py`, não cria outro
`Reporter` e não chama `Reporter.emit`.

Preservar a sequência fail-fast atual:

```text
carregar registro
→ resolver escopo quando document_id estiver presente
→ validar contratos
→ validar instâncias
→ validar registro e arquivos
→ validar canonicalidade
→ executar gate
→ validar links
→ retornar None
```

O pipeline deve chamar módulos:

```python
registry.load_registry(...)
registry.resolve_document_version(...)
contracts.validate_contract_schemas(...)
instances.validate_instances(...)
registry.validate_registry_integrity(...)
registry.validate_canonical_registry(...)
dispatcher.dispatch_gate(...)
links.validate_links(...)
```

### 20.2 CLI estrutural

Criar `cli.py` e mover:

- `parse_args`;
- `validate_cli_args`;
- `main`.

`main` passa a:

1. obter argumentos com `parse_args`;
2. criar exatamente um `Reporter`;
3. executar `validate_cli_args`;
4. quando os argumentos forem válidos, chamar
   `pipeline.run_validation(args, reporter)`;
5. chamar `reporter.emit(...)` exatamente uma vez, tanto em sucesso quanto em
   qualquer falha;
6. retornar somente o código produzido por `emit`.

`cli.py` pode importar `pipeline.py`; `pipeline.py` não pode importar `cli.py`.
Essa regra elimina o ciclo que seria criado se o pipeline consultasse
`validate_cli_args`.

### 20.3 CLI comportamental

Executar somente com `BEH-06 = APPROVED`. Em subciclo 10B, depois do RED:

```python
def parse_args(
    argv: Sequence[str] | None = None,
) -> ValidatorArgs:
    ...


def main(
    argv: Sequence[str] | None = None,
) -> int:
    ...
```

Testes RED–GREEN e de caracterização:

- argumentos explícitos não exigem alteração de `sys.argv`;
- `argv=None` preserva a entrada real;
- escopo inexistente interrompe antes de contratos e instâncias;
- cada fronteira fail-fast impede os estágios posteriores;
- `pipeline.run_validation` nunca chama `emit`;
- `main` chama `emit` exatamente uma vez em sucesso, erro de CLI e erro de
  pipeline;
- `pipeline.py` não importa `cli.py`.

### 20.4 `__main__.py`

Manter mínimo:

```python
from .cli import main

raise SystemExit(main())
```

Não incluir regra de negócio em `__main__.py`.

### Gate de saída da Fase 10

```text
PIPELINE-EXTRACTION = PASS
CLI-EXTRACTION = PASS
```

## 21. Fase 11 — fachada pública

### 21.1 Política

O commit-base não possui `__all__`. Trinta nomes são acessados pelos testes,
mas o único consumidor operacional interno que precisa permanecer público é
`main`.

Durante as extrações:

- manter reexports necessários para compatibilidade transitória;
- migrar testes para os módulos proprietários;
- remover um reexport somente quando `rg` provar que não há consumidor interno.

A contração não é consequência automática da modularização. Antes de remover o
primeiro reexport:

1. exigir `BEH-07 = APPROVED`;
2. pesquisar consumidores internos, documentação operacional e integrações
   conhecidas;
3. registrar explicitamente que a pesquisa local não comprova a inexistência de
   consumidores externos;
4. criar `test_public_api_matches_beh_07`;
5. confirmar RED antes da contração e GREEN depois dela.

Estado final somente quando `BEH-07` aprovar a fachada mínima:

```python
"""Validador documental do CEPRAEA."""

from .cli import main

__all__ = ["main"]
```

Se `BEH-07` for rejeitado ou identificar consumidor externo aprovado, preservar
os reexports exigidos, documentar a fachada efetiva e ajustar o teste de
contrato. Nenhum símbolo pode desaparecer apenas porque `rg` não encontrou
consumidor no repositório.

### 21.2 Consumidores transitórios

| Símbolo usado pelos testes | Módulo proprietário final |
| --- | --- |
| `DEFAULT_REGISTRY` | `config` |
| `DEFAULT_WORKFLOW` | `config` |
| `GATE_RESULT_SCHEMA` | `config` |
| `JsonObject` | `json_types` |
| `Reporter` | `reporter` |
| `ValidatorArgs` | `models` |
| `WORKFLOW_SCHEMA` | `config` |
| `WORKSPACE_ROOT` | `config` |
| `as_json_array` | `json_types` |
| `as_json_object` | `json_types` |
| `dispatch_gate` | `gates.dispatcher` |
| `load_json` | `contracts` |
| `main` | `cli`, reexport público |
| `parse_front_matter` | `front_matter` |
| `resolve_document_version` | `registry` |
| `schema_validation_errors` | `contracts` |
| `validate_approval_cross_references` | `approvals` |
| `validate_cli_args` | `cli` |
| `validate_document_instances` | `instances` |
| `validate_feature_spec` | `front_matter` |
| `validate_front_matter` | `gates.g_fm` |
| `validate_g2` | `gates.g2` |
| `validate_gate_result_instances` | `instances` |
| `validate_governed` | `front_matter` |
| `validate_ingestion_consistency` | `ingestion` |
| `validate_links` | `links` |
| `validate_record` | `registry` |
| `validate_uniqueness` | `registry` |
| `validate_workflow_instance` | `instances` |
| `validate_workflow_references` | `workflow` |

### Gate de saída da Fase 11

```text
PUBLIC-FACADE = PASS
BEH-07-CONTRACT = PASS
```

## 22. Fase 12 — validação final

Executar:

```bash
python3 -m compileall -q \
  scripts/documentation/validate_documentation \
  scripts/documentation/tests \
  scripts/documentation/integration_tests

python3 -m unittest discover \
  -s scripts/documentation/tests \
  -t . \
  -v

python3 -m unittest discover \
  -s scripts/documentation/integration_tests \
  -t . \
  -v

npx --yes pyright@1.1.411 \
  --project pyrightconfig.json \
  --outputjson

python3 -m scripts.documentation.validate_documentation --help

npm run validate
```

Executar também todos os gates da Fase 2 e comparar com a baseline.

Verificações estruturais:

```bash
rg 'sys\.path\.(insert|append)' scripts/documentation/tests
rg 'import validate_documentation|from validate_documentation' \
  scripts/documentation
rg '^def |^class ' \
  scripts/documentation/validate_documentation/__init__.py
```

Esperado:

- nenhuma alteração dinâmica de `sys.path` nos testes;
- nenhum import curto;
- nenhuma implementação no `__init__.py`;
- ausência de ciclos;
- fachada pública corresponde exatamente à decisão `BEH-07`;
- 45 funções-base rastreadas até módulos proprietários;
- 3 classes-base rastreadas;
- 49 patches migrados;
- nenhuma invocação de Pyright sem a versão `1.1.411`;
- `npm run validate` aprovado;
- funções complexas documentam o porquê das decisões não evidentes;
- outputs semanticamente equivalentes, salvo mudanças autorizadas;
- README e mapa coerentes com a arquitetura final.

O relatório final deve repetir que as quatro limitações da seção 3.3 permanecem
abertas e que este gate não declara prontidão para uso bloqueante em produção.

### 22.1 Auditoria do próprio plano

Executar:

```bash
npx markdownlint-cli2 \
  .inicio/PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md

rg 'npx --yes pyright([[:space:]]|$)' \
  .inicio/PLANO-MODULARIZACAO-VALIDATE-DOCUMENTATION.md
```

O segundo comando deve retornar zero ocorrências. Recontar os inventários por
AST e busca estrutural, sem confiar apenas nos números escritos no plano.

Aceitação:

```text
45 funções de topo
3 classes de topo
92 métodos de teste na baseline
49 ocorrências de patch.object
13 grupos de alvos de patch
0 invocações de Pyright sem versão fixa
0 problemas de Markdownlint
```

Se o código-base mudar, atualizar conjuntamente commit-base, linhas históricas,
inventários e testes esperados; não corrigir apenas os totais.

### 22.2 Gate final

```text
MODULARIZATION-VALIDATE-DOCUMENTATION = PASS
NPM-PROJECT-VALIDATION = PASS
```

## 23. Inventário completo: função atual → módulo futuro

Inventário extraído por AST do commit-base. As linhas são âncoras históricas e
deixarão de ser estáveis após as movimentações.

| Nº | Linha-base | Função atual | Módulo futuro | Fase |
| ---: | ---: | --- | --- | ---: |
| 1 | 23 | `_accept_dynamic_value` | `json_types.py` | 4 |
| 2 | 28 | `_accept_dynamic_mapping` | `json_types.py` | 4 |
| 3 | 33 | `as_json_object` | `json_types.py` | 4 |
| 4 | 45 | `_accept_dynamic_array` | `json_types.py` | 4 |
| 5 | 50 | `as_json_array` | `json_types.py` | 4 |
| 6 | 221 | `parse_args` | `cli.py` | 10 |
| 7 | 265 | `validate_cli_args` | `cli.py` | 10 |
| 8 | 280 | `workspace_path` | `filesystem.py` | 4 |
| 9 | 290 | `sha256` | `filesystem.py` | 4 |
| 10 | 298 | `valid_name` | `registry.py` | 6 |
| 11 | 310 | `validate_top_level` | `registry.py` | 6 |
| 12 | 332 | `resolve_document_version` | `registry.py` | 6 |
| 13 | 383 | `validate_record` | `registry.py` | 6 |
| 14 | 492 | `validate_uniqueness` | `registry.py` | 6 |
| 15 | 518 | `managed_files` | `registry.py` | 6 |
| 16 | 531 | `normalize_link_target` | `links.py` | 8 |
| 17 | 555 | `validate_links` | `links.py` | 8 |
| 18 | 578 | `validate_canonical_registry` | `registry.py` | 6 |
| 19 | 605 | `load_json` | `contracts.py` | 6 |
| 20 | 613 | `validate_schema_definition` | `contracts.py` | 6 |
| 21 | 627 | `schema_validation_errors` | `contracts.py` | 6 |
| 22 | 642 | `validate_contract_schemas` | `contracts.py` | 6 |
| 23 | 653 | `validate_document_instances` | `instances.py` | 7 |
| 24 | 671 | `validate_workflow_instance` | `instances.py` | 7 |
| 25 | 710 | `validate_gate_result_instances` | `instances.py` | 7 |
| 26 | 744 | `validate_evidence_instances` | `instances.py` | 7 |
| 27 | 814 | `validate_instances` | `instances.py` | 7 |
| 28 | 825 | `validate_approval_cross_references` | `approvals.py` | 7 |
| 29 | 1029 | `validate_yaml_instance` | `contracts.py` | 6 |
| 30 | 1061 | `validate_provenance_packages` | `provenance.py` | 7 |
| 31 | 1111 | `validate_workflow_references` | `workflow.py` | 7 |
| 32 | 1227 | `ingestion_records` | `ingestion.py` | 7 |
| 33 | 1239 | `validate_ingestion_consistency` | `ingestion.py` | 7 |
| 34 | 1395 | `validate_g0` | `gates/g0.py` | 9 |
| 35 | 1429 | `validate_g1` | `gates/g1.py` | 9 |
| 36 | 1539 | `validate_garch` | `gates/g_arch.py` | 9 |
| 37 | 1564 | `validate_g2` | `gates/g2.py` | 9 |
| 38 | 1858 | `parse_front_matter` | `front_matter.py` | 8 |
| 39 | 1939 | `validate_governed` | `front_matter.py` | 8 |
| 40 | 2017 | `validate_feature_spec` | `front_matter.py` | 8 |
| 41 | 2022 | `validate_front_matter` | `gates/g_fm.py` | 9 |
| 42 | 2062 | `load_registry` | `registry.py` | 6 |
| 43 | 2081 | `validate_registry_integrity` | `registry.py` | 6 |
| 44 | 2111 | `dispatch_gate` | `gates/dispatcher.py` | 9 |
| 45 | 2134 | `main` | `cli.py`; corpo para `pipeline.run_validation` | 10 |

### 23.1 Classes

| Linha-base | Classe atual | Conteúdo | Módulo futuro | Fase |
| ---: | --- | --- | --- | ---: |
| 135 | `ValidatorArgs` | namespace tipado da CLI | `models.py` | 4 |
| 147 | `Reporter` | `__init__`, `error`, `warning`, `emit` | `reporter.py` | 5 |
| 1835 | `_DuplicateKeyLoader` | `construct_mapping` | `front_matter.py` | 8 |

### 23.2 Constantes e aliases

| Grupo atual | Módulo futuro |
| --- | --- |
| `JsonObject` | `json_types.py` |
| `WORKSPACE_ROOT`, `DEFAULT_REGISTRY`, `DEFAULT_WORKFLOW`, `SCHEMA_ROOT`, paths de schemas, `INTEGRITY_MANIFEST`, paths de Front Matter | `config.py` |
| `MANAGED_SUFFIXES`, `NAME_RE`, `SCHEMA_NAME_RE`, `EXPECTED_PATH_RE`, `REQUIRED_FIELDS` | `registry.py` |
| `MARKDOWN_LINK_RE`, `LINE_REFERENCE_RE` | `links.py` |
| `GLOBAL_GATES` | `cli.py` |
| `_FM_EXCLUSIONS` e glob de feature specs | `front_matter.py` |

### 23.3 Funções novas autorizadas

| Função nova | Módulo | Justificativa |
| --- | --- | --- |
| `find_workspace_root(start: Path \| None = None) -> Path` | `config.py` | substituir dependência estrutural de `parents[3]` em subciclo comportamental |
| `run_validation(args: ValidatorArgs, reporter: Reporter) -> None` | `pipeline.py` | separar orquestração documental da validação da CLI e da emissão única |

## 24. Inventário completo: patch atual → namespace futuro

Prefixo canônico omitido na coluna futura:

```text
scripts.documentation.validate_documentation.
```

As 13 linhas agrupam todas as 49 ocorrências. A soma da coluna “Qtd.” deve
permanecer 49 até que cada ocorrência seja migrada.

| Alvo atual | Qtd. | Ocorrências no commit-base | Namespace futuro |
| --- | ---: | --- | --- |
| `validator.DEFAULT_WORKFLOW` | 1 | `test_instances.py:34` — `test_invalid_workflow_instance_fails` | `config.DEFAULT_WORKFLOW` |
| `validator.INTEGRITY_MANIFEST` | 1 | `test_workflow_and_ingestion.py:175` — `_run` | `config.INTEGRITY_MANIFEST` |
| `validator.WORKSPACE_ROOT` | 6 | `test_approvals.py:116` — `_run`; `test_cli_and_resolution.py:123` — `_validate`; `test_instances.py:55` — `test_invalid_gate_result_instance_fails`; `test_registry_invariants.py:85` — `_validate_record`; `test_scoped_gates.py:107` — `_run`; `test_workflow_and_ingestion.py:174` — `_run` | `config.WORKSPACE_ROOT` |
| `validator.dispatch_gate` | 4 | `test_main_pipeline.py:90` — `test_main_stops_before_gate_when_registry_stage_fails`; `:121` — `test_main_stops_before_links_when_gate_fails`; `:173` — `test_main_uses_exact_scoped_record`; `:214` — `test_global_gate_emits_null_document_metadata` | `gates.dispatcher.dispatch_gate` |
| `validator.load_registry` | 5 | `test_main_pipeline.py:44` — `test_main_stops_before_files_when_contract_stage_fails`; `:78` — `test_main_stops_before_gate_when_registry_stage_fails`; `:112` — `test_main_stops_before_links_when_gate_fails`; `:164` — `test_main_uses_exact_scoped_record`; `:205` — `test_global_gate_emits_null_document_metadata` | `registry.load_registry` |
| `validator.parse_args` | 5 | `test_main_pipeline.py:43` — `test_main_stops_before_files_when_contract_stage_fails`; `:77` — `test_main_stops_before_gate_when_registry_stage_fails`; `:111` — `test_main_stops_before_links_when_gate_fails`; `:159` — `test_main_uses_exact_scoped_record`; `:204` — `test_global_gate_emits_null_document_metadata` | `cli.parse_args` |
| `validator.validate_canonical_registry` | 3 | `test_main_pipeline.py:120` — `test_main_stops_before_links_when_gate_fails`; `:172` — `test_main_uses_exact_scoped_record`; `:213` — `test_global_gate_emits_null_document_metadata` | `registry.validate_canonical_registry` |
| `validator.validate_contract_schemas` | 5 | `test_main_pipeline.py:49` — `test_main_stops_before_files_when_contract_stage_fails`; `:83` — `test_main_stops_before_gate_when_registry_stage_fails`; `:117` — `test_main_stops_before_links_when_gate_fails`; `:169` — `test_main_uses_exact_scoped_record`; `:210` — `test_global_gate_emits_null_document_metadata` | `contracts.validate_contract_schemas` |
| `validator.validate_garch` | 1 | `test_main_pipeline.py:233` — `test_garch_has_explicit_dispatch` | `gates.g_arch.validate_garch` |
| `validator.validate_instances` | 5 | `test_main_pipeline.py:54` — `test_main_stops_before_files_when_contract_stage_fails`; `:84` — `test_main_stops_before_gate_when_registry_stage_fails`; `:118` — `test_main_stops_before_links_when_gate_fails`; `:170` — `test_main_uses_exact_scoped_record`; `:211` — `test_global_gate_emits_null_document_metadata` | `instances.validate_instances` |
| `validator.validate_links` | 3 | `test_main_pipeline.py:126` — `test_main_stops_before_links_when_gate_fails`; `:178` — `test_main_uses_exact_scoped_record`; `:215` — `test_global_gate_emits_null_document_metadata` | `links.validate_links` |
| `validator.validate_registry_integrity` | 5 | `test_main_pipeline.py:55` — `test_main_stops_before_files_when_contract_stage_fails`; `:85` — `test_main_stops_before_gate_when_registry_stage_fails`; `:119` — `test_main_stops_before_links_when_gate_fails`; `:171` — `test_main_uses_exact_scoped_record`; `:212` — `test_global_gate_emits_null_document_metadata` | `registry.validate_registry_integrity` |
| `validator.Reporter.emit` | 5 | `test_main_pipeline.py:59` — `test_main_stops_before_files_when_contract_stage_fails`; `:94` — `test_main_stops_before_gate_when_registry_stage_fails`; `:127` — `test_main_stops_before_links_when_gate_fails`; `:179` — `test_main_uses_exact_scoped_record`; `:216` — `test_global_gate_emits_null_document_metadata` | `reporter.Reporter.emit` |

### 24.1 Forma de patch esperada

```python
from unittest.mock import patch

from scripts.documentation.validate_documentation import (
    config,
    contracts,
    instances,
    links,
    registry,
    reporter,
)
from scripts.documentation.validate_documentation.gates import (
    dispatcher,
    g_arch,
)


with (
    patch.object(config, "WORKSPACE_ROOT", root),
    patch.object(registry, "load_registry", return_value=(data, documents)),
    patch.object(contracts, "validate_contract_schemas"),
    patch.object(instances, "validate_instances"),
    patch.object(dispatcher, "dispatch_gate"),
    patch.object(links, "validate_links"),
    patch.object(reporter.Reporter, "emit", return_value=0),
):
    ...
```

### 24.2 Momento de migração

- patches de `config` migram na Fase 4;
- patch de `Reporter.emit` migra na Fase 5;
- patches de `contracts` e `registry` migram na Fase 6;
- patch de `instances` migra na Fase 7;
- patch de `links` migra na Fase 8;
- patches de dispatcher e G-ARCH migram na Fase 9;
- `parse_args` migra na Fase 10.

Não migrar um patch antes de o código consumidor consultar o novo namespace.

## 25. Política de interrupção

Parar imediatamente quando:

- o gate da fase anterior não estiver aprovado;
- um teste anteriormente verde ficar vermelho em extração estrutural;
- Pyright produzir novo diagnóstico;
- output normalizado de gate mudar sem autorização;
- API transitória desaparecer antes da migração de consumidores;
- patch atingir alias em vez do módulo consultado;
- surgir ciclo de importação;
- `find_workspace_root` selecionar raiz diferente da esperada;
- TAR estiver ausente ou com hash divergente;
- mudança lógica não tiver contrato;
- mais de uma responsabilidade comportamental mudar no mesmo change set;
- surgir nova modificação não relacionada, ou uma alteração classificada na
  Fase -1 mudar inesperadamente;
- qualquer comando Git mutável exigir autorização não concedida.

Ao interromper:

1. não executar `git reset --hard` ou `git checkout --`;
2. preservar diff e logs;
3. registrar a última fase aprovada;
4. registrar comando, código de saída e erro;
5. solicitar decisão.

## 26. Política de commits e pull request

Sem autorização para implementar este plano:

- gerar evidências;
- não alterar código ou configuração;
- não criar commit, tag, push ou pull request.

Quando a implementação for autorizada:

- cumprir `GIT-WORKFLOW-READY` antes da primeira alteração;
- um commit exclusivo para governança;
- um commit exclusivo para identidade canônica;
- um commit por extração estrutural;
- um commit separado por correção comportamental;
- nunca misturar baseline com primeira extração;
- nunca misturar múltiplos gates em uma extração.
- não adicionar mudanças preexistentes não relacionadas;
- publicar a branch e entregar por pull request;
- tratar impossibilidade de push ou abertura do pull request como bloqueio de
  entrega, não como tarefa concluída;
- nunca criar tag, usar force-push ou reescrever histórico como parte deste
  plano.

Mensagens sugeridas:

```text
docs(documentation): autorizar plano de modularização do validador
test(documentation): adotar identidade canônica do pacote
refactor(documentation): extrair tipos JSON do validador
refactor(documentation): extrair configuração do validador
refactor(documentation): extrair Reporter do validador
fix(documentation): <correção comportamental autorizada>
```

## 27. Definição de pronto

A modularização está concluída somente quando:

- Fases -1–12 estão aprovadas;
- `GIT-WORKFLOW-READY = PASS`;
- `BEH-01` a `BEH-07` possuem decisão e evidência;
- os três TARs possuem hashes exatos;
- baseline inicial e resultado final estão preservados;
- 92 testes unitários passam ou a alteração de contagem está explicada;
- a integração do repositório passa;
- Pyright estrito possui zero diagnósticos;
- todas as invocações de Pyright usam `1.1.411`;
- `npm run validate` passa na baseline, após cada change set aplicável e no
  resultado final;
- todos os gates aplicáveis passam;
- outputs não autorizados não mudaram;
- as 45 funções possuem módulo proprietário;
- as 3 classes possuem módulo proprietário;
- os 49 patches foram migrados;
- nenhum teste altera `sys.path`;
- nenhum import curto permanece;
- não existem ciclos;
- `__init__.py` corresponde ao contrato aprovado em `BEH-07`;
- `__main__.py` contém somente a entrada;
- `main(argv)` e `parse_args(argv)` são testáveis;
- `pipeline.run_validation(args, reporter)` retorna `None`, não importa a CLI e
  não emite resultados;
- a resolução de escopo ocorre antes de contratos e instâncias;
- funções complexas explicam o porquê das decisões técnicas com docstrings ou
  comentários inline;
- README e mapa refletem a arquitetura real;
- planos históricos continuam preservados;
- as quatro limitações residuais continuam explicitamente abertas;
- a branch específica foi publicada e entregue por pull request;
- nenhuma mudança não relacionada foi incluída na entrega.

## 28. Fontes verificáveis

- [Repositório `cepraea/beach-pro`](https://github.com/cepraea/beach-pro)
- [Commit-base `defaa043`](https://github.com/cepraea/beach-pro/commit/defaa0439e5163b159dfd18359dd31cc65f469f4)
- [Implementação monolítica](https://github.com/cepraea/beach-pro/blob/main/scripts/documentation/validate_documentation/__init__.py)
- [README operacional](https://github.com/cepraea/beach-pro/blob/main/scripts/documentation/validate_documentation/README.md)
- [Mapa ativo](https://github.com/cepraea/beach-pro/blob/main/scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md)
- [Registro documental](https://github.com/cepraea/beach-pro/blob/main/docs/registry/registro-documentos.yaml)
- [Workflow documental](https://github.com/cepraea/beach-pro/blob/main/docs/registry/workflow-documentacao.yaml)
- [Configuração Pyright](https://github.com/cepraea/beach-pro/blob/main/pyrightconfig.json)
- [Pylance: imports não resolvidos](https://github.com/microsoft/pylance-release/blob/main/docs/howto/unresolved-imports.md)
- [Python: onde aplicar patch](https://docs.python.org/3/library/unittest.mock.html#where-to-patch)
- [Python: pacotes](https://docs.python.org/3/tutorial/modules.html#packages)
- [Python: `__main__`](https://docs.python.org/3/library/__main__.html)
