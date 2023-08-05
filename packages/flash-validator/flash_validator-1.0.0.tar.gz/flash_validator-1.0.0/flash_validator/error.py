# /usr/bin/env python
# -*- coding:utf8 -*-


class ValidationError(ValueError):
    def __init__(self, rule, field):
        msg = rule.error_message % field
        super(ValidationError, self).__init__(msg)
