# -*- coding: UTF-8 -*-


import requests
from base import BaseProvider, MissingConfigParameter, ServerError


class FreeProvider(BaseProvider):
    """
    This is a provider class for the French telco 'Free'.

    >>> f = FreeProvider({'api_id': '12345678', 'api_key':'xyz'})
    >>> f.send('Hello, World!')
    True
    """

    def required_keys(self):
        return ['api_id', 'api_key']

    def send(self, msg):
        params = {
            'user': self.params['api_id'],
            'pass': self.params['api_key'],
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
