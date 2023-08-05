# coding=utf8

from __future__ import unicode_literals

from collections import namedtuple

Blog = namedtuple('Blog', 'title author post_time read_count')


class CatalogData():
    pass


class Series(object):
    pass


class DataSource(object):
    def __init__(self, opts):
        pass

    def create(self, dict_list):
        pass


def build():
    pass
