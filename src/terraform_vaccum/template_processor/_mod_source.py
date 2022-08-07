import os

import yaml

from . import TemplateProcessor, KW_LOOP, KW_LOOP_ITERATOR, KW_LOOP_TEMPLATE, KW_FILENAME, KW_SOURCE
from ._module_processor import with_corrected_input, process_expression, process_children
from ..renderers import TRenderer


@with_corrected_input
def process(data, parameters, template_processor: TemplateProcessor) -> list[TRenderer]:
    if KW_FILENAME not in parameters:
        raise KeyError('Module "{}" needs the property "{}" to be set.'.format(KW_SOURCE, KW_FILENAME))
    filename = parameters[KW_FILENAME]
    if not os.path.exists(filename):
        raise FileNotFoundError('Unable to load the template "{}".'.format(filename))
    with open(filename, 'r') as file:
        template = yaml.safe_load(file)

    results = []
    if isinstance(template, dict):
        for keyword, params in template.items():
            results.append(template_processor.process(keyword, params, data))
    elif isinstance(template, list):
        for item in template:
            keyword, params = tuple(item.items())[0]
            results.append(template_processor.process(keyword, params, data))
    return results

