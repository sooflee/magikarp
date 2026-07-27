#!/usr/bin/env python3
"""Build the public archive (GitHub Pages) for 'The Current Regime'.

Blog-style: docs/index.html lists every issue as a linked post, and each issue
gets its own page at docs/issues/<id>.html. Styled after bwang.io/elekid, with a
small serif type scale and a forest-green accent.

Usage:
    python3 build_site.py        # writes docs/index.html + docs/issues/*.html
"""

from __future__ import annotations

import html
import json
from pathlib import Path

import regime_engine

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "regime_state.json"
DOCS = ROOT / "docs"

ACCENT = "#1a7f4b"
SUBSCRIBE_HREF = ("mailto:bensonw.dev@gmail.com?subject=subscribe&body="
                  "Just%20send%20this%20email%20to%20subscribe%20to%20The%20Current%20Regime.")


def _apps_script_url():
    p = Path(__file__).resolve().parent / "apps_script_url.txt"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line.startswith("https://"):
                return line
    return ""


APPS_URL = _apps_script_url()

if APPS_URL:
    # Box POSTs directly to the Apps Script (Google Sheet); no mail client.
    SUBSCRIBE_FORM = (
        '<form class="joinform" id="joinform">'
        '<input class="joininput" type="email" name="email" required placeholder="you@example.com">'
        '<button type="submit" class="subscribe">Join email list</button></form>'
        '<p class="subnote" id="joinmsg" style="display:none">Thanks, you&rsquo;re on the list.</p>'
        "<script>(function(){var f=document.getElementById('joinform');"
        "f.addEventListener('submit',function(ev){ev.preventDefault();"
        "var em=f.email.value.trim();if(!em)return;"
        "fetch('" + APPS_URL + "',{method:'POST',mode:'no-cors',"
        "body:new URLSearchParams({email:em})});"
        "f.style.display='none';document.getElementById('joinmsg').style.display='block';"
        "});})();</script>")
else:
    # Fallback until the Apps Script URL is set: box drops the typed address into a
    # "subscribe" email that signups.py reads over IMAP.
    SUBSCRIBE_FORM = (
        '<form class="joinform" onsubmit="var e=this.em.value.trim();'
        "if(e){location.href=&#39;mailto:bensonw.dev@gmail.com?subject=subscribe&amp;body=&#39;"
        "+encodeURIComponent(&#39;subscribe: &#39;+e);}return false;\">"
        '<input class="joininput" type="email" name="em" required placeholder="you@example.com">'
        '<button type="submit" class="subscribe">Join email list</button>'
        '</form>')
WARN_STATES = {"state-capture", "risk-off", "contracting", "liability-reckoning",
               "stressed", "constrained"}

