# The Current Regime

A weekly newsletter that reads the week's top Hacker News posts (plus GitHub
trending and arXiv), names the **regimes** organizing the moment, verifies every
claim against primary reporting, and tracks how those regimes change over time.

- **Public archive:** https://www.bwang.io/magikarp/
- **Design reference:** bwang.io/elekid · accent `#1a7f4b`

## How an issue is made

The full curation and organization process lives in the skill at
[`.claude/skills/current-regime/SKILL.md`](.claude/skills/current-regime/SKILL.md).
In short, each week:

1. `python3 sources.py` — pull HN (by points), GitHub trending, arXiv.
2. `python3 classify.py` — tag stories into regimes, record momentum.
3. `../ekans` `daily_check.py` — refresh the market regime (optional).
4. Choose the live regimes; write a direct headline, a didactic paragraph, and a
   verifiable implication for each. Verify all claims against primary reporting.
5. Append the issue to `regime_state.json` and `the-current-regime.md`.
6. `python3 build_site.py` — rebuild the archive in `docs/`.
7. `send_regime_email.py` — send over Gmail SMTP (`GMAIL_APP_PASSWORD`).
8. Commit and push.

House style: didactic and flowing, no em-dashes, plain language, no internal
jargon or code names in reader-facing text.

## Scheduling

A cloud routine (`trig_01PARqr7swfpBeKGnBSzPGuE`) runs the curation weekly.
Manage it at https://claude.ai/code/routines/trig_01PARqr7swfpBeKGnBSzPGuE.
Delivery is currently manual via `send_regime_email.py`.

## Sign-ups and delivery

Subscribers are managed with plain Gmail — no third-party provider.

- The site's **Subscribe** button opens a pre-filled email (subject `subscribe`).
- `signups.py` reads `subscribe` / `unsubscribe` mail over IMAP and updates
  `subscribers.txt` (gitignored; it holds addresses and stays local).
- `send_regime_email.py` sends the latest issue to everyone in `subscribers.txt`
  (BCC-style via `to_addrs`, with a `List-Unsubscribe` header). `--test` sends only
  to the owner; `--dry-run` sends nothing.

## Weekly automation (launchd)

`run_weekly.sh` ingests sign-ups, generates the issue with Claude (headless),
builds the archive, pushes, and delivers. By default it sends a **preview to the
owner**; set `AUTO_SEND=1` to publish to the full list.

One-time setup:

```sh
# 1. store the Gmail app password in the Keychain (not in any file)
security add-generic-password -s the-current-regime -a gmail -w 'YOUR_APP_PASSWORD'

# 2. install the weekly job (Mondays 8am local)
cp com.bwang.currentregime.weekly.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.bwang.currentregime.weekly.plist

# run it once by hand to test:
./run_weekly.sh            # preview to owner
AUTO_SEND=1 ./run_weekly.sh  # publish to subscribers
```

Logs go to `weekly.log`. Note: the local job and the cloud routine both generate
issues — run only one to avoid double-publishing.

## Local preview

```sh
python3 sources.py            # this week across all sources
python3 classify.py --dry-run # regime classification, nothing written
python3 regime_engine.py      # the week-over-week diff + watchlist
./fetch_hn.sh                 # raw HN query (last 7 days, >150 points)
```

## Files

| Path | Purpose |
|---|---|
| `sources.py` | HN + GitHub trending + arXiv fetchers |
| `classify.py` | daily news to regime classifier |
| `regime_state.json` | regime definitions, per-issue state, watchlist |
| `regime_engine.py` | week-over-week diff + rendered blocks |
| `send_regime_email.py` | assembles + sends the issue |
| `build_site.py` | renders the public archive into `docs/` |
| `the-current-regime.md` | running ledger of every issue |
