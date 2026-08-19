# NewBe Wallpapers

The complete NewBe wallpaper collection is stored in this repository so it can be used independently of the GTK, Shell, and icon themes.

Every wallpaper includes its original PNG master and ready-to-use JPEG exports at 1920×1080, 1920×1200, 2560×1440, 2560×1600, 3440×1440, 3840×2160, and 5120×2160.

Running `scripts/install.sh` installs the seven 4K exports into the current user's data directory and registers them with GNOME Background settings. It does not select a wallpaper or modify any GNOME setting.

| Wallpaper | Role | Browse files | 4K download |
|---|---|---|---|
| Desert Dawn | Supporting | [All sizes](01-desert-dawn/) | [3840×2160](01-desert-dawn/newbe-01-desert-dawn-3840x2160.jpg) |
| Glass Horizon | Primary light hero | [All sizes](02-glass-horizon/) | [3840×2160](02-glass-horizon/newbe-02-glass-horizon-3840x2160.jpg) |
| Brushed Arc | Alternate light hero | [All sizes](03-brushed-arc/) | [3840×2160](03-brushed-arc/newbe-03-brushed-arc-3840x2160.jpg) |
| Alpine Sun | Supporting | [All sizes](04-alpine-sun/) | [3840×2160](04-alpine-sun/newbe-04-alpine-sun-3840x2160.jpg) |
| Coastal Pavilion | Supporting | [All sizes](05-coastal-pavilion/) | [3840×2160](05-coastal-pavilion/newbe-05-coastal-pavilion-3840x2160.jpg) |
| Floating Panels | Supporting | [All sizes](06-floating-panels/) | [3840×2160](06-floating-panels/newbe-06-floating-panels-3840x2160.jpg) |
| Moon Reflection | Dark hero | [All sizes](07-moon-reflection/) | [3840×2160](07-moon-reflection/newbe-07-moon-reflection-3840x2160.jpg) |

## Integrity

`SHA256SUMS` covers all 56 wallpaper assets. From this directory, verify a downloaded checkout with:

```bash
sha256sum --check SHA256SUMS
```

The repository's dependency-free `scripts/wallpaper-audit.py` additionally verifies the inventory and exact pixel dimensions.

Generation details and the creative specifications for every master are documented in [PROVENANCE.md](PROVENANCE.md).
