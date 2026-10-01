"""Builds the animated README art in assets/: header, four work cards, buttons.

    python tools/build_svgs.py

Pure SVG + CSS animation (what GitHub renders inside <img>): no scripts, no
external fonts or images. Two small PNGs are inlined: the site's dither and
Look20's bubble, both rendered by the ports on 444005129.xyz. Every animation
stops under prefers-reduced-motion and rests on a meaningful frame.
"""
import base64, io, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONT = "'Segoe UI Variable Display','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
RED, GREEN, NV, BLUE, ORANGE = '#FF4750', '#3DD68C', '#76B900', '#609CFF', '#FF3D00'


def png64(path, colors=None):
    im = Image.open(ROOT / 'tools' / path)
    if colors:
        im = im.convert('RGB').quantize(colors=colors)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


DITHER = png64('wallpaper.png', 4)
BUBBLE = png64('look20-bubble.png')
f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')


def mic(x, y, u, fill, op=None):
    """render.c DrawMic in box (x, y, u)."""
    cx, cy, rx, ry = x + .5 * u, y + .41 * u, .345 * u, .31 * u
    o = f' opacity="{op}"' if op else ''
    return (f'<g{o}><rect x="{f(x+.33*u)}" y="{f(y+.04*u)}" width="{f(.34*u)}" height="{f(.56*u)}" rx="{f(.17*u)}" fill="{fill}"/>'
            f'<g fill="none" stroke="{fill}" stroke-width="{f(.085*u)}" stroke-linecap="round">'
            f'<path d="M{f(cx+rx)} {f(cy)}A{f(rx)} {f(ry)} 0 0 1 {f(cx-rx)} {f(cy)}"/>'
            f'<path d="M{f(x+.5*u)} {f(y+.72*u)}V{f(y+.88*u)}M{f(x+.34*u)} {f(y+.92*u)}H{f(x+.66*u)}"/></g></g>')


def badge(bx, by, s, uid):
    """render.c RenderBadge at size s, top-left (bx, by): returns (plate, muted glyph, live glyph)."""
    m, r = s * 3 / 8, s * .24
    spread, u = m * .8, s * .6
    gx, gy = bx + (s - u) / 2, by + (s - u) / 2
    shadow = ''.join(f'<rect x="{f(bx-g)}" y="{f(by-g+spread*.35)}" width="{f(s+2*g)}" height="{f(s+2*g)}" rx="{f(r+g)}" fill="#000" fill-opacity="{(5+j*6)/255:.3f}"/>'
                     for j in range(6) for g in [spread * (6 - j) / 6])
    plate = (f'{shadow}<rect x="{f(bx)}" y="{f(by)}" width="{f(s)}" height="{f(s)}" rx="{f(r)}" fill="#15171F" fill-opacity=".933"/>'
             f'<rect x="{f(bx+.5)}" y="{f(by+.5)}" width="{f(s-1)}" height="{f(s-1)}" rx="{f(r)}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="{f(max(1, s*.02))}"/>')
    x1, y1, x2, y2 = gx + .13 * u, gy + .08 * u, gx + .87 * u, gy + .92 * u
    sl = f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}'
    defs = (f'<mask id="n{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="999" height="999"><rect width="999" height="999" fill="#fff"/>'
            f'<path d="{sl}" stroke="#000" stroke-width="{f(.19*u)}" stroke-linecap="round"/></mask>')
    muted = (f'<g mask="url(#n{uid})">{mic(gx+.05*u, gy+.05*u, u, "#101218", ".35")}{mic(gx, gy, u, "#F2F3F7")}</g>'
             f'<path d="{sl}" stroke="{RED}" stroke-width="{f(.10*u)}" stroke-linecap="round"/>')
    live = mic(gx + .05 * u, gy + .05 * u, u, '#101218', '.35') + mic(gx, gy, u, GREEN)
    return defs, plate, muted, live


def card(name, accent, line, stats, screen, css, alt):
    stat = '<tspan dx="9"> </tspan>'.join(
        f'<tspan fill="#F2F3F7" font-weight="600">{v}</tspan><tspan fill="#8B93A5"> {k}</tspan>' for v, k in stats)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240" width="200" height="240" role="img" font-family="{FONT}">
