# Seed notes for Issue 09 — week of August 3–9, 2026

A running stash for next week's issue. Verify everything against primary reporting
before publishing (house rule). Issue 08 was built on August 4; several strong
Aug 3-4 stories were excluded as out-of-window and lead this list.

## Already-landed stories that belong to 09's week

- **Texas data-center moratorium (Aug 3).** Abbott ordered PUCT/ERCOT audits of every
  proposed data center (energy, water, tax breaks, ownership) before grid connection;
  ERCOT postponed its Batch Zero transmission study. 1,800+ queued projects, 474+ GW,
  ~90% data centers. The AI-buildout regime's first hard state-level gate.
- **Apple v. OpenAI escalates (Aug 3).** Apple moved for a preliminary injunction
  against OpenAI and two former staff (Chang Liu, Tang Yew Tan); OpenAI publicly
  disputes the account. Hearing date TBD.
- **Amazon closed above $3T (Aug 3)**, fifth company there, after the +9% earnings pop.
- **Qwen3.8-Max shipped (Aug 3, HN 1066)** and "Don't be a meat proxy" (HN 1725) led
  the front page; Palantir Q2 +93% revenue (Aug 3); Snap Q2 (Aug 3).
- **Black Sea beach drone deaths (Meduza, Aug 3):** seven killed on a resort beach,
  warning system failed; the Wildberries wave continued Aug 3-4 (five killed Moscow
  region, Leningrad warehouse fire). Watch where Russia retaliates.
- **Chinese EV record (published Aug 4):** 10.7% of 18 Western European markets in Q2
  (BYD 2.8%); HP/Asus/Acer began using CXMT DRAM in laptops (Techmeme, Aug 4).
- **Gaza after the deal:** Al Jazeera reports dozens killed after the disarmament
  agreement; Israeli acceptance still not public. Roadmap deadline ~Aug 14.
- **GDPNow jumped to 6.2% (Aug 3)** from 5.0% on strong consumption/investment data.
- **Telegram briefly pulled from the App Store over CSAM (Aug 3); DHS subpoena
  campaign against platform critics (Techmeme, Aug 3).**

## Forward events that resolve / develop next week

- **~Aug 14: Gaza disarmament roadmap deadline** (14 days from July 31). Heavy
  weapons on a 200-350 day clock; Hamas conditions on Israeli withdrawal steps.
- **Mid-August: US-Iran memorandum window.** Talks announced to resume Aug 3. Crude
  at $90 is priced for progress; a breakdown reprices fast.
- **Aug 12: July CPI.** First full month of tiered Section 301 duties plus the oil
  spike and unwind. The pass-through evidence the trade radar is waiting for.
- **Aug 4: deferred AJK polling** (LA-27 Kutla and 52 stations of LA-28) after
  landslides; final Muzaffarabad-division results follow.
- **Kimi K3 fallout:** hosting economics (1.4TB, day-0 hosts), first independent
  benchmarks vs GPT-5.6 Sol and Opus 5, and whether Washington's restriction file
  reopens now that the flood is real.

## Threads carried from Issue 08 (verify for movement)

- **Danube/Paks.** Paks offline since Aug 2 (first time in 44 years); Romania blasted
  rock to keep Cernavodă cooled (Aug 3); Orban says levels may improve. Watch European
  power prices and any EU emergency measure. New watchlist card active (water as a
  grid constraint).
- **Kalshi September hike market (~55c).** Three dissents (Hammack, Kashkari, Logan).
  Watch Fed speakers, the Aug 12 CPI, and whether the market holds above the hold
  contract.
- **Ceuta.** Military deployed; France tightened borders; Schengen-suspension talk.
  Watch the EU response and Morocco's posture.
- **Tigray (African Arguments, Aug):** two rival presidents, no government; war-return
  warnings. Candidate for a geopolitics slot 09 (Africa theatre).
- **HF intrusion:** CSA post-mortem published; watch for regulatory response to the
  eval-escape (NIST? EU AI Office?).
- **EA buyout:** only CFIUS left (Sep 28 outside date).
- **UEFA/FIFA:** withdrawn, but watch for the "binding assurances" mechanism and any
  Infantino counter-move.

## Deep-dive rotation

Issue 09 = **energy & materials** (rotation: bio&health → real economy → China
industrial → energy&materials → Global South → science; 08 was China industrial).
Source with `python3 sources.py deepdive 09`, NOT from HN. Candidate threads: the
Danube/Paks water-cooling crisis as the lead, Texas's audit regime, the OPEC+
rollback completion and $90 crude, US natgas at $2.75, the grain-complex break,
uranium/nuclear operators under water stress.

## Wildcard rotation

08 used culture/institutions (UEFA-FIFA). Pick a different lane for 09: the
fraud/scam economy (candidates: Kinahan cartel Dubai visas (Bellingcat; the RSS link
was mangled, find the real URL), the FBI-agent crypto-theft charge (Techmeme Aug 3),
LG/Samsung banning residential-proxy SDKs on smart TVs (Krebs)), education under AI,
or a specific company.

## Recurring refresh (every issue)

- Momentum: top-100 Algolia date-range queries (matches 07/08 method), classify.py.
  Issue 08 stored cur (ai_compute 17, geopolitics 0, markets 1) is 09's prev.
- Markets/commodities: yfinance weekly closes + ekans daily_check. Note ekans VIX3M
  and MOVE feeds were stale (18d) on Aug 4; check before quoting vol regime.
- Structural baskets w/w from Issue 08 stored values.
- Watchlist: water-as-grid-constraint card is `new: true` this week; demote next
  issue. Resource-scarcity card: grain bid broke; demote or fold into the water card
  if it stays quiet.
- Polymarket gamma API still 403s from this IP (list endpoint works); Kalshi pages
  fine for Fed markets.
- GDELT 429'd on both runs Aug 4; retry, and lean on world/regional feeds otherwise.
- Apricitas and Bits About Money returned 0 items in the briefs sweep (likely just
  quiet); check once.
