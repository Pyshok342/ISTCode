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

Do not add an `images` command or image-specific public API. It was removed because attachments can be any file type.

Files attached to a ticket:

```cmd
ist-ticket files 6
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

Before publishing a new PyPI release, use `publish_new_version.bat`; it bumps the last number in `pyproject.toml` automatically after tests and GitHub push preflight pass. PyPI never accepts the same version twice. Check current PyPI versions when unsure:

```cmd
python -m pip index versions istcode
```

User-facing publish helper:

```cmd
publish_new_version.bat
```

The helper:

1. Runs tests.
2. Checks GitHub push access.
3. Shows the version bump and asks only `Continue? [y/n]`.
4. Bumps the last number in `pyproject.toml`.
5. Cleans `build/` and `dist/`.
6. Builds package.
7. Runs `twine check` only for the current version artifacts.
8. Builds commit message automatically as `Publish istcode <version>`.
9. Commits changes.
10. Pushes to GitHub.
11. Starts `publish.yml` via `gh workflow run` if GitHub CLI is installed.
12. Otherwise prints the GitHub Actions URL for manual `Run workflow`.

If modifying release flow, keep `publish_new_version.bat`, `PUBLISH_TO_PYPI.md`, `USER_GUIDE_RU.md`, and `.github/workflows/publish.yml` in sync.

## Ticket Data

Preferred editable ticket text lives in Word `.docx` files inside each ticket folder:

```text
src/my_python_library/assets/files/ticket_01/ticket.docx
src/my_python_library/assets/files/ticket_02/ticket.docx
...
src/my_python_library/assets/files/ticket_20/ticket.docx
```

`ticket.md` remains a fallback when `ticket.docx` is missing.
`src/my_python_library/tickets.py` remains the final fallback source when both `ticket.docx` and `ticket.md` are missing.

`ist-ticket N` reads `ticket.docx` with `python-docx`. Paragraphs are printed as plain text. Tables are rendered as console-friendly ASCII grids.
Old binary `.doc` files are not supported unless a converter is added later.

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
`ist-ticket open N` tries to open every non-README file in that ticket folder, keeps going if one file fails, reports failed files, and also opens the ticket folder so the user can see all contents.

Folder contents are intentionally dynamic. Do not hardcode attachment filenames in tests or docs. A ticket folder may contain any mix of `.md`, `.jpg`, `.png`, `.pptx`, `.pdf`, `.docx`, `.xlsx`, `.txt`, or other normal user files.

Public helpers:

```python
from my_python_library import format_ticket, get_ticket, list_ticket_numbers
```

File helpers:

```python
from my_python_library import format_ticket_files, list_ticket_files, list_tickets_with_files
```

When changing tickets:

1. Prefer editing the matching `ticket.docx`, for example `src/my_python_library/assets/files/ticket_06/ticket.docx`.
2. If no Word file exists, edit fallback `ticket.md`.
3. Keep ticket numbers sequential unless user asks otherwise.
4. Run `python -m pytest`.
5. Test CLI with `ist-ticket 1`.

When adding files/photos/presentations:

1. Put files into the matching folder, e.g. `src/my_python_library/assets/files/ticket_06`.
2. Do not edit Python mapping for normal attachments; folder contents are discovered automatically.
3. Tests must assert current discovered files, not a specific filename such as `ticket_1_question_1_types.png`.
4. Keep filenames ASCII when possible.
5. Run `python -m pytest`.
6. Test `ist-ticket files <number>` and `ist-ticket open <number>`.
7. Let `publish_new_version.bat` bump `version` in `pyproject.toml` before PyPI publish.

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
python -m pip install --upgrade --force-reinstall --no-cache-dir istcode
```

GitHub fallback:

```cmd
python -m pip install --upgrade --force-reinstall --no-cache-dir https://github.com/Pyshok342/ISTCode/archive/refs/heads/main.zip
```

After install:

```cmd
ist-ticket 1
```

Fallback:

```cmd
python -m my_python_library 1
```
