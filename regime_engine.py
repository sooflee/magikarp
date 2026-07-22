#!/usr/bin/env python3
"""Structured regime state + week-over-week diff for 'The Current Regime'.

The newsletter's premise is that regimes change. This turns that from prose into
data: each issue stores a state per regime in regime_state.json, and this module
computes what moved since the previous issue — the "What changed" block.

CLI:
    python3 regime_engine.py            # print the latest diff + bsig watchlist
    python3 regime_engine.py --html     # emit the HTML blocks used by the email
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parent / "regime_state.json"

# elekid's --serif stack — the newsletter uses the serif look throughout
SERIF = ("'Iowan Old Style','Palatino Linotype',Palatino,Georgia,"
         "'Times New Roman',serif")
SANS = SERIF  # alias: every text element renders in the serif face


# A renamed lane inherits its predecessor's history so week-over-week continuity
# survives the rename. ai_compute (issue 06+) continues the former tech_policy lane;
# both share the open-acceleration / consolidation / state-capture state space.
LANE_ALIASES = {"ai_compute": "tech_policy"}


def _regime_at(iss: dict, key: str):
    """The regime dict for `key` in an issue, falling back to a predecessor lane."""
    regs = iss.get("regimes", {})
    if key in regs:
        return regs[key]
    alias = LANE_ALIASES.get(key)
    return regs.get(alias) if alias else None


def load() -> dict:
    return json.loads(STATE.read_text())


def latest_issue(state: dict) -> dict:
    return [i for i in state["issues"] if not i.get("partial")][-1]


# News-outlet hosts where a bare homepage link can only be a placeholder: a real
# citation to these always has an article path.
_NEWS_HOSTS = {
    "www.aljazeera.com", "aljazeera.com", "www.statnews.com", "statnews.com",
    "www.techmeme.com", "techmeme.com", "www.reuters.com", "reuters.com",
    "www.bloomberg.com", "bloomberg.com", "www.cnbc.com", "cnbc.com",
    "www.nytimes.com", "nytimes.com", "www.wsj.com", "wsj.com",
    "www.ft.com", "ft.com", "polymarket.com", "www.polymarket.com",
    "news.ycombinator.com", "www.theregister.com", "arstechnica.com",
    "www.wired.com", "techcrunch.com", "www.engadget.com",
}


def lint_issue(iss: dict) -> list[str]:
    """Catch placeholder links before an issue can render or send.

    An unverified draft looks plausible but links wrong: invented round-numbered
    HN item ids, bare news-outlet homepages, one URL reused for several stories.
    """
    import re
    from urllib.parse import urlsplit

    problems: list[str] = []
    seen: dict[str, set[str]] = {}

    def walk(node, title=""):
        if isinstance(node, dict):
            t = node.get("title") or node.get("metric") or title
            for v in node.values():
                walk(v, t)
        elif isinstance(node, list):
            for v in node:
                walk(v, title)
        elif isinstance(node, str) and node.startswith("http"):
            seen.setdefault(node, set()).add(title)
            parts = urlsplit(node)
            if parts.path in ("", "/") and not parts.query:
                if parts.netloc in _NEWS_HOSTS:
                    problems.append(f"placeholder homepage link: {node} ({title!r})")
                else:
                    print(f"[lint] warning: homepage-only link {node} ({title!r})",
                          file=sys.stderr)
            m = re.match(r"https?://news\.ycombinator\.com/item\?id=(\d+)$", node)
            if m and int(m.group(1)) % 1000 == 0:
                problems.append(f"suspicious round HN item id: {node} ({title!r})")

    walk(iss)
    for url, titles in seen.items():
        if len(titles) > 1:
            problems.append(
                f"one URL cited for {len(titles)} different items: {url} {sorted(titles)}")
    return problems


def lint_or_die(iss: dict) -> None:
    problems = lint_issue(iss)
    if problems:
        print(f"LINT: issue {iss.get('id')} has placeholder-style links; "
              "replace them with URLs actually fetched during verification:",
              file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)


def momentum(state: dict):
    return latest_issue(state).get("momentum")


def weeks_in_state(state: dict, key: str) -> int:
    issues = [i for i in state["issues"] if _regime_at(i, key)]
    if not issues:
        return 0
    cur = _regime_at(issues[-1], key).get("state")
    n = 0
    for iss in reversed(issues):
        if _regime_at(iss, key).get("state") == cur:
            n += 1
        else:
            break
    return n


def trajectory_line(state: dict, key: str):
    """Compact 'Rising · week N in <state>' line for a regime, or None."""
    m = momentum(state)
    if not m or key not in m.get("series", {}):
        return None
    ser = m["series"][key]
    if len(ser) < 2:
        return None
    prev, cur = ser[-2], ser[-1]
    direction = "Rising" if cur > prev else ("Cooling" if cur < prev else "Steady")
    st = latest_issue(state)["regimes"].get(key, {}).get("state", "")
    n = weeks_in_state(state, key)
    return f"{direction} · week {n} in {st}" if st else direction


def _issue(state: dict, idx: int) -> dict | None:
    issues = state.get("issues", [])
    return issues[idx] if -len(issues) <= idx < len(issues) else None


def _market_signal_deltas(prev: dict, cur: dict) -> list[str]:
    ps = (prev or {}).get("signals", {})
    cs = (cur or {}).get("signals", {})
    out = []
    if "vol" in ps and "vol" in cs and ps["vol"] != cs["vol"]:
        out.append(f"volatility {ps['vol']} -> {cs['vol']}")
    if "curve_bp" in ps and "curve_bp" in cs and ps["curve_bp"] != cs["curve_bp"]:
        out.append(f"curve +{ps['curve_bp']}bp -> +{cs['curve_bp']}bp")
    for k in ("trend", "liquidity", "crypto"):
        if ps.get(k) and cs.get(k) and ps[k] != cs[k]:
            out.append(f"{k} {ps[k]} -> {cs[k]}")
    return out


def diff(state: dict, prev_idx: int = -2, cur_idx: int = -1) -> dict:
    prev, cur = _issue(state, prev_idx), _issue(state, cur_idx)
    defs = state["regime_defs"]
    changes, new, steady = [], [], []
    pr = (prev or {}).get("regimes", {})
    cr = (cur or {}).get("regimes", {})
    for key in defs:
        if key == "deep_dive":          # rotating domain lane: not comparable week to week
            continue
        cc = cr.get(key)
        if cc is None:
            continue
        # a renamed lane inherits its predecessor's prior state (tech_policy -> ai_compute)
        pc = pr.get(key) or (pr.get(LANE_ALIASES[key]) if key in LANE_ALIASES else None)
        label = defs[key]["label"]
        if pc is None:
            new.append((key, label, cc.get("state"), cc.get("headline", "")))
        elif pc.get("state") != cc.get("state"):
            changes.append((key, label, pc.get("state"), cc.get("state")))
        else:
            sig = _market_signal_deltas(pc, cc) if key == "markets" else []
            steady.append((key, label, cc.get("state"), sig))
    return {"prev": prev, "cur": cur, "changed": changes, "new": new, "steady": steady}


def changed_items(state: dict, prev_idx: int = -2, cur_idx: int = -1) -> list:
    """Trimmed week-over-week changes (no implication paragraphs), folded into the
    'Where the week's attention went' section. Each item is (label, oneliner).
    Returns [] when the prior issue is the partial baseline."""
    d = diff(state, prev_idx, cur_idx)
    if not d["prev"] or d["prev"].get("partial"):
        return []
    out = []
    for _key, label, a, b in d["changed"]:
        out.append((label, f"{a} -> {b}"))
    for _key, label, _st, sig in d["steady"]:
        if sig:
            out.append((label, ", ".join(sig)))
    for _key, label, _st, head in d["new"]:
        out.append((label, head))
    return out


# ---- text ----

def render_text(state: dict) -> str:
    """Watchlist block only. The week-over-week change list is folded into the
    attention section by the issue renderers (see changed_items)."""
    lines = []
    watch = state.get("bsig_watch", [])
    lines += ["", "EXPONENTIAL TRENDS TO WATCH", ""]
    for w in [w for w in watch if w.get("new")]:
        lines.append(f"  - {w['trend']}  [{w['status']}]")
        lines.append(f"      why: {w['why_exponential']}")
        lines.append(f"      watch: {w['watch']}")
        lines.append(f"      via: {w['expressions']}")
    old = [w for w in watch if not w.get("new")]
    if old:
        lines.append("")
        lines.append("  Still on watch:")
        for w in old:
            lines.append(f"    - {w['trend']} [{w['status']}]: {w['expressions']}")
    return "\n".join(lines)


# ---- html ----

def _eyebrow(txt):
    return (f'<p style="margin:0 0 10px; text-align:center; color:#9a9a9a; '
            f'font-size:12px; letter-spacing:2.5px; text-transform:uppercase; '
            f'font-family:{SANS};">{txt}</p>')


def render_changed_html(state: dict) -> str:
    d = diff(state)
    cur, prev = d["cur"], d["prev"]
    if prev.get("partial"):
        return ""   # nothing meaningful to diff against the baseline issue
    cregs = cur.get("regimes", {})

    def row(key, label, oneliner):
        impl = cregs.get(key, {}).get("implication", "")
        impl_html = (f'<br><span style="color:#9a9a9a;">{impl}</span>' if impl else "")
        return (f'<li style="margin:0 0 14px;"><strong>{label}:</strong> '
                f'{oneliner}{impl_html}</li>')

    rows = []
    for key, label, a, b in d["changed"]:
        rows.append(row(key, label, f'{a} &rarr; <strong>{b}</strong>'))
    for key, label, st, sig in d["steady"]:
        if sig:
            rows.append(row(key, label, ", ".join(sig)))
    for key, label, st, head in d["new"]:
        rows.append(row(key, label, head))
    if not rows:
        rows.append('<li>No changes.</li>')
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SANS};">What changed.</h2>
              <p style="margin:0 0 10px; color:#1a7f4b; font-size:14px; font-weight:600; font-family:{SANS};">Since {prev['date']}</p>
              <ul style="margin:0; padding:0 0 0 20px; color:#1a1a1a; font-size:16px; line-height:1.7; font-family:{SANS};">
                {''.join(rows)}
              </ul>
            </td>
          </tr>
"""


