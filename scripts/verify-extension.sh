#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXTENSION_DIR="$PROJECT_ROOT/extension/newbe@infamous-pattern.github.io"
REQUIRE_PACKAGE_TOOL=false

if [[ "${1:-}" == "--require-package-tool" ]]; then
    REQUIRE_PACKAGE_TOOL=true
    shift
fi

if (($#)); then
    printf 'Usage: %s [--require-package-tool]\n' "$0" >&2
    exit 2
fi

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

python3 - "$EXTENSION_DIR/metadata.json" <<'PY'
import json
import sys
from pathlib import Path

metadata = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
expected_versions = ["48", "49", "50"]
if metadata.get("uuid") != "newbe@infamous-pattern.github.io":
    raise SystemExit("ERROR: Unexpected extension UUID")
if metadata.get("shell-version") != expected_versions:
    raise SystemExit(
        f"ERROR: shell-version must be {expected_versions}, "
        f"found {metadata.get('shell-version')!r}"
    )
PY

printf '[OK] metadata.json\n'

glib-compile-schemas \
    --strict \
    "$EXTENSION_DIR/schemas"

printf '[OK] GSettings schema\n'

if command -v gnome-extensions >/dev/null 2>&1; then
    package_root="$(mktemp -d /tmp/newbe-extension-package.XXXXXX)"
    case "$package_root" in
        /tmp/newbe-extension-package.*)
            ;;
        *)
            printf 'ERROR: Refusing unsafe temporary path: %s\n' "$package_root" >&2
            exit 1
            ;;
    esac

    cleanup() {
        rm -rf -- "$package_root"
    }
    trap cleanup EXIT

    gnome-extensions pack \
        --force \
        --out-dir "$package_root" \
        "$EXTENSION_DIR" \
        >/dev/null

    package="$package_root/newbe@infamous-pattern.github.io.shell-extension.zip"
    test -f "$package"
    python3 -m zipfile --test "$package" >/dev/null
    printf '[OK] Extension package\n'

    cleanup
    trap - EXIT
elif "$REQUIRE_PACKAGE_TOOL"; then
    printf 'ERROR: gnome-extensions is required for this compatibility job.\n' >&2
    exit 1
else
    printf '[SKIP] Extension package (gnome-extensions unavailable)\n'
fi

printf '\nExtension validation passed.\n'
