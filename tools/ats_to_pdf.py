"""Render an ATS plain-text resume into a clean single-column PDF.

Usage: uv run --with fpdf2 tools/ats_to_pdf.py <resume-ats.txt> [-o out.pdf]

Format: line 1 name, line 2 contact, ALL CAPS lines are section headers,
lines containing '|' under EXPERIENCE/EDUCATION are role lines, '- ' lines are bullets.
Default output: '<First> <Last>.pdf' next to the source (name from line 1 of the resume txt);
cover-letter sources get '<First> <Last> Cover Letter.pdf'.
"""

import argparse
import re
from pathlib import Path

from fpdf import FPDF

TEXT = (25, 25, 25)
RULE = (120, 120, 120)
REPLACEMENTS = {"\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2022": "-"}


def clean(line: str) -> str:
    for k, v in REPLACEMENTS.items():
        line = line.replace(k, v)
    return line.encode("latin-1", "replace").decode("latin-1")


def is_header(line: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Z &/]+", line)) and len(line) <= 40


MIN_ROLE_SIZE = 8.0
WARNINGS: list[str] = []


def split_role(parts: list[str]) -> tuple[str, str]:
    left = "  |  ".join(parts[:-1]) if len(parts) > 1 else parts[0]
    right = parts[-1] if len(parts) > 1 else ""
    return left, right


def role_fits(pdf: FPDF, left: str, right: str, size: float, width: float) -> bool:
    pdf.set_font("Helvetica", "B", size)
    lw = pdf.get_string_width(left)
    pdf.set_font("Helvetica", "", size)
    return lw + pdf.get_string_width(right) + 4 <= width


def uniform_role_size(pdf: FPDF, role_lines: list[list[str]], width: float) -> float:
    """Largest size (<= 10.2) at which every role line fits on one row, so all headers match."""
    size = 10.2
    while size > MIN_ROLE_SIZE and not all(role_fits(pdf, *split_role(p), size, width) for p in role_lines):
        size = round(size - 0.2, 1)
    for p in role_lines:
        if not role_fits(pdf, *split_role(p), size, width):
            WARNINGS.append(f"Role line too long even at {MIN_ROLE_SIZE}pt; shorten it: {' | '.join(p)}")
    return size


def render_role_line(pdf: FPDF, parts: list[str], width: float, size: float) -> None:
    """Role line on one row: bold left text, dates right-aligned."""
    left, right = split_role(parts)
    pdf.set_font("Helvetica", "", size)
    rw = pdf.get_string_width(right)
    pdf.set_font("Helvetica", "B", size)
    pdf.cell(width - rw, 5, left)
    pdf.set_font("Helvetica", "", size)
    pdf.cell(rw, 5, right, align="R", new_x="LMARGIN", new_y="NEXT")


def render(src: Path, out: Path) -> int:
    lines = [clean(l.rstrip()) for l in src.read_text(encoding="utf-8").splitlines()]
    while lines and not lines[0]:
        lines.pop(0)

    pdf = FPDF(format="Letter")
    pdf.set_margins(15, 13, 15)
    pdf.set_auto_page_break(True, margin=13)
    pdf.add_page()
    pdf.set_text_color(*TEXT)
    width = pdf.w - pdf.l_margin - pdf.r_margin
    body = lines[2:]
    role_size = uniform_role_size(
        pdf, [[p.strip() for p in l.split("|")] for l in body if "|" in l and not l.startswith("- ")], width)

    pdf.set_font("Helvetica", "B", 17)
    pdf.cell(width, 8, lines[0], align="C", new_x="LMARGIN", new_y="NEXT")
    if len(lines) > 1:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.cell(width, 5, lines[1], align="C", new_x="LMARGIN", new_y="NEXT")

    for line in lines[2:]:
        if not line:
            pdf.ln(1.2)
        elif is_header(line):
            pdf.ln(2.5)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(width, 5.5, line, align="L", new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*RULE)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + width, pdf.get_y())
            pdf.ln(1.5)
        elif line.startswith("- "):
            pdf.set_font("Helvetica", "", 9.8)
            pdf.set_x(pdf.l_margin + 3)
            pdf.cell(3.5, 4.6, "-")
            pdf.multi_cell(width - 6.5, 4.6, line[2:], align="L", new_x="LMARGIN", new_y="NEXT")
        elif "|" in line:
            pdf.ln(0.8)
            render_role_line(pdf, [p.strip() for p in line.split("|")], width, role_size)
        else:
            pdf.set_font("Helvetica", "", 9.8)
            pdf.multi_cell(width, 4.6, line, align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(out))
    return pdf.pages_count


def first_line(path: Path) -> str:
    return next((l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()), "")


def owner_name(src: Path) -> str:
    """Candidate name from line 1 of the resume txt in the same folder (falls back to src)."""
    resume = next(iter(sorted(src.parent.glob("*resume-ats.txt"))), src)
    name = clean(first_line(resume))
    if name.isupper():
        name = re.sub(r"[A-Za-z]+", lambda m: m.group().capitalize(), name.lower())
    return re.sub(r'[<>:"/\\|?*]', "", name).strip() or "resume"


def default_out(src: Path) -> Path:
    """'<First> <Last>.pdf' for resumes; '<First> <Last> Cover Letter.pdf' for cover letters."""
    suffix = " Cover Letter" if "cover" in src.stem.lower() else ""
    return src.with_name(f"{owner_name(src)}{suffix}.pdf")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args()
    out = args.out or default_out(args.src)
    pages = render(args.src, out)
    print(f"Wrote {out} ({pages} page{'s' if pages != 1 else ''})")
    for w in WARNINGS:
        print(f"WARNING: {w}")


if __name__ == "__main__":
    main()
