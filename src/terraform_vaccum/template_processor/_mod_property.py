from . import KW_PROPERTY, KW_KEY, KW_VALUE, KW_IS_RAW
from ..renderers import TPropertyRenderer
from ._template_processor import TemplateProcessor
from ._module_processor import with_corrected_input, process_expression


@with_corrected_input
def process(data, params, _template_processor: TemplateProcessor) -> TPropertyRenderer:
    if KW_KEY not in params:
        raise KeyError('The module "{}" needs a "{}" value.'.format(KW_PROPERTY, KW_KEY))
    if KW_VALUE not in params:
        raise KeyError('The module "{}" needs a "{}" value.'.format(KW_PROPERTY, KW_VALUE))
    key = process_expression(data, params[KW_KEY])
    value = process_expression(data, params[KW_VALUE])
    r = TPropertyRenderer(key, value)
    if KW_IS_RAW in params and params[KW_IS_RAW]:
        r.set_raw()
    return r