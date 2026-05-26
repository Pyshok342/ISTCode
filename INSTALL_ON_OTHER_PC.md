# Install on another computer

## 1. Install Python

Install Python 3.10 or newer from:

https://www.python.org/downloads/

During install, enable:

```text
Add python.exe to PATH
```

## 2. Copy this wheel file to the other computer

```text
my_python_library-0.1.0-py3-none-any.whl
```

## 3. Install

Open PowerShell in the folder with the `.whl` file:

```powershell
python -m pip install .\my_python_library-0.1.0-py3-none-any.whl
```

## 4. Test

```powershell
python -c "from my_python_library import hello; print(hello('Alex'))"
```

Expected output:

```text
Hello, Alex!
```

## Optional: uninstall

```powershell
python -m pip uninstall my-python-library
```
