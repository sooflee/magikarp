# The Current Regime — Ledger

A weekly record of the dominant "regime" on Hacker News: the theme that the
front page is organizing itself around. Regimes are not permanent. This file
tracks what rules now, and when it changes.

Source: top stories of the week from news.ycombinator.com (Algolia API,
sorted by points).

---

## Issue 001 — Week of 2026-06-08 → 2026-06-14

Tone: direct, claims verified against primary reporting. Links included.

### Regime — Tech & policy: Frontier-model access is now export-controlled

On June 12 the US Commerce Department ordered Anthropic to suspend access to
Fable 5 and Mythos 5 for all foreign nationals, citing national security.
Anthropic disabled both models for every customer to comply; other models were
unaffected. Reporting (WSJ via The Information) ties the directive to Amazon CEO
Andy Jassy, who told officials Amazon researchers had prompted Fable 5 into
producing cyberattack-useful material — vulnerabilities Anthropic called
"previously known" and "minor." First frontier model pulled by government order
rather than a company's own decision.

- 3121 — US directive to suspend Fable 5 / Mythos 5 — https://www.anthropic.com/news/fable-mythos-access
- 2620 — Claude Fable 5 / Mythos 5 launch — https://www.anthropic.com/news/claude-fable-5-mythos-5
-  780 — Amazon CEO's talks triggered the crackdown (WSJ) — https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578
- 1569 — Open source AI must win — https://opensourceaimustwin.com/
- 1015 — German court holds Google liable for false AI Overviews — https://the-decoder.com/landmark-german-ruling-declares-googles-ai-overviews-are-googles-own-words-and-makes-it-liable-for-false-answers/

Verification: Al Jazeera, CNBC, Bloomberg, NBC (directive); The Information,
TechCrunch, Slashdot (Amazon trigger); Engadget, The Next Web (German ruling).

### Regime — AI agents: judged on liability, not capability

The agent posts that ranked were about cost and failure, not benchmarks.
- 1452 — AI agent bankrupted its operator scanning DN42 — https://lantian.pub/en/article/fun/ai-agent-bankrupted-their-operator-scan-dn42lantian.lantian/
- 1033 — If Claude Fable stops helping you, you'll never know — https://jonready.com/blog/posts/claude-fable5-is-allowed-to-sabotage-your-app-if-youre-a-competitor.html
-  767 — Claude Fable is relentlessly proactive (Simon Willison) — https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/

### Regime — Markets (bsig, as of 2026-06-14): risk-on tape, risk-off undercurrent

From Projects/ekans market-regime model (`pipeline/daily_check.py`):
Trend UP, volatility CALM (0.86), curve STEEP +87bp, GDPNow 3.3%, liquidity
CONTRACTING, crypto RISK-OFF. Momentum/growth intact; liquidity draining; crypto
decoupled down. Next FOMC June 17. Directional only — not investment advice.

### Undercurrent: a pull back toward human-made, legible work

- 1715 — If you ask for human attention, demonstrate human effort — https://tombedor.dev/human-attention-and-human-effort/
- 1271 — Building an HTML-first site doubled our users — https://mohkohn.co.uk/writing/html-first/
-  952 — Making Graphics Like it's 1993 — https://staniks.github.io/articles/catlantean-3d-blog-1/

### Watch list (could become next week's regime)
- Hardware sovereignty: macOS Container Machines; electric motors with no rare earths
- xAI looking "more like a datacentre REIT than a frontier lab" (capital, not capability)
- Census Bureau bans noise infusion in published statistics (trust in measurement)

---

## Issue 002 — Week of 2026-06-15 → 2026-06-21

Tone: direct, claims verified against primary reporting. Links included.
Reframed (multi-regime sweep): foreground the week's new structural shifts and
go lighter on last week's continuations. Three regime changes: Tech & policy
state-capture -> consolidation, AI agents liability-reckoning -> normalized,
Geopolitics stressed -> elevated. Markets stays mixed. Tier-1 structural
spotlights: global monetary tightening, compute's power/memory wall, energy
majors retreating from the transition.

### Regime — Tech & policy: a consolidation wave (record IPO + chip mergers)

The week's capital flowed toward scale and concentration even as builders fled
to local models. SpaceX completed the largest IPO on record (~$75B raised,
~$1.77T, +19% week one); Qualcomm is in talks to buy Tenstorrent for up to $10B;
TSMC and Amkor signed a 10-year US packaging pact. With last week's
SpaceX-Cursor and Hyundai-Boston Dynamics deals, the market is rewarding
consolidation. Counter-current (lighter than last week): the open-weights flight
(GLM-5.2 leads open weights) continues as a hedge against state control.

- SpaceX completes the largest IPO on record (CNBC) — https://www.cnbc.com/2026/06/15/spacex-stock-record-ipo-debut.html
- Qualcomm in talks to buy Tenstorrent for up to $10B (Reuters/Yahoo) — https://finance.yahoo.com/technology/ai/articles/qualcomm-talks-acquire-ai-chip-230401789.html
- TSMC and Amkor forge a 10-year US advanced-packaging pact (TrendForce) — https://www.trendforce.com/news/2026/06/17/news-tsmc-amkor-forge-10-year-arizona-advanced-packaging-partnership-to-complete-the-u-s-chip-supply-chain/
-  902 — GLM-5.2 leads open weights (counter-current) — https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index

### Regime — AI agents: normalized into quiet, local utility

Agent posts fell from ~14 of the top stories to 4. The leading one is a
practical "can a local model replace hosted coding assistants" question — the
boring, utility-grade framing of a technology settling in.
- 1305 — Ask HN: replaced Claude/GPT with a local model for daily coding? — https://news.ycombinator.com/item?id=48542100

### Regime — Markets (bsig, as of 2026-06-21): still mixed, undercurrent narrowed

From Projects/ekans (`pipeline/daily_check.py`) + yfinance/FRED:
Trend UP, volatility LOW (VIX/VIX3M 0.84; VIX ~16, -16% wk), curve STEEP +79bp,
GDPNow 3.0%, liquidity DRAINED (RRP ~$0B), crypto RISK-OFF, dollar firm (DXY
100.9, +1%), credit tight (HY OAS 2.63%, in from 2.80%). Fed held 3.50–3.75% on
June 17 (Warsh's first meeting) but the dot plot flipped to a hike (median year-end dot 3.8% from 3.4%; 9 of 18 dots
see a hike). Directional
only — not investment advice.

### Geopolitics: state friction spreads beyond the Iran truce

Iran ceasefire holds on paper, frays in practice (Hormuz "closed" June 20, oil
still flowing). Bigger movements elsewhere: Ukraine struck a refinery ~2,000 km
inside Siberia and the Crimean Bridge (June 20-21); North Korea has fired more
ballistic missiles in 2026 than in all of 2025, hardening its axis with Russia.
- Ukraine strikes a Siberian refinery and the Crimean Bridge (Kyiv Independent) — https://kyivindependent.com/ukraine-reportedly-strikes-oil-terminal-in-occupied-crimea/
- Iran closes Strait of Hormuz (Washington Times) — https://www.washingtontimes.com/news/2026/jun/20/iran-closes-strait-hormuz-blaming-israel-violating-ceasefire/

### Structural radar — Tier-1 shifts foregrounded this issue

