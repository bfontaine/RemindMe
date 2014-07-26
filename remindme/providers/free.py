# -*- coding: UTF-8 -*-


import requests
from base import BaseProvider, MissingConfigParameter, ServerError


class FreeProvider(BaseProvider):
    """
    This is a provider class for the French telco 'Free'.

    >>> f = FreeProvider({'user': '12345678', 'pass':'xyz'})
    >>> f.send('Hello, World!')
    True
    """

    def required_keys(self):
        return ['user', 'pass']

    def send(self, msg):
        params = {
            'user': self.params['user'],
            'pass': self.params['pass'],
            'msg': msg,
        }
        res = requests.get('https://smsapi.free-mobile.fr/sendmsg',
                params=params, verify=False)
        if res.status_code == 200:
            return True
        if res.status_code == 400:
            raise MissingConfigParameter()
        if res.status_code == 500:
            raise ServerError()
        return False
