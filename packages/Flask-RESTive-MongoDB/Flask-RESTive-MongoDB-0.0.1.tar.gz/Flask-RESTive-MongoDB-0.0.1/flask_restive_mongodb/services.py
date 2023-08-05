# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pymongo import UpdateOne
from mongoengine.connection import connect, disconnect
from mongoengine import Q
from flask_restive.services import Service as BaseService
from flask_restive.services import Storage as BaseStorage
from flask_restive import types
from flask_restive.params import SortingParams
from flask_restive.exceptions import DoesNotExist, AlreadyExists

from flask_restive_mongodb.models import Model
from flask_restive_mongodb.utils import (
    make_connection_settings, filter_multiple_keys_multiple_values)


class Service(BaseService):
    _config = None

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.connection = None

    @classmethod
    def _get_connection_config(cls):
        if cls._config is None:
            cls._config = make_connection_settings(cls.app)

    def _retrieve_connection_from_pool(self):
        self.connection = connect(**self._config)

    def _close_connection_and_return_to_pool(self):
        if self.connection is not None:
            del self.connection
            disconnect()

    def open(self):
        self._get_connection_config()
        self._retrieve_connection_from_pool()

    def close(self, exception=None):
        self._close_connection_and_return_to_pool()


class Storage(Service, BaseStorage):

    class Meta(object):
        model_cls = Model

    @property
    def model_cls(self):
        return self.opts.model_cls

    @property
    def collection(self):
        return self.model_cls.get_collection()

    def _make_query(self, params=None):
        query = self.model_cls.objects
        if params:
            for attr_name, attr_value in params.items():
                attr_query = self._make_attr_filter(attr_name, attr_value)
                if attr_query is not None:
                    query = query.filter(attr_query)
        return query

    @classmethod
    def _make_range_attr_filter(cls, attr_name, attr_value):
        query = Q()
        if attr_value.min is not None:
            query = query & Q(**{attr_name + '__gte': attr_value.min})
        if attr_value.max is not None:
            query = query & Q(**{attr_name + '__lte': attr_value.max})
        return query

    @classmethod
    def _make_list_attr_filter(cls, attr_name, attr_value):
        return Q(**{attr_name + '__in': attr_value})

    @classmethod
    def _make_const_attr_filter(cls, attr_name, attr_value):
        return Q(**{attr_name: attr_value})

    @classmethod
    def _make_attr_filter(cls, attr_name, attr_value):
        """
        Make sub-query object that depend from the filter value.

        :param attr_name: filter attribute name
        :param attr_value: filter attribute value
        :return: sub-query object
        :rtype: mongoengine.queryset.visitor.Q
        """
        if isinstance(attr_value, types.Range):
            query = cls._make_range_attr_filter(attr_name, attr_value)

        elif isinstance(attr_value, types.List):
            query = cls._make_list_attr_filter(attr_name, attr_value)

        else:
            query = cls._make_const_attr_filter(attr_name, attr_value)

        return query

    def _make_order_by(self, sorting_params=None):
        """
        When sorting params is not set
        the queryset will be sorted by primary key fields asc.
        """
        if not sorting_params:
            order_by = list(self.model_cls.primary_key_fields.keys())
            return order_by

        order_by = []
        for attr_name, sorting_order in sorting_params.sort_by.items():

            if sorting_order == SortingParams.SortingType.DESC:
                order_by.append('-' + attr_name)

            elif sorting_order == SortingParams.SortingType.ASC:
                order_by.append(attr_name)

        return order_by

    def _make_sorted_query(self, query, sorting_params=None):
        query = query.order_by(*self._make_order_by(sorting_params))
        return query

    @classmethod
    def _make_sliced_query(cls, query, slice_params=None):
        if slice_params:
            if slice_params.offset:
                query = query.skip(slice_params.offset)
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
        pk_attrs = self.model_cls.primary_key_fields.keys()
        pk_values = []

        for params in params_list:
            assert params.has_primary_key(), 'No primary key to find.'
            pk_values.append(params.primary_key.values())

        query = filter_multiple_keys_multiple_values(pk_attrs, pk_values)
        query = self.model_cls.objects.filter(query)
        return query

    def create_list(self, data_params, **kwargs):
        any_exists = bool(self._make_query_pk_in(data_params).count())
        if any_exists:
            raise AlreadyExists

        items = []
        for params in data_params:
            item = self.model_cls(**params)  # pylint: disable=not-callable
            items.append(item)

        bulk = self.collection.initialize_ordered_bulk_op()
        for item in items:
            item.validate()
            bulk.insert(item.to_mongo())
        bulk.execute()

        result = [self.wrap_data(item.to_dict()) for item in items]
        return result

    def update_list(self, data_params, **kwargs):
        query = self._make_query_pk_in(data_params)

        all_exist = query.count() == len(data_params)
        if not all_exist:
            raise DoesNotExist

        i = 0
        items = list(query.all())
        for params in data_params:
            item = items[i]
            item_params = item.to_dict()
            item_params.update(params)  # update fields
            item.set_attrs(**item_params)
            i += 1

        bulk_op = []
        for item in items:
            item.validate()
            item_data = item.to_mongo()
            bulk_op.append(
                UpdateOne({'_id': item_data['_id']},
                          {'$set': item_data.to_dict()})
            )
        self.collection.bulk_write(bulk_op, ordered=True)

        result = [self.wrap_data(item.to_dict()) for item in items]
        return result

    def delete_list(self, filter_params=None, **kwargs):
        query = self._make_query(filter_params)
        query.delete()
