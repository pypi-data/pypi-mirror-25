# /usr/bin/env python
# -*- coding:utf8 -*-
try :
    from flask import request
except ImportError as e:
    print(e)

from ..source import BaseSource


class FlaskRequestSource(BaseSource):
    def __init__(self):
        try:
            self.request = request
        except Exception as e:
            raise e
        super(FlaskRequestSource, self).__init__()


class FlaskViewArgsSource(FlaskRequestSource):
    def find_field_value(self, field):
        return request.view_args.get(field)


class FlaskFormSource(FlaskRequestSource):
    def find_field_value(self, field):
        return request.form.get(field)


class FlaskQuerySource(FlaskRequestSource):
    def find_field_value(self, field):
        return request.args.get(field)


class FlaskJsonSource(FlaskRequestSource):
    def find_field_value(self, field):
        return request.get_json(force=True).get(field)