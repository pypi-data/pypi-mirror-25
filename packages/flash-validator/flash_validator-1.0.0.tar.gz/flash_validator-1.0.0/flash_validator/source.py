# /usr/bin/env python
# -*- coding:utf8 -*-


class BaseSource(object):
    def __init__(self, default_data = None):
        self.data = default_data

    def find_field_value(self, field):
        raise ValueError("write your own find_field_value func")


class DictSource(BaseSource):
    def __init__(self, default_data):
        super(DictSource, self).__init__(default_data)

    def find_field_value(self, field):
        return self.data.get(field, None)
