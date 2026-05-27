from __future__ import annotations

import argparse
import re
from pathlib import Path


VERSION_RE = re.compile(r'(?m)^version\s*=\s*"([^"]+)"\s*$')


def read_version(path: Path) -> str:
    match = VERSION_RE.search(path.read_text(encoding="utf-8"))
    if match is None:
        raise SystemExit("version field not found in pyproject.toml")
    return match.group(1)


def next_version(version: str) -> str:
    parts = version.split(".")
    if not parts or not parts[-1].isdigit():
        raise SystemExit(f"cannot auto-bump version: {version}")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def write_version(path: Path, version: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = VERSION_RE.subn(f'version = "{version}"', text, count=1)
    if count != 1:
        raise SystemExit("version field not found in pyproject.toml")
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--write")
    args = parser.parse_args()

    path = Path("pyproject.toml")
    current = read_version(path)

    if args.next:
        print(f"{current}|{next_version(current)}")
        return 0

    if args.write:
        write_version(path, args.write)
        print(args.write)
        return 0

    print(current)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
