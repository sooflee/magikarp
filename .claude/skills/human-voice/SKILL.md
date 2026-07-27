---
name: human-voice
description: Use BEFORE writing or editing any reader-facing prose (newsletter issues, site copy, ledger entries, README text, emails). A checklist for stripping machine-writing tells, distilled from Wikipedia's "Signs of AI writing", adapted to this project's house style. Also use when the user asks to "de-AI" or humanize a piece of text.
---

# Human voice — write like a person who knows the material

The tells below share one root: text that **performs meaning instead of stating
it**. The fix is always the same — replace the gesture with the concrete fact
(the named actor, the number, the dated event). If a sentence could appear
unchanged in an article about a different subject, it is filler; cut it or make
it specific.

Wikipedia's editors catalogued these as the reliable signs of machine prose
(en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). They are tells, not
proof — humans write this way too, which is exactly why the goal is removing
the pattern, not passing a detector.

## Vocabulary to never use

delve, tapestry, pivotal, crucial, testament, underscore/underscores,
showcase, foster, vibrant, nestled, boasts, rich heritage, robust, seamless,
comprehensive (as praise), game-changing, cutting-edge, landscape or ecosystem
(as metaphor), navigate (as metaphor), leverage (as a verb), enhance,
align with, empower, elevate, "in today's …" and "in the world of …" openers.
Additionally / Moreover / Furthermore as paragraph glue — start with the fact
instead.

## Constructions to never use

- **Negative parallelism**: "not just X but Y", "not X — it's Y",
  "no A, no B, just C". State what the thing is.
- **Rhetorical "X rather than Y"** used for contrast-as-flourish
  ("consolidation rather than ideological purity"). Fine only for literal
  choices between two named options.
- **Rule of three**: triads of adjectives, phrases, or clauses deployed for
  rhythm. Two concrete items beat three vague ones.
- **Copula avoidance**: "serves as", "stands as", "functions as",
  "represents a", "marks a" → write "is" or "was".
- **Present-participle commentary** bolted to a fact: ", highlighting …",
  ", underscoring …", ", emphasizing …", ", reflecting …", ", cementing …",
  ", fostering …". Either the observation is a fact — give it its own plain
  sentence — or it's air; cut it.
- **Significance inflation**: "a pivotal moment", "a significant shift",
  "part of a broader trend/conversation", "solidified its reputation". If it
  matters, the number or event that shows it matters belongs there instead.
- **Dramatic colon reveal**: "The result: …", "The catch: …",
  "The market noticed: …". Write the sentence.
- **Vague attribution**: "observers note", "experts say", "industry reports",
  "critics argue". Name the source and date it, or drop the claim.
- **Outline conclusions**: "Despite these challenges … the future …",
  "Looking ahead …". End on the last fact worth knowing.
- **Elegant variation**: cycling synonyms to avoid repeating a word
  ("the rocket … the vehicle … the launcher"). Repeat the plain word.
- **Editorializing adverbs**: conspicuously, notably, remarkably,
  significantly, importantly. If the reader can't see it from the fact, the
  adverb won't help.

## Formatting tells

- No em-dashes (house rule; also a known tell). No curly-quote artifacts.
- Sentence case in headings, never Title Case.
- No walls of **bold-term:** bullets; prefer prose, or a plain list.
- No emoji as section markers or list bullets.
- No table where a sentence would do.

## The self-edit pass (run over every draft)

1. **First sentence test**: does it state a dated, named, or numbered fact?
   Theme-restatement openers ("The week turned on a reversal.") carry no
   information — the headline already frames the theme.
2. **Sweep** the draft for the lists above:

   ```
   grep -inE "delve|tapestry|pivotal|crucial|testament|underscor|showcas|foster|vibrant|nestled|boasts|robust|seamless|leverag|enhanc|align with|empower|game-chang|cutting-edge|landscape|ecosystem|navigat|additionally|moreover|furthermore" draft.txt
   grep -inE "not (just|only|merely) [^.]{3,60}, but|no [a-z]+[^.]*, no [a-z]+|serves as|stands as|functions as|represents a|marks a|, (highlighting|underscoring|emphasizing|reflecting|cementing|fostering)|observers|experts (say|note)|industry reports|despite (these|its) challenges|conspicuous|notabl|remarkabl|The (result|catch|upshot):" draft.txt
   grep -c "—" draft.txt
   ```

3. **Anything-article test**: sentence by sentence, ask whether it could
   describe any subject. Generic sentences get cut or get a number.
4. **Claims**: every claim bounded and traceable to a named, dated source —
   never "reports suggest".
5. **Read it aloud once**: machine prose has even, unbroken rhythm; a human
   paragraph varies sentence length. If every sentence is medium-long with two
   clauses, break some.

For this repo specifically: run the pass over headlines, summaries,
implications, geopolitics comments, watchlist cards, and ledger entries before
`build_site.py` / `send_regime_email.py`, alongside the link lint.
