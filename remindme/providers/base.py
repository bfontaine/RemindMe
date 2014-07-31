# -*- coding: UTF-8 -*-

class SMSException(Exception):
    pass


class MissingConfigParameter(SMSException):

    def __init__(self, key):
        msg = "Missing key: '%s'" % (key)
        super(SMSException, self).__init__(msg)


class ServerError(SMSException):
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
