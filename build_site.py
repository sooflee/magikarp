#!/usr/bin/env python3
"""Build the public archive (GitHub Pages) for 'The Current Regime'.

Blog-style: docs/index.html lists every issue as a linked post, and each issue
gets its own page at docs/issues/<id>.html. Styled after bwang.io/elekid, with a
small serif type scale and a forest-green accent.

Usage:
    python3 build_site.py        # writes docs/index.html + docs/issues/*.html
"""

from __future__ import annotations

import sys
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


# ---------- images & charts (site only; the email renderer ignores these keys) ----------
# A section may carry `image` (an open-licence photo stored under docs/img/<issue>/) and/or
# `chart` (one dated series, drawn as HTML + a stretched SVG line so the text stays at
# CSS size on any screen width). lint_media() enforces credit, licence and file presence.
MEDIA_CSS = """
.fig{margin:4px 0 14px}
.fig img{display:block;width:100%;height:auto;max-height:340px;object-fit:cover;border-radius:3px;background:#f2f2f2}
.fig figcaption{font-size:var(--fs-meta);color:var(--muted);line-height:1.5;margin-top:6px}
.fig .credit,.fig .credit a{color:var(--faint)}
.chart{margin:14px 0 16px}
.chart .ctitle{font-size:var(--fs-detail);font-weight:700;margin:0;line-height:1.35}
.chart .csub{font-size:var(--fs-meta);color:var(--muted);margin:0 0 8px;line-height:1.4}
.cbox{position:relative;height:220px;outline:none}
.cbox:focus-visible{box-shadow:0 0 0 2px var(--accent-bg);border-radius:3px}
.plot{position:absolute;left:44px;right:62px;top:10px;bottom:26px;touch-action:pan-y}
.plot svg{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible}
.plot .g{position:absolute;left:0;right:0;border-top:1px solid #ededed}
.plot .yl{position:absolute;left:-44px;width:36px;text-align:right;transform:translateY(-50%);
  font-size:12px;color:var(--faint);font-variant-numeric:tabular-nums;line-height:1}
.plot .xl{position:absolute;top:100%;margin-top:8px;transform:translateX(-50%);font-size:12px;
  color:var(--faint);white-space:nowrap;line-height:1}
.plot .band{position:absolute;top:0;bottom:0;right:0;background:var(--accent-bg)}
.plot .bandl{position:absolute;bottom:4px;right:0;padding-right:5px;font-size:11px;color:var(--accent);
  white-space:nowrap;line-height:1}
.plot .ref{position:absolute;left:0;right:0;border-top:1px solid var(--faint)}
.plot .refl{position:absolute;left:4px;transform:translateY(-130%);font-size:11px;color:var(--muted);
  line-height:1;white-space:nowrap}
.plot .dot,.plot .hdot{position:absolute;width:8px;height:8px;margin:-4px 0 0 -4px;border-radius:50%;
  background:var(--accent);box-shadow:0 0 0 2px #fff}
.plot .endl{position:absolute;left:100%;margin-left:9px;transform:translateY(-50%);font-size:13px;
  font-weight:700;color:var(--fg);white-space:nowrap;line-height:1}
.plot .xh{position:absolute;top:0;bottom:0;border-left:1px solid var(--muted);display:none}
.plot .hdot{display:none}
.plot .tip{position:absolute;top:0;display:none;pointer-events:none;background:#fff;
  border:1px solid var(--line);border-radius:4px;padding:5px 8px;font-size:12px;line-height:1.35;
  color:var(--muted);white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.08);z-index:2}
.plot .tip b{display:block;font-size:14px;color:var(--fg)}
.chart details{font-size:var(--fs-meta);color:var(--muted);margin-top:8px}
.chart details summary{cursor:pointer}
.chart details table{border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
.chart details td{padding:2px 16px 2px 0;border-bottom:1px solid #f0f0f0}
.chart .csrc{font-size:12px;color:var(--faint);margin:4px 0 0}
.chart .csrc a{color:var(--faint)}
.dek{font-size:var(--fs-body);line-height:1.5;margin:16px 0 0;color:var(--fg)}
.brief{margin:22px 0 0;padding:14px 0 6px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.brief .blbl{font-size:var(--fs-meta);letter-spacing:2px;text-transform:uppercase;font-weight:700;margin:0 0 8px}
.brief ul{margin:0;padding:0;list-style:none}
.brief li{font-size:var(--fs-detail);line-height:1.5;margin:0 0 8px}
.brief a.lane{font-weight:700;text-decoration:none;margin-right:4px}
.kick{font-size:var(--fs-meta);font-weight:600;color:var(--accent);margin:0 0 4px}
.kick .badge{margin-left:8px}
.badge.neutral{background:#efefef;color:#555}
.impl{border-left:2px solid var(--line);padding-left:12px;margin:4px 0 12px}
.impl .lbl{display:block;font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--faint);font-weight:700;margin-bottom:2px}
details.more{margin:6px 0 0}
details.more summary{cursor:pointer;color:var(--muted);font-size:var(--fs-meta);margin:4px 0}
.story .cmt{color:#4b5058}
.sec h2{margin:0 0 10px}
.impl{color:#333}
.gl{position:relative;border-bottom:1px dotted #8a9099;cursor:help;outline:none}
.gl:focus-visible{background:var(--accent-bg);border-radius:2px}
.gl-tip{display:none;position:absolute;left:0;top:100%;margin-top:6px;z-index:30;width:max-content;
  max-width:min(300px,82vw);background:#fff;color:var(--fg);border:1px solid var(--line);border-radius:6px;
  box-shadow:0 3px 12px rgba(0,0,0,.12);padding:8px 11px;font-size:14px;line-height:1.45;font-weight:400;
  font-style:normal;text-align:left;white-space:normal;letter-spacing:0;text-transform:none}
.gl-tip::before{content:"";position:absolute;left:0;right:0;top:-8px;height:8px}
.gl:hover .gl-tip,.gl:focus-within .gl-tip,.gl.open .gl-tip{display:block}
.gl-tip a{color:var(--accent);font-size:12px;margin-left:5px}
"""

