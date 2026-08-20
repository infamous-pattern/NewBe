# Accessibility and compatibility

NewBe treats accessibility as a release requirement. Its automated baseline is
informed by [WCAG 2.2 AA contrast criteria](https://www.w3.org/TR/WCAG22/)
and the GNOME Human Interface Guidelines for
[accessibility](https://developer.gnome.org/hig/guidelines/accessibility.html)
and [keyboard input](https://developer.gnome.org/hig/guidelines/keyboard.html),
while recognizing that automated checks alone do not establish conformance.

## Automated baseline

Run the dedicated audit with:

```bash
./scripts/accessibility-audit.py
```

It verifies:

- at least 4.5:1 contrast for representative normal text and link pairs;
- at least 3:1 contrast for light and dark keyboard-focus indicators;
- explicit focus styling for GTK 3, GTK 4, GNOME Shell, and the extension;
- balanced CSS blocks and expected accessibility selectors;
- no fixed font-size overrides in the GTK themes, preserving user font scaling.

The audit is also part of `scripts/verify.sh` and the GitHub Actions quality
workflow.

## Tested platform

The current desktop test target is Fedora Workstation 44 on Wayland with:

- GNOME Shell 50.4
- GTK 3.24.52
- GTK 4.22.4
- libadwaita 1.9.3

The clean-environment test covers installation, uninstallation, and packaged
release verification in a Fedora 44 container. A container does not replace a
real GNOME desktop usability test.

The broader GNOME and Fedora test matrix, including the distinction between
package validation and live testing, is documented in
[COMPATIBILITY.md](COMPATIBILITY.md).

## Manual release checklist

Before a stable release, test the installed theme on a real GNOME Wayland
session with:

- keyboard-only navigation, including visible focus in panels, menus, dialogs,
  Quick Settings, search, and the overview;
- Large Text enabled and text scaled to 200%;
- High Contrast enabled to confirm NewBe does not prevent the system override;
- Orca screen-reader navigation through the extension and standard controls;
- the on-screen keyboard for text entry and panel interaction;
- 100%, 125%, 150%, and 200% display scaling where supported;
- both light and dark appearances.

Report accessibility problems through the project issue tracker with the GNOME,
GTK, and NewBe versions, the appearance mode, and a screenshot when useful.
