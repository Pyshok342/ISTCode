# my-python-library

Small example Python library.

## Install for development

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Install from GitHub

After publishing this project to GitHub:

```powershell
python -m pip install git+https://github.com/USERNAME/REPOSITORY.git
```

## Use

```python
from my_python_library import hello

print(hello("Alex"))
```

## Test

```powershell
python -m pytest
```

## Build

```powershell
python -m build
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
