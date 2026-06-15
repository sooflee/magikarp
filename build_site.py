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
WARN_STATES = {"state-capture", "risk-off", "contracting", "liability-reckoning",
               "stressed", "constrained"}

CSS = f"""
:root{{
  --serif:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif;
  --fg:#1a1a1a; --muted:#6b7280; --faint:#9aa0aa; --line:#e8e8e8;
  --accent:{ACCENT}; --accent-bg:#e7f3ec; --bg:#fff; --warn:#b1300f;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 var(--serif);
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:640px;margin:0 auto;padding:52px 22px 72px}}
a{{color:var(--accent)}}
header.mast{{border-bottom:1px solid var(--accent);padding-bottom:16px;margin-bottom:8px}}
header.mast.home{{text-align:center;padding-bottom:20px}}
header.mast h1{{font-size:30px;line-height:1.1;letter-spacing:-0.02em;margin:0;font-weight:700}}
header.mast h1 a{{color:var(--fg);text-decoration:none}}
header.mast .kicker{{font-size:13px;color:var(--accent);font-style:italic;margin-top:8px}}
.back{{font-size:13px;font-style:italic}}
/* index: issues as posts */
.post{{padding:22px 0;border-bottom:1px solid var(--line)}}
.post .date{{font-size:12.5px;color:var(--faint);margin:0 0 3px}}
.post h2{{font-size:21px;line-height:1.25;letter-spacing:-0.01em;margin:0 0 4px;font-weight:700}}
.post h2 a{{color:var(--fg);text-decoration:none}}
.post h2 a:hover{{color:var(--accent)}}
.post .dek{{font-size:15px;color:var(--muted);margin:0}}
.post .tags{{font-size:12.5px;color:var(--faint);margin:6px 0 0}}
/* issue page sections */
.sec{{padding-top:30px}}
.sec h2{{font-size:21px;line-height:1.3;letter-spacing:-0.01em;margin:0 0 2px;font-weight:700}}
.sec .sub{{font-size:13px;font-weight:600;color:var(--accent);margin:0 0 9px}}
.sec p{{font-size:16px;line-height:1.65;margin:0 0 9px}}
.badge{{display:inline-block;font-size:11.5px;font-weight:600;padding:1px 7px;
  border-radius:3px;background:var(--accent-bg);color:var(--accent);
  margin-left:7px;vertical-align:middle}}
.badge.warn{{background:#fbeae6;color:var(--warn)}}
.impl{{color:var(--muted);font-size:15px}}
ul.links{{margin:8px 0 0;padding-left:18px}}
ul.links li{{margin:0 0 4px;font-size:14px;line-height:1.45}}
ul.links .pts{{color:var(--faint);font-size:12px}}
ul.chg{{margin:6px 0 0;padding-left:18px}}
ul.chg li{{margin:0 0 8px;font-size:15px;line-height:1.5}}
.across p{{font-size:15px;line-height:1.6;margin:0 0 8px}}
table.mkt{{width:100%;border-collapse:collapse;margin:8px 0 0}}
table.mkt td{{padding:7px 2px;border-bottom:1px solid var(--line);font-size:14px}}
table.mkt td.v{{text-align:right;font-weight:700}}
.means{{color:var(--muted);font-size:14px;line-height:1.7;margin-top:12px}}
.watch{{padding:12px 0;border-bottom:1px solid var(--line)}}
.watch .t{{font-size:16px;font-weight:700}}
.watch .st{{font-size:12.5px;color:var(--faint);font-weight:400;font-style:italic}}
.watch .why{{font-size:14px;color:#333;margin:4px 0}}
.watch .via{{font-size:13px;color:var(--muted)}}
.watch.small{{padding:6px 0;font-size:13px;color:#999}}
footer{{margin-top:48px;border-top:1px solid var(--accent);padding-top:14px;
  font-size:12.5px;color:var(--faint);text-align:center;line-height:1.7}}
footer a{{color:var(--accent)}}
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
<footer>The Current Regime &middot; <a href="https://github.com/sooflee/magikarp">source on GitHub</a><br>
Market notes are directional only and are not investment advice.</footer>
</div></body></html>
"""


def badge(state: str) -> str:
    cls = "badge warn" if state in WARN_STATES else "badge"
    return f'<span class="{cls}">{esc(state)}</span>'


def lead_headline(iss: dict) -> str:
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
        f'<li><a href="{esc(l["url"])}">{esc(l["title"])}</a> '
        f'<span class="pts">{esc(l.get("points",""))} pts</span></li>'
        for l in links)
    return f'<ul class="links">{rows}</ul>'


def render_regime(label: str, r: dict) -> str:
    body = r.get("summary") or " ".join(r.get("evidence", []))
    impl = (f'<p class="impl">{esc(r["implication"])}</p>' if r.get("implication") else "")
    return (f'<div class="sec"><h2>{esc(r.get("headline", label))}{badge(r.get("state",""))}</h2>'
            f'<p class="sub">{esc(label)}</p><p>{esc(body)}</p>{impl}'
            f'{render_links(r.get("links"))}</div>')


