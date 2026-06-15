#!/usr/bin/env python3
"""Build 1 — daily news -> regime classifier.

Pulls the day's stories (via sources.py), assigns each to one of the regimes
defined in regime_state.json (or 'unaligned'), and scores whether it *confirms*
or *contradicts* the current state of that regime. Appends an idempotent daily
record to regime_state.json -> "daily_counts", so the weekly issue can show
regime momentum and early warnings of a flip.

Usage:
    python3 classify.py                 # classify today's stories, write counts
    python3 classify.py --date 2026-06-14
    python3 classify.py --days 1 --dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

import sources

STATE = Path(__file__).resolve().parent / "regime_state.json"

# Keyword rules: story -> regime. A story is assigned to the regime with the
# most keyword hits; ties break by this dict's order. No hits -> 'unaligned'.
REGIME_KEYWORDS = {
    "tech_policy": ["export control", "regulat", "ban ", "banned", "lawsuit", "court",
                    "ruling", "antitrust", "ftc", "doj", "gdpr", "privacy", "surveillance",
                    "censor", "copyright", "license", "open source", "open-weights",
                    "open weights", "sovereign", "national security", "directive", "liable"],
    "ai_agents": ["agent", "agentic", "autonomous", "copilot", "assistant", "llm",
                  "gpt", "claude", "fable", "mythos", "prompt", "hallucinat", "benchmark",
                  "fine-tune", "rag ", "chatbot", "model "],
    "compute_energy": ["gpu", "datacenter", "data center", "nuclear", "power grid",
                       " grid", "electric", "energy", "chip", "semiconductor", "tsmc",
                       "nvidia", "h100", "capex", "cooling", "watt", "asic", "foundry"],
    "markets": ["stock", "market", "ipo", "earnings", "valuation", "venture",
                " vc ", "funding round", "raise", "acquisition", "merger", "revenue",
                "bond", "yield", " fed ", "interest rate", "inflation", "recession",
                "crypto", "bitcoin", "ethereum", " token", "etf"],
    "labor_ai": ["layoff", "hiring", "job ", "jobs", "employee", "worker", "union",
                 "wage", "return to office", "headcount", "replace work", "white-collar"],
    "geopolitics": ["china", "russia", "ukraine", "israel", "iran", " war", "sanction",
                    "tariff", "military", "drone", "election", "vote", "espionage",
                    "spy", "nato", "taiwan", "meddl"],
}

# Per current-state confirm/contradict cues (light heuristic).
CONFIRM_CONTRADICT = {
    "tech_policy": {  # current state: state-capture
        "confirm": ["export control", "ban", "directive", "national security",
                    "takedown", "regulat", "liable", "antitrust", "sanction"],
        "contradict": ["open source", "open-weights", "open weights", "self-host",
                       "local model", "decentrali", "jailbreak"],
    },
    "ai_agents": {  # current state: liability-reckoning
        "confirm": ["bankrupt", "sabotage", "fail", "risk", "cost", "vulnerab",
                    "hallucinat", "lawsuit", "proactive", "runaway"],
        "contradict": ["benchmark", "state-of-the-art", "outperform", "breakthrough",
                       "fastest", "best model"],
    },
    "markets": {  # current state: mixed
        "confirm": ["volatil", "selloff", "decoupl", "liquidity", "risk-off"],
        "contradict": ["all-time high", "rally", "surge", "record high"],
    },
}


def classify_story(title: str) -> str:
    t = title.lower()
    best, best_n = "unaligned", 0
    for regime, kws in REGIME_KEYWORDS.items():
        n = sum(1 for kw in kws if kw in t)
        if n > best_n:
            best, best_n = regime, n
    return best


def confirm_contradict(regime: str, title: str, state: str | None) -> str | None:
    rules = CONFIRM_CONTRADICT.get(regime)
    if not rules:
        return None
    t = title.lower()
    if any(kw in t for kw in rules["contradict"]):
        return "contradict"
    if any(kw in t for kw in rules["confirm"]):
        return "confirm"
    return None


def current_state(state_doc: dict, regime: str) -> str | None:
    issues = state_doc.get("issues", [])
    for iss in reversed(issues):
        r = iss.get("regimes", {}).get(regime)
        if r and r.get("state"):
            return r["state"]
    return None


def run(date: str, days: int) -> dict:
    doc = json.loads(STATE.read_text())
    stories = sources.fetch_hn(days=days, limit=50)
    counts = {r: 0 for r in REGIME_KEYWORDS}
    counts["unaligned"] = 0
    examples = {r: [] for r in REGIME_KEYWORDS}
    cc = {r: {"confirm": 0, "contradict": 0} for r in CONFIRM_CONTRADICT}
    for s in stories:
        regime = classify_story(s["title"])
        counts[regime] += 1
        if regime != "unaligned" and len(examples[regime]) < 3:
            examples[regime].append(s["title"])
        verdict = confirm_contradict(regime, s["title"], current_state(doc, regime))
        if verdict and regime in cc:
            cc[regime][verdict] += 1
    aligned = {r: c for r, c in counts.items() if r != "unaligned"}
    top = max(aligned, key=aligned.get) if any(aligned.values()) else None
    record = {
        "date": date,
        "window_days": days,
        "total": len(stories),
        "counts": counts,
        "top_regime": top,
        "confirm_contradict": cc,
        "examples": {r: ex for r, ex in examples.items() if ex},
    }
    return record, doc


def write(record: dict, doc: dict):
    dc = doc.setdefault("daily_counts", [])
    dc[:] = [r for r in dc if r.get("date") != record["date"]]
    dc.append(record)
    dc.sort(key=lambda r: r["date"])
    STATE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    record, doc = run(args.date, args.days)
    print(f"=== regime classification · {record['date']} · {record['total']} stories ===")
    for r, c in sorted(record["counts"].items(), key=lambda x: -x[1]):
        bar = "#" * c
        print(f"  {r:14} {c:3}  {bar}")
    print(f"  top regime: {record['top_regime']}")
    for r, v in record["confirm_contradict"].items():
        if v["confirm"] or v["contradict"]:
            print(f"  {r}: confirm {v['confirm']} / contradict {v['contradict']}")
    if not args.dry_run:
        write(record, doc)
        print("  (written to regime_state.json -> daily_counts)")
    else:
        print("  (dry-run, nothing written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
