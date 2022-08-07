import yaml
import json
from jsonpath_ng.ext import parse as jparse

from src.terraform_vaccum.renderers import TRenderer, TSectionRenderer, TFileRenderer, TPropertyRenderer, \
    THeaderRenderer


def process_expression(expr: str, data) -> str:
    if not expr.startswith('$'):
        return expr

    match = jparse(expr).find(data)
    if len(match) == 0:
        raise KeyError('No match found for {}'.format(expr))
    return match[0].value


def process_input(parameters: dict, data):
    if 'input' not in parameters:
        return data
    return process_expression(parameters['input'], data)


def process(key: str, parameters: dict, data) -> TRenderer:
    if key == 'section': return section(parameters, data)
    if key == 'loop': return loop(parameters, data)
    if key == 'property': return property(parameters, data)
    if key == 'header': return header(parameters, data)
    if key == 'source': return source(parameters, data)
    return False


def section(parameters: dict, data) -> TSectionRenderer:
    data = process_input(parameters, data)
    s = TSectionRenderer()
    h = header(parameters['header'], data)
    s.set_header(h)
    for child in parameters.get('children', []):
        child: dict
        name = list(child.keys())[0]
        params = list(child.values())[0]
        res = process(name, params, data)
        if not res: raise KeyError('No module...')

        s.add(res)
    return s


def header(parameters: dict, data) -> THeaderRenderer:
    data = process_input(parameters, data)
    h = THeaderRenderer(parameters.get('keyword', ''))
    for p in parameters.get('parameters', []):
        value = process_expression(p, data)
        h.add_parameter(value)
    if parameters.get('is_property', False):
        h.set_equal()
    return h


def loop(parameters: dict, data) -> list[TRenderer]:
    data = process_input(parameters, data)
    data = process_expression(parameters['through'], data)
    if not isinstance(data, list):
        data = [data]
    object_type = list(parameters['object'].keys())[0]
    object_params = list(parameters['object'].values())[0]
    res = []
    for d in data:
        res.append(process(object_type, object_params, d))
    return res


def property(parameters: dict, data) -> TPropertyRenderer:
    data = process_input(parameters, data)
    key = process_expression(parameters['key'], data)
    value = process_expression(parameters['value'], data)
    p = TPropertyRenderer(key, value)
    return p


def source(parameters: dict, data) -> TRenderer:
    data = process_input(parameters, data)
    with open(parameters['file'], 'r') as file:
        template = yaml.safe_load(file)
    final = []
    for key, value in template.items():
        res = process(key, value, data)
        if res: final.append(res)
    return final


with open('data/test.t.yml', 'r') as file:
    template: dict = yaml.safe_load(file)
with open('data/test.json', 'r') as file:
    json_data: dict = json.load(file)

tfile = TFileRenderer()
for key, value in template.items():
    res = process(key, value, json_data)
    if res is False: continue
    tfile.add(res)
print(tfile.adjust_indent().render())
tfile.set_filename('data/test.tf').save()
