# Saudi flag artwork

Original ASCII texture, layout, animation, and generator: **© 2026 iAlturki**, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

The underlying national flag design is separately identified as public domain on [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Flag_of_Saudi_Arabia.svg). Its source credits the Shura Council and the official Saudi flag website. An unchanged copy is stored in `reference/saudi-flag.svg`; its white shahada and sword paths are reused without transcription or reflection.

- [Original vector](https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg)
- [Official Saudi flag website](https://saudiflag.sa/)
- [Ministry of Culture flag guideline, 2023, English](https://cms.saudiflag.sa/uploads/Saudi_flag_ENGLISH_2023_617441c5ce.pdf)

Sources retrieved on **2026-10-13**. The green base is `#005430`, as specified in the guideline. The reference uses a 3:2 field. The digital cloth effect adds ASCII texture and gentle lighting; it does not change the inscription or sword design.

Rebuild the self-contained profile image with `python tools/build_saudi_flag.py`. It uses native SVG and CSS, with no JavaScript, tracking, external requests, or runtime dependencies. `prefers-reduced-motion: reduce` displays the flat, static flag.
