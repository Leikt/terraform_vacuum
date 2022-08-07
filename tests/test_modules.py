import unittest

from src.terraform_vaccum.template_processor._Module import Module


class TestModule(unittest.TestCase):
    def test_dummy(self):
        m = Module({}, {}, {})
        print(m.run().render())