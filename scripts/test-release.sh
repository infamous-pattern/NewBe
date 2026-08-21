#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(<"$PROJECT_ROOT/VERSION")"
TEST_ROOT="$(mktemp -d /tmp/newbe-release-test.XXXXXX)"

case "$TEST_ROOT" in
    /tmp/newbe-release-test.*)
        ;;
    *)
        printf 'ERROR: Refusing unsafe temporary path: %s\n' "$TEST_ROOT" >&2
        exit 1
        ;;
esac

cleanup() {
    rm -rf -- "$TEST_ROOT"
}
trap cleanup EXIT

ARTIFACT_ROOT="$TEST_ROOT/artifacts"
EXTRACT_ROOT="$TEST_ROOT/extracted"
DATA_ROOT="$TEST_ROOT/data"

mkdir -p "$ARTIFACT_ROOT" "$EXTRACT_ROOT"

"$PROJECT_ROOT/scripts/build-release.py" --output-dir "$ARTIFACT_ROOT" >/dev/null

(
    cd "$ARTIFACT_ROOT"
    sha256sum --check "NewBe-$VERSION.tar.gz.sha256" >/dev/null
)

tar \
    --extract \
    --gzip \
    --file "$ARTIFACT_ROOT/NewBe-$VERSION.tar.gz" \
    --directory "$EXTRACT_ROOT" \
    --no-same-owner \
    --no-same-permissions

PACKAGE_ROOT="$EXTRACT_ROOT/NewBe-$VERSION"
test -x "$PACKAGE_ROOT/scripts/install.sh"
test -x "$PACKAGE_ROOT/scripts/uninstall.sh"

XDG_DATA_HOME="$DATA_ROOT" \
    "$PACKAGE_ROOT/scripts/install.sh" --without-extension >/dev/null

test -f "$DATA_ROOT/themes/NewBe/gnome-shell/gnome-shell.css"
test -f "$DATA_ROOT/icons/NewBe/cursors/left_ptr"
test -f "$DATA_ROOT/gnome-background-properties/newbe.xml"
test ! -e "$DATA_ROOT/gnome-shell/extensions/newbe@infamous-pattern.github.io"

XDG_DATA_HOME="$DATA_ROOT" "$PACKAGE_ROOT/scripts/uninstall.sh" >/dev/null

XDG_DATA_HOME="$DATA_ROOT" "$PACKAGE_ROOT/scripts/install.sh" >/dev/null

test -f "$DATA_ROOT/themes/NewBe/gnome-shell/gnome-shell.css"
test -f "$DATA_ROOT/icons/NewBe/cursors/left_ptr"
test -f "$DATA_ROOT/gnome-background-properties/newbe.xml"
test -f "$DATA_ROOT/gnome-shell/extensions/newbe@infamous-pattern.github.io/metadata.json"

XDG_DATA_HOME="$DATA_ROOT" "$PACKAGE_ROOT/scripts/uninstall.sh" >/dev/null

test ! -e "$DATA_ROOT/themes/NewBe"
test ! -e "$DATA_ROOT/icons/NewBe"
test ! -e "$DATA_ROOT/gnome-background-properties/newbe.xml"
test ! -e "$DATA_ROOT/gnome-shell/extensions/newbe@infamous-pattern.github.io"

printf 'NewBe extracted release install/uninstall test passed.\n'
