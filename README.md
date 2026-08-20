# NewBe

**NewBe** is a modern Wayland-first GNOME desktop experience inspired by the idea that BeOS continued evolving into a fluid, elegant, productivity-focused operating system.

NewBe is designed primarily for Fedora Workstation and modern GNOME, while remaining as portable as practical across current GNOME-based Linux distributions.

## Preview

Current development previews use NewBe's repository-owned artwork and SVG assets.

### Glass Horizon wallpaper

![NewBe Glass Horizon wallpaper](docs/images/glass-horizon.png)

### Application icons

![NewBe application icons](docs/images/application-icons.png)

### Places and devices

![NewBe folder, place, and device icons](docs/images/places-and-devices.png)

### GNOME utilities

![NewBe GNOME utility icons](docs/images/gnome-utilities.png)

### Cursor theme

![NewBe cursor theme](docs/images/cursors.png)

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
- Automated accessibility contrast and focus checks
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

The NewBe cursor theme includes 15 original designs, four HiDPI sizes, and standard compatibility aliases. Its editable vector sources and reproducible build details are documented in [cursors/README.md](cursors/README.md).

## Installation

Download and extract the release archive, then run:

```bash
./scripts/verify.sh
./scripts/install.sh
```

Each archive is published with a `.sha256` file. Verify both files from the same directory before extraction:

```bash
sha256sum --check NewBe-0.1.0-alpha.2.tar.gz.sha256
```

Installation is user-scoped and does not require root. It installs the GTK and Shell themes, icon and cursor theme, seven wallpapers, and the NewBe GNOME Shell extension. It does not change or enable any GNOME setting automatically.

After installation, use GNOME Tweaks to select NewBe components. The extension can be enabled explicitly with:

```bash
gnome-extensions enable newbe@infamous-pattern.github.io
```

To remove all NewBe-owned user files without changing GNOME settings:

```bash
./scripts/uninstall.sh
```

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

[Browse and download every wallpaper in all supported sizes](assets/wallpapers/README.md). Original PNG masters and SHA-256 checksums are included.

The user installer registers all seven 4K wallpapers with GNOME Background settings. Glass Horizon automatically pairs with Moon Reflection in GNOME's light/dark background mode. Installation never changes the currently selected wallpaper.

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

Accessibility expectations, automated coverage, and the manual GNOME test
matrix are documented in [docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md).

## Status

NewBe is currently in early development.

The primary target platform is Fedora Workstation 44 running GNOME 50 on
Wayland. The Shell extension is also package-validated for GNOME 48 and 49 on
Fedora 42 and 43. See [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) for the
tested-support matrix and its limits.

## License

NewBe uses a split license: software, scripts, extension code, and CSS are available under MIT; original icons, cursors, wallpapers, and preview artwork are available under CC BY-SA 4.0. Exact path coverage and full license texts are in the [`LICENSE`](LICENSE) file and [`LICENSES`](LICENSES/) directory.

## Featured visual identity

NewBe's initial hero wallpaper set is:

- Glass Horizon — primary light hero
- Brushed Arc — alternate light hero
- Moon Reflection — dark hero

These form the initial visual identity for screenshots, release artwork, and default GNOME background configuration.
