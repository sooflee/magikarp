#!/usr/bin/env python3
"""Coverage-debt ledger for The Current Regime.

Reads every issue in regime_state.json, tags each issue's reader-facing text by
REGION and by TOPIC with keyword rules, and prints:

  * a per-issue table of what got covered,
  * WARN lines for any region or topic that has not appeared in the last N issues
    (default 3), in the spirit of sources.py's FEED HEALTH block,
  * a recommendation for next issue's wildcard: the most-indebted topic that is
    outside the four core lanes and not the deep-dive domain.

Usage:
    python3 coverage.py                # ledger + warnings for the next issue
    python3 coverage.py --window 4     # widen the debt window
    python3 coverage.py --issue 10     # show what a specific issue covered

The classifier is deliberately crude (keyword hits on titles, headlines,
summaries and comments). It is a forcing function, not a metric: a WARN means
"go look", the same way a feed WARN does. Tune the keyword lists as the
newsletter's beats settle.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict, defaultdict
from pathlib import Path

STATE = Path(__file__).resolve().parent / "regime_state.json"

# ---------------------------------------------------------------------------
# Regions. Each entry: name -> keywords (lowercase substrings). Order matters
# only for display.
REGIONS: "OrderedDict[str, list[str]]" = OrderedDict([
    ("US", ["washington", "white house", "trump", "congress", "senate", "fed ", "federal reserve",
            "supreme court", "ftc", "doe ", "energy department", "pentagon", "hegseth", "u.s.", " us ",
            "american", "california", "texas", "new mexico", "illinois", "florida", "new york"]),
    ("Europe/UK", ["europe", "eu ", "european", "brussels", "germany", "german", "france", "french",
                   "uk ", "britain", "british", "london", "spain", "spanish", "italy", "netherlands",
                   "denmark", "danish", "hungary", "romania", "bulgaria", "poland", "sweden", "clacton"]),
    ("Russia/Ukraine", ["russia", "ukrain", "kyiv", "moscow", "kremlin", "putin", "crimea", "wildberries"]),
    ("Middle East", ["iran", "israel", "gaza", "hamas", "hormuz", "saudi", "gulf", "uae", "qatar", "yemen",
                     "houthi", "lebanon", "iraq", "syria", "turkey", "turkiye", "erdogan", "pkk", "tehran"]),
    ("China", ["china", "chinese", "beijing", "alibaba", "qwen", "deepseek", "zhipu", "glm-", "kimi",
               "moonshot", "huawei", "cxmt", "smic", "renminbi", "yuan", "pboc", "shanghai", "hong kong"]),
    ("India/South Asia", ["india", "indian", "delhi", "pakistan", "kashmir", "bangladesh", "sri lanka",
                          "nepal", "himal", "islamabad", "modi"]),
    ("East/SE Asia", ["japan", "japanese", "tokyo", "korea", "korean", "taiwan", "tsmc", "indonesia",
                      "singapore", "vietnam", "thailand", "thai", "myanmar", "philippines", "malaysia",
                      "asean", "flores"]),
    ("Africa", ["africa", "nigeria", "kenya", "ethiopia", "tigray", "zambia", "malawi", "congo", "drc",
                "sudan", "ghana", "south africa", "egypt", "libya", "tripoli", "tunisia", "morocco",
                "ceuta", "sahel", "niger", "mali", "rwanda", "ebola", "lusaka", "hichilema"]),
    ("Latin America", ["latin america", "brazil", "brasil", "lula", "bolsonaro", "colombia", "cali",
                       "venezuela", "caracas", "maduro", "mexico", "argentina", "milei", "chile", "peru",
                       "ecuador", "guatemala", "honduras", "panama", "cartel", "uruguay", "de la espriella"]),
    ("Central Asia/Caucasus", ["kazakh", "kyrgyz", "uzbek", "tajik", "turkmen", "almaty", "bishkek",
                               "caucasus", "azerbaijan", "armenia", "georgia", "caspian"]),
    ("Oceania", ["australia", "new zealand", "pacific islands"]),
])

# Topics. Kept coarse on purpose. "AI/compute", "markets/macro" and "conflict"
# are the always-covered beats; the debt check cares about the rest.
TOPICS: "OrderedDict[str, list[str]]" = OrderedDict([
    ("AI/compute", ["model", "open weights", "open-weight", "gpu", "datacenter", "data center", "chip",
                    "inference", "agent", "llm", "nvidia", "anthropic", "openai", "claude", "gemini"]),
    ("markets/macro", ["s&p", "fed ", "yield", "inflation", "cpi", "payroll", "jobs report", "gdpnow",
                       "treasury", "bond", "volatility", "kalshi", "polymarket", "rate hike", "recession"]),
    ("energy/commodities", ["oil", "brent", "wti", "crude", "gas", "lng", "uranium", "nuclear", "wind",
                            "solar", "grid", "power plant", "reserve", "copper", "gold", "silver", "wheat",
                            "corn", "cocoa", "coffee", "sugar"]),
    ("conflict/security", ["war", "strike", "drone", "missile", "ceasefire", "blockade", "military",
                           "troops", "navy", "carrier", "sanction", "defence pact", "defense", "armed"]),
    ("trade/industrial policy", ["tariff", "section 301", "export control", "trade", "subsid",
                                 "reciprocity", "supply chain", "manufactur", "reshor"]),
    ("elections/domestic politics", ["election", "vote", "ballot", "parliament", "by-election", "primary",
                                     "sworn in", "inaugurat", "coalition", "opposition", "referendum",
                                     "turnout", "campaign"]),
    ("law/courts/regulators", ["court", "judge", "ruling", "lawsuit", "sued", "indict", "settlement",
                               "ftc", "doj", "attorney general", "constitutional", "antitrust", "cftc",
                               "regulator", "prosecut", "verdict"]),
    ("privacy/digital rights", ["surveillance", "facial recognition", "encryption", "age verification",
                                "attestation", "privacy", "scanning", "spy", "anonymity", "ad block",
                                "ublock", "tracking", "watermark", "censor"]),
    ("fraud/cyber/crime", ["fraud", "scam", "hack", "breach", "ransom", "extortion", "stolen", "leak",
                           "cyber", "phishing", "laundering", "counterfeit"]),
    ("health/bio", ["health", "hospital", "vaccine", "ebola", "disease", "outbreak", "drug", "fda",
                    "clinical", "cancer", "obesity", "semaglutide", "glp-1", "hepatitis", "dementia",
                    "implant", "biolog", "cell", "pandemic", "who "]),
    ("climate/disasters/water", ["climate", "el ni", "drought", "flood", "heat", "wildfire", "earthquake",
                                 "quake", "cyclone", "hurricane", "storm", "danube", "river", "water",
                                 "emissions", "co2", "carbon"]),
    ("labor/jobs/migration", ["union", "strike", "wage", "layoff", "workers", "employment", "unemploy",
                              "job losses", "hiring", "migrant", "migration", "deport", "refugee",
                              "asylum", "visa", "tps", "protected status", "workforce"]),
    ("housing/cities/real economy", ["housing", "rent", "mortgage", "home price", "homes", "zoning",
                                     "transit", "retail sales", "consumer", "cost of living",
                                     "affordab", "construction", "real estate", "reconstruction"]),
    ("science/space", ["scientist", "physics", "mathemat", "riemann", "theorem", "fusion", "quantum",
                       "space", "rocket", "launch", "orbit", "satellite", "nasa", "telescope",
                       "genome", "nature medicine", "eclipse", "research paper"]),
    ("culture/media/sport", ["film", "music", "streaming", "netflix", "hollywood", "festival",
                             "football", "world cup", "fifa", "olympic", "creator", "influencer",
                             "journalis", "newspaper", "podcast", "game studio", "gaming", "book",
                             "art ", "museum", "attention economy", "social media", "tiktok",
                             "instagram", "facebook", "meta ", "youtube"]),
    ("education", ["school", "student", "university", "teacher", "homework", "exam", "curriculum",
                   "tuition", "college"]),
    ("crypto/fintech", ["bitcoin", "crypto", "stablecoin", "ether", "coinbase", "binance", "stripe",
                        "payments", "fintech", "prediction market", "token"]),
    ("companies/deals", ["ipo", "acquisition", "acquire", "buyout", "valuation", "funding round",
                         "raised", "series b", "merger", "revenue", "earnings"]),
])

CORE_LANE_TOPICS = {"AI/compute", "markets/macro", "conflict/security", "energy/commodities"}
# Map deep-dive domains onto topics so the wildcard never doubles the deep-dive.
DOMAIN_TOPIC = {
    "bio_health": "health/bio", "real_economy": "housing/cities/real economy",
    "china_industrial": "trade/industrial policy", "energy_materials": "energy/commodities",
    "global_south": None, "science_frontier": "science/space",
    "labor_demographics": "labor/jobs/migration", "law_courts": "law/courts/regulators",
    "climate_disasters": "climate/disasters/water", "culture_media": "culture/media/sport",
    "cities_housing": "housing/cities/real economy",
}


# ---------------------------------------------------------------------------
def _texts(issue: dict) -> dict[str, str]:
    """Reader-facing text of an issue, grouped by section, lowercased."""
    out: dict[str, list[str]] = defaultdict(list)

    def add(sec: str, s):
        if isinstance(s, str) and s:
            out[sec].append(s.lower())

    for key, r in (issue.get("regimes") or {}).items():
        sec = key
        for f in ("headline", "summary", "implication"):
            add(sec, r.get(f))
        # evidence[] and links[] are provenance, not what the reader sees as the
        # week's story; leave them out so a footnote cannot count as coverage.
        for it in r.get("items", []) or []:
            add(sec, it.get("title")); add(sec, it.get("comment"))
    for sec in ("undercurrent", "wildcard", "commodities"):
        blk = issue.get(sec) or {}
        for f in ("headline", "summary", "topic"):
            add(sec, blk.get(f))
    for b in issue.get("briefs", []) or []:
        add("briefs", b.get("title")); add("briefs", b.get("comment"))
    for s in issue.get("structural_regimes", []) or []:
        add("radar", s.get("name")); add("radar", s.get("read"))
    for w in issue.get("watch_next", []) or []:
        add("watch_next", w.get("event")); add("watch_next", w.get("note"))
    return {k: " \n ".join(v) for k, v in out.items()}


def _hits(text: str, kws: list[str]) -> tuple[int, int]:
    """(total hits, distinct keywords hit)."""
    counts = [text.count(k) for k in kws]
    return sum(counts), sum(1 for c in counts if c)


def classify(issue: dict, min_hits: int = 3, min_distinct: int = 2) -> tuple[dict, dict]:
    """Return (regions, topics): name -> {section: hits} for names above threshold.
    A region/topic counts as covered when the reader-facing body (headlines,
    summaries, geopolitics items, wildcard, undercurrent, briefs) has at least
    min_hits keyword hits from at least min_distinct different keywords. The radar
    and watch_next restate the lanes and are ignored; evidence and link titles are
    provenance and are ignored."""
    texts = _texts(issue)
    body_secs = [s for s in texts if s not in ("radar", "watch_next")]

    def score(table):
        res = {}
        for name, kws in table.items():
            per = {s: _hits(texts[s], kws) for s in body_secs}
            tot = sum(n for n, _ in per.values())
            distinct = _hits(" ".join(texts[s] for s in body_secs), kws)[1]
            if tot >= min_hits and distinct >= min_distinct:
                res[name] = {s: n for s, (n, _) in per.items() if n}
        return res

    return score(REGIONS), score(TOPICS)


def sections_summary(hits: dict) -> str:
    """'geopolitics 4, deep_dive 2' -> compact provenance."""
    return ", ".join(f"{s} {n}" for s, n in sorted(hits.items(), key=lambda x: -x[1])[:3])


def ledger(issues: list[dict], window: int) -> list[str]:
    lines: list[str] = []
    cov_r: dict[str, list[str]] = defaultdict(list)   # region -> issue ids
    cov_t: dict[str, list[str]] = defaultdict(list)
    per_issue = []
    for iss in issues:
        r, t = classify(iss)
        per_issue.append((iss["id"], r, t))
        for name in r:
            cov_r[name].append(iss["id"])
        for name in t:
            cov_t[name].append(iss["id"])

    lines.append("=== COVERAGE LEDGER (per issue: regions | topics) ===")
    for iid, r, t in per_issue:
        lines.append(f"  {iid}: " + ", ".join(sorted(r)) + "  |  " + ", ".join(sorted(t)))

    recent = [i["id"] for i in issues[-window:]]
    lines.append(f"\n=== COVERAGE DEBT (not seen in the last {window} issues: {', '.join(recent)}) ===")
    warns = 0
    for name in REGIONS:
        seen = [i for i in cov_r.get(name, []) if i in recent]
        if not seen:
            last = cov_r[name][-1] if cov_r.get(name) else "never"
            lines.append(f"  WARN region  {name:24s} last seen: {last}")
            warns += 1
    debt_topics = []
    for name in TOPICS:
        seen = [i for i in cov_t.get(name, []) if i in recent]
        if not seen:
            last = cov_t[name][-1] if cov_t.get(name) else "never"
            lines.append(f"  WARN topic   {name:24s} last seen: {last}")
            warns += 1
            debt_topics.append((name, last))
    if not warns:
        lines.append("  none: every region and topic appeared at least once in the window")

    # Streaks: things that appear every single issue (the sameness signal).
    always_r = [n for n in REGIONS if all(n in r for _, r, _ in per_issue[-window:])]
    always_t = [n for n in TOPICS if all(n in t for _, _, t in per_issue[-window:])]
    lines.append(f"\n=== EVERY ISSUE in the window (the sameness signal) ===")
    lines.append("  regions: " + (", ".join(always_r) or "none"))
    lines.append("  topics:  " + (", ".join(always_t) or "none"))
    return lines, debt_topics, cov_t


def recommend_wildcard(next_issue: int, debt_topics: list, cov_t: dict, issues: list[dict]) -> list[str]:
    try:
        import sources
        domain = sources.deep_dive_domain(next_issue)
    except Exception:
        domain = "?"
    dd_topic = DOMAIN_TOPIC.get(domain)
    last_wc = (issues[-1].get("wildcard") or {}).get("topic", "")
    lines = [f"\n=== NEXT ISSUE {next_issue:02d} ===",
             f"  deep-dive domain: {domain}" + (f" (topic {dd_topic})" if dd_topic else "")]
    # rank ALL non-core topics by how long since last covered (oldest first)
    order = {iss["id"]: n for n, iss in enumerate(issues)}
    ranked = []
    for name in TOPICS:
        if name in CORE_LANE_TOPICS or name == dd_topic:
            continue
        hist = cov_t.get(name, [])
        last_idx = order[hist[-1]] if hist else -1
        ranked.append((last_idx, name, hist[-1] if hist else "never"))
    ranked.sort()
    lines.append("  wildcard candidates, most-indebted first (outside core lanes and the deep-dive):")
    for last_idx, name, last in ranked[:5]:
        lines.append(f"    - {name:28s} last seen: {last}")
    lines.append(f"  last wildcard topic: {last_wc!r}; do not repeat it")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=3)
    ap.add_argument("--issue", help="show classification detail for one issue id")
    args = ap.parse_args()
    state = json.load(open(STATE))
    issues = [i for i in state["issues"] if i.get("id") != "00"]

    if args.issue:
        iss = next(i for i in issues if i["id"] == args.issue)
        r, t = classify(iss)
        print(f"Issue {args.issue}")
        print(" regions:")
        for n, h in r.items():
            print(f"   {n:24s} {sections_summary(h)}")
        print(" topics:")
        for n, h in t.items():
            print(f"   {n:28s} {sections_summary(h)}")
        return 0

    lines, debt_topics, cov_t = ledger(issues, args.window)
    print("\n".join(lines))
    print("\n".join(recommend_wildcard(int(issues[-1]["id"]) + 1, debt_topics, cov_t, issues)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