CSS = f"""
:root{{
  --serif:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif;
  --fg:#1a1a1a; --muted:#6b7280; --faint:#9aa0aa; --line:#e8e8e8;
  --accent:{ACCENT}; --accent-bg:#e7f3ec; --bg:#fff; --warn:#b1300f;
  --fs-display:30px; --fs-head:22px; --fs-body:17px; --fs-detail:15px; --fs-meta:13px;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--fg);font:var(--fs-body)/1.7 var(--serif);
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:640px;margin:0 auto;padding:52px 22px 72px}}
a{{color:var(--accent)}}
header.mast{{border-bottom:1px solid var(--accent);padding-bottom:16px;margin-bottom:8px}}
header.mast.home{{text-align:center;padding-bottom:20px}}
header.mast h1{{font-size:var(--fs-display);line-height:1.1;letter-spacing:-0.02em;margin:0;font-weight:700}}
header.mast h1 a{{color:var(--fg);text-decoration:none}}
header.mast .kicker{{font-size:var(--fs-meta);color:var(--accent);font-style:italic;margin-top:8px}}
.back{{font-size:var(--fs-meta);font-style:italic}}
/* index: issues as posts */
.post{{padding:22px 0;border-bottom:1px solid var(--line)}}
.post .date{{font-size:var(--fs-meta);color:var(--faint);margin:0 0 3px}}
.post h2{{font-size:var(--fs-head);line-height:1.25;letter-spacing:-0.01em;margin:0 0 4px;font-weight:700}}
.post h2 a{{color:var(--fg);text-decoration:none}}
.post h2 a:hover{{color:var(--accent)}}
.post .dek{{font-size:var(--fs-detail);color:var(--muted);margin:0}}
.sec.wildcard{{border-left:2px solid var(--accent);padding-left:16px}}
.sec.wildcard .sub{{letter-spacing:1px;text-transform:uppercase;font-size:var(--fs-meta)}}
/* issue page sections */
.lede{{font-size:var(--fs-body);line-height:1.6;margin:24px 0 0;color:var(--fg)}}
.act{{text-align:center;margin:42px 0 0}}
.act .actlabel{{font-size:var(--fs-meta);letter-spacing:3px;text-transform:uppercase;font-weight:700;color:var(--fg)}}
.act hr{{border:0;border-top:2px solid var(--fg);margin:8px 0 0}}
.sec{{padding-top:30px}}
.sec h2{{font-size:var(--fs-head);line-height:1.3;letter-spacing:-0.01em;margin:0 0 2px;font-weight:700}}
.sec .sub{{font-size:var(--fs-meta);font-weight:600;color:var(--accent);margin:0 0 9px}}
.sec p{{font-size:var(--fs-body);line-height:1.65;margin:0 0 9px}}
.badge{{display:inline-block;font-size:var(--fs-meta);font-weight:600;padding:1px 7px;
  border-radius:3px;background:var(--accent-bg);color:var(--accent);
  margin-left:7px;vertical-align:middle}}
.badge.warn{{background:#fbeae6;color:var(--warn)}}
.impl{{color:var(--muted);font-size:var(--fs-detail)}}
ul.links{{margin:8px 0 0;padding-left:18px}}
ul.links li{{margin:0 0 4px;font-size:var(--fs-detail);line-height:1.45}}
ul.links .pts{{color:var(--faint);font-size:var(--fs-meta)}}
ul.chg{{margin:6px 0 0;padding-left:18px}}
ul.chg li{{margin:0 0 8px;font-size:var(--fs-detail);line-height:1.5}}
.across p{{font-size:var(--fs-detail);line-height:1.6;margin:0 0 8px}}
.story{{font-size:var(--fs-detail);line-height:1.5;margin:12px 0 0}}
.story .cmt{{color:var(--muted);font-size:var(--fs-detail)}}
.traj{{color:var(--faint);font-size:var(--fs-meta);font-style:italic;margin:0 0 10px}}
.wn{{font-size:var(--fs-detail);line-height:1.5;margin:10px 0 0;padding-bottom:8px;border-bottom:1px solid var(--line)}}
.wn .when{{color:var(--accent);font-weight:700}}
.wn .cmt{{color:var(--muted);font-size:var(--fs-detail)}}
.radar{{padding:14px 0;border-bottom:1px solid var(--line)}}
.radar .rname{{font-size:var(--fs-body);margin:0 0 3px}}
.radar .rdir{{color:var(--accent);font-style:italic;font-size:var(--fs-meta)}}
.radar .rread{{font-size:var(--fs-detail);line-height:1.55;margin:0 0 5px}}
.radar .rbask{{margin:0;padding:0 0 0 18px;font-size:var(--fs-meta);line-height:1.45;color:var(--muted)}}
.radar-steady{{color:#b3b3b3;font-size:var(--fs-meta);letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 0}}
.rcompact{{font-size:var(--fs-detail);line-height:1.55;color:#555;margin:7px 0 0}}
.rcompact .rdir{{color:var(--accent);font-style:italic}}
.ghnote{{font-size:var(--fs-detail);line-height:1.6;color:var(--muted);margin:14px 0 0}}
table.mkt{{width:100%;border-collapse:collapse;margin:8px 0 0}}
table.mkt td{{padding:7px 2px;border-bottom:1px solid var(--line);font-size:var(--fs-detail)}}
table.mkt td.v{{text-align:right;font-weight:700}}
.means{{color:var(--muted);font-size:var(--fs-detail);line-height:1.7;margin-top:12px}}
.watch{{padding:12px 0;border-bottom:1px solid var(--line)}}
.watch .t{{font-size:var(--fs-body);font-weight:700}}
.watch .st{{font-size:var(--fs-meta);color:var(--faint);font-weight:400;font-style:italic}}
.watch .why{{font-size:var(--fs-detail);color:#333;margin:4px 0}}
.watch .via{{font-size:var(--fs-meta);color:var(--muted)}}
.watch.small{{padding:6px 0;font-size:var(--fs-meta);color:#999}}
footer{{margin-top:48px;border-top:1px solid var(--accent);padding-top:14px;
  font-size:var(--fs-meta);color:var(--faint);text-align:center;line-height:1.7}}
footer a{{color:var(--accent)}}
.subwrap{{text-align:center;margin:18px 0 0}}
.joinform{{display:flex;gap:8px;justify-content:center;align-items:stretch;margin:32px 0 0;flex-wrap:wrap}}
.joininput{{border:1px solid var(--line);border-radius:4px;padding:9px 13px;
  font-size:var(--fs-detail);font-family:var(--serif);color:var(--fg);min-width:220px}}
.joininput:focus{{outline:none;border-color:var(--accent)}}
a.subscribe,button.subscribe{{display:inline-block;background:transparent;color:var(--accent);
  border:1.5px solid var(--accent);text-decoration:none;font-size:var(--fs-detail);font-weight:600;
  padding:8px 20px;border-radius:4px;cursor:pointer;font-family:var(--serif)}}
a.subscribe:hover,button.subscribe:hover{{background:var(--accent);color:#fff}}
.subnote{{text-align:center;font-size:var(--fs-meta);color:var(--faint);margin:8px 0 0}}
"""


