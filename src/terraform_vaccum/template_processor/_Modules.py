from . import Template
from ._Module import Module
from ._ModuleManager import ModuleManager
from ._keywords import *
from ..renderers import TRenderer, TInfraRenderer, TFileRenderer, TPropertyRenderer, TSectionRenderer, THeaderRenderer


class MTest(Module):
    def _run(self) -> TRenderer:
        r = TRenderer()
        r.add_comment('TEST MODULE')
        return r


class MInfrastructure(Module):
    def _run(self) -> TInfraRenderer:
        r = TInfraRenderer()
        self.p_directory(r)
        self.p_children(r)
        return r


class MModule(Module):
    def _run(self) -> TFileRenderer:
        r = TFileRenderer()
        self.p_filename(r)
        self.p_children(r)
        return r


class MSection(Module):
    def _run(self) -> TSectionRenderer:
        r = TSectionRenderer()
        self.p_sub_module(r, KW_HEADER, 'set_header', required=True)
        self.p_children(r)
        return r


class MHeader(Module):
    def _run(self) -> THeaderRenderer:
        keyword = self.p_value(KW_KEYWORD, required=True)
        r = THeaderRenderer(keyword)
        if self._parameters.get(KW_IS_PROPERTY, False):
            r.set_equal()
        for p in self._parameters.get(KW_PARAMETERS, []):
            r.add_parameter(self.p_raw(p))
        return r


class MProperty(Module):
    def _run(self) -> TPropertyRenderer:
        key = self.p_value(KW_KEY)
        value = self.p_value(KW_VALUE)
        r = TPropertyRenderer(key, value)
        if self._parameters.get(KW_IS_RAW, False):
            r.set_raw()
        return r


class MLoop(Module):
    def _run(self) -> TRenderer:
        values = self.p_value(KW_LOOP_ITERATOR, required=True)
        if not isinstance(values, list):
            raise ValueError('Loop data must be a list.')
        template = self.p_value(KW_LOOP_TEMPLATE, required=True)
        keyword, parameters = list(template.items())[0]
        r = TRenderer()
        for value in values:
            sub_module = ModuleManager.create(value, self._variables, keyword, parameters)
            r.add(sub_module.run())
        return r


class MSource(Module):
    def _run(self) -> TRenderer:
        template_file = self.p_value(KW_FILENAME)
        results = Template()\
            .load_template(template_file)\
            .set_data(self._data)\
            .set_variables(self._variables)\
            .run()
        r = TRenderer()
        return r.add(results)
