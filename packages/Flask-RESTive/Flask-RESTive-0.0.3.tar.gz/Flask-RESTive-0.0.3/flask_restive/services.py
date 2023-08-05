# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app

from flask_restive.schema_opts import PrimaryKeySchemaOpts
from flask_restive.params import SliceParams
from flask_restive.exceptions import DoesNotExist


class Service(object):
    """
    The abstract service class.
    Provides methods to initialize and finalize the service session:
        - open
        - close

    Can be used in with statement also:
        with Service() as service:
            storage.do_something()
    """
    OPTIONS_CLASS = PrimaryKeySchemaOpts
    opts = None
    app = None

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        meta = self.__class__.__dict__.get('Meta')
        setattr(self.__class__, 'opts', self.OPTIONS_CLASS(meta))
        setattr(self.__class__, 'app', current_app)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(exc_val)
        return exc_type is None

    def open(self):
        raise NotImplementedError

    def close(self, exception=None):
        raise NotImplementedError

    def wrap_data(self, *args, **kwargs):
        """
        This method should be called for each item
        returned by service methods.
        :param args: the first argument is data
            returned by service method
        :param kwargs: key-value attributes for
            manual creation
        :return: wrapped data
        :rtype: flask_restive.params.Params
        """
        return self.opts.wrap_data(*args, **kwargs)


class Storage(Service):
    """
    The abstract base storage class. Provides methods to manage data:
        - get_item
        - get_count
        - get_list
        - create_item
        - create_list
        - update_item
        - update_list
        - delete_list

    Provides methods to initialize and finalize the storage session:
        - open
        - close

    Can be used in with statement also:
        with Storage() as storage:
            filter_params = Params(id=1, primary_key_fields=('id',))
            item = storage.get_item(filter_params=filter_params)
    """

    def get_item(self, filter_params, **kwargs):
        """
        Get one item by filter. Filter should contain primary key.
        The found item should be wrapped in Params class and
        should contain primary key.

        :param filter_params: filtering parameters
        :type filter_params: flask_restive.params.Params
        :param kwargs: options, to be forwarded to get_list method
        :return: found item
        :rtype: flask_restive.params.Params
        """
        items = self.get_list(filter_params=filter_params,
                              slice_params=SliceParams(limit=1), **kwargs)
        if not items:
            raise DoesNotExist
        assert len(items) == 1, 'Too many items to unpack.'
        return items[0]

    def get_count(self, filter_params=None, **kwargs):
        """
        Get count of items by filter.

        :param filter_params: filtering parameters
        :type filter_params: flask_restive.params.Params
        :param kwargs: options
        :return: count of found items
        :rtype: int
        """
        raise NotImplementedError

    def get_list(self, filter_params=None, slice_params=None,
                 sorting_params=None, **kwargs):
        """
        Get list of items by filter, can be sliced and sorted.
        Each of found item should be wrapped in Params class and
        should contain primary key.

        :param filter_params: filtering parameters
        :type filter_params: flask_restive.params.Params
        :param slice_params: slice (paging) parameters
        :type slice_params: flask_restive.params.SliceParams
        :param sorting_params: sorting parameters
        :type sorting_params: flask_restive.params.SortingParams
        :param kwargs: options
        :return: found items, list of flask_restive.params.Params
        :rtype: list
        """
        raise NotImplementedError

    def create_item(self, data_params, **kwargs):
        """
        Create one item. Data params should contain primary key.
        The created item should be wrapped in Params class and
        should contain primary key.

        :param data_params: item data
        :type data_params: flask_restive.params.Params
        :param kwargs: options
        :return: created item
        :rtype: flask_restive.params.Params
        """
        items = self.create_list(data_params=[data_params], **kwargs)
        assert len(items) == 1, 'Too many items to unpack.'
        return items[0]

    def create_list(self, data_params, **kwargs):
        """
        Create list of items. Each item should contain primary key.
        Each of created item should be wrapped in Params class and
        should contain primary key.

        :param data_params: items data to create,
            list of flask_restive.params.Params
        :type data_params: list
        :param kwargs: options
        :return: created items, list of flask_restive.params.Params
        :rtype: list
        """
        raise NotImplementedError

    def update_item(self, data_params, **kwargs):
        """
        Update one item. Data params should contain primary key.
        The rest of item parameters are values to update.
        The updated item should be wrapped in Params class and
        should contain primary key.

        :param data_params: item to update
        :type data_params: flask_restive.params.Params
        :param kwargs: options
        :return: updated item
        :rtype: flask_restive.params.Params
        """
        items = self.update_list(data_params=[data_params], **kwargs)
        assert len(items) == 1, 'Too many items to unpack.'
        return items[0]

    def update_list(self, data_params, **kwargs):
        """
        Update list of items. Each of items to update should contain
        primary key. The rest of item parameters are values to update.
        Each updated item should be wrapped in Params class and
        should contain primary key.

        :param data_params: items to update,
            list of flask_restive.params.Params
        :type data_params: list
        :param kwargs: options
        :return: updated items, list of flask_restive.params.Params
        :rtype: list
        """
        raise NotImplementedError

    def delete_list(self, filter_params=None, **kwargs):
        """
        Delete list of items by filter.

        :param filter_params: filtering parameters
        :type filter_params: flask_restive.params.Params
        :param kwargs: options
        """
        raise NotImplementedError
