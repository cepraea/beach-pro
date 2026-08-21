# Verificação Formal FVR-1.0 — arquivado

**Arquivado em 2026-08-17.** Não priorizado.

Conteúdo original:
- `planejamento/` — GUIA 0 a 06 da "Implantação da Arquitetura Formal de Verificação e Assurance"
  (`docs/arquiteturas/assurance/planejamento/desenvolvendo/`), ~1.211 linhas.
- `runner/` — implementação candidata do FVR-1.0 (`.drive/FVR-1.0/`): contratos de tarefa com hash
  SHA-256, verificador determinístico, harness de conformidade Python, sandbox `bwrap` probado por
  `strace`, ~6.900 linhas incluindo `verify.sh` e `conformance_harness.py`.

**Por que foi arquivado:**
1. Nunca executou com sucesso neste ambiente — `runner/CONFORMANCE_CERTIFICATE_NOT_ISSUED.json`
   registra `certificate_issued: false`, `reason: HARNESS_INVALID` por dependências ausentes
   (`shellcheck`, `bwrap`, `strace`).
2. Propunha uma segunda camada de verificação formal sobre a arquitetura dual-agente
   (Claude EXECUTOR / Codex REVIEWER / Davi humano) que já existe e já está em uso — validada
   diretamente em produção de trabalho, não apenas em plano.
3. O nível de rigor (contratos formais com âncora criptográfica, álgebra fechada de propriedades
   TRUE/FALSE/UNKNOWN, publicação atômica com suíte de crash-consistency) é desproporcional ao
   estágio e à escala do CEPRAEA BEACH PRO — um PWA de gestão de time para 1 treinador e ~19 atletas.
4. Estava formalmente "PENDENTE DE DECISÃO HUMANA" desde a criação (GUIA 0), nunca aprovado.

**Condição para retomar:** só faz sentido revisitar se, no futuro, o projeto tiver escala, equipe ou
requisitos de compliance que justifiquem esse nível de rigor — e nesse caso, provavelmente vale
reconstruir calibrado ao problema real, não reativar este pacote como está.
