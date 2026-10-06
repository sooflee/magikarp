# Playbook: building an issue step by step

SKILL.md says what an issue is and why. This file says exactly what to do, in order, with
the checks that catch the mistakes past issues actually shipped. It is written so that a
model with less judgment can follow it and produce the same quality: when in doubt, follow
the rule literally, and when a rule and your instinct disagree, the rule wins.

Run every command from the repo root. Keep a scratch directory for dossiers and drafts
(`$S` below); never put drafts in the repo.

---

## 0. Before you start (5 minutes)

1. **Which issue?** `python3 -c "import json;d=json.load(open('regime_state.json'));i=d['issues'][-1];print(i['id'],i['week'])"`.
   The new issue is that id + 1, covering the next Monday-to-Sunday week. If today is
   Monday, the week is the seven days that ended yesterday. Check `git log origin/main` in
   case another session already built it.
2. **Read** `next-issue.md` (seed notes left by the last build: leads, forward calendar,
   lane rules, the previous basket values, contract-roll warnings). Everything in it is a
   lead, not a fact; verify before use.
3. **Read the previous issue object in full.** It is the template for tone, length and
   every field. Copy its shape; do not invent fields.

## 1. Pull the data (all mechanical)

```
python3 sources.py > $S/sources.txt          # feeds; read the FEED HEALTH block at the end
python3 sources.py deepdive <N> > $S/deepdive.txt
python3 coverage.py                          # coverage debt + wildcard shortlist
python3 momentum.py <monday> <sunday>        # momentum JSON for the issue (prev = last issue's cur)
(cd ../ekans && .venv/bin/python pipeline/daily_check.py | tail -3)   # market regime line
```

Write down, before any research: the deep-dive domain (`sources.deep_dive_domain(N)`), the
coverage WARNs (each one is an assignment), the top wildcard candidate, and the three lane
rules from next-issue.md (who led the AI lane and geopolitics the last two weeks, whether the
undercurrent must be non-AI).

## 2. Research: one agent per lane, plus a sweep

Launch these in parallel, each with the brief in `research-brief.md` pasted at the top and
about 18 web searches. Do not let agents spawn sub-agents (the search budget is about 200
for the whole session, and the audit needs 80 of them).

| Agent | Delivers |
|---|---|
| AI & compute | lead + state, 8-12 verified stories, GitHub trending line, Hugging Face downloads |
| Deep-dive | one domain story with a trend and hard numbers, 2-3 secondary items |
| Geopolitics | 6-8 candidates obeying the theatre rule, one covering each coverage WARN region |
| Markets + commodities | every number in the markets card, commodities table, radar baskets, market moves, one chart series |
| Wildcard + undercurrent + briefs | the three small sections |
| Big-story sweep | every front-page story of the week from Wikipedia's current-events day pages, tagged by lane |

Each writes `$S/dossier_<lane>.md`. When the sweep comes back, check every story on its
list against the dossiers: each one goes into a lane, becomes a brief, or gets a one-line
reason for leaving it out in the ledger. `evidence` does not render, so a story parked only there
is still missing (issue 17 hid the White House AI accord that way). Past issues missed a Saudi pipeline shutdown, an ECB
hike and a lab's own safety disclosure because no lane was looking.

## 3. Decide before you write

Fill this in (in your scratch notes) before drafting any prose:

- **States.** For each lane, the state and the one fact that justifies it. Keep the previous
  state unless the week's evidence clearly fits another state's definition in
  `regime_defs` (read the `rule` text). A state change is a claim; the summary must show
  the evidence for it.
  - `ai_compute`: open-acceleration (prices falling, launches, few constraints) /
    consolidation (a few firms dominate, M&A, exclusive deals) / state-capture
    (governments gate access).
  - `geopolitics`: calm / elevated / stressed. Stressed = active wars affecting trade or
    energy plus new escalation.
  - `markets`: from the ekans line (`risk MIXED` → mixed).
  - `deep_dive`: accelerating / steady / stalling, describing that domain's own trend.
- **Leads.** Each lane's lead must differ from the last two issues' lead actor and angle.
  Geopolitics may not lead with Iran or Ukraine three weeks running.
- **One home per story.** List every story once, with the one section that owns it.
  Events → geopolitics, prices → commodities, rates → markets, slow reads → radar. Anywhere
  else refers to it in a clause at most.
- **Theatre rule.** Count geopolitics items touching Ukraine/Russia or Iran/Israel/Gaza/
  Lebanon/Yemen/Gulf: at most two. At least two from elsewhere.

## 4. Write the issue object

Copy the previous issue object, change `id`, `week`, `date` (the Sunday), `date_label`,
then replace every field. Write it into `regime_state.json -> issues` with a small Python
script (`json.load`, append, `json.dump(..., indent=2, ensure_ascii=False)`), never by hand
editing the 650 KB file.

### Sentence-level rules, with examples from past audits

