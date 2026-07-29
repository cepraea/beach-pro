# Plano de migração do validador documental para pacote Python

## 1. Identificação

| Campo | Valor |
| --- | --- |
| Implementação atual | `scripts/documentation/validate_documentation/__init__.py` |
| Diretório do pacote | `scripts/documentation/validate_documentation/` |
| Pacote | `scripts.documentation.validate_documentation` |
| Mapa atual | `scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md` |
| Comando canônico | `python3 -m scripts.documentation.validate_documentation` |
| Estratégia | Migração compatível em duas etapas |
| Suíte de proteção | `scripts/documentation/tests/` |
| Verificação estática | Pyright `strict` |
| Estado | Migração concluída; Etapas 1 e 2 verdes |

## 2. Objetivo

Mover a implementação do validador para
`scripts/documentation/validate_documentation/` sem:

- manter duas implementações concorrentes;
- interromper imediatamente consumidores do caminho antigo;
- alterar o comportamento dos gates;
- perder a API usada pelos testes;
- separar o mapa de manutenção do código que ele orienta;
- reescrever evidências históricas;
- introduzir a modularização funcional no mesmo conjunto de mudanças;
- incorporar Python ao pipeline npm ou à imagem Docker sem decisão própria.

Ao final, o entrypoint operacional será:

```bash
python3 -m scripts.documentation.validate_documentation
```

## 3. Decisão arquitetural

### 3.1 Estrutura da Etapa 1

```text
scripts/documentation/
├── validate_documentation.py
└── validate_documentation/
    ├── MAPA-VALIDADOR-DOC.md
    ├── README.md
    ├── __init__.py
    └── __main__.py
```

Responsabilidades:

- `validate_documentation/__init__.py`: única implementação do validador;
- `validate_documentation/__main__.py`: entrypoint fino que chama `main()`;
- `validate_documentation.py`: encaminhador temporário e sem regras de negócio;
- `MAPA-VALIDADOR-DOC.md`: mapa de intervenção colocado junto ao código;
- `README.md`: contrato operacional, transição entre comandos e catálogo dos
  testes.

### 3.2 Estrutura final da Etapa 2

```text
scripts/documentation/
└── validate_documentation/
    ├── MAPA-VALIDADOR-DOC.md
    ├── README.md
    ├── __init__.py
    └── __main__.py
```

O arquivo `validate_documentation.py` deixa de existir somente depois que todos
os consumidores operacionais utilizarem o módulo.

### 3.3 Por que a implementação ficará inicialmente em `__init__.py`

Os testes importam `validate_documentation` e modificam constantes do módulo com
`patch.object()`. Colocar imediatamente as funções em `core.py` e apenas
reexportá-las pelo pacote faria os testes alterarem o namespace do pacote, mas
não necessariamente os globais consultados pelas funções definidas em
`core.py`.

Manter a implementação em `__init__.py` nesta migração:

- preserva a API atual;
- preserva os mocks e fixtures;
- evita novos imports internos;
- permite provar que a movimentação é puramente estrutural;
- adia a divisão funcional para um plano independente.

## 4. Regras de qualidade e limites

Regras de Qualidade: O código **DEVE** ser autoexplicativo, mas cada função
complexa deve conter *docstrings* ou *comentários inline* voltados para outros
desenvolvedores ou agentes de IA. Comentar o "porquê" de decisões técnicas para
mitigar erros em futuras manutenções.

Esta migração:

- **NÃO DEVE** modificar regras de validação;
- **NÃO DEVE** dividir gates ou helpers em novos módulos funcionais;
- **NÃO DEVE** introduzir Pydantic;
- **NÃO DEVE** alterar schemas;
- **NÃO DEVE** adicionar o validador a `npm run validate`;
- **NÃO DEVE** instalar Python no Docker;
- **NÃO DEVE** substituir caminhos dentro de evidências históricas;
- **NÃO DEVE** persistir resultado `RUNTIME` como nova evidência;
- **DEVE** manter uma única implementação;
- **DEVE** manter o mapa e o README junto ao pacote;
- **DEVE** fazer o README identificar a suíte funcional e os testes próprios
  da migração;
