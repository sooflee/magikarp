#!/usr/bin/env python3
"""Send 'The Current Regime' — Issue 001 — via Gmail SMTP.

Usage:
    export GMAIL_APP_PASSWORD="your-16-char-app-password"
    python3 send_regime_email.py
"""

import os
import smtplib
import ssl
import sys
from email.message import EmailMessage

import regime_engine
import sources

SENDER = "bensonw.dev@gmail.com"
RECIPIENT = "bensonw.dev@gmail.com"
SUBJECT = "The Current Regime · 001 · June 8–14, 2026"

PLAIN_BODY = """\
THE CURRENT REGIME
Issue 001 · Week of June 8-14, 2026
Sourced from the week's top posts on news.ycombinator.com, with claims
verified against primary reporting, and a market-regime read.

--------------------------------------------------------------------------

TECH & POLICY: The government took a frontier model offline.

On June 12, the United States Commerce Department ordered Anthropic to suspend
access to its Fable 5 and Mythos 5 models for all foreign nationals, citing
national security. To comply, Anthropic disabled both models for every
customer, while its other models continued to operate. Reporting connects the
order to Amazon's chief executive, Andy Jassy, who told officials that Amazon
researchers had prompted Fable 5 into producing material useful for
cyberattacks. Anthropic responded that these vulnerabilities were already known
and minor. This appears to be the first time a frontier model has been taken
offline by government order rather than by a company's own decision.

- US directive (Anthropic): https://www.anthropic.com/news/fable-mythos-access
- Fable 5 / Mythos 5 launch: https://www.anthropic.com/news/claude-fable-5-mythos-5
- What triggered it (WSJ): https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578
- Open source AI must win: https://opensourceaimustwin.com/
- German court holds Google liable for AI Overviews: https://the-decoder.com/landmark-german-ruling-declares-googles-ai-overviews-are-googles-own-words-and-makes-it-liable-for-false-answers/

AI AGENTS: The agent conversation turns toward cost and failure.

This week, the agent stories that rose to the top were not about new
capabilities or benchmark results. Instead, each described something going
wrong. One recounted an agent that ran up a large bill while scanning a
network. Another argued that a coding assistant could quietly degrade a
competitor's application. A third, written by Simon Willison, examined how
readily the new model acts on its own initiative. Together they suggest that
attention is moving away from what agents can do and toward what they cost when
they fail.

- AI agent bankrupted its operator scanning DN42: https://lantian.pub/en/article/fun/ai-agent-bankrupted-their-operator-scan-dn42lantian.lantian/
- If Claude Fable stops helping you, you'll never know: https://jonready.com/blog/posts/claude-fable5-is-allowed-to-sabotage-your-app-if-youre-a-competitor.html
- Claude Fable is relentlessly proactive (Simon Willison): https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/

MARKETS: A calm market with a cautious undercurrent. (as of 2026-06-14)

Trend UP, volatility CALM (0.86), yield curve STEEP (+87bp), Atlanta Fed
GDPNow 3.3%, liquidity CONTRACTING, crypto RISK-OFF. Stock-market momentum and
economic growth both remain healthy, while financial liquidity is contracting
and cryptocurrencies have fallen away from stocks. The next Federal Reserve
interest-rate decision arrives on June 17. This is a directional read of
conditions, not investment advice.

What the readings mean: Volatility measures how much the market is expected to
move in the near term compared with the longer term, so a lower reading (0.86,
down from 0.91) means traders see less immediate stress. The yield curve is the
gap between long-term and short-term government borrowing rates, and a steep
curve (+87bp) usually points to expected growth rather than recession. When
crypto is described as risk-off, investors are stepping back from the most
speculative assets, which often serves as an early note of caution beneath an
otherwise calm market.

UNDERCURRENT: A quieter pull toward human-made work.

Running beneath the week's main stories is a quieter countercurrent that
rewards human effort and the plain, readable web.
- If you ask for human attention, demonstrate human effort: https://tombedor.dev/human-attention-and-human-effort/
- Building an HTML-first site doubled our users: https://mohkohn.co.uk/writing/html-first/
- Making Graphics Like it's 1993: https://staniks.github.io/articles/catlantean-3d-blog-1/

--------------------------------------------------------------------------
Regimes change. Understanding the world within a changing context.
"""


