#!/usr/bin/env python3

"""Build and validate a reproducible, versioned NewBe release archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "VERSION"
PACKAGE_ITEMS = (
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSES",
    "README.md",
    "SECURITY.md",
    "VERSION",
    "assets",
    "cursors",
    "docs",
    "extension",
    "gnome-shell",
    "gtk-3.0",
    "gtk-4.0",
    "icons",
    "scripts",
    "themes",
)
REQUIRED_MEMBERS = (
    "README.md",
    "docs/ACCESSIBILITY.md",
    "docs/COMPATIBILITY.md",
    "LICENSE",
    "LICENSES/MIT.txt",
    "LICENSES/CC-BY-SA-4.0.txt",
    "VERSION",
    "scripts/install.sh",
    "scripts/release-metadata-audit.py",
    "scripts/uninstall.sh",
    "scripts/verify.sh",
    "themes/NewBe/gnome-shell/gnome-shell.css",
    "icons/NewBe/index.theme",
    "icons/NewBe/cursors/left_ptr",
    "extension/newbe@infamous-pattern.github.io/metadata.json",
    "assets/wallpapers/02-glass-horizon/newbe-02-glass-horizon-3840x2160.jpg",
)


def version() -> str:
    value = VERSION_FILE.read_text(encoding="utf-8").strip()
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
    if not value or set(value) - allowed or value.startswith((".", "-")):
        raise ValueError(f"invalid VERSION: {value!r}")
    return value


def package_paths() -> list[Path]:
    paths: list[Path] = []
    for item in PACKAGE_ITEMS:
        source = PROJECT_ROOT / item
        if not source.exists():
            raise FileNotFoundError(f"missing release input: {source}")
        paths.append(source)
        if source.is_dir():
            paths.extend(
                path
                for path in source.rglob("*")
                if "__pycache__" not in path.parts
            )
    return sorted(set(paths), key=lambda path: path.relative_to(PROJECT_ROOT).as_posix())


def file_digest(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def normalized_info(path: Path, archive_name: str) -> tarfile.TarInfo:
    info = tarfile.TarInfo(archive_name)
    status = path.lstat()
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = 0
    info.mode = status.st_mode & 0o777

    if path.is_symlink():
        info.type = tarfile.SYMTYPE
        info.linkname = path.readlink().as_posix()
        info.size = 0
    elif path.is_dir():
        info.type = tarfile.DIRTYPE
        info.size = 0
    elif path.is_file():
        info.type = tarfile.REGTYPE
        info.size = status.st_size
    else:
        raise ValueError(f"unsupported release input type: {path}")
    return info


def create_archive(output: Path, release_version: str) -> None:
    for license_path in (
        PROJECT_ROOT / "LICENSE",
        PROJECT_ROOT / "LICENSES" / "MIT.txt",
        PROJECT_ROOT / "LICENSES" / "CC-BY-SA-4.0.txt",
    ):
        if not license_path.is_file() or not license_path.read_text(encoding="utf-8").strip():
            raise ValueError(f"missing or empty release license: {license_path}")

    subprocess.run([PROJECT_ROOT / "scripts" / "build-themes.sh"], check=True)
    prefix = f"NewBe-{release_version}"
    paths = package_paths()
    manifest_lines = [
        f"{file_digest(path)}  {path.relative_to(PROJECT_ROOT).as_posix()}"
        for path in paths
        if path.is_file() and not path.is_symlink()
    ]
    manifest = ("\n".join(manifest_lines) + "\n").encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw_stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_stream, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in paths:
                    relative = path.relative_to(PROJECT_ROOT).as_posix()
                    info = normalized_info(path, f"{prefix}/{relative}")
                    if info.isfile():
                        with path.open("rb") as stream:
                            archive.addfile(info, stream)
                    else:
                        archive.addfile(info)

                manifest_info = tarfile.TarInfo(f"{prefix}/RELEASE-MANIFEST.sha256")
                manifest_info.size = len(manifest)
                manifest_info.mode = 0o644
                manifest_info.uid = 0
                manifest_info.gid = 0
                manifest_info.uname = "root"
                manifest_info.gname = "root"
                manifest_info.mtime = 0
                archive.addfile(manifest_info, io.BytesIO(manifest))

    digest = file_digest(output)
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )


def validate_archive(archive_path: Path, release_version: str) -> None:
    prefix = PurePosixPath(f"NewBe-{release_version}")
    with tarfile.open(archive_path, mode="r:gz") as archive:
        members = archive.getmembers()
        relative_members: dict[str, tarfile.TarInfo] = {}
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts or not path.is_relative_to(prefix):
                raise ValueError(f"unsafe archive member: {member.name}")
            relative = path.relative_to(prefix).as_posix()
            relative_members[relative] = member
            if member.isdev() or member.isfifo() or member.islnk():
                raise ValueError(f"unsupported archive member: {member.name}")
            if member.issym() and (PurePosixPath(member.linkname).is_absolute() or "/" in member.linkname):
                raise ValueError(f"unsafe archive symlink: {member.name}")

        missing = set(REQUIRED_MEMBERS) - set(relative_members)
        if missing:
            raise ValueError(f"release archive is missing required files: {sorted(missing)}")

        manifest_member = relative_members.get("RELEASE-MANIFEST.sha256")
        if not manifest_member:
            raise ValueError("release archive is missing RELEASE-MANIFEST.sha256")
        manifest_stream = archive.extractfile(manifest_member)
        if not manifest_stream:
            raise ValueError("release manifest cannot be read")
        for line in manifest_stream.read().decode("utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            member = relative_members.get(relative)
            if not member or not member.isfile():
                raise ValueError(f"manifest references a missing file: {relative}")
            stream = archive.extractfile(member)
            if not stream or hashlib.sha256(stream.read()).hexdigest() != digest:
                raise ValueError(f"release manifest checksum mismatch: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "dist")
    parser.add_argument(
        "--check",
        action="store_true",
        help="build and validate in a temporary directory without keeping artifacts",
    )
    args = parser.parse_args()

    release_version = version()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="newbe-release-test-") as temporary:
            output = Path(temporary) / f"NewBe-{release_version}.tar.gz"
            create_archive(output, release_version)
            validate_archive(output, release_version)
        print(f"NewBe release archive validation passed: {release_version}")
        return 0

    output = args.output_dir.expanduser().resolve() / f"NewBe-{release_version}.tar.gz"
    create_archive(output, release_version)
    validate_archive(output, release_version)
    print(f"Built and validated: {output}")
    print(f"SHA-256: {output}.sha256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
