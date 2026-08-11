# Seed notes for Issue 10 — week of August 10–16, 2026

A running stash for next week's issue. Verify everything against primary reporting
before publishing (house rule). Issue 09 was built on August 11, so several strong
Aug 10-11 stories were excluded as out-of-window and lead this list.

## Already-landed stories that belong to 10's week

- **Anthropic goes for the biggest IPO ever (Techmeme, Aug 11).** Courting investors,
  touting growth. Same 48 hours: a 20-year, $9.1B compute deal with Riot Platforms for
  191 MW at a Rockdale site, Claude Sonnet 5's introductory pricing made permanent at
  $2/$10 per million, and EU-region Claude output getting invisible watermarks plus C2PA
  metadata. Four separate moves; the IPO is the frame that ties them.
- **Meta's Muse Glimmer 30B (Aug 10).** Apache 2.0, distilled from a larger Muse system,
  2B ViT encoder feeding a 28B decoder, 4-bit build under 20GB so it fits one consumer
  GPU. Landed with Zuckerberg's 6,500-word superintelligence essay the same day, which
  404 Media covered unkindly. Techmeme's read: he returns to "open" arguments at an
  opportune moment for him.
- **Colombia earthquake (Aug 10).** M7.4 near San José del Palmar, 132 dead, 570 injured,
  1,600+ buildings damaged, strongest this century; hit three days into de la Espriella's
  term. Emergency declared.
- **Turkey's PKK law actually passed (Aug 10),** 468 votes of 600, ~3,500 detainees in
  phase one. Issue 09 covered the Aug 5 draft; the passage and the first releases are the
  follow-through.
- **OpenAI $7B employee tender at a new valuation; head of ethics Chloé Bakalar departs**
  after the head of safety (Techmeme, Aug 10). The exits are becoming a pattern worth a
  paragraph.
- **FTC halts Credit Glory (Aug 10-11):** court order, alleged ~$200M taken since 2016 via
  fake credit-repair promises, impersonating collectors, illegal upfront fees. Fraud-economy
  wildcard fodder if 10 rotates that way.
- **Long March 7A explodes 90 seconds after liftoff (Aug 10-11).**
- **Libya: Zawiya refinery on fire after a drone attack; force majeure under consideration.**
  The one live oil-supply risk while Brent keeps falling.
- **Nvidia partners with lenders to finance AI infrastructure (Semafor, Aug 10).** Feeds the
  off-balance-sheet financing watchlist card directly.
- **Yen erases gains after US-Japan intervention (Semafor, Aug 10).**
- **Singapore raises 2026 GDP forecast to 4.5-5.5% from 2-4%, citing AI demand.**

## Forward events that resolve / develop next week

- **Aug 12: July CPI.** First full month of tiered Section 301 duties, with the oil spike
  and its unwind both inside the window. Also the test of the hold the Aug 7 payroll miss
  priced in: GDPNow at 5.8% and payrolls at -23,000 cannot both be right for long.
- **Aug 12: total solar eclipse** over Greenland, Iceland, Portugal and northern Spain.
- **Aug 13: Zambia's general election.** Hichilema's first national vote since 2021.
- **Aug 14: DOE Genesis pretraining contribution window closes** (fine-tuning Aug 25). Who
  actually contributes proprietary scientific data is the finding.
- **~Aug 14: Gaza roadmap deadline.** Netanyahu rejected the 15-point plan Aug 9; Hamas says
  it still accepts. Watch whether the Board of Peace produces anything or the clock lapses.
- **Mid-August: US-Iran memorandum window.** Talks were to resume Aug 3. Trump has said he
  will demand compensation from Iran; crude at $83 is priced for progress.
- **Late August: Nvidia reports.**

## Threads carried from Issue 09 (verify for movement)

- **Uranium.** URA +15% on the week to Aug 7 with U3O8 spot flat at ~$86. Either contracting
  catches up or the equity move gives back. Watch utility contract announcements and the
  Westinghouse AP1000 pipeline.
- **RWE and the wind cancellations.** Fifth payment, ~$4B total. Watch for a sixth, and for
  whether the LNG redirection draws a challenge.
- **SPR below 300M barrels.** Lowest since 1983. Watch EIA weeklies and any refill signal.
- **Mecca Pact.** Pakistan says open to further members. Watch who asks to join, and Iran's
  and India's responses.
- **Central Asian fuel squeeze.** Kazakh road-export ban runs to Nov 21. Watch Kyrgyz
  shortages and any Russian refinery back online.
- **Tigray.** Two claimants, no government. Candidate for an Africa geopolitics slot again
  if anything breaks.
- **AMD-Taalas.** Close expected Q4; watch for a Helios integration roadmap.
- **Meta New Mexico remedies.** Appeal expected; the design orders (Like counts, 10pm-7am
  notification pause, 90-hour cap) are the part with precedent value.
- **EA buyout:** only CFIUS left (Sep 28 outside date).

## Deep-dive rotation

Issue 10 = **the Global South** (rotation: bio&health → real economy → China industrial →
energy&materials → Global South → science; 09 was energy & materials). Source with
`python3 sources.py deepdive 10`, NOT from HN. Candidate threads: Zambia's Aug 13 election
and the austerity record, Colombia's earthquake response under a three-day-old government,
the Mecca Pact as Global South security self-organisation, Central Asian fuel dependency,
Singapore's AI-driven upgrade, African Arguments on reparations and on Tunisia's democratic
unwinding.

## Wildcard rotation

09 used education under AI. Pick a different lane for 10: the fraud/scam economy (Credit
Glory, the Op4G survey-data indictment, ASEAN's cyberscam coordination, the Kinahan Dubai
visas), a specific company (Anthropic's IPO run-up is the obvious one), or culture and the
attention economy.

## Recurring refresh (every issue)

- Momentum: top-100 Algolia date-range queries, classify.py, ai_compute = tech_policy +
  ai_agents + compute_energy (this mapping reproduces 08's stored numbers exactly). Issue 09
  stored cur (ai_compute 19, geopolitics 3, markets 0) is 10's prev.
- Markets/commodities: yfinance weekly closes plus ekans daily_check. ekans ^VIX3M and ^MOVE
  feeds were stale 24 days on Aug 11, so the volatility regime read UNKNOWN and the VIX spot
  was used. Curve stays on the ekans ^TNX-^IRX series for continuity; do not mix in FRED
  T10Y3M, which reads ~17bp lower on a bond-equivalent basis.
- Structural baskets w/w from Issue 09 stored values.
- Watchlist: custom-silicon card is `new: true` this week; demote next issue. Water card
  demoted to regular watch. Resource-scarcity card has now had two quiet weeks; fold or drop.
- GDELT 429'd on both runs again (two issues running). Consider a longer backoff or an
  alternate endpoint; geopolitics is currently carried by world plus regional feeds.
- The energy_materials deep-dive feed is only CleanTechnica plus OilPrice and ran thin.
  Worth adding IEA, EIA Today in Energy, Mining.com or Argus before the rotation comes round.
- MercoPress still returns 0 (three issues running); likely dead, consider replacing it in
  the world group. Apricitas and Bits About Money also 0 again.
- Polymarket gamma list endpoint works and gives 24h volume; the per-market gamma API still
  403s from this IP. Kalshi pages fine for Fed markets.
