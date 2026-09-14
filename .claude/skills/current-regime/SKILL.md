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

The issue opens with a summary and then runs in three acts. Keep this order; both renderers
(site and email) follow it, and the plain-text email mirrors it.

0. **Masthead and the week in brief** — the issue's `index_title` as a one-sentence dek under
   the masthead, then `brief`: one line per lane (AI & compute, the deep-dive, geopolitics,
   markets, the wildcard), each under 30 words, each linking to its section on the site.
1. **— The tech world —**
   - **AI & compute** regime — the whole AI industry in one lane: model launches
     and pricing, who controls access, agent security and the money. Carries the inline
     "On GitHub this week" note folded under it.
   - **Undercurrent** (a quieter counter-theme, if present)
2. **— The wider world —**
   - **Deep-dive of the week** — the rotating non-tech core lane; it leads this act.
     Its domain changes every week (see the rotation below), so the issue is not all-tech.
   - **Geopolitics** (a 4–6 story digest across more than one theatre, each tied to
     a regime; the issue's breadth beyond tech, sourced from world reporting, not HN)
   - **Commodities & energy** (big movers only)
   - **Markets** (the cards + a collapsible plain-language explainer)
   - **The wildcard** (one rotating theme, from a different rotation than the
     deep-dive; mandatory each week)
   - **Smaller stories** (optional: 3-6 one-line briefs from the briefs sweep)
3. **— Tracking the regimes —** the standing trackers, together at the end:
   - **Where the week's attention went** — regime momentum (HN story counts per covered
     regime, this week vs last), **What changed** (the week-over-week diff; suppressed when
     the previous issue is the partial baseline) and **Markets that swung this week**.
   - **Exponential trends to watch** (the forward watchlist; "still on watch" collapses)
   - **The structural picture** (the regime radar)
   - **What to watch next week** — a short forward calendar.

Every editorial section is a **small label (with the state badge) above a direct declarative
headline**, then a short didactic paragraph, then the **Key fact** (the `implication`), then any
chart, items and sources. Length scales with the week (see Adaptive depth) inside the length
budget in House style.

## Build pipeline

