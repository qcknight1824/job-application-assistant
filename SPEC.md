# Career Agent Kit — specification.

A thinking map for any coding agent to build and run an evidence-backed career workspace for one person: a private record of their work, and a pipeline that turns that record into tailored, ATS-safe resumes, cover letters, and application answers.

This document explains **why** each piece exists so an agent can rebuild it faithfully, adapt it to a new person, and avoid the failure modes that shaped it. The templates and skills in this kit are the **what**.

---

## 1. THE CORE IDEA

Most AI resume tools generate from a prompt. That produces confident, generic, and often fabricated output. This kit inverts the flow:

```
  sources + conversation  ──►  private evidence record  ──►  tailored external documents
  (resume, docs, interview)    (ledger, metrics, stories)    (resume, cover letter, answers)
            ▲                                                          │
            └──────────────── gaps found while tailoring ◄─────────────┘
```

1. **The record is the product.** Resumes are disposable views over a durable, private record of accomplishments and numbers.
2. **Every external claim traces to a record entry.** If it isn't in the record, it can't go on a resume. Missing facts become questions, never inventions.
3. **Tailoring is a discovery loop.** Mapping a posting to the record exposes gaps. Asking about those gaps surfaces unrecorded experience, which is written back to the record. Each application makes the next one better. (Observed in practice: a fit score moved from 5 to 7 after three targeted gap questions surfaced modeling work the person had never written down.)
4. **Internal and external are separate vocabularies.** The record holds real names (internal products, systems, colleagues). Every entry also carries an external-safe phrasing. A sanitization file defines the boundary and is checked mechanically before anything leaves the machine.
5. **Ingested material is a draft, not a fact.** A resume, a document, or an assistant's summary is a source of claims. Only the owner's confirmation turns a claim into record.

---

## 2. INVARIANTS (never relax these)

| # | Invariant | Why |
|---|---|---|
| I1 | Never invent titles, dates, employers, metrics, tools, scope, or opinions | One fabricated claim found in an interview destroys credibility for the whole document |
| I2 | Every number used externally exists in `metrics.md` with an as-of date and status | Numbers drift; the ledger is the one place they are reconciled |
| I3 | `Estimated` numbers carry "~" or "roughly"; `Unverified`, `Immature`, and `Projection` numbers are never stated as achieved or used as fact | Prevents accidental overclaiming |
| I4 | External files pass the sanitization check before saving | Employers' internal names, regulations, and colleagues must not leak |
| I5 | Profile changes are proposed as diffs and applied only after the owner approves | The owner is the source of truth; the agent is the scribe |
| I6 | Never imply unapproved plans are approved, or planned work exists | Common overclaim ("led a 10-person expansion" when it was only pitched) |
| I7 | Write only inside the career root; every other folder is read-only evidence | Agents often start in a different CWD; career files must not land in work repos |
| I8 | Never open credential material (`.env`, keys, certs, `secrets/`), even in evidence folders | Evidence roots are often real code repos |
| I9 | For free-form answers and case questions, interview first; never substitute the agent's opinions for the owner's | These are judged on the candidate's thinking |
| I10 | Do not ingest or register employer material unless the owner states they may use it this way; when unsure, route to the harvest prompt or the interview | The agent cannot verify permission; the default must be the safe path |

---

## 3. ARCHITECTURE

### 3.1 Folder layout

