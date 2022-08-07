import json
import logging
import os.path

import yaml

from src.terraform_vaccum.renderers import TRenderer


class TemplateProcessor:
    def __init__(self, template_file: str, data_file: str):
        if not os.path.exists(template_file):
            raise FileNotFoundError('Cannot find the file "{}"'.format(template_file))
        if not os.path.exists(data_file):
            raise FileNotFoundError('Cannot find the file "{}"'.format(data_file))

        with open(template_file, 'r') as file:
            self._template = yaml.safe_load(file)
            logging.info('Template "{}" loaded.'.format(template_file))
        with open(data_file, 'r') as file:
            self._initial_data = json.load(file)
            logging.info('Template "{}" loaded.'.format(template_file))

    _registered_module_processors: dict = {}

    @classmethod
    def register_module(cls, keyword: str, function: callable):
        if keyword in cls._registered_module_processors:
            raise KeyError('A module processor is already registered for the keyword "{}".'.format(keyword))
        cls._registered_module_processors[keyword] = function

    def process(self, keyword: str, parameters, data) -> TRenderer:
        if keyword not in self._registered_module_processors:
            raise KeyError('No module processor registered on keyword "{}"'.format(keyword))
        return self._registered_module_processors[keyword](data, parameters, self)

    def run(self) -> TRenderer:
        first_keyword, first_parameters = tuple(self._template.items())[0]
        return self.process(first_keyword, first_parameters, self._initial_data)