GL_JS = """<script>
(function(){
  function place(g){
    var tip=g.querySelector('.gl-tip'); if(!tip) return;
    tip.style.left='0px';
    requestAnimationFrame(function(){
      var r=tip.getBoundingClientRect(), vw=document.documentElement.clientWidth, dx=0;
      if(r.width===0) return;
      if(r.right>vw-8) dx=vw-8-r.right;
      if(r.left+dx<8) dx=8-r.left;
      tip.style.left=dx+'px';
    });
  }
  function closeAll(except){
    document.querySelectorAll('.gl.open').forEach(function(o){ if(o!==except) o.classList.remove('open'); });
  }
  document.querySelectorAll('.gl').forEach(function(g){
    g.addEventListener('mouseenter',function(){ place(g); });
    g.addEventListener('focus',function(){ place(g); });
    g.addEventListener('click',function(e){
      if(e.target.closest('a')) return;
      var was=g.classList.contains('open'); closeAll(g);
      g.classList.toggle('open',!was); if(!was) place(g);
      e.stopPropagation();
    });
  });
  document.addEventListener('click',function(){ closeAll(null); });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){ closeAll(null); var a=document.activeElement; if(a&&a.classList.contains('gl')) a.blur(); }
  });
})();
</script>"""

NOTE_SKIP_TAGS = {"a", "h1", "h2", "script", "style", "summary", "title", "svg", "button", "figcaption"}


def page_notes(doc: dict, iss: dict) -> list:
    """Issue annotations first (they win on a shared term), then the shared glossary."""
    return list(iss.get("annotations") or []) + list(doc.get("glossary") or [])


