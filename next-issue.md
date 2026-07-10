# Seed notes for Issue 06 — week of July 13–19, 2026

A running stash for next week's issue: deferred threads, forward events that resolve
next week, and recurring items to refresh. Verify everything against primary reporting
before publishing (house rule). Issues 03, 04, and 05 were backfilled on 2026-07-10 to
close the June 22 → July 10 gap; Issue 05 was built through July 10, so re-check the
full July 6–12 week if regenerating it on the Monday run.

## Forward events that resolve / develop next week
- **US Section 301 tariff decision (July 20).** Proposed duties near 12% on ~46
  countries; the next step in the tariff campaign after the US-EU 15% deal and the
  non-renewed USMCA both took effect July 1.
- **July 28-29 FOMC.** With commodities firming (crude +4-5%, grains +4-6% this week)
  and the year-end dot still pointing to a hike, watch for the first increase under
  Chair Warsh. Markets priced ~78% hold / ~22% hike going in.
- **US-Iran memorandum window (mid-August).** The 60-day clock on the June 17 MoU keeps
  running without an implementing deal; the Strait of Hormuz stays the pressure point.
- **GPT-5.6 and Grok 4.5 in the EU.** Both shipped outside the EU first; watch when and
  how they clear the bloc's rules (an AI-sovereignty datapoint).

## Threads carried from Issue 05 (verify for movement)
- **AI margin question.** Grok 4.5 at ~$2/$6 per M tokens (~60% below frontier); the
  "margin collapse" thesis (Alderson) vs the "inference is quietly profitable" rebuttal
  (Goedecke). Watch for any frontier price cut or a real inference-margin disclosure.
- **Agent security / lethal trifecta.** After GitLost (GitHub AI agent leaked private
  repos via a public issue) and the prior Claude Code fingerprinting story, watch for
  the next agent-permission exploit. Feeds the "agents are the new attack surface" thread.
- **EU surveillance stack.** Chat Control interim rule now runs to April 2028; the
  permanent CSA Regulation and the driver-monitoring mandate are the live follow-ons.
- **Compute power wall.** US heatwave grid strain; substation lead times 3-5 yrs driving
  "bring your own power" (gas). Watch FERC/PJM follow-through and any new gigawatt deals.
- **Labor / AI.** Microsoft's id Software cuts (~136) were part of the largest Xbox
  restructure; AI remains the #1 stated US layoff reason. Watch the June Challenger print.

## Recurring refresh (every issue)
- Re-run the momentum counts (two Algolia date-range queries, top 50 by points,
  classify.py). Issue 05's stored `cur` values are Issue 06's `prev`.
- Reconstruct markets/commodities from yfinance historical closes for the week
  (WTI, Brent, gold, silver, copper, natgas, corn/wheat/soy; SPX trend, VIX, 10y-3m
  curve, DXY, BTC/ETH). Recompute the week-over-week % changes.
- Recompute each structural basket week-over-week from Issue 05's stored values.
- Check whether Markets tips again (crypto + the commodity bid are the swing factors);
  whether the inflation question forces the Fed's hand at the July 28-29 meeting.
