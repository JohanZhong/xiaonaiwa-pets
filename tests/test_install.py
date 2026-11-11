import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallerTests(unittest.TestCase):
    def test_both_variants_and_existing_protection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            installed = installer.install('all', root)
            self.assertEqual(len(installed), 2)
            first = root / 'xiaonaiwa-2d/pet.json'
            original = first.read_bytes()
            with self.assertRaises(FileExistsError):
                installer.install('all', root)
            self.assertEqual(first.read_bytes(), original)
            installer.install('2d', root, True)
            backups = list(root.glob('xiaonaiwa-2d.backup-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'pet.json').read_bytes(), original)
    def test_corruption_rejected_before_destination_creation(self):
        import shutil
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / 'source'
            shutil.copytree(installer.ROOT / 'pets', source / 'pets')
            shutil.copy2(installer.ROOT / 'manifest.json', source / 'manifest.json')
            (source / 'pets/xiaonaiwa-2d/pet.json').write_text('{}')
            previous = installer.ROOT
            installer.ROOT = source
            try:
                with self.assertRaises(ValueError):
                    installer.install('2d', root / 'destination')
                self.assertFalse((root / 'destination').exists())
            finally:
                installer.ROOT = previous

if __name__ == '__main__':
    unittest.main()
