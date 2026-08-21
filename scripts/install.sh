#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

THEME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
ICON_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
WALLPAPER_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/NewBe"
BACKGROUND_PROPERTIES_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-background-properties"
BACKGROUND_PROPERTIES="$BACKGROUND_PROPERTIES_ROOT/newbe.xml"
EXTENSION_UUID="newbe@infamous-pattern.github.io"
EXTENSION_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-shell/extensions"
EXTENSION_TARGET="$EXTENSION_ROOT/$EXTENSION_UUID"

DRY_RUN=false
INSTALL_EXTENSION=true
EXTENSION_OPTION=""

usage() {
    cat <<USAGE
Usage: $0 [--dry-run] [--with-extension | --without-extension]

Install NewBe into the current user's local GNOME data directories.

Options:
  --dry-run             Show planned operations without modifying files
  --with-extension      Install the GNOME Shell extension (default)
  --without-extension   Skip the extension and preserve any installed copy
  -h, --help            Show this help
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
        --with-extension)
            if [[ "$EXTENSION_OPTION" == "without" ]]; then
                printf 'Conflicting extension options were provided.\n' >&2
                exit 2
            fi
            INSTALL_EXTENSION=true
            EXTENSION_OPTION="with"
            ;;
        --without-extension)
            if [[ "$EXTENSION_OPTION" == "with" ]]; then
                printf 'Conflicting extension options were provided.\n' >&2
                exit 2
            fi
            INSTALL_EXTENSION=false
            EXTENSION_OPTION="without"
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
run mkdir -p "$WALLPAPER_ROOT"
run mkdir -p "$BACKGROUND_PROPERTIES_ROOT"
if "$INSTALL_EXTENSION"; then
    run mkdir -p "$EXTENSION_ROOT"
fi

run rm -rf -- "$THEME_ROOT/NewBe"
run rm -rf -- "$THEME_ROOT/NewBe-Dark"

run cp -R "$PROJECT_ROOT/themes/NewBe" "$THEME_ROOT/"
run cp -R "$PROJECT_ROOT/themes/NewBe-Dark" "$THEME_ROOT/"

run rm -rf -- "$ICON_ROOT/NewBe"
run cp -R "$PROJECT_ROOT/icons/NewBe" "$ICON_ROOT/"

while IFS='|' read -r number slug _; do
    [[ -n "$number" && "${number:0:1}" != "#" ]] || continue
    source="$PROJECT_ROOT/assets/wallpapers/$number-$slug/newbe-$number-$slug-3840x2160.jpg"
    destination="$WALLPAPER_ROOT/newbe-$number-$slug-3840x2160.jpg"
    run cp "$source" "$destination"
done < "$PROJECT_ROOT/assets/wallpapers/wallpapers.conf"

run "$PROJECT_ROOT/scripts/generate-background-properties.py" \
    --wallpaper-root "$WALLPAPER_ROOT" \
    --output "$BACKGROUND_PROPERTIES"

if "$INSTALL_EXTENSION"; then
    run rm -rf -- "$EXTENSION_TARGET"
    run cp -R "$PROJECT_ROOT/extension/$EXTENSION_UUID" "$EXTENSION_ROOT/"
    run glib-compile-schemas --strict "$EXTENSION_TARGET/schemas"
fi

printf '\nNewBe installation complete.\n'
printf 'No GNOME settings were modified automatically.\n'
printf '\nAvailable themes:\n'
printf '  NewBe\n'
printf '  NewBe-Dark\n'
printf '\nCursor theme:\n'
printf '  NewBe\n'
printf '\nWallpapers:\n'
printf '  Seven NewBe wallpapers are available in GNOME Background settings.\n'
printf '\nGNOME Shell extension:\n'
if "$INSTALL_EXTENSION"; then
    printf '  Installed but not enabled automatically: %s\n' "$EXTENSION_UUID"
else
    printf '  Skipped; any existing installed copy was left unchanged.\n'
fi
