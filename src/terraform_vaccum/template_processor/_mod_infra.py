from . import TemplateProcessor, KW_CHILDREN, KW_DIRECTORY
from ._module_processor import process_children, with_corrected_input
from ..renderers import TInfraRenderer


@with_corrected_input
def process(data, params, template_processor: TemplateProcessor) -> TInfraRenderer:
    r = TInfraRenderer()
    if KW_DIRECTORY in params:
        r.set_directory(params[KW_DIRECTORY])
    if KW_CHILDREN in params:
        r.add(process_children(data, params[KW_CHILDREN], template_processor))
    return r
