#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v rsvg-convert >/dev/null 2>&1; then
    printf 'ERROR: rsvg-convert is required.\n' >&2
    printf 'Install Fedora package: librsvg2-tools\n' >&2
    exit 1
fi

OUTPUT="$PROJECT_ROOT/build/icon-tests"

rm -rf -- "$OUTPUT"
mkdir -p "$OUTPUT"

icons=(
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/user-home.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-download.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-documents.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-pictures.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-projects.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-publicshare.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-templates.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-music.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-videos.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/folder-network.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/user-desktop.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/network-server.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/trash-empty.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/places/trash-full.svg"

    "$PROJECT_ROOT/icons/NewBe/scalable/devices/drive-harddisk.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/devices/drive-removable-media.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/devices/computer.svg"

    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Nautilus.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Calculator.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Calendar.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Software.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.TextEditor.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Settings.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Ptyxis.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.SystemMonitor.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.DiskUtility.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Loupe.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Snapshot.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Characters.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Contacts.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Weather.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.clocks.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.Maps.svg"
    "$PROJECT_ROOT/icons/NewBe/scalable/apps/org.gnome.tweaks.svg"
)

sizes=(
    16
    24
    32
    48
    64
    128
    256
)

for icon in "${icons[@]}"; do
    name="$(basename "$icon" .svg)"

    for size in "${sizes[@]}"; do
        destination="$OUTPUT/${name}-${size}.png"

        rsvg-convert \
            --width "$size" \
            --height "$size" \
            --output "$destination" \
            "$icon"
    done
done

while IFS= read -r -d '' icon; do
    name="$(basename "$icon" .svg)"

    for size in 16 32; do
        destination="$OUTPUT/${name}-${size}.png"

        rsvg-convert \
            --width "$size" \
            --height "$size" \
            --output "$destination" \
            "$icon"
    done
done < <(find \
    "$PROJECT_ROOT/icons/NewBe/symbolic/actions" \
    "$PROJECT_ROOT/icons/NewBe/symbolic/apps" \
    "$PROJECT_ROOT/icons/NewBe/symbolic/status" \
    -type f -name '*.svg' -print0)

printf 'NewBe icon render tests created:\n'
printf '  %s\n' "$OUTPUT"
