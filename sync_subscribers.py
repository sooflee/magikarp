#!/usr/bin/env python3
"""Pull sign-ups from the Google Sheet (via the Apps Script doGet) into
subscribers.txt. The Sheet is the store; this merges any new addresses into the
local list the sender delivers to. Run before each send (see run_weekly.sh).

Usage:
    python3 sync_subscribers.py
    python3 sync_subscribers.py --dry-run
"""

import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL_FILE = ROOT / "apps_script_url.txt"
KEY_FILE = ROOT / "apps_script_key.txt"
SUBSCRIBERS = ROOT / "subscribers.txt"
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def apps_url():
    if URL_FILE.exists():
        for line in URL_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("https://"):
                return line
    return ""


def read_key():
    if os.environ.get("APPS_SCRIPT_KEY"):
        return os.environ["APPS_SCRIPT_KEY"].strip()
    if KEY_FILE.exists():
        for line in KEY_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line
    return ""


def load():
    comments, subs = [], []
    if SUBSCRIBERS.exists():
        for line in SUBSCRIBERS.read_text().splitlines():
            s = line.strip()
            if s.startswith("#") or not s:
                comments.append(line)
            elif "@" in s:
                subs.append(s)
    return comments, subs


def main() -> int:
    url = apps_url()
    if not url:
        print("no Apps Script URL in apps_script_url.txt; skipping sheet sync")
        return 0
    dry = "--dry-run" in sys.argv
    key = read_key()
    if key:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode({"key": key})
    try:
        data = urllib.request.urlopen(url, timeout=20).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"sheet fetch failed: {e}", file=sys.stderr)
        return 1

    sheet = [l.strip().lower() for l in data.splitlines() if EMAIL.match(l.strip())]
    comments, subs = load()
    cur = {s.lower() for s in subs}
    added = [e for e in sheet if e not in cur]
    for e in added:
        subs.append(e)

    print(f"sheet sync: +{len(added)} (list size {len({s.lower() for s in subs})})")
    for e in added:
        print(f"  + {e}")

    if not dry:
        uniq = sorted({s.lower() for s in subs})
        SUBSCRIBERS.write_text("\n".join(comments + uniq) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
