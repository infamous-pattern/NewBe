#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

printf 'NewBe Local Verification\n'
printf '========================\n\n'

printf '[1/14] Bash syntax\n'
while IFS= read -r -d '' script; do
    bash -n "$script"
done < <(find scripts -type f -name '*.sh' -print0)

printf '[2/14] ShellCheck\n'
if command -v shellcheck >/dev/null 2>&1; then
    while IFS= read -r -d '' script; do
        shellcheck "$script"
    done < <(find scripts -type f -name '*.sh' -print0)
else
    printf 'ERROR: ShellCheck is not installed.\n' >&2
    exit 1
fi

printf '[3/14] Generated symbolic UI\n'
./scripts/build-symbolic-ui.py --check >/dev/null

printf '[4/14] Icon coverage report\n'
./scripts/icon-audit.py \
    --manifest icons/coverage-apps.conf \
    --check docs/ICON-COVERAGE.txt

printf '[5/14] Cursor theme\n'
./scripts/cursor-audit.py >/dev/null

printf '[6/14] Wallpaper pack\n'
./scripts/wallpaper-audit.py >/dev/null

printf '[7/14] GNOME background metadata\n'
./scripts/generate-background-properties.py \
    --wallpaper-root /example/user/.local/share/backgrounds/NewBe \
    --check >/dev/null

printf '[8/14] Installer dry-run\n'
./scripts/install.sh --dry-run >/dev/null

printf '[9/14] Uninstaller dry-run\n'
./scripts/uninstall.sh --dry-run >/dev/null

printf '[10/14] Extension validation\n'
./scripts/verify-extension.sh >/dev/null

printf '[11/14] Isolated install/uninstall\n'
./scripts/test-install.sh >/dev/null

printf '[12/14] Release archive\n'
./scripts/build-release.py --check >/dev/null

printf '[13/14] Extracted release install/uninstall\n'
./scripts/test-release.sh >/dev/null

printf '[14/14] Git whitespace check\n'
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git diff --check
else
    printf 'Not a Git checkout; whitespace check skipped.\n'
fi

printf '\nAll NewBe verification checks passed.\n'