def esc(s) -> str:
    return html.escape(str(s))


def page(title: str, inner: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head><body><div class="wrap">
{inner}
<footer><a href="https://github.com/sooflee/magikarp">source on GitHub</a><br>
Market notes are directional only and are not investment advice.</footer>
</div></body></html>
"""


def badge(state: str) -> str:
    cls = "badge warn" if state in WARN_STATES else "badge"
    return f'<span class="{cls}">{esc(state)}</span>'


def lead_headline(iss: dict) -> str:
    if iss.get("index_title"):
        return iss["index_title"]
    reg = iss.get("regimes", {})
    for key, r in reg.items():
        if r.get("headline"):
            return r["headline"]
    return f"Issue {iss['id']}"


def first_sentence(text: str) -> str:
    if not text:
        return ""
    parts = text.split(". ")
    return parts[0] + ("." if not parts[0].endswith(".") else "")


def week_label(iss: dict) -> str:
    return iss.get("week", "").replace("/", " to ")


def render_links(links: list) -> str:
    if not links:
        return ""
    rows = "".join(
        f'<li><a href="{esc(l["url"])}">{esc(l["title"])}</a></li>'
        for l in links)
    return f'<ul class="links">{rows}</ul>'


def render_items(items: list) -> str:
    if not items:
        return ""
    return "".join(
        f'<p class="story"><a href="{esc(it["url"])}">{esc(it["title"])}</a><br>'
        f'<span class="cmt">{esc(it.get("comment",""))}</span></p>'
        for it in items)


def render_regime(label: str, r: dict, traj: str = None) -> str:
    body = r.get("summary") or " ".join(r.get("evidence", []))
    impl = (f'<p class="impl">{esc(r["implication"])}</p>' if r.get("implication") else "")
    traj_html = f'<p class="traj">{esc(traj)}</p>' if traj else ""
    return (f'<div class="sec"><h2>{esc(r.get("headline", label))}{badge(r.get("state",""))}</h2>'
            f'<p class="sub">{esc(label)}</p>{traj_html}<p>{esc(body)}</p>'
            f'{render_items(r.get("items"))}{render_links(r.get("links"))}{impl}</div>')


def _abs_index(doc: dict, iss: dict) -> int:
    for i, it in enumerate(doc.get("issues", [])):
        if it.get("id") == iss.get("id"):
            return i
    return len(doc.get("issues", [])) - 1


def _weeks_in_state_asof(doc: dict, key: str, idx: int) -> int:
    """weeks_in_state as of issue at absolute index idx (not just the latest)."""
    issues = [i for i in doc.get("issues", [])[:idx + 1] if key in i.get("regimes", {})]
    if not issues:
        return 0
    cur = issues[-1]["regimes"][key].get("state")
    n = 0
    for it in reversed(issues):
        if it["regimes"][key].get("state") == cur:
            n += 1
        else:
            break
    return n


def render_momentum(doc: dict, iss: dict) -> str:
    m = iss.get("momentum")
    if not m:
        return ""
    ser, weeks = m["series"], m["weeks"]
    idx = _abs_index(doc, iss)
    covered = set(iss.get("regimes", {})) - {"markets"}   # only chart regimes we cover
    rows = []
    for k in sorted(ser, key=lambda k: -ser[k][-1]):
        if k not in covered:
            continue
        cur = ser[k][-1]
        prev = ser[k][-2] if len(ser[k]) > 1 else cur
        if cur == 0 and prev == 0:
            continue
        arr, color = ("&#9650;", "#1a7f4b") if cur > prev else (
            ("&#9660;", "#b1300f") if cur < prev else ("&#9644;", "#9aa0aa"))
        label = esc(doc["regime_defs"].get(k, {}).get("label", k))
        st = iss.get("regimes", {}).get(k, {}).get("state")
        if st:
            label += (f' <span class="traj" style="display:inline;margin:0">'
                      f'&middot; week {_weeks_in_state_asof(doc, k, idx)} in {esc(st)}</span>')
        rows.append(f'<tr><td>{label}</td><td class="v" style="font-weight:400;white-space:nowrap">'
                    f'<span style="color:var(--faint)">{prev} &rarr; </span>'
                    f'<strong>{cur}</strong> <span style="color:{color}">{arr}</span></td></tr>')
    chg = regime_engine.changed_items(doc, idx - 1, idx) if idx > 0 else []
    chg_html = ""
    if chg:
        lis = "".join(
            f'<li><strong>{esc(lbl)}:</strong> {esc(one).replace("-&gt;", "&rarr;")}</li>'
            for lbl, one in chg)
        chg_html = ('<p style="margin-top:18px"><strong>What changed this week:</strong></p>'
                    f'<ul class="chg">{lis}</ul>')
    return (f'<div class="sec"><h2>Where the week&rsquo;s attention went.</h2>'
            f'<p class="sub">Regime momentum &middot; {esc(weeks[0])} vs {esc(weeks[-1])}</p>'
            f'<p class="means">Number of the week&rsquo;s top Hacker News stories in '
            f'each regime we cover, this week against last.</p>'
            f'<table class="mkt">{"".join(rows)}</table>{chg_html}{render_moves(iss)}</div>')


def render_moves(iss: dict) -> str:
    moves = ""
    for mv in iss.get("market_moves", []):
        arr = "&#9650;" if mv.get("dir") == "up" else ("&#9660;" if mv.get("dir") == "down" else "&#9644;")
        moves += (f'<li><a href="{esc(mv["url"])}">{esc(mv["market"])}</a> '
                  f'<span style="color:#9aa0aa">{arr}</span> {esc(mv.get("detail",""))}</li>')
    return (f'<p style="margin-top:18px"><strong>Markets that swung this week:</strong></p>'
            f'<ul class="links">{moves}</ul>') if moves else ""


def render_watch_next(iss: dict) -> str:
    wn = iss.get("watch_next", [])
    if not wn:
        return ""
    rows = "".join(
        f'<p class="wn"><span class="when">{esc(it.get("when",""))}</span> '
        f'<strong>{esc(it.get("event",""))}</strong><br>'
        f'<span class="cmt">{esc(it.get("note",""))}</span></p>' for it in wn)
    return (f'<div class="sec"><h2>What to watch next week.</h2>'
            f'<p class="sub">The calendar ahead</p>{rows}</div>')


def render_radar(iss: dict) -> str:
    regs = iss.get("structural_regimes", [])
    if not regs:
        return ""
    blocks = []
    for r in [r for r in regs if r.get("spotlight")]:
        basket = "".join(
            f'<li>{esc(b["metric"])}: <strong>{esc(b["value"])}</strong>'
            + (f' <a href="{esc(b["url"])}">source</a>' if b.get("url") else "")
            + '</li>' for b in r.get("basket", []))
        blocks.append(
            f'<div class="radar"><p class="rname"><strong>{esc(r["name"])}</strong> '
            f'<span class="rdir">{esc(r.get("direction",""))}</span></p>'
            f'<p class="rread">{esc(r["read"])}</p>'
            f'<ul class="rbask">{basket}</ul></div>')
    steady = [r for r in regs if not r.get("spotlight")]
    if steady:
        blocks.append('<p class="radar-steady">Holding steady</p>')
        for r in steady:
            b0 = (r.get("basket") or [None])[0]
            fact = f' {esc(b0["metric"])}: {esc(b0["value"])}.' if b0 else ""
            blocks.append(
                f'<p class="rcompact"><strong>{esc(r["name"])}</strong> '
                f'<span class="rdir">{esc(r.get("direction",""))}</span>.{fact}</p>')
    return ('<div class="sec"><h2>The structural picture.</h2>'
            '<p class="sub">Regime radar &middot; read through markets and hard data</p>'
            '<p class="means">The slow currents beneath the week. Each is read from a basket of '
            'dated markets and hard data, not a single headline.</p>'
            f'{"".join(blocks)}</div>')


def _chg_mag(chg):
    try:
        return abs(float(chg.replace("%", "").replace("+", "")))
    except Exception:
        return 999.0


def render_commodities(c: dict) -> str:
    floor = c.get("min_change", 0)
    rows = "".join(
        f'<tr><td>{esc(it["name"])}</td>'
        f'<td class="v">{esc(it.get("level",""))}</td>'
        f'<td class="v" style="font-weight:400;color:'
        f'{"#b1300f" if it.get("change","").startswith("-") else "#1a7f4b"}">{esc(it.get("change",""))}</td></tr>'
        for it in c.get("items", []) if _chg_mag(it.get("change", "")) >= floor)
    return (f'<div class="sec"><h2>{esc(c.get("headline", "Crude falls as the fear premium unwinds."))}</h2>'
            f'<p class="sub">Commodities &amp; energy &middot; {esc(c.get("as_of",""))}</p>'
            f'<p>{esc(c.get("summary",""))}</p>'
            f'<table class="mkt">{rows}</table></div>')


def render_contrarian(doc: dict, iss: dict) -> str:
    rows = []
    for key, r in iss.get("regimes", {}).items():
        if not r.get("contrarian"):
            continue
        label = doc["regime_defs"].get(key, {}).get("label", key)
        rows.append(f'<li><strong>{esc(label)}.</strong> {esc(r["contrarian"])}</li>')
    if not rows:
        return ""
    return (f'<div class="sec"><h2>What could change this.</h2>'
            f'<p class="sub">Contrarian read</p><ul class="chg">{"".join(rows)}</ul></div>')


def render_undercurrent(u: dict) -> str:
    return (f'<div class="sec"><h2>{esc(u["headline"])}</h2>'
            f'<p class="sub">{esc(u.get("label","Undercurrent"))}</p>'
            f'<p>{esc(u.get("summary",""))}</p>{render_links(u.get("links"))}</div>')


def render_wildcard(w: dict) -> str:
    """The rotating wildcard: one theme each week outside the four tracked lanes.
    Not part of the week-over-week momentum; renders only when present."""
    if not w or not w.get("headline"):
        return ""
    topic = w.get("topic", "")
    sub = f'The wildcard &middot; {esc(topic)}' if topic else 'The wildcard'
    return (f'<div class="sec wildcard"><h2>{esc(w["headline"])}</h2>'
            f'<p class="sub">{sub}</p>'
            f'<p>{esc(w.get("summary",""))}</p>'
            f'{render_items(w.get("items"))}{render_links(w.get("links"))}</div>')


def render_briefs(items: list) -> str:
    """Smaller stories: one-line briefs from the research/accountability sweep.
    Optional; renders only when the issue carries a briefs list."""
    if not items:
        return ""
    return (f'<div class="sec"><h2>Smaller stories.</h2>'
            f'<p class="sub">short items from the week&rsquo;s edges</p>'
            f'{render_items(items)}</div>')


def render_across_inline(a: dict) -> str:
    gh = a.get("github", [])
    if not gh:
        return ""
    items = " &middot; ".join(f'<a href="{esc(r["url"])}">{esc(r["title"])}</a>' for r in gh)
    return ('<p class="ghnote"><strong>On GitHub this week</strong>, trending is mostly '
            f'{esc(a.get("github_theme",""))}: {items}</p>')


MKT_ORDER = [("trend", "Trend"), ("vol", "Volatility"), ("curve_bp", "Yield curve"),
             ("gdpnow", "Growth (GDPNow)"), ("dollar", "Dollar"), ("credit", "Credit"),
             ("liquidity", "Liquidity"), ("crypto", "Crypto")]
MKT_FMT = {"curve_bp": lambda v: f"Steep (+{v} bp)", "vol": lambda v: f"Calm ({v})",
           "gdpnow": lambda v: f"{v}%"}
MKT_SENSE = {"trend": "pos", "vol": "pos", "curve_bp": "pos", "gdpnow": "pos",
             "dollar": "neutral", "credit": "pos", "liquidity": "neg", "crypto": "neg"}
MKT_COLOR = {"pos": "#1a7f4b", "neg": "#b1300f", "neutral": "#1a1a1a"}
# Directional tokens color by value, so a down/risk-off week reads red and a
# recovering week reads green. Unmatched values fall back to the per-key sense,
# which keeps earlier issues rendering exactly as before.
MKT_VALUE_SENSE = {"UP": "pos", "DOWN": "neg", "RISK-ON": "pos", "RISK-OFF": "neg",
                   "AMPLE": "pos", "EXPANDING": "pos", "DRAINED": "neg",
                   "DRAINING": "neg", "CONTRACTING": "neg"}


def mkt_color(key, val) -> str:
    sense = MKT_VALUE_SENSE.get(str(val).strip().upper(), MKT_SENSE.get(key, "neutral"))
    return MKT_COLOR[sense]


def render_markets(m: dict) -> str:
    sg = m.get("signals", {})
    rows = "".join(
        f'<tr><td>{lbl}</td><td class="v" style="color:{mkt_color(k, sg[k])}">'
        f'{esc(MKT_FMT.get(k, lambda v: v)(sg[k]))}</td></tr>'
        for k, lbl in MKT_ORDER if k in sg)
    summary = f"<p>{esc(m['summary'])}</p>" if m.get("summary") else ""
    means = (
        '<p class="means">Volatility measures how much the market is expected to '
        'move in the near term compared with the longer term, so a lower reading '
        'means less immediate stress. The yield curve is the gap between long-term '
        'and short-term government borrowing rates, and a steep curve usually points '
        'to expected growth rather than recession. When crypto is described as '
        'risk-off, investors are stepping back from the most speculative assets, '
        'which often serves as an early note of caution beneath a calm market.</p>')
    return (f'<div class="sec"><h2>{esc(m.get("headline","Markets"))}</h2>'
            f'<p class="sub">Markets</p>{summary}'
            f'<table class="mkt">{rows}</table>{means}</div>')


def render_watch(watch: list) -> str:
    new = [w for w in watch if w.get("new")]
    old = [w for w in watch if not w.get("new")]
    out = ['<div class="sec"><h2>Exponential trends to watch.</h2>'
           '<p class="sub">Signals to watch</p>']
    for w in new:
        out.append(
            f'<div class="watch"><div class="t">{esc(w["trend"])} '
            f'<span class="st">&middot; {esc(w["status"])}</span></div>'
            f'<div class="why">{esc(w["why_exponential"])}</div>'
            f'<div class="via"><strong>What to watch:</strong> {esc(w["watch"])} '
            f'<strong>Where it shows up:</strong> {esc(w["expressions"])}</div></div>')
    if old:
        out.append('<div class="watch small" style="color:#b3b3b3;border:0;font-style:italic">Still on watch</div>')
        for w in old:
            out.append(f'<div class="watch small"><strong style="color:#666">{esc(w["trend"])}</strong> '
                       f'&middot; {esc(w["status"])} &middot; {esc(w["expressions"])}</div>')
    out.append("</div>")
    return "".join(out)


def render_lede(iss: dict) -> str:
    return f'<p class="lede">{esc(iss["lede"])}</p>' if iss.get("lede") else ""


def render_act(title: str) -> str:
    return f'<div class="act"><div class="actlabel">{esc(title)}</div><hr></div>'


def _regime(doc, iss, key):
    r = iss.get("regimes", {}).get(key)
    return render_regime(doc["regime_defs"].get(key, {}).get("label", key), r) if r else ""


def render_issue_page(doc: dict, iss: dict) -> str:
    reg = iss.get("regimes", {})
    secs = [render_lede(iss), render_momentum(doc, iss)]
    # Act 1 — the tech world
    secs.append(render_act("The tech world"))
    if "ai_compute" in reg:                       # issue 06+ : one merged AI lane
        secs.append(_regime(doc, iss, "ai_compute"))
    else:                                          # archive (01-05) : the old two lanes
        secs.append(_regime(doc, iss, "tech_policy"))
        secs.append(_regime(doc, iss, "ai_agents"))
    if iss.get("across_sources"):
        secs.append(render_across_inline(iss["across_sources"]))   # GitHub note under AI
    secs.append(render_watch(iss.get("bsig_watch") or doc.get("bsig_watch", [])))
    if iss.get("undercurrent"):
        secs.append(render_undercurrent(iss["undercurrent"]))
    # Act 2 — the wider world
    secs.append(render_act("The wider world"))
    if "deep_dive" in reg:                         # rotating non-tech lane, leads Act 2
        secs.append(_regime(doc, iss, "deep_dive"))
    secs.append(_regime(doc, iss, "geopolitics"))
    if iss.get("commodities"):
        secs.append(render_commodities(iss["commodities"]))
    if "markets" in reg:
        secs.append(render_markets(reg["markets"]))
    if iss.get("wildcard"):
        secs.append(render_wildcard(iss["wildcard"]))
    if iss.get("briefs"):
        secs.append(render_briefs(iss["briefs"]))
    secs.append(render_radar(iss))
    secs.append(render_watch_next(iss))
    inner = (
        f'<header class="mast"><h1><a href="../">The Current Regime</a></h1>'
        f'<div class="kicker">Issue {esc(iss["id"])} &middot; {esc(week_label(iss))}</div></header>'
        f'<p class="back" style="margin-top:14px"><a href="../">&larr; all issues</a></p>'
        + "".join(secs)
    )
    return page(f"The Current Regime · Issue {iss['id']}", inner)


def render_index(doc: dict, issues: list) -> str:
    posts = []
    for iss in issues:
        posts.append(
            f'<div class="post">'
            f'<p class="date">Issue {esc(iss["id"])} &middot; {esc(week_label(iss))}</p>'
            f'<h2><a href="issues/{esc(iss["id"])}.html">{esc(lead_headline(iss))}</a></h2>'
            f'<p class="dek">{esc(first_sentence(_lead_summary(iss)))}</p>'
            f'</div>')
    inner = (
        '<header class="mast home"><h1>The Current Regime</h1></header>'
        + "".join(posts)
        + '<div id="join">' + SUBSCRIBE_FORM + '</div>'
    )
    return page("The Current Regime", inner)


def _lead_summary(iss: dict) -> str:
    for r in iss.get("regimes", {}).values():
        if r.get("summary"):
            return r["summary"]
    return ""




def build():
    doc = json.loads(STATE.read_text())
    regime_engine.lint_or_die(regime_engine.latest_issue(doc))
    issues = [i for i in doc.get("issues", []) if not i.get("partial")]
    issues.sort(key=lambda i: i["id"], reverse=True)
    (DOCS / "issues").mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(render_index(doc, issues))
    for iss in issues:
        (DOCS / "issues" / f"{iss['id']}.html").write_text(render_issue_page(doc, iss))
    return issues


def main() -> int:
    issues = build()
    print(f"wrote docs/index.html + {len(issues)} issue page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
