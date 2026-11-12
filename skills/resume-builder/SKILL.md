---
name: resume-builder
description: Build a tailored, ATS-compatible resume from a job posting URL or pasted job description, using only facts from the career profile. Produces a fit/gap analysis and an ATS plain-text resume. Use when the user shares a job link, says "build a resume for", or "tailor my resume".
---

# Resume builder

Career root and write boundary: see `AGENTS.md`. Read `AGENTS.md` first.

## Steps

1. **Get the posting.** Fetch the URL. If it fails, requires login, or returns no job text (common for Workday/Greenhouse/Lever JS pages), ask the user to paste the description. Never guess posting content.
2. **Create the folder** `resumes/YYYY-MM-DD-<company>-<role-slug>/` and save `posting.md` (company, title, URL, location, comp if listed, full text).
3. **Extract requirements.** Must-haves, nice-to-haves, seniority signals (staff/principal/director, IC vs. manager), domain, tech stack, and the exact keywords an ATS will match.
4. **Map to evidence.** Read `profile/accomplishments.md`, `metrics.md`, and `positioning.md` if present. For each requirement: matching entry IDs and strength (strong / partial / gap). Write `fit-analysis.md`:
   - Fit score (1-10) with one-line reasoning
   - Level and comp notes (step up, lateral, step down)
   - Requirement -> evidence -> strength table
   - Gaps and handling (reframe, cover letter, honest omission)
   - Keywords covered, and keywords truthfully not covered
   - Positioning angle. Default: IC-heavy roles lead with building and technical depth, then leadership; leadership roles lead with scope and outcomes, keeping one hands-on proof point.
5. **Pause** and show the fit score, top gaps, and positioning in 5-8 lines. Proceed unless redirected.
6. **Write `resume-ats.txt`** in the format below, starting from `resumes/base/base-resume-ats.txt`:
   - Reorder and rewrite bullets to mirror posting language, using only ledger facts.
   - Summary: include if the posting is a pivot, seniority needs framing, or keyword density helps screening; 2-3 lines max. Otherwise omit.
   - Bullet budget per `AGENTS.md` Resume defaults (default: current role 5-7, older roles 1-3, oldest may be one line).
   - Bullet shape: strong verb + what + scale/metric + outcome. One line where possible, two max.
   - Page limit per Resume defaults (default: 1 preferred, 2 max).
7. **Sanitization check.** Search the txt for every term in `profile/sanitization.md` FORBIDDEN TERMS (case-insensitive). Fix hits. Confirm every number exists in `metrics.md`; Estimated values prefixed with "~"; never use Unverified or Immature metrics; Projections only as targets.
8. **Report** in a few lines: file path, what was emphasized, gaps to fill. Offer `ats-to-pdf`.

## ATS text format (required by the PDF converter)

```
FIRST LAST
City, ST | email | phone | linkedin

SUMMARY
One paragraph.

EXPERIENCE
Title | Company | City, ST | MMM YYYY - Present
- Bullet.

EDUCATION
Degree | School | Year

SKILLS
Category: item, item, item
```
- Dates (default): the current and previous role use `MMM YYYY - MMM YYYY` / `MMM YYYY - Present`; earlier roles use years only (`YYYY - YYYY`). Override in `AGENTS.md`.
- Every role line gets its own bullets directly beneath it. Never stack two role lines over a shared bullet list (readers attach the bullets to the bottom role). The current role always has at least one bullet of its own.
- Role lines render on ONE line. The last `|` segment (dates) is right-aligned; the converter shrinks the font to fit and warns if it cannot. Keep role lines under ~110 characters; if over, shorten the title or drop the city.
- Line 1: name. Line 2: contact. Section headers: ALL CAPS on their own line. Role lines contain `|`. Bullets start with `- `.
- Plain ASCII: no tables, columns, tabs, smart quotes, or special bullet glyphs.
- Standard section names (SUMMARY, EXPERIENCE, EDUCATION, SKILLS, CERTIFICATIONS).

## Rules

- Never invent titles, dates, employers, metrics, or tools. Missing facts become questions.
- Concrete tone; no buzzword stacking ("synergy", "passionate", "results-driven").
- Never name internal products, systems, regulations, or colleagues (see sanitization).
- Lapsed credentials: "formerly held" or omit.
