#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_ROOT="$(mktemp -d /tmp/newbe-install-test.XXXXXX)"

case "$TEST_ROOT" in
    /tmp/newbe-install-test.*)
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

export XDG_DATA_HOME="$TEST_ROOT/data"

base_required=(
    themes/NewBe/gtk-3.0/gtk.css
    themes/NewBe/gtk-4.0/gtk.css
    themes/NewBe/gnome-shell/gnome-shell.css
    themes/NewBe-Dark/gtk-3.0/gtk.css
    themes/NewBe-Dark/gtk-4.0/gtk.css
    themes/NewBe-Dark/gnome-shell/gnome-shell.css
    icons/NewBe/index.theme
    icons/NewBe/cursors/left_ptr
    backgrounds/NewBe/newbe-02-glass-horizon-3840x2160.jpg
    gnome-background-properties/newbe.xml
)

extension_required=(
    gnome-shell/extensions/newbe@infamous-pattern.github.io/metadata.json
    gnome-shell/extensions/newbe@infamous-pattern.github.io/schemas/gschemas.compiled
)

check_base_install() {
    local relative_path

    for relative_path in "${base_required[@]}"; do
        test -e "$XDG_DATA_HOME/$relative_path"
    done

    test "$(find "$XDG_DATA_HOME/backgrounds/NewBe" -maxdepth 1 -type f -name '*.jpg' | wc -l)" -eq 7
    test "$(find "$XDG_DATA_HOME/icons/NewBe/cursors" -maxdepth 1 -type f | wc -l)" -eq 15
    test "$(find "$XDG_DATA_HOME/icons/NewBe/cursors" -maxdepth 1 -type l | wc -l)" -eq 53
}

if "$PROJECT_ROOT/scripts/install.sh" \
    --with-extension --without-extension >/dev/null 2>&1; then
    printf 'ERROR: Conflicting extension options were accepted.\n' >&2
    exit 1
fi

"$PROJECT_ROOT/scripts/install.sh" --without-extension >/dev/null
check_base_install
test ! -e "$XDG_DATA_HOME/gnome-shell/extensions/newbe@infamous-pattern.github.io"

"$PROJECT_ROOT/scripts/uninstall.sh" >/dev/null

extension_target="$XDG_DATA_HOME/gnome-shell/extensions/newbe@infamous-pattern.github.io"
mkdir -p "$extension_target"
touch "$extension_target/existing-install-marker"

"$PROJECT_ROOT/scripts/install.sh" --without-extension >/dev/null
check_base_install
test -f "$extension_target/existing-install-marker"

"$PROJECT_ROOT/scripts/install.sh" --with-extension >/dev/null
check_base_install

for relative_path in "${extension_required[@]}"; do
    test -e "$XDG_DATA_HOME/$relative_path"
done

test ! -e "$extension_target/existing-install-marker"

touch "$XDG_DATA_HOME/backgrounds/NewBe/unrelated-user-file"

"$PROJECT_ROOT/scripts/uninstall.sh" >/dev/null

test ! -e "$XDG_DATA_HOME/themes/NewBe"
test ! -e "$XDG_DATA_HOME/themes/NewBe-Dark"
test ! -e "$XDG_DATA_HOME/icons/NewBe"
test ! -e "$XDG_DATA_HOME/gnome-background-properties/newbe.xml"
test ! -e "$XDG_DATA_HOME/gnome-shell/extensions/newbe@infamous-pattern.github.io"
test -f "$XDG_DATA_HOME/backgrounds/NewBe/unrelated-user-file"
test "$(find "$XDG_DATA_HOME/backgrounds/NewBe" -maxdepth 1 -type f -name '*.jpg' | wc -l)" -eq 0

printf 'NewBe isolated install/uninstall test passed.\n'
