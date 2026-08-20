# NewBe Design Language

## Philosophy

NewBe is not a reproduction of historical BeOS.

It represents what BeOS might have become if its design language had continued to mature into a modern Wayland desktop.

The visual experience should feel:

- precise
- elegant
- calm
- fast
- engineered
- warm
- slightly luxurious
- immediately recognizable

## Core palette

### Gold

Primary accent:

    #D6A928

Bright accent:

    #E4BE45

Pressed / dark gold:

    #A77A12

Accessible light-surface link:

    #79570B

### Light surfaces

Primary background:

    #E8E6DF

Secondary background:

    #D8D6CF

Raised surface:

    #F3F1EA

### Dark surfaces

Primary dark:

    #272927

Secondary dark:

    #343633

Raised dark:

    #41433F

### Text

Light mode primary:

    #20211F

Light mode secondary:

    #595B57

Dark mode primary:

    #F0EEE7

Dark mode secondary:

    #BBBDB7

## Windows

Active windows should use the NewBe gold identity prominently but with restraint.

Inactive windows should reduce saturation and contrast.

Window geometry should remain crisp and structured, avoiding excessive rounded corners.

## Motion

Animations should feel fluid but controlled.

Avoid:

- elastic motion
- excessive bounce
- unnecessary blur
- long transitions

Prefer:

- short ease-out transitions
- subtle fades
- smooth workspace motion
- clear response to input

## Icons

Icons should feel realistic and regal rather than cartoon-like.

Characteristics:

- dimensional
- polished
- restrained metallic highlights
- warm gold accents where appropriate
- readable silhouettes
- high legibility at small sizes
- symbolic variants for GNOME interface use

## Typography

Recommended:

- IBM Plex Sans
- IBM Plex Mono

Typography remains user-configurable through GNOME Tweaks.

## Appearance modes

NewBe supports both light and dark desktop appearances.

### Light

The light appearance uses:

- warm neutral gray surfaces
- dark graphite text
- restrained gold focus indicators
- subtle dimensional highlights

### Dark

The dark appearance uses:

- charcoal surfaces rather than absolute black
- warm off-white typography
- slightly subdued gold
- stronger but restrained depth and shadow

### System integration

NewBe follows the GNOME system color-scheme preference.

It should not require users to maintain an independent NewBe light/dark preference.

The theme must remain usable when users modify fonts, cursors, icons, and other standard GNOME settings through GNOME Tweaks.

## Accessibility

Keyboard focus must remain visibly distinct from hover and selection. NewBe
uses a darker gold outline on light surfaces and a bright gold outline on dark
surfaces. Normal-size links on light surfaces use the deeper link token instead
of the decorative gold accent.

GTK themes must not override the user's chosen font size. Accessibility and
compatibility expectations, automated checks, and the manual release checklist
are documented in [ACCESSIBILITY.md](ACCESSIBILITY.md).
