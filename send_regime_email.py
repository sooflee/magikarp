#!/usr/bin/env python3
"""Send the latest issue of 'The Current Regime' via Gmail SMTP.

Fully data-driven: every section is rendered from the latest issue in
regime_state.json, so the email cannot drift from the public archive (build_site.py
renders the same data) or from the 'What changed' diff.

Usage:
    export GMAIL_APP_PASSWORD="your-16-char-app-password"
    python3 send_regime_email.py
"""

import html
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path

import regime_engine

SENDER = "bensonw.dev@gmail.com"
RECIPIENT = "bensonw.dev@gmail.com"
SUBSCRIBERS = Path(__file__).resolve().parent / "subscribers.txt"


def load_subscribers():
    """One email per line in subscribers.txt; blanks and #comments ignored.
    Falls back to just the sender if the list is missing or empty."""
    if SUBSCRIBERS.exists():
        subs = []
        for line in SUBSCRIBERS.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "@" in line:
                subs.append(line)
        if subs:
            return subs
    return [SENDER]

SERIF = ("'Iowan Old Style','Palatino Linotype',Palatino,Georgia,"
         "'Times New Roman',serif")
ACCENT = "#1a7f4b"

STATE = regime_engine.load()
ISSUE = [i for i in STATE["issues"] if not i.get("partial")][-1]
DEFS = STATE["regime_defs"]
DATE_LABEL = ISSUE.get("date_label", ISSUE.get("week", ""))
SUBJECT = f"The Current Regime · {ISSUE['id']} · {DATE_LABEL}"

MARKET_MEANS = (
    "Volatility measures how much the market is expected to move in the near term "
    "compared with the longer term, so a lower reading means less immediate stress. "
    "The yield curve is the gap between long-term and short-term government borrowing "
    "rates, and a steep curve usually points to expected growth rather than recession. "
    "When crypto is described as risk-off, investors are stepping back from the most "
    "speculative assets, which often serves as an early note of caution beneath a calm "
    "market.")

MKT_ORDER = [("trend", "Trend"), ("vol", "Volatility"), ("curve_bp", "Yield curve"),
             ("gdpnow", "Growth (GDPNow)"), ("dollar", "Dollar"), ("credit", "Credit"),
             ("liquidity", "Liquidity"), ("crypto", "Crypto")]
MKT_FMT = {"vol": lambda v: f"Calm ({v})", "curve_bp": lambda v: f"Steep (+{v} bp)",
           "gdpnow": lambda v: f"{v}%"}
# sense: "pos" constructive (green), "neg" cautious (red), "neutral" (dark)
MKT_SENSE = {"trend": "pos", "vol": "pos", "curve_bp": "pos", "gdpnow": "pos",
             "dollar": "neutral", "credit": "pos", "liquidity": "neg", "crypto": "neg"}
MKT_COLOR = {"pos": "#1a7f4b", "neg": "#b1300f", "neutral": "#1a1a1a"}


def esc(s) -> str:
    return html.escape(str(s), quote=False)


# ---------- HTML ----------

def _links_html(links):
    if not links:
        return ""
    rows = "".join(
        '<tr><td style="padding:9px 0; border-bottom:1px solid #ededed; '
        f'font-family:{SERIF}; font-size:15px; line-height:1.5; vertical-align:top;">'
        f'<a href="{l["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(l["title"])}</a>'
        '</td></tr>' for l in links)
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin-top:8px;">{rows}</table>')


def _items_html(items):
    if not items:
        return ""
    return "".join(
        f'<p style="margin:14px 0 0; font-size:15px; line-height:1.6; font-family:{SERIF};">'
        f'<a href="{it["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(it["title"])}</a><br>'
        f'<span style="color:#555;">{esc(it.get("comment",""))}</span></p>'
        for it in items)


