@echo off
setlocal

cd /d "%~dp0"

echo.
echo ISTCode publish helper
echo ======================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv not found.
  echo Run first:
  echo   python -m venv .venv
  echo   .venv\Scripts\python.exe -m pip install -e ".[dev]"
  exit /b 1
)

echo Checking package version...
.venv\Scripts\python.exe -c "import tomllib; print('Version:', tomllib.load(open('pyproject.toml','rb'))['project']['version'])"
if errorlevel 1 exit /b 1

echo.
echo Running tests...
.venv\Scripts\python.exe -m pytest
if errorlevel 1 (
  echo.
  echo ERROR: tests failed. Fix tests before publish.
  exit /b 1
)

echo.
echo Checking package build...
.venv\Scripts\python.exe -m build
if errorlevel 1 exit /b 1

.venv\Scripts\python.exe -m twine check dist\istcode-*
if errorlevel 1 exit /b 1

echo.
echo Git status:
git status --short
if errorlevel 1 exit /b 1

echo.
set /p COMMIT_MSG=Commit message [Publish new version]: 
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Publish new version

git add .
if errorlevel 1 exit /b 1

git diff --cached --quiet
if errorlevel 1 (
  git commit -m "%COMMIT_MSG%"
  if errorlevel 1 exit /b 1
) else (
  echo Nothing to commit.
)

git push
if errorlevel 1 exit /b 1

echo.
where gh >nul 2>nul
if errorlevel 1 (
  echo GitHub CLI gh not found.
  echo.
  echo Open this page and run workflow manually:
  echo   https://github.com/Pyshok342/ISTCode/actions/workflows/publish.yml
  echo.
  echo Click:
  echo   Run workflow - main - Run workflow
  echo.
  goto done
)

echo Starting GitHub Actions publish workflow...
gh workflow run publish.yml --ref main
if errorlevel 1 (
  echo.
  echo Could not start workflow with gh.
  echo Open manually:
  echo   https://github.com/Pyshok342/ISTCode/actions/workflows/publish.yml
  goto done
)

echo.
echo Workflow started.
echo Check progress:
echo   https://github.com/Pyshok342/ISTCode/actions/workflows/publish.yml

:done
echo.
echo After workflow succeeds, update on any computer:
echo   python -m pip install --upgrade istcode
echo.
echo Press any key to close.
pause >nul
