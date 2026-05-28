@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv not found.
  echo Run first:
  echo   python -m venv .venv
  echo   .venv\Scripts\python.exe -m pip install -e ".[dev]"
  pause
  exit /b 1
)

.venv\Scripts\python.exe scripts\build_offline_bundle.py
if errorlevel 1 (
  echo.
  echo Offline bundle build failed.
  pause
  exit /b 1
)

echo.
echo Done.
pause
