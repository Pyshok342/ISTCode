from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


def read_docx_text(path: Path) -> str:
    document = Document(path)
    lines: list[str] = []

    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                lines.append(text)
        elif isinstance(block, Table):
            table_text = format_table(block)
            if table_text:
                lines.append(table_text)

    return "\n".join(lines).strip()


def iter_block_items(document: DocumentObject):
    body = document.element.body
    for child in body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def format_table(table: Table) -> str:
    rows = [
        [normalize_cell_text(cell.text) for cell in row.cells]
        for row in table.rows
    ]
    rows = [row for row in rows if any(cell for cell in row)]
    if not rows:
        return ""

    column_count = max(len(row) for row in rows)
    normalized_rows = [row + [""] * (column_count - len(row)) for row in rows]
    widths = [
        max(len(row[index]) for row in normalized_rows)
        for index in range(column_count)
    ]

    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    lines = [border]
    for row in normalized_rows:
        lines.append("| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)) + " |")
        lines.append(border)
    return "\n".join(lines)


def normalize_cell_text(text: str) -> str:
    return " ".join(part.strip() for part in text.splitlines() if part.strip())
