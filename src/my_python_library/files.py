from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path


@dataclass(frozen=True)
class TicketFile:
    ticket_number: int
    question_number: int
    filename: str
    title: str = ""


# Add file links here. Put files into src/my_python_library/assets/files/.
# Supported examples: .png, .jpg, .pdf, .pptx, .docx, .xlsx, .txt.
# Example:
# TICKET_FILES = {
#     6: (
#         TicketFile(6, 3, "ticket_6_form.png", "Форма для задания"),
#         TicketFile(6, 3, "ticket_6_demo.pptx", "Презентация"),
#     ),
# }
TICKET_FILES: dict[int, tuple[TicketFile, ...]] = {
    1: (
        TicketFile(1, 1, "ticket_1_question_1_types.png", "Схема типов данных"),
        TicketFile(1, 1, "ticket_1_question_1_presentation.pptx", "Мини-презентация"),
    ),
}


def list_ticket_files(ticket_number: int) -> tuple[TicketFile, ...]:
    return TICKET_FILES.get(ticket_number, ())


def list_tickets_with_files() -> list[int]:
    return sorted(TICKET_FILES)


def resolve_ticket_file_path(ticket_file: TicketFile) -> Path:
    local_path = Path.cwd() / "istcode_files" / ticket_file.filename
    if local_path.exists():
        return local_path.resolve()

    local_image_path = Path.cwd() / "istcode_images" / ticket_file.filename
    if local_image_path.exists():
        return local_image_path.resolve()

    package_path = files("my_python_library").joinpath("assets", "files", ticket_file.filename)
    return Path(str(package_path)).resolve()


def format_ticket_files(ticket_number: int) -> str:
    ticket_files = list_ticket_files(ticket_number)
    if not ticket_files:
        return f"Файлы для билета N {ticket_number} не добавлены."

    lines = [f"Файлы для билета N {ticket_number}:"]
    for ticket_file in ticket_files:
        path = resolve_ticket_file_path(ticket_file)
        title = f" - {ticket_file.title}" if ticket_file.title else ""
        lines.append(f"  вопрос {ticket_file.question_number}{title}: {path}")
    return "\n".join(lines)


def open_ticket_files(ticket_number: int) -> int:
    ticket_files = list_ticket_files(ticket_number)
    if not ticket_files:
        return 0

    for ticket_file in ticket_files:
        path = resolve_ticket_file_path(ticket_file)
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)

    return len(ticket_files)