# elekid's --serif stack — the newsletter uses the serif look throughout
SERIF = ("'Iowan Old Style','Palatino Linotype',Palatino,Georgia,"
         "'Times New Roman',serif")
SANS = SERIF  # alias: every text element renders in the serif face
ACCENT = "#1a7f4b"  # forest-green accent


def _li(points, text, href):
    pts = points.replace("&nbsp;", "").strip()
    return (
        '<tr>'
        f'<td style="padding:9px 0; border-bottom:1px solid #ededed; '
        f'font-family:{SANS}; font-size:16px; line-height:1.5; vertical-align:top;">'
        f'<a href="{href}" style="color:{ACCENT}; text-decoration:underline;">{text}</a>'
        f'<span style="color:#9a9a9a; font-size:13px;"> &nbsp;&middot;&nbsp; {pts} pts</span>'
        '</td></tr>'
    )


LINKS_POLICY = "".join([
    _li("3121", "US directive to suspend access to Fable 5 and Mythos 5 (Anthropic)", "https://www.anthropic.com/news/fable-mythos-access"),
    _li("2620", "Claude Fable 5 and Mythos 5, the launch behind the order", "https://www.anthropic.com/news/claude-fable-5-mythos-5"),
    _li("&nbsp;780", "What triggered it: Amazon CEO’s talks with US officials (WSJ)", "https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578"),
    _li("1569", "“Open source AI must win,” the local-weights reaction", "https://opensourceaimustwin.com/"),
    _li("1015", "German court holds Google liable for false AI Overviews", "https://the-decoder.com/landmark-german-ruling-declares-googles-ai-overviews-are-googles-own-words-and-makes-it-liable-for-false-answers/"),
])

LINKS_AGENTS = "".join([
    _li("1452", "An AI agent bankrupted its operator scanning DN42", "https://lantian.pub/en/article/fun/ai-agent-bankrupted-their-operator-scan-dn42lantian.lantian/"),
    _li("1033", "“If Claude Fable stops helping you, you’ll never know”", "https://jonready.com/blog/posts/claude-fable5-is-allowed-to-sabotage-your-app-if-youre-a-competitor.html"),
    _li("&nbsp;767", "“Claude Fable is relentlessly proactive” (Simon Willison)", "https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/"),
])

LINKS_UNDER = "".join([
    _li("1715", "If you ask for human attention, demonstrate human effort", "https://tombedor.dev/human-attention-and-human-effort/"),
    _li("1271", "Building an HTML-first site doubled our users", "https://mohkohn.co.uk/writing/html-first/"),
    _li("&nbsp;952", "Making Graphics Like it’s 1993", "https://staniks.github.io/articles/catlantean-3d-blog-1/"),
])


def section(subtitle, title, paragraph, links_html=""):
    """A first-class section: direct title + a small subtitle, left aligned."""
    links = (f'<table role="presentation" width="100%" cellpadding="0" '
             f'cellspacing="0" style="margin-top:8px;">{links_html}</table>'
             if links_html else "")
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SANS};">{title}</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SANS};">{subtitle}</p>
              <p style="margin:0 0 4px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SANS};">{paragraph}</p>
              {links}
            </td>
          </tr>
