---
name: ats-to-pdf
description: Convert an ATS plain-text resume or cover letter (resume-ats.txt, cover-letter.txt) in the career workspace into a clean single-column PDF. Use when the user says "make the PDF", "convert to PDF", or "render the resume".
---

# ATS to PDF

Career root: see `AGENTS.md`.

## Steps

1. Identify the source txt. If not given, use the most recently modified `resumes/*/resume-ats.txt` and confirm the path in one line.
2. Run from the career root:
   ```
   uv run --with fpdf2 tools/ats_to_pdf.py "<path/to/resume-ats.txt>"
   ```
   Without uv: `pip install fpdf2` then `python tools/ats_to_pdf.py "<path>"`.
   Output is written next to the source as `<First> <Last>.pdf`, named from line 1 of the resume txt in that folder, title-cased. Cover-letter sources become `<First> <Last> Cover Letter.pdf`. Override with `-o <path>` only if asked. The script prints the page count.
3. If the script prints a role-line WARNING, shorten that line in the txt (title wording or drop city) and re-run. Role lines must be a single line.
4. If the page count exceeds the limit in `AGENTS.md` (default 2), say so and suggest specific bullets to cut; never silently shrink fonts.
5. Verify: read the PDF text back and confirm order matches the txt.

## Notes

- Expects the format defined in `resume-builder` (name line, contact line, ALL CAPS headers, `|` role lines, `- ` bullets).
- Core Helvetica, single column, no images or tables, so ATS parsers extract text cleanly. Non-Latin-1 characters are replaced; keep the txt ASCII.
- Near-black text for print safety; no employer branding (external document).
