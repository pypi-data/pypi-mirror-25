# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import Hashable, OrderedDict


class BaseParams(OrderedDict):
    """
    Lazy attribute dictionary. Allows access to the dictionary keys
    via attributes, returns None on unknown attribute/key reading.
    Example:
        >>> p = BaseParams({'a': 1})
        >>> p.a
        1
        >>> p.unknown
        None
    """

    def __init__(self, items=None, **kwargs):
        data = OrderedDict(items or ((k, kwargs[k]) for k in sorted(kwargs)))
        super(BaseParams, self).__init__(data)

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError as e:
            if key.startswith('_'):
                raise e
            return self.__getitem__(key)

    def __missing__(self, key):
        return None

    def __setattr__(self, key, value):
        if not key.startswith('_'):
            self.__setitem__(key, value)
        else:
            super(BaseParams, self).__setattr__(key, value)

    def __setitem__(self, key, value):
        # pylint: disable=signature-differs
        super(BaseParams, self).__setitem__(key, value)
        super(BaseParams, self).__setattr__(key, value)


class Params(BaseParams, Hashable):
    """
    Primary key attribute dictionary. Receives primary_key_fields
    attribute on initializing and uses it to check if dictionary
    contains all necessary parts of the primary key.
    It's hashable: when has primary key the hash is some int value,
    otherwise the hash is 0.
    Example:
        >>> p = Params({'a': 1, 'b': 2}, primary_key_fields=['a', 'b'])
        >>> p.has_primary_key()
        True
        >>> p = Params({'a': 1}, primary_key_fields=['a', 'b'])
        >>> p.has_primary_key()
        False
    """

    def __init__(self, items=None, primary_key_fields=None, **kwargs):
        super(Params, self).__init__(items=items, **kwargs)
        self._primary_key_fields = primary_key_fields or ()

    def has_primary_key(self):
        """
        :return: bool, True if it contains all primary key fields.
        """
        pk_fields = set(self._primary_key_fields)
        result = (pk_fields.intersection(self.keys()) == pk_fields and
                  all(isinstance(self[k], Hashable) for k in pk_fields))
        return result

    @property
    def primary_key(self):
        if self.has_primary_key():
            result = OrderedDict([
                (k, self[k])
                for k in self._primary_key_fields
            ])
            return result

    def __hash__(self):
        result = 0
        if self.has_primary_key():
            for k in self._primary_key_fields:
                result ^= hash(self[k])
        return result

    def __repr__(self):
        return '{0}, {1})'.format(
            super(Params, self).__repr__()[:-1],
            repr(self._primary_key_fields))


class SliceParams(BaseParams):
    """
    Slice attribute dictionary. Provides attributes to work with slice
    of iterable data. offset & limit attributes allow to get access
    to some part of iterable data. total_count & items_count allow
    to understand how many elements contains full source iterable object
    and how many of them contains the current slice. items_list allows
    to work with sliced elements. items_count parameter is read only
    and is auto calculated as count of the items_list elements.
    Example:
        >>> p = SliceParams(offset=0, limit=2)
        >>> p.total_count = 3
        >>> p.items_list = [1, 2]
        >>> p.offset
        0
        >>> p.limit
        2
        >>> p.total_count
        3
        >>> p.items_list
        [1, 2]
        >>> p.items_count
        2
    """

    def __init__(self, items=None, **kwargs):
        super(SliceParams, self).__init__(items, **kwargs)
        self.offset = self.get('offset', 0)
        self.limit = self.get('limit')
        self.total_count = self.get('total_count', 0)
        self.items_list = self.get('items_list', [])

    def __setitem__(self, key, value):
        if key == 'items_count':
            raise AttributeError('read only property')

        if key == 'items_list':
            items_count = len(value)
            super(SliceParams, self).__setitem__('items_count', items_count)

        super(SliceParams, self).__setitem__(key, value)

    def __repr__(self):
        template = ('{class_name}(offset={offset}, limit={limit}, '
                    'total_count={total_count}, '
                    'items_count={items_count}, '
                    'items_list={items_list})')
        return template.format(
            class_name=self.__class__.__name__,
            offset=self.offset, limit=self.limit,
            total_count=self.total_count,
            items_count=self.items_count,
            items_list=repr(self.items_list))


class SortingParams(BaseParams):
    """
    Sorting attribute dictionary. Provides just one read only attribute
    to set ordered list of prefixed names.
    Example:
        >>> p = SortingParams(sort_by=['-updated_on', '-created_on', 'id'])
        >>> p.sort_by
        OrderedDict([
            ('updated_on', 'desc'),
            ('created_on', 'desc'),
            ('id', 'asc')
        ])
    """

    class SortingType(object):
        ASC = 'asc'
        DESC = 'desc'

    def __init__(self, items=None, **kwargs):
        super(SortingParams, self).__init__(items, **kwargs)
        sort_by = self.get('sort_by', [])
        sort_by = self._convert_prefixed_list(sort_by)
        self.sort_by = sort_by

    def _convert_prefixed_list(self, value):
        value = OrderedDict([
            (k[1:], self.SortingType.DESC) if k.startswith('-')
            else (k, self.SortingType.ASC) for k in value
        ])
        return value

    def __repr__(self):
        return '{class_name}(sort_by={sort_by})'.format(
            class_name=self.__class__.__name__,
            sort_by=repr(self.sort_by)[12:-1])
