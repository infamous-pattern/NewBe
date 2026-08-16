#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

printf 'NewBe Local Verification\n'
printf '========================\n\n'

printf '[1/6] Bash syntax\n'
while IFS= read -r -d '' script; do
    bash -n "$script"
done < <(find scripts -type f -name '*.sh' -print0)

printf '[2/6] ShellCheck\n'
if command -v shellcheck >/dev/null 2>&1; then
    while IFS= read -r -d '' script; do
        shellcheck "$script"
    done < <(find scripts -type f -name '*.sh' -print0)
else
    printf 'ERROR: ShellCheck is not installed.\n' >&2
    exit 1
fi

printf '[3/6] Installer dry-run\n'
./scripts/install.sh --dry-run >/dev/null

printf '[4/6] Uninstaller dry-run\n'
./scripts/uninstall.sh --dry-run >/dev/null

printf '[5/6] Extension validation\n'
./scripts/verify-extension.sh >/dev/null

printf '[6/6] Git whitespace check\n'
git diff --check

printf '\nAll NewBe verification checks passed.\n'
