from ._Template import Template
from ._keywords import *


def register_modules():
    from ._ModuleManager import ModuleManager
    from ._Modules import MTest, MInfrastructure, MModule, MProperty, MSection, MHeader, MLoop, MSource, MComment, \
        MBlankLines
    ModuleManager.register('_dummy', MTest)
    ModuleManager.register(KW_INFRA, MInfrastructure)
    ModuleManager.register(KW_MODULE, MModule)
    ModuleManager.register(KW_SECTION, MSection)
    ModuleManager.register(KW_HEADER, MHeader)
    ModuleManager.register(KW_PROPERTY, MProperty)
    ModuleManager.register(KW_LOOP, MLoop)
    ModuleManager.register(KW_SOURCE, MSource)
    ModuleManager.register(KW_COMMENT, MComment)
    ModuleManager.register(KW_BLANK_LINES, MBlankLines)


def clear_modules():
    from ._ModuleManager import ModuleManager
    ModuleManager.clear_modules()
