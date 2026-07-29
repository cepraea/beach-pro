# Evidência de qualificação da especificação VSCODE

## 1. Identificação

| Campo | Valor |
| --- | --- |
| Baseline | ESP-CEPRAEA-VSCODE-001 v1.0.0 |
| Data da execução | 2026-07-28 |
| Executor automatizado | Codex |
| Diretório | `/home/davis/projetos/cepraea-beach-pro` |
| Estado do repositório | Baseline Git criada em 2026-07-29; remote configurado em `https://github.com/cepraea/beach-pro` |
| Resultado | Qualificação automatizada aprovada; qualificação manual pendente |

## 2. Ambiente observado

| Elemento | Resultado | Estado |
| --- | --- | --- |
| Sistema | WSL 2, kernel `6.6.87.2-microsoft-standard-WSL2` | Aprovado |
| Node.js | 24.14.1 via NVM no Linux | Aprovado |
| npm | 11.11.0 no Linux | Aprovado |
| Processadores no WSL | 4 | Aprovado |
| Memória visível no WSL | 7,5 GiB | Aprovado para mínimo de 8 GB físicos informado no inventário |
| Swap visível | 2,0 GiB | Informativo |
| Sistema de arquivos | Projeto sob `/home/davis/projetos` | Aprovado |
| Espaço no volume Linux | 911 GB disponíveis na execução | Aprovado no Linux |
| Espaço na unidade Windows | Não verificável por esta execução | Pendente manual |
| Docker | Comando indisponível no Ubuntu | Não aplicável ao fluxo principal |

## 3. Resultados automatizados

| Verificação | Resultado | Estado |
| --- | --- | --- |
| `npm ci` | 621 pacotes instalados; lockfile utilizado | Aprovado |
| `npm run lint` | Código zero | Aprovado |
| `npm run lint:md:vscode` | Zero ocorrências em dois arquivos | Aprovado |
| `npm run quality:workspace` | “Validação do Workspace aprovada” | Aprovado |
| `npm run typecheck` | Código zero | Aprovado |
| `npm run test` | 1 arquivo e 1 teste aprovados | Aprovado |
| `npm run build` | Build Vite e geração PWA concluídos | Aprovado |
| `npm run format:check` | Todos os arquivos no escopo conformes | Aprovado |
| `npm audit --omit=dev` | Zero vulnerabilidades | Aprovado |
| `npm run lint:md` | 1.414 ocorrências preexistentes | Desvio DV-VSC-001 |
| `npm audit` | 10 vulnerabilidades altas somente em desenvolvimento | Desvio DV-VSC-002 |

## 4. PWA

| Verificação | Evidência | Estado |
| --- | --- | --- |
| Manifesto | `dist/manifest.webmanifest` gerado | Aprovado |
| Service worker | `dist/sw.js` e Workbox gerados | Aprovado |
| Registro | `dist/registerSW.js` gerado | Aprovado |
| Ícone 192 | PNG RGBA de 192 × 192; HTTP 200 no servidor local | Aprovado |
| Ícone 512 | PNG RGBA de 512 × 512; HTTP 200 no servidor local | Aprovado |
| Atualização | `registerType: 'autoUpdate'` na fonte canônica | Aprovado por inspeção |
| Fluxos de negócio offline | Não implementados | Pendente por escopo |

Os ícones foram produzidos deterministicamente por
`scripts/assets/generate-pwa-icons.mjs`. A regeneração é feita por `npm run assets:pwa`.

## 5. Servidor e navegador automatizado

| Verificação | Resultado | Estado |
| --- | --- | --- |
| Servidor Vite | Porta 5173, endereço local e endereço de rede apresentados | Aprovado |
| HTTP local | `curl` obteve o HTML com sucesso | Aprovado |
| Conteúdo renderizado | `CEPRAEA Beach Pro` | Aprovado |
| Título | `CEPRAEA Beach Pro` | Aprovado |
| Página em branco | Não | Aprovado |
| Overlay de erro | Ausente | Aprovado |
| Erros capturados no console | Nenhum | Aprovado |
| Screenshot | Gerado pela automação de navegador | Aprovado |

## 6. Segurança

| Verificação | Resultado | Estado |
| --- | --- | --- |
| `.env` ignorado | Regra confirmada em `.gitignore` | Aprovado |
| `.env.local` ignorado | Regra confirmada em `.gitignore` | Aprovado |
| Chaves privadas e tokens conhecidos | Nenhuma ocorrência confirmada na revisão automatizada | Aprovado |
| `service_role` no contrato público | Ausente | Aprovado |
| Auditoria de produção | Zero vulnerabilidades | Aprovado |

## 7. Validações manuais pendentes

| ID | Validação | Motivo |
| --- | --- | --- |
| MAN-VSC-001 | Confirmar o VS Code instalado no Windows e conectado ao WSL | Requer interface do Windows |
| MAN-VSC-002 | Confirmar extensões instaladas no lado WSL | Requer interface do VS Code |
| MAN-VSC-003 | Executar F5 e atingir breakpoint TypeScript | Requer Chrome e VS Code |
| MAN-VSC-004 | Confirmar espaço livre na unidade Windows | Requer consulta ao hospedeiro |
| MAN-VSC-005 | Testar acesso por celular em rede privada | Requer dispositivo físico |
| MAN-VSC-006 | Testar instalação e atualização da PWA | Requer navegador compatível e interação |
| MAN-VSC-007 | Aprovar ou rejeitar os desvios propostos | Requer autoridade do proprietário |
| MAN-VSC-008 | Registrar proprietário nominal e aprovador | Requer decisão humana |

## 8. Status das ações do relatório

| Ações | Resultado |
| --- | --- |
| A-01 | Parcial: controle criado; identificação nominal e aprovação pendentes |
| A-02 a A-07 | Executadas |
| A-08 | Executada: arquivos canônicos referenciados sem cópias concorrentes |
| A-09 a A-10 | Executadas: estado separado e legado preservado |
| A-11 a A-17 | Executadas |
| A-18 | Parcial: configuração consolidada; breakpoint manual pendente |
| A-19 a A-22 | Executadas |
| A-23 a A-27 | Executadas |
| A-28 | Executada documentalmente; aprovação dos desvios pendente |
| A-29 a A-30 | Executadas |
| A-31 | Parcial: instalação e validação automatizadas aprovadas; etapas físicas pendentes |
| A-32 | Pendente: revisão e aprovação independentes exigem outra autoridade |

## 9. Conclusão

A baseline automatizada está aprovada. A baseline Git foi criada em 2026-07-29 (MAN-VSC-009
executada). O estado da especificação permanece “Em qualificação” porque os testes manuais,
a aprovação independente e os desvios ainda não foram concluídos.

Nenhuma validação pendente foi apresentada como aprovada.