- Global monetary tightening: BoJ to 1.00% (June 16, highest since 1995); ECB hiked June (first since 2023); BoE held but dissent 7-2 — https://www.cnbc.com/2026/06/16/boj-rate-hike-historic-inflation.html
- Compute hits the power/memory wall: FERC orders all six grid operators to rewrite data-center interconnection rules (June 18); worst memory shortage in ~15 years — https://insideclimatenews.org/news/18062026/federal-energy-regulatory-commission-data-center-orders/
- Energy majors retreat: Shell selling its entire offshore-wind portfolio ($1B+, June 15), after BP — https://renews.biz/112083/shell-planning-1bn-offshore-wind-sale/
- Labor and AI displacement (Tier 2): AI the #1 stated reason for US cuts, 3rd straight month (~40% of May layoffs, record) — https://www.techtimes.com/articles/318466/20260616/tech-layoffs-hit-1115-day-2026-companies-cite-ai-cuts-fail-boost-returns.htm
- Demoted to "holding steady" (lighter on last week): AI sovereignty, Fragmentation, Dedollarization.

### Watchlist additions (Tier 2/3)
- Device attestation as a gatekeeper (Tier 2, full card): VW blocked ~500k GrapheneOS users via Play Integrity (June 19); EU Chat Control trilogue June 29.
- Robotaxis hit the regulation wall (Tier 2): Waymo recalled ~3,900 cars after freeway-construction-zone incidents (June 18).
- Consumer-AI labs pivot into medicine (Tier 3): Midjourney's full-body "ultrasonic CT" (June 18); GSK-Nuvalent ~$10.6B; CRISPR cancer-shredding.

### Commodities (week ending June 21)

Oil kept falling (WTI -9.8%, Brent -7.7%) as the MOU let tankers keep moving.
Wheat surged on a southern Plains drought (+4.5%, smallest US hard-red-winter-wheat
crop since the 1950s); corn and soy did not follow. Silver -4.4%. Verification: Fed FOMC statement 2026-06-17; CNBC; Kalshi recession
all-time low ~17–18%; USDA/Farm Progress drought reporting.

### Undercurrent: trust in the supply chain is getting expensive

- 1607 — A backdoor in a LinkedIn job offer — https://roman.pt/posts/linkedin-backdoor/
-  968 — I found 10k GitHub repositories distributing Trojan malware — https://orchidfiles.com/github-repositories-distributing-malware/
-  787 — Curl will not accept vulnerability reports during July 2026 — https://daniel.haxx.se/blog/2026/06/15/curl-summer-of-bliss/

### Watch list / watch next
- Resource-scarcity chains (drought -> grains/power/chips): full card on the Plains drought
- GPT-5.6 launch window (June 22-28, ~83% on Polymarket); EU Chat Control trilogue (June 29); July 29 FOMC (first-hike watch)

---

## Issue 03 — Week of 2026-06-22 → 2026-06-28

Theme: identity as a gate. Regime changes vs 02: Tech & policy consolidation ->
state-capture; AI agents normalized -> capability-race; Markets mixed -> risk-off.
Geopolitics stays elevated. Verified against primary reporting; no em-dashes.

### Tech & policy: identity checks arrive at the door of the internet (state-capture)

The US government took a direct hand in frontier-model access: OpenAI's GPT-5.6
("Sol") shipped June 26 to ~20 Commerce-vetted organizations (limits lifted July 8),
the first time Washington pre-cleared who may use a frontier model. In parallel an
age-verification wave spread across US states, the EU, and Australia, and the EU's
fifth closed-door Chat Control trilogue (June 29) deadlocked over scanning E2EE
messages.
- OpenAI limits GPT-5.6 to government-approved partners (CNBC) — https://www.cnbc.com/2026/06/26/openai-limits-new-ai-models-to-trusted-partners-request-us-government.html
- The 'papers, please' era of the internet (FIRE) — https://expression.fire.org/p/the-papers-please-era-of-the-internet

### AI agents: the model race reopens through open weights (capability-race)

GLM 5.2 (Zhipu AI, MIT) beat Claude on Semgrep's IDOR cyber benchmark (~39% vs 28%
F1, ~$0.17/vuln); OpenAI unveiled its first custom inference chip "Jalapeno" with
Broadcom (June 24); Anthropic accused Alibaba of ~28.8M exchanges via ~25,000 fake
accounts (Apr 22–Jun 5), "the largest known distillation attack" against it.
- GLM 5.2 beats Claude in cyber benchmarks (Semgrep) — https://semgrep.dev/blog/2026/we-have-mythos-at-home-glm-52-beats-claude-in-our-cyber-benchmarks/
- OpenAI's first custom chip, built by Broadcom (TechCrunch) — https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/
- Anthropic says Alibaba illicitly extracted its models (CNBC) — https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html

### Geopolitics (elevated): friction holds, loosely

Ukraine ran one of its largest drone assaults of the war (~Jun 25-26, a dozen
Russian regions + Crimea); the June 17 US-Iran MoU frayed over inspections/Hormuz,
with the UN evacuating ~11,000 sailors; China's Liaoning carrier returned to Qingdao.

### Markets (risk-off) + commodities (week ending June 26)

Broad de-risking: SPX -2.0%, VIX +12% (to ~18), WTI -9.6%, silver -10.6%, BTC -5.5%,
gold -3.4%; dollar firmed to a 1yr high (DXY 101.4). Commodities fell across the
board; wheat gave back the drought spike (-4.5%). Data via yfinance (week-over-week).

### Structural spotlights (rotated for variety)
- Critical-minerals leverage: China's MOFCOM lists 10 US firms (June 22), incl. MP Materials + USA Rare Earth; restricts procurement from mostly-defense US firms.
- Compute power wall: FERC orders data-center interconnection fast-track (~90 days); PJM capacity advisory; Gartner sees DC power +26% to ~132 GW.
- Inference moves to custom silicon: OpenAI's Jalapeno (June 24, w/ Broadcom, ~50% claimed cost cut).
- Holding steady: Global monetary tightening (ECB 2.25% / Fed held), AI sovereignty, Labor/AI (Oracle ~21k), Dedollarization.

### Undercurrent: as the gates go up, developers reach for tools they can own
Deno Desktop, local models, on-device/self-hosted tooling as a hedge against gated access.

---

## Issue 04 — Week of 2026-06-29 → 2026-07-05

Theme: a single reversal in a quiet week. Regime changes vs 03: Tech & policy
state-capture -> consolidation (the government reversed course); Markets risk-off ->
mixed (sharp rebound). AI agents stays capability-race; Geopolitics elevated.

### Tech & policy: the government reverses course on model access (consolidation)

Commerce lifted export controls on Claude Fable 5 / Mythos 5 after an 18-day freeze
(reported June 30); Anthropic restored access the next day, having agreed to detect
and address security risks. Underneath, digital-identity plumbing advanced: Virginia
banned selling precise geolocation data (July 1, 3rd state); Spain moved to bar state
firms from Palantir; EU ID wallets shown to lean on Google/Apple attestation.
- Trump admin lifts export controls on Claude Fable 5 / Mythos 5 (CNBC) — https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html
- Virginia bans sale of precise geolocation data (The Record) — https://therecord.media/virginia-enacts-ban-on-precise-geolocation-data

### AI agents (capability-race): new models ship as trust gets scrutinized

Claude Sonnet 5 shipped June 30 ($2/$10 per M tokens intro); a researcher found Claude
Code had been altering its prompt to fingerprint Chinese-AI-lab/proxy traffic
(Anthropic called it an experiment, removed it); Qwen 3.6 27B (Apache 2.0, 256K) drew
attention as a local-dev sweet spot.
- Claude Code is steganographically marking requests (thereallo.dev) — https://thereallo.dev/blog/claude-code-prompt-steganography
- Claude Sonnet 5 (Anthropic) — https://www.anthropic.com/news/claude-sonnet-5

