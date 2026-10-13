# Saudi flag artwork

Original ASCII texture, layout, animation, and generator: **© 2026 iAlturki**, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

The underlying national flag design is separately identified as public domain on [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Flag_of_Saudi_Arabia.svg). Its source credits the Shura Council and the official Saudi flag website. An unchanged copy is stored in `reference/saudi-flag.svg`; its white shahada and sword paths are reused without transcription or reflection.

- [Original vector](https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg)
- [Official Saudi flag website](https://saudiflag.sa/)
- [Ministry of Culture flag guideline, 2023, English](https://cms.saudiflag.sa/uploads/Saudi_flag_ENGLISH_2023_617441c5ce.pdf)

Sources retrieved on **2026-10-13**. The green base is `#005430`, as specified in the guideline. The reference uses a 3:2 field. The digital cloth effect adds ASCII texture and gentle lighting; it does not change the inscription or sword design.

Rebuild with `python -m pip install Pillow resvg-py`, then `python tools/build_saudi_flag.py`. The generator rasterizes the original vector once at 816 × 560 pixels, deforms it offline, and downsamples each frame to produce a pre-rendered, transparent WebP animation at 408 × 280 pixels, 20 fps, with a 5.6-second loop. The image is displayed at its native size. This replaces the original 225 animated, clipped SVG copies, which caused excessive rendering work on mobile devices.

The README uses a `<picture>` element: `prefers-reduced-motion: reduce` selects the flat static SVG; WebP-capable browsers select the animation; other browsers use the still SVG fallback. Neither output needs JavaScript, tracking, external requests, or runtime dependencies. The static SVG contains just one copy of the flag artwork and no animation.