```
<career-root>/
├── AGENTS.md                 entry point: roots, write boundary, read order, rules, skill router
├── README.md                 human-facing usage
├── applications.md           application tracker (one row per posting)
├── intake/                   optional starting material (private)
│   ├── sources/              owner-dropped files: resume, LinkedIn export, reviews, harvest output
│   ├── harvest-prompt.md     prompt to run in the owner's work AI assistant
│   ├── extracted.txt         raw text from sources, one SOURCE header per file (generated)
│   └── extract.md            index: roles found, claims with sources, conflicts, gaps (generated)
├── profile/                  SOURCE OF TRUTH (private)
│   ├── master-profile.md     identity, roles + dates, education, credentials, skills (with levels)
│   ├── accomplishments.md    ledger: the only source for resume bullets
│   ├── metrics.md            authoritative numbers, as-of dates, status, derivation
│   ├── narrative.md          career arc / leadership story (optional, high value)
│   ├── stories.md            STAR story bank, tagged by theme, linked to ledger IDs
│   ├── positioning.md        target roles, one-sentence story, top proof points
│   └── sanitization.md       internal -> external replacements + forbidden terms
├── journal/                  dated check-ins (raw notes + extracted facts)
├── exploration/              direction reports from browsing sessions
├── resumes/
│   ├── base/base-resume-ats.txt          master resume (the default view)
│   └── YYYY-MM-DD-<company>-<role>/      one folder per posting
│       ├── posting.md, fit-analysis.md, resume-ats.txt
│       ├── cover-letter.txt, responses.md, thought-experiment.md, interview-prep.md
│       └── <First> <Last>.pdf, <First> <Last> Cover Letter.pdf
├── tools/
│   ├── ats_to_pdf.py         deterministic txt -> PDF renderer
│   └── extract_text.py       DOCX / PDF / TXT / MD -> plain text with provenance headers
└── <agent skills dir>/       career-bootstrap, application-aid, resume-builder, career-checkin, ats-to-pdf
```

### 3.2 Layers and responsibilities

| Layer | Files | Changes when | Owner |
|---|---|---|---|
| Rules | `AGENTS.md`, `sanitization.md` | Rarely; when a new failure mode appears | Owner + agent |
| Source | `intake/*` | At bootstrap, or when new documents arrive | Owner drops files; agent extracts and indexes |
| Record | `profile/*` | After approved check-ins and gap answers | Agent proposes, owner approves |
| Views | `resumes/**`, `exploration/**` | Every application | Agent drafts, owner edits |
| Log | `journal/`, `applications.md` | Every session | Agent |
| Tooling | `tools/*.py` | Rarely | Code |

Keep rendering and text extraction in deterministic code, not agent judgment. Layout decisions an LLM makes ad hoc (fonts, spacing, wrapping) drift between runs, and an agent reading a DOCX natively often drops tables, headers, and text boxes, which is where contact details and skills tables hide. A small script does not.

### 3.3 Skills (workflow units)

| Skill | Role | Calls |
|---|---|---|
| `career-bootstrap` | First run: intake menu, extract and index sources, interview the owner, build `profile/`, write the first base resume | `tools/extract_text.py`, `resume-builder` format, `ats-to-pdf` |
| `application-aid` | Default entry point and orchestrator. Five modes (below) | `resume-builder`, `career-checkin`, `ats-to-pdf` |
| `resume-builder` | Posting -> fit analysis -> tailored ATS txt | — |
| `career-checkin` | Periodic interview -> journal -> profile diffs | — |
| `ats-to-pdf` | Render txt to PDF, enforce page and line limits | `tools/ats_to_pdf.py` |

`application-aid` modes:

| Mode | Trigger | Output |
|---|---|---|
| A — Apply | specific posting or program | packet with only the items the application asks for |
| B — Refresh | "update my resume" | check-in + base resume refresh |
| C — Rebuild | change in direction | positioning interview -> `positioning.md` -> new base (old one archived) |
| D — Explore fit | a link with no clear intent (default for ambiguous input) | `fit-analysis.md` with verdict: Apply / Apply with caveats / Pass |
| E — Browse | "not sure where to look" | 3-5 role archetypes, search strings, optional live scan |

---

## 4. DATA MODEL

The record is markdown so any agent can read and diff it without tooling. IDs make cross-references cheap and auditable.

### 4.1 Accomplishment entry (`accomplishments.md`)

```
### <ID> — <short name>
- **Internal:** what actually happened, with real names (private)
- **External:** one sanitized, resume-ready sentence
- **Metrics:** <metric IDs> | **Status:** Confirmed | Unverified | Estimated | Planned (+ caveats)
```

- IDs are prefixed per employer or era (e.g. `A01` current, `B01` prior) and never reused.
- Grouped under role headers that match `master-profile.md`.
- Roles with no recorded wins hold an explicit `Open question:` line. These drive future check-ins.
- Caveats live on the entry, e.g. "dataset confirmed / models planned — never imply models exist".
- Entries seeded from intake start `Unverified` and become `Confirmed` only through the owner's confirmation pass.

