# NewBe Icon Design Language

## Objective

NewBe icons should look like the visual language of BeOS matured into a modern premium workstation environment.

They are not intended to reproduce historical BeOS icons.

## Character

NewBe application and object icons should feel:

- dimensional
- realistic
- elegant
- polished
- slightly luxurious
- friendly
- immediately readable

## Materials

Preferred visual materials include:

- warm brushed gold
- satin aluminum
- polished steel
- glass
- ceramic
- rich colored enamel
- subtle translucent materials

Avoid:

- flat monochrome application artwork
- excessive gradients
- cartoon-style exaggeration
- excessive gloss
- photorealistic clutter

## Geometry

Primary application icons should:

- use strong silhouettes
- remain readable at small sizes
- use moderate corner rounding
- avoid excessive circular badges
- retain visual depth without becoming skeuomorphic

## Gold

NewBe gold is an identity accent, not a requirement for every icon.

Primary:
#D6A928

Bright:
#E4BE45

Dark:
#A77A12

## Symbolic Icons

Symbolic icons are a separate visual family.

They should be:

- simple
- geometric
- monochrome
- readable at 16px
- compatible with GNOME recoloring
- named with the -symbolic suffix

Do not apply dimensional effects to symbolic icons.

## Application Branding

For third-party application icons:

- preserve enough of the application's identity to remain recognizable
- reinterpret the artwork into the NewBe material and dimensional language where legally and practically appropriate
- do not intentionally mimic proprietary artwork pixel-for-pixel
- provide aliases for legacy desktop-file icon names where necessary

## Compatibility

NewBe should prefer scalable SVG source artwork.

Fallback order:

NewBe
  -> Adwaita
  -> hicolor
  -> application's own installed icon

## Coverage Goal

Long-term target:

- Core desktop: 100%
- Major current Linux applications: 95%+
- Common legacy Linux applications: 90%+
- Standard actions / devices / places: 95%+
- Unknown applications: graceful inherited fallback

## Source Canvas

Primary dimensional icons are designed on a nominal:

    256 × 256

SVG canvas.

Artwork must remain clearly recognizable when rendered at:

    16
    24
    32
    48
    64
    128
    256

pixels.

## Lighting

All dimensional NewBe icons use a consistent virtual light source:

    upper-left, approximately 10:30

Highlights should appear primarily on:

- upper edges
- left-facing surfaces

Shadows should fall subtly toward:

- lower-right

Avoid dramatic drop shadows.

## Depth

Icons should use approximately three visual layers:

1. Base silhouette
2. Material / dimensional surface
3. Identity detail

Do not create excessive micro-detail that disappears below 48px.

## Third-party Applications

Third-party icons should remain immediately recognizable.

NewBe may reinterpret:

- depth
- material
- edge treatment
- lighting
- dimensionality

but should preserve the application's essential visual identity.

Do not simply copy or embed proprietary raster artwork.
