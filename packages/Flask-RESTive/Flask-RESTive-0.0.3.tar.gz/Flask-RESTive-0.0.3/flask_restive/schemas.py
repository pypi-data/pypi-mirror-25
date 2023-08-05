# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from copy import deepcopy

from marshmallow import MarshalResult, UnmarshalResult, Schema as BaseSchema
from marshmallow import validates_schema, post_load, pre_dump
from marshmallow.validate import ValidationError, Range, OneOf
from marshmallow.utils import is_collection

import flask_restive.schema_fields as fields
from flask_restive.schema_opts import (
    DataWrapperSchemaOpts, PrimaryKeySchemaOpts)
from flask_restive.params import SliceParams, SortingParams
from flask_restive import types


class Schema(BaseSchema):
    """
    Base schema class. Wraps all loaded & dumped data
    to named dictionary class. Important things:

        - all attributes of Meta are allowed
          via opts object:

              class MySchema(Schema):
                  class Meta(Schema.Meta):
                      my_option = 1

              >>> MySchema().opts.my_option
              1

        - data_wrapper meta attribute can be
          changed to change the wrapper class:

              class MySchema(Schema):
                  class Meta(Schema.Meta):
                      data_wrapper = MyWrapperClass

              >>> data, errors = MySchema().load({'hello': 'world'})
              >>> type(data)
              <type: 'MyWrapperClass'>

        - wrap_data method can be overridden
          to change wrapping behaviour

    """
    OPTIONS_CLASS = DataWrapperSchemaOpts
    opts = None

    class Meta(BaseSchema.Meta):
        ordered = True
        dateformat = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, strict=True, **kwargs):
        super(Schema, self).__init__(strict=strict, **kwargs)

    def wrap_data(self, data):
        return self.opts.wrap_data(data)

    def load(self, data, many=None, partial=None):
        """
        Load data and wrap results into the data wrapper.
        """
        many = is_collection(data)
        result, errors = super(Schema, self).load(
            data, many=many, partial=partial)

        if not errors:
            if is_collection(result):
                result = [self.wrap_data(item) for item in result]
            else:
                result = self.wrap_data(result)

        return UnmarshalResult(result, errors)

    def dump(self, obj, many=None, update_fields=True, **kwargs):
        """
        Dump data and wrap results into the data wrapper.
        """
        many = is_collection(obj)
        result, errors = super(Schema, self).dump(
            obj, many=many, update_fields=update_fields, **kwargs)

        if not errors:
            if is_collection(result):
                result = [self.wrap_data(item) for item in result]
            else:
                result = self.wrap_data(result)

        return MarshalResult(result, errors)


class DataSchema(Schema):
    OPTIONS_CLASS = PrimaryKeySchemaOpts

    class Meta(Schema.Meta):
        sortable_fields = ()
        default_sorting = ()


class IntegerIDSchema(DataSchema):
    id = fields.Integer(required=True, validate=Range(min=1))

    class Meta(DataSchema.Meta):
        primary_key_fields = ('id',)
        sortable_fields = ('id',)
        default_sorting = ('id',)


class StringIDSchema(DataSchema):
    id = fields.String(required=True)

    class Meta(DataSchema.Meta):
        primary_key_fields = ('id',)
        sortable_fields = ('id',)
        default_sorting = ('id',)


class UUIDSchema(DataSchema):
    id = fields.UUID(required=True, missing=uuid.uuid1)

    class Meta(DataSchema.Meta):
        primary_key_fields = ('id',)
        sortable_fields = ('id',)
        default_sorting = ('id',)


