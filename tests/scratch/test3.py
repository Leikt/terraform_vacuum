import functools
import time


def deco(func):
    @functools.wraps(func)
    def wrapper_deco(obj, *args, **kwargs):
        if not isinstance(obj, object):
            raise Exception('Wrong context. This decorator should be used on methods only.')
        expression = func(obj, *args, **kwargs)
        return expression + " World"

    return wrapper_deco


def deco2(func):
    @functools.wraps(func)
    def wrapper_deco(obj, *args, **kwargs):
        if not isinstance(obj, object):
            raise Exception('Wrong context. This decorator should be used on methods only.')
        expression = func(obj, *args, **kwargs)
        return expression + " !"

    return wrapper_deco


class Foo:
    def __init__(self):
        self._value = "Hello"

    @deco2
    @deco
    def foo(self):
        return self._value


print(Foo().foo())
