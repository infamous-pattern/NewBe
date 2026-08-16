#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ALIAS_FILE = PROJECT_ROOT / "icons" / "aliases" / "apps.conf"
APP_DIR = PROJECT_ROOT / "icons" / "NewBe" / "scalable" / "apps"


def parse_aliases() -> list[tuple[str, str]]:
    aliases: list[tuple[str, str]] = []

    if not ALIAS_FILE.exists():
        return aliases

    for line_number, raw in enumerate(
        ALIAS_FILE.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ValueError(
                f"{ALIAS_FILE}:{line_number}: invalid alias"
            )

        alias, target = (item.strip() for item in line.split("=", 1))

        if not alias or not target:
            raise ValueError(
                f"{ALIAS_FILE}:{line_number}: empty alias or target"
            )

        aliases.append((alias, target))

    return aliases


def locate_target(name: str) -> Path | None:
    for suffix in (".svg", ".png", ".xpm"):
        candidate = APP_DIR / f"{name}{suffix}"

        if candidate.exists():
            return candidate

    return None


def main() -> int:
    APP_DIR.mkdir(parents=True, exist_ok=True)

    failures = 0

    for alias, target_name in parse_aliases():
        target = locate_target(target_name)

        if target is None:
            print(
                f"ERROR: target icon does not exist: {target_name}",
                file=sys.stderr,
            )
            failures += 1
            continue

        alias_path = APP_DIR / f"{alias}{target.suffix}"

        if alias_path.exists() or alias_path.is_symlink():
            alias_path.unlink()

        alias_path.symlink_to(target.name)

        print(f"{alias} -> {target.name}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
