# Публикация ISTCode на PyPI

После публикации установка будет короткой:

```cmd
pip install istcode
```

или надежнее:

```cmd
python -m pip install istcode
```

## 1. Аккаунт PyPI

Зарегистрируйся на PyPI:

```text
https://pypi.org/account/register/
```

Почта:

```text
spqamsjf@clokkmail.com
```

После регистрации подтверди письмо на почте.

## 2. API-токен

Открой:

```text
https://pypi.org/manage/account/token/
```

Создай токен:

```text
Add API token
```

Scope можно выбрать:

```text
Entire account
```

Токен выглядит примерно так:

```text
pypi-...
```

Никому его не отправляй. В чат тоже не отправляй.

## 3. Подготовка проекта

Открой `cmd`:

```cmd
cd "C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library"
.venv\Scripts\activate
python -m pip install --upgrade build twine
```

## 4. Собрать пакет

Сначала очисти старые сборки:

```cmd
rmdir /s /q dist
```

Если напишет, что папка не найдена - это нормально.

Собери новую версию:

```cmd
python -m build
```

В папке `dist` должны появиться файлы:

```text
istcode-0.2.0.tar.gz
istcode-0.2.0-py3-none-any.whl
```

## 5. Загрузить на PyPI

```cmd
python -m twine upload dist/*
```

Когда спросит:

```text
username
```

введи:

```text
__token__
```

Когда спросит:

```text
password
```

вставь PyPI API-токен, который начинается с `pypi-`.

## 6. Проверить установку

На любом компьютере:

```cmd
python -m pip install istcode
ist-ticket 1
```

Если `ist-ticket` не найден:

```cmd
python -m my_python_library 1
```

## Если PyPI скажет, что имя занято

Значит `istcode` уже кто-то занял или PyPI его не разрешил.

Тогда надо поменять `name` в `pyproject.toml`, например:

```toml
name = "istcode-pyshok342"
```

После этого увеличить версию и снова собрать:

```cmd
rmdir /s /q dist
python -m build
python -m twine upload dist/*
```