- **DEVE** preservar os 72 testes existentes;
- **DEVE** manter Pyright strict com zero diagnóstico.

A restrição anterior de não mover o script, registrada no plano de correção do
validador, aplicava-se àquela execução já concluída. Este plano autoriza somente
a movimentação estrutural aqui descrita; as demais regras de qualidade
continuam vigentes.

## 5. Inventário de impacto

### 5.1 Arquivos alterados na Etapa 1

| Arquivo | Ação |
| --- | --- |
| `scripts/documentation/validate_documentation.py` | Reduzir a encaminhador temporário |
| `scripts/documentation/validate_documentation/__init__.py` | Receber a implementação atual |
| `scripts/documentation/validate_documentation/__main__.py` | Criar entrypoint do módulo |
| `.inicio/MAPA-VALIDADOR-DOC.md` | Mover para o diretório do pacote |
| `scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md` | Tornar-se o mapa canônico junto ao código |
| `scripts/documentation/validate_documentation/README.md` | Documentar comando novo, compatibilidade e testes |
| `scripts/documentation/tests/test_package_entrypoints.py` | Criar testes de migração |
| `pyrightconfig.json` | Incluir pacote, encaminhador e testes |
| `.inicio/Plano-validator.md` | Atualizar o destino do mapa e registrar que a restrição de movimentação foi superada |

### 5.2 Arquivos alterados na Etapa 2

| Arquivo | Ação |
| --- | --- |
| `scripts/documentation/validate_documentation.py` | Remover encaminhador |
| `docs/registry/workflow-documentacao.yaml` | Migrar quatro comandos para `python3 -m` |
| `docs/README.md` | Migrar comandos operacionais |
| `docs/registry/registro-documentos.yaml` | Atualizar versões e hashes controlados |
| `scripts/documentation/validate_documentation/README.md` | Remover instrução de compatibilidade e consolidar testes |
| `scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md` | Consolidar comandos finais |
| `.inicio/Plano-validator.md` | Registrar entrypoint sucessor |
| `pyrightconfig.json` | Remover inclusão do encaminhador antigo |
| Testes de entrypoint | Rejeitar retorno do caminho antigo |

### 5.3 Arquivos que não devem mudar

| Arquivo ou grupo | Motivo |
| --- | --- |
| `package.json` | O pipeline npm não executa o validador Python |
| `package-lock.json` | Nenhuma dependência npm muda |
| `Dockerfile` | A imagem Node não passa a executar Python |
| `docker-compose.yml` | O Compose não despacha o validador |
| `.inicio/VSCODE.md` | A baseline VS Code/Node permanece separada |
| Schemas em `docs/contracts/schemas/` | A forma dos artefatos não muda |
| Aprovações existentes | IDs, decisões e hashes aprovados não mudam |
| Pacotes de proveniência | A migração não altera documentos comprovados |

### 5.4 Referências históricas preservadas

Não executar substituição global em:

- 34 arquivos existentes em `docs/evidence/gates/` cujo `evaluator` registra
  `scripts/documentation/validate_documentation.py`;
- `docs/evidence/integrity/divergencia-relatorio-validacao-contexto-v01.yaml`,
  cujo `detected_by` registra o caminho antigo;
- `docs/validation/reports/relatorio-auditoria-acervo.md`, que documenta comando
  executado no passado;
- arquivos `HISTORICO-*` e snapshots editoriais;
- decisões canônicas que citam `validate_documentation.py` como nome histórico
  do componente.

Essas referências descrevem o executor existente na data da evidência.
Reescrevê-las alteraria os bytes históricos e criaria uma remediação de hashes
sem mudança factual correspondente.

## 6. Invariantes obrigatórias

1. `WORKSPACE_ROOT` continua apontando para a raiz do repositório.
2. Todos os schemas continuam sendo encontrados sob `docs/contracts/schemas/`.
3. O registro padrão continua sendo
   `docs/registry/registro-documentos.yaml`.
