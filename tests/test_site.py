"""Basic content checks plus a minimal security smoke test."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import build


class WebsiteTests(unittest.TestCase):
    def test_build_creates_both_files(self):
        with TemporaryDirectory() as tmp:
            built = build(output_dir=tmp)
            self.assertTrue((built / 'index.html').is_file())
            self.assertTrue((built / 'styles.css').is_file())

    def test_homepage_says_hello_world(self):
        html = (ROOT / 'site' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Hello, World!', html)
        self.assertIn('<main', html)

    def test_browser_security_basics(self):
        html = (ROOT / 'site' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Content-Security-Policy', html)
        self.assertIn("default-src 'none'", html)
        self.assertNotIn('<script', html.lower())
        self.assertNotIn('http://', html.lower())


if __name__ == '__main__':
    unittest.main()