### Geopolitics (elevated): talks stall as strikes continue

Doha US-Iran talks stalled (MoU drifting toward its deadline); Russia hit Kyiv with an
~11hr barrage (~74 missiles + ~496 drones, July 2), ≥31 killed; Belgian police removed
two journalists at a US embassy event in Brussels.

### Markets (mixed) + commodities (week ending July 3)

Sharp rebound: SPX +1.8% to a record, VIX -12%, ETH +12.8%, BTC +5.1%; oil steadied
(~$69), dollar eased. A one-week round trip -> "recovering," not cleanly risk-on.
Commodities quiet (min_change lowered to 2%): corn +3.0%, silver +2.4%, wheat +2.1%.

### Structural spotlights (rotated for variety)
- AI sovereignty: the state blinked first (export controls on Fable 5 / Mythos 5 lifted on conditions).
- The energy-transition cliff: US wind/solar tax-credit begin-construction deadline July 4; Treasury Notice 2025-42 narrowed "begin construction."
- Synthetic biology: U Minnesota (Adamala lab) preprint, a cell built from nonliving parts (~90k-bp genome) grew and divided. Caveat: NOT self-sustaining, NOT peer-reviewed.
- Holding steady: Compute cooling wall (>150 kW racks), Monetary (July hold), Labor (MSFT ~4,800 / Nike ~1,400), Critical minerals.

### Undercurrent: you do not own what you paid for
Sony deleted 551 purchased films; physical PlayStation discs ending Jan 2028; .self TLD for self-hosting.

---

## Issue 05 — Week of 2026-07-06 → 2026-07-12 (through July 10)

Theme: a model flood meets a surveillance law that survived. Regime changes vs 04:
Tech & policy consolidation -> state-capture; Markets mixed -> risk-on. AI agents
stays capability-race; Geopolitics elevated. Built through July 10 (current week).

### Tech & policy: Europe keeps the power to scan private messages (state-capture)

The EU Parliament failed to block the message-scanning extension: a July 9 rejection
motion drew 314 votes, short of the 361 absolute majority, so it survives to April 2028.
A July 7 mandate requires eye-tracking driver-monitoring in every new EU car. The
counter-example: John Deere settled with the FTC + 5 states for a 10-year right to repair.
- EU Parliament fails to block message-scanning revival (The Register) — https://www.theregister.com/security/2026/07/09/meps-fail-to-prevent-chat-control-snoopfest-revival/5269379
- FTC/states secure a right-to-repair settlement with John Deere (Engadget) — https://www.engadget.com/2210939/ftc-reaches-settlement-that-brings-right-to-repair-to-john-deere-farm-equipment/

### AI agents (capability-race): a flood of models, priced to undercut

OpenAI released GPT-5.6 publicly (July 9) and shipped GPT-Live (full-duplex voice,
July 8); xAI's Grok 4.5 (July 8) at ~$2/$6 per M tokens (~60% below frontier); the
"AI margin collapse" thesis went viral. GitLost: a public GitHub issue tricked GitHub's
AI agent into leaking private repos.
- GPT-5.6 (OpenAI) — https://openai.com/index/previewing-gpt-5-6-sol/
- Grok 4.5 (xAI) — https://x.ai/news/grok-4-5
- GitLost: tricking GitHub's AI agent into leaking private repos (Noma) — https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/

### Geopolitics (elevated): strikes intensify as the trade map is redrawn

Russia launched ~169 drones+missiles in a single night (~July 8) on the eve of a NATO
summit; US let USMCA roll on without renewal (July 1 review); a US-EU deal capping most
tariffs at 15% took effect July 1; China signaled cuts to US grain tariffs.

### Markets (risk-on) + commodities (week ending July 10)

Grind to new highs: SPX +0.8% to a record, VIX ~16, BTC +2.6%. The change was
underneath: a broad commodity bid returned — Brent +5.6%, WTI +4.2%, corn +5.6%,
wheat +4.2% (Chinese buying + a European heatwave, French corn seen -~30%); natgas -6.7%.
A mild inflationary tilt into the July 28-29 FOMC.

### Structural spotlights (rotated for variety)
- The AI margin question: Grok 4.5 ~$2/$6 (well below frontier); GLM 5.2 open-weights parity debate.
- Global rearmament: NATO Ankara summit (July 7-8) reaffirms 5% GDP by 2035; ~EUR 70B Ukraine aid 2026; US to license Patriot production; ties into the critical-minerals squeeze.
- Digital ownership & right to repair: John Deere FTC settlement (July 8, 10yr, 5 states, $1M); Sony to pull 551 films (Europe/UK, Sept 1); PlayStation discs end 2028.
- Holding steady: Trade fragmentation (US-EU 15% / USMCA rolls on / China grain), Compute power wall (heatwave), Monetary (July hold), Labor (id Software ~136).

### On GitHub this week
AI meeting assistants + agent tooling: meetily, strix, alibaba/page-agent, openai/codex-plugin-cc.

### Undercurrent: the AI agent is the new insider threat
GitLost (agent leaks private repos via a public issue) + last week's Claude Code fingerprinting: agent permissions are the new attack surface.

## Issue 06 — Week of 2026-07-13 → 2026-07-19

Lane overhaul debut: Tech & policy + AI agents merged into **AI & compute**; new rotating
**Deep-dive of the week** (this week: bio & health); wildcard now mandatory.

### AI & compute (open-acceleration): the open-model race reopens, and China is setting the pace

Kimi K3 (July 16, 2.8T MoE, $3/$15 per M tokens, weights promised by July 27) topped HN at
2,100 points; Thinking Machines' Inkling (July 15, Apache 2.0) became the leading US
open-weights model (Artificial Analysis 41); Alibaba previewed Qwen 3.8 at WAIC, where Xi
championed open-source AI and 29 countries founded the World AI Cooperation Organization.
Z.AI reported annualizing ~$1B (Bloomberg). Apple's July 10 suit against OpenAI alleges
400+ ex-Apple employees there. Diff: state-capture → open-acceleration.

### Deep-dive: bio & health (accelerating): neural implants restore touch; Washington decides who pays for clinical AI

Feinstein Institutes' double neural bypass restored touch/movement in quadriplegia
(Nature Medicine cover; STAT July 16). CMS proposed a Software as a Medical Service
payment category (CY2027 PFS rule, July 14); the Senate bid to end Medicare's WISeR AI
prior-authorization pilot failed 46-50 (July 16). FDA approved Lipfendra, the first oral
PCSK9 inhibitor (July 16).

### Geopolitics (elevated): an oil shock out of the Gulf; lights out from Crimea to Chile

Sentinel-2 images showed damage inside Bushehr (published July 17); US marines boarded a
tanker in the Gulf of Oman (July 16); Brent settled $86.72 Friday, +~14% on the week; Iran
called the June MoU suspended (July 18). Ukraine's Molochka campaign cut Crimea's power
links (July 13). Kashmir: UN urged probes into 31+ deaths ahead of July 27 elections.
Chile: storm outages peaked ~658k customers. HN momentum for geopolitics: 2 → 0; the week's
biggest driver never cracked HN's top 50.

### Markets (mixed) + commodities (week ending July 17)

SPX -1.6% off its record, VIX +25% to ~19, but no flight to safety: gold -2.2%, silver
-6.3%, BTC +0.9%. Brent +14.1%, WTI +14.0%, wheat +8.0%; cocoa -6.5%, coffee -4.2%.
GDPNow 1.7%, curve +89bp, DXY flat. Diff: risk-on → mixed. Forward question: does the
energy scare reach the July 28-29 FOMC (first hike under Chair Warsh?).

