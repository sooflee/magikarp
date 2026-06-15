# HN Weekly Themes Briefing

A weekly briefing that pulls the top Hacker News stories from the past 7 days and
distills them into popular **themes** — split into perishable *Events* and recurring
*Currents*.

## How it runs

A **cloud routine** (scheduled Claude Code agent) generates the briefing automatically.
It runs on Anthropic's cloud infra, so it fires whether or not this machine is on.

| | |
|---|---|
| Routine ID | `trig_01PARqr7swfpBeKGnBSzPGuE` |
| Schedule | `0 12 * * 1` — Mondays 12:00 UTC (**8am EDT / 7am EST**) |
| Model | claude-opus-4-8 (curation/organization task) |
| Data source | HN Algolia Search API (public, no auth) |
| Output | markdown briefing in the routine session + `briefing.md` |

**Manage / read results:** https://claude.ai/code/routines/trig_01PARqr7swfpBeKGnBSzPGuE

## Checking that it ran

The briefing appears as a session in the routines UI each Monday. If a week looks
skipped, open the routine and hit **Run now** to backfill it.

## Local preview

Run the same data query locally to eyeball the week before/without the routine:

```sh
./fetch_hn.sh            # last 7 days, >150 points
./fetch_hn.sh 30 150     # last 30 days
```

## Delivery note

There's currently no email/Slack connector on the account, so the briefing lives in
the routines web UI. To get it delivered to an inbox or channel, connect one at
https://claude.ai/customize/connectors and the routine can be updated to use it.
