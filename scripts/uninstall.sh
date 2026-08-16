#!/usr/bin/env bash

set -euo pipefail

THEME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
ICON_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/icons"

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

printf 'NewBe uninstaller\n\n'

run rm -rf -- "$THEME_ROOT/NewBe"
run rm -rf -- "$ICON_ROOT/NewBe"

printf '\nNewBe user files removed.\n'
printf 'GNOME settings were not changed.\n'