| Rule | Wrong (shipped, then corrected) | Right |
|---|---|---|
| Lead with the fact, not the theme | "The week turned on a reversal." | "On September 22 Anthropic released Claude Opus 5.5 at $4 per million input tokens..." |
| Quotes are verbatim or not quotes | "Warsh said labour markets were 'basically fine'" (a paraphrase) | Warsh said "Labor markets are quite stable" |
| No invented causation | "after the Treasury bought back fewer bonds than expected" (no source) | "even as the Treasury kept up its enlarged buybacks" (what the report said) |
| No invented precision | "nine votes short of sixty" (there was no vote) | "a cloture vote is set for September 15" |
| Attribute claims | "Six transcripts showed..." | "Semafor counted six transcripts..." |
| Date every number | "the 30-year rate is 7.03 percent" | "Freddie Mac's 30-year rate rose to 7.03 percent on September 24" |
| Records must be records | "the S&P closed at a record" (it was 1% below) | check the high before writing "record" |
| In-window only | an Enigma break from September 15 presented in a Sept 21-27 issue | context from before the week is labelled as such, or cut |
| Explicit futures contracts | continuous WTI showed -7.9% (a roll artifact) | "the November WTI contract fell 3.8 percent" |
| Timezones | a Polymarket 00:00 UTC print labelled as the next day | use UTC daily closes from `media.py polymarket` |
| Implication is a different fact | implication repeating the summary's 5.18 | a bounded fact the summary did not state |

### Field rules

- `index_title`: one sentence, the week's defining event stated as a move in its trend.
  Never "X happens; Y happens." Example: "The ten-year Treasury yield climbs to its highest
  since 2007 as the rate cycle reaches housing on both sides of the Pacific..."
- `brief`: exactly five lines with anchors `ai, deep-dive, geopolitics, markets, wildcard`,
  each under 30 words, each a fact.
- Each lane: `headline` (≤20 words, declarative, states the theme), `summary` (90-130 words,
  first sentence names an actor, a number or a date), `implication` (one bounded,
  verifiable statement: a count, a reported fact; no number repeated from the summary),
  `evidence` (detail that does not render on the site; anything readers must see goes in
  the summary), `links` ordered by importance (`points` = HN points, 0 if not from HN).
- Geopolitics `items`: 4-6, title = outlet headline + (Outlet, Month D), comment = two
  sentences, about 60 words, tying the story to a regime.
- `commodities`: explicit contracts in item names, `min_change` 3.5-4, a `headline`, a
  summary that leads with the big movers and ends with the forward call.
- `structural_regimes`: update every basket value with a dated reading; spotlight what
  moved; every non-spotlit regime gets a one-sentence `line`.
- `watch_next`: dated events after the week only.
- `annotations`: 10-25 notes for people, places and jargon a non-specialist would stop at,
  45 words max, facts only.

## 5. Check, mechanically, then by reading

```
python3 validate_issue.py            # house rules; fix every ERROR, justify every WARN
python3 validate_issue.py --quotes   # the quote list the audit must check
python3 build_site.py                # link lint, media lint, hover-note lint, renders docs/
```

Then run the `human-voice` and `humanize` passes over all reader text and re-run the validator.

## 6. Audit (never skip)

Four adversarial verifier agents, one per lane group: (1) AI, (2) geopolitics and trade,
(3) markets and commodities, (4) deep-dive, wildcard, briefs, undercurrent. Each gets its
sections of the issue JSON, the quote list, and these instructions: open every URL, check
every number, date, quote and attribution against it, assume the draft is wrong until
shown right, report each problem as exact old text → new text with the source URL. About
20 searches each.

Apply fixes as exact-match string replacements in a script that raises if the old text is
not found (silent misses are how corrections get lost). Re-run the validator and the build
after applying.

Typical audit yield is 30-60 corrections. If an audit comes back with fewer than ten, it
was not adversarial enough; re-run it with a stricter prompt.

## 7. Record and ship

1. Ledger: append `## Issue N — Week of ...` to `the-current-regime.md`: states and
   momentum, the spine of the week, lane choices (what led and why, which coverage debts
   were paid, what was left out and why), then `### Issue N audit` with the corrections.
2. `next-issue.md`: rewrite for N+1 (leads in view, forward calendar, lane rules, basket
   values to diff against, contract-roll notes).
3. Look at the page: screenshot `docs/issues/<N>.html` at desktop width and inside a 375px
   iframe (headless Chrome will not render below about 500px directly).
4. Commit (`Issue N: <index_title paraphrase>`) and push to `main`.
5. Email: `python3 send_regime_email.py --test` sends a preview to the owner only, and needs
   `GMAIL_APP_PASSWORD`. Never send to the list; that is the owner's step.

## Failure modes to expect, and the fix

| Symptom | Fix |
|---|---|
| A feed WARNs dead in FEED HEALTH | widen that lane with the research agent; say so in the ledger |
| GDELT 429 | normal; the world feeds and regional outlets cover it |
| A site blocks fetches (fortune, reuters, bloomberg) | `https://r.jina.ai/<url>`, or cite a syndicated copy and name the original |
| Search budget runs out | finish verification with WebFetch on primary pages; never guess |
| A number has two sources that disagree | use the primary data (FRED, Treasury, exchange, agency), say which |
| Polymarket gamma 403 | use the list endpoint or `media.py polymarket`; Kalshi unauthenticated returns null prices |
| An aggregator says the company's own figure differs (issue 17's "dozens" vs "over 100") | open the company's own page; the aggregator was wrong |
| "X opened an investigation on <date>" | check whether the date is when it began or when it was reported or confirmed |
| An agent reads a number off a table that disagrees with the last issue | re-pull it from the CSV (FRED) before believing either |
| A hover note's term was cut by an edit | build_site fails on the dead note; delete or re-point the annotation |
| A sentence compares two futures contracts | make sure both are the same contract month, or say they are not |
| Validator ERROR you believe is wrong | fix the text anyway if you can; otherwise explain in the ledger and tell the owner |