4. `import validate_documentation` continua expondo a mesma API na Etapa 1.
5. O encaminhador não contém regra documental.
6. O comando antigo e o novo retornam o mesmo código e os mesmos achados na
   Etapa 1.
7. O comando antigo deixa de existir na Etapa 2.
8. G-ARCH, G0 e G1 continuam globais.
9. G2 e G-FM continuam resolvendo `(document_id, version)`.
10. Resultados novos usam uma identidade lógica do pacote.
11. Evidências históricas mantêm a identidade antiga.
12. O mapa canônico fica em `validate_documentation/MAPA-VALIDADOR-DOC.md`.
13. O README lista os testes existentes, o teste de migração e os comandos para
    executá-los.

## 7. Etapa 1 — Introduzir o pacote com compatibilidade

### 7.1 Pré-condições

Executar e registrar a baseline:

```bash
python3 -m unittest discover -s scripts/documentation/tests -q
npx --yes pyright
python3 scripts/documentation/validate_documentation.py --format text
python3 scripts/documentation/validate_documentation.py \
  --gate G-ARCH \
  --format text
```

Resultado esperado:

- 72 testes verdes;
- Pyright com zero diagnóstico;
- validação global verde;
- G-ARCH verde.

### 7.2 Testes vermelhos

Criar `scripts/documentation/tests/test_package_entrypoints.py` antes de mover a
implementação.

Os testes devem proteger:

1. `test_module_entrypoint_exists`:
   a resolução ainda aponta para `validate_documentation.py`, em vez de
   `validate_documentation/__init__.py`, e o pacote não possui `__main__.py`;
2. `test_package_exports_main`:
   a API continua expondo `main`;
3. `test_package_workspace_root_is_repository_root`:
   a raiz calculada continua sendo a raiz do repositório;
4. `test_legacy_and_module_entrypoints_are_equivalent`:
   os dois entrypoints permanecem equivalentes durante a compatibilidade;
5. `test_package_contains_single_implementation`:
   a implementação ainda reside no arquivo legado.
6. `test_maintenance_map_is_colocated_with_package`:
   o mapa ainda reside em `.inicio/`;
7. `test_package_readme_documents_tests`:
   o README ainda não identifica o teste de entrypoint e seu comando de
   execução.

Falha por dependência ausente, fixture incorreta ou diretório de execução errado
não constitui vermelho válido.

Antes da migração, os testes especificamente vermelhos devem ser os de origem
do módulo, implementação única, localização do mapa e identidade do avaliador.
Os demais funcionam como guardas verdes de comportamento que não pode regredir
durante a movimentação.

### 7.3 Mover a implementação

1. Criar `validate_documentation/__init__.py`.
2. Mover integralmente a implementação atual para esse arquivo.
3. Não reorganizar funções durante a movimentação.
4. Não alterar mensagens, opções ou regras.
5. Remover o shebang do corpo movido ou mantê-lo somente no entrypoint quando
   houver utilidade real.

### 7.4 Corrigir a raiz do workspace

O arquivo atual usa:

```python
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
```

No pacote, a profundidade muda. Ajustar para:

```python
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
```

O comentário ou teste deve explicar que a mudança é consequência da nova
profundidade física, não uma alteração do workspace autorizado.

### 7.5 Criar `__main__.py`

O entrypoint deve apenas importar e executar `main()`:

```python
from . import main


if __name__ == "__main__":
    raise SystemExit(main())
```

Nenhuma regra de negócio pode ser adicionada a `__main__.py`.

### 7.6 Transformar o arquivo antigo em encaminhador

`scripts/documentation/validate_documentation.py` deve:

- importar `main` do pacote adjacente;
- chamar `main()` somente sob `if __name__ == "__main__"`;
- emitir, no máximo, aviso de depreciação em `stderr` se houver decisão
  explícita para isso;
- não duplicar constantes, funções ou classes;
- não alterar a saída processável por padrão.

Para não quebrar consumidores YAML, a opção recomendada é não imprimir aviso
durante a Etapa 1. A depreciação deve ser documentada no README.

