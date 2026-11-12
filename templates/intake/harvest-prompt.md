# Harvest prompt.

For people whose best evidence (documents, tickets, repos, dashboards, reviews) lives in work systems. You run this prompt **inside your work AI assistant**, where that material already is. It produces a career fact sheet with internal names replaced, which you review and trim before anything leaves the work tool.

## BEFORE YOU RUN IT

- Check your employer's policy on using AI assistants for this and on copying summaries out of work systems. This kit cannot grant permission. If in doubt, skip this and use the interview only.
- Use an approved tool only.
- Run it once per role (start with your two or three most recent). Fill in the `{{...}}` fields.
- Read the output before you copy it. Delete anything you are not comfortable sharing, or anything that looks wrong. The assistant can be mistaken or incomplete; you are the check.

## PROMPT (copy everything between the lines)

---

I am writing down my own career accomplishments for a personal resume. Using only material you can access that I authored or contributed to (documents, tickets, code repositories, dashboards, decks, status reports, my own performance reviews), produce a fact sheet for this role:

Role: {{TITLE}} at {{EMPLOYER}} ({{START MONTH/YEAR}} to {{END MONTH/YEAR or present}})
Focus areas, if any: {{OPTIONAL}}

Rules:
1. Report only what the material supports. If you cannot find something, write "not found". Do not estimate, round, or infer numbers.
2. Do not include: customer or employee personal data, account or system identifiers, source code, credentials, internal URLs, non-public financial results, names of colleagues or clients, security details, or anything marked confidential or restricted.
3. Replace internal product, system, project, and team names, and regulation names, with neutral labels (for example "the internal case-management system", "Project A"). Record each replacement in section C.
4. If an exact figure may be sensitive, give a magnitude or range ("~10K", "low millions") and say that you did.
5. For every number, say how it is known: STATED in a document, CALCULATED from figures in a document (show the formula), or ESTIMATED (not in any document).
6. Describe my role precisely in each item: led, built, contributed, or supported. If the material does not show what my part was, write "role unclear".

Output exactly this structure:

A. SCOPE OF ROLE
Team size and my reports, users or customers served, data or transaction volume, budget or geography, tools and methods that appear repeatedly. Only what the material shows.

B. ACCOMPLISHMENTS (5 to 15, most significant first)
For each:
- What was done (verb + object) and my role (led / built / contributed / supported / role unclear)
- Before and after, or scale
- Numbers: value | unit | period | basis (STATED / CALCULATED / ESTIMATED) | source type (kind of document, not file name)
- Outcome: decision made, money, risk, time saved, adoption
- Recognition, if any
- Confidence: high / medium / low

C. LABEL MAP (private)
Each internal term you replaced -> the neutral label you used.

D. GAPS
Questions a hiring manager would ask about this role that the material does not answer.

---

## AFTER IT RUNS

1. Review and trim. Fix anything wrong.
2. Save sections A, B, and D to `intake/sources/harvest-<role>.md` (or paste them into the chat).
3. Section C is optional. It lists internal names, so share it only if you are comfortable doing so; it makes the "never put these on a resume" list faster to build. If you skip it, the agent will ask for those terms in the interview.
4. Treat everything as **unverified** until you confirm it in the interview. Output from an assistant is a draft of your record, not the record.
