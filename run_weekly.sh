#!/bin/bash
# Weekly driver for The Current Regime. Intended to be run by launchd.
#
# Flow: ingest sign-ups -> generate the issue (Claude, headless) -> build the
# archive -> commit/push -> send a PREVIEW to the owner only.
#
# This job never emails subscribers. Publishing to the list is a deliberate,
# manual step you run after reviewing the preview:
#   GMAIL_APP_PASSWORD=... python3 send_regime_email.py
#
# Secrets: the Gmail app password is read from the macOS Keychain. One-time setup:
#   security add-generic-password -s the-current-regime -a gmail -w 'APP PASSWORD'
#
# Env toggles:
#   GENERATE=0   skip the Claude generation step (just rebuild + preview)

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
log "syncing sign-ups from the Google Sheet"
python3 sync_subscribers.py || log "sheet sync failed (continuing)"
log "ingesting sign-ups from email (mailto / unsubscribes)"
python3 signups.py || log "signups step failed (continuing)"

# --- generate this week's issue ---
if [ "${GENERATE:-1}" = "1" ]; then
  log "generating issue via Claude (headless)"
  claude -p "Produce this week's issue of The Current Regime by following .claude/skills/current-regime/SKILL.md exactly. Do every data step, verify each factual claim with web search, write the new issue object into regime_state.json, append the ledger the-current-regime.md, then run 'python3 build_site.py'. LINK RULE (hard): never write a URL you did not actually fetch this run from a source API or a web search result; no invented HN item ids, no homepage links standing in for articles. build_site.py and the email sender lint for placeholder links and will fail the run if you break this; if a claim has no real URL, drop the claim. Commit and push. Do NOT send any email; delivery is handled by this script." \
    --dangerously-skip-permissions --model claude-opus-4-8 2>&1 | tail -8 \
    || log "Claude generation failed (continuing with current state)"
fi

# --- build + publish the archive ---
log "building site"
python3 build_site.py || log "build_site failed"
git add regime_state.json docs the-current-regime.md next-issue.md \
  && git commit -m "weekly run $(date '+%Y-%m-%d')" >/dev/null 2>&1 || true
if git push >/dev/null 2>&1; then log "pushed"; else log "push skipped/failed"; fi

# --- deliver: PREVIEW TO OWNER ONLY (never the list) ---
log "sending preview to owner only"
python3 send_regime_email.py --test
log "preview sent. Review it, then publish manually: python3 send_regime_email.py"
log "done"
