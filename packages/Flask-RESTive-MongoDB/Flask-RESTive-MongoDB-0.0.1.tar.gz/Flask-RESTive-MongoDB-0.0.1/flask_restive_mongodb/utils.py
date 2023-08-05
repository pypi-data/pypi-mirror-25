# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import Q


def make_connection_settings(app):
    """
    Use MONGODB_DATABASE_URI config attribute to set default connection
    credentials.

    To use replicaset write a few comma hosts with replicaSet parameter:
        mongodb://10.0.0.1:27017,10.0.0.2:27017/db?replicaSet=foo

    See also:
        http://api.mongodb.com/python/current/examples/high_availability.html
    """
    uri = app.config.get('MONGODB_DATABASE_URI', 'mongodb://localhost/local')
    settings = {'host': uri}
    return settings


def filter_multiple_keys(keys, values):
    """
    Make $and filter query for multiple keys.

    :param keys: list of keys
        Example: ['field1', 'field2']
    :param values: list of values for each key
        Example: [1, 2]
    :return: sub-query object
    :rtype: mongoengine.queryset.visitor.Q
    """
    values = list(values)
    query = Q()
    for i, key in enumerate(keys):
        query = query & Q(**{key: values[i]})
    return query


def filter_multiple_keys_multiple_values(keys, values_list):
    """
    Make $or filter query for list of
    multiple values of multiple keys.

    :param keys: list of keys
        Example: ['field1', 'field2']
    :param values: list of list of values for each key
        Example: [[1, 2], [3, 4], [5, 6]]
    :return: sub-query object
    :rtype: mongoengine.queryset.visitor.Q
    """
    query = Q()
    for values in values_list:
        query = query | filter_multiple_keys(keys, values)
    return query