### 4.2 Metric row (`metrics.md`)

`| ID | Metric | Value | As of | Status | Derivation / source |`

| Status | External use |
|---|---|
| Confirmed | Yes |
| Derived | Yes; formula shown (e.g. `M06 / M05`) |
| Estimated | Only with "~" / "roughly", or confirm first |
| Unverified | No. Ingested from a resume, document, or assistant summary; not yet confirmed by the owner |
| Immature | No (sample too small or too recent) |
| Projection | Only as a target, never as achieved |

Derived metrics show the formula so inconsistencies are catchable. When a new number conflicts with existing ones, the agent says so before recording it.

### 4.3 Story (`stories.md`)

An index table (ID, theme tags, ledger refs) followed by STAR entries. Unresolved parts are marked `Open:` (e.g. "what the business did with the result"). Stories feed cover letters, free-form answers, and interview prep; tags let the agent pick the right one per prompt.

### 4.4 Sanitization (`sanitization.md`)

Three parts: a replacement table (internal -> external phrase), a flat FORBIDDEN TERMS list for mechanical search, and an allowed list (employers, public technologies). Forbidden terms cover internal product and system names, named regulations when sensitive, colleague names, internal URLs and identifiers.

### 4.5 Application row (`applications.md`)

`Date | Company | Role | Folder | Fit | Status | Next step | Notes`. Status: Exploring, Drafted, Submitted, Screening, Interviewing, Offer, Rejected, Withdrawn, Not pursued. Check-ins ask about open rows.

### 4.6 Intake extract (`intake/extract.md`)

Sources table (ID, file, type, document date); roles found (dates, company, title, which sources, conflicts); claims (ID `X01...`, role, claim quoted as stated, number, credit, source, priority, status); conflicts; not found.

- **Quote, don't improve.** No strengthened verbs, no rounding, no merging.
- **Credit** is one of led / built / contributed / supported / unclear. Documents show what happened, not what the owner did; credit is the most common source of resume overclaiming.
- **Priority:** 1 = high-impact claim with no number (interview first); 2 = has a number, needs confirmation; 3 = routine duty (usually skipped).
- **Conflicts are listed, never resolved by the agent.** Typical reliability, highest first: dated contemporaneous documents (reviews, promotion packets, dashboards) > harvest output > LinkedIn > resume. This ordering decides what to ask about first, not which value to keep.

---

## 5. WORKFLOW LOGIC (the thinking)

### 5.1 Evidence intake and bootstrap (new owner, empty record)

The highest-leverage moment. A thin record produces generic resumes forever. A resume is mostly claims ("improved efficiency", "led initiatives"); the substance is in the evidence behind them (documents, dashboards, reviews, the work itself) and in the owner's memory of the numbers. So the resume is treated as an outline, and the work is getting from outline to evidence.

#### 5.1.1 Sources, strongest first

| # | Source | Examples | Yields | Handling |
|---|---|---|---|---|
| 1 | Interview | role-by-role questions | numbers behind vague claims, credit, context | The only route to `Confirmed` |
| 2 | Work evidence | design docs, repos, dashboards, wikis (read-only) | scope and metrics the owner may not remember | High on scale; owner still confirms role and credit. Only with I10 satisfied |
| 3 | Self-authored records | performance reviews, promotion packets, brag docs, LinkedIn, decks | wins, numbers, recognition, with dates | Contemporaneous and specific; `Unverified` until confirmed |
| 4 | Harvest output | fact sheet the owner produced inside work tooling | same as 2 without exposing the source | Secondhand; `Unverified` |
| 5 | Resume | latest resume as PDF, DOCX, or pasted | role and date skeleton, claims | Claims are the owner's marketing; `Unverified` |

All are optional. Every path ends in the interview. Absent sources just mean more questions.

#### 5.1.2 The confidentiality boundary

Most people cannot, or should not, point a personal tool at employer systems. Some owners work in an approved environment where the agent can read work repos or docs as read-only evidence; most do not. The defaults:

