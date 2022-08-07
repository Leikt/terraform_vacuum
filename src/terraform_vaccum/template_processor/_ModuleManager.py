from __future__ import annotations


class ModuleManager:
    _registered_modules = {}

    def __init__(self):
        raise NotImplemented()

    @classmethod
    def register(cls, keyword: str, klass: callable):
        if keyword in cls._registered_modules:
            raise KeyError('Keyword "{}" is already registered.'.format(keyword))
        cls._registered_modules[keyword] = klass

    @classmethod
    def clear_modules(cls):
        cls._registered_modules.clear()

    @classmethod
    def create(cls, data, variables, keyword: str, parameters: dict):
        if keyword not in cls._registered_modules:
            raise KeyError('No module registered on keyword "{}".'.format(keyword))
        module = cls._registered_modules[keyword](data, variables, parameters)
        return module
