from __future__ import annotations

import os
import re


def _format_string(string: str) -> str:
    if re.search(" ", string, ) is not None:
        return '"{}"'.format(string)
    return string


class TRenderer:
    def __init__(self):
        self._indent = 0
        self._children: list[TRenderer] = []

    def render(self):
        content = []
        for child in self._children:
            content.append(child.render())
        return self._render_content(content)

    def _render_line(self, *elements, separator: str = ' ', ignore_empty: bool = True) -> str:
        if ignore_empty:
            elements = list(filter(lambda x: len(x) > 0, elements))
        line = "\t" * self._indent
        line += separator.join(elements)
        return line

    @staticmethod
    def _render_content(content: list[str]) -> str:
        return "\n".join(content)

    def adjust_indent(self, current: int = 0) -> TRenderer:
        self._indent = self._compute_indentation(current)
        for child in self._children:
            child.adjust_indent(self._indent)
        return self

    def _compute_indentation(self, current: int) -> int:
        return current

    def add(self, child: TRenderer) -> TRenderer:
        if isinstance(child, list):
            for c in child:
                self.add(c)
        else:
            self._children.append(child)
        return self

    def add_blank_lines(self, count: int = 1) -> TRenderer:
        self.add(TBlankLinesRenderer(count))
        return self

    def add_comment(self, comment: str) -> TRenderer:
        self.add(TCommentRenderer(comment))
        return self

    def save(self) -> bool:
        res = True
        for child in self._children:
            res = child.save() and res
        return res


class TSectionRenderer(TRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._header = None

    def render(self) -> str:
        if self._header is None:
            raise ValueError('TSectionRenderer requires a header. Call set_header to fix the issue.')

        content = [self._render_line(self._header.render(), '{')]
        for child in self._children:
            content.append(child.render())
        content.append(self._render_line('}'))
        return self._render_content(content)

    def _compute_indentation(self, current: int) -> int:
        return current + 1

    def set_header(self, renderer: TRenderer) -> TSectionRenderer:
        self._header = renderer
        return self

    def set_basic_header(self, *args, **kwargs) -> TSectionRenderer:
        self._header = THeaderRenderer(*args, **kwargs)
        return self

    def add_property(self, *args, **kwargs) -> TSectionRenderer:
        return self.add(TPropertyRenderer(*args, **kwargs))


class THeaderRenderer(TRenderer):
    def __init__(self, keyword: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keyword = keyword
        self._parameters = []
        self._sign = ''

    def _compute_indentation(self, current: int) -> int:
        return current

    def add_parameter(self, value: str) -> THeaderRenderer:
        self._parameters.append(value)
        return self

    def set_equal(self) -> THeaderRenderer:
        self._sign = '='
        return self

    def render(self) -> str:
        pre_rendered_parameters = list(map(lambda p: '"{}"'.format(p), self._parameters))
        line = self._render_line(self._keyword, *pre_rendered_parameters, self._sign)
        return line


class TPropertyRenderer(TRenderer):
    def __init__(self, keyword: str, value: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keyword = _format_string(keyword)
        self._value = value
        self._raw = False

    def render(self) -> str:
        if self._raw:
            pre_rendered_value = self._value
        else:
            pre_rendered_value = '"{}"'.format(self._value)
        return self._render_line(self._keyword, '=', pre_rendered_value)

    def set_raw(self) -> TPropertyRenderer:
        self._raw = True
        return self

    def _compute_indentation(self, current: int) -> int:
        return current + 1


class TCommentRenderer(TRenderer):
    def __init__(self, comment: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._comment = comment

    def _compute_indentation(self, current: int) -> int:
        return current + 1

    def render(self):
        return self._render_line('#', self._comment)


class TBlankLinesRenderer(TRenderer):
    def __init__(self, count: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._count = count

    def _compute_indentation(self, current: int) -> int:
        return current

    def render(self):
        lines = [''] * self._count
        return self._render_content(lines)


class TVariableRenderer(TSectionRenderer):
    def __init__(self, name: str, var_type: object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_header(THeaderRenderer('variable').add_parameter(name))
        self.add(TPropertyRenderer('type', str(var_type)))
        self._value = None

    def set_default(self, value: object, raw: bool = False) -> TVariableRenderer:
        prop = TPropertyRenderer('default', str(value))
        if raw:
            prop.set_raw()
        self.add(prop)
        return self


class TFileRenderer(TRenderer):
    """Special renderer that can save the render inside a single file."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._filename = None

    def _compute_indentation(self, current: int) -> int:
        if current > 0:
            raise ValueError('TFileRenderer must be used at root level. Therefore, it cannot have an indent \
                             different than 0.')
        return -1

    def set_filename(self, filename: str) -> TFileRenderer:
        if filename.find('/') == -1:
            filename = './' + filename
        self._filename = filename
        return self

    def save(self) -> bool:
        if self._filename is None:
            raise ValueError('Filename is not defined. Call set_filename before save.')

        content = self.render()
        directory = os.path.dirname(self._filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
            print('Directory created: {}/'.format(directory))

        with open(self._filename, 'w') as file:
            file.write(content)
            print('File saved in {}'.format(self._filename))

        return super().save()


class TInfraRenderer(TRenderer):
    """Special renderer that can only accept TFileRenderer as children. The TInfraRenderer can also be saved, that
    will build the directory hierarchy and save all the module children inside this directory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._directory = None
        self._children: list[TFileRenderer] = []

    def _compute_indentation(self, current: int) -> int:
        if current > 0:
            raise ValueError('TInfraRenderer must be used at root level. Therefore, it cannot have an indent \
                             different than 0.')
        return -1

    def set_directory(self, directory: str) -> TInfraRenderer:
        self._directory = directory
        return self

    def add(self, module: TFileRenderer) -> TInfraRenderer:
        # if not isinstance(module, TFileRenderer) and not isinstance(module, list):
        #     raise ValueError('Infrastructure only take TModuleRenderer as children.')

        super().add(module)
        return self

    def save(self) -> bool:
        if self._directory is None:
            raise ValueError('Directory is not defined. Call set_directory before save. ')

        if not os.path.isdir(self._directory):
            os.makedirs(self._directory)
            print('Directory created: {}/'.format(self._directory))

        pwd = os.path.dirname(__file__)
        os.chdir(self._directory)
        # for module in self._children:
        #     module.save()
        res = super().save()
        print('Infrastructure save in {}/'.format(self._directory))
        os.chdir(pwd)
        return res
