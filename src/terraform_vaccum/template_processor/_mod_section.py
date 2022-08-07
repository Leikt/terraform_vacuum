from . import TemplateProcessor, KW_HEADER, KW_CHILDREN, KW_SECTION
from ._module_processor import with_corrected_input, process_children
from ..renderers import TSectionRenderer


@with_corrected_input
def process(data, params, template_processor: TemplateProcessor) -> TSectionRenderer:
    r = TSectionRenderer()
    if KW_HEADER in params:
        r.set_header(template_processor.process(KW_HEADER, params[KW_HEADER], data))
    else:
        raise KeyError('The module "{}" requires a "{}" module inside.'.format(KW_SECTION, KW_HEADER))
    if KW_CHILDREN in params:
        r.add(process_children(data, params[KW_CHILDREN], template_processor))
    return r
