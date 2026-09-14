#!/usr/bin/env python3
"""Images and chart series for the archive site (the email does not render them).

Photos must be open-licence and stored locally under docs/img/<issue>/; news-agency
photos from linked articles are never used. Each helper prints a JSON block ready to
paste into a section's `image` or `chart` in regime_state.json; fill in `alt` and
`caption` by looking at the image, and write the caption as a fact about the picture
(what, where, when), not about the week's story.

  python3 media.py commons "File:Name.jpg" docs/img/15/geopolitics.jpg
  python3 media.py worldview 2026-09-08 -5,105,4,119 docs/img/15/deep_dive.jpg
  python3 media.py polymarket fed-decision-in-september-762 "25 bps" 2026-08-20 2026-09-13
  python3 media.py yf BZ=F 2026-06-01 2026-09-11

worldview BBOX is south,west,north,east in degrees. polymarket returns UTC daily closes
(the last hourly print of each UTC day) in cents for the Yes side of the first market
whose question contains the match text. yf returns unadjusted daily closes through the
end date, using the sibling ekans venv (system python has no yfinance).
"""
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
UA = {"User-Agent": "magikarp-newsletter/1.0 (bensonw.dev@gmail.com)"}
EKANS_PY = ROOT.parent / "ekans" / ".venv" / "bin" / "python"


def _get_json(url: str):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        dest.write_bytes(r.read())


def _fit(dest: Path, width: int = 1280) -> tuple[int, int]:
    """Resize in place to at most `width` px on the long side, JPEG quality 78 (macOS sips)."""
    subprocess.run(["sips", "-Z", str(width), "-s", "formatOptions", "78", str(dest)],
                   check=True, capture_output=True)
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dest)],
                         check=True, capture_output=True, text=True).stdout
    w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return w, h


def _strip(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def commons(title: str, dest: str, width: int = 1280) -> dict:
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": title,
                                "prop": "imageinfo", "iiprop": "url|size|extmetadata",
                                "iiurlwidth": width})
    page = next(iter(_get_json(f"https://commons.wikimedia.org/w/api.php?{q}")["query"]["pages"].values()))
    if "imageinfo" not in page:
        sys.exit(f"not found on Commons: {title}")
    ii = page["imageinfo"][0]
    meta = {k: _strip(v.get("value", "")) for k, v in ii.get("extmetadata", {}).items()}
    path = ROOT / dest
    _download(ii.get("thumburl") or ii["url"], path)
    w, h = _fit(path, width)
    print(f"# Commons notes: date {meta.get('DateTimeOriginal', '?')}; "
          f"description: {meta.get('ImageDescription', '')[:200]}", file=sys.stderr)
    return {"src": str(path.relative_to(DOCS)), "width": w, "height": h, "alt": "", "caption": "",
            "credit": meta.get("Artist", ""), "license": meta.get("LicenseShortName", ""),
            "license_url": meta.get("LicenseUrl", ""), "source_url": ii["descriptionurl"]}


def worldview(date: str, bbox: str, dest: str,
              layer: str = "MODIS_Terra_CorrectedReflectance_TrueColor") -> dict:
    s, w_, n, e = (float(x) for x in bbox.split(","))
    q = urllib.parse.urlencode({"REQUEST": "GetSnapshot", "TIME": date, "BBOX": f"{s},{w_},{n},{e}",
                                "CRS": "EPSG:4326", "LAYERS": f"{layer},Coastlines_15m",
                                "WRAP": "day,x", "FORMAT": "image/jpeg", "WIDTH": 1400, "HEIGHT": 900})
    path = ROOT / dest
    _download(f"https://wvs.earthdata.nasa.gov/api/v1/snapshot?{q}", path)
    w, h = _fit(path)
    sat = "Aqua" if "Aqua" in layer else ("Terra" if "Terra" in layer else "VIIRS")
    link = (f"https://worldview.earthdata.nasa.gov/?v={w_},{s},{e},{n}"
            f"&l={layer},Coastlines_15m&t={date}")
    return {"src": str(path.relative_to(DOCS)), "width": w, "height": h, "alt": "", "caption": "",
            "credit": f"NASA Worldview, MODIS on {sat}" if sat != "VIIRS" else "NASA Worldview, VIIRS",
            "license": "Public domain", "source_url": link}


def polymarket_daily(slug: str, match: str, start: str, end: str) -> list:
    ev = _get_json(f"https://gamma-api.polymarket.com/events?slug={urllib.parse.quote(slug)}")
    if not ev:
        sys.exit(f"no Polymarket event {slug}")
    found = [m for m in ev[0]["markets"] if match.lower() in m["question"].lower()]
    if len(found) != 1:
        listing = "\n  ".join(m["question"] for m in (found or ev[0]["markets"]))
        sys.exit(f"{len(found)} markets in {slug} match {match!r}; use text unique to one:\n  {listing}")
    mk = found[0]
    token = json.loads(mk["clobTokenIds"])[0]
    hist = _get_json(f"https://clob.polymarket.com/prices-history?market={token}"
                     f"&interval=max&fidelity=60")["history"]
    days = {}
    for p in sorted(hist, key=lambda p: p["t"]):
        days[dt.datetime.fromtimestamp(p["t"], dt.timezone.utc).date().isoformat()] = p["p"]
    print(f"# market: {mk['question']}", file=sys.stderr)
    return [[d, round(v * 100, 1)] for d, v in sorted(days.items()) if start <= d <= end]


def yf_daily(ticker: str, start: str, end: str) -> list:
    stop = (dt.date.fromisoformat(end) + dt.timedelta(days=1)).isoformat()
    code = ("import json,sys,yfinance as yf\n"
            f"h=yf.Ticker({ticker!r}).history(start={start!r},end={stop!r},auto_adjust=False)['Close']\n"
            "print(json.dumps([[d.strftime('%Y-%m-%d'),round(float(v),2)] for d,v in h.items()]))")
    out = subprocess.run([str(EKANS_PY), "-c", code], check=True, capture_output=True, text=True).stdout
    return json.loads(out.strip().splitlines()[-1])


def main(argv: list) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd, args = argv[1], argv[2:]
    if cmd == "commons":
        out = commons(*args)
    elif cmd == "worldview":
        out = worldview(*args)
    elif cmd == "polymarket":
        out = polymarket_daily(*args)
    elif cmd == "yf":
        out = yf_daily(*args)
    else:
        print(__doc__)
        return 1
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
