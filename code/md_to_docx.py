"""Convert every Markdown file in markdown/ to a Word document in docs/.

The .md files are the editable sources; the .docx files are what gets shared or
submitted. Supports the Markdown used in this project: headings, paragraphs, bold,
italic, inline code, links, bullet and numbered lists (one level of nesting),
block quotes, horizontal rules and pipe tables.

Requires python-docx (pip install python-docx).
Usage (from the project folder):   python code/md_to_docx.py
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
SRC, DST = ROOT / "markdown", ROOT / "docs"
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")


def add_inline(paragraph, text):
    """Write text into a paragraph, honouring **bold**, *italic*, `code` and [links](url)."""
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(9.5)
        elif part.startswith("[") and "](" in part:
            label, url = part[1:-1].split("](", 1)
            run = paragraph.add_run(label)
            run.font.color.rgb = RGBColor(0x1F, 0x5F, 0x8B)
            if url.startswith("http"):
                paragraph.add_run(f" ({url})").font.size = Pt(8.5)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            paragraph.add_run(part[1:-1]).italic = True
        else:
            paragraph.add_run(part)


def add_table(doc, lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)]
    table = doc.add_table(rows=len(rows), cols=max(len(r) for r in rows))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            p = table.cell(i, j).paragraphs[0]
            add_inline(p, cell.replace("\\|", "|"))
            for run in p.runs:
                run.font.size = Pt(9)
                run.bold = run.bold or i == 0
    doc.add_paragraph()


def convert(md_path, docx_path):
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)
    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            add_table(doc, block)
            continue
        if not stripped:
            pass
        elif re.fullmatch(r"-{3,}|\*{3,}", stripped):
            doc.add_paragraph("_" * 60)
        elif m := re.match(r"(#{1,6})\s+(.*)", stripped):
            heading = doc.add_heading(level=min(len(m.group(1)), 4))
            add_inline(heading, m.group(2))
        elif stripped.startswith(">"):
            p = doc.add_paragraph(style="Intense Quote")
            add_inline(p, stripped.lstrip("> "))
        elif m := re.match(r"(\s*)[-*]\s+(?:\[[ x]\]\s+)?(.*)", line):
            style = "List Bullet 2" if len(m.group(1)) >= 2 else "List Bullet"
            add_inline(doc.add_paragraph(style=style), m.group(2))
        elif m := re.match(r"(\s*)\d+\.\s+(.*)", line):
            style = "List Number 2" if len(m.group(1)) >= 2 else "List Number"
            add_inline(doc.add_paragraph(style=style), m.group(2))
        else:
            add_inline(doc.add_paragraph(), stripped)
        i += 1
    doc.save(docx_path)


if __name__ == "__main__":
    DST.mkdir(exist_ok=True)
    for md in sorted(SRC.glob("*.md")):
        convert(md, DST / f"{md.stem}.docx")
        print("written:", (DST / f"{md.stem}.docx").relative_to(ROOT))
