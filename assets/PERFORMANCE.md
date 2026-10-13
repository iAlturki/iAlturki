# Profile artwork performance

**© 2026 iAlturki — CC BY-NC-SA 4.0.** Measurements recorded on 2026-10-13.

The flag retains **112 frames at 20 fps**, 408 × 280 pixels, and its 5.6-second loop. Its AVIF sequence has temporal compression; the existing full-frame WebP remains available for browsers that do not support AVIF. Reduced-motion preferences select the still SVG.

The current AVIF output is approximately **110 KB**, compared with the **1.6 MB** WebP. The primary profile image payload falls from approximately **1.64 MB to 151 KB** for AVIF-capable browsers. These are uncompressed file-byte totals of the image assets loaded for ordinary animated playback, excluding the alternatives a browser does not select, source documents, and GitHub's own page resources. Rebuilds may change the exact byte totals.

The header uses the four authentic app logos and one gentle group transform. It no longer needs independently animated card transforms or a text reveal that clips the name. Both custom buttons use the actual destination logos, continuously rotating accent rings, and a short arrow movement. Their animation has no frame-rate cap, heavy filter, or script.

The MicMute card's glyph mask is bounded to the actual **44 × 44** badge instead of a **999 × 999** area. The Look20 card reuses a single embedded bubble image. Existing card demo loops and their timing remain intact. The generator also retains current release counts when rebuilding and removes indentation without removing meaningful text spacing.

The animations respect reduced-motion preferences. Desktop browser playback and a 390-pixel iframe layout are checked during visual review; this does not measure a physical phone's frame rate or guarantee identical playback across devices.
