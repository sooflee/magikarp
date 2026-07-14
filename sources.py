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
    try:
        data = json.loads(_get(f"https://api.gdeltproject.org/api/v2/doc/doc?{q}"))
    except Exception as e:
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


def fetch_all() -> dict[str, list[dict]]:
    return {
        "hn": fetch_hn(),
        "github": fetch_github_trending(),
        "arxiv": fetch_arxiv(),
        "gdelt": fetch_gdelt(),
        "aljazeera": fetch_aljazeera(),
        "techmeme": fetch_techmeme(),
        "lobsters": fetch_lobsters(),
        "polymarket": fetch_polymarket(),
    }


def _print(items: list[dict], n: int):
    for it in items[:n]:
        s = it["score"]
        tag = f"[{s:>4}]" if isinstance(s, int) else "[   -]"
        print(f"  {tag} {it['title'][:78]}")


def main() -> int:
    data = fetch_all()
    print(f"=== Hacker News (top {len(data['hn'])}) ===")
    _print(data["hn"], 12)
    print(f"\n=== GitHub trending weekly ({len(data['github'])}) ===")
    _print(data["github"], 12)
    print(f"\n=== arXiv cs.AI/LG/CL recent ({len(data['arxiv'])}) ===")
    _print(data["arxiv"], 10)
    print(f"\n=== GDELT geopolitics ({len(data['gdelt'])}) ===")
    _print(data["gdelt"], 12)
    print(f"\n=== Al Jazeera world ({len(data['aljazeera'])}) ===")
    _print(data["aljazeera"], 12)
    print(f"\n=== Techmeme ({len(data['techmeme'])}) ===")
    _print(data["techmeme"], 12)
    print(f"\n=== Lobsters ({len(data['lobsters'])}) ===")
    _print(data["lobsters"], 12)
    print(f"\n=== Polymarket forward odds ({len(data['polymarket'])}) ===")
    _print(data["polymarket"], 12)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
