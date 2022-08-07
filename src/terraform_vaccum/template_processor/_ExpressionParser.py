import re
from jsonpath_ng.ext import parse as jpaparse

_NESTED_REGEX = "\{\{ (.*?) \}\}"
_NESTED_BUILDER = lambda expr: '{{ ' + expr + ' }}'
_NESTED_TYPES = [int, bool, float, str]
_KW_VARS = '~'
_KW_JSONPATH = '$'  # DO NOT CHANGE
_VAR_KW_REGEX = "^(\\" + _KW_JSONPATH + "|" + _KW_VARS + ")"


class ExpressionParser:
    def __init__(self, data, variables):
        self._data = data
        self._variables = variables

    def set_data(self, new_data):
        self._data = new_data

    def parse(self, expression: str) -> any:
        simple = re.search(_VAR_KW_REGEX, expression)
        if simple: return self._parse_simple_expression(expression)

        nested = re.search(_NESTED_REGEX, expression)
        if nested: return self._parse_nested_expression(expression)

        return expression

    def _parse_simple_expression(self, expression: str) -> any:
        original_expression = expression
        target = self._data
        if expression.startswith(_KW_VARS):
            target = self._variables
            expression = _KW_JSONPATH + expression[1:]
        matches = jpaparse(expression).find(target)
        if len(matches) == 0:
            raise KeyError('No data or variable match the expression: "{}"'.format(original_expression))
        return matches[0].value

    def _parse_nested_expression(self, expression: str) -> any:
        def check_type(e, var) -> str:
            for t in _NESTED_TYPES:
                if isinstance(var, t):
                    return str(var)
            raise ValueError('Wrong type return for the expression "{}"'.format(e))

        var_expr = re.findall(_NESTED_REGEX, expression)
        for expr in var_expr:
            new_expr = self._parse_simple_expression(expr)
            new_expr = check_type(expr, new_expr)
            expression = expression.replace(_NESTED_BUILDER(expr), new_expr)
        return expression
