# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple


__all__ = ['Range', 'List']


Range = namedtuple('Range', ('min', 'max'))


class List(list):
    pass