class FilterSchema(DataSchema):
    """
    There are three ways to use this class:

        1. Use it "as is": all filter fields will be made
           automatically from the template schema class.
           Use default value of meta parameter:
           use_schema_template = True.

        2. Make custom filter as child from FilterSchema.
           Set meta parameter use_schema_template = False
           Define custom filter fields.

        3. Mix options 1 & 2. use_schema_template = True.
           Your additional filter fields will be added
           to the auto-generated fields from schema template.
    """

    class Meta(DataSchema.Meta):
        use_schema_template = True

    def __init__(self, schema_cls=None, *args, **kwargs):
        super(FilterSchema, self).__init__(*args, **kwargs)
        self._set_schema_template(schema_cls)

    def _set_schema_template(self, schema_cls=None):
        if schema_cls and self.opts.use_schema_template:
            schema_template = schema_cls()
            self._make_opts_from_schema_template(schema_template)
            self._make_fields_from_schema_template(schema_template)

    def _make_opts_from_schema_template(self, schema_template):
        """
        Set meta opts fields from schema template meta opts.
        """
        for opt_name in ('data_wrapper', 'primary_key_fields',
                         'sortable_fields', 'default_sorting'):
            opt_value = getattr(schema_template.opts, opt_name)
            setattr(self.opts.meta, opt_name, opt_value)
            setattr(self.opts, opt_name, opt_value)

    def _make_fields_from_schema_template(self, schema_template):
        """
        Make filter fields based on schema template fields.

        Mark all fields as optional. It's important because
        source template scheme can contain required fields or
        fields with default values.

        Beside of equal fields, adds range fields with suffixes: __min, __max,
        and in-set fields with suffix __in.
        """
        for field_name, field in schema_template.declared_fields.items():
            field = deepcopy(field)
            field.required = False
            field.missing = fields.missing_
            field.default = fields.missing_
            self.declared_fields[field_name] = field
            self.fields[field_name] = field

            if self._is_countable_field(field):
                self._make_field__in(field_name, field)

            if self._is_range_field(field):
                self._make_field__min(field_name, field)
                self._make_field__max(field_name, field)

    @classmethod
    def _is_countable_field(cls, field):
        is_countable = isinstance(
            field, (fields.String, fields.Number, fields.Date))
        return is_countable

    def _make_field__in(self, field_name, field):
        impl = deepcopy(field)
        field__in = fields.CommaString(impl, validate=field.validate)
        self.declared_fields[field_name + '__in'] = field__in
        self.fields[field_name + '__in'] = field__in

    @classmethod
    def _is_range_field(cls, field):
        is_range = isinstance(
            field, (fields.Number, fields.Date, fields.DateTime,
                    fields.Time, fields.TimeDelta))
        return is_range

    def _make_field__min(self, field_name, field):
        field__min = deepcopy(field)
        self.declared_fields[field_name + '__min'] = field__min
        self.fields[field_name + '__min'] = field__min

    def _make_field__max(self, field_name, field):
        field__max = deepcopy(field)
        self.declared_fields[field_name + '__max'] = field__max
        self.fields[field_name + '__max'] = field__max

    @validates_schema(pass_many=False)
    def validate_in_min_max(self, data):
        # pylint: disable=no-self-use
        """
        Check that list (__in), range (__min, __max) & const values
        are not set together for one parameter.
        """
        field_names = set()

        for field_name in data:
            if field_name.endswith('__in'):
                attr_name = field_name[:-4]
            elif field_name.endswith('__min') or field_name.endswith('__max'):
                attr_name = field_name[:-5]
            else:
                attr_name = field_name

            if attr_name in data and attr_name + '__in' in data:
                field_names.add(attr_name)
                field_names.add(attr_name + '__in')
            if attr_name in data and attr_name + '__min' in data:
                field_names.add(attr_name)
                field_names.add(attr_name + '__min')
            if attr_name in data and attr_name + '__max' in data:
                field_names.add(attr_name)
                field_names.add(attr_name + '__max')
            if attr_name + '__in' in data and attr_name + '__min' in data:
                field_names.add(attr_name + '__in')
                field_names.add(attr_name + '__min')
            if attr_name + '__in' in data and attr_name + '__max' in data:
                field_names.add(attr_name + '__in')
                field_names.add(attr_name + '__max')

        if field_names:
            raise ValidationError('Invalid schema.', field_names=field_names)

    @post_load(pass_many=False)
    def load_in_min_max(self, data):
        # pylint: disable=no-self-use
        """
        __in values => types.List &
        __min, __max values => types.Range.
        """
        data = deepcopy(data)

        for field_name in self.fields:
            if field_name not in data:
                continue

            elif field_name.endswith('__in'):
                attr_name = field_name[:-4]
                attr_value = data.pop(field_name)
                data[attr_name] = types.List(attr_value)

            elif field_name.endswith('__min') or field_name.endswith('__max'):
                attr_name = field_name[:-5]
                attr_value = types.Range(
                    min=data.pop(attr_name + '__min', None),
                    max=data.pop(attr_name + '__max', None))
                data[attr_name] = attr_value

        return data

    @pre_dump(pass_many=False)
    def dump_in_min_max(self, data):
        # pylint: disable=no-self-use
        """
        types.List => __in values &
        types.Range => __min, __max values.
        """
        result = deepcopy(data)

        for attr_name, attr_value in data.items():

            if isinstance(attr_value, types.List):
                result[attr_name + '__in'] = list(result[attr_name])

            elif isinstance(attr_value, types.Range):
                attr_value = result[attr_name]
                if attr_value.min:
                    result[attr_name + '__min'] = attr_value.min
                if attr_value.max:
                    result[attr_name + '__max'] = attr_value.max

            else:
                result[attr_name] = attr_value

        return result


