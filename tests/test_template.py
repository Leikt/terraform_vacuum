import unittest

from src.terraform_vaccum.template_processor import Template, register_modules, clear_modules


class TestTemplate(unittest.TestCase):
    def test_dummy(self):
        register_modules()
        t = Template()
        # t.set_template({'_dummy': {'value': 12}})
        t.load_template('tests/template_parsing/dummy.t.yml')
        t.set_data({})
        res = t.run()
        for r in res:
            print(r.render())
        clear_modules()

    def test_simple(self):
        register_modules()
        t = Template()
        t.load_template('tests/template_parsing/simple.t.yml')
        t.load_data('tests/template_parsing/simple.json')
        t.set_variables({'author': 'Robin LIORET', 'messages': {'hello': 'Hello World!'}, 'version': '0.0.1'})
        res = t.run()
        for r in res:
            r.adjust_indent()
            print(r.render())
            r.save()
        clear_modules()

    def test_realistic(self):
        register_modules()

        t = Template()
        t.load_template('tests/realistic/main.t.yml')
        t.load_data('tests/realistic/data.json')
        t.load_variables('tests/realistic/variables.yml')

        clear_modules()


if __name__ == '__main__':
    unittest.main()
