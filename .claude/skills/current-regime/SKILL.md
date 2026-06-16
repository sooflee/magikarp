---
name: current-regime
description: Build the weekly issue of "The Current Regime" — read the week's top Hacker News posts, name the regimes, verify every claim against primary reporting, refresh markets/commodities data, write the issue into regime_state.json (email, site and plain text all render from it), rebuild the public archive, and preview it.
---

# The Current Regime — how an issue is built

A weekly newsletter that reads what the world is paying attention to and names the
**regimes** organizing it, then tracks how those regimes change. Audience:
developers and professionals. Design reference: bwang.io/elekid (serif, forest
green `#1a7f4b`). Repo: github.com/sooflee/magikarp. Archive: www.bwang.io/magikarp.

**Everything is data-driven.** You author one issue object in `regime_state.json`;
`send_regime_email.py` (HTML + plain text) and `build_site.py` (the archive) both
render from it. They must stay 1:1. Never hand-edit the rendered output.

## The shape of an issue (sections, in order)

The issue is organized into two acts. Keep this order; the renderers follow it.

1. **Where the week's attention went** — regime momentum (HN story counts per
   covered regime, this week vs last, with each regime's "week N in <state>"),
   then **Markets that swung this week** (high-volume, big-swing prediction markets).
2. **What changed** — the week-over-week regime diff. Suppressed automatically when
   the previous issue is the partial baseline (issue 01 has none; it begins at 02).
3. **— The tech world —**
   - **Tech & policy** regime
   - **AI agents** regime, with an inline "On GitHub this week" note folded under it
   - **Exponential trends to watch** (the forward watchlist)
   - **Undercurrent** (a quieter counter-theme, if present)
4. **— The wider world —**
   - **Geopolitics** (a 3–5 story digest, each tied to a regime)
   - **Commodities & energy** (big movers only)
   - **Markets** (the cards + plain-language explainer)
   - **The structural picture** (the regime radar)
5. **What to watch next week** — a short forward calendar.

Every editorial section is a **direct declarative headline + a small subtitle**
(the category) + a short didactic paragraph. Length scales with the week (see
Adaptive depth).

## Build pipeline

1. **Pull sources.** `python3 sources.py` → top HN posts (Algolia, by points) and
   GitHub trending. HN is the spine.
2. **Regime momentum.** Count the week's top HN stories per regime for **this week
   and last** (two Algolia `created_at_i` date-range queries, classified with the
   keyword rules in `classify.py`). Store as `momentum:{weeks:[a,b], series:{regime:[prev,cur]}}`.
   Only chart regimes you actually cover this issue.
3. **Refresh markets + commodities** (needs the sibling `../ekans` repo and its venv):
   - Market regime: `.venv/bin/python pipeline/daily_check.py` → one line of
     trend / volatility / curve / growth / liquidity / crypto.
   - Add **dollar** (DXY) and **credit** (HY spread) via yfinance/FRED.
   - **Commodity prices** via yfinance (Brent, WTI, gold, silver, copper, nat-gas,
     grains, softs) with the week's % change.
   If ekans is unavailable, carry the last reading forward, clearly dated, or omit.
4. **Choose the live regimes and write them.** Always consider Tech & policy and
   AI agents; add Geopolitics, Compute & energy, or Labor & AI displacement when
   they clearly emerge. For each: a `state` (from its state space), a direct
   `headline`, a didactic `summary` (~40–90 words), an `implication` that is **one
   bounded, verifiable statement** (a reported fact, a count, an observation — never
   a sweeping claim), `evidence`, and the article `links`. Geopolitics uses
   `items:[{title,url,comment}]` where each comment ties the story to a regime.
5. **Verify before publishing.** Web-search every factual claim against primary
   reporting; cite outlets. Soften or drop anything unverified.
6. **Update state + ledger.** Append the issue object to `regime_state.json -> issues`;
   append a human-readable entry to `the-current-regime.md`.
7. **Build + check.** `python3 build_site.py`; confirm email and site stay 1:1.
8. **Deliver.** `send_regime_email.py` (Gmail SMTP, password from `GMAIL_APP_PASSWORD`).
   Default is a preview to the owner (`--test`); sending to the subscriber list
   (`subscribers.txt`) is a deliberate manual step after review.
9. **Commit and push** to `main`.

## House style (strict)

- Didactic and flowing, never staccato. Explain finance/technical terms in plain
  language (volatility, yield curve, risk-off).
- **No em-dashes.** Use commas, periods, or restructure.
- **No internal jargon or code names** in reader-facing text (no "bsig", no signal
  IDs like AE-1). The market model and watchlist come from ekans; spell out what
  the reader sees.
- Keep summaries tight (~40–90 words). Implications are bounded and verifiable.

## Section conventions

- **Geopolitics** — 3 to 5 of the week's biggest *world* stories (not just HN),
  each with a one-line comment connecting it to a tracked regime. This is where the
  issue earns breadth beyond tech.
