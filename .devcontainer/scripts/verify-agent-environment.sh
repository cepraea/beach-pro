#!/usr/bin/env bash
## Verificação do ambiente BASE do agente CEPRAEA.
##
## Adaptações ao ambiente real em relação ao documento de arquitetura:
##   - CLAUDE_GUARD aponta para /usr/local/lib/cepraea-guards/pretool
##   - CODEX_CONFIG verifica .codex/config.toml (projeto) e /etc/codex/requirements.toml (sistema)
##   - Usuário esperado: agent (não vscode)
##
## Referência arquitetural:
##   .drive/multi-agentes/Arquivos-Human-Governed Dual-Agent SDLC Architecture.md (seção 9)

set -u

FAILURES=0
WARNINGS=0

REPO="/workspaces/cepraea-beach-pro"
SOURCE_ROOT="$REPO/.drive/CEPRAEA BEACH PRO"
CLAUDE_POLICY="/etc/claude-code/managed-settings.json"
CLAUDE_GUARD="/usr/local/lib/cepraea-guards/pretool"
CODEX_CONFIG_PROJECT="$REPO/.codex/config.toml"
CODEX_CONFIG_SYSTEM="/etc/codex/requirements.toml"


pass() { printf 'PASS  %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; FAILURES=$((FAILURES + 1)); }
warn() { printf 'WARN  %s\n' "$1"; WARNINGS=$((WARNINGS + 1)); }


echo "CEPRAEA Agent Environment Verification"
echo "======================================="


## ------------------------------------------------------------
## User
## ------------------------------------------------------------

if [ "$(id -u)" -ne 0 ]; then
    pass "container session is non-root"
else
    fail "container session is running as root"
fi


## ------------------------------------------------------------
## Docker socket
## ------------------------------------------------------------

if [ ! -S /var/run/docker.sock ]; then
    pass "Docker socket is not mounted"
else
    fail "Docker socket is available inside the container"
fi


## ------------------------------------------------------------
## Repository / Git
## ------------------------------------------------------------

if cd "$REPO" 2>/dev/null; then
    pass "repository is accessible"
else
    fail "repository is not accessible at $REPO"
fi


if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    pass "Git repository detected"
else
    fail "Git repository not detected"
fi


## ------------------------------------------------------------
## SOURCE_ROOT
## ------------------------------------------------------------

if [ -d "$SOURCE_ROOT" ]; then
    pass "SOURCE_ROOT exists"
else
    fail "SOURCE_ROOT not found at: $SOURCE_ROOT"
fi


if command -v findmnt >/dev/null 2>&1 && [ -e "$SOURCE_ROOT" ]; then
    OPTIONS="$(findmnt -T "$SOURCE_ROOT" -n -o OPTIONS 2>/dev/null || true)"
    if printf '%s' "$OPTIONS" | tr ',' '\n' | grep -qx 'ro'; then
        pass "SOURCE_ROOT is mounted read-only"
    else
        fail "SOURCE_ROOT is not confirmed read-only via findmnt"
    fi
else
    if [ -w "$SOURCE_ROOT" ]; then
        fail "SOURCE_ROOT appears writable"
    else
        pass "SOURCE_ROOT is not writable by current user"
    fi
fi


## ------------------------------------------------------------
## Claude managed policy
## ------------------------------------------------------------

if [ -f "$CLAUDE_POLICY" ]; then
    pass "Claude managed settings installed"
else
    fail "Claude managed settings missing at: $CLAUDE_POLICY"
fi


if [ -x "$CLAUDE_GUARD" ]; then
    pass "Claude guard installed and executable"
else
    fail "Claude guard missing or not executable at: $CLAUDE_GUARD"
fi


if [ -f "$CLAUDE_POLICY" ]; then
    OWNER="$(stat -c '%U' "$CLAUDE_POLICY" 2>/dev/null || true)"
    MODE="$(stat -c '%a' "$CLAUDE_POLICY" 2>/dev/null || true)"

    if [ "$OWNER" = "root" ]; then
        pass "Claude managed settings owned by root"
    else
        fail "Claude managed settings are not root-owned (owner: $OWNER)"
    fi

    case "$MODE" in
        444|640|644)
            pass "Claude managed settings mode is $MODE (acceptable)"
            ;;
        *)
            warn "Claude managed settings mode is $MODE; expected 444"
            ;;
    esac
fi


## ------------------------------------------------------------
## Codex
## ------------------------------------------------------------

if [ -f "$CODEX_CONFIG_PROJECT" ]; then
    pass "Codex project config exists (.codex/config.toml)"
else
    warn "Codex project config missing at: $CODEX_CONFIG_PROJECT"
fi

if [ -f "$CODEX_CONFIG_SYSTEM" ]; then
    pass "Codex system config exists (/etc/codex/requirements.toml)"
else
    fail "Codex system config missing at: $CODEX_CONFIG_SYSTEM"
fi


## ------------------------------------------------------------
## Obvious production credentials
## ------------------------------------------------------------

FORBIDDEN_VARS=(
    "GITHUB_TOKEN"
    "GH_TOKEN"
    "SUPABASE_SERVICE_ROLE_KEY"
    "VERCEL_TOKEN"
)

for name in "${FORBIDDEN_VARS[@]}"; do
    val="${!name:-}"
    if [ -n "$val" ]; then
        fail "forbidden privileged credential is present: $name"
    else
        pass "credential not exposed: $name"
    fi
done


## ------------------------------------------------------------
## Result
## ------------------------------------------------------------

echo
echo "Failures: $FAILURES"
echo "Warnings: $WARNINGS"

if [ "$FAILURES" -eq 0 ]; then
    echo "BASE_CONTAINER_CHECK=PASS"
    exit 0
else
    echo "BASE_CONTAINER_CHECK=FAIL"
    exit 1
fi
