#!/usr/bin/env python3
"""Verify that NewBe release-facing metadata agrees with VERSION."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VERSION_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?$"
)
EXPECTED_SHELL_VERSIONS = ["48", "49", "50"]


def main() -> int:
    errors: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    if not VERSION_PATTERN.fullmatch(version):
        errors.append(f"VERSION is not a supported semantic version: {version!r}")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"^## {re.escape(version)} — \d{{4}}-\d{{2}}-\d{{2}}$", changelog, re.MULTILINE):
        errors.append(f"CHANGELOG.md has no dated heading for {version}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    referenced_versions = set(
        re.findall(r"NewBe-([0-9A-Za-z.-]+)\.tar\.gz\.sha256", readme)
    )
    if referenced_versions != {version}:
        errors.append(
            "README.md checksum example does not exclusively reference "
            f"{version}: {sorted(referenced_versions)}"
        )

    metadata_path = ROOT / "extension/newbe@infamous-pattern.github.io/metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("shell-version") != EXPECTED_SHELL_VERSIONS:
        errors.append(
            "extension shell-version must be "
            f"{EXPECTED_SHELL_VERSIONS}, found {metadata.get('shell-version')!r}"
        )

    if errors:
        print("NewBe release metadata audit failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"NewBe release metadata audit passed: {version}")
    print(f"GNOME Shell package targets: {', '.join(EXPECTED_SHELL_VERSIONS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
