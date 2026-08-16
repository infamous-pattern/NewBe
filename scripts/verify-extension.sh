#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXTENSION_DIR="$PROJECT_ROOT/extension/newbe@infamous-pattern.github.io"

printf 'NewBe Extension Verification\n'
printf '============================\n\n'

required=(
    metadata.json
    extension.js
    prefs.js
    stylesheet.css
    schemas/org.gnome.shell.extensions.newbe.gschema.xml
)

for file in "${required[@]}"; do
    if [[ ! -f "$EXTENSION_DIR/$file" ]]; then
        printf 'ERROR: Missing %s\n' "$file" >&2
        exit 1
    fi
done

printf '[OK] Required files\n'

python3 -m json.tool \
    "$EXTENSION_DIR/metadata.json" \
    >/dev/null

printf '[OK] metadata.json\n'

glib-compile-schemas \
    --strict \
    "$EXTENSION_DIR/schemas"

printf '[OK] GSettings schema\n'

printf '\nExtension validation passed.\n'
