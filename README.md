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
python -m pip install --upgrade --force-reinstall --no-cache-dir https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

After publishing to PyPI:

```powershell
python -m pip install --upgrade --force-reinstall --no-cache-dir istcode
```

## Use

Show ticket by number:

```powershell
ist-ticket 1
```

The command first reads ticket text from Word:

```text
src/my_python_library/assets/files/ticket_01/ticket.docx
```

If `ticket.docx` is missing, it reads the fallback file:

```text
src/my_python_library/assets/files/ticket_01/ticket.md
```

Tables from `ticket.docx` are printed as console-friendly ASCII tables.

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

Search across ticket files:

```powershell
ist-ticket search "метрики регрессии"
ist-ticket search sklearn metrics
ist-ticket search "метрики регрессии" --show
```

Ticket folders live in:

```text
src/my_python_library/assets/files/ticket_01
src/my_python_library/assets/files/ticket_02
...
src/my_python_library/assets/files/ticket_20
```

Each folder can contain `ticket.docx`. This is the preferred editable Word file shown by `ist-ticket N`.
If there is no `ticket.docx`, `ticket.md` is used as fallback.

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

The helper automatically bumps the last number in `pyproject.toml` before it builds and pushes the release.

## Publish

First publish to TestPyPI:

```powershell
python -m twine upload --repository testpypi dist/*
```

Then publish to PyPI:

```powershell
python -m twine upload dist/*
```