### 7.7 Preservar a API dos testes

Os nove módulos existentes devem continuar podendo usar:

```python
import validate_documentation as validator
```

e:

```python
from validate_documentation import Reporter
```

Não alterar todos os imports apenas para acomodar a movimentação. O pacote deve
preservar a API já testada.

### 7.8 Atualizar a identidade de novas execuções

Alterar somente o valor produzido por novas execuções do Reporter para uma
identidade estável, por exemplo:

```text
scripts.documentation.validate_documentation
```

Não alterar resultados de gate já persistidos.

Adicionar teste:

- `test_new_result_uses_package_evaluator_identity`.

### 7.9 Atualizar Pyright

Durante a compatibilidade, `pyrightconfig.json` deve incluir:

```json
[
  "scripts/documentation/validate_documentation",
  "scripts/documentation/validate_documentation.py",
  "scripts/documentation/tests"
]
```

O modo `strict` e `pythonVersion: 3.10` permanecem inalterados.

### 7.10 Atualizar documentação não governada

Atualizar:

- README interno do validador;
- mapa do validador;
- nota pós-execução do plano anterior.

Mover:

```text
.inicio/MAPA-VALIDADOR-DOC.md
→ scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md
```

Após o movimento:

- o README deve apontar para `MAPA-VALIDADOR-DOC.md` por link relativo local;
- `.inicio/Plano-validator.md` deve apontar para o novo destino;
- não deve permanecer uma segunda cópia ativa em `.inicio/`;
- referências retrospectivas que apenas registram o caminho anterior podem
  permanecer quando estiverem claramente identificadas como históricas.

Documentar:

- comando canônico novo;
- comando antigo temporariamente suportado;
- data ou condição para retirada;
- estrutura do pacote;
- proibição de manter duas implementações.

O README deve conter uma seção de testes com:

- comando da suíte completa;
- relação dos nove módulos funcionais existentes e seus escopos;
- `scripts/documentation/tests/test_package_entrypoints.py` como proteção
  estrutural da migração;
- comando para executar apenas os testes de entrypoint;
- verificações de sintaxe do pacote e do encaminhador durante a Etapa 1;
- comando do Pyright;
- indicação de que vermelho válido falha pela regra sob correção e verde válido
  inclui o teste localizado e a suíte completa.

Não atualizar ainda `docs/README.md` nem o workflow processável.

### 7.11 Testes verdes da Etapa 1

Executar:

```bash
python3 -m compileall -q \
  scripts/documentation/validate_documentation

python3 -m py_compile \
  scripts/documentation/validate_documentation.py

python3 -m unittest discover -s scripts/documentation/tests -q
python3 -m unittest \
  scripts.documentation.tests.test_package_entrypoints
npx --yes pyright

python3 scripts/documentation/validate_documentation.py --help
python3 -m scripts.documentation.validate_documentation --help
```

Executar pelos dois entrypoints:

```bash
python3 scripts/documentation/validate_documentation.py --format text
python3 -m scripts.documentation.validate_documentation --format text

python3 scripts/documentation/validate_documentation.py \
  --gate G-FM \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1.1 \
  --format text

python3 -m scripts.documentation.validate_documentation \
  --gate G-FM \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1.1 \
  --format text
```

Comparar:

- códigos de saída;
- conjunto ordenado de erros e avisos;
- resumo;
- metadados de documento e versão.

Para YAML, normalizar ou ignorar apenas `evaluated_at`. Nenhum outro campo pode
divergir.

### 7.12 Critérios de aceitação da Etapa 1

- pacote executável com `python3 -m`;
- caminho antigo ainda funcional;
- uma única implementação;
- mapa canônico movido para junto do pacote;
- links para o mapa atualizados;
- README identifica testes funcionais e testes de migração;
- API dos testes preservada;
- `WORKSPACE_ROOT` correto;
- nenhuma regra documental alterada;
- suíte completa verde;
- strict-mode verde;
- validação global e gates com paridade;
- nenhum arquivo governado em `docs/` alterado;
- `package.json`, lockfile, Docker, Compose e VSCODE inalterados.

