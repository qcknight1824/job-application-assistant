---
name: career-checkin
description: On-demand career check-in. Interviews the user with 5-8 adaptive questions, writes a dated journal entry, and proposes diffs to the profile files. Use when the user says "check in", "career update", "log a win", or "update my profile".
---

# Career check-in

Career root and write boundary: see `AGENTS.md`. Read `AGENTS.md` first.

## Steps

1. **Load context.** Read `profile/master-profile.md`, `accomplishments.md`, `metrics.md`, `narrative.md` (if present), and the most recent file in `journal/`. Note the date of the last check-in.
2. **Build the question set (5-8).** Prioritize:
   - Open questions / Unknown fields in the profile (oldest first, max 2 per session).
   - Metrics whose as-of date is stale or marked Estimated/Immature/Unverified.
   - Standard prompts: wins since last check-in; new numbers; people (hires, coaching, team changes); executive or stakeholder moments; scope or title changes; setbacks and lessons; new skills or tools.
   - Open rows in `applications.md` (Submitted, Screening, Interviewing): ask for status and update the tracker.
   - Any win with a clear situation/action/result: propose a new `stories.md` entry.
   Ask in one message, numbered, concise. Say short rough answers are fine.
3. **Write the journal entry** at `journal/YYYY-MM-DD-checkin.md` (append `-2` if one exists today):
   ```
   # Check-in YYYY-MM-DD.
   ## RAW NOTES
   <answers, lightly cleaned>
   ## EXTRACTED
   - Wins: ...
   - Metrics: ...
   - People: ...
   - Open questions remaining: ...
   ```
4. **Propose profile diffs.** Compact list: file, entry ID (new or existing), change. New accomplishments get the next ID in that role's prefix, with internal + external phrasing, metric IDs, and status. New numbers go to `metrics.md` with as-of date, status, and derivation. External phrasing must comply with `profile/sanitization.md`. New internal names mentioned -> propose adding them to FORBIDDEN TERMS.
5. **Apply only after approval** (all, some, or edited). Update `Last updated` in `master-profile.md`.
6. **Close** with one line: what changed, and the top remaining gap.

## Rules

- Never invent or round up numbers. Derived metrics show the formula.
- Challenge vague claims: ask for a number, a scale, or a before/after.
- If a metric looks inconsistent with existing data, say so before recording it.
