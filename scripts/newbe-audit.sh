#!/usr/bin/env bash

set -euo pipefail

THEME_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/themes/NewBe"
ICON_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons/NewBe"

printf 'NewBe Installation Audit\n'
printf '========================\n\n'

check_path() {
    local label="$1"
    local path="$2"

    if [[ -e "$path" ]]; then
        printf '[OK]      %-18s %s\n' "$label" "$path"
    else
        printf '[MISSING] %-18s %s\n' "$label" "$path"
    fi
}

check_path "GTK 3 theme" "$THEME_DIR/gtk-3.0/gtk.css"
check_path "GTK 4 theme" "$THEME_DIR/gtk-4.0/gtk.css"
check_path "Icon theme" "$ICON_DIR/index.theme"

printf '\nSecurity posture\n'
printf '----------------\n'
printf 'System files modified by this script: None\n'
printf 'Root privileges required:             No\n'
printf 'Automatic GNOME settings changes:     None\n'
