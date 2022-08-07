from ._template_processor import TemplateProcessor
from ._keywords import *

from ._mod_infra import process
TemplateProcessor.register_module(KW_INFRA, process)

from ._mod_file import process
TemplateProcessor.register_module(KW_FILE, process)

from ._mod_section import process
TemplateProcessor.register_module(KW_SECTION, process)

from ._mod_header import process
TemplateProcessor.register_module(KW_HEADER, process)

from ._mod_property import process
TemplateProcessor.register_module(KW_PROPERTY, process)

from ._mod_loop import process
TemplateProcessor.register_module(KW_LOOP, process)

from ._mod_source import process
TemplateProcessor.register_module(KW_SOURCE, process)