# -*- coding: utf-8 -*-
from __future__ import unicode_literals


__all__ = ['classproperty', 'decapitalize', 'plural']


class classproperty(object):
    """
    cached class property
    Example:

    class MyClass(object):
        _counter = 0

        @classproperty
        def counter(cls):
            cls._counter += 1
            return cls._counter

    >>> MyClass.counter
    1
    # now it's loaded from class cache
    >>> MyClass.counter
    1
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, class_):
        cached_attr_name = '_cached_' + self.func.__name__

        obj = instance.__class__ if instance is not None else class_
        if hasattr(obj, cached_attr_name):
            return getattr(obj, cached_attr_name)

        value = self.func(obj)
        setattr(obj, cached_attr_name, value)
        return value


def decapitalize(value):
    """
    Set string to lowercase
    and insert undreline symbol
    bettween chars that have different cases.
    For example:
        HelloWorld => hello_world

    :param value: capitalized string like 'CamelCase'
    :type value: str
    :return: decapitalized string like 'camel_case'
    :rtype: str
    """
    low = value.lower()
    result = []
    for i in range(0, len(low)):
        if i and result[-1] != '_':
            if (low[i] != value[i] and low[i-1] == value[i-1] or
                    low[i].isdigit() != low[i-1].isdigit()):
                result.append('_')
        result.append(low[i])
    return ''.join(result)


def plural(value):
    """
    Set noun to plural form.
    For example:
        book => books
        box => boxes
        hero => heroes
        slash => slashes
        story => stories
        day => days
        wolf => wolves

    :param value: string in single form
    :return: string in plural form
    """
    if value[-1] in ('s', 'x', 'o') or value[-2:] in ('sh', 'ch'):
        result = value + 'es'
    elif (value[-1] == 'y' and
          value[-2] not in ('a', 'e', 'i', 'o', 'u')):
        result = value[:-1] + 'ies'
    elif value[-1] == 'f':
        result = value[:-1] + 'ves'
    elif value[-2:] == 'fe':
        result = value[:-2] + 'ves'
    else:
        result = value + 's'
    return result
