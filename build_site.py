#!/usr/bin/env python3
"""Build the public archive (GitHub Pages) for 'The Current Regime'.

Renders every issue in regime_state.json into docs/index.html, styled after
bwang.io/elekid (serif, light, print-like). GitHub Pages serves /docs on main.

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

WARN_STATES = {"state-capture", "risk-off", "contracting", "liability-reckoning",
               "stressed", "constrained"}

CSS = """
:root{
  --serif:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,system-ui,sans-serif;
  --fg:#1a1a1a; --muted:#6b7280; --faint:#9aa0aa; --line:#e5e7eb;
  --link:#0b5fff; --bg:#ffffff; --warn:#b1300f; --good:#1a7f4b;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--serif);
  font-size:18px;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:720px;margin:0 auto;padding:64px 22px 96px}
a{color:var(--link)}
header.mast{text-align:center;border-bottom:1px solid var(--fg);padding-bottom:26px;margin-bottom:8px}
header.mast h1{font-size:46px;letter-spacing:-0.5px;margin:0}
header.mast .kicker{font-family:var(--sans);text-transform:uppercase;letter-spacing:2.5px;
  font-size:12px;color:var(--faint);margin-top:14px}
header.mast .dek{color:var(--muted);font-size:17px;max-width:480px;margin:14px auto 0}
.issue{padding-top:44px}
.issue > .ihead{font-family:var(--sans);text-transform:uppercase;letter-spacing:2.5px;
  font-size:12px;color:var(--faint);text-align:center;margin-bottom:8px}
