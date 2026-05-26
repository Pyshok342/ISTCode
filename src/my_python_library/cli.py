from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .tickets import format_ticket, list_ticket_numbers


HELP_TEXT = """ISTCode - вывод экзаменационных билетов.

Команды:
  ist-ticket 1        показать билет N 1
  ist-ticket 20       показать билет N 20
  ist-ticket list     показать все доступные номера
  ist-ticket help     показать эту справку

Запасной запуск:
  python -m my_python_library 1
  python -m my_python_library list
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
        help="номер билета, либо list/список для просмотра доступных номеров",
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
        return 0

    try:
        number = int(ticket_arg)
    except ValueError:
        print("Ошибка: нужен номер билета, например: ist-ticket 1", file=sys.stderr)
        return 2

    try:
        print(format_ticket(number))
    except KeyError:
        first, last = list_ticket_numbers()[0], list_ticket_numbers()[-1]
        print(f"Ошибка: билет {number} не найден. Доступно: {first}-{last}", file=sys.stderr)
        return 2

    return 0
