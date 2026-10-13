"""Build iAlturki's self-contained, waving ASCII-style Saudi flag.

Copyright 2026 iAlturki. Original layout and animation: CC BY-NC-SA 4.0.
The national flag artwork has separate provenance in assets/SAUDI-FLAG-SOURCE.md.
Run from any directory with Python 3; no third-party packages are required.
"""

from copy import deepcopy
from html import escape
from math import cos, pi, sin
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def build():
    original = ET.parse(ROOT / "assets/reference/saudi-flag.svg").getroot()
    white = deepcopy(original.find(f"{{{NS}}}g[@id='white']"))
    if white is None:
        raise ValueError("The reference must contain the original white flag artwork")
    # No transcription, font substitution, reflection, or redrawing of the shahada.
    artwork = ET.tostring(white, encoding="unicode")

    # Literal ASCII characters, deterministically arranged into a woven texture.
    alphabet = ".:;+=*#@"
    rows = []
    for row in range(36):
        chars = []
        for col in range(100):
            density = (sin(col * .29 + row * .57) + cos(col * .11 - row * .37) + 2) / 4
            chars.append(alphabet[min(7, int(density * 8))])
        rows.append(f'<text x="0" y="{row * 16 + 13}" textLength="900" lengthAdjust="spacingAndGlyphs">{escape("".join(chars))}</text>')

    clips, strips, rules = [], [], []
    bands = 225
    band_width = 900 / bands
    for i in range(bands):
        x = i * band_width
        # The hoist is on the right; the free left edge has the greatest motion.
        distance = 1 - (x + band_width / 2) / 900
        amplitude = 38 * distance ** .9
        phase = distance * pi * 3.1
        frames = []
        for step in range(17):
            angle = phase - step * pi / 8
            y = amplitude * sin(angle)
            frames.append(f'{step * 6.25:g}%{{transform:translateY({y:.2f}px);}}')
        rules.append(f'.s{i}{{transform:translateY({amplitude * sin(phase):.2f}px);animation:w{i} 5.6s linear infinite}}@keyframes w{i}{{{"".join(frames)}}}')
        # A small overlap prevents antialiasing seams at fractional display sizes.
        clips.append(f'<clipPath id="b{i}"><rect x="{x-.2:g}" y="0" width="{band_width+.4:g}" height="600"/></clipPath>')
        strips.append(f'<g class="strip s{i}"><g clip-path="url(#b{i})"><use href="#cloth"/><rect x="{x:g}" width="{band_width:g}" height="600" fill="#fff" opacity="{.025 + .055 * (.5 + .5 * cos(phase)):.3f}"/></g></g>')

    svg = f'''<svg xmlns="{NS}" viewBox="0 0 1020 700" width="408" height="280" role="img" aria-labelledby="title desc">
<title id="title">Saudi Arabia — a waving ASCII-style flag by iAlturki</title>
<desc id="desc">Green fabric made of ASCII characters, with the original white shahada and sword. A gentle wave travels from the right-hand hoist to the free edge. Reduced-motion preferences show a still flag.</desc>
<!-- Original ASCII layout and animation: Copyright 2026 iAlturki, CC BY-NC-SA 4.0. National flag artwork: see SAUDI-FLAG-SOURCE.md. -->
<style>{''.join(rules)}
@media(prefers-reduced-motion:reduce){{.strip{{animation:none!important;transform:none!important}}}}
</style>
<defs>
<linearGradient id="pole" x1="0" x2="1"><stop stop-color="#46504e"/><stop offset=".48" stop-color="#ccd8d0"/><stop offset="1" stop-color="#64756b"/></linearGradient>
<g id="cloth"><path d="M0 0H900V600H0Z" fill="#005430"/>
<g fill="#d0ffe0" opacity=".19" font-family="Consolas,'Liberation Mono',monospace" font-size="14">{''.join(rows)}</g>
{artwork}
<rect x=".5" y=".5" width="899" height="599" fill="none" stroke="#fff" stroke-opacity=".13"/>
</g>
{''.join(clips)}
</defs>
<g transform="translate(50 50)">{''.join(strips)}</g>
<rect x="951" y="34" width="6" height="638" rx="3" fill="url(#pole)"/>
<circle cx="954" cy="32" r="6" fill="#a7c1af"/>
</svg>
'''
    output = ROOT / "assets/saudi-flag.svg"
    output.write_text(svg, encoding="utf-8", newline="\n")
    ET.parse(output)
    print(f"{output.name}: {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