class CustomFilterSchema(FilterSchema):
    """
    Base class to make custom filter schemas
    without any auto-generated fields.
    """

    class Meta(FilterSchema.Meta):
        use_schema_template = False


class SliceSchema(Schema):
    """
    This class is used with DataSchema & items_list attribute
    is the list of nested schema class instances.
    Important meta attributes:
        - max_limit - how many items can be loaded in one request
        - allow_none_limit - allow load all items in one request
    """
    offset = fields.Integer(validate=Range(min=0), missing=0)
    limit = fields.Integer(validate=Range(min=1))
    total_count = fields.Integer(default=0, dump_only=True)
    items_count = fields.Integer(default=0, dump_only=True)
    items_list = fields.Nested(DataSchema, dump_only=True)

    class Meta(Schema.Meta):
        data_wrapper = SliceParams
        max_limit = None
        allow_none_limit = True

    def wrap_data(self, data):
        if 'items_count' in data:
            del data['items_count']
        return super(SliceSchema, self).wrap_data(data)

    def __init__(self, schema_cls, **kwargs):
        super(SliceSchema, self).__init__(**kwargs)
        self._set_nested_schema(schema_cls)
        self._set_max_limit()

    def _set_nested_schema(self, schema_cls):
        nested_schema = schema_cls(many=True, partial=False)
        self.declared_fields['items_list'].nested = nested_schema
        self.fields['items_list'].nested = nested_schema

    def _set_max_limit(self):
        validator = Range(min=1, max=self.opts.max_limit)
        self.declared_fields['limit'].validate = validator
        self.declared_fields['limit'].validators = [validator]
        self.declared_fields['limit'].missing = self.opts.max_limit
        self.declared_fields['limit'].allow_none = self.opts.allow_none_limit
        self.fields['limit'].validate = validator
        self.fields['limit'].validators = [validator]
        self.fields['limit'].missing = self.opts.max_limit
        self.fields['limit'].allow_none = self.opts.allow_none_limit


class SortingSchema(Schema):
    sort_by = fields.CommaString()

    class Meta(Schema.Meta):
        data_wrapper = SortingParams

    def __init__(self, schema_cls, **kwargs):
        super(SortingSchema, self).__init__(**kwargs)
        self._set_schema_template(schema_cls)

    def _set_schema_template(self, schema_cls):
        schema_template = schema_cls()

        sortable_fields = list(schema_template.opts.sortable_fields)
        allowed_values = sortable_fields + list(map(
            lambda x: '-' + x, sortable_fields))
        default_sorting = ','.join(schema_template.opts.default_sorting)

        validator = OneOf(allowed_values)
        self.declared_fields['sort_by'].validate = validator
        self.declared_fields['sort_by'].missing = default_sorting
        self.fields['sort_by'].validate = validator
        self.fields['sort_by'].missing = default_sorting
