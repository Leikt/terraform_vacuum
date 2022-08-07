from . import TemplateProcessor, KW_LOOP, KW_LOOP_ITERATOR, KW_LOOP_TEMPLATE
from ._module_processor import with_corrected_input, process_expression
from ..renderers import TRenderer


@with_corrected_input
def process(data, parameters, template_processor: TemplateProcessor) -> list[TRenderer]:
    if KW_LOOP_ITERATOR not in parameters:
        raise KeyError('The module "{}" needs "{}" to be defined.'.format(KW_LOOP, KW_LOOP_ITERATOR))
    if KW_LOOP_TEMPLATE not in parameters:
        raise KeyError('The module "{}" needs "{}" to be defined.'.format(KW_LOOP, KW_LOOP_TEMPLATE))

    data = process_expression(data, parameters[KW_LOOP_ITERATOR])
    if not isinstance(data, list):
        data = [data]

    keyword, params = tuple(parameters[KW_LOOP_TEMPLATE].items())[0]
    result = []
    for element in data:
        result.append(template_processor.process(keyword, params, element))
    return result