1. **Pull sources.** `python3 sources.py` → HN (Algolia, by points), GitHub
   trending, arXiv, **GDELT** (world-news events; auto-retries once on a 429),
   **world reporting** (nine feeds: Al Jazeera, BBC World, DW, France24, AllAfrica,
   El País English, MercoPress, The Hindu, Semafor), **big regional stories**
   (eleven in-region outlets: The Continent, African Arguments, Himal Southasian,
   The Diplomat, Fulcrum, Americas Quarterly, Middle East Eye, +972, Eurasianet,
   Balkan Insight, Meduza — the layer beneath the wires; mine it for the
   geopolitics digest's non-Ukraine/Iran slots), **Techmeme** (curated tech),
   **Lobsters** (dev cross-check), **Polymarket** (forward odds), **AI analysis
   weeklies** (Interconnects, Import AI, Zvi, SemiAnalysis — what HN's front page
   missed), **cyber/fraud reporting** (404 Media, Risky Business, Krebs — wildcard
   fodder), **Wikipedia top pageviews** (neutral attention gauge), and **Hugging
   Face trending** (the open-weights race in downloads), the **briefs sweep**
   (research/accountability outlets, date-filtered to the last 10 days — feeds
   the Smaller-stories section), and **OpenRouter's newest routable models**.
   HN is the spine for tech
   attention, but never name Geopolitics or the wildcard from HN alone.
   **Read the FEED HEALTH block at the end of the run and act on it**: a WARN for
   a dead feed or a single-source group means that lane's pull is suspect — widen
   it with research agents before writing, and say so in the ledger. Targeted
   helpers, not in the default run: `fetch_edgar('"query"')` for SEC filings
   behind a story; `fetch_eia()` / `fetch_acled()` activate when EIA_API_KEY /
   ACLED_KEY+ACLED_EMAIL are exported.
   **Then run the big-story sweep** (section below) so no week-defining story is left to
   whichever lane happened to look for it.
   **Then run `python3 coverage.py` and act on it the same way.** It reads every
   past issue and prints a COVERAGE DEBT block: WARN lines for any region or topic
   that has not appeared in the last three issues, an "every issue" list (the
   sameness signal), and a ranked wildcard shortlist for the next issue. A region
   or topic WARN is an assignment: put it in the geopolitics digest, the briefs,
   the wildcard or the undercurrent this week, or say in the ledger why not.
   **Lane rules that follow from it:** no lane may open with the same lead actor
   as the previous two issues (if the AI lane led with a Chinese lab's launch two
   weeks running, lead with money, labor, security, users or policy this week); the
   geopolitics lead may not be Iran or Ukraine three weeks running; the
   undercurrent must be non-AI at least every other week.
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
4. **Write the four core lanes.** The four lanes are fixed: **AI & compute**
   (`ai_compute`), the **Deep-dive of the week** (`deep_dive`), **Geopolitics**
   (`geopolitics`), and **Markets** (`markets`). For each: a `state` (from its state
   space), a direct `headline`, a didactic `summary` (90–130 words at most), an `implication`
   that is **one bounded, verifiable statement** (a reported fact, a count, an
   observation — never a sweeping claim), `evidence`, and the article `links`.
   Geopolitics uses `items:[{title,url,comment}]` where each comment ties the story
   to a regime.
   - **AI & compute** holds model launches/pricing, access politics, and agent
     security together. Do not split the same story across two cards.
   - **Deep-dive of the week** rotates its domain by issue number through eleven
     domains: bio & health → the real economy → China's industrial stack → energy &
     materials → the Global South → science & frontier → labor & demographics → law &
     courts → climate & disasters → culture & media → cities & housing (issue 06 is
     bio & health; 12 is the first labor & demographics; `sources.deep_dive_domain(N)`
     is the source of truth). Widened from six on 2026-08-18 after the coverage
     review found the non-tech act cycling through the same few beats. Source it
     from that domain's feeds (`python3 sources.py deepdive <issue#>`), **not** HN.
     Its domain rotates, so it is deliberately **not** part of the momentum or the
     week-over-week diff. Use states `accelerating / steady / stalling`.
5. **Verify before publishing.** Web-search every factual claim against primary
   reporting; cite outlets. Soften or drop anything unverified. Then run the **audit**: four
   adversarial verifier agents, one per lane group (AI; geopolitics and trade; markets and
   commodities; deep-dive, wildcard, briefs), about 20 searches each, reporting exact
   old/new text; apply fixes as exact-match replacements that fail loudly. Run the big-story
   sweep again before the audit. Budget searches: the session cap is about 200, so keep lane
   researchers near 18 each. Run the `human-voice` and `humanize` passes over all reader text.
6. **Update state + ledger.** Append the issue object to `regime_state.json -> issues`;
   append a human-readable entry to `the-current-regime.md`.
7. **Build + check.** `python3 build_site.py` (link lint and `lint_media` run inside); confirm
   email and site stay 1:1 for text; check the length budget; screenshot the page at desktop
   width and inside a 375px iframe and look at it before sending.
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
- **Length budget.** Aim for about 3,000 rendered words. Headlines at most about 20 words
  (the label and badge sit above them). Summaries 90–130 words at most. Geopolitics, wildcard
  and brief comments two sentences, about 60 words. The wildcard carries at most four items.
  More than six links collapse behind "more sources" on the site, so order links by importance.
- **One home per story.** Geopolitics owns events, commodities owns prices, markets owns
  rates, the radar owns the slow read in one sentence. A fact already told is referred to, not
  retold; issue 14 first shipped with the pipeline in four sections and the Fed odds in four.
- Implications are bounded and verifiable, render as the **Key fact** under the summary, and
  must not repeat a number from their own summary.
- **Run the `human-voice` skill's self-edit pass** over all reader-facing text
  (headlines, summaries, comments, watchlist cards, ledger) before building or
  sending; it is the machine-writing-tell checklist and includes grep sweeps.
- **No theme-restatement openers.** Never open a summary (or the `lede`) with an
  abstract framing of the week: "The week turned on a reversal.", "Identity became
  the gate this week.", "This week the money moved toward scale." They sound
  meaningful but carry no information. **Lead with the concrete development** — the
  named actor, the number, the dated event — and let the reader infer the theme.
  The `headline` already states the theme; the summary's job is the fact.

## Section conventions

- **Geopolitics** — 4 to 6 of the week's biggest *world* stories, each with a
  one-line comment connecting it to a tracked regime. This is where the issue earns
  breadth beyond tech, so give it real weight: source it from **GDELT + Al Jazeera +
  wider reporting**, not from whatever geopolitics happened to reach HN's front page.
  **Theatre rule (enforce it):** of the 4–6 slots, **at most two** may go to the
  Ukraine/Russia and Iran/Middle East theatres *combined*; **at least two** must come
  from a different theatre — elections, the Global South, sanctions, a non-conflict
  shift, or the domestic politics of a state other than the US/EU/China. The past
  issues drifted into Ukraine + Iran + trade every week; break that. Fewer stories
  only in a genuinely thin week.
- **The wildcard** (`wildcard`) — one theme each week from *outside* the four core
  lanes, and from a **different rotation than the deep-dive** so the two do not
  collide: the fraud/scam economy, culture and the attention economy, education under
  AI, a specific company, a cultural shift. **Pick it from the top of
  `coverage.py`'s wildcard shortlist** (most-indebted topic first, never the last
  issue's topic, never the deep-dive's domain) unless the week hands you something
  plainly better, and say which in the ledger. It is **mandatory** each week (a quiet
  week must still reach outside the tech box); only omit it if you genuinely cannot
  find one, and say why in the seed notes. It is deliberately rotating, so it is
  **not** part of the week-over-week momentum/diff. Same shape as a regime section
  but no `state`: `{topic, headline, summary, links, items?}`.
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
- **Smaller stories** (`briefs`) — 3-6 one-line items from the date-filtered
  briefs sweep (`fetch_briefs`: NBER, Apricitas, Bits About Money, Bellingcat,
  War on the Rocks, FTC, Retraction Watch, Pew). Each item: `{title, url,
  comment}`, source and date in the title, comment one bounded sentence. These
  are deliberately small; a brief that needs a paragraph belongs in a lane.
  Verify each URL resolves — feed links get truncated, and a guessed slug is
  how fabricated URLs happen. Optional; omit in a thin week.
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
- **Geopolitics**: 4–6 stories under the theatre rule; fewer only in a thin week.
- **Watchlist** (`new`): full cards only for what is elevated this week.

