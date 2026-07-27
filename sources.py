#!/usr/bin/env python3
"""Multi-source signal fetchers for 'The Current Regime'.

Beyond Hacker News: GitHub trending (what developers are building) and arXiv
(what researchers are publishing). Each fetcher is best-effort — a failure in
one source returns [] rather than aborting the run. No third-party deps.

CLI:
    python3 sources.py            # print this week's top items from every source
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
import urllib.parse
from html import unescape

UA = {"User-Agent": "the-current-regime/1.0 (+newsletter)"}


def _get(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def fetch_hn(days: int = 7, limit: int = 30) -> list[dict]:
    """Top HN stories of the last `days`, by points (Algolia)."""
    import time
    since = int(time.time()) - days * 86400
    q = urllib.parse.urlencode({
        "tags": "story",
        "numericFilters": f"created_at_i>{since}",
        "hitsPerPage": limit,
    })
    try:
        data = json.loads(_get(f"https://hn.algolia.com/api/v1/search?{q}"))
    except Exception as e:
        print(f"[hn] failed: {e}", file=sys.stderr)
        return []
    out = []
    for h in data.get("hits", []):
        out.append({
            "source": "hn",
            "title": (h.get("title") or "").strip(),
            "score": h.get("points") or 0,
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
        })
    return [x for x in out if x["title"]]


def fetch_github_trending(since: str = "weekly", limit: int = 20) -> list[dict]:
    """Trending repos (scrape github.com/trending — no official API)."""
    try:
        html = _get(f"https://github.com/trending?since={since}")
    except Exception as e:
        print(f"[github] failed: {e}", file=sys.stderr)
        return []
    # Each repo row: <h2 class="h3 lh-condensed"><a ... href="/owner/repo" ...>
    repos = re.findall(
        r'<h2[^>]*lh-condensed[^>]*>\s*<a[^>]*?href="/([^"/]+/[^"/?#]+)"',
        html, re.S)
    seen, out = set(), []
    for slug in repos:
        if slug in seen:
            continue
        seen.add(slug)
        out.append({
            "source": "github",
            "title": slug,
            "score": None,
            "url": f"https://github.com/{slug}",
        })
        if len(out) >= limit:
            break
    return out


def fetch_arxiv(categories=("cs.AI", "cs.LG", "cs.CL"), limit: int = 15) -> list[dict]:
    """Most recent submissions in the given arXiv categories (Atom API)."""
    cat = "+OR+".join(f"cat:{c}" for c in categories)
    url = (f"http://export.arxiv.org/api/query?search_query={cat}"
           f"&sortBy=submittedDate&sortOrder=descending&max_results={limit}")
    try:
        xml = _get(url)
    except Exception as e:
        print(f"[arxiv] failed: {e}", file=sys.stderr)
        return []
    out = []
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        tm = re.search(r"<title>(.*?)</title>", entry, re.S)
        lm = re.search(r'<link[^>]*rel="alternate"[^>]*href="([^"]+)"', entry)
        if not tm:
            continue
        title = unescape(re.sub(r"\s+", " ", tm.group(1)).strip())
        out.append({
            "source": "arxiv",
            "title": title,
            "score": None,
            "url": lm.group(1) if lm else "",
        })
    return out


def _rss_items(xml: str, source: str, limit: int) -> list[dict]:
    """Parse <item>/<entry> title+link from an RSS or Atom feed."""
    out = []
    blocks = re.findall(r"<item>(.*?)</item>", xml, re.S) or \
        re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    for b in blocks:
        tm = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", b, re.S)
        lm = re.search(r"<link[^>]*href=\"([^\"]+)\"", b) or \
            re.search(r"<link>(.*?)</link>", b, re.S)
        if not tm:
            continue
        title = unescape(re.sub(r"\s+", " ", tm.group(1)).strip())
        url = (lm.group(1).strip() if lm else "")
        if title:
            out.append({"source": source, "title": title, "score": None, "url": url})
        if len(out) >= limit:
            break
    return out


def fetch_gdelt(query: str = "(war OR sanctions OR tariff OR ceasefire OR "
               "summit OR election OR coup) sourcelang:english",
               limit: int = 15) -> list[dict]:
    """Global news on geopolitics themes, ranked by relevance (GDELT DOC 2.0)."""
    q = urllib.parse.urlencode({
        "query": query, "mode": "artlist", "maxrecords": limit,
        "timespan": "1w", "sort": "hybridrel", "format": "json",
    })
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?{q}"
    try:
        data = json.loads(_get(url))
    except Exception as e:
        if "429" in str(e):        # GDELT rate-limits per IP; one retry after a pause
            import time
            time.sleep(6)
            try:
                data = json.loads(_get(url))
            except Exception as e2:
                print(f"[gdelt] failed after retry: {e2}", file=sys.stderr)
                return []
        else:
            print(f"[gdelt] failed: {e}", file=sys.stderr)
            return []
    out = []
    for a in data.get("articles", []):
        title = (a.get("title") or "").strip()
        if title:
            out.append({"source": "gdelt", "title": title, "score": None,
                        "url": a.get("url") or ""})
    return out


def fetch_aljazeera(limit: int = 15) -> list[dict]:
    """World-news reporting (Al Jazeera all-news RSS)."""
    try:
        return _rss_items(_get("https://www.aljazeera.com/xml/rss/all.xml"),
                          "aljazeera", limit)
    except Exception as e:
        print(f"[aljazeera] failed: {e}", file=sys.stderr)
        return []


def fetch_techmeme(limit: int = 15) -> list[dict]:
    """Curated tech-news aggregation (Techmeme RSS)."""
    try:
        return _rss_items(_get("https://www.techmeme.com/feed.xml"),
                          "techmeme", limit)
    except Exception as e:
        print(f"[techmeme] failed: {e}", file=sys.stderr)
        return []


def fetch_lobsters(limit: int = 20) -> list[dict]:
    """Dev-community front page (lobste.rs hottest.json) — an HN cross-check."""
    try:
        data = json.loads(_get("https://lobste.rs/hottest.json"))
    except Exception as e:
        print(f"[lobsters] failed: {e}", file=sys.stderr)
        return []
    out = []
    for s in data[:limit]:
        title = (s.get("title") or "").strip()
        if title:
            out.append({"source": "lobsters", "title": title,
                        "score": s.get("score"),
                        "url": s.get("url") or s.get("comments_url") or ""})
    return out


def fetch_polymarket(limit: int = 15) -> list[dict]:
    """Most-traded open prediction markets (Polymarket gamma API) — forward odds."""
    q = urllib.parse.urlencode({
        "limit": limit, "order": "volume24hr", "ascending": "false",
        "closed": "false",
    })
    try:
        data = json.loads(_get(f"https://gamma-api.polymarket.com/events?{q}"))
    except Exception as e:
        print(f"[polymarket] failed: {e}", file=sys.stderr)
        return []
    out = []
    for e in data:
        title = (e.get("title") or "").strip()
        vol = e.get("volume24hr")
        if title:
            out.append({"source": "polymarket", "title": title,
                        "score": int(vol) if isinstance(vol, (int, float)) else None,
                        "url": f"https://polymarket.com/event/{e.get('slug','')}"})
    return out


# --- Feed groups + health (issue 08+) --------------------------------------
# Every multi-feed pull routes through fetch_feed_group so per-feed counts are
# recorded. A feed that returns nothing, or a group where one feed supplied
# everything, is reported loudly by feed_health_report() — the July 20-26 issue
# shipped with a lane that silently collapsed to a single outlet.

FEED_HEALTH: dict[str, list[tuple[str, int]]] = {}   # group -> [(feed, count)]

# World reporting beyond one outlet. Al Jazeera stays; the rest widen the
# theatres (Africa, Latin America, South Asia, Europe) so the geopolitics
# digest is not named from a single feed. All verified fetchable 2026-07-27.
WORLD_FEEDS = [
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("DW", "https://rss.dw.com/xml/rss-en-world"),
    ("France24", "https://www.france24.com/en/rss"),
    ("AllAfrica", "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf"),
    ("El País English", "https://feeds.elpais.com/mrss-s/pages/ep/site/english.elpais.com/portada"),
    ("MercoPress", "https://en.mercopress.com/rss/"),
    ("The Hindu Intl", "https://www.thehindu.com/news/international/feeder/default.rss"),
    ("Semafor", "https://www.semafor.com/rss.xml"),
]

# Weekly AI analysis that catches what HN's front page missed; Interconnects
# in particular tracks the open-weights race the AI-sovereignty regime reads.
AI_ANALYSIS_FEEDS = [
    ("Interconnects", "https://www.interconnects.ai/feed"),
    ("Import AI", "https://jack-clark.net/feed/"),
    ("Zvi", "https://thezvi.wordpress.com/feed/"),
    ("SemiAnalysis", "https://semianalysis.com/feed/"),
]

# Original cyber/fraud reporting for the wildcard rotation, as configured
# feeds instead of lucky HN appearances.
CYBER_FEEDS = [
    ("404 Media", "https://www.404media.co/rss/"),
    ("Risky Business", "https://news.risky.biz/feed/"),
    ("Krebs", "https://krebsonsecurity.com/feed/"),
]


def fetch_feed_group(group: str, feeds: list[tuple[str, str]],
                     per_feed: int = 8, limit: int = 25) -> list[dict]:
    """Merged best-effort items from several feeds; per-feed counts land in
    FEED_HEALTH so dead feeds and single-source groups get reported. Feeds are
    interleaved round-robin so an early feed cannot crowd the others out of
    the truncated result."""
    from itertools import zip_longest
    per_lists, health = [], []
    for name, url in feeds:
        try:
            items = _rss_items(_get(url), group, per_feed)
        except Exception as e:
            items = []
            print(f"[{group}] {name} failed: {e}", file=sys.stderr)
        health.append((name, len(items)))
        per_lists.append(items)
    FEED_HEALTH[group] = health
    seen, uniq = set(), []
    for row in zip_longest(*per_lists):
        for it in row:
            if it is None or it["title"] in seen:
                continue
            seen.add(it["title"])
            uniq.append(it)
    return uniq[:limit]


def feed_health_report() -> list[str]:
    """Per-group feed counts with warnings. Empty until fetchers have run."""
    lines = []
    for group, health in FEED_HEALTH.items():
        total = sum(n for _, n in health)
        parts = ", ".join(f"{name} {n}" for name, n in health)
        lines.append(f"  {group}: {total} items ({parts})")
        for name, n in health:
            if n == 0:
                lines.append(f"    WARN: {name} returned 0 items (dead feed or bot block)")
        live = [name for name, n in health if n > 0]
        if len(health) > 1 and len(live) == 1:
            lines.append(f"    WARN: single-source group; everything came from {live[0]}")
        if not live:
            lines.append("    WARN: group returned nothing at all")
    return lines


def fetch_world(limit: int = 25) -> list[dict]:
    """World reporting across WORLD_FEEDS (supersedes the Al Jazeera-only pull)."""
    return fetch_feed_group("world", WORLD_FEEDS, per_feed=6, limit=limit)


def fetch_ai_analysis(limit: int = 12) -> list[dict]:
    """Weekly AI analysis feeds — the between-the-issues synthesis layer."""
    return fetch_feed_group("ai_analysis", AI_ANALYSIS_FEEDS, per_feed=4, limit=limit)


def fetch_cyber(limit: int = 12) -> list[dict]:
    """Cyber/fraud original reporting for the wildcard rotation."""
    return fetch_feed_group("cyber", CYBER_FEEDS, per_feed=5, limit=limit)


# --- Attention + primary-document APIs (all keyless) ------------------------

def fetch_wikipedia_top(limit: int = 15) -> list[dict]:
    """Yesterday's most-viewed English Wikipedia articles — a neutral gauge of
    what the world is suddenly curious about, independent of any editor."""
    import datetime as dt
    d = dt.date.today() - dt.timedelta(days=1)
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
           f"en.wikipedia/all-access/{d.year}/{d.month:02d}/{d.day:02d}")
    try:
        data = json.loads(_get(url))
    except Exception as e:
        print(f"[wikipedia] failed: {e}", file=sys.stderr)
        return []
    skip = ("Main_Page", "Special:", "Wikipedia:", "Portal:", "Help:", "File:")
    out = []
    for a in data.get("items", [{}])[0].get("articles", []):
        name = a.get("article", "")
        if name.startswith(skip):
            continue
        out.append({"source": "wikipedia", "title": name.replace("_", " "),
                    "score": a.get("views"),
                    "url": f"https://en.wikipedia.org/wiki/{name}"})
        if len(out) >= limit:
            break
    return out


def fetch_hf_trending(limit: int = 12) -> list[dict]:
    """Trending models on Hugging Face — the open-weights race, measured in
    downloads rather than announcements."""
    try:
        data = json.loads(_get("https://huggingface.co/api/models"
                               f"?sort=trendingScore&direction=-1&limit={limit}"))
    except Exception as e:
        print(f"[hf] failed: {e}", file=sys.stderr)
        return []
    out = []
    for m in data:
        mid = m.get("id", "")
        if mid:
            out.append({"source": "hf", "title": mid,
                        "score": m.get("downloads"),
                        "url": f"https://huggingface.co/{mid}"})
    return out


def fetch_edgar(query: str, forms: str = "8-K", limit: int = 10) -> list[dict]:
    """SEC EDGAR full-text search — primary documents behind a known story.
    Helper for targeted digs (e.g. fetch_edgar('\"special purpose vehicle\" \"data center\"')),
    not part of the default run: unscoped results are noisy."""
    q = urllib.parse.urlencode({"q": query, "forms": forms})
    try:
        data = json.loads(_get(f"https://efts.sec.gov/LATEST/search-index?{q}"))
    except Exception as e:
        print(f"[edgar] failed: {e}", file=sys.stderr)
        return []
    out = []
    for h in data.get("hits", {}).get("hits", [])[:limit]:
        src = h.get("_source", {})
        names = src.get("display_names") or ["?"]
        acc = (src.get("adsh") or "").replace("-", "")
        cik = (h.get("_id") or ":").split(":")[0]
        out.append({"source": "edgar", "title": f"{names[0]} ({src.get('file_type', forms)})",
                    "score": None,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}"})
    return out


# --- Key-gated fetchers (activate by exporting the env var) -----------------

def fetch_eia(series: str = "PET.WCESTUS1.W", limit: int = 8) -> list[dict]:
    """EIA weekly energy data (crude stocks by default). Needs EIA_API_KEY
    (free at eia.gov/opendata); returns [] with a note until it is set."""
    import os
    key = os.environ.get("EIA_API_KEY")
    if not key:
        print("[eia] skipped: set EIA_API_KEY (free key at eia.gov/opendata)",
              file=sys.stderr)
        return []
    q = urllib.parse.urlencode({"api_key": key, "series_id": series, "num": limit})
    try:
        data = json.loads(_get(f"https://api.eia.gov/series/?{q}"))
        pts = data.get("series", [{}])[0].get("data", [])[:limit]
    except Exception as e:
        print(f"[eia] failed: {e}", file=sys.stderr)
        return []
    return [{"source": "eia", "title": f"{series} {d}: {v}", "score": None,
             "url": "https://www.eia.gov/opendata/"} for d, v in pts]


def fetch_acled(limit: int = 15) -> list[dict]:
    """ACLED conflict events, last week. Needs ACLED_KEY + ACLED_EMAIL
    (register at acleddata.com); returns [] with a note until they are set."""
    import os
    key, email = os.environ.get("ACLED_KEY"), os.environ.get("ACLED_EMAIL")
    if not (key and email):
        print("[acled] skipped: set ACLED_KEY and ACLED_EMAIL "
              "(register at acleddata.com)", file=sys.stderr)
        return []
    q = urllib.parse.urlencode({"key": key, "email": email, "limit": limit,
                                "event_date_where": "BETWEEN", "terms": "accept"})
    try:
        data = json.loads(_get(f"https://api.acleddata.com/acled/read?{q}"))
    except Exception as e:
        print(f"[acled] failed: {e}", file=sys.stderr)
        return []
    out = []
    for ev in data.get("data", [])[:limit]:
        out.append({"source": "acled",
                    "title": f"{ev.get('event_date','')} {ev.get('country','')}: "
                             f"{ev.get('event_type','')} ({ev.get('fatalities','0')} deaths)",
                    "score": None, "url": "https://acleddata.com"})
    return out


# --- Rotating deep-dive lane (issue 06+) ----------------------------------
# The second core lane rotates its domain each week so the issue stops being
# all-tech. Domains cycle in this fixed order; pick with deep_dive_domain().
DEEP_DIVE_ROTATION = [
    "bio_health",        # GLP-1 second-order effects, longevity, AI drug discovery, synth-bio
    "real_economy",      # housing, cost-of-living, demographics, the labor market
    "china_industrial",  # EVs/BYD, domestic chips, overcapacity deflation
    "energy_materials",  # solar/battery deflation, SMRs, the grid as its own story
    "global_south",      # India, SE Asia, Africa, Latin America: growth, elections, capital
    "science_frontier",  # fusion, quantum, the space economy beyond the launch business
]

# Each domain is a set of best-effort RSS/Atom feeds. Failures drop to [].
DEEP_DIVE_FEEDS = {
    "bio_health": [
        ("STAT", "https://www.statnews.com/feed/"),
        ("Nature", "https://www.nature.com/nature.rss"),
    ],
    "real_economy": [
        # feedburner URL died silently before issue 07; substack feed verified live.
        ("Calculated Risk", "https://calculatedrisk.substack.com/feed"),
        ("Wolf Street", "https://wolfstreet.com/feed/"),
        ("Liberty Street (NY Fed)", "https://libertystreeteconomics.newyorkfed.org/feed/"),
    ],
    "china_industrial": [
        ("SCMP Business", "https://www.scmp.com/rss/92/feed"),
        ("ChinaTalk", "https://www.chinatalk.media/feed"),
        ("SemiAnalysis", "https://semianalysis.com/feed/"),
    ],
    "energy_materials": [
        ("CleanTechnica", "https://cleantechnica.com/feed/"),
        ("OilPrice", "https://oilprice.com/rss/main"),
    ],
    "global_south": [
        ("Rest of World", "https://restofworld.org/feed/latest/"),
        ("AllAfrica", "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf"),
        ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ],
    "science_frontier": [
        ("Quanta", "https://api.quantamagazine.org/feed/"),
        ("Phys.org", "https://phys.org/rss-feed/"),
    ],
}

# A GDELT query to widen the two domains that are thin on English RSS.
DEEP_DIVE_GDELT = {
    "china_industrial": "(China AND (EV OR chip OR semiconductor OR export OR "
                        "overcapacity OR manufacturing)) sourcelang:english",
    "global_south": "(India OR Indonesia OR Nigeria OR Brazil OR \"South Africa\" "
                    "OR Vietnam) AND (economy OR election OR trade OR investment) "
                    "sourcelang:english",
}


def deep_dive_domain(issue_num: int) -> str:
    """The deep-dive domain for issue N, cycling through DEEP_DIVE_ROTATION.
    Deterministic and auditable: issue 06 -> bio_health, 07 -> real_economy, ..."""
    return DEEP_DIVE_ROTATION[(int(issue_num) - 6) % len(DEEP_DIVE_ROTATION)]


def fetch_deep_dive(domain: str, limit: int = 15) -> list[dict]:
    """Merged best-effort items for one rotating deep-dive domain."""
    group = f"deepdive:{domain}"
    out = fetch_feed_group(group, DEEP_DIVE_FEEDS.get(domain, []),
                           per_feed=limit, limit=limit * 3)
    gq = DEEP_DIVE_GDELT.get(domain)
    if gq:
        gitems = [dict(it, source=group) for it in fetch_gdelt(gq, limit)]
        FEED_HEALTH[group].append(("GDELT", len(gitems)))
        out += gitems
    seen, uniq = set(), []
    for it in out:
        if it["title"] in seen:
            continue
        seen.add(it["title"])
        uniq.append(it)
    return uniq[:limit]


def fetch_all() -> dict[str, list[dict]]:
    return {
        "hn": fetch_hn(),
        "github": fetch_github_trending(),
        "arxiv": fetch_arxiv(),
        "gdelt": fetch_gdelt(),
        "world": fetch_world(),
        "techmeme": fetch_techmeme(),
        "lobsters": fetch_lobsters(),
        "polymarket": fetch_polymarket(),
        "ai_analysis": fetch_ai_analysis(),
        "cyber": fetch_cyber(),
        "wikipedia": fetch_wikipedia_top(),
        "hf": fetch_hf_trending(),
    }


def _print(items: list[dict], n: int):
    for it in items[:n]:
        s = it["score"]
        tag = f"[{s:>4}]" if isinstance(s, int) else "[   -]"
        print(f"  {tag} {it['title'][:78]}")


def main() -> int:
    # `python3 sources.py deepdive 06` previews just the rotating lane for an issue.
    if len(sys.argv) >= 2 and sys.argv[1] == "deepdive":
        n = sys.argv[2] if len(sys.argv) >= 3 else "6"
        dom = deep_dive_domain(n)
        items = fetch_deep_dive(dom)
        print(f"=== Deep-dive for issue {n}: {dom} ({len(items)}) ===")
        _print(items, 15)
        print("\n=== FEED HEALTH ===")
        for line in feed_health_report():
            print(line)
        return 0
    data = fetch_all()
    print(f"=== Hacker News (top {len(data['hn'])}) ===")
    _print(data["hn"], 12)
    print(f"\n=== GitHub trending weekly ({len(data['github'])}) ===")
    _print(data["github"], 12)
    print(f"\n=== arXiv cs.AI/LG/CL recent ({len(data['arxiv'])}) ===")
    _print(data["arxiv"], 10)
    print(f"\n=== GDELT geopolitics ({len(data['gdelt'])}) ===")
    _print(data["gdelt"], 12)
    print(f"\n=== World reporting, {len(WORLD_FEEDS)} feeds ({len(data['world'])}) ===")
    _print(data["world"], 16)
    print(f"\n=== Techmeme ({len(data['techmeme'])}) ===")
    _print(data["techmeme"], 12)
    print(f"\n=== Lobsters ({len(data['lobsters'])}) ===")
    _print(data["lobsters"], 12)
    print(f"\n=== Polymarket forward odds ({len(data['polymarket'])}) ===")
    _print(data["polymarket"], 12)
    print(f"\n=== AI analysis weeklies ({len(data['ai_analysis'])}) ===")
    _print(data["ai_analysis"], 10)
    print(f"\n=== Cyber & fraud reporting ({len(data['cyber'])}) ===")
    _print(data["cyber"], 10)
    print(f"\n=== Wikipedia top pageviews, yesterday ({len(data['wikipedia'])}) ===")
    _print(data["wikipedia"], 10)
    print(f"\n=== Hugging Face trending models ({len(data['hf'])}) ===")
    _print(data["hf"], 10)
    print("\n=== FEED HEALTH ===")
    for line in feed_health_report():
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
