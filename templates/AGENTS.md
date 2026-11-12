# Career workspace agent entry point.

Owner: {{OWNER_NAME}}. Purpose: maintain an evidence-backed career record and produce tailored, external-safe resumes.

## ROOTS AND WRITE BOUNDARY

| Root | Path | Access |
|---|---|---|
| career | `{{CAREER_ROOT_ABSOLUTE_PATH}}` | Read/write (only write target) |
| evidence (optional) | `{{EVIDENCE_PATH}}` | Read-only |

- Always use absolute paths. The agent's default CWD may be elsewhere; never write career files outside the career root.
- Never open credential material: `.env`, keys, certs, tokens, `secrets/`.

## SOURCE OF TRUTH

Read in this order before any task:
1. `profile/master-profile.md` — roles, dates, education, skills
2. `profile/accomplishments.md` — accomplishment ledger (the only source for resume bullets)
3. `profile/metrics.md` — authoritative numbers with as-of dates
4. `profile/narrative.md` — career arc (optional)
5. `profile/stories.md` — STAR story bank
6. `profile/positioning.md` — target roles and narrative (if present)
7. `profile/sanitization.md` — mandatory for anything external-facing
8. `applications.md` — application tracker

If `master-profile.md` is missing or still a template, run `career-bootstrap`.

## RULES

- **Never invent metrics, titles, dates, or scope.** If a resume needs a fact the profile lacks, list it as a gap and ask.
- Every number used externally must exist in `metrics.md`. Estimated values are phrased as approximate ("~", "roughly"). Unverified and Immature metrics are never used externally; Projections only as targets.
- `intake/` holds owner-supplied source material. It is private, never quoted in external outputs, and never published. Only the confirmed ledger feeds resumes.
- **External outputs must pass `sanitization.md`.** No internal product, system, regulation, or colleague names, internal URLs, or data.
- Internal record files (`profile/`, `journal/`) may hold internal names; they never leave this machine. Do not publish this folder.
- Profile updates are proposed as a diff and applied only after the owner approves.
- Never imply unapproved plans are approved or planned work exists.
- Tone: {{TONE, e.g. "concise, direct, no emojis, no sycophancy; disagree with reasoning when warranted"}}.

## RESUME DEFAULTS

- Page limit: 1 preferred, 2 max.
- Bullets: current role 5-7, older roles 1-3, oldest may be one line.
- Dates: month + year for current and previous role; years only for older roles.
- Region conventions: {{e.g. "US resume, no photo"}}.

## SKILLS

| Skill | Trigger | Output |
|---|---|---|
| `career-bootstrap` | first run, "set up", empty profile | populated `profile/`, first base resume |
| `application-aid` | **default entry point**: "apply to", "help me apply", "refresh / rebuild my resume", a job link | Mode A packet, B refresh, C rebuild, D fit verdict, E directions |
| `career-checkin` | "check in", "career update", "log a win" | `journal/YYYY-MM-DD-checkin.md` + approved profile diffs |
| `resume-builder` | called by `application-aid`, or "just the resume" | `resumes/<date>-<company>-<role>/` with posting, fit analysis, ATS txt |
| `ats-to-pdf` | "make the PDF" | `<First> <Last>.pdf` / `<First> <Last> Cover Letter.pdf` next to the source |
