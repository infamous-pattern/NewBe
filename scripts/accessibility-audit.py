#!/usr/bin/env python3
"""Check NewBe's automated accessibility and compatibility baseline."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

COLORS = {
    "graphite": "#20211f",
    "secondary text": "#595b57",
    "light background": "#e8e6df",
    "light surface": "#f3f1ea",
    "white": "#ffffff",
    "gold": "#d6a928",
    "dark gold": "#a77a12",
    "light link": "#79570b",
    "dark background": "#272927",
    "dark surface": "#41433f",
    "dark text": "#f0eee7",
    "dark secondary text": "#bbbdb7",
    "bright gold": "#e4be45",
}

CONTRAST_CHECKS = (
    ("primary text / light background", "graphite", "light background", 4.5),
    ("primary text / light surface", "graphite", "light surface", 4.5),
    ("secondary text / light background", "secondary text", "light background", 4.5),
    ("secondary text / light surface", "secondary text", "light surface", 4.5),
    ("light link / white", "light link", "white", 4.5),
    ("light link / light surface", "light link", "light surface", 4.5),
    ("text / gold selection", "graphite", "gold", 4.5),
    ("primary text / dark background", "dark text", "dark background", 4.5),
    ("primary text / dark surface", "dark text", "dark surface", 4.5),
    ("secondary text / dark background", "dark secondary text", "dark background", 4.5),
    ("secondary text / dark surface", "dark secondary text", "dark surface", 4.5),
    ("dark link / dark background", "bright gold", "dark background", 4.5),
    ("dark link / dark surface", "bright gold", "dark surface", 4.5),
    ("light focus / light background", "dark gold", "light background", 3.0),
    ("light focus / light surface", "dark gold", "light surface", 3.0),
    ("dark focus / dark background", "bright gold", "dark background", 3.0),
    ("dark focus / dark surface", "bright gold", "dark surface", 3.0),
)

REQUIRED_CSS = {
    "gtk-3.0/gtk.css": (
        "@define-color newbe_gold_dark #a77a12;",
        "@define-color newbe_link #79570b;",
        "button:focus",
        "checkbutton:focus",
        "outline-color: @newbe_gold_dark;",
        "color: @newbe_link;",
    ),
    "gtk-3.0/gtk-dark.css": (
        "@define-color newbe_gold_bright #d6a928;",
        "button:focus",
        "checkbutton:focus",
        "outline-color: @newbe_gold_bright;",
    ),
    "gtk-4.0/gtk.css": (
        "@define-color newbe_gold_dark #a77a12;",
        "@define-color newbe_link #79570b;",
        "*:focus-visible",
        "outline-color: @newbe_gold_dark;",
        "color: @newbe_link;",
    ),
    "gtk-4.0/gtk-dark.css": (
        "@define-color newbe_gold_bright #e4be45;",
        "*:focus-visible",
        "outline-color: @newbe_gold_bright;",
    ),
    "gnome-shell/gnome-shell.css": (
        "#panel .panel-button:focus",
        ".quick-toggle:focus",
        ".search-entry:focus",
    ),
    "extension/newbe@infamous-pattern.github.io/stylesheet.css": (
        ".newbe-panel-button:focus",
    ),
}


def channel(value: int) -> float:
    component = value / 255
    return component / 12.92 if component <= 0.04045 else ((component + 0.055) / 1.055) ** 2.4


def luminance(color: str) -> float:
    red, green, blue = (int(color[index : index + 2], 16) for index in (1, 3, 5))
    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def contrast(first: str, second: str) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def check_contrast() -> list[str]:
    errors = []
    print("Contrast baseline")
    for label, foreground, background, threshold in CONTRAST_CHECKS:
        ratio = contrast(COLORS[foreground], COLORS[background])
        status = "PASS" if ratio >= threshold else "FAIL"
        print(f"  {status} {ratio:5.2f}:1  {label} (minimum {threshold:.1f}:1)")
        if ratio < threshold:
            errors.append(f"{label}: {ratio:.2f}:1 is below {threshold:.1f}:1")
    return errors


def check_css() -> list[str]:
    errors = []
    print("CSS accessibility hooks")
    for relative, required in REQUIRED_CSS.items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        if stripped.count("{") != stripped.count("}"):
            errors.append(f"{relative}: unbalanced braces")
        missing = [fragment for fragment in required if fragment not in text]
        if missing:
            errors.append(f"{relative}: missing {', '.join(missing)}")
        else:
            print(f"  PASS {relative}")

    for relative in (
        "gtk-3.0/gtk.css",
        "gtk-3.0/gtk-dark.css",
        "gtk-4.0/gtk.css",
        "gtk-4.0/gtk-dark.css",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if re.search(r"\bfont-size\s*:", text):
            errors.append(f"{relative}: fixed font-size overrides user scaling")
    print("  PASS GTK themes do not override the user's font size")
    return errors


def main() -> int:
    print("NewBe Accessibility Baseline Audit")
    print("===================================")
    errors = check_contrast() + check_css()
    if errors:
        print("\nAccessibility audit failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("\nAccessibility baseline passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
