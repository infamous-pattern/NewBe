#!/usr/bin/env python3

"""Compile NewBe SVG cursor sources into the Xcursor binary format."""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import shutil
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CURSOR_ROOT = PROJECT_ROOT / "cursors"
SOURCE_ROOT = CURSOR_ROOT / "src"
CURSOR_CONFIG = CURSOR_ROOT / "cursors.conf"
ALIAS_CONFIG = CURSOR_ROOT / "aliases.conf"
DEFAULT_OUTPUT = PROJECT_ROOT / "icons" / "NewBe" / "cursors"
SIZES = (24, 32, 48, 64)


class XcursorImage(ctypes.Structure):
    _fields_ = [
        ("version", ctypes.c_uint32),
        ("size", ctypes.c_uint32),
        ("width", ctypes.c_uint32),
        ("height", ctypes.c_uint32),
        ("xhot", ctypes.c_uint32),
        ("yhot", ctypes.c_uint32),
        ("delay", ctypes.c_uint32),
        ("pixels", ctypes.POINTER(ctypes.c_uint32)),
    ]


class XcursorImages(ctypes.Structure):
    _fields_ = [
        ("nimage", ctypes.c_int),
        ("images", ctypes.POINTER(ctypes.POINTER(XcursorImage))),
        ("name", ctypes.c_char_p),
    ]


def data_lines(path: Path) -> list[tuple[int, str]]:
    return [
        (number, line)
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if (line := raw.strip()) and not line.startswith("#")
    ]


def cursors() -> list[tuple[str, int, int]]:
    result: list[tuple[str, int, int]] = []
    for line_number, line in data_lines(CURSOR_CONFIG):
        parts = line.split("|")
        if len(parts) != 3:
            raise ValueError(f"{CURSOR_CONFIG}:{line_number}: invalid cursor entry")
        name, xhot, yhot = parts
        hotspot = (int(xhot), int(yhot))
        if not name.replace("-", "_").isidentifier():
            raise ValueError(f"{CURSOR_CONFIG}:{line_number}: invalid cursor name")
        if not all(0 <= coordinate < 64 for coordinate in hotspot):
            raise ValueError(f"{CURSOR_CONFIG}:{line_number}: invalid hotspot")
        if not (SOURCE_ROOT / f"{name}.svg").is_file():
            raise ValueError(f"missing cursor source: {name}.svg")
        result.append((name, *hotspot))
    if len({name for name, _xhot, _yhot in result}) != len(result):
        raise ValueError("duplicate cursor name")
    return result


def aliases(targets: set[str]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for line_number, line in data_lines(ALIAS_CONFIG):
        if "=" not in line:
            raise ValueError(f"{ALIAS_CONFIG}:{line_number}: invalid alias entry")
        alias, target = line.split("=", 1)
        if not alias or "/" in alias or target not in targets:
            raise ValueError(f"{ALIAS_CONFIG}:{line_number}: invalid alias target")
        result.append((alias, target))
    if len({alias for alias, _target in result}) != len(result):
        raise ValueError("duplicate cursor alias")
    return result


def load_library() -> ctypes.CDLL:
    library_name = ctypes.util.find_library("Xcursor")
    if not library_name:
        raise RuntimeError("libXcursor is required to build cursor binaries")
    library = ctypes.CDLL(library_name)
    library.XcursorImageCreate.argtypes = [ctypes.c_int, ctypes.c_int]
    library.XcursorImageCreate.restype = ctypes.POINTER(XcursorImage)
    library.XcursorImagesCreate.argtypes = [ctypes.c_int]
    library.XcursorImagesCreate.restype = ctypes.POINTER(XcursorImages)
    library.XcursorFilenameSaveImages.argtypes = [
        ctypes.c_char_p,
        ctypes.POINTER(XcursorImages),
    ]
    library.XcursorFilenameSaveImages.restype = ctypes.c_int
    library.XcursorImagesDestroy.argtypes = [ctypes.POINTER(XcursorImages)]
    library.XcursorImagesDestroy.restype = None
    return library


def render_rgba(source: Path, size: int) -> bytes:
    magick = shutil.which("magick") or shutil.which("convert")
    if not magick:
        raise RuntimeError("ImageMagick is required to build cursor binaries")
    command = [
        magick,
        "-background",
        "none",
        str(source),
        "-resize",
        f"{size}x{size}!",
        "-depth",
        "8",
        "rgba:-",
    ]
    rendered = subprocess.run(command, check=True, stdout=subprocess.PIPE).stdout
    expected = size * size * 4
    if len(rendered) != expected:
        raise RuntimeError(
            f"ImageMagick returned {len(rendered)} bytes for {size}x{size}, expected {expected}"
        )
    return rendered


def argb_pixels(rgba: bytes) -> list[int]:
    pixels: list[int] = []
    for red, green, blue, alpha in zip(*[iter(rgba)] * 4, strict=True):
        red = (red * alpha + 127) // 255
        green = (green * alpha + 127) // 255
        blue = (blue * alpha + 127) // 255
        pixels.append((alpha << 24) | (red << 16) | (green << 8) | blue)
    return pixels


def compile_cursor(
    library: ctypes.CDLL,
    source: Path,
    destination: Path,
    hotspot_x: int,
    hotspot_y: int,
) -> None:
    images = library.XcursorImagesCreate(len(SIZES))
    if not images:
        raise MemoryError("XcursorImagesCreate failed")
    images.contents.nimage = len(SIZES)
    try:
        for index, size in enumerate(SIZES):
            image = library.XcursorImageCreate(size, size)
            if not image:
                raise MemoryError("XcursorImageCreate failed")
            image.contents.size = size
            image.contents.xhot = min(size - 1, round(hotspot_x * size / 64))
            image.contents.yhot = min(size - 1, round(hotspot_y * size / 64))
            image.contents.delay = 0
            for pixel_index, pixel in enumerate(argb_pixels(render_rgba(source, size))):
                image.contents.pixels[pixel_index] = pixel
            images.contents.images[index] = image

        if not library.XcursorFilenameSaveImages(
            str(destination).encode("utf-8"), images
        ):
            raise RuntimeError(f"failed to save Xcursor file: {destination}")
    finally:
        library.XcursorImagesDestroy(images)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    cursor_entries = cursors()
    cursor_names = {name for name, _xhot, _yhot in cursor_entries}
    alias_entries = aliases(cursor_names)
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)

    for name in cursor_names | {alias for alias, _target in alias_entries}:
        path = output / name
        if path.exists() or path.is_symlink():
            path.unlink()

    library = load_library()
    for name, hotspot_x, hotspot_y in cursor_entries:
        compile_cursor(
            library,
            SOURCE_ROOT / f"{name}.svg",
            output / name,
            hotspot_x,
            hotspot_y,
        )

    for alias, target in alias_entries:
        (output / alias).symlink_to(target)

    print(
        f"Built {len(cursor_entries)} NewBe cursors at {len(SIZES)} sizes "
        f"with {len(alias_entries)} compatibility aliases."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