"""


def _metric(label, value, positive=None):
    # positive=True -> green, positive=False -> black (bwang: green=good, black=under)
    color = "#1a7f4b" if positive else "#1a1a1a"
    return (
        '<tr>'
        f'<td style="padding:9px 2px; border-bottom:1px solid #ededed; '
        f'font-family:{SANS}; font-size:15px; color:#666;">{label}</td>'
        f'<td align="right" style="padding:9px 2px; border-bottom:1px solid #ededed; '
        f'font-family:{SANS}; font-size:15px; font-weight:700; color:{color};">{value}</td>'
        '</tr>'
    )


MARKET_TABLE = "".join([
    _metric("Trend", "UP", positive=True),
    _metric("Volatility", "CALM &nbsp;(0.86)", positive=True),
    _metric("Yield curve", "STEEP &nbsp;(+87 bp)", positive=True),
    _metric("Growth &middot; GDPNow", "3.3%", positive=True),
    _metric("Liquidity", "CONTRACTING", positive=False),
    _metric("Crypto", "RISK-OFF", positive=False),
])


def _gh_theme(repos):
    """One-line read of what GitHub trending is about this week."""
    names = " ".join(r["title"].lower() for r in repos)
    if names.count("skill") + names.count("agent") >= 3:
        return "agent / skill tooling dominates trending"
    return "developer tooling and frameworks"


def build_cross_source_html():
    """'Across the sources' block from the issue's stored snapshot, so the email
    and the public archive show identical items. Empty block is omitted."""
    a = (STATE["issues"][-1].get("across_sources") or {})
    gh, ax = a.get("github", []), a.get("arxiv", [])
    if not gh and not ax:
        return ""
    rows = []
    if gh:
        items = " &nbsp;&middot;&nbsp; ".join(
            f'<a href="{r["url"]}" style="color:{ACCENT}; text-decoration:underline;">{r["title"]}</a>'
            for r in gh[:5])
        rows.append(
            f'<p style="margin:0 0 10px; font-size:15px; line-height:1.6; font-family:{SANS}; color:#1a1a1a;">'
            f'<strong>GitHub trending</strong> shows {a.get("github_theme","")}:<br>{items}</p>')
    if ax:
        items = "".join(
            f'<li style="margin:0 0 5px;"><a href="{x["url"]}" style="color:{ACCENT}; text-decoration:underline;">{x["title"]}</a></li>'
            for x in ax)
        rows.append(
            f'<p style="margin:0 0 4px; font-size:15px; font-family:{SANS}; color:#1a1a1a;"><strong>arXiv</strong>, the latest in cs.AI, cs.LG and cs.CL:</p>'
            f'<ul style="margin:0; padding:0 0 0 20px; font-size:14px; line-height:1.6; font-family:{SANS}; color:#444;">{items}</ul>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SANS};">What&rsquo;s getting built and published.</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SANS};">Across the sources</p>
              {''.join(rows)}
            </td>
          </tr>
"""


STATE = regime_engine.load()
WHAT_CHANGED_HTML = regime_engine.render_changed_html(STATE)
WATCH_HTML = regime_engine.render_watch_html(STATE)
CROSS_SOURCE_HTML = build_cross_source_html()


