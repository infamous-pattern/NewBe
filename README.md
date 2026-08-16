# NewBe

**NewBe** is a modern Wayland-first GNOME desktop experience inspired by the idea that BeOS continued evolving into a fluid, elegant, productivity-focused operating system.

NewBe is designed primarily for Fedora Workstation and modern GNOME, while remaining as portable as practical across current GNOME-based Linux distributions.

## Design goals

- Wayland-first
- Smooth and fluid
- Modern evolution of BeOS design principles
- Compatible with GNOME Tweaks
- Modular GTK, Shell, icon, cursor, and wallpaper components
- No X11-specific hacks
- No modifications to Mutter
- No modification of GNOME system files during user installation
- Auditable installation and maintenance scripts
- Security scanning in CI
- Clean uninstall and rollback support

## Components

- GTK 3 theme
- GTK 4 theme
- GNOME Shell theme
- NewBe icon theme
- NewBe cursor theme
- NewBe wallpaper collection
- NewBe GNOME Shell extension
- Installation and audit tools

## Typography

Recommended defaults:

- Interface: IBM Plex Sans
- Monospace: IBM Plex Mono

Fonts are not hard-coded. Users remain free to select other fonts through GNOME Tweaks.

## Wallpapers

NewBe includes seven official wallpapers:

1. Desert Dawn
2. Glass Horizon
3. Brushed Arc
4. Alpine Sun
5. Coastal Pavilion
6. Floating Panels
7. Moon Reflection

Featured hero wallpapers:

- Glass Horizon — primary hero
- Brushed Arc — alternate light hero
- Moon Reflection — dark hero

Target resolutions:

- 1920x1080
- 1920x1200
- 2560x1440
- 2560x1600
- 3440x1440
- 3840x2160
- 5120x2160

## Security

NewBe installation scripts are intended to be readable, auditable, and reversible.

The project will use automated security and quality checks including:

- ShellCheck
- CodeQL
- dependency review
- RPM validation
- GNOME extension validation
- install/uninstall testing

NewBe will never use `curl | sh` style installation.

## Status

NewBe is currently in early development.

The initial target platform is Fedora Workstation 44 running GNOME on Wayland.

## License

License information is available in the `LICENSE` file.

## Featured visual identity

NewBe's initial hero wallpaper set is:

- Glass Horizon — primary light hero
- Brushed Arc — alternate light hero
- Moon Reflection — dark hero

These form the initial visual identity for screenshots, release artwork, and default GNOME background configuration.
