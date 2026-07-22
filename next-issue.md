# Seed notes for Issue 07 — week of July 20–26, 2026

A running stash for next week's issue: deferred threads, forward events that resolve
next week, and recurring items to refresh. Verify everything against primary reporting
before publishing (house rule). Issue 06 was finished and shipped on July 21 (the
Friday cron draft had placeholder links and stale numbers; a full verification pass
rewrote it), so re-check July 20-21 developments when building 07.

## Forward events that resolve / develop next week

- **Section 301 tariffs (by July 24).** The July 20 deadline passed without an
  announcement; USTR's Greer said duties near 12.5% on 46 countries could land before
  the 10% Section 122 surcharge sunsets July 24. Whatever lands is the top trade story.
- **EA buyout clearances (July 22 merger decision; July 30 FSR window).** The Saudi
  PIF-led $55B take-private of Electronic Arts; CFIUS outside date September 28.
- **Kimi K3 open weights (promised by July 27).** The test of whether the open flood
  is real. Also watch for Qwen 3.8 weights/model card (preview shipped July 19).
- **Elections in Pakistani-administered Kashmir (July 27)** after 31+ deaths in unrest
  and a UN call for investigations.
- **July 28-29 FOMC.** The oil spike revived the hike question just as GDPNow cooled
  to ~1.7%; watch for the first increase under Chair Warsh. This resolves inside
  issue 07's week if the issue runs through July 29; otherwise it leads issue 08.

## Threads carried from Issue 06 (verify for movement)

- **Gulf oil shock.** Brent settled $86.72 (+14% w/w) on Bushehr damage images and the
  tanker boarding; Iran called the June MoU "suspended" July 18 (nominal clock to
  mid-August). Does crude hold the gain, and does the safe-haven bid finally show up
  (gold fell 2% during the escalation week)?
- **Open-weights race.** Kimi K3 weights due; Inkling adoption (Apache 2.0, AA index
  41); Z.AI ~$1B ARR (Bloomberg); WAICO's 29 founding members; any US policy response
  to Xi's open-source posture.
- **Apple v. OpenAI.** Filed July 10 (NDCal; Tang Tan, Chang Liu named; 400+ ex-Apple
  employees alleged). Watch for OpenAI's response or a TRO motion.
- **Crimea energy crisis.** Molochka campaign cut the peninsula's power/fuel links
  July 13; watch Russian repair/retaliation.
- **Medicare clinical AI.** SaMS payment category comments run to Sept 14; WISeR pilot
  continues after the 46-50 Senate vote.
- **Agent security.** The Claude memory-heist writeup (671 pts) extends the
  GitLost/fingerprinting thread: agent memory is now part of the attack surface.

## Deep-dive rotation

Issue 07 = **the real economy** (rotation: bio&health → real economy → China
industrial → energy&materials → Global South → science). Source with
`python3 sources.py deepdive 07`, NOT from HN. Candidate threads: tariff pass-through
to prices, freight/shipping under the Gulf escalation, housing under a steep curve,
the June/July layoff and hiring prints, GLP-1 consumer-demand effects (deferred from
the bio week).

## Wildcard rotation

Issue 06 used Deals (EA buyout). Pick a different lane for 07: fraud/scam economy,
culture and the attention economy, education under AI, or a specific company.

## Recurring refresh (every issue)

- Momentum: two Algolia date-range queries (top 50 by points, classify.py). Issue 06's
  stored cur values (ai_compute 12, geopolitics 0, markets 2) are Issue 07's prev.
- Markets/commodities from yfinance weekly closes (Brent, WTI, gold, silver, copper,
  natgas, corn/wheat/soy, cocoa/coffee/sugar; SPX, VIX, 10y-3m, DXY, BTC/ETH) plus the
  ekans regime line (`cd ../ekans && .venv/bin/python pipeline/daily_check.py`).
- Recompute structural baskets week-over-week from Issue 06's stored values.
- Watchlist: resource-scarcity card is still `new: true` (wheat +8% two weeks running);
  demote it once the grain bid fades. Device-attestation card was demoted to
  "Still on watch" in 06.
- Polymarket gamma API returned 403 from this IP on direct event queries (the
  sources.py list endpoint works); market_moves stayed empty in 05 and 06. Try again
  or find swing data elsewhere if a market clearly moved.
