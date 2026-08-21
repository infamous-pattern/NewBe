#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYMBOLIC_ROOT = PROJECT_ROOT / "icons" / "NewBe" / "symbolic"


def svg(body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
        'viewBox="0 0 16 16">\n'
        f'  {body}\n'
        '</svg>\n'
    )


def filled(path: str, *, rule: str = "") -> str:
    fill_rule = f' fill-rule="{rule}"' if rule else ""
    return f'<path fill="currentColor"{fill_rule} d="{path}"/>'


def stroked(path: str, width: float = 1.8) -> str:
    return (
        f'<path d="{path}" fill="none" stroke="currentColor" '
        f'stroke-width="{width}" stroke-linecap="round" '
        'stroke-linejoin="round"/>'
    )


ICONS = {
    # Navigation and views.
    "actions/go-previous-symbolic.svg": filled("M10.8 2 4.8 8l6 6 1.4-1.4L7.6 8l4.6-4.6z"),
    "actions/go-next-symbolic.svg": filled("M5.2 2 11.2 8l-6 6-1.4-1.4L8.4 8 3.8 3.4z"),
    "actions/go-up-symbolic.svg": filled("M2 10.8 8 4.8l6 6-1.4 1.4L8 7.6l-4.6 4.6z"),
    "actions/go-down-symbolic.svg": filled("M2 5.2 8 11.2l6-6-1.4-1.4L8 8.4 3.4 3.8z"),
    "actions/go-home-symbolic.svg": filled("M1 7.2 8 1l7 6.2-1.4 1.5L13 8.1V15H9v-4H7v4H3V8.1l-.6.6z"),
    "actions/view-refresh-symbolic.svg": filled("M8 2a6 6 0 0 1 5.2 3H15L12 8 9 5h2a4 4 0 1 0 .7 5.2l1.5 1.3A6 6 0 1 1 8 2z"),
    "actions/view-grid-symbolic.svg": '<path fill="currentColor" d="M2 2h5v5H2zm7 0h5v5H9zM2 9h5v5H2zm7 0h5v5H9z"/>',
    "actions/view-list-symbolic.svg": '<path fill="currentColor" d="M2 2h3v3H2zm5 0h7v3H7zM2 6.5h3v3H2zm5 0h7v3H7zM2 11h3v3H2zm5 0h7v3H7z"/>',
    "actions/view-more-symbolic.svg": '<circle fill="currentColor" cx="3" cy="8" r="1.5"/><circle fill="currentColor" cx="8" cy="8" r="1.5"/><circle fill="currentColor" cx="13" cy="8" r="1.5"/>',
    "actions/open-menu-symbolic.svg": filled("M2 3h12v2H2zm0 4h12v2H2zm0 4h12v2H2z"),
    "actions/sidebar-show-symbolic.svg": filled("M1 2h14v12H1zm2 2v8h3V4zm5 0v8h5V4z", rule="evenodd"),
    "actions/zoom-in-symbolic.svg": '<circle cx="6.5" cy="6.5" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path fill="currentColor" d="M5.5 4h2v1.5H9v2H7.5V9h-2V7.5H4v-2h1.5zm4.2 5.7 1.4-1.4 4.2 4.2-1.4 1.4z"/>',
    "actions/zoom-out-symbolic.svg": '<circle cx="6.5" cy="6.5" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path fill="currentColor" d="M4 5.5h5v2H4zm5.7 4.2 1.4-1.4 4.2 4.2-1.4 1.4z"/>',

    # File and document actions.
    "actions/folder-new-symbolic.svg": filled("M1 4h5l1.5 2H15v8H1zm8 3v2H7v2h2v2h2v-2h2V9h-2V7z", rule="evenodd"),
    "actions/folder-open-symbolic.svg": filled("M1 4h5l1.5 2H15l-2 8H1zm2 4 1 4h7l1-4z", rule="evenodd"),
    "actions/document-new-symbolic.svg": filled("M3 1h6l4 4v10H3zm6 1.8V6h3.2zM7 7v2H5v2h2v2h2v-2h2V9H9V7z", rule="evenodd"),
    "actions/document-open-symbolic.svg": filled("M3 1h7l3 3v4h-2V5H9V3H5v10h3v2H3zm8 7 4 3-4 3v-2H7v-2h4z"),
    "actions/document-save-symbolic.svg": filled("M2 1h11l2 2v12H1V2zm2 2v4h7V3zm0 7v3h8v-3z", rule="evenodd"),
    "actions/document-edit-symbolic.svg": filled("M3 1h7l3 3v3h-2V5H9V3H5v10h3v2H3zm9 6 3 3-5 5H7v-3z"),
    "actions/edit-copy-symbolic.svg": filled("M5 1h9v10h-3v4H2V5h3zm2 2v6h5V3zM4 7v6h5v-2H5V7z", rule="evenodd"),
    "actions/edit-cut-symbolic.svg": filled("M3.5 1a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zm0 9a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM5 5l9 8-1.3 1.5-9-8zm7.7-3.5L8 5.7l1.5 1.4L14 3z"),
    "actions/edit-paste-symbolic.svg": filled("M5 1h6l1 2h2v12H2V3h2zm1 2v2h4V3zM4 7v6h8V7z", rule="evenodd"),
    "actions/edit-delete-symbolic.svg": filled("M5 1h6l1 2h3v2H1V3h3zm-2 5h10l-1 9H4zm3 2v5h1V8zm3 0v5h1V8z"),
    "actions/edit-find-symbolic.svg": '<circle cx="6.5" cy="6.5" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path fill="currentColor" d="m9.7 9.7 1.4-1.4 4.2 4.2-1.4 1.4z"/>',
    "actions/edit-undo-symbolic.svg": filled("M6 3 1 7l5 4V8h2a4 4 0 0 1 4 4v2h2v-2a6 6 0 0 0-6-6H6z"),
    "actions/edit-redo-symbolic.svg": filled("M10 3v3H8a6 6 0 0 0-6 6v2h2v-2a4 4 0 0 1 4-4h2v3l5-4z"),
    "actions/edit-clear-symbolic.svg": filled("M2 10 9 3l5 5-6 6H5zm7-4-5 5 2 1h1l4-4z", rule="evenodd"),
    "actions/edit-select-all-symbolic.svg": filled("M1 1h4v2H3v2H1zm10 0h4v4h-2V3h-2zM1 11h2v2h2v2H1zm12 0h2v4h-4v-2h2zM5 5h6v6H5z"),
    "actions/object-select-symbolic.svg": filled("M1 1h4v2H3v2H1zm10 0h4v4h-2V3h-2zM1 11h2v2h2v2H1zm12 0h2v4h-4v-2h2z"),
    "actions/list-add-symbolic.svg": filled("M7 1h2v6h6v2H9v6H7V9H1V7h6z"),
    "actions/list-remove-symbolic.svg": filled("M2 7h12v2H2z"),
    "actions/media-eject-symbolic.svg": filled("M8 2 2 10h12zm-6 10h12v2H2z"),
    "actions/process-stop-symbolic.svg": filled("M8 1a7 7 0 1 1 0 14A7 7 0 0 1 8 1zm-3 4v6h6V5z", rule="evenodd"),
    "actions/tab-new-symbolic.svg": filled("M1 3h5l1 2h8v10H1zm7 4v2H6v2h2v2h2v-2h2V9h-2V7z", rule="evenodd"),
    "actions/window-new-symbolic.svg": filled("M1 2h10v3h4v10H5v-3H1zm2 2v6h2V5h4V4zm4 3v6h6V7z", rule="evenodd"),
    "actions/window-close-symbolic.svg": filled("M3 4.4 4.4 3 8 6.6 11.6 3 13 4.4 9.4 8l3.6 3.6-1.4 1.4L8 9.4 4.4 13 3 11.6 6.6 8z"),
    "actions/window-minimize-symbolic.svg": filled("M3 7h10v2H3z"),
    "actions/window-maximize-symbolic.svg": filled("M2 2h12v12H2zm2 2v8h8V4z", rule="evenodd"),
    "actions/window-restore-symbolic.svg": filled("M4 1h11v11h-3v3H1V4h3zm2 2v1h6v6h1V3zM3 6v7h7V6z", rule="evenodd"),
    "actions/external-link-symbolic.svg": filled("M9 1h6v6h-2V4.4L7.7 9.7 6.3 8.3 11.6 3H9zM2 3h5v2H4v7h7V9h2v5H2z"),
    "actions/bookmark-new-symbolic.svg": filled("M3 1h10v14l-5-3-5 3zm4 3v2H5v2h2v2h2V8h2V6H9V4z", rule="evenodd"),
    "actions/starred-symbolic.svg": filled("m8 1 2.1 4.3 4.9.7-3.5 3.4.8 4.8L8 11l-4.3 2.2.8-4.8L1 6l4.9-.7z"),
    "actions/non-starred-symbolic.svg": filled("m8 1 2.1 4.3 4.9.7-3.5 3.4.8 4.8L8 11l-4.3 2.2.8-4.8L1 6l4.9-.7zm0 4-1 2-2.2.3 1.6 1.5L6 11l2-1 2 1-.4-2.2 1.6-1.5L9 7z", rule="evenodd"),
    "actions/info-outline-symbolic.svg": filled("M8 1a7 7 0 1 1 0 14A7 7 0 0 1 8 1zm0 2a5 5 0 1 0 0 10A5 5 0 0 0 8 3zM7 7h2v5H7zm0-3h2v2H7z", rule="evenodd"),
    "actions/funnel-outline-symbolic.svg": filled("M1 2h14L10 8v5l-4 2V8zm4 2 3 3 3-3z", rule="evenodd"),

    # Media controls.
    "actions/media-playback-start-symbolic.svg": filled("M4 2v12l10-6z"),
    "actions/media-playback-pause-symbolic.svg": filled("M3 2h4v12H3zm6 0h4v12H9z"),
    "actions/media-playback-stop-symbolic.svg": filled("M3 3h10v10H3z"),
    "actions/media-skip-backward-symbolic.svg": filled("M2 2h2v12H2zm12 0v12L4 8z"),
    "actions/media-skip-forward-symbolic.svg": filled("M12 2h2v12h-2zM2 2l10 6-10 6z"),
    "actions/media-seek-backward-symbolic.svg": filled("M8 2v12L1 8zm7 0v12L8 8z"),
    "actions/media-seek-forward-symbolic.svg": filled("M1 2l7 6-7 6zm7 0 7 6-7 6z"),

    # Network and connectivity.
    "status/network-wired-symbolic.svg": filled("M2 1h12v8H9v2h3v4H9v-2H7v2H4v-4h3V9H2zm2 2v4h8V3z", rule="evenodd"),
    "status/network-vpn-symbolic.svg": filled("M8 1 14 3v4c0 4-2.5 6.5-6 8-3.5-1.5-6-4-6-8V3zm0 3a2 2 0 0 0-1 3.7V11h2V7.7A2 2 0 0 0 8 4z", rule="evenodd"),
    "status/network-offline-symbolic.svg": filled("M2.3 1 15 13.7 13.7 15l-3-3A7 7 0 0 1 1 5.3zm1.6 5.1A5 5 0 0 0 8 11a5 5 0 0 0 1.1-.1zm1.8-4.8A7 7 0 0 1 14.7 10l-2.2-2.2A5 5 0 0 0 8 3c-.3 0-.6 0-.9.1z"),

    # Volume and microphone states.
    "status/audio-volume-muted-symbolic.svg": filled("M1 6h3l4-4v12l-4-4H1zm9-1 1.4-1.4L13 5.2l1.6-1.6L16 5l-1.6 1.6L16 8l-1.4 1.4L13 7.8l-1.6 1.6L10 8l1.6-1.4z"),
    "status/audio-volume-low-symbolic.svg": filled("M1 6h3l4-4v12l-4-4H1zm9-1.5a5 5 0 0 1 0 7l-1.4-1.4a3 3 0 0 0 0-4.2z"),
    "status/audio-volume-medium-symbolic.svg": filled("M1 6h3l4-4v12l-4-4H1zm9-1.5a5 5 0 0 1 0 7l-1.4-1.4a3 3 0 0 0 0-4.2zm2-2a8 8 0 0 1 0 11l-1.4-1.4a6 6 0 0 0 0-8.2z"),
    "status/audio-volume-high-symbolic.svg": filled("M0 6h3l4-4v12l-4-4H0zm9-1.5a5 5 0 0 1 0 7l-1.4-1.4a3 3 0 0 0 0-4.2zm2-2a8 8 0 0 1 0 11l-1.4-1.4a6 6 0 0 0 0-8.2z"),
    "status/microphone-sensitivity-muted-symbolic.svg": filled("M6 1h4v7a2 2 0 0 1-3.7 1L3 5.7 4.4 4.3 13.7 13.6 12.3 15l-2.6-2.6c-.2.1-.5.1-.7.1V15H7v-2.7A5 5 0 0 1 3 8V7h2v1a3 3 0 0 0 3 3h.1L6 8.9z"),
    "status/microphone-sensitivity-high-symbolic.svg": filled("M5 1h6v7a3 3 0 0 1-6 0zm-3 6h2v1a4 4 0 0 0 8 0V7h2v1a6 6 0 0 1-5 5.9V16H7v-2.1A6 6 0 0 1 2 8z"),

    # General system status.
    "status/dialog-error-symbolic.svg": filled("M8 1a7 7 0 1 1 0 14A7 7 0 0 1 8 1zm-1 3v6h2V4zm0 8v2h2v-2z", rule="evenodd"),
    "status/dialog-warning-symbolic.svg": filled("M8 1 16 15H0zm-1 5v4h2V6zm0 6v2h2v-2z", rule="evenodd"),
    "status/dialog-information-symbolic.svg": filled("M8 1a7 7 0 1 1 0 14A7 7 0 0 1 8 1zm-1 5v6h2V6zm0-3v2h2V3z", rule="evenodd"),
    "status/emblem-readonly-symbolic.svg": filled("M4 7V5a4 4 0 0 1 8 0v2h2v8H2V7zm2 0h4V5a2 2 0 0 0-4 0z", rule="evenodd"),
    "status/emblem-symbolic-link-symbolic.svg": filled("M6 3H4a4 4 0 0 0 0 8h3V9H4a2 2 0 0 1 0-4h2zm4 0h2a4 4 0 0 1 0 8H9V9h3a2 2 0 0 0 0-4h-2zM5 7h6v2H5z"),
    "status/emblem-synchronizing-symbolic.svg": filled("M8 1a7 7 0 0 1 5.6 2.8L16 1.5V8H9.5l2.6-2.6A5 5 0 0 0 3 8H1a7 7 0 0 1 7-7zm7 7a7 7 0 0 1-12.6 4.2L0 14.5V8h6.5l-2.6 2.6A5 5 0 0 0 13 8z"),
    "status/file-operation-finished-symbolic.svg": '<circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="m4 8 2.5 2.5L12 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "status/file-operation-cancelled-symbolic.svg": '<circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="m5 5 6 6m0-6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
}


