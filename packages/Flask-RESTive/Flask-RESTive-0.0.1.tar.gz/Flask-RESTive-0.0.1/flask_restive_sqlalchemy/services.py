# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, between, tuple_

from flask_restive.services import Storage as BaseStorage
from flask_restive.utils import RangeValue, ListValue
from flask_restive.exceptions import DoesNotExist, AlreadyExists
from flask_restive.params import SortingParams

from flask_restive_sqlalchemy.models import Model
from flask_restive_sqlalchemy.utils import make_connection_settings


class Storage(BaseStorage):
    _engine = None
    _session_cls = None

    class Meta(object):
        model_cls = Model

    def __init__(self):
        super(Storage, self).__init__()
        self.session = None

    @property
    def model_cls(self):
        return self.opts.model_cls

    @classmethod
    def _get_or_create_connection_pool(cls):
        if cls._engine is None:
            info, options = make_connection_settings(cls.app)
            cls._engine = create_engine(info, **options)

        if cls._session_cls is None:
            cls._session_cls = scoped_session(sessionmaker(
                bind=cls._engine, autoflush=True, autocommit=False))

    @classmethod
    def _return_connection_to_pool(cls):
        if cls._session_cls is not None:
            cls._session_cls.remove()

    def _retrieve_connection_from_pool(self):
        self.session = self._session_cls()

    def _close_connection_and_return_to_pool(self):
        if self.session is not None:
            self.session.close()
        self._return_connection_to_pool()

    def open(self):
        self._get_or_create_connection_pool()
        self._retrieve_connection_from_pool()
        self.model_cls.metadata.create_all(self._engine)

    def close(self, exception=None):
        if not exception:
            self._commit()
        else:
            self._rollback()
        self._close_connection_and_return_to_pool()

    def _commit(self):
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def _rollback(self):
        self.session.rollback()

    def _make_query(self, params=None):
        query = self.session.query(self.model_cls)

        if params:
            for attr_name, attr_value in params.items():
                attr_query = self._make_attr_filter(attr_name, attr_value)
                if attr_query is not None:
                    query = query.filter(attr_query)

        return query

    def _make_range_attr_filter(self, attr_name, attr_value):
        if attr_value.min is not None and attr_value.max is not None:
            return between(self.model_cls.fields[attr_name],
                           attr_value.min, attr_value.max)

        if attr_value.min is not None:
            return and_(self.model_cls.fields[attr_name] >= attr_value.min)

        if attr_value.max is not None:
            return and_(self.model_cls.fields[attr_name] <= attr_value.max)

    def _make_list_attr_filter(self, attr_name, attr_value):
        return self.model_cls.fields[attr_name].in_(attr_value)

    def _make_const_attr_filter(self, attr_name, attr_value):
        return and_(self.model_cls.fields[attr_name] == attr_value)

    def _make_attr_filter(self, attr_name, attr_value):
        if isinstance(attr_value, RangeValue):
            query = self._make_range_attr_filter(attr_name, attr_value)
        elif isinstance(attr_value, ListValue):
            query = self._make_list_attr_filter(attr_name, attr_value)
        else:
            query = self._make_const_attr_filter(attr_name, attr_value)
        return query

    def _make_order_by(self, sorting_params=None):
        if not sorting_params:
            order_by = list(map(lambda attr: attr.asc(),
                                self.model_cls.primary_key_fields.values()))
            return order_by
        order_by = []
        for attr_name, sorting_order in sorting_params.sort_by.items():
            if sorting_order == SortingParams.SortingType.DESC:
                attr = self.model_cls.fields[attr_name].desc()
                order_by.append(attr)
            elif sorting_order == SortingParams.SortingType.ASC:
                attr = self.model_cls.fields[attr_name].asc()
                order_by.append(attr)
        return order_by

    def _make_sorted_query(self, query, sorting_params=None):
        query = query.order_by(*self._make_order_by(sorting_params))
        return query

    @classmethod
    def _make_sliced_query(cls, query, slice_params=None):
        if slice_params:
            if slice_params.offset:
                query = query.offset(slice_params.offset)
            if slice_params.limit:
                query = query.limit(slice_params.limit)
        return query

    def get_count(self, filter_params=None, **kwargs):
        query = self._make_query(filter_params)
        result = query.count()
        return result

    def get_list(self, filter_params=None, slice_params=None,
                 sorting_params=None, **kwargs):
        query = self._make_query(filter_params)
        query = self._make_sorted_query(query, sorting_params)
        query = self._make_sliced_query(query, slice_params)
        result = []
        for item in query.all():
            result.append(self.wrap_data(item.to_dict()))
        return result

    def _make_query_pk_in(self, params_list):
        pk_attrs = self.model_cls.primary_key_fields.values()
        pk_values = []
        for params in params_list:
            assert params.has_primary_key(), 'No primary key to find.'
            pk_values.append(params.primary_key.values())
        query = self.session.query(self.model_cls).filter(
            tuple_(*pk_attrs).in_(pk_values))
        return query

    def create_list(self, data_params, **kwargs):
        any_exists = bool(self._make_query_pk_in(data_params).count())
        if any_exists:
            raise AlreadyExists

        items = []
        for params in data_params:
            item = self.model_cls(**params)  # pylint: disable=not-callable
            items.append(item)

        self.session.bulk_save_objects(items, return_defaults=True)

        result = [self.wrap_data(item.to_dict()) for item in items]
        return result

    def update_list(self, data_params, **kwargs):
        query = self._make_query_pk_in(data_params)

        all_exist = query.count() == len(data_params)
        if not all_exist:
            raise DoesNotExist

        i = 0
        items = query.all()
        for params in data_params:
            item = items[i]
            item_params = item.to_dict()
            item_params.update(params)  # update fields
            item.set_attrs(**item_params)
            i += 1

        self.session.bulk_save_objects(items, return_defaults=True)

        result = [self.wrap_data(item.to_dict()) for item in items]
        return result

    def delete_list(self, filter_params=None, **kwargs):
        query = self._make_query(filter_params)
        for item in query.all():
            self.session.delete(item)
