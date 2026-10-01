"""Builds assets/banner-light.svg and assets/banner-dark.svg.

Left: "iAlturki" drawn out of its own letters (the i from i's, the A from A's),
sampled from a real font onto a character grid, with a one-step depth copy.
Right: MicMute's mute badge on a corner of the 444005129.xyz wallpaper, playing
its real timeline once: in 180 ms, plate melts at 3.18 s, dims to 70% at 6.18 s,
then rests with nothing animating.

    python tools/build_banner.py [--font path/to/font.ttf]

Needs Python 3 and Pillow. The font is only used to rasterise the grid; the SVG
itself uses the viewer's monospace font and embeds nothing but a 90x90 PNG.
"""
import argparse, base64, io, pathlib
from PIL import Image, ImageDraw, ImageFont

# keep in sync with MicMute/src/overlay.c @9a054c4
IN_MS, HOLD_MS, MELT_MS, WAIT_MS, DIM_MS, DIM_ALPHA = 180, 3000, 600, 2400, 400, 179 / 255

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = 'iAlturki'
COLS, ROWS, CELL_W, CELL_H, X0, Y0 = 124, 26, 5.0, 6.5, 8, 10

ap = argparse.ArgumentParser()
ap.add_argument('--font', default=r'C:\Windows\Fonts\seguisb.ttf')  # Segoe UI Semibold
args = ap.parse_args()

# ---- letterized name -------------------------------------------------------
font = ImageFont.truetype(args.font, 300)
left, top, right, bottom = font.getbbox(NAME)
img = Image.new('L', (right - left + 4, bottom - top + 4), 0)
ImageDraw.Draw(img).text((2 - left, 2 - top), NAME, font=font, fill=255)
gw, gh = img.size
# horizontal span of each glyph, from the advances of growing prefixes
edges = [font.getlength(NAME[:i]) - left + 2 for i in range(len(NAME) + 1)]

rows = []
for r in range(ROWS):
    cells = []
    for c in range(COLS):
        x0, x1 = int(c * gw / COLS), int((c + 1) * gw / COLS)
        y0, y1 = int(r * gh / ROWS), int((r + 1) * gh / ROWS)
        box = img.crop((x0, y0, max(x1, x0 + 1), max(y1, y0 + 1)))
        cov = sum(box.getdata()) / (255 * box.size[0] * box.size[1])
        cx = (x0 + x1) / 2
        ch = next((NAME[i] for i in range(len(NAME)) if edges[i] <= cx < edges[i + 1]), NAME[-1])
        cells.append((ch, 'full' if cov >= 0.5 else 'edge' if cov >= 0.2 else None))
    rows.append(cells)

def row_svg(cells, y):
    out, run, kind = [], '', None
    def flush():
        nonlocal run
        if run:
            out.append(f'<tspan class="e">{run}</tspan>' if kind == 'edge' else run)
            run = ''
    for ch, k in cells:
        k2 = k or 'blank'
        if k2 != kind:
            flush(); kind = k2
        run += ch if k else ' '
    flush()
    return (f'<text x="{X0}" y="{y:.1f}" textLength="{COLS * CELL_W:.0f}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve">{"".join(out)}</text>')

name_rows = '\n'.join(row_svg(cells, Y0 + (i + 1) * CELL_H) for i, cells in enumerate(rows))

# ---- MicMute badge (render.c RenderBadge geometry, badge 64 px) ------------
s, bx, by = 64.0, 758.0, 24.0
m = 24.0                       # max(8, 64*3/8): the shadow margin
r = s * 0.24
spread = m * 0.8
u = s * 0.6
gx, gy = bx + (s - u) / 2, by + (s - u) / 2
f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')

shadow = '\n'.join(
    f'<rect x="{f(bx - g)}" y="{f(by - g + spread * 0.35)}" width="{f(s + 2 * g)}" height="{f(s + 2 * g)}" '
    f'rx="{f(r + g)}" fill="#000" fill-opacity="{(5 + j * 6) / 255:.3f}"/>'
    for j in range(6) for g in [spread * (6 - j) / 6])

def mic(dx, dy, fill, op=None):
    x, y = gx + dx, gy + dy
    cx, cy, rx, ry = x + 0.5 * u, y + 0.41 * u, 0.345 * u, 0.31 * u
    o = f' opacity="{op}"' if op else ''
    return (f'<g{o}><rect x="{f(x + .33 * u)}" y="{f(y + .04 * u)}" width="{f(.34 * u)}" height="{f(.56 * u)}" rx="{f(.17 * u)}" fill="{fill}"/>'
            f'<g fill="none" stroke="{fill}" stroke-width="{f(.085 * u)}" stroke-linecap="round">'
            f'<path d="M{f(cx + rx)} {f(cy)}A{f(rx)} {f(ry)} 0 0 1 {f(cx - rx)} {f(cy)}"/>'
            f'<path d="M{f(x + .5 * u)} {f(y + .72 * u)}V{f(y + .88 * u)}M{f(x + .34 * u)} {f(y + .92 * u)}H{f(x + .66 * u)}"/></g></g>')