def wireless(level: int) -> str:
    # Keep every wireless segment fill-only. GNOME Shell's symbolic recoloring
    # can treat strokes and fills differently, which makes a single status icon
    # appear in two colors.
    arcs = ['<circle fill="currentColor" cx="8" cy="13.5" r="1.2"/>']
    if level >= 1:
        arcs.append(filled("M5.6 10.4C6.9 9.1 9.1 9.1 10.4 10.4L9 11.8c-.6-.6-1.4-.6-2 0z"))
    if level >= 2:
        arcs.append(filled("M3.2 8c2.7-2.7 6.9-2.7 9.6 0l-1.4 1.4c-1.9-1.9-4.9-1.9-6.8 0z"))
    if level >= 3:
        arcs.append(filled("M.8 5.6c4-4 10.4-4 14.4 0L13.8 7C10.6 3.8 5.4 3.8 2.2 7z"))
    return "".join(arcs)


WIRELESS_LEVELS = {
    "none": 0,
    "weak": 1,
    "ok": 2,
    "good": 3,
    "excellent": 3,
}

for name, level in WIRELESS_LEVELS.items():
    body = wireless(level)
    if "stroke=" in body:
        raise ValueError(f"wireless symbolic icon must be fill-only: {name}")
    ICONS[f"status/network-wireless-signal-{name}-symbolic.svg"] = body


