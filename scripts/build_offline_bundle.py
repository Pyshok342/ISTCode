from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
WORK_DIR = ROOT / ".tmp" / "offline_bundle"
WINDOWS_PYTHONS = {
    "3.8": ("cp38", ["python-docx>=1.1.2,<1.2", "importlib-resources>=5.12"]),
    "3.9": ("cp39", ["python-docx>=1.1.2"]),
    "3.10": ("cp310", ["python-docx>=1.1.2"]),
    "3.11": ("cp311", ["python-docx>=1.1.2"]),
    "3.12": ("cp312", ["python-docx>=1.1.2"]),
    "3.13": ("cp313", ["python-docx>=1.1.2"]),
}


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def read_version() -> str:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("Could not read version from pyproject.toml")
    return match.group(1)


def write_text(path: Path, text: str) -> None:
    path.write_text(text.replace("\n", "\r\n"), encoding="utf-8")


def download_windows_wheels(wheels_dir: Path) -> None:
    for python_version, (abi, requirements) in WINDOWS_PYTHONS.items():
        print()
        print(f"Downloading Windows wheels for Python {python_version}...")
        run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--dest",
                str(wheels_dir),
                "--only-binary=:all:",
                "--platform",
                "win_amd64",
                "--implementation",
                "cp",
                "--python-version",
                python_version,
                "--abi",
                abi,
                *requirements,
            ]
        )


def make_zip(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir.parent))


def main() -> int:
    version = read_version()
    bundle_name = f"istcode-offline-{version}-win_amd64-py38-py313"
    bundle_dir = WORK_DIR / bundle_name
    wheels_dir = bundle_dir / "wheels"
    zip_path = DIST_DIR / f"{bundle_name}.zip"

    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    if (ROOT / "build").exists():
        shutil.rmtree(ROOT / "build")
    if DIST_DIR.exists():
        for path in DIST_DIR.glob("istcode-*"):
            if path.is_file():
                path.unlink()
    bundle_dir.mkdir(parents=True)
    wheels_dir.mkdir()
    DIST_DIR.mkdir(exist_ok=True)

    run([sys.executable, "-m", "build"])

    for dist_file in DIST_DIR.glob(f"istcode-{version}*"):
        if dist_file.suffix in {".whl", ".gz"}:
            shutil.copy2(dist_file, wheels_dir / dist_file.name)

    download_windows_wheels(wheels_dir)

    write_text(
        bundle_dir / "install_offline.bat",
        """@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  echo ERROR: Python not found.
  echo Install Python 3.8 or newer, then run this file again.
  pause
  exit /b 1
)

%PYTHON_CMD% --version

%PYTHON_CMD% -m pip --version >nul 2>nul
if errorlevel 1 (
  echo.
  echo pip not found. Trying to enable pip with ensurepip...
  %PYTHON_CMD% -m ensurepip --upgrade
  if errorlevel 1 (
    echo.
    echo ERROR: pip is not available and ensurepip failed.
    echo Reinstall Python with pip enabled.
    pause
    exit /b 1
  )
)

echo.
echo Installing ISTCode from local wheels, no internet...
%PYTHON_CMD% -m pip install --no-index --find-links "%CD%\\wheels" --upgrade --force-reinstall istcode
if errorlevel 1 (
  echo.
  echo ERROR: offline install failed.
  pause
  exit /b 1
)

echo.
echo Installed. Test:
echo   ist-ticket 1
echo.
echo If ist-ticket is not found in this terminal, run:
echo   %PYTHON_CMD% -m my_python_library 1
echo.
pause
""",
    )

    write_text(
        bundle_dir / "README_OFFLINE.txt",
        f"""ISTCode offline bundle {version}

This archive installs ISTCode without internet on Windows x64.
Supported Python: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13.

How to use:
1. Copy this folder to another computer.
2. Install Python 3.8 or newer if it is missing.
3. Run install_offline.bat.
4. Check:
   ist-ticket 1

The installer uses only local files from the wheels folder:
- istcode
- python-docx
- lxml
- importlib-resources for Python 3.8

No internet is required.
If pip is missing, install_offline.bat tries:
  python -m ensurepip --upgrade
""",
    )

    make_zip(bundle_dir, zip_path)
    print()
    print(f"Offline bundle created: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
