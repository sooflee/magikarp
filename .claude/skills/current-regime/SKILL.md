---
name: current-regime
description: Curate and organize the weekly issue of "The Current Regime" — read the week's top Hacker News posts plus GitHub trending and arXiv, classify them into regimes, verify every claim against primary reporting, write didactic copy, refresh the market regime, update the structured state and ledger, rebuild the public archive, and send the email.
---

# The Current Regime — weekly curation & organization

A weekly newsletter that reads what the world is paying attention to and names
the **regimes** that organize it: the dominant theme the front page is forming
around. Regimes change over time, and tracking that change is the point.

Audience: developers and professionals. Reference design: bwang.io/elekid.
Accent color: forest green `#1a7f4b`. Repo: github.com/sooflee/magikarp.

## Each run, in order

1. **Pull the sources.** `python3 sources.py` returns the week's top Hacker News
   posts (Algolia, ranked by points), GitHub trending repos, and recent arXiv
   papers. HN is the spine; GitHub and arXiv corroborate or add what HN misses.

2. **Classify and measure momentum.** `python3 classify.py` tags each story into
   one of the six regimes (or unaligned), scores confirm/contradict against the
   current state, and appends a record to `regime_state.json -> daily_counts`.

3. **Refresh the market regime.** In `../ekans`, run
   `.venv/bin/python pipeline/daily_check.py` and take its one-line summary
   (trend, volatility, curve, growth, liquidity, crypto). If ekans is not
   available in the run environment, skip this step rather than fail.

4. **Choose this week's regimes.** From the top posts decide which editorial
   regimes are live: always consider Tech & policy and AI agents; add Compute &
   energy, Labor & AI displacement, or Geopolitics when they clearly emerge.
   For each, write:
   - a **direct headline** (a plain declarative sentence),
   - a short **didactic paragraph** that explains the situation,
   - an **implication**: one bounded, verifiable statement — a reported fact, a
     count, or a described observation. Never a sweeping claim about how the
     world "now" works.

5. **Verify before publishing.** Every factual claim is checked against primary
   reporting via web search. Record the outlets used. If a claim cannot be
   verified, soften it to what is supported or drop it.

6. **Hold the house style.**
   - Didactic and flowing, never staccato. Explain finance and technical terms
     in plain language (volatility, yield curve, risk-off, etc.).
   - **No em-dashes.** Use commas, periods, or restructure the sentence.
   - No internal jargon or code names in reader-facing text (no "bsig", no
     signal IDs like AE-1). Spell out what the reader sees.

7. **Update the structured state.** Append a new issue object to
   `regime_state.json -> issues` with, per regime: `state` (from that regime's
   defined state space), `headline`, `summary`, `implication`, and `evidence`.
   Update the `new` flag on each `bsig_watch` item (elevated this issue vs.
   ongoing). Append a human-readable entry to `the-current-regime.md`.

8. **Rebuild the archive.** `python3 build_site.py` writes `docs/index.html`
   (serif throughout, forest-green accent). GitHub Pages serves it at
   https://www.bwang.io/magikarp/.

9. **Send.** `send_regime_email.py` sends the issue over Gmail SMTP, reading the
   app password from `GMAIL_APP_PASSWORD` (never hard-coded). The claude.ai
   Gmail connector only has read scopes, so SMTP is the delivery path.

10. **Commit and push** all changes to `main`.

## Adaptive depth: let the issue breathe with the week

Issue length should scale with how much actually happened. A week with a war
ending, a model nationalized, or a Fed surprise runs long; a quiet week runs
short. Do not pad a slow week to last week's length, and do not truncate a
genuinely eventful one. Concretely, vary these by significance, not by habit:

- **Prediction-market moves** (`market_moves`): include only markets that genuinely
  moved or are decision-relevant this week. That might be one, it might be five.
  If nothing moved, omit the block; the momentum table stands on its own.
- **Structural radar** (`spotlight`): spotlight only regimes with real news or a
  possible shift. Most weeks, most regimes are steady one-liners. A pivotal week
  promotes several to the full block.
- **Geopolitics**: 3 to 5 stories, fewer in a thin week.
- **Watchlist** (`new`): full cards only for what is elevated this week.

The renderers already degrade gracefully to zero items in any of these, so a
short issue is a feature, not a failure.

## The structural picture (regime radar)

Beyond the weekly editorial regimes, each issue carries a **regime radar**: a set
of slow, structural regimes read through prediction markets. A regime is a
structural current (Dedollarization, Monetary policy, Fragmentation, the AI
buildout, AI sovereignty), not an event. A single market ("Iran ceasefire holds")
is an event, never a regime.

Read a regime from the **drift of a basket** of dated, liquid markets, not one
headline:
- Pick 2-3 dated, resolvable markets per regime (Polymarket and Kalshi for
  econ/politics, Metaculus for long-horizon structural questions).
- Record each market's value and, from issue 02 on, its week-over-week move.
- Flag any market that crosses 50% or moves more than 10 points, and watch for
  divergence (the market drifting while the spot read stays calm).
- Weight by liquidity: a high probability on thin volume is noise; cite volume.
- If a regime has no liquid market (AI governance today), say so. The absence is
  itself a finding.

Store these in `regime_state.json -> issues[].structural_regimes` as
`{name, direction, read, basket:[{metric, value, url}], spotlight}`. Verify every figure.

Keep the radar short by default. Set `spotlight: true` only on regimes with real
news or a possible structural shift that week; those get the full block. The rest
collapse to a one-line "Holding steady" summary. Most weeks, most regimes are steady.

Also surface the week's **biggest prediction-market moves** in the momentum section
(`issues[].market_moves: [{market, dir, detail, url}]`): which dated markets swung
hardest and why. From issue 02 on, compute the week-over-week delta from the prior
issue's stored basket values rather than describing the move qualitatively.

## The six weekly regimes (state spaces live in regime_state.json)

- **Tech & policy** — open-acceleration / consolidation / state-capture
- **AI agents** — capability-race / liability-reckoning / normalized
- **Markets** — risk-on / mixed / risk-off (from the ekans market read)
- **Compute & energy** — abundant / tightening / constrained
- **Labor & AI displacement** — hiring / flat / contracting
- **Geopolitics** — calm / elevated / stressed

## Files

- `sources.py` — multi-source fetchers (HN, GitHub trending, arXiv).
- `classify.py` — daily news to regime classifier + confirm/contradict.
- `regime_state.json` — regime definitions, per-issue state, watchlist, daily counts.
- `regime_engine.py` — week-over-week diff and the rendered blocks.
- `send_regime_email.py` — assembles and sends the HTML + plain-text issue.
- `build_site.py` — renders the public archive into `docs/`.
- `the-current-regime.md` — running ledger of every issue.
