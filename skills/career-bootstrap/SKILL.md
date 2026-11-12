---
name: career-bootstrap
description: First-run setup for a new career workspace. Offers an intake menu (existing resume, other career documents, a harvest prompt to run in work tooling, or interview only), extracts and indexes what the user provides, interviews role by role, and builds the profile record, sanitization rules, and first base resume. Use when the user says "set up my career workspace", "start from scratch", "bootstrap", or when profile/master-profile.md is missing or still a template.
---

# Career bootstrap

Goal: a profile rich enough that every later resume is tailored from evidence, not generated from a prompt. The resume (if any) is an outline; evidence and the interview are the substance. Spend the effort here.

## STEP 1 — Root and scaffold

1. Ask for the career root (absolute path) if `AGENTS.md` does not define one. Confirm it is not inside a work repo or a shared drive the user doesn't control.
2. If missing, create: `profile/`, `journal/`, `exploration/`, `resumes/base/`, `intake/sources/`, `tools/`. Copy templates from the kit (`templates/*`, including `intake/`) to the matching locations, and `tools/ats_to_pdf.py` and `tools/extract_text.py` into `tools/`. If the user versions the workspace with git, install `templates/gitignore.template` as `.gitignore` at the career root (it keeps `profile/`, `journal/`, `intake/`, `resumes/`, and `applications.md` out of commits).
3. Fill `AGENTS.md` placeholders: owner name, root path, tone preference, resume defaults (ask only about regional conventions and page limit; keep other defaults).

## STEP 2 — Intake

### 2.1 Menu (one message)

> How do you want to start? Pick any combination; every path ends in a short interview.
> 1. **I have a resume.** Put it in `intake/sources/` (PDF, DOCX, TXT, MD) or paste it.
> 2. **I have other career documents.** LinkedIn export, performance reviews, promotion packets, brag docs, decks, award notes. Same folder, or paste.
> 3. **My best evidence lives in work systems.** I'll give you a prompt to run in your work AI assistant. It returns career facts only, with internal names replaced, so you can review and trim before anything leaves the work tool.
> 4. **Interview only.**
>
> Only share employer material your employer permits. If you're unsure, choose 3 or 4.

Do not register read-only evidence roots in `AGENTS.md` unless the user states the material is permitted for this use. Never open credential material (`.env`, keys, certs, `secrets/`).

### 2.2 Read the files

- DOCX: always use the extractor. PDF/TXT/MD: native read is fine; use the extractor if the native read is garbled.
  ```
  uv run --with python-docx --with pypdf tools/extract_text.py intake/sources -o intake/extracted.txt
  ```
  (Without uv: `pip install python-docx pypdf`, then `python tools/extract_text.py ...`.) Read `intake/extracted.txt`; each source sits under a `=== SOURCE: ... ===` header.
- Read the script's WARNING and ERROR lines (stderr) and act on each: a scanned or empty PDF, legacy `.doc`, an unreadable or password-protected file, or a missing library (install it or re-run with `uv --with`) -> ask the user to paste the text or re-save the file. A file with a warning produces no extracted text; never assume it was read. If the tool cannot run at all, ask for pasted text. Never guess at unreadable content.

### 2.3 Harvest prompt (if option 3)

Show the prompt from `intake/harvest-prompt.md` (the part between the lines) and its "before you run it" notes. Ask them to run it per role, most recent two or three first, review and trim the output, and save it as `intake/sources/harvest-<role>.md` or paste it. Do not wait: continue with the other sources and interview, and fold the harvest in when it arrives. Harvest output is secondhand: treat it as `Unverified`.

### 2.4 Index

Write `intake/extract.md` from the template: sources, roles found, and one row per distinct claim, quoted as stated, with number, role credit (led / built / contributed / supported / unclear), source, and priority. Do not strengthen verbs, round numbers, or merge claims. List conflicts between sources and what is missing. When sources disagree, record both and ask; do not choose.

### 2.5 Confirm the skeleton (short)

Show 5-8 lines: roles and dates found, number of claims, how many have numbers, conflicts, what is missing. Ask for corrections to roles and dates only; details come in the interview.

### 2.6 Seed draft profile files

- `master-profile.md`: identity, roles and dates, education, credentials, skills.
- `accomplishments.md`: one entry per priority 1-2 claim, ID prefixed per employer (A = most recent, B = previous, ...). Status `Unverified`.
- `metrics.md`: every number found, status `Unverified`, with the source file.

## STEP 3 — Role interviews (newest first)

One message per role, 5-8 numbered questions, adaptive to the intake. Order: priority 1 claims from `extract.md` first (high-impact, no number), then the standard prompts the intake did not already answer:
1. Scope: team size, reports, budget, users, data or transaction volume, geography.
2. The 2-3 things you'd most want a hiring manager to know from this role.
3. For each: the number behind it (before vs. after, compared to what, how measured).
4. What changed because of it (decision, revenue, risk, time, adoption).
5. Your part: led, built, contributed, or supported? Documents show what happened, not what you did.
6. Recognition: awards, promotions, being asked to expand scope.
7. Tools and methods used hands-on vs. delegated.

Push on vague answers once ("roughly how many?"). Unknowns become `Open question:` lines; do not block on them. Roles older than ~10 years or low relevance: 2-3 questions max.

**Confirmation pass (per role):** show every `Unverified` claim and number you intend to use in a compact table (ID, claim, value) and ask for confirm / edit / drop. Confirmed -> status `Confirmed` with an as-of date. Edited -> record the new value. Dropped -> remove. Ingested numbers are never used externally until confirmed.

After each role, show proposed entries (internal + external phrasing, metric rows with status and derivation). Apply on approval.

## STEP 4 — Sanitization

Seed candidates from the intake: scan the sources for product, system, and project names, internal-looking URLs and identifiers, client and colleague names, and regulations; add the harvest label map if the user shared it. Show the candidates and ask (one message): what to add or remove; any other internal names; anything the employer would not want public. Write `profile/sanitization.md` (replacements table, FORBIDDEN TERMS, allowed list). Check every external phrasing in the ledger against it.

## STEP 5 — Stories and narrative

From the confirmed entries, propose 4-8 STAR stories in `stories.md` with theme tags (influence, scale, ambiguity, failure/lesson, technical depth, leadership, speed). Ask 2-3 questions to fill the weakest themes. Optionally draft `narrative.md` (career arc in 5-10 bullets) and confirm.

## STEP 6 — Positioning (short)

Ask: target role families and level; one-sentence story for a recruiter; roles or eras to de-emphasize. Write `profile/positioning.md`.

## STEP 7 — First base resume

Write `resumes/base/base-resume-ats.txt` using the `resume-builder` format and rules, driven by positioning. Run the review gate (sanitization, metric trace). Render with `ats-to-pdf`. Report page count, open questions, and the top 3 gaps to fill at the first check-in. Set `Last updated` in `master-profile.md`. Offer to delete `intake/sources/` (keeping `extract.md`).

## RULES

- Never invent facts. Anything ingested stays `Unverified` until the user confirms it.
- Source files in `intake/` are never quoted in external outputs; only the ledger's external phrasing is.
- Batch questions; tell the user rough answers are fine.
- Save progress after each step so the session can resume.