def annotate_html(body: str, notes: list) -> tuple:
    """Mark the first occurrence of each note's terms on the page (the brief counts separately).
    Skips links, headings, captions, chart markup and anything inside tags. Returns
    (html, set of note indexes that matched at least once)."""
    import re
    if not notes:
        return body, set()
    term_idx = {}
    for i, n in enumerate(notes):
        for t in n.get("terms", []):
            term_idx.setdefault(esc(t), i)
    if not term_idx:
        return body, set()
    alts = "|".join(re.escape(t) for t in sorted(term_idx, key=len, reverse=True))
    rx = re.compile(rf"(?<![A-Za-z0-9])({alts})(?![A-Za-z0-9])")
    page_used, brief_used = set(), set()
    out, used, hits, skip, counter = [], page_used, set(), 0, [0]

    def mark(m):
        i = term_idx[m.group(1)]
        if i in used:
            return m.group(0)
        used.add(i)
        hits.add(i)
        counter[0] += 1
        n = notes[i]
        src_link = f' <a href="{esc(n["url"])}">source</a>' if n.get("url") else ""
        nid = f"gl-{counter[0]}"
        return (f'<span class="gl" tabindex="0" aria-describedby="{nid}">{m.group(1)}'
                f'<span class="gl-tip" role="tooltip" id="{nid}">{esc(n["note"])}{src_link}</span></span>')

    for part in re.split(r"(<[^>]+>)", body):
        if part.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", part)
            if m:
                closing, name = m.group(1) == "/", m.group(2).lower()
                if name in NOTE_SKIP_TAGS and not part.endswith("/>"):
                    skip += -1 if closing else 1
                if not closing and name == "div":
                    cm = re.search(r'class="(sec|brief)', part)
                    if cm:   # once per page for the sections; the brief keeps its own set
                        used = brief_used if cm.group(1) == "brief" else page_used
            out.append(part)
        elif skip > 0 or not part.strip():
            out.append(part)
        else:
            out.append(rx.sub(mark, part))
    return "".join(out), hits


