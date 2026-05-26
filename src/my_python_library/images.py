from __future__ import annotations

from dataclasses import dataclass

from .files import (
    TicketFile,
    format_ticket_files,
    list_ticket_files,
    list_tickets_with_files,
    open_ticket_files,
    resolve_ticket_folder_path,
)


@dataclass(frozen=True)
class TicketImage(TicketFile):
    pass


def list_ticket_images(ticket_number: int) -> tuple[TicketFile, ...]:
    return list_ticket_files(ticket_number)


def list_tickets_with_images() -> list[int]:
    return list_tickets_with_files()


def resolve_image_path(image: TicketFile):
    return (resolve_ticket_folder_path(image.ticket_number) / image.filename).resolve()


def format_ticket_images(ticket_number: int) -> str:
    return format_ticket_files(ticket_number)


def open_ticket_images(ticket_number: int) -> int:
    return open_ticket_files(ticket_number)
