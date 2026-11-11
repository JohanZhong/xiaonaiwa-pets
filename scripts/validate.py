#!/usr/bin/env python3
"""Validate release integrity, transparency, required cells and metadata."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]

def validate(root=ROOT):
    manifest = json.loads((root / 'manifest.json').read_text())
    for rel, info in manifest['files'].items():
        path = (root / rel).resolve()
        assert path.is_relative_to(root.resolve()), rel
        assert path.stat().st_size == info['bytes'], rel
        assert hashlib.sha256(path.read_bytes()).hexdigest() == info['sha256'], rel
    for style in ('2d', '3d'):
        name = f'xiaonaiwa-{style}'
        folder = root / 'pets' / name
        meta = json.loads((folder / 'pet.json').read_text(encoding='utf-8'))
        assert meta['id'] == name and meta['spriteVersionNumber'] == 2
        assert meta['spritesheetPath'] == 'spritesheet.webp'
        with Image.open(folder / 'spritesheet.webp') as source:
            atlas = source.convert('RGBA')
        assert atlas.size == (1536, 2288)
        for row, count in enumerate(COUNTS):
            for col in range(8):
                cell = atlas.crop((col*192, row*208, (col+1)*192, (row+1)*208))
                alpha = cell.getchannel('A')
                if col < count:
                    assert alpha.getbbox() is not None, (name, row, col)
                    assert alpha.getextrema()[0] == 0, (name, row, col, 'opaque')
                    assert not alpha.crop((0,0,192,1)).getbbox(), 'top clipping'
                    assert not alpha.crop((0,207,192,208)).getbbox(), 'bottom clipping'
                else:
                    assert alpha.getbbox() is None, (name, row, col, 'unused')
        png = Image.open(folder / 'work-spritesheet.png').convert('RGBA')
        assert png.tobytes() == atlas.tobytes(), f'{name}: WebP changed pixels'
        legacy = Image.open(folder / 'legacy-v1.png').convert('RGBA')
        assert legacy.size == (1536,1872)
        assert legacy.tobytes() == atlas.crop((0,0,1536,1872)).tobytes()
    print('PASS: checksums, metadata, 146 used cells, transparency, lossless exports and v1 crops')

if __name__ == '__main__':
    validate()
