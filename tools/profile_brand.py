"""Small, smoothly animated brand components. Copyright 2026 iAlturki.
Original layout and animation: CC BY-NC-SA 4.0; see assets/logos/NOTICE.md.
"""
import base64
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def logo(name):
    raw = (ROOT / f'assets/logos/{name}.png').read_bytes()
    return 'data:image/png;base64,' + base64.b64encode(raw).decode()


def button(kind, font):
    hire = kind == 'hire'
    color = '#3DD68C' if hire else '#609CFF'
    title = 'Hire me' if hire else '444005129.xyz'
    label = 'LET’S BUILD' if hire else 'MY SOFTWARE'
    if hire:
        source = ET.parse(ROOT / 'assets/logos/github.svg').getroot()
        path = next(e for e in source.iter() if e.tag.endswith('path')).attrib['d']
        icon = f'<g transform="translate(24 22)" fill="#F2F3F7"><path d="{path}"/></g>'
    else:
        # Exact native website favicon: the green pixel i, not an invented logo.
        icon = '<g transform="translate(23 21) scale(.8125)"><rect width="32" height="32" rx="7" fill="#15171F"/><path fill="#80FF80" d="M13 6h6v5h-6zM13 13h6v13h-6z"/></g>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 232 68" width="232" height="68" role="img" font-family="{font}">
<title>{title} — iAlturki</title>
<!-- Original button and animation © 2026 iAlturki. Icon provenance: assets/logos/NOTICE.md. -->
<style>.orbit{{transform-origin:36px 34px;animation:orbit 8s linear infinite}}.arrow{{animation:arrow 3.2s ease-in-out infinite}}@keyframes orbit{{to{{transform:rotate(360deg)}}}}@keyframes arrow{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(3px)}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<defs><linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{color}" stop-opacity=".65"/><stop offset=".5" stop-color="#2A2F3B"/><stop offset="1" stop-color="{color}" stop-opacity=".25"/></linearGradient></defs>
<rect x=".75" y=".75" width="230.5" height="66.5" rx="14" fill="#15171F" stroke="url(#edge)" stroke-width="1.5"/>
<path d="M73 11h126" stroke="{color}" stroke-opacity=".16"/>
<circle cx="36" cy="34" r="23" fill="#0D0F14" stroke="#2A2F3B"/>
<g class="orbit"><circle cx="36" cy="34" r="23" fill="none" stroke="{color}" stroke-width="1.7" stroke-dasharray="18 19 8 99" stroke-linecap="round"/><circle cx="59" cy="34" r="2.2" fill="{color}"/></g>
{icon}
<text x="72" y="24" font-size="8.5" font-weight="600" letter-spacing="1.25" fill="{color}">{label}</text>
<text x="72" y="45" font-size="{'18' if hire else '14.5'}" font-weight="600" fill="#F2F3F7">{title}</text>
<path class="arrow" d="M207 35h10m-4-4 4 4-4 4" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


def header(font, dither):
    projects = [('micmute', '#FF4750'), ('instant-replay', '#76B900'), ('look20', '#609CFF'), ('ytr-music', '#FF3D00')]
    cards = []
    for i, (name, accent) in enumerate(projects):
        x = 482 + i * 82
        cards.append(f'<g transform="translate({x} 49)"><rect width="74" height="96" rx="10" fill="#1B1E27" stroke="#2E3340"/><rect x="6" y="6" width="62" height="46" rx="6" fill="#0D0F14"/><image href="{logo(name)}" x="23" y="14" width="28" height="28"/><rect x="8" y="62" width="6" height="6" rx="1.5" fill="{accent}"/><rect x="18" y="63" width="40" height="4" rx="2" fill="#C9CED7"/><rect x="8" y="74" width="50" height="3" rx="1.5" fill="#4A5060"/><rect x="8" y="82" width="32" height="3" rx="1.5" fill="#4A5060"/></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 846 210" width="846" height="210" role="img" font-family="{font}">
<title>iAlturki. Small native Windows software, in C and C++. Open to software engineering roles.</title>
<!-- Original layout and animation © 2026 iAlturki. Authentic project logos: assets/logos/NOTICE.md. -->
<style>.logos{{animation:float 6s ease-in-out infinite}}@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}@media(prefers-reduced-motion:reduce){{.logos{{animation:none}}}}</style>
<defs><pattern id="dither" width="180" height="180" patternUnits="userSpaceOnUse"><image width="180" height="180" href="{dither}" style="image-rendering:pixelated"/></pattern><clipPath id="frame"><rect width="846" height="210" rx="18"/></clipPath></defs>
<g clip-path="url(#frame)"><rect width="846" height="210" fill="#0D0F14"/><rect y="196" width="846" height="14" fill="url(#dither)"/>
<text x="36" y="96" font-size="66" font-weight="600" letter-spacing="-1.6" fill="#F2F3F7">iAlturki</text>
<text x="38" y="130" font-size="17" fill="#A3AAB8">Small native Windows software, in C and C++.</text>
<rect x="36" y="146" width="238" height="28" rx="14" fill="#15171F" stroke="#2A2F3B"/><circle cx="52" cy="160" r="4" fill="#3DD68C"/><text x="63" y="164.5" font-size="12.5" fill="#C9CED7">Open to software engineering roles</text>
<g class="logos">{''.join(cards)}</g></g><rect x=".5" y=".5" width="845" height="209" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".07"/>
</svg>'''
