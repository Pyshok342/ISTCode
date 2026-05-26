from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .files import format_ticket_files, list_ticket_files, list_tickets_with_files, open_ticket_files
from .tickets import format_ticket, list_ticket_numbers


HELP_TEXT = """ISTCode - вывод экзаменационных билетов.

Команды:
  ist-ticket 1        показать билет N 1
  ist-ticket 20       показать билет N 20
  ist-ticket list     показать все доступные номера
  ist-ticket files 6  показать путь к папке файлов билета N 6
  ist-ticket images 6 то же самое, но привычное имя для фото
  ist-ticket open 6   открыть все файлы из папки билета N 6
  ist-ticket help     показать эту справку

Запасной запуск:
  python -m my_python_library 1
  python -m my_python_library list
  python -m my_python_library files 6
  python -m my_python_library images 6
  python -m my_python_library open 6
  python -m my_python_library help

Установка:
  python -m pip install istcode

Обновление:
  python -m pip install --upgrade istcode
"""


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ist-ticket",
        description="Показать экзаменационный билет в командной строке.",
    )
    parser.add_argument(
        "ticket",
        nargs="?",
        help="номер билета, list/список, files/файлы, images/фото, open/открыть или help/помощь",
    )
    parser.add_argument(
        "number",
        nargs="?",
        help="номер билета для команд files/images/open",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="не выводить пути к файлам вместе с билетом",
    )
    parser.add_argument(
        "--open-images",
        action="store_true",
        help="открыть файлы после вывода билета",
    )
    args = parser.parse_args(argv)

    ticket_arg = args.ticket
    if ticket_arg is None:
        ticket_arg = input("Введите номер билета: ").strip()

    if ticket_arg.lower() in {"help", "помощь", "справка", "?"}:
        print(HELP_TEXT)
        return 0

    if ticket_arg.lower() in {"list", "ls", "список"}:
        numbers = list_ticket_numbers()
        print("Доступные билеты: " + ", ".join(str(number) for number in numbers))
        file_numbers = list_tickets_with_files()
        if file_numbers:
            print("Билеты с файлами: " + ", ".join(str(number) for number in file_numbers))
        return 0

    if ticket_arg.lower() in {"files", "file", "attachments", "materials", "материалы", "файлы", "images", "image", "photo", "photos", "фото", "картинки"}:
        if args.number is None:
            print("Ошибка: укажите номер билета, например: ist-ticket files 6", file=sys.stderr)
            return 2
        try:
            number = int(args.number)
        except ValueError:
            print("Ошибка: нужен номер билета, например: ist-ticket files 6", file=sys.stderr)
            return 2
        print(format_ticket_files(number))
        return 0

    if ticket_arg.lower() in {"open", "open-images", "открыть"}:
        if args.number is None:
            print("Ошибка: укажите номер билета, например: ist-ticket open 6", file=sys.stderr)
            return 2
        try:
            number = int(args.number)
        except ValueError:
            print("Ошибка: нужен номер билета, например: ist-ticket open 6", file=sys.stderr)
            return 2
        opened = open_ticket_files(number)
        if opened:
            print(f"Открыто файлов: {opened}")
        else:
            print(f"Файлы для билета N {number} не добавлены. Открыта папка билета.")
        return 0

    try:
        number = int(ticket_arg)
    except ValueError:
        print("Ошибка: нужен номер билета, например: ist-ticket 1", file=sys.stderr)
        return 2

    try:
        print(format_ticket(number))
        if not args.no_images and list_ticket_files(number):
            print()
            print(format_ticket_files(number))
        if args.open_images:
            opened = open_ticket_files(number)
            if opened:
                print()
                print(f"Открыто файлов: {opened}")
    except KeyError:
        first, last = list_ticket_numbers()[0], list_ticket_numbers()[-1]
        print(f"Ошибка: билет {number} не найден. Доступно: {first}-{last}", file=sys.stderr)
        return 2

    return 0
