# Publish to PyPI

After publish, install on any computer:

```powershell
python -m pip install my-python-library
```

## Requirements

1. Create account:
   - https://pypi.org/account/register/
   - https://test.pypi.org/account/register/
2. Pick a unique package name.
3. Update `name` in `pyproject.toml`.
4. Create an API token on PyPI.

## Build

```powershell
cd "C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library"
.venv\Scripts\Activate.ps1
python -m build
```

## Upload to TestPyPI first

```powershell
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI:

```powershell
python -m pip install --index-url https://test.pypi.org/simple/ my-python-library
```

## Upload to PyPI

```powershell
python -m twine upload dist/*
```
