---
name: application-aid
description: End-to-end job and program application assistant. Default entry point for applying to a specific job or program, refreshing or rebuilding the resume, exploring fit for one posting, or browsing for career direction. Produces resumes, cover letters, free-form responses, thought-experiment answers, fit verdicts, direction reports, and optional interview prep. Use when the user says "apply to", "application", "help me apply", "cover letter", "refresh my resume", "rebuild my resume", "am I a fit", "what should I look for", "browsing", or shares a job/program link.
---

# Application aid

Career root and write boundary: see `AGENTS.md`. Read `AGENTS.md` and all of `profile/` first. If `profile/master-profile.md` is missing or still a template, run `career-bootstrap` instead.

This skill orchestrates. It calls `resume-builder`, `career-checkin`, and `ats-to-pdf` as steps; follow those skills' rules when you reach them.

## STEP 0 — Mode

Ask one question:
> What are we doing today? **A)** Applying to a specific job or program, **B)** refreshing the resume with recent work, **C)** totally rebuilding the resume, **D)** exploring my fit for a specific job, **E)** just browsing — not sure where to start.

If the answer is ambiguous (e.g. a link with no intent), default to D and offer to escalate to A.

---

## MODE A — Specific job or program

### A1. Intake (one message)
Ask for:
1. Link or pasted posting/program description.
2. What the application requires: resume, cover letter, free-form questions (with any character/word limits), thought experiment or case, portfolio links, salary expectation, other.
3. Context the posting will not show: referral or contact, recruiter notes, deadline, why this role interests them.

### A2. Fit read
Run `resume-builder` steps 1-5. Show fit score, top gaps, and positioning in 5-8 lines. If fit <= 4, ask whether to continue before building.

### A3. Gap questions (3-6)
Generated from the fit gaps and the application's specific asks, never generic. Example: "Have you ever run an A/B test or measured before/after impact, even informally?" New facts -> propose ledger/metrics/stories diffs; apply after approval.

### A4. Build the packet (only items the application requires)
All files go in the application folder.

| Item | Mode | File |
|---|---|---|
| Resume | Draft (via `resume-builder` steps 6-7) | `resume-ats.txt` |
| Cover letter | **Draft first**, user edits | `cover-letter.txt` |
| Free-form responses | **Interview first**: 2-3 questions per prompt, then draft in the user's voice | `responses.md` |
| Thought experiment / case | **Interview first**: present a framework, collect the user's reasoning, then structure it. Never substitute your own thinking | `thought-experiment.md` |

**Cover letter:** 250-350 words. (1) Hook specific to the company/role and why them; (2-3) two proof points mapped to the top requirements, with metrics from `metrics.md`; (4) close with a concrete ask. No "I am writing to apply", no restating the resume. Format for PDF: line 1 name, line 2 contact, then plain paragraphs.

**Free-form responses:** respect limits exactly (report the count). Lead with the answer, then evidence from `stories.md`. Mirror the question's language.

**Thought experiment framework:** clarify the question -> assumptions -> approach/method -> metrics and validation -> risks and trade-offs -> recommendation. Ask for the user's take at each stage before writing.

### A5. Review gate
- Sanitization check on every external file (`profile/sanitization.md` forbidden terms, case-insensitive).
- Every number traces to `metrics.md`; Estimated values carry "~"; no Unverified or Immature metrics; Projections only as targets.
- Short packet summary (files, word counts, open items).
- Offer `ats-to-pdf` for resume and cover letter.

### A6. Log and close
- Add or update the row in `applications.md` (status `Drafted` unless the user says submitted).
- **Ask** whether they want interview prep. Optional; never block the packet on it. If yes, write `interview-prep.md`: likely questions by theme, mapped story IDs, gaps to rehearse, 3-5 questions to ask the interviewer.

---

## MODE B — Refresher

1. Run `career-checkin` (its questions plus: anything to retire from the resume, new tools/skills, title or scope changes, applications that moved).
2. After profile diffs are approved, update `resumes/base/base-resume-ats.txt` from the ledger. Show a short before/after of changed bullets.
3. Review gate; offer the PDF.

## MODE C — Full rebuild

1. Positioning interview (one message): target role families and level; what they want more and less of; deal-breakers (comp floor, level, location, remote); the one-sentence story they want a recruiter to repeat; roles or eras to de-emphasize.
2. Write `profile/positioning.md` (target roles, narrative, top 5 proof points, keywords) and get approval.
3. Archive the current base to `resumes/base/archive/YYYY-MM-DD-base-resume-ats.txt`, then write a new base from the ledger and positioning.
4. Review gate; offer the PDF.

## MODE D — Explore fit for a specific job

Fit only; no packet unless the user escalates.

1. Get the posting. Create the folder and `posting.md` as in `resume-builder` step 2.
2. Write `fit-analysis.md` (`resume-builder` step 4) plus a **Verdict** section:
   - Fit score 1-10 with breakdown: must-have coverage, nice-to-have coverage, level match, domain match, comp/location match (if known).
   - Recommendation: **Apply**, **Apply with caveats**, or **Pass**, with one-line reasoning.
   - What would move the score: unrecorded experience to ask about vs. true gaps.
3. Ask 2-4 gap questions; if answers change the score, update it and the profile (with approval).
4. Log in `applications.md` with status `Exploring`.
5. Offer: escalate to Mode A, or Mode E for similar roles.

## MODE E — Browsing / direction finding

1. **Freshness check.** Compare `master-profile.md` "Last updated" and the latest journal date to today. If older than ~60 days, or many Unknowns matter, recommend Mode B first; proceed if declined.
2. **Direction questions (one message, 4-6):** more/less of; IC vs. people leadership; industries in or out; level and comp floor; location/remote; timeline.
3. **Directions.** 3-5 role archetypes ranked by fit, each with: typical titles; why it fits (ledger IDs) and the main gap; level and rough comp band (labeled estimate unless sourced); example company types (named companies only from a fetched source); search strings and ATS keywords.
4. **Optional live scan.** 1-3 web searches per top archetype; list real postings (title, company, link). Never fabricate postings.
5. Write `exploration/YYYY-MM-DD-directions.md`. Recommend which archetype should drive the base resume; offer Mode C or Mode D.

---

## RULES

- Ask questions in batches, numbered, concise. Rough answers are fine; say so.
- Never invent facts, metrics, stories, or opinions. Missing facts become questions.
- If the agent cannot ask questions (headless), write them to `open-questions.md` in the output folder and draft using confirmed facts only.
- New stories go to `profile/stories.md` with a new ID after approval.
- Keep momentum: do everything that doesn't depend on an unanswered question first.