def _watch_card_full(w: dict) -> str:
    return f"""
              <tr><td style="padding:16px 0; border-bottom:1px solid #ededed; font-family:{SANS};">
                <p style="margin:0 0 4px; font-size:17px; font-weight:700; color:#1a1a1a;">{w['trend']}
                  <span style="font-size:12px; font-weight:400; color:#9a9a9a;">&nbsp;&middot;&nbsp;{w['status']}</span></p>
                <p style="margin:0 0 6px; font-size:15px; line-height:1.6; color:#444;">{w['why_exponential']}</p>
                <p style="margin:0; font-size:14px; line-height:1.6; color:#666;"><strong>Watch:</strong> {w['watch']}<br>
                  <strong>Where it shows up:</strong> {w['expressions']}</p>
              </td></tr>"""


def _watch_card_small(w: dict) -> str:
    # Not new this issue -> one compact, smaller line.
    return f"""
              <tr><td style="padding:8px 0; border-bottom:1px solid #f1f1f1; font-family:{SANS}; font-size:13px; line-height:1.5; color:#888;">
                <strong style="color:#555;">{w['trend']}</strong> &middot; {w['status']} &middot;
                <span style="color:#999;">{w['expressions']}</span></td></tr>"""


def render_watch_html(state: dict) -> str:
    watch = state.get("bsig_watch", [])
    new = [w for w in watch if w.get("new")]
    old = [w for w in watch if not w.get("new")]
    cards = "".join(_watch_card_full(w) for w in new)
    if old:
        cards += ('<tr><td style="padding:14px 0 4px; font-family:%s; font-size:12px; '
                  'letter-spacing:1.5px; text-transform:uppercase; color:#b3b3b3;">'
                  'Still on watch</td></tr>' % SANS)
        cards += "".join(_watch_card_small(w) for w in old)
    return f"""
          <tr>
            <td style="padding:40px 0 0;">
              <h2 style="margin:0 0 2px; color:#1a1a1a; font-size:26px; font-weight:700; line-height:1.25; letter-spacing:-0.3px; font-family:{SANS};">Exponential trends to watch.</h2>
              <p style="margin:0 0 14px; color:#1a7f4b; font-size:14px; font-weight:600; font-family:{SANS};">Signals to watch</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{cards}</table>
            </td>
          </tr>
"""


def main() -> int:
    state = load()
    if "--html" in sys.argv:
        print(render_changed_html(state))
        print(render_watch_html(state))
    else:
        print(render_text(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
