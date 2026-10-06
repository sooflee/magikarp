#!/usr/bin/env python3
"""Apply audit corrections to an issue as exact-match replacements that fail loudly.

Usage:
    python3 apply_fixes.py fixes.json            # latest issue
    python3 apply_fixes.py fixes.json 17         # a given issue id

fixes.json is a list of {"old": "...", "new": "..."} objects. Each `old` must occur
in the issue's text fields; it is replaced everywhere it occurs in that issue (so a
number repeated in two sections is fixed in both, which is usually what you want;
check the printed counts). If any `old` is not found, nothing is written and the
script exits 1, so a silently missed correction cannot ship. Edits touch only the
chosen issue object, never other issues or the watchlist (edit those by hand).
"""
import json
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parent / "regime_state.json"


def replace_in(node, old, new, count):
    if isinstance(node, dict):
        return {k: replace_in(v, old, new, count) for k, v in node.items()}
    if isinstance(node, list):
        return [replace_in(v, old, new, count) for v in node]
    if isinstance(node, str) and old in node:
        count[0] += node.count(old)
        return node.replace(old, new)
    return node


def main() -> int:
    fixes = json.loads(Path(sys.argv[1]).read_text())
    doc = json.loads(STATE.read_text())
    issues = doc["issues"]
    idx = (next(i for i, x in enumerate(issues) if x["id"] == sys.argv[2])
           if len(sys.argv) > 2 else len(issues) - 1)
    iss = issues[idx]
    missing = []
    for f in fixes:
        count = [0]
        iss = replace_in(iss, f["old"], f["new"], count)
        if count[0] == 0:
            missing.append(f["old"])
        else:
            print(f"{count[0]}x  {f['old'][:70]!r}")
    if missing:
        print("\nNOT FOUND (nothing written):", file=sys.stderr)
        for m in missing:
            print(f"  {m!r}", file=sys.stderr)
        return 1
    issues[idx] = iss
    STATE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"applied {len(fixes)} fix(es) to issue {iss['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