def lint_notes(doc: dict) -> None:
    problems = []
    groups = [("glossary", doc.get("glossary") or [])]
    groups += [(f"issue {i['id']} annotations", i.get("annotations") or []) for i in doc.get("issues", [])]
    for where, notes in groups:
        for n in notes:
            terms, note = n.get("terms") or [], n.get("note", "")
            if not terms or not note:
                problems.append(f"{where}: note needs terms and note text: {n}")
                continue
            if len(note.split()) > 45:
                problems.append(f"{where}: note over 45 words for {terms[0]!r}")
            if "\u2014" in note:
                problems.append(f"{where}: em-dash in note for {terms[0]!r}")
    if problems:
        print("NOTES LINT:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)



CHART_JS = """<script>
document.querySelectorAll('.cbox').forEach(function(box){
  var plot=box.querySelector('.plot'), pts=JSON.parse(box.getAttribute('data-pts'));
  var xh=plot.querySelector('.xh'), hd=plot.querySelector('.hdot'), tip=plot.querySelector('.tip');
  var tv=tip.querySelector('b'), tl=tip.querySelector('span'), cur=-1;
  function show(i){
    cur=i; var p=pts[i];
    xh.style.left=p[0]+'%'; hd.style.left=p[0]+'%'; hd.style.top=p[1]+'%';
    tv.textContent=p[3]; tl.textContent=p[2];
    xh.style.display=hd.style.display=tip.style.display='block';
    var w=plot.clientWidth, x=p[0]/100*w, tw=tip.offsetWidth;
    var left=(x+12+tw>w)?x-12-tw:x+12;
    tip.style.left=Math.max(0,Math.min(w-tw,left))+'px';
  }
  function hide(){xh.style.display=hd.style.display=tip.style.display='none';}
  function nearest(cx){
    var r=plot.getBoundingClientRect(), f=(cx-r.left)/r.width*100, b=0;
    for(var i=1;i<pts.length;i++){if(Math.abs(pts[i][0]-f)<Math.abs(pts[b][0]-f))b=i;}
    return b;
  }
  box.addEventListener('pointermove',function(e){show(nearest(e.clientX));});
  box.addEventListener('pointerleave',hide);
  box.addEventListener('focus',function(){show(cur<0?pts.length-1:cur);});
  box.addEventListener('blur',hide);
  box.addEventListener('keydown',function(e){
    var i=cur<0?pts.length-1:cur;
    if(e.key==='ArrowLeft'){show(Math.max(0,i-1));e.preventDefault();}
    if(e.key==='ArrowRight'){show(Math.min(pts.length-1,i+1));e.preventDefault();}
  });
});
</script>"""

LICENSE_OK = ("Public domain", "CC0", "CC BY ", "CC BY-SA ")


def render_figure(img) -> str:
    if not img:
        return ""
    lic = esc(img["license"])
    if img.get("license_url"):
        lic = f'<a href="{esc(img["license_url"])}">{lic}</a>'
    return (f'<figure class="fig"><img src="../{esc(img["src"])}" alt="{esc(img["alt"])}" '
            f'width="{int(img["width"])}" height="{int(img["height"])}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(img["caption"])} <span class="credit">{esc(img["credit"])} &middot; '
            f'{lic} &middot; <a href="{esc(img["source_url"])}">source</a></span></figcaption></figure>')


def _nice_step(span: float, n: int = 4) -> float:
    import math
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def _fmt_val(ch: dict, v: float, decimals=None) -> str:
    d = ch.get("decimals", 0) if decimals is None else decimals
    return f'{ch.get("prefix", "")}{v:,.{d}f}{ch.get("suffix", "")}'


def _day(d) -> str:
    return f'{d.strftime("%B")} {d.day}'


def render_chart(ch) -> str:
    """One dated series as a line: hairline grid, 2px line, end dot + end label, optional
    reference line and shaded issue week, crosshair tooltip, and a table view."""
    if not ch:
        return ""
    import datetime as dt
    import json as _json
    import math
    pts = ch["series"][0]["points"]
    days = [dt.date.fromisoformat(d) for d, _ in pts]
    vals = [float(v) for _, v in pts]
    t0, t1 = days[0], days[-1]
    span_d = max(1, (t1 - t0).days)
    extra = [ch["ref"]["value"]] if ch.get("ref") else []
    lo, hi = min(vals + extra), max(vals + extra)
    step = _nice_step((ch.get("y_max", hi) - ch.get("y_min", lo)) or 1)
    ylo = ch.get("y_min", math.floor(lo / step) * step)
    yhi = ch.get("y_max", math.ceil(hi / step) * step)
    X = lambda d: (d - t0).days / span_d * 100
    Y = lambda v: (yhi - v) / (yhi - ylo) * 100
    grid = []
    for i in range(int(round((yhi - ylo) / step)) + 1):
        v = ylo + i * step
        grid.append(f'<div class="g" style="top:{Y(v):.2f}%"></div>'
                    f'<div class="yl" style="top:{Y(v):.2f}%">'
                    f'{esc(_fmt_val(ch, v, ch.get("tick_decimals", 0)))}</div>')
    ticks = []
    if span_d > 45:                                    # month starts
        d = dt.date(t0.year, t0.month, 1)
        while d <= t1:
            if d >= t0:
                ticks.append((d, d.strftime("%b")))
            d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    else:                                              # weekly from the first date
        d = t0
        while d <= t1:
            ticks.append((d, f'{d.strftime("%b")} {d.day}'))
            d += dt.timedelta(days=7)
    xl = "".join(f'<div class="xl" style="left:{X(d):.2f}%">{esc(t)}</div>' for d, t in ticks)
    band = ""
    if ch.get("highlight_from"):
        bx = X(max(dt.date.fromisoformat(ch["highlight_from"]), t0))
        band = (f'<div class="band" style="left:{bx:.2f}%"></div>'
                f'<div class="bandl">{esc(ch.get("highlight_label", "this week"))}</div>')
    ref = ""
    if ch.get("ref"):
        ry = Y(ch["ref"]["value"])
        ref = (f'<div class="ref" style="top:{ry:.2f}%"></div>'
               f'<div class="refl" style="top:{ry:.2f}%">{esc(ch["ref"]["label"])}</div>')
    poly = " ".join(f"{X(d) * 10:.1f},{Y(v) * 10:.1f}" for d, v in zip(days, vals))
    svg = (f'<svg viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-hidden="true">'
           f'<polyline points="{poly}" fill="none" stroke="{ACCENT}" stroke-width="2" '
           f'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')
    ex, ey = X(days[-1]), Y(vals[-1])
    end = (f'<span class="dot" style="left:{ex:.2f}%;top:{ey:.2f}%"></span>'
           f'<span class="endl" style="top:{ey:.2f}%">{esc(_fmt_val(ch, vals[-1]))}</span>')
    jpts = [[round(X(d), 3), round(Y(v), 3), _day(d), _fmt_val(ch, v)] for d, v in zip(days, vals)]
    rows = "".join(f'<tr><td>{_day(d)}</td><td>{esc(_fmt_val(ch, v))}</td></tr>'
                   for d, v in zip(days, vals))
    src = esc(ch["source"])
    if ch.get("source_url"):
        src = f'<a href="{esc(ch["source_url"])}">{src}</a>'
    aria = (f'{ch["title"]}: {_fmt_val(ch, vals[0])} on {_day(days[0])}, '
            f'{_fmt_val(ch, vals[-1])} on {_day(days[-1])}')
    sub = f'<p class="csub">{esc(ch["subtitle"])}</p>' if ch.get("subtitle") else ""
    return (f'<div class="chart"><p class="ctitle">{esc(ch["title"])}</p>{sub}'
            f'<div class="cbox" tabindex="0" role="img" aria-label="{esc(aria)}" '
            f'data-pts="{esc(_json.dumps(jpts))}"><div class="plot">'
            f'{"".join(grid)}{band}{ref}{svg}{end}'
            '<div class="xh"></div><span class="hdot"></span><div class="tip"><b></b><span></span></div>'
            f'{xl}</div></div>'
            f'<details><summary>Show the numbers</summary><table>{rows}</table></details>'
            f'<p class="csrc">Source: {src}</p></div>')


def lint_media(doc: dict) -> None:
    problems = []
    for iss in doc.get("issues", []):
        secs = [(f"regimes.{k}", v) for k, v in (iss.get("regimes") or {}).items()]
        secs += [(k, iss.get(k)) for k in ("commodities", "wildcard", "undercurrent")]
        for name, sec in secs:
            if not isinstance(sec, dict):
                continue
            where = f"issue {iss['id']} {name}"
            img = sec.get("image")
            if img:
                for key in ("src", "alt", "caption", "credit", "license", "source_url", "width", "height"):
                    if not img.get(key):
                        problems.append(f"{where}.image is missing {key}")
                if img.get("src") and not (DOCS / img["src"]).is_file():
                    problems.append(f"{where}.image file not found: docs/{img['src']}")
                if img.get("license") and not str(img["license"]).startswith(LICENSE_OK):
                    problems.append(f"{where}.image licence not open: {img['license']!r}")
            ch = sec.get("chart")
            if ch:
                series = ch.get("series") or []
                if len(series) != 1:
                    problems.append(f"{where}.chart needs exactly one series "
                                    "(two or more need a legend and a validated palette)")
                else:
                    dates = [p[0] for p in series[0].get("points", [])]
                    if len(dates) < 2 or dates != sorted(dates):
                        problems.append(f"{where}.chart points must be 2+ ISO dates in order")
                for key in ("title", "source"):
                    if not ch.get(key):
                        problems.append(f"{where}.chart is missing {key}")
    if problems:
        print("MEDIA LINT:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)


def esc(s) -> str:
    return html.escape(str(s))


def page(title: str, inner: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<style>{CSS}{MEDIA_CSS}</style>
</head><body><div class="wrap">
{inner}
<footer><a href="https://github.com/sooflee/magikarp">source on GitHub</a><br>
Market notes are directional only and are not investment advice.</footer>
</div></body></html>
"""


def badge(state: str, neutral: bool = False) -> str:
    if not state:
        return ""
    cls = "badge neutral" if neutral else ("badge warn" if state in WARN_STATES else "badge")
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


def render_links(links: list, keep: int = 5) -> str:
    """Show the first few sources; fold a long tail into a collapsible list."""
    if not links:
        return ""
    li = [f'<li><a href="{esc(l["url"])}">{esc(l["title"])}</a></li>' for l in links]
    if len(li) <= keep + 1:
        return f'<ul class="links">{"".join(li)}</ul>'
    return (f'<ul class="links">{"".join(li[:keep])}</ul>'
            f'<details class="more"><summary>{len(li) - keep} more sources</summary>'
            f'<ul class="links">{"".join(li[keep:])}</ul></details>')


def render_impl(r: dict) -> str:
    if not r.get("implication"):
        return ""
    return f'<p class="impl"><span class="lbl">Key fact</span>{esc(r["implication"])}</p>'


def kick(label_html: str, state: str = "", neutral: bool = False) -> str:
    return f'<p class="kick">{label_html}{badge(state, neutral)}</p>'


def human_date(s: str) -> str:
    import datetime as dt
    try:
        d = dt.date.fromisoformat(s)
        return f"{d.strftime('%B')} {d.day}"
    except Exception:
        return s


SECTION_IDS = {"ai_compute": "ai", "tech_policy": "tech-policy", "ai_agents": "ai-agents",
               "deep_dive": "deep-dive", "geopolitics": "geopolitics", "markets": "markets"}


def render_items(items: list) -> str:
    if not items:
        return ""
    return "".join(
        f'<p class="story"><a href="{esc(it["url"])}">{esc(it["title"])}</a><br>'
        f'<span class="cmt">{esc(it.get("comment",""))}</span></p>'
        for it in items)


def render_regime(label: str, r: dict, traj: str = None, sid: str = "", neutral: bool = False) -> str:
    body = r.get("summary") or " ".join(r.get("evidence", []))
    traj_html = f'<p class="traj">{esc(traj)}</p>' if traj else ""
    idattr = f' id="{sid}"' if sid else ""
    return (f'<div class="sec"{idattr}>{kick(esc(label), r.get("state", ""), neutral)}'
            f'<h2>{esc(r.get("headline", label))}</h2>{traj_html}{render_figure(r.get("image"))}'
            f'<p>{esc(body)}</p>{render_impl(r)}{render_chart(r.get("chart"))}'
            f'{render_items(r.get("items"))}{render_links(r.get("links"))}</div>')


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
    return (f'<div class="sec" id="attention">{kick("Regime momentum &middot; " + esc(weeks[0]) + " vs " + esc(weeks[-1]))}'
            f'<h2>Where the week&rsquo;s attention went.</h2>'
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
    return (f'<div class="sec" id="watch-next">{kick("The calendar ahead")}'
            f'<h2>What to watch next week.</h2>{rows}</div>')


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
            if r.get("line"):
                fact = f' {esc(r["line"])}'
            else:
                b0 = (r.get("basket") or [None])[0]
                fact = f' {esc(b0["metric"])}: {esc(b0["value"])}.' if b0 else ""
            blocks.append(
                f'<p class="rcompact"><strong>{esc(r["name"])}</strong> '
                f'<span class="rdir">{esc(r.get("direction",""))}</span>.{fact}</p>')
    return ('<div class="sec" id="radar">'
            + kick("Regime radar &middot; read through markets and hard data")
            + '<h2>The structural picture.</h2>'
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
    return (f'<div class="sec" id="commodities">'
            f'{kick("Commodities &amp; energy &middot; " + esc(human_date(c.get("as_of",""))))}'
            f'<h2>{esc(c.get("headline", "Crude falls as the fear premium unwinds."))}</h2>'
            f'{render_figure(c.get("image"))}<p>{esc(c.get("summary",""))}</p>'
            f'{render_chart(c.get("chart"))}<table class="mkt">{rows}</table></div>')


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
    return (f'<div class="sec" id="undercurrent">{kick(esc(u.get("label","Undercurrent")))}'
            f'<h2>{esc(u["headline"])}</h2>{render_figure(u.get("image"))}'
            f'<p>{esc(u.get("summary",""))}</p>{render_links(u.get("links"))}</div>')


def render_wildcard(w: dict) -> str:
    """The rotating wildcard: one theme each week outside the four tracked lanes.
    Not part of the week-over-week momentum; renders only when present."""
    if not w or not w.get("headline"):
        return ""
    topic = w.get("topic", "")
    sub = f'The wildcard &middot; {esc(topic)}' if topic else 'The wildcard'
    return (f'<div class="sec wildcard" id="wildcard">{kick(sub)}<h2>{esc(w["headline"])}</h2>'
            f'{render_figure(w.get("image"))}<p>{esc(w.get("summary",""))}</p>'
            f'{render_items(w.get("items"))}{render_links(w.get("links"))}</div>')


def render_briefs(items: list) -> str:
    """Smaller stories: one-line briefs from the research/accountability sweep.
    Optional; renders only when the issue carries a briefs list."""
    if not items:
        return ""
    return (f'<div class="sec" id="briefs">{kick("Short items from the week&rsquo;s edges")}'
            f'<h2>Smaller stories.</h2>{render_items(items)}</div>')


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
        '<details class="more"><summary>What the readings mean</summary>'
        '<p class="means">Volatility measures how much the market is expected to '
        'move in the near term compared with the longer term, so a lower reading '
        'means less immediate stress. The yield curve is the gap between long-term '
        'and short-term government borrowing rates, and a steep curve usually points '
        'to expected growth rather than recession. When crypto is described as '
        'risk-off, investors are stepping back from the most speculative assets, '
        'which often serves as an early note of caution beneath a calm market.</p></details>')
    return (f'<div class="sec" id="markets">{kick("Markets", m.get("state", ""))}'
            f'<h2>{esc(m.get("headline","Markets"))}</h2>'
            f'{render_figure(m.get("image"))}{summary}{render_impl(m)}{render_chart(m.get("chart"))}'
            f'<table class="mkt">{rows}</table>{means}</div>')


def render_watch(watch: list) -> str:
    new = [w for w in watch if w.get("new")]
    old = [w for w in watch if not w.get("new")]
    out = [f'<div class="sec" id="trends">{kick("Signals to watch")}<h2>Exponential trends to watch.</h2>']
    for w in new:
        out.append(
            f'<div class="watch"><div class="t">{esc(w["trend"])} '
            f'<span class="st">&middot; {esc(w["status"])}</span></div>'
            f'<div class="why">{esc(w["why_exponential"])}</div>'
            f'<div class="via"><strong>What to watch:</strong> {esc(w["watch"])} '
            f'<strong>Where it shows up:</strong> {esc(w["expressions"])}</div></div>')
    if old:
        out.append(f'<details class="more"><summary>Still on watch ({len(old)})</summary>')
        for w in old:
            out.append(f'<div class="watch small"><strong style="color:#666">{esc(w["trend"])}</strong> '
                       f'&middot; {esc(w["status"])} &middot; {esc(w["expressions"])}</div>')
        out.append("</details>")
    out.append("</div>")
    return "".join(out)


def render_lede(iss: dict) -> str:
    return f'<p class="lede">{esc(iss["lede"])}</p>' if iss.get("lede") else ""


def render_brief(iss: dict) -> str:
    """The week in brief: one line per lane under the masthead, each linking to its section."""
    items = iss.get("brief") or []
    if not items:
        return ""
    lis = "".join(f'<li><a class="lane" href="#{esc(b["anchor"])}">{esc(b["lane"])}</a> {esc(b["line"])}</li>'
                  for b in items)
    return f'<div class="brief"><p class="blbl">The week in brief</p><ul>{lis}</ul></div>'


def render_act(title: str) -> str:
    return f'<div class="act"><div class="actlabel">{esc(title)}</div><hr></div>'


def _regime(doc, iss, key):
    r = iss.get("regimes", {}).get(key)
    if not r:
        return ""
    return render_regime(doc["regime_defs"].get(key, {}).get("label", key), r,
                         sid=SECTION_IDS.get(key, ""), neutral=(key == "deep_dive"))


def render_issue_page(doc: dict, iss: dict) -> str:
    reg = iss.get("regimes", {})
    dek = f'<p class="dek">{esc(iss["index_title"])}</p>' if iss.get("brief") and iss.get("index_title") else ""
    secs = [render_brief(iss), render_lede(iss)]
    # Act 1 — the tech world
    secs.append(render_act("The tech world"))
    if "ai_compute" in reg:                       # issue 06+ : one merged AI lane
        secs.append(_regime(doc, iss, "ai_compute"))
    else:                                          # archive (01-05) : the old two lanes
        secs.append(_regime(doc, iss, "tech_policy"))
        secs.append(_regime(doc, iss, "ai_agents"))
    if iss.get("across_sources"):
        secs.append(render_across_inline(iss["across_sources"]))   # GitHub note under AI
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
    # Act 3 — the standing trackers, together
    secs.append(render_act("Tracking the regimes"))
    secs.append(render_momentum(doc, iss))
    secs.append(render_watch(iss.get("bsig_watch") or doc.get("bsig_watch", [])))
    secs.append(render_radar(iss))
    secs.append(render_watch_next(iss))
    body = "".join(secs)
    notes = page_notes(doc, iss)
    body, hits = annotate_html(body, notes)
    n_issue = len(iss.get("annotations") or [])
    missed = [notes[i]["terms"][0] for i in range(n_issue) if i not in hits]
    if missed:
        print(f"NOTES LINT: issue {iss['id']} annotations never matched the page: {missed}", file=sys.stderr)
        raise SystemExit(1)
    if 'class="cbox"' in body:
        body += CHART_JS
    if 'class="gl"' in body:
        body += GL_JS
    label = iss.get("date_label") or week_label(iss)
    inner = (
        f'<header class="mast"><h1><a href="../">The Current Regime</a></h1>'
        f'<div class="kicker">Issue {esc(iss["id"])} &middot; {esc(label)}</div>{dek}</header>'
        f'<p class="back" style="margin-top:14px"><a href="../">&larr; all issues</a></p>'
        + body
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
    lint_media(doc)
    lint_notes(doc)
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