- **Commodities & energy** (`commodities`) — show **only big movers**: a
  `min_change` threshold (default 4%) filters the table, so small moves drop out.
  The summary leads with the big moves and ends with the larger forward call. Label
  `as_of` to the issue's end date.
- **Markets** (`regimes.markets.signals`) — cards for trend, volatility, yield
  curve, growth (GDPNow), dollar, credit, liquidity, crypto, color-coded
  constructive / cautious / neutral, followed by a fixed plain-language "what the
  readings mean." Directional only, not investment advice.
- **Exponential trends to watch** (`bsig_watch`) — each entry: a **one-sentence**
  why, a **concise** "what to watch," and a **one-line** "where it shows up." `new:
  true` gets a full card; the rest collapse under "Still on watch."
- **Undercurrent** (`undercurrent`) — a single quieter counter-theme with a few links.
- **On GitHub this week** (`across_sources`) — one inline line under AI agents
  naming what trending shows. (No arXiv; it was dropped as low-signal.)
- **What to watch next** (`watch_next`) — dated forward events only; cross-reference
  rather than repeat what a section already covered.

## Adaptive depth: let the issue breathe with the week

Length scales with significance, not habit. A blockbuster week runs long; a quiet
week runs short. The renderers degrade to zero items, so a short issue is a feature.
- **Markets that swung** (`market_moves`): only markets that genuinely moved on high
  volume. One, several, or none.
- **Structural radar** (`spotlight`): spotlight only regimes with real news or a
  possible shift; the rest are "Holding steady" one-liners.
- **Geopolitics**: 3–5 stories; fewer in a thin week.
- **Watchlist** (`new`): full cards only for what is elevated this week.

## The structural picture (regime radar)

Beyond the weekly regimes, each issue carries a radar of slow, **structural**
regimes (Dedollarization, Monetary policy, Fragmentation, the AI buildout, AI
sovereignty). A regime is a structural current, not an event ("Iran ceasefire
holds" is an event). Read each from the **drift of a basket** of dated markets and
hard data, not one headline. Store as
`structural_regimes:[{name, direction, read, basket:[{metric,value,url}], spotlight}]`.
Subtitle the section "read through markets and hard data" (most baskets are data +
Metaculus forecasts, not swinging money markets).

**Prediction-market policy.** Only present a prediction market when it is **high
volume AND has a large signal swing**; otherwise use hard data and keep the honest
label. Platform preference: **Kalshi** first (regulated), **Metaculus** for
long-horizon forecasts, and **Polymarket when it is the high-volume market for a
question** (well-calibrated at high volume). The volume + swing bar is the accuracy
gate; never quote a thin or static market. The week's high-volume, big-swing markets
go in "Where the week's attention went" (`market_moves`). If a regime has no liquid
market (AI governance today), say so — the absence is the finding. From issue 02 on,
compute each basket's week-over-week move from the prior issue's stored values.

## The weekly regimes (state spaces in regime_state.json)

- **Tech & policy** — open-acceleration / consolidation / state-capture
- **AI agents** — capability-race / liability-reckoning / normalized
- **Markets** — risk-on / mixed / risk-off (from the ekans read)
- **Compute & energy** — abundant / tightening / constrained
- **Labor & AI displacement** — hiring / flat / contracting
- **Geopolitics** — calm / elevated / stressed

## Issue object schema (regime_state.json -> issues[])

```
id, week, date, date_label, partial
regimes: { tech_policy|ai_agents|geopolitics|markets: {
   state, headline, summary, implication, evidence[],
   links:[{points,title,url}], items:[{title,url,comment}](geopolitics),
   signals:{...}(markets only) } }
momentum: { weeks:[a,b], series:{regime:[prev,cur]} }
market_moves: [{market, dir(up|down|flat), detail, url}]
commodities: { as_of, min_change, summary, items:[{name,level,change}] }
undercurrent: { label, headline, summary, links:[...] }
across_sources: { github_theme, github:[{title,url}] }
structural_regimes: [{name, direction, read, basket:[{metric,value,url}], spotlight}]
watch_next: [{when, event, note}]
```
Global: `regime_defs` (state spaces) and `bsig_watch` (the watchlist).

## Files

- `sources.py` — HN (Algolia) + GitHub trending fetchers.
- `classify.py` — keyword classifier → regime momentum counts.
- `regime_state.json` — regime defs, every issue object, the watchlist.
- `regime_engine.py` — week-over-week diff, momentum/trajectory, rendered blocks.
- `send_regime_email.py` — renders + sends the HTML + plain-text issue (list-aware).
- `build_site.py` — renders the blog-style archive into `docs/`.
- `the-current-regime.md` — running ledger of every issue.
- Delivery/sign-ups: `subscribers.txt` (local), `sync_subscribers.py` (Google
  Sheet), `signups.py` (email), `add_subscriber.py` (manual), `run_weekly.sh` +
  the launchd plist (weekly local job: generate, build, push, preview to owner).
