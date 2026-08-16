#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LIGHT="$PROJECT_ROOT/themes/NewBe"
DARK="$PROJECT_ROOT/themes/NewBe-Dark"

rm -rf -- "$LIGHT" "$DARK"

mkdir -p \
    "$LIGHT/gtk-3.0" \
    "$LIGHT/gtk-4.0" \
    "$DARK/gtk-3.0" \
    "$DARK/gtk-4.0"

cp "$PROJECT_ROOT/gtk-3.0/gtk.css" \
   "$LIGHT/gtk-3.0/gtk.css"

cp "$PROJECT_ROOT/gtk-4.0/gtk.css" \
   "$LIGHT/gtk-4.0/gtk.css"

cp "$PROJECT_ROOT/gtk-3.0/gtk-dark.css" \
   "$DARK/gtk-3.0/gtk.css"

cp "$PROJECT_ROOT/gtk-4.0/gtk-dark.css" \
   "$DARK/gtk-4.0/gtk.css"

printf 'Built:\n'
printf '  %s\n' "$LIGHT"
printf '  %s\n' "$DARK"
