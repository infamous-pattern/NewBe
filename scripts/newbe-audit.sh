#!/usr/bin/env bash

set -euo pipefail

DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"

check() {
    local label="$1"
    local path="$2"

    if [[ -e "$path" ]]; then
        printf '[OK]      %-24s %s\n' "$label" "$path"
    else
        printf '[MISSING] %-24s %s\n' "$label" "$path"
    fi
}

printf 'NewBe Installation Audit\n'
printf '========================\n\n'

check "NewBe GTK3" \
    "$DATA_HOME/themes/NewBe/gtk-3.0/gtk.css"

check "NewBe GTK4" \
    "$DATA_HOME/themes/NewBe/gtk-4.0/gtk.css"

check "NewBe-Dark GTK3" \
    "$DATA_HOME/themes/NewBe-Dark/gtk-3.0/gtk.css"

check "NewBe-Dark GTK4" \
    "$DATA_HOME/themes/NewBe-Dark/gtk-4.0/gtk.css"

check "NewBe icons" \
    "$DATA_HOME/icons/NewBe/index.theme"

check "NewBe cursors" \
    "$DATA_HOME/icons/NewBe/cursors/left_ptr"

check "NewBe wallpapers" \
    "$DATA_HOME/backgrounds/NewBe/newbe-02-glass-horizon-3840x2160.jpg"

check "GNOME wallpaper catalog" \
    "$DATA_HOME/gnome-background-properties/newbe.xml"

printf '\nSecurity posture\n'
printf '%s\n' '----------------'
printf 'System files modified by this script: None\n'
printf 'Root privileges required:             No\n'
printf 'Automatic GNOME settings changes:     None\n'
