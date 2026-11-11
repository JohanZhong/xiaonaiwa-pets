#!/usr/bin/env python3
"""Install verified local pet bundles without executing downloaded code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'2d': 'xiaonaiwa-2d', '3d': 'xiaonaiwa-3d'}

def install(variant, destination, force=False):
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    selected = [key for key, name in NAMES.items() if (ROOT / 'pets' / name).is_dir()] if variant == 'all' else [variant]
    if not selected:
        raise ValueError('No bundled pet editions found.')
    destination = Path(destination).expanduser().resolve()
    plans = []
    for key in selected:
        name = NAMES[key]
        source = ROOT / 'pets' / name
        target = destination / name
        if target.is_symlink():
            raise ValueError(f'Refusing symlink target: {target}')
        if target.exists() and not force:
            raise FileExistsError(f'{target} already exists. Use --force to back it up and replace it.')
        for filename in ('pet.json', 'spritesheet.webp'):
            path = source / filename
            expected = manifest['files'][f'pets/{name}/{filename}']['sha256']
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f'Checksum mismatch: {path}')
        plans.append((source, target))
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    for source, target in plans:
        temporary = Path(tempfile.mkdtemp(prefix='.xiaonaiwa-', dir=destination))
        backup = None
        try:
            for filename in ('pet.json', 'spritesheet.webp'):
                shutil.copy2(source / filename, temporary / filename)
            if target.exists():
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                backup = destination / f'{target.name}.backup-{stamp}'
                target.rename(backup)
            try:
                temporary.rename(target)
            except Exception:
                if backup and not target.exists():
                    backup.rename(target)
                raise
            installed.append(str(target))
        finally:
            # Only our fresh, private staging directory may be removed.
            if temporary.exists() and temporary.parent == destination and temporary.name.startswith('.xiaonaiwa-'):
                shutil.rmtree(temporary)
    return installed

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=['2d', '3d', 'all'], default='all')
    parser.add_argument('--dest', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'pets')
    parser.add_argument('--force', action='store_true', help='Back up existing folders before replacement')
    args = parser.parse_args()
    try:
        for path in install(args.variant, args.dest, args.force):
            print(f'Installed: {path}')
        print('In Codex: Settings > Pets > Custom pets > Refresh, then select a version.')
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Installation failed: {exc}\n')

if __name__ == '__main__':
    main()
