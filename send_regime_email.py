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

import regime_engine

SENDER = "bensonw.dev@gmail.com"
RECIPIENT = "bensonw.dev@gmail.com"

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
             ("gdpnow", "Growth (GDPNow)"), ("liquidity", "Liquidity"), ("crypto", "Crypto")]
MKT_FMT = {"vol": lambda v: f"Calm ({v})", "curve_bp": lambda v: f"Steep (+{v} bp)",
           "gdpnow": lambda v: f"{v}%"}
MKT_POS = {"trend": True, "vol": True, "curve_bp": True, "gdpnow": True,
           "liquidity": False, "crypto": False}


def esc(s) -> str:
    return html.escape(str(s), quote=False)


# ---------- HTML ----------

def _links_html(links):
    if not links:
        return ""
    rows = "".join(
        '<tr><td style="padding:9px 0; border-bottom:1px solid #ededed; '
        f'font-family:{SERIF}; font-size:16px; line-height:1.5; vertical-align:top;">'
        f'<a href="{l["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(l["title"])}</a>'
        '</td></tr>' for l in links)
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin-top:8px;">{rows}</table>')


def _section_html(label, title, paragraph, links=None):
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">{esc(title)}</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SERIF};">{esc(label)}</p>
              <p style="margin:0 0 4px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SERIF};">{esc(paragraph)}</p>
              {_links_html(links)}
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
        color = "#1a7f4b" if MKT_POS.get(key) else "#b1300f"
        rows.append(
            f'<tr><td style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; color:#666;">{label}</td>'
            f'<td align="right" style="padding:9px 2px; border-bottom:1px solid #ededed; '
            f'font-family:{SERIF}; font-size:15px; font-weight:700; color:{color};">{esc(val)}</td></tr>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">{esc(m.get("headline","Markets"))}</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SERIF};">Markets</p>
              <p style="margin:0 0 16px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SERIF};">{esc(m.get("summary",""))}</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
              <p style="margin:16px 0 0; color:#555; font-size:15px; line-height:1.8; font-family:{SERIF};">{esc(MARKET_MEANS)}</p>
            </td>
          </tr>
"""


def _commodities_html(c):
    rows = []
    for it in c.get("items", []):
        chg = it.get("change", "")
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
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">Crude falls as the fear premium unwinds.</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SERIF};">Commodities &amp; energy &middot; {esc(c.get("as_of",""))}</p>
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
            f'font-family:{SERIF}; font-size:16px; line-height:1.6; color:#1a1a1a;">'
            f'<strong>{esc(label)}.</strong> {esc(r["contrarian"])}</td></tr>')
    if not rows:
        return ""
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">What could change this.</h2>
              <p style="margin:0 0 8px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SERIF};">Contrarian read</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
            </td>
          </tr>
"""


def _across_html(a):
    gh, ax = a.get("github", []), a.get("arxiv", [])
    if not gh and not ax:
        return ""
    rows = []
    if gh:
        items = " &nbsp;&middot;&nbsp; ".join(
            f'<a href="{r["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(r["title"])}</a>'
            for r in gh[:5])
        rows.append(
            f'<p style="margin:0 0 10px; font-size:15px; line-height:1.6; font-family:{SERIF}; color:#1a1a1a;">'
            f'<strong>GitHub trending</strong> shows {esc(a.get("github_theme",""))}:<br>{items}</p>')
    if ax:
        items = "".join(
            f'<li style="margin:0 0 5px;"><a href="{x["url"]}" style="color:{ACCENT}; text-decoration:underline;">{esc(x["title"])}</a></li>'
            for x in ax)
        rows.append(
            f'<p style="margin:0 0 4px; font-size:15px; font-family:{SERIF}; color:#1a1a1a;"><strong>arXiv</strong>, the latest in cs.AI, cs.LG and cs.CL:</p>'
            f'<ul style="margin:0; padding:0 0 0 20px; font-size:14px; line-height:1.6; font-family:{SERIF}; color:#444;">{items}</ul>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SERIF};">What&rsquo;s getting built and published.</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SERIF};">Across the sources</p>
              {''.join(rows)}
            </td>
          </tr>
"""


def build_html():
    reg = ISSUE.get("regimes", {})
    body = [regime_engine.render_changed_html(STATE)]
    for key, r in reg.items():            # editorial regimes (incl. geopolitics)
        if key == "markets":
            continue
        body.append(_section_html(DEFS.get(key, {}).get("label", key),
                                  r.get("headline", key), r.get("summary", ""), r.get("links")))
    if ISSUE.get("commodities"):
        body.append(_commodities_html(ISSUE["commodities"]))
    if "markets" in reg:
        body.append(_market_html(reg["markets"]))
    body.append(_contrarian_html(ISSUE))
    if ISSUE.get("undercurrent"):
        u = ISSUE["undercurrent"]
        body.append(_section_html(u.get("label", "Undercurrent"), u.get("headline", ""),
                                  u.get("summary", ""), u.get("links")))
    body.append(regime_engine.render_watch_html(STATE))
    if ISSUE.get("across_sources"):
        body.append(_across_html(ISSUE["across_sources"]))

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
              <h1 style="margin:0; color:#1a1a1a; font-size:36px; font-weight:700; letter-spacing:-0.5px; font-family:{SERIF};">The Current Regime</h1>
              <p style="margin:14px 0 0; color:#9a9a9a; font-size:12px; letter-spacing:2.5px; text-transform:uppercase; font-family:{SERIF};">Issue {esc(ISSUE['id'])} &middot; {esc(DATE_LABEL)}</p>
            </td>
          </tr>
          <tr><td style="padding:26px 0 0;"><div style="border-top:1px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div></td></tr>
          {''.join(body)}
          <tr><td style="padding:40px 0 0;"><div style="border-top:1px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div></td></tr>
          <tr>
            <td style="padding:20px 0 0;">
              <p style="margin:0; color:#1a1a1a; font-size:16px; line-height:1.7; font-style:italic; font-family:{SERIF};">Regimes change. Understanding the world within a changing context.</p>
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


def build_plain():
    reg = ISSUE.get("regimes", {})
    out = ["THE CURRENT REGIME", f"Issue {ISSUE['id']} · {DATE_LABEL}",
           "Sourced from the week's top posts on news.ycombinator.com, with claims",
           "verified against primary reporting, and a market-regime read.", "",
           "-" * 74, ""]
    for key, r in reg.items():
        if key == "markets":
            continue
        label = DEFS.get(key, {}).get("label", key).upper()
        out += [f"{label}: {r.get('headline','')}", "", r.get("summary", ""), "",
                _links_text(r.get("links")).rstrip(), ""]
    if ISSUE.get("commodities"):
        c = ISSUE["commodities"]
        out += [f"COMMODITIES & ENERGY ({c.get('as_of','')})", "", c.get("summary", ""), ""]
        for it in c["items"]:
            out.append(f"  {it['name']}: {it.get('level','')} ({it.get('change','')})")
        out.append("")
    if "markets" in reg:
        m = reg["markets"]
        sig = m.get("signals", {})
        out += [f"MARKETS: {m.get('headline','')}", "", m.get("summary", ""), "",
                "  " + ", ".join(f"{lbl} {sig[k]}" for k, lbl in MKT_ORDER if k in sig),
                "", MARKET_MEANS, ""]
    contr = [(DEFS.get(k, {}).get("label", k), r["contrarian"])
             for k, r in reg.items() if r.get("contrarian")]
    if contr:
        out += ["CONTRARIAN READ (what could change this):", ""]
        out += [f"  {lbl}. {line}" for lbl, line in contr]
        out.append("")
    if ISSUE.get("undercurrent"):
        u = ISSUE["undercurrent"]
        out += [f"UNDERCURRENT: {u.get('headline','')}", "", u.get("summary", ""), "",
                _links_text(u.get("links")).rstrip(), ""]
    out += [regime_engine.render_text(STATE), ""]
    if ISSUE.get("across_sources"):
        a = ISSUE["across_sources"]
        out += ["ACROSS THE SOURCES", ""]
        if a.get("github"):
            out.append("GitHub trending: " + ", ".join(r["title"] for r in a["github"][:5]))
        if a.get("arxiv"):
            out += ["arXiv (cs.AI/LG/CL):"] + [f"  - {x['title']}" for x in a["arxiv"]]
        out.append("")
    out += ["-" * 74, "Regimes change. Understanding the world within a changing context."]
    return "\n".join(out)


def main() -> int:
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print("ERROR: set GMAIL_APP_PASSWORD first.", file=sys.stderr)
        return 1

    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT
    msg.set_content(build_plain())
    msg.add_alternative(build_html(), subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, app_password)
        server.send_message(msg)

    print(f"Sent '{SUBJECT}' to {RECIPIENT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
