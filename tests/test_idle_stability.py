import importlib.util
from pathlib import Path
import unittest
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT/'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
class BlinkRegressionTests(unittest.TestCase):
    def test_published_idle_has_stable_body(self):
        with Image.open(ROOT/'pets/xiaonaiwa-2d/work-spritesheet.png') as im:
            validator.validate_idle_stability(im.convert('RGBA'))
    def test_body_color_regression_is_rejected(self):
        with Image.open(ROOT/'pets/xiaonaiwa-2d/work-spritesheet.png') as im:
            changed=im.convert('RGBA')
        changed.putpixel((192+96,150),(250,180,30,255))
        with self.assertRaisesRegex(AssertionError,'body color'):
            validator.validate_idle_stability(changed)
