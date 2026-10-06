#!/usr/bin/env python3
"""Regime momentum for an issue week: classify the week's top-100 HN stories.

Usage:
    python3 momentum.py 2026-09-28 2026-10-04     # start and end dates (inclusive, UTC)

Prints the per-regime counts and the JSON fragment for the issue's `momentum`
block. ai_compute = tech_policy + ai_agents + compute_energy (the merged lane);
geopolitics and markets map one-to-one. The previous week's count is the
previous issue's stored current value, not a recompute (Algolia points drift).
"""
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request

import classify

LANES = {"ai_compute": ("tech_policy", "ai_agents", "compute_energy"),
         "geopolitics": ("geopolitics",), "markets": ("markets",)}


def top_stories(start: str, end: str, n: int = 100) -> list[dict]:
    a = int(dt.datetime.fromisoformat(start).replace(tzinfo=dt.timezone.utc).timestamp())
    b = int((dt.datetime.fromisoformat(end) + dt.timedelta(days=1)).replace(tzinfo=dt.timezone.utc).timestamp())
    q = urllib.parse.urlencode({"tags": "story", "hitsPerPage": n,
                                "numericFilters": f"created_at_i>={a},created_at_i<{b}"})
    req = urllib.request.Request(f"https://hn.algolia.com/api/v1/search?{q}",
                                 headers={"User-Agent": "Mozilla/5.0"})
    hits = json.load(urllib.request.urlopen(req, timeout=30))["hits"]
    return sorted(hits, key=lambda h: -(h.get("points") or 0))


def main() -> int:
    start, end = sys.argv[1], sys.argv[2]
    stories = top_stories(start, end)
    raw = {}
    for h in stories:
        r = classify.classify_story(h.get("title") or "")
        raw.setdefault(r, []).append(h)
    for r, hs in sorted(raw.items()):
        print(f"{r:15} {len(hs):3}  e.g. " + " | ".join(h['title'][:50] for h in hs[:3]))
    cur = {lane: sum(len(raw.get(k, [])) for k in ks) for lane, ks in LANES.items()}
    prev = {}
    doc = json.load(open(classify.STATE))
    last = doc["issues"][-1].get("momentum", {}).get("series", {})
    prev = {lane: last.get(lane, [0, 0])[1] for lane in LANES}
    label = lambda d: dt.date.fromisoformat(d).strftime("%b %-d")
    prev_label = doc["issues"][-1].get("momentum", {}).get("weeks", ["", ""])[1]
    print(json.dumps({"weeks": [prev_label, label(end)],
                      "series": {lane: [prev[lane], cur[lane]] for lane in LANES}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
