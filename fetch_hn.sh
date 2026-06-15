#!/usr/bin/env bash
# Fetch the top Hacker News stories from the past 7 days (>150 points),
# sorted by points. Same query the weekly cloud routine uses.
# Usage: ./fetch_hn.sh [days] [min_points]
set -euo pipefail

days="${1:-7}"
min_points="${2:-150}"

since=$(date -v-"${days}"d +%s 2>/dev/null || date -d "${days} days ago" +%s)

curl -sS "https://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i>${since},points>${min_points}&hitsPerPage=100" \
| python3 -c "
import json,sys
d=json.load(sys.stdin)
hits=sorted(d['hits'], key=lambda h:-(h.get('points') or 0))
print(f'{len(hits)} stories (last ${days}d, >${min_points} pts)\n')
for h in hits:
    pts=h.get('points'); nc=h.get('num_comments'); t=h.get('title')
    oid=h.get('objectID')
    print(f'{pts:>5} | {nc:>5}c | {t}')
    print(f'        https://news.ycombinator.com/item?id={oid}')
"
