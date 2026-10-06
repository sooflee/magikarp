#!/usr/bin/env python3
"""Editorial lint for one issue of The Current Regime.

build_site.py already fails on bad links, media and hover notes. This checks the
house rules a model is most likely to break while writing: the schema, the length
budget, em-dashes and machine-writing tells, the theatre rule, implications that
repeat their summary's numbers, out-of-window dates and recycled links.

Usage:
    python3 validate_issue.py            # the latest issue
    python3 validate_issue.py 16         # a given issue id
    python3 validate_issue.py --quotes   # also list every quoted phrase for the audit

ERROR lines exit 1 and must be fixed. WARN lines need a look and a reason; a
known-good issue (16) passes with a few WARNs. Run it after every edit to the
issue object, and before build_site.py.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

import sources

STATE = Path(__file__).resolve().parent / "regime_state.json"

LANES = ("ai_compute", "deep_dive", "geopolitics", "markets")
BRIEF_ANCHORS = ("ai", "deep-dive", "geopolitics", "markets", "wildcard")
SIGNAL_KEYS = ("trend", "vol", "curve_bp", "gdpnow", "dollar", "credit", "liquidity", "crypto")

# Machine-writing tells (the human-voice skill's sweep, as code).
BANNED_WORDS = re.compile(
    r"\b(delve|tapestry|pivotal|crucial|testament|underscor\w*|showcas\w*|foster\w*|vibrant|"
    r"nestled|boasts|robust|seamless\w*|leverag\w*|enhanc\w*|align(s|ed)? with|empower\w*|"
    r"game-chang\w*|cutting-edge|landscape|ecosystem|navigat\w*|additionally|moreover|"
    r"furthermore|notabl\w*|remarkabl\w*|conspicuous\w*|significantly|importantly)\b", re.I)
BANNED_CONSTRUCTIONS = re.compile(
    r"(not (just|only|merely) [^.]{3,60}, but|serves as|stands as|functions as|"
    r"represents a |marks a |, (highlighting|underscoring|emphasizing|reflecting|cementing|"
    r"fostering|signaling|signalling)\b|observers|experts (say|note)|industry reports|"
    r"despite (these|its) challenges|looking ahead|The (result|catch|upshot|takeaway):|"
    r"a (significant|major) shift|broader trend|in today's)", re.I)
THEME_OPENER = re.compile(r"^(this week|the week|it was a week|a week (of|in which))", re.I)
RESTRICTED_THEATRE = re.compile(
    r"\b(ukrain\w*|russia\w*|kremlin|putin|zelensky\w*|moscow|kyiv|crimea|donbas|"
    r"iran\w*|tehran|hormuz|israel\w*|gaza|rafah|west bank|hamas|hezbollah|lebanon|"
    r"houthi\w*|yemen\w*|netanyahu)\b", re.I)
MONTHS = ("January February March April May June July August September October "
          "November December").split()
DATE_RE = re.compile(r"\b(" + "|".join(MONTHS) + r") (\d{1,2})\b")
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")

errors: list[str] = []
warns: list[str] = []


def err(msg): errors.append(msg)
def warn(msg): warns.append(msg)


def words(s: str) -> int:
    return len(re.findall(r"[A-Za-z0-9$€£%][\w$€£%.,'’-]*", s or ""))


def sentences(s: str) -> list[str]:
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z'\"‘“])", (s or "").strip()) if x]


def reader_text(iss: dict):
    """Yield (where, text) for every string a reader sees."""
    yield "index_title", iss.get("index_title", "")
    yield "lede", iss.get("lede", "")
    for b in iss.get("brief", []):
        yield f"brief[{b.get('anchor')}]", b.get("line", "")
    for k, r in iss.get("regimes", {}).items():
        for f in ("headline", "summary", "implication"):
            yield f"{k}.{f}", r.get(f, "")
        for i, it in enumerate(r.get("items", [])):
            yield f"{k}.items[{i}]", it.get("title", "") + " " + it.get("comment", "")
        for ln in r.get("links", []):
            yield f"{k}.links", ln.get("title", "")
    for sec in ("undercurrent", "wildcard"):
        s = iss.get(sec) or {}
        for f in ("headline", "summary"):
            yield f"{sec}.{f}", s.get(f, "")
        for i, it in enumerate(s.get("items", [])):
            yield f"{sec}.items[{i}]", it.get("title", "") + " " + it.get("comment", "")
    c = iss.get("commodities") or {}
    yield "commodities.headline", c.get("headline", "")
    yield "commodities.summary", c.get("summary", "")
    for i, b in enumerate(iss.get("briefs", [])):
        yield f"briefs[{i}]", b.get("title", "") + " " + b.get("comment", "")
    for i, m in enumerate(iss.get("market_moves", [])):
        yield f"market_moves[{i}]", m.get("market", "") + " " + m.get("detail", "")
    for i, s in enumerate(iss.get("structural_regimes", [])):
        yield f"radar[{s.get('name')}]", " ".join(
            [s.get("read", ""), s.get("line", "")] + [f"{b.get('metric','')} {b.get('value','')}"
                                                       for b in s.get("basket", [])])
    for i, w in enumerate(iss.get("watch_next", [])):
        yield f"watch_next[{i}]", f"{w.get('event','')} {w.get('note','')}"
    a = iss.get("across_sources") or {}
    yield "across_sources", a.get("github_theme", "")
    for i, n in enumerate(iss.get("annotations", [])):
        yield f"annotations[{i}]", n.get("note", "")


def check_schema(doc: dict, iss: dict, prev: dict | None):
    for f in ("id", "week", "date", "date_label", "index_title", "brief", "regimes"):
        if not iss.get(f):
            err(f"missing required field `{f}`")
    defs = doc.get("regime_defs", {})
    for k in LANES:
        r = iss.get("regimes", {}).get(k)
        if not r:
            err(f"missing core lane regimes.{k}")
            continue
        states = defs.get(k, {}).get("states", [])
        if r.get("state") not in states:
            err(f"regimes.{k}.state {r.get('state')!r} not in {states}")
        for f in ("headline", "summary", "implication", "links"):
            if f == "links" and r.get("items"):
                continue
            if not r.get(f):
                err(f"regimes.{k}.{f} is empty")
    try:
        n = int(iss["id"])
        want = sources.deep_dive_domain(n).replace("_", " ")
        got = (iss.get("regimes", {}).get("deep_dive", {}).get("domain") or "").lower()
        key = {"bio health": "bio", "real economy": "economy", "china industrial": "china",
               "energy materials": "energy", "global south": "global south",
               "science frontier": "science", "labor demographics": "labor",
               "law courts": "law", "climate disasters": "climate", "culture media": "culture",
               "cities housing": "cities"}.get(want, want.split()[0])
        if key not in got:
            err(f"deep_dive.domain {got!r} does not match the rotation for issue {n}: {want}")
    except (KeyError, ValueError):
        pass
    anchors = [b.get("anchor") for b in iss.get("brief", [])]
    if sorted(anchors) != sorted(BRIEF_ANCHORS):
        err(f"brief anchors {anchors} must be exactly {list(BRIEF_ANCHORS)}")
    sig = iss.get("regimes", {}).get("markets", {}).get("signals", {})
    missing = [k for k in SIGNAL_KEYS if k not in sig]
    if missing:
        warn(f"markets.signals missing {missing}")
    if not iss.get("wildcard"):
        warn("no wildcard (mandatory unless genuinely impossible; say why in the ledger)")
    elif prev and (prev.get("wildcard") or {}).get("topic") == iss["wildcard"].get("topic"):
        err(f"wildcard topic repeats last issue's: {iss['wildcard'].get('topic')!r}")
    if len((iss.get("wildcard") or {}).get("items", [])) > 4:
        err("wildcard carries more than four items")
    # momentum
    m = iss.get("momentum") or {}
    ser = m.get("series", {})
    if set(ser) != {"ai_compute", "geopolitics", "markets"}:
        err(f"momentum.series keys must be ai_compute, geopolitics, markets (got {sorted(ser)})")
    if prev and prev.get("momentum"):
        for k, v in ser.items():
            pv = prev["momentum"]["series"].get(k, [None, None])[1]
            if v and v[0] != pv:
                err(f"momentum.{k} prev={v[0]} but last issue stored cur={pv}")
    # radar
    for s in iss.get("structural_regimes", []):
        if not s.get("spotlight") and not s.get("line"):
            err(f"radar {s.get('name')!r} is not spotlit and has no one-sentence `line`")
        if not s.get("basket"):
            err(f"radar {s.get('name')!r} has an empty basket")
    c = iss.get("commodities") or {}
    if c and not c.get("headline"):
        err("commodities.headline missing (the renderer falls back to a stale headline)")


def check_style(iss: dict):
    total = 0
    for where, text in reader_text(iss):
        if not text:
            continue
        total += words(text)
        if "—" in text or " -- " in text:
            err(f"em-dash in {where}")
        for m in BANNED_WORDS.finditer(text):
            warn(f"tell word {m.group(0)!r} in {where}")
        for m in BANNED_CONSTRUCTIONS.finditer(text):
            warn(f"tell construction {m.group(0)!r} in {where}")
    if total > 3800:
        warn(f"about {total} reader words; the budget is about 3,000")
    print(f"reader words (approx): {total}")

    t = iss.get("index_title", "")
    if ";" in t or len(sentences(t)) > 1:
        err("index_title must be ONE declarative sentence (event as a move in its trend), not a list")
    if words(t) > 40:
        warn(f"index_title is {words(t)} words")
    for b in iss.get("brief", []):
        if words(b.get("line", "")) > 30:
            warn(f"brief[{b.get('anchor')}] is {words(b['line'])} words (limit 30)")

    secs = [(k, r) for k, r in iss.get("regimes", {}).items()]
    secs += [(s, iss[s]) for s in ("wildcard", "undercurrent", "commodities") if iss.get(s)]
    for k, r in secs:
        h, s, imp = r.get("headline", ""), r.get("summary", ""), r.get("implication", "")
        if words(h) > 24:
            warn(f"{k}.headline is {words(h)} words (aim for 20 or fewer)")
        n = words(s)
        if n > 160:
            err(f"{k}.summary is {n} words (limit 130)")
        elif n > 135:
            warn(f"{k}.summary is {n} words (limit 130)")
        first = sentences(s)[0] if s else ""
        if first and not re.search(r"\d", first) and (
                THEME_OPENER.match(first) or "this week" in first.lower()):
            err(f"{k}.summary opens with a theme, not a fact: {first[:80]!r}")
        if imp:
            snums = {x.replace(",", "") for x in NUM_RE.findall(s) if len(x.replace(",", "")) > 1}
            inums = {x.replace(",", "") for x in NUM_RE.findall(imp) if len(x.replace(",", "")) > 1}
            years = {x for x in inums if re.fullmatch(r"(19|20)\d\d", x)}
            dates = {d for _, d in DATE_RE.findall(imp)}
            rep = sorted(inums & snums - years - dates)
            if rep:
                warn(f"{k}.implication repeats number(s) from its summary: {rep}")
            if len(sentences(imp)) > 2:
                warn(f"{k}.implication should be one bounded statement")
        for i, it in enumerate(r.get("items", [])):
            c = it.get("comment", "")
            if words(c) > 75 or len(sentences(c)) > 3:
                warn(f"{k}.items[{i}] comment is {words(c)} words / {len(sentences(c))} sentences "
                     "(two sentences, about 60 words)")
    for i, b in enumerate(iss.get("briefs", [])):
        if len(sentences(b.get("comment", ""))) > 1:
            warn(f"briefs[{i}] comment should be one sentence")
    for i, n in enumerate(iss.get("annotations", [])):
        if words(n.get("note", "")) > 45:
            warn(f"annotations[{i}] ({n.get('terms')}) is {words(n['note'])} words (limit 45)")


def check_geopolitics(iss: dict):
    g = iss.get("regimes", {}).get("geopolitics", {})
    items = g.get("items", [])
    if not 4 <= len(items) <= 6:
        warn(f"geopolitics has {len(items)} items (4-6 unless a genuinely thin week)")
    restricted = [it["title"] for it in items
                  if RESTRICTED_THEATRE.search(it.get("title", "") + " " + it.get("comment", "")[:120])]
    if len(restricted) > 2:
        err("theatre rule: more than two items from Ukraine/Russia + Iran/Middle East combined: "
            + " | ".join(t[:60] for t in restricted))
    if len(items) - len(restricted) < 2:
        err("theatre rule: fewer than two items from other theatres")


def check_dates(iss: dict, prev: dict | None):
    start, end = [dt.date.fromisoformat(x) for x in iss["week"].split("/")]
    year = end.year
    for where, text in reader_text(iss):
        if where.startswith(("watch_next", "annotations", "radar")):
            continue
        for mon, day in DATE_RE.findall(text or ""):
            try:
                d = dt.date(year, MONTHS.index(mon) + 1, int(day))
            except ValueError:
                continue
            if d < start - dt.timedelta(days=3):
                warn(f"{where} mentions {mon} {day}, before the week: context only, never "
                     "this week's news; check it was not covered last issue")
    for w in iss.get("watch_next", []):
        m = DATE_RE.search(w.get("when", ""))
        if m:
            d = dt.date(year, MONTHS.index(m.group(1)) + 1, int(m.group(2)))
            if d <= end:
                err(f"watch_next {w.get('when')!r} is not after the week")
    if prev:
        old = set(re.findall(r"https?://[^\s\"']+", json.dumps(prev)))
        for url in sorted(set(re.findall(r"https?://[^\s\"']+", json.dumps(iss))) & old):
            if any(h in url for h in ("fred.stlouisfed.org", "polymarket.com", "atlantafed",
                                      "huggingface.co", "tradingeconomics.com", "github.com",
                                      "cmegroup.com", "treasury.gov", "freddiemac.com")):
                continue
            warn(f"link also used last issue (recycled story?): {url}")


def list_quotes(iss: dict):
    print("\n=== QUOTES (each must appear verbatim at a cited URL) ===")
    for where, text in reader_text(iss):
        for q in re.findall(r"(?:^|[\s(])['‘\"“]([^'’\"”]{12,}?)['’\"”](?=[\s.,;:)]|$)", text or ""):
            print(f"  {where}: '{q}'")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    doc = json.loads(STATE.read_text())
    issues = doc["issues"]
    idx = next((i for i, x in enumerate(issues) if x["id"] == args[0]), None) if args else len(issues) - 1
    if idx is None:
        print(f"no issue {args[0]}")
        return 2
    iss, prev = issues[idx], (issues[idx - 1] if idx > 0 else None)
    print(f"validating issue {iss['id']} ({iss.get('week')})")
    check_schema(doc, iss, prev)
    check_style(iss)
    check_geopolitics(iss)
    check_dates(iss, prev)
    if "--quotes" in sys.argv:
        list_quotes(iss)
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
