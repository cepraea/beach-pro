# Política de tradução controlada de documentação técnica

## Identidade normativa

| Campo | Valor |
| --- | --- |
| ID | `POL-TRAD-001` |
| Versão | `1.0.0-rc.1` |
| Status | `CANDIDATA_EM_VALIDACAO` |
| Autoridade | `docs/governance/policies/tradutor.md` e decisão humana de promoção |
| Idioma-alvo | `pt-BR` |
| Parser | `markdown-it@14.3.0`, preset `default`, `html=true`, `breaks=false`, `linkify=false`, `typographer=false` |

Esta política governa exclusivamente a tradução de linguagem natural. Correção, modernização, adaptação de plataforma, atualização factual e refatoração são operações separadas e não podem ser ocultadas em um diff de tradução.

## Autoridade e dependência

A dependência normativa é unidirecional:

```text
registro mestre → tradutor.md → política → perfil individual → manifesto → evidências
```

Perfis podem restringir a política, mas não relaxar seus gates. Evidências descrevem uma execução e não criam regras.

## Política de idioma canônico

A promoção para português brasileiro é uma mudança breaking. Após aprovação e corte atômico:

- o arquivo ativo canônico usa português brasileiro e não possui sufixo de idioma;
- a origem japonesa ou inglesa permanece recuperável por Git, URL imutável e SHA-256;
- nenhuma segunda cópia normativa ativa é permitida;
- o corte somente ocorre quando todo o conjunto interdependente estiver aprovado.

## Segmentação e classificação

A origem deve ser UTF-8 estrito, fixada por SHA-256 e processada pelo parser fixado. Os segmentos devem cobrir todos os bytes do blob, sem lacunas nem sobreposição.

| Classe | Tratamento |
| --- | --- |
| `PROTECTED_EXACT` | Congelar e restaurar byte a byte |
| `TRANSLATABLE_CONTROLLED` | Traduzir conforme glossário e perfil |
| `MARKDOWN_SYNTAX` | Preservar estrutura e delimitadores |
| `AMBIGUOUS` | Encerrar como `BLOCKED` |

Frontmatter YAML é classificado por campo: chaves, tipos, `name`, `tools` e `model` são protegidos; somente o valor de `description` é traduzível. Em Mermaid, Gherkin, YAML, JSON e Markdown exemplificativo, a sintaxe e os identificadores permanecem protegidos; apenas rótulos humanos explicitamente autorizados são traduzíveis.

## Congelamento e placeholders

Placeholders somente podem existir na cópia de trabalho. A origem nunca é modificada. Colisão, ausência, duplicidade ou mudança do valor protegido resultam em `BLOCKED`.

## Equivalência

A aprovação exige simultaneamente:

1. equivalência estrutural;
2. preservação dos contratos protegidos;
3. preservação das relações entre arquivos;
4. rastreabilidade proposição a proposição;
5. ausência de adições sem fonte e de fontes sem destino;
6. revisão bilíngue independente;
7. aprovação humana vinculada ao hash.

Tradução reversa isolada não é prova suficiente.

## Hierarquia de ownership

```text
regras documentais §11
  → agent-list.md (projeção consolidada)
    → S3 Ownership dos prompts (projeção operacional)
```

Divergência entre as três camadas bloqueia a promoção. A tradução não corrige divergências preexistentes; registra-as para decisão separada.

## Gates

- `G-TRAD-01`: fonte fixada e proveniência íntegra;
- `G-TRAD-02`: cobertura de bytes e classificação total;
- `G-TRAD-03`: placeholders restaurados exatamente;
- `G-TRAD-04`: sintaxe e estrutura equivalentes;
- `G-TRAD-05`: contratos individuais equivalentes;
- `G-TRAD-06`: contratos coletivos equivalentes;
- `G-TRAD-07`: cobertura semântica bidirecional de 100%;
- `G-TRAD-08`: revisão bilíngue independente;
- `G-TRAD-09`: aprovação humana;
- `G-TRAD-10`: corte atômico e ausência de fontes concorrentes.

Falha em qualquer gate impede a promoção.
