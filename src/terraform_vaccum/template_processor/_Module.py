from ._ExpressionParser import ExpressionParser
from ._keywords import *
from ..renderers import TRenderer
from ._ModuleManager import ModuleManager


class Module:
    def __init__(self, data, variables, parameters):
        self._data = data
        self._variables = variables
        self._parameters = parameters
        self._expression_parser = ExpressionParser(data, variables)

    def run(self) -> TRenderer:
        inputs = self.p_value(KW_INPUT, required=False)
        if inputs:
            self._data = inputs
            self._expression_parser.set_data(inputs)
        return self._run()

    def _run(self):
        raise NotImplemented()

    def check_tags(self, expression: str) -> bool:
        if KW_TAGS not in self._parameters:
            return True
        tags = self._parameters[KW_TAGS]
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]

        if expression == '*':
            return True
        valid_tags = [tag.strip() for tag in expression.split(',')]
        for tag in valid_tags:
            if tag in tags:
                return True
        return False

    def _expr(self, expression: str) -> any:
        return self._expression_parser.parse(expression)

    def p_value(self, key: str, evaluate: bool = True, required: bool = True, default: str = None) -> any:
        if key not in self._parameters:
            if required:
                raise KeyError('Missing key "{}" in module parameters.'.format(key))
            return default
        value = self._parameters[key]
        if evaluate and isinstance(value, str):
            return self._expr(value)
        return value

    def p_raw(self, value: str, evaluate: bool = True):
        if evaluate:
            return self._expr(value)
        return value

    def p_children(self, renderer: TRenderer, required: bool = False):
        if KW_CHILDREN not in self._parameters:
            if required:
                raise KeyError('Missing required parameters "{}".'.format(KW_CHILDREN))
            return
        children = self._parameters[KW_CHILDREN]
        if not isinstance(children, list):
            raise ValueError('Wrong type for "{}" keyword.'.format(KW_CHILDREN))
        for child in children:
            keyword, params = list(child.items())[0]
            module = ModuleManager.create(self._data, self._variables, keyword, params)
            renderer.add(module.run())

    def p_filename(self, renderer: TRenderer, required: bool = False, evaluate: bool = True):
        value = self.p_value(KW_FILENAME, required=required, evaluate=evaluate)
        renderer.__getattribute__('set_filename')(value)

    def p_directory(self, renderer: TRenderer, required: bool = False, evaluate: bool = True):
        value = self.p_value(KW_DIRECTORY, required=required, evaluate=evaluate)
        renderer.__getattribute__('set_directory')(self._parameters[KW_DIRECTORY])

    def p_sub_module(self, renderer: TRenderer, keyword: str, attribute: str, required: bool = False):
        if keyword not in self._parameters:
            if required:
                raise KeyError('Missing required parameters "{}".'.format(keyword))
            return
        sub_module = ModuleManager.create(self._data, self._variables, keyword, self._parameters[keyword])
        renderer.__getattribute__(attribute)(sub_module.run())
