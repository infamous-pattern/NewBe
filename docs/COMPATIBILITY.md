# Compatibility

NewBe is Wayland-first and primarily developed on Fedora Workstation. Support
claims distinguish a complete live desktop test from automated package
validation so users can make an informed choice.

## GNOME and Fedora matrix

| Fedora | GNOME Shell | Extension package | Live desktop |
|---|---:|---:|---:|
| 42 | 48 | Automated | Community testing requested |
| 43 | 49 | Automated | Community testing requested |
| 44 | 50 | Automated | Tested |

The compatibility workflow builds the extension with each Fedora release's
own `gnome-extensions` tool. It also validates the metadata, GSettings schema,
and packaged ZIP structure. This catches packaging and declared-version
problems, but it does not emulate a complete graphical GNOME session.

The shared extension source is appropriate for GNOME 48–50 because the
official GNOME porting guides report no relevant `metadata.json`,
`extension.js`, or `prefs.js` changes across those releases. NewBe does not
declare support for a Shell release until it is included in the automated
matrix.

## Desktop components

- GTK 3 and GTK 4 themes use standard CSS and are runtime-parsed on the primary
  Fedora 44 development system.
- The icon and cursor themes follow freedesktop naming and inheritance
  conventions, with aliases audited by the repository verifier.
- Wallpaper assets are desktop-independent JPEG and PNG files; GNOME metadata
  registration is tested by isolated installation.
- GNOME Shell CSS can still require adjustment when upstream Shell internals
  change, even when the extension JavaScript remains compatible.

## Reporting compatibility results

Include the Fedora or distribution release, GNOME Shell version, GTK version,
Wayland session type, NewBe version, and the affected component. A screenshot
or relevant journal excerpt is useful, but remove private information first.

Official GNOME references:

- [Targeting older GNOME versions](https://gjs.guide/extensions/development/targeting-older-gnome.html)
- [Porting to GNOME Shell 48](https://gjs.guide/extensions/upgrading/gnome-shell-48.html)
- [Porting to GNOME Shell 49](https://gjs.guide/extensions/upgrading/gnome-shell-49.html)
- [Porting to GNOME Shell 50](https://gjs.guide/extensions/upgrading/gnome-shell-50.html)
