from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from importlib.resources import files
except ImportError:  # pragma: no cover - Python 3.8 fallback.
    from importlib_resources import files

TICKET_COUNT = 20
TICKET_TEXT_FILENAME = "ticket.md"
TICKET_WORD_FILENAME = "ticket.docx"
IGNORED_FILENAMES = {"README.md", ".gitkeep"}
ATTACHMENT_IGNORED_FILENAMES = IGNORED_FILENAMES | {TICKET_TEXT_FILENAME, TICKET_WORD_FILENAME}


@dataclass(frozen=True)
class TicketFile:
    ticket_number: int
    question_number: int
    filename: str
    title: str = ""


@dataclass(frozen=True)
class OpenTicketFilesResult:
    opened: int
    failed: tuple[tuple[str, str], ...] = ()
    folder_opened: bool = False


# Put files for each ticket into src/my_python_library/assets/files/ticket_XX/.
# Supported examples: .png, .jpg, .pdf, .pptx, .docx, .xlsx, .txt.


def list_tickets_with_files() -> list[int]:
    return [
        ticket_number
        for ticket_number in range(1, TICKET_COUNT + 1)
        if list_ticket_attachment_paths(ticket_number)
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
    return _list_ticket_file_paths(ticket_number, IGNORED_FILENAMES)


def list_ticket_attachment_paths(ticket_number: int) -> tuple[Path, ...]:
    return _list_ticket_file_paths(ticket_number, ATTACHMENT_IGNORED_FILENAMES)


def _list_ticket_file_paths(ticket_number: int, ignored_filenames: set[str]) -> tuple[Path, ...]:
    folder = resolve_ticket_folder_path(ticket_number)
    if not folder.exists() or not folder.is_dir():
        return ()

    return tuple(
        sorted(
            path.resolve()
            for path in folder.iterdir()
            if path.is_file() and path.name not in ignored_filenames and not path.name.startswith(".")
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


def open_ticket_files(ticket_number: int) -> OpenTicketFilesResult:
    folder = resolve_ticket_folder_path(ticket_number)
    file_paths = list_ticket_file_paths(ticket_number)
    if not file_paths:
        folder_error = open_path(folder)
        return OpenTicketFilesResult(0, folder_opened=folder_error is None)

    opened = 0
    failed: list[tuple[str, str]] = []
    for path in file_paths:
        error = open_path(path)
        if error is None:
            opened += 1
        else:
            failed.append((path.name, error))

    folder_error = open_path(folder)
    if folder_error is not None:
        failed.append((folder.name, folder_error))

    return OpenTicketFilesResult(
        opened,
        failed=tuple(failed),
        folder_opened=folder_error is None,
    )


def open_path(path: Path) -> str | None:
    try:
        return _open_path(path)
    except OSError as exc:
        return str(exc)


def _open_path(path: Path) -> str | None:
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
        return None

    command = ["open", str(path)] if sys.platform == "darwin" else ["xdg-open", str(path)]
    completed = subprocess.run(command, check=False)
    if completed.returncode:
        return f"exit code {completed.returncode}"
    return None
