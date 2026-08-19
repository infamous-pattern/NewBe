#!/usr/bin/env python3

from __future__ import annotations

import argparse
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


def live_requests() -> dict[str, set[str]]:
    requested: dict[str, set[str]] = {}

    for desktop in desktop_files():
        icon = read_icon_name(desktop)

        if not icon:
            continue

        requested.setdefault(icon, set()).add(desktop.name)

    return requested


def manifest_requests(path: Path) -> dict[str, set[str]]:
    requested: dict[str, set[str]] = {}

    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{path}:{line_number}: invalid coverage entry")
        icon, desktop_names = (item.strip() for item in line.split("=", 1))
        users = {item.strip() for item in desktop_names.split(",") if item.strip()}
        if not icon or not users:
            raise ValueError(f"{path}:{line_number}: empty icon or desktop name")
        requested.setdefault(icon, set()).update(users)

    return requested


def report(requested: dict[str, set[str]], available: set[str]) -> str:
    covered = sorted(name for name in requested if name in available)
    missing = sorted(name for name in requested if name not in available)

    total = len(requested)
    coverage = (len(covered) / total * 100.0) if total else 100.0

    lines = [
        "NewBe Icon Coverage Audit",
        "=========================",
        "",
        f"Unique themed icon names requested: {total}",
        f"NewBe native matches:               {len(covered)}",
        f"Fallback required:                  {len(missing)}",
        f"Native coverage:                    {coverage:.1f}%",
        "",
    ]

    if missing:
        lines.extend(["Missing NewBe icons", "-------------------"])

        for icon in missing:
            users = ", ".join(sorted(requested[icon]))
            lines.extend([icon, f"  {users}"])

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit NewBe application icons.")
    parser.add_argument(
        "--manifest",
        type=Path,
        help="use a deterministic icon-to-desktop manifest instead of live apps",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--output", type=Path, help="write the report to a file")
    output.add_argument("--check", type=Path, help="verify that a report is current")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested = (
        manifest_requests(args.manifest)
        if args.manifest is not None
        else live_requests()
    )
    rendered = report(requested, theme_icons())

    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    elif args.check is not None:
        if not args.check.is_file():
            print(f"ERROR: missing coverage report: {args.check}", file=sys.stderr)
            return 1
        if args.check.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale coverage report: {args.check}", file=sys.stderr)
            return 1
    else:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    sys.exit(main())
