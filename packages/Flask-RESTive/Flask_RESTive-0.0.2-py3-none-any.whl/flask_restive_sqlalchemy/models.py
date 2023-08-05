# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import NoInspectionAvailable

from flask_restive.utils import classproperty, plural, decapitalize


Base = declarative_base()


class Model(Base):
    """
    Abstract model class.
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self.set_attrs(**kwargs)

    def set_attrs(self, **attrs):
        for attr_name, attr_value in attrs.items():
            # pylint: disable=unsupported-membership-test
            if attr_name in self.fields:
                setattr(self, attr_name, attr_value)

    def to_dict(self):
        result = {}
        for attr_name in self.fields:  # pylint: disable=not-an-iterable
            attr_value = getattr(self, attr_name)
            if attr_value is not None:
                result[attr_name] = attr_value
        return result

    @declared_attr
    def __tablename__(cls):
        # pylint: disable=no-self-argument
        return plural(decapitalize(cls.__name__))

    @classmethod
    def get_model_columns(cls):
        try:
            columns = inspect(cls).mapper.column_attrs
        except NoInspectionAvailable:  # pragma: no cover
            pass
        else:
            columns = list(sorted(columns, key=lambda column: column.key))
            return columns

    @classmethod
    def get_model_primary_key_columns(cls):
        try:
            columns = list(inspect(cls).mapper.primary_key)
        except NoInspectionAvailable:  # pragma: no cover
            pass
        else:
            return columns

    @classproperty
    def fields(cls):
        # pylint: disable=no-self-argument
        columns = cls.get_model_columns()
        if columns:
            fields = OrderedDict([(column.key, getattr(cls, column.key))
                                  for column in columns])
            return fields

    @classproperty
    def primary_key_fields(cls):
        # pylint: disable=no-self-argument
        columns = cls.get_model_primary_key_columns()
        if columns:
            fields = OrderedDict([(column.key, getattr(cls, column.key))
                                  for column in columns])
            return fields
