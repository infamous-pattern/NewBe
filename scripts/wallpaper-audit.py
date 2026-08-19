#!/usr/bin/env python3

"""Validate the checked-in NewBe wallpaper pack without external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import struct
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
WALLPAPER_ROOT = PROJECT_ROOT / "assets" / "wallpapers"

WALLPAPERS = (
    "01-desert-dawn",
    "02-glass-horizon",
    "03-brushed-arc",
    "04-alpine-sun",
    "05-coastal-pavilion",
    "06-floating-panels",
    "07-moon-reflection",
)

RESOLUTIONS = (
    (1920, 1080),
    (1920, 1200),
    (2560, 1440),
    (2560, 1600),
    (3440, 1440),
    (3840, 2160),
    (5120, 2160),
)

JPEG_START_OF_FRAME = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)

    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"invalid PNG: {path}")

    return struct.unpack(">II", header[16:24])


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        if stream.read(2) != b"\xff\xd8":
            raise ValueError(f"invalid JPEG: {path}")

        while True:
            marker_start = stream.read(1)
            if not marker_start:
                break
            if marker_start != b"\xff":
                continue

            marker = stream.read(1)
            while marker == b"\xff":
                marker = stream.read(1)
            if not marker:
                break

            marker_value = marker[0]
            if marker_value in {0x01, *range(0xD0, 0xDA)}:
                continue

            length_data = stream.read(2)
            if len(length_data) != 2:
                break
            segment_length = struct.unpack(">H", length_data)[0]
            if segment_length < 2:
                break

            if marker_value in JPEG_START_OF_FRAME:
                frame = stream.read(5)
                if len(frame) != 5:
                    break
                height, width = struct.unpack(">HH", frame[1:5])
                return width, height

            stream.seek(segment_length - 2, 1)

    raise ValueError(f"JPEG dimensions not found: {path}")


def expected_files() -> dict[Path, tuple[int, int] | None]:
    expected: dict[Path, tuple[int, int] | None] = {}

    for wallpaper in WALLPAPERS:
        source = Path(wallpaper) / f"newbe-{wallpaper}-source.png"
        expected[source] = None

        for width, height in RESOLUTIONS:
            filename = f"newbe-{wallpaper}-{width}x{height}.jpg"
            expected[Path(wallpaper) / filename] = (width, height)

    return expected


def digest(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def checksum_text(paths: list[Path]) -> str:
    lines = [f"{digest(WALLPAPER_ROOT / path)}  {path.as_posix()}" for path in paths]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-checksums",
        action="store_true",
        help="replace SHA256SUMS with checksums for the validated wallpaper files",
    )
    args = parser.parse_args()

    expected = expected_files()
    expected_paths = sorted(expected)
    actual_paths = sorted(
        path.relative_to(WALLPAPER_ROOT)
        for path in WALLPAPER_ROOT.glob("[0-9][0-9]-*/*")
        if path.is_file() and (path.suffix == ".jpg" or path.name.endswith("-source.png"))
    )

    if actual_paths != expected_paths:
        missing = sorted(set(expected_paths) - set(actual_paths))
        extra = sorted(set(actual_paths) - set(expected_paths))
        for path in missing:
            print(f"ERROR: missing wallpaper asset: {path}")
        for path in extra:
            print(f"ERROR: unexpected wallpaper asset: {path}")
        return 1

    for relative_path, dimensions in expected.items():
        path = WALLPAPER_ROOT / relative_path
        actual_dimensions = (
            png_dimensions(path) if path.suffix == ".png" else jpeg_dimensions(path)
        )
        if dimensions is not None and actual_dimensions != dimensions:
            print(
                f"ERROR: {relative_path} is {actual_dimensions[0]}x{actual_dimensions[1]}, "
                f"expected {dimensions[0]}x{dimensions[1]}"
            )
            return 1

    checksums = checksum_text(expected_paths)
    checksum_path = WALLPAPER_ROOT / "SHA256SUMS"

    if args.write_checksums:
        checksum_path.write_text(checksums, encoding="utf-8")
    elif not checksum_path.exists() or checksum_path.read_text(encoding="utf-8") != checksums:
        print("ERROR: assets/wallpapers/SHA256SUMS is missing or stale")
        return 1

    print("NewBe Wallpaper Audit")
    print("=====================")
    print(f"Wallpaper masters: {len(WALLPAPERS)}")
    print(f"Exported JPEGs:    {len(WALLPAPERS) * len(RESOLUTIONS)}")
    print(f"Verified assets:   {len(expected_paths)}")
    print("Checksums:         current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
