from . import TemplateProcessor, KW_KEYWORD, KW_IS_PROPERTY, KW_PARAMETERS
from ._module_processor import with_corrected_input, process_expression
from ..renderers import THeaderRenderer


@with_corrected_input
def process(data, params, _template_processor: TemplateProcessor) -> THeaderRenderer:
    keyword = params[KW_KEYWORD]
    r = THeaderRenderer(keyword)
    if KW_IS_PROPERTY in params and params[KW_IS_PROPERTY]:
        r.set_equal()
    if KW_PARAMETERS in params:
        for param in params[KW_PARAMETERS]:
            processed_param = process_expression(data, param)
            r.add_parameter(processed_param)
    return r