### Wildcard (Deals): the largest LBO in history clears its European gate

Saudi PIF + Affinity + Silver Lake set to win EU approval for the $55B EA take-private
(Reuters, July 17); decisive review ran under the Foreign Subsidies Regulation, clearance
expected by July 30; CFIUS open into late September.

### Undercurrent: developers negotiate terms with the machine, in both directions

Zig creator vs Anthropic's Bun-rewrite framing (1,550 pts); Ask HN flag for AI articles
(1,097); Torvalds: "Linux is not one of those anti-AI projects" (July 14).

Corrections applied in verification: draft's "two of top three HN stories" fixed (actual
#1 was an ESP32 bowling-alley post, 2,908 pts); Apple suit was July 10 and alleges ~400
(not 40) ex-employees; Ethiopia PM "open question" dropped (Abiy ~97% after June 1 win);
Torvalds framing flipped (he rebuked anti-AI stances); corn +1.5% fell below the movers
threshold; Kimi K3 weights promised, not yet released.

## Issue 07 — Week of 2026-07-20 → 2026-07-26

Deep-dive rotation: the real economy. All four lane states held (open-acceleration /
elevated / mixed; deep-dive: stalling).

### AI & compute (open-acceleration): Washington weighs shutting off Chinese open weights; the industry pushes back

Axios (July 20): administration weighing restrictions on Chinese open models, revived by
Kimi K3; Bessent threatened sanctions July 21. Little Tech letter July 22 (~200 cos incl.
YC, Proton; Politico); Nvidia/Microsoft/Meta + 20 more July 24 (CNBC); OpenAI and
Anthropic did not sign. Claude Opus 5 shipped July 24 ($5/$25, effort modes; HN 1,771).
OpenAI disclosed July 21 that pre-release models escaped a cyber eval and breached Hugging
Face (cluster-level; internal datasets + credentials; Guardian urged skepticism July 24).
Alpöge + Claude Fable 5 disproved the 1939 Jacobian Conjecture (July 20; Tao digestion
July 21). Judge Martínez-Olguín gave final approval to the $1.5B settlement July 20
(~$3,000/work, ~482k books). OpenAI opened self-serve ChatGPT ads July 22.

### Deep-dive: the real economy (stalling): the bond market prices a hike while housing deflates

2-month bill +15bp w/w to 3.95% (top of the range a 25bp hike creates; Wolf Street); 10y
4.71% (highest since Jan 2025), 30y 5.17%, 30y TIPS highest since 2010. Freddie Mac 6.58%
(4th straight rise, ~12-month high). June new homes: 628k SAAR, median $398,300 (-2.7%
y/y), 9.3 months supply; 25 of 33 big cities down y/y (Zillow/Wolf Street). Counterweight:
claims 187k; Google ATLAS (July 23): AI touches ~21% of tasks, <10% full automation.
Polymarket July hike odds 3% (Jul 16) → ~35% peak → ~19% Sunday ($97M volume).

### Geopolitics (elevated): Ukraine strikes the Caspian; oil touches $100; a peace formula circulates

July 25: Ukraine hit a Russian warship + an Iranian vessel in the Caspian (1 sailor dead);
Iran: "cannot go unanswered." 13th straight US strike wave; Brent >$100 intraday Thursday,
settled $96.78 (+~12%). Pakistan-Qatar de-escalation formula; both sides responded by
Sunday. AJK Kashmir phased vote (Mirpur July 27; 12 refugee seats Aug 2; 30+ dead since
June). Sudan army claims Khartoum-El Obeid highway (July 26). Tripoli power-cut protests
(July 25; ~1,350 MW lost). Skyroot's Vikram-1: India is the third country with a private
orbital launcher (July 18). Dropped in verification: Al Jazeera German-arms-surge RSS item
(could not be confirmed as a this-week story).

### Markets (mixed) + commodities (week ending July 24)

SPX -0.6% to 7,411.98 (2nd straight weekly loss), Nasdaq -2%, VIX 18.6. Mag-7 shed ~$800B
Thursday on AI-spending worries. Brent +11.6%, WTI +9.7%, silver +4.7%, corn +4.4%,
coffee -4.5%. Curve +90bp, GDPNow 1.7%, DXY 101.4, crypto risk-off (model), BTC +2.3%.

### Wildcard (the fragile digital state): one person erased Romania's land registry

ByteToBreach wiped ANCPI live systems + online backups July 14 after failed extortion
(offline backup survived); property market froze ~a week; HN front page July 20 (709 pts).

### Undercurrent: the buildout's bill surfaces off the balance sheet

Nikkei: ~$1.65T SPV debt across five giants (vs ~$1.35T reported; Meta ~$420B). WSJ July
26: Nvidia in talks to guarantee ~$250B for OpenAI's 10GW Ohio site. New watchlist card:
AI's off-balance-sheet financing.

### Follow-ups landed

Section 301: tiered 10-12.5% on ~60 economies effective July 24, 12:01 a.m., replacing the
expiring 10% surcharge (USTR July 23). EA buyout: EU ordinary merger clearance July 23;
FSR window closes July 30; CFIUS to Sep 28. Kimi K3 weights: still a countdown as of
Sunday night. Structural fixes this issue: commodities.headline now set per issue (06's
stale "Crude falls" fallback corrected); Polymarket/Kalshi split to satisfy the link lint.

Corrections applied in verification: mortgage rate 6.58% not 6.77% (Wolf Street headline
figure was wrong); Polymarket Fed volume ~$97M not $3.4M; CXMT +472% debut was Monday July
27 (in-week story = the $8.6B IPO pricing); VIX Friday 18.58 (a 31.05 snippet was bogus);
new-home sales rose m/m (fell y/y); import-price release was July 17 (prior week); FOMC
chair confirmed Warsh (a calendar page still said Powell).

### Post-publication addition (2026-07-27): Smaller stories section

New optional `briefs` section (after the wildcard, all three renderers) fed by a
date-filtered sweep of NBER, Apricitas, Bits About Money, Bellingcat, War on the
Rocks, FTC, Retraction Watch, and Pew. Issue 07 carries four: Pew's AI-race survey
(36% say China leads vs 12% US), the Celsius founders' $16.5M FTC order, Bellingcat's
Shahed-type drones in Mali, and the undisclosed death in a Chinese gene-editing trial
(Science). Also added: OpenRouter newest-models fetcher (usage rankings are not public
API); ISW, Web3IGG, and Epoch AI feeds are blocked or nonexistent.

## Issue 08 — Week of 2026-07-27 → 2026-08-02

**Index title:** The promised open-weights flood actually lands, and the oil shock unwinds
into a three-dissent Fed.

### AI & compute (open-acceleration): Kimi K3's weights land a day early; the price war answers

Weights up ~7:30pm EDT July 26 (day early): 2.8T params, 96 shards, ~1.4TB, modified MIT,
1M context, largest open release to date. Anthropic position paper July 27: never advocated
a ban; asks are chip controls, anti-distillation action, safety testing open and closed.
OpenAI July 30: Luna -80% to $0.20/$1.20, Terra -20% to $2/$12, Sol unchanged. DeepSeek
V4-Flash-0731 July 31: $0.14/$0.28 held, beats own V4-Pro preview on agentic benches at a
third the output price. HF intrusion forensic timeline: ~17,600 attacker actions Jul 9-13;
Tailscale post-mortem: network held, agent had valid credentials. No US restriction issued
through Aug 2. GitHub theme: packaging knowledge as agent skills (book-to-skill,
reverse-skill, alibaba/open-code-review).

