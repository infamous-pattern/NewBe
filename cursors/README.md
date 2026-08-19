# NewBe Cursor Theme

NewBe ships 15 original cursor designs at 24, 32, 48, and 64 pixels, plus standard Xcursor compatibility aliases. The compiled files live in `icons/NewBe/cursors`, so the same `NewBe` theme name works for both icons and cursors.

The source of truth is:

- `src/*.svg` — editable 64×64 vector artwork
- `cursors.conf` — cursor names and source-canvas hotspots
- `aliases.conf` — compatibility names mapped to compiled designs

End users do not need cursor build tools. The compiled Xcursor files are checked into the repository and installed with the icon theme.

Maintainers can rebuild them with:

```bash
./scripts/build-cursors.py
./scripts/cursor-audit.py
```

The builder uses the system `libXcursor` library and ImageMagick. The dependency-free audit parses the compiled format directly and verifies every size, hotspot, source, and alias.