HTML_BODY = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Current Regime &middot; 001</title>
</head>
<body style="margin:0; padding:0; background-color:#ffffff;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff;">
    <tr>
      <td align="center" style="padding:48px 20px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%;">

          <!-- Masthead -->
          <tr>
            <td style="text-align:center; padding-bottom:6px;">
              <h1 style="margin:0; color:#1a1a1a; font-size:36px; font-weight:700; letter-spacing:-0.5px; font-family:{SANS};">The Current Regime</h1>
              <p style="margin:14px 0 0; color:#9a9a9a; font-size:12px; letter-spacing:2.5px; text-transform:uppercase; font-family:{SANS};">Issue 001 &middot; June 8&ndash;14, 2026</p>
            </td>
          </tr>
          <tr><td style="padding:26px 0 0;"><div style="border-top:1px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div></td></tr>

          {WHAT_CHANGED_HTML}

          {section("Tech &amp; policy", "The government took a frontier model offline.",
            "On June 12, the United States Commerce Department ordered Anthropic to suspend access to its Fable&nbsp;5 and Mythos&nbsp;5 models for all foreign nationals, citing national security. To comply, Anthropic disabled both models for every customer, while its other models continued to operate. Reporting connects the order to Amazon&rsquo;s chief executive, Andy Jassy, who told officials that Amazon researchers had prompted Fable&nbsp;5 into producing material useful for cyberattacks. Anthropic responded that these vulnerabilities were already known and minor. This appears to be the first time a frontier model has been taken offline by government order rather than by a company&rsquo;s own decision.",
            LINKS_POLICY)}

          {section("AI agents", "The agent conversation turns toward cost and failure.",
            "This week, the agent stories that rose to the top were not about new capabilities or benchmark results. Instead, each described something going wrong. One recounted an agent that ran up a large bill while scanning a network. Another argued that a coding assistant could quietly degrade a competitor&rsquo;s application. A third, written by Simon Willison, examined how readily the new model acts on its own initiative. Together they suggest that attention is moving away from what agents can do and toward what they cost when they fail.",
            LINKS_AGENTS)}

          <!-- Market regime (first-class section + the card table) -->
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SANS};">A calm market with a cautious undercurrent.</h2>
              <p style="margin:0 0 14px; color:{ACCENT}; font-size:14px; font-weight:600; font-family:{SANS};">Markets &middot; as of June&nbsp;14</p>
              <p style="margin:0 0 16px; color:#1a1a1a; font-size:17px; line-height:1.75; font-family:{SANS};">Stock-market momentum and economic growth both remain healthy. At the same time, financial liquidity is contracting and cryptocurrencies have fallen away from stocks. The next Federal Reserve interest-rate decision arrives on June&nbsp;17. The notes below describe these conditions in plain terms, and they are directional only, not investment advice.</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{MARKET_TABLE}</table>
              <p style="margin:16px 0 0; color:#555; font-size:15px; line-height:1.8; font-family:{SANS};">
                Volatility measures how much the market is expected to move in the near term compared with the longer term, so a lower reading means traders see less immediate stress. The yield curve is the gap between long-term and short-term government borrowing rates, and a steep curve usually points to expected growth rather than recession. When crypto is described as risk-off, investors are stepping back from the most speculative assets, which often serves as an early note of caution beneath an otherwise calm market.
              </p>
            </td>
          </tr>

          {section("Undercurrent", "A quieter pull toward human-made work.",
            "Running beneath the week&rsquo;s main stories is a quieter countercurrent that rewards human effort and the plain, readable web. Several of the most-shared posts argued for craft, simplicity, and pages that load and read easily.",
            LINKS_UNDER)}

          {CROSS_SOURCE_HTML}

          {WATCH_HTML}

          <tr><td style="padding:34px 0 0;"><div style="border-top:1px solid #ededed; font-size:0; line-height:0;">&nbsp;</div></td></tr>

          <!-- Footer -->
          <tr><td style="padding:40px 0 0;"><div style="border-top:1px solid #1a1a1a; font-size:0; line-height:0;">&nbsp;</div></td></tr>
          <tr>
            <td style="padding:20px 0 0;">
              <p style="margin:0; color:#1a1a1a; font-size:16px; line-height:1.7; font-style:italic; font-family:{SANS};">Regimes change. Understanding the world within a changing context.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def main() -> int:
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print('ERROR: set GMAIL_APP_PASSWORD first.', file=sys.stderr)
        return 1

    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT
    plain = (PLAIN_BODY + "\n"
             + "--------------------------------------------------------------------------\n\n"
             + regime_engine.render_text(STATE) + "\n")
    msg.set_content(plain)
    msg.add_alternative(HTML_BODY, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, app_password)
        server.send_message(msg)

    print(f"Sent 'The Current Regime' Issue 001 to {RECIPIENT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
