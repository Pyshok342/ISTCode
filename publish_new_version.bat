@echo off
setlocal

cd /d "%~dp0"
set "STEP=starting"
set "LOCAL_TEMP=%CD%\.tmp"
set "TEMP=%LOCAL_TEMP%\temp"
set "TMP=%LOCAL_TEMP%\temp"
set "PYTEST_BASETEMP=%TEMP%\pytest-%RANDOM%-%RANDOM%"

echo.
echo ISTCode publish helper
echo ======================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv not found.
  echo Run first:
  echo   python -m venv .venv
  echo   .venv\Scripts\python.exe -m pip install -e ".[dev]"
  goto fail
)

if not exist "%LOCAL_TEMP%" mkdir "%LOCAL_TEMP%"
if errorlevel 1 goto fail
if not exist "%TEMP%" mkdir "%TEMP%"
if errorlevel 1 goto fail

echo Checking package version...
set "STEP=reading package version"
for /f "delims=" %%v in ('.venv\Scripts\python.exe -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])"') do set VERSION=%%v
echo Version: %VERSION%
if errorlevel 1 goto fail

echo.
echo Running tests...
set "STEP=running tests"
.venv\Scripts\python.exe -m pytest --basetemp "%PYTEST_BASETEMP%" -p no:cacheprovider
if errorlevel 1 (
  echo.
  echo ERROR: tests failed. Fix tests before publish.
  goto fail
)

echo.
echo Checking package build...
set "STEP=cleaning build folder"
if exist "build" rmdir /s /q "build"
if errorlevel 1 goto fail
set "STEP=cleaning dist folder"
if exist "dist" rmdir /s /q "dist"
if errorlevel 1 goto fail

set "STEP=building package"
.venv\Scripts\python.exe -m build
if errorlevel 1 goto fail

set "STEP=checking package with twine"
.venv\Scripts\python.exe -m twine check dist\istcode-%VERSION%*
if errorlevel 1 goto fail

echo.
echo Git status:
set "STEP=reading git status"
git status --short
if errorlevel 1 goto fail

echo.
echo Checking GitHub push access...
set "STEP=checking GitHub push access"
set "GCM_HAS_ACCOUNT="
for /f "delims=" %%a in ('git credential-manager github list 2^>nul') do set "GCM_HAS_ACCOUNT=1"
if not defined GCM_HAS_ACCOUNT (
  echo WARNING: Git Credential Manager has no saved GitHub account.
  echo Login command:
  echo   git credential-manager github login --no-ui
  echo.
)
git -c http.sslBackend=openssl push --dry-run
if errorlevel 1 (
  echo.
  echo ERROR: GitHub push access failed.
  echo Git cannot push to this repository.
  echo.
  echo Try this, then run publish_new_version.bat again:
  echo   git credential-manager github login --no-ui
  echo   git credential-manager github list
  echo.
  echo If HTTPS still fails, use SSH:
  echo   git remote set-url origin git@github.com:Pyshok342/ISTCode.git
  goto fail
)

echo.
set COMMIT_MSG=Publish istcode %VERSION%
echo Commit message:
echo   %COMMIT_MSG%
echo.
set /p CONFIRM=Continue? [y/n]: 
if /i not "%CONFIRM%"=="y" (
  echo Cancelled.
  goto cancelled
)

set "STEP=staging files"
git add .
if errorlevel 1 goto fail

set "STEP=checking staged files"
git diff --cached --quiet
if errorlevel 1 (
  set "STEP=creating git commit"
  git commit -m "%COMMIT_MSG%"
  if errorlevel 1 goto fail
) else (
  echo Nothing to commit.
)

set "STEP=pushing to GitHub"
git -c http.sslBackend=openssl push
if errorlevel 1 goto fail

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
echo   python -m pip install --upgrade --force-reinstall --no-cache-dir istcode
echo.
echo Press any key to close.
pause >nul
exit /b 0

:cancelled
echo.
echo Press any key to close.
pause >nul
exit /b 0

:fail
echo.
echo Publish failed while: %STEP%
echo Press any key to close.
pause >nul
exit /b 1
