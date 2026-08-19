#!/usr/bin/env python3

"""Validate NewBe Xcursor binaries, SVG sources, hotspots, and aliases."""

from __future__ import annotations

import struct
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CURSOR_ROOT = PROJECT_ROOT / "cursors"
SOURCE_ROOT = CURSOR_ROOT / "src"
OUTPUT_ROOT = PROJECT_ROOT / "icons" / "NewBe" / "cursors"
SIZES = {24, 32, 48, 64}
XCURSOR_MAGIC = 0x72756358
XCURSOR_IMAGE_TYPE = 0xFFFD0002


def data_lines(path: Path) -> list[str]:
    return [
        line
        for raw in path.read_text(encoding="utf-8").splitlines()
        if (line := raw.strip()) and not line.startswith("#")
    ]


def cursor_names() -> set[str]:
    names = {line.split("|", 1)[0] for line in data_lines(CURSOR_ROOT / "cursors.conf")}
    sources = {path.stem for path in SOURCE_ROOT.glob("*.svg")}
    if names != sources:
        raise ValueError(f"cursor source mismatch: missing={names - sources}, extra={sources - names}")
    return names


def aliases() -> dict[str, str]:
    return dict(line.split("=", 1) for line in data_lines(CURSOR_ROOT / "aliases.conf"))


def audit_binary(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 16:
        raise ValueError(f"truncated Xcursor file: {path}")
    magic, header_length, version, toc_count = struct.unpack_from("<4I", data)
    if magic != XCURSOR_MAGIC or header_length != 16 or version != 0x00010000:
        raise ValueError(f"invalid Xcursor header: {path}")
    if toc_count != len(SIZES):
        raise ValueError(f"unexpected image count in {path}: {toc_count}")

    found_sizes: set[int] = set()
    for index in range(toc_count):
        chunk_type, subtype, position = struct.unpack_from("<3I", data, 16 + index * 12)
        if chunk_type != XCURSOR_IMAGE_TYPE or subtype not in SIZES:
            raise ValueError(f"invalid Xcursor TOC entry: {path}")
        chunk = struct.unpack_from("<9I", data, position)
        chunk_header, image_type, image_size, image_version = chunk[:4]
        width, height, xhot, yhot, _delay = chunk[4:]
        if (
            chunk_header != 36
            or image_type != XCURSOR_IMAGE_TYPE
            or image_size != subtype
            or image_version != 1
            or width != subtype
            or height != subtype
            or xhot >= width
            or yhot >= height
            or position + 36 + width * height * 4 > len(data)
        ):
            raise ValueError(f"invalid Xcursor image chunk: {path}")
        pixels = struct.unpack_from(f"<{width * height}I", data, position + 36)
        corners = (pixels[0], pixels[width - 1], pixels[-width], pixels[-1])
        if not any(pixel >> 24 == 0 for pixel in corners) or not any(
            pixel >> 24 for pixel in pixels
        ):
            raise ValueError(f"invalid Xcursor transparency: {path}")
        found_sizes.add(subtype)
    if found_sizes != SIZES:
        raise ValueError(f"missing Xcursor sizes in {path}: {SIZES - found_sizes}")


def main() -> int:
    names = cursor_names()
    alias_map = aliases()
    if not set(alias_map.values()) <= names:
        raise ValueError("cursor alias references an unknown target")

    expected = names | set(alias_map)
    actual = {path.name for path in OUTPUT_ROOT.iterdir()}
    if actual != expected:
        raise ValueError(f"compiled cursor mismatch: missing={expected - actual}, extra={actual - expected}")

    for name in sorted(names):
        path = OUTPUT_ROOT / name
        if path.is_symlink():
            raise ValueError(f"compiled cursor must not be a symlink: {path}")
        audit_binary(path)

    for alias, target in sorted(alias_map.items()):
        path = OUTPUT_ROOT / alias
        if not path.is_symlink() or path.readlink() != Path(target):
            raise ValueError(f"invalid cursor alias: {alias} -> {target}")

    print("NewBe Cursor Audit")
    print("==================")
    print(f"Cursor designs:       {len(names)}")
    print(f"Raster sizes/design:  {len(SIZES)}")
    print(f"Compatibility aliases: {len(alias_map)}")
    print("Xcursor binaries:     valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
