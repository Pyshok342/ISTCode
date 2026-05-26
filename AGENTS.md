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

Help:

```cmd
ist-ticket help
```

Files attached to a ticket:

```cmd
ist-ticket files 6
ist-ticket images 6
ist-ticket open 6
```

Fallback help:

```cmd
python -m my_python_library help
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

Before publishing a new PyPI release, bump `version` in `pyproject.toml`; PyPI never accepts the same version twice.

User-facing publish helper:

```cmd
publish_new_version.bat
```

The helper:

1. Runs tests.
2. Builds package.
3. Runs `twine check`.
4. Builds commit message automatically as `Publish istcode <version>`.
5. Asks only `Continue? [y/n]`.
6. Commits changes.
7. Pushes to GitHub.
8. Starts `publish.yml` via `gh workflow run` if GitHub CLI is installed.
9. Otherwise prints the GitHub Actions URL for manual `Run workflow`.

If modifying release flow, keep `publish_new_version.bat`, `PUBLISH_TO_PYPI.md`, `USER_GUIDE_RU.md`, and `.github/workflows/publish.yml` in sync.

## Ticket Data

Editable ticket text lives in `ticket.md` files inside each ticket folder:

```text
src/my_python_library/assets/files/ticket_01/ticket.md
src/my_python_library/assets/files/ticket_02/ticket.md
...
src/my_python_library/assets/files/ticket_20/ticket.md
```

`src/my_python_library/tickets.py` remains the fallback source when `ticket.md` is missing.

Ticket file attachments are stored in:

```text
src/my_python_library/assets/files/ticket_01 ... ticket_20
```

Bundled attachment files live in:

```text
src/my_python_library/assets/files
```

There are 20 per-ticket folders:

```text
ticket_01, ticket_02, ..., ticket_20
```

`ist-ticket files N` prints the ticket folder path and current file names.
`ist-ticket open N` opens every non-README file in that ticket folder. If the folder has no files, it opens the folder itself.

Public helpers:

```python
from my_python_library import format_ticket, get_ticket, list_ticket_numbers
```

File helpers:

```python
from my_python_library import format_ticket_files, list_ticket_files, list_tickets_with_files
```

When changing tickets:

1. Edit the matching `ticket.md`, for example `src/my_python_library/assets/files/ticket_06/ticket.md`.
2. Keep ticket numbers sequential unless user asks otherwise.
3. Run `python -m pytest`.
4. Test CLI with `ist-ticket 1`.

When adding files/photos/presentations:

1. Put files into the matching folder, e.g. `src/my_python_library/assets/files/ticket_06`.
2. Do not edit Python mapping for normal attachments; folder contents are discovered automatically.
3. Keep filenames ASCII when possible.
4. Run `python -m pytest`.
5. Test `ist-ticket files <number>` and `ist-ticket open <number>`.
6. Bump `version` in `pyproject.toml` before PyPI publish.

When changing CLI help:

1. Edit `src/my_python_library/cli.py`.
2. Update `README.md` and `USER_GUIDE_RU.md` if command behavior changes.
3. Add or update tests in `tests/test_core.py`.
4. Run `python -m pytest`.

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
