#!/usr/bin/env python3
"""Build deterministic, verified release archives from public files only."""
from pathlib import Path
import hashlib
import zipfile
from validate import validate, ROOT

VERSION = '1.0.0'

def build():
    validate()
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    common = ['LICENSE', 'ASSET_NOTICE.md', 'CHANGELOG.md', 'manifest.json', 'scripts/install.py', 'docs/INSTALL.md']
    archives = []
    for variant in ('all', '2d', '3d'):
        variants = ['2d', '3d'] if variant == 'all' else [variant]
        paths = [ROOT / p for p in common]
        for style in variants:
            paths += sorted((ROOT / 'pets' / f'xiaonaiwa-{style}').glob('*'))
        label = 'pets' if variant == 'all' else variant
        target = out / f'xiaonaiwa-{label}-v{VERSION}.zip'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            info = zipfile.ZipInfo('README.md', (2026,11,11,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, f'# Xiaonaiwa Pets {VERSION}\n\nIncluded editions: {", ".join(variants)}.\n\nCopy the folders inside pets/ into your Codex custom pets directory, then refresh. Or run `python scripts/install.py --variant all` to install all included editions with checksum verification. Existing folders are protected by default.\n\n中文：复制 pets/ 下的宠物文件夹到自定义宠物目录，刷新后选择。安装脚本默认校验文件且拒绝覆盖已有目录。\n\n[Full documentation and previews](https://github.com/JohanZhong/xiaonaiwa-pets) · [Local installation guide](docs/INSTALL.md)\n\nUnofficial fan work; character artwork is excluded from the code license. See ASSET_NOTICE.md.\n')
            for path in sorted(paths):
                info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), (2026,11,11,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes())
        with zipfile.ZipFile(target) as archive:
            assert archive.testzip() is None
        archives.append(target)
    (out / 'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in archives), encoding='utf-8')
    print('\n'.join(f'{p.name}: {p.stat().st_size:,} bytes' for p in archives))

if __name__ == '__main__':
    build()