<title>{alt}</title>
<style>
{css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect x=".5" y=".5" width="199" height="239" rx="16" fill="#15171F" stroke="#2A2F3B"/>
<clipPath id="scr"><rect x="8" y="8" width="184" height="116" rx="10"/></clipPath>
<g clip-path="url(#scr)"><rect x="8" y="8" width="184" height="116" fill="#0D0F14"/>{screen}</g>
<rect x="8.5" y="8.5" width="183" height="115" rx="9.5" fill="none" stroke="#fff" stroke-opacity=".06"/>
<rect x="18" y="143" width="8" height="8" rx="2" fill="{accent}"/>
<text x="33" y="151.5" font-size="15" font-weight="600" fill="#F2F3F7">{name}</text>
<text x="18" y="174" font-size="11.5" fill="#A3AAB8">{line}</text>
<text x="18" y="200" font-size="11">{stat}</text>
<text x="18" y="224" font-size="10.5" fill="#6B7385">Open on GitHub</text>
<path d="M174 220.5h8m-3-3 3 3-3 3" stroke="#6B7385" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


# ---------------------------------------------------------------- MicMute
def card_micmute():
    T = 9000                                    # one loop; MicMute's real timings inside it
    p = lambda ms: f'{ms / T * 100:.2f}%'
    defs, plate, muted, live = badge(130, 20, 44, 'm')
    bars = ''.join(f'<rect class="bar b{i}" x="{22 + i * 7}" y="96" width="4" height="18" rx="2" fill="{GREEN}"/>' for i in range(5))
    screen = f'''<defs>{defs}</defs>
<g class="voice">{bars}</g><rect class="flat" x="22" y="104" width="32" height="2" rx="1" fill="#4A5060"/>
<g class="key"><rect x="62" y="96" width="26" height="20" rx="5" fill="#1E2129" stroke="#6B7385"/><rect class="cap" x="62" y="96" width="26" height="17" rx="5" fill="#2A2E39"/><text x="75" y="108.5" font-size="9" font-weight="700" fill="#F2F3F7" text-anchor="middle" class="cap">F8</text></g>
<g class="all"><g class="plate">{plate}</g><g class="m">{muted}</g><g class="l">{live}</g></g>'''
    css = f'''.all{{animation:all {T}ms infinite}}
@keyframes all{{0%{{opacity:0;transform:translateY(-9px)}}{p(180)}{{opacity:1;transform:none}}{p(6180)}{{opacity:1}}{p(6580)}{{opacity:.702}}{p(7200)}{{opacity:.702}}{p(7210)}{{opacity:1}}{p(7520)}{{opacity:1;transform:none}}{p(7940)}{{opacity:0;transform:translateY(-9px)}}100%{{opacity:0}}}}
.plate{{animation:plate {T}ms infinite}}
@keyframes plate{{0%,{p(3180)}{{opacity:1}}{p(3780)}{{opacity:0}}{p(7199)}{{opacity:0}}{p(7200)},100%{{opacity:1}}}}
.m{{animation:m {T}ms steps(1,end) infinite}}@keyframes m{{0%{{opacity:1}}{p(7200)},100%{{opacity:0}}}}
.l{{opacity:0;animation:l {T}ms steps(1,end) infinite}}@keyframes l{{0%{{opacity:0}}{p(7200)},100%{{opacity:1}}}}
.voice{{animation:voice {T}ms steps(1,end) infinite}}@keyframes voice{{0%{{opacity:0}}{p(8000)},100%{{opacity:1}}}}
.flat{{animation:flat {T}ms steps(1,end) infinite}}@keyframes flat{{0%{{opacity:1}}{p(8000)},100%{{opacity:0}}}}
.bar{{transform-box:fill-box;transform-origin:50% 50%;animation:talk .5s ease-in-out infinite alternate}}
.b1{{animation-delay:-.2s}}.b2{{animation-delay:-.35s}}.b3{{animation-delay:-.1s}}.b4{{animation-delay:-.42s}}
@keyframes talk{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}
.cap{{animation:cap {T}ms infinite}}
@keyframes cap{{0%{{transform:translateY(2px)}}{p(250)}{{transform:none}}{p(7150)}{{transform:none}}{p(7200)}{{transform:translateY(2px)}}{p(7450)},100%{{transform:none}}}}'''
    return card('MicMute', RED, 'One key mutes your mic.', [('159', 'KB'), ('<!-- dl:MicMute -->263<!-- /dl -->', 'downloads')],
                screen, css, 'MicMute: press F8, the mute badge appears, melts away, and the voice meter goes flat. 159 KB.')


# ---------------------------------------------------------------- Instant Replay Fix
def card_irfix():
    T = 7000
    x0, w = 20, 160
    cut = .38
    xs = ''.join(f'<g class="x x{i}" transform="translate({f(x0 + (i + .5) * w * cut / 3)} 53)"><path d="M-4 -4L4 4M4 -4L-4 4" stroke="#10131A" stroke-width="3.5" stroke-linecap="round"/><path d="M-4 -4L4 4M4 -4L-4 4" stroke="#F2F3F7" stroke-width="1.6" stroke-linecap="round"/></g>' for i in range(3))
    screen = f'''<g class="win" transform="translate(0 -4)"><rect x="78" y="14" width="44" height="26" rx="4" fill="#1E2129" stroke="#2E3340"/><rect x="78" y="14" width="44" height="7" rx="3" fill="#2A2E39"/>
<path d="M95 34.5a2.6 1.9-25 1 1 0-.1zM104 32.5a2.6 1.9-25 1 1 0-.1z" fill="#F2F3F7"/><path d="M96.6 34V25.4l9 -2V32" stroke="#F2F3F7" stroke-width="1.4" fill="none"/></g>
<text x="{x0}" y="69" font-size="8.5" font-weight="600" fill="#C9CED7">NVIDIA alone</text>
<rect x="{x0}" y="50" width="{w}" height="6" rx="3" fill="#1B1F29"/>
<rect class="g1" x="{x0}" y="50" width="{w * cut}" height="6" rx="3" fill="{NV}"/>
<rect class="r1" x="{x0}" y="50" width="{w * cut}" height="6" rx="3" fill="{RED}"/>
<line class="dash" x1="{x0 + w * cut + 3}" y1="53" x2="{x0 + w}" y2="53" stroke="#7D8390" stroke-width="1.2" stroke-dasharray="2 3"/>
{xs}
<text class="lost" x="{x0 + w * cut + 8}" y="69" font-size="8.5" font-weight="700" fill="{RED}">Replay lost</text>
<text x="{x0}" y="107" font-size="8.5" font-weight="600" fill="#C9CED7">With the fix</text>
<rect x="{x0}" y="88" width="{w}" height="6" rx="3" fill="#1B1F29"/>
<rect class="g2" x="{x0}" y="88" width="{w}" height="6" rx="3" fill="{NV}"/>
<text class="kept" x="{x0 + w * cut + 8}" y="107" font-size="8.5" font-weight="700" fill="{NV}">Still recording</text>'''
    css = f'''.g1{{transform-box:fill-box;transform-origin:0 50%;animation:g1 {T}ms linear infinite}}
@keyframes g1{{0%{{transform:scaleX(0)}}38%,100%{{transform:scaleX(1)}}}}
.g2{{transform-box:fill-box;transform-origin:0 50%;animation:g2 {T}ms linear infinite}}
@keyframes g2{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}
.r1{{opacity:0;transform-box:fill-box;transform-origin:100% 50%;animation:r1 {T}ms infinite}}
@keyframes r1{{0%,38.5%{{opacity:1;transform:scaleX(0)}}44%,94%{{opacity:1;transform:scaleX(1)}}97%,100%{{opacity:0;transform:scaleX(1)}}}}
.dash{{opacity:0;animation:dash {T}ms infinite}}@keyframes dash{{0%,39%{{opacity:0}}42%,94%{{opacity:1}}97%,100%{{opacity:0}}}}
.x{{opacity:0}}.x0{{animation:x {T}ms infinite}}.x1{{animation:x {T}ms -.1s infinite}}.x2{{animation:x {T}ms -.2s infinite}}
@keyframes x{{0%,46%{{opacity:0}}49%,94%{{opacity:1}}97%,100%{{opacity:0}}}}
.lost,.kept{{opacity:0;animation:lost {T}ms infinite}}@keyframes lost{{0%,42%{{opacity:0}}46%,94%{{opacity:1}}97%,100%{{opacity:0}}}}
.win{{opacity:0;transform-box:fill-box;transform-origin:50% 0;animation:win {T}ms infinite}}
@keyframes win{{0%,35%{{opacity:0;transform:translateY(-6px)}}39%,94%{{opacity:1;transform:none}}97%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.r1,.dash,.x,.lost,.kept,.win{{opacity:1}}}}'''
    return card('Instant Replay Fix', NV, 'Keeps NVIDIA Instant Replay on.',
                [('234', 'KB'), ('<!-- dl:Nvidia_Instant_Replay_Fix -->170<!-- /dl -->', 'downloads')],
                screen, css, 'Instant Replay Fix: when a protected app opens, NVIDIA alone throws the whole replay away; with the fix it keeps recording. 234 KB.')


# ---------------------------------------------------------------- Look20
def card_look20():
    T = 8000
    A, B = (14, 26, 108, 64), (128, 14, 52, 92)          # a 120 DPI landscape beside a 96 DPI portrait
    sa, sb = .44, .352                                     # 1.25x apart, like the real pair
    aw, ah, bw, bh = 160 * sa, 58 * sa, 160 * sb, 58 * sb
    cy = (max(A[1], B[1]) + min(A[1] + A[3], B[1] + B[3])) / 2
    ra, rb = A[0] + A[2] - 3 - aw, B[0] + 3
    lid = lambda s: f'<rect class="lid" x="{f(10*s)}" y="{f(13*s)}" width="{f(33*s)}" height="{f(30*s)}" fill="#1E2334"/>'
    drain = lambda s: f'<rect class="drain" x="{f(50*s)}" y="{f(37*s)}" width="{f(100*s)}" height="{f(4*s)}" fill="#30374E"/>'
    screen = f'''<rect x="{A[0]-2}" y="{A[1]-2}" width="{A[2]+4}" height="{A[3]+4}" rx="3" fill="#1B1F29"/><rect x="{A[0]}" y="{A[1]}" width="{A[2]}" height="{A[3]}" fill="#10131A"/>
<rect x="{B[0]-2}" y="{B[1]-2}" width="{B[2]+4}" height="{B[3]+4}" rx="3" fill="#1B1F29"/><rect x="{B[0]}" y="{B[1]}" width="{B[2]}" height="{B[3]}" fill="#10131A"/>
<clipPath id="ca"><rect x="{A[0]}" y="{A[1]}" width="{A[2]}" height="{A[3]}"/></clipPath><clipPath id="cb"><rect x="{B[0]}" y="{B[1]}" width="{B[2]}" height="{B[3]}"/></clipPath>
<g clip-path="url(#ca)"><g class="sa"><g transform="translate({f(ra)} {f(cy - ah/2)})"><image width="{f(aw)}" height="{f(ah)}" href="{BUBBLE}" style="image-rendering:pixelated"/>{lid(sa)}{drain(sa)}</g></g></g>
<g clip-path="url(#cb)"><g class="sb"><g transform="translate({f(rb)} {f(cy - bh/2)})"><image width="{f(bw)}" height="{f(bh)}" href="{BUBBLE}" style="image-rendering:pixelated"/>{lid(sb)}{drain(sb)}</g></g></g>
<text x="{A[0]+A[2]}" y="102" font-size="7.5" fill="#7A8296" text-anchor="end">120 DPI</text><text x="{B[0]}" y="118" font-size="7.5" fill="#7A8296">96 DPI</text>'''
    css = f'''.sa{{animation:sa {T}ms infinite}}.sb{{animation:sb {T}ms infinite}}
@keyframes sa{{0%,8%{{transform:translateX({f(aw+3)}px)}}13.25%,75%{{transform:none;animation-timing-function:cubic-bezier(.333,1,.667,1)}}80.25%,100%{{transform:translateX({f(aw+3)}px)}}}}
@keyframes sb{{0%,8%{{transform:translateX(-{f(bw+3)}px)}}13.25%,75%{{transform:none}}80.25%,100%{{transform:translateX(-{f(bw+3)}px)}}}}
.drain{{transform-box:fill-box;transform-origin:100% 50%;animation:drain {T}ms infinite}}
@keyframes drain{{0%,13.25%{{transform:scaleX(0)}}75%,100%{{transform:scaleX(1)}}}}
.lid{{transform-box:fill-box;transform-origin:50% 50%;transform:scaleY(0);animation:blink 3s infinite}}
@keyframes blink{{0%,92%,100%{{transform:scaleY(0)}}95%{{transform:scaleY(1)}}}}
@media (prefers-reduced-motion:reduce){{.sa,.sb{{transform:none}}}}'''
    return card('Look20', BLUE, 'Look away, every 20 minutes.', [('172', 'KB'), ('Every', 'monitor')],
                screen, css, 'Look20: a pixel-art eye bubble slides out from behind the seam on two monitors and counts down. 172 KB.')


# ---------------------------------------------------------------- ytr-music
def card_ytr():
    T = 7000
    S = .31                                              # miniplayer.cpp: idle 44x160, expanded 340x224
    ew, eh = 340 * S, 224 * S
    rx, by = 192 - 6, 124 - 14                           # bottom-right corner, above the taskbar
    x, y = rx - ew, by - eh
    sx, sy = 44 / 340, 160 / 224
    screen = f'''<rect x="8" y="112" width="184" height="12" fill="#1B1F29"/>
{''.join(f'<rect x="{78 + i * 10}" y="114.5" width="7" height="7" rx="1.5" fill="{"#3A3F4C" if i == 2 else "#2A2E39"}"/>' for i in range(5))}
<g class="mp"><rect x="{f(x)}" y="{f(y)}" width="{f(ew)}" height="{f(eh)}" rx="{f(14*S)}" fill="#1A1416" stroke="#fff" stroke-opacity=".12"/>
<rect x="{f(x)}" y="{f(y)}" width="{f(ew)}" height="{f(eh)}" rx="{f(14*S)}" fill="{ORANGE}" fill-opacity=".09"/></g>
<g class="dock"><circle cx="{f(rx - 22*S)}" cy="{f(by - eh*sy + 26*S)}" r="{f(16*S)}" fill="{ORANGE}"/>{''.join(f'<circle cx="{f(rx - 22*S)}" cy="{f(by - eh*sy + (70 + i*28)*S)}" r="{f(5*S)}" fill="#C9CED7"/>' for i in range(3))}</g>
<g class="full"><rect x="{f(x+18*S)}" y="{f(y+18*S)}" width="{f(68*S)}" height="{f(68*S)}" rx="3" fill="{ORANGE}"/><circle cx="{f(x+52*S)}" cy="{f(y+52*S)}" r="{f(19*S)}" fill="#0D0F14" fill-opacity=".55"/>
<rect x="{f(x+100*S)}" y="{f(y+28*S)}" width="{f(150*S)}" height="{f(10*S)}" rx="{f(5*S)}" fill="#F2F3F7"/><rect x="{f(x+100*S)}" y="{f(y+48*S)}" width="{f(100*S)}" height="{f(8*S)}" rx="{f(4*S)}" fill="#7A8296"/>
<rect x="{f(x+20*S)}" y="{f(y+120*S)}" width="{f(300*S)}" height="1.4" rx=".7" fill="#fff" fill-opacity=".15"/><rect class="seek" x="{f(x+20*S)}" y="{f(y+120*S)}" width="{f(300*S)}" height="1.4" rx=".7" fill="{ORANGE}"/>
<path d="M{f(x+ew/2-2.5)} {f(y+172*S-3.5)}l6 3.5-6 3.5z" fill="#F2F3F7"/><path d="M{f(x+ew/2-14)} {f(y+172*S-2.5)}l-3.5 2.5 3.5 2.5zM{f(x+ew/2+14)} {f(y+172*S-2.5)}l3.5 2.5-3.5 2.5z" fill="#F2F3F7"/></g>
<path class="ptr" d="M0 0v11l3-3 2.2 4.6 1.6-.8L4.6 7.3H8.6z" fill="#F2F3F7" stroke="#10131A" stroke-width=".8"/>'''
    css = f'''.mp{{transform-box:view-box;transform-origin:{rx}px {by}px;animation:mp {T}ms infinite}}
@keyframes mp{{0%,18%{{transform:scale({sx:.3f},{sy:.3f})}}26%,78%{{transform:none;animation-timing-function:cubic-bezier(.2,.9,.25,1)}}86%,100%{{transform:scale({sx:.3f},{sy:.3f})}}}}
.mp{{animation-timing-function:cubic-bezier(.2,.9,.25,1)}}
.dock{{animation:dock {T}ms infinite}}@keyframes dock{{0%,18%{{opacity:1}}21%,82%{{opacity:0}}86%,100%{{opacity:1}}}}
.full{{opacity:0;animation:full {T}ms infinite}}@keyframes full{{0%,23%{{opacity:0}}27%,76%{{opacity:1}}80%,100%{{opacity:0}}}}
.seek{{transform-box:fill-box;transform-origin:0 50%;animation:seek {T}ms linear infinite}}@keyframes seek{{0%,26%{{transform:scaleX(.18)}}78%,100%{{transform:scaleX(.72)}}}}
.ptr{{animation:ptr {T}ms infinite}}
@keyframes ptr{{0%{{transform:translate(200px,70px)}}16%{{transform:translate({f(rx-12)}px,{f(by-40)}px)}}78%{{transform:translate({f(rx-40)}px,{f(by-38)}px)}}92%,100%{{transform:translate(200px,70px)}}}}
@media (prefers-reduced-motion:reduce){{.full{{opacity:1}}.dock,.ptr{{opacity:0}}.mp{{transform:none}}}}'''
    return card('ytr-music', ORANGE, 'YouTube Music for Windows.', [('<!-- kb:ytr-music -->684<!-- /kb -->', 'KB'), ('C++', '')],
                screen, css, 'ytr-music: the native miniplayer docked above the taskbar expands into a player card on hover. Built on pear-desktop.')


# ---------------------------------------------------------------- header
def header():
    T = 7000
    cards = [('m', RED), ('i', NV), ('l', BLUE), ('y', ORANGE)]
    rest = [(0, 0, 0), (-5, 4, -6), (6, 5, 5), (-1, 9, -2)]
    deal = [-123, -41, 41, 123]
    icons = {
        'm': mic(-11, -22, 22, '#F2F3F7') + f'<path d="M-8.1 -20.2L8.1 -2.7" stroke="{RED}" stroke-width="2.2" stroke-linecap="round"/>',
        'i': f'<rect x="-16" y="-17" width="32" height="4" rx="2" fill="{NV}"/><rect x="-16" y="-8" width="14" height="4" rx="2" fill="{RED}"/><path d="M-10 -9l4 3m0 -3l-4 3" stroke="#fff" stroke-width="1.2"/>',
        'l': f'<ellipse cx="0" cy="-11" rx="13" ry="10" fill="#E8EEF8"/><circle cx="1" cy="-11" r="7.5" fill="#603E1A"/><circle cx="1" cy="-11" r="5.8" fill="#96642C"/><circle cx="1" cy="-11" r="3.2" fill="#121622"/>',
        'y': f'<circle cx="0" cy="-11" r="13" fill="{ORANGE}"/><path d="M-4 -17.5v13l10.5 -6.5z" fill="#fff"/>',
    }
    g, css = [], []
    for i, (k, acc) in reversed(list(enumerate(cards))):
        x, y, r = rest[i]
        g.append(f'<g class="c c{i}"><rect x="-37" y="-48" width="74" height="96" rx="10" fill="#1B1E27" stroke="#2E3340"/>'
                 f'<rect x="-31" y="-42" width="62" height="46" rx="6" fill="#0D0F14"/>{icons[k]}'
                 f'<rect x="-29" y="14" width="6" height="6" rx="1.5" fill="{acc}"/><rect x="-19" y="15" width="40" height="4" rx="2" fill="#C9CED7"/>'
                 f'<rect x="-29" y="26" width="50" height="3" rx="1.5" fill="#4A5060"/><rect x="-29" y="34" width="32" height="3" rx="1.5" fill="#4A5060"/></g>')
        css.append(f'.c{i}{{transform:translate({x}px,{y}px) rotate({r}deg);animation:d{i} {T}ms cubic-bezier(.2,.9,.25,1) infinite;animation-delay:{i*60}ms}}'
                   f'@keyframes d{i}{{0%,14%{{transform:translate({x}px,{y}px) rotate({r}deg)}}30%,74%{{transform:translate({deal[i]}px,0) rotate(0deg)}}90%,100%{{transform:translate({x}px,{y}px) rotate({r}deg)}}}}')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 846 210" width="846" height="210" role="img" font-family="{FONT}">
<title>iAlturki. Small native Windows software, in C and C++. Open to software engineering roles.</title>
<style>
.name{{clip-path:inset(0 100% 0 0);animation:wipe 900ms cubic-bezier(.333,1,.667,1) 150ms forwards}}
@keyframes wipe{{to{{clip-path:inset(0 0 0 0)}}}}
.sub{{opacity:0;animation:up 600ms cubic-bezier(.333,1,.667,1) 500ms forwards}}.chip{{opacity:0;animation:up 600ms cubic-bezier(.333,1,.667,1) 700ms forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
{''.join(css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.name{{clip-path:none}}.sub,.chip{{opacity:1}}{''.join(f'.c{i}{{transform:translate({deal[i]}px,0)}}' for i in range(4))}}}
</style>
<defs><pattern id="dither" width="180" height="180" patternUnits="userSpaceOnUse"><image width="180" height="180" href="{DITHER}" style="image-rendering:pixelated"/></pattern>
<clipPath id="frame"><rect width="846" height="210" rx="18"/></clipPath></defs>
<g clip-path="url(#frame)">
<rect width="846" height="210" fill="#0D0F14"/>
<rect y="196" width="846" height="14" fill="url(#dither)"/>
<text class="name" x="36" y="96" font-size="66" font-weight="600" letter-spacing="-1.6" fill="#F2F3F7">iAlturki</text>
<text class="sub" x="38" y="130" font-size="17" fill="#A3AAB8">Small native Windows software, in C and C++.</text>
<g class="chip"><rect x="36" y="146" width="238" height="28" rx="14" fill="#15171F" stroke="#2A2F3B"/><circle cx="52" cy="160" r="4" fill="{GREEN}"/>
<text x="63" y="164.5" font-size="12.5" fill="#C9CED7">Open to software engineering roles</text></g>
<g transform="translate(642 98)">{''.join(g)}</g>
</g>
<rect x=".5" y=".5" width="845" height="209" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".07"/>
</svg>'''


def pill(text, fill, ink, stroke=None, w=150):
    st = f' stroke="{stroke}"' if stroke else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" role="img" font-family="{FONT}">
<title>{text}</title><rect x=".5" y=".5" width="{w-1}" height="39" rx="19.5" fill="{fill}"{st}/>
<text x="{w/2}" y="25" font-size="14.5" font-weight="600" fill="{ink}" text-anchor="middle">{text}</text></svg>'''


files = {
    'header.svg': header(),
    'card-micmute.svg': card_micmute(),
    'card-irfix.svg': card_irfix(),
    'card-look20.svg': card_look20(),
    'card-ytr.svg': card_ytr(),
    'btn-hire.svg': pill('Hire me', GREEN, '#0D0F14'),
    'btn-site.svg': pill('444005129.xyz', 'none', '#8B93A5', '#8B93A5', 160),
}
for name, svg in files.items():
    (OUT / name).write_text(svg, encoding='utf-8', newline='\n')
    print(f'{name:18} {len(svg.encode()):>6} bytes')