def battery(level: int, charging: bool = False) -> str:
    width = max(0, round(8 * level / 100))
    body = [
        '<path fill="currentColor" fill-rule="evenodd" d="M1 4h12v8H1zm2 2v4h8V6z"/>',
        '<path fill="currentColor" d="M13 6h2v4h-2z"/>',
    ]
    if width and not charging:
        body.append(f'<rect fill="currentColor" x="3" y="6" width="{width}" height="4"/>')
    if charging:
        body.append('<path fill="currentColor" d="m8 3-3 5h2l-1 5 4-6H8z"/>')
    return "".join(body)


for level in range(0, 101, 10):
    ICONS[f"status/battery-level-{level}-symbolic.svg"] = battery(level)
    ICONS[f"status/battery-level-{level}-charging-symbolic.svg"] = battery(level, True)

ICONS["status/battery-level-100-charged-symbolic.svg"] = battery(100)


ALIASES = {
    # Nautilus and compatibility names.
    "actions/arrow-next-symbolic.svg": "go-next-symbolic.svg",
    "actions/cancel-operation-symbolic.svg": "process-stop-symbolic.svg",
    "actions/cut-symbolic.svg": "edit-cut-symbolic.svg",
    "actions/cut-large-symbolic.svg": "edit-cut-symbolic.svg",
    "actions/remove-custom-icon-symbolic.svg": "edit-delete-symbolic.svg",
    "actions/selection-mode-symbolic.svg": "object-select-symbolic.svg",
    # RTL mirrors are handled by dedicated semantic aliases for now.
    "actions/go-next-symbolic-rtl.svg": "go-previous-symbolic.svg",
    "actions/go-previous-symbolic-rtl.svg": "go-next-symbolic.svg",
    "actions/edit-undo-symbolic-rtl.svg": "edit-redo-symbolic.svg",
    "actions/edit-redo-symbolic-rtl.svg": "edit-undo-symbolic.svg",
    # Common state aliases.
    "status/network-wireless-symbolic.svg": "network-wireless-signal-excellent-symbolic.svg",
    "status/network-wireless-connected-symbolic.svg": "network-wireless-signal-excellent-symbolic.svg",
    "status/network-wireless-offline-symbolic.svg": "network-offline-symbolic.svg",
    "status/network-wired-disconnected-symbolic.svg": "network-offline-symbolic.svg",
    "status/network-vpn-disconnected-symbolic.svg": "network-offline-symbolic.svg",
    "status/audio-volume-overamplified-symbolic.svg": "audio-volume-high-symbolic.svg",
    "status/microphone-sensitivity-low-symbolic.svg": "microphone-sensitivity-high-symbolic.svg",
    "status/microphone-sensitivity-medium-symbolic.svg": "microphone-sensitivity-high-symbolic.svg",
    "status/emblem-unwriteable-symbolic.svg": "emblem-readonly-symbolic.svg",
}

