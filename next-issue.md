# Seed notes for Issue 20 — week of October 19 – 25, 2026

Verify everything against primary reporting before publishing. Issue 19 was built on October 19.
Follow `.claude/skills/current-regime/PLAYBOOK.md` step by step.

## Leads already in view
- **China Q3 GDP, released Monday October 19 (in 20's window):** +4.5% y/y, with September industrial output +5.5% y/y. The first read on whether the export/price windfall is reaching domestic demand. Source the NBS release, not the wire summary.
- **France after 17 October:** curfews in parts of Paris and other cities; Macron refused the interior minister's resignation and ordered a review of planning and intelligence failures; the arrest count rose to about 2,400. The political question is whether the cost-of-living movement becomes an April presidential force.
- **Gulf war:** Iran's seven-day Hormuz offer (reopen on day six if the US lifts the port blockade and oil sanctions) is still live; Trump has threatened to "finish the job"; Riyadh's airport was hit for a third day and missiles reached Dammam; Brent settled at $109.86, the highest since May 19. Watch the offer, the insurance/freight market and OPEC+ on November 1.
- **AI:** Meta's 816B Muse Spark Open and DeepSeek's 763B MIT release reset the open-weight price floor; the licence terms (attribution, $20M model-as-a-service trigger, gated repo) are the next argument. AI credit stress is the other thread: CoreWeave -15.5% with bonds near 15%, Oracle -8.8%, Nebius -10%, Microsoft out of Nscale's Essex project. Eight states sued OpenAI over child safety (October 14) and the FTC sent CIDs to OpenAI and Anthropic; Character.AI filed Chapter 11 with Disney as the $20M opening bidder. All three need a rendered home or a ledger reason.
- **Markets:** FOMC October 27-28 (Polymarket hold 87.5c, hike 12.5c); ECB October 29; US Q3 GDP and September PCE October 29; BoJ October 29-30; Brazil runoff and Serbia election October 25; Israel election October 27. The ten-year ended at 5.09% and the 10s-2s curve at 35bp despite CPI 3.7% and PPI 6.3%.
- **Energy & materials (deep-dive 20):** OPEC+ November 1; Brent $110 and the Hormuz risk premium; Russian refinery strikes and the diesel licence to April 2027; silver's bust (December $57.31, more than 50% below January's record); coffee at a one-month high; China's September chip and vehicle export mix. Source from the energy/materials feeds, not HN.

## Forward calendar
Oct 19 China Q3 GDP and September activity data · Oct 20 Netflix Q3 earnings · Oct 21 US 20-year bond auction · Oct 22 US 5-year TIPS auction · Oct 25 Brazil runoff and Serbia snap election · Oct 27 Israel general election · Oct 27-28 FOMC · Oct 28 Bank of Canada and RBNZ · Oct 29 ECB, BEA Q3 GDP and September PCE · Oct 29-30 BoJ · Nov 1 OPEC+ seven · Nov 3 US midterms · Nov 18-19 APEC Shenzhen (Putin has proposed a Trump-Putin-Xi meeting; the White House has not agreed) · Nov 29 Spain general election · Dec 2-4 RBI · Dec 14-15 G20 at Doral.

## Lane rules for 20
- Deep-dive rotation: **energy & materials**. `python3 sources.py deepdive 20`.
- AI led with open weights in 19, money in 18, regulators in 17. Lead with chips, labor, security, policy or users in 20, not another launch roundup and not another "open weights shipped" card. The open-weight story is now a watchlist theme.
- Geopolitics led with France in 19, Yemen/Saudi in 18, Brazil in 17. Iran or Ukraine may lead, but do not let the Gulf repeat as a bare escalation story; find the new decision point (the Hormuz offer, the Saudi air-defence failure, the insurance market). Theatre rule still applies: at most two restricted slots, at least two from other theatres.
- Coverage debt: **Oceania** (last seen issue 16). Put an Australia, New Zealand or Pacific story in geopolitics, the briefs or the undercurrent, or say why not.
- Topics not seen in 17-19: **crypto/fintech, education, fraud/cyber/crime, privacy/digital rights**. The wildcard shortlist is exactly those four. Wildcard 19 was culture/media; do not repeat it.
- Undercurrent 19 was non-AI (Starlink sabotage). Keep 20 non-AI if possible; the "at least every other week" rule is satisfied but the section is stronger outside the AI box.

## Recurring refresh
- Momentum prev from 19: ai_compute 14, geopolitics 3, markets 1.
- Baskets from 19 (Friday Oct 16 unless noted): 10y 5.09 (5.24 Oct 9), 2y 4.74, 30y 5.43, DFII10 2.74, T5YIE 2.37, HY OAS 3.31, DXY 101.84, VIX 19.99, gold Dec 4,181.10, Brent Dec 109.86, WTI Dec 99.02, WTI Nov 101.41, NG Nov 3.116, corn Dec 474.25, GDPNow 3.6 (Oct 15), mortgage 7.40, S&P 7,659.44, BTC 81,500.80, ten-year auction 5.300% (Oct 7), RBI 5.50%.
- Curve: 10s-2s 35bp; 10y-3m 83bp. Issue 19's `curve_bp` is 83, not the ekans line's 103; recheck DGS3MO before diffing.
- Polymarket (Oct 18): Oct Fed rise 12.5c, hold 87.5c, Iran ceasefire through Oct 82.5c and through Nov 44.0c, Flávio 78.8c, Lula 21.5c, Netanyahu 30.5c, Eizenkot 45.7c.
- HF 30-day (Oct 19): GLM-5.3-Flash 6,536,333; Bonsai 2 GGUF 3,268,225; Qwen3.8-27B 7,458,401; MiMo-V2.6-Pro-RL 103,098; Kolibri-1 19,881; EmbeddingGemma 2 167,750; DeepSeek-V4.1-Flash-1017 17,924 (created Oct 17).
- WTI November (CLX26) expires around October 20: use December from 20 on. Brent December, gold December, silver December, copper December, corn December, wheat December, soybeans November, coffee December, cocoa December, sugar March.

## Big-story sweep notes for 20
Do not lose: China Q3 GDP (Oct 19), France's post-riot curfews and Macron's review, the Hormuz offer and Saudi air-defence failure, AI credit stress (CoreWeave, Oracle, Nebius, Nscale), the eight-state OpenAI suits and FTC CIDs, Character.AI's Chapter 11, Taiwan/China chip controls, Nvidia's HBM base-die re-cut with Samsung/SK Hynix/Micron on TSMC 3nm, Apple above $5T, the IMF's 3.1% forecast, ECB approval of UniCredit's Commerzbank stake, the Starshield slowdown, the CS conference submission caps and California's billionaire-tax estimate.
