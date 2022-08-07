import unittest

from src.terraform_vaccum.template_processor._ExpressionParser import ExpressionParser

DATA = {
    'id': 'i-8172NOIJ1LNOLK',
    'tags': [
        {
            'key': 'Name',
            'value': 'myvm1212'
        },
        {
            'key': 'Patch Group',
            'value': 'lindev'
        }
    ]
}

VARIABLES = {
    'id': '63e2fs1f65se130dfs',
    'value1': '12',
    'value2': 'the name of the killer is...',
    'value3': {
        'value4': 3
    }
}


class TestExpressionParsing(unittest.TestCase):
    def test_basic_json_path(self):
        parser = ExpressionParser(DATA, {})
        self.assertEqual(parser.parse('not_an_json_path'), 'not_an_json_path')
        self.assertEqual(parser.parse('$.id'), DATA['id'])
        self.assertEqual(parser.parse('$.tags[?(@.key == "Name")].value'), DATA['tags'][0]['value'])
        with self.assertRaises(KeyError) as ke:
            parser.parse('$.not_found')

    def test_nested_json_path(self):
        parser = ExpressionParser(DATA, {})
        self.assertEqual(parser.parse('not_an_json_path'), 'not_an_json_path')
        self.assertEqual(parser.parse('{{ $.id }}'), DATA['id'])
        self.assertEqual(parser.parse('/somedir/{{ $.id }}'), '/somedir/' + DATA['id'])
        self.assertEqual(parser.parse('/somedire/{{ $.tags[?(@.key == "Name")].value }}.{{ $.id }}.tf'),
                         '/somedire/{}.{}.tf'.format(DATA['tags'][0]['value'], DATA['id']))
        with self.assertRaises(KeyError) as ke:
            parser.parse('/{{ $.not_found }}/{{ $.tags[?(@.key == "Name")].value }}.{{ $.id }}.tf')
        with self.assertRaises(ValueError) as ke:
            parser.parse('{{ $.tags }}')

    def test_variable(self):
        parser = ExpressionParser(DATA, VARIABLES)
        self.assertEqual(parser.parse('not_an_json_path'), 'not_an_json_path')
        self.assertEqual(parser.parse('{{ $.id }}'), DATA['id'])
        self.assertEqual(parser.parse('{{ ~.id }}'), VARIABLES['id'])
        self.assertEqual(parser.parse('{{ ~.value3.value4 }}'), str(VARIABLES['value3']['value4']))


if __name__ == '__main__':
    unittest.main()
