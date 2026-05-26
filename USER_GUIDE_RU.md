# Инструкция пользователя ISTCode

## Что это

ISTCode - Python-библиотека и команда для вывода экзаменационных билетов в командную строку.

Команда:

```cmd
ist-ticket 1
```

выводит билет N 1.

## Установка на другом компьютере

Если библиотека уже опубликована на PyPI:

```cmd
python -m pip install istcode
```

Если ставишь с GitHub:

1. Установи Python 3.10 или новее:

```text
https://www.python.org/downloads/
```

При установке включи галочку:

```text
Add python.exe to PATH
```

2. Открой командную строку `cmd` или PowerShell.

3. Установи библиотеку с GitHub:

```cmd
python -m pip install --upgrade https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

## Как пользоваться

Показать билет по номеру:

```cmd
ist-ticket 1
```

Показать список доступных билетов:

```cmd
ist-ticket list
```

Если команда `ist-ticket` не найдена, запускай так:

```cmd
python -m my_python_library 1
```

Список билетов через запасной запуск:

```cmd
python -m my_python_library list
```

## Примеры

Билет N 5:

```cmd
ist-ticket 5
```

Билет N 20:

```cmd
ist-ticket 20
```

## Как обновить библиотеку на другом компьютере

Если библиотека стоит через PyPI:

```cmd
python -m pip install --upgrade istcode
```

Если библиотека стоит через GitHub:

```cmd
python -m pip install --upgrade https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

Потом снова:

```cmd
ist-ticket 1
```

## Как работать с проектом на своем компьютере

Перейти в папку проекта:

```cmd
cd "C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library"
```

Активировать виртуальное окружение:

```cmd
.venv\Scripts\activate
```

Установить проект для разработки:

```cmd
python -m pip install -e ".[dev]"
```

Проверить тесты:

```cmd
python -m pytest
```

Проверить команду:

```cmd
ist-ticket 1
```

## Как изменить билеты

Открой файл:

```text
src/my_python_library/tickets.py
```

В нем есть словарь:

```python
TICKETS = {
    1: Ticket(
        1,
        (
            "Первый вопрос",
            "Второй вопрос",
            "Третий вопрос",
        ),
    ),
}
```

Меняй текст внутри кавычек.

После изменения проверь:

```cmd
python -m pytest
ist-ticket 1
```

## Как отправить изменения на GitHub

После правок:

```cmd
git add .
git commit -m "Update tickets"
git push
```

После этого другой компьютер сможет обновиться командой:

```cmd
python -m pip install --upgrade https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

## Частые ошибки

Если написано:

```text
python is not recognized
```

значит Python не добавлен в PATH. Переустанови Python и включи `Add python.exe to PATH`.

Если написано:

```text
ist-ticket is not recognized
```

используй запасной запуск:

```cmd
python -m my_python_library 1
```

Если билет не найден:

```text
Ошибка: билет 999 не найден
```

посмотри доступные номера:

```cmd
ist-ticket list
```
