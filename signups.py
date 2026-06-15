#!/usr/bin/env python3
"""Ingest newsletter sign-ups and unsubscribes from Gmail over IMAP.

The site's "Subscribe" button opens a pre-filled email with the subject
"subscribe" (and the List-Unsubscribe header uses subject "unsubscribe"). This
script reads those messages with the same Gmail app password used to send,
updates subscribers.txt, and marks the messages read so they are not reprocessed.

Usage:
    export GMAIL_APP_PASSWORD="..."
    python3 signups.py            # process new subscribe/unsubscribe mail
    python3 signups.py --dry-run  # show what would change, write nothing
"""

import email
import email.utils
import imaplib
import os
import sys
from pathlib import Path

ACCOUNT = "bensonw.dev@gmail.com"
SUBSCRIBERS = Path(__file__).resolve().parent / "subscribers.txt"
IMAP_HOST = "imap.gmail.com"


def load():
    subs, comments = [], []
    if SUBSCRIBERS.exists():
        for line in SUBSCRIBERS.read_text().splitlines():
            s = line.strip()
            if s.startswith("#") or not s:
                comments.append(line)
            elif "@" in s and s.lower() not in [x.lower() for x in subs]:
                subs.append(s)
    return comments, subs


def save(comments, subs):
    body = "\n".join(comments + sorted(set(subs), key=str.lower)) + "\n"
    SUBSCRIBERS.write_text(body)


def fetch_requests(app_password):
    """Return (subscribes, unsubscribes) sender-address sets from unread mail."""
    subs, unsubs = set(), set()
    M = imaplib.IMAP4_SSL(IMAP_HOST)
    M.login(ACCOUNT, app_password)
    M.select("INBOX")
    # unread messages whose subject mentions (un)subscribe
    typ, data = M.search(None, '(UNSEEN SUBJECT "subscribe")')
    ids = data[0].split() if data and data[0] else []
    for num in ids:
        typ, raw = M.fetch(num, "(RFC822)")
        if not raw or not raw[0]:
            continue
        msg = email.message_from_bytes(raw[0][1])
        sender = email.utils.parseaddr(msg.get("From") or "")[1].strip().lower()
        # normalize subject: drop Re:/Fwd: prefixes and surrounding punctuation
        subj = (msg.get("Subject") or "").strip().lower()
        while subj.startswith(("re:", "fwd:", "fw:")):
            subj = subj.split(":", 1)[1].strip()
        subj = subj.strip(" .!\t")
        # exact match only, so marketing mail like "Subscribe to Bloomberg" is ignored
        if subj == "unsubscribe":
            unsubs.add(sender)
        elif subj == "subscribe":
            subs.add(sender)
        else:
            continue                        # leave unrelated mail untouched (stays unread)
        M.store(num, "+FLAGS", "\\Seen")    # mark the real request processed
    M.logout()
    return subs, unsubs


def main() -> int:
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print("ERROR: set GMAIL_APP_PASSWORD first.", file=sys.stderr)
        return 1
    dry = "--dry-run" in sys.argv

    subs, unsubs = fetch_requests(app_password)
    comments, current = load()
    cur_lower = {x.lower() for x in current}

    added = [s for s in subs if s not in cur_lower and s not in unsubs]
    removed = [x for x in current if x.lower() in unsubs]

    for a in added:
        current.append(a)
    current = [x for x in current if x.lower() not in unsubs]

    print(f"sign-ups: +{len(added)}  unsubscribes: -{len(removed)}  "
          f"list size: {len(set(x.lower() for x in current))}")
    for a in added:
        print(f"  + {a}")
    for r in removed:
        print(f"  - {r}")

    if dry:
        print("(dry-run, nothing written)")
    else:
        save(comments, current)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
