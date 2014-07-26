# -*- coding: UTF-8 -*-


class MissingConfigParameter(Exception):
    pass


class ServerError(Exception):
    pass


class BaseProvider(object):

    def __init__(self, params={}):
        self.params = params
        for key in self.required_keys():
            if key not in self.params:
                raise MissingConfigParameter(key)

    def required_keys(self):
        return []

    def send(self, msg):
        return False
