#!/usr/bin/env python3
"""Build the public archive (GitHub Pages) for 'The Current Regime'.

Renders every issue in regime_state.json into docs/index.html, styled after
bwang.io/elekid: a single serif face throughout, a forest-green accent, and a
calm, didactic layout. GitHub Pages serves /docs on main.

Usage:
    python3 build_site.py        # writes docs/index.html
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "regime_state.json"
OUT = ROOT / "docs" / "index.html"

ACCENT = "#1a7f4b"
WARN_STATES = {"state-capture", "risk-off", "contracting", "liability-reckoning",
               "stressed", "constrained"}

CSS = f"""
:root{{
  --serif:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif;
  --fg:#1a1a1a; --muted:#6b7280; --faint:#9aa0aa; --line:#e5e7eb;
  --accent:{ACCENT}; --accent-bg:#e7f3ec; --bg:#ffffff; --warn:#b1300f;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--serif);
  font-size:19px;line-height:1.75}}
.wrap{{max-width:680px;margin:0 auto;padding:72px 24px 96px}}
a{{color:var(--accent)}}
/* every text element shares the serif face and one type scale */
header.mast{{text-align:center;border-bottom:2px solid var(--accent);padding-bottom:28px}}
header.mast h1{{font-size:48px;line-height:1.1;letter-spacing:-0.5px;margin:0;font-weight:700}}
header.mast .kicker{{font-size:15px;letter-spacing:1px;color:var(--accent);
  font-style:italic;margin-top:16px}}
.sec{{padding-top:44px}}
.sec h2{{font-size:28px;line-height:1.3;letter-spacing:-0.3px;margin:0 0 4px;font-weight:700}}
.sec .sub{{font-size:16px;font-weight:600;color:var(--accent);margin:0 0 14px}}
.sec p{{font-size:19px;line-height:1.75;margin:0 0 12px}}
.badge{{display:inline-block;font-size:14px;font-weight:600;padding:1px 10px;
  border-radius:3px;background:var(--accent-bg);color:var(--accent);
  margin-left:10px;vertical-align:middle}}
.badge.warn{{background:#fbeae6;color:var(--warn)}}
.ihead{{font-size:16px;color:var(--faint);text-align:center;margin-bottom:6px;font-style:italic}}
table.mkt{{width:100%;border-collapse:collapse;margin:10px 0 0}}
table.mkt td{{padding:11px 2px;border-bottom:1px solid var(--line);font-size:17px}}
table.mkt td.v{{text-align:right;font-weight:700}}
.means{{color:var(--muted);font-size:17px;line-height:1.75;margin-top:16px}}
.watch{{padding:18px 0;border-bottom:1px solid var(--line)}}
.watch .t{{font-size:20px;font-weight:700}}
.watch .st{{font-size:15px;color:var(--faint);font-weight:400;font-style:italic}}
.watch .why{{font-size:17px;color:#333;margin:6px 0}}
.watch .via{{font-size:16px;color:var(--muted)}}
.watch.small{{padding:9px 0;font-size:16px;color:#888}}
footer{{margin-top:72px;border-top:2px solid var(--accent);padding-top:22px;
  font-size:15px;color:var(--faint);text-align:center;line-height:1.7}}
footer a{{color:var(--accent)}}
"""


def esc(s) -> str:
    return html.escape(str(s))


def badge(state: str) -> str:
    cls = "badge warn" if state in WARN_STATES else "badge"
    return f'<span class="{cls}">{esc(state)}</span>'


def render_regime(label: str, r: dict) -> str:
    body = r.get("summary")
    if body:
        text = f"<p>{esc(body)}</p>"
    else:
        ev = "".join(f"<li>{esc(x)}</li>" for x in r.get("evidence", []))
        text = f'<ul class="ev">{ev}</ul>' if ev else ""
    impl = (f'<p style="color:var(--muted)">{esc(r["implication"])}</p>'
            if r.get("implication") else "")
    return (f'<div class="sec"><h2>{esc(r.get("headline", label))}{badge(r.get("state",""))}</h2>'
            f'<p class="sub">{esc(label)}</p>{text}{impl}</div>')


def render_markets(m: dict) -> str:
    sg = m.get("signals", {})
    rows = []
    order = [("trend", "Trend"), ("vol", "Volatility"), ("curve_bp", "Yield curve"),
             ("gdpnow", "Growth (GDPNow)"), ("liquidity", "Liquidity"), ("crypto", "Crypto")]
    fmt = {"curve_bp": lambda v: f"Steep (+{v} bp)", "vol": lambda v: f"Calm ({v})",
           "gdpnow": lambda v: f"{v}%"}
    for key, label in order:
        if key not in sg:
            continue
        val = fmt.get(key, lambda v: v)(sg[key])
        rows.append(f'<tr><td>{label}</td><td class="v">{esc(val)}</td></tr>')
    summary = f"<p>{esc(m['summary'])}</p>" if m.get("summary") else ""
    means = (
        '<p class="means">Volatility measures how much the market is expected to '
        'move in the near term compared with the longer term, so a lower reading '
        'means traders see less immediate stress. The yield curve is the gap '
        'between long-term and short-term government borrowing rates, and a steep '
        'curve usually points to expected growth rather than recession. When crypto '
        'is described as risk-off, investors are stepping back from the most '
        'speculative assets, which often serves as an early note of caution beneath '
        'an otherwise calm market.</p>')
    return (f'<div class="sec"><h2>{esc(m.get("headline","Markets"))}</h2>'
            f'<p class="sub">Markets</p>{summary}'
            f'<table class="mkt">{"".join(rows)}</table>{means}</div>')


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
        out.append('<div class="watch small" style="color:#b3b3b3;border:0;font-style:italic;'
                   'padding-top:16px">Still on watch</div>')
        for w in old:
            out.append(f'<div class="watch small"><strong style="color:#555">{esc(w["trend"])}</strong> '
                       f'&middot; {esc(w["status"])} &middot; {esc(w["expressions"])}</div>')
    out.append("</div>")
    return "".join(out)


def render_issue(doc: dict, iss: dict) -> str:
    parts = [f'<div class="ihead">Issue {esc(iss["id"])} &middot; '
             f'{esc(iss.get("week","").replace("/", " to "))}</div>']
    defs = doc["regime_defs"]
    reg = iss.get("regimes", {})
    for key, r in reg.items():
        if key == "markets":
            continue
        parts.append(render_regime(defs.get(key, {}).get("label", key), r))
    if "markets" in reg:
        parts.append(render_markets(reg["markets"]))
    return "".join(parts)


def build() -> str:
    doc = json.loads(STATE.read_text())
    issues = [i for i in doc.get("issues", []) if not i.get("partial")]
    issues.sort(key=lambda i: i["id"], reverse=True)
    body = [render_issue(doc, iss) for iss in issues]
    body.append(render_watch(doc.get("bsig_watch", [])))
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Current Regime</title>
<style>{CSS}</style>
</head><body><div class="wrap">
<header class="mast">
  <h1>The Current Regime</h1>
  <div class="kicker">A weekly read on what rules now</div>
</header>
{"".join(body)}
<footer>The Current Regime &middot; <a href="https://github.com/sooflee/magikarp">source on GitHub</a><br>
Market notes are directional only and are not investment advice.</footer>
</div></body></html>
"""


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build())
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
