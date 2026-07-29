#!/usr/bin/env python3
"""Guardrail determinístico para Claude Code. Não usa API externa."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def emit(decision: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))


def normalize_path(value: str, cwd: str) -> Path:
    p = Path(value)
    if not p.is_absolute():
        p = Path(cwd) / p
    try:
        return p.resolve()
    except OSError:
        return p.absolute()


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(f"Hook inválido: não foi possível ler JSON: {exc}", file=sys.stderr)
        return 2

    tool = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input") or {}
    cwd = str(payload.get("cwd") or ".")
    project = Path(cwd).resolve()

    if tool in {"Bash", "PowerShell"}:
        command = str(tool_input.get("command", "")).strip()
        compact = re.sub(r"\s+", " ", command).lower()

        deny_rules = [
            (r"(^|[;&|]\s*)rm\s+-[^\n]*r[^\n]*f|rm\s+-rf", "remoção recursiva forçada"),
            (r"\bformat(\.com)?\b|\bmkfs(\.\w+)?\b", "formatação de disco"),
            (r"\bdd\s+if=", "gravação direta em dispositivo"),
            (r"\bshutdown\b|\breboot\b|\bpoweroff\b", "desligamento/reinicialização"),
            (r"\bsudo\b|\brunas\b", "elevação de privilégio"),
            (r"chmod\s+(-r\s+)?777\b", "permissão 777"),
            (r"git\s+(reset\s+--hard|clean\s+-[^\n]*f)", "descarte destrutivo de alterações Git"),
            (r"git\s+push[^\n]*(--force|-f)\b", "push forçado"),
            (r"(curl|wget)[^\n]*\|\s*(sh|bash|zsh|pwsh|powershell)", "execução direta de script remoto"),
            (r"\b(drop\s+(database|schema|table)|truncate\s+table)\b", "operação destrutiva em banco"),
        ]
        for pattern, label in deny_rules:
            if re.search(pattern, compact, flags=re.I):
                emit("deny", f"Bloqueado pelo guardrail: {label}. Proponha uma alternativa reversível.")
                return 0

        ask_rules = [
            (r"\bgit\s+push\b", "envio para repositório remoto"),
            (r"\b(npm|pnpm|yarn|pip|pip3|poetry|uv|cargo|go)\s+(install|add|get)\b", "instalação de dependências"),
            (r"\b(terraform\s+apply|kubectl\s+apply|helm\s+(install|upgrade)|vercel\s+--prod)\b", "alteração de infraestrutura/deploy"),
            (r"\b(alembic\s+upgrade|prisma\s+migrate|rails\s+db:migrate|sequelize\s+db:migrate)\b", "migração de banco"),
            (r"\b(npm\s+publish|twine\s+upload|cargo\s+publish)\b", "publicação de pacote"),
        ]
        for pattern, label in ask_rules:
            if re.search(pattern, compact, flags=re.I):
                emit("ask", f"Confirmação obrigatória: {label}. Revise o comando e o destino.")
                return 0

        return 0

    if tool in {"Write", "Edit", "NotebookEdit"}:
        raw_path = (
            tool_input.get("file_path")
            or tool_input.get("notebook_path")
            or tool_input.get("path")
            or ""
        )
        if not raw_path:
            return 0

        target = normalize_path(str(raw_path), cwd)
        try:
            relative = target.relative_to(project).as_posix().lower()
        except ValueError:
            emit("ask", f"O agente quer alterar um arquivo fora do projeto: {target}")
            return 0

        protected_exact = {
            ".env", ".env.local", ".env.production",
            "id_rsa", "id_ed25519", "credentials.json",
        }
        protected_prefixes = (
            ".git/", "secrets/", "credentials/",
            "infra/prod/", "infrastructure/prod/", "terraform/prod/",
        )
        name = target.name.lower()

        if name in protected_exact or relative.startswith(protected_prefixes):
            emit("deny", f"Arquivo/diretório protegido: {relative}. Faça a mudança manualmente após revisão.")
            return 0

        sensitive_patterns = (
            "docker-compose.prod", "compose.prod",
            "production.yml", "production.yaml",
            "deploy-prod", "prod.tfvars",
        )
        if any(token in relative for token in sensitive_patterns):
            emit("ask", f"Alteração sensível requer confirmação: {relative}")
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
