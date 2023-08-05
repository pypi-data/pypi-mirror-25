# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from flask import request
from flask_restful import Resource as BaseView
from marshmallow.utils import is_collection

from flask_restive.services import Storage
from flask_restive.schemas import (
    DataSchema, FilterSchema, SliceSchema, SortingSchema)
from flask_restive.utils import decapitalize


class Resource(BaseView):
    """
    Base resource view class. Provides methods
    to get request parameters.
    """

    @classmethod
    def get_endpoint(cls):
        return decapitalize(cls.__name__)

    @classmethod
    def get_request_params(cls, *args, **kwargs):
        # pylint: disable=unused-argument
        if request.method in ('HEAD', 'GET', 'DELETE'):
            return cls.get_query_params(**kwargs)
        return cls.get_body_params(**kwargs)

    @classmethod
    def get_header_params(cls):
        result = {}
        for key, value in request.headers.items():
            attr_name = key.replace('HTTP_', '', 1)
            attr_value = value.encode('latin1').decode('utf-8')
            result[attr_name] = attr_value
        return result

    @classmethod
    def get_path_params(cls, **kwargs):
        result = cls.get_header_params()
        for attr_name, attr_value in kwargs.items():
            if attr_value is not None:
                result[attr_name] = attr_value
        return result

    @classmethod
    def get_query_params(cls, **kwargs):
        result = cls.get_path_params(**kwargs)
        result.update(request.args.to_dict())
        return result

    @classmethod
    def get_body_params(cls, **kwargs):
        path_params = cls.get_path_params(**kwargs)

        body_params = request.get_json()
        if body_params is None:
            body_params = request.form.to_dict()

        if isinstance(body_params, list):
            result = []
            for body_item in body_params:
                result_item = deepcopy(path_params)
                result_item.update(body_item)
                result.append(result_item)
        else:
            result = deepcopy(path_params)
            result.update(body_params)

        return result


class StorageResource(Resource):
    storage_cls = Storage
    data_schema_cls = DataSchema
    filter_schema_cls = FilterSchema
    slice_schema_cls = SliceSchema
    sorting_schema_cls = SortingSchema

    @classmethod
    def get(cls, *args, **kwargs):
        data = cls.get_request_params(*args, **kwargs)

        filter_schema = cls.filter_schema_cls(cls.data_schema_cls)
        filter_params, _ = filter_schema.load(
            data, many=False, partial=True)

        if filter_params.has_primary_key():

            with cls.storage_cls() as storage:
                item = storage.get_item(filter_params)

            data_schema = cls.data_schema_cls()
            result, _ = data_schema.dump(item, many=False)

        else:

            slice_schema = cls.slice_schema_cls(cls.data_schema_cls)
            slice_params, _ = slice_schema.load(
                data, many=False, partial=False)

            sorting_schema = cls.sorting_schema_cls(cls.data_schema_cls)
            sorting_params, _ = sorting_schema.load(
                data, many=False, partial=False)

            with cls.storage_cls() as storage:
                slice_params.total_count = storage.get_count(filter_params)
                if slice_params.total_count:
                    slice_params.items_list = storage.get_list(
                        filter_params, slice_params, sorting_params)

            result, _ = slice_schema.dump(slice_params, many=False)

        return result, 200

    @classmethod
    def post(cls, *args, **kwargs):
        data = cls.get_request_params(*args, **kwargs)

        data_schema = cls.data_schema_cls()
        data_params, _ = data_schema.load(data, partial=False)

        if not is_collection(data_params):

            with cls.storage_cls() as storage:
                item = storage.create_item(data_params)

            result, _ = data_schema.dump(item, many=False)

        else:

            with cls.storage_cls() as storage:
                items = storage.create_list(data_params)

            result, _ = data_schema.dump(items, many=True)

        return result, 201

    @classmethod
    def patch(cls, *args, **kwargs):
        data = cls.get_request_params(*args, **kwargs)

        data_schema = cls.data_schema_cls()
        data_params, _ = data_schema.load(data, partial=True)

        if not is_collection(data_params):

            with cls.storage_cls() as storage:
                item = storage.update_item(data_params)

            result, _ = data_schema.dump(item, many=False)

        else:

            with cls.storage_cls() as storage:
                items = storage.update_list(data_params)

            result, _ = data_schema.dump(items, many=True)

        return result, 200

    @classmethod
    def delete(cls, *args, **kwargs):
        data = cls.get_request_params(*args, **kwargs)

        filter_schema = cls.filter_schema_cls(cls.data_schema_cls)
        filter_params, _ = filter_schema.load(data, partial=True)

        with cls.storage_cls() as storage:
            storage.delete_list(filter_params)

        return {}, 204
