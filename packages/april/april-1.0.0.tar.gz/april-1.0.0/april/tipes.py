# -*- coding: utf-8 -*-

import inspect


__all__ = ('listof', 'setof', 'tupleof')


def __new(klass, obj):
    nested_type = klass.nested_type

    if not isinstance(obj, (list, set, tuple)):
        raise ValueError('only list set or tuple can be container type, got {}'
                         .format(type(obj)))
    for each in obj:
        if not isinstance(each, nested_type):
            raise ValueError("element should be {}, got {}"
                             .format(nested_type, type(each)))

    assert klass.__bases__[0] in (list, tuple, set)
    assert isinstance(obj, (list, tuple, set))
    return klass.__bases__[0].__new__(klass, obj)


def _validate(nested_type):
    if not inspect.isclass(nested_type):
        raise ValueError('nested_type must be a class')


def listof(nested_type):
    """listof_* type creation

    Usage::

        listof_str = listof(str)
        str_list = listof_str(['hello', 'world'])
        isinstance(str_list, listof_str)
    """
    _validate(nested_type)
    return type('listof_' + nested_type.__name__, (list, ), {
        'nested_type': nested_type,
        '__new__': __new
    })


def setof(nested_type):
    _validate(nested_type)
    return type('setof_' + nested_type.__name__, (set, ), {
        'nested_type': nested_type,
        '__new__': __new
    })


def tupleof(nested_type):
    _validate(nested_type)
    return type('tupleof_' + nested_type.__name__, (tuple, ), {
        'nested_type': nested_type,
        '__new__': __new
    })
