#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MODE="${1:-light}"
TOOL="${2:-auto}"

case "$MODE" in
    light|dark) ;;
    *)
        printf 'Usage: %s [light|dark] [gtk3|gtk4|auto]\n' "$0" >&2
        exit 2
        ;;
esac

case "$TOOL" in
    gtk3|gtk4|auto) ;;
    *)
        printf 'Usage: %s [light|dark] [gtk3|gtk4|auto]\n' "$0" >&2
        exit 2
        ;;
esac

TMP_ROOT="$(mktemp -d -t newbe-preview.XXXXXXXX)"

cleanup() {
    rm -rf -- "$TMP_ROOT"
}

trap cleanup EXIT INT TERM

LIGHT_DIR="$TMP_ROOT/themes/NewBe"
DARK_DIR="$TMP_ROOT/themes/NewBe-Dark"

mkdir -p \
    "$LIGHT_DIR/gtk-3.0" \
    "$LIGHT_DIR/gtk-4.0" \
    "$DARK_DIR/gtk-3.0" \
    "$DARK_DIR/gtk-4.0"

cp "$PROJECT_ROOT/gtk-3.0/gtk.css" \
   "$LIGHT_DIR/gtk-3.0/gtk.css"

cp "$PROJECT_ROOT/gtk-3.0/gtk-dark.css" \
   "$DARK_DIR/gtk-3.0/gtk.css"

cp "$PROJECT_ROOT/gtk-4.0/gtk.css" \
   "$LIGHT_DIR/gtk-4.0/gtk.css"

cp "$PROJECT_ROOT/gtk-4.0/gtk-dark.css" \
   "$DARK_DIR/gtk-4.0/gtk.css"

export XDG_DATA_HOME="$TMP_ROOT"

if [[ "$MODE" == "dark" ]]; then
    export GTK_THEME="NewBe-Dark"
else
    export GTK_THEME="NewBe"
fi

printf 'NewBe Theme Preview\n'
printf '===================\n'
printf 'Mode:      %s\n' "$MODE"
printf 'GTK_THEME: %s\n\n' "$GTK_THEME"

run_gtk3() {
    if command -v gtk3-widget-factory >/dev/null 2>&1; then
        exec gtk3-widget-factory
    fi

    exec gtk3-demo
}

run_gtk4() {
    if command -v gtk4-widget-factory >/dev/null 2>&1; then
        exec gtk4-widget-factory
    fi

    exec gtk4-demo
}

case "$TOOL" in
    gtk3)
        run_gtk3
        ;;
    gtk4)
        run_gtk4
        ;;
    auto)
        if command -v gtk4-widget-factory >/dev/null 2>&1; then
            run_gtk4
        else
            run_gtk3
        fi
        ;;
esac