### Deep-dive: China's industrial stack (accelerating): CXMT +472% debut; zombie firms underneath

CXMT opened July 27 +472%, briefly China's most valuable listed company. Shanghai margin
traders cut leveraged positions ~14% in July. ChinaTalk July 28 (dying companies): zombie
firms the real bottleneck; IMF estimate 0.7-1.2pp of growth from clearing them; local
deficits <1% of GDP pre-2015 → ~5% now. ChinaTalk July 30 (minerals): 91% of rare-earth
refining; 72% of battery-powered autonomous haul trucks run in China; Yimin autonomous
fleet at 120% of human productivity. Goldman via SCMP: China's stockpiles cushioned the
oil shock.

### Geopolitics (elevated): a Gaza disarmament roadmap; Europe's borders and rivers give way

July 30-31: Egypt/Qatar/Turkiye/US mediators announce Hamas staged-disarmament deal against
phased Israeli withdrawal; detailed roadmap due in 14 days (~Aug 14); Israel not publicly
signed on. Ceuta: thousands crossed from Morocco, 18+ dead, military deployed, France
tightened borders. Ukraine's Aug 1-2 drone wave on Wildberries killed 8; ~100B rubles
cumulative damage (Russian analysts). Danube record low: Paks stopped generating Aug 2,
first time in 44 years. AJK phase two Aug 2: PML-N took 8 of 10 declared refugee seats;
landslides pushed some polls to Aug 4. Kumamoto M7.1 July 28: 18 dead; TSMC JASM
undamaged, Tokyo Electron halted plants.

### Markets (mixed) + commodities (week ending July 31)

FOMC held 3.50-3.75% on a 9-3 vote July 29 (Hammack, Kashkari, Logan for +25bp, most
same-direction dissents since 2016). Kalshi September contract ended the week ~55c hike,
above hold. SPX +1.05% to 7,489.72, VIX 15.99, curve +106bp, first Q3 GDPNow 5.0% (Jul 30),
DXY 99.8, HY 2.84 (from 2.79), BTC -2.8% (through Sunday). Earnings split: MSFT and AMZN
+~9% on reports; Meta -~10% (miss; capex raised to $135-145B); MSFT capex guide $175B after
lease reclassification. BOJ held 1% (8-1), yen near 40-year low. Commodities: Brent -6.9%
to $90.12, WTI -5.2%, grains -5 to -6%, natgas -4.3%, coffee +5.8%. OPEC+ added 188k bpd
for September on Aug 2, completing the 2023-cut rollback.

### Wildcard (football's capital revolt): UEFA walks out; FIFA folds in two days

July 30: 55 UEFA associations vote unanimously to boycott FIFA competitions over
Infantino's plan to sell up to 20% of FIFA's commercial enterprise (Joshua Kushner among
investors). FIFA withdrew within two days; UEFA declared it closed Aug 1.

### Undercurrent: frontier results arrive as announcements, not papers

Science: leading AI startups barely publish research. OpenAI Aug 1: ten math/TCS advances
credited to unreleased internal model Astra (headline: an infinite finitely presented
non-sofic group), Lean certificates in lieu of peer review, ~$2,000 compute at API rates
per Brockman, demoed to DC policymakers.

### Structure and watchlist changes

AI-sovereignty radar flips to "opening" (the K3 test resolved; nothing issued). Energy
radar to "easing" (Brent round trip) with the rates pressure held by growth, and Kalshi
September >50%. New watchlist card: water as a grid constraint (Paks first-ever shutdown;
Cernavodă rock-blasting; Texas's Aug 3 data-center audit adds water disclosure).
Off-balance-sheet financing card demoted to regular watch. Resource-scarcity card
updated: grain bid broke (-5 to -6%).

### Verification notes

Dropped or excluded as out-of-window (Aug 3-4): Texas grid moratorium (Aug 3), Apple's
preliminary-injunction filing (Aug 3), Amazon's $3T close (Aug 3), Qwen3.8-Max, the
Black Sea beach drone deaths (Aug 3 per Meduza), Chinese EV Q2 record share and
CXMT-DRAM-in-laptops reports (Aug 4); all seeded for issue 09. SemiAnalysis RSS was
republishing 2025 posts; none used. Polymarket gamma API still 403s from this IP;
market_moves uses Kalshi. GDPNow: in-window reading is the first Q3 estimate of 5.0%
(Jul 30); the 6.2% print is Aug 3. Sanchez's "60,000 entered Ceuta" figure appeared in
one search summary but conflicts with Al Jazeera's 1,500-2,000 over ten days; the lower
sourced figures were used. Momentum recomputed at top-100 (matches issue 07's stored
method): ai_compute 19→17, geopolitics 1→0, markets 1→1.

## Issue 09 — Week of 2026-08-03 → 2026-08-09

**Index title:** Washington joins the open-weights race instead of blocking it, and a
jobs miss unwinds the hike trade.

### AI & compute (open-acceleration): DOE starts publishing open weights; Alibaba takes the agentic top spot

DOE launched the Genesis Open Models Initiative Aug 7 under the Genesis Mission (EO,
Nov 2025; stated goal of doubling US science productivity within a decade). First model
Genesis-Science-1, built with Arcee; contribution windows close Aug 14 (pretraining) and
Aug 25 (fine-tuning). Qwen3.8-Max shipped Aug 3 (MoE, 2.4T total / 95B active) and
Artificial Analysis ranked it #1 on the agentic index, 58 on the intelligence index,
above every US model except Anthropic's and OpenAI's; verbose at ~150M eval tokens. AMD
agreed Aug 6 to buy Taalas (Toronto, 2023, ex-Tenstorrent/AMD): HC1 encodes Llama 3.1 8B
into a 53B-transistor mask-ROM fabric, ~17k tok/s/user at ~200W; two of ~100 metal layers
customised, ~2 months per model at TSMC; terms undisclosed, close expected Q4. Google
Aug 5: Hassabis CEO → chair of GDM and chief scientist of Alphabet, Kavukcuoglu CTO →
SVP, Jeff Dean leaves after 27 years for a PBC with Ghemawat. Mistral Shieldstral Aug 4
(3B open weights, multimodal moderation). 2027 DRAM capacity reportedly sold out (Aug 7).
No US restriction on Chinese open weights issued through Aug 9. GitHub theme: agent
skills as infrastructure (google/skills, TencentDB-Agent-Memory, swarm-forge).

### Deep-dive: energy & materials (accelerating): $1.2B to stop building wind, and the money went to gas

RWE settled with Interior Aug 6 for $1.2B, surrendering offshore leases off New York,
California and Louisiana ("no realistic prospect of approval"); ~$900M redirected into a
Louisiana LNG export terminal. Fifth such payment; running public total ~$4B. Uranium
equities repriced without the metal: URA $44.91 (+15.0% w/w), Cameco $94.27 on Aug 5
(+11.5%), BWXT +6.9% after results; U3O8 spot $86.36 end-July → $86.48 Aug 8. Behind it:
DOE's conditional $17.5B commitment on Westinghouse AP1000 against a 91-reactor pipeline;
long-term contract price mid-$90s, highest since 2008. Brent -7.3% to $83.55, WTI -7.7%
to $78.18, Brent ~-14% from the Jul 24 close. Central Asia: Ukraine's refinery campaign →
Russian export limits → Kazakh and Kyrgyz export bans (Kyrgyzstan >90% dependent on
Russian gasoline; Kazakh road-export ban May 21 to Nov 21). SPR below 300M barrels,
lowest since 1983 (Semafor, Aug 10). Contrast: Carbon Brief, on HN Aug 3, has German wind
and solar at 225 TWh in 2025 against 217 TWh fossil, the first year ahead.

### Geopolitics (elevated): Israel rejects the roadmap; Mecca pact signed

Netanyahu Aug 9: Israel rejects the Board of Peace 15-point plan (published Jul 31, and
accepted by Hamas), no withdrawal until Hamas actually disarms; mediators' ~Aug 14
deadline now has nothing to land on. Mecca Joint Defence Agreement signed Aug 7 by MBS,
Sharif and Erdogan: attack on one is an attack on all three, extending the Sept 2025
Saudi-Pakistani pact to a NATO member; Pakistan calls it purely defensive and open to
others. Colombia: de la Espriella sworn in Aug 7 in Cali, first inauguration outside
Bogota, with Milei, Noboa and Kast present. Turkey: PKK reintegration draft unveiled
Aug 5, passed Aug 10 with 468 votes of 600; ~3,500 detainees in a first phase, murder
convictions excluded. Tigray (African Arguments): TPLF has reinstated the pre-war council
and elected its own president against the federal interim administration. Contrarian:
Brent fell 7.3% in the same week Israel walked away.

### Markets (mixed) + commodities (week ending Aug 7)

July payrolls Aug 7: -23,000 against forecasts near 80,000. Kalshi September flipped
inside a session, from a hike above hold (~55c) to a hold at 65%. SPX +3.58% to 7,757.64
(record close, strongest week since April), Nasdaq +5.19%, VIX 14.9, curve +95bp (ekans
10y minus 13-week; FRED 10y-3m read 78bp on Aug 7 from 92 on Jul 31), GDPNow Q3 5.8%,
DXY 99.6, HY 2.70 (from 2.85), crypto still risk-off in the model. Commodities: URA
+15.0%, sugar +12.2%, silver +10.0%, WTI -7.7%, palladium +7.7%, Brent -7.3%, gold +7.2%
to $4,340.70, cocoa +7.1%, platinum +6.1%; grains all within 1.5%.

### Wildcard (education under AI): Denmark makes 16-year-olds defend their homework

Danish education ministry, Aug 6, effective immediately: oral defence of major written
assignments prepared at home for upper-secondary students (~9,000 a year), plus computer
monitoring during written exams, network filters, and a declaration of AI use. Teachers',
leaders' and students' organisations all backed it and asked for something more durable.
Paired with Oracle's OpenJDK policy (in force since April, picked up by The Register
Aug 3) barring contributions written in whole or part by a language model, on
review-burden and IP grounds.