### 7.13 Rollback da Etapa 1

Se qualquer critério falhar:

1. restaurar a implementação integral em `validate_documentation.py`;
2. remover somente `__init__.py`, `__main__.py` e os testes específicos da
   migração;
3. devolver `MAPA-VALIDADOR-DOC.md` para `.inicio/` e restaurar seus links;
4. restaurar o README e o `pyrightconfig.json`;
5. executar a baseline novamente.

Como nenhum documento governado é alterado nesta etapa, o rollback não exige
remediação de hashes.

### 7.14 Registro da execução da Etapa 1

Etapa executada em 2026-07-29.

Baseline anterior à movimentação:

- 72 testes verdes;
- Pyright strict: zero erro, aviso ou informação;
- validação global: `errors=0 warnings=0`;
- G-ARCH: `errors=0 warnings=0`.

Teste vermelho criado antes do patch:

- oito testes estruturais e comportamentais executados;
- quatro falhas esperadas:
    - origem ainda em `validate_documentation.py`;
    - implementação ainda no arquivo legado;
    - mapa ainda em `.inicio/`;
    - identidade antiga do avaliador.

Resultado após o patch:

- implementação única em
  `scripts/documentation/validate_documentation/__init__.py`;
- `__main__.py` fino e encaminhador legado sem regra documental;
- mapa movido para junto do pacote e cópia antiga removida;
- README atualizado com comandos, compatibilidade e catálogo de testes;
- 80 testes verdes, incluindo os oito testes de migração;
- `compileall` do pacote e `py_compile` do encaminhador verdes;
- Pyright strict: zero erro, aviso ou informação;
- Markdownlint: zero ocorrência nos quatro documentos alterados;
- validação global e G-FM localizado verdes pelos dois entrypoints;
- saídas textuais idênticas entre os entrypoints;
- saída YAML idêntica após remover somente `evaluated_at`;
- identidade de novas execuções:
  `scripts.documentation.validate_documentation`;
- nenhum documento governado em `docs/` alterado nesta etapa;
- Etapa 2 não iniciada.

## 8. Etapa 2 — Migrar consumidores e retirar compatibilidade

### 8.1 Pré-condições

A Etapa 2 só pode começar quando:

- todos os critérios da Etapa 1 estiverem verdes;
- o comando de módulo tiver sido usado em uma execução completa;
- não houver consumidor externo conhecido dependente do arquivo antigo;
- workflow e README puderem ser atualizados atomicamente com o registro;
- os hashes atuais dos documentos governados tiverem sido registrados.

### 8.2 Testes vermelhos

Adicionar ou ajustar testes para demonstrar:

1. `test_workflow_uses_module_entrypoint`:
   o workflow ainda aponta para o arquivo antigo;
2. `test_operational_docs_use_module_entrypoint`:
   `docs/README.md` ainda ensina o comando antigo;
3. `test_no_active_reference_uses_legacy_entrypoint`:
   ainda existem referências operacionais fora da lista histórica permitida;
4. `test_legacy_entrypoint_is_removed`:
   o encaminhador antigo ainda existe;
5. `test_historical_evaluator_references_are_preserved`:
   uma substituição global indevida deve ser detectada.
6. `test_maintenance_map_has_no_active_legacy_location`:
   nenhuma instrução vigente deve depender do mapa em `.inicio/`;
7. `test_package_readme_documents_final_test_commands`:
   o README não pode ensinar testes pelo entrypoint removido.

### 8.3 Migrar o workflow processável

Nos quatro gates, substituir:

```yaml
command:
  - python3
  - scripts/documentation/validate_documentation.py
```

por:

```yaml
command:
  - python3
  - -m
  - scripts.documentation.validate_documentation
```

Aplicar a G-ARCH, G0, G1 e G-FM.

Como o comando processável muda materialmente:

