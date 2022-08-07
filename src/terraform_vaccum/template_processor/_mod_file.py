from . import TemplateProcessor
from ._module_processor import with_corrected_input, process_children, process_expression
from ..renderers import TFileRenderer
from ._keywords import KW_FILENAME, KW_CHILDREN


@with_corrected_input
def process(data, params, template_processor: TemplateProcessor) -> TFileRenderer:
    r = TFileRenderer()
    if KW_FILENAME in params:
        filename = process_expression(data, params[KW_FILENAME])
        r.set_filename(filename)
    if KW_CHILDREN in params:
        r.add(process_children(data, params[KW_CHILDREN], template_processor))
    return r
