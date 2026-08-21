#!/usr/bin/env bash
# Verificação do ambiente BASE do agente CEPRAEA.
# Referência:
# docs/arquiteturas/multi-agentes/main/Human-Governed Dual-Agent SDLC Architecture.md

set -u
FAILURES=0
WARNINGS=0

REPO="/workspaces/cepraea-beach-pro"
SOURCE_ROOT="$REPO/.drive/CEPRAEA BEACH PRO"
CLAUDE_POLICY="/etc/claude-code/managed-settings.json"
CLAUDE_GUARD="/usr/local/lib/cepraea-guards/pretool"
CODEX_CONFIG_PROJECT="$REPO/.codex/config.toml"
CODEX_CONFIG_SYSTEM="/etc/codex/requirements.toml"
CONTROL_CONFIG="$REPO/.ai/control/control-plane.json"

pass(){ printf 'PASS  %s\n' "$1"; }
fail(){ printf 'FAIL  %s\n' "$1"; FAILURES=$((FAILURES+1)); }
warn(){ printf 'WARN  %s\n' "$1"; WARNINGS=$((WARNINGS+1)); }

echo "CEPRAEA Agent Environment Verification"
echo "======================================="

[ "$(id -u)" -ne 0 ] && pass "container session is non-root" || fail "container session is running as root"
[ ! -S /var/run/docker.sock ] && pass "Docker socket is not mounted" || fail "Docker socket is available inside the container"

if cd "$REPO" 2>/dev/null; then pass "repository is accessible"; else fail "repository is not accessible at $REPO"; fi
git rev-parse --is-inside-work-tree >/dev/null 2>&1 && pass "Git repository detected" || fail "Git repository not detected"

[ -d "$SOURCE_ROOT" ] && pass "SOURCE_ROOT exists" || fail "SOURCE_ROOT not found at: $SOURCE_ROOT"
if command -v findmnt >/dev/null 2>&1 && [ -e "$SOURCE_ROOT" ]; then
  OPTIONS="$(findmnt -T "$SOURCE_ROOT" -n -o OPTIONS 2>/dev/null || true)"
  printf '%s' "$OPTIONS" | tr ',' '\n' | grep -qx 'ro' && pass "SOURCE_ROOT is mounted read-only" || fail "SOURCE_ROOT is not confirmed read-only via findmnt"
elif [ -w "$SOURCE_ROOT" ]; then
  fail "SOURCE_ROOT appears writable"
else
  pass "SOURCE_ROOT is not writable by current user"
fi

[ -f "$CLAUDE_POLICY" ] && pass "Claude managed settings installed" || fail "Claude managed settings missing at: $CLAUDE_POLICY"
[ -x "$CLAUDE_GUARD" ] && pass "Claude guard installed and executable" || fail "Claude guard missing or not executable at: $CLAUDE_GUARD"

if [ -f "$CLAUDE_POLICY" ]; then
  OWNER="$(stat -c '%U' "$CLAUDE_POLICY" 2>/dev/null || true)"
  MODE="$(stat -c '%a' "$CLAUDE_POLICY" 2>/dev/null || true)"
  [ "$OWNER" = "root" ] && pass "Claude managed settings owned by root" || fail "Claude managed settings are not root-owned (owner: $OWNER)"
  case "$MODE" in
    444|640|644) pass "Claude managed settings mode is $MODE (acceptable)" ;;
    *) warn "Claude managed settings mode is $MODE; expected 444/640/644" ;;
  esac
fi

[ -f "$CODEX_CONFIG_PROJECT" ] && pass "Codex project config exists" || warn "Codex project config missing at: $CODEX_CONFIG_PROJECT"
[ -f "$CODEX_CONFIG_SYSTEM" ] && pass "Codex system config exists" || fail "Codex system config missing at: $CODEX_CONFIG_SYSTEM"
[ -f "$CONTROL_CONFIG" ] && pass "canonical control-plane config exists" || fail "control-plane config missing at: $CONTROL_CONFIG"

FORBIDDEN_VARS=("GITHUB_TOKEN" "GH_TOKEN" "SUPABASE_SERVICE_ROLE_KEY" "VERCEL_TOKEN")
for name in "${FORBIDDEN_VARS[@]}"; do
  val="${!name:-}"
  [ -n "$val" ] && fail "forbidden privileged credential is present: $name" || pass "credential not exposed: $name"
done

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
