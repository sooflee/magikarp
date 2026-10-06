# Seed notes for Issue 18 — week of October 5 – 11, 2026

Verify everything against primary reporting before publishing. Issue 17 was built on October 5.
Follow `.claude/skills/current-regime/PLAYBOOK.md` step by step.

## Leads already in view
- **October 5, already known (in 18's window):** Spain's snap election called for November 29; a grain
  ship sunk in Romania's waters; a Nigerian air force crash with 32 aboard; US B-1s leaving RAF Fairford;
  Turkey and Pakistan agreeing to deploy to Saudi Arabia; the UK threatening to expel Israeli diplomats;
  the Nobel in Medicine (optogenetics); Vaxcyte's pneumococcal readout; the CFTC's proposal on leveraged
  retail crypto trading; the ten-year at 5.31 on the Treasury curve.
- **France:** the pupils' national day of action on October 6, after the lycée blockades (issue 17 wildcard).
- **OpenAI:** FTC civil investigative demands "in the next few weeks"; California's subpoena; whether the
  training pause lifts; more organisations notified. The Florida AG's injunction request (September 28) and
  the three fired safety researchers (October 1) were seen only via Techmeme, never opened: verify.
- **Trump's "Super Intelligence Force"** chaired by DNI Jay Clayton (Politico, October 4): unverified.
- **Ethiopia** after Mekelle: does the TPLF fight on, and does Eritrea enter?
- **Brazil runoff campaign** (October 25); Flávio Bolsonaro and the Banco Master investigation.
- **Irkutsk plague death** (October 2): only the Kyiv Independent; check for WHO or Russian confirmation.
- **Yemen:** Saudi-backed counteroffensive near Taiz; Yemeni forces retaking Mocha was reported October 6.

## Forward calendar
Oct 6 French pupils' day of action · Oct 7 FOMC minutes (RBI decision expected, unverified) · Oct 8 NOAA
ENSO · Oct 13 Apple smart-home event (Bloomberg) · Oct 25 Brazil runoff, Serbia snap election · Oct 27
Israel election · Oct 28 Fed, Bank of Canada, ECB (28-29) · Oct 29 BEA personal income · Nov 1 OPEC+ seven ·
Nov 3 US midterms · Nov 12 OpenAI-Cursor · Dec 14-15 G20 at Doral.

## Lane rules for 18
- Deep-dive rotation: **the real economy** (issue 18). `python3 sources.py deepdive 18`.
- AI led with regulators vs OpenAI in 17, pricing in 16: lead with something else (chips, money, users,
  labor, open weights).
- Geopolitics led with Brazil in 17, Serbia in 16. Israel and Iran took the two restricted slots in 17.
- Undercurrent was non-AI in 17, so 18 may be AI-adjacent.
- Wildcard 17 was education; not again. Re-run coverage.py (crypto/fintech is now the longest debt).

## Recurring refresh
- Momentum prev from 17: ai_compute 18, geopolitics 2, markets 1 (`python3 momentum.py 2026-10-05 2026-10-11`).
- Baskets from 17 (Friday Oct 2 unless noted): 10y 5.28 (5.29 Sept 30), 2y 4.83, DFII10 2.92, T5YIE 2.37,
  HY OAS 3.10, DXY 101.93, gold Dec 4,162.30, Brent Dec 102.25, WTI Nov 91.11 (Dec 89.43), NG Nov 3.035,
  sugar Mar 19.93, cocoa Dec 5,670, GDPNow Q3 3.7, mortgage 7.28, S&P 7,722.72, BTC 84,497,
  Polymarket Oct Fed rise 17.5c, Iran ceasefire through Oct 71.5c, Flávio Bolsonaro to win 82.8c.
  HF 30-day: GLM-5.3-Flash 5,740,734; Bonsai 2 GGUF 4,120,718; Qwen3.8-27B 6,758,884; MiMo-V2.6-Pro-RL
  86,278; Kolibri-1 2,453; Qwen3.8-Flash-Next GSQ GGUF 2,244,732.
- Curve: the card's curve_bp is ^TNX minus ^IRX (128 on Oct 2); FRED's T10Y3M read 109. Keep the ^TNX-^IRX
  method for continuity.
- WTI November (CLX26) expires around October 20: switch to December and say so.
- Treasury's par-curve table was misread by an agent in 17; take yields from FRED CSVs.