1. Ask once what the owner may share. The agent cannot verify permission (I10).
2. If the owner says no or is unsure, use the **harvest prompt** or the interview. Do not register evidence roots.
3. The **harvest prompt** (`intake/harvest-prompt.md`) is run by the owner inside their work AI assistant, where the evidence already is. It returns only career facts: scope, accomplishments, numbers with their basis (stated / calculated / estimated), the owner's role in each, and gaps. Internal names are replaced with neutral labels, and it forbids personal data, identifiers, source code, credentials, non-public financials, and colleague or client names. The owner reviews and trims before anything leaves the work tool. An optional label map (internal term -> neutral label) speeds up the sanitization file; sharing it is the owner's call.
4. The kit grants no permission. The prompt tells the owner to check employer policy.
5. `intake/` is private, never quoted in external outputs, and can be deleted after bootstrap (keep `extract.md`).

#### 5.1.3 Document extraction

Run `tools/extract_text.py intake/sources -o intake/extracted.txt`. It handles DOCX (paragraphs and tables in document order, headings and bullets preserved, headers and footers, text boxes), PDF text layer, TXT, and MD, and emits a `=== SOURCE: path ===` header per file so every claim keeps its provenance. It skips credential-like files (I8).

It deliberately warns rather than guesses: scanned or empty PDFs, password-protected files, legacy `.doc`, and text-box layout. On any warning, or if the tool cannot run, the fallback is to ask the owner to paste the text or re-save the file. Never fill in unreadable content.

#### 5.1.4 Flow

1. **Scaffold and menu.** Create the layout; ask how the owner wants to start (resume, other documents, harvest prompt, interview only; any combination).
2. **Extract and index.** Write `intake/extract.md` (4.6). Show a 5-8 line summary: roles and dates, claim count, how many have numbers, conflicts, missing. Ask for corrections to roles and dates only.
3. **Seed drafts.** `master-profile.md`, `accomplishments.md`, `metrics.md`, all `Unverified`.
4. **Interview per role, newest first**, batches of 5-8 numbered questions, priority-1 claims first, skipping what the intake already answered. Cover scope, the 2-3 wins, the number behind each (before vs. after, compared to what, how measured), what changed, the owner's part, recognition. Push on vague answers once.
5. **Confirmation pass per role.** Show each `Unverified` claim and number to be used as a compact table; owner marks confirm / edit / drop. Only confirmed items become `Confirmed` with an as-of date.
6. **Sanitization file.** Seed candidates by scanning sources for product, system and project names, internal-looking URLs, client and colleague names, regulations (plus the label map if shared); owner adds and removes.
7. **Stories, positioning, first base resume.** Render it. Log open questions; they seed the first check-in.

### 5.2 Tailoring (resume-builder)

```
fetch posting -> save posting.md -> extract requirements -> map to ledger IDs
     |                                                         |
  (fetch fails -> ask for paste; never guess)           fit-analysis.md
                                                               |
                                 pause: score, top gaps, positioning (5-8 lines)
                                                               |
                                 gap questions -> record diffs (approved)
                                                               |
                      draft resume-ats.txt from base + ledger, mirroring posting language
                                                               |
                      sanitization + metric trace check -> report -> offer PDF
```

Fit analysis contents: score 1-10 with reasoning; requirement -> evidence -> strength (strong / partial / gap) table; how each gap is handled (reframe, cover letter, honest omission); keywords covered and **truthfully not covered**; positioning angle; level and comp notes.

Positioning heuristics (defaults; override in `positioning.md`):
- IC-heavy postings: lead with building and technical depth, compress leadership to one line.
- Leadership postings: lead with scope, team, influence, outcomes; keep one hands-on proof point.
- Pivot or seniority mismatch: add a 2-3 line summary to frame it. Otherwise omit the summary.

### 5.3 Packet building (application-aid Mode A)

| Item | Approach | Reason |
|---|---|---|
| Resume | Draft | Facts are in the record |
| Cover letter | Draft, owner edits | Structure is formulaic; voice is the owner's |
| Free-form answers | Interview first (2-3 questions per prompt), then draft | Graders look for the person, not polish |
| Thought experiment / case | Present a framework, collect the owner's reasoning per stage, then structure | Never substitute agent thinking |
| Interview prep | Offer after the packet; never block on it | Momentum |

