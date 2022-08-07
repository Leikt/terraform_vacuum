import unittest

from src.terraform_vaccum.template_processor import Template, register_modules, clear_modules


class TestTemplate(unittest.TestCase):

    def test_realistic(self):
        register_modules()

        t = Template()
        t.load_template('tests/realistic/main.t.yml')
        t.load_data('tests/realistic/data.json')
        t.load_variables('tests/realistic/variables.yml')

        for r in t.run():
            r.adjust_indent().save()

        clear_modules()


if __name__ == '__main__':
    unittest.main()
