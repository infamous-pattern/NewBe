#!/usr/bin/env python3

from __future__ import annotations

import configparser
import os
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ICON_ROOT = PROJECT_ROOT / "icons" / "NewBe"
MANIFEST_ROOT = PROJECT_ROOT / "icons" / "manifests"

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

    if os.path.isabs(icon):
        return None

    return icon


def theme_icons() -> set[str]:
    icons: set[str] = set()

    if not ICON_ROOT.is_dir():
        return icons

    for path in ICON_ROOT.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue

        if path.suffix.lower() not in {".svg", ".png", ".xpm"}:
            continue

        icons.add(path.stem)

    return icons


def read_manifest(name: str) -> list[str]:
    path = MANIFEST_ROOT / name

    if not path.exists():
        return []

    entries = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        entries.append(line)

    return entries


def app_inventory() -> dict[str, set[str]]:
    requested: dict[str, set[str]] = {}

    for desktop in desktop_files():
        icon = read_icon_name(desktop)

        if not icon:
            continue

        requested.setdefault(icon, set()).add(desktop.name)

    return requested


def coverage(expected: list[str], available: set[str]) -> tuple[int, int, float]:
    total = len(expected)
    native = sum(1 for name in expected if name in available)

    pct = (native / total * 100.0) if total else 100.0

    return native, total, pct


def print_section(
    title: str,
    native: int,
    total: int,
    pct: float,
) -> None:
    print(title)
    print("-" * len(title))
    print(f"Expected:   {total}")
    print(f"Native:     {native}")
    print(f"Fallback:   {total - native}")
    print(f"Coverage:   {pct:.1f}%")
    print()


def main() -> int:
    available = theme_icons()

    apps = app_inventory()
    app_expected = sorted(apps)

    places = read_manifest("places.txt")
    devices = read_manifest("devices.txt")
    symbolic = read_manifest("symbolic.txt")

    app_native, app_total, app_pct = coverage(app_expected, available)
    place_native, place_total, place_pct = coverage(places, available)
    device_native, device_total, device_pct = coverage(devices, available)
    symbolic_native, symbolic_total, symbolic_pct = coverage(symbolic, available)

    overall_total = (
        app_total +
        place_total +
        device_total +
        symbolic_total
    )

    overall_native = (
        app_native +
        place_native +
        device_native +
        symbolic_native
    )

    overall_pct = (
        overall_native / overall_total * 100.0
        if overall_total
        else 100.0
    )

    print("NewBe Icon Coverage Audit")
    print("=========================")
    print()

    print_section(
        "Applications",
        app_native,
        app_total,
        app_pct,
    )

    print_section(
        "Places",
        place_native,
        place_total,
        place_pct,
    )

    print_section(
        "Devices",
        device_native,
        device_total,
        device_pct,
    )

    print_section(
        "Symbolic UI",
        symbolic_native,
        symbolic_total,
        symbolic_pct,
    )

    print_section(
        "Overall",
        overall_native,
        overall_total,
        overall_pct,
    )

    missing_apps = sorted(
        name for name in app_expected if name not in available
    )

    if missing_apps:
        print("Missing application icons")
        print("-------------------------")

        for icon in missing_apps:
            users = ", ".join(sorted(apps[icon]))
            print(f"{icon}")
            print(f"  {users}")

        print()

    for title, expected in (
        ("Missing Places", places),
        ("Missing Devices", devices),
        ("Missing Symbolic UI", symbolic),
    ):
        missing = [name for name in expected if name not in available]

        if not missing:
            continue

        print(title)
        print("-" * len(title))

        for name in missing:
            print(name)

        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