def _section_html(label, title, paragraph, links=None, items=None, trajectory=None):
    traj = (f'<p style="margin:0 0 12px; color:#9a9a9a; font-size:13px; font-style:italic; '
            f'font-family:{SERIF};">{esc(trajectory)}</p>' if trajectory else "")
    sub_mb = "2px" if trajectory else "14px"
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">{esc(title)}</h2>
              <p style="margin:0 0 {sub_mb}; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">{esc(label)}</p>
              {traj}
              <p style="margin:0 0 4px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SERIF};">{esc(paragraph)}</p>
              {_items_html(items)}
              {_links_html(links)}
            </td>
          </tr>
"""


def _momentum_html(state):
    m = regime_engine.momentum(state)
    if not m:
        return ""
    series, weeks = m["series"], m["weeks"]
    covered = set(ISSUE.get("regimes", {})) - {"markets"}   # only chart regimes we cover
    rows = []
    for k in sorted(series, key=lambda k: -series[k][-1]):
        if k not in covered:
            continue
        cur = series[k][-1]
        prev = series[k][-2] if len(series[k]) > 1 else cur
        if cur == 0 and prev == 0:
            continue
        arrow, color = ("&#9650;", "#1a7f4b") if cur > prev else (
            ("&#9660;", "#b1300f") if cur < prev else ("&#9644;", "#9a9a9a"))
        label = esc(DEFS.get(k, {}).get("label", k))
        st = ISSUE.get("regimes", {}).get(k, {}).get("state")
        if st:
            label += (f' <span style="color:#9a9a9a; font-size:13px; font-style:italic;">'
                      f'&middot; week {regime_engine.weeks_in_state(state, k)} in {esc(st)}</span>')
        rows.append(
            f'<tr><td style="padding:8px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; color:#1a1a1a;">{label}</td>'
            f'<td align="right" style="padding:8px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; color:#9a9a9a; white-space:nowrap;">{prev} &rarr; '
            f'<span style="color:#1a1a1a; font-weight:700;">{cur}</span> '
            f'<span style="color:{color};">{arrow}</span></td></tr>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">Where the week&rsquo;s attention went.</h2>
              <p style="margin:0 0 8px; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">Regime momentum &middot; {esc(weeks[0])} vs {esc(weeks[-1])}</p>
              <p style="margin:0 0 6px; color:#555; font-size:15px; line-height:1.6; font-family:{SERIF};">Number of the week&rsquo;s top Hacker News stories in each regime we cover, this week against last.</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
              {_market_moves_html(ISSUE)}
            </td>
          </tr>
"""


def _market_moves_html(issue):
    moves = issue.get("market_moves", [])
    if not moves:
        return ""
    lis = []
    for mv in moves:
        arrow = "&#9650;" if mv.get("dir") == "up" else ("&#9660;" if mv.get("dir") == "down" else "&#9644;")
        lis.append(
            f'<li style="margin:0 0 6px;"><a href="{mv["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(mv["market"])}</a> '
            f'<span style="color:#9a9a9a;">{arrow}</span> {esc(mv.get("detail",""))}</li>')
    return (
        f'<p style="margin:18px 0 4px; color:#1a1a1a; font-size:15px; font-family:{SERIF};">'
        f'<strong>Markets that swung this week:</strong></p>'
        f'<ul style="margin:0; padding:0 0 0 20px; font-size:15px; line-height:1.55; font-family:{SERIF}; color:#555;">{"".join(lis)}</ul>')


