# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from marshmallow import SchemaOpts

from flask_restive.params import BaseParams, Params


class ProxySchemaOpts(SchemaOpts):
    """
    Provides read only access to all Meta properties via "opts"
    serializer's attribute.
    Example:
        class MySerializer(Schema):
            OPTIONS_CLASS = ProxySchemaOpts

            class Meta(object):
                my_param1 = 1
                my_param2 = 2

        >>> MySerializer().opts.my_param1
        1
        >>> MySerializer().opts.my_param2
        2
    """

    def __init__(self, meta, ordered=True):
        super(ProxySchemaOpts, self).__init__(meta, ordered=ordered)
        self.meta = meta

    def __getattr__(self, attr_name):
        if hasattr(self.meta, attr_name):
            return getattr(self.meta, attr_name)
        return self.__getattribute__(attr_name)


class DataWrapperSchemaOpts(ProxySchemaOpts):
    """
    Provides "data_wrapper" meta parameter, by default it's BaseParams.
    Provides "wrap_data" method, returns wrapped params.
    Example:
        class MySchema(Schema):
            OPTIONS_CLASS = BaseParamsSchemaOpts

            class Meta(object):
                data_wrapper = BaseParams

        >>> MySchema().opts.wrap_data({'a': 1, 'b': 2})
        BaseParams([('a', 1), ('b', 2)])
    """

    def __init__(self, meta, *args, **kwargs):
        super(DataWrapperSchemaOpts, self).__init__(meta, *args, **kwargs)
        self.data_wrapper = getattr(meta, 'data_wrapper', BaseParams)

    def wrap_data(self, *args, **kwargs):
        return self.data_wrapper(*args, **kwargs)


class PrimaryKeySchemaOpts(DataWrapperSchemaOpts):
    """
    Provides "primary_key_fields" meta parameter, by default it's empty tuple.
    Default "data_wrapper" meta parameter is Params.
    Provides "wrap_data" method, returns wrapped params with primary key.
    Example:
        class MySchema(Schema):
            OPTIONS_CLASS = ParamsSchemaOpts

            class Meta(object):
                data_wrapper = MyDataWrapper
                primary_key_fields = ('a',)

        >>> MySchema().opts.wrap_data({'a': 1, 'b': 2})
        Params([('a', 1), ('b', 2)], ('a',))
    """

    def __init__(self, meta, *args, **kwargs):
        super(PrimaryKeySchemaOpts, self).__init__(meta, *args, **kwargs)
        self.primary_key_fields = getattr(meta, 'primary_key_fields', ())
        self.data_wrapper = getattr(meta, 'data_wrapper', Params)

    def wrap_data(self, *args, **kwargs):
        kwargs['primary_key_fields'] = self.primary_key_fields
        return super(PrimaryKeySchemaOpts, self).wrap_data(*args, **kwargs)
