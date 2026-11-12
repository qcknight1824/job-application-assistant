# Career Agent Kit

An agent-agnostic kit for building an evidence-backed career workspace and generating tailored, ATS-safe resumes, cover letters, and application answers from it.

The difference from typical AI resume tools: nothing is generated from a prompt. The agent interviews you, keeps a private ledger of what you actually did and the numbers behind it, and builds every resume as a view over that ledger. Each application surfaces gaps, the agent asks about them, and the record gets better.

Read [SPEC.md](SPEC.md) for the design and reasoning. It is written so an agent can rebuild or adapt the system without this repo.

## WHAT'S INCLUDED

```
SPEC.md                 design spec / thinking map
skills/
  career-bootstrap/     first run: intake menu, interview, build profile, first resume
  application-aid/      default entry point: apply, refresh, rebuild, explore fit, browse
  resume-builder/       posting -> fit analysis -> tailored ATS resume
  career-checkin/       periodic interview -> journal -> profile updates
  ats-to-pdf/           render txt -> clean single-column PDF
templates/              AGENTS.md, profile/*, intake/*, applications.md, base resume
tools/ats_to_pdf.py     deterministic txt -> PDF renderer (Python, fpdf2)
tools/extract_text.py   DOCX / PDF / TXT / MD -> plain text for intake (python-docx, pypdf)
```

## QUICKSTART

1. Create a private folder for your career workspace (not inside a work repo, and not a public git repo).
2. Copy `templates/*` into it, and `tools/` alongside.
3. Copy `skills/*` into your agent's skill directory:

| Agent | Location |
|---|---|
| Claude Code | `<root>/.claude/skills/` and add a `CLAUDE.md` containing `Read AGENTS.md first.` |
| Snowflake Cortex Code | `<root>/.cortex/skills/` |
| Codex / other `AGENTS.md` readers | `<root>/skills/` (the router table in `AGENTS.md` points to them) |
| Others | Any rules/prompt location; point it at `AGENTS.md` |

4. Open the folder in your agent and say: **"Set up my career workspace."** That runs `career-bootstrap`.
5. After that, the default entry point is **"Help me with an application"** or just paste a job link.

## STARTING POINTS (intake)

Bootstrap asks how you want to start. Pick any combination; every path ends in a short interview.

| Option | What you do | What the agent does |
|---|---|---|
| Resume | Drop your latest resume (PDF, DOCX, TXT, MD) in `intake/sources/`, or paste it | Builds the role and date outline; each bullet becomes an unverified claim |
| Other documents | LinkedIn export, reviews, promotion packets, brag docs, decks | Pulls out wins, numbers, and recognition, noting which file each came from |
| Harvest prompt | Run `intake/harvest-prompt.md` in your work AI assistant, review the output, save it to `intake/sources/` | Treats it as a secondhand draft to confirm in the interview |
| Interview only | Nothing to prepare | Asks role by role, starting with scope and numbers |

Nothing taken from a resume or document is used on an external document until you confirm it. Only share employer material your employer permits. When unsure, use the harvest prompt (review before anything leaves the work tool) or the interview.

## REQUIREMENTS

- An agent with file read/write. Web fetch and web search are optional (posting fetch, browsing mode).
- Python 3.10+.
  - PDFs out: `fpdf2`. `uv run --with fpdf2 tools/ats_to_pdf.py resumes/base/base-resume-ats.txt` or `pip install fpdf2`.
  - Documents in: `python-docx` and `pypdf`. `uv run --with python-docx --with pypdf tools/extract_text.py intake/sources -o intake/extracted.txt` or `pip install python-docx pypdf`.
- Without Python, paste your resume text and use the interview. Everything else is markdown.

## PRIVACY

Your `profile/`, `journal/`, and `intake/` hold real internal names and numbers by design. Keep the workspace private. If you version your workspace, install `templates/gitignore.template` as `.gitignore` at its root; it excludes them. the skills sanitize every external document against `profile/sanitization.md` before saving.

## WORKFLOWS

| Say | Result |
|---|---|
| "Set up my career workspace" | Intake menu, then a profile built from your material and interviews; first base resume and PDF |
| "Help me with an application" / a job link | Mode menu: A) apply, B) refresh, C) rebuild, D) explore fit, E) browse |
| "Check in" | Short interview -> journal entry -> proposed profile updates you approve |
| "Build a resume for <link>" | `resumes/<date>-<company>-<role>/` with posting, fit analysis, ATS txt |
| "Make the PDF" | `<First> <Last>.pdf` next to the txt |

## LICENSE

MIT. See [LICENSE](LICENSE).

## BEFORE SENDING

- Fill contact placeholders.
- Confirm any `~` estimated numbers.
- The PDF is for humans; paste the txt into portals that parse PDFs poorly.
