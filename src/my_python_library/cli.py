from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .files import format_ticket_files, list_ticket_attachment_paths, list_tickets_with_files, open_ticket_files
from .search import format_search_results, search_tickets
from .tickets import format_ticket, list_ticket_numbers


HELP_TEXT = """ISTCode - вывод экзаменационных билетов.

Команды:
  ist-ticket 1        показать билет N 1
  ist-ticket 20       показать билет N 20
  ist-ticket list     показать все доступные номера
  ist-ticket files 6  показать путь к папке файлов билета N 6
  ist-ticket open 6   открыть все файлы из папки билета N 6
  ist-ticket search "метрики регрессии"  найти фразу в файлах билетов
  ist-ticket help     показать эту справку

Запасной запуск:
  python -m my_python_library 1
  python -m my_python_library list
  python -m my_python_library files 6
  python -m my_python_library open 6
  python -m my_python_library search "метрики регрессии"
  python -m my_python_library help

Установка:
  python -m pip install istcode

Обновление:
  python -m pip install --upgrade istcode
"""


def main(argv: Sequence[str] | None = None) -> int:
    configure_output_encoding()

    parser = argparse.ArgumentParser(
        prog="ist-ticket",
        description="Показать экзаменационный билет в командной строке.",
    )
    parser.add_argument(
        "ticket",
        nargs="?",
        help="номер билета, list/список, files/файлы, open/открыть или help/помощь",
    )
    parser.add_argument(
        "number",
        nargs="*",
        help="номер билета для команд files/open",
    )
    parser.add_argument(
        "--no-files",
        action="store_true",
        help="не выводить список файлов вместе с билетом",
    )
    parser.add_argument(
        "--open-files",
        action="store_true",
        help="открыть файлы после вывода билета",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="после поиска вывести текст первого найденного билета",
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

    if ticket_arg.lower() in {"files", "file", "attachments", "materials", "материалы", "файлы"}:
        if not args.number:
            print("Ошибка: укажите номер билета, например: ist-ticket files 6", file=sys.stderr)
            return 2
        try:
            number = int(args.number[0])
        except ValueError:
            print("Ошибка: нужен номер билета, например: ist-ticket files 6", file=sys.stderr)
            return 2
        if number not in list_ticket_numbers():
            first, last = list_ticket_numbers()[0], list_ticket_numbers()[-1]
            print(f"Ошибка: билет {number} не найден. Доступно: {first}-{last}", file=sys.stderr)
            return 2
        print(format_ticket_files(number))
        return 0

    if ticket_arg.lower() in {"open", "открыть"}:
        if not args.number:
            print("Ошибка: укажите номер билета, например: ist-ticket open 6", file=sys.stderr)
            return 2
        try:
            number = int(args.number[0])
        except ValueError:
            print("Ошибка: нужен номер билета, например: ist-ticket open 6", file=sys.stderr)
            return 2
        if number not in list_ticket_numbers():
            first, last = list_ticket_numbers()[0], list_ticket_numbers()[-1]
            print(f"Ошибка: билет {number} не найден. Доступно: {first}-{last}", file=sys.stderr)
            return 2
        result = open_ticket_files(number)
        if result.opened:
            print(f"Открыто файлов: {result.opened}")
        elif result.folder_opened:
            print(f"Файлы для билета N {number} не добавлены. Открыта папка билета.")
        else:
            print(f"Файлы для билета N {number} не добавлены. Папку билета открыть не удалось.")
        if result.folder_opened:
            print("Папка билета открыта.")
        if result.failed:
            print("Не удалось открыть:")
            for filename, error in result.failed:
                print(f"  {filename}: {error}")
        return 0

    if ticket_arg.lower() in {"search", "find", "поиск", "найти"}:
        query = " ".join(args.number).strip()
        if not query:
            print('Ошибка: укажите фразу, например: ist-ticket search "метрики регрессии"', file=sys.stderr)
            return 2

        results = search_tickets(query)
        print(format_search_results(query, results))
        if not results:
            return 0

        first_match = results[0].ticket_number
        if args.show:
            print()
            print(format_ticket(first_match))
        if args.open_files:
            result = open_ticket_files(first_match)
            print()
            if result.opened:
                print(f"Открыто файлов: {result.opened}")
            if result.folder_opened:
                print("Папка билета открыта.")
            if result.failed:
                print("Не удалось открыть:")
                for filename, error in result.failed:
                    print(f"  {filename}: {error}")
        return 0

    try:
        number = int(ticket_arg)
    except ValueError:
        print("Ошибка: нужен номер билета, например: ist-ticket 1", file=sys.stderr)
        return 2

    try:
        print(format_ticket(number))
        if not args.no_files and list_ticket_attachment_paths(number):
            print()
            print(format_ticket_files(number))
        if args.open_files:
            result = open_ticket_files(number)
            if result.opened:
                print()
                print(f"Открыто файлов: {result.opened}")
            if result.failed:
                print("Не удалось открыть:")
                for filename, error in result.failed:
                    print(f"  {filename}: {error}")
    except KeyError:
        first, last = list_ticket_numbers()[0], list_ticket_numbers()[-1]
        print(f"Ошибка: билет {number} не найден. Доступно: {first}-{last}", file=sys.stderr)
        return 2

    return 0


def configure_output_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
