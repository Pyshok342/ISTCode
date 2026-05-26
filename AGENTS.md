# AGENTS.md

## Project

ISTCode is a Python package with a console command for printing exam tickets.

Main local path:

```text
C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library
```

GitHub repo:

```text
https://github.com/Pyshok342/ISTCode
```

## User Style

User prefers Russian, direct commands, minimal English. Keep instructions concrete and copy-paste ready.

## Package

Important files:

```text
pyproject.toml
src/my_python_library/tickets.py
src/my_python_library/cli.py
src/my_python_library/__main__.py
tests/test_core.py
README.md
USER_GUIDE_RU.md
```

Console script:

```cmd
ist-ticket 1
```

Fallback module launch:

```cmd
python -m my_python_library 1
```

List tickets:

```cmd
ist-ticket list
```

## Development

Use local venv:

```cmd
cd "C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library"
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Run tests:

```cmd
python -m pytest
```

Build:

```cmd
python -m build
```

## Ticket Data

Ticket data is hardcoded in:

```text
src/my_python_library/tickets.py
```

Public helpers:

```python
from my_python_library import format_ticket, get_ticket, list_ticket_numbers
```

When changing tickets:

1. Edit `TICKETS`.
2. Keep ticket numbers sequential unless user asks otherwise.
3. Run `python -m pytest`.
4. Test CLI with `ist-ticket 1`.

## Git Notes

The `.git` directory may be owned by the normal Windows user, not the Codex sandbox. If Codex cannot run `git add` because of `index.lock` or permission denied, give the user exact commands:

```cmd
git add .
git commit -m "Update tickets"
git push
```

Do not include generated or local folders in commits:

```text
.venv/
.pytest_cache/
dist/
build/
tmp_doc_extract/
src/my_python_library.egg-info/
```

## Install Command For Other Computers

Current user-facing install command:

```cmd
python -m pip install istcode
```

GitHub fallback:

```cmd
python -m pip install --upgrade https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

After install:

```cmd
ist-ticket 1
```

Fallback:

```cmd
python -m my_python_library 1
```
