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

Показать справку:

```cmd
ist-ticket help
```

Показать папку с файлами билета:

```cmd
ist-ticket files 6
```

Для фото можно писать так же:

```cmd
ist-ticket images 6
```

Открыть все файлы из папки билета в стандартных программах Windows:

```cmd
ist-ticket open 6
```

Если команда `ist-ticket` не найдена, запускай так:

```cmd
python -m my_python_library 1
```

Список билетов через запасной запуск:

```cmd
python -m my_python_library list
```

Справка через запасной запуск:

```cmd
python -m my_python_library help
```

Файлы через запасной запуск:

```cmd
python -m my_python_library files 6
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

Открой папку нужного билета:

```text
src/my_python_library/assets/files/ticket_01
```

Внутри есть файл:

```text
ticket.md
```

Меняй вопросы и ответы прямо в `ticket.md`. Команда:

```cmd
ist-ticket 1
```

выводит текст из этого файла.

Для других билетов меняй номер папки:

```text
ticket_01 -> билет 1
ticket_02 -> билет 2
ticket_20 -> билет 20
```

После изменения проверь:

```cmd
python -m pytest
ist-ticket 1
```

## Где лежат файлы билетов

Основная папка:

```text
C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library\src\my_python_library\assets\files
```

Внутри есть 20 папок:

```text
ticket_01
ticket_02
ticket_03
ticket_04
ticket_05
ticket_06
ticket_07
ticket_08
ticket_09
ticket_10
ticket_11
ticket_12
ticket_13
ticket_14
ticket_15
ticket_16
ticket_17
ticket_18
ticket_19
ticket_20
```

Пример:

```text
Билет 1 -> ticket_01
Билет 2 -> ticket_02
Билет 20 -> ticket_20
```

В каждой папке есть `ticket.md`. Это основной файл билета: вопросы и ответы для команды `ist-ticket`.

Команда:

```cmd
ist-ticket files 1
```

покажет путь до папки:

```text
...\assets\files\ticket_01
```

Команда:

```cmd
ist-ticket open 1
```

откроет все файлы из папки `ticket_01`.

## Как добавить фото, презентацию или другой файл к билету

Поддерживаются разные форматы:

```text
.png
.jpg
.jpeg
.pdf
.pptx
.docx
.xlsx
.txt
```

1. Положи файл в папку нужного билета:

```text
C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library\src\my_python_library\assets\files\ticket_01
```

Например:

```text
C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library\src\my_python_library\assets\files\ticket_06\ticket_6_form.png
C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library\src\my_python_library\assets\files\ticket_06\ticket_6_presentation.pptx
```

2. Проверь:

```cmd
ist-ticket files 6
ist-ticket open 6
```

3. Опубликуй новую версию:

```cmd
publish_new_version.bat
```

## Как отправить изменения на GitHub

Простой способ:

```cmd
publish_new_version.bat
```

Файл сам:

- запускает тесты;
- собирает пакет;
- проверяет пакет;
- показывает текст commit;
- спрашивает только `y/n`;
- делает commit;
- делает push;
- запускает публикацию на PyPI через GitHub Actions, если установлен `gh`.

Если `gh` не установлен, файл покажет ссылку, где нажать `Run workflow` вручную.

Ручной способ:

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