.sec{padding-top:38px}
.sec h2{font-size:27px;line-height:1.25;letter-spacing:-0.3px;margin:0 0 2px}
.sec .sub{font-family:var(--sans);font-size:13px;font-weight:600;color:var(--faint);margin:0 0 12px}
.badge{display:inline-block;font-family:var(--sans);font-size:11px;font-weight:700;
  letter-spacing:1px;text-transform:uppercase;padding:2px 8px;border-radius:3px;
  background:#eef0f3;color:#444;margin-left:8px;vertical-align:middle}
.badge.warn{background:#fbeae6;color:var(--warn)}
.sec p{margin:0 0 10px}
ul.ev{margin:6px 0 0;padding-left:20px}
ul.ev li{margin:0 0 6px}
table.mkt{width:100%;border-collapse:collapse;margin:8px 0 0}
table.mkt td{padding:9px 2px;border-bottom:1px solid var(--line);font-family:var(--sans);font-size:15px}
table.mkt td.v{text-align:right;font-weight:700}
.means{color:var(--muted);font-size:15px;margin-top:14px}
.watch{padding:14px 0;border-bottom:1px solid var(--line)}
.watch .t{font-size:18px;font-weight:700}
.watch .st{font-family:var(--sans);font-size:12px;color:var(--faint);font-weight:400}
.watch .why{font-size:15px;color:#444;margin:4px 0}
.watch .via{font-family:var(--sans);font-size:13px;color:var(--muted)}
.watch.small{padding:7px 0;font-size:14px;color:#888}
.momentum{font-family:var(--sans);font-size:14px}
.momentum .row{display:flex;align-items:center;gap:10px;margin:3px 0}
.momentum .lab{width:130px;color:#444}
.momentum .bar{height:12px;background:#1a1a1a;border-radius:2px}
.momentum .n{color:var(--faint)}
footer{margin-top:64px;border-top:1px solid var(--fg);padding-top:20px;
  font-family:var(--sans);font-size:13px;color:var(--faint);text-align:center}
"""


def esc(s) -> str:
    return html.escape(str(s))


def badge(state: str) -> str:
    cls = "badge warn" if state in WARN_STATES else "badge"
    return f'<span class="{cls}">{esc(state)}</span>'


def render_markets(m: dict) -> str:
    sg = m.get("signals", {})
    rows = []
    order = [("trend", "Trend"), ("vol", "Volatility"), ("curve_bp", "Yield curve"),
             ("gdpnow", "Growth (GDPNow)"), ("liquidity", "Liquidity"), ("crypto", "Crypto")]
    fmt = {"curve_bp": lambda v: f"STEEP (+{v} bp)", "vol": lambda v: f"CALM ({v})",
           "gdpnow": lambda v: f"{v}%"}
    for key, label in order:
        if key not in sg:
            continue
        val = fmt.get(key, lambda v: v)(sg[key])
        rows.append(f'<tr><td>{label}</td><td class="v">{esc(val)}</td></tr>')
    means = (
        '<p class="means"><strong>What the readings mean.</strong> '
        'Volatility is the ratio of near-term to longer-term expected market swings; '
        'lower means less immediate stress. A steep yield curve (long minus short '
        'government rates) usually signals expected growth, not recession. Crypto '
        '&ldquo;risk-off&rdquo; means money is leaving the most speculative assets &mdash; '
        'an early caution sign beneath a calm surface.</p>')
    return (f'<div class="sec"><h2>{esc(m.get("headline","Markets"))}</h2>'
            f'<p class="sub">Markets</p>'
            f'<table class="mkt">{"".join(rows)}</table>{means}</div>')


def render_regime(label: str, r: dict) -> str:
    ev = "".join(f"<li>{esc(x)}</li>" for x in r.get("evidence", []))
    ev = f'<ul class="ev">{ev}</ul>' if ev else ""
    return (f'<div class="sec"><h2>{esc(r.get("headline", label))}{badge(r.get("state",""))}</h2>'
            f'<p class="sub">{esc(label)}</p>{ev}</div>')


def render_watch(watch: list) -> str:
    new = [w for w in watch if w.get("new")]
    old = [w for w in watch if not w.get("new")]
    out = ['<div class="sec"><h2>Exponential trends to watch.</h2><p class="sub">Signals to watch</p>']
    for w in new:
        out.append(
            f'<div class="watch"><div class="t">{esc(w["trend"])} '
            f'<span class="st">&middot; {esc(w["status"])}</span></div>'
            f'<div class="why">{esc(w["why_exponential"])}</div>'
            f'<div class="via"><strong>Watch:</strong> {esc(w["watch"])} &middot; '
            f'<strong>Where it shows up:</strong> {esc(w["expressions"])}</div></div>')
    if old:
        out.append('<div class="watch small" style="color:#b3b3b3;border:0;text-transform:uppercase;'
                   'letter-spacing:1.5px;font-size:12px;padding-top:14px">Still on watch</div>')
        for w in old:
            out.append(f'<div class="watch small"><strong style="color:#555">{esc(w["trend"])}</strong> '
                       f'&middot; {esc(w["status"])} &middot; {esc(w["expressions"])}</div>')
    out.append("</div>")
    return "".join(out)


def render_momentum(doc: dict) -> str:
    dc = doc.get("daily_counts", [])
    if not dc:
        return ""
    rec = dc[-1]
    counts = {k: v for k, v in rec["counts"].items() if k != "unaligned" and v}
    if not counts:
        return ""
    mx = max(counts.values())
    labels = {k: doc["regime_defs"].get(k, {}).get("label", k) for k in counts}
    rows = []
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        w = int(160 * v / mx) + 6
        rows.append(f'<div class="row"><span class="lab">{esc(labels[k])}</span>'
                    f'<span class="bar" style="width:{w}px"></span><span class="n">{v}</span></div>')
    return (f'<div class="sec"><h2>What the week was about.</h2>'
            f'<p class="sub">Regime momentum &middot; {esc(rec["date"])} &middot; '
            f'{rec["total"]} stories classified</p><div class="momentum">{"".join(rows)}</div></div>')


def render_issue(doc: dict, iss: dict) -> str:
    parts = [f'<div class="issue"><div class="ihead">Issue {esc(iss["id"])} &middot; '
             f'{esc(iss.get("week","").replace("/", " to "))}</div>']
    defs = doc["regime_defs"]
    reg = iss.get("regimes", {})
    # editorial regimes first (skip markets, rendered specially), then markets
    for key, r in reg.items():
        if key == "markets":
            continue
        parts.append(render_regime(defs.get(key, {}).get("label", key), r))
    if "markets" in reg:
        parts.append(render_markets(reg["markets"]))
    parts.append("</div>")
    return "".join(parts)


def build() -> str:
    doc = json.loads(STATE.read_text())
    issues = [i for i in doc.get("issues", []) if not i.get("partial")]
    issues.sort(key=lambda i: i["id"], reverse=True)
    body = [render_momentum(doc)]
    for iss in issues:
        body.append(render_issue(doc, iss))
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
  <p class="dek">The dominant themes from the top of Hacker News each week, verified
  against primary reporting, with a market-regime read. Regimes change; this is the record.</p>
</header>
{"".join(body)}
<footer>The Current Regime &middot; <a href="https://github.com/sooflee/magikarp">source on GitHub</a>
&middot; market notes are directional only, not investment advice</footer>
</div></body></html>
"""


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build())
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