def _watch_next_html(issue):
    wn = issue.get("watch_next", [])
    if not wn:
        return ""
    rows = []
    for it in wn:
        rows.append(
            f'<tr><td style="padding:10px 0; border-bottom:1px solid #ededed; font-family:{SERIF};">'
            f'<span style="color:{ACCENT}; font-weight:700; font-size:15px;">{esc(it.get("when",""))}</span> '
            f'<span style="color:#1a1a1a; font-weight:700; font-size:15px;">{esc(it.get("event",""))}</span><br>'
            f'<span style="color:#555; font-size:15px; line-height:1.55;">{esc(it.get("note",""))}</span></td></tr>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">What to watch next week.</h2>
              <p style="margin:0 0 8px; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">The calendar ahead</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
            </td>
          </tr>
"""


def _radar_compact(r):
    b0 = (r.get("basket") or [None])[0]
    fact = f' {esc(b0["metric"])}: {esc(b0["value"])}.' if b0 else ""
    return (f'<p style="margin:7px 0 0; font-family:{SERIF}; font-size:15px; line-height:1.55; color:#555;">'
            f'<strong style="color:#1a1a1a;">{esc(r["name"])}</strong> '
            f'<span style="color:{ACCENT}; font-style:italic;">{esc(r.get("direction",""))}</span>.'
            f'{fact}</p>')


def _radar_html(issue):
    regs = issue.get("structural_regimes", [])
    if not regs:
        return ""
    blocks = []
    for r in [r for r in regs if r.get("spotlight")]:
        basket = "".join(
            f'<li style="margin:0 0 3px;">{esc(b["metric"])}: <strong>{esc(b["value"])}</strong>'
            + (f' <a href="{b["url"]}" style="color:{ACCENT}; text-decoration:underline;">source</a>' if b.get("url") else "")
            + '</li>' for b in r.get("basket", []))
        blocks.append(
            f'<div style="padding:16px 0; border-bottom:1px solid #ededed;">'
            f'<p style="margin:0 0 4px; font-family:{SERIF}; font-size:17px;">'
            f'<strong>{esc(r["name"])}</strong> '
            f'<span style="color:{ACCENT}; font-style:italic; font-size:15px;">{esc(r.get("direction",""))}</span></p>'
            f'<p style="margin:0 0 6px; font-family:{SERIF}; font-size:15px; line-height:1.6; color:#1a1a1a;">{esc(r["read"])}</p>'
            f'<ul style="margin:0; padding:0 0 0 20px; font-family:{SERIF}; font-size:13px; line-height:1.5; color:#666;">{basket}</ul>'
            f'</div>')
    steady = [r for r in regs if not r.get("spotlight")]
    if steady:
        blocks.append(
            f'<p style="margin:16px 0 0; color:#b3b3b3; font-size:13px; letter-spacing:1.5px; '
            f'text-transform:uppercase; font-family:{SERIF};">Holding steady</p>')
        blocks += [_radar_compact(r) for r in steady]
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">The structural picture.</h2>
              <p style="margin:0 0 8px; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">Regime radar &middot; read through markets and hard data</p>
              <p style="margin:0 0 6px; color:#555; font-size:15px; line-height:1.6; font-family:{SERIF};">The slow currents beneath the week. Each is read from a basket of dated, money-backed markets, not a single headline.</p>
              {''.join(blocks)}
            </td>
          </tr>
"""


def _market_html(m):
    rows = []
    for key, label in MKT_ORDER:
        sg = m.get("signals", {})
        if key not in sg:
            continue
        val = MKT_FMT.get(key, lambda v: v)(sg[key])
        color = MKT_COLOR[MKT_SENSE.get(key, "neutral")]
        rows.append(
            f'<tr><td style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; color:#666;">{label}</td>'
            f'<td align="right" style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; font-weight:700; color:{color};">{esc(val)}</td></tr>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">{esc(m.get("headline","Markets"))}</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">Markets</p>
              <p style="margin:0 0 16px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SERIF};">{esc(m.get("summary",""))}</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
              <p style="margin:16px 0 0; color:#555; font-size:15px; line-height:1.8; font-family:{SERIF};">{esc(MARKET_MEANS)}</p>
            </td>
          </tr>
"""


def _chg_mag(chg):
    try:
        return abs(float(chg.replace("%", "").replace("+", "")))
    except Exception:
        return 999.0


def _commodities_html(c):
    floor = c.get("min_change", 0)
    rows = []
    for it in c.get("items", []):
        chg = it.get("change", "")
        if _chg_mag(chg) < floor:          # only big movers
            continue
        color = "#b1300f" if chg.startswith("-") else "#1a7f4b"
        rows.append(
            f'<tr><td style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; color:#666;">{esc(it["name"])}</td>'
            f'<td align="right" style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; font-weight:700; color:#1a1a1a;">{esc(it.get("level",""))}</td>'
            f'<td align="right" style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; color:{color};">{esc(chg)}</td></tr>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">Crude falls as the fear premium unwinds.</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">Commodities &amp; energy &middot; {esc(c.get("as_of",""))}</p>
              <p style="margin:0 0 16px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SERIF};">{esc(c.get("summary",""))}</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
            </td>
          </tr>
"""


def _contrarian_html(issue):
    rows = []
    for key, r in issue.get("regimes", {}).items():
        if not r.get("contrarian"):
            continue
        label = DEFS.get(key, {}).get("label", key)
        rows.append(
            f'<tr><td style="padding:10px 0; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; line-height:1.6; color:#1a1a1a;">'
            f'<strong>{esc(label)}.</strong> {esc(r["contrarian"])}</td></tr>')
    if not rows:
        return ""
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:22px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">What could change this.</h2>
              <p style="margin:0 0 8px; color:{ACCENT}; font-size:15px; font-weight:600; font-family:{SERIF};">Contrarian read</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
            </td>
          </tr>
"""


def _across_inline(a):
    gh = a.get("github", [])
    if not gh:
        return ""
    items = " &middot; ".join(
        f'<a href="{r["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(r["title"])}</a>'
        for r in gh[:5])
    return f"""
          <tr>
            <td style="padding:16px 0 0;">
              <p style="margin:0; color:#555; font-size:15px; line-height:1.6; font-family:{SERIF};"><strong>On GitHub this week</strong>, trending is mostly {esc(a.get("github_theme",""))}: {items}</p>
            </td>
          </tr>
"""


def _act_html(title):
    return f"""
          <tr>
            <td style="padding:46px 0 0; text-align:center;">
              <p style="margin:0 0 8px; color:#1a1a1a; font-size:13px; letter-spacing:3px; text-transform:uppercase; font-weight:700; font-family:{SERIF};">{esc(title)}</p>
              <div style="border-top:2px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div>
            </td>
          </tr>
"""


def _lede_html():
    if not ISSUE.get("lede"):
        return ""
    return f"""
          <tr>
            <td style="padding:28px 0 0;">
              <p style="margin:0; color:#1a1a1a; font-size:17px; line-height:1.6; font-family:{SERIF};">{esc(ISSUE['lede'])}</p>
            </td>
          </tr>
"""


def _regime_section(key):
    r = ISSUE.get("regimes", {}).get(key)
    if not r:
        return ""
    return _section_html(DEFS.get(key, {}).get("label", key), r.get("headline", key),
                         r.get("summary", ""), r.get("links"), r.get("items"))


def build_html():
    reg = ISSUE.get("regimes", {})
    body = [_lede_html(), regime_engine.render_changed_html(STATE), _momentum_html(STATE)]

    # Act 1 — the tech world
    body.append(_act_html("The tech world"))
    body.append(_regime_section("tech_policy"))
    body.append(_regime_section("ai_agents"))
    if ISSUE.get("across_sources"):
        body.append(_across_inline(ISSUE["across_sources"]))   # GitHub note folded under agents
    body.append(regime_engine.render_watch_html(STATE))
    if ISSUE.get("undercurrent"):
        u = ISSUE["undercurrent"]
        body.append(_section_html(u.get("label", "Undercurrent"), u.get("headline", ""),
                                  u.get("summary", ""), u.get("links")))

    # Act 2 — the wider world
    body.append(_act_html("The wider world"))
    body.append(_regime_section("geopolitics"))
    if ISSUE.get("commodities"):
        body.append(_commodities_html(ISSUE["commodities"]))
    if "markets" in reg:
        body.append(_market_html(reg["markets"]))
    body.append(_radar_html(ISSUE))

    body.append(_watch_next_html(ISSUE))

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Current Regime &middot; {esc(ISSUE['id'])}</title>
</head>
<body style="margin:0; padding:0; background-color:#ffffff;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff;">
    <tr>
      <td align="center" style="padding:48px 20px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%;">
          <tr>
            <td style="text-align:center; padding-bottom:6px;">
              <h1 style="margin:0; color:#1a1a1a; font-size:32px; font-weight:700; letter-spacing:-0.5px; font-family:{SERIF};">The Current Regime</h1>
              <p style="margin:14px 0 0; color:#9a9a9a; font-size:13px; letter-spacing:2.5px; text-transform:uppercase; font-family:{SERIF};">Issue {esc(ISSUE['id'])} &middot; {esc(DATE_LABEL)}</p>
            </td>
          </tr>
          <tr><td style="padding:26px 0 0;"><div style="border-top:1px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div></td></tr>
          {''.join(body)}
          <tr><td style="padding:40px 0 0;"><div style="border-top:1px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div></td></tr>
          <tr>
            <td style="padding:20px 0 0;">
              <p style="margin:0; color:#1a1a1a; font-size:15px; line-height:1.7; font-style:italic; font-family:{SERIF};">Regimes change. Understanding the world within a changing context.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


# ---------- plain text ----------

def _links_text(links):
    return "".join(f"- {l['title']}: {l['url']}\n" for l in (links or []))


def _items_text(items):
    out = []
    for it in (items or []):
        out.append(f"- {it['title']}: {it['url']}")
        if it.get("comment"):
            out.append(f"    {it['comment']}")
    return "\n".join(out)


def build_plain():
    reg = ISSUE.get("regimes", {})
    out = ["THE CURRENT REGIME", f"Issue {ISSUE['id']} · {DATE_LABEL}",
           "Sourced from the week's top posts on news.ycombinator.com, with claims",
           "verified against primary reporting, and a market-regime read.", "",
           "-" * 74, ""]
    if ISSUE.get("lede"):
        out += [ISSUE["lede"], "", "-" * 74, ""]
    m = ISSUE.get("momentum")
    if m:
        ser = m["series"]
        out += [f"WHERE ATTENTION WENT (regime momentum, {m['weeks'][0]} vs {m['weeks'][-1]}):", ""]
        covered = set(ISSUE.get("regimes", {})) - {"markets"}
        for k in sorted(ser, key=lambda k: -ser[k][-1]):
            if k not in covered:
                continue
            cur = ser[k][-1]
            prev = ser[k][-2] if len(ser[k]) > 1 else cur
            if cur == 0 and prev == 0:
                continue
            arrow = "up" if cur > prev else ("down" if cur < prev else "flat")
            st = ISSUE.get("regimes", {}).get(k, {}).get("state")
            tail = f", week {regime_engine.weeks_in_state(STATE, k)} in {st}" if st else ""
            out.append(f"  {DEFS.get(k, {}).get('label', k)}: {prev} -> {cur} ({arrow}){tail}")
        out.append("")
        if ISSUE.get("market_moves"):
            out.append("  Markets that swung this week:")
            for mv in ISSUE["market_moves"]:
                dd = {"up": "up", "down": "down"}.get(mv.get("dir"), "flat")
                out.append(f"    - {mv['market']} ({dd}): {mv.get('detail','')}  {mv['url']}")
            out.append("")
    for key, r in reg.items():
        if key == "markets":
            continue
        label = DEFS.get(key, {}).get("label", key).upper()
        refs = _items_text(r.get("items")) or _links_text(r.get("links")).rstrip()
        out += [f"{label}: {r.get('headline','')}", "", r.get("summary", ""), "", refs, ""]
    if ISSUE.get("commodities"):
        c = ISSUE["commodities"]
        out += [f"COMMODITIES & ENERGY ({c.get('as_of','')})", "", c.get("summary", ""), ""]
        for it in c["items"]:
            if _chg_mag(it.get("change", "")) < c.get("min_change", 0):
                continue
            out.append(f"  {it['name']}: {it.get('level','')} ({it.get('change','')})")
        out.append("")
    if "markets" in reg:
        m = reg["markets"]
        sig = m.get("signals", {})
        out += [f"MARKETS: {m.get('headline','')}", "", m.get("summary", ""), "",
                "  " + ", ".join(f"{lbl} {sig[k]}" for k, lbl in MKT_ORDER if k in sig),
                "", MARKET_MEANS, ""]
    if ISSUE.get("undercurrent"):
        u = ISSUE["undercurrent"]
        out += [f"UNDERCURRENT: {u.get('headline','')}", "", u.get("summary", ""), "",
                _links_text(u.get("links")).rstrip(), ""]
    if ISSUE.get("structural_regimes"):
        regs = ISSUE["structural_regimes"]
        out += ["THE STRUCTURAL PICTURE (regime radar, read through markets and hard data):", ""]
        for r in [r for r in regs if r.get("spotlight")]:
            out.append(f"  {r['name']} [{r.get('direction','')}]")
            out.append(f"    {r['read']}")
            for b in r.get("basket", []):
                u = f"  {b['url']}" if b.get("url") else ""
                out.append(f"    - {b['metric']}: {b['value']}{u}")
            out.append("")
        steady = [r for r in regs if not r.get("spotlight")]
        if steady:
            out.append("  Holding steady:")
            for r in steady:
                b0 = (r.get("basket") or [None])[0]
                fact = f" {b0['metric']}: {b0['value']}." if b0 else ""
                out.append(f"    - {r['name']} ({r.get('direction','')}).{fact}")
            out.append("")
    if ISSUE.get("watch_next"):
        out += ["WHAT TO WATCH NEXT WEEK:", ""]
        for it in ISSUE["watch_next"]:
            out.append(f"  {it.get('when','')} - {it.get('event','')}: {it.get('note','')}")
        out.append("")
    out += [regime_engine.render_text(STATE), ""]
    if ISSUE.get("across_sources"):
        a = ISSUE["across_sources"]
        if a.get("github"):
            out += ["ACROSS THE SOURCES", "",
                    f"GitHub trending shows {a.get('github_theme','')}: "
                    + ", ".join(r["title"] for r in a["github"][:5]), ""]
    out += ["-" * 74, "Regimes change. Understanding the world within a changing context."]
    return "\n".join(out)


def main() -> int:
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print("ERROR: set GMAIL_APP_PASSWORD first.", file=sys.stderr)
        return 1

    recipients = load_subscribers()
    dry = "--dry-run" in sys.argv
    only_me = "--test" in sys.argv
    if only_me:
        recipients = [SENDER]

    msg = EmailMessage()
    msg["From"] = f"The Current Regime <{SENDER}>"
    msg["To"] = SENDER                       # list goes out via to_addrs, not headers
    msg["Subject"] = SUBJECT
    # one-click unsubscribe (a reply that signups.py will process)
    msg["List-Unsubscribe"] = f"<mailto:{SENDER}?subject=unsubscribe>"
    msg.set_content(build_plain())
    msg.add_alternative(build_html(), subtype="html")

    if dry:
        print(f"[dry-run] would send '{SUBJECT}' to {len(recipients)} recipient(s)")
        return 0

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, app_password)
        server.send_message(msg, from_addr=SENDER, to_addrs=recipients)

    print(f"Sent '{SUBJECT}' to {len(recipients)} recipient(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