## Big-story sweep (before writing, and again before the audit)

Lane researchers find what their lane looks for, and issue 14 shipped without the week's
largest oil event (drones from Iraq shutting Saudi Arabia's East-West pipeline), an ECB
hike, Anthropic's own sandbox-escape disclosure and Apple's September event. So once per
issue, run one cross-lane sweep: read Wikipedia's current-events day pages for the week
(`https://en.wikipedia.org/wiki/Portal:Current_events/<YYYY>_<Month>_<D>`), the Al Jazeera,
AP and Guardian world front pages, Techmeme's daily archive and the other central banks'
calendars, and list every story that would lead a major front page or move a tracked regime.
Each one either goes into the lane or radar whose argument it changes, becomes a brief, or
gets a one-line reason in the ledger for leaving it out. Run it with web-search budget to
spare: the gap check for issue 14 ran after the session's search cap and had to verify by
page fetches alone.

## Hover notes (archive site only)

The site marks the first appearance of a term in each section with a dotted underline and a note
that opens on hover, keyboard focus or tap. The email shows the text without notes.

- **Shared glossary** (`glossary`, top level of `regime_state.json`): plain-language definitions
  that stay true every week (basis points, high-yield spread, front month, Polymarket prices, El
  Niño, Lean). It applies to every archive page, so add a term once and it works everywhere.
- **Issue notes** (`annotations` on the issue): who a person is, where a place is, what a bill
  does. Use only facts already verified for that issue or settled general knowledge; a note is
  reader-facing text and gets the same verification, house style and audit as the lanes.
- Shape: `{terms:[...], note, url?}`. `terms` are exact, case-sensitive spellings as they appear
  in the text (list variants). Notes run 45 words at most, one or two sentences, no em-dashes, no
  opinion. The build fails on an issue note that never matches the page, so a renamed person or a
  cut sentence cannot leave a dead note behind.
- Aim for the terms a curious non-specialist would stop at: jargon, acronyms, people and places the
  issue names without introducing. Ten to twenty-five issue notes is plenty.

## Images and charts (archive site only)

The site renders an optional `image` and/or `chart` on any lane (`regimes.*`),
`commodities`, `wildcard` or `undercurrent`. The email ignores both, so the
email/site 1:1 rule applies to text only. `build_site.lint_media` fails the build on
a missing credit, licence, alt, caption, dimensions or file.

- **Photos: open licence only, stored locally.** Public domain (NASA, NOAA, other US
  federal agencies), CC0, CC BY or CC BY-SA. Never use news-agency or outlet photos
  from the linked articles, and never hotlink. Fetch with `python3 media.py commons
  "File:Name.jpg" docs/img/<issue>/<section>.jpg` (Wikimedia Commons, licence and
  author read from the file page) or `python3 media.py worldview <date> <S,W,N,E>
  docs/img/<issue>/<section>.jpg` (a NASA satellite image of that day, public domain).
  Both resize to 1280px and print the JSON block.
- **Look at every image before writing its `alt` and `caption`.** The caption states
  what the picture shows, where and when ("The Bab al-Mandeb strait ... photographed
  from the ISS in February 2020"). An archive photo must carry its own date so it is
  never mistaken for this week. Claim nothing you cannot see in the frame.
- **Only photos that show something about this week**, such as a satellite image of the
  event. No stock, trade-fair or archive shots: issue 14's 2012 LG stand and 2020 strait photo
  were removed as decoration. A lane with nothing like that gets no photo, and most weeks that
  means one photo or none.
- **Charts: one dated series each** (`chart:{title, subtitle, series:[{name, points:
  [[YYYY-MM-DD, value]]}], prefix|suffix, decimals, y_min?, y_max?, ref?:{value,label},
  highlight_from, highlight_label, source, source_url?}`). Two or more series need a
  legend and a validated palette, which the renderer does not do yet, so the lint
  rejects them. Pull series with `media.py polymarket <slug> "<question match>" <start>
  <end>` (UTC daily closes, in cents) or `media.py yf <ticker> <start> <end>`; never
  type values by hand. The chart must agree with the numbers the text quotes.
  `source_url` must not repeat a URL cited elsewhere in the issue (link lint).
- Good chart candidates: the week's biggest market move (a Fed or election contract),
  Brent when energy leads, a download or price series the AI lane argues from.

## The structural picture (regime radar)

Beyond the weekly regimes, each issue carries a radar of slow, **structural**
regimes (Dedollarization, Monetary policy, Fragmentation, the AI buildout, AI
sovereignty). A regime is a structural current, not an event ("Iran ceasefire
holds" is an event). Read each from the **drift of a basket** of dated markets and
hard data, not one headline. Store as
`structural_regimes:[{name, direction, read, line?, basket:[{metric,value,url}], spotlight}]`.
Spotlight every regime that moved this week. Give every other regime a one-sentence `line`;
the Holding-steady list renders it, and without it only the first basket entry shows, which
is how issue 14's BRICS and Nvidia–Anthropic updates first went invisible.
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

The four core lanes (issue 06+):
- **AI & compute** (`ai_compute`) — open-acceleration / consolidation / state-capture
- **Deep-dive of the week** (`deep_dive`) — accelerating / steady / stalling
  (rotating domain; not in momentum/diff)
- **Geopolitics** (`geopolitics`) — calm / elevated / stressed
- **Markets** (`markets`) — risk-on / mixed / risk-off (from the ekans read)

`ai_compute` inherits the former `tech_policy` history for continuity (same state
space); the renderers and `regime_engine.diff` alias the two so issue 06 reads as a
continuation, not a new lane. Archived defs kept for issues 01–05:
- **Tech & policy** (`tech_policy`) and **AI agents** (`ai_agents`) — ARCHIVE ONLY,
  merged into `ai_compute`.
- **Compute & energy** (`compute_energy`), **Labor & AI displacement** (`labor_ai`)
  — structural radar inputs.

## Issue object schema (regime_state.json -> issues[])

```
id, week, date, date_label, partial
index_title   # archive/index title: state the week's defining event AS a move in its
              # larger trend ("Open weights become Chinese industrial policy as oil
              # re-enters the inflation story."), never a bare event list ("X ships;
              # Y lands."). Event anchor + trend meaning in one declarative sentence.
brief         # [{lane, anchor, line}] the week in brief; anchors: ai, deep-dive, geopolitics,
              # markets, wildcard (section ids on the site)
regimes: { ai_compute|deep_dive|geopolitics|markets: {
   state, headline, summary, implication, evidence[],
   links:[{points,title,url}], items:[{title,url,comment}](geopolitics),
   signals:{...}(markets only) } }
   # deep_dive also carries {domain} naming the week's rotating topic.
   # any lane, commodities, wildcard or undercurrent may carry image{...} / chart{...} (site only)
momentum: { weeks:[a,b], series:{regime:[prev,cur]} }   # ai_compute/geopolitics/markets only; never deep_dive
market_moves: [{market, dir(up|down|flat), detail, url}]
commodities: { as_of, min_change, summary, items:[{name,level,change}] }
undercurrent: { label, headline, summary, links:[...] }
across_sources: { github_theme, github:[{title,url}] }
wildcard: { topic, headline, summary, links:[...], items?:[{title,url}] }   # rotating, optional
briefs: [{title, url, comment}]   # Smaller stories; optional, 3-6 one-liners
structural_regimes: [{name, direction, read, line?, basket:[{metric,value,url}], spotlight}]
watch_next: [{when, event, note}]
```
Global: `regime_defs` (state spaces) and `bsig_watch` (the watchlist).

## Files

- `sources.py` — fetchers: HN (Algolia), GitHub trending, arXiv, GDELT
  (geopolitics), Al Jazeera + Techmeme (RSS), Lobsters, Polymarket, and the rotating
  **deep-dive** feeds (`fetch_deep_dive` / `deep_dive_domain`, per-domain RSS +
  GDELT). All best-effort.
- `classify.py` — keyword classifier → regime momentum counts.
- `coverage.py` — coverage-debt ledger: region/topic tags per past issue, WARNs for
  anything unseen in three issues, the sameness signal, next issue's wildcard shortlist.
- `media.py` — site images and chart series: Wikimedia Commons and NASA Worldview photos with
  licence metadata, Polymarket UTC daily closes (match must hit exactly one market), yfinance
  closes via the ekans venv.
- `regime_state.json` — regime defs, every issue object, the watchlist.
- `regime_engine.py` — week-over-week diff, momentum/trajectory, rendered blocks.
- `send_regime_email.py` — renders + sends the HTML + plain-text issue (list-aware).
- `build_site.py` — renders the blog-style archive into `docs/`.
- `the-current-regime.md` — running ledger of every issue.
- Delivery/sign-ups: `subscribers.txt` (local), `sync_subscribers.py` (Google
  Sheet), `signups.py` (email), `add_subscriber.py` (manual), `run_weekly.sh` +
  the launchd plist (weekly local job: generate, build, push, preview to owner).
