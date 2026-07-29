#!/usr/bin/env python3
"""Verifica o arquivo editado e devolve feedback ao Claude. Não envia dados para fora."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    ("chave privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token GitHub", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("possível segredo atribuído", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']"
    )),
]

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    raw_path = (
        tool_input.get("file_path")
        or tool_input.get("notebook_path")
        or tool_input.get("path")
        or ""
    )
    if not raw_path:
        return 0

    path = Path(str(raw_path))
    if not path.is_absolute():
        path = Path(payload.get("cwd") or ".") / path

    try:
        if not path.is_file() or path.stat().st_size > 2_000_000:
            return 0
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0

    findings = [label for label, pattern in SECRET_PATTERNS if pattern.search(text)]
    if findings:
        reason = (
            f"Verificação local encontrou possível(is) segredo(s) em {path.name}: "
            + ", ".join(findings)
            + ". Remova o valor, use variável de ambiente e não conclua a tarefa até corrigir."
        )
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
        return 0

    # Feedback leve para arquivos muito grandes; não bloqueia.
    if text.count("\n") > 1500:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    f"O arquivo {path.name} ultrapassou 1.500 linhas. "
                    "Considere modularização antes de concluir."
                )
            }
        }, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
