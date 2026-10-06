# Research brief template (paste at the top of every lane-agent prompt)

Fill in the angle-bracket fields, save it to the scratch directory, and tell each agent to read
it first. Then add the lane-specific part: what the lane covers, its state space and last
state, the lane rule (who led the last two issues), coverage debts it must pay, and the leads
from next-issue.md and the HN top 100 it should verify.

---

# Research brief: The Current Regime, issue <N> (week of Monday <YYYY-MM-DD> to Sunday <YYYY-MM-DD>)

Today is <date>. You are researching one lane of a weekly newsletter for developers and
professionals. Repo: <repo path> (read-only for you; do NOT edit repo files).
Useful context, read what you need:
- The previous issue's object for tone and shape:
  `python3 -c "import json;print(json.dumps(json.load(open('regime_state.json'))['issues'][-1],indent=1,ensure_ascii=False))"`
- Seed notes for this issue: next-issue.md
- The week's HN top 100 (points, title, url): <SCRATCH>/hn_top100.txt
- Feed pull: <SCRATCH>/sources.txt and <SCRATCH>/deepdive.txt

## Rules
- Budget: about 18 WebSearch calls. Use WebFetch freely for primary pages (no search cost). If a
  site blocks you, try `https://r.jina.ai/<url>`.
- Every fact you report needs: the exact claim, the outlet, the date of the event, the date of
  the article, and a URL you actually opened. Mark anything you could not open or confirm as
  UNVERIFIED.
- In-window means the event happened inside the issue week. Flag anything earlier as context,
  never as this week's news (the previous issue covered the week before; do not recycle it).
- Quotes: only words you saw verbatim on the page, in quote marks. Otherwise reported speech.
- No invented causation: if the source does not say X caused Y, do not say it.
- Numbers: give level, prior level and dates. Timezone matters for dates.
- Never guess a URL slug. Only report URLs you opened.

## Output
Write your dossier as markdown to <SCRATCH>/dossier_<lane>.md, then reply with a 10-line
summary. Structure: (1) recommended lead story + proposed state and why, (2) ranked candidate
stories with the verified facts above, (3) links list in importance order [title (Outlet,
Month D) | url | HN points if it was on HN], (4) things you checked and rejected, with reason.