x1, y1, x2, y2 = gx + .13 * u, gy + .08 * u, gx + .87 * u, gy + .92 * u
slash = f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}'

wp = Image.open(ROOT / 'tools' / 'wallpaper.png').convert('RGB').quantize(colors=4)
buf = io.BytesIO(); wp.save(buf, 'PNG', optimize=True)
wallpaper = base64.b64encode(buf.getvalue()).decode()

def svg(dark):
    face, depth = ('#E6EDF3', '#3D444D') if dark else ('#1F2328', '#D1D9E0')
    stroke = ' stroke="#30363D"' if dark else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 846 180" width="846" height="180" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="7.2">
<style>
.face{{fill:{face}}}.depth{{fill:{depth}}}.e{{fill-opacity:.55}}
.in{{animation:in {IN_MS}ms cubic-bezier(.333,1,.667,1) both}}
@keyframes in{{from{{opacity:0;transform:translateY(-14px)}}to{{opacity:1;transform:none}}}}
.plate{{opacity:0;animation:melt {MELT_MS}ms cubic-bezier(.333,0,.667,1) {IN_MS + HOLD_MS}ms both}}
@keyframes melt{{from{{opacity:1}}to{{opacity:0}}}}
.dim{{opacity:{DIM_ALPHA:.3f};animation:dim {DIM_MS}ms cubic-bezier(.333,.667,.667,1) {IN_MS + HOLD_MS + MELT_MS + WAIT_MS}ms both}}
@keyframes dim{{from{{opacity:1}}to{{opacity:{DIM_ALPHA:.3f}}}}}
@media (prefers-reduced-motion:reduce){{.in,.plate,.dim{{animation:none}}}}
</style>
<defs>
<g id="name">
{name_rows}
</g>
<clipPath id="tile"><rect x="666" y="0" width="180" height="180" rx="12"/></clipPath>
<linearGradient id="hl" x1="0" y1="{f(by)}" x2="0" y2="{f(by + .6 * s)}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="notch" maskUnits="userSpaceOnUse" x="666" y="0" width="180" height="180"><rect x="666" y="0" width="180" height="180" fill="#fff"/><path d="{slash}" stroke="#000" stroke-width="{f(.19 * u)}" stroke-linecap="round"/></mask>
</defs>
<use href="#name" xlink:href="#name" class="depth" transform="translate(2.5 2.5)"/>
<use href="#name" xlink:href="#name" class="face"/>
<g clip-path="url(#tile)">
<rect x="666" y="0" width="180" height="180" fill="#0D0F14"/>
<image x="666" y="0" width="180" height="180" style="image-rendering:pixelated" href="data:image/png;base64,{wallpaper}"/>
</g>
<rect x="666.5" y=".5" width="179" height="179" rx="12" fill="none"{stroke or ' stroke="none"'}/>
<g class="dim"><g class="in">
<g class="plate">
{shadow}
<rect x="{f(bx)}" y="{f(by)}" width="{f(s)}" height="{f(s)}" rx="{f(r)}" fill="#15171F" fill-opacity=".933"/>
<rect x="{f(bx + 1)}" y="{f(by + 1)}" width="{f(s - 2)}" height="{f(.6 * s - 1)}" rx="{f(r - 1)}" fill="url(#hl)"/>
<rect x="{f(bx + .5)}" y="{f(by + .5)}" width="{f(s - 1)}" height="{f(s - 1)}" rx="{f(r)}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="1.28"/>
<circle cx="{f(gx + .5 * u)}" cy="{f(gy + .5 * u)}" r="{f(.6 * u)}" fill="#90202A" fill-opacity=".125"/>
</g>
<g mask="url(#notch)">
{mic(.05 * u, .05 * u, '#101218', '.35')}
{mic(0, 0, '#F2F3F7')}
</g>
<path d="{slash}" stroke="#FF4750" stroke-width="{f(.10 * u)}" stroke-linecap="round"/>
</g></g>
</svg>
'''

for dark, name in [(False, 'banner-light.svg'), (True, 'banner-dark.svg')]:
    p = ROOT / 'assets' / name
    p.parent.mkdir(exist_ok=True)
    p.write_text(svg(dark), encoding='utf-8', newline='\n')
    print(p.name, p.stat().st_size, 'bytes')
