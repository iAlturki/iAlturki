"""Compile the real iAlturki application logos for the profile's small UI slots.
Copyright 2026 iAlturki. CC BY-NC-SA 4.0.
Pass a directory containing the four public project checkouts.
"""
import argparse
from io import BytesIO
from pathlib import Path
from PIL import Image
import resvg_py

parser = argparse.ArgumentParser()
parser.add_argument('checkouts', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = root / 'assets/logos'
out.mkdir(exist_ok=True)
sources = {
    'micmute': 'MicMute/assets/logo.png',
    'instant-replay': 'Nvidia_Instant_Replay_Fix/assets/logo.png',
    'ytr-music': 'ytr-music/assets/logo.png',
}
for name, file in sources.items():
    with Image.open(args.checkouts / file) as im:
        im.convert('RGBA').resize((40, 40), Image.Resampling.LANCZOS).save(out / f'{name}.png', optimize=True)
(out / 'look20.svg').write_bytes((args.checkouts / 'Look20/assets/logo.svg').read_bytes())
Image.open(BytesIO(resvg_py.svg_to_bytes(svg_path=str(out / 'look20.svg'), width=40, height=40))).save(out / 'look20.png', optimize=True)