Cover letter: 250-350 words; hook specific to the company and role; two proof points mapped to top requirements with metrics; concrete close. No "I am writing to apply", no resume recap.

Free-form: respect limits exactly and report the count; lead with the answer; evidence from a story; mirror the question's wording.

### 5.4 Check-in

Question priority: (1) Unknown/Open fields, oldest first, max 2 per session; (2) stale, Estimated, Immature, or Unverified metrics; (3) standard prompts: wins, new numbers, people, stakeholder moments, scope/title changes, setbacks, new skills; (4) open application rows. Output: dated journal entry (raw notes + extracted), then a compact diff list (file, ID, change). Apply on approval; update `Last updated`.

### 5.5 Review gate (every external file)

1. Case-insensitive search for every forbidden term. Fix hits.
2. Every number traces to a metric ID; Estimated has "~"; no Unverified or Immature; Projections framed as targets.
3. No unapproved plans implied.
4. Packet summary: files, word counts, open items.

---

## 6. ATS RESUME FORMAT (contract between agent and renderer)

```
FIRST LAST
City, ST | email | phone | linkedin

SUMMARY
Optional, 2-3 lines.

EXPERIENCE
Title | Company | City, ST | MMM YYYY - Present
- Strong verb + what + scale/metric + outcome.

EDUCATION
Degree | School | Year

SKILLS
Category: item, item, item
```

Parsing rules the renderer relies on: line 1 name, line 2 contact; ALL CAPS lines are headers; lines containing `|` are role lines (last segment right-aligned); `- ` lines are bullets; plain ASCII only.

Rules learned the hard way:
- **Every role line gets its own bullets directly beneath it.** Stacking two role lines (e.g. a promotion) over a shared bullet list makes readers and parsers attach all bullets to the bottom role. The current role always has at least one bullet of its own.
- **Role lines fit on one line.** The renderer shrinks all role lines uniformly and warns if one cannot fit at the minimum size. Fix by shortening the title or dropping the city, not by shrinking fonts. Aim under ~110 characters.
- **Date granularity:** month + year for the current and previous role; years only for older roles (less clutter, less age signal). Configurable.
- Bullet budget: current role 5-7, older roles 1-3, the oldest may collapse to one line. 1 page preferred, 2 max. Over 2 pages: propose specific cuts; never shrink fonts silently.
- Standard section names only (SUMMARY, EXPERIENCE, EDUCATION, SKILLS, CERTIFICATIONS).
- No buzzword stacking ("synergy", "passionate", "results-driven").
- Lapsed credentials are "formerly held" or omitted, never listed as active.

PDF naming: `<First> <Last>.pdf` and `<First> <Last> Cover Letter.pdf`, derived from line 1 of the resume txt in the same folder and written next to the source so each application folder is self-contained.

---

## 7. ADAPTING TO A NEW PERSON

| Item | Where | How |
|---|---|---|
| Career root path | `AGENTS.md` | Fill during bootstrap; absolute path |
| Starting material | `intake/sources/` | Owner's choice: resume, documents, harvest output, or nothing |
| Evidence roots (read-only) | `AGENTS.md` | Only if the owner states the material is permitted (I10) |
| Identity, roles, skills | `profile/master-profile.md` | Extracted sources + bootstrap interview |
| Forbidden terms | `profile/sanitization.md` | Seeded from sources, confirmed by the owner |
| Target roles and narrative | `profile/positioning.md` | Bootstrap step, then Mode C |
| ID prefixes per employer | `accomplishments.md` | One letter per employer or era |
| Date granularity, bullet budget, page limit | `AGENTS.md` -> Resume defaults | Defaults in section 6 |
| Agent tone | `AGENTS.md` -> Tone | Ask the owner once |
| Regional conventions (CV vs resume, photo, length) | `AGENTS.md` | Some markets expect 2-page CVs or different sections; set before the first build |

Skills never name the owner, an employer, or an absolute path. They reference "the career root" defined in `AGENTS.md`.

