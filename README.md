# ISTCode

Command-line helper for exam tickets.

Русская инструкция:

```text
USER_GUIDE_RU.md
```

## Install for development

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Install from GitHub

Install on any computer:

```powershell
python -m pip install https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

After publishing to PyPI:

```powershell
python -m pip install istcode
```

## Use

Show ticket by number:

```powershell
ist-ticket 1
```

The command reads ticket text from:

```text
src/my_python_library/assets/files/ticket_01/ticket.md
```

Edit this file to change ticket questions or answers.

Show available tickets:

```powershell
ist-ticket list
```

Show help:

```powershell
ist-ticket help
```

Show folder and names for attached files/photos/presentations:

```powershell
ist-ticket files 6
```

Open all files from the ticket folder:

```powershell
ist-ticket open 6
```

Ticket folders live in:

```text
src/my_python_library/assets/files/ticket_01
src/my_python_library/assets/files/ticket_02
...
src/my_python_library/assets/files/ticket_20
```

Each folder contains `ticket.md`. This is the editable text shown by `ist-ticket N`.

Alternative launch:

```powershell
python -m my_python_library 1
```

Python import:

```python
from my_python_library import format_ticket

print(format_ticket(1))
```

## Test

```powershell
python -m pytest
```

## Build

```powershell
python -m build
```

## Publish New Version

```powershell
publish_new_version.bat
```

## Publish

First publish to TestPyPI:

```powershell
python -m twine upload --repository testpypi dist/*
```

Then publish to PyPI:

```powershell
python -m twine upload dist/*
```
