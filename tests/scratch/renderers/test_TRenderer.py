import unittest
from src.terraform_vaccum.renderers import TRenderer


class TestTRenderer(unittest.TestCase):
    def test_basic(self):
        r = TRenderer()
        res = r.render()
        self.assertEqual(res, '')


if __name__ == '__main__':
    unittest.main()
