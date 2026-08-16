#!/usr/bin/env python3

from __future__ import annotations

import configparser
import os
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ICON_ROOT = PROJECT_ROOT / "icons" / "NewBe"

APPLICATION_DIRS = [
    Path("/usr/share/applications"),
    Path.home() / ".local/share/applications",
]


def desktop_files() -> list[Path]:
    files: list[Path] = []

    for directory in APPLICATION_DIRS:
        if directory.is_dir():
            files.extend(sorted(directory.glob("*.desktop")))

    return files


def read_icon_name(path: Path) -> str | None:
    parser = configparser.ConfigParser(
        interpolation=None,
        strict=False,
    )

    try:
        parser.read(path, encoding="utf-8")
    except (OSError, UnicodeError, configparser.Error):
        return None

    if "Desktop Entry" not in parser:
        return None

    entry = parser["Desktop Entry"]

    if entry.get("NoDisplay", "").lower() == "true":
        return None

    icon = entry.get("Icon", "").strip()

    if not icon:
        return None

    # Absolute icons bypass icon-theme lookup.
    if os.path.isabs(icon):
        return None

    return icon


def theme_icons() -> set[str]:
    icons: set[str] = set()

    if not ICON_ROOT.is_dir():
        return icons

    for path in ICON_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".svg", ".png", ".xpm"}:
            continue

        icons.add(path.stem)

    return icons


def main() -> int:
    available = theme_icons()

    requested: dict[str, set[str]] = {}

    for desktop in desktop_files():
        icon = read_icon_name(desktop)

        if not icon:
            continue

        requested.setdefault(icon, set()).add(desktop.name)

    covered = sorted(name for name in requested if name in available)
    missing = sorted(name for name in requested if name not in available)

    total = len(requested)
    coverage = (len(covered) / total * 100.0) if total else 100.0

    print("NewBe Icon Coverage Audit")
    print("=========================")
    print()
    print(f"Unique themed icon names requested: {total}")
    print(f"NewBe native matches:               {len(covered)}")
    print(f"Fallback required:                  {len(missing)}")
    print(f"Native coverage:                    {coverage:.1f}%")
    print()

    if missing:
        print("Missing NewBe icons")
        print("-------------------")

        for icon in missing:
            users = ", ".join(sorted(requested[icon]))
            print(f"{icon}")
            print(f"  {users}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
