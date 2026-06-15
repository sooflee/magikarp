#!/bin/bash
# Weekly driver for The Current Regime. Intended to be run by launchd.
#
# Flow: ingest sign-ups -> generate the issue (Claude, headless) -> build the
# archive -> commit/push -> send. By default it sends a PREVIEW to the owner
# only; set AUTO_SEND=1 to send to the full subscriber list.
#
# Secrets: the Gmail app password is read from the macOS Keychain. One-time setup:
#   security add-generic-password -s the-current-regime -a gmail -w 'APP PASSWORD'
#
# Env toggles:
#   GENERATE=0   skip the Claude generation step (just rebuild + send current issue)
#   AUTO_SEND=1  send to the whole subscriber list instead of a preview to the owner

set -uo pipefail
export PATH="/Users/benson/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(dirname "$0")" || exit 1

log() { echo "[$(date '+%F %T')] $*"; }

# --- secrets ---
PW="$(security find-generic-password -s the-current-regime -a gmail -w 2>/dev/null || true)"
export GMAIL_APP_PASSWORD="${PW:-${GMAIL_APP_PASSWORD:-}}"
if [ -z "${GMAIL_APP_PASSWORD:-}" ]; then
  log "ERROR: no Gmail app password in Keychain (service 'the-current-regime') or env"; exit 1
fi

# --- sign-ups ---
log "ingesting sign-ups"
python3 signups.py || log "signups step failed (continuing)"

# --- generate this week's issue ---
if [ "${GENERATE:-1}" = "1" ]; then
  log "generating issue via Claude (headless)"
  claude -p "Produce this week's issue of The Current Regime by following .claude/skills/current-regime/SKILL.md exactly. Do every data step, verify each factual claim with web search, write the new issue object into regime_state.json, append the ledger the-current-regime.md, then run 'python3 build_site.py'. Commit and push. Do NOT send any email; delivery is handled by this script." \
    --dangerously-skip-permissions --model claude-opus-4-8 2>&1 | tail -8 \
    || log "Claude generation failed (continuing with current state)"
fi

# --- build + publish the archive ---
log "building site"
python3 build_site.py || log "build_site failed"
git add -A && git commit -m "weekly run $(date '+%Y-%m-%d')" >/dev/null 2>&1 || true
if git push >/dev/null 2>&1; then log "pushed"; else log "push skipped/failed"; fi

# --- deliver ---
if [ "${AUTO_SEND:-0}" = "1" ]; then
  log "sending to the full subscriber list"
  python3 send_regime_email.py
else
  log "sending preview to owner only (set AUTO_SEND=1 to publish to subscribers)"
  python3 send_regime_email.py --test
  log "preview sent. To publish to subscribers: GMAIL_APP_PASSWORD=... python3 send_regime_email.py"
fi
log "done"