1. elevar `workflow.version` de `0.2.2` para `0.2.3`;
2. elevar a versão do registro `DOC-REG-WF-DOCUMENTACAO` para `0.2.3`;
3. recalcular o SHA-256 do workflow;
4. atualizar seu `content_hash` no registro;
5. não criar aprovação, pois o registro permanece em `RASCUNHO`;
6. validar o workflow contra seu schema e suas referências internas.

### 8.4 Migrar `docs/README.md`

Substituir somente comandos operacionais vigentes pelo módulo.

Como o documento muda:

1. elevar o Front Matter de `0.2.1` para `0.2.2`;
2. elevar a versão do registro `DOC-REG-ENTRADA-DOCUMENTACAO` para `0.2.2`;
3. recalcular o SHA-256;
4. atualizar o `content_hash` no registro;
5. preservar estado `RASCUNHO`;
6. executar G-FM para a nova versão.

Não alterar o relatório inicial de auditoria, pois seu comando é histórico.

### 8.5 Atualizar documentação do validador

Atualizar:

- README interno;
- mapa já movido para
  `scripts/documentation/validate_documentation/MAPA-VALIDADOR-DOC.md`;
- plano anterior, apenas com nota de sucessão;
- este plano, registrando a execução.

Os comandos finais devem usar exclusivamente:

```bash
python3 -m scripts.documentation.validate_documentation
```

### 8.6 Remover o encaminhador

Remover `scripts/documentation/validate_documentation.py` somente depois de:

- workflow atualizado;
- README operacional atualizado;
- hashes atualizados;
- testes pelo módulo verdes;
- busca de referências ativas aprovada.

O pacote passa a ser o único entrypoint.

### 8.7 Consolidar Pyright

Remover o arquivo antigo da configuração. A inclusão final deve cobrir:

```json
[
  "scripts/documentation/validate_documentation",
  "scripts/documentation/tests"
]
```

### 8.8 Auditoria de referências

Executar busca:

```bash
rg -n \
  --hidden \
  --glob '!node_modules/**' \
  --glob '!.git/**' \
  'scripts/documentation/validate_documentation\.py'
```

Classificar cada ocorrência remanescente.

Ocorrências permitidas:

- evidências de gate históricas;
- divergência de integridade histórica;
- relatório de auditoria histórico;
- arquivos `HISTORICO-*`;
- texto deste plano ao descrever o caminho legado.

Ocorrências bloqueantes:

- workflow processável;
- README operacional vigente;
- Pyright;
- testes que executem o arquivo antigo;
- scripts de automação ativos;
- tarefas do editor;
- instruções atuais do mapa;
- links vigentes para `.inicio/MAPA-VALIDADOR-DOC.md`.

### 8.9 Ordem de atualização dos hashes

Executar atomicamente:

1. editar workflow, README e suas versões;
2. calcular os hashes definitivos:

   ```bash
   sha256sum \
     docs/README.md \
     docs/registry/workflow-documentacao.yaml
   ```

3. atualizar no registro somente:
   - versão e hash de `DOC-REG-ENTRADA-DOCUMENTACAO`;
   - versão e hash de `DOC-REG-WF-DOCUMENTACAO`;
4. não calcular hash do registro para si mesmo, pois ele é
   `self_hash_exempt`;
5. não modificar hashes de evidências históricas;
6. executar o validador antes de produzir qualquer nova evidência.

### 8.10 Testes verdes da Etapa 2

```bash
python3 -m compileall -q \
  scripts/documentation/validate_documentation

python3 -m unittest discover -s scripts/documentation/tests -q
npx --yes pyright

python3 -m scripts.documentation.validate_documentation --format text
python3 -m scripts.documentation.validate_documentation \
  --gate G-ARCH \
  --format text
python3 -m scripts.documentation.validate_documentation \
  --gate G0 \
  --format text
python3 -m scripts.documentation.validate_documentation \
  --gate G1 \
  --format text
python3 -m scripts.documentation.validate_documentation \
  --gate G2 \
  --document-id DOC-CEPRAEA-CANDIDATA-CONTEXTO \
  --version 0.1 \
  --format text
python3 -m scripts.documentation.validate_documentation \
  --gate G-FM \
  --document-id DOC-REG-ENTRADA-DOCUMENTACAO \
  --version 0.2.2 \
  --format text
```

