#!/usr/bin/env python3

"""Generate GNOME background metadata for the installed NewBe wallpapers."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
WALLPAPER_SOURCE = PROJECT_ROOT / "assets" / "wallpapers"
WALLPAPER_CONFIG = WALLPAPER_SOURCE / "wallpapers.conf"
EXPORT_SIZE = "3840x2160"
VALID_ROLE = {
    "supporting",
    "hero-light-default",
    "hero-light-alternate",
    "hero-dark-default",
}
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def load_wallpapers() -> list[tuple[str, str, str]]:
    wallpapers: list[tuple[str, str, str]] = []

    for line_number, raw_line in enumerate(
        WALLPAPER_CONFIG.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split("|")
        if len(parts) != 3:
            raise ValueError(f"{WALLPAPER_CONFIG}:{line_number}: invalid entry")

        number, slug, role = parts
        if not re.fullmatch(r"[0-9]{2}", number):
            raise ValueError(f"{WALLPAPER_CONFIG}:{line_number}: invalid number")
        if not SLUG_PATTERN.fullmatch(slug):
            raise ValueError(f"{WALLPAPER_CONFIG}:{line_number}: invalid slug")
        if role not in VALID_ROLE:
            raise ValueError(f"{WALLPAPER_CONFIG}:{line_number}: invalid role")

        source = (
            WALLPAPER_SOURCE
            / f"{number}-{slug}"
            / f"newbe-{number}-{slug}-{EXPORT_SIZE}.jpg"
        )
        if not source.is_file():
            raise ValueError(f"missing wallpaper export: {source}")

        wallpapers.append((number, slug, role))

    identities = {(number, slug) for number, slug, _role in wallpapers}
    if len(identities) != len(wallpapers):
        raise ValueError(f"duplicate wallpaper entry in {WALLPAPER_CONFIG}")
    if len(wallpapers) != 7:
        raise ValueError(f"expected 7 wallpapers, found {len(wallpapers)}")

    role_counts = {role: 0 for role in VALID_ROLE}
    for _number, _slug, role in wallpapers:
        role_counts[role] += 1
    if role_counts["hero-light-default"] != 1:
        raise ValueError("expected exactly one light default wallpaper")
    if role_counts["hero-dark-default"] != 1:
        raise ValueError("expected exactly one dark default wallpaper")

    return wallpapers


def installed_filename(root: Path, number: str, slug: str) -> Path:
    return root / f"newbe-{number}-{slug}-{EXPORT_SIZE}.jpg"


def build_xml(wallpaper_root: Path) -> bytes:
    wallpapers = load_wallpapers()
    dark_default = next(
        (number, slug)
        for number, slug, role in wallpapers
        if role == "hero-dark-default"
    )

    root = ET.Element("wallpapers")
    for number, slug, role in wallpapers:
        wallpaper = ET.SubElement(root, "wallpaper", {"deleted": "false"})
        title = " ".join(word.capitalize() for word in slug.split("-"))
        ET.SubElement(wallpaper, "name").text = f"NewBe — {title}"
        ET.SubElement(wallpaper, "filename").text = str(
            installed_filename(wallpaper_root, number, slug)
        )
        if role == "hero-light-default":
            dark_number, dark_slug = dark_default
            ET.SubElement(wallpaper, "filename-dark").text = str(
                installed_filename(wallpaper_root, dark_number, dark_slug)
            )
        ET.SubElement(wallpaper, "options").text = "zoom"
        ET.SubElement(wallpaper, "pcolor").text = "#292b28"
        ET.SubElement(wallpaper, "scolor").text = "#d6a928"

    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wallpaper-root",
        required=True,
        type=Path,
        help="absolute directory containing the installed 4K wallpaper files",
    )
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument("--output", type=Path, help="write GNOME XML to this path")
    output.add_argument(
        "--check",
        action="store_true",
        help="validate the manifest and generated XML without writing files",
    )
    args = parser.parse_args()

    wallpaper_root = args.wallpaper_root.expanduser()
    if not wallpaper_root.is_absolute():
        parser.error("--wallpaper-root must be an absolute path")
    wallpaper_root = wallpaper_root.resolve()
    xml_data = build_xml(wallpaper_root)

    parsed = ET.fromstring(xml_data)
    entries = parsed.findall("wallpaper")
    if parsed.tag != "wallpapers" or len(entries) != 7:
        raise ValueError("generated GNOME background metadata is invalid")

    if args.check:
        print("NewBe GNOME background metadata: valid (7 wallpapers)")
        return 0

    output_path = args.output.expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(xml_data)
    print(f"Wrote NewBe GNOME background metadata: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
