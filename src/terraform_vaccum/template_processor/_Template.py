from __future__ import annotations

import json
import yaml

from ..renderers import TRenderer
from ._ModuleManager import ModuleManager


class Template:
    def __init__(self):
        self._template: list = None
        self._data: dict = {}
        self._variables: dict = {}

    def set_template(self, template: [dict, list]) -> Template:
        if isinstance(template, dict):
            self._template = [template]
        elif isinstance(template, list):
            self._template = template
        else:
            raise TypeError('Template must be a list or dict.')
        return self

    def set_data(self, data: [dict, list]) -> Template:
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise TypeError('Data must be a list or a dict.')
        self._data = data
        return self

    def set_variables(self, variables: dict) -> Template:
        if not isinstance(variables, dict):
            raise TypeError('Variables should be stored in a dict')
        self._variables = variables
        return self

    def load_template(self, filename: str) -> Template:
        template = self._load_file(filename)
        return self.set_template(template)

    def load_data(self, filename: str):
        data = self._load_file(filename)
        return self.set_data(data)

    def load_variables(self, filename: str) -> Template:
        variables = self._load_file(filename)
        return self.set_variables(variables)

    def run(self) -> list[TRenderer]:
        if self._template is None:
            raise ValueError('Missing template.')
        renderers = []
        for module_dict in self._template:
            if not isinstance(module_dict, dict):
                raise ValueError('Module must be a dictionary.')
            keyword, parameters = list(module_dict.items())[0]
            module = ModuleManager.create(self._data, self._variables, keyword, parameters)
            renderers.append(module.run())
        return renderers

    @staticmethod
    def _load_file(filename: str) -> any:
        with open(filename, 'r') as file:
            if filename.endswith('.yml'):
                data = yaml.safe_load(file)
            elif filename.endswith('.json'):
                data = json.load(file)
            else:
                raise Exception('Wrong file extension. Only yml and json files are accepted.')
        return data