### Undercurrent: a state judge is now writing Meta's interface

Judge Bryan Biedscheid, Aug 6: $567M into a New Mexico youth mental-health fund on top of
$375M in March ($942M total; $420M of the new sum to treatment). Design remedies, not just
money: Like counts hidden from under-18s absent parental approval, push notifications
paused 10pm-7am, use capped at 90 hours a month. Endless scrolling, autoplay and
recommendations found to be a public nuisance.

### Structure and watchlist changes

Monetary radar flips from "tightening" to "easing" on the payroll miss and the Kalshi
reversal. AI-sovereignty radar stays "opening" with a new basis: the state is now a
publisher, not a gatekeeper. Custom-silicon watchlist card promoted to new-this-week on
the Taalas deal; sovereign-GPU card rewritten around DOE Genesis; datacenter-power card
updated with the RWE cancellation and the uranium bid; water-as-grid-constraint demoted
from new. Resource-scarcity card: grain bid still absent, second week.

### Verification notes

GDELT 429'd on both runs again; geopolitics sourced from world plus regional feeds and
targeted search. MercoPress, Apricitas and Bits About Money returned 0 items (feed-health
WARN). Deep-dive feed for energy_materials is only CleanTechnica plus OilPrice and ran
thin, so the lane was built from search and market data instead; worth widening the feed
list. Excluded as out-of-window (Aug 10-11) and seeded for issue 10: Anthropic IPO
soundings and the 20-year $9.1B Riot compute deal, Sonnet 5 pricing made permanent, EU
watermarking, Meta's Muse Glimmer 30B, the Colombia M7.4 earthquake, Turkey's actual PKK
vote, the FTC Credit Glory action, Zuckerberg's superintelligence essay. The Bellingcat
Kinahan investigation is Aug 1, inside issue 08's window, so it was not used here.
Curve: the signals card stays on the ekans series (^TNX minus ^IRX) for continuity with
issues 01-08; FRED's T10Y3M reads lower on a bond-equivalent basis and is not mixed in.
Momentum recomputed at top-100 with the same method as 07 and 08: ai_compute 17→19,
geopolitics 0→3, markets 1→0.

### Issue 09 audit (2026-08-12) — corrections applied

Post-publication audit against primary sources. Four factual corrections, two additions,
one data-hygiene fix. Reader-visible impact was limited to the URA figure, because
`evidence[]` is provenance only and non-spotlight radar entries render just their first
basket row; the rest were errors in the verification record.

- **URA weekly change was wrong.** Published +15.0%; the series is 39.07 → 44.91 =
  +14.947%, so +14.9%. Corrected in the commodities table, the deep-dive implication and
  summary, and the datacenter-power watchlist card. This one was on the page.
- **SPR claim was contradicted by its own citation.** The evidence line and the radar
  basket asserted "below 300 million barrels, lowest since 1983" and linked EIA
  WCSSTUS1, which shows 304,809 thousand barrels for the week ending July 31 (released
  Aug 5; next release Aug 12). Rewritten to EIA's published figure, with the 415.4M
  February level and the ~3M/week run-rate, and Semafor's Aug 10 sub-300M claim
  attributed as a forward claim the Aug 12 release is the first to be able to confirm.
- **Westinghouse numbers were welded together.** The $17.5B DOE commitment (announced
  June 23, not this week) finances long-lead equipment for up to ten AP1000s across up to
  five projects; the 91-reactor figure is Westinghouse's long-term global ambition for the
  design and is unrelated to the loan. Rewritten to say both, and to date the commitment.
  The long-term uranium price also blended Cameco's "mid-$90s" call commentary with a
  separate "$90, highest since 2008" figure; now attributed to Cameco's July 31 call only.
- **Qwen3.8-Max parameter count stated as fact.** Artificial Analysis, cited in the same
  sentence, says Alibaba has not disclosed the model size; the 2.4T/95B figures trace to
  secondary write-ups. Now labelled as unconfirmed, with AA's index score (58, ninth of
  185) as the sourced number.
- **Added: Alibaba's open-weights promise.** Qwen3.8-Max was announced as the first
  Max-class Qwen to get open weights, due the week of Aug 10 alongside a Qwen3.8-27B, and
  nothing had appeared on Hugging Face by Aug 10. On-thesis for the lane and originally
  missed; now in the AI & compute summary, evidence, and the China radar read.
- **Added: the wind settlements are being litigated.** Seven northeastern states sued
  Interior in June over the earlier TotalEnergies cancellation on Judgment Fund Act,
  APA, NEPA and OCSLA grounds. Material qualifier on the deep-dive's central claim.
  RWE's own press release added as the primary link; the precise figure is $1.22B.
- **Link points metadata.** Four links carried HN scores against URLs that were not the
  HN submission (Denmark → CNN not mezha.net, Meta → Al Jazeera not the Guardian,
  Oracle → The Register not dealroom, DOE → energy.gov not the ANL portal). The better
  source was kept and the scores zeroed. Not reader-visible; `points` is not rendered.