Também executar as verificações de não impacto:

```bash
npm run quality:workspace
npm run lint:md:vscode
```

Docker permanece opcional. Se disponível:

```bash
docker compose config
```

### 8.11 Critérios de aceitação da Etapa 2

- arquivo antigo removido;
- comando de módulo é o único entrypoint operacional;
- workflow usa `python3 -m` nos quatro gates;
- README vigente usa o módulo;
- mapa reside junto ao pacote e não possui cópia ativa em `.inicio/`;
- README enumera a suíte funcional e os testes de migração;
- versões e hashes controlados atualizados;
- nenhuma evidência histórica modificada;
- todos os testes verdes;
- Pyright strict verde;
- validação global verde;
- G-ARCH, G0, G1, G2 no escopo coberto e G-FM verdes;
- nenhum consumidor ativo aponta para o arquivo removido;
- arquivos npm, lock, Docker, Compose e VSCODE continuam inalterados;
- documentação e implementação concordam.

### 8.12 Rollback da Etapa 2

Se qualquer verificação falhar:

1. restaurar o encaminhador;
2. restaurar atomicamente:
   - comandos e versão do workflow;
   - comandos e versão de `docs/README.md`;
   - versões e hashes anteriores no registro;
3. manter o pacote da Etapa 1, já validado;
4. executar os dois entrypoints;
5. não tocar nas evidências históricas.

O rollback retorna ao estado compatível da Etapa 1, não ao monólito anterior.

### 8.13 Registro da execução da Etapa 2

Etapa executada em 2026-07-29.

Baseline anterior ao corte:

- 80 testes verdes;
- Pyright strict sem diagnósticos;
- validação global verde;
- hash anterior de `docs/README.md`:
  `8c840e0d711ecdeaffcee58ee59ec93b9df9ecfae096bc9bf69fd4caf6f9bd27`;
- hash anterior do workflow:
  `1a87bcba8ff4c2269a1018764fa66038cca27151aec5b2a493f50bb456405831`;
- 34 resultados de gate preservavam a identidade histórica do avaliador.

Teste vermelho criado antes da alteração dos consumidores:

- 16 testes estruturais, operacionais e de metadados executados;
- 13 falhas esperadas cobriram:
    - versões e hashes anteriores;
    - quatro comandos antigos no workflow;
    - comandos antigos no README governado;
    - referências antigas no mapa e README interno;
    - inclusão do encaminhador no Pyright;
    - presença física do encaminhador.

Alterações governadas:

- `docs/README.md`: versão `0.2.1` para `0.2.2`;
- `DOC-REG-ENTRADA-DOCUMENTACAO`: versão sincronizada em `0.2.2`;
- hash definitivo do README:
  `4ed088772e3db7ec470be41b3fe1f0472638e0feff52fd9c42f8396cc49474e7`;
- `workflow-documentacao.yaml`: versão `0.2.2` para `0.2.3`;
- `DOC-REG-WF-DOCUMENTACAO`: versão sincronizada em `0.2.3`;
- hash definitivo do workflow:
  `b8761f48dc0a5fc45380f2070d3cc8381b1a778d970afc155519ee113eb4b7ad`;
- os dois registros permaneceram em `RASCUNHO`, sem criação de aprovação.

Resultado final:

- encaminhador `scripts/documentation/validate_documentation.py` removido;
- pacote é a única implementação e o único entrypoint operacional;
- quatro gates do workflow usam `python3 -m`;
- README governado e documentação interna usam o módulo;
- Pyright inclui somente pacote e testes;
- 88 testes verdes, incluindo 16 testes da migração;
- Pyright strict: zero erro, aviso ou informação;
- `compileall` verde;
- validação global, G-ARCH, G0, G1, G2 no escopo `0.1` e G-FM do README
  `0.2.2` verdes;
- Markdownlint sem ocorrências nos cinco documentos verificados;
- `npm run quality:workspace` verde;
- `npm run lint:md:vscode` verde;
- 34 evidências de gate, a divergência de integridade e o relatório de
  auditoria mantêm os bytes e a identidade histórica;
