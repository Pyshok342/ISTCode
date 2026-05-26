import pytest

from my_python_library import format_ticket, format_ticket_files, get_ticket, hello, list_ticket_numbers
from my_python_library.cli import main


def test_hello() -> None:
    assert hello("Alex") == "Hello, Alex!"


def test_ticket_numbers() -> None:
    assert list_ticket_numbers() == list(range(1, 21))


def test_get_ticket() -> None:
    ticket = get_ticket(1)
    assert ticket.number == 1
    assert "машинном обучении" in ticket.questions[0]


def test_format_ticket() -> None:
    formatted = format_ticket(20)
    assert formatted.startswith("Билет №20")
    assert "Проблемы интеллектуального права" in formatted


def test_missing_ticket() -> None:
    with pytest.raises(KeyError):
        get_ticket(999)


def test_cli_prints_ticket(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["1"]) == 0
    output = capsys.readouterr().out
    assert "Билет №1" in output
    assert "Папка файлов билета N 1" in output
    assert "ticket_1_question_1_types.png" in output


def test_cli_lists_tickets(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list"]) == 0
    assert "1, 2, 3" in capsys.readouterr().out


def test_cli_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["help"]) == 0
    output = capsys.readouterr().out
    assert "Команды" in output
    assert "ist-ticket 1" in output
    assert "ist-ticket files 6" in output
    assert "ist-ticket images 6" in output


def test_ticket_files() -> None:
    formatted = format_ticket_files(1)
    assert "ticket_01" in formatted
    assert "ticket_1_question_1_types.png" in formatted
    assert "ticket_1_question_1_presentation.pptx" in formatted


def test_empty_ticket_files() -> None:
    formatted = format_ticket_files(2)
    assert "ticket_02" in formatted
    assert "Файлы не добавлены." in formatted


def test_cli_prints_empty_files(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["files", "2"]) == 0
    assert "не добавлены" in capsys.readouterr().out


def test_cli_images_alias(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["images", "1"]) == 0
    assert "ticket_1_question_1_types.png" in capsys.readouterr().out


def test_cli_rejects_bad_ticket(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["999"]) == 2
    assert "не найден" in capsys.readouterr().err
