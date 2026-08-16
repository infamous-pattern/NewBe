#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

THEME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
ICON_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/icons"

DRY_RUN=false

usage() {
    cat <<USAGE
Usage: $0 [--dry-run]

Install NewBe into the current user's local GNOME data directories.

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

printf 'NewBe installer\n'
printf 'Project: %s\n\n' "$PROJECT_ROOT"

if ! "$DRY_RUN"; then
    "$PROJECT_ROOT/scripts/build-themes.sh"
fi

run mkdir -p "$THEME_ROOT"
run mkdir -p "$ICON_ROOT"

run rm -rf -- "$THEME_ROOT/NewBe"
run rm -rf -- "$THEME_ROOT/NewBe-Dark"

run cp -R "$PROJECT_ROOT/themes/NewBe" "$THEME_ROOT/"
run cp -R "$PROJECT_ROOT/themes/NewBe-Dark" "$THEME_ROOT/"

run rm -rf -- "$ICON_ROOT/NewBe"
run cp -R "$PROJECT_ROOT/icons/NewBe" "$ICON_ROOT/"

printf '\nNewBe installation complete.\n'
printf 'No GNOME settings were modified automatically.\n'
printf '\nAvailable themes:\n'
printf '  NewBe\n'
printf '  NewBe-Dark\n'
