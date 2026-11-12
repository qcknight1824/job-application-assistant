"""Extract plain text from resumes and career documents (.docx, .pdf, .txt, .md).

Usage:
  uv run --with python-docx --with pypdf tools/extract_text.py <file-or-folder> [...] [-o out.txt]
Without uv:
  pip install python-docx pypdf
  python tools/extract_text.py <file-or-folder> [...] [-o out.txt]

Each source is emitted under a '=== SOURCE: <path> ===' header so every extracted
claim can be traced to its file. Folders are searched recursively. Credential-like
files (.env, keys, certs, secrets/) are always skipped. Output goes to stdout unless -o is given.

DOCX: paragraphs and tables in document order (headings -> '## ', bullets -> '- '),
plus headers/footers and text boxes (contact info often hides there).
PDF: text layer only. A scanned PDF has none; the script says so and you should paste the text.
Legacy .doc is not supported: re-save as .docx or PDF.

Files that yield no text get a WARNING and no SOURCE block. Exit code is 0 if at least one
source was extracted and nothing failed to read; otherwise 1. Read WARNING lines on stderr.
"""

import argparse
import sys
from pathlib import Path

TEXT_SUFFIXES = {".txt", ".md"}
SUPPORTED = TEXT_SUFFIXES | {".docx", ".pdf"}
SKIP_DIRS = {"secrets", "certs", ".git", "node_modules", ".venv", "__pycache__"}
SKIP_SUFFIXES = {".p8", ".pem", ".key", ".pfx", ".p12", ".crt"}


class MissingDependency(Exception):
    pass


def is_credential(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.startswith(".env")
        or path.suffix.lower() in SKIP_SUFFIXES
        or any(part.lower() in SKIP_DIRS for part in path.parts)
    )


def format_table(table) -> list[str]:
    rows = []
    for row in table.rows:
        seen, cells = set(), []
        for cell in row.cells:
            if id(cell._tc) in seen:  # merged cells repeat
                continue
            seen.add(id(cell._tc))
            text = " ".join(cell.text.split())
            if text:
                cells.append(text)
        if cells:
            rows.append(" | ".join(cells))
    return rows


def format_paragraph(p) -> str:
    text = p.text.strip()
    if not text:
        return ""
    try:
        style = p.style.name or ""
    except Exception:
        style = ""
    ppr = p._p.pPr
    if style.startswith("Heading") or style == "Title":
        return f"\n## {text}"
    if "List" in style or (ppr is not None and ppr.numPr is not None):
        return f"- {text}"
    return text


def read_docx(path: Path) -> tuple[str, list[str]]:
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError as e:
        raise MissingDependency("python-docx") from e

    doc = Document(str(path))
    warnings: list[str] = []
    lines: list[str] = []

    seen_hf: set[str] = set()
    for section in doc.sections:
        for part in (section.header, section.footer):
            found = [p.text.strip() for p in part.paragraphs]
            for table in part.tables:
                found.extend(format_table(table))
            for text in found:
                if text and text not in seen_hf:
                    seen_hf.add(text)
                    lines.append(f"[header/footer] {text}")

    for child in doc.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            lines.append(format_paragraph(Paragraph(child, doc)))
        elif tag == "tbl":
            lines.extend(format_table(Table(child, doc)))

    extras, seen = [], set(lines)
    for box in doc.element.body.xpath(".//w:txbxContent"):
        for p in box.xpath("./w:p"):
            text = "".join(t.text or "" for t in p.xpath(".//w:t")).strip()
            if text and text not in seen:
                seen.add(text)
                extras.append(text)
    if extras:
        lines.append("[text boxes]")
        lines.extend(extras)
        warnings.append("text boxes found; their position in the output may differ from the visual layout")

    return "\n".join(lines).strip(), warnings


def read_pdf(path: Path) -> tuple[str, list[str]]:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise MissingDependency("pypdf") from e

    reader = PdfReader(str(path))
    if reader.is_encrypted and not reader.decrypt(""):
        raise ValueError("PDF is password-protected; remove the password or paste the text")
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n\n".join(p for p in pages if p)
    warnings = []
    if not text:
        warnings.append("no text layer found (likely a scan or image); paste the text instead")
    elif len(text) < 25 * max(1, len(reader.pages)):
        warnings.append("very little text for the page count; check that nothing is image-only")
    return text, warnings


def read_text_file(path: Path) -> tuple[str, list[str]]:
    return path.read_text(encoding="utf-8", errors="replace").strip(), []


READERS = {".docx": read_docx, ".pdf": read_pdf, ".txt": read_text_file, ".md": read_text_file}


def unsupported_message(path: Path) -> str:
    if path.suffix.lower() == ".doc":
        return f"{path}: legacy .doc is not supported; re-save as .docx or PDF"
    return f"{path}: unsupported type {path.suffix or '(none)'}, skipped; supported: {', '.join(sorted(SUPPORTED))}"


def collect(paths: list[str], skip: Path | None) -> tuple[list[Path], list[str], list[str]]:
    """Return (files to read, warnings, errors)."""
    files: list[Path] = []
    warnings: list[str] = []
    errors: list[str] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if not f.is_file() or is_credential(f) or f.resolve() == skip:
                    continue
                if f.suffix.lower() in SUPPORTED:
                    files.append(f)
                elif not f.name.startswith("."):
                    warnings.append(unsupported_message(f))
        elif p.is_file():
            if is_credential(p):
                warnings.append(f"{p}: credential-like file, skipped")
            elif p.suffix.lower() in SUPPORTED:
                files.append(p)
            else:
                warnings.append(unsupported_message(p))
        else:
            errors.append(f"{p}: not found")
    return files, warnings, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract text from resumes and career documents.")
    ap.add_argument("paths", nargs="+", help="files or folders (.docx, .pdf, .txt, .md)")
    ap.add_argument("-o", "--out", type=Path, help="write to this file instead of stdout")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    skip = args.out.resolve() if args.out else None
    files, warnings, errors = collect(args.paths, skip)
    blocks: list[str] = []

    for f in files:
        try:
            text, file_warnings = READERS[f.suffix.lower()](f)
        except MissingDependency as e:
            errors.append(f"{f}: missing dependency '{e}'; run with `uv run --with python-docx --with pypdf` or pip install it")
            continue
        except Exception as e:
            errors.append(f"{f}: could not read ({type(e).__name__}: {e})")
            continue
        warnings.extend(f"{f}: {w}" for w in file_warnings)
        if not text:
            if not file_warnings:
                warnings.append(f"{f}: no text extracted")
            continue
        blocks.append(f"=== SOURCE: {f} ===\n{text}\n")

    output = "\n".join(blocks)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"Wrote {args.out} ({len(blocks)} source{'s' if len(blocks) != 1 else ''}, {len(output):,} chars)", file=sys.stderr)
    elif output:
        print(output)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    return 1 if errors or not blocks else 0


if __name__ == "__main__":
    sys.exit(main())