- referências antigas remanescentes fora de `docs/` estão limitadas a
  históricos, propostas congeladas/não autorizadas, este plano e constantes
  negativas dos testes;
- `package.json`, `package-lock.json`, `Dockerfile`, `docker-compose.yml` e
  `.inicio/VSCODE.md` não foram alterados;
- `docker compose config` não foi executado porque o binário `docker` não está
  instalado no ambiente; a verificação era opcional.

## 9. Matriz de testes

| Regra | Vermelho | Verde |
| --- | --- | --- |
| Pacote executável | `-m` não encontra `__main__` | `--help` retorna zero |
| API preservada | pacote não expõe símbolos | 72 testes existentes passam |
| Raiz correta | schemas procurados sob `scripts/docs` | raiz é o repositório |
| Implementação única | regras existem em dois arquivos | somente `__init__.py` contém regras |
| Compatibilidade | entrypoint antigo quebra na Etapa 1 | ambos produzem resultado equivalente |
| Workflow migrado | comando contém `.py` | quatro gates usam `-m` |
| Referências ativas | busca encontra caminho antigo vigente | somente históricos permanecem |
| Evidência histórica | substituição altera evaluator antigo | bytes históricos permanecem |
| Hashes | registro mantém hash anterior | hashes correspondem aos bytes finais |
| Retirada | encaminhador ainda existe | caminho antigo não existe |
| Mapa junto ao código | mapa permanece ativo em `.inicio/` | mapa canônico está no pacote |
| Testes no README | suíte ou entrypoints não são citados | módulos e comandos estão documentados |

## 10. Riscos e mitigações

| Risco | Impacto | Mitigação |
| --- | --- | --- |
| `WORKSPACE_ROOT` incorreto | Todos os caminhos falham | Teste explícito da raiz e `parents[3]` |
| Pacote e módulo com mesmo nome | Import ambíguo na transição | Testar import e manter pacote como fonte única |
| Duas implementações | Divergência silenciosa | Arquivo antigo contém somente encaminhamento |
| Mocks alteram namespace errado | Testes deixam de isolar filesystem | Implementação permanece em `__init__.py` |
| Consumidor externo usa `.py` | Quebra após Etapa 2 | Período compatível e busca antes da remoção |
| Substituição em evidência histórica | Cascata de hashes e perda de fidelidade | Lista explícita de referências permitidas |
| Workflow atualizado sem registro | Hash desatualizado | Mudança atômica com versão e SHA-256 |
| npm passa a depender de Python | Baseline deixa de ser reproduzível | Manter pipelines separados |
| Docker passa a executar Python sem contrato | Falha na imagem Alpine | Não integrar nesta migração |
| Modularização simultânea | Escopo e risco excessivos | Planejar divisão funcional posteriormente |

## 11. Definição de pronto

A migração está concluída somente quando:

- as duas etapas tiverem seus critérios atendidos;
- o pacote for a única implementação e o único entrypoint operacional;
- o caminho antigo permanecer apenas em registros históricos;
- a API usada pelos testes estiver preservada;
- os documentos governados alterados tiverem versões e hashes corretos;
- os 72 testes existentes e os novos testes de entrypoint estiverem verdes;
- Pyright strict estiver sem diagnósticos;
- os gates aplicáveis estiverem verdes;
- nenhuma alteração indevida tiver sido feita em npm, lockfile, Docker, Compose,
  VSCODE, schemas, aprovações ou proveniência.

## 12. Referências

- [Python: pacotes](https://docs.python.org/3/tutorial/modules.html#packages)
- [Python: `__main__`](https://docs.python.org/3/library/__main__.html)
- [Python: opção `-m`](https://docs.python.org/3/using/cmdline.html#cmdoption-m)
- [Python: `compileall`](https://docs.python.org/3/library/compileall.html)
- [Python: `unittest`](https://docs.python.org/3/library/unittest.html)
- [Pyright: configuração](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
