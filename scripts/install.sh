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

run mkdir -p "$THEME_ROOT/NewBe"
run mkdir -p "$ICON_ROOT/NewBe"

run cp -R "$PROJECT_ROOT/gtk-3.0" "$THEME_ROOT/NewBe/"
run cp -R "$PROJECT_ROOT/gtk-4.0" "$THEME_ROOT/NewBe/"

run cp -R "$PROJECT_ROOT/icons/NewBe/." "$ICON_ROOT/NewBe/"

printf '\nNewBe installation complete.\n'
printf 'No GNOME settings were modified automatically.\n'
printf 'Use GNOME Tweaks to select installed components.\n'
