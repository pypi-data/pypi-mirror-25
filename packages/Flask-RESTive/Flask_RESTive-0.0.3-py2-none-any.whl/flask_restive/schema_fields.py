# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six
from marshmallow.fields import (
    Field, Raw, Nested, Dict, List, String, UUID, Number, Integer, Decimal,
    Boolean, FormattedString, Float, DateTime, LocalDateTime, Time, Date,
    TimeDelta, Url, URL, Email, Method, Function, Str, Bool, Int, Constant,
    missing_)


__all__ = [
    'Field',
    'Raw',
    'Nested',
    'Dict',
    'List',
    'String',
    'UUID',
    'Number',
    'Integer',
    'Decimal',
    'Boolean',
    'FormattedString',
    'Float',
    'DateTime',
    'LocalDateTime',
    'Time',
    'Date',
    'TimeDelta',
    'Url',
    'URL',
    'Email',
    'Method',
    'Function',
    'Str',
    'Bool',
    'Int',
    'Constant',
    'CommaString',
    'missing_',
]


class CommaString(List):
    """
    Provides comma separated lists support.

    :param impl: elements implementation field instance or class
    :type impl: marshmallow.fields.Field
    :param separator: string separator
    :type separator: str
    :param validate: elements validator
    :type validate: marshmallow.validate.Validator
    :param kwargs: to be forwarded to base class constructor
    """
    default_error_messages = {
        'invalid': 'Not a valid comma separated string.',
    }

    def __init__(self, impl=String, separator=',', validate=None, **kwargs):
        super(CommaString, self).__init__(impl, validate=None, **kwargs)
        self.separator = separator
        self.validate = validate

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        result = super(CommaString, self)._serialize(value, attr, obj)
        result = map(str, result)
        return self.separator.join(result)

    def _deserialize(self, value, attr, data):
        if not isinstance(value, six.string_types):
            self.fail('invalid')
        if value.startswith(self.separator):
            value = value[len(self.separator):]
        if value.endswith(self.separator):
            value = value[:-len(self.separator)]
        if not value:
            return []
        value = value.split(self.separator)
        return super(CommaString, self)._deserialize(value, attr, data)

    @property
    def validate(self):
        return self.container.validate

    @validate.setter
    def validate(self, validator):
        if validator:
            self.container.validate = validator
            self.container.validators = [validator]
