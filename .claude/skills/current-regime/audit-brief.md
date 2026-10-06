# Audit brief template (one auditor per lane group)

Dump the auditor's sections of the draft issue to a scratch file first, e.g.
`python3 -c "import json;i=json.load(open('regime_state.json'))['issues'][-1];print(json.dumps({k:i[k] for k in ['wildcard','briefs','undercurrent']},indent=1,ensure_ascii=False))" > $S/audit_misc.json`
and include `python3 validate_issue.py --quotes` output for those sections.

Lane groups: (1) AI & compute + GitHub line + AI watchlist cards; (2) geopolitics + trade
radar + watch_next; (3) markets + commodities + market_moves + monetary/energy radar + chart;
(4) deep-dive + wildcard + undercurrent + briefs + annotations.

---

You are an adversarial fact-checker for a newsletter issue covering <week>. Assume every
sentence is wrong until a source you open shows it is right. Your sections: <file>.

For every sentence check, against the cited URL or a primary source you find:
1. Every number, its unit, and its date (is the date the event's date, in the right timezone?).
2. Every quote: is it verbatim on the page? Paraphrase inside quote marks is an error.
3. Every attribution: did that outlet or person say it, or someone else?
4. Every causal claim ("after", "because", "as a result of", "on"): does a source make the link?
5. Every superlative ("record", "highest since", "first", "only"): verify against the data.
6. Window: did the event happen inside <week>? Was it already covered in the previous issue?
7. Every link: does it open, and does the page support the sentence that cites it?
8. Futures and market numbers: explicit contract months, Friday-to-Friday closes.

Budget: about 20 WebSearch calls; WebFetch freely; `https://r.jina.ai/<url>` for blocked sites.

Report ONLY problems, each as:
- OLD: exact text as it appears in the JSON (copy-paste, so a script can find it)
- NEW: replacement text (same style: no em-dashes, plain language)
- WHY: one line, with the source URL
Also list what you checked and confirmed, in one line each, so the editor knows coverage.
Write the report to <SCRATCH>/audit_<group>.md and reply with the count of problems.
