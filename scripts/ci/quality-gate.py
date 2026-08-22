#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${QUALITY_GATE_BASE:-origin/main}"

fail() {
  printf '\nQUALITY_GATE=FAIL\n' >&2
  exit 1
}

trap fail ERR

section() {
  printf '\n== %s ==\n' "$1"
}

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'ERRO: ferramenta obrigatória ausente: %s\n' "$1" >&2
    return 1
  fi
}

# ---------------------------------------------------------------------------
# Ambiente
# ---------------------------------------------------------------------------

section "Environment"

require git
require node
require python3
require prettier
require markdownlint-cli2
require pyright
require mypy

printf 'node:              %s\n' "$(node --version)"
printf 'python:            %s\n' "$(python3 --version 2>&1)"
printf 'prettier:          %s\n' "$(prettier --version)"
printf 'markdownlint-cli2: %s\n' "$(markdownlint-cli2 --version | head -n 1)"
printf 'pyright:           %s\n' "$(pyright --version)"
printf 'mypy:              %s\n' "$(mypy --version)"

python3 - <<'PY'
import pydantic
print("pydantic:          " + pydantic.__version__)
PY

# ---------------------------------------------------------------------------
# Determina arquivos alterados
#
# Inclui:
# - commits da feature em relação à main
# - alterações ainda não staged
# - alterações staged
#
# Não varre indiscriminadamente todo o legado do repositório.
# ---------------------------------------------------------------------------

section "Changed files"

declare -a changed_files=()

if git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  while IFS= read -r file; do
    [[ -n "$file" ]] && changed_files+=("$file")
  done < <(
    {
      git diff --name-only --diff-filter=ACMRT "$BASE_REF"...HEAD
      git diff --name-only --diff-filter=ACMRT
      git diff --cached --name-only --diff-filter=ACMRT
    } | sort -u
  )
else
  printf 'ERRO: base Git não encontrada: %s\n' "$BASE_REF" >&2
  exit 1
fi

# Mantém somente arquivos que ainda existem.
declare -a existing_files=()

for file in "${changed_files[@]}"; do
  if [[ -f "$file" ]]; then
    existing_files+=("$file")
    printf '%s\n' "$file"
  fi
done

if [[ ${#existing_files[@]} -eq 0 ]]; then
  printf 'Nenhum arquivo alterado aplicável.\n'
fi

# ---------------------------------------------------------------------------
# Classificação
# ---------------------------------------------------------------------------

declare -a prettier_files=()
declare -a markdown_files=()
declare -a python_files=()

for file in "${existing_files[@]}"; do
  case "$file" in
    *.md)
      markdown_files+=("$file")
      prettier_files+=("$file")
      ;;
    *.json|*.jsonc|*.yaml|*.yml|*.js|*.mjs|*.cjs|*.ts|*.tsx|*.css|*.scss|*.html)
      prettier_files+=("$file")
      ;;
    *.py)
      python_files+=("$file")
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Prettier
# ---------------------------------------------------------------------------

section "Prettier"

if [[ ${#prettier_files[@]} -gt 0 ]]; then
  prettier --check "${prettier_files[@]}"
else
  printf 'SKIP: nenhum arquivo aplicável.\n'
fi

# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

section "Markdownlint"

if [[ ${#markdown_files[@]} -gt 0 ]]; then
  markdownlint-cli2 "${markdown_files[@]}"
else
  printf 'SKIP: nenhum Markdown alterado.\n'
fi

# ---------------------------------------------------------------------------
# Python syntax
# ---------------------------------------------------------------------------

section "Python syntax"

if [[ ${#python_files[@]} -gt 0 ]]; then
  python3 -m py_compile "${python_files[@]}"
else
  printf 'SKIP: nenhum Python alterado.\n'
fi

# ---------------------------------------------------------------------------
# Pyright / Pylance engine
# ---------------------------------------------------------------------------

section "Pyright"

if [[ ${#python_files[@]} -gt 0 ]]; then
  pyright "${python_files[@]}"
else
  printf 'SKIP: nenhum Python alterado.\n'
fi

# ---------------------------------------------------------------------------
# mypy + Pydantic
# ---------------------------------------------------------------------------

section "mypy / Pydantic"

if [[ ${#python_files[@]} -gt 0 ]]; then
  mypy "${python_files[@]}"
else
  printf 'SKIP: nenhum Python alterado.\n'
fi

# ---------------------------------------------------------------------------
# Control plane CEPRAEA
# ---------------------------------------------------------------------------

section "Control plane"

if [[ -f .ai/control/validate-control-plane.mjs ]]; then
  node .ai/control/validate-control-plane.mjs
else
  printf 'ERRO: validator canônico não encontrado.\n' >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Git whitespace integrity
# ---------------------------------------------------------------------------

section "Git diff check"

git diff --check
git diff --cached --check

printf '\nQUALITY_GATE=PASS\n'