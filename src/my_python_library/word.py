from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph


ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*=")
FUNCTION_CALL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\(.*\)$")
CODE_VALUE_PADDING_RE = re.compile(r"(?<=\S) {2,}(?=\{)")


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
    raw_rows = [[cell_text_lines(cell) for cell in row.cells] for row in table.rows]
    if is_code_table(raw_rows):
        return format_code_table(raw_rows)

    rows = [[normalize_cell_lines(cell_lines) for cell_lines in row] for row in raw_rows]
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


def cell_text_lines(cell: _Cell) -> list[str]:
    return [line.rstrip() for line in cell.text.splitlines()]


def normalize_cell_lines(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


def is_code_table(rows: list[list[list[str]]]) -> bool:
    if not rows or max(len(row) for row in rows) != 1:
        return False

    lines = flatten_single_column_rows(rows)
    meaningful_lines = [line for line in lines if line.strip()]
    if len(meaningful_lines) < 2:
        return len(meaningful_lines) == 1 and len(meaningful_lines[0]) > 80 and looks_like_code_line(meaningful_lines[0])

    code_line_count = sum(looks_like_code_line(line) for line in meaningful_lines)
    return code_line_count >= max(2, len(meaningful_lines) // 3)


def flatten_single_column_rows(rows: list[list[list[str]]]) -> list[str]:
    lines: list[str] = []
    for row_index, row in enumerate(rows):
        if not row:
            continue
        if row_index and lines and lines[-1] != "":
            lines.append("")
        lines.extend(row[0])
    return lines


def looks_like_code_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    code_prefixes = (
        "#",
        "//",
        "/*",
        "*/",
        ")",
        "{",
        "}",
        "<",
        "</",
        "import ",
        "from ",
        "export ",
        "const ",
        "let ",
        "var ",
        "def ",
        "class ",
        "function ",
        "interface ",
        "type ",
        "return ",
        "print(",
        "for ",
        "while ",
        "if ",
        "elif ",
        "else:",
        "try:",
        "except ",
        "with ",
    )
    if stripped.startswith(code_prefixes):
        return True

    if stripped in {")", "]", "}", "),", "],", "},"}:
        return True
    if line[:1].isspace() and stripped.endswith(","):
        return True
    if ASSIGNMENT_RE.match(stripped):
        return True
    if stripped.endswith(("{", "}", ";", ">", "/>", ");", "};")):
        return True
    return FUNCTION_CALL_RE.match(stripped) is not None


def format_code_table(rows: list[list[list[str]]]) -> str:
    lines = flatten_single_column_rows(rows)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(normalize_code_line(line) for line in lines)


def normalize_code_line(line: str) -> str:
    return CODE_VALUE_PADDING_RE.sub(" ", line)