for level in range(0, 101, 10):
    ALIASES[f"status/battery-level-{level}-plugged-in-symbolic.svg"] = (
        "battery-level-100-charged-symbolic.svg"
    )

ALIASES.update({
    "status/battery-symbolic.svg": "battery-level-100-symbolic.svg",
    "status/battery-low-symbolic.svg": "battery-level-10-symbolic.svg",
    "status/battery-caution-symbolic.svg": "battery-level-10-symbolic.svg",
})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build NewBe symbolic UI icons.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated icons and aliases without changing files",
    )
    return parser.parse_args()


def safe_path(relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or len(path.parts) != 2:
        raise ValueError(f"unsafe symbolic icon path: {relative}")
    if path.parts[0] not in {"actions", "status"}:
        raise ValueError(f"unsupported symbolic icon context: {relative}")
    return SYMBOLIC_ROOT / path


def main() -> int:
    args = parse_args()
    failures = 0

    for relative, body in sorted(ICONS.items()):
        path = safe_path(relative)
        expected = svg(body)
        if args.check:
            if path.is_symlink() or not path.is_file():
                print(f"ERROR: missing generated icon: {relative}", file=sys.stderr)
                failures += 1
            elif path.read_text(encoding="utf-8") != expected:
                print(f"ERROR: stale generated icon: {relative}", file=sys.stderr)
                failures += 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.is_symlink():
                path.unlink()
            path.write_text(expected, encoding="utf-8")

    for relative, target in sorted(ALIASES.items()):
        path = safe_path(relative)
        target_path = path.parent / target
        if target_path.parent != path.parent or not target_path.exists():
            print(f"ERROR: invalid alias target: {relative} -> {target}", file=sys.stderr)
            failures += 1
            continue
        if args.check:
            if not path.is_symlink() or path.readlink() != Path(target):
                print(f"ERROR: stale generated alias: {relative}", file=sys.stderr)
                failures += 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() or path.is_symlink():
                path.unlink()
            path.symlink_to(target)

    if failures:
        return 1

    if not args.check:
        print(f"Built {len(ICONS)} symbolic icons and {len(ALIASES)} aliases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
