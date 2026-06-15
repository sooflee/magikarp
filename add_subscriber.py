#!/usr/bin/env python3
"""Manually manage the subscriber list (subscribers.txt).

The list is the same file send_regime_email.py delivers to and signups.py keeps
up to date, so anything added here receives the next issue.

Usage:
    python3 add_subscriber.py alice@example.com bob@example.com   # add one or more
    python3 add_subscriber.py                                     # interactive prompt
    python3 add_subscriber.py --list                             # show the current list
    python3 add_subscriber.py --remove alice@example.com         # remove one or more
"""

import re
import sys
from pathlib import Path

SUBSCRIBERS = Path(__file__).resolve().parent / "subscribers.txt"
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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


def save(comments, subs):
    uniq = sorted({s.strip().lower() for s in subs})   # lowercase + dedupe
    SUBSCRIBERS.write_text("\n".join(comments + uniq) + "\n")


def main() -> int:
    args = sys.argv[1:]
    comments, subs = load()
    cur = {s.lower() for s in subs}

    if "--list" in args:
        for s in sorted(cur):
            print(s)
        print(f"({len(cur)} subscriber{'s' if len(cur) != 1 else ''})", file=sys.stderr)
        return 0

    if "--remove" in args:
        targets = {a.strip().lower() for a in args[args.index("--remove") + 1:]}
        kept = [s for s in subs if s.lower() not in targets]
        removed = len(subs) - len(kept)
        save(comments, kept)
        print(f"removed {removed}; list size {len({s.lower() for s in kept})}")
        return 0

    emails = [a for a in args if not a.startswith("-")]
    if not emails:
        print("Enter emails (one per line, blank line to finish):")
        try:
            while True:
                line = input("> ").strip()
                if not line:
                    break
                emails.append(line)
        except EOFError:
            pass

    added = 0
    for e in emails:
        e = e.strip()
        if not EMAIL.match(e):
            print(f"  skip (not an email): {e}")
        elif e.lower() in cur:
            print(f"  already on list: {e}")
        else:
            subs.append(e)
            cur.add(e.lower())
            added += 1
            print(f"  added: {e}")
    save(comments, subs)
    print(f"list size: {len(cur)} ({added} added)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
