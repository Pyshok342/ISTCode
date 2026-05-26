from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

TICKET_COUNT = 20
IGNORED_FILENAMES = {"README.md", ".gitkeep"}


@dataclass(frozen=True)
class TicketFile:
    ticket_number: int
    question_number: int
    filename: str
    title: str = ""


# Put files for each ticket into src/my_python_library/assets/files/ticket_XX/.
# Supported examples: .png, .jpg, .pdf, .pptx, .docx, .xlsx, .txt.


def list_tickets_with_files() -> list[int]:
    return [
        ticket_number
        for ticket_number in range(1, TICKET_COUNT + 1)
        if list_ticket_file_paths(ticket_number)
    ]


def ticket_folder_name(ticket_number: int) -> str:
    return f"ticket_{ticket_number:02d}"


def resolve_ticket_folder_path(ticket_number: int) -> Path:
    folder_name = ticket_folder_name(ticket_number)

    local_path = Path.cwd() / "istcode_files" / folder_name
    if local_path.exists():
        return local_path.resolve()

    package_path = files("my_python_library").joinpath("assets", "files", folder_name)
    return Path(str(package_path)).resolve()


def list_ticket_file_paths(ticket_number: int) -> tuple[Path, ...]:
    folder = resolve_ticket_folder_path(ticket_number)
    if not folder.exists() or not folder.is_dir():
        return ()

    return tuple(
        sorted(
            path.resolve()
            for path in folder.iterdir()
            if path.is_file() and path.name not in IGNORED_FILENAMES and not path.name.startswith(".")
        )
    )


def list_ticket_files(ticket_number: int) -> tuple[TicketFile, ...]:
    return tuple(
        TicketFile(ticket_number, 0, path.name, path.stem)
        for path in list_ticket_file_paths(ticket_number)
    )


def format_ticket_files(ticket_number: int) -> str:
    folder = resolve_ticket_folder_path(ticket_number)
    file_paths = list_ticket_file_paths(ticket_number)
    lines = [f"Папка файлов билета N {ticket_number}:", f"  {folder}"]

    if not file_paths:
        lines.append("Файлы не добавлены.")
        return "\n".join(lines)

    lines.append("Файлы:")
    lines.extend(f"  {path.name}" for path in file_paths)
    return "\n".join(lines)


def open_ticket_files(ticket_number: int) -> int:
    folder = resolve_ticket_folder_path(ticket_number)
    file_paths = list_ticket_file_paths(ticket_number)
    if not file_paths:
        open_path(folder)
        return 0

    for path in file_paths:
        open_path(path)

    return len(file_paths)


def open_path(path: Path) -> None:
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)