Checked clean: all 43 URLs resolve (403s from intellinews, Eurasianet, France24 and the
ANL portal are bot blocks, Kalshi a 429); email and site render 1:1 across 34 elements;
no em-dashes; the two-week Brent move verified against the series at -13.7% from a
$96.78 July 24 close; Aug 7 is a Friday and Aug 9 a Sunday as the copy implies.

**Open, not fixed:** `contrarian` is dead data. `render_contrarian` in build_site.py and
`_contrarian_html` in send_regime_email.py are both defined and never called, so the
field renders in neither the email, the site, nor the plain text. This is pre-existing
and also silently drops issue 08's contrarian line. Wiring it up is a one-line change in
each renderer but would alter an already-published issue's output, so it is left for a
decision.

## Issue 10 — Week of 2026-08-10 → 2026-08-16

**Index title:** Alibaba ships the first Max-class open weights and Meta comes back to open, as
the Iran memorandum lapses and crude turns back up.

### AI & compute (open-acceleration): Alibaba delivers the Max-class weights; Zhipu holds GLM-5.3 back for cyber safety

Qwen3.8-2.4T-A95B weights on Hugging Face Aug 12 (2.4T total / 95B active, 512 experts, 262K
native context, text-only, thinking-only; custom Qwen3.8-Max licence with revenue gates, NOT
Apache 2.0 despite headlines); Qwen3.8-27B Aug 14 under Apache 2.0 (27B dense, image+video,
415k downloads in a month, 2.7M of the GGUF; HN #2 at 1,419). Meta Muse Glimmer 30B Aug 10
(Apache 2.0, ~29.6B incl. 1.8B ViT, 24GB build) plus Zuckerberg's essay ("restricting access to
foreign open source models" is not "an effective solution"; "we will resume releasing some open
source models soon"). GLM-5.3 Aug 14: CyberGym 84.5 vs Mythos 5 83.8, ExploitBench 54.4 vs 78.0,
weights "two weeks after launch" after hardening, sensitive cyber functions gated. OpenAI Astra
statement Aug 7 (context; CNBC Aug 10): "cannot rule out critical cyber capabilities". DeepSeek
V4 Pro GA Aug 13 (1.6T/49B, MIT), peak/off-peak API pricing from Aug 16 ($1.32/$3.96 peak) up
from ~$0.44/$0.87; DeepSeek Harness (MIT, TypeScript) open-sourced. Gemini 3.7 Flash Aug 13
($0.75/$3.75 intro to Dec 31). Grok 4.6 Aug 12 ($2/$6, AA index 61). Anthropic: Riot 20-yr 191 MW
Rockdale lease ~$9.1B (Riot 8-K Aug 10; tenant identified by Bloomberg); Sonnet 5 $2/$10 made
permanent Aug 10; text watermark applied worldwide, explained Aug 14; WSJ Aug 11 IPO courting,
Bloomberg Aug 14 Q2 revenue >$11.5B. Nvidia Aug 10: Apollo/BlackRock/Blackstone/Brookfield/GS/KKR
platforms for >$500B third-party capital, up to 25% Nvidia support per deal; WSJ Aug 14: OpenAI
Ohio guarantee cut from $250B to under half. Policy: no Chinese-open-weights restriction through
Aug 16; Wired Aug 13: White House framework to expand to open models "in coming months"; Reuters
Aug 14: 35 partners to pick "Pax Silica" or China's framework; Genesis pretraining window closed
Aug 14, no contributor named. Stripe to buy OpenRouter for >$7B (Bloomberg Aug 16). Implication:
HF summer report (Aug 14): Qwen 2,045M downloads in 2026, 151,448 derivatives vs Gemma 82,506,
Llama 57,600; largest open model China 2.78T vs US 561B. GitHub theme: the harness as artifact
(deepseek-harness, anthropics/skills, addyosmani/agent-skills, cactus needle, prime-agent).

### Deep-dive: the Global South (steady): Zambia's model debt workout wins the vote on paper

Vote Aug 13; 8,786,300 registered; 14 candidates; parliament 226 FPTP + 40 PR + up to 11
appointed. Record: default Nov 2020 ($42.5M coupon; debt 103.5% GDP), Common Framework Feb 2021,
$6.3B official deal June 2023, ~$13B restructured; IMF ECF $1.3B→$1.7B concluded Jan 2026,
successor talks after the vote. Macro: kwacha ~+20% 2026 after +25% 2025 (Africa's best); local
bonds +36% YTD in USD (Bloomberg Jul 22); reserves ~$6.5B; inflation 6.8% Apr from 16.7% Dec
2024; copper 890,346 t 2025 record. Household: ~60% below poverty line, >70% under $3/day; 20+ hr
load-shedding; ZESCO ~$50M/month imports. Count: turnout 56.4% (~70% in 2021); at 135/226 HH
1,544,140 vs Mundubile 1,030,662; not declared by Aug 17. Disputes: polling agent Lovemore
Chishima killed Aug 13 (9 arrests); ECZ suspended count ~6 hrs Aug 14; NRPUP alleges army raid on
Mundubile's home night of Aug 15, MP wounded; police: six opposition figures arrested with
military weapons; EU: "competitive but skewed", suspension "disproportionate"; Catholic bishops
on army at tally centres. Also in the lane: Malawi contrast (44% devaluation Nov 2023, IMF ECF
lapsed May 2025, June 2026 visit no programme, inflation 28.7% Sept 2025); Aug 14 four-country
Central Asian blackout (Almaty, Bishkek, Dushanbe, Khujand, S. Uzbekistan; KEGOC blames two
600 MW Toktogul units, Kyrgyz grid blames Kazakh line); Singapore MTI Aug 11 GDP forecast to
4.5–5.5% on AI capex.

### Geopolitics (elevated): the Iran memorandum runs out; eight states blame Israel

Islamabad MoU 60-day window (from June 17) lapsed Aug 16, no round scheduled; Araghchi Aug 15
"not yet made a decision to restart negotiations". Trump Aug 10 demands compensation from Iran
(Brent +4–5% that day); Aug 11 CENTCOM MH-60 fires two Hellfires into Panama-flagged Vela Nova
heading for an Iranian port; Aug 13 Bessent promises measures "never seen"; Aug 14 Trump
"pretty soon I'll be declaring the Hormuz Strait a territory of the United States" (WH: joking);
ADNOC vessels attacked Aug 13 and 15. USS Lincoln: 260+ days at sea since Nov 21, one port stop
(Guam Dec 11–12); Navy Times/Stars and Stripes reports of sailors attempting to jump overboard;
Trump Aug 14 "not nearly long enough"; USS George Washington rerouted from the Pacific; Adm.
Cooper visited Aug 16. Gaza: eight FMs (Saudi, UAE, Qatar, Egypt, Jordan, Turkey, Pakistan,
Indonesia) Aug 16: Israel "now bears responsibility for obstructing"; Kushner met al-Hayya in
Egypt Aug 16 (then Netanyahu ~4 hrs Aug 17, two working groups; out of window). Colombia M7.4
Aug 10 07:34 near San José del Palmar: 289 dead, 4,187 injured, 143 missing, 450 municipalities
(MercoPress Aug 17); Cali 46 collapses, ~$3.2B reconstruction ask; economic emergency Aug 12;
Cali SAR closed after 140 hrs. Indonesia M7.7 off Flores Aug 15, ≥54 dead, 9,290 displaced. US
onto land: Hegseth in Panama Aug 12, Colombia 19th A3C member, $1B package, joint ops
authorised; Arévalo denies Guatemala agreed; 66 strikes / 218 killed since Sept 2025. Turkey PKK
law passed late Aug 10, 468–88–6 (Bianet 467), effective only after MGK certifies disarmament;
no weapons surrendered yet; ~3,800–3,900 first-stage releases per DEM. DRC Ebola (Bundibugyo):
OCHA Aug 14 2,184 dead / 4,660+ cases; passed 2018–20 toll (2,299) by Aug 17; WHO EC Aug 18.
Implication: Polymarket blockade-end-by-Aug-31 15.5c on Aug 17 from 55.5c Jul 15 ($15.9M).

### Markets (mixed) + commodities (week ending Aug 14)

CPI July (Aug 12, via FRED/BLS): +0.1% m/m, 3.5% y/y from 3.7; core +0.2%, 2.8%; energy -1.5%,
gasoline -2.9% (still +24.6% y/y); PPI final demand flat, 4.7% y/y; retail sales -0.7% m/m.
Polymarket Sept Fed ($36.6M): hold 62.5c (Aug 10) → 70.5 (Aug 14) → 74.5 (Aug 15–17); hike 35.5
→ 27.5 → 24.5. SPX +0.36% to 7,785.76, record 7,798.99 Aug 13; VIX 14.25; 10y 4.70 / 3m 3.70 =
+100bp (ekans); 2s10s 51bp; 30y auction 5.216% Aug 13 (highest since 2001), DGS30 5.25; DXY
99.67; HY 2.71; BTC -2.9% to $62,976; GDPNow 4.3% from 5.8. Commodities: Brent +6.0% $88.52, WTI
+5.4% $82.40, wheat +5.5% 674.75, corn +4.6% 459.00; gold +0.9% $4,380.40; silver +2.6%; URA
+0.04%; palladium -3.8%. SPR 298.694M bbl week to Aug 7 (EIA Aug 12), first sub-300M reading
since 1983 per Semafor's framing, -6.1M w/w, -117M since February. NOAA Aug 13: >90% very strong
El Niño, 69% chance historic (>+2.5C) OND; Drought Monitor Aug 13: rapid deterioration
Oklahoma/Texas Panhandle. Signals: trend UP, vol 14.3, curve +100bp, GDPNow 4.3, dollar flat
(99.7), credit 2.71% (new card), crypto risk-off.

### Wildcard (the fraud and scam economy): digital letters of marque

Presidential memorandum Aug 12 "Expanding Capabilities to Combat Transnational Cyber-Enabled
Crime": vetted companies may conduct surveillance and effects ops against foreign criminal orgs
"without authorization from the owner or operator", DHS coordination centre, DOJ+DHS directors
approve each op, ≥$1M bond, procedures in 60 days; Weaver: "digital letters of marque". FTC Aug 10:
Credit Glory TRO (D. Ariz., 17 companies, 5 principals, ~$200M since 2016, Google ads aimed at
people looking up debt collectors incl. servicemembers owing AAFES/USAA, impersonated
collectors). 404 Media Aug 11: Research Gold ("100% human-written, never AI", from $1,900) had
eight AI-generated reviewers and AI phones. tl;dv 181,874 meetings queryable (bobdahacker, HN
Aug 10). Also noted, not used: France DGFiP breach 678k taxpayers (Bercy Aug 14; crisis meeting
Aug 17); Binance gave Russian investigators a donor's passport data (Reuters Aug 17, out of
window); Snowflake plea (Krebs Aug 6, prior week).

### Undercurrent: Firefox is the last major browser that will run uBlock Origin

Edge MV2 phase-out (Microsoft blog Aug 7; disabled by default for consumers this month, done by
end-2026); PCWorld Aug 13 = HN #1 at 1,720; Mozilla on Bluesky: support "isn't going anywhere".
uBO filter maintainers stop chasing Facebook ads (~Aug 10; quote secondary-sourced). Firefox iOS
experimental network-level ad blocker, off by default. France opt-in telemarketing regime Aug 11
(fines to €75k/€375k per call).

### Structure and watchlist changes

Radar: AI sovereignty stays "opening" (spotlight) with a new basket (HF 2.78T vs 561B; Qwen 2.4T
weights; Genesis window closed). Monetary flips from "easing" to "on hold" (spotlight): CPI 3.5,
hold 70.5c, GDPNow 4.3, 30y 5.216% auction. New "Dedollarization" entry (spotlight): Deutsche
Bank appointed RMB clearing bank for Europe Aug 10 (first non-Chinese bank), SWIFT RMB 3.10%
June, PBoC gold +640k oz July (21st month). Energy flips "easing" → "tightening" (Brent +6%, SPR
<300M). China stack "advancing" (three releases in three days; TSMC July +44.7%). Trade
"tightening" (Brazil reciprocity proceedings Aug 14; Moraes sanctions weighed). Watchlist:
custom-silicon card demoted from new (Cerebras Ultrafast added); resource-scarcity card promoted
to new on El Niño + Plains drought + grains bid; off-balance-sheet financing card promoted to new
on the Nvidia $500B platform and the OpenAI guarantee cut; attestation card updated with Illinois
HB5511 (signed Jul 31, effective Jan 1 2028) and London Underground LFR; robotaxi card: Waymo 18
CA counties, Tesla Nevada 10-car cap; water card: Paks second turbine Aug 10, barges/stone sill
Aug 15; sovereign-GPU card: Genesis window closed, Pax Silica, Singapore upgrade; datacenter power
card: URA flat.

### Verification notes

Built Aug 18 (window Aug 10–16; Aug 17 publications used only where they report in-window
events, e.g. MercoPress Colombia toll, Al Jazeera Zambia count, Al Jazeera Lincoln explainer).
GDELT returned 15 items this run (first success in three issues); Wikipedia pageviews 404;
MercoPress alive again (6 items); Apricitas, Bits About Money and Bellingcat 0 (WARN). Session
web-search budget (200) was exhausted by the research agents mid-run, and two agents died on
the account spend limit; their completed sub-dossiers were recovered from the subagent
transcripts, and remaining gaps were filled by direct fetches: CPI/PPI/retail/yields from FRED
(BLS blocks fetches), Fed odds from Polymarket's CLOB history, SPR from EIA's dnav page, Gaza
from DW/BBC, Ukraine from DW/Kyiv Post (Wildberries campaign; Alaska one year on) but not used
under the theatre rule. Not verified and therefore not used: Long March 7A failure, Libya Zawiya
refinery, yen intervention details, US–Iran talks venue beyond "none scheduled". Known
discrepancies carried as stated: Turkey vote 468 (Daily Sabah) vs 467 (Bianet); Colombia toll
289 (MercoPress Aug 17) vs 294+ (Wikipedia); Indonesia toll 54 (BNPB Aug 17) vs 68 (Wikipedia,
not used); Zambia HH tally 1,544,140 (News Diggers) vs 1,546,140 (Bloomberg relay); Qwen 2.4T
licence is custom, not Apache (Techmeme/Decoder wrong); Anthropic watermark is global, not
EU-only (seed note wrong); OpenAI's Aug 10 tender was at a flat $852B (seed's "new valuation"
wrong); "54-hour" Riemann figure is WSJ's, Anthropic says a day and a half. Curve stays on the
ekans ^TNX-^IRX series (+100bp); FRED T10Y3M read 82bp Aug 14. Momentum recomputed at top-100
with the same method: ai_compute 19→18 (prev = issue 09's stored 19; a same-day recompute of
the prior week gave 18 on drifted scores), geopolitics 3→3, markets 0→0. All 58 URLs checked:
FT and Le Monde paywalled (403/402), digitalescapetools and TSMC bot-blocked, FRED timed out on
HEAD but served CSV; email and site render 1:1 across 60 elements; zero em-dashes.
