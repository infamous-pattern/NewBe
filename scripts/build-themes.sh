#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LIGHT="$PROJECT_ROOT/themes/NewBe"
DARK="$PROJECT_ROOT/themes/NewBe-Dark"

rm -rf -- "$LIGHT" "$DARK"

mkdir -p \
    "$LIGHT/gtk-3.0" \
    "$LIGHT/gtk-4.0" \
    "$LIGHT/gnome-shell" \
    "$DARK/gtk-3.0" \
    "$DARK/gtk-4.0" \
    "$DARK/gnome-shell"

cp "$PROJECT_ROOT/gtk-3.0/gtk.css" \
   "$LIGHT/gtk-3.0/gtk.css"

cp "$PROJECT_ROOT/gtk-4.0/gtk.css" \
   "$LIGHT/gtk-4.0/gtk.css"

cp "$PROJECT_ROOT/gtk-3.0/gtk-dark.css" \
   "$DARK/gtk-3.0/gtk.css"

cp "$PROJECT_ROOT/gtk-4.0/gtk-dark.css" \
   "$DARK/gtk-4.0/gtk.css"

cp "$PROJECT_ROOT/gnome-shell/gnome-shell.css" \
   "$LIGHT/gnome-shell/gnome-shell.css"

cp "$PROJECT_ROOT/gnome-shell/gnome-shell.css" \
   "$DARK/gnome-shell/gnome-shell.css"

printf 'Built:\n'
printf '  %s\n' "$LIGHT"
printf '  %s\n' "$DARK"
