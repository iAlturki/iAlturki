"""Build iAlturki's mobile-friendly, waving ASCII-style Saudi flag.

Copyright 2026 iAlturki. Original layout and animation: CC BY-NC-SA 4.0.
The national flag artwork has separate provenance in assets/SAUDI-FLAG-SOURCE.md.
Install Pillow, resvg-py, and FFmpeg with libaom-av1, then run with Python 3.
The browser only decodes pre-rendered WebP frames; it never animates SVG strips.
"""

from copy import deepcopy
from html import escape
from io import BytesIO
from math import cos, pi, sin
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from PIL import Image
import resvg_py

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
    for row in range(24):
        chars = []
        for col in range(72):
            density = (sin(col * .29 + row * .57) + cos(col * .11 - row * .37) + 2) / 4
            chars.append(alphabet[min(7, int(density * 8))])
        rows.append(f'<text x="0" y="{row * 25 + 20}" textLength="900" lengthAdjust="spacingAndGlyphs">{escape("".join(chars))}</text>')

    svg = f'''<svg xmlns="{NS}" viewBox="0 0 1020 700" width="408" height="280" role="img" aria-labelledby="title desc">
<title id="title">Saudi Arabia — an ASCII-style flag by iAlturki</title>
<desc id="desc">Green fabric made of ASCII characters, with the original white shahada and sword. The still version for reduced-motion preferences and image-format fallbacks.</desc>
<!-- Original ASCII layout and animation: Copyright 2026 iAlturki, CC BY-NC-SA 4.0. National flag artwork: see SAUDI-FLAG-SOURCE.md. -->
<defs>
<linearGradient id="pole" x1="0" x2="1"><stop stop-color="#46504e"/><stop offset=".48" stop-color="#ccd8d0"/><stop offset="1" stop-color="#64756b"/></linearGradient>
<linearGradient id="light"><stop stop-color="#fff" stop-opacity=".08"/><stop offset=".28" stop-color="#fff" stop-opacity=".025"/><stop offset=".52" stop-color="#fff" stop-opacity=".08"/><stop offset=".76" stop-color="#fff" stop-opacity=".025"/><stop offset="1" stop-color="#fff" stop-opacity=".07"/></linearGradient>
</defs>
<g transform="translate(50 50)"><path d="M0 0H900V600H0Z" fill="#005430"/>
<g fill="#d0ffe0" opacity=".19" font-family="Consolas,'Liberation Mono',monospace" font-size="20">{''.join(rows)}</g>
{artwork}
<rect width="900" height="600" fill="url(#light)"/>
<rect x=".5" y=".5" width="899" height="599" fill="none" stroke="#fff" stroke-opacity=".13"/>
</g>
<rect x="951" y="34" width="6" height="638" rx="3" fill="url(#pole)"/>
<circle cx="954" cy="32" r="6" fill="#a7c1af"/>
</svg>
'''
    output = ROOT / "assets/saudi-flag.svg"
    output.write_text(svg, encoding="utf-8", newline="\n")
    ET.parse(output)
    print(f"{output.name}: {output.stat().st_size:,} bytes")

    # Rasterize once at 2x display resolution, then downsample each frame.
    # Deform that single raster
    # during the build, rather than making each visitor redraw thousands of
    # vector paths and hundreds of thousands of text glyphs every frame.
    width, height = 816, 560
    scale = width / 1020
    base = Image.open(BytesIO(resvg_py.svg_to_bytes(svg_string=svg, width=width, height=height))).convert("RGBA")
    frames = []
    count = 112  # 20 fps, 5.6-second seamless cycle; integer 50ms frame duration.
    for index in range(count):
        angle = index * 2 * pi / count

        def displacement(x):
            distance = min(1, max(0, 1 - (x / scale - 50) / 900))
            return 38 * scale * distance ** .9 * sin(distance * pi * 3.1 - angle)

        mesh = []
        for x in range(0, width, 3):
            end = min(width, x + 3)
            left, right = displacement(x), displacement(end)
            mesh.append(((x, 0, end, height), (x, -left, x, height-left, end, height-right, end, -right)))
        frame = base.transform(base.size, Image.Transform.MESH, mesh, Image.Resampling.BICUBIC)
        frames.append(frame.resize((408, 280), Image.Resampling.LANCZOS))

    animation = ROOT / "assets/saudi-flag.webp"
    frames[0].save(animation, format="WEBP", save_all=True, append_images=frames[1:], duration=50, loop=0, quality=60, method=3, minimize_size=True)
    print(f"{animation.name}: {animation.stat().st_size:,} bytes; {count} frames at 20 fps")

    # AV1's temporal compression retains every frame. Use an opaque dark
    # stage because animated AVIF alpha has reported Safari playback bugs.
    # Transparent WebP remains the compatibility fallback with identical timing.
    compact = ROOT / "assets/saudi-flag.avif"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "408x280", "-r", "20", "-i", "pipe:0", "-frames:v", str(count), "-c:v", "libaom-av1", "-crf", "28", "-cpu-used", "6", "-row-mt", "1", "-threads", "4", "-pix_fmt", "yuv420p", "-g", str(count), "-loop", "0", str(compact)]
    encoder = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for frame in frames:
            stage = Image.new("RGB", frame.size, "#0d1117")
            stage.paste(frame, mask=frame.getchannel("A"))
            encoder.stdin.write(stage.tobytes())
    finally:
        encoder.stdin.close()
    if encoder.wait() != 0:
        raise RuntimeError("FFmpeg failed to encode the full-frame AVIF")
    print(f"{compact.name}: {compact.stat().st_size:,} bytes; {count} frames at 20 fps")


if __name__ == "__main__":
    build()
