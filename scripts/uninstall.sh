#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

THEME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
ICON_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
WALLPAPER_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/NewBe"
BACKGROUND_PROPERTIES="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-background-properties/newbe.xml"
EXTENSION_TARGET="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-shell/extensions/newbe@infamous-pattern.github.io"

DRY_RUN=false

usage() {
    cat <<USAGE
Usage: $0 [--dry-run]

Remove user-installed NewBe files.

Options:
  --dry-run    Show planned operations without modifying files
  -h, --help   Show this help
USAGE
}

run() {
    if "$DRY_RUN"; then
        printf '[dry-run]'
        printf ' %q' "$@"
        printf '\n'
    else
        "$@"
    fi
}

while (($#)); do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf 'Unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac

    shift
done

run rm -rf -- "$THEME_ROOT/NewBe"
run rm -rf -- "$THEME_ROOT/NewBe-Dark"
run rm -rf -- "$ICON_ROOT/NewBe"
run rm -rf -- "$EXTENSION_TARGET"

while IFS='|' read -r number slug _; do
    [[ -n "$number" && "${number:0:1}" != "#" ]] || continue
    run rm -f -- "$WALLPAPER_ROOT/newbe-$number-$slug-3840x2160.jpg"
done < "$PROJECT_ROOT/assets/wallpapers/wallpapers.conf"

run rm -f -- "$BACKGROUND_PROPERTIES"

if "$DRY_RUN"; then
    run rmdir --ignore-fail-on-non-empty "$WALLPAPER_ROOT"
else
    rmdir --ignore-fail-on-non-empty "$WALLPAPER_ROOT" 2>/dev/null || true
fi

printf 'NewBe user files removed.\n'
printf 'GNOME settings were not changed.\n'