---

## 8. AGENT PORTABILITY

Skills use the common `SKILL.md` format (YAML frontmatter `name` + `description`, markdown body). Install by copying `skills/*` into the agent's skill directory:

| Agent | Skills location | Entry file |
|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md` | `CLAUDE.md` containing "Read AGENTS.md" |
| Snowflake Cortex Code | `.cortex/skills/<name>/SKILL.md` | `AGENTS.md` |
| Codex and other `AGENTS.md` readers | `skills/<name>/SKILL.md`, referenced from `AGENTS.md` | `AGENTS.md` |
| Continue / Cursor / others | rules or prompt files pointing to `skills/` | `AGENTS.md` |

Agents without native skill loading still work: `AGENTS.md` holds the router table, and the agent reads the skill file as a document when triggered.

Tool requirements: file read/write; optional web fetch (postings) and web search (Mode E); a shell with Python 3.10+ for the two scripts:
- PDF out: `uv run --with fpdf2 tools/ats_to_pdf.py <txt>` (or `pip install fpdf2`, then `python tools/ats_to_pdf.py <txt>`).
- Documents in: `uv run --with python-docx --with pypdf tools/extract_text.py <file-or-folder> -o <out>` (or `pip install python-docx pypdf`).

Without a shell, intake falls back to pasted text and PDFs the agent can read natively; PDF output is unavailable, but `resume-ats.txt` is still the deliverable. Everything else is markdown.

Headless use: every skill can run from a single message if inputs are supplied up front (posting text, application asks, answers to gap questions). Pauses are review points, not hard stops: "proceed unless redirected". If the agent cannot ask questions at all, it writes them to `open-questions.md` in the output folder and drafts with only confirmed facts.

---

## 9. FAILURE MODES THIS DESIGN PREVENTS

| Failure | Countermeasure |
|---|---|
| Fabricated or inflated metrics | I1-I3, metric trace check |
| Resume claims treated as facts | `Unverified` status, confirmation pass, never external until confirmed |
| Documents credit the team; resume credits the owner | Credit field (led / built / contributed / supported), asked in the interview |
| Sources disagree and the agent silently picks one | Conflicts listed in `extract.md` and asked, never resolved by the agent |
| Employer-confidential material pulled into a personal tool | I10, harvest prompt run inside the work tool, owner review before export, no default evidence roots |
| DOCX tables, headers, or text boxes dropped by native readers | Deterministic extractor with provenance headers |
| Scanned PDF or legacy `.doc` yields nothing, and the agent fills the gap | Extractor warns; fallback is paste or re-save; never guess |
| Internal names leaking | Dual phrasing per entry + mechanical forbidden-term search; sources never quoted externally |
| Job page fetch returns an empty JS shell (Workday, Greenhouse, etc.) | Detect missing job text -> ask for paste; never guess posting content |
| Generic answers to essay prompts | Interview-first for responses and cases |
| Rounded-up numbers drifting over time | As-of dates, derivations, stale-metric prompts in check-ins |
| Agent writes into the wrong repo | Single write root, absolute paths |
| Layout drift between runs | Deterministic renderer, strict txt contract |
| Bullets attached to the wrong role | Own-bullets-per-role rule |
| Record goes stale | Freshness check (~60 days) before browse/apply; check-in skill |
| Long back-and-forth burns the owner's time | Intake does the first pass; batched numbered questions; do all non-blocked work first |

---

## 10. REBUILD CHECKLIST (for an agent standing this up)

1. Create the layout in 3.1 at the owner's chosen root. Copy `templates/` (including `intake/`) into place and both `tools/*.py` into `tools/`.
2. Copy `skills/*` into the agent's skill directory (section 8).
3. Fill `AGENTS.md` placeholders: root path, tone, resume defaults. Add evidence roots only under I10.
4. Run `career-bootstrap`: offer the intake menu, extract, index, interview, confirm.
5. Render the base resume; confirm 1-2 pages and no warnings.
6. Run `application-aid` Mode D on one real posting to exercise the loop end to end.
7. Set a check-in cadence (monthly is a reasonable default).