def render_what_changed(doc: dict) -> str:
    d = regime_engine.diff(doc)
    cregs = d["cur"].get("regimes", {})

    def impl(k):
        return cregs.get(k, {}).get("implication", "")

    items = []
    for key, label, a, b in d["changed"]:
        items.append((f'<strong>{esc(label)}:</strong> {esc(a)} &rarr; <strong>{esc(b)}</strong>', impl(key)))
    for key, label, st, sig in d["steady"]:
        if sig:
            items.append((f'<strong>{esc(label)}:</strong> {esc(", ".join(sig))}', impl(key)))
    for key, label, st, head in d["new"]:
        items.append((f'<strong>{esc(label)}:</strong> {esc(head)}', impl(key)))
    if not items:
        return ""
    lis = ""
    for one, im in items:
        lis += f'<li>{one}'
        if im:
            lis += f'<br><span style="color:var(--muted)">{esc(im)}</span>'
        lis += '</li>'
    return (f'<div class="sec"><h2>What changed.</h2>'
            f'<p class="sub">Since {esc(d["prev"]["date"])}</p>'
            f'<ul class="chg">{lis}</ul></div>')


def render_undercurrent(u: dict) -> str:
    return (f'<div class="sec"><h2>{esc(u["headline"])}</h2>'
            f'<p class="sub">{esc(u.get("label","Undercurrent"))}</p>'
            f'<p>{esc(u.get("summary",""))}</p>{render_links(u.get("links"))}</div>')


def render_across(a: dict) -> str:
    gh, ax = a.get("github", []), a.get("arxiv", [])
    if not gh and not ax:
        return ""
    out = ['<div class="sec across"><h2>What&rsquo;s getting built and published.</h2>'
           '<p class="sub">Across the sources</p>']
    if gh:
        items = " &middot; ".join(f'<a href="{esc(r["url"])}">{esc(r["title"])}</a>' for r in gh)
        out.append(f'<p><strong>GitHub trending</strong> shows {esc(a.get("github_theme",""))}: {items}</p>')
    if ax:
        items = "".join(f'<li><a href="{esc(x["url"])}">{esc(x["title"])}</a></li>' for x in ax)
        out.append('<p style="margin-bottom:2px"><strong>arXiv</strong>, the latest in cs.AI, cs.LG and cs.CL:</p>'
                   f'<ul class="links">{items}</ul>')
    out.append("</div>")
    return "".join(out)


def render_markets(m: dict) -> str:
    sg = m.get("signals", {})
    order = [("trend", "Trend"), ("vol", "Volatility"), ("curve_bp", "Yield curve"),
             ("gdpnow", "Growth (GDPNow)"), ("liquidity", "Liquidity"), ("crypto", "Crypto")]
    fmt = {"curve_bp": lambda v: f"Steep (+{v} bp)", "vol": lambda v: f"Calm ({v})",
           "gdpnow": lambda v: f"{v}%"}
    rows = "".join(f'<tr><td>{lbl}</td><td class="v">{esc(fmt.get(k, lambda v: v)(sg[k]))}</td></tr>'
                   for k, lbl in order if k in sg)
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
            f'<div class="via"><strong>What to watch:</strong> {esc(w["watch"])}. '
            f'<strong>Where it shows up:</strong> {esc(w["expressions"])}.</div></div>')
    if old:
        out.append('<div class="watch small" style="color:#b3b3b3;border:0;font-style:italic">Still on watch</div>')
        for w in old:
            out.append(f'<div class="watch small"><strong style="color:#666">{esc(w["trend"])}</strong> '
                       f'&middot; {esc(w["status"])} &middot; {esc(w["expressions"])}</div>')
    out.append("</div>")
    return "".join(out)


def render_issue_page(doc: dict, iss: dict) -> str:
    defs = doc["regime_defs"]
    reg = iss.get("regimes", {})
    # email order: what-changed, editorial regimes (+links), markets, undercurrent, across, watch
    secs = [render_what_changed(doc)]
    for key, r in reg.items():
        if key == "markets":
            continue
        secs.append(render_regime(defs.get(key, {}).get("label", key), r))
    if "markets" in reg:
        secs.append(render_markets(reg["markets"]))
    if iss.get("undercurrent"):
        secs.append(render_undercurrent(iss["undercurrent"]))
    if iss.get("across_sources"):
        secs.append(render_across(iss["across_sources"]))
    secs.append(render_watch(doc.get("bsig_watch", [])))
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
            f'<p class="tags">{esc(_tags(doc, iss))}</p>'
            f'</div>')
    inner = (
        '<header class="mast home"><h1>The Current Regime</h1></header>'
        + "".join(posts)
    )
    return page("The Current Regime", inner)


def _lead_summary(iss: dict) -> str:
    for r in iss.get("regimes", {}).values():
        if r.get("summary"):
            return r["summary"]
    return ""


def _tags(doc: dict, iss: dict) -> str:
    defs = doc["regime_defs"]
    return "  ·  ".join(defs.get(k, {}).get("label", k) for k in iss.get("regimes", {}))


def build():
    doc = json.loads(STATE.read_text())
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
