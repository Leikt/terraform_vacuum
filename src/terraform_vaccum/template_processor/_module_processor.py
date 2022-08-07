import re

from . import TemplateProcessor
from ._keywords import KW_INPUT
from jsonpath_ng.ext import parse as jpaparse

REGEX_NESTED_EXPRESSION = r"\{\{ (.*?) \}\}"

def _correct_input(data, parameters) -> any:
    if KW_INPUT not in parameters:
        return data
    if not isinstance(parameters[KW_INPUT], str):
        raise TypeError('"{}" parameter must be a string.'.format(KW_INPUT))
    if not parameters[KW_INPUT].startswith('$'):
        return data

    match = jpaparse(parameters[KW_INPUT]).find(data)
    if len(match) == 0:
        raise ValueError('No data found using the JsonPath "{}"'.format(parameters[KW_INPUT]))
    return match[0].value


def with_corrected_input(func):
    def wrapper(data, parameters, *args, **kwargs):
        data = _correct_input(data, parameters)
        return func(data, parameters, *args, *kwargs)

    return wrapper


def process_children(data, children: list, template_processor: TemplateProcessor):
    result = []
    for child in children:
        keyword, parameters = tuple(child.items())[0]
        result.append(template_processor.process(keyword, parameters, data))
    return result


def process_nested_expressions(data, expression: str) -> str:
    nested_expressions = re.findall(REGEX_NESTED_EXPRESSION, expression)
    result = expression
    for ne in nested_expressions:
        processed_expr = process_expression(data, ne)
        if not isinstance(processed_expr, str):
            raise TypeError('Nested expression must return a simple string. "{}" does not.'.format(ne))
        result = result.replace("{{ " + ne + " }}", processed_expr)
    return result


def process_expression(data, expression: str) -> any:
    nested_expression = re.search(REGEX_NESTED_EXPRESSION, expression)
    if nested_expression:
        return process_nested_expressions(data, expression)
    if not expression.startswith('$'):
        return expression

    match = jpaparse(expression).find(data)
    if len(match) == 0:
        raise KeyError('No match found for {}'.format(expression))
    return match[0].value
